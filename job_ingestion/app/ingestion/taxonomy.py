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
    "AEROSPACE_ENGINEER": "Aerospace_Defense",
    # Hardware_Electrical
    "HARDWARE_ENGINEER": "Hardware_Electrical",
    "FIELD_SERVICE_ENGINEER": "Hardware_Electrical",
    # Industrial_Automation
    "CONTROLS_ENGINEER": "Industrial_Automation",
    # Research_Science
    "RESEARCH_SCIENTIST": "Research_Science",
    "LIFE_SCIENTIST": "Research_Science",
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
    "job_domain: The professional discipline this role belongs to.\n\n"
    "CRITICAL RULE: Assign based on what THIS JOB requires the person to DO each day — "
    "not what the company's industry is. The company's industry never determines the domain.\n\n"
    "Correct examples:\n"
    "  - Hardware Engineer at American Express → Hardware_Electrical\n"
    "  - Data Analyst at RTX/Boeing → Data_Analytics\n"
    "  - Operations Manager, Supply Chain at any company → Management\n"
    "  - Software Engineer, Enterprise Applications at Boeing → Software\n"
    "  - Software Engineer, Avionics Systems at Boeing → Aerospace_Defense\n"
    "  - Finance Analyst at a SaaS company → Business\n\n"
    "Wrong examples:\n"
    "  - Hardware Engineer at Amex → Business (wrong: based on company industry)\n"
    "  - Data Analyst at RTX → Aerospace_Defense (wrong: based on company industry)\n"
    "  - Software Engineer at Boeing always → Aerospace_Defense (wrong: depends on job content)\n\n"
    f"Choose exactly one value from: {', '.join(DOMAIN_NAMES)}.\n"
    "- Software: Primary output is running software code, systems, APIs, platforms.\n"
    "- Data_Analytics: Business-facing data work — insights, reports, models for decisions.\n"
    "- Management: Decisions and coordination — PM, program/project management.\n"
    "- Business: Non-technical business — sales, marketing, finance, HR, legal, ops.\n"
    "- Hardware_Electrical: Hardware or electrical systems — circuits, PCB, FPGA, RF.\n"
    "- Mechanical: Mechanical systems — structural analysis, CAD, manufacturing design.\n"
    "- Aerospace_Defense: Serves aerospace/defense systems when domain expertise is required.\n"
    "- Industrial_Automation: PLC, SCADA, manufacturing automation, process control.\n"
    "- Design: UX, product, visual design, user research.\n"
    "- Research_Science: Scientific research, laboratory, computational science.\n"
    "- Other: Does not fit any category above.\n\n"
    "AEROSPACE_DEFENSE vs SOFTWARE — how to distinguish at defense/aerospace companies:\n"
    "  → Software if ALL are true: general software development (web apps, APIs, internal tools, "
    "data platforms); no aerospace/defense knowledge requirements (avionics, flight software, "
    "missile systems, radar, DO-178C, MIL-STD); a generalist SWE could apply without aerospace "
    "background. Examples: Software Engineer, IT Systems @ Boeing; Data Platform @ RTX.\n"
    "  → Aerospace_Defense if ANY are true: explicit aerospace/defense domain work; domain "
    "standards (DO-178C, DO-254, MIL-STD-461, ITAR); title signals defense context (Mission "
    "Systems, Avionics, Flight Software, Space Systems); clearance required. Examples: Mission "
    "Systems SWE @ RTX; Avionics Software Engineer @ Boeing.\n"
    "Software + Aerospace_Defense is not a valid secondary pair.\n\n"
    "SYSTEMS_ENGINEER at tech companies (not aerospace/defense/industrial context):\n"
    "  → At SaaS or general tech companies, 'Systems Engineer' usually means platform, "
    "distributed systems, or infrastructure engineering — use BACKEND_ENGINEER or "
    "DEVOPS_ENGINEER, NOT SYSTEMS_ENGINEER.\n"
    "  → SYSTEMS_ENGINEER is for aerospace/defense/industrial systems integration "
    "(avionics, radar, PLC-adjacent integration, V&V of complex physical systems).\n\n"
    "job_secondary_domain: Second domain ONLY when the role requires substantial expertise in "
    "two disciplines as core responsibilities. If in doubt, leave null. Must differ from "
    "job_domain. Invalid pairs are stripped automatically.\n\n"
    "Secondary domain assignment rules (apply ONLY when criteria match — do NOT assign "
    "secondary to every job in a primary domain):\n"
    "  - Management + Business: ONLY when the role is project/program/PMO/operations "
    "management (project manager, program manager, program scheduler, PMO). NOT for people "
    "leadership, home care team managers, bereavement managers, or manufacturing floor "
    "supervisors without PM scope.\n"
    "  - Management + Software: ONLY for TECHNICAL_PROGRAM_MANAGER roles working in a "
    "software engineering context (engineering roadmaps, delivery to eng teams).\n"
    "  - Mechanical + Hardware_Electrical: mechanical design roles that also need hardware "
    "engineering pools (mechanical engineer, CAD, structural design).\n"
    "  - Hardware_Electrical + Aerospace_Defense: field service or systems integration in "
    "defense electronics / aerospace hardware context.\n"
    "  - Industrial_Automation + Hardware_Electrical: automation/controls roles spanning "
    "industrial electronics and PLC/SCADA work.\n"
    "  - Do NOT assign Business secondary to all Management jobs — many Management roles "
    "should have null secondary and stay without cross-domain pools."
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
