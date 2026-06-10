"""Post-Process-Uebersicht fuer die zentrale Streamlit-Oberflaeche."""

from __future__ import annotations

from ma_workflow import list_post_process_steps


def post_process_step_rows() -> list[dict[str, object]]:
    """Bereitet die Post-Process-Schritte fuer UI-Tabellen auf."""
    return [
        {
            "Schritt": step.label,
            "Modul": step.module_key,
            "Status": step.status,
            "Beschreibung": step.description,
        }
        for step in list_post_process_steps()
    ]
