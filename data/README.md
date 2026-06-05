# Datenbereiche

Die Datenordner sind nach Modulen und Datenrollen gegliedert.

## Aktive ma_analyse-Pfade

- `data/ma_analyse/input/`: bestehende IDA-ICE-Rohdaten.
- `data/ma_analyse/database/`: bestehende aufbereitete Nutzdaten.
- `data/ma_analyse/output/`: bestehende regulaere Analyseausgaben.

Diese Pfade sind die verbindlichen Arbeitsordner fuer `ma_analyse`. Die frueheren Root-Pfade fuer Analyse-Eingaben, Nutzdaten und Ausgaben werden nicht mehr genutzt.

## Neue Modulbereiche

- `ma_variants/`: Importberichte, Variantenexports, IDA-Uebergaben und spaetere Varianten-Datenbankartefakte.
- `ma_analyse/`: aktive Datenstruktur fuer die Analysepipeline.
- `ma_weather/`: vorbereitete Zielstruktur fuer Wetterdatenanalyse.
- `catalogs/`: Produkt-, Material-, Quellen- und Dokumentkataloge.
- `common/`: uebergreifende Berichte.
- `test_output/`: lokaler, semi-wichtiger Smoke-Test- und Arbeitsordner.
