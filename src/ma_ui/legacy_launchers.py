"""Starter fuer bewusst getrennte Legacy-Oberflaechen."""

from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class LegacyLaunchResult:
    """Beschreibt den Startversuch einer externen Legacy-Oberflaeche."""

    command: tuple[str, ...]
    process_id: int | None
    error: str | None = None

    @property
    def success(self) -> bool:
        return self.error is None and self.process_id is not None


def build_tkinter_analyse_command(python_executable: str | None = None) -> tuple[str, ...]:
    """Baut den venv-kompatiblen Startbefehl fuer die bestehende Tkinter-Analyse."""
    return (python_executable or sys.executable, "-m", "ma_analyse", "gui")


def launch_tkinter_analyse(
    *,
    python_executable: str | None = None,
    cwd: Path | str | None = None,
) -> LegacyLaunchResult:
    """Startet die bestehende Tkinter-Analyse als separaten Prozess."""
    command = build_tkinter_analyse_command(python_executable)
    try:
        process = subprocess.Popen(command, cwd=str(cwd) if cwd is not None else None)  # noqa: S603
    except OSError as exc:
        return LegacyLaunchResult(command=command, process_id=None, error=str(exc))
    return LegacyLaunchResult(command=command, process_id=process.pid)
