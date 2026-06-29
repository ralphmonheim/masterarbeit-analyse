import pytest

from ma_analyse.app.cli import apply_plot_template_config_defaults, build_parser


def test_cli_parser_accepts_main_commands():
    parser = build_parser()

    assert parser.parse_args(["prepare"]).command == "prepare"
    assert parser.parse_args(["comfort"]).command == "comfort"
    assert parser.parse_args(["analyze-data"]).command == "analyze-data"
    assert parser.parse_args(["heating", "--view", "year"]).command == "heating"
    assert parser.parse_args(["cooling", "--view", "year"]).command == "cooling"
    assert parser.parse_args(["plot-template"]).command == "plot-template"
    assert parser.parse_args(["plot-template-examples"]).command == "plot-template-examples"
    assert parser.parse_args(["all"]).command == "all"


def test_cli_parser_rejects_removed_gui_command():
    parser = build_parser()

    with pytest.raises(SystemExit):
        parser.parse_args(["gui"])


def test_cli_parser_accepts_plot_template_options():
    parser = build_parser()

    args = parser.parse_args(
        [
            "plot-template",
            "--template",
            "heating-year",
            "--setpoint-min",
            "21",
            "--setpoint-max",
            "26",
            "--temperature-ymin",
            "-20",
            "--temperature-ymax",
            "40",
            "--outdoor-column",
            "tair",
            "--no-setpoint-band",
            "--no-outdoor-temperature",
            "--no-operative-temperature",
        ]
    )

    assert args.template == "heating-year"
    assert args.setpoint_min == 21
    assert args.setpoint_max == 26
    assert args.temperature_ymin == -20
    assert args.temperature_ymax == 40
    assert args.outdoor_column == "tair"
    assert args.show_setpoint_band is False
    assert args.show_outdoor_temperature is False
    assert args.show_operative_temperature is False
    assert args.output_root == "data/test_output"


def test_cli_parser_accepts_all_plot_template_views():
    parser = build_parser()

    templates = [
        "heating-year",
        "heating-overlay",
        "heating-month",
        "heating-week",
        "heating-day",
        "heating-bar",
        "cooling-year",
        "cooling-month",
        "cooling-week",
        "cooling-day",
        "cooling-absolute-year",
        "cooling-absolute-month",
        "cooling-absolute-week",
        "cooling-absolute-day",
        "cooling-bar",
        "comfort-plot",
        "comfort-plot-overview",
        "comfort-analysis",
        "comfort-analysis-overview",
        "energy-balance-year",
        "energy-balance-month",
        "energy-balance-week",
        "energy-balance-day",
        "thermal-room-climate-year",
        "thermal-room-climate-month",
        "thermal-room-climate-week",
        "thermal-room-climate-day",
        "internal-loads-year",
        "internal-loads-month",
        "internal-loads-week",
        "internal-loads-day",
        "internal-loads-monthly-sum",
        "internal-loads-room-comparison",
    ]

    for template in templates:
        args = parser.parse_args(["plot-template", "--template", template])
        assert args.template == template


def test_cli_parser_accepts_heating_overlay_template():
    parser = build_parser()
    args = parser.parse_args(["plot-template", "--template", "heating-overlay"])

    assert args.template == "heating-overlay"


def test_cli_applies_template_defaults_for_heating_year_and_overlay():
    parser = build_parser()

    year_args = parser.parse_args(["plot-template", "--template", "heating-year"])
    apply_plot_template_config_defaults(year_args, ["plot-template", "--template", "heating-year"])

    assert year_args.show_setpoint_band is False
    assert year_args.show_outdoor_temperature is False
    assert year_args.show_operative_temperature is False
    assert year_args.fixed_overlays == []

    overlay_args = parser.parse_args(["plot-template", "--template", "heating-overlay"])
    apply_plot_template_config_defaults(overlay_args, ["plot-template", "--template", "heating-overlay"])

    assert overlay_args.show_setpoint_band is True
    assert overlay_args.show_outdoor_temperature is True
    assert overlay_args.show_operative_temperature is True
    assert overlay_args.fixed_overlays[0]["id"] == "outdoor_temperature"


def test_cli_parser_uses_plot_template_config_defaults(tmp_path):
    config_file = tmp_path / "plot_templates.toml"
    config_file.write_text(
        "\n".join(
            [
                "[heating_year]",
                "setpoint_min = 19.0",
                "setpoint_max = 24.0",
                "temperature_ymin = -10.0",
                "temperature_ymax = 32.0",
                "show_setpoint_band = false",
                "show_outdoor_temperature = true",
                "show_operative_temperature = false",
                'outdoor_column = "tout"',
                "",
                "[[heating_year.default_overlays]]",
                'id = "outdoor_temperature"',
                'label = "Aussenluft tout"',
                'source = "aux"',
                'column = "tout"',
                'axis = "temperature"',
                "enabled = true",
            ]
        ),
        encoding="utf-8",
    )
    parser = build_parser(plot_template_config_path=config_file)

    args = parser.parse_args(["plot-template"])

    assert args.setpoint_min == 19
    assert args.setpoint_max == 24
    assert args.temperature_ymin == -10
    assert args.temperature_ymax == 32
    assert args.show_setpoint_band is False
    assert args.show_outdoor_temperature is True
    assert args.show_operative_temperature is False
    assert args.outdoor_column == "tout"
    assert args.fixed_overlays[0]["label"] == "Aussenluft tout"


def test_cli_parser_uses_plot_template_config_dir(tmp_path):
    config_dir = tmp_path / "plot_templates"
    config_dir.mkdir()
    config_file = config_dir / "heating_year.toml"
    config_file.write_text(
        "\n".join(
            [
                "setpoint_min = 19.0",
                "setpoint_max = 24.0",
                "temperature_ymin = -10.0",
                "temperature_ymax = 32.0",
                "show_setpoint_band = false",
                "show_outdoor_temperature = true",
                "show_operative_temperature = false",
                'outdoor_column = "tout"',
                "",
                "[[default_overlays]]",
                'id = "outdoor_temperature"',
                'label = "Aussenluft tout"',
                'source = "aux"',
                'column = "tout"',
                'axis = "temperature"',
                "enabled = true",
            ]
        ),
        encoding="utf-8",
    )

    parser = build_parser(plot_template_config_path=config_dir)

    args = parser.parse_args(["plot-template"])

    assert args.setpoint_min == 19
    assert args.setpoint_max == 24
    assert args.temperature_ymin == -10
    assert args.temperature_ymax == 32
    assert args.show_setpoint_band is False
    assert args.show_outdoor_temperature is True
    assert args.show_operative_temperature is False
    assert args.outdoor_column == "tout"
    assert args.fixed_overlays[0]["label"] == "Aussenluft tout"


def test_cli_applies_plot_template_config_from_runtime_argument(tmp_path):
    config_dir = tmp_path / "plot_templates"
    config_dir.mkdir()
    config_file = config_dir / "heating_year.toml"
    config_file.write_text(
        "\n".join(
            [
                "setpoint_min = 19.0",
                "setpoint_max = 24.0",
                "temperature_ymin = -10.0",
                "temperature_ymax = 32.0",
                "show_setpoint_band = false",
                "show_outdoor_temperature = true",
                "show_operative_temperature = false",
                'outdoor_column = "tout"',
                "",
                "[[default_overlays]]",
                'id = "outdoor_temperature"',
                'label = "Aussenluft tout"',
                'source = "aux"',
                'column = "tout"',
                'axis = "temperature"',
                "enabled = true",
            ]
        ),
        encoding="utf-8",
    )

    parser = build_parser()
    args = parser.parse_args(["plot-template", "--plot-template-config", str(config_dir)])
    apply_plot_template_config_defaults(args, ["plot-template", "--plot-template-config", str(config_dir)])

    assert args.setpoint_min == 19
    assert args.setpoint_max == 24
    assert args.temperature_ymin == -10
    assert args.temperature_ymax == 32
    assert args.show_setpoint_band is False
    assert args.show_outdoor_temperature is True
    assert args.show_operative_temperature is False
    assert args.outdoor_column == "tout"
    assert args.fixed_overlays[0]["label"] == "Aussenluft tout"
