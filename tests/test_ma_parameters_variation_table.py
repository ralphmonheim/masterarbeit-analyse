from types import SimpleNamespace

from ma_ui.streamlit_app.module_views.parameters_view import variation_span_table_rows


def test_variation_span_table_rows_lists_every_baseline_parameter_with_saved_values():
    baseline = SimpleNamespace(
        parameter_values=(
            SimpleNamespace(parameter_key="building_length_m", label="Gebaeudelaenge", value=17.0, unit="m"),
            SimpleNamespace(parameter_key="heating_setpoint_c", label="Heizsollwert", value=21.0, unit="degC"),
        )
    )

    rows = variation_span_table_rows(
        baseline,
        [
            {
                "parameter_key": "building_length_m",
                "minimum": 15.0,
                "maximum": 20.0,
                "step": 0.5,
                "enabled": True,
            }
        ],
    )

    assert rows == [
        {
            "parameter_key": "building_length_m",
            "label": "Gebaeudelaenge",
            "unit": "m",
            "reference_value": 17.0,
            "minimum": 15.0,
            "maximum": 20.0,
            "step": 0.5,
            "enabled": True,
        },
        {
            "parameter_key": "heating_setpoint_c",
            "label": "Heizsollwert",
            "unit": "degC",
            "reference_value": 21.0,
            "minimum": 21.0,
            "maximum": 21.0,
            "step": 1.0,
            "enabled": False,
        },
    ]
