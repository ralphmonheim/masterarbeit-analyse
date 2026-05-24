# Zentrales Namens-Mapping

Dieses Dokument ist die zentrale Quelle fuer spaetere Namensaenderungen in den Skripten.

Regeln:
- Trage neue Werte ausschliesslich in der Spalte `Neuer Name` ein.
- Leere `Neuer Name`-Felder bedeuten: keine Aenderung.
- `Aktueller Name` bleibt als Referenz unveraendert.
- Die Spalte `Fundstellen/Hinweis` enthaelt technische Hinweise fuer die spaetere automatische Uebernahme.
- Die automatische Uebernahme wird ueber `python Skripte\apply_namensmapping.py` ausgefuehrt.

## Ordner & Pfade

| Kategorie | Aktueller Name | Neuer Name | Verwendung | Fundstellen/Hinweis |
| --- | --- | --- | --- | --- |
| Ordner & Pfade | 0_Input |  | Standard-Input-Ordner fuer Rohdatenvarianten | ID=path.input_dir; MODE=literal; prepare_data.py, run_pipeline_display.py, 0_Befehle.md |
| Ordner & Pfade | 1_Datenbank |  | Standard-Ausgabeordner fuer aufbereitete Nutzdaten | ID=path.database_dir; MODE=literal; alle Hauptskripte, 0_Befehle.md |
| Ordner & Pfade | 2_Output |  | Standard-Output-Ordner fuer Diagramme, PDFs und Excel | ID=path.output_dir; MODE=literal; Plot-/Analyse-/Heating-Skripte, 0_Befehle.md |
| Ordner & Pfade | analyze_simulation |  | Unterordner fuer die Excel-Gesamtauswertung | ID=path.analyze_simulation; MODE=literal; analyze_simulation_results.py |
| Ordner & Pfade | HeatingComparison |  | Vergleichsname fuer Heiz-Ausgaben und Prefixe | ID=path.heating_comparison_root; MODE=literal; compare_heating_loads.py |

## Befehle & CLI

| Kategorie | Aktueller Name | Neuer Name | Verwendung | Fundstellen/Hinweis |
| --- | --- | --- | --- | --- |
| Befehle & CLI | prepare |  | CLI-Befehl fuer Datenaufbereitung | ID=command.prepare; MODE=quoted; run_pipeline_display.py, 0_Befehle.md |
| Befehle & CLI | comfort |  | CLI-Befehl fuer Komfortausgaben | ID=command.comfort; MODE=quoted; run_pipeline_display.py, create_comfort_plots.py, 0_Befehle.md |
| Befehle & CLI | analyze_data |  | CLI-Befehl fuer Excel-Auswertung | ID=command.analyze_data; MODE=literal; run_pipeline_display.py, 0_Befehle.md |
| Befehle & CLI | heating |  | CLI-Befehl fuer Heizvergleich | ID=command.heating; MODE=quoted; run_pipeline_display.py, compare_heating_loads.py, 0_Befehle.md |
| Befehle & CLI | all |  | CLI-Sammelbefehl fuer den kombinierten Lauf | ID=command.all; MODE=quoted; run_pipeline_display.py, 0_Befehle.md |
| Befehle & CLI | --input-dir |  | CLI-Option fuer den Input-Ordner | ID=option.input_dir; MODE=literal; run_pipeline_display.py, 0_Befehle.md |
| Befehle & CLI | --datenbank-dir |  | CLI-Option fuer den Datenbank-Ordner | ID=option.database_dir; MODE=literal; run_pipeline_display.py, analyze_simulation_results.py, create_comfort_plots.py, 0_Befehle.md |
| Befehle & CLI | --output-root |  | CLI-Option fuer das Ausgabe-Root | ID=option.output_root; MODE=literal; run_pipeline_display.py, analyze_simulation_results.py, create_comfort_plots.py, compare_heating_loads.py, 0_Befehle.md |
| Befehle & CLI | --run-id |  | CLI-Option fuer eine feste Lauf-ID | ID=option.run_id; MODE=literal; run_pipeline_display.py, analyze_simulation_results.py, create_comfort_plots.py, compare_heating_loads.py, 0_Befehle.md |
| Befehle & CLI | --variants |  | CLI-Option fuer Variantenlisten | ID=option.variants; MODE=literal; run_pipeline_display.py, compare_heating_loads.py, 0_Befehle.md |
| Befehle & CLI | --rooms |  | CLI-Option fuer Raumlisten | ID=option.rooms; MODE=literal; run_pipeline_display.py, analyze_simulation_results.py, 0_Befehle.md |
| Befehle & CLI | --view |  | CLI-Option fuer Darstellungsmodus bei Heating | ID=option.view; MODE=literal; run_pipeline_display.py, compare_heating_loads.py, 0_Befehle.md |
| Befehle & CLI | --heating-mode |  | CLI-Option fuer Vergleichs- oder Einzelmodus | ID=option.heating_mode; MODE=literal; run_pipeline_display.py, 0_Befehle.md |

## Output-Struktur

| Kategorie | Aktueller Name | Neuer Name | Verwendung | Fundstellen/Hinweis |
| --- | --- | --- | --- | --- |
| Output-Struktur | plots |  | Interner Schrittname und Plot-Unterordner beim all-Befehl | ID=output.plots; MODE=quoted; run_pipeline_display.py, create_comfort_plots.py |
| Output-Struktur | overview |  | Interner Schrittname fuer PDF-Uebersichten | ID=output.overview; MODE=quoted; run_pipeline_display.py |
| Output-Struktur | analysis |  | Interner Schrittname und Analyse-Unterordner | ID=output.analysis; MODE=quoted; run_pipeline_display.py, create_comfort_plots.py |
| Output-Struktur | analyze |  | Interner Schrittname fuer Excel-Auswertung | ID=output.analyze; MODE=quoted; run_pipeline_display.py |
| Output-Struktur | excel |  | Unterordner fuer Excel-Dateien | ID=output.excel; MODE=quoted; analyze_simulation_results.py |

## Datei- & Run-Namen

| Kategorie | Aktueller Name | Neuer Name | Verwendung | Fundstellen/Hinweis |
| --- | --- | --- | --- | --- |
| Datei- & Run-Namen | Dimensionierung |  | Tagesprefix fuer Comfort-/Excel-Dateien | ID=naming.dimensionierung; MODE=literal; create_comfort_plots.py, analyze_simulation_results.py, compare_heating_loads.py |
| Datei- & Run-Namen | _output |  | Standardsuffix fuer variantenbezogene Run-Ordner im Output | ID=naming.variant_run_suffix; MODE=literal; create_comfort_plots.py, compare_heating_loads.py |
| Datei- & Run-Namen | excel-analysis |  | Run-ID-Suffix fuer Excel-Gesamtauswertung | ID=naming.excel_analysis; MODE=literal; analyze_simulation_results.py |
| Datei- & Run-Namen | heating_comparison |  | Run-ID-Suffix fuer Heating-Ausgaben | ID=naming.heating_comparison; MODE=literal; compare_heating_loads.py |
| Datei- & Run-Namen | plots_uebersicht |  | Dateinamensuffix fuer Comfort-Overview-PDF | ID=naming.plots_overview_suffix; MODE=literal; create_comfort_plots.py |
| Datei- & Run-Namen | analyse_uebersicht |  | Dateinamensuffix fuer Analyse-Overview-PDF | ID=naming.analysis_overview_suffix; MODE=literal; create_comfort_plots.py |
| Datei- & Run-Namen | analysis_table |  | Dateinamensuffix fuer Analyse-Excel je Variante | ID=naming.analysis_table_suffix; MODE=literal; create_comfort_plots.py |

## GUI- & Textbezeichnungen

| Kategorie | Aktueller Name | Neuer Name | Verwendung | Fundstellen/Hinweis |
| --- | --- | --- | --- | --- |
| GUI- & Textbezeichnungen | ANALYSE TOOLS |  | Fenstertitel und Ueberschrift der GUI | ID=ui.app_title; MODE=literal; run_pipeline_display.py |
| GUI- & Textbezeichnungen | Alle Varianten |  | GUI-Auswahl fuer alle Varianten | ID=ui.scope_all; MODE=literal; run_pipeline_display.py |
| GUI- & Textbezeichnungen | Eine Variante |  | GUI-Auswahl fuer Einzelvariante | ID=ui.scope_single; MODE=literal; run_pipeline_display.py |
| GUI- & Textbezeichnungen | Mehrere Varianten |  | GUI-Auswahl fuer mehrere Varianten | ID=ui.scope_multiple; MODE=literal; run_pipeline_display.py |
| GUI- & Textbezeichnungen | Analyse Raum |  | GUI-Analyseebene fuer Raum-Auswahl | ID=ui.analysis_room; MODE=literal; run_pipeline_display.py |
| GUI- & Textbezeichnungen | Analyse Variante |  | GUI-Analyseebene fuer Varianten-Sicht | ID=ui.analysis_variant; MODE=literal; run_pipeline_display.py |

## Suffixe & Variantenlogik

| Kategorie | Aktueller Name | Neuer Name | Verwendung | Fundstellen/Hinweis |
| --- | --- | --- | --- | --- |
| Suffixe & Variantenlogik | _rohdaten |  | Varianten-Suffix fuer Input-Daten | ID=suffix.rawdata; MODE=literal; prepare_data.py, run_pipeline_display.py |
| Suffixe & Variantenlogik | _nutzdaten |  | Varianten-Suffix fuer aufbereitete Daten | ID=suffix.processeddata; MODE=literal; prepare_data.py, create_comfort_plots.py, compare_heating_loads.py, analyze_simulation_results.py, run_pipeline_display.py |

## Raeume

| Kategorie | Aktueller Name | Neuer Name | Verwendung | Fundstellen/Hinweis |
| --- | --- | --- | --- | --- |
| Raeume | 101 lobby |  | Raumname in ROOMS-Listen, Dateinamen und GUI | ID=room.101_lobby; MODE=literal; alle Hauptskripte, 0_Befehle.md |
| Raeume | 109 office |  | Raumname in ROOMS-Listen, Dateinamen und GUI | ID=room.109_office; MODE=literal; alle Hauptskripte, 0_Befehle.md |
| Raeume | 113 meeting |  | Raumname in ROOMS-Listen, Dateinamen und GUI | ID=room.113_meeting; MODE=literal; alle Hauptskripte, 0_Befehle.md |
| Raeume | 208 office |  | Raumname in ROOMS-Listen, Dateinamen und GUI | ID=room.208_office; MODE=literal; alle Hauptskripte, 0_Befehle.md |
| Raeume | 214 meeting |  | Raumname in ROOMS-Listen, Dateinamen und GUI | ID=room.214_meeting; MODE=literal; alle Hauptskripte, 0_Befehle.md |
