"""Map normalized job roles to H-1B pool_family for summary lookup."""

from __future__ import annotations

ROLE_TO_H1B_POOL_FAMILY: dict[str, str] = {
    # SWE family
    "SWE": "SWE",
    "BACKEND_ENGINEER": "SWE",
    "FRONTEND_ENGINEER": "SWE",
    "FULLSTACK_ENGINEER": "SWE",
    "MOBILE_ENGINEER": "SWE",
    "ML_ENGINEER": "SWE",
    "SOLUTIONS_ENGINEER": "SWE",
    # Data
    "DATA_SCIENTIST": "DATA_SCIENTIST",
    "DATA_ENGINEER": "DATA_ENGINEER",
    "DATA_ANALYST": "DATA_ANALYST",
    # Infrastructure / security
    "DEVOPS_ENGINEER": "DEVOPS_ENGINEER",
    "SECURITY_ENGINEER": "SECURITY_ENGINEER",
    "SUPPORT_ENGINEER": "SUPPORT_ENGINEER",
    # Management
    "TECHNICAL_PROGRAM_MANAGER": "TECHNICAL_PROGRAM_MANAGER",
    # Hardware / systems
    "HARDWARE_ENGINEER": "HARDWARE_ENGINEER",
    "SYSTEMS_ENGINEER": "SYSTEMS_ENGINEER",
    "AEROSPACE_ENGINEER": "AEROSPACE_ENGINEER",
    "CONTROLS_ENGINEER": "SYSTEMS_ENGINEER",
    "FIELD_SERVICE_ENGINEER": "HARDWARE_ENGINEER",
    # Research
    "RESEARCH_SCIENTIST": "RESEARCH_SCIENTIST",
    "LIFE_SCIENTIST": "RESEARCH_SCIENTIST",
}


def pool_family_from_roles(normalized_roles: list[str]) -> str | None:
    """Return the best H-1B pool_family for a job's normalized roles."""
    for role in normalized_roles:
        pool = ROLE_TO_H1B_POOL_FAMILY.get(role)
        if pool:
            return pool
    return None
