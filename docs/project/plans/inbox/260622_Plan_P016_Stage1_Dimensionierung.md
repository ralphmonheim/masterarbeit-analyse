# P016 Analyse Stufe 1 Dimensionierung

Stand: 2026-06-22
Status: Geplant
Prioritaet: Hoch
Abhaengigkeiten: P015

## Ziel

Die Referenz mit transparenten vereinfachten Verfahren fuer Heizlast,
Kuehllast und Luftmengen dimensionieren.

## Reifegrad

Produktive Lite-Berechnung mit vorbereitetem Ausbau zu ausfuehrlicheren und
normnaeheren Verfahren.

## Arbeitspakete

- Eingabebedarf und Berechnungsannahmen je Teilverfahren dokumentieren.
- Vereinfachte Heizlast-, Kuehllast- und Luftmengenberechnung implementieren.
- Rechenweg, Zwischenwerte, Warnungen und Ergebnisqualitaet ausgeben.
- Ergebnisse gegen bekannte IDA-Referenzwerte plausibilisieren.
- `DimensioningResult` und Uebergabe als neuer Parametersnapshot planen.
- Ausbaustufe fuer ausfuehrliche Verfahren getrennt dokumentieren.

## Akzeptanzkriterien

- Ergebnisse sind ohne versteckte Konstanten nachvollziehbar.
- Fehlende Eingaben fuehren zu `not_evaluable` statt Ersatzwerten.
- Demo-Referenzfall besitzt erwartete Ergebnisse und Toleranzen.
- `ma_variants` haengt nicht direkt von Stage 1 ab.
