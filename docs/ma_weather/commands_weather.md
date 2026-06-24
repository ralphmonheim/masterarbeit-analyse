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

Die Schaltflaeche `Bestand und Validierung pruefen` prueft alle katalogisierten
Wetterdatensaetze gegen lokale TRY-Dateien und zeigt fehlende, fehlerhafte oder
noch freizugebende Datensaetze im Bereich `Offene Wetterdatensaetze`.

Nach einer Analyse zeigt der Bereich `Kritische Wetterereignisse` Ereignisse
wie heissester Tag, kaeltester Tag, heisseste und kaelteste Drei-Tage-Periode,
strahlungsreichster Tag und windstaerkster Tag. Die Berechnung nutzt nur den
bewusst ausgewaehlten Datensatz, also Jahr, Sommer oder Winter.

## Einzelbefehle

### Aktuelle Pruefung

Katalog- und Strukturtests fuer den aktuellen Stand:

```powershell
.\.venv\Scripts\python.exe -m pytest tests -k ma_weather
.\.venv\Scripts\python.exe -m pytest tests -k weather
.\.venv\Scripts\python.exe -m ruff check src tests --no-cache
```

## Referenz und Hinweise

- Der Katalog darf auf lokale TRY-Dateien verweisen, die nicht im Repo liegen.
- `weather_key` bleibt der bestehende technische Schluessel. Die spaetere
  Uebergabe erfolgt kontrolliert ueber `ma_parameters`.
- Jahresdatensaetze tragen im `weather_key` die Endung `_JAHR`, damit sie
  eindeutig neben `_SOMM` und `_WINT` stehen.
- Wetterdaten bleiben fachlich von `ma_analyse`-Zonenwerten getrennt.
- Bestehende Analyse-Textlogs unter `logs/*.log` bleiben unveraendert.
