from ma_analyse.app.cli import build_parser


def test_cli_parser_accepts_main_commands():
    parser = build_parser()

    assert parser.parse_args(["prepare"]).command == "prepare"
    assert parser.parse_args(["comfort"]).command == "comfort"
    assert parser.parse_args(["analyze-data"]).command == "analyze-data"
    assert parser.parse_args(["heating", "--view", "year"]).command == "heating"
    assert parser.parse_args(["cooling", "--view", "year"]).command == "cooling"
    assert parser.parse_args(["all"]).command == "all"
