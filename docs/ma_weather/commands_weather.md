# ma_weather Befehle

Das Wettermodul besitzt einen Wetterkatalog und eine erste lokale
TRY-Analysepipeline fuer Import, Validierung, Kennwerte, Diagramme und
Markdown-Bericht.

## Aktueller Status

- Das Paket `src/ma_weather/` ist vorbereitet.
- Der Wetterkatalog liegt unter `config/ma_weather/datasets/example_weather_datasets.yaml`.
- Aktuell sind sechs Jahresdatensaetze aktiv: Frankfurt am Main, Muenchen und Hamburg jeweils fuer 2015 und 2045.
- Echte TRY-Dateien liegen lokal unter `data/ma_weather/input/` und werden nicht versioniert.
- Aufbereitete Wetterdaten sind spaeter fuer `data/ma_weather/database/` vorgesehen.
- Wetterdiagramme sind spaeter fuer `data/ma_weather/output/` vorgesehen.
- Der Runner kann als Modul gestartet werden.
- Der Plan liegt unter `docs/project/plans/inbox/250603_Plan_Wetterdatenanalyse_TRY_Integration.md`.

## Sammelbefehle

### Wetteranalyse starten

Der Runner fuehrt Import, Validierung, Kennwerte, Diagramme und Bericht fuer
einen `weather_key` aus.

```powershell
.\.venv\Scripts\python.exe -m ma_weather.run_weather_analysis --weather-key TRY_FFM_2015
```

Weitere aktive Jahresdatensaetze:

```powershell
.\.venv\Scripts\python.exe -m ma_weather.run_weather_analysis --weather-key TRY_FFM_2045
.\.venv\Scripts\python.exe -m ma_weather.run_weather_analysis --weather-key TRY_MUC_2015
.\.venv\Scripts\python.exe -m ma_weather.run_weather_analysis --weather-key TRY_MUC_2045
.\.venv\Scripts\python.exe -m ma_weather.run_weather_analysis --weather-key TRY_HAM_2015
.\.venv\Scripts\python.exe -m ma_weather.run_weather_analysis --weather-key TRY_HAM_2045
```

Der Befehl fuehrt folgende Schritte aus:

- TRY-Datei aus dem Wetterkatalog laden
- Wetterdaten validieren
- Wetterkennwerte berechnen
- aufbereitete CSV unter `data/ma_weather/database/` schreiben
- Diagramme unter `data/ma_weather/output/` erzeugen
- Markdown-Bericht unter `data/ma_weather/reports/` schreiben

## Einzelbefehle

### Aktuelle Pruefung

Katalog- und Strukturtests fuer den aktuellen Stand:

```powershell
.\.venv\Scripts\python.exe -m pytest tests -k ma_weather
.\.venv\Scripts\python.exe -m ruff check src tests --no-cache
```

## Referenz und Hinweise

- Der Katalog darf auf lokale TRY-Dateien verweisen, die nicht im Repo liegen.
- `weather_key` ist die spaetere Verbindung zum Variantenmodul.
- Wetterdaten bleiben fachlich von `ma_analyse`-Zonenwerten getrennt.
