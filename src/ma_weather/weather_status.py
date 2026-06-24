"""Statuspruefung fuer katalogisierte Wetterdatensaetze."""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path

from ma_core import create_run_id
from ma_validation import ReleaseDecision, ReleaseStatus

from .try_importer import import_try_weather_file
from .weather_catalog import WeatherCatalog, WeatherDataset
from .weather_validation import validate_weather_dataframe


class WeatherFileStatus(StrEnum):
    """Technischer Dateistatus eines katalogisierten Wetterdatensatzes."""

    MISSING = "missing"
    AVAILABLE = "available"


class WeatherImportCheckStatus(StrEnum):
    """Status einer optionalen Import-/Validierungspruefung."""

    NOT_CHECKED = "not_checked"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"


@dataclass(frozen=True, slots=True)
class WeatherDatasetStatus:
    """Zusammenfassung fuer Auswahl, offene Datensaetze und Aktivierung."""

    weather_key: str
    display_name: str
    file_path: Path
    file_exists: bool
    file_status: WeatherFileStatus
    import_status: WeatherImportCheckStatus = WeatherImportCheckStatus.NOT_CHECKED
    release_status: ReleaseStatus | None = None
    import_id: str = ""
    session_id: str = ""
    run_id: str = ""
    source_id: str = ""
    row_count: int | None = None
    warning_count: int = 0
    error_count: int = 0
    messages: tuple[str, ...] = ()

    @property
    def status_label(self) -> str:
        """Lesbarer Status fuer Streamlit-Tabellen und Auswahltexte."""
        if not self.file_exists:
            return "Datei fehlt"
        if self.import_status is WeatherImportCheckStatus.NOT_CHECKED:
            return "Datei vorhanden"
        if self.import_status is WeatherImportCheckStatus.ERROR:
            return "Fehlerhaft"
        if self.release_status is ReleaseStatus.BLOCKED:
            return "Blockiert"
        if self.release_status is ReleaseStatus.CONFIRMATION_REQUIRED:
            return "Freigabe erforderlich"
        if self.release_status is ReleaseStatus.RELEASED:
            return "Freigegeben"
        return "Geprueft"

    @property
    def is_regularly_selectable(self) -> bool:
        """Regulaere Auswahl blendet offene, fehlerhafte und blockierte Daten aus."""
        return self.file_exists and not self.is_open

    @property
    def is_open(self) -> bool:
        """Offene Datensaetze brauchen Nacharbeit oder bewusste Freigabe."""
        return (
            not self.file_exists
            or self.import_status is WeatherImportCheckStatus.ERROR
            or self.release_status in {ReleaseStatus.BLOCKED, ReleaseStatus.CONFIRMATION_REQUIRED}
        )

    @property
    def can_be_activated(self) -> bool:
        """Aktivierung ist erst nach freigegebenem Validierungsstand erlaubt."""
        return self.release_status is ReleaseStatus.RELEASED


def create_weather_import_id() -> str:
    """Erzeugt eine stabile ID fuer einen Wetterimport."""
    return create_run_id("weather_import")


def infer_weather_start_year(dataset: WeatherDataset) -> int:
    """Leitet das Startjahr fuer den Wetter-Zeitindex aus Katalogdaten ab."""
    candidates = (
        dataset.weather_key,
        dataset.file_path.name,
        dataset.display_name,
        dataset.climate_scenario,
    )
    for candidate in candidates:
        match = re.search(r"(19|20)\d{2}", candidate)
        if match:
            return int(match.group(0))
    return 2015


def inspect_weather_dataset_status(
    dataset: WeatherDataset,
    *,
    project_root: str | Path | None = None,
    validate_file: bool = False,
    import_id: str = "",
    session_id: str = "",
    run_id: str = "",
) -> WeatherDatasetStatus:
    """Prueft Datei, optional Import und Validierung eines Wetterdatensatzes."""
    root = Path.cwd() if project_root is None else Path(project_root)
    resolved_path = dataset.resolved_file_path(root)
    if not resolved_path.exists():
        return WeatherDatasetStatus(
            weather_key=dataset.weather_key,
            display_name=dataset.display_name,
            file_path=dataset.file_path,
            file_exists=False,
            file_status=WeatherFileStatus.MISSING,
            import_id=import_id,
            session_id=session_id,
            run_id=run_id,
            error_count=1,
            messages=(f"Lokale TRY-Datei fehlt: {dataset.file_path}",),
        )

    if not validate_file:
        return WeatherDatasetStatus(
            weather_key=dataset.weather_key,
            display_name=dataset.display_name,
            file_path=dataset.file_path,
            file_exists=True,
            file_status=WeatherFileStatus.AVAILABLE,
            import_id=import_id,
            session_id=session_id,
            run_id=run_id,
        )

    try:
        import_result = import_try_weather_file(
            resolved_path,
            weather_key=dataset.weather_key,
            start_year=infer_weather_start_year(dataset),
        )
        validation_report = validate_weather_dataframe(
            import_result.data,
            additional_messages=import_result.import_diagnostic.messages,
        )
    except Exception as exc:  # noqa: BLE001 - Statuspruefung soll Fehler als Datenstatus melden.
        return WeatherDatasetStatus(
            weather_key=dataset.weather_key,
            display_name=dataset.display_name,
            file_path=dataset.file_path,
            file_exists=True,
            file_status=WeatherFileStatus.AVAILABLE,
            import_status=WeatherImportCheckStatus.ERROR,
            import_id=import_id,
            session_id=session_id,
            run_id=run_id,
            error_count=1,
            messages=(str(exc),),
        )

    release_status = validation_report.validation_result.release_status
    import_status = _import_status_from_release_status(release_status)
    messages = tuple(
        message.message
        for message in validation_report.validation_result.messages
    )
    return WeatherDatasetStatus(
        weather_key=dataset.weather_key,
        display_name=dataset.display_name,
        file_path=dataset.file_path,
        file_exists=True,
        file_status=WeatherFileStatus.AVAILABLE,
        import_status=import_status,
        release_status=release_status,
        import_id=import_id,
        session_id=session_id,
        run_id=run_id,
        source_id=import_result.source.source_id,
        row_count=import_result.row_count,
        warning_count=len(validation_report.validation_result.warnings),
        error_count=len(validation_report.validation_result.errors),
        messages=messages,
    )


def inspect_weather_catalog_statuses(
    catalog: WeatherCatalog,
    *,
    project_root: str | Path | None = None,
    validate_files: bool = False,
) -> list[WeatherDatasetStatus]:
    """Prueft alle katalogisierten Datensaetze in stabiler Katalogreihenfolge."""
    return [
        inspect_weather_dataset_status(
            dataset,
            project_root=project_root,
            validate_file=validate_files,
        )
        for dataset in catalog.datasets
    ]


def weather_statuses_by_key(
    statuses: list[WeatherDatasetStatus] | tuple[WeatherDatasetStatus, ...],
) -> dict[str, WeatherDatasetStatus]:
    """Indexiert Statusobjekte nach `weather_key`."""
    return {status.weather_key: status for status in statuses}


def weather_status_from_analysis_result(
    result: object,
    *,
    decision: ReleaseDecision | None = None,
) -> WeatherDatasetStatus:
    """Erzeugt einen aktuellen Status aus einem abgeschlossenen Analyseergebnis."""
    dataset = result.dataset
    validation_result = result.validation_report.validation_result
    release_status = (
        decision.resulting_status
        if decision is not None
        else result.release_decision.resulting_status
        if result.release_decision is not None
        else validation_result.release_status
    )
    return WeatherDatasetStatus(
        weather_key=dataset.weather_key,
        display_name=dataset.display_name,
        file_path=dataset.file_path,
        file_exists=result.import_result.source_path.exists(),
        file_status=WeatherFileStatus.AVAILABLE,
        import_status=_import_status_from_release_status(release_status),
        release_status=release_status,
        import_id=result.import_id,
        session_id=result.session_id,
        run_id=result.run_id,
        source_id=result.import_result.source.source_id,
        row_count=result.import_result.row_count,
        warning_count=len(validation_result.warnings),
        error_count=len(validation_result.errors),
        messages=tuple(message.message for message in validation_result.messages),
    )


def _import_status_from_release_status(release_status: ReleaseStatus | None) -> WeatherImportCheckStatus:
    if release_status is ReleaseStatus.RELEASED:
        return WeatherImportCheckStatus.SUCCESS
    if release_status is ReleaseStatus.CONFIRMATION_REQUIRED:
        return WeatherImportCheckStatus.WARNING
    if release_status is ReleaseStatus.BLOCKED:
        return WeatherImportCheckStatus.ERROR
    return WeatherImportCheckStatus.NOT_CHECKED
