# ma_weather

Modulbereich fuer Wetterdatenanalyse und TRY-Integration.

Der erste P002-Struktur-Slice hat das Paket `src/ma_weather/` und einen
einfachen Wetterkatalog angelegt. Der aktuelle Stand enthaelt zusaetzlich eine
erste lokale TRY-Analyse mit Import, Validierung, Kennwerten, Diagrammen,
Markdown-Bericht und Runner.

Reale TRY-Dateien werden vom Nutzer lokal unter `data/ma_weather/input/`
bereitgestellt und nicht im Git-Repo versioniert.

Der aktive Beispielkatalog enthaelt Jahresdatensaetze fuer Frankfurt am Main,
Muenchen und Hamburg jeweils fuer 2015 und 2045.

## Dateien

- `commands_weather.md`: Befehle und Pruefungen fuer das Wettermodul.
- `workflow.md`: geplanter Ablauf von Wetterkatalog bis spaeterem Bericht.
- `data_model.md`: Datenmodell des Wetterkatalogs.
- `try_locations.md`: Zuordnung lokaler TRY-Kennungen zu Standorten.

## Start

```powershell
.\.venv\Scripts\python.exe -m ma_weather.run_weather_analysis --weather-key TRY_FFM_2015
```

Der Befehl erwartet, dass die lokale TRY-Datei aus dem Katalogpfad vorhanden
ist. Reale TRY-Dateien werden nicht versioniert.

Weitere aktive `weather_key` Werte stehen in `commands_weather.md`.
