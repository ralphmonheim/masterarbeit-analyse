"""Kompatibilitaetsuebersicht fuer die frueheren Pre-Process-Schritte."""

from __future__ import annotations

from ma_workflow import list_pre_process_steps


def pre_process_step_rows() -> list[dict[str, object]]:
    """Bereitet den Pre-Process fuer bestehende UI-Aufrufer auf."""
    return [
        {
            "Schritt": step.label,
            "Modul": step.module_key,
            "Status": step.status,
            "Beschreibung": step.description,
        }
        for step in list_pre_process_steps()
    ]
