# ma_weather

Modulbereich fuer Wetterdatenanalyse und TRY-Integration.

## Zweck

Reale TRY-Wetterdaten katalogisieren, importieren, validieren, analysieren und
fuer nachfolgende Module referenzierbar machen.

## Eingaben

- lokale reale TRY-Dateien
- Wetterkatalog und `weather_key`
- optionale lokale Gemeinde- und PLZ-Geodaten fuer ortsgenaue
  Standortpruefung

## Ausgaben

- validierte Wetterdaten, Kennwerte, Diagramme, CSV und Bericht
- dokumentierter `weather_key` fuer die spaetere Uebergabe an `ma_parameters`
- Quellenmetadaten, strukturierte Diagnosen, Freigabestatus und lokaler
  Sitzungsnachweis

## Abgrenzung

- keine synthetischen TRY-Daten
- keine direkte fachliche Kopplung an `ma_variants`

## Abhaengigkeiten

- lokale TRY-Dateien unter `data/ma_weather/input/`
- P008-Gesamtplan fuer Abschlusspruefung, Standort-/Referenzlogik,
  Dateiimport, Freigabe und P007-Anbindung
- optionale Geodaten-Metadaten unter `config/ma_weather/geodata/`

## Status

Teilweise aktiv. Ein realer Jahresdatensatz ist geprueft; fuenf Realtests und
die Diagrammabstimmung fehlen noch.

## Naechster Schritt

P008 mit der vereinfachten `Pruefen`-Ansicht, der ortsgenauen
EPSG:3034-/Gemeinde-Standorterkennung, optionaler PLZ-Aufloesung und der
kontrollierten Uebergabe an `ma_parameters` fortsetzen.

Der erste P002-Struktur-Slice hat das Paket `src/ma_weather/` und einen
einfachen Wetterkatalog angelegt. Der aktuelle Stand enthaelt zusaetzlich eine
erste lokale TRY-Analyse mit Import, Validierung, Kennwerten, Diagrammen,
Markdown-Bericht und Runner.

P010 ergaenzt jeden TRY-Import um Quellen-ID, Dateimetadaten und SHA-256.
Import- und Validierungsmeldungen besitzen stabile Codes, eindeutige IDs und
Fundstellen. Fehler blockieren; Warnungen koennen in Streamlit bewusst
blockiert oder fuer den konkreten Lauf freigegeben werden. Der Nachweis liegt
unter `logs/sessions/<session_id>.jsonl`.

Reale TRY-Dateien werden vom Nutzer lokal unter `data/ma_weather/input/`
bereitgestellt und nicht im Git-Repo versioniert.

Slice 5 ergaenzt den lokalen Import in der Streamlit-Wetterseite. Der
Importbutton liegt unten im Bereich `Wetterdatensaetze`, vor der Tabelle der
aktiven Datensaetze. Eigene entpackte TRY-`.dat`-Dateien werden unter
`data/ma_weather/input/custom/<weather_key>/` kopiert und in einem lokalen,
nicht versionierten Katalog unter
`data/ma_weather/config/datasets/weather_datasets_local.yaml` registriert.

Zusaetzlich fuehrt die Wetterseite die Schritte `Import`, `Scannen` und
`Pruefen`. Importierte TRY-Dateien werden zunaechst nur lokal abgelegt.
Der Scan nutzt die versionierte Zuordnung von TRY-Ordnerkennung zu Standort
unter `config/ma_weather/try_locations/example_try_file_locations.yaml`.
Gefundene Dateien werden zuerst als Datensatzentwuerfe angezeigt und erst nach
Pruefung sowie Nutzeraktion in den lokalen Katalog uebernommen.

Fuer ortsgenaue TRY-Dateien liest `ma_weather` Rechtswert und Hochwert aus dem
TRY-Kopf. Die vorbereitete Standortaufloesung interpretiert diese Werte als
EPSG:3034 und kann sie mit lokalen GeoJSON-Gemeinde- und PLZ-Geodaten
abgleichen. Die Geodaten sind lokal und unversioniert; nur ihre Metadaten
werden versioniert.

Der aktive Beispielkatalog enthaelt Datensaetze fuer Frankfurt am Main,
Muenchen und Hamburg jeweils fuer 2015 und 2045 als Jahr-, Sommer- und
Winterdatensatz.

Der Standortkatalog unter `config/ma_weather/locations/` bildet Staedte,
Klimaregionen und TRY-Referenzstandorte ab. Die Streamlit-Wetterseite nutzt ihn
fuer die automatische Anzeige von Klimaregion und Referenzstandort.

Die reduzierte P008-Umsetzung fuehrt Datensatzstatus, `import_id`,
offene Wetterdatensaetze, bewusste Aktivierung und einen lokalen
Projekt-Default ein. Aktivierung und Default werden nicht automatisch aus einem
Import abgeleitet.

Slice 4 ergaenzt kritische Wetterereignisse je bewusst ausgewaehltem
Datensatz. Jahr-, Sommer- und Winterdateien werden nicht vermischt.

## Dateien

- `commands_weather.md`: Befehle und Pruefungen fuer das Wettermodul.
- `workflow.md`: geplanter Ablauf von Wetterkatalog bis spaeterem Bericht.
- `data_model.md`: Datenmodell des Wetterkatalogs.
- `try_locations.md`: Zuordnung lokaler TRY-Kennungen zu Standorten.

## Start

```powershell
.\.venv\Scripts\python.exe -m ma_weather.run_weather_analysis --weather-key TRY_FFM_2015_JAHR
```

Der Befehl erwartet, dass die lokale TRY-Datei aus dem Katalogpfad vorhanden
ist. Reale TRY-Dateien werden nicht versioniert.

Weitere aktive `weather_key` Werte stehen in `commands_weather.md`. Der aktive
Plan liegt unter
`docs/project/plans/inbox/260623_Plan_P008_ma_weather_Gesamtplan.md`.
