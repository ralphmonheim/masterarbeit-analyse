"""UI-neutrale Ergebnisansichten fuer die vier Analyse-Stufen."""

from __future__ import annotations

from dataclasses import dataclass

from .models import AnalysisResult
from .stage_3_standards_verification import build_verification_readiness_rows


@dataclass(frozen=True, slots=True)
class AnalysisStageView:
    """Beschreibt den darstellbaren Stand genau einer Analyse-Stufe."""

    stage_key: str
    label: str
    purpose: str
    status: str
    available_functions: tuple[str, ...]
    limits: tuple[str, ...]
    result: AnalysisResult | None = None


def build_analysis_stage_views(result: AnalysisResult | None = None) -> tuple[AnalysisStageView, ...]:
    """Ordnet den aktuellen PostProcess-Lauf in das vierstufige Zielbild ein.

    Der bestehende ``ma_analyse``-Service fuehrt heute Stage 2 aus. Die
    anderen Stufen werden bewusst als getrennte, noch nicht auswertbare
    Ansichten gezeigt, bis ihre jeweiligen Fachvertraege Ergebnisse liefern.
    """

    optimization_status = "not_run"
    if result is not None:
        optimization_status = "completed" if result.success else "failed"
    verification_readiness = AnalysisResult(
        success=True,
        steps=("standards_verification_readiness",),
        summary_table=build_verification_readiness_rows(),
        warnings=["Die Tabelle ist eine Bereitschaftsprüfung und kein fachlicher Normnachweis."],
    )

    return (
        AnalysisStageView(
            stage_key="dimensioning",
            label="Dimensionierung",
            purpose="Ausgangslasten, Rechenweg und Annahmen nachvollziehbar darstellen.",
            status="separate_owner",
            available_functions=(
                "LoD-1-Referenzdimensionierung im Modul ma_dimensionierung",
                "manuell uebernommene IDA-Referenzlasten mit Quellenmetadaten",
            ),
            limits=(
                "Die Dimensionierungsberechnung bleibt ausserhalb von ma_analyse.",
                "Der vorhandene LoD-1-Rechenweg ist keine normative Lastberechnung.",
            ),
        ),
        AnalysisStageView(
            stage_key="optimization",
            label="Optimierung",
            purpose="Varianten anhand vorhandener Last-, Energie-, Komfort- und Zeitreihendaten vergleichen.",
            status=optimization_status,
            available_functions=(
                "Heiz- und Kuehllastvergleiche",
                "Komfort-, Energie- und Raumklimaauswertungen",
                "Excel-Tabellen und Diagrammdateien",
            ),
            limits=(
                "Fehlende Ergebnisvariablen bleiben nicht auswertbar.",
                "Stage 2 trifft keinen Norm-Nachweis und keine automatische Optimierungsentscheidung.",
            ),
            result=result,
        ),
        AnalysisStageView(
            stage_key="standards_verification",
            label="Nachweis",
            purpose="Analysewerte gegen fachlich freigegebene Kriterien bewerten.",
            status="not_evaluable",
            available_functions=(
                "vorbereitete Statusstruktur fuer PASS, FAIL, WARNING und NOT_EVALUATED",
                "spaetere Kriterienmatrix mit Quelle, Version, Einheit und Geltungsbereich",
            ),
            limits=(
                "Es sind noch keine produktiven Normregeln oder Grenzwerte hinterlegt.",
                "Normwerte und Rechenverfahren werden nicht erfunden oder aus geschuetzten Volltexten uebernommen.",
            ),
            result=verification_readiness,
        ),
        AnalysisStageView(
            stage_key="sensitivity",
            label="Sensitivitaet",
            purpose="Parameter-, Wetter- und Betriebsfaelle gegen einen Referenzfall vergleichen.",
            status="not_evaluable",
            available_functions=(
                "vorhandene Varianten-, Tages-, Wochen- und Jahresansichten",
                "vorhandene Wetterereignisse als spaetere reproduzierbare Zeitfenster",
            ),
            limits=(
                "Ein formaler Robustheitsvertrag ist noch nicht umgesetzt.",
                "Die Ansicht veraendert weder Varianten noch technische Kapazitaeten automatisch.",
            ),
        ),
    )


def analysis_stage_overview_rows(views: tuple[AnalysisStageView, ...]) -> list[dict[str, str]]:
    """Bereitet eine kompakte Uebersicht fuer UI und Tests auf."""

    return [
        {
            "Stufe": view.label,
            "Status": view.status,
            "Zweck": view.purpose,
        }
        for view in views
    ]
