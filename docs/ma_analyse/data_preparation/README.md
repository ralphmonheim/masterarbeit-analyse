# ma_analyse.data_preparation

## Zweck

Importierte Simulationsergebnisse fuer die fachlichen Analysestufen
vorbereiten. Dazu gehoeren aktuell der bestehende `prepare`-Befehl und der
Basisbericht ueber `analyze-data`.

## Eingaben

- standardisierte Simulationsergebnisse aus `ma_import_simulation`
- lokale IDA-Rohdatenvarianten unter `data/ma_analyse/ida_imports/`
- Varianten-, Raum- und Ausgabeauswahl fuer den Basisbericht

## Ausgaben

- aufbereitete Raumtabellen unter `data/ma_analyse/database/`
- Basisbericht und Excel-Datenuebersicht
- Logdateien fuer die ausgefuehrten Vorbereitungsschritte

## Abgrenzung

- keine Variantenoptimierung
- kein Norm-Nachweis
- keine Sensitivitaetsbewertung
- kein Importadapter fuer IDA ICE

## Abhaengigkeiten

- `ma_analyse`
- `ma_import_simulation`

## Status

Teilweise vorhanden. `prepare` und `analyze-data` existieren bereits als
Befehle in `ma_analyse`; ein gemeinsamer Datenvorbereitungsablauf nach einem
erfolgreichen Simulationsergebnisimport ist noch nicht vollstaendig
orchestriert.

## Naechster Schritt

`prepare` nach erfolgreichem Import als Standard-Folgeschritt anbieten und
`analyze-data` als sichtbaren Basisbericht vor Analyse Stufe 2 einordnen.
