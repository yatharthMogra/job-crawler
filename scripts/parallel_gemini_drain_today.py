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
  ...
  export GEMINI_API_KEY_7="..."
  python scripts/parallel_gemini_drain_today.py --launch-all

Probe all keys for daily quota (one minimal request per key):

  python scripts/parallel_gemini_drain_today.py --probe-keys

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
    _is_daily_quota_exhausted,
    _is_transient_rate_limit,
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


def _mask_key(api_key: str) -> str:
    if len(api_key) <= 8:
        return "***"
    return f"{api_key[:4]}...{api_key[-4:]}"


async def probe_api_keys(worker_count: int) -> int:
    """Send one minimal Gemini request per key to detect daily quota exhaustion."""
    keys = _load_env_keys(worker_count)
    missing = [index for index, key in enumerate(keys) if not key]
    if missing:
        names = ", ".join(f"GEMINI_API_KEY_{index + 1}" for index in missing)
        print(f"Missing API keys for worker(s) {missing}: set {names}", file=sys.stderr)
        return 1

    try:
        from google import genai
    except ImportError:
        print("google-genai is not installed.", file=sys.stderr)
        return 1

    settings = Settings()
    model = settings.gemini_model
    print(f"Probing {worker_count} keys (model={model}, one request each)...")
    print(f"{'Worker':<8} {'Key':<14} {'Status':<14} Detail")
    print("-" * 72)

    exit_code = 0
    for worker_id, api_key in enumerate(keys):
        assert api_key is not None
        client = genai.Client(api_key=api_key)
        status = "OK"
        detail = ""
        try:
            response = await client.aio.models.generate_content(
                model=model,
                contents="Reply with exactly: OK",
            )
            text = getattr(response, "text", None) or ""
            detail = f"response={text[:40]!r}"
        except Exception as exc:
            message = str(exc)
            if _is_daily_quota_exhausted(message):
                status = "DAILY_QUOTA"
                detail = message[:120]
                exit_code = 1
            elif _is_transient_rate_limit(message):
                status = "RATE_LIMIT"
                detail = message[:120]
            else:
                status = "ERROR"
                detail = message[:120]
                exit_code = 1

        print(f"{worker_id:<8} {_mask_key(api_key):<14} {status:<14} {detail}")

    if exit_code == 0:
        print("All keys passed probe — no daily quota exhaustion detected.")
    else:
        print("One or more keys failed probe — do not start drain until resolved.")
    return exit_code


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
                  AND nj.is_active
                  AND eq.status IN ('failed', 'quota_blocked', 'cooldown')
                """
            )
        )
        await db.commit()
        return int(result.rowcount or 0)


async def write_drain_summary() -> None:
    """Snapshot queue + v6 coverage to /tmp for monitoring."""
    summary_path = Path("/tmp/gemini_drain_summary.log")
    async with AsyncSessionLocal() as db:
        queue = await count_queue()
        row = (
            await db.execute(
                text(
                    """
                    SELECT
                      COUNT(*) FILTER (WHERE is_active) AS active,
                      COUNT(*) FILTER (WHERE is_active AND extraction_version = 'v6') AS v6,
                      COUNT(*) FILTER (WHERE is_active AND role_intent IS NOT NULL) AS role_intent
                    FROM normalized_jobs
                    """
                )
            )
        ).one()
    ts = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())
    line = (
        f"[{ts}] queue={queue} v6={row.v6}/{row.active} "
        f"({100 * row.v6 / row.active:.1f}%) role_intent={row.role_intent}\n"
    )
    with summary_path.open("a", encoding="utf-8") as handle:
        handle.write(line)
        handle.flush()


def write_drain_summary_sync() -> None:
    """No-op in parent; workers call write_drain_summary per window."""


def _append_worker_progress(worker_id: int, message: str) -> None:
    log_dir = Path("/tmp/parallel_gemini_drain")
    log_dir.mkdir(parents=True, exist_ok=True)
    path = log_dir / f"progress_worker_{worker_id}.log"
    ts = time.strftime("%H:%M:%S", time.gmtime())
    with path.open("a", encoding="utf-8") as handle:
        handle.write(f"[{ts}] {message}\n")
        handle.flush()


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


def _baseline_drain_settings(gemini_api_key: str) -> Settings:
    """Conservative defaults matching job_ingestion config (pre-pilot baseline)."""
    return Settings(
        gemini_api_key=gemini_api_key,
        extraction_version=os.environ.get("EXTRACTION_VERSION", "v6"),
        enrichment_llm_max_rpm=int(os.environ.get("PARALLEL_ENRICHMENT_LLM_MAX_RPM", "10")),
        enrichment_stop_on_daily_quota=False,
    )


def _greedy_pilot_settings(gemini_api_key: str, *, micro_batch_size: int, batches_per_window: int) -> Settings:
    """Aggressive single-worker tuning — pilot only."""
    return Settings(
        gemini_api_key=gemini_api_key,
        extraction_version=os.environ.get("EXTRACTION_VERSION", "v6"),
        enrichment_micro_batch_size=micro_batch_size,
        enrichment_max_input_tokens_per_batch=int(
            os.environ.get("PILOT_MAX_INPUT_TOKENS_PER_BATCH", "24000")
        ),
        enrichment_window_token_budget=int(os.environ.get("PILOT_WINDOW_TOKEN_BUDGET", "245000")),
        enrichment_llm_max_rpm=int(os.environ.get("PILOT_LLM_MAX_RPM", "14")),
        enrichment_max_batches_per_window=batches_per_window,
        enrichment_max_jobs_per_window=micro_batch_size * batches_per_window,
        enrichment_window_seconds=int(os.environ.get("PILOT_WINDOW_SECONDS", "30")),
        enrichment_stop_on_daily_quota=False,
    )


async def _fetch_latest_batch_stats(db: AsyncSession, source: str) -> dict | None:
    row = (
        await db.execute(
            text(
                """
                SELECT jobs_total, status, failure_reason,
                       actual_input_tokens, actual_output_tokens, latency_ms
                FROM enrichment_batches
                WHERE source = :source
                ORDER BY started_at DESC
                LIMIT 1
                """
            ),
            {"source": source},
        )
    ).one_or_none()
    if row is None:
        return None
    total = int(row.actual_input_tokens or 0) + int(row.actual_output_tokens or 0)
    return {
        "jobs": int(row.jobs_total),
        "status": str(row.status),
        "failure_reason": row.failure_reason,
        "input_tokens": int(row.actual_input_tokens or 0),
        "output_tokens": int(row.actual_output_tokens or 0),
        "total_tokens": total,
        "latency_ms": int(row.latency_ms or 0),
    }


async def _prior_pilot_summary(db: AsyncSession, source: str) -> dict[int, dict]:
    rows = (
        await db.execute(
            text(
                """
                SELECT jobs_total,
                  COUNT(*)::int AS runs,
                  COUNT(*) FILTER (WHERE status = 'completed')::int AS ok,
                  ROUND(AVG(actual_input_tokens + actual_output_tokens))::int AS avg_tokens,
                  MAX(actual_input_tokens + actual_output_tokens)::int AS max_tokens
                FROM enrichment_batches
                WHERE source = :source
                  AND started_at > NOW() - INTERVAL '24 hours'
                GROUP BY jobs_total
                ORDER BY jobs_total DESC
                """
            ),
            {"source": source},
        )
    ).all()
    return {
        int(row.jobs_total): {
            "runs": int(row.runs),
            "ok": int(row.ok),
            "avg_tokens": int(row.avg_tokens or 0),
            "max_tokens": int(row.max_tokens or 0),
        }
        for row in rows
    }


async def pilot_sweep(
    *,
    gemini_api_key: str,
    batch_sizes: list[int],
    batches_per_size: int,
    throughput_windows: int,
    skip_sweep: bool = False,
    best_size_override: int | None = None,
) -> int:
    """Empirical batch-size sweep on worker 0, then a greedy throughput burst."""
    import app.ingestion.enrichment_worker as enrichment_worker

    enrichment_worker._pause_for_daily_quota = lambda _message: None  # noqa: SLF001
    clear_quota_pause()

    worker_id = 0
    worker_count = 1
    source = "parallel_worker_0"
    exit_code = 0
    size_results: dict[int, list[dict]] = {}
    best_size = best_size_override or (batch_sizes[0] if batch_sizes else 12)

    if skip_sweep:
        async with AsyncSessionLocal() as db:
            prior = await _prior_pilot_summary(db, source)
        print("=== PILOT RESUME: skipping phase 1 (prior sweep results) ===")
        for size, stats in sorted(prior.items(), reverse=True):
            print(
                f"  size={size}: {stats['ok']}/{stats['runs']} ok, "
                f"avg_tokens={stats['avg_tokens']}, max_tokens={stats['max_tokens']}"
            )
        if best_size_override is None and prior:
            best_size = max(
                prior.keys(),
                key=lambda size: (prior[size]["ok"] / max(prior[size]["runs"], 1)) * size,
            )
        print(f"  using best_size={best_size} for phase 2")
    else:
        print("=== PILOT PHASE 1: batch size sweep (1 batch per window) ===")
        print(f"Sizes: {batch_sizes}, {batches_per_size} batches each, RPM cap=14")
    for size in ([] if skip_sweep else batch_sizes):
        settings = _greedy_pilot_settings(gemini_api_key, micro_batch_size=size, batches_per_window=1)
        size_results[size] = []
        print(f"\n--- testing micro_batch_size={size} ---")
        for attempt in range(batches_per_size):
            async with AsyncSessionLocal() as db:
                processed, batch_count = await process_enrichment_window_partitioned(
                    db,
                    settings=settings,
                    worker_id=worker_id,
                    worker_count=worker_count,
                )
                stats = await _fetch_latest_batch_stats(db, source=source)
            if processed == 0 or not stats:
                print(f"  batch {attempt + 1}: no work left")
                break
            stats["attempt"] = attempt + 1
            size_results[size].append(stats)
            flag = ""
            if stats["failure_reason"] == "token_limit_exceeded":
                flag = " TOKEN_LIMIT"
                exit_code = 1
            elif stats["status"] != "completed":
                flag = f" {stats['status']}/{stats['failure_reason']}"
            print(
                f"  batch {attempt + 1}: jobs={stats['jobs']} "
                f"tokens={stats['total_tokens']} (in={stats['input_tokens']} out={stats['output_tokens']}) "
                f"latency={stats['latency_ms']}ms{flag}"
            )
            if stats["failure_reason"] == "token_limit_exceeded":
                print(f"  stopping size {size} early after token_limit_exceeded")
                break
            await asyncio.sleep(settings.enrichment_batch_interval_seconds)

    if not skip_sweep:
        print("\n=== PILOT PHASE 1 SUMMARY ===")
        best_score = -1.0
        for size, runs in size_results.items():
            if not runs:
                print(f"  size={size}: no runs")
                continue
            ok = sum(1 for row in runs if row["status"] == "completed")
            avg_jobs = sum(row["jobs"] for row in runs) / len(runs)
            avg_tokens = sum(row["total_tokens"] for row in runs) / len(runs)
            max_tokens = max(row["total_tokens"] for row in runs)
            success_rate = ok / len(runs)
            score = success_rate * avg_jobs
            print(
                f"  size={size}: {ok}/{len(runs)} ok, avg_jobs={avg_jobs:.1f}, "
                f"avg_tokens={avg_tokens:.0f}, max_tokens={max_tokens}, score={score:.2f}"
            )
            if success_rate >= 0.8 and score > best_score:
                best_score = score
                best_size = size

    print(f"\n=== PILOT PHASE 2: throughput @ size={best_size} ({throughput_windows} windows) ===")
    burst_settings = _greedy_pilot_settings(
        gemini_api_key,
        micro_batch_size=best_size,
        batches_per_window=int(os.environ.get("PILOT_BURST_BATCHES_PER_WINDOW", "12")),
    )
    burst_jobs = 0
    burst_batches = 0
    burst_failures = 0
    for window_idx in range(throughput_windows):
        async with AsyncSessionLocal() as db:
            processed, batches = await process_enrichment_window_partitioned(
                db,
                settings=burst_settings,
                worker_id=worker_id,
                worker_count=worker_count,
            )
        if processed == 0:
            print(f"  window {window_idx + 1}: idle")
            break
        burst_jobs += processed
        burst_batches += batches
        print(f"  window {window_idx + 1}: +{processed} jobs in {batches} batches (total={burst_jobs})")
        await asyncio.sleep(burst_settings.enrichment_window_seconds)

    async with AsyncSessionLocal() as db:
        recent = (
            await db.execute(
                text(
                    """
                    SELECT failure_reason, COUNT(*)::int
                    FROM enrichment_batches
                    WHERE source = :source
                      AND started_at > NOW() - INTERVAL '2 hours'
                    GROUP BY failure_reason
                    """
                ),
                {"source": source},
            )
        ).all()
    for reason, count in recent:
        if reason:
            burst_failures += count

    print("\n=== PILOT RECOMMENDATION ===")
    print(f"  optimal_micro_batch_size: {best_size}")
    print(f"  burst: {burst_jobs} jobs / {burst_batches} batches in phase 2")
    print(f"  phase2 failures: {burst_failures}")
    print(
        f"  suggested drain env: ENRICHMENT_MICRO_BATCH_SIZE={best_size} "
        f"PILOT_BURST_BATCHES_PER_WINDOW={burst_settings.enrichment_max_batches_per_window} "
        f"PARALLEL_ENRICHMENT_LLM_MAX_RPM=14"
    )
    return exit_code


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

    target_version = os.environ.get("EXTRACTION_VERSION", "v6")
    settings = _baseline_drain_settings(gemini_api_key)
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
        progress_msg = (
            f"window {window_idx + 1}: +{window_processed} jobs ({batches} batches), total={processed}"
        )
        print(f"[worker {worker_id}] {progress_msg}")
        _append_worker_progress(worker_id, progress_msg)
        await write_drain_summary()
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
        env["PYTHONUNBUFFERED"] = "1"
        log_path = log_dir / f"worker_{worker_id}.log"
        print(f"Launching worker {worker_id} -> {log_path}")
        with log_path.open("w", encoding="utf-8") as log_file:
            proc = subprocess.Popen(
                [sys.executable, "-u", *base_cmd[1:], "--worker-id", str(worker_id)],
                env=env,
                stdout=log_file,
                stderr=subprocess.STDOUT,
                cwd=str(ROOT),
            )
        procs.append(proc)

    log_names = ", ".join(f"worker_{index}.log" for index in range(args.worker_count))
    print(f"Logs: {log_dir}/ ({log_names})")
    print("Progress: /tmp/gemini_drain_summary.log + /tmp/parallel_gemini_drain/progress_worker_*.log")
    print("Stop job_ingestion first to avoid queue contention.")
    exit_code = 0
    try:
        while procs:
            write_drain_summary_sync()
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
    if args.probe_keys:
        return await probe_api_keys(args.worker_count)

    if args.launch_all:
        return _launch_all_processes(args)

    if args.pilot:
        args.worker_id = 0
        args.worker_count = 1

    if args.worker_id is None:
        print(f"Pass --worker-id 0..{args.worker_count - 1} or use --launch-all", file=sys.stderr)
        return 1

    if args.worker_id < 0 or args.worker_id >= args.worker_count:
        print(f"--worker-id must be between 0 and {args.worker_count - 1}", file=sys.stderr)
        return 1

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key and args.pilot:
        file_values = _parse_env_file(_parallel_keys_env_path())
        api_key = file_values.get("GEMINI_API_KEY_1") or file_values.get("GEMINI_API_KEY")
    if not api_key:
        print("Set GEMINI_API_KEY for this worker process.", file=sys.stderr)
        return 1

    if args.reset_stuck or args.pilot:
        reset_count = await reset_stuck_queue_rows()
        print(f"Reset {reset_count} failed/quota_blocked queue rows")

    before = await count_queue()
    print(f"Queue before: {before}")

    if args.pilot:
        sizes = [int(part.strip()) for part in args.pilot_sizes.split(",") if part.strip()]
        return await pilot_sweep(
            gemini_api_key=api_key,
            batch_sizes=sizes,
            batches_per_size=args.pilot_batches_per_size,
            throughput_windows=args.pilot_throughput_windows,
            skip_sweep=args.pilot_resume,
            best_size_override=args.pilot_best_size,
        )

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
    parser.add_argument("--worker-count", type=int, default=7, help="Number of parallel workers")
    parser.add_argument("--max-windows", type=int, default=2000, help="Max enrichment windows per worker")
    parser.add_argument("--idle-exit-rounds", type=int, default=5, help="Stop after N consecutive empty windows")
    parser.add_argument("--reset-stuck", action="store_true", help="Re-queue failed/quota_blocked rows first")
    parser.add_argument(
        "--probe-keys",
        action="store_true",
        help="Send one minimal request per GEMINI_API_KEY_N to check daily quota",
    )
    parser.add_argument(
        "--launch-all",
        action="store_true",
        help="Spawn N subprocesses with GEMINI_API_KEY_1..N",
    )
    parser.add_argument(
        "--pilot",
        action="store_true",
        help="Greedy single-worker batch-size sweep (worker 0, worker-count=1)",
    )
    parser.add_argument(
        "--pilot-sizes",
        default="12,11,10,9,8",
        help="Comma-separated micro_batch sizes to test (greedy order)",
    )
    parser.add_argument(
        "--pilot-batches-per-size",
        type=int,
        default=5,
        help="API batches to run per size in pilot phase 1",
    )
    parser.add_argument(
        "--pilot-throughput-windows",
        type=int,
        default=8,
        help="Greedy throughput windows at winning batch size",
    )
    parser.add_argument(
        "--pilot-resume",
        action="store_true",
        help="Skip phase 1 sweep; run phase 2 throughput at --pilot-best-size",
    )
    parser.add_argument(
        "--pilot-best-size",
        type=int,
        default=None,
        help="Batch size for phase 2 (default: 12 on resume, or sweep winner)",
    )
    args = parser.parse_args()
    raise SystemExit(asyncio.run(_main_async(args)))


if __name__ == "__main__":
    main()
