# Changelog

Alle nennenswerten Aenderungen an `ma_analyse` werden in dieser Datei dokumentiert.

## Unreleased

Keine offenen Aenderungen.

## 0.5.0 - 2026-06-05

### Changed
- Dokumentation modularisiert: aktive Projektsteuerung liegt nun unter `docs/project/`, Fachdocumentation unter `docs/ma_analyse/`, `docs/ma_variants/`, `docs/ma_weather/` und gemeinsame Hinweise unter `docs/common/`.
- `docs/PLAN.md` aus der aktiven Steuerung geloest und als abgelegter Plan nach `docs/project/plans/archived/PLAN_Projektplan_Version_1_0_0.md` verschoben.
- `PLAN_STATUS.md` nach Modulen neu strukturiert und nach `docs/project/plans/PLAN_STATUS.md` verschoben.
- Umgesetzten Strukturplan P003 nach `docs/project/plans/archived/` verschoben und Planindex/Planstatus entsprechend aktualisiert.
- Plan-Inbox auf konsistente Markdown-Dateinamen fuer P001 und P002 normalisiert.
- `ma_variants`-Konfigurationen nach `config/ma_variants/` verschoben.
- Variantenbezogene Import-, Export- und IDA-Uebergabeordner nach `data/ma_variants/` verschoben.
- `ma_analyse` hart auf `data/ma_analyse/input`, `data/ma_analyse/database` und `data/ma_analyse/output` migriert; alte Root-Pfade werden nicht mehr unterstuetzt.
- Produkt- und Materialdokument-Platzhalter nach `data/catalogs/documents/` verschoben.
- `plot-template-examples` schreibt die Galerie-Dokumentation nun nach `docs/ma_analyse/plot_template_examples.md`.
- `.gitignore` an die neuen Datenbereiche angepasst.
- Variantenoberflaeche unter `src/ma_variants/ui/app.py` nach P001 in getrennte Bereiche fuer Parameter/Optionen, Variantenraum, Auswahl, Namensgebung, Export, Ergebnisse und Status gegliedert.

### Added
- Planindex, Strukturreview, Cleanup-Plan, Implementierungshinweise und getrennte Nutzerentscheidungsdateien unter `docs/project/` ergaenzt.
- Vorbereitete Modulbereiche fuer `ma_weather`, `data/ma_analyse`, `data/ma_weather`, `config/ma_analyse` und `config/ma_weather` angelegt.
- `data/test_output/README.md` dokumentiert den Ordner als lokalen, semi-wichtigen Arbeits- und Smoke-Test-Bereich.
- Testbare UI-Services fuer manuelle Variantenauswahl, reproduzierbare Zufallsauswahl, Filterauswahl und Namensgenerierung ergaenzt.
- Modulbezogene Befehlsuebersichten fuer `ma_variants`, `ma_weather` und gemeinsame Projektbefehle unter `docs/*/commands_<modul>.md` ergaenzt.
- `docs/project/UPDATE_ROUTINES.md` als feste Codex-Routine fuer `update repo`, `direkt update repo` und `update planung` ergaenzt.

### Removed
- Leeren, nicht versionierten Ordner `scripts/` entfernt.
- Alte Root-Datenordner fuer Analyse-Eingaben, Nutzdaten und regulaere Ausgaben nach erfolgreichem Datentransfer entfernt.
- Alten leeren Dokumentenordner `data/documents/` entfernt; aktive Produkt- und Materialdatenblaetter liegen unter `data/catalogs/documents/`.

### Fixed
- `COMMAND_DOC` zeigt nun auf `docs/ma_analyse/commands_analyse.md`.
- GUI-Import korrigiert: `get_heating_year_template_defaults` wird aus `ma_analyse.settings.plot_templates` geladen.
- Falschen relativen Import in `src/ma_analyse/analysis/comfort/plots.py` korrigiert, damit die `ma_analyse`-Tests wieder gesammelt werden koennen.
- Comfort-Template-Builder akzeptiert den vom gemeinsamen Plot-Template-Dispatcher uebergebenen `plot_template_config`-Parameter.

## 0.4.0 - 2026-06-04

### Added
- Projektlokale Codex-Konfiguration unter `.codex/config.toml` ergaenzt, damit dieses Repository mit `workspace-write`, `on-request` und Windows-`unelevated`-Sandbox gestartet werden kann.
- `docs/PLAN.md` als Projektplan Version 1.0.0 fuer den modularen Varianten-, Simulations- und Bewertungskern ergaenzt.
- Projektvorbereitung mit `config/.gitkeep`, `docs/WORKFLOW.md`, `docs/DATA_MODEL.md`, `docs/DECISIONS.md` und Pflege ueber den zentralen Root-`CHANGELOG.md` ergaenzt.
- Abschnitt 1 umgesetzt: neues Paket `ma_variants` mit `parameter_catalog`, `option_catalog`, `variant_manager`, `validation` und zentralen dataclass-Modellen fuer Parameter, Optionen und Varianten ergaenzt.
- Tests fuer die neuen `ma_variants`-Modelle und einfache Pflichtfeldvalidierung ergaenzt.
- Pytest-Cacheprovider deaktiviert und `tmp_path` lokal unter `data/test_output/pytest_runs` bereitgestellt, um gesperrte Windows-Cache- und Tempordner ohne Einfluss auf die Testausfuehrung zu umgehen.
- Abschnitt 2 umgesetzt: kleine YAML-Beispielkonfigurationen fuer Parameter und Optionen sowie dateibasierte Importer mit Validierung und JSON-Importbericht ergaenzt.
- Tests fuer Parameterimport, Optionsimport, doppelte Keys, fehlende Optionsgruppenreferenzen und Importberichte ergaenzt.
- Abschnitt 3 umgesetzt: Variantenzaehlung, einfache In-Memory-Variantenerzeugung und JSON-Export fuer Beispielvarianten ergaenzt.
- Beispielausgabe `data/exports/example_variants.json` und Tests fuer Variantenanzahl, Filterung aktiver Optionen und Variantengenerierung ergaenzt.
- Abschnitt 4 umgesetzt: manuelle Auswahl, Filterauswahl, reproduzierbare Zufallsauswahl und einfache Namensgenerierung mit Duplikatspruefung ergaenzt.
- Beispielregeln `config/naming/example_naming_rules.yaml`, Beispielausgabe `data/exports/example_selected_named_variants.json` und Tests fuer Auswahl/Naming ergaenzt.
- Abschnitt 5 umgesetzt: Basisexporte unter `ma_variants.reporting` mit JSON, CSV und Exportbericht fuer ausgewaehlte Varianten ergaenzt.
- Beispielausgaben `data/exports/example_variant_overview.json`, `data/exports/example_variant_overview.csv` und `data/exports/example_variant_report.json` sowie Tests fuer Export und Reporting ergaenzt.
- Abschnitt 6 umgesetzt: SQLAlchemy-/Alembic-Grundstruktur fuer PostgreSQL unter `ma_variants.database` mit env-basierter Verbindungskonfiguration ergaenzt.
- Datenbankmodelle, erste Migration und Repository-Funktionen fuer `parameters`, `option_sets`, `option_values`, `variants`, `variant_values` und `import_logs` ergaenzt.
- Beispielkonfiguration `config/database/example.env` ohne echte Zugangsdaten sowie lokale SQLite-Tests fuer die DB-Repositorylogik ergaenzt.
- Abschnitt 7 umgesetzt: `system_catalog` mit Systemtemplates, Templatewerten, einfachen Dependency-Regeln und Template-Aufloesung ergaenzt.
- Beispielsysteme `HEAT_01`, `COOL_01`, `PV_01` und `VENT_01` unter `config/systems/example_system_templates.yaml` sowie Tests fuer die Template-Aufloesung ergaenzt.
- Datenbankmodelle, Alembic-Migration und Repository-Funktionen fuer `system_templates`, `system_template_values` und `dependency_rules` ergaenzt.
- Abschnitt 8 umgesetzt: `ida_export` mit vorbereiteter IDA-ICE-Uebergabestruktur je Variante ergaenzt.
- Beispielkonfiguration `config/export/example_ida_export.yaml`, Zielordner `data/ida_exports` und Tests fuer Ordnererzeugung, Metadaten, aufgeloeste Parameter und Exportlog ergaenzt.
- Abschnitt 9 umgesetzt: `simulation_results` als lesender Adapter fuer vorhandene `ma_analyse`-Ergebnisordner ergaenzt.
- Zuordnung von `*_nutzdaten`-Ordnern zu Varianten, Kennwertimport aus Raum-CSV-Dateien und JSON-Export fuer Simulationsergebnisse ergaenzt.
- Schnittstelle zur bestehenden Analysepipeline in `docs/WORKFLOW.md` dokumentiert, ohne bestehende Analysefunktionen umzubauen.
- Abschnitt 10 umgesetzt: `economic_analysis` mit generischen Kostenannahmen, Energiepreisen, Wirtschaftlichkeitsszenarien und einfacher Varianten-Kostenberechnung ergaenzt.
- Beispielannahmen unter `config/economic/example_economic_assumptions.yaml`, JSON-/CSV-Export fuer Kostenergebnisse und `docs/ECONOMIC_MODEL.md` ergaenzt.
- Datenbankmodelle, Alembic-Migration und Repository-Funktionen fuer `generic_system_costs`, `energy_prices`, `economic_scenarios` und `variant_cost_results` ergaenzt.
- Tests fuer Import, Kostenberechnung mit Simulationsergebnissen, Fallback auf Beispielwerte, Systemtemplate-Zuordnung, Export und DB-Speicherung ergaenzt.
- Abschnitt 11 umgesetzt: Produkt-, Material-, Dokument- und Quellenkataloge mit dataclass-Modellen und einfachen Importern ergaenzt.
- Beispielkataloge unter `config/products`, `config/materials`, `config/documents` und `config/sources` sowie Dokumentpfadstruktur unter `data/documents` ergaenzt.
- Datenbankmodelle, Alembic-Migration und Repository-Funktionen fuer `products`, `product_properties`, `materials`, `material_properties`, `documents` und `sources` ergaenzt.
- Tests fuer Produkt-/Materialimport, Dokument-/Quellenimport und DB-Speicherung der neuen Kataloge ergaenzt.
- Abschnitt 12 umgesetzt: lokale Streamlit-Oberflaeche unter `ma_variants.ui` fuer Parameter, Optionen, Variantenanzahl, Variantenauswahl, Basisexport und Ergebnisdateien ergaenzt.
- Streamlit als Projektabhaengigkeit ergaenzt und testbare UI-Servicefunktionen ohne eigene Fachlogik eingefuehrt.
- Startbefehl und manuelle Testhinweise fuer die lokale Oberflaeche in `docs/WORKFLOW.md` dokumentiert.

## 0.3.2 - 2026-05-28

### Changed
- Aktualisiert die Dokumentation der Plot-Template-Beispiele mit stabilen Referenzbildern unter `docs/examples/plot_templates/`.
- Erweitert die Standard-Ausgabeformatverwaltung um kompakte Plot-Template-Formate und neue Internal-Loads-/Energy-Balance-/Thermal-Room-Climate-Ziele.
- Verbessert die Benutzerführung im GUI-Dialog für Ausgabeformate.
- Verfeinert die Beschriftung des Heating-Year-Zeitstrahls.

## 0.3.1 - 2026-05-26

### Added
- `plot-template` um Comfort-PNGs, Comfort-PDF-Uebersichten, Heating-/Cooling-Barplots und Thermisches-Raumklima-Templates erweitert.
- Neuer CLI-Befehl `plot-template-examples` erzeugt die reproduzierbare Dokumentationsgalerie unter `docs/examples/plot_templates/` und aktualisiert `docs/plot_template_examples.md`.

### Changed
- GUI-Fenster bleibt unter Windows auch mit eigener Titelleiste in der Taskleiste sichtbar.

## 0.3.0 - 2026-05-26

### Added
- Plot-Templates fuer interne Lasten aus Licht, Belegung und Equipment ergaenzt.
- Plot-Templates fuer Energiebilanz-Uebersichten in Year/Month/Week/Day ergaenzt.

### Changed
- GUI-Plot-Template-Auswahl erlaubt fuer `internal-loads-room-comparison` mehrere Raeume.
- Internal-Loads-Templates auf drei sichtbare Datenreihen aus Personen, Geraeten und Beleuchtung ausgerichtet; Week/Day nutzen gestapelte Lastprofil-Balken.

## 0.2.3 - 2026-05-26

### Added
- `plot-template` um `heating-month`, `heating-week`, `heating-day`, `cooling-year`, `cooling-month`, `cooling-week` und `cooling-day` erweitert.
- Gemeinsamen Template-Katalog und Timeline-Template-Builder fuer Heating-/Cooling-Zeitansichten ergaenzt.
- Tests fuer neue Plot-Template-Auswahlwerte, Zeitvalidierung und PNG-Smoke-Laeufe ergaenzt.
- `docs/PLAN_STATUS.md` als persoenliche Planungssuebersicht ergaenzt.
- Archivordner `docs/plan_status/` fuer regelmaessige Planstatus-Staende ergaenzt.

### Changed
- GUI-Template-Auswahl zeigt alle Plot-Templates und blendet Zeitdetails fuer Monats-, Wochen- und Tages-Templates ein.
- Professor-Agent unter `.github/agents/Professor.md` auf die Masterarbeits-Auswertungssoftware und Dokumentationsregeln ausgerichtet.
- GUI-Reset springt nach dem Zuruecksetzen wieder auf den ersten Schritt `Befehl`.
- Planungsuebersicht nach `docs/PLAN_STATUS.md` verschoben; `CHANGELOG.md` bleibt im Projekt-Root.
- `docs/PLAN_STATUS.md` auf aktive offene Punkte reduziert; Vollstand nach `docs/plan_status/2026-05-26.md` archiviert.

### Docs
- Plot-Template-Promotion ueber geteilte Helper in `docs/architecture.md` dokumentiert.

## 0.2.2 - 2026-05-25

### Added
- CLI-Befehl `plot-template` fuer manuell anpassbare Diagramm-Vorlagen ergaenzt.
- Erste Vorlage `heating-year` fuer eine oder mehrere Varianten und genau einen Raum eingefuehrt.
- Neues Modul `analysis/templates/` fuer Plot-Templates und Overlay-Logik ergaenzt.
- Plot-Template-Defaults ueber `settings/plot_templates.toml` und Loader `settings.plot_templates` konfigurierbar gemacht.
- Heating-Year-Template um Aussenlufttemperatur, operative Temperatur, Sollwertband und freie Overlay-Linien aus Raum-CSV oder `REPORT-AUX.prn` erweitert.
- GUI um die Schritte `Template` und `Ueberlagerungen` fuer Plot-Templates ergaenzt.
- Rechten GUI-Bereich um einen `summary`-Kasten fuer abgeschlossene vorherige Schritte erweitert.
- Unteren GUI-Bereich um einen `log`-Button neben `settings` erweitert, der die bestehende Protokollansicht oeffnet oder ein laufendes Analyse-Logfenster fokussiert.
- Tests fuer Plot-Template-Validierung, PRN-Stundenaggregation, Overlay-Kataloge, freie Overlays, TOML-Defaults, CLI-Optionen und Logging ergaenzt.

### Changed
- GUI im Wizard-Stil ueberarbeitet: linke Schritt-Navigation, rechter Inhaltsbereich und getrennte Kaesten fuer `summary` und aktuellen Schritt.
- GUI startet ohne vorausgewaehlte sichtbare Auswahl; Pflichtauswahlen werden erst beim Start validiert.
- Aktiver GUI-Schritt wird mit kleinem Punkt markiert, ohne blaue Flaechenmarkierung.
- Nach Auswahl eines Befehls springt die GUI automatisch zum naechsten sichtbaren Schritt.
- Automatisches Weitergehen auf weitere Einzelauswahl-Schritte erweitert; bei mehrteiligen Optionen wartet die GUI bis die Pflichtauswahl vollstaendig ist.
- Drei-Punkte-Menue aus der Titelleiste entfernt; Tools-Menue wird ueber `settings` geoeffnet.
- Rechte GUI-Scrollbar wird nur eingeblendet und per Mausrad genutzt, wenn der rechte Inhalt ueber das sichtbare Feld hinausgeht.
- Temperaturachsen-Eingaben in den Schritt `Ueberlagerungen` verschoben.
- `plot-template` kann nun mehrere Varianten aus der GUI-/CLI-Auswahl verarbeiten und erzeugt pro Variante ein eigenes Template-PNG.
- Heating-Year-Plot-Layout verfeinert: X-Achse naeher am Zeitstrahl, Abstand zur Monatsbeschriftung auf ca. 5 mm gesetzt und Abstand zwischen Zeitstrahl-Beschriftung und `Stunden [h]` auf ca. 3 mm reduziert.
- Positionen von Legende und `Stunden [h]` im Heating-Year-Plot getauscht.
- Jahres-Zeitstrahl trennt Grid-Markierungen oberhalb der Hauptlinie von 1000er-Stundenticks unterhalb der Hauptlinie.
- `plot-template` in die Laufprotokollierung aufgenommen.

### Docs
- `README.md`, `docs/commands.md` und `docs/architecture.md` um `plot-template`, Plot-Template-Config und Setup-/Start-Hinweise erweitert.
- `*.toml` als Package-Daten fuer `ma_analyse.settings` aufgenommen.
- Pytest-Testpfad in `pyproject.toml` dokumentiert.

## 0.2.1 - 2026-05-25

### Changed
- Analysecode weiter modularisiert: gemeinsame Energy-Logik fuer Heating/Cooling, Tabellenpaket fuer Excel-Berichte und Comfort-Module fuer Daten, Zonen, Tabellen und Plots ergaenzt.

## 0.2.0 - 2026-05-24

### Added
- `CHANGELOG.md` als zentrale Aenderungshistorie eingefuehrt.
- Laufprotokolle mit Schritt- und Gesamtlaufzeiten fuer Analysebefehle ergaenzt.
- `data/`-Ordnerstruktur mit versionierten Platzhalterdateien vorbereitet.
- Minimale Tests fuer CLI, Konfiguration, Logging, Varianten und Zeitfenster ergaenzt.

### Changed
- Projekt von losen Skripten zu einem Paket mit `src/ma_analyse` umgebaut.
- Code fachlich in `app`, `core`, `preprocessing`, `analysis`, `analysis/components`, `gui` und `settings` strukturiert.
- CLI-Einstieg auf `python -m ma_analyse ...` und `ma-analyse ...` ausgerichtet.
- Datenordner auf `data/input`, `data/database`, `data/output` und `data/test_output` umgestellt.
- `requirements.txt` auf direkte Runtime-Abhaengigkeiten reduziert.
- GUI so angepasst, dass der `all`-Befehl automatisch alle Raeume auswaehlt.

### Removed
- Alte Skriptstruktur unter `Skripte/` als Hauptschnittstelle entfernt.
- Uebergangsmodul `pipeline.py` entfernt, nachdem CLI, Commands und GUI ausgelagert wurden.
- Alte Root-Module wie `config.py`, `commands.py`, `heating.py`, `cooling.py`, `prepare.py`, `comfort.py` und `analyze.py` durch Paketmodule ersetzt.

## 0.1.0 - 2026-05-24

### Added
- Erster Paketstand fuer `ma_analyse` mit zentralem CLI-Einstieg.
