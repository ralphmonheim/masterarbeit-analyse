"""UI-neutral helpers for the analysis command wizard.

The module intentionally contains no Streamlit or Tkinter imports. It describes
which analysis steps are relevant for each command and keeps selection handling
consistent across UIs.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

COMMAND_OPTIONS: tuple[str, ...] = (
    "prepare",
    "comfort",
    "analyze_data",
    "heating",
    "cooling",
    "plot-template",
    "plot-template-analyse",
    "plot-template-weather",
    "all",
)
STREAMLIT_COMMAND_OPTIONS: tuple[str, ...] = tuple(
    command for command in COMMAND_OPTIONS if command not in {"all", "plot-template", "plot-template-weather"}
)

ANALYSIS_SECTION_ORDER: tuple[str, ...] = (
    "command",
    "subcommand",
    "template_diagram",
    "variants",
    "rooms",
    "overlays",
    "export",
    "run",
)

VARIANT_SCOPE_OPTIONS: tuple[str, ...] = (
    "Eine Variante",
    "Mehrere Varianten",
    "Alle Varianten",
)
ROOM_SCOPE_OPTIONS: tuple[str, ...] = (
    "Ein Raum",
    "Mehrere Räume",
    "Alle Räume",
)

# Backwards-compatible names used by older tests and UI code.
ANALYSIS_SCOPE_OPTIONS = VARIANT_SCOPE_OPTIONS
PLOT_TEMPLATE_SCOPE_OPTIONS = VARIANT_SCOPE_OPTIONS

EXPORT_FORMAT_OPTIONS: tuple[str, ...] = ("csv", "excel", "both")
COMFORT_SUBCOMMAND_OPTIONS: tuple[str, ...] = ("t_op_rel_hum",)
COMFORT_SUBCOMMAND_LABELS: dict[str, str] = {
    "t_op_rel_hum": "t_op / rel_hum",
}
COMFORT_OUTPUT_OPTIONS: tuple[str, ...] = (
    "plot",
    "plot_analysis",
    "plot_overview",
    "plot_analysis_overview",
)
LOAD_SUBCOMMAND_OPTIONS: tuple[str, ...] = ("bar", "timeline")
LOAD_VIEW_OPTIONS: tuple[str, ...] = ("year", "month", "week", "day")
PLOT_TEMPLATE_MODE_OPTIONS: tuple[str, ...] = ("single", "compare")
AXIS_RANGE_MODE_OPTIONS: tuple[str, ...] = ("automatic", "manual")
PLOT_TEMPLATE_ANALYSIS_GROUP_OPTIONS: tuple[str, ...] = (
    "comfort",
    "heating",
    "cooling",
    "energy-balance",
    "internal-loads",
    "thermal-room-climate",
)
VARIANT_MODE_OPTIONS: tuple[str, ...] = ("single", "compare")
SERIES_LAYOUT_OPTIONS: tuple[str, ...] = ("separate", "combined")

# Legacy constant kept so external imports do not break. Comfort no longer uses
# a separate analysis level in the active wizard.
COMFORT_ANALYSIS_LEVEL_OPTIONS: tuple[str, ...] = ("Analyse Raum", "Analyse Variante")
COMFORT_ALLOWED_BY_LEVEL: dict[str, set[str]] = {
    "Analyse Raum": set(COMFORT_OUTPUT_OPTIONS),
    "Analyse Variante": set(COMFORT_OUTPUT_OPTIONS),
}


@dataclass(frozen=True)
class AnalysisWizardState:
    command: str = ""
    comfort_subcommand: str = ""
    plot_template_group: str = ""
    load_subcommand: str = ""
    prepare_export_format: str = ""
    comfort_type: str = ""
    analysis_level: str = ""
    variant_mode: str = ""
    plot_template_mode: str = ""
    series_layout: str = ""
    view: str = ""
    month: str = ""
    week: str = ""
    day: str = ""
    plot_template: str = ""
    analysis_scope: str = ""
    room_scope: str = ""
    selected_variants: tuple[str, ...] = ()
    selected_rooms: tuple[str, ...] = ()
    variant_count: int = 0
    room_count: int = 0
    overlay_count: int = 0
    show_setpoint_band: bool = False
    show_outdoor_temperature: bool = False
    show_operative_temperature: bool = False
    overlay_enabled: bool = False
    primary_axis_mode: str = "automatic"
    primary_ymin: float | None = None
    primary_ymax: float | None = None
    secondary_axis_mode: str = "automatic"
    secondary_ymin: float | None = None
    secondary_ymax: float | None = None


def normalize_command(command: str | None, *, streamlit: bool = False) -> str:
    """Return a supported command or a sensible default."""

    allowed = STREAMLIT_COMMAND_OPTIONS if streamlit else COMMAND_OPTIONS
    if streamlit and command == "plot-template":
        return "plot-template-analyse"
    if command in allowed:
        return str(command)
    return "plot-template-analyse" if streamlit else ""


def backend_command(command: str) -> str:
    """Map UI command names to the existing ma_analyse backend command."""

    if command == "plot-template-analyse":
        return "plot-template"
    return command


def command_label(command: str) -> str:
    labels = {
        "prepare": "Daten vorbereiten",
        "comfort": "Komfortanalyse",
        "analyze_data": "Datenanalyse",
        "heating": "Heizleistung",
        "cooling": "Kühlung",
        "plot-template": "Plot-Template",
        "plot-template-analyse": "Plot-Template Analyse",
        "plot-template-weather": "Plot-Template Wetter",
        "all": "Kompletter Ablauf",
    }
    return labels.get(command, command or "Befehl wählen")


def section_label(section: str) -> str:
    labels = {
        "command": "Befehl",
        "subcommand": "Unterbefehl",
        "export": "Export / Ausgabe",
        "template_diagram": "Template / Diagramm",
        "variants": "Varianten",
        "rooms": "Räume",
        "overlays": "Overlay",
        "run": "Analyse starten",
    }
    return labels.get(section, section)


def section_relevant(command_or_state: str | AnalysisWizardState, section: str) -> bool:
    """Return whether a wizard section is relevant for the selected command."""

    state = command_or_state if isinstance(command_or_state, AnalysisWizardState) else None
    command = state.command if state is not None else command_or_state
    if section == "command":
        return True
    if not command:
        return False
    if section == "subcommand":
        return command in {"comfort", "heating", "cooling", "plot-template", "plot-template-analyse", "plot-template-weather"}
    if section == "export":
        return bool(command)
    if section == "template_diagram":
        return command in {"comfort", "heating", "cooling", "plot-template", "plot-template-analyse", "plot-template-weather"}
    if section == "variants":
        return command in {"prepare", "comfort", "analyze_data", "heating", "cooling", "plot-template", "plot-template-analyse", "all"}
    if section == "rooms":
        return command not in {"", "prepare", "plot-template-weather"}
    if section == "overlays":
        if command not in {"plot-template", "plot-template-analyse"}:
            return False
        return bool(state.overlay_enabled) if state is not None else True
    if section == "run":
        return bool(command)
    return False


def visible_analysis_steps(
    command_or_state: str | AnalysisWizardState,
    *,
    template_supports_overlays: bool | None = None,
) -> tuple[str, ...]:
    """Return all relevant sections for the command in UI order.

    ``template_supports_overlays`` is accepted for compatibility with the old
    Streamlit wizard. Overlay options now live inside ``Template / Diagramm``.
    """

    relevance_source: str | AnalysisWizardState = command_or_state
    return tuple(section for section in ANALYSIS_SECTION_ORDER if section_relevant(relevance_source, section))


def irrelevant_section_hint(command: str, section: str) -> str:
    if not command and section != "command":
        return "Dieser Bereich wird nach der Befehlsauswahl relevant."
    hints = {
        "subcommand": "Für diesen Befehl ist kein Unterbefehl nötig.",
        "export": "Für diesen Befehl gibt es keine separate Exportauswahl.",
        "template_diagram": "Für diesen Befehl sind keine Diagramm- oder Template-Optionen nötig.",
        "variants": "Für diesen Befehl ist keine Variantenauswahl nötig.",
        "rooms": "Für diesen Befehl ist keine Raumauswahl nötig.",
        "overlays": "Overlay wird unter Template / Diagramm aktiviert.",
        "run": "Wähle zuerst einen Befehl.",
    }
    return hints.get(section, "Dieser Bereich ist für den aktuellen Befehl nicht relevant.")


def allowed_comfort_outputs(_: str | None = None) -> tuple[str, ...]:
    """Comfort no longer depends on a separate analysis level."""

    return COMFORT_OUTPUT_OPTIONS


def comfort_subcommand_label(value: str) -> str:
    return COMFORT_SUBCOMMAND_LABELS.get(value, value or "Unterbefehl wählen")


def plot_template_group_label(value: str) -> str:
    labels = {
        "comfort": "Comfort",
        "heating": "Heating",
        "cooling": "Cooling",
        "energy-balance": "Energy Balance",
        "internal-loads": "Internal Loads",
        "thermal-room-climate": "Thermal Room Climate",
    }
    return labels.get(value, value or "Diagrammgruppe wählen")


def sanitize_comfort_output(first: str, second: str | None = None) -> str:
    """Return a valid comfort output.

    The active wizard passes only the current comfort output. Older callers used
    ``sanitize_comfort_output(analysis_level, current_output)``. Both forms stay
    supported while the Tkinter and Streamlit screens are being aligned.
    """

    current = second if first in COMFORT_ANALYSIS_LEVEL_OPTIONS else first
    if current in COMFORT_OUTPUT_OPTIONS:
        return str(current)
    return COMFORT_OUTPUT_OPTIONS[0]


def time_view_requires_month(view: str) -> bool:
    return view in {"month", "day"}


def time_view_requires_week(view: str) -> bool:
    return view == "week"


def time_view_requires_day(view: str) -> bool:
    return view == "day"


def load_view_complete(view: str, *, month: str = "", week: str = "", day: str = "") -> bool:
    if view not in LOAD_VIEW_OPTIONS:
        return False
    if time_view_requires_month(view) and not month:
        return False
    if time_view_requires_week(view) and not week:
        return False
    if time_view_requires_day(view) and not day:
        return False
    return True


def _has_variant_selection(state: AnalysisWizardState) -> bool:
    if state.analysis_scope not in VARIANT_SCOPE_OPTIONS:
        return False
    if state.analysis_scope == "Alle Varianten":
        return state.variant_count > 0
    return bool(state.selected_variants)


def _has_room_selection(state: AnalysisWizardState) -> bool:
    if state.room_scope not in ROOM_SCOPE_OPTIONS:
        return False
    if state.room_scope == "Alle Räume":
        return state.room_count > 0
    return bool(state.selected_rooms)


def section_complete(state: AnalysisWizardState, section: str) -> bool:
    """Return whether a section has all required values."""

    command = state.command
    if not section_relevant(state, section):
        return True
    if section == "command":
        return bool(command)
    if section == "subcommand":
        if command == "comfort":
            return state.comfort_subcommand in COMFORT_SUBCOMMAND_OPTIONS
        if command in {"heating", "cooling"}:
            return state.load_subcommand in LOAD_SUBCOMMAND_OPTIONS
        if command in {"plot-template", "plot-template-analyse"}:
            return bool(state.plot_template)
        if command == "plot-template-weather":
            return bool(state.plot_template_group)
        return True
    if section == "export":
        if command == "prepare":
            return state.prepare_export_format in EXPORT_FORMAT_OPTIONS
        if command == "analyze_data":
            return state.series_layout in SERIES_LAYOUT_OPTIONS
        if command in {"heating", "cooling"}:
            if state.variant_mode not in VARIANT_MODE_OPTIONS:
                return False
            if state.variant_mode == "compare":
                return state.series_layout in SERIES_LAYOUT_OPTIONS
            return True
        if command in {"plot-template", "plot-template-analyse"}:
            return state.plot_template_mode in PLOT_TEMPLATE_MODE_OPTIONS
        if command == "plot-template-weather":
            return state.plot_template_mode in {"single", "compare"}
        return True
    if section == "template_diagram":
        if command == "comfort":
            return state.comfort_type in COMFORT_OUTPUT_OPTIONS
        if command in {"heating", "cooling"}:
            if state.load_subcommand == "bar":
                return True
            if state.load_subcommand == "timeline":
                return load_view_complete(
                    state.view,
                    month=state.month,
                    week=state.week,
                    day=state.day,
                )
            return False
        if command in {"plot-template", "plot-template-analyse"}:
            return (
                _plot_template_view_complete(state)
                and bool(state.plot_template)
                and state.primary_axis_mode in AXIS_RANGE_MODE_OPTIONS
                and state.secondary_axis_mode in AXIS_RANGE_MODE_OPTIONS
                and _manual_axis_range_complete(
                    state.primary_axis_mode,
                    state.primary_ymin,
                    state.primary_ymax,
                )
                and _manual_axis_range_complete(
                    state.secondary_axis_mode,
                    state.secondary_ymin,
                    state.secondary_ymax,
                )
            )
        if command == "plot-template-weather":
            return bool(state.plot_template)
        return True
    if section == "variants":
        return _has_variant_selection(state)
    if section == "rooms":
        return _has_room_selection(state)
    if section == "overlays":
        return True
    if section == "run":
        return all(section_complete(state, item) for item in visible_analysis_steps(state) if item != "run")
    return True


def analysis_step_complete(state: AnalysisWizardState, section: str, **_: Any) -> bool:
    """Backwards-compatible wrapper for older UI tests and callers."""

    return section_complete(state, section)


def first_incomplete_step(
    state: AnalysisWizardState,
    visible_steps: Iterable[str] | None = None,
    **_: Any,
) -> str | None:
    steps = list(visible_steps or visible_analysis_steps(state))
    for step in steps:
        if not section_complete(state, step):
            return step
    return None


def analysis_ready(state: AnalysisWizardState) -> bool:
    return first_incomplete_step(state) in {None, "run"} and section_complete(state, "run")


def section_summary(state: AnalysisWizardState, section: str) -> str:
    if not section_relevant(state, section):
        return "-"
    if section == "command":
        return command_label(state.command) if state.command else "nicht gewählt"
    if section == "subcommand":
        if state.command == "comfort":
            return comfort_subcommand_label(state.comfort_subcommand) if state.comfort_subcommand else "nicht gewählt"
        if state.command in {"heating", "cooling"}:
            return state.load_subcommand or "nicht gewählt"
        if state.command in {"plot-template", "plot-template-analyse"}:
            return state.plot_template or "nicht gewählt"
        if state.command == "plot-template-weather":
            return plot_template_group_label(state.plot_template_group) if state.plot_template_group else "nicht gewählt"
    if section == "export":
        if state.command == "prepare":
            return state.prepare_export_format or "nicht gewählt"
        if state.command == "analyze_data":
            return f"Excel {state.series_layout}" if state.series_layout else "nicht gewählt"
        if state.command in {"heating", "cooling"}:
            parts = []
            if state.variant_mode:
                parts.append(state.variant_mode)
            if state.series_layout and state.variant_mode == "compare":
                parts.append(state.series_layout)
            return ", ".join(parts) if parts else "nicht gewählt"
        if state.command in {"plot-template", "plot-template-analyse", "plot-template-weather"}:
            parts = []
            if state.plot_template_mode:
                parts.append(state.plot_template_mode)
            return ", ".join(parts) if parts else "nicht gewählt"
    if section == "template_diagram":
        parts = []
        if state.command == "comfort":
            if state.comfort_type:
                parts.append(state.comfort_type)
        if state.command in {"heating", "cooling"}:
            if state.load_subcommand == "timeline" and state.view:
                parts.append(_time_summary(state))
        elif state.command in {"plot-template", "plot-template-analyse"}:
            if state.view:
                parts.append(_time_summary(state))
            parts.append(
                "Achsen automatisch"
                if state.primary_axis_mode == "automatic" and state.secondary_axis_mode == "automatic"
                else "Achsen angepasst"
            )
        return ", ".join(parts) if parts else "nicht gewählt"
    if section == "variants":
        return _scope_summary(state.analysis_scope, state.selected_variants, state.variant_count)
    if section == "rooms":
        return _scope_summary(state.room_scope, state.selected_rooms, state.room_count)
    if section == "overlays":
        parts = []
        if state.show_setpoint_band:
            parts.append("Sollwertband")
        if state.show_outdoor_temperature:
            parts.append("Außenluft")
        if state.show_operative_temperature:
            parts.append("operative Temperatur")
        if state.overlay_count:
            parts.append(f"{state.overlay_count} freie Linien")
        return ", ".join(parts) if parts else "aktiv, keine zusätzlichen Linien"
    if section == "run":
        return "bereit" if section_complete(state, "run") else "nicht vollständig"
    return ""


def analysis_step_summary(state: AnalysisWizardState, section: str, **_: Any) -> str:
    """Backwards-compatible wrapper for older UI tests and callers."""

    return section_summary(state, section)


def _scope_summary(scope: str, values: tuple[str, ...], count: int) -> str:
    if not scope:
        return "nicht gewählt"
    if scope.startswith("Alle"):
        return f"{scope} ({count})"
    if values:
        return f"{scope}: {', '.join(values[:3])}" + (" ..." if len(values) > 3 else "")
    return f"{scope}: keine Auswahl"


def _time_summary(state: AnalysisWizardState) -> str:
    if state.view == "year":
        return "Jahr"
    if state.view == "month":
        return f"Monat {state.month}"
    if state.view == "week":
        return f"Woche {state.week}"
    if state.view == "day":
        return f"Tag {state.month} {state.day}"
    return state.view


def _manual_axis_range_complete(mode: str, minimum: float | None, maximum: float | None) -> bool:
    if mode == "automatic":
        return True
    if mode != "manual" or minimum is None or maximum is None:
        return False
    return minimum < maximum


def _plot_template_view_complete(state: AnalysisWizardState) -> bool:
    if state.view in LOAD_VIEW_OPTIONS:
        return load_view_complete(
            state.view,
            month=state.month,
            week=state.week,
            day=state.day,
        )
    return bool(state.view)


def select_values_by_scope(
    scope: str,
    selected_values: Iterable[str],
    available_values: Iterable[str],
) -> tuple[str, ...] | None:
    """Resolve UI scope to values passed into the backend.

    ``None`` means "all variants" for the existing analysis backend.
    Rooms always resolve to concrete room names because the backend expects them.
    """

    selected = tuple(value for value in selected_values if value)
    available = tuple(value for value in available_values if value)
    if scope == "Alle Varianten":
        return None
    if scope == "Alle Räume":
        return available
    return selected


def select_rooms_for_template(
    *,
    room_scope: str,
    selected_rooms: Iterable[str],
    available_rooms: Iterable[str],
    requires_single_room: bool,
) -> tuple[tuple[str, ...], str | None]:
    """Resolve room selection for a plot template.

    Single-room templates cannot use multiple rooms. If the user chooses all
    rooms, the first available room is used and the UI can display the note.
    """

    rooms = tuple(value for value in selected_rooms if value)
    available = tuple(value for value in available_rooms if value)
    note: str | None = None
    if room_scope == "Alle Räume":
        rooms = available
        if requires_single_room and rooms:
            note = f"Dieses Template nutzt genau einen Raum. Verwendet wird: {rooms[0]}"
            rooms = rooms[:1]
    elif requires_single_room and len(rooms) > 1:
        note = f"Dieses Template nutzt genau einen Raum. Verwendet wird: {rooms[0]}"
        rooms = rooms[:1]
    return rooms, note


def room_selection_disabled(state: AnalysisWizardState | None = None, **__: Any) -> bool:
    """Legacy helper kept for imports.

    The new active wizard uses explicit room scope. A legacy comfort state with
    ``Analyse Variante`` still reports disabled room selection so old tests and
    transitional Tkinter code do not break.
    """

    return bool(state and state.command == "comfort" and state.analysis_level == "Analyse Variante")


def filter_templates_by_mode_and_view(
    templates: Iterable[str],
    specs: dict[str, Any],
    *,
    mode: str,
    view: str,
) -> list[str]:
    """Filter plot templates by selected mode and time view.

    The filter is intentionally conservative. If mode-based filtering would
    remove every template for a view, the view-matching templates are returned.
    """

    view_matches = [
        template
        for template in templates
        if _spec_value(specs.get(template), "view") == view
    ]
    if mode not in PLOT_TEMPLATE_MODE_OPTIONS:
        return view_matches
    filtered: list[str] = []
    for template in view_matches:
        spec = specs.get(template)
        requires_single = bool(_spec_value(spec, "requires_single_room"))
        if mode == "single" and requires_single:
            filtered.append(template)
        elif mode == "compare" and not requires_single:
            filtered.append(template)
    return filtered or view_matches


def _spec_value(spec: Any, key: str) -> Any:
    if isinstance(spec, dict):
        return spec.get(key)
    return getattr(spec, key, None)


def filter_templates_by_group_mode_and_view(
    templates: Iterable[str],
    specs: dict[str, Any],
    *,
    group: str,
    mode: str,
    view: str,
) -> list[str]:
    """Filter plot templates by module group, output mode and time view."""

    group_matches = [
        template
        for template in templates
        if _template_matches_group(template, _spec_value(specs.get(template), "metric"), group)
    ]
    return filter_templates_by_mode_and_view(group_matches, specs, mode=mode, view=view)


def _template_matches_group(template: str, metric: Any, group: str) -> bool:
    if group == "comfort":
        return str(metric) == "comfort" or template.startswith("comfort-")
    if group == "heating":
        return str(metric) == "heating" or template.startswith("heating-")
    if group == "cooling":
        return str(metric) == "cooling" or template.startswith("cooling-")
    return template.startswith(f"{group}-")
