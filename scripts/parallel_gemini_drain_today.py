#!/usr/bin/env python3
"""ONE-DAY ONLY — parallel enrichment drain with multiple Gemini API keys.

Does not change app code. Partitions the enrichment queue by job id so workers
do not claim the same rows. Stop job_ingestion before running so the built-in
worker does not compete for queue rows.

Usage (one worker per terminal):

  GEMINI_API_KEY="<key-1>" python scripts/parallel_gemini_drain_today.py --worker-id 0
  GEMINI_API_KEY="<key-2>" python scripts/parallel_gemini_drain_today.py --worker-id 1
  GEMINI_API_KEY="<key-3>" python scripts/parallel_gemini_drain_today.py --worker-id 2

Or launch all workers from one command (reads keys from env):

  export GEMINI_API_KEY_1="..."
  export GEMINI_API_KEY_2="..."
  export GEMINI_API_KEY_3="..."
  export GEMINI_API_KEY_4="..."
  python scripts/parallel_gemini_drain_today.py --launch-all

Keys are read from scripts/parallel_gemini_drain.env (copy from parallel_gemini_drain.env.example).
Shell exports still override file values. Override path with PARALLEL_GEMINI_ENV_FILE.
"""

from __future__ import annotations

import argparse
import asyncio
import os
import subprocess
import sys
import time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
JOB_INGESTION = ROOT / "job_ingestion"
sys.path.insert(0, str(JOB_INGESTION))
os.chdir(JOB_INGESTION)

from sqlalchemy import and_, or_, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings
from app.database import AsyncSessionLocal
from app.ingestion.enrichment_worker import (
    _build_work_items,
    _pack_batches,
    _process_batch,
    clear_quota_pause,
)
from app.models.enrichment_queue import EnrichmentQueue

DEFAULT_KEYS_ENV_FILE = ROOT / "scripts" / "parallel_gemini_drain.env"


def _parallel_keys_env_path() -> Path:
    override = os.environ.get("PARALLEL_GEMINI_ENV_FILE", "").strip()
    if override:
        return Path(override).expanduser()
    return DEFAULT_KEYS_ENV_FILE


def _parse_env_file(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    values: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        name, _, value = line.partition("=")
        values[name.strip()] = value.strip().strip('"').strip("'")
    return values


def _load_env_keys(worker_count: int) -> list[str | None]:
    file_values = _parse_env_file(_parallel_keys_env_path())
    keys: list[str | None] = [None] * worker_count
    keys[0] = (
        os.environ.get("GEMINI_API_KEY_1")
        or os.environ.get("GEMINI_API_KEY")
        or file_values.get("GEMINI_API_KEY_1")
        or file_values.get("GEMINI_API_KEY")
    )
    for index in range(1, worker_count):
        env_name = f"GEMINI_API_KEY_{index + 1}"
        keys[index] = os.environ.get(env_name) or file_values.get(env_name)
    return keys


def _partition_filter(worker_id: int, worker_count: int):
    return text(
        "mod(abs(hashtext(enrichment_queue.normalized_job_id::text)), :worker_count) = :worker_id"
    ).bindparams(worker_count=worker_count, worker_id=worker_id)


async def process_enrichment_window_partitioned(
    db: AsyncSession,
    *,
    settings: Settings,
    worker_id: int,
    worker_count: int,
) -> tuple[int, int]:
    """Same as enrichment_worker.process_enrichment_window but queue-partitioned."""
    from app.ingestion.enrichment_worker import _utcnow

    clear_quota_pause()
    now = _utcnow()
    partition = _partition_filter(worker_id, worker_count)
    eligible = and_(
        EnrichmentQueue.status.in_(["queued", "cooldown"]),
        or_(EnrichmentQueue.next_retry_at.is_(None), EnrichmentQueue.next_retry_at <= now),
        partition,
    )
    first_attempt_rows = (
        await db.scalars(
            select(EnrichmentQueue)
            .where(eligible, EnrichmentQueue.attempt_count == 0)
            .order_by(EnrichmentQueue.created_at.asc())
            .limit(settings.enrichment_max_jobs_per_window)
        )
    ).all()

    remaining_capacity = max(0, settings.enrichment_max_jobs_per_window - len(first_attempt_rows))
    retry_rows: list[EnrichmentQueue] = []
    if remaining_capacity > 0:
        retry_rows = (
            await db.scalars(
                select(EnrichmentQueue)
                .where(eligible, EnrichmentQueue.attempt_count > 0)
                .order_by(EnrichmentQueue.next_retry_at.asc(), EnrichmentQueue.updated_at.asc())
                .limit(remaining_capacity)
            )
        ).all()

    first_work = await _build_work_items(
        db=db, settings=settings, queue_rows=first_attempt_rows, priority_bucket="first_attempt"
    )
    retry_work = await _build_work_items(
        db=db, settings=settings, queue_rows=retry_rows, priority_bucket="retry"
    )
    candidates = first_work + retry_work
    if not candidates:
        await db.commit()
        return 0, 0

    batches, deferred = _pack_batches(settings=settings, items=candidates)
    for row in deferred:
        row.queue_row.status = "queued"
    if not batches:
        await db.commit()
        return 0, 0

    rpm_cap = max(settings.enrichment_llm_max_rpm, 1)
    batches = batches[: min(settings.enrichment_max_batches_per_window, rpm_cap)]
    processed_jobs = 0
    for idx, batch in enumerate(batches):
        if idx > 0:
            await asyncio.sleep(settings.enrichment_batch_interval_seconds)
        await _process_batch(
            db=db, settings=settings, batch_items=batch, source=f"parallel_worker_{worker_id}"
        )
        processed_jobs += len(batch)
        await db.commit()
    return processed_jobs, len(batches)


async def reset_stuck_queue_rows() -> int:
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            text(
                """
                UPDATE enrichment_queue eq
                SET status = 'queued',
                    attempt_count = 0,
                    next_retry_at = NULL,
                    last_error = NULL,
                    last_failure_reason = NULL
                FROM normalized_jobs nj
                JOIN raw_jobs rj ON rj.id = nj.raw_job_id
                WHERE eq.normalized_job_id = nj.id
                  AND eq.status IN ('failed', 'quota_blocked')
                  AND nj.is_active
                """
            )
        )
        await db.commit()
        return int(result.rowcount or 0)


async def count_queue() -> dict[str, int]:
    async with AsyncSessionLocal() as db:
        rows = (
            await db.execute(
                text(
                    """
                    SELECT status, COUNT(*)::int
                    FROM enrichment_queue
                    GROUP BY status
                    """
                )
            )
        ).all()
    return {str(status): int(count) for status, count in rows}


async def drain_loop(
    *,
    worker_id: int,
    worker_count: int,
    gemini_api_key: str,
    max_windows: int,
    idle_exit_rounds: int,
) -> int:
    import app.ingestion.enrichment_worker as enrichment_worker

    # Per-process: don't freeze this worker when the other key hits daily quota.
    enrichment_worker._pause_for_daily_quota = lambda _message: None  # noqa: SLF001
    clear_quota_pause()

    target_version = os.environ.get("EXTRACTION_VERSION", "v5")
    settings = Settings(
        gemini_api_key=gemini_api_key,
        extraction_version=target_version,
        enrichment_llm_max_rpm=int(os.environ.get("PARALLEL_ENRICHMENT_LLM_MAX_RPM", "10")),
    )
    processed = 0
    idle_rounds = 0
    print(f"[worker {worker_id}] started (partition {worker_id}/{worker_count})")
    for window_idx in range(max_windows):
        async with AsyncSessionLocal() as db:
            window_processed, batches = await process_enrichment_window_partitioned(
                db,
                settings=settings,
                worker_id=worker_id,
                worker_count=worker_count,
            )
        if window_processed == 0:
            idle_rounds += 1
            if idle_rounds >= idle_exit_rounds:
                print(f"[worker {worker_id}] idle exit after {idle_exit_rounds} empty windows")
                break
            await asyncio.sleep(2)
            continue
        idle_rounds = 0
        processed += window_processed
        print(
            f"[worker {worker_id}] window {window_idx + 1}: "
            f"+{window_processed} jobs ({batches} batches), total={processed}"
        )
        await asyncio.sleep(settings.enrichment_window_seconds)
    return processed


def _launch_all_processes(args: argparse.Namespace) -> int:
    keys = _load_env_keys(args.worker_count)
    missing = [index for index, key in enumerate(keys) if not key]
    if missing:
        names = ", ".join(f"GEMINI_API_KEY_{index + 1}" for index in missing)
        env_file = _parallel_keys_env_path()
        print(
            f"Missing API keys for worker(s) {missing}: set {names} in {env_file}.",
            file=sys.stderr,
        )
        return 1

    unique_keys = set(keys)
    if len(unique_keys) < len(keys):
        print("Warning: some API keys are identical — parallelism benefit is reduced.", file=sys.stderr)

    script = str(Path(__file__).resolve())
    base_cmd = [
        sys.executable,
        script,
        "--worker-count",
        str(args.worker_count),
        "--max-windows",
        str(args.max_windows),
        "--idle-exit-rounds",
        str(args.idle_exit_rounds),
    ]
    if args.reset_stuck:
        base_cmd.append("--reset-stuck")

    procs: list[subprocess.Popen[bytes]] = []
    log_dir = Path("/tmp/parallel_gemini_drain")
    log_dir.mkdir(parents=True, exist_ok=True)

    for worker_id, api_key in enumerate(keys):
        env = os.environ.copy()
        env["GEMINI_API_KEY"] = api_key
        log_path = log_dir / f"worker_{worker_id}.log"
        print(f"Launching worker {worker_id} -> {log_path}")
        with log_path.open("w", encoding="utf-8") as log_file:
            proc = subprocess.Popen(
                [*base_cmd, "--worker-id", str(worker_id)],
                env=env,
                stdout=log_file,
                stderr=subprocess.STDOUT,
                cwd=str(ROOT),
            )
        procs.append(proc)

    log_names = ", ".join(f"worker_{index}.log" for index in range(args.worker_count))
    print(f"Logs: {log_dir}/ ({log_names})")
    print("Stop job_ingestion first to avoid queue contention.")
    exit_code = 0
    try:
        while procs:
            for proc in list(procs):
                code = proc.poll()
                if code is None:
                    continue
                print(f"Worker exited with code {code}")
                procs.remove(proc)
                if code != 0:
                    exit_code = code
            if procs:
                time.sleep(5)
    except KeyboardInterrupt:
        print("Interrupt — terminating workers...")
        for proc in procs:
            proc.terminate()
        exit_code = 130
    return exit_code


async def _main_async(args: argparse.Namespace) -> int:
    if args.launch_all:
        return _launch_all_processes(args)

    if args.worker_id is None:
        print(f"Pass --worker-id 0..{args.worker_count - 1} or use --launch-all", file=sys.stderr)
        return 1

    if args.worker_id < 0 or args.worker_id >= args.worker_count:
        print(f"--worker-id must be between 0 and {args.worker_count - 1}", file=sys.stderr)
        return 1

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Set GEMINI_API_KEY for this worker process.", file=sys.stderr)
        return 1

    if args.reset_stuck:
        reset_count = await reset_stuck_queue_rows()
        print(f"Reset {reset_count} failed/quota_blocked queue rows")

    before = await count_queue()
    print(f"Queue before: {before}")

    processed = await drain_loop(
        worker_id=args.worker_id,
        worker_count=args.worker_count,
        gemini_api_key=api_key,
        max_windows=args.max_windows,
        idle_exit_rounds=args.idle_exit_rounds,
    )

    after = await count_queue()
    print(f"Worker {args.worker_id} processed {processed} jobs")
    print(f"Queue after: {after}")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description="One-day parallel Gemini enrichment drain")
    parser.add_argument("--worker-id", type=int, default=None, help="Partition id 0..N-1")
    parser.add_argument("--worker-count", type=int, default=4, help="Number of parallel workers")
    parser.add_argument("--max-windows", type=int, default=2000, help="Max enrichment windows per worker")
    parser.add_argument("--idle-exit-rounds", type=int, default=5, help="Stop after N consecutive empty windows")
    parser.add_argument("--reset-stuck", action="store_true", help="Re-queue failed/quota_blocked rows first")
    parser.add_argument(
        "--launch-all",
        action="store_true",
        help="Spawn N subprocesses (default 4) with GEMINI_API_KEY_1..N",
    )
    args = parser.parse_args()
    raise SystemExit(asyncio.run(_main_async(args)))


if __name__ == "__main__":
    main()
