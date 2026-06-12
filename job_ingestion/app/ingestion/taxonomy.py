"""Domain taxonomy — must match domain_taxonomy_spec.md."""

from __future__ import annotations

from collections import Counter
from typing import Literal

DomainName = Literal[
    "Software",
    "Data_Analytics",
    "Management",
    "Business",
    "Hardware_Electrical",
    "Mechanical",
    "Aerospace_Defense",
    "Industrial_Automation",
    "Design",
    "Research_Science",
    "Other",
]

DOMAIN_NAMES: tuple[str, ...] = (
    "Software",
    "Data_Analytics",
    "Management",
    "Business",
    "Hardware_Electrical",
    "Mechanical",
    "Aerospace_Defense",
    "Industrial_Automation",
    "Design",
    "Research_Science",
    "Other",
)

ROLE_SUFFIXES: tuple[str, ...] = ("FULLTIME", "INTERNSHIP", "NEW_GRAD")

_ROLE_DOMAIN_MAP: dict[str, DomainName] = {
    # Software
    "SWE": "Software",
    "BACKEND_ENGINEER": "Software",
    "FRONTEND_ENGINEER": "Software",
    "FULLSTACK_ENGINEER": "Software",
    "ML_ENGINEER": "Software",
    "DATA_ENGINEER": "Software",
    "DEVOPS_ENGINEER": "Software",
    "SECURITY_ENGINEER": "Software",
    "MOBILE_ENGINEER": "Software",
    "SOLUTIONS_ENGINEER": "Software",
    "SUPPORT_ENGINEER": "Software",
    "TECHNICAL_PROGRAM_MANAGER": "Software",
    # Data_Analytics
    "DATA_SCIENTIST": "Data_Analytics",
    "DATA_ANALYST": "Data_Analytics",
    # Management
    "PRODUCT_MANAGER": "Management",
    # Business
    "SALES": "Business",
    "MARKETING": "Business",
    "FINANCE": "Business",
    "CUSTOMER_SUCCESS": "Business",
    "RECRUITING": "Business",
    "PARTNERSHIPS": "Business",
    "LEGAL": "Business",
    "OPERATIONS": "Business",
    "SOLUTIONS_CONSULTANT": "Business",
    # Design
    "PRODUCT_DESIGNER": "Design",
    # Aerospace_Defense
    "SYSTEMS_ENGINEER": "Aerospace_Defense",
    # Hardware_Electrical
    "HARDWARE_ENGINEER": "Hardware_Electrical",
    # Fallback
    "OTHER": "Other",
}


def _build_pool_domain_map() -> dict[str, DomainName]:
    mapping: dict[str, DomainName] = {}
    for role_base, domain in _ROLE_DOMAIN_MAP.items():
        for suffix in ROLE_SUFFIXES:
            mapping[f"{role_base}_{suffix}"] = domain
    return mapping


POOL_DOMAIN_MAP: dict[str, DomainName] = _build_pool_domain_map()

DOMAIN_POOLS: dict[str, list[str]] = {}
for _pool, _domain in POOL_DOMAIN_MAP.items():
    DOMAIN_POOLS.setdefault(_domain, []).append(_pool)

VALID_SECONDARY_PAIRS: set[frozenset[str]] = {
    frozenset({"Software", "Data_Analytics"}),
    frozenset({"Software", "Management"}),
    frozenset({"Data_Analytics", "Research_Science"}),
    frozenset({"Data_Analytics", "Management"}),
    frozenset({"Hardware_Electrical", "Mechanical"}),
    frozenset({"Hardware_Electrical", "Aerospace_Defense"}),
    frozenset({"Mechanical", "Aerospace_Defense"}),
    frozenset({"Industrial_Automation", "Hardware_Electrical"}),
    frozenset({"Management", "Business"}),
    frozenset({"Design", "Software"}),
}

CAPABILITY_DOMAIN_MAP: dict[str, list[DomainName]] = {
    "Backend Engineering": ["Software"],
    "Frontend Engineering": ["Software"],
    "Full Stack Development": ["Software"],
    "Cloud Infrastructure": ["Software"],
    "DevOps": ["Software"],
    "AI Systems": ["Software"],
    "Machine Learning Research": ["Software", "Data_Analytics"],
    "Distributed Systems": ["Software"],
    "Data Engineering": ["Software", "Data_Analytics"],
    "Security Engineering": ["Software"],
    "Research": ["Software", "Research_Science"],
    "Machine Learning": ["Data_Analytics", "Software"],
    "Analytics Engineering": ["Data_Analytics"],
    "Statistical Analysis": ["Data_Analytics"],
    "Business Intelligence": ["Data_Analytics"],
    "Product Management": ["Management"],
    "Program Management": ["Management"],
    "Technical Leadership": ["Management", "Software"],
    "Sales": ["Business"],
    "Marketing": ["Business"],
    "Finance": ["Business"],
    "Customer Success": ["Business"],
    "Business Development": ["Business"],
    "UX Design": ["Design"],
    "Product Design": ["Design"],
    "Electrical Engineering": ["Hardware_Electrical"],
    "Hardware Design": ["Hardware_Electrical"],
    "Mechanical Engineering": ["Mechanical"],
    "Structural Analysis": ["Mechanical"],
    "Avionics": ["Aerospace_Defense"],
    "Systems Engineering": ["Aerospace_Defense"],
    "Scientific Research": ["Research_Science"],
    "Computational Science": ["Research_Science", "Software"],
}

MIN_CAPABILITIES_FOR_DOMAIN = 3

DOMAIN_PROMPT_RULES = (
    "job_domain: The professional discipline this role belongs to. Choose exactly one value "
    f"from: {', '.join(DOMAIN_NAMES)}. Assign based on what the role's PRIMARY OUTPUT is, "
    "not the tools used or the company's industry.\n"
    "- Software: Primary output is running software code, systems, APIs, platforms.\n"
    "- Data_Analytics: Business-facing data work — insights, reports, models for decisions.\n"
    "- Management: Decisions and coordination — PM, program/project management.\n"
    "- Business: Non-technical business — sales, marketing, finance, HR, legal, ops.\n"
    "- Hardware_Electrical: Hardware or electrical systems — circuits, PCB, FPGA, RF.\n"
    "- Mechanical: Mechanical systems — structural analysis, CAD, manufacturing design.\n"
    "- Aerospace_Defense: Serves aerospace/defense systems. Assign even for software roles "
    "when aerospace/defense context is required (avionics, flight software, radar, space).\n"
    "- Industrial_Automation: PLC, SCADA, manufacturing automation, process control.\n"
    "- Design: UX, product, visual design, user research.\n"
    "- Research_Science: Scientific research, laboratory, computational science.\n"
    "- Other: Does not fit any category above.\n\n"
    "Software vs Aerospace_Defense (mutually exclusive — never assign both):\n"
    "- Requires aerospace/defense domain knowledge (DO-178C, flight software safety, avionics, "
    "missile/radar/space, classified context) → Aerospace_Defense primary, no secondary.\n"
    "- At an aerospace company but no aerospace expertise required (internal tools, enterprise "
    "SWE, data pipelines) → Software primary, no secondary.\n"
    "- Software + Aerospace_Defense is not a valid pair.\n\n"
    "job_secondary_domain: Second domain ONLY when the role requires substantial expertise in "
    "two disciplines as core responsibilities. If in doubt, leave null. Must differ from "
    "job_domain. Invalid pairs are stripped automatically."
)


def is_valid_domain_pair(primary: str, secondary: str) -> bool:
    return frozenset({primary, secondary}) in VALID_SECONDARY_PAIRS


def coerce_job_domain(value: object) -> str:
    if not isinstance(value, str):
        return "Other"
    normalized = value.strip()
    if normalized in DOMAIN_NAMES:
        return normalized
    return "Other"


def sanitize_job_secondary_domain(primary: str, secondary: str | None) -> str | None:
    if secondary is None:
        return None
    if secondary == primary:
        return None
    if not is_valid_domain_pair(primary, secondary):
        return None
    return secondary


def validate_pools_against_domain(
    job_domain: str,
    assigned_pools: list[str],
    job_secondary_domain: str | None = None,
) -> list[str]:
    valid_domains = {job_domain}
    if job_secondary_domain:
        valid_domains.add(job_secondary_domain)
    return [
        pool
        for pool in assigned_pools
        if POOL_DOMAIN_MAP.get(pool) in valid_domains
    ]


def derive_user_domains(capabilities: list[str]) -> tuple[str, str | None]:
    domain_counts: Counter[str] = Counter()
    for cap in capabilities:
        for domain in CAPABILITY_DOMAIN_MAP.get(cap, []):
            domain_counts[domain] += 1

    if not domain_counts:
        return ("Other", None)

    ranked = domain_counts.most_common()
    primary_domain, primary_count = ranked[0]
    if primary_count < MIN_CAPABILITIES_FOR_DOMAIN:
        return ("Other", None)

    secondary_domain = None
    if len(ranked) >= 2:
        candidate_secondary, secondary_count = ranked[1]
        if (
            secondary_count >= MIN_CAPABILITIES_FOR_DOMAIN
            and is_valid_domain_pair(primary_domain, candidate_secondary)
        ):
            secondary_domain = candidate_secondary

    return (primary_domain, secondary_domain)
