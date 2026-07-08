# P016 Analyse Stufe 1 Dimensionierung

Stand: 2026-07-08
Status: Teilweise umgesetzt, P016-S1 LoD-1-Referenzdimensionierung
Prioritaet: Hoch
Abhaengigkeiten: P015-S1

## Ziel

Die Referenz mit transparenten vereinfachten Verfahren fuer Heizlast,
Kuehllast und Luftmengen dimensionieren.

## Reifegrad

Lite-Berechnung fuer die BusinessIntegration-LoD-1-Kette mit vorbereitetem
Ausbau zu ausfuehrlicheren und normnaeheren Verfahren.

## Arbeitspakete

- Eingabebedarf und Berechnungsannahmen je Teilverfahren dokumentieren.
- Vereinfachte Heizlast-, Kuehllast- und Luftmengenberechnung implementieren.
- Rechenweg, Zwischenwerte, Warnungen und Ergebnisqualitaet ausgeben.
- Ergebnisse gegen bekannte IDA-Referenzwerte plausibilisieren.
- `DimensioningResult` und Uebergabe als neuer Parametersnapshot planen.
- Ausbaustufe fuer ausfuehrliche Verfahren getrennt dokumentieren.

## Umsetzungsbezug P015-S1

P015-S1 liefert einen validierten `ParameterSnapshot` v1 fuer die
BusinessIntegration-LoD-1-Kette. Stage 1 soll kuenftig nicht mehr direkt auf
Building-, Zonen- oder Technik-Demos zugreifen, sondern die benoetigten
Gebaeude-, Huelle-, Nutzungs- und Technikwerte aus diesem Snapshot lesen.
Ergebnisse aus Stage 1 duerfen den Baseline-Snapshot nicht still veraendern,
sondern muessen als neuer Vorschlag oder Folgesnapshot modelliert werden.

## Umsetzungsstand P016-S1

- Paket `src/ma_analyse/stage_1_dimensioning/` enthaelt Fachmodelle,
  LoD-1-Service und UI-Tabellenhelfer.
- `run_business_integration_lod1_reference_dimensioning()` nutzt den
  validierten `ParameterSnapshot` v1 als einzige fachliche Eingabequelle.
- Berechnet werden Brutto-Aussenwandflaeche, Fensterflaeche, opake
  Aussenwandflaeche, Transmissions-Heizlast, Lueftungs-Heizlast,
  Gesamt-Heizlast, Mindest-Luftvolumenstrom und eine interne
  Kuehllastannahme.
- Jeder Rechenschritt enthaelt Formel, Wert, Einheit, Quellenparameter und
  Hinweistext.
- Fehlende oder nicht auswertbare Eingaben erzeugen `not_evaluable` statt
  Ersatzwerte.
- Streamlit zeigt eine eigene Pruefansicht fuer die Referenzdimensionierung
  mit Ergebnis, Rechenweg und Hinweisen.

## Nicht umgesetzt in P016-S1

- normgerechte Heizlastberechnung
- dynamische oder solare Kuehllastberechnung
- Plausibilisierung gegen IDA-ICE-Ergebnisse
- Speicherung als neuer Parameter-Folgesnapshot
- Variantenbildung oder automatische Systemauslegung

## Akzeptanzkriterien

- Ergebnisse sind ohne versteckte Konstanten nachvollziehbar.
- Fehlende Eingaben fuehren zu `not_evaluable` statt Ersatzwerten.
- Demo-Referenzfall besitzt erwartete Ergebnisse und Toleranzen.
- `ma_variants` haengt nicht direkt von Stage 1 ab.

## Naechster Schritt

Stage-1-Ergebnis als Folgesnapshot beziehungsweise Vorschlag modellieren und
gegen IDA-/SmallOffice-Referenzen plausibilisieren.
