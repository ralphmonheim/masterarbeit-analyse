from ma_analyse.preprocessing.prepare import normalize_variant_name, strip_variant_suffix


def test_variant_suffix_helpers():
    assert normalize_variant_name("Dimensionierung", "_rohdaten") == "Dimensionierung_rohdaten"
    assert normalize_variant_name("Dimensionierung_rohdaten", "_rohdaten") == "Dimensionierung_rohdaten"
    assert strip_variant_suffix("Dimensionierung_rohdaten") == "Dimensionierung"
    assert strip_variant_suffix("Dimensionierung_nutzdaten") == "Dimensionierung"
