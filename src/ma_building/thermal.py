"""UI-neutrale Hilfen fuer eine bewusst einfache thermische Huelle.

Die Rechnung ist eine transparente Demo-Transmissionsbilanz und ersetzt keine
normative Bilanzierung.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from math import isfinite

from .models import BuildingModelSpecification, Opening, PhysicalElement
from .validation import (
    is_within_confirmed_area_tolerance,
    validate_building_spec,
)

DEFAULT_DELTA_U_WB_W_M2K = 0.10
"""Demo-Annahme fuer einen flaechenbezogenen Waermebrueckenzuschlag."""


@dataclass(frozen=True, slots=True)
class ThermalComponentRow:
    """Eine fuer Tabellen geeignete Zeile der thermischen Gebaeudehuelle."""

    component_id: str
    source_type: str
    category: str
    construction_code: str
    gross_area_m2: float
    effective_area_m2: float
    orientation_deg: float | None
    u_value_w_m2k: float | None
    temperature_correction_factor: float | None
    is_complete: bool
    assumption_notes: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class ThermalCategoryResult:
    """Flaechen und Kennwerte einer Bauteilkategorie."""

    category: str
    area_m2: float
    weighted_u_value_w_m2k: float | None
    transmission_contribution_w_k: float | None
    is_complete: bool
    warnings: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class ThermalTransmissionResult:
    """Gesamtresultat der vereinfachten Transmissionsbilanz."""

    rows: tuple[ThermalComponentRow, ...]
    category_results: tuple[ThermalCategoryResult, ...]
    envelope_area_m2: float
    heat_loss_coefficient_w_k: float | None
    heat_loss_coefficient_per_area_w_m2k: float | None
    thermal_bridge_delta_u_w_m2k: float
    is_complete: bool
    warnings: tuple[str, ...] = ()


_CATEGORY_BY_CODE = {"AW": "Waende", "DA": "Dach", "BP": "Boden", "GD": "Oberste Geschossdecke", "FA": "Fenster", "TA": "Tueren"}
_EXCLUDED_INTERNAL_CODES = frozenset({"IW", "GD"})


def build_thermal_component_rows(
    specification: BuildingModelSpecification, *, include_internal: bool = False
) -> tuple[ThermalComponentRow, ...]:
    """Erzeugt geordnete Huellezeilen; Oeffnungen reduzieren ihre Hostflaeche."""
    if not specification.elements and not specification.openings:
        return _aggregate_envelope_rows(specification)

    openings_by_host: dict[str, list[Opening]] = {}
    for opening in specification.openings:
        if opening.area_m2 > 0:
            openings_by_host.setdefault(opening.host_element_id, []).append(opening)

    rows: list[ThermalComponentRow] = []
    elements_by_id = {element.element_id: element for element in specification.elements}
    invalid_opening_hosts = {
        host_id
        for host_id, openings in openings_by_host.items()
        if host_id in elements_by_id and sum(opening.area_m2 for opening in openings) > elements_by_id[host_id].area_m2
    }
    for element in specification.elements:
        if not include_internal and _is_internal_element(element):
            continue
        opening_area_m2 = sum(opening.area_m2 for opening in openings_by_host.get(element.element_id, ()))
        invalid_host = element.element_id in invalid_opening_hosts
        rows.append(
            _element_row(
                element,
                max(0.0, element.area_m2 - opening_area_m2),
                specification,
                invalid_host=invalid_host,
            )
        )
    for opening in specification.openings:
        if opening.area_m2 <= 0:
            continue
        host = elements_by_id.get(opening.host_element_id)
        if host is None:
            rows.append(_opening_row(opening, None, specification, invalid_host=True))
        elif include_internal or not _is_internal_element(host):
            rows.append(
                _opening_row(opening, host, specification, invalid_host=host.element_id in invalid_opening_hosts)
            )
    return tuple(rows)


def _is_internal_element(element: PhysicalElement) -> bool:
    """Haelt oberste Geschossdecken gegen einen unconditioned Dachraum sichtbar."""
    return element.construction_code in _EXCLUDED_INTERNAL_CODES and element.element_type != "uppermost_storey_ceiling"


def calculate_weighted_u_value(rows: tuple[ThermalComponentRow, ...] | list[ThermalComponentRow]) -> float | None:
    """Berechnet den flaechengewichteten U-Wert nur fuer vollstaendige Zeilen."""
    relevant_rows = [row for row in rows if row.effective_area_m2 > 0]
    if not relevant_rows or any(not row.is_complete for row in relevant_rows):
        return None
    area_m2 = sum(row.effective_area_m2 for row in relevant_rows)
    return (
        sum(row.u_value_w_m2k * row.effective_area_m2 for row in relevant_rows if row.u_value_w_m2k is not None)
        / area_m2
    )


def calculate_thermal_transmission(
    specification: BuildingModelSpecification,
    *,
    include_internal: bool = False,
) -> ThermalTransmissionResult:
    """Berechnet H_T und H'_T nur bei einer vollstaendigen, nichtleeren Huelle."""
    source_rows = build_thermal_component_rows(specification, include_internal=include_internal)
    blocking_reasons = _thermal_blocking_reasons(specification, source_rows)
    rows = source_rows
    if blocking_reasons:
        rows = _mark_rows_incomplete(rows, blocking_reasons)
    category_order = (
        "Dach",
        "Oberste Geschossdecke",
        "Waende",
        "Boden",
        "Fenster",
        "Tueren",
        "Unbekannt",
    )
    categories: list[ThermalCategoryResult] = []
    for category in category_order:
        category_rows = [row for row in rows if row.category == category and row.effective_area_m2 > 0]
        if not category_rows:
            continue
        source_category_rows = [
            row for row in source_rows if row.category == category and row.effective_area_m2 > 0
        ]
        incomplete = [row for row in category_rows if not row.is_complete]
        source_incomplete = [row for row in source_category_rows if not row.is_complete]
        categories.append(
            ThermalCategoryResult(
                category=category,
                area_m2=sum(row.effective_area_m2 for row in category_rows),
                weighted_u_value_w_m2k=calculate_weighted_u_value(source_category_rows),
                transmission_contribution_w_k=(
                    None if source_incomplete else sum(_row_transmission(row) for row in source_category_rows)
                ),
                is_complete=not incomplete,
                warnings=tuple(f"{row.component_id}: Zeile ist unvollstaendig oder ungueltig." for row in incomplete),
            )
        )

    envelope_area_m2 = sum(row.effective_area_m2 for row in rows)
    incomplete_rows = [row for row in rows if row.effective_area_m2 > 0 and not row.is_complete]
    is_complete = bool(rows) and envelope_area_m2 > 0 and not incomplete_rows
    warnings: list[str] = []
    if incomplete_rows:
        warnings.append("Unvollstaendige oder ungueltige Bauteilzeilen verhindern eine Transmissionsbilanz.")
    if not rows or envelope_area_m2 <= 0:
        warnings.append("Keine auswertbare thermische Huelle vorhanden.")
    warnings.extend(blocking_reasons)
    warnings.append("DeltaU_WB = 0.10 W/(m2K) ist eine feste Demo-Annahme.")
    heat_loss_w_k = None
    h_t_prime = None
    if is_complete:
        heat_loss_w_k = sum(_row_transmission(row) for row in rows if row.effective_area_m2 > 0)
        heat_loss_w_k += DEFAULT_DELTA_U_WB_W_M2K * envelope_area_m2
        h_t_prime = heat_loss_w_k / envelope_area_m2
    return ThermalTransmissionResult(
        rows=rows,
        category_results=tuple(categories),
        envelope_area_m2=envelope_area_m2,
        heat_loss_coefficient_w_k=heat_loss_w_k,
        heat_loss_coefficient_per_area_w_m2k=h_t_prime,
        thermal_bridge_delta_u_w_m2k=DEFAULT_DELTA_U_WB_W_M2K,
        is_complete=is_complete,
        warnings=tuple(warnings),
    )


def _aggregate_envelope_rows(specification: BuildingModelSpecification) -> tuple[ThermalComponentRow, ...]:
    """Leitet LoD-1-Zeilen aus vorhandenen Aggregatflaechen ab."""
    envelope = specification.simple_envelope
    if envelope is None:
        return ()
    note = "LoD-1-Aggregatflaeche; AW wird als Bruttoflaeche vor Fensterabzug angenommen."
    wall_gross = envelope.external_wall_area_m2
    window_area, window_notes, window_is_invalid = _resolve_lod1_window_area(specification)
    rows: list[ThermalComponentRow] = []
    if wall_gross is not None:
        invalid = window_is_invalid or (window_area is not None and window_area > wall_gross)
        rows.append(
            _synthetic_row(
                "LOD1-AW",
                "Waende",
                "AW",
                wall_gross,
                max(0.0, wall_gross - (window_area or 0.0)),
                specification,
                note,
                invalid,
                extra_notes=window_notes,
            )
        )
    if window_area is not None and window_area > 0:
        invalid = window_is_invalid or wall_gross is None or window_area > wall_gross
        rows.append(
            _synthetic_row(
                "LOD1-FA",
                "Fenster",
                "FA",
                window_area,
                window_area,
                specification,
                note,
                invalid,
                extra_notes=window_notes,
            )
        )
    if envelope.roof_area_m2 is not None:
        rows.append(
            _synthetic_row("LOD1-DA", "Dach", "DA", envelope.roof_area_m2, envelope.roof_area_m2, specification, note)
        )
    if envelope.floor_area_m2 is not None:
        rows.append(
            _synthetic_row(
                "LOD1-BP", "Boden", "BP", envelope.floor_area_m2, envelope.floor_area_m2, specification, note
            )
        )
    return tuple(rows)


def _synthetic_row(
    component_id: str,
    category: str,
    code: str,
    gross_area_m2: float,
    effective_area_m2: float,
    specification: BuildingModelSpecification,
    note: str,
    invalid: bool = False,
    extra_notes: tuple[str, ...] = (),
) -> ThermalComponentRow:
    u_value, notes = _u_value_for_code(code, specification)
    factor, factor_notes = _temperature_factor_for_code(code)
    if invalid:
        notes += ("LoD-1-Fensterbilanz ist unvollstaendig oder widerspruechlich.",)
    return ThermalComponentRow(
        component_id,
        "SimpleEnvelope",
        category,
        code,
        gross_area_m2,
        effective_area_m2,
        None,
        u_value,
        factor,
        u_value is not None and factor is not None and not invalid,
        (note,) + extra_notes + notes + factor_notes,
    )


def _element_row(
    element: PhysicalElement, effective_area_m2: float, specification: BuildingModelSpecification, *, invalid_host: bool
) -> ThermalComponentRow:
    u_value, notes = _u_value_for_code(element.construction_code, specification)
    factor, factor_notes = _temperature_factor_for_code(element.construction_code)
    if invalid_host:
        notes += ("Zugeordnete Oeffnungen sind groesser als die Host-Bruttoflaeche.",)
    return ThermalComponentRow(
        element.element_id,
        "PhysicalElement",
        _CATEGORY_BY_CODE.get(element.construction_code, "Unbekannt"),
        element.construction_code,
        element.area_m2,
        effective_area_m2,
        element.orientation_deg,
        u_value,
        factor,
        u_value is not None and factor is not None and not invalid_host,
        notes + factor_notes,
    )


def _opening_row(
    opening: Opening, host: PhysicalElement | None, specification: BuildingModelSpecification, *, invalid_host: bool
) -> ThermalComponentRow:
    u_value, notes = _u_value_for_code(opening.construction_code, specification)
    factor, factor_notes = _temperature_factor_for_code(opening.construction_code)
    if host is None:
        notes += ("Host-Bauteil fehlt; Orientierung ist unbekannt.",)
    if invalid_host:
        notes += ("Hostflaeche ist durch zu grosse Oeffnungsflaechen ungueltig.",)
    return ThermalComponentRow(
        opening.opening_id,
        "Opening",
        _CATEGORY_BY_CODE.get(opening.construction_code, "Unbekannt"),
        opening.construction_code,
        opening.area_m2,
        opening.area_m2,
        host.orientation_deg if host else None,
        u_value,
        factor,
        u_value is not None and factor is not None and host is not None and not invalid_host,
        notes + factor_notes,
    )


def _row_transmission(row: ThermalComponentRow) -> float:
    assert row.u_value_w_m2k is not None
    assert row.temperature_correction_factor is not None
    return row.temperature_correction_factor * row.u_value_w_m2k * row.effective_area_m2


def _u_value_for_code(code: str, specification: BuildingModelSpecification) -> tuple[float | None, tuple[str, ...]]:
    envelope = specification.simple_envelope
    if envelope is None:
        return None, ("simple_envelope mit U-Werten fehlt.",)
    values = {
        "AW": envelope.external_wall_u_value_w_m2k,
        "DA": envelope.roof_u_value_w_m2k,
        "BP": envelope.floor_u_value_w_m2k,
        "FA": envelope.window_u_value_w_m2k,
        "TA": envelope.window_u_value_w_m2k,
    }
    notes: tuple[str, ...] = ("Demo-Annahme: TA verwendet den U-Wert von FA.",) if code == "TA" else ()
    value = values.get(code)
    if value is None:
        notes += (f"Kein U-Wert fuer Baucode {code} vorhanden.",)
        return None, notes
    if not _is_positive_finite(value):
        notes += (f"U-Wert fuer Baucode {code} ist nicht positiv und endlich.",)
        return None, notes
    return value, notes


def _temperature_factor_for_code(code: str) -> tuple[float | None, tuple[str, ...]]:
    if code == "BP":
        return 0.5, ("Demo-Annahme: BP gegen Erdreich mit F = 0.5.",)
    if code in {"AW", "DA", "FA", "TA"}:
        return 1.0, ()
    return None, (f"Kein Temperaturkorrekturfaktor fuer Baucode {code} vorhanden.",)


def _resolve_lod1_window_area(specification: BuildingModelSpecification) -> tuple[float | None, tuple[str, ...], bool]:
    """Nutzt die explizite Fensterflaeche oder leitet sie nachvollziehbar aus dem Anteil ab."""
    envelope = specification.simple_envelope
    assert envelope is not None
    wall_area = envelope.external_wall_area_m2
    explicit_area = envelope.window_area_m2
    ratio = envelope.window_area_ratio_percent
    if not _is_positive_finite(wall_area):
        return explicit_area, ("Aussenwandflaeche fehlt fuer die LoD-1-Fensterbilanz.",), True
    if not _is_finite_between(ratio, 0.0, 100.0):
        return explicit_area, ("Fensterflaechenanteil ist ungueltig.",), True

    derived_area = wall_area * ratio / 100.0
    if explicit_area is None:
        return (
            derived_area,
            ("Fensterflaeche wurde aus Aussenwandflaeche und Fensteranteil abgeleitet.",),
            False,
        )
    if not _is_positive_finite(explicit_area):
        return explicit_area, ("Explizite Fensterflaeche ist nicht positiv und endlich.",), True
    if not is_within_confirmed_area_tolerance(explicit_area, derived_area):
        return (
            explicit_area,
            ("Explizite Fensterflaeche und Fensteranteil widersprechen sich.",),
            True,
        )
    return explicit_area, (), False


def _thermal_blocking_reasons(
    specification: BuildingModelSpecification,
    rows: tuple[ThermalComponentRow, ...],
) -> tuple[str, ...]:
    """Sammelt fachliche Fehler, die keine scheinbar vollstaendige H_T-Bilanz zulassen."""
    reasons = [
        f"Fachvalidierung blockiert die Transmissionsbilanz: {message.code}."
        for message in validate_building_spec(specification).errors
    ]
    if not rows:
        return tuple(reasons)
    if specification.elements or specification.openings:
        if not specification.thermal_envelope_complete:
            reasons.append("Explizite Huelle besitzt keinen bestaetigten Vollstaendigkeitsnachweis.")
        external_codes = {
            row.construction_code for row in rows if row.source_type == "PhysicalElement" and row.effective_area_m2 > 0
        }
        missing_codes = {"AW", "DA", "BP"} - external_codes
        if missing_codes:
            readable_codes = ", ".join(sorted(missing_codes))
            reasons.append(f"Explizite Huelle ist unvollstaendig; Aussenbauteile fehlen: {readable_codes}.")
        reasons.extend(_aggregate_coverage_reasons(specification, rows))
    elif specification.simple_envelope is not None:
        envelope = specification.simple_envelope
        missing_areas = [
            label
            for label, area in (
                ("Aussenwand", envelope.external_wall_area_m2),
                ("Dach", envelope.roof_area_m2),
                ("Boden", envelope.floor_area_m2),
            )
            if not _is_positive_finite(area)
        ]
        if missing_areas:
            reasons.append("LoD-1-Huelle ist unvollstaendig; Flaechen fehlen: " + ", ".join(missing_areas) + ".")
    return tuple(reasons)


def _aggregate_coverage_reasons(
    specification: BuildingModelSpecification,
    rows: tuple[ThermalComponentRow, ...],
) -> tuple[str, ...]:
    """Vergleicht explizite V1-Huellflaechen mit vorhandenen bestaetigten Aggregatwerten."""
    envelope = specification.simple_envelope
    if envelope is None:
        return ()
    expected_by_code = {
        "AW": envelope.external_wall_area_m2,
        "DA": envelope.roof_area_m2,
        "BP": envelope.floor_area_m2,
        "FA": _lod1_window_area_for_coverage(envelope),
    }
    reasons: list[str] = []
    for code, expected_area in expected_by_code.items():
        if not _is_positive_finite(expected_area):
            continue
        actual_area = sum(
            row.gross_area_m2 for row in rows if row.construction_code == code and row.effective_area_m2 > 0
        )
        if not is_within_confirmed_area_tolerance(actual_area, expected_area):
            reasons.append(f"Explizite Huelle stimmt fuer {code} nicht mit der bestaetigten Aggregatflaeche ueberein.")
    return tuple(reasons)


def _lod1_window_area_for_coverage(envelope) -> float | None:
    """Liefert die erwartete transparente Flaeche fuer den Vollstaendigkeitsabgleich."""
    if _is_positive_finite(envelope.window_area_m2):
        return envelope.window_area_m2
    if _is_positive_finite(envelope.external_wall_area_m2) and _is_finite_between(
        envelope.window_area_ratio_percent,
        0.0,
        100.0,
    ):
        return envelope.external_wall_area_m2 * envelope.window_area_ratio_percent / 100.0
    return None


def _mark_rows_incomplete(
    rows: tuple[ThermalComponentRow, ...], reasons: tuple[str, ...]
) -> tuple[ThermalComponentRow, ...]:
    """Erhaelt sichtbare Quellwerte, markiert sie aber fuer die Ergebnislogik als unvollstaendig."""
    return tuple(replace(row, is_complete=False, assumption_notes=row.assumption_notes + reasons) for row in rows)


def _is_positive_finite(value: float | None) -> bool:
    return value is not None and isfinite(value) and value > 0


def _is_finite_between(value: float | None, lower: float, upper: float) -> bool:
    return value is not None and isfinite(value) and lower <= value <= upper
