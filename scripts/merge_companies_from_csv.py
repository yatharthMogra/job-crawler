#!/usr/bin/env python3
"""Merge supported companies from a CSV export into job_ingestion/data/companies.json."""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CSV = ROOT / "companies_1.csv"
DEFAULT_JSON = ROOT / "job_ingestion" / "data" / "companies.json"

UNSUPPORTED_REASONS: dict[str, str] = {}

SUCCESSFACTORS_SITES: dict[str, dict[str, Any]] = {
    "jobs.mcdonalds.com": {
        "board_token": "mcdonalds",
        "platform_config": {
            "career_site_url": "https://jobs.mcdonalds.com",
            "locale": "en_US",
            "search_page_size": 10,
        },
    },
    "careers.westinghousenuclear.com": {
        "board_token": "westinghouse-nuclear",
        "platform_config": {
            "career_site_url": "https://careers.westinghousenuclear.com",
            "locale": "en_US",
            "search_page_size": 25,
            "search_default_params": {"searchby": "location", "d": "10"},
        },
    },
}

MANUAL_ENTRIES: dict[str, dict[str, Any]] = {
    "hudson river trading": {
        "platform": "greenhouse",
        "board_token": "hrttalentcommunity",
        "fetch_tier": 2,
    },
    "ixl learning": {
        "platform": "greenhouse",
        "board_token": "ixllearning",
        "fetch_tier": 2,
        "platform_config": {"careers_url": "https://www.ixl.com/company/jobs/"},
    },
    "nymbus": {
        "platform": "greenhouse",
        "board_token": "nymbusinc",
        "fetch_tier": 2,
        "platform_config": {"careers_url": "https://nymbus.com/careers"},
    },
    "steel point solutions": {
        "platform": "greenhouse",
        "board_token": "steelpointsolutions",
        "fetch_tier": 2,
        "platform_config": {
            "careers_url": "https://steelpoint-llc.com/government-it-consultant-careers/"
        },
    },
    "konrad group": {
        "platform": "greenhouse",
        "board_token": "konradgroup",
        "fetch_tier": 2,
    },
    "oscar health": {
        "platform": "greenhouse",
        "board_token": "oscar",
        "fetch_tier": 2,
        "platform_config": {"careers_url": "https://www.hioscar.com/careers/"},
    },
    "trustpilot": {
        "platform": "greenhouse",
        "board_token": "trustpilot",
        "fetch_tier": 2,
        "platform_config": {"careers_url": "https://corporate.trustpilot.com/careers/"},
    },
    "brain corp": {
        "platform": "greenhouse",
        "board_token": "braincorporation",
        "fetch_tier": 2,
        "platform_config": {"careers_url": "https://braincorp.com/open-positions"},
    },
    "state street": {
        "platform": "workday",
        "board_token": "statestreet-global",
        "fetch_tier": 3,
        "platform_config": {
            "tenant": "statestreet",
            "instance": "wd1",
            "career_site": "Global",
            "public_path_prefix": "Global",
        },
    },
    "zoll medical corporation": {
        "platform": "workday",
        "board_token": "zoll-zollmedicalcorp",
        "fetch_tier": 3,
        "platform_config": {
            "tenant": "zoll",
            "instance": "wd5",
            "career_site": "ZOLLMedicalCorp",
            "public_path_prefix": "en-US/ZOLLMedicalCorp",
        },
    },
    "waymo": {
        "platform": "greenhouse",
        "board_token": "waymo",
        "fetch_tier": 2,
        "platform_config": {"careers_url": "https://careers.withwaymo.com/jobs"},
    },
}

NAME_ALIASES: dict[str, str] = {
    "the boeing company": "boeing-external-careers",
    "brain co": "brainco",
    "gm financial": "fa-exvu-saasfaprod1",
    "general motors": "generalmotors",
    "playstation": "sonyinteractiveentertainmentglobal",
    "sony interactive entertainment": "sonyinteractiveentertainmentglobal",
    "susquehanna international group sig": "sig",
    "general dynamics mission systems": "gdms",
    "cerebras": "earlytalentcerebras",
    "palantir": "palantir",
    "notion": "notion",
    "nvidia": "nvidia",
    "spacex": "spacex",
    "salesforce": "salesforce",
}


def normalize_name(name: str) -> str:
    cleaned = re.sub(r"^[\U0001F525🔥\s]+", "", name).strip().lower()
    cleaned = re.sub(r"[^a-z0-9]+", " ", cleaned).strip()
    return cleaned


def clean_display_name(name: str) -> str:
    return re.sub(r"^[\U0001F525🔥\s]+", "", name).strip()


def parse_workday(url: str) -> dict[str, Any] | None:
    parsed = urlparse(url)
    host = parsed.netloc.lower()
    match = re.search(r"([\w-]+)\.wd(\d+)\.myworkdayjobs\.com", host)
    if not match:
        return None
    tenant = match.group(1)
    instance = f"wd{match.group(2)}"
    parts = [part for part in parsed.path.split("/") if part]
    if not parts:
        return None
    if parts[0].lower().startswith("en-") and len(parts) >= 2:
        career_site = parts[1]
        prefix = f"{parts[0]}/{parts[1]}"
    else:
        career_site = parts[0]
        prefix = parts[0]
    board_token = tenant
    if career_site.lower() not in {"external", "careers", "search"}:
        board_token = f"{tenant}-{career_site}".lower().replace("_", "-")
    return {
        "platform": "workday",
        "board_token": board_token,
        "fetch_tier": 3,
        "platform_config": {
            "tenant": tenant,
            "instance": instance,
            "career_site": career_site,
            "public_path_prefix": prefix,
        },
    }


def parse_oracle(url: str) -> dict[str, Any] | None:
    parsed = urlparse(url)
    host = parsed.netloc.lower()
    board_token = host.split(".")[0]
    site_match = re.search(r"/sites/([^/]+)/", url)
    site_number = site_match.group(1) if site_match else "CX_1"
    dc_match = re.search(r"\.fa\.(\w+)\.oraclecloud\.com", host)
    datacenter = dc_match.group(1) if dc_match else "us2"
    return {
        "platform": "oracle_hcm",
        "board_token": board_token.lower(),
        "fetch_tier": 3,
        "platform_config": {"datacenter": datacenter, "site_number": site_number},
    }


def parse_greenhouse(name: str, url: str) -> dict[str, Any] | None:
    board_match = re.search(r"(?:boards|job-boards)\.greenhouse\.io/([^/?]+)", url, re.IGNORECASE)
    if board_match:
        slug = board_match.group(1)
        if slug.lower() not in {"embed", "job_app"}:
            return {"platform": "greenhouse", "board_token": slug.lower(), "fetch_tier": 2}

    if "gh_jid" not in url.lower() and "greenhouse" not in url.lower():
        return None

    parsed = urlparse(url)
    host = parsed.netloc.lower().replace("www.", "")
    slug = host.split(".")[0]
    if slug in {"boards", "job-boards", "careers"}:
        return None
    careers_url = url.split("?")[0]
    entry: dict[str, Any] = {
        "platform": "greenhouse",
        "board_token": slug.lower(),
        "fetch_tier": 2,
        "platform_config": {"careers_url": careers_url},
    }
    return entry


def parse_entry(name: str, url: str) -> dict[str, Any] | None:
    normalized = normalize_name(name)
    if normalized in MANUAL_ENTRIES:
        return dict(MANUAL_ENTRIES[normalized])

    url_lower = url.lower()
    if "jobs.lever.co" in url_lower:
        slug = urlparse(url).path.strip("/").split("/")[0]
        return {"platform": "lever", "board_token": slug.lower(), "fetch_tier": 2}
    if "jobs.ashbyhq.com" in url_lower or "jobs.ashby.com" in url_lower:
        slug = urlparse(url).path.strip("/").split("/")[0]
        return {"platform": "ashby", "board_token": slug, "fetch_tier": 2}
    if "myworkdayjobs.com" in url_lower:
        return parse_workday(url)
    if "oraclecloud.com" in url_lower:
        return parse_oracle(url)
    if ".icims.com" in url_lower:
        host = urlparse(url).netloc.lower()
        slug = host.split(".")[0]
        if slug.startswith("careers-"):
            slug = slug[len("careers-") :]
        return {
            "platform": "icims",
            "board_token": slug.lower(),
            "fetch_tier": 3,
            "platform_config": {},
        }
    if "apply.workable.com" in url_lower:
        slug_match = re.search(r"apply\.workable\.com/([^/]+)", url, re.IGNORECASE)
        if not slug_match:
            return None
        return {
            "platform": "workable",
            "board_token": slug_match.group(1).lower(),
            "fetch_tier": 2,
        }
    greenhouse = parse_greenhouse(name, url)
    if greenhouse:
        return greenhouse

    if "smartrecruiters.com" in url_lower:
        jobs_match = re.search(
            r"jobs\.smartrecruiters\.com/([^/?#]+)",
            url,
            re.IGNORECASE,
        )
        api_match = re.search(
            r"api\.smartrecruiters\.com/v1/companies/([^/?#]+)",
            url,
            re.IGNORECASE,
        )
        slug_match = jobs_match or api_match
        if slug_match:
            return {
                "platform": "smartrecruiters",
                "board_token": slug_match.group(1).lower(),
                "fetch_tier": 2,
            }
        return None

    bamboohr_match = re.search(
        r"([a-z0-9-]+)\.bamboohr\.com/careers",
        url,
        re.IGNORECASE,
    )
    if bamboohr_match:
        return {
            "platform": "bamboohr",
            "board_token": bamboohr_match.group(1).lower(),
            "fetch_tier": 2,
        }

    rippling_match = re.search(
        r"ats\.rippling\.com/([^/?#]+)/jobs",
        url,
        re.IGNORECASE,
    )
    if rippling_match:
        return {
            "platform": "rippling",
            "board_token": rippling_match.group(1).lower(),
            "fetch_tier": 2,
        }

    host = urlparse(url).netloc.lower()
    rmk_job_match = re.search(r"https?://[^/]+/job/[^/]+/\d+", url, re.IGNORECASE)
    if "successfactors" in url_lower or rmk_job_match:
        site = SUCCESSFACTORS_SITES.get(host)
        if site:
            return {
                "platform": "successfactors",
                "board_token": site["board_token"],
                "fetch_tier": 3,
                "platform_config": site["platform_config"],
            }
        if "successfactors" in url_lower and rmk_job_match:
            board_token = host.split(".")[0].replace("careers", "").strip("-") or host
            return {
                "platform": "successfactors",
                "board_token": board_token,
                "fetch_tier": 3,
                "platform_config": {
                    "career_site_url": f"https://{host}",
                    "locale": "en_US",
                },
            }

    if "google.com/about/careers" in url_lower or "careers.google.com" in url_lower:
        return {
            "platform": "google_careers",
            "board_token": "google",
            "fetch_tier": 1,
            "platform_config": {},
        }

    if "amazon.jobs" in url_lower:
        return {
            "platform": "amazon_jobs",
            "board_token": "amazon",
            "fetch_tier": 1,
            "platform_config": {
                "locale": "en",
                "job_categories": [
                    "software-development",
                    "data-science",
                    "research-science",
                    "project-program-product-management-technical",
                    "hardware-development",
                    "solutions-architect",
                ],
                "exclude_job_categories": [
                    "Fulfillment & Operations Management",
                    "Medical, Health, & Safety",
                ],
                "exclude_job_families": [
                    "Fulfillment Center",
                    "Fulfillment Associates",
                ],
            },
        }

    if any(
        marker in url_lower
        for marker in (
            "jobvite.com",
            "metacareers.com",
            "citadelsecurities.com",
            "intuit.com/job",
        )
    ):
        UNSUPPORTED_REASONS[normalized] = "no connector for ATS"
        return None

    if "boards.greenhouse.io/embed/job_app" in url_lower:
        UNSUPPORTED_REASONS[normalized] = "greenhouse embed URL without board slug"
        return None

    if normalized == "dat freight analytics":
        UNSUPPORTED_REASONS[normalized] = "could not resolve greenhouse board token"
        return None

    if normalized == "uber":
        UNSUPPORTED_REASONS[normalized] = "custom careers site (no public GH board slug)"
        return None

    UNSUPPORTED_REASONS[normalized] = "unrecognized URL pattern"
    return None


def build_entry(name: str, parsed: dict[str, Any]) -> dict[str, Any]:
    entry: dict[str, Any] = {
        "company": clean_display_name(name),
        "platform": parsed["platform"],
        "board_token": parsed["board_token"],
        "is_active": True,
        "fetch_tier": parsed.get("fetch_tier", 2),
    }
    if parsed.get("platform_config"):
        entry["platform_config"] = parsed["platform_config"]
    return entry


def merge_csv_into_json(
    csv_path: Path,
    json_path: Path,
    *,
    dry_run: bool = False,
) -> dict[str, Any]:
    existing: list[dict[str, Any]] = json.loads(json_path.read_text(encoding="utf-8"))
    existing_tokens = {str(item["board_token"]).lower() for item in existing if item.get("board_token")}
    existing_names = {normalize_name(str(item.get("company", ""))) for item in existing}

    added: list[dict[str, Any]] = []
    skipped_existing: list[str] = []
    skipped_unsupported: list[str] = []

    for row in csv.DictReader(csv_path.open(encoding="utf-8")):
        name = (row.get("Company") or row.get("company") or "").strip()
        url = (row.get("Job Link") or row.get("job link") or row.get("url") or "").strip()
        if not name or not url:
            continue

        normalized = normalize_name(name)
        alias_token = NAME_ALIASES.get(normalized)
        if alias_token and alias_token.lower() in existing_tokens:
            skipped_existing.append(name)
            continue
        if normalized in existing_names:
            skipped_existing.append(name)
            continue

        parsed = parse_entry(name, url)
        if parsed is None:
            skipped_unsupported.append(name)
            continue

        token = str(parsed["board_token"]).lower()
        if token in existing_tokens:
            skipped_existing.append(name)
            continue

        entry = build_entry(name, parsed)
        added.append(entry)
        existing.append(entry)
        existing_tokens.add(token)
        existing_names.add(normalized)

    result = {
        "added_count": len(added),
        "added": added,
        "skipped_existing_count": len(skipped_existing),
        "skipped_unsupported_count": len(skipped_unsupported),
        "skipped_unsupported": skipped_unsupported,
        "total_after": len(existing),
    }

    if not dry_run and added:
        json_path.write_text(json.dumps(existing, indent=2) + "\n", encoding="utf-8")

    return result


def main() -> int:
    args = [arg for arg in sys.argv[1:] if arg != "--dry-run"]
    dry_run = "--dry-run" in sys.argv
    csv_path = Path(args[0]) if len(args) > 0 else DEFAULT_CSV
    json_path = Path(args[1]) if len(args) > 1 else DEFAULT_JSON
    result = merge_csv_into_json(csv_path, json_path, dry_run=dry_run)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
