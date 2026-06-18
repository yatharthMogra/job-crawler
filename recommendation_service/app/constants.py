"""Shared taxonomy — must match job_ingestion and profile_service."""

NORMALIZED_ROLES = [
    "SWE",
    "BACKEND_ENGINEER",
    "FRONTEND_ENGINEER",
    "FULLSTACK_ENGINEER",
    "ML_ENGINEER",
    "DATA_ENGINEER",
    "DATA_SCIENTIST",
    "DEVOPS_ENGINEER",
    "SECURITY_ENGINEER",
    "MOBILE_ENGINEER",
    "SOLUTIONS_ENGINEER",
    "SUPPORT_ENGINEER",
    "SYSTEMS_ENGINEER",
    "HARDWARE_ENGINEER",
    "TECHNICAL_PROGRAM_MANAGER",
    "PRODUCT_MANAGER",
    "PRODUCT_DESIGNER",
    "DATA_ANALYST",
    "SALES",
    "CUSTOMER_SUCCESS",
    "SOLUTIONS_CONSULTANT",
    "PARTNERSHIPS",
    "MARKETING",
    "OPERATIONS",
    "RECRUITING",
    "FINANCE",
    "LEGAL",
    "OTHER",
]

CAPABILITY_TAXONOMY = [
    "Backend Engineering",
    "Frontend Engineering",
    "Full Stack Development",
    "AI Systems",
    "Machine Learning",
    "Machine Learning Research",
    "Data Engineering",
    "Distributed Systems",
    "Cloud Infrastructure",
    "Platform Engineering",
    "DevOps",
    "Product Engineering",
    "Mobile Development",
    "Security Engineering",
    "Analytics Engineering",
    "Research",
]

ROLE_TYPES = ["INTERNSHIP", "NEW_GRAD", "FULLTIME"]

ROLE_INTENTS = [
    "engineer",
    "researcher",
    "consultant",
    "educator",
    "manager",
    "analyst",
    "accountant",
    "auditor",
    "investment_banker",
    "sales",
    "operations",
    "legal",
    "other",
]

DEFAULT_ROLE_INTENTS = ["engineer", "researcher"]


def normalize_pool_name(pool_name: str) -> str:
    """Map legacy *_INTERN suffix to canonical *_INTERNSHIP."""
    if pool_name.endswith("_INTERN"):
        return f"{pool_name}SHIP"
    return pool_name


def normalize_pool_names(pool_names: list[str]) -> list[str]:
    return list(dict.fromkeys(normalize_pool_name(name) for name in pool_names))

EFFORT_LABELS = {
    "LOW": "Quick Apply",
    "MEDIUM": "Standard",
    "HIGH": "Detailed",
}
