# Dokumentation

Die Dokumentation ist nach Projektorganisation und Fachmodulen gegliedert.

## Bereiche

| Bereich | Zweck |
|---|---|
| `project/` | Planung, Status, Strukturreviews, Aufraeumplaene und Entscheidungen |
| `ma_analyse/` | bestehende Analysepipeline, CLI, GUI und Plot-Templates |
| `ma_variants/` | Variantenkern, Datenmodell, Workflow, Wirtschaftlichkeit und Exporte |
| `ma_weather/` | Wetterdatenanalyse und TRY-Integration |
| `ma_ui/` | zentrale Streamlit-Oberflaeche und Bedienablauf |
| `ma_workflow/` | Workflow-Katalog, Statuswerte und interne Orchestrierung |
| `ma_core/`, `ma_database/`, `ma_project/` | technische Plattform und Projektinitialisierung |
| `ma_building/`, `ma_zones/`, `ma_technical/`, `ma_parameters/` | Eingangsdaten und zentrale Parameter |
| `ma_analyse/stage_1_dimensioning/` bis `stage_4_sensitivity/` | Dimensionierung, Optimierung, Standards Compliance und Sensitivitaet |
| `ma_simulation_setup/`, `ma_export_simulation/`, `ma_import_simulation/` | Simulationsvorbereitung und Schnittstellen |
| `ma_economy/`, `ma_sustainability/`, `ma_assessment/` | Wirtschaftlichkeit, Nachhaltigkeit und Gesamtbewertung |
| `ma_reporting/`, `ma_data_export/` | Berichte und maschinenlesbare Datenpakete |
| `ma_validation/`, `ma_feedback/` | phasenuebergreifende Freigaben und Rueckspruenge |
| `common/` | uebergreifende Hinweise wie Commit- und Hook-Dokumentation |
| `examples/` | belastbare Beispielausgaben, getrennt fuer Analyse- und Wetter-Plot-Templates |

`CHANGELOG.md` bleibt im Projekt-Root und dokumentiert nur tatsaechlich umgesetzte Aenderungen.

Der zentrale Orientierungsleitfaden fuer die Masterarbeit liegt unter
`project/MASTERARBEIT_LEITFADEN.md`. Aeltere Leitfadenfassungen und externe
Referenzen liegen unter `project/archive/leitfaeden/`. Ersetzte
Workflow-Fassungen liegen unter `project/archive/workflow/`.

Zweck, Ein- und Ausgaben, Abgrenzung, Status und naechster Schritt aller
Zielmodule werden zusaetzlich zentral in `ma_workflow` gepflegt und im
Streamlit-Dashboard angezeigt.
