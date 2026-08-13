# Fachlicher Gesamtworkflow

Stand: 2026-08-13  
Status: P037-A umgesetzt; fachliche Inhaltsquelle für Workflowansicht und Ablaufhilfe

## Zweck und Führungsrolle

Diese Dokumentation ist die operative fachliche Hauptquelle für den Ablauf der Masterarbeitssoftware. Sie beschreibt die Nutzung, fachlichen Übergaben, Begriffe, Datenherkunft und Grenzen der Module. Technische Architektur, Tests, aktive Umsetzungspläne und Restarbeit werden bewusst nicht hier gepflegt, sondern in Architektur, Entscheidungen, Plänen und der technischen Modulinfo.

Stabile Modul-ID, Name, Status, Prozessbereich und Paketzuordnung stammen aus `src/ma_workflow/catalog.py`. Die folgenden Steckbriefe ergänzen diese Metadaten um nutzungsorientierten Text; sie sind keine zweite Quelle für Status oder technische Umsetzung.

## Gesamtprozess

```text
PreProcess → Kernprozess → PostProcess
    ↕             ↕              ↕
  Validierung und Feedback wirken phasenübergreifend.
```

- **PreProcess:** Projekt, Wetter, Gebäude, Zonen, Technik, Parameter, Dimensionierung, Varianten und Simulation-Setup.
- **Kernprozess:** Simulationsexport, manueller IDA-ICE-Lauf und neutraler Ergebnisimport.
- **PostProcess:** Datenvorbereitung, Analyse, Nachweisbereitschaft, Sensitivität, Wirtschaftlichkeit, Nachhaltigkeit, Bewertung, Reporting und Datenexport.
- **Querschnitt:** Technische Grundlagen, Datenbank, Benutzeroberfläche, Workflow-Steuerung, Projektdokumentation, Validierung und Feedback.

## Modulsteckbriefe

| Modul | Modul-ID | Prozessbereich | Status |
|---|---|---|---|
| [Technische Grundlagen](modules/ma_core.md) | `ma_core` | Querschnitt | geplant |
| [Datenbank](modules/ma_database.md) | `ma_database` | Querschnitt | geplant |
| [Benutzeroberflaeche](modules/ma_ui.md) | `ma_ui` | Querschnitt | geplant |
| [Workflow-Steuerung](modules/ma_workflow.md) | `ma_workflow` | Querschnitt | geplant |
| [Projektdokumentation](modules/project_documentation.md) | `project_documentation` | PostProcess | umgesetzt |
| [Projektinitialisierung](modules/ma_project.md) | `ma_project` | PreProcess | geplant |
| [Gebaeude](modules/ma_building.md) | `ma_building` | PreProcess | teilweise umgesetzt |
| [Wetterdaten](modules/ma_weather.md) | `ma_weather` | PreProcess | umgesetzt |
| [Zonen](modules/ma_zones.md) | `ma_zones` | PreProcess | teilweise umgesetzt |
| [Technische Systeme](modules/ma_technical.md) | `ma_technical` | PreProcess | teilweise umgesetzt |
| [Zentrale Parameter](modules/ma_parameters.md) | `ma_parameters` | PreProcess | teilweise umgesetzt |
| [Parameter-Variationsspezifikation](modules/ma_parameters__variation_specification.md) | `ma_parameters.variation_specification` | PreProcess | teilweise umgesetzt |
| [Referenzdimensionierung](modules/ma_analyse__stage_1_dimensioning.md) | `ma_analyse.stage_1_dimensioning` | PreProcess | teilweise umgesetzt |
| [Analyse-Grundlagen](modules/ma_analyse.md) | `ma_analyse` | Querschnitt | teilweise umgesetzt |
| [Datenvorbereitung](modules/ma_data_preparation.md) | `ma_data_preparation` | PostProcess | teilweise umgesetzt |
| [Analyse Stufe 2 - Optimierung](modules/ma_analyse__stage_2_optimization.md) | `ma_analyse.stage_2_optimization` | PostProcess | teilweise umgesetzt |
| [Analyse Stufe 3 - Norm-Nachweis](modules/ma_analyse__stage_3_standards_verification.md) | `ma_analyse.stage_3_standards_verification` | PostProcess | geplant |
| [Analyse Stufe 4 - Sensitivitaet](modules/ma_analyse__stage_4_sensitivity.md) | `ma_analyse.stage_4_sensitivity` | PostProcess | geplant |
| [Varianten](modules/ma_variants.md) | `ma_variants` | PreProcess | geplant |
| [Simulation konfigurieren](modules/ma_simulation_setup.md) | `ma_simulation_setup` | PreProcess | geplant |
| [Simulationsexport](modules/ma_export_simulation.md) | `ma_export_simulation` | Kernprozess | geplant |
| [IDA ICE](modules/ida_ice.md) | `ida_ice` | Kernprozess | manuell / extern |
| [Simulationsergebnisimport](modules/ma_import_simulation.md) | `ma_import_simulation` | Kernprozess | geplant |
| [Wirtschaftlichkeit](modules/ma_economy.md) | `ma_economy` | PostProcess | geplant |
| [Nachhaltigkeit](modules/ma_sustainability.md) | `ma_sustainability` | PostProcess | geplant |
| [Gesamtbewertung](modules/ma_assessment.md) | `ma_assessment` | PostProcess | geplant |
| [Reporting](modules/ma_reporting.md) | `ma_reporting` | PostProcess | geplant |
| [Datenexport](modules/ma_data_export.md) | `ma_data_export` | PostProcess | geplant |
| [Zentrale Validierung](modules/ma_validation.md) | `ma_validation` | Querschnitt | geplant |
| [Feedback und Rueckspruenge](modules/ma_feedback.md) | `ma_feedback` | Querschnitt | geplant |

## Pflege- und Abgrenzungsregel

1. Nutzungswissen wird zuerst im passenden Steckbrief geändert.
2. Stabile Strukturfelder werden im technischen Katalog geändert.
3. Entscheidungen werden ausschließlich im Entscheidungsregister festgehalten.
4. Aktive Arbeit wird ausschließlich in Plan und Planstatus gepflegt.
5. Fachliche Regelwerte oder Quellen werden erst nach ihrem jeweiligen Rechte- und Fachgate ergänzt. Ungeklärte Inhalte bleiben als offen gekennzeichnet.

Die Workflowansicht rendert diese Steckbriefe. Geplante oder externe Module bleiben sichtbar, werden aber nicht als ausführbar dargestellt.

