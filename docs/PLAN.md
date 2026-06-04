# Projektplan Version 1.0.0

Stand: 2026-06-02

Dieser Plan beschreibt den ersten stabilen Ausbau des bestehenden Python-Projekts zu einem modularen Varianten-, Simulations- und Bewertungssystem fuer IDA ICE. Ziel von Version 1 ist nicht das vollstaendige Endsystem, sondern ein technischer Kern fuer Parameter, Optionen, Varianten, Auswahl, Benennung und Export.

## Status dieses Umsetzungsschritts

Dieser Schritt ist reine Projektvorbereitung. Es werden nur Grundstruktur und Dokumentation vorbereitet. Es werden keine bestehenden Analysefunktionen umgebaut, keine Variantenlogik implementiert, keine Datenbanklogik angelegt und kein IDA-ICE-Export umgesetzt.

## 1. Bestandsanalyse

### Vorhandene Projektstruktur

Das Repository ist bereits als Python-Paket `ma_analyse` unter `src/ma_analyse` aufgebaut. Der aktuelle Paketstand ist laut `pyproject.toml` Version `0.4.0`.

Wesentliche vorhandene Bereiche:

- `src/ma_analyse/app`: CLI-Parser und Befehlssteuerung.
- `src/ma_analyse/gui`: grafische Oberflaeche mit gemeinsamer Befehlslogik.
- `src/ma_analyse/core`: zentrale Pfade, Raumlisten, Dateinamen und Logging.
- `src/ma_analyse/preprocessing`: Aufbereitung von IDA-ICE-PRN-Rohdaten zu Raumtabellen.
- `src/ma_analyse/analysis`: Comfort-, Heating-, Cooling-, Excel- und Plot-Template-Auswertungen.
- `src/ma_analyse/settings`: Naming-, Ausgabeformat- und Plot-Template-Konfiguration.
- `tests`: bestehende Pytest-Tests fuer CLI, Konfiguration, Variantenhelfer, Zeitfenster, Logging, GUI-Auswahl und Plot-Templates.
- `docs`: vorhandene Befehls-, Architektur-, Commit- und Planstatus-Dokumentation.
- `data/input`, `data/database`, `data/output`, `data/test_output`: Datenordner fuer Rohdaten, aufbereitete Nutzdaten, regulaere Ausgaben und Testausgaben.
- `logs`: Laufprotokolle der Analysebefehle.

### Vorhandene Daten und Artefakte

Im Projekt liegen bereits echte IDA-ICE-Daten:

- Rohdatenvarianten unter `data/input`, unter anderem `Dimensionierung` und mehrere Heizleistungsvarianten.
- IDA-ICE-Dateien wie `.prn`, `.idm`, `.idc` und `vers.summary`.
- Aufbereitete Nutzdaten unter `data/database/<Variante>_nutzdaten` als CSV und XLSX.
- Bestehende Analyseausgaben unter `data/output` und `data/test_output`, unter anderem PNG, PDF und XLSX.

Relevante vorhandene Konfiguration:

- `pyproject.toml` definiert Paket, CLI-Entrypoint, Ruff und Pytest.
- `requirements.txt` enthaelt aktuell nur Runtime-Abhaengigkeiten fuer Analyse und Plots.
- `src/ma_analyse/settings/plot_templates.toml` ist die vorhandene TOML-Konfiguration fuer Plot-Templates.

Nicht als Kernstruktur vorhanden:

- Keine eigenstaendige Katalogstruktur unter `config/parameters`, `config/options`, `config/systems` oder `config/naming`.
- Keine PostgreSQL-, SQLAlchemy- oder Alembic-Struktur.
- Keine Prisma-Struktur.
- Keine dedizierten JSON- oder YAML-Beispieldateien fuer Parameter und Optionen.

### Bestehende Analysepipeline

Die aktuelle Anwendung arbeitet im Wesentlichen so:

1. `prepare` liest Variantenordner aus `data/input`.
2. Pro Raum werden erwartete PRN-Dateien zusammengefuehrt.
3. Die Nutzdaten landen in `data/database/<Variante>_nutzdaten`.
4. `comfort`, `heating`, `cooling`, `analyze-data` und `plot-template` lesen diese Nutzdaten.
5. Ergebnisse werden nach `data/output` oder `data/test_output` geschrieben.

Diese Pipeline ist fuer Simulationsergebnis-Auswertung bereits tragfaehig und soll nicht geloescht oder ungeprueft umgebaut werden. Fuer Version 1 des neuen Systems wird sie als vorhandenes Analyse-Subsystem behandelt, das spaeter ueber Adapter angebunden wird.

## 2. Zielarchitektur

Der neue Variantenkern sollte getrennt vom bestehenden Analysecode aufgebaut werden. Vorgeschlagen wird ein neues Paket `ma_variants`, waehrend `ma_analyse` als Analyse-Subsystem erhalten bleibt.

Vorgeschlagene Paketstruktur:

```text
src/
  ma_analyse/
    ...
  ma_variants/
    __init__.py
    parameter_catalog/
    option_catalog/
    system_catalog/
    database/
    variant_manager/
    selection/
    naming/
    ida_export/
    simulation_results/
    analysis/
    economic_analysis/
    reporting/
```

Vorgesehene Modulverantwortung:

- `parameter_catalog`: Parameterdefinitionen, Datentypen, Einheiten, Standardwerte.
- `option_catalog`: Optionsgruppen und Optionswerte je Parameter oder Entscheidungsebene.
- `system_catalog`: Systemvorlagen und spaetere technische Systemkonfigurationen.
- `database`: SQLAlchemy-Modelle, Engine, Session, Alembic-Migrationen.
- `variant_manager`: Variantenanzahl, Kombinatorik, Variantenerzeugung und Variantenwerte.
- `selection`: manuelle und einfache regelbasierte Auswahl.
- `naming`: Namensregeln und stabile technische Variantenschluessel.
- `ida_export`: spaeterer Export Richtung IDA ICE, in V1 nur vorbereitet.
- `simulation_results`: spaetere Verwaltung von Simulationsergebnissen.
- `analysis`: spaetere Adapter zu `ma_analyse` und Bewertungsfunktionen.
- `economic_analysis`: spaeterer Wirtschaftlichkeitskern, in V1 nur vorbereitet.
- `reporting`: JSON-/Excel-Export und spaeter Berichte.

## 3. Mindestumfang Version 1

Version 1 soll enthalten:

- Grundstruktur fuer `ma_variants`.
- PostgreSQL-Zieldatenbank mit SQLAlchemy und Alembic vorbereiten.
- Datenmodelle fuer Parameter, Optionsgruppen, Optionswerte, Varianten und Variantenwerte.
- Import von Beispielparametern und Beispieloptionen aus bearbeitbaren Dateien.
- Eingabevalidierung fuer fehlende Keys, doppelte Keys und ungueltige Referenzen.
- Berechnung der theoretischen Variantenanzahl.
- Einfache Variantenerzeugung aus Optionsgruppen.
- Einfache manuelle oder regelbasierte Variantenauswahl.
- Einfache Namensgenerierung.
- Export einer Variantenuebersicht als JSON und optional Excel.
- Dokumentation von Workflow, Datenfluss, Datenmodell, Entscheidungen und offenen Fragen.

Version 1 soll noch nicht enthalten:

- Vollstaendiger Produktkatalog.
- Vollstaendiger Materialkatalog.
- Vollstaendige Wirtschaftlichkeitsanalyse.
- Vollstaendiger IDA-ICE-Export.
- Vollstaendige Weboberflaeche.
- Komplexe Optimierungsalgorithmen.
- Automatische Produktrecherche.

Diese Bereiche werden als Module vorbereitet, bleiben aber nicht Hauptaufgabe der ersten Umsetzung.

## 4. Konfiguration und Eingabedateien

Neue bearbeitbare Eingabestruktur:

```text
config/
  parameters/
  options/
  systems/
  naming/
data/
  imports/
  exports/
  reports/
```

Fuer Version 1 ist JSON als erste Importquelle sinnvoll, weil dafuer keine neue Parser-Abhaengigkeit erforderlich ist. YAML kann spaeter mit `PyYAML` ergaenzt werden, falls die manuelle Pflege dadurch angenehmer wird.

Beispielquellen:

- `config/parameters/example_parameters.json`
- `config/options/example_options.json`
- `config/systems/example_system_templates.json`
- `config/naming/example_naming_rules.json`

Excel- und Prisma-Importe werden nur als spaetere Importquellen vorgesehen.

## 5. Datenbankgrundmodell

PostgreSQL ist die Zieldatenbank. In Version 1 wird die Struktur mit SQLAlchemy und Alembic vorbereitet. Alle Tabellen erhalten stabile technische Schluessel. Frei geschriebene Anzeigenamen duerfen nicht als Verknuepfungsgrundlage dienen.

Vorgeschlagene Tabellen:

- `parameters`
  - `id`, `key`, `label`, `value_type`, `unit`, `default_value`, `description`, `is_active`
- `option_sets`
  - `id`, `key`, `label`, `parameter_id`, `description`, `is_active`
- `option_values`
  - `id`, `option_set_id`, `key`, `label`, `value`, `sort_order`, `metadata_json`, `is_active`
- `variants`
  - `id`, `key`, `name`, `source`, `status`, `created_at`, `metadata_json`
- `variant_values`
  - `id`, `variant_id`, `parameter_id`, `option_value_id`, `raw_value`, `unit`
- `system_templates`
  - `id`, `key`, `label`, `description`, `is_active`
- `system_template_values`
  - `id`, `system_template_id`, `parameter_id`, `option_value_id`, `raw_value`
- `naming_rules`
  - `id`, `key`, `scope`, `template`, `sort_order`, `is_active`
- `import_logs`
  - `id`, `source_type`, `source_path`, `status`, `message`, `imported_at`

Empfehlung fuer technische Keys:

- Primaerschluessel: Datenbank-ID, vorzugsweise UUID oder Integer mit eindeutiger technischer Spalte.
- Fachliche Referenz: eindeutiger `key`, z. B. `heating_capacity_factor`.
- Anzeigenamen: `label` oder `name`, nicht fuer Joins verwenden.

## 6. Workflow Version 1

1. Beispielparameter in `config/parameters` pflegen.
2. Beispieloptionen in `config/options` pflegen.
3. Importer liest die Dateien und validiert Keys und Referenzen.
4. Optional: Import in PostgreSQL protokollieren.
5. Variantenkern berechnet die theoretische Variantenanzahl.
6. Variantenkern erzeugt einfache Kombinationen.
7. Auswahlmodul reduziert die Menge manuell oder per einfacher Regel.
8. Naming-Modul generiert stabile Variantennamen und technische Keys.
9. Reporting-Modul exportiert eine Variantenuebersicht nach `data/exports`.
10. Spaeter: ausgewaehlte Varianten werden an IDA-ICE-Export oder `ma_analyse`-Adapter uebergeben.

## 7. Umsetzungsvorschlag

### Schritt 1: Dokumentation und Projektgrenzen

- `docs/PLAN.md` als Planungsbasis anlegen.
- Spaeter ergaenzen:
  - `docs/WORKFLOW.md`
  - `docs/DATA_MODEL.md`
  - `docs/DECISIONS.md`
- Aenderungen zentral im Root-`CHANGELOG.md` dokumentieren.
- Bestehendes `ma_analyse` als Analyse-Subsystem dokumentieren.

### Schritt 2: Paket- und Ordnergeruest

- `src/ma_variants` mit den Zielmodulen anlegen.
- `config/parameters`, `config/options`, `config/systems`, `config/naming` anlegen.
- `data/imports`, `data/exports`, `data/reports` anlegen.
- Keine bestehenden Analysepfade verschieben.

### Schritt 3: Datenmodelle und Datenbank

- Abhaengigkeiten in `pyproject.toml` vorbereiten:
  - `sqlalchemy`
  - `alembic`
  - `psycopg` oder `psycopg-binary` fuer lokale Entwicklung
- SQLAlchemy-Modelle fuer die Kerntabellen anlegen.
- Alembic-Struktur mit erster Migration vorbereiten.
- Datenbank-URL ueber Umgebungsvariable oder lokale Config lesen.

### Schritt 4: Import und Validierung

- JSON-Beispieldateien fuer Parameter und Optionen erstellen.
- Importer fuer Parameter und Optionen implementieren.
- Validierung:
  - Pflichtfelder vorhanden.
  - `key` eindeutig.
  - Optionswerte referenzieren existierende Optionsgruppen.
  - Optionsgruppen referenzieren existierende Parameter.

### Schritt 5: Variantenkern

- Theoretische Variantenanzahl als Produkt der Optionswertanzahlen berechnen.
- Einfache Variantengenerierung aus Optionsgruppen.
- Begrenzung der erzeugten Varianten fuer Tests und erste Anwendung ermoeglichen.
- Variantenwerte strukturiert ablegen.

### Schritt 6: Auswahl, Naming und Export

- Manuelle Auswahl ueber Liste von Variantenschluesseln.
- Einfache Regelwahl, z. B. Include/Exclude nach Parameter-Key und Optionswert-Key.
- Namensgenerierung ueber definierte Naming-Regeln.
- JSON-Export als Pflichtausgabe.
- Excel-Export optional, da `openpyxl` bereits vorhanden ist.

### Schritt 7: Tests

Neue fokussierte Tests:

- `tests/test_parameter_import.py`
- `tests/test_option_import.py`
- `tests/test_variant_counting.py`
- `tests/test_variant_naming.py`

Die bestehende Pytest-Struktur kann ohne Umbau weiterverwendet werden.

## 8. Spaetere Ausbaustufen

- Produktkatalog mit Hersteller-, Produkt- und Leistungsdaten.
- Materialkatalog mit bauphysikalischen Eigenschaften.
- Wirtschaftlichkeitsanalyse mit Investitions-, Betriebs- und Energiekosten.
- IDA-ICE-Export mit konkreter Modell-/Parameteruebergabe.
- Weboberflaeche fuer Katalogpflege, Variantenauswahl und Ergebnisuebersicht.
- Simulationsergebnis-Import und Adapter zu `ma_analyse`.
- Optimierung und Priorisierung nach Komfort, Energie, Kosten und Robustheit.

## 9. Offene Fragen

- Soll das neue Paket `ma_variants` heissen, oder soll alles unter `ma_analyse` bleiben?
- Soll Version 1 zuerst rein dateibasiert arbeiten oder direkt PostgreSQL schreiben?
- Soll JSON als erste Importquelle reichen, oder ist YAML fuer die Pflege wichtiger?
- Welche Parametergruppen sind fuer die ersten Beispielvarianten fachlich am wichtigsten?
- Wie soll ein stabiler Variantenname aussehen: kurz, technisch, lesbar oder kombiniert?
- Welche Auswahlregel ist fuer den ersten realen Anwendungsfall sinnvoll?
- Soll der erste Export nur JSON sein, oder sofort auch Excel?
- Wann soll der bestehende Analyseworkflow `ma_analyse` angebunden werden?

## 10. Naechster sinnvoller Schritt

Nach Freigabe dieses Plans sollte zuerst das Dokumentations- und Paketgeruest angelegt werden. Danach folgen Beispielkonfigurationen, Importvalidierung und die ersten vier Tests fuer Parameterimport, Optionsimport, Variantenanzahl und Namensgenerierung.
