"""Workflow-Tabellen fuer die zentrale Streamlit-Oberflaeche."""

from __future__ import annotations

from ma_workflow import list_workflow_steps


def workflow_step_rows() -> list[dict[str, object]]:
    """Bereitet den Gesamtworkflow fuer UI-Tabellen auf."""
    return [
        {
            "Phase": step.phase,
            "Schritt": step.label,
            "Modul": step.module_key,
            "Status": step.status,
            "Beschreibung": step.description,
        }
        for step in list_workflow_steps()
    ]
