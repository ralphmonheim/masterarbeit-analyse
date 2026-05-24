"""Gemeinsame Projektkonfiguration fuer Pfade, Raeume und Dateinamen."""

from __future__ import annotations

from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent
SRC_DIR = PACKAGE_DIR.parent
PROJECT_ROOT = SRC_DIR.parent.parent
SUPPORT_DOC_DIR = PROJECT_ROOT / "Skripte" / "Unterstützung"
COMMAND_DOC = PROJECT_ROOT / "Skripte" / "0_Befehle.md"

INPUT_DIR = "0_Input"
DATENBANK_DIR = "1_Datenbank"
OUTPUT_DIR = "2_Output"
TEST_OUTPUT_DIR = "9_test_"

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
