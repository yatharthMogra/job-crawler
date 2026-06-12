"""Domain derivation for candidate profiles — mirrors job_ingestion/app/ingestion/taxonomy.py."""

from __future__ import annotations

from collections import Counter

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

CAPABILITY_DOMAIN_MAP: dict[str, list[str]] = {
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


def is_valid_domain_pair(primary: str, secondary: str) -> bool:
    return frozenset({primary, secondary}) in VALID_SECONDARY_PAIRS


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
