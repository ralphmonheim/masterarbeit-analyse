# Befehlsuebersicht

Kompakte Sammlung der wichtigsten Befehle fuer die Analyse-Skripte. Standard-Einstieg ist fast immer:

```powershell
python -m ma_analyse <befehl> [optionen]
```

## Start am naechsten Tag

```powershell
cd "C:\Users\ralph\Documents\Master\5.Semester\Masterarbeit - lokal\TEIL1_Fach-Anwendungskompetenz\260429_Masterarbeit_Analyse"
code .

.\.venv\Scripts\Activate.ps1

python -m ma_analyse gui
```

Falls PowerShell die Aktivierung nicht direkt akzeptiert:

```powershell
& .\.venv\Scripts\Activate.ps1
```

Kurz pruefen:

```powershell
python --version
where python
```

Wichtig:

- Terminal im Projektordner starten, damit relative Pfade wie `1_Datenbank` und `2_Output` stimmen.
- Aktive Umgebung ist meist am Praefix `(.venv)` erkennbar.
- Neue GUI-Aufrufe priorisieren die neue Instanz.
- Testausgaben immer unter `9_test_\<testart>` speichern.

## Hauptbefehl: run_pipeline_display.py

| Befehl | Zweck | Kurzbeispiel |
|---|---|---|
| `gui` | Grafische Oberflaeche starten | `python -m ma_analyse gui` |
| `prepare` | Rohdaten aufbereiten | `python -m ma_analyse prepare --export-format both` |
| `comfort` | Komfortplots und Analyseausgaben | `python -m ma_analyse comfort --output-type plot_analysis_overview` |
| `analyze_data` | Excel-Auswertung erstellen | `python -m ma_analyse analyze-data --series-layout separate` |
| `heating` | Heizlastdiagramme | `python -m ma_analyse heating --view year --heating-mode single` |
| `cooling` | Kuehllastdiagramme | `python -m ma_analyse cooling --view year --variant-mode single` |
| `all` | Uebersichten plus Heating-/Cooling-Bar und Jahr | `python -m ma_analyse all` |

Gemeinsame Optionen:

- `--variants "Dimensionierung,I_04_DIM_Heizleistung_60%"`
- `--rooms "101 lobby,109 office"`
- `--output-root "9_test_\<testart>"`
- `--run-id "<Lauf-ID>"`
- `--debug` / `--no-debug`

### Befehl gui

```powershell
python -m ma_analyse gui
```

Hinweise:

- Die GUI bleibt nach ausgefuehrten Befehlen offen.
- Dreipunktmenue `•••`: Namensmapping und `GUI aktualisieren`.
- Wenn bereits eine GUI offen ist, wird beim neuen Aufruf die neue Instanz priorisiert.

### Befehl prepare

```powershell
python -m ma_analyse prepare
python -m ma_analyse prepare --export-format csv
python -m ma_analyse prepare --export-format excel
python -m ma_analyse prepare --export-format both
```

Wichtige Optionen: `--input-dir`, `--datenbank-dir`, `--variants`, `--rooms`, `--export-format`.

### Befehl comfort

```powershell
python -m ma_analyse comfort --output-type plot
python -m ma_analyse comfort --output-type plot_overview
python -m ma_analyse comfort --output-type plot_analysis
python -m ma_analyse comfort --output-type plot_analysis_overview
```

Wichtige Optionen: `--variants`, `--rooms`, `--output-root`, `--run-id`.

### Befehl analyze_data

```powershell
python -m ma_analyse analyze-data
python -m ma_analyse analyze-data --variants "Dimensionierung" --rooms "101 lobby,109 office"
python -m ma_analyse analyze-data --series-layout separate --variants "Dimensionierung,I_04_DIM_Heizleistung_60%" --rooms "101 lobby,109 office"
python -m ma_analyse analyze-data --series-layout combined --variants "Dimensionierung,I_04_DIM_Heizleistung_60%" --rooms "101 lobby,109 office"
```

Erzeugt die Excel-Auswertung aus den aufbereiteten Daten.

- Standard ist `--series-layout separate`.
- `--series-layout separate`: eine Excel pro Variante im jeweiligen Variantenordner.
- `--series-layout combined`: eine gemeinsame Excel fuer alle ausgewaehlten Varianten/Raeume.

### Befehl heating

```powershell
python -m ma_analyse heating --view year --heating-mode single
python -m ma_analyse heating --view month --month Aug --heating-mode compare --heating-series-layout combined
python -m ma_analyse heating --view week --week 7 --variant-mode compare --series-layout separate --output-root "9_test_\heating_week"
```

Ansichten: `bar`, `year`, `month`, `week`, `day`.

Modi:

- `--heating-mode single` oder `--variant-mode single`: eine Datenreihe je Diagramm.
- `--heating-mode compare` oder `--variant-mode compare`: mehrere Datenreihen je Diagramm.
- `--heating-series-layout separate` / `combined`
- Alias: `--series-layout separate` / `combined`
- Standard fuer die Diagrammausgabe ist `separate`.

### Befehl cooling

```powershell
python -m ma_analyse cooling --view year --variant-mode single
python -m ma_analyse cooling --view bar --variant-mode compare
python -m ma_analyse cooling --view month --month Aug --variant-mode compare --series-layout combined
python -m ma_analyse cooling --view week --week 7 --variant-mode compare --series-layout separate --output-root "9_test_\cooling_week"
```

Ansichten: `bar`, `year`, `month`, `week`, `day`.

Hinweise:

- Datenquelle: `zone_energy_q_cool`.
- Ausgabe als negative Kuehllast nach unten.
- `bar` zeigt die staerkste Kuehllast je Raum als negative Balken.

### Befehl all

```powershell
python -m ma_analyse all
python -m ma_analyse all --variants "Dimensionierung,I_04_DIM_Heizleistung_60%" --debug
python -m ma_analyse all --variants "Dimensionierung" --rooms "101 lobby,109 office" --output-root "9_test_\all_profile"
```

Erzeugt Comfort-Uebersichten, Analyse-Uebersichten sowie Heating-/Cooling-Barplots und Heating-/Cooling-Jahresansichten.

- Pro Variante/Raum entsteht je ein Single-Jahresplot.
- Zusaetzlich wird pro Variante ein kombiniertes Raum-Jahresdiagramm gespeichert.
- Zusaetzlich wird pro Variante je ein Heating- und Cooling-Barplot fuer die ausgewaehlten Raeume gespeichert.
- `analyze_data` laeuft noch nicht mit und wird spaeter separat ergaenzt.

## Direkte Einzelskripte

Diese Befehle sind nuetzlich fuer gezielte Tests oder wenn die GUI nicht benoetigt wird.

### compare_heating_loads.py

```powershell
python Skripte\compare_heating_loads.py --variants "Dimensionierung" --rooms "101 lobby" --view year --variant-mode single
python Skripte\compare_heating_loads.py --variants "Dimensionierung,I_04_DIM_Heizleistung_60%" --rooms "101 lobby" --view year --variant-mode compare --series-layout combined
```

Optionen: `--datenbank_dir`, `--variants`, `--rooms`, `--view`, `--month`, `--week`, `--day`, `--variant-mode`, `--series-layout`, `--output-root`, `--run-id`, `--debug`.

### compare_cooling_loads.py

```powershell
python Skripte\compare_cooling_loads.py --variants "Dimensionierung" --rooms "101 lobby" --view year --variant-mode single
python Skripte\compare_cooling_loads.py --variants "Dimensionierung,I_04_DIM_Heizleistung_60%" --rooms "101 lobby" --view year --variant-mode compare --series-layout combined
```

Optionen: `--datenbank_dir`, `--variants`, `--rooms`, `--view`, `--month`, `--week`, `--day`, `--variant-mode`, `--series-layout`, `--output-root`, `--run-id`, `--debug`.

### analyze_simulation_results.py

```powershell
python Skripte\analyze_simulation_results.py
python Skripte\analyze_simulation_results.py --variants "Dimensionierung" --rooms "101 lobby,109 office"
```

### create_comfort_plots.py

```powershell
python Skripte\create_comfort_plots.py comfort
python Skripte\create_comfort_plots.py comfort --output-type plot_analysis_overview
```

Hinweis: Dieses Skript nutzt intern die hinterlegten Raeume; fuer Varianten-/Raumauswahl besser `run_pipeline_display.py comfort` verwenden.

### prepare_data.py

```powershell
python Skripte\prepare_data.py
```

Hinweis: Direkter Start nutzt die Defaults im Skript. Fuer variable Pfade, Varianten oder Raeume besser `run_pipeline_display.py prepare` verwenden.

### apply_namensmapping.py

```powershell
python Skripte\Unterstützung\apply_namensmapping.py --dry-run
python Skripte\Unterstützung\apply_namensmapping.py
```

In der GUI ist dasselbe Mapping ueber das Dreipunktmenue bearbeitbar.

## Pflegehinweis

- Neue Skripte als eigenen Abschnitt dokumentieren.
- Befehle exakt mit echtem Skriptpfad eintragen.
- Optionen nicht zwischen verschiedenen Skripten vermischen.
- Testbeispiele immer mit `--output-root "9_test_\<testart>"`.


## Projektpflege

```powershell
python -m pip install -r requirements.txt
python -m ma_analyse --help
python -m ruff check src ma_analyse
python -m ruff format src ma_analyse
python -m pre_commit run --all-files
```

Hinweise:

- Die aktive Projektlogik liegt im Paket `src\ma_analyse`.
- Direkte Skriptaufrufe unter `Skripte\...` sind nur noch Altbestand; neue Befehle laufen ueber `python -m ma_analyse`.
- Grosse Daten- und Ausgabeordner bleiben lokal und werden nicht versioniert.
