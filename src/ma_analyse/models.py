"""UI-neutrale Datenmodelle fuer ma_analyse-Services."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .core.config import DATENBANK_DIR, INPUT_DIR, OUTPUT_DIR, ROOMS


@dataclass
class AnalysisConfig:
    """Beschreibt einen fachlichen Analyseauftrag ohne UI-Abhaengigkeit."""

    steps: tuple[str, ...]
    input_dir: Path = Path(INPUT_DIR)
    database_dir: Path = Path(DATENBANK_DIR)
    output_root: Path = Path(OUTPUT_DIR)
    run_id: str | None = None
    variants: list[str] | None = None
    rooms: list[str] = field(default_factory=lambda: ROOMS.copy())
    debug: bool = True
    export_format: str = "csv"
    comfort_output_type: str | None = None
    load_kind: str | None = None
    view: str | None = None
    month: str | None = None
    week: int | None = None
    day: int | None = None
    variant_mode: str | None = None
    series_layout: str | None = None
    plot_template: str | None = None
    plot_template_mode: str = "single"
    plot_template_options: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.steps = tuple(self.steps)
        self.input_dir = Path(self.input_dir)
        self.database_dir = Path(self.database_dir)
        self.output_root = Path(self.output_root)
        self.rooms = list(self.rooms)
        if self.variants is not None:
            self.variants = list(self.variants)


@dataclass
class AnalysisResult:
    """Beschreibt das Ergebnis eines ma_analyse-Serviceaufrufs."""

    success: bool
    steps: tuple[str, ...]
    run_id: str | None = None
    created_files: list[Path] = field(default_factory=list)
    summary_table: Any | None = None
    detail_tables: dict[str, Any] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    log_text: str = ""
