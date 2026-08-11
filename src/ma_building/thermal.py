"""UI-neutrale Hilfen fuer eine bewusst einfache thermische Huelle.

Die Rechnung ist eine transparente Demo-Transmissionsbilanz und ersetzt keine
normative Bilanzierung.
"""

from __future__ import annotations

from dataclasses import dataclass

from .models import BuildingModelSpecification, Opening, PhysicalElement

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


_CATEGORY_BY_CODE = {"AW": "Waende", "DA": "Dach", "BP": "Boden", "FA": "Fenster", "TA": "Tueren"}
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
        if not include_internal and element.construction_code in _EXCLUDED_INTERNAL_CODES:
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
        elif include_internal or host.construction_code not in _EXCLUDED_INTERNAL_CODES:
            rows.append(
                _opening_row(opening, host, specification, invalid_host=host.element_id in invalid_opening_hosts)
            )
    return tuple(rows)


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
    delta_u_wb_w_m2k: float = DEFAULT_DELTA_U_WB_W_M2K,
    include_internal: bool = False,
) -> ThermalTransmissionResult:
    """Berechnet H_T und H'_T nur bei einer vollstaendigen, nichtleeren Huelle."""
    rows = build_thermal_component_rows(specification, include_internal=include_internal)
    category_order = ("Dach", "Waende", "Boden", "Fenster", "Tueren", "Unbekannt")
    categories: list[ThermalCategoryResult] = []
    for category in category_order:
        category_rows = [row for row in rows if row.category == category and row.effective_area_m2 > 0]
        if not category_rows:
            continue
        incomplete = [row for row in category_rows if not row.is_complete]
        categories.append(
            ThermalCategoryResult(
                category=category,
                area_m2=sum(row.effective_area_m2 for row in category_rows),
                weighted_u_value_w_m2k=calculate_weighted_u_value(category_rows),
                transmission_contribution_w_k=(
                    None if incomplete else sum(_row_transmission(row) for row in category_rows)
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
    if delta_u_wb_w_m2k == DEFAULT_DELTA_U_WB_W_M2K:
        warnings.append("DeltaU_WB = 0.10 W/(m2K) ist eine Demo-Annahme.")
    heat_loss_w_k = None
    h_t_prime = None
    if is_complete:
        heat_loss_w_k = sum(_row_transmission(row) for row in rows if row.effective_area_m2 > 0)
        heat_loss_w_k += delta_u_wb_w_m2k * envelope_area_m2
        h_t_prime = heat_loss_w_k / envelope_area_m2
    return ThermalTransmissionResult(
        rows=rows,
        category_results=tuple(categories),
        envelope_area_m2=envelope_area_m2,
        heat_loss_coefficient_w_k=heat_loss_w_k,
        heat_loss_coefficient_per_area_w_m2k=h_t_prime,
        thermal_bridge_delta_u_w_m2k=delta_u_wb_w_m2k,
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
    window_area = envelope.window_area_m2
    rows: list[ThermalComponentRow] = []
    if wall_gross is not None:
        invalid = window_area is not None and window_area > wall_gross
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
            )
        )
    if window_area is not None and window_area > 0:
        invalid = wall_gross is not None and window_area > wall_gross
        rows.append(_synthetic_row("LOD1-FA", "Fenster", "FA", window_area, window_area, specification, note, invalid))
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
) -> ThermalComponentRow:
    u_value, notes = _u_value_for_code(code, specification)
    factor, factor_notes = _temperature_factor_for_code(code)
    if invalid:
        notes += ("Oeffnungsflaeche ist groesser als die angenommene Host-Bruttoflaeche.",)
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
        (note,) + notes + factor_notes,
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
    return value, notes


def _temperature_factor_for_code(code: str) -> tuple[float | None, tuple[str, ...]]:
    if code == "BP":
        return 0.5, ("Demo-Annahme: BP gegen Erdreich mit F = 0.5.",)
    if code in {"AW", "DA", "FA", "TA"}:
        return 1.0, ()
    return None, (f"Kein Temperaturkorrekturfaktor fuer Baucode {code} vorhanden.",)
