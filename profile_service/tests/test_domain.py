from app.domain import derive_user_domains, is_valid_domain_pair


def test_software_aerospace_not_valid_pair() -> None:
    assert is_valid_domain_pair("Software", "Aerospace_Defense") is False


def test_derive_user_domains_software() -> None:
    primary, secondary = derive_user_domains(
        [
            "Backend Engineering",
            "Full Stack Development",
            "AI Systems",
            "Distributed Systems",
            "Cloud Infrastructure",
            "DevOps",
        ]
    )
    assert primary == "Software"
    assert secondary is None
