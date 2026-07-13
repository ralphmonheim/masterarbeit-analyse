# ma_weather Datenmodell

## WeatherDataset

Der erste P002-Slice fuehrt einen einfachen Wetterkatalog ein. Ein Datensatz
wird als `WeatherDataset` in `src/ma_weather/weather_catalog.py` modelliert.

Felder:

| Feld | Zweck |
|---|---|
| `weather_key` | technischer Schluessel fuer spaetere Variantenverknuepfung |
| `display_name` | lesbarer Name |
| `file_path` | lokaler Pfad zur TRY-Datei |
| `file_format` | Format, aktuell z. B. `TRY` |
| `source` | Quelle, z. B. DWD TRY |
| `location` | Ort oder Klimaregion |
| `year_type` | z. B. Referenzjahr, Sommer, Winter |
| `climate_scenario` | Klimaszenario oder Zeitraum |
| `dataset_role` | optionale Rolle, z. B. `try_reference` oder `site_specific` |
| `location_id` | optionale Stadt-ID fuer standortgenaue Datensaetze |
| `reference_location_id` | optionale Referenzstandort-ID fuer TRY-Referenzdatensaetze |
| `selection_priority` | Sortierung innerhalb gleicher Rolle |
| `is_active` | steuert, ob der Datensatz aktiv verwendet werden soll |
| `notes` | kurze Hinweise |
| `location_resolution_source` | Herkunft der Standortzuordnung, z. B. Datei-/Mapping-Verweis, TRY-Koordinaten oder manuelle Pruefung |
| `location_resolution_status` | Status der Standortzuordnung, z. B. bestaetigt, Vorschlag, fehlend, Konflikt |

`is_active` beschreibt die Katalogsicht und steuert, ob ein freigegebener
Datensatz regulaer in der Wetterauswahl erscheinen darf. Neue lokale
Registrierungen aus dem Pruefworkflow werden nach erfolgreicher technischer
Pruefung und bewusster Uebernahme direkt mit `is_active: true` geschrieben.
Der Projekt-Default bleibt davon getrennt und muss weiterhin bewusst gesetzt
werden.

Aktive `year_type` Werte fuer den P008-Wetterkatalog:

| Wert | Bedeutung |
|---|---|
| `reference_year` | Jahresdatensatz fuer Gegenwart |
| `future_year` | Jahresdatensatz fuer Zukunftsszenario |
| `summer_extreme` | Sommer-TRY-Datei als eigener Datensatz |
| `winter_extreme` | Winter-TRY-Datei als eigener Datensatz |

Die automatische Dateierkennung kennt fuer DWD-TRY-2011-Altdateien zusaetzlich
die Szenarien `present_2010` und `future_2035`. Fuer den regulaeren
DWD-TRY-2015/2045-Datenbestand bleiben `present` und `future_2045` die
Standardwerte.

## Standort- und Referenzkatalog

Der P008-Slice fuer Standortlogik fuehrt einen YAML-basierten
Zwischenkatalog ein:

```text
config/ma_weather/locations/example_weather_locations.yaml
```

Der Katalog enthaelt:

- `weather_regions`: TRY-Klimaregionen 1 bis 15 mit Referenzstandort
- `weather_locations`: Staedte, Legacy-Codes, Klimaregion und
  Referenzstandort

Die Fachlogik liegt in `src/ma_weather/weather_locations.py`.

Der Ablauf ist bewusst noch keine Datenbankmigration. Die YAML-Struktur dient
als Seed- und Abstimmungsgrundlage fuer die spaetere Datenbank.

## Datensatzrollen

Wetterdatensaetze koennen optional eine fachliche Rolle erhalten:

| Rolle | Bedeutung |
|---|---|
| `try_reference` | TRY-Referenzdatensatz fuer einen Referenzstandort; wird in der Auswahl zuerst empfohlen |
| `site_specific` | standortgenauer Datensatz fuer eine konkrete Stadt |

Der TRY-Referenzdatensatz und standortgenaue Datensaetze werden nicht
stillschweigend gleichgesetzt. Wenn fuer einen Referenzstandort kein
TRY-Referenzdatensatz katalogisiert ist, wird kein anderer Datensatz als
Referenzdatensatz ausgegeben.

## Katalogdatei

Der Beispielkatalog liegt unter:

```text
config/ma_weather/datasets/example_weather_datasets.yaml
```

Der Katalog referenziert lokale Dateien unter `data/ma_weather/input/`. Diese
Dateien werden nicht im Git-Repo versioniert.

Lokale UI-Imports werden nicht in die versionierte Vorlage geschrieben. Sie
liegen in einem eigenen Arbeitskatalog:

```text
data/ma_weather/config/datasets/weather_datasets_local.yaml
```

Beim Laden des Standardkatalogs werden Beispielkatalog und vorhandener lokaler
Importkatalog zusammengefuehrt. Doppelte `weather_key` Werte werden dabei
abgelehnt.

Manuell abgelegte TRY-Dateien koennen zunaechst als Datensatzentwuerfe erkannt
werden. Die TRY-Ordnerkennung-zu-Standort-Zuordnung dafuer liegt versioniert
unter:

```text
config/ma_weather/try_locations/example_try_file_locations.yaml
```

Vollstaendige Entwuerfe werden erst nach Nutzeraktion in den lokalen Katalog
geschrieben. Unvollstaendige Entwuerfe bleiben offen und werden nicht regulaer
auswaehlbar.

Die TRY-Ordnerzuordnung bildet lokale DWD-Dateiordner auf fachliche
Klimakartenpunkte ab. Die aus BKG VG250 erkannte Gemeinde bleibt als technische
Metadaten erhalten, kann aber vom Klimakartenpunkt abweichen. Beispiele:

| VG250-Gemeinde | Fachlicher Klimakartenpunkt |
|---|---|
| Geislingen an der Steige | Stoetten |
| Oberwiesenthal | Fichtelberg |
| Bad Marienberg (Westerwald) | Bad Marienberg |

Klimaregion 13 fuehrt `Passau` als TRY-Referenzpunkt. `Muehldorf` bleibt
Standort der Klimaregion, ist aber kein Referenzpunkt.

## Datenordner

| Ordner | Zweck |
|---|---|
| `data/ma_weather/input/` | lokale TRY-Eingabedateien |
| `data/ma_weather/input/custom/` | ueber Streamlit importierte TRY-Dateien |
| `data/ma_weather/input/TRY_01_Bremerhaven/` | Beispiel fuer konvertierte DWD-TRY-2011-PRN-Dateien mit lesbarem Stadtordner |
| `data/ma_weather/config/datasets/` | lokaler, nicht versionierter Importkatalog |
| `data/ma_weather/database/` | lokaler Auswahlstatus und spaetere Datenbankartefakte |
| `data/ma_weather/output/<weather_key>/<run_id>/data/` | aufbereitete Wetterdaten je Lauf |
| `data/ma_weather/output/<weather_key>/<run_id>/plots/` | Wetterdiagramme je Lauf |
| `data/ma_weather/output/<weather_key>/<run_id>/reports/` | Markdown-Wetterberichte je Lauf |
| `data/ma_weather/output/<weather_key>/<run_id>/weather_run_manifest.json` | Run-Manifest je Wetterlauf |
| `data/ma_weather/exports/` | spaetere strukturierte Exporte |

## Validierung

Der aktuelle Katalogimport prueft:

- fehlende Pflichtfelder
- leere technische Schluessel
- doppelte `weather_key` Werte
- boolesches Feld `is_active`
- optionale Datensatzrolle und zugehoerige Standort-IDs

Die Datei selbst muss im Struktur-Slice nicht existieren. Ein spaeterer
Integrationstest kann echte TRY-Dateien bewusst voraussetzen.

## Analyse-Ergebnisse

Die Wetteranalyse nutzt zusaetzliche strukturierte Rueckgaben:

| Modell | Zweck |
|---|---|
| `TryImportResult` | eingelesener DataFrame, Quelle, Spalten, Warnungen |
| `WeatherValidationReport` | Status, Warnungen, Fehler, Zeilenanzahl, fehlende Werte |
| `WeatherMetrics` | abgeleitete Wetterkennwerte |
| `WeatherPlotResult` | Status und Pfad je Diagramm |
| `WeatherOutputPaths` | gebuendelte Run-Pfade fuer CSV, Plots, Bericht und Manifest |
| `WeatherAnalysisResult` | Gesamtergebnis des Runners |
| `WeatherEvent` | Kritisches Wetterereignis aus einem ausgewaehlten Datensatz |

Jeder Analyseimport besitzt zusaetzlich eine stabile `import_id`. Sie verbindet
Wetterdatensatz, Quelle, Validierung, `session_id`, `run_id`, Logpfad und
Ausgabepfade. Das Run-Manifest wird unter
`data/ma_weather/output/<weather_key>/<run_id>/weather_run_manifest.json`
geschrieben.

## Lokaler Auswahlstatus

Bis zur spaeteren Datenbankmigration wird Aktivierung und Projekt-Default lokal
als YAML gespeichert:

```text
data/ma_weather/database/weather_selection_state.yaml
```

Der Status enthaelt bewusst aktivierte `weather_key` Werte, die zugehoerige
`import_id` und optional den aktuellen Projekt-Default. Nur freigegebene
Datensaetze duerfen aktiviert werden. Nur aktivierte Datensaetze duerfen
Projekt-Default werden.

Abgeleitete Kennwerte wie Stunden ueber 25/30 Grad C, Heizgradstunden und
Kuehlgradstunden stehen nicht direkt in der TRY-Datei. Sie werden aus der
Aussentemperatur berechnet und als Klimakennwerte dokumentiert.

Kritische Ereignisse werden aus dem analysierten DataFrame abgeleitet. Sie
enthalten Ereignis-ID, Typ, `weather_key`, Start, Ende, Kennwert, Einheit und
Begruendung. Jahr-, Sommer- und Winterdatensaetze bleiben dabei getrennt.
