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

1. Stadt in der Streamlit-Oberflaeche auswaehlen.
2. Klimaregion und TRY-Referenzstandort automatisch aus dem Standortkatalog
   ableiten.
3. TRY-Referenzdatensatz zuerst empfehlen, sofern er katalogisiert ist.
4. Standortgenaue Datensaetze fuer die gewaehlte Stadt zusaetzlich anbieten.
5. Datensatz ueber `weather_key` aus dem Katalog auswaehlen.
6. TRY-Datei lokal unter `data/ma_weather/input/` bereitstellen.
7. TRY-Datei importieren und validieren.
8. Wetterkennwerte berechnen.
9. Aufbereitete Wetterdaten unter `data/ma_weather/database/` schreiben.
10. Diagramme unter `data/ma_weather/output/` schreiben.
11. Bericht unter `data/ma_weather/reports/` schreiben.

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

## Standortlogik

Die erste P008-Umsetzung nutzt einen YAML-Standortkatalog unter
`config/ma_weather/locations/`. Die Klimaregion wird nicht manuell gewaehlt,
sondern aus der Stadt abgeleitet. Die Klimaregionenkarte wird in Streamlit links
angezeigt, sobald das Bild unter `src/ma_ui/assets/weather/` vorhanden ist.
