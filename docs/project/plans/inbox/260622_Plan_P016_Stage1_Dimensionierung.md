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

## P016-Prep-Checkpoint: Zielnamespace 2026-08-02

Der oeffentliche Namespace `ma_dimensionierung` ist als kleiner,
reversibler Vorbereitungsslice angelegt. Er re-exportiert die bestehenden
Modelle, Konstanten, Tabellenprojektionen und Services direkt und
objektidentisch aus `ma_analyse.stage_1_dimensioning`. Direkte
Dimensionierungsverbraucher in UI, SmallOffice-PreProcess und
SmallOffice-Variantenhilfe importieren ueber die neue Grenze. Es wurden
keine Gleichungen, Zahlenwerte, Diagnosecodes, Payloads oder
Persistenzschluessel geaendert.

Dieser Checkpoint ist keine abgeschlossene fachliche Owner-Migration. Die
Implementierung, der Workspace-Schluessel
`ma_analyse_stage_1_dimensioning` und der Workflow-Katalog bleiben
vorlaeufig historischer Bestand. `OutputRequirementProfile` wird nicht ueber
`ma_dimensionierung` exportiert und bleibt als Ausgabeanforderung bei
`ma_analyse`.

Vor einer physischen Owner-Migration gelten folgende Council-Befunde als
Blocker:

- der Gateway muss einen validierten Snapshot und erwartete Einheiten
  verlangen;
- Ergebnis und Eingaben brauchen Methoden-/Versionsbezug, strukturierte
  Annahmen sowie kanonische Fingerprints und Rundungsregel;
- berechnete LoD-1-Naeherung und manuell uebernommene externe IDA-
  Referenzwerte brauchen getrennte Ergebnisvertraege;
- fachliche Manual-Entry-Validierung und Payloadbildung muessen aus der UI
  in den Owner ueberfuehrt werden;
- `ma_variants` darf nach der spaeteren fruehen Auswahl keine Lasten selbst
  berechnen; der P016/P017-Ablauf bleibt ein eigener Slice.

Der P027-Workflow-Ansichtsslice bleibt unveraendert am Ende. Die spaetere
Katalogmigration ist kein Bestandteil dieses Prep-Checkpoints.

## P016-S2a Owner-Gateway 2026-08-02

Der additive Owner-Gateway ist umgesetzt. Er akzeptiert fuer diesen
Uebergangsslice ausschliesslich den bestehenden `ParameterSnapshot` v1; eine
stillschweigende Konvertierung des `BaselineParameterSnapshot` v2 findet nicht
statt. Vor der Delegation an die unveraenderte historische LoD-1-Berechnung
prueft er `validate_parameter_snapshot()`, die kanonischen Einheiten aller
rechenwirksamen globalen, zonalen und optionalen Parameter sowie endliche
Auslegungsannahmen. Es gibt keine Einheitenumrechnung.

Der Auftrag fuehrt Methoden-ID/-Version, Vertragsversion, strukturierte
Annahmen, die dokumentierte Rundungsregel `python round(float, 2) nach der
Berechnung` und einen kanonischen SHA-256-Eingangsfingerprint. Ein getrennter
Gateway-Ausfuehrungsrahmen ergaenzt den Ergebnisfingerprint ohne zufaellige
Diagnose-IDs oder Zeitstempel. Das bisherige `ReferenceDimensioningResult`
bleibt unveraendert und kompatibel.

Die getrennten fachlichen Ergebnisvertraege fuer berechnete LoD-1-Naeherung
und manuelle IDA-Referenzwerte, die UI-neutrale Manual-Entry-Regel sowie die
physische Owner-Migration bleiben ausdruecklich P016-S2b/S2c.

## P016-S2b/S2c Ergebnis- und Manual-Entry-Vertraege 2026-08-03

`ma_dimensionierung` besitzt nun getrennte, versionierte Vertraege fuer die
berechnete LoD-1-Referenz und manuell aus einem externen IDA-Lauf uebernommene
Zonenlasten. Der Gateway adaptiert die LoD-1-Ausfuehrung additiv; der
Manual-IDA-Vertrag prueft Zonensatz, Werte, Quellenprovenienz, Review und
Fingerprints. Die UI ist nur noch fuer Eingabe, Darstellung und Workspace-I/O
zustaendig; sie nutzt die Owner-Validierung und erzeugt weiterhin den
unveraenderten Legacy-Payload unter `ma_analyse_stage_1_dimensioning`.

Offen bleibt die physische Migration der historischen Gleichungen,
Persistenz- und Workflowkataloggrenze. Der naechste gekoppelte P016/P017-
Slice muss VVER-ausgewaehlte Kandidaten als gruppierte
Dimensionierungsauftraege an diesen Owner uebergeben und die verbleibende
Kapazitaetsableitung aus `ma_variants` entfernen.

## P016-S2b Ergebnisarten 2026-08-02

`CalculatedLod1ReferenceResult` und `ManualIdaReferenceLoadSet` sind nun
getrennte, versionierte Owner-Vertraege. Der erste adaptiert die Gateway-
Ausfuehrung, der zweite liest den unveraenderten manuellen Legacy-Payload nur
pruefend. Workspace-Schluessel, Payloadschema und UI bleiben bis S2c erhalten.

## P016/P017 SmallOffice-VVER-Gruppen 2026-08-03

Der historische SmallOffice-Optimierungspfad erzeugt nun ausschliesslich mit
einem aktuellen `VverSelectionRecord` LoD-1-Auftraege. Der Owner
`ma_dimensionierung` validiert die Kandidatenreferenzen, bildet Gruppen nach
dem kanonischen LoD-1-Eingangsfingerprint, berechnet die Lasten und leitet
erst danach die absoluten Heiz-/Kuehlkapazitaeten aus dem gekoppelten Faktor
ab. `ma_variants` besitzt keine Last- oder Kapazitaetsgleichung mehr.

Der Slice erzeugt weder finale `VAR-ID`s noch `VCAT`, `VSEL`, `VGEN`, `CASE`
oder `SimulationCase`. Der LoD-1-Owner bleibt bis zur physischen Migration
noch ein Gateway vor der historischen Berechnung; finaler VCAT/VSEL sowie
die P018-Anbindung sind getrennte Folgeslices.

## Fachliche Arbeitsnotiz 2026-08-11: SmallOffice-Huelle fuer manuelle Heizlast

Der flaechengewichtete Huelle-U-Wert ist fuer eine vereinfachte manuelle
Heizlastannahme als `sum(A_i * U_i) / sum(A_i)` zu bilden. Die lokale,
noch zu reproduzierende SmallOffice-Gebaeudeaggregation ergab mit Wand
`0.28`, Fenster `1.30`, Tuer `1.80`, Dach `0.20` und Boden `0.35` W/(m2 K)
rund `0.448` W/(m2 K); der Wert `0.45` ist damit als gerundete
Gebaeudeannahme plausibel. Mit Boden `0.28` ergab sich rund `0.430` W/(m2 K).

Der Bezug in der Nutzer-Arbeitsmappe
`Masterarbeit_Heizlastberechnung_DIN_EN_12831.xlsx` betrifft das Blatt `5Z`
und Zelle `B7` fuer den mittleren U-Wert der Huelle. Diese Werte
ersetzen keine zonale Bauteilbilanz. Fuer die fuenf thermischen Zonen sind
Huelle, Oeffnungen und Boden-U-Wert vor einer fachlichen Nutzung manuell zu
bestaetigen; die IFC-Raumgrenzen liefern dafuer derzeit keine vollstaendige
Vertikalhuelle. Die Auslegungstemperatur `-12 Grad C` ist separat gegen den
fuer den Standort geltenden Nationalen Anhang zu DIN EN 12831-1 zu pruefen.
