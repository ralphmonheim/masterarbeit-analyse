# ma_weather Workflow

## Ziel

`ma_weather` bereitet die getrennte Analyse von TRY-Wetterdaten vor. Wetterdaten
sind Eingangs- und Randbedingungsdaten. Sie werden nicht mit den
IDA-ICE-Zonenwerten aus `ma_analyse` vermischt.

## P002 Stand

Der aktuelle Stand umfasst:

- importierbares Paket `src/ma_weather/`
- Wetterkatalog unter `config/ma_weather/datasets/`
- lokale Eingabeordner unter `data/ma_weather/`
- Tests fuer Katalogstruktur und Pflichtfelder
- TRY-Datei einlesen
- Plausibilitaetspruefung
- Wetterkennwerte berechnen
- Wetterdiagramme erzeugen
- Markdown-Wetterbericht schreiben
- Runner fuer die lokale Wetteranalyse

## Geplanter Ablauf

1. TRY-Dateien lokal unter `data/ma_weather/input/` ablegen.
2. Datensatz in `config/ma_weather/datasets/example_weather_datasets.yaml` registrieren.
3. Datensatz ueber `weather_key` aus dem Katalog auswaehlen.
4. TRY-Datei importieren und validieren.
5. Wetterkennwerte berechnen.
6. Aufbereitete Wetterdaten unter `data/ma_weather/database/` schreiben.
7. Diagramme unter `data/ma_weather/output/` schreiben.
8. Bericht unter `data/ma_weather/reports/` schreiben.

## Verbindung zu Varianten

Das Wettermodul erzeugt keine Varianten. Die spaetere Verbindung soll ueber den
technischen `weather_key` laufen:

```text
weather_datasets
climate_file_options
PROJECT_DATA_CLIMATE
Variante
```

Damit bleibt das Wettermodul eigenstaendig und kann gepruefte Wetterdatensaetze
bereitstellen, ohne IDA ICE automatisch zu starten.
