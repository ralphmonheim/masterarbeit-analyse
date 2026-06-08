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
| `is_active` | steuert, ob der Datensatz aktiv verwendet werden soll |
| `notes` | kurze Hinweise |

## Katalogdatei

Der Beispielkatalog liegt unter:

```text
config/ma_weather/datasets/example_weather_datasets.yaml
```

Der Katalog referenziert lokale Dateien unter `data/ma_weather/input/`. Diese
Dateien werden nicht im Git-Repo versioniert.

## Datenordner

| Ordner | Zweck |
|---|---|
| `data/ma_weather/input/` | lokale TRY-Eingabedateien |
| `data/ma_weather/database/` | spaeter aufbereitete Wetterdaten |
| `data/ma_weather/output/` | spaeter erzeugte Wetterdiagramme |
| `data/ma_weather/reports/` | spaetere Markdown-Berichte |
| `data/ma_weather/exports/` | spaetere strukturierte Exporte |

## Validierung

Der aktuelle Katalogimport prueft:

- fehlende Pflichtfelder
- leere technische Schluessel
- doppelte `weather_key` Werte
- boolesches Feld `is_active`

Die Datei selbst muss im Struktur-Slice nicht existieren. Ein spaeterer
Integrationstest kann echte TRY-Dateien bewusst voraussetzen.
