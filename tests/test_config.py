from ma_analyse.core import config


def test_default_data_paths_live_under_data_dir():
    assert config.INPUT_DIR == "data/ma_analyse/ida_imports"
    assert config.DATENBANK_DIR == "data/ma_analyse/database"
    assert config.OUTPUT_DIR == "data/ma_analyse/output"
    assert config.TEST_OUTPUT_DIR == "data/test_output"
    assert config.LOG_DIR == "logs"


def test_settings_documents_live_next_to_settings_modules():
    assert config.COMMAND_DOC == config.DOCS_DIR / "ma_analyse" / "commands_analyse.md"
    assert config.NAMING_DOC == config.SETTINGS_DIR / "naming.md"
    assert config.OUTPUT_FORMATS_DOC == config.SETTINGS_DIR / "output_formats.md"
    assert config.SETTINGS_DIR == config.PACKAGE_DIR / "settings"
