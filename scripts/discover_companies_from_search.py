#!/usr/bin/env python3
"""Discover companies from web search and/or CSV job links for companies.json.

Examples:
  # Dry-run CSV discovery (no API keys required)
  python scripts/discover_companies_from_search.py --from-csv newgrad_apply_links.csv --dry-run

  # Search via SerpAPI or Google Custom Search, validate boards, write candidates
  python scripts/discover_companies_from_search.py --dry-run

  # Merge validated candidates into job_ingestion/data/companies.json
  python scripts/discover_companies_from_search.py --from-csv newgrad_apply_links.csv --merge

Environment (search mode only):
  SERPAPI_API_KEY
  GOOGLE_CSE_API_KEY + GOOGLE_CSE_CX
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from company_discovery import (  # noqa: E402
    DEFAULT_COMPANIES_JSON,
    DEFAULT_OUTPUT,
    DEFAULT_SEARCH_QUERIES,
    WORKDAY_SEARCH_QUERIES,
    build_search_provider,
    collect_candidates_from_csv,
    discover_from_common_crawl,
    discover_from_search,
    load_existing_tokens,
    load_queries_from_file,
    merge_candidates_into_json,
    validate_candidates,
    write_candidates_report,
)


async def run(args: argparse.Namespace) -> dict:
    existing_tokens = load_existing_tokens(args.companies_json)
    result = None

    if args.from_common_crawl:
        result = await discover_from_common_crawl(
            existing_tokens=existing_tokens,
            index_count=args.cc_index_count,
            max_pages_per_pattern=args.cc_max_pages,
            page_size=args.cc_page_size,
            page_delay_s=args.cc_page_delay_s,
            max_retries=args.cc_max_retries,
            retry_base_s=args.cc_retry_base_s,
            log=print if args.verbose else None,
        )
    elif args.from_csv:
        result = collect_candidates_from_csv(args.from_csv, existing_tokens=existing_tokens)
    else:
        queries = DEFAULT_SEARCH_QUERIES.copy()
        if args.include_workday:
            queries.extend(WORKDAY_SEARCH_QUERIES)
        if args.queries_file:
            queries = load_queries_from_file(args.queries_file)
        provider = build_search_provider()
        result = await discover_from_search(
            provider,
            queries,
            existing_tokens=existing_tokens,
            max_results_per_query=args.max_results_per_query,
            query_delay_s=args.query_delay_s,
        )

    if args.validate and result.candidates:
        await validate_candidates(result.candidates, concurrency=args.validate_concurrency)

    write_candidates_report(args.output, result)

    from collections import Counter

    platform_counts = Counter(c.platform for c in result.candidates)
    validation_counts = Counter(c.validation_status for c in result.candidates)

    summary: dict = {
        "mode": (
            "common_crawl"
            if args.from_common_crawl
            else ("csv" if args.from_csv else "search")
        ),
        "candidate_count": len(result.candidates),
        "skipped_existing_count": len(result.skipped_existing),
        "skipped_unsupported_count": len(result.skipped_unsupported),
        "search_queries_run": result.search_queries_run,
        "cdx_indexes_scanned": result.cdx_indexes_scanned,
        "cdx_pages_fetched": result.cdx_pages_fetched,
        "cdx_page_failures": result.cdx_page_failures,
        "unique_tokens_seen": result.unique_tokens_seen,
        "urls_collected": result.urls_collected,
        "output": str(args.output),
        "validation": {
            status: validation_counts.get(status, 0)
            for status in sorted(validation_counts or {"none"})
        },
        "candidates_by_platform": dict(platform_counts.most_common()),
    }

    if args.merge:
        summary["merge"] = merge_candidates_into_json(
            result.candidates,
            args.companies_json,
            only_valid=not args.merge_unvalidated,
            dry_run=args.dry_run,
        )

    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--from-csv",
        type=Path,
        help="Discover from a CSV with company + apply_link/job link columns (no search API needed)",
    )
    parser.add_argument(
        "--from-common-crawl",
        action="store_true",
        help="Enumerate ATS board tokens from Common Crawl CDX (no search API needed)",
    )
    parser.add_argument(
        "--cc-index-count",
        type=int,
        default=6,
        help="Number of recent Common Crawl indexes to scan (default: 6)",
    )
    parser.add_argument(
        "--cc-max-pages",
        type=int,
        default=200,
        help="Max CDX pages per URL pattern per index (default: 200)",
    )
    parser.add_argument(
        "--cc-page-size",
        type=int,
        default=2000,
        help="CDX results per page (default: 2000)",
    )
    parser.add_argument(
        "--cc-page-delay-s",
        type=float,
        default=0.25,
        help="Delay between CDX page requests (default: 0.25)",
    )
    parser.add_argument(
        "--cc-max-retries",
        type=int,
        default=6,
        help="Max retries per CDX request on 429/5xx or connection errors (default: 6)",
    )
    parser.add_argument(
        "--cc-retry-base-s",
        type=float,
        default=2.0,
        help="Base delay seconds for CDX exponential backoff (default: 2.0)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Log CDX progress to stderr",
    )
    parser.add_argument(
        "--companies-json",
        type=Path,
        default=DEFAULT_COMPANIES_JSON,
        help=f"Path to companies.json (default: {DEFAULT_COMPANIES_JSON})",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"Write candidate report JSON here (default: {DEFAULT_OUTPUT})",
    )
    parser.add_argument(
        "--queries-file",
        type=Path,
        help="Optional text file with one Google search query per line",
    )
    parser.add_argument(
        "--include-workday",
        action="store_true",
        help="Add Workday site: queries (search mode only)",
    )
    parser.add_argument(
        "--max-results-per-query",
        type=int,
        default=50,
        help="Max search results to fetch per query (default: 50)",
    )
    parser.add_argument(
        "--query-delay-s",
        type=float,
        default=1.0,
        help="Delay between search API calls (default: 1.0)",
    )
    parser.add_argument(
        "--validate",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Probe ATS APIs to confirm board tokens (default: on)",
    )
    parser.add_argument(
        "--validate-concurrency",
        type=int,
        default=6,
        help="Concurrent board validation requests (default: 6)",
    )
    parser.add_argument(
        "--merge",
        action="store_true",
        help="Append validated candidates to companies.json",
    )
    parser.add_argument(
        "--merge-unvalidated",
        action="store_true",
        help="With --merge, include candidates that failed validation",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Do not write companies.json even with --merge",
    )
    args = parser.parse_args()

    if sum(bool(x) for x in (args.from_csv, args.from_common_crawl)) > 1:
        parser.error("Use only one of --from-csv or --from-common-crawl")

    if not args.from_csv and not args.from_common_crawl:
        try:
            build_search_provider()
        except RuntimeError as exc:
            parser.error(
                f"{exc} Use --from-csv for offline discovery, or set search API env vars."
            )

    summary = asyncio.run(run(args))
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
