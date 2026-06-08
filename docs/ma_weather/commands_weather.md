# ma_weather Befehle

Das Wettermodul besitzt aktuell einen importierbaren Paket-Skeleton und einen
einfachen Wetterkatalog. Die vollstaendige TRY-Analyse folgt spaeter.

## Aktueller Status

- Das Paket `src/ma_weather/` ist vorbereitet.
- Der Wetterkatalog liegt unter `config/ma_weather/datasets/example_weather_datasets.yaml`.
- Echte TRY-Dateien liegen lokal unter `data/ma_weather/input/` und werden nicht versioniert.
- Aufbereitete Wetterdaten sind spaeter fuer `data/ma_weather/database/` vorgesehen.
- Wetterdiagramme sind spaeter fuer `data/ma_weather/output/` vorgesehen.
- Es gibt noch keinen CLI-Befehl fuer TRY-Import oder Wetterauswertung.
- Der Plan liegt unter `docs/project/plans/inbox/250603_Plan_Wetterdatenanalyse_TRY_Integration.md`.

## Aktuelle Pruefung

Katalog- und Strukturtests fuer den aktuellen Stand:

```powershell
.\.venv\Scripts\python.exe -m pytest tests -k ma_weather
.\.venv\Scripts\python.exe -m ruff check src tests --no-cache
```

## Geplante Befehle

Nach Umsetzung von P002 koennen hier Befehle fuer folgende Schritte ergaenzt werden:

- TRY-Datei importieren
- Wetterdatensatz validieren
- Wetterkennwerte berechnen
- Wetterdiagramme erzeugen
- Wetterbericht exportieren

## Hinweise

- Der Katalog darf auf lokale TRY-Dateien verweisen, die nicht im Repo liegen.
- `weather_key` ist die spaetere Verbindung zum Variantenmodul.
- Wetterdaten bleiben fachlich von `ma_analyse`-Zonenwerten getrennt.
