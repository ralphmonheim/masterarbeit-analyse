"""Kompatibilitaetsuebersicht fuer die Schritte des Main-Process."""

from __future__ import annotations

from ma_workflow import list_main_process_steps


def main_process_step_rows() -> list[dict[str, object]]:
    """Bereitet Export, manuellen Simulationslauf und Import fuer die UI auf."""
    return [
        {
            "Schritt": step.label,
            "Modul": step.module_key,
            "Status": step.status,
            "Beschreibung": step.description,
        }
        for step in list_main_process_steps()
    ]
