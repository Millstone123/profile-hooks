from profilehooks.checker import check_profiles


def test_default_profiles_pass():
    assert check_profiles("profiles") == []
