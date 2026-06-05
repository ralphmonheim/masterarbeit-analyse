# Workflow

Stand: 2026-06-04

Dieses Dokument beschreibt den geplanten Ablauf des modularen Varianten-, Simulations- und Bewertungssystems. Der Import kleiner Beispielparameter und Beispieloptionen ist als erster dateibasierter Schritt umgesetzt.

## Ausgangslage

Das bestehende Paket `ma_analyse` wertet bereits IDA-ICE-Simulationsergebnisse aus. Die aktuelle Pipeline liest Rohdaten aus `data/ma_analyse/input`, erzeugt Nutzdaten unter `data/ma_analyse/database` und schreibt Auswertungen nach `data/ma_analyse/output` oder `data/test_output`.

Diese Analysepipeline bleibt bestehen und wird nicht ungeprueft umgebaut. Der neue Varianten- und Bewertungskern wird zunaechst daneben geplant.

## Geplanter Ablauf

1. Parameterdefinitionen werden aus bearbeitbaren Dateien importiert.
2. Optionsgruppen und Optionswerte werden importiert und gegen die Parameter geprueft.
3. Systemvorlagen koennen mit generischen Variantenentscheidungen verknuepft werden.
4. Der Variantenmanager berechnet die theoretische Anzahl moeglicher Varianten.
5. Der Variantenmanager erzeugt einfache Variantenkombinationen.
6. Eine Auswahl reduziert die Varianten manuell oder mit einfachen Regeln.
7. Das Naming-Modul erzeugt stabile technische Keys und lesbare Variantennamen.
8. Die ausgewaehlten Varianten werden als Uebersicht exportiert.
9. Spaeter werden Varianten an IDA ICE uebergeben oder mit Simulationsergebnissen verknuepft.
10. Die bestehende Analysepipeline kann ueber einen Adapter Ergebnisse auswerten.
11. Eine generische Wirtschaftlichkeitsanalyse bewertet Varianten mit einfachen Kostenannahmen.

## Umgesetzter Beispielimport

Abschnitt 2 importiert kleine YAML-Beispieldateien:

- `config/ma_variants/parameters/example_parameters.yaml`
- `config/ma_variants/options/example_options.yaml`

Der kombinierte Import erfolgt ueber `ma_variants.importing.catalog.import_catalog`. Der Importer liest zuerst Optionsgruppen und Optionswerte, danach Parameter. Anschliessend prueft er, ob jede in einem Parameter referenzierte `option_set_key` tatsaechlich existiert.

Aktuelle Validierung:

- fehlende Pflichtfelder
- doppelte `parameter_key` Werte
- doppelte `option_key` Werte
- nicht vorhandene referenzierte Optionsgruppen
- ungueltige oder leere Pflichtwerte

Der Import liefert Python-Objekte fuer `Parameter`, `OptionSet` und `OptionValue`. Ein JSON-Importbericht wird standardmaessig nach `data/ma_variants/imports/import_report.json` geschrieben. In Tests kann ein eigener Berichtspfad uebergeben werden.

## Umgesetzte Variantenzaehlung und Variantenerzeugung

Abschnitt 3 nutzt die importierten Python-Objekte fuer eine einfache In-Memory-Variantenerzeugung.

Die theoretische Variantenanzahl wird mit `ma_variants.variant_manager.calculate_theoretical_variant_count` berechnet. Gezaehlt werden nur:

- Parameter mit `is_variant_relevant = true`
- Optionswerte mit `is_active = true`

Die Anzahl ist das Produkt der aktiven Optionswerte je variantenrelevantem Parameter. Wenn kein variantenrelevanter Parameter vorhanden ist oder fuer eine referenzierte Optionsgruppe keine aktive Option existiert, wird `0` zurueckgegeben.

Die einfache Variantenerzeugung erfolgt mit `ma_variants.variant_manager.generate_variants`. Sie bildet das kartesische Produkt der aktiven Optionsgruppen und gibt Python-Objekte zurueck:

- `Variant`
- Liste zugehoeriger `VariantValue`

Die Varianten bleiben zunaechst reine Python-Objekte. Ein JSON-Export ist ueber `ma_variants.variant_manager.export_variants_to_json` moeglich. Eine kleine Beispielausgabe liegt unter `data/ma_variants/exports/example_variants.json`.

## Umgesetzte Auswahl und Namensgebung

Abschnitt 4 reduziert erzeugte Varianten zunaechst ohne Optimierungslogik.

Die Auswahl liegt unter `ma_variants.selection`:

- `select_variants_by_key` waehlt manuell ueber `variant_key` und erhaelt die Reihenfolge der angefragten Keys.
- `filter_variants_by_options` filtert ueber `parameter_key` und erlaubte `option_key` Werte.
- `random_select_variants` waehlt mit festem `random_seed` reproduzierbar eine Teilmenge.

Die Namensgebung liegt unter `ma_variants.naming`. Namensregeln werden aus `config/ma_variants/naming/example_naming_rules.yaml` geladen. Die Beispielregeln nutzen:

- Prefix `V`
- dreistelligen Index
- `_` als Trenner
- kurze Optionstokens je Parameter

Ausgewaehlte Varianten koennen mit `apply_variant_names` benannt werden. Dabei werden die erzeugten Namen auf Duplikate geprueft. Eine kleine Beispielausgabe fuer ausgewaehlte und benannte Varianten liegt unter `data/ma_variants/exports/example_selected_named_variants.json`.

## Umgesetzte Export- und Reportingstruktur

Abschnitt 5 erstellt eine kontrollierbare Variantenuebersicht unter `ma_variants.reporting`. Der Export setzt auf bereits erzeugten, ausgewaehlten und optional benannten Varianten auf. Er veraendert keine IDA-ICE-Dateien und startet keine Simulation.

`export_variant_overview` schreibt standardmaessig drei Dateien nach `data/ma_variants/exports`:

- `selected_variants.json`: strukturierte Variantenliste mit `variant_count`, Variantendaten und zugehoerigen `VariantValue` Eintraegen.
- `selected_variants.csv`: flache Prueftabelle mit einer Zeile pro Variantenwert.
- `variant_report.json`: Exportbericht mit Anzahl aller erzeugten Varianten, Anzahl ausgewaehlter Varianten, verwendeten Parametern, verwendeten Optionsgruppen, Exportzeitpunkt und Hinweisen zu fehlenden Katalogdaten.

Die CSV-Struktur ist bewusst einfach gehalten:

- `variant_key`
- `variant_name`
- `status`
- `parameter_key`
- `option_key`
- `resolved_value`

Die Berichtsdaten dienen der manuellen Kontrolle, Dokumentation und spaeteren Uebergabeplanung. Kleine Beispielausgaben liegen unter:

- `data/ma_variants/exports/example_variant_overview.json`
- `data/ma_variants/exports/example_variant_overview.csv`
- `data/ma_variants/exports/example_variant_report.json`

## Umgesetzte Systemtemplate-Aufloesung

Abschnitt 7 fuehrt `ma_variants.system_catalog` ein. Der Systemkatalog liegt beispielhaft unter `config/ma_variants/systems/example_system_templates.yaml` und enthaelt kleine Vorlagen fuer:

- Heizung: `HEAT_01`
- Kuehlung: `COOL_01`
- PV: `PV_01`
- Lueftung: `VENT_01`

Eine Variante kann auf ein Systemtemplate verweisen, ohne alle Detailwerte selbst zu enthalten. Der Resolver erkennt ein aktives Template, wenn ein `VariantValue.option_key` oder ein `VariantValue.resolved_value` dem `system_template_key` entspricht.

Beispiel:

1. Eine Variante verweist auf `PV_01`.
2. `resolve_system_templates_for_variant` findet das aktive Template.
3. Der Resolver gibt konkrete Werte wie `pv_area_m2`, `pv_tilt_deg`, `pv_azimuth_deg` und `pv_peak_power_kwp` als `ResolvedSystemTemplateValue` zurueck.

Einfache Abhaengigkeitsregeln liegen als `DependencyRule` im selben Katalog. Aktuell wird nur geprueft, ob ein Template ein anderes Template voraussetzt. Im Beispiel benoetigt `COOL_01` das Template `VENT_01`.

## Vorbereitete IDA-ICE-Uebergabestruktur

Abschnitt 8 fuehrt `ma_variants.ida_export` ein. Ziel ist noch kein automatisches Schreiben in IDA-ICE-Dateien, sondern eine saubere, pruefbare Ordnerstruktur je ausgewaehlter Variante.

Die Beispielkonfiguration liegt unter `config/ma_variants/export/example_ida_export.yaml`. Sie definiert:

- Zielordner `data/ma_variants/ida_exports`
- Ordnernamensschema je Variante
- Dateinamen fuer Metadaten, aufgeloeste Parameter und Exportlog

`export_ida_variant_structure` erzeugt fuer jede ausgewaehlte Variante einen eigenen Ordner. Darin liegen:

- `metadata.json`
- `resolved_parameters.json`
- `export_log.txt`

`metadata.json` enthaelt `variant_key`, `variant_name`, `export_time`, `status` und `source_config`.

`resolved_parameters.json` enthaelt die aufgeloesten Parameterwerte. Dazu gehoeren die direkten `VariantValue` Werte und, falls uebergeben, die Werte aus der Systemtemplate-Aufloesung.

`export_log.txt` dokumentiert die wichtigsten Verarbeitungsschritte und haelt explizit fest, dass keine bestehenden IDA-ICE-Dateien veraendert, kein IDA-ICE-Variantenmanager gestartet und keine Simulation aus Python angestossen wurde.

Spaeter kann diese Struktur als Uebergabeschicht dienen, um IDA-ICE-Eingabedateien kontrolliert zu erzeugen oder anzupassen. Dieser spaetere Schritt braucht eigene Regeln fuer Dateizuordnung, Parametermapping, Validierung und Rueckmeldung aus IDA ICE.

## Kontrollierte Anbindung der bestehenden Analysepipeline

Abschnitt 9 fuehrt `ma_variants.simulation_results` als Adapter auf das vorhandene Analyseprojekt `ma_analyse` ein. Die bestehenden Analysefunktionen werden dabei nicht umgebaut. Der Adapter liest vorhandene aufbereitete Ergebnisordner und schreibt erste Kennwerte strukturiert als JSON.

### Erwartete Eingabedateien

Die Rohdatenaufbereitung `ma_analyse prepare` erwartet unter `data/ma_analyse/input/<Variante>/<Raum>/` pro Raum diese IDA-ICE-PRN-Dateien:

- `HEAT_BALANCE.prn`
- `IAQ.prn`
- `LOCAL-DE-COMF-DIAG-T.prn`
- `TEMPERATURES.prn`
- `ZONE-ENERGY.prn`

Die Rohdateien muessen eine Zeitspalte `time` enthalten. `prepare` fuehrt die Dateien stundenweise zusammen und schreibt Raumtabellen.

### Erwartete Ordnerstruktur

Rohdaten:

```text
data/ma_analyse/input/<Variante>/<Raum>/<PRN-Datei>
```

Aufbereitete Nutzdaten:

```text
data/ma_analyse/database/<Variante>_nutzdaten/<raum_name>.csv
data/ma_analyse/database/<Variante>_nutzdaten/<raum_name>.xlsx
```

Raumnamen werden fuer Dateien mit Unterstrichen geschrieben, zum Beispiel `101_lobby.csv`.

Regulaere Analyseausgaben liegen unter:

```text
data/ma_analyse/output/<Variante>/<run_id>_output/
```

Tests und Experimente koennen nach `data/test_output/` schreiben.

### Gelesene Ergebnisdateien

Der neue Adapter liest zunaechst nur die aufbereiteten Raum-CSV-Dateien aus `data/ma_analyse/database/<Variante>_nutzdaten`. Bestehende PNG-, PDF- und XLSX-Ausgaben werden nicht als Quelle benoetigt.

Wichtige Spalten aus den Raum-CSV-Dateien:

- `zone_energy_q_heat`
- `zone_energy_q_cool`
- `temperatures_top` oder `local_de_comf_diag_t_top`
- `iaq_relhum`
- `iaq_xco2vol`
- optional `local_de_comf_diag_t_ppd`
- optional `local_de_comf_diag_t_pmv`

### Kennwerte

`ma_variants.simulation_results` kann aktuell je Raum und aggregiert je Variante folgende Kennwerte lesen:

- `heating_energy_kwh`
- `cooling_energy_kwh`
- `max_heating_power_w`
- `max_cooling_power_w`
- `comfort_hours`
- `overtemperature_hours_25`
- `overtemperature_hours_27`
- `max_co2_ppm`
- `mean_co2_ppm`
- `max_ppd_percent`
- `max_pmv`
- `mean_pmv`

Fehlende Spalten werden pro Kennwert dokumentiert und nicht als ungepruefter Fehler behandelt.

### Bestehende Diagramme und Reports

Das bestehende `ma_analyse` erzeugt je nach Befehl:

- Comfort-Einzelraum-PNGs
- Comfort-PDF-Uebersichten
- Comfort-Analyseplots und Analyse-Excel
- Heating-Barplots und Heating-Zeitreihen als PNG
- Cooling-Barplots und Cooling-Zeitreihen als PNG
- Excel-Kennwertberichte unter `excel/`
- Plot-Template-Ausgaben fuer Heating, Cooling, Comfort, Energiebilanz, interne Lasten und Raumklima

### Neue Adapterfunktionen

- `discover_result_folders` findet vorhandene `*_nutzdaten`-Ordner.
- `map_result_folders_to_variants` ordnet diese Ordner vorhandenen `Variant`-Objekten zu.
- `collect_simulation_metrics` liest Kennwerte aus zugeordneten Ordnern.
- `export_simulation_metrics_to_json` schreibt die Kennwerte als JSON.

Der Adapter ist eine Leseschicht. Er startet keine Simulation, erzeugt keine neuen Analyseplots und veraendert keine bestehenden Analyseauswertungen.

## Generische Wirtschaftlichkeitsanalyse

Abschnitt 10 fuehrt `ma_variants.economic_analysis` ein. Das Modul bewertet Varianten mit generischen Kostenannahmen und bleibt bewusst unabhaengig von einer Produkt- oder Materialdatenbank.

Die Beispielannahmen liegen unter:

```text
config/ma_variants/economic/example_economic_assumptions.yaml
```

Der Import erfolgt ueber `import_economic_assumptions` und prueft:

- fehlende Pflichtfelder
- doppelte `system_type` Werte
- doppelte `energy_carrier` Werte
- doppelte `scenario_key` Werte
- Szenarien, die fehlende Energiepreise referenzieren
- ungueltige Kosten-, Preis- oder Zeitraumwerte

`calculate_variant_costs` berechnet je Variante:

- Investitionskosten
- Wartungskosten pro Jahr
- Wartungskosten ueber den Betrachtungszeitraum
- einfache Ersatzinvestitionen anhand der Lebensdauer
- Energiekosten pro Jahr
- Energiekosten ueber den Betrachtungszeitraum
- Gesamtkosten

Wenn Simulationsergebnisse aus `ma_variants.simulation_results` vorhanden sind, werden `heating_energy_kwh` und `cooling_energy_kwh` aus den aggregierten `summary_metrics` genutzt. Fehlende Energiewerte fallen auf Beispielwerte aus dem Szenario zurueck und werden im Ergebnis mit `uses_example_energy_values` sowie `assumption_notes` gekennzeichnet.

Ausgewaehlte Systemtypen koennen direkt uebergeben oder aus Systemtemplate-Keys abgeleitet werden. So kann eine Variante zum Beispiel auf `PV_01` verweisen, waehrend die Wirtschaftlichkeitsrechnung den generischen Systemtyp `pv` bewertet.

Die Ergebnisse koennen als JSON und CSV nach `data/ma_variants/exports` geschrieben werden:

- `variant_cost_results.json`
- `variant_cost_results.csv`

Die Annahmen, Formeln und Grenzen sind zusaetzlich in `docs/ma_variants/economic_model.md` dokumentiert.

## Lokale Bedienoberflaeche

Abschnitt 12 fuehrt `ma_variants.ui` als einfache lokale Oberflaeche ein. Die erste Umsetzung nutzt Streamlit und liegt unter:

```text
src/ma_variants/ui/app.py
```

Start aus dem Projektverzeichnis:

```powershell
.\.venv\Scripts\python.exe -m streamlit run .\src\ma_variants\ui\app.py
```

Die Oberflaeche nutzt vorhandene Funktionen aus den Modulen:

- `import_catalog`
- `calculate_theoretical_variant_count`
- `generate_variants`
- `select_variants_by_key`
- `random_select_variants`
- `filter_variants_by_options`
- `apply_variant_names`
- `export_variant_overview`

Die UI enthaelt keine eigene Fachlogik. Sie zeigt Parameter und Optionen an, berechnet die Variantenanzahl ueber den Variantenmanager, erzeugt die vorhandenen Beispielvarianten, erlaubt manuelle Auswahl, reproduzierbare Zufallsauswahl und Filterauswahl, wendet optional Namensregeln an, startet den Basisexport und listet vorhandene Ergebnisdateien aus dem Exportordner.

Vorbereitete, aber noch nicht implementierte Auswahlmethoden werden sichtbar gefuehrt:

- Monte Carlo
- strukturierte Abdeckung
- Sensitivitaetsvarianten
- regelbasierte Auswahl

Diese Methoden sind absichtlich Platzhalter. Es gibt noch keine Optimierung, keine Sensitivitaetsanalyse und keine komplexe regelbasierte Variantenauswahl.

Manuelle Testhinweise:

1. App mit dem oben genannten Streamlit-Befehl starten.
2. Standardpfade fuer Parameter und Optionen unveraendert lassen.
3. Pruefen, ob 3 Parameter, 6 Optionswerte und 8 Varianten angezeigt werden.
4. Im Tab `Auswahl` manuelle Auswahl, Zufallsauswahl mit festem `random_seed` und Filterauswahl pruefen.
5. Im Tab `Namensgebung` pruefen, ob kurze eindeutige Namen angezeigt werden.
6. Export starten.
7. Im Tab `Ergebnisse` pruefen, ob `selected_variants.json`, `selected_variants.csv` und `variant_report.json` angezeigt werden.

## Geplante Datenbereiche

- `config/ma_variants/`: bearbeitbare Variantenkonfigurationen fuer Parameter, Optionen, Systeme, Namensregeln, Wirtschaftlichkeit, IDA-Export, Datenbank, Produkte, Materialien, Dokumente und Quellen.
- `config/ma_analyse/`: vorbereiteter Bereich fuer spaetere Analysekonfigurationen.
- `config/ma_weather/`: vorbereiteter Bereich fuer spaetere Wetterdatenkonfigurationen.
- `data/ma_analyse/input/`: verbindlicher Pfad fuer vorhandene IDA-ICE-Rohdaten und Variantenordner der bestehenden Analysepipeline.
- `data/ma_analyse/database/`: verbindlicher Pfad fuer vorhandene aufbereitete Nutzdaten aus der Analysepipeline.
- `data/ma_analyse/output/`: verbindlicher Pfad fuer regulaere Analyseausgaben.
- `data/test_output/`: lokaler, semi-wichtiger Smoke-Test- und Arbeitsordner; der Ordner wird bewusst separat gefuehrt und regelmaessig manuell geleert.
- `data/ma_variants/imports/`: Zielordner fuer Varianten-Importberichte.
- `data/ma_variants/exports/`: Zielordner fuer Variantenuebersichten, Basisexporte, Wirtschaftlichkeitsergebnisse und Exportberichte.
- `data/ma_variants/ida_exports/`: Zielordner fuer vorbereitete IDA-ICE-Uebergabestrukturen je Variante.
- `data/catalogs/documents/`: Zielordner fuer referenzierte Produkt- und Materialdatenblaetter; Dateien werden nicht in PostgreSQL gespeichert.
- `data/common/reports/`: vorbereiteter Bereich fuer uebergreifende Berichte.

## Abgrenzung

In diesem Abschnitt werden nur kleine Beispielkonfigurationen importiert. Es gibt noch keinen vollstaendigen Import vorhandener PEVA-/Excel-/Prisma-Dateien, keine direkten Datenbankimporte aus Fachdateien, keine Optimierungen und keine vollstaendige IDA-ICE-Dateibearbeitung.

Die Variantenerzeugung beruecksichtigt noch keine komplexen Abhaengigkeiten und keine Optimierungslogik. Systemtemplates werden erst nachgelagert aufgeloest und veraendern die einfache Kombinatorik nicht.

Die Variantenauswahl ist bewusst einfach gehalten. Es gibt noch keine maschinelle Auswahl, keine Optimierungsalgorithmen, keine Sensitivitaetsanalyse und keine IDA-ICE-Exportstruktur.

Die Exportstruktur ist weiterhin ein Basisexport. Es gibt noch keine echte IDA-ICE-Ordnerstruktur, kein Schreiben in IDA-ICE-Eingabedateien, keinen Simulationsstart und keine Wirtschaftlichkeitsberechnung.

Die Systemtemplates sind bewusst nur Beispielvorlagen. Es gibt noch keine vollstaendige technische Systembibliothek, keine automatische Produktzuordnung, keine detaillierte Wirtschaftlichkeitsbewertung und keine vollstaendige IDA-ICE-Dateiaenderung.

Die IDA-ICE-Uebergabestruktur ist ebenfalls nur vorbereitet. Es gibt noch keine vollstaendige automatische Aenderung aller IDA-ICE-Dateien, keinen Start des IDA-ICE-Variantenmanagers und keinen Simulationsstart aus Python.

Die Analyseanbindung ist ebenfalls bewusst schmal. Es gibt keine komplette Neuschreibung des Analyseprojekts und keine ungeprueften Aenderungen an bestehenden Auswertungen.

Die Wirtschaftlichkeitsanalyse ist generisch. Es gibt keine produktspezifische Bewertung, keine detaillierte LCA, keine Materialdatenbank, keine automatische Produktzuordnung, keine Diskontierung und keine belastbare Kostenfreigabe der Beispielwerte.

Die Produkt-, Material-, Dokument- und Quellenkataloge sind nur strukturell vorbereitet. Es gibt keine automatische Produktrecherche, kein KI-Training, keine vollstaendige Herstellerdatenbank und keine Pflicht, Produktdaten fuer alle Varianten zu erfassen.
