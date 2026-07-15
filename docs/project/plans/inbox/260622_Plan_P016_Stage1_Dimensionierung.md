# P016 Analyse Stufe 1 Dimensionierung

Stand: 2026-07-14
Status: Teilweise umgesetzt, P016-S1 LoD-1-Referenzdimensionierung; VariantDimensioningResult fuer P017 geplant
Prioritaet: Hoch
Abhaengigkeiten: P015, P017, P027

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
- Variantenspezifische Dimensionierungsanfragen aus P017 entgegennehmen,
  sobald `VariantVerification` dimensionierungsrelevante Gruppen bildet.
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
- `VariantDimensioningResult` fuer dimensionierungsrelevante
  P017-Kandidatengruppen
- Variantenbildung oder automatische Systemauslegung

## Umsetzungsbezug P017

P017 berechnet keine Heiz- oder Kuehllasten selbst. Wenn
`VariantVerification` dimensionierungsrelevante Aenderungen erkennt, bildet
es Gruppen mit gleichem `dimensioning_input_fingerprint` und uebergibt
`DimensioningRequest`-Objekte ueber `ma_workflow` an Stage 1.

P016 liefert dafuer spaeter je Gruppe:

- `dimensioning_result_id`
- erforderliche Heizlast
- erforderliche Kuehllastannahme
- erforderlicher Luftvolumenstrom
- Rechenstatus, Rechenweg und Provenienz

Diese Ergebnisse werden an `VariantVerification` zurueckgegeben und dort den
Candidates zugeordnet. P016 erzeugt keine Varianten und trifft keine
VariantSelection.

## Akzeptanzkriterien

- Ergebnisse sind ohne versteckte Konstanten nachvollziehbar.
- Fehlende Eingaben fuehren zu `not_evaluable` statt Ersatzwerten.
- Demo-Referenzfall besitzt erwartete Ergebnisse und Toleranzen.
- `ma_variants` haengt nicht direkt von Stage 1 ab.

## Naechster Schritt

Stage-1-Ergebnis als Folgesnapshot beziehungsweise Vorschlag modellieren,
`VariantDimensioningResult` fuer P017 vorbereiten und gegen
IDA-/SmallOffice-Referenzen plausibilisieren.

## Preprocess V1-Mindestumfang

P016 liest in Preprocess V1 die freigegebene Baseline aus P015 und erzeugt
einen eigenen `ReferenceDimensioningResult` mit Eingangs-Fingerprint,
Rechenweg und Status. Eine normative Berechnung, IDA-Plausibilisierung und
variantenspezifische Dimensionierungsgruppen sind keine V1-Voraussetzung.

## Handover-Abgleich: OutputRequirementProfiles fuer MVP V1

P016 und die bestehende Analyse definieren gemeinsam einen kleinen,
programmunabhaengigen Vertrag `OutputRequirementProfile`. P018 uebernimmt ihn
nur als Pflichtausgabeanforderung; P009 und `ma_analyse` verwenden ihn bei
Ergebnisaufnahme und Diagrammerzeugung.

Der Vertrag und die drei MVP-V1-Profile sind am 2026-07-14 in
`ma_analyse.stage_1_dimensioning` umgesetzt; P018 referenziert sie nur.

Fuer MVP V1 sind genau drei Profile erforderlich:

1. Heiz-/Kuehllast nach Variante und Zone,
2. Raumtemperatur beziehungsweise Komfortzeitreihe fuer ausgewaehlte Zonen,
3. Jahres- oder Spitzenwertvergleich zwischen Baseline und Varianten.

Ein Profil beschreibt Kennwert, Einheit, zeitliche Aufloesung, Bezugsobjekt,
Pflichtstatus und erwarteten Diagrammtyp. Es enthaelt keine
programmspezifischen Ergebnisnamen und keine IDA-Exportlogik. Weitere
Optimierungs-, Norm- oder Sensitivitaetsausgaben bleiben ausserhalb von MVP V1.
