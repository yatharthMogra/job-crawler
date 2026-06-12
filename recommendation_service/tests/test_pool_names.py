from app.constants import normalize_pool_name, normalize_pool_names


def test_normalize_pool_name_intern_suffix() -> None:
    assert normalize_pool_name("SWE_INTERN") == "SWE_INTERNSHIP"
    assert normalize_pool_name("ML_ENGINEER_INTERN") == "ML_ENGINEER_INTERNSHIP"


def test_normalize_pool_name_unchanged() -> None:
    assert normalize_pool_name("SWE_FULLTIME") == "SWE_FULLTIME"
    assert normalize_pool_name("SWE_INTERNSHIP") == "SWE_INTERNSHIP"


def test_normalize_pool_names_dedupes() -> None:
    assert normalize_pool_names(["SWE_INTERN", "SWE_INTERNSHIP"]) == ["SWE_INTERNSHIP"]
