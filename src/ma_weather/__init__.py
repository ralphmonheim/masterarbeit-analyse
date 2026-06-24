"""Wetterdatenmodul fuer TRY-Datensaetze."""

from .run_weather_analysis import (
    WeatherAnalysisResult,
    plot_template_weather,
    record_weather_release_decision,
    run_weather_analysis,
)
from .try_importer import TryImportResult, import_try_weather_file
from .weather_catalog import DEFAULT_WEATHER_DATASETS_CONFIG, WeatherCatalog, WeatherDataset, import_weather_catalog
from .weather_events import WeatherEvent, detect_critical_weather_events, weather_event_rows
from .weather_imports import (
    DWD_TRY_URL,
    LOCAL_WEATHER_DATASETS_CONFIG,
    LOCAL_WEATHER_INPUT_DIR,
    WeatherDatasetImportDraft,
    WeatherDatasetImportResult,
    import_local_weather_dataset,
    suggest_weather_key,
    validate_weather_import_draft,
)
from .weather_locations import (
    DEFAULT_WEATHER_LOCATIONS_CONFIG,
    WeatherLocation,
    WeatherLocationCatalog,
    WeatherRegion,
    import_weather_location_catalog,
)
from .weather_metrics import WeatherMetrics, calculate_weather_metrics
from .weather_plots import WeatherPlotResult, build_weather_plots
from .weather_report import write_weather_report
from .weather_selection import (
    DEFAULT_WEATHER_SELECTION_STATE_PATH,
    WeatherActivationRecord,
    WeatherSelectionState,
    activate_weather_dataset,
    load_weather_selection_state,
    project_default_weather_dataset,
    save_weather_selection_state,
    set_project_default_weather_dataset,
)
from .weather_status import (
    WeatherDatasetStatus,
    WeatherFileStatus,
    WeatherImportCheckStatus,
    create_weather_import_id,
    infer_weather_start_year,
    inspect_weather_catalog_statuses,
    inspect_weather_dataset_status,
    weather_status_from_analysis_result,
    weather_statuses_by_key,
)
from .weather_validation import WeatherValidationReport, validate_weather_dataframe

__all__ = [
    "DEFAULT_WEATHER_DATASETS_CONFIG",
    "DEFAULT_WEATHER_LOCATIONS_CONFIG",
    "DEFAULT_WEATHER_SELECTION_STATE_PATH",
    "DWD_TRY_URL",
    "LOCAL_WEATHER_DATASETS_CONFIG",
    "LOCAL_WEATHER_INPUT_DIR",
    "TryImportResult",
    "WeatherActivationRecord",
    "WeatherAnalysisResult",
    "WeatherCatalog",
    "WeatherDataset",
    "WeatherDatasetImportDraft",
    "WeatherDatasetImportResult",
    "WeatherDatasetStatus",
    "WeatherEvent",
    "WeatherFileStatus",
    "WeatherImportCheckStatus",
    "WeatherLocation",
    "WeatherLocationCatalog",
    "WeatherMetrics",
    "WeatherPlotResult",
    "WeatherRegion",
    "WeatherSelectionState",
    "WeatherValidationReport",
    "activate_weather_dataset",
    "build_weather_plots",
    "calculate_weather_metrics",
    "create_weather_import_id",
    "detect_critical_weather_events",
    "infer_weather_start_year",
    "import_try_weather_file",
    "import_local_weather_dataset",
    "import_weather_catalog",
    "import_weather_location_catalog",
    "inspect_weather_catalog_statuses",
    "inspect_weather_dataset_status",
    "load_weather_selection_state",
    "plot_template_weather",
    "project_default_weather_dataset",
    "record_weather_release_decision",
    "run_weather_analysis",
    "save_weather_selection_state",
    "set_project_default_weather_dataset",
    "suggest_weather_key",
    "validate_weather_import_draft",
    "validate_weather_dataframe",
    "weather_event_rows",
    "weather_status_from_analysis_result",
    "weather_statuses_by_key",
    "write_weather_report",
]
