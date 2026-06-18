"""Hard-coded mapping from retrieval pool base names to role_intent values."""

from __future__ import annotations

from app.constants import ROLE_INTENTS, normalize_pool_name

POOL_SUFFIXES = ("_FULLTIME", "_INTERNSHIP", "_NEW_GRAD")

# Pool base (without employment suffix) → role_intent for retrieval filtering.
POOL_BASE_TO_ROLE_INTENT: dict[str, str] = {
    # Engineering
    "SWE": "engineer",
    "BACKEND_ENGINEER": "engineer",
    "FRONTEND_ENGINEER": "engineer",
    "FULLSTACK_ENGINEER": "engineer",
    "ML_ENGINEER": "engineer",
    "DATA_ENGINEER": "engineer",
    "DEVOPS_ENGINEER": "engineer",
    "SECURITY_ENGINEER": "engineer",
    "MOBILE_ENGINEER": "engineer",
    "SOLUTIONS_ENGINEER": "engineer",
    "SUPPORT_ENGINEER": "engineer",
    "SYSTEMS_ENGINEER": "engineer",
    "HARDWARE_ENGINEER": "engineer",
    "FIELD_SERVICE_ENGINEER": "engineer",
    "CONTROLS_ENGINEER": "engineer",
    "AEROSPACE_ENGINEER": "engineer",
    "RESEARCH_SCIENTIST": "researcher",
    "LIFE_SCIENTIST": "researcher",
    # Data
    "DATA_SCIENTIST": "researcher",
    "DATA_ANALYST": "analyst",
    # Product & design
    "TECHNICAL_PROGRAM_MANAGER": "manager",
    "PRODUCT_MANAGER": "manager",
    "PRODUCT_DESIGNER": "other",
    # Go-to-market & business
    "SALES": "sales",
    "CUSTOMER_SUCCESS": "operations",
    "SOLUTIONS_CONSULTANT": "consultant",
    "PARTNERSHIPS": "sales",
    "MARKETING": "operations",
    "OPERATIONS": "operations",
    "RECRUITING": "operations",
    "FINANCE": "accountant",
    "LEGAL": "legal",
    "OTHER": "other",
}

for intent in set(POOL_BASE_TO_ROLE_INTENT.values()):
    if intent not in ROLE_INTENTS:
        raise ValueError(f"Invalid role_intent in pool mapping: {intent}")


def pool_base_name(pool_name: str) -> str:
    normalized = normalize_pool_name(pool_name)
    for suffix in POOL_SUFFIXES:
        if normalized.endswith(suffix):
            return normalized[: -len(suffix)]
    return normalized


def role_intent_for_pool(pool_name: str) -> str | None:
    return POOL_BASE_TO_ROLE_INTENT.get(pool_base_name(pool_name))


def role_intents_for_pools(pool_names: list[str]) -> list[str]:
    intents: list[str] = []
    seen: set[str] = set()
    for pool_name in pool_names:
        intent = role_intent_for_pool(pool_name)
        if intent and intent not in seen:
            seen.add(intent)
            intents.append(intent)
    return intents
