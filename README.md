# ma_analyse

Analysepipeline fuer Simulationsdaten der Masterarbeit.

## Setup

```powershell
python -m pip install -e ".[dev]"
```

## Ordnerstruktur

| Ordner | Zweck |
|---|---|
| `data/ma_analyse/ida_imports/` | IDA-Importdaten und Variantenordner |
| `data/ma_analyse/database/` | aufbereitete Raumdaten |
| `data/ma_analyse/output/` | regulaere Analyseausgaben |
| `data/test_output/` | lokale Test- und Smoke-Test-Ausgaben |
| `data/ma_variants/` | Import-, Export- und IDA-Uebergabedaten des Variantenkerns |
| `data/ma_weather/` | lokale TRY-Dateien, aufbereitete Wetterdaten, Wetterdiagramme und Berichte |
| `data/catalogs/` | Produkt-, Material-, Quellen- und Dokumentkataloge |
| `docs/project/` | Planstatus, Planindex, Entscheidungen und Strukturreviews |
| `docs/ma_analyse/` | Befehle, Architektur und Plot-Template-Beispiele der Analysepipeline |
| `docs/ma_variants/` | Workflow, Datenmodell und Wirtschaftlichkeitsmodell des Variantenkerns |
| `docs/ma_weather/` | Wetterdatenanalyse und TRY-Integration |
| `src/ma_analyse/app/` | CLI und Befehlssteuerung |
| `src/ma_analyse/core/` | zentrale Konfiguration und Logging |
| `src/ma_analyse/preprocessing/` | Datenvorbereitung aus Rohdaten |
| `src/ma_analyse/analysis/` | Datenverarbeitung, Auswertung und gemeinsame Analyse-Komponenten |
| `src/ma_analyse/settings/` | Naming- und Formatlogik plus zugehoerige Markdown-Dateien |
| `src/ma_analyse/gui/` | grafische Oberflaeche |
| `src/ma_variants/` | modularer Varianten-, Export-, Katalog- und Bewertungskern |
| `src/ma_weather/` | vorbereiteter Wetterkatalog und spaeteres TRY-Modul |
| `tests/` | automatisierte Code-Tests |
| `logs/` | automatisch erzeugte Laufprotokolle der Analysebefehle |

## Wichtige Befehle

```powershell
python -m ma_analyse --help
python -m ma_analyse gui
python -m ma_analyse prepare --export-format both
python -m ma_analyse comfort --output-type plot_analysis_overview
python -m ma_analyse analyze-data --series-layout separate
python -m ma_analyse heating --view year --heating-mode single
python -m ma_analyse cooling --view year --variant-mode single
python -m ma_analyse plot-template --template heating-year --variants Dimensionierung --rooms "101 lobby"
python -m ma_analyse all
```

## Qualitaetssicherung

```powershell
python -m ruff check src tests --no-cache
python -m ruff format --check src tests --no-cache
python -m pytest
```

Lokale Daten- und Ausgabeordner unter `data/` sind in `.gitignore` ausgeschlossen. Analysebefehle schreiben automatisch Logdateien mit Schritt- und Gesamtlaufzeiten nach `logs/`; die Logdateien selbst werden nicht versioniert.

## Projektsteuerung

- Aktiver Planstatus: `docs/project/plans/PLAN_STATUS.md`
- Planindex und Plan-Inbox: `docs/project/plans/`
- Technische Entscheidungen: `docs/project/decisions/TECHNICAL_DECISIONS.md`
- Nutzerentscheidungen: `docs/project/decisions/USER_DECISIONS_MASTERTHESIS_CODE.md`
- Root-Changelog: `CHANGELOG.md`
