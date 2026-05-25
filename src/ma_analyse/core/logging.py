"""Schreibt pro CLI-Lauf eine Logdatei, ohne die Konsolenausgabe zu verschlucken."""

from __future__ import annotations

import contextlib
import sys
import time
import traceback
from datetime import datetime
from pathlib import Path
from typing import TextIO

from .config import LOG_DIR

LOGGED_COMMANDS = {
    "prepare",
    "comfort",
    "analyze-data",
    "analyze_data",
    "heating",
    "cooling",
    "plot-template",
    "all",
}


class TeeStream:
    """Schreibt Ausgaben gleichzeitig in die Konsole und in eine Logdatei."""

    def __init__(self, console_stream: TextIO, log_stream: TextIO):
        self.console_stream = console_stream
        self.log_stream = log_stream

    def write(self, text: str) -> int:
        self.console_stream.write(text)
        self.log_stream.write(text)
        return len(text)

    def flush(self) -> None:
        self.console_stream.flush()
        self.log_stream.flush()


def should_log_command(command_name: str | None) -> bool:
    """Entscheidet, ob ein CLI-Befehl als Analyse-Lauf geloggt wird."""
    return command_name in LOGGED_COMMANDS


def format_duration(seconds: float) -> str:
    """Formatiert Laufzeiten lesbar fuer Konsole und Logdatei."""
    if seconds < 60:
        return f"{seconds:.2f} s"

    minutes, remaining_seconds = divmod(seconds, 60)
    if minutes < 60:
        return f"{int(minutes)} min {remaining_seconds:.2f} s"

    hours, remaining_minutes = divmod(minutes, 60)
    return f"{int(hours)} h {int(remaining_minutes)} min {remaining_seconds:.2f} s"


def build_log_file_path(command_name: str, log_root: str | Path = LOG_DIR, timestamp: datetime | None = None) -> Path:
    """Erzeugt den Dateipfad fuer eine neue Logdatei."""
    if timestamp is None:
        timestamp = datetime.now()
    safe_command = command_name.replace("_", "-")
    return Path(log_root) / f"{timestamp.strftime('%Y-%m-%d_%H%M%S')}_{safe_command}.log"


@contextlib.contextmanager
def timed_step(step_name: str):
    """Misst einen Auswertungsschritt und schreibt die Laufzeit in die Ausgabe."""
    start_time = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start_time
        print(f"Laufzeit Schritt '{step_name}': {format_duration(elapsed)}")


@contextlib.contextmanager
def command_log(command_name: str, log_root: str | Path = LOG_DIR):
    """Kontextmanager, der stdout/stderr in eine Lauf-Logdatei spiegelt."""
    log_file_path = build_log_file_path(command_name, log_root=log_root)
    log_file_path.parent.mkdir(parents=True, exist_ok=True)
    start_perf = time.perf_counter()
    start_timestamp = datetime.now()

    with log_file_path.open("w", encoding="utf-8") as log_file:
        log_file.write("=" * 70 + "\n")
        log_file.write(f"ma_analyse Log: {command_name}\n")
        log_file.write(f"Start: {start_timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n")
        log_file.write("=" * 70 + "\n\n")

        stdout = TeeStream(sys.stdout, log_file)
        stderr = TeeStream(sys.stderr, log_file)
        try:
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                yield log_file_path
        except BaseException:
            log_file.write("\n" + "=" * 70 + "\n")
            log_file.write("FEHLER\n")
            log_file.write("=" * 70 + "\n")
            traceback.print_exc(file=log_file)
            raise
        finally:
            elapsed = time.perf_counter() - start_perf
            log_file.write("\n" + "=" * 70 + "\n")
            log_file.write(f"Ende: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            log_file.write(f"Gesamtlaufzeit: {format_duration(elapsed)}\n")
            log_file.write("=" * 70 + "\n")
