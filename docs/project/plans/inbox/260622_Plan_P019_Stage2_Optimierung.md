# P019 Analyse Stufe 2 Optimierung

Stand: 2026-06-22
Status: Geplant, teilweise vorhanden
Prioritaet: Mittel
Abhaengigkeiten: P009 Importgrenze, vorhandenes ma_analyse

## Ziel

Vorhandene Befehle fuer Variantenvergleich, Energie, Leistung, Komfort und
Zeitreihen zu einem dokumentierten Optimierungsablauf buendeln.

## Wiederzuverwendender Bestand

- `prepare`, `analyze-data`, `comfort`, `heating`, `cooling`
- Plot-Templates fuer Energie, interne Lasten und Raumklima
- vorhandene Varianten- und Raumkennwerte

## Arbeitspakete

- Kennwertkatalog und benoetigte Daten je Optimierungsfrage dokumentieren.
- Bestehende Services orchestrieren, nicht kopieren.
- Variantenvergleich und Optimierungshinweise als neutrales Ergebnisobjekt
  planen.
- Fehlende CO2-/PMV-/PPD-Daten sichtbar behandeln.
- Kalibrierung gegen Messdaten und Variantenoptimierung als getrennte
  Arbeitsablaeufe modellieren. Eine Kalibrierung veraendert nicht automatisch
  die Optimierungsentscheidung; beide Ergebnisse behalten eigene
  Randbedingungen, Datenquellen und Run-Referenzen.
- Einen leichten QA-Zyklus mit Ausgangsannahmen, Variantenhypothese,
  Auswertung, fachlicher Pruefung und nachvollziehbarer Entscheidung planen.

## Akzeptanzkriterien

- Bestehende Befehle bleiben kompatibel.
- Ein Stufe-2-Lauf ist Varianten, Raeumen und Run eindeutig zugeordnet.
- Stufe 2 fuehrt keinen Norm-Nachweis durch.
