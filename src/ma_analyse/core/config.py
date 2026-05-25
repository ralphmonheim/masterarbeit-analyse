"""Gemeinsame Projektkonfiguration fuer Pfade, Raeume und Dateinamen."""

from __future__ import annotations

from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = PACKAGE_DIR.parent
PROJECT_ROOT = SRC_DIR.parent
DOCS_DIR = PROJECT_ROOT / "docs"
SETTINGS_DIR = PACKAGE_DIR / "settings"
COMMAND_DOC = DOCS_DIR / "commands.md"
NAMING_DOC = SETTINGS_DIR / "naming.md"
OUTPUT_FORMATS_DOC = SETTINGS_DIR / "output_formats.md"
PLOT_TEMPLATES_CONFIG = SETTINGS_DIR / "plot_templates.toml"

INPUT_DIR = "data/input"
DATENBANK_DIR = "data/database"
OUTPUT_DIR = "data/output"
TEST_OUTPUT_DIR = "data/test_output"
LOG_DIR = "logs"

ROOMS = [
    "101 lobby",
    "109 office",
    "113 meeting",
    "208 office",
    "214 meeting",
]

PRN_FILES = [
    "HEAT_BALANCE.prn",
    "IAQ.prn",
    "LOCAL-DE-COMF-DIAG-T.prn",
    "TEMPERATURES.prn",
    "ZONE-ENERGY.prn",
]

TIME_COLUMN = "time"
RELHUM_FILE = "IAQ.prn"
RELHUM_COLUMN = "relhum"
TARGET_HOURS = 8760
EXPORT_FORMATS = ("csv", "excel", "both")
ROOM_FILE_EXTENSIONS = {
    "csv": ".csv",
    "excel": ".xlsx",
}

ROOM_FILE_EXTENSION = ".csv"
RUN_FOLDER_SUFFIX = "_output"
COMBINED_HEATING_OUTPUT_DIR = "CombinedHeatingPlots"
COMBINED_COOLING_OUTPUT_DIR = "CombinedCoolingPlots"

MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
MONTH_DAY_COUNTS = {
    "Jan": 31,
    "Feb": 28,
    "Mar": 31,
    "Apr": 30,
    "May": 31,
    "Jun": 30,
    "Jul": 31,
    "Aug": 31,
    "Sep": 30,
    "Oct": 31,
    "Nov": 30,
    "Dec": 31,
}
MAX_CALENDAR_WEEK = 52
