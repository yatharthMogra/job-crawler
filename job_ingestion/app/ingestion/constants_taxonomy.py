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
    "- OPERATIONS: business operations, program manager (non-TPM), RevOps, strategy\n"
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
    "- HARDWARE_ENGINEER: hardware engineer, mechanical engineer, electrical engineer, "
    "electronics engineer, manufacturing engineer, PCB/FPGA/embedded hardware roles "
    "(physical product, not software-only)\n"
    "- Prefer SYSTEMS_ENGINEER over SWE for aerospace/defense systems engineering titles; "
    "prefer HARDWARE_ENGINEER over OPERATIONS for engineering (not management) manufacturing "
    "roles\n"
    "- Use OTHER only when no taxonomy role fits; prefer specific roles over OTHER"
)

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
