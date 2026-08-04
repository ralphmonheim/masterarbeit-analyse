# ma_analyse.stage_1_dimensioning (historischer Kompatibilitaetspfad)

Der Zielowner ist `ma_dimensionierung`. Im aktuellen Prep-Slice bleibt die
Fachimplementierung hier unveraendert; der neue Namespace re-exportiert
dieselben Objekte direkt. Dieser Stand ist noch keine abgeschlossene
fachliche Owner-Migration. `OutputRequirementProfile` verbleibt als
Analyse-/PostProcess-Vertrag bewusst unter `ma_analyse`.

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
dem BusinessIntegration-`ParameterSnapshot` v1. Der P016-Prep-Slice stellt
den identitaetsgleichen Zielnamespace bereit; Implementierung,
Persistenzschluessel und Workflow-Katalog sind noch historischer Bestand.
P016-S2a ergaenzt im Zielnamespace einen validierenden Gateway mit
Einheitenmatrix, Methoden- und Annahmenmetadaten sowie kanonischen
Fingerprints. Er delegiert weiterhin an diese historische Implementierung und
ist keine physische Owner-Migration.

## Naechster Schritt

Getrennte Ergebnisvertraege fuer berechnete LoD-1-Naeherung und manuelle
IDA-Referenzwerte modellieren; danach die physische Owner-Migration planen.
