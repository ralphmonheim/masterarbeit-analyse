import pytest

from ma_variants import OptionSet, OptionValue, Parameter, Variant, VariantValue


def test_parameter_model_requires_technical_key_and_flags():
    parameter = Parameter(
        parameter_key="heating_capacity_factor",
        display_name="Heizleistungsfaktor",
        category="hvac",
        parameter_class="sizing",
        option_set_key="heating_capacity_factors",
        unit="%",
        is_variant_relevant=True,
        is_naming_relevant=True,
        is_export_relevant=True,
    )

    assert parameter.parameter_key == "heating_capacity_factor"
    assert parameter.option_set_key == "heating_capacity_factors"
    assert parameter.is_variant_relevant is True


def test_option_models_keep_option_set_reference():
    option_set = OptionSet(
        option_set_key="heating_capacity_factors",
        display_name="Heizleistungsfaktoren",
        description="Reduzierte Heizleistungsstufen fuer Varianten.",
    )
    option_value = OptionValue(
        option_key="heating_capacity_80",
        option_set_key=option_set.option_set_key,
        label="80 Prozent",
        value=80,
        unit="%",
        is_active=True,
    )

    assert option_value.option_set_key == option_set.option_set_key
    assert option_value.value == 80


def test_variant_models_keep_parameter_and_option_references():
    variant = Variant(
        variant_key="var_heating_80",
        variant_name="Heizleistung 80 Prozent",
        status="draft",
    )
    variant_value = VariantValue(
        variant_key=variant.variant_key,
        parameter_key="heating_capacity_factor",
        option_key="heating_capacity_80",
        resolved_value=80,
    )

    assert variant_value.variant_key == variant.variant_key
    assert variant_value.resolved_value == 80


@pytest.mark.parametrize(
    "model_factory",
    [
        lambda: Parameter(
            parameter_key="",
            display_name="Heizleistungsfaktor",
            category="hvac",
            parameter_class="sizing",
            option_set_key="heating_capacity_factors",
            unit="%",
            is_variant_relevant=True,
            is_naming_relevant=True,
            is_export_relevant=True,
        ),
        lambda: OptionSet(
            option_set_key="",
            display_name="Heizleistungsfaktoren",
            description="Reduzierte Heizleistungsstufen fuer Varianten.",
        ),
        lambda: OptionValue(
            option_key="",
            option_set_key="heating_capacity_factors",
            label="80 Prozent",
            value=80,
            unit="%",
            is_active=True,
        ),
        lambda: Variant(
            variant_key="",
            variant_name="Heizleistung 80 Prozent",
            status="draft",
        ),
        lambda: VariantValue(
            variant_key="",
            parameter_key="heating_capacity_factor",
            option_key="heating_capacity_80",
            resolved_value=80,
        ),
    ],
)
def test_models_reject_empty_required_keys(model_factory):
    with pytest.raises(ValueError):
        model_factory()


def test_option_value_allows_zero_but_rejects_missing_value():
    option_value = OptionValue(
        option_key="heating_capacity_0",
        option_set_key="heating_capacity_factors",
        label="0 Prozent",
        value=0,
        unit="%",
        is_active=True,
    )

    assert option_value.value == 0

    with pytest.raises(ValueError):
        OptionValue(
            option_key="heating_capacity_missing",
            option_set_key="heating_capacity_factors",
            label="Fehlend",
            value=None,
            unit="%",
            is_active=True,
        )
