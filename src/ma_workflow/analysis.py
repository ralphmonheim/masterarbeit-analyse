"""Workflow-Adapter fuer die Simulationsergebnisanalyse."""

from __future__ import annotations

from ma_analyse.models import AnalysisConfig, AnalysisResult
from ma_analyse.services import run_analysis


def run_analysis_action(config: AnalysisConfig) -> AnalysisResult:
    """Startet die Analyse ueber die UI-neutrale ma_analyse-Service-Fassade."""
    return run_analysis(config)
