# P016 Dimensionierung (historischer Dateititel: Analyse Stufe 1)

Stand: 2026-07-31
Status: Teilweise umgesetzt im Altbestand; Ziel-Ownership nach UD-112 ist `ma_dimensionierung`, Migrationsplanung ausstehend
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

Dieser Abschnitt beschreibt den historischen Profilvertrag. Sein Owner und
die Begrenzung auf drei Profile sind durch UD-112 abgeloest; der aktuelle
Zielvertrag steht im Konsolidierungsabschnitt am Ende dieses Plans.

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

## Handover-Ergaenzung 2026-07-21

Bei dimensionierungsrelevanten Varianten liefert P016 einen
`ReferenceDimensioningResult` fuer die Baseline und spaeter gruppierbare
`VariantDimensioningResult`-Ergebnisse. `ma_variants` erzeugt dafuer nur
Anfragen; es berechnet keine Lasten selbst. Kandidaten mit identischem
`dimensioning_input_fingerprint` duerfen ein Ergebnis teilen. Analyseergebnisse
bleiben fachlich bewertend und erzeugen hoechstens einen nicht-ausfuehrbaren
`StudyDirectionProposal`; sie aendern weder Varianten noch technische
Kapazitaeten automatisch.

## Umsetzungsstand 2026-07-27: Mehrzonen-Referenz

Die bestehende LoD-1-Berechnung verarbeitet nun die fuenf Zonen mit ihren
jeweiligen Volumen-, Luftwechsel- und internen Lastwerten. Fuer den
SmallOffice-V1-Referenzfall ergeben sich 54.130,38 W Heizlast, 9.723,26 W
interne Kuehllast und 3.053,88 m3/h Luftvolumenstrom.

Die Methode bleibt bewusst eine transparente Naeherung. Solare Gewinne,
dynamische Bilanz und ein normatives Heiz-/Kuehllastverfahren sind nicht
enthalten und werden im PreProcess als Warnungen weitergegeben.

## Konsolidierte V1-Referenzdimensionierungs-UI 2026-07-27

Nach UD-106 zeigt die Bearbeitungsansicht ausschliesslich die Zonen des
aktiven thermischen Modells sowie `Heizlast [W]` und `Kuehllast [W]`.
Diese Werte werden manuell aus IDA eingetragen. Jede Zone benoetigt beide
Werte; negative Werte sind ungueltig und `0 W` bleibt mit Pruefhinweis
zulaessig.

Die bestehende LoD-1-Berechnung bleibt technischer Referenz- und
Plausibilitaetsnachweis, ersetzt aber nicht die abgestimmte manuelle
IDA-Eingabeoberflaeche. Geaenderte vorgelagerte Fachwerte markieren die
IDA-Referenzwerte als aktualisierungsbeduerftig.

## UD-106-Umsetzungsstand 2026-07-27

Die Bearbeitungsansicht zeigt ausschliesslich die Zonen des aktiven
thermischen Modells sowie `Heizlast [W]` und `Kuehllast [W]`. Beide Werte
sind verpflichtend, negative Werte blockieren und `0 W` erzeugt einen
Pruefhinweis. Speichern erzeugt eine projektbezogene manuelle
IDA-Referenzdatei und markiert Variantenstaende aktualisierungsbeduerftig.

Die gespeicherte Referenz bindet den exakten 5Z-Zonensatz und dessen
Inhaltshash. Sortierte oder veraenderte Zonenspalten, nichtendliche Werte,
unvollstaendige Zonenmengen und ein aktives, noch gesperrtes 29Z-Modell
blockieren. IDA-Version, Modell-/Run-ID, Quelldateiname und SHA-256,
Lastdefinition, Maximumsdefinition, Auslegungsbedingungen,
Eingabeverantwortlicher und Pruefstatus sichern die Provenienz. Erst
`reviewed` mit Reviewer, ISO-Pruefdatum und Pruefhinweis ist fuer
`ma_variants` weitergabefaehig. Der gespeicherte
Referenzparameter-Fingerprint bindet die IDA-Lasten an die
dimensionierungsrelevante Baseline; geaenderte Referenzwerte sperren alte
Lasten vor einer neuen Kandidatenerzeugung.

## Konsolidierung nach UD-112 2026-07-31

Der Fachowner ist kuenftig das eigene Kernmodul `ma_dimensionierung`, nicht
`ma_analyse.stage_1_dimensioning`. P016 bewahrt den bisherigen LoD-1-Stand
als nachvollziehbaren Ausgangspunkt, ist aber zugleich der Migrationsplan:
Modelle, Services, manuelle externe IDA-Referenzwerte, Rechenwege und
Provenienz werden ohne parallele zweite Fachwahrheit in den neuen Owner
ueberfuehrt. Ein allenfalls befristeter Kompatibilitaetsadapter muss klar
markiert sein und darf keine dauerhafte doppelte Dimensionierungslogik
schaffen.

Die Dimensionierung bleibt in der UI als Unterablauf der Variantenbearbeitung
erreichbar, wird fachlich aber durch `ma_dimensionierung` ausgefuehrt. Sie
unterstuetzt je nach Studienbedarf vereinfachte und ausfuehrliche
Norm-/Excel-Verfahren sowie statische oder dynamische externe Berechnung;
deren Verfahren, Quellen und Ergebnisarten bleiben sichtbar getrennt.

`ma_import_simulation` uebernimmt nur technisch eine externe Ergebnisdatei
bis `standardized`. Die fachliche Annahme und Freigabe liegen danach in
`ma_dimensionierung`. Die bisherige direkte Eingabe zonaler IDA-Werte wird
als eigener Manual-Entry-Adapter dieses Fachmoduls gefuehrt und nicht mit
einem Dateimport vermischt.

Die verbindliche Auswahl erfolgt vor dem tatsaechlichen
Dimensionierungsauftrag. Nur ausgewaehlte, dimensionierungsrelevante
Kandidaten werden gruppiert und dimensioniert. Leistungsfaktoren erfordern
vorher nur die Referenzdimensionierung, sofern sie in absolute Leistung
ueberfuehrt werden muessen; sie begruenden fuer sich allein keine
Neudimensionierung.
