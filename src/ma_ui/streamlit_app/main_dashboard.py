"""Dashboard-Daten fuer die zentrale Streamlit-Oberflaeche."""

from __future__ import annotations

from ma_workflow import list_dashboard_actions


def dashboard_action_rows() -> list[dict[str, object]]:
    """Bereitet Dashboard-Aktionen fuer eine Statusuebersicht auf."""
    return [
        {
            "Aktion": action.action_key,
            "Beschriftung": action.label,
            "Schritt": action.step_key,
            "Modul": action.module_key,
            "Status": action.status,
            "Beschreibung": action.description,
        }
        for action in list_dashboard_actions()
    ]
