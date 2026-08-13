# ma_data_preparation

## Zweck

Standardisierte Simulationsergebnisse programmunabhaengig pruefen und in
eine nachvollziehbare Analysedatenbasis ueberfuehren.

## Eingaben

- standardisierte numerische Zeitreihen aus `ma_import_simulation`
- Zeitsemantik, Einheit und Quellenprovenienz
- erwartete Zeitauflösung, soweit fachlich belegt

## Ausgaben

- vorbereitete Stundenreihen ohne festes 8760-Zeilen-Limit
- Qualitaets- und Eignungsstatus `READY`, `PARTIAL` oder `NOT_READY`
- CSV-Reihen und ein JSON-Manifest unter einem konfigurierbaren Zielpfad

## Abgrenzung

- programmspezifische Erkennung bleibt im Adapter; die derzeitige IDA-Bruecke
  in `ma_data_preparation.ida_ice` ist ein befristeter Integrationspfad und
  wird noch vollstaendig auf den strukturierten Importvertrag umgestellt
- keine fachliche Kennwertberechnung oder Variantenbewertung
- keine Diagramme und kein Normnachweis
- keine stillen Ersatzwerte bei Luecken oder unklaren Einheiten

## Abhaengigkeiten

- `ma_import_simulation` liefert die standardisierte Eingabe
- `ma_analyse` verwendet die vorbereitete Ausgabe

## Status

P036-S1 bis S3 sind als technischer Prototyp umgesetzt: Vertraege,
Zeitachsenpruefung, IDA-Bruecke, zeitgewichtete Aufbereitung,
Eignungsstatus und dateibasierter Export sind vorhanden. Erkannte Luecken
werden bei bekanntem Sollschritt nicht integriert und als leere
Stundenabdeckung exportiert.

## Naechster Schritt

Den strukturierten IDA-Standardvertrag durchgaengig anbinden und die offene
IDA-Zeit-/Leistungssemantik fachlich bestaetigen. Bis dahin bleiben daraus
abgeleitete Energiekennwerte `PARTIAL`.
