"""Kompatibilitaetsuebersicht fuer die frueheren Post-Process-Schritte."""

from __future__ import annotations

from ma_workflow import list_post_process_steps


def post_process_step_rows() -> list[dict[str, object]]:
    """Bereitet die Phasen 4 und 5 fuer bestehende UI-Aufrufer auf."""
    return [
        {
            "Schritt": step.label,
            "Modul": step.module_key,
            "Status": step.status,
            "Beschreibung": step.description,
        }
        for step in list_post_process_steps()
    ]
