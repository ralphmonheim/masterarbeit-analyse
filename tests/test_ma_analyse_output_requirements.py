import pytest

from ma_analyse import default_output_requirements, select_output_requirements


def test_output_requirement_selection_is_owned_by_analysis_and_keeps_catalog_order():
    selected = select_output_requirements(("OUT-PEAK", "OUT-LOAD"))

    assert [profile.profile_id for profile in selected] == ["OUT-LOAD", "OUT-PEAK"]
    assert {profile.profile_id for profile in default_output_requirements()} == {
        "OUT-LOAD",
        "OUT-COMFORT",
        "OUT-PEAK",
    }


@pytest.mark.parametrize("profile_ids", [(), ("OUT-LOAD", "OUT-LOAD"), ("OUT-UNKNOWN",)])
def test_output_requirement_selection_rejects_missing_duplicate_or_unknown_profiles(profile_ids):
    with pytest.raises(ValueError):
        select_output_requirements(profile_ids)
