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

## Umsetzungsstand 2026-08-11: gemeinsame Analyse-Demo

- Die bestehende Streamlit-Auswahl bleibt als `Auswahl & Lauf` erhalten.
- Eine gemeinsame Tab-Ansicht ordnet Dimensionierung, Optimierung, Nachweis
  und Sensitivitaet sichtbar, ohne ihre Fachlogik zu vermischen.
- Der aktuelle `AnalysisResult` wird ausschliesslich Stage 2 zugeordnet;
  Diagrammvorschau, Dateien, Warnungen und Fehler werden gemeinsam
  dargestellt. Der Renderer fuer Summary- und Detailtabellen ist vorbereitet,
  deren produktive Befuellung bleibt ein eigener PostProcess-Slice.
- Stage 1 bleibt beim Owner `ma_dimensionierung`. Stage 3 und Stage 4 zeigen
  bis zu eigenen Ergebnisvertraegen sichtbar `nicht auswertbar`.
- Ein aktiver Projekt-Workspace liefert standardmaessig
  `<Projektordner>/output/ma_analyse/`; bestehende interne Dateinamen und
  Unterordner bleiben unveraendert. Letzte Ergebnisse werden an die aktive
  Projekt-ID gebunden und bei einem Projektwechsel verworfen.

## Umsetzungsstand 2026-08-11: P029-S12 Ergebnisvertrag

- `analyze-data` befuellt `AnalysisResult.summary_table` und
  `detail_tables` produktiv aus demselben Tabellenvertrag wie der Excel-
  Export.
- Die Leistungsdarstellung ist `W`, `W/m2` oder `Beides`; automatische
  Ausgaben verwenden `Beides`. `W/m2` wird nur mit positiver, raumbezogener
  Nettoflaeche berechnet.
- Dateninventar und Berechnungsgrenzen unterscheiden Auswertungsstunden von
  noch nicht belegten Nutzungsstunden und zeigen fehlende Daten oder Flaechen
  sichtbar `nicht auswertbar`.
- Eine Readiness-Tabelle bereitet Stage 3 vor, ohne Normwerte oder
  Nachweisergebnisse in Stage 2 zu berechnen.
