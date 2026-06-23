"""Discover job-board companies from web search results and CSV job links."""

from __future__ import annotations

import asyncio
import csv
import json
import os
import re
import sys
from collections.abc import Iterable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Protocol
from urllib.parse import parse_qs, urlparse

import httpx

SCRIPTS_DIR = Path(__file__).resolve().parent
ROOT = SCRIPTS_DIR.parent
DEFAULT_COMPANIES_JSON = ROOT / "job_ingestion" / "data" / "companies.json"
DEFAULT_OUTPUT = ROOT / "exports" / "discovered_companies_candidates.json"

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import merge_companies_from_csv as mcc  # noqa: E402

ATS_URL_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    (
        "greenhouse",
        re.compile(
            r"https?://(?:boards|job-boards)\.greenhouse\.io/[^/\s\"'?]+(?:/jobs/\d+)?",
            re.IGNORECASE,
        ),
    ),
    (
        "lever",
        re.compile(r"https?://jobs\.lever\.co/[^/\s\"'?]+(?:/[0-9a-f-]{36})?", re.IGNORECASE),
    ),
    (
        "ashby",
        re.compile(r"https?://jobs\.ashbyhq\.com/[^/\s\"'?]+", re.IGNORECASE),
    ),
    (
        "workday",
        re.compile(r"https?://[\w-]+\.wd\d+\.myworkdayjobs\.com/[^\s\"']+", re.IGNORECASE),
    ),
]

DEFAULT_SEARCH_QUERIES: list[str] = [
    (
        '(site:boards.greenhouse.io OR site:job-boards.greenhouse.io) '
        '("software engineer intern" OR "new grad software engineer" OR "early career software engineer")'
    ),
    (
        'site:jobs.lever.co '
        '("software engineer intern" OR "new grad software engineer" OR "early career software engineer")'
    ),
    (
        'site:jobs.ashbyhq.com '
        '("software engineer intern" OR "new grad software engineer" OR "early career software engineer")'
    ),
    (
        '(site:boards.greenhouse.io OR site:job-boards.greenhouse.io) '
        '("associate software engineer" OR "software engineer I" OR "entry level software engineer")'
    ),
    'site:jobs.lever.co ("associate software engineer" OR "software engineer I")',
    'site:jobs.ashbyhq.com ("software engineer new grad" OR "new grad software")',
]

WORKDAY_SEARCH_QUERIES: list[str] = [
    (
        'site:myworkdayjobs.com '
        '("software engineer intern" OR "new grad software engineer" OR "early career software engineer")'
    ),
]

ASHBY_LIST_QUERY = """
query ApiJobBoardWithTeams($organizationHostedJobsPageName: String!) {
  jobBoard: jobBoardWithTeams(
    organizationHostedJobsPageName: $organizationHostedJobsPageName
  ) {
    jobPostings { id }
  }
}
""".strip()

SKIP_BOARD_TOKENS = frozenset({
    "embed",
    "job_app",
    "jobs",
    "job",
    "api",
    "login",
    "signin",
    "cdn",
    "static",
    "assets",
    "www",
})

CDX_RETRYABLE_STATUS = frozenset({429, 500, 502, 503, 504})
CDX_DEFAULT_MAX_RETRIES = 6
CDX_DEFAULT_RETRY_BASE_S = 2.0
COMMON_CRAWL_COLLINFO_URL = "https://index.commoncrawl.org/collinfo.json"

# CDX url patterns — wildcards per Common Crawl index API
COMMON_CRAWL_URL_PATTERNS: list[str] = [
    "boards.greenhouse.io/*",
    "job-boards.greenhouse.io/*",
    "jobs.lever.co/*",
    "jobs.ashbyhq.com/*",
    "jobs.ashby.com/*",
    "jobs.smartrecruiters.com/*",
    "*.myworkdayjobs.com/*",
    "*.oraclecloud.com/hcmUI/*",
    "*.icims.com/jobs/*",
    "apply.workable.com/*",
    "*.bamboohr.com/careers/*",
    "ats.rippling.com/*",
    "*/api/apply/v2/jobs*",
]

# Backwards-compatible alias
COMMON_CRAWL_PATTERNS = COMMON_CRAWL_URL_PATTERNS

UUID_RE = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
    re.IGNORECASE,
)


@dataclass
class DiscoveredCandidate:
    company: str
    platform: str
    board_token: str
    source_url: str
    fetch_tier: int = 2
    platform_config: dict[str, Any] | None = None
    validation_status: str = "pending"
    validation_detail: str | None = None

    def to_json_entry(self, *, is_active: bool = True) -> dict[str, Any]:
        entry: dict[str, Any] = {
            "company": self.company,
            "platform": self.platform,
            "board_token": self.board_token,
            "fetch_tier": self.fetch_tier,
            "is_active": is_active,
            "source_url": self.source_url,
            "validation_status": self.validation_status,
        }
        if self.platform_config:
            entry["platform_config"] = self.platform_config
        if self.validation_detail:
            entry["validation_detail"] = self.validation_detail
        return entry


@dataclass
class DiscoveryResult:
    candidates: list[DiscoveredCandidate] = field(default_factory=list)
    skipped_existing: list[str] = field(default_factory=list)
    skipped_unsupported: list[str] = field(default_factory=list)
    search_queries_run: int = 0
    urls_collected: int = 0
    cdx_indexes_scanned: int = 0
    cdx_pages_fetched: int = 0
    cdx_page_failures: int = 0
    unique_tokens_seen: int = 0


class SearchProvider(Protocol):
    async def search(self, query: str, *, max_results: int) -> list[dict[str, str]]: ...


@dataclass
class GoogleCseProvider:
    api_key: str
    cx: str
    results_per_page: int = 10

    async def search(self, query: str, *, max_results: int) -> list[dict[str, str]]:
        collected: list[dict[str, str]] = []
        start = 1
        async with httpx.AsyncClient(timeout=30.0) as client:
            while len(collected) < max_results:
                params = {
                    "key": self.api_key,
                    "cx": self.cx,
                    "q": query,
                    "start": start,
                    "num": min(self.results_per_page, max_results - len(collected)),
                }
                response = await client.get(
                    "https://www.googleapis.com/customsearch/v1",
                    params=params,
                )
                response.raise_for_status()
                payload = response.json()
                items = payload.get("items") or []
                if not items:
                    break
                for item in items:
                    if not isinstance(item, dict):
                        continue
                    collected.append(
                        {
                            "link": str(item.get("link") or ""),
                            "title": str(item.get("title") or ""),
                            "snippet": str(item.get("snippet") or ""),
                        }
                    )
                if len(items) < self.results_per_page:
                    break
                start += self.results_per_page
                if start > 91:
                    break
                await asyncio.sleep(0.4)
        return collected[:max_results]


@dataclass
class SerpApiProvider:
    api_key: str

    async def search(self, query: str, *, max_results: int) -> list[dict[str, str]]:
        collected: list[dict[str, str]] = []
        start = 0
        async with httpx.AsyncClient(timeout=60.0) as client:
            while len(collected) < max_results:
                params = {
                    "engine": "google",
                    "q": query,
                    "api_key": self.api_key,
                    "start": start,
                    "num": min(10, max_results - len(collected)),
                }
                response = await client.get("https://serpapi.com/search.json", params=params)
                response.raise_for_status()
                payload = response.json()
                items = payload.get("organic_results") or []
                if not items:
                    break
                for item in items:
                    if not isinstance(item, dict):
                        continue
                    collected.append(
                        {
                            "link": str(item.get("link") or ""),
                            "title": str(item.get("title") or ""),
                            "snippet": str(item.get("snippet") or ""),
                        }
                    )
                if len(items) < 10:
                    break
                start += 10
                if start >= 100:
                    break
                await asyncio.sleep(0.5)
        return collected[:max_results]


def load_existing_tokens(companies_path: Path) -> set[str]:
    if not companies_path.exists():
        return set()
    payload = json.loads(companies_path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        return set()
    return {
        str(item["board_token"]).lower()
        for item in payload
        if isinstance(item, dict) and item.get("board_token")
    }


def extract_urls_from_search_hit(hit: dict[str, str]) -> list[str]:
    urls: list[str] = []
    for key in ("link", "title", "snippet"):
        text = hit.get(key) or ""
        urls.extend(extract_ats_urls(text))
    link = (hit.get("link") or "").strip()
    if link and link not in urls:
        urls.append(link)
    return urls


def extract_ats_urls(text: str) -> list[str]:
    found: list[str] = []
    seen: set[str] = set()
    for _, pattern in ATS_URL_PATTERNS:
        for match in pattern.finditer(text):
            url = match.group(0).rstrip(").,;\"'")
            if url not in seen:
                seen.add(url)
                found.append(url)
    return found


def _company_name_from_token(board_token: str) -> str:
    return board_token.replace("-", " ").replace("_", " ").title()


def _company_name_from_url(url: str, board_token: str) -> str:
    parsed = urlparse(url)
    host = parsed.netloc.lower().replace("www.", "")
    if host and host not in {
        "boards.greenhouse.io",
        "job-boards.greenhouse.io",
        "jobs.lever.co",
        "jobs.ashbyhq.com",
    }:
        slug = host.split(".")[0]
        if slug not in {"boards", "job-boards", "jobs", "careers"}:
            return slug.replace("-", " ").title()
    return _company_name_from_token(board_token)


def parse_eightfold_from_url(url: str) -> dict[str, Any] | None:
    parsed = urlparse(url)
    if "/api/apply/v2/jobs" not in parsed.path:
        return None
    domain_vals = parse_qs(parsed.query).get("domain") or []
    if not domain_vals or not str(domain_vals[0]).strip():
        return None
    domain = str(domain_vals[0]).strip()
    api_host = parsed.netloc.lower().replace("www.", "")
    if not api_host:
        return None
    root = domain.split(".")[0].lower()
    board_token = root if root and root not in SKIP_BOARD_TOKENS else domain.replace(".", "-").lower()
    return {
        "platform": "eightfold",
        "board_token": board_token[:120],
        "fetch_tier": 2,
        "platform_config": {"api_host": api_host, "domain": domain},
    }


def parse_url_to_candidate(url: str, *, company_hint: str = "") -> DiscoveredCandidate | None:
    eightfold = parse_eightfold_from_url(url)
    if eightfold is not None:
        token = str(eightfold["board_token"]).lower()
        display_name = mcc.clean_display_name(company_hint) if company_hint else _company_name_from_token(token)
        return DiscoveredCandidate(
            company=display_name or _company_name_from_token(token),
            platform="eightfold",
            board_token=token,
            source_url=url,
            fetch_tier=2,
            platform_config=eightfold.get("platform_config"),
        )

    name = company_hint.strip() or _company_name_from_url(url, "")
    parsed = mcc.parse_entry(name or "unknown", url)
    if parsed is None:
        return None
    token = str(parsed["board_token"]).lower()
    if token in SKIP_BOARD_TOKENS:
        return None
    display_name = mcc.clean_display_name(company_hint) if company_hint else _company_name_from_token(token)
    if not display_name:
        display_name = _company_name_from_token(token)
    return DiscoveredCandidate(
        company=display_name,
        platform=str(parsed["platform"]),
        board_token=token,
        source_url=url,
        fetch_tier=int(parsed.get("fetch_tier", 2)),
        platform_config=parsed.get("platform_config"),
    )


def collect_candidates_from_urls(
    urls: Iterable[str],
    *,
    existing_tokens: set[str],
    company_hints: dict[str, str] | None = None,
) -> tuple[list[DiscoveredCandidate], list[str], list[str]]:
    hints = company_hints or {}
    by_token: dict[str, DiscoveredCandidate] = {}
    skipped_existing: list[str] = []
    skipped_unsupported: list[str] = []

    for url in urls:
        url = url.strip()
        if not url:
            continue
        hint = hints.get(url, "")
        candidate = parse_url_to_candidate(url, company_hint=hint)
        if candidate is None:
            skipped_unsupported.append(url)
            continue
        if candidate.board_token in existing_tokens:
            skipped_existing.append(candidate.board_token)
            continue
        if candidate.board_token in by_token:
            continue
        by_token[candidate.board_token] = candidate

    return list(by_token.values()), skipped_existing, skipped_unsupported


def collect_candidates_from_csv(csv_path: Path, *, existing_tokens: set[str]) -> DiscoveryResult:
    result = DiscoveryResult()
    urls: list[str] = []
    hints: dict[str, str] = {}

    with csv_path.open(encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            name = (
                row.get("Company")
                or row.get("company")
                or row.get("category")
                or ""
            ).strip()
            url = (
                row.get("Job Link")
                or row.get("job link")
                or row.get("apply_link")
                or row.get("url")
                or ""
            ).strip()
            if not url:
                continue
            urls.append(url)
            if name and name.lower() not in {"software engineering", "category"}:
                hints[url] = name

    result.urls_collected = len(urls)
    candidates, skipped_existing, skipped_unsupported = collect_candidates_from_urls(
        urls,
        existing_tokens=existing_tokens,
        company_hints=hints,
    )
    result.candidates = candidates
    result.skipped_existing = skipped_existing
    result.skipped_unsupported = skipped_unsupported
    return result


async def validate_board(
    client: httpx.AsyncClient,
    candidate: DiscoveredCandidate,
) -> tuple[str, str | None]:
    platform = candidate.platform
    board_token = candidate.board_token
    platform_config = candidate.platform_config if isinstance(candidate.platform_config, dict) else {}
    try:
        if platform == "greenhouse":
            url = f"https://boards-api.greenhouse.io/v1/boards/{board_token}/jobs"
            response = await client.get(url, timeout=20.0)
            if response.status_code == 404:
                return "invalid", "board not found"
            response.raise_for_status()
            payload = response.json()
            if not isinstance(payload, dict) or "jobs" not in payload:
                return "invalid", "unexpected response shape"
            return "valid", None

        if platform == "lever":
            url = f"https://api.lever.co/v0/postings/{board_token}"
            response = await client.get(url, params={"mode": "json"}, timeout=20.0)
            if response.status_code == 404:
                return "invalid", "board not found"
            response.raise_for_status()
            payload = response.json()
            if not isinstance(payload, list):
                return "invalid", "unexpected response shape"
            return "valid", None

        if platform == "ashby":
            payload = {
                "operationName": "ApiJobBoardWithTeams",
                "variables": {"organizationHostedJobsPageName": board_token},
                "query": ASHBY_LIST_QUERY,
            }
            response = await client.post(
                "https://jobs.ashbyhq.com/api/non-user-graphql?op=ApiJobBoardWithTeams",
                json=payload,
                timeout=20.0,
            )
            if response.status_code == 404:
                return "invalid", "board not found"
            response.raise_for_status()
            body = response.json()
            errors = body.get("errors") if isinstance(body, dict) else None
            if isinstance(errors, list) and errors:
                message = errors[0].get("message") if isinstance(errors[0], dict) else str(errors[0])
                return "invalid", message
            job_board = body.get("data", {}).get("jobBoard") if isinstance(body, dict) else None
            if not isinstance(job_board, dict):
                return "invalid", "job board missing"
            return "valid", None

        if platform == "smartrecruiters":
            url = f"https://api.smartrecruiters.com/v1/companies/{board_token}/postings"
            response = await client.get(url, params={"limit": 1}, timeout=20.0)
            if response.status_code == 404:
                return "invalid", "company not found"
            response.raise_for_status()
            payload = response.json()
            if not isinstance(payload, dict):
                return "invalid", "unexpected response shape"
            return "valid", None

        if platform == "workable":
            url = f"https://apply.workable.com/api/v1/widget/accounts/{board_token}"
            response = await client.get(url, params={"details": "true"}, timeout=20.0)
            if response.status_code == 404:
                return "invalid", "account not found"
            response.raise_for_status()
            return "valid", None

        if platform == "bamboohr":
            url = f"https://{board_token}.bamboohr.com/careers/list"
            response = await client.get(url, timeout=20.0)
            if response.status_code == 404:
                return "invalid", "careers site not found"
            response.raise_for_status()
            payload = response.json()
            if not isinstance(payload, dict) or "result" not in payload:
                return "invalid", "unexpected response shape"
            return "valid", None

        if platform == "rippling":
            url = f"https://ats.rippling.com/{board_token}/jobs"
            response = await client.get(url, timeout=20.0)
            if response.status_code == 404:
                return "invalid", "jobs page not found"
            if response.status_code >= 400:
                return "invalid", f"HTTP {response.status_code}"
            return "valid", None

        if platform == "workday":
            tenant = platform_config.get("tenant")
            instance = platform_config.get("instance")
            career_site = platform_config.get("career_site")
            if not tenant or not instance or not career_site:
                return "skipped", "missing workday platform_config"
            base = f"https://{tenant}.{instance}.myworkdayjobs.com/wday/cxs/{tenant}/{career_site}"
            response = await client.post(
                f"{base}/jobs",
                json={"appliedFacets": {}, "limit": 1, "offset": 0, "searchText": ""},
                timeout=30.0,
            )
            if response.status_code == 404:
                return "invalid", "career site not found"
            if response.status_code >= 400:
                return "invalid", f"HTTP {response.status_code}"
            return "valid", None

        if platform == "oracle_hcm":
            datacenter = str(platform_config.get("datacenter") or "us2")
            site_number = str(platform_config.get("site_number") or "CX_1")
            url = (
                f"https://{board_token}.fa.{datacenter}.oraclecloud.com"
                f"/hcmUI/CandidateExperience/en/sites/{site_number}/jobs"
            )
            response = await client.get(url, timeout=20.0)
            if response.status_code == 404:
                return "invalid", "site not found"
            if response.status_code >= 400:
                return "invalid", f"HTTP {response.status_code}"
            return "valid", None

        if platform == "icims":
            base = str(platform_config.get("base_url") or f"https://careers-{board_token}.icims.com").rstrip("/")
            response = await client.get(f"{base}/sitemap.xml", timeout=20.0)
            if response.status_code == 404:
                return "invalid", "sitemap not found"
            if response.status_code >= 400:
                return "invalid", f"HTTP {response.status_code}"
            return "valid", None

        if platform == "eightfold":
            api_host = platform_config.get("api_host")
            domain = platform_config.get("domain")
            if not api_host or not domain:
                return "skipped", "missing eightfold platform_config"
            response = await client.get(
                f"https://{api_host}/api/apply/v2/jobs",
                params={"domain": domain, "start": 0},
                timeout=20.0,
            )
            if response.status_code == 404:
                return "invalid", "api not found"
            if response.status_code >= 400:
                return "invalid", f"HTTP {response.status_code}"
            return "valid", None

        if platform == "successfactors":
            career_site_url = platform_config.get("career_site_url")
            if not career_site_url:
                return "skipped", "missing successfactors career_site_url"
            response = await client.get(str(career_site_url), timeout=20.0)
            if response.status_code >= 400:
                return "invalid", f"HTTP {response.status_code}"
            return "valid", None

        return "skipped", f"no validator for {platform}"
    except httpx.HTTPStatusError as exc:
        return "invalid", f"HTTP {exc.response.status_code}"
    except Exception as exc:  # noqa: BLE001
        return "invalid", str(exc)


async def validate_candidates(
    candidates: list[DiscoveredCandidate],
    *,
    concurrency: int = 6,
) -> None:
    semaphore = asyncio.Semaphore(max(concurrency, 1))

    async with httpx.AsyncClient() as client:

        async def _validate(candidate: DiscoveredCandidate) -> None:
            async with semaphore:
                status, detail = await validate_board(client, candidate)
                candidate.validation_status = status
                candidate.validation_detail = detail

        await asyncio.gather(*[_validate(candidate) for candidate in candidates])


async def discover_from_search(
    provider: SearchProvider,
    queries: list[str],
    *,
    existing_tokens: set[str],
    max_results_per_query: int = 50,
    query_delay_s: float = 1.0,
) -> DiscoveryResult:
    result = DiscoveryResult()
    urls: list[str] = []
    seen_urls: set[str] = set()

    for query in queries:
        hits = await provider.search(query, max_results=max_results_per_query)
        result.search_queries_run += 1
        for hit in hits:
            for url in extract_urls_from_search_hit(hit):
                if url not in seen_urls:
                    seen_urls.add(url)
                    urls.append(url)
        await asyncio.sleep(query_delay_s)

    result.urls_collected = len(urls)
    candidates, skipped_existing, skipped_unsupported = collect_candidates_from_urls(
        urls,
        existing_tokens=existing_tokens,
    )
    result.candidates = candidates
    result.skipped_existing = skipped_existing
    result.skipped_unsupported = skipped_unsupported
    return result


def merge_candidates_into_json(
    candidates: list[DiscoveredCandidate],
    companies_path: Path,
    *,
    only_valid: bool = True,
    dry_run: bool = False,
) -> dict[str, Any]:
    existing: list[dict[str, Any]] = []
    if companies_path.exists():
        payload = json.loads(companies_path.read_text(encoding="utf-8"))
        if isinstance(payload, list):
            existing = payload

    existing_tokens = {
        str(item["board_token"]).lower() for item in existing if item.get("board_token")
    }
    added: list[dict[str, Any]] = []
    skipped: list[str] = []

    for candidate in candidates:
        if only_valid and candidate.validation_status not in {"valid", "skipped", "pending"}:
            skipped.append(candidate.board_token)
            continue
        if candidate.board_token in existing_tokens:
            skipped.append(candidate.board_token)
            continue
        entry = mcc.build_entry(candidate.company, {
            "platform": candidate.platform,
            "board_token": candidate.board_token,
            "fetch_tier": candidate.fetch_tier,
            "platform_config": candidate.platform_config,
        })
        added.append(entry)
        existing.append(entry)
        existing_tokens.add(candidate.board_token)

    if not dry_run and added:
        companies_path.write_text(json.dumps(existing, indent=2) + "\n", encoding="utf-8")

    return {
        "added_count": len(added),
        "added": added,
        "skipped_count": len(skipped),
        "skipped": skipped,
        "total_after": len(existing),
    }


def build_search_provider() -> SearchProvider:
    serpapi_key = os.environ.get("SERPAPI_API_KEY", "").strip()
    if serpapi_key:
        return SerpApiProvider(api_key=serpapi_key)

    google_key = os.environ.get("GOOGLE_CSE_API_KEY", "").strip()
    google_cx = os.environ.get("GOOGLE_CSE_CX", "").strip()
    if google_key and google_cx:
        return GoogleCseProvider(api_key=google_key, cx=google_cx)

    raise RuntimeError(
        "Set SERPAPI_API_KEY or both GOOGLE_CSE_API_KEY and GOOGLE_CSE_CX for search discovery."
    )


def load_queries_from_file(path: Path) -> list[str]:
    lines = [
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]
    if not lines:
        raise ValueError(f"No queries found in {path}")
    return lines


def write_candidates_report(path: Path, result: DiscoveryResult) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "search_queries_run": result.search_queries_run,
        "cdx_indexes_scanned": result.cdx_indexes_scanned,
        "cdx_pages_fetched": result.cdx_pages_fetched,
        "cdx_page_failures": result.cdx_page_failures,
        "unique_tokens_seen": result.unique_tokens_seen,
        "urls_collected": result.urls_collected,
        "candidate_count": len(result.candidates),
        "skipped_existing_count": len(result.skipped_existing),
        "skipped_unsupported_count": len(result.skipped_unsupported),
        "candidates": [candidate.to_json_entry() for candidate in result.candidates],
        "skipped_unsupported": result.skipped_unsupported[:100],
    }
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


async def fetch_common_crawl_indexes(
    client: httpx.AsyncClient,
    *,
    limit: int = 6,
    max_retries: int = CDX_DEFAULT_MAX_RETRIES,
    retry_base_s: float = CDX_DEFAULT_RETRY_BASE_S,
    log: Any = None,
) -> list[str]:
    last_error: Exception | None = None
    for attempt in range(max_retries + 1):
        try:
            response = await client.get(COMMON_CRAWL_COLLINFO_URL, timeout=30.0)
            if response.status_code in CDX_RETRYABLE_STATUS:
                raise httpx.HTTPStatusError(
                    f"CDX collinfo HTTP {response.status_code}",
                    request=response.request,
                    response=response,
                )
            response.raise_for_status()
            payload = response.json()
            if not isinstance(payload, list):
                raise ValueError("Unexpected collinfo.json shape")
            return [str(item["id"]) for item in payload[:limit] if isinstance(item, dict) and item.get("id")]
        except Exception as exc:  # noqa: BLE001
            if not _is_retryable_cdx_error(exc) or attempt >= max_retries:
                raise
            last_error = exc
            delay = retry_base_s * (2**attempt)
            if log:
                log(f"CDX collinfo retry {attempt + 1}/{max_retries} in {delay:.1f}s ({exc})")
            await asyncio.sleep(delay)
    raise RuntimeError(f"CDX collinfo failed after retries: {last_error}")


def board_token_from_cdx_url(url: str, platform_hint: str) -> tuple[str, str] | None:
    parsed = urlparse(url)
    host = parsed.netloc.lower().replace("www.", "")
    parts = [part for part in parsed.path.split("/") if part]
    if not parts:
        return None

    platform = platform_hint
    token = parts[0].lower()

    if "greenhouse.io" in host:
        platform = "greenhouse"
        token = parts[0].lower()
    elif host == "jobs.lever.co":
        platform = "lever"
        token = parts[0].lower()
    elif host == "jobs.ashbyhq.com":
        platform = "ashby"
        token = parts[0].lower()
    elif host == "jobs.smartrecruiters.com":
        platform = "smartrecruiters"
        token = parts[0].lower()

    if not token or token in SKIP_BOARD_TOKENS:
        return None
    if token.isdigit():
        return None
    if UUID_RE.match(token):
        return None
    if len(token) < 2 or len(token) > 120:
        return None
    return platform, token


def _canonical_source_url(platform: str, board_token: str) -> str:
    if platform == "greenhouse":
        return f"https://boards.greenhouse.io/{board_token}"
    if platform == "lever":
        return f"https://jobs.lever.co/{board_token}"
    if platform == "ashby":
        return f"https://jobs.ashbyhq.com/{board_token}"
    if platform == "smartrecruiters":
        return f"https://jobs.smartrecruiters.com/{board_token}"
    return f"https://{board_token}"


def _is_retryable_cdx_error(exc: Exception) -> bool:
    if isinstance(
        exc,
        (
            httpx.RemoteProtocolError,
            httpx.ConnectError,
            httpx.ReadTimeout,
            httpx.WriteTimeout,
            httpx.PoolTimeout,
            httpx.NetworkError,
        ),
    ):
        return True
    if isinstance(exc, httpx.HTTPStatusError):
        return exc.response.status_code in CDX_RETRYABLE_STATUS
    return False


def _parse_cdx_response_text(text: str) -> list[str]:
    urls: list[str] = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(row, dict) and row.get("url"):
            urls.append(str(row["url"]))
    return urls


async def _fetch_cdx_page(
    client: httpx.AsyncClient,
    *,
    index_id: str,
    url_pattern: str,
    page: int,
    page_size: int,
    max_retries: int = CDX_DEFAULT_MAX_RETRIES,
    retry_base_s: float = CDX_DEFAULT_RETRY_BASE_S,
    log: Any = None,
) -> list[str] | None:
    """Fetch one CDX page. Returns None if retries are exhausted."""
    endpoint = f"https://index.commoncrawl.org/{index_id}-index"
    params = {
        "url": url_pattern,
        "output": "json",
        "fl": "url",
        "filter": "status:200",
        "limit": page_size,
        "page": page,
    }
    last_error: Exception | None = None
    for attempt in range(max_retries + 1):
        try:
            response = await client.get(endpoint, params=params, timeout=120.0)
            if response.status_code in {400, 404}:
                return []
            if response.status_code in CDX_RETRYABLE_STATUS:
                raise httpx.HTTPStatusError(
                    f"CDX HTTP {response.status_code}",
                    request=response.request,
                    response=response,
                )
            response.raise_for_status()
            return _parse_cdx_response_text(response.text)
        except Exception as exc:  # noqa: BLE001
            if not _is_retryable_cdx_error(exc):
                raise
            last_error = exc
            if attempt >= max_retries:
                break
            delay = retry_base_s * (2**attempt)
            if log:
                log(
                    f"CDX retry {attempt + 1}/{max_retries} in {delay:.1f}s: "
                    f"{index_id} {url_pattern} page={page} ({exc})"
                )
            await asyncio.sleep(delay)
    if log:
        log(
            f"CDX skipped after retries: {index_id} {url_pattern} page={page} ({last_error})"
        )
    return None


async def discover_from_common_crawl(
    *,
    existing_tokens: set[str],
    index_count: int = 6,
    max_pages_per_pattern: int = 200,
    page_size: int = 2000,
    page_delay_s: float = 0.25,
    max_retries: int = CDX_DEFAULT_MAX_RETRIES,
    retry_base_s: float = CDX_DEFAULT_RETRY_BASE_S,
    patterns: list[str] | None = None,
    log: Any = None,
) -> DiscoveryResult:
    result = DiscoveryResult()
    patterns = patterns or COMMON_CRAWL_URL_PATTERNS
    seen_keys: set[tuple[str, str]] = set()
    key_to_url: dict[tuple[str, str], str] = {}

    async with httpx.AsyncClient(follow_redirects=True) as client:
        indexes = await fetch_common_crawl_indexes(
            client,
            limit=index_count,
            max_retries=max_retries,
            retry_base_s=retry_base_s,
            log=log,
        )
        result.cdx_indexes_scanned = len(indexes)

        for index_id in indexes:
            for url_pattern in patterns:
                if log:
                    log(f"CDX {index_id} {url_pattern}")
                for page in range(max_pages_per_pattern):
                    urls = await _fetch_cdx_page(
                        client,
                        index_id=index_id,
                        url_pattern=url_pattern,
                        page=page,
                        page_size=page_size,
                        max_retries=max_retries,
                        retry_base_s=retry_base_s,
                        log=log,
                    )
                    result.cdx_pages_fetched += 1
                    if urls is None:
                        result.cdx_page_failures += 1
                        break
                    if not urls:
                        break
                    result.urls_collected += len(urls)
                    for url in urls:
                        candidate = parse_url_to_candidate(url)
                        if candidate is None:
                            continue
                        key = (candidate.platform, candidate.board_token)
                        if key in seen_keys:
                            continue
                        seen_keys.add(key)
                        key_to_url[key] = url
                    if len(urls) < page_size:
                        break
                    await asyncio.sleep(page_delay_s)

    result.unique_tokens_seen = len(seen_keys)
    candidates: list[DiscoveredCandidate] = []
    skipped_existing: list[str] = []

    for key in sorted(seen_keys, key=lambda item: item[1]):
        platform, token = key
        if token in existing_tokens:
            skipped_existing.append(token)
            continue
        url = key_to_url[key]
        candidate = parse_url_to_candidate(url)
        if candidate is None:
            continue
        candidates.append(candidate)

    result.candidates = candidates
    result.skipped_existing = skipped_existing
    return result
