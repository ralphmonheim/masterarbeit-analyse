# ma_weather Befehle

Das Wettermodul besitzt einen Wetterkatalog und eine erste lokale
TRY-Analysepipeline fuer Import, Validierung, Kennwerte, Diagramme und
Markdown-Bericht.

## Aktueller Status

- Das Paket `src/ma_weather/` ist vorbereitet.
- Der Wetterkatalog liegt unter `config/ma_weather/datasets/example_weather_datasets.yaml`.
- Aktuell sind 18 Datensaetze aktiv: Frankfurt am Main, Muenchen und Hamburg
  jeweils fuer 2015 und 2045 als Jahr-, Sommer- und Winterdatensatz.
- Echte TRY-Dateien liegen lokal unter `data/ma_weather/input/` und werden nicht versioniert.
- Aufbereitete Wetterdaten sind spaeter fuer `data/ma_weather/database/` vorgesehen.
- Wetterdiagramme sind spaeter fuer `data/ma_weather/output/` vorgesehen.
- Der Runner kann als Modul gestartet werden.
- Der aktive Plan liegt unter `docs/project/plans/inbox/260623_Plan_P008_ma_weather_Gesamtplan.md`.
- Ein YAML-Standortkatalog liegt unter `config/ma_weather/locations/example_weather_locations.yaml`.
- Die Streamlit-Wetterseite zeigt Stadt, Klimaregion, TRY-Referenzstandort und
  sortierte Wetterdatensaetze.
- Die Wetterseite bietet fuer `plot-template-weather` die Auswahl `all` oder
  eines einzelnen vorhandenen Wetterdiagramms.
- Unten im Bereich `Wetterdatensaetze` koennen entpackte TRY-`.dat`-Dateien
  lokal importiert werden. Lokale Importdaten liegen unter
  `data/ma_weather/input/custom/`; der lokale Katalog liegt unter
  `data/ma_weather/config/datasets/weather_datasets_local.yaml`.
- Lokal manuell unter `data/ma_weather/input/` abgelegte TRY-Dateien koennen
  ueber `Lokale TRY-Dateien scannen` als Datensatzentwuerfe erkannt werden.
  Die Standortzuordnung erfolgt ueber
  `config/ma_weather/try_locations/example_try_file_locations.yaml`.
- Die neue ortsgenaue Standortpruefung nutzt vorbereitete
  Geodaten-Metadaten unter
  `config/ma_weather/geodata/example_weather_geodata_sources.yaml`.
  Lokale GeoJSON-Geodaten liegen unter `data/ma_weather/geodata/` und werden
  nicht versioniert.

## Sammelbefehle

### Wetteranalyse starten

Der Runner fuehrt Import, Validierung, Kennwerte, Diagramme und Bericht fuer
einen `weather_key` aus.

```powershell
.\.venv\Scripts\python.exe -m ma_weather.run_weather_analysis --weather-key TRY_FFM_2015_JAHR
```

Weitere aktive Jahresdatensaetze:

```powershell
.\.venv\Scripts\python.exe -m ma_weather.run_weather_analysis --weather-key TRY_FFM_2045_JAHR
.\.venv\Scripts\python.exe -m ma_weather.run_weather_analysis --weather-key TRY_MUC_2015_JAHR
.\.venv\Scripts\python.exe -m ma_weather.run_weather_analysis --weather-key TRY_MUC_2045_JAHR
.\.venv\Scripts\python.exe -m ma_weather.run_weather_analysis --weather-key TRY_HAM_2015_JAHR
.\.venv\Scripts\python.exe -m ma_weather.run_weather_analysis --weather-key TRY_HAM_2045_JAHR
```

Beispiele fuer Sommer- und Winterdatensaetze:

```powershell
.\.venv\Scripts\python.exe -m ma_weather.run_weather_analysis --weather-key TRY_FFM_2015_SOMM
.\.venv\Scripts\python.exe -m ma_weather.run_weather_analysis --weather-key TRY_FFM_2015_WINT
.\.venv\Scripts\python.exe -m ma_weather.run_weather_analysis --weather-key TRY_MUC_2045_SOMM
.\.venv\Scripts\python.exe -m ma_weather.run_weather_analysis --weather-key TRY_HAM_2045_WINT
```

Der Befehl fuehrt folgende Schritte aus:

- TRY-Datei aus dem Wetterkatalog laden
- Wetterdaten validieren
- Wetterkennwerte berechnen
- aufbereitete CSV unter `data/ma_weather/database/` schreiben
- Diagramme unter `data/ma_weather/output/` erzeugen
- Markdown-Bericht unter `data/ma_weather/reports/` schreiben
- kritische Wetterereignisse fuer den ausgewaehlten Datensatz erkennen

Die gleiche Pipeline kann auch in `ma_ui` ueber die Seite `Wetterdaten`
gestartet werden. Dort wird ein aktiver `weather_key` ausgewaehlt und die
erzeugten Diagramme werden direkt angezeigt.

Im Bereich `Wetterdatensaetze` stehen die drei Schritte `Import`, `Scannen`
und `Pruefen`. `Import` enthaelt den Link zur DWD-TRY-Seite und legt
entpackte `.dat`-Dateien nur lokal unter `data/ma_weather/input/TRY_*` ab.
`Scannen` erzeugt daraus Entwuerfe fuer noch nicht katalogisierte TRY-Dateien.
`Pruefen` erlaubt die fachliche Anpassung dieser Entwuerfe und die bewusste
Registrierung im lokalen Katalog. Kein Schritt setzt Aktivierung oder
Projekt-Default automatisch.

Die Wetterseite zeigt zusaetzlich Quellenmetadaten, Diagnose-IDs und
Fundstellen. Bei Warnungen muss der Lauf bewusst mit `Nicht freigeben` oder
`Warnungen bestaetigen und freigeben` entschieden werden. Die Entscheidung
gilt nur fuer den aktuellen Lauf und wird lokal unter
`logs/sessions/<session_id>.jsonl` protokolliert.

Jeder Analyseimport erhaelt eine `import_id`. Freigegebene Datensaetze koennen
in Streamlit bewusst aktiviert und danach als Projekt-Default gesetzt werden.
Der lokale Auswahlstatus liegt unter
`data/ma_weather/database/weather_selection_state.yaml` und wird nicht
versioniert.

Der Schritt `Pruefen` zeigt `Gefundene lokale TRY-Dateien` und
`Parameter pruefen`. Katalogisierte Bestandspruefungen bleiben technisch
erhalten, sind aber nicht Teil dieser Entwurfspruefung. In `Parameter pruefen`
werden nur Stadt, Bezugsjahr, Datensatztyp und Szenario angezeigt. Rolle,
`weather_key` und Anzeigename werden daraus generiert.

Nach einer Analyse zeigt der Bereich `Kritische Wetterereignisse` Ereignisse
wie heissester Tag, kaeltester Tag, heisseste und kaelteste Drei-Tage-Periode,
strahlungsreichster Tag und windstaerkster Tag. Die Berechnung nutzt nur den
bewusst ausgewaehlten Datensatz, also Jahr, Sommer oder Winter.

## Einzelbefehle

### Wetter-Template-Diagramm erzeugen

Der installierte CLI-Einstieg erzeugt alle Wetterdiagramme oder ein einzelnes
Diagramm aus dem vorhandenen Wetterdiagramm-Katalog.

```powershell
.\.venv\Scripts\plot-template-weather.exe all --weather-key TRY_FFM_2015_JAHR
.\.venv\Scripts\plot-template-weather.exe temperature_year --weather-key TRY_FFM_2015_JAHR
.\.venv\Scripts\plot-template-weather.exe wind_rose --weather-key TRY_FFM_2015_JAHR
```

Vorhandene Diagramm-Schluessel:

- `temperature_year`
- `temperature_heatmap`
- `monthly_radiation`
- `monthly_degree_hours`
- `wind_rose`
- `temperature_humidity_scatter`

### Aktuelle Pruefung

Katalog- und Strukturtests fuer den aktuellen Stand:

```powershell
.\.venv\Scripts\python.exe -m pytest tests -k ma_weather
.\.venv\Scripts\python.exe -m pytest tests -k weather
.\.venv\Scripts\python.exe -m ruff check src tests --no-cache
```

## Referenz und Hinweise

- Das uebergreifende Befehls- und Ausgabeninventar steht unter
  `docs/project/COMMAND_OUTPUT_INVENTORY.md`.
- Der Katalog darf auf lokale TRY-Dateien verweisen, die nicht im Repo liegen.
- `weather_key` bleibt der bestehende technische Schluessel. Die spaetere
  Uebergabe erfolgt kontrolliert ueber `ma_parameters`.
- Jahresdatensaetze tragen im `weather_key` die Endung `_JAHR`, damit sie
  eindeutig neben `_SOMM` und `_WINT` stehen.
- Wetterdaten bleiben fachlich von `ma_analyse`-Zonenwerten getrennt.
- Bestehende Analyse-Textlogs unter `logs/*.log` bleiben unveraendert.
