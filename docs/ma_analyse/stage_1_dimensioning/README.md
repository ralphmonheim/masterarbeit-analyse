# ma_analyse.stage_1_dimensioning

## Zweck

LoD-1-Referenzdimensionierung vor der Variantenbildung.

## Eingaben

- validierter `ParameterSnapshot` v1 aus `ma_parameters`
- dokumentierte LoD-1-Auslegungsannahmen
- spaeter DimensioningRequests aus `ma_variants.VariantVerification`

## Ausgaben

- nachvollziehbare LoD-1-Startwerte fuer Heizlast, interne Kuehllastannahme
  und Mindest-Luftvolumenstrom
- Rechenweg mit Formel, Wert, Einheit und Quellenparametern
- Hinweise zur Ergebnisqualitaet
- spaeter `VariantDimensioningResult` je dimensionierungsrelevanter Gruppe

## Abgrenzung

- keine Variantenbildung
- keine Simulationsergebnisanalyse
- kein normatives Heiz- oder Kuehllastverfahren
- keine automatische Systemauslegung
- keine Selection- oder Katalogentscheidung

## Abhaengigkeiten

- `ma_parameters`
- P015-S1 `ParameterSnapshot` v1
- P017 fuer spaetere dimensionierungsrelevante Variantengruppen
- spaeter belastbare Referenzfaelle und IDA-Plausibilisierung

## Status

Teilweise umgesetzt. P016-S1 berechnet eine LoD-1-Referenzdimensionierung aus
dem BusinessIntegration-`ParameterSnapshot` v1.

## Naechster Schritt

Stage-1-Ergebnis als Folgesnapshot beziehungsweise Vorschlag modellieren,
`VariantDimensioningResult` vorbereiten und gegen IDA-/SmallOffice-Referenzen
plausibilisieren.
