"""UI-neutrale Zustandslogik fuer die ma_analyse-Bedienung.

Die Regeln spiegeln die bestehende Tkinter-GUI, ohne Tkinter oder Streamlit zu
importieren. So kann die Streamlit-Oberflaeche dieselben Entscheidungen nutzen,
ohne fachliche Analysefunktionen in die UI zu verschieben.
"""

from __future__ import annotations

from dataclasses import dataclass

from .analysis.templates import HEATING_YEAR_TEMPLATE

COMMAND_OPTIONS = ("prepare", "comfort", "analyze_data", "heating", "cooling", "plot-template", "all")
ANALYSIS_SCOPE_OPTIONS = ("Eine Variante", "Mehrere Varianten", "Alle Varianten")
PLOT_TEMPLATE_SCOPE_OPTIONS = ("Eine Variante", "Mehrere Varianten")
EXPORT_FORMAT_OPTIONS = ("csv", "excel", "both")
COMFORT_OUTPUT_OPTIONS = ("plot", "plot_analysis", "plot_overview", "plot_analysis_overview")
COMFORT_ANALYSIS_LEVEL_OPTIONS = ("Analyse Raum", "Analyse Variante")
LOAD_SUBCOMMAND_OPTIONS = ("bar", "timeline")
LOAD_VIEW_OPTIONS = ("year", "month", "week", "day")
VARIANT_MODE_OPTIONS = ("single", "compare")
SERIES_LAYOUT_OPTIONS = ("separate", "combined")

COMMAND_TO_STEPS = {
    "prepare": ("prepare",),
    "comfort": (),
    "analyze_data": ("analyze",),
    "heating": ("heating",),
    "cooling": ("cooling",),
    "plot-template": ("plot_template",),
    "all": ("overview", "analysis", "heating", "cooling"),
}

COMFORT_ALLOWED_BY_LEVEL = {
    "Analyse Raum": ("plot", "plot_analysis"),
    "Analyse Variante": ("plot_overview", "plot_analysis_overview"),
}

WIZARD_STEP_ORDER = (
    "command",
    "subcommand",
    "prepare_export",
    "options",
    "overlays",
    "analysis_scope",
    "variants",
    "rooms",
)


@dataclass(frozen=True)
class AnalysisWizardState:
    """Beschreibt den aktuellen Bedienzustand ohne konkrete UI-Technik."""

    command: str = ""
    load_subcommand: str = ""
    prepare_export_format: str = ""
    comfort_type: str = ""
    analysis_level: str = ""
    variant_mode: str = ""
    series_layout: str = ""
    view: str = ""
    month: str | None = None
    week: int | None = None
    day: int | None = None
    plot_template: str = HEATING_YEAR_TEMPLATE
    analysis_scope: str = ""
    selected_variants: tuple[str, ...] = ()
    selected_rooms: tuple[str, ...] = ()
    variant_count: int = 0
    overlay_count: int = 0
    show_setpoint_band: bool = False
    show_outdoor_temperature: bool = False
    show_operative_temperature: bool = False


def command_label(command: str) -> str:
    """Gibt den Befehl so zurueck, wie er in Tkinter gefuehrt wird."""
    labels = {
        "prepare": "prepare - Rohdaten aufbereiten",
        "comfort": "comfort - Komfortausgaben",
        "analyze_data": "analyze_data - Excel-Auswertung",
        "heating": "heating - Heizleistung",
        "cooling": "cooling - Kuehlleistung",
        "plot-template": "plot-template - Diagrammvorlagen",
        "all": "all - Standardprofil",
    }
    return labels.get(command, "Bitte waehlen")


def normalize_command(command: str) -> str:
    """Normalisiert alte UI-Schreibweisen auf die Tkinter-Schreibweise."""
    aliases = {
        "analysis": "analyze_data",
        "analyze-data": "analyze_data",
    }
    return aliases.get(command, command)


def visible_analysis_steps(
    state: AnalysisWizardState,
    *,
    template_supports_overlays: bool = False,
) -> tuple[str, ...]:
    """Ermittelt die sichtbaren Wizard-Schritte nach Tkinter-Regeln."""
    selected_command = normalize_command(state.command)
    if not selected_command:
        return ("command",)

    is_prepare = selected_command == "prepare"
    show_subcommands = selected_command in {"comfort", "heating", "cooling"}
    load_without_subcommand = selected_command in {"heating", "cooling"} and state.load_subcommand not in {
        "bar",
        "timeline",
    }
    hide_options_step = selected_command in {"prepare", "all"} or load_without_subcommand

    steps = ["command"]
    if show_subcommands:
        steps.append("subcommand")
    if is_prepare:
        steps.append("prepare_export")
    if not hide_options_step:
        steps.append("options")
    if selected_command == "plot-template" and template_supports_overlays:
        steps.append("overlays")

    steps.extend(("analysis_scope", "variants"))
    if not is_prepare:
        steps.append("rooms")
    return tuple(steps)


def allowed_comfort_outputs(analysis_level: str) -> tuple[str, ...]:
    """Begrenzt Comfort-Unterbefehle wie in Tkinter nach Analyseebene."""
    return COMFORT_ALLOWED_BY_LEVEL.get(analysis_level, COMFORT_ALLOWED_BY_LEVEL["Analyse Raum"])


def time_selection_complete(view: str, month: str | None, week: int | None, day: int | None) -> bool:
    """Prueft, ob die benoetigte Zeitwahl fuer eine Ansicht vorhanden ist."""
    if view == "month":
        return bool(month)
    if view == "week":
        return week is not None
    if view == "day":
        return bool(month) and day is not None
    return True


def analysis_step_complete(
    state: AnalysisWizardState,
    step: str,
    *,
    template_view: str = "",
    room_selection_disabled: bool = False,
) -> bool:
    """Prueft, ob der aktuelle Schritt ausreichend ausgefuellt ist."""
    command = normalize_command(state.command)
    if step == "command":
        return command in COMMAND_OPTIONS
    if step == "subcommand":
        if command == "comfort":
            return state.comfort_type in allowed_comfort_outputs(state.analysis_level)
        if command in {"heating", "cooling"}:
            return state.load_subcommand in LOAD_SUBCOMMAND_OPTIONS
        return True
    if step == "prepare_export":
        return state.prepare_export_format in EXPORT_FORMAT_OPTIONS
    if step == "options":
        if command == "plot-template":
            return bool(state.plot_template) and time_selection_complete(
                template_view,
                state.month,
                state.week,
                state.day,
            )
        if command == "comfort":
            return state.analysis_level in COMFORT_ANALYSIS_LEVEL_OPTIONS
        if command == "analyze_data":
            return state.series_layout in SERIES_LAYOUT_OPTIONS
        if command in {"heating", "cooling"}:
            if state.variant_mode not in VARIANT_MODE_OPTIONS:
                return False
            if state.variant_mode == "compare" and state.series_layout not in SERIES_LAYOUT_OPTIONS:
                return False
            if state.load_subcommand == "timeline":
                return state.view in LOAD_VIEW_OPTIONS and time_selection_complete(
                    state.view,
                    state.month,
                    state.week,
                    state.day,
                )
            return True
        return True
    if step == "overlays":
        return True
    if step == "analysis_scope":
        scope_options = PLOT_TEMPLATE_SCOPE_OPTIONS if command == "plot-template" else ANALYSIS_SCOPE_OPTIONS
        return state.analysis_scope in scope_options
    if step == "variants":
        if state.analysis_scope == "Alle Varianten" and command != "plot-template":
            return state.variant_count > 0
        return bool(state.selected_variants)
    if step == "rooms":
        return room_selection_disabled or bool(state.selected_rooms)
    return False


def first_incomplete_step(
    state: AnalysisWizardState,
    visible_steps: tuple[str, ...],
    *,
    template_view: str = "",
    room_selection_disabled: bool = False,
) -> str:
    """Findet den naechsten offenen Schritt."""
    for step in visible_steps:
        if not analysis_step_complete(
            state,
            step,
            template_view=template_view,
            room_selection_disabled=room_selection_disabled,
        ):
            return step
    return visible_steps[-1]


def analysis_step_summary(
    state: AnalysisWizardState,
    step: str,
    *,
    template_view: str = "",
) -> str:
    """Baut eine kurze Zusammenfassung wie die rechte Tkinter-Karte."""
    command = normalize_command(state.command)
    if step == "command" and command:
        return f"Befehl: {command}"
    if step == "subcommand":
        if command == "comfort" and state.comfort_type:
            return f"Unterbefehl: {state.comfort_type}"
        if command in {"heating", "cooling"} and state.load_subcommand:
            return f"Unterbefehl: {state.load_subcommand}"
    if step == "prepare_export" and state.prepare_export_format:
        return f"Exportformat: {state.prepare_export_format}"
    if step == "options":
        if command == "plot-template":
            template_label = state.plot_template
            if template_view == "month":
                return f"Template: {template_label}, Monat {state.month}"
            if template_view == "week":
                return f"Template: {template_label}, KW {state.week}"
            if template_view == "day":
                return f"Template: {template_label}, {state.day}. {state.month}"
            return f"Template: {template_label}"
        if command == "comfort" and state.analysis_level:
            return f"Analyseebene: {state.analysis_level}"
        if command == "analyze_data" and state.series_layout:
            return f"Excel-Ausgabe: {state.series_layout}"
        if command in {"heating", "cooling"}:
            parts = []
            if state.variant_mode:
                parts.append(f"Modus {state.variant_mode}")
            if state.variant_mode == "compare" and state.series_layout:
                parts.append(f"Ausgabe {state.series_layout}")
            if state.load_subcommand == "timeline" and state.view:
                view_label = state.view
                if state.view == "month":
                    view_label = f"month {state.month}"
                elif state.view == "week":
                    view_label = f"week KW {state.week}"
                elif state.view == "day":
                    view_label = f"day {state.month} {state.day}"
                parts.append(f"Ansicht {view_label}")
            return f"Optionen: {', '.join(parts)}" if parts else ""
    if step == "overlays":
        parts = []
        if state.show_setpoint_band:
            parts.append("Sollwertband")
        if state.show_outdoor_temperature:
            parts.append("Aussenluft")
        if state.show_operative_temperature:
            parts.append("Operative Temperatur")
        if state.overlay_count:
            line_label = "freie Linie" if state.overlay_count == 1 else "freie Linien"
            parts.append(f"{state.overlay_count} {line_label}")
        return f"Ueberlagerungen: {', '.join(parts)}" if parts else "Ueberlagerungen: Standard"
    if step == "analysis_scope" and state.analysis_scope:
        return f"Analyseumfang: {state.analysis_scope}"
    if step == "variants":
        if state.analysis_scope == "Alle Varianten" and command != "plot-template":
            return f"Varianten: alle ({state.variant_count})"
        return _selection_summary("Variante", "Varianten", state.selected_variants)
    if step == "rooms":
        return _selection_summary("Raum", "Raeume", state.selected_rooms)
    return ""


def _selection_summary(singular_label: str, plural_label: str, values: tuple[str, ...]) -> str:
    if not values:
        return ""
    if len(values) == 1:
        return f"{singular_label}: {values[0]}"
    return f"{plural_label}: {len(values)} ausgewaehlt"
