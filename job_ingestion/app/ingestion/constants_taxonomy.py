"""Shared taxonomy lists — must match profile_service capability prompt and recommendation spec."""

NORMALIZED_ROLES = [
    # Engineering
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
    "FIELD_SERVICE_ENGINEER",
    "CONTROLS_ENGINEER",
    "AEROSPACE_ENGINEER",
    "RESEARCH_SCIENTIST",
    "LIFE_SCIENTIST",
    "TECHNICAL_PROGRAM_MANAGER",
    # Product & design
    "PRODUCT_MANAGER",
    "PRODUCT_DESIGNER",
    # Data
    "DATA_ANALYST",
    # Go-to-market
    "SALES",
    "CUSTOMER_SUCCESS",
    "SOLUTIONS_CONSULTANT",
    "PARTNERSHIPS",
    "MARKETING",
    # Business operations
    "OPERATIONS",
    "RECRUITING",
    "FINANCE",
    "LEGAL",
    # Fallback
    "OTHER",
]

ENGINEERING_ROLES = frozenset(
    {
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
        "FIELD_SERVICE_ENGINEER",
        "CONTROLS_ENGINEER",
    }
)

ROLE_CLASSIFICATION_RULES = (
    "Role classification hints (use title + department + description):\n"
    "- SALES: account executive, BDR, SDR, sales manager, commercial/enterprise sales\n"
    "- CUSTOMER_SUCCESS: customer success manager, CSM, customer activation/enablement\n"
    "- SOLUTIONS_CONSULTANT: solutions consultant, deployment strategist, professional "
    "services consultant, engagement manager (client-facing, not pre-sales engineering)\n"
    "- SOLUTIONS_ENGINEER: solutions/sales engineer, pre-sales engineer (technical demo/PoC)\n"
    "- PARTNERSHIPS: partnerships, channel/alliance/ecosystem manager\n"
    "- MARKETING: marketing, growth, demand gen, brand, product marketing\n"
    "- OPERATIONS: project/program/PMO management, business operations, RevOps — when "
    "job_domain is Management, assign OPERATIONS for PM roles (enables Business secondary "
    "domain). NOT for people leadership or home care / nursing home managers\n"
    "- RECRUITING: recruiter, sourcer, people partner, talent acquisition\n"
    "- FINANCE: finance, accounting, FP&A, revenue analyst, controller\n"
    "- LEGAL: counsel, legal, compliance, GRC, privacy\n"
    "- PRODUCT_DESIGNER: product/UX/UI/brand/visual/motion designer\n"
    "- TECHNICAL_PROGRAM_MANAGER: technical program manager, TPM\n"
    "- DATA_ANALYST: data analyst, business analyst, analytics analyst (not data scientist)\n"
    "- SUPPORT_ENGINEER: support engineer, incident management engineer, technical support\n"
    "- SYSTEMS_ENGINEER: systems engineer integrating complex hardware/software systems in "
    "aerospace, defense, or industrial contexts (integration/V&V focus). NOT platform "
    "engineer or distributed systems engineer at tech companies — use DEVOPS_ENGINEER or "
    "BACKEND_ENGINEER for those\n"
    "- AEROSPACE_ENGINEER: aerospace vehicle/system design — structural, propulsion, "
    "aerodynamics, flight dynamics, propulsion. NOT software engineers at aerospace companies\n"
    "- RESEARCH_SCIENTIST: research scientist, principal/staff scientist, scientist I/II/III, "
    "research engineer in a lab context, postdoctoral researcher, research fellow\n"
    "- LIFE_SCIENTIST: bioscientist, biochemist, biologist, chemist, biomedical scientist, "
    "lab scientist, research associate in biosciences. Use RESEARCH_SCIENTIST for broader "
    "research roles\n"
    "- HARDWARE_ENGINEER: hardware engineer, electrical engineer, electronics engineer, "
    "PCB/FPGA/embedded hardware roles (physical product, not software-only). For pure "
    "mechanical design at Mechanical domain companies, still use HARDWARE_ENGINEER\n"
    "- FIELD_SERVICE_ENGINEER: field service engineer/technician, on-site installation and "
    "repair of hardware/industrial equipment (NOT IT helpdesk — use SUPPORT_ENGINEER for that)\n"
    "- CONTROLS_ENGINEER: controls engineer, automation engineer, PLC/SCADA, Industry 4.0, "
    "process control, manufacturing automation — use when job_domain is Industrial_Automation\n"
    "- Prefer SYSTEMS_ENGINEER over SWE for aerospace/defense systems engineering titles; "
    "prefer HARDWARE_ENGINEER over OPERATIONS for engineering (not management) manufacturing "
    "roles\n"
    "- Use OTHER only when no taxonomy role fits; prefer specific roles over OTHER"
)

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

_VALID_ROLE_INTENTS = frozenset(ROLE_INTENTS)

ROLE_INTENT_PROMPT_RULES = (
    "role_intent: The primary CAREER TRACK of this role — what kind of professional is being "
    "hired? Choose exactly one value from the taxonomy.\n"
    f"- Taxonomy: {', '.join(ROLE_INTENTS)}\n"
    "- engineer — building, developing, shipping software/systems hands-on\n"
    "- researcher — research as primary output (research scientist, R&D, lab work)\n"
    "- consultant — advising or implementing for clients as a service\n"
    "- educator — teaching or training others as the primary function\n"
    "- manager — coordination/leadership as primary function (EM, PM, TPM, ops leadership)\n"
    "- analyst — analysis/reporting focus (business analyst, data analyst, financial analyst)\n"
    "- accountant / auditor / investment_banker — finance track roles\n"
    "- sales — revenue/sales as primary function (AE, BDR, SDR, enterprise sales)\n"
    "- operations — business operations, RevOps, PMO, supply chain (non-engineering)\n"
    "- legal — counsel, compliance, GRC, privacy\n"
    "- other — does not fit any category above\n\n"
    "Critical disambiguation:\n"
    '"Technical Instructor (AWS Machine Learning)" → educator\n'
    '"Data Engineering Instructor" → educator\n'
    '"Machine Learning Engineer" → engineer\n'
    '"Research Data Scientist" → researcher (or engineer if shipping production systems)\n'
    '"Data Analyst" / "Business Analyst" → analyst\n'
    '"Enterprise Sales Engineer" (quota-carrying sales) → sales\n'
    '"Solutions Engineer" (technical demo/PoC) → engineer\n'
    '"Solutions Consultant" (client advisory) → consultant\n'
    '"Engineering Manager" with people-management focus → manager\n\n'
    "requires_clearance:\n"
    "- true ONLY when the posting requires an ACTIVE, EXISTING clearance at time of application "
    '("must hold TS/SCI", "active Secret clearance required", "existing clearance required")\n'
    "- false when clearance is sponsorable, preferred, or obtainable "
    '("clearance sponsorship available", "clearance preferred", "must be able to obtain clearance")\n'
    "- false when clearance is not mentioned"
)


def coerce_role_intent(value: object) -> str:
    if value is None:
        return "other"
    normalized = str(value).strip().lower().replace(" ", "_").replace("-", "_")
    if normalized in _VALID_ROLE_INTENTS:
        return normalized
    return "other"


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
