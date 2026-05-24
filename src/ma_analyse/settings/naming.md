# Zentrales Namens-Mapping

Dieses Dokument ist die zentrale Quelle fuer spaetere Namensaenderungen in den Modulen.

Regeln:
- Trage neue Werte ausschliesslich in der Spalte `Neuer Name` ein.
- Leere `Neuer Name`-Felder bedeuten: keine Aenderung.
- `Aktueller Name` bleibt als Referenz unveraendert.
- Die Spalte `Fundstellen/Hinweis` enthaelt technische Hinweise fuer die spaetere automatische Uebernahme.
- Die automatische Uebernahme wird ueber `python -m ma_analyse.settings.naming` ausgefuehrt.

## Ordner & Pfade

| Kategorie | Aktueller Name | Neuer Name | Verwendung | Fundstellen/Hinweis |
| --- | --- | --- | --- | --- |
| Ordner & Pfade | data/input |  | Standard-Input-Ordner fuer Rohdatenvarianten | ID=path.input_dir; MODE=literal; core/config.py, app/cli.py, preprocessing/prepare.py, docs/commands.md |
| Ordner & Pfade | data/database |  | Standard-Ausgabeordner fuer aufbereitete Nutzdaten | ID=path.database_dir; MODE=literal; alle Hauptmodule, docs/commands.md |
| Ordner & Pfade | data/output |  | Standard-Output-Ordner fuer Diagramme, PDFs und Excel | ID=path.output_dir; MODE=literal; Plot-/Analyse-/Heating-Module, docs/commands.md |
| Ordner & Pfade | data/test_output |  | Standard-Ordner fuer lokale Test- und Smoke-Test-Ausgaben | ID=path.test_output_dir; MODE=literal; docs/commands.md, tests |
| Ordner & Pfade | analyze_simulation |  | Unterordner fuer die Excel-Gesamtauswertung | ID=path.analyze_simulation; MODE=literal; analysis/excel.py |
| Ordner & Pfade | HeatingComparison |  | Vergleichsname fuer Heiz-Ausgaben und Prefixe | ID=path.heating_comparison_root; MODE=literal; analysis/heating.py |

## Befehle & CLI

| Kategorie | Aktueller Name | Neuer Name | Verwendung | Fundstellen/Hinweis |
| --- | --- | --- | --- | --- |
| Befehle & CLI | prepare |  | CLI-Befehl fuer Datenaufbereitung | ID=command.prepare; MODE=quoted; app/cli.py, app/commands.py, docs/commands.md |
| Befehle & CLI | comfort |  | CLI-Befehl fuer Komfortausgaben | ID=command.comfort; MODE=quoted; app/cli.py, app/commands.py, analysis/comfort/main.py, docs/commands.md |
| Befehle & CLI | analyze_data |  | CLI-Befehl fuer Excel-Auswertung | ID=command.analyze_data; MODE=literal; app/cli.py, app/commands.py, docs/commands.md |
| Befehle & CLI | heating |  | CLI-Befehl fuer Heizvergleich | ID=command.heating; MODE=quoted; app/cli.py, app/commands.py, analysis/heating.py, docs/commands.md |
| Befehle & CLI | all |  | CLI-Sammelbefehl fuer den kombinierten Lauf | ID=command.all; MODE=quoted; app/cli.py, app/commands.py, docs/commands.md |
| Befehle & CLI | --input-dir |  | CLI-Option fuer den Input-Ordner | ID=option.input_dir; MODE=literal; app/cli.py, app/commands.py, docs/commands.md |
| Befehle & CLI | --datenbank-dir |  | CLI-Option fuer den Datenbank-Ordner | ID=option.database_dir; MODE=literal; app/cli.py, app/commands.py, analysis/excel.py, analysis/comfort/main.py, docs/commands.md |
| Befehle & CLI | --output-root |  | CLI-Option fuer das Ausgabe-Root | ID=option.output_root; MODE=literal; app/cli.py, app/commands.py, analysis/excel.py, analysis/comfort/main.py, analysis/heating.py, docs/commands.md |
| Befehle & CLI | --run-id |  | CLI-Option fuer eine feste Lauf-ID | ID=option.run_id; MODE=literal; app/cli.py, app/commands.py, analysis/excel.py, analysis/comfort/main.py, analysis/heating.py, docs/commands.md |
| Befehle & CLI | --variants |  | CLI-Option fuer Variantenlisten | ID=option.variants; MODE=literal; app/cli.py, app/commands.py, analysis/heating.py, docs/commands.md |
| Befehle & CLI | --rooms |  | CLI-Option fuer Raumlisten | ID=option.rooms; MODE=literal; app/cli.py, app/commands.py, analysis/excel.py, docs/commands.md |
| Befehle & CLI | --view |  | CLI-Option fuer Darstellungsmodus bei Heating | ID=option.view; MODE=literal; app/cli.py, app/commands.py, analysis/heating.py, docs/commands.md |
| Befehle & CLI | --heating-mode |  | CLI-Option fuer Vergleichs- oder Einzelmodus | ID=option.heating_mode; MODE=literal; app/cli.py, app/commands.py, docs/commands.md |

## Output-Struktur

| Kategorie | Aktueller Name | Neuer Name | Verwendung | Fundstellen/Hinweis |
| --- | --- | --- | --- | --- |
| Output-Struktur | plots |  | Interner Schrittname und Plot-Unterordner beim all-Befehl | ID=output.plots; MODE=quoted; app/commands.py, analysis/comfort/main.py |
| Output-Struktur | overview |  | Interner Schrittname fuer PDF-Uebersichten | ID=output.overview; MODE=quoted; app/commands.py |
| Output-Struktur | analysis |  | Interner Schrittname und Analyse-Unterordner | ID=output.analysis; MODE=quoted; app/commands.py, analysis/comfort/main.py |
| Output-Struktur | analyze |  | Interner Schrittname fuer Excel-Auswertung | ID=output.analyze; MODE=quoted; app/commands.py |
| Output-Struktur | excel |  | Unterordner fuer Excel-Dateien | ID=output.excel; MODE=quoted; analysis/excel.py |

## Datei- & Run-Namen

| Kategorie | Aktueller Name | Neuer Name | Verwendung | Fundstellen/Hinweis |
| --- | --- | --- | --- | --- |
| Datei- & Run-Namen | Dimensionierung |  | Tagesprefix fuer Comfort-/Excel-Dateien | ID=naming.dimensionierung; MODE=literal; analysis/comfort/main.py, analysis/excel.py, analysis/heating.py |
| Datei- & Run-Namen | _output |  | Standardsuffix fuer variantenbezogene Run-Ordner im Output | ID=naming.variant_run_suffix; MODE=literal; analysis/comfort/main.py, analysis/heating.py |
| Datei- & Run-Namen | excel-analysis |  | Run-ID-Suffix fuer Excel-Gesamtauswertung | ID=naming.excel_analysis; MODE=literal; analysis/excel.py |
| Datei- & Run-Namen | heating_comparison |  | Run-ID-Suffix fuer Heating-Ausgaben | ID=naming.heating_comparison; MODE=literal; analysis/heating.py |
| Datei- & Run-Namen | plots_uebersicht |  | Dateinamensuffix fuer Comfort-Overview-PDF | ID=naming.plots_overview_suffix; MODE=literal; analysis/comfort/main.py |
| Datei- & Run-Namen | analyse_uebersicht |  | Dateinamensuffix fuer Analyse-Overview-PDF | ID=naming.analysis_overview_suffix; MODE=literal; analysis/comfort/main.py |
| Datei- & Run-Namen | analysis_table |  | Dateinamensuffix fuer Analyse-Excel je Variante | ID=naming.analysis_table_suffix; MODE=literal; analysis/comfort/main.py |

## GUI- & Textbezeichnungen

| Kategorie | Aktueller Name | Neuer Name | Verwendung | Fundstellen/Hinweis |
| --- | --- | --- | --- | --- |
| GUI- & Textbezeichnungen | ANALYSE TOOLS |  | Fenstertitel und Ueberschrift der GUI | ID=ui.app_title; MODE=literal; gui/app.py |
| GUI- & Textbezeichnungen | Alle Varianten |  | GUI-Auswahl fuer alle Varianten | ID=ui.scope_all; MODE=literal; gui/app.py |
| GUI- & Textbezeichnungen | Eine Variante |  | GUI-Auswahl fuer Einzelvariante | ID=ui.scope_single; MODE=literal; gui/app.py |
| GUI- & Textbezeichnungen | Mehrere Varianten |  | GUI-Auswahl fuer mehrere Varianten | ID=ui.scope_multiple; MODE=literal; gui/app.py |
| GUI- & Textbezeichnungen | Analyse Raum |  | GUI-Analyseebene fuer Raum-Auswahl | ID=ui.analysis_room; MODE=literal; gui/app.py |
| GUI- & Textbezeichnungen | Analyse Variante |  | GUI-Analyseebene fuer Varianten-Sicht | ID=ui.analysis_variant; MODE=literal; gui/app.py |

## Suffixe & Variantenlogik

| Kategorie | Aktueller Name | Neuer Name | Verwendung | Fundstellen/Hinweis |
| --- | --- | --- | --- | --- |
| Suffixe & Variantenlogik | _rohdaten |  | Varianten-Suffix fuer Input-Daten | ID=suffix.rawdata; MODE=literal; preprocessing/prepare.py, gui/selection.py |
| Suffixe & Variantenlogik | _nutzdaten |  | Varianten-Suffix fuer aufbereitete Daten | ID=suffix.processeddata; MODE=literal; preprocessing/prepare.py, analysis/comfort/main.py, analysis/heating.py, analysis/excel.py, gui/selection.py |

## Raeume

| Kategorie | Aktueller Name | Neuer Name | Verwendung | Fundstellen/Hinweis |
| --- | --- | --- | --- | --- |
| Raeume | 101 lobby |  | Raumname in ROOMS-Listen, Dateinamen und GUI | ID=room.101_lobby; MODE=literal; alle Hauptmodule, docs/commands.md |
| Raeume | 109 office |  | Raumname in ROOMS-Listen, Dateinamen und GUI | ID=room.109_office; MODE=literal; alle Hauptmodule, docs/commands.md |
| Raeume | 113 meeting |  | Raumname in ROOMS-Listen, Dateinamen und GUI | ID=room.113_meeting; MODE=literal; alle Hauptmodule, docs/commands.md |
| Raeume | 208 office |  | Raumname in ROOMS-Listen, Dateinamen und GUI | ID=room.208_office; MODE=literal; alle Hauptmodule, docs/commands.md |
| Raeume | 214 meeting |  | Raumname in ROOMS-Listen, Dateinamen und GUI | ID=room.214_meeting; MODE=literal; alle Hauptmodule, docs/commands.md |






