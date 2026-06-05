# Strukturreview

Datum der Pruefung: 2026-06-04

## Projektuebersicht

Das Projekt besteht aktuell aus zwei produktiven Python-Paketen:

- `ma_analyse`: bestehende Analysepipeline fuer IDA-ICE-Simulationsergebnisse.
- `ma_variants`: neuer Varianten-, Export-, Katalog- und Bewertungskern.

`ma_weather` ist als spaeteres Modul fuer Wetterdatenanalyse und TRY-Integration vorbereitet, aber fachlich noch nicht implementiert.

## Gefundene Ordnerstruktur

- `src/ma_analyse/`: Analyse, CLI, GUI, Preprocessing, Plot-Templates.
- `src/ma_variants/`: Parameter, Optionen, Varianten, Datenbank, IDA-Export, Simulationsergebnisse, Wirtschaftlichkeit, Kataloge, UI.
- `docs/`: wurde in `project`, `ma_analyse`, `ma_variants`, `ma_weather`, `common` und `examples` modularisiert.
- `config/ma_variants/`: Variantenbezogene Beispielkonfigurationen.
- `data/ma_analyse/`: aktive Rohdaten, aufbereitete Nutzdaten und regulaere Analyseausgaben der Analysepipeline.
- `data/ma_variants/`: Variantenbezogene Import-, Export- und IDA-Uebergabedaten.
- `data/catalogs/`: separater Bereich fuer Produkt-/Material-/Quellkataloge und Datenblaetter.
- `data/test_output/`: lokaler, semi-wichtiger Arbeits- und Smoke-Test-Ordner.
- `docs/project/plans/inbox/`: aktuelle, noch nicht archivierte Umsetzungsplaene.
- `docs/project/plans/archived/`: umgesetzte oder alte Plaene.

## Staerken

- Die Quellcodepakete `ma_analyse` und `ma_variants` sind fachlich getrennt.
- Tests fuer beide Bereiche sind vorhanden.
- Die neue Dokumentationsstruktur ordnet Plaene und Modul-Dokumente klarer.
- `CHANGELOG.md` bleibt als zentrale Aenderungshistorie im Root.
- Produkt- und Materialdatenblaetter werden nicht in PostgreSQL gespeichert, sondern ueber Pfade referenziert.
- P001 und P002 liegen als Markdown-Plaene in der Plan-Inbox vor.

## Schwachstellen

- `src/ma_analyse/gui/app.py` ist sehr gross und sollte spaeter aufgeteilt werden.
- `src/ma_analyse/analysis/heating.py` und `src/ma_analyse/analysis/cooling.py` enthalten aehnliche Strukturen und sollten spaeter ueber gemeinsame Runner/Helper weiter vereinheitlicht werden.
- In `data/test_output/` liegen lokale Arbeits- und Testartefakte verschiedener Pruefungen. Der Ordner ist bewusst nicht als Referenzbereich gedacht.

## Risiken

- Eine weitere GUI-Aufteilung sollte nicht parallel zu groesseren Analyse-Refactorings erfolgen.
- Die Plan-Inbox enthaelt aktive Plaene. Umgesetzte Plaene muessen konsequent nach `docs/project/plans/archived/` verschoben werden.

## Empfehlungen

- P001 nach manueller Streamlit-Pruefung abschliessen und danach archivieren.
- P002 erst nach gesonderter Bestandspruefung des TRY-Plans vorbereiten.
- `data/test_output/` regelmaessig manuell leeren, aber nicht als Referenzgalerie verwenden.
- `docs/examples/plot_templates/` als wichtige Referenz fuer aktuelle `ma_analyse`-Plot-Templates behalten.

## Offene Fragen

- Soll P001 nach manueller Streamlit-Pruefung als abgeschlossen archiviert werden?
- Welche Chat-Exporte sollen fuer Nutzerentscheidungen ausgewertet werden?
