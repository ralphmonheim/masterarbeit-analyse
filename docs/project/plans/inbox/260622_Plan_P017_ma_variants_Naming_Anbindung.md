# P017 ma_variants und Naming-Anbindung

Stand: 2026-07-21
Status: P017-Referenzslice umgesetzt; Ausbau fuer weitere StudyCases offen
Prioritaet: Hoch
Abhaengigkeiten: P015, P016, P018, P027

## Ziel

`ma_variants` bildet aus freigegebenen Parametern nachvollziehbare,
wissenschaftlich dokumentierte und simulationsbereite Varianten. Das Modul
trennt Variationsraum, Verifikation, Katalog, Auswahl und vollstaendige
Variantenerzeugung.

Der aktive erste Ausbau endet mit vollstaendig erzeugten ausgewaehlten
Varianten und deren Uebergabe an `ma_simulation_setup`.

Alle Ketten-, VCAT- und VSEL-Aussagen vor dem Abschnitt
`Konsolidierung nach UD-112 2026-07-31` beschreiben den damaligen
Implementierungs- oder Planstand. Bei einem Widerspruch gilt ausschliesslich
der dort dokumentierte Zielvertrag.

## Ausgangslage

Ein produktiver Prototyp fuer Varianten, Auswahl, Naming und IDA-Export ist
vorhanden. P028 nutzt bereits die Demo-Optionsauswahl aus `ma_parameters` und
ein neutrales Benennungsprofil aus `ma_project`.

Noch offen ist die verbindliche Umstellung auf:

- versionierte Eingaben aus P015.
- Stage-1-Referenzdimensionierung aus P016.
- getrennte Schritte `VSP`, `VVER`, `VCAT`, `VSEL` und `VGEN`.
- direkte Uebergabe vollstaendiger Varianten an P018.

## Historischer Umsetzungsstand 2026-07-21: erster vorfuehrbarer Referenzslice

Der folgende Referenzslice beschreibt den implementierten Altbestand. Seine
Ketten- und VSEL-Aussagen werden durch die Konsolidierung nach UD-112 am Ende
dieses Plans als Zielvertrag abgeloest.

`ma_variants.workflow` bildet fuer die freigegebene Zonenreferenz die Kette
`VSP -> VVER -> VCAT -> VSEL -> VGEN` ab:

- VSP erzeugt Kandidaten ausschliesslich aus nicht gesperrten P015-Dimensionen.
- VVER prueft die aus dem Zonenmodul gesammelte Kopplungsregel und dokumentiert
  Ablehnungen.
- VCAT enthaelt nur verifizierte Kandidaten und erzwingt die Grenze von 500.
- VSEL speichert nur `VAR-ID`s aus genau diesem Katalog.
- VGEN materialisiert nur die ausgewaehlten Varianten als `PreprocessVariant`
  mit Baselinebezug und Fingerprint.

Die Streamlit-Ansicht zeigt Variationsraum, aufklappbare Regeln, Katalog,
Auswahl und Generierung. Die fruehere P028-Optionsdemo bleibt als
kompatibler Altbestand erhalten, ist aber nicht mehr die fachliche Quelle des
Thesis-Variantenraums.

Weiter offen bleiben mehrere StudyCases, allgemeine Regeltypen,
persistierte VSP/VVER/VCAT/VSEL-Artefakte, Namensgebung auf P017-`VAR-ID`s
und die direkte P018-Handover-Integration.

## Verbindliche Hierarchie

```text
Project
-> StudyDirection
   -> StudyCase
      -> VariantSpace
         -> VariantVerification
         -> VariantCatalog
         -> VariantSelection
         -> VariantGeneration
         -> ma_simulation_setup
```

Technische Praefixe:

| Praefix | Objekt |
|---|---|
| `PRJ` | Project |
| `SDIR` | StudyDirection |
| `STC` | StudyCase |
| `VSP` | VariantSpace |
| `VVER` | VariantVerification |
| `VCAT` | VariantCatalog |
| `VSEL` | VariantSelection |
| `VGEN` | VariantGeneration |
| `CAND` | Candidate |
| `VAR` | Variant |
| `RUN` | SimulationRun |

Nicht aktiv:

- `CASE` entfaellt.
- `SimulationCase` entfaellt.
- `VHND` oder ein eigenes VariantHandover-Objekt entfaellt.
- Iterationsobjekte wie `DirectionCycle`, `StudyCaseRevision` und
  `CaseIteration` sind spaetere Updates.

## Eingaben

`ma_variants` konsumiert freigegebene, versionierbare Eingaben:

```text
BaselineParameterSnapshot
ReferenceDimensioningResult
ParameterVariationSpecification
AppliedRuleSet oder RuleSet-Referenz
project_id
study_direction_id
study_case_id
input_fingerprint
release_status
```

`ma_variants` darf nicht selbst Gebaeudedaten, Zonenparameter, Technikdaten,
Wetterdaten, Heiz-/Kuehllasten oder Simulationsparameter erfinden.

## Untersuchungsmodi

### baseline_only

Genau eine Baseline wird weitergegeben. Es gibt keine aktiven
Variationsdimensionen und keine Overrides.

### variant_study

Die Baseline bleibt kanonische Referenz. Mindestens eine aktive
Variationsdimension wird ueber `VariantSpace`, `VariantVerification`,
`VariantCatalog`, `VariantSelection` und `VariantGeneration` verarbeitet.

Die Baseline ist keine Sonder-ID. Sobald sie als Variante im Katalog gefuehrt
wird, erhaelt sie eine normale projektweite `VAR-ID` und die Rolle
`variant_role = baseline`.

## VariantSpace

Der `VariantSpace` beschreibt den theoretisch zulaessigen Kombinationsraum
eines StudyCase.

Eine Dimension kann sein:

- einzelner Parameter.
- gekoppeltes Wertepaar, zum Beispiel Heiz- und Kuehlsollwert.
- referenzierte komplexe Option.
- gemeinsamer Scope fuer mehrere Zielobjekte.

Unterstuetzte Scopes kommen aus P015, mindestens:

- `project`
- `building`
- `zone_group`
- `zone`
- `technical_system`

Jede Dimension kennzeichnet, ob sie `dimensioning_relevant` ist.

## Referenzstrategien

P017 beruecksichtigt zwei Strategien:

- `variant_specific`: Randbedingungen aendern, Last neu berechnen, Faktor auf
  die neue Last anwenden.
- `fixed_reference`: erforderliche Last kann neu berechnet werden, installierte
  oder verfuegbare Leistung bleibt auf einem festen Referenzstand.

Die fachliche Definition liegt in P015. P017 nutzt sie bei Verifikation,
Dimensionierungsgruppen und VariantGeneration.

## VariantVerification

`VariantVerification` ist der fruehe pruefende Schritt. Er erzeugt noch keine
vollstaendigen simulationsbereiten Variantenobjekte.

Aufgaben:

1. theoretische Kombinationen bestimmen.
2. Candidates in deterministischer Reihenfolge bilden.
3. Vorpruefungsregeln anwenden.
4. dimensionierungsrelevante Gruppen bilden.
5. DimensioningRequests ueber `ma_workflow` an P016 ausloesen.
6. DimensioningResults zuordnen.
7. Nachpruefungsregeln anwenden.
8. Duplikate ueber `VariantFingerprint` erkennen.
9. gueltige kompakte VariantRecords fuer den `VCAT` erzeugen.
10. VerificationReport und RejectionReport erstellen.

Fehlerhafte Candidates koennen ausgeschlossen werden, ohne den gesamten
Katalog zu blockieren. Strukturfehler, fehlende Fingerprints oder mehr als
500 gueltige Katalogeintraege blockieren den Katalog.

## Dimensionierungsgruppen

Candidates mit identischen dimensionierungsrelevanten Eingaben teilen einen
`dimensioning_input_fingerprint`.

Beispiel:

```text
5 Sollwertbaender
x 6 Heizfaktoren
x 6 Kuehlfaktoren
= 180 Kombinationen

Nur Sollwertband dimensionierungsrelevant
-> 5 Dimensionierungsgruppen
```

`ma_variants` berechnet keine Lasten selbst. Es erzeugt Anforderungen, laesst
`ma_workflow` P016 aufrufen und ordnet Ergebnisse wieder zu.

## Regeln und Fingerprints

Regelphasen:

- `pre_combination`
- `candidate_pre_dimensioning`
- `post_dimensioning`
- `catalog_integrity`
- `selection_validation`
- `generation_validation`

Ein `VariantFingerprint` beschreibt fachliche Gleichheit einer Variante. Er
enthaelt keine IDs, Namen, Erstellungszeiten oder Anzeigenamen.

Ein separater `SelectionFingerprint` ist fuer den ersten Ausbau nicht
vorgesehen. Eine Selection ist durch ID, Modus, Katalogbezug und gespeicherte
`VAR-IDs` ausreichend nachvollziehbar.

## VariantCatalog

Der `VCAT` ist ein kompakter, verifizierter Variantenindex. Er speichert nicht
alle vollstaendigen simulationsbereiten Modellobjekte.

Harte Grenze erster Ausbau:

```text
VCAT max = 500 verifizierte Varianten
```

Katalogeintrag mindestens:

- `VAR-ID`
- `VariantFingerprint`
- Dimensionswert-Referenzen
- kompakter technischer Anzeigecode
- VerificationStatus
- Herkunft aus `VVER`
- Baseline-Rolle, falls zutreffend

Statuswerte:

- `draft`
- `validating`
- `valid`
- `blocked`
- `frozen`
- `historical`

Ein fuer eine Selection verwendeter Katalogstand wird nicht stillschweigend
veraendert.

## VariantSelection

`VSEL` ist kein zweiter Katalog. Sie speichert ausgewaehlte `VAR-IDs` aus
genau einem `VCAT`.

Auswahlmodi erster Ausbau:

- `all`: nur bei `VCAT <= 50`.
- `manual`: nur bei `VCAT <= 100`.
- `random`: reproduzierbar mit `sample_size` und `random_seed`, bis zur
  VCAT-Grenze.

Grenzen:

| Ausgewaehlte Varianten | Verhalten |
|---:|---|
| 1-50 | normal |
| 51-100 | warning |
| 101-499 | approval_required mit Begruendung |
| ab 500 | blocked |

Eine verwendete Selection gehoert genau zu einem Run. Fuer einen weiteren Run
wird eine neue Selection erzeugt, auch wenn dieselben Varianten gewaehlt
werden.

Reload-Logik:

- `variant_reload` fuer lokale Probleme an einer Variante.
- `selection_reload` fuer mehrere oder strukturelle Probleme.
- `abort`, wenn der Fehler nach vollstaendigem Reload weiter besteht.

## VariantGeneration

`VGEN` erzeugt ausschliesslich die ausgewaehlten Varianten vollstaendig.

Aufgaben je `VAR-ID`:

1. Parameter- und Optionsreferenzen aufloesen.
2. Baseline-Werte und Overrides zusammenfuehren.
3. Dimensionierungsergebnisse zuordnen.
4. abgeleitete Werte berechnen.
5. Einheiten und Datentypen normalisieren.
6. vollstaendigen fachlichen Parametersatz bilden.
7. Fingerprint final bestaetigen.
8. Provenienz und Regelstatus verknuepfen.
9. simulationsrelevante Werte kennzeichnen.
10. Uebergabestatus setzen.

Die `VAR-ID` aus dem Katalog bleibt bestehen. `VGEN` kopiert oder benennt die
Variante nicht um.

Alles-oder-nichts-Regel erster Ausbau:

```text
100 ausgewaehlt
100 erfolgreich vollstaendig erzeugt
-> Uebergabe zulaessig
```

```text
100 ausgewaehlt
99 erfolgreich
1 generation_failed
-> Uebergabe blockiert
```

## Uebergabe an ma_simulation_setup

Es gibt kein separates Handover-Paketobjekt. Nach erfolgreichem `VGEN`
uebergibt P017:

- `VAR-ID`
- vollstaendigen fachlichen Parametersatz
- simulationsrelevante Teilmenge der Fachwerte
- notwendige Referenzen auf Projektmodelle

Wissenschaftliche Provenienz verbleibt in `ma_variants`:

- `VVER-ID`
- Ablehnungsstatistiken
- Regelprotokolle
- Auswahlbegruendungen
- Verification- und RejectionReports

`ma_simulation_setup` veraendert keine fachlichen Variantenwerte.

## Persistenz und Datenmengen

Softwareweit dauerhaft:

- Parameterdefinitionen und Schemas.
- Datentypen und Einheiten.
- allgemeine Optionsdefinitionen.
- technische Mappingdefinitionen.

Projektbezogen:

- StudyDirections und StudyCases.
- `VSP`, `VVER`, `VCAT`, `VSEL`, `VGEN`.
- Varianten, Regel- und Dimensionierungsprotokolle.
- wissenschaftliche Reports.
- Runs und Ergebnisverweise.

## Konsolidierung nach UD-112 2026-07-31

`ma_variants` bleibt Owner von VariantSpace, Kandidaten, Vorpruefung,
Regelprotokollen, Auswahl und Generation. Es besitzt keine
Dimensionierungsberechnung. Nach der Vorpruefung wird die tatsaechlich zu
untersuchende Menge verbindlich ausgewaehlt; nur darin werden
dimensionierungsrelevante Kandidaten nach Fingerprint gruppiert und an
`ma_dimensionierung` uebergeben. Nach Ergebnisimport und Nachpruefung wird
der finale VCAT gebildet und VGEN erzeugt die ausgewaehlten Varianten.

Die bestehende Objektmenge `VSP`, `VVER`, `VCAT`, `VSEL`, `VGEN` bleibt
massgeblich. Der bislang beschriebene Ablauf `VSP -> VVER -> VCAT -> VSEL ->
VGEN` ist deshalb als abgeloeste Reihenfolge markiert: Ein eigener
Vorab-VCAT, `CASE`, `SimulationCase` oder sonstiges Parallelobjekt wird nicht
eingefuehrt. Die fruehe verbindliche Auswahl wird als versionierter
VVER-Bestandteil mit Kandidaten-Fingerprints, Auswahlbegruendung und
gegebenenfalls Seed gespeichert. Nach Dimensionierung und Nachpruefung bildet
der finale VCAT die finalen VAR-IDs. VSEL referenziert anschliessend exakt
diese aus VVER hergeleitete Menge und dokumentiert ihre Abbildung auf VAR-IDs;
es trifft keine zweite fachliche Auswahl. Die bisherigen VSEL-Invarianten
gelten damit nur fuer den Altbestand und sind im Migrationsslice mit Tests und
Rueckwaertskompatibilitaetspruefung anzupassen.

Alle per VGEN erzeugten Varianten werden im V1 anschliessend manuell in IDA
ICE ausgefuehrt. Das ist Teil der Zeitmessung; es gibt keine unbestimmte
spaetere Kapazitaetsauswahl mehr.

Temporaer:

- nicht persistierte Kombinationen.
- UI-Sortierungen.
- Vorschauzaehlungen.
- Zwischenindizes.

Grosse Protokolle und externe Artefakte werden als Dateien gespeichert; die
Projektdatenbank haelt Referenzen, Hashes und Metadaten.

## Naming und Anzeige

Projektweite IDs laufen je Objektart fort:

```text
VAR-000001
VAR-000002
...
```

Format:

```text
<PREFIX>-<sechsstellige Nummer>
```

Die erste Anzeige bleibt technisch und kompakt:

```text
VAR-000041 | W04 | SP02 | HF080 | CF070
```

Lange lesbare Variantentitel, Baumdarstellungen und finale Exportpfade sind
bewusst zurueckgestellt. Pfade sollen spaeter eher `RUN-000001/VAR-000041/`
nutzen als lange fachliche Namen.

## Checkpoints und Validierung

P017 nutzt mit P027:

- `VSP Checkpoint`
- `VVER Checkpoint`
- `VCAT Checkpoint`
- `VSEL Checkpoint`
- `VGEN Checkpoint`

Schweregrade:

- `info`
- `warning`
- `error`
- `critical`

`valid_with_warnings` darf weitergegeben werden, wenn keine Errors oder
Criticals bestehen, alle Pflichtwerte vorhanden sind, alle Referenzen
aufloesbar sind und erforderliche Freigaben dokumentiert sind.

## Umsetzungsslices

### Preprocess V1-Mindestumfang

Preprocess V1 setzt die Grundkette `VSP -> VVER -> VCAT -> VSEL -> VGEN` mit
einer kleinen expliziten VariationSpecification aus P015 um. Der Referenzlauf
enthaelt eine Baseline und nur wenige kontrollierte Varianten; die bestehende
500er-Grenze bleibt die harte Obergrenze, ist aber kein V1-Zielwert.

`baseline_only` bleibt ein gueltiger Test- und Fallback-Modus. Die erste
fachlich nutzbare V1 schliesst jedoch mindestens eine kleine
`variant_study` ein, damit der Uebergang an P018 nicht nur demonstriert wird.
Die vorhandenen Prototypen werden dabei nicht stillschweigend zum neuen
Zielvertrag umgedeutet.

1. IDs und Grundobjekte `PRJ`, `SDIR`, `STC`.
2. `VariantSpace` und Zaehlmodell.
3. Schnittstellen zu P015, Regeln und P027-Validierung.
4. `VariantVerification` mit Candidates und Reports.
5. Dimensionierungsgruppen und Workflow-Schnittstelle zu P016.
6. `VariantFingerprint` und projektweite Duplikaterkennung.
7. `VariantCatalog` mit 500er-Grenze.
8. `VariantSelection` mit `all`, `manual`, `random` und Limits.
9. `VariantGeneration` zur vollstaendigen Aufloesung.
10. Uebergabe an P018.
11. wissenschaftliche Reports, Cache und Export der Protokolle.

## Bewusst ausgelagerte Updates

Nicht Teil der ersten Ausbaustufe:

- DirectionCycles.
- StudyCaseRevisions.
- CaseIterations.
- automatische oder assistierte Iterationen.
- Rule-based Selection.
- Filter Selection.
- Monte Carlo und Latin Hypercube.
- Kataloge groesser als 500.
- lange Variantentitel und finale Dateinamenslogik.
- `SimulationCase`.

## Akzeptanzkriterien

- Jede Reduktion der Variantenanzahl ist dokumentiert.
- `VVER` und `VGEN` sind fachlich getrennte Schritte.
- `VCAT` bleibt auf 500 Eintraege begrenzt.
- `VSEL` ist eine Auswahl, kein eigener Katalog.
- Nur ausgewaehlte Varianten werden vollstaendig erzeugt.
- Varianten werden nicht in `SimulationCases` kopiert oder umbenannt.
- Wissenschaftliche Provenienz verbleibt in `ma_variants`.
- P018 erhaelt vollstaendige Varianten mit `VAR-ID`, aber keine versteckten
  fachlichen Regeln.

## Naechster Schritt

P017-S1 planen: Grundobjekte, IDs, `VariantSpace`, Zaehlmodell und stabile
Eingangsreferenzen auf P015/P016 ohne Bruch des bestehenden Prototyps.

## Handover-Ergaenzung 2026-07-21

Die Varianten-Handover praezisieren P017-S1 und seine Folgeslices:

- Die lineare Kette bleibt `VSP -> VVER -> VCAT -> VSEL -> VGEN`. `VGEN`
  erzeugt vollstaendige `VAR`; ein separates Handover- oder `SimulationCase`
  Objekt wird nicht eingefuehrt.
- `VVER` dokumentiert Ausschluesse, Dimensionierungsbedarf,
  Fingerprints und Regeln. `VCAT` enthaelt nur verifizierte, rekonstruierbare
  Varianten und bleibt auf 500 Eintraege begrenzt.
- `VSEL` arbeitet in V1 mit `all`, `manual` oder `random`; regelbasierte
  Selection, automatisches Sampling und automatische Iterationen bleiben
  spaetere, nicht freigegebene Erweiterungen.
- Bei lokalen Aenderungen sind selektive Reloads moeglich; strukturelle
  Inkonsistenzen erfordern einen neuen oder vollstaendig neu validierten
  Katalog. Begrenzte technische Kapazitaeten sind als Variantenwert zulaessig,
  solange keine technische Invariante verletzt ist.
- P018 erhaelt nach `VGEN` vollstaendige Varianten mit `VAR-ID`; Regeln,
  Ausschlussgruende und wissenschaftliche Provenienz verbleiben in P017.

## Umsetzungsstand 2026-07-27: SmallOffice-V1-Studie

`config/ma_variants/studies/small_office_v1.yaml` beschreibt die erste
versionierte V1-Studie. Fuenf globale Temperatur-Sollwertbaender werden mit
sechs gekoppelten Faktoren fuer verfuegbare Heiz- und Kuehlleistung
kombiniert. Daraus entstehen 30 Optimierungsfaelle; innerhalb jedes Falls
gelten dieselben Sollwerte fuer alle fuenf Zonen.

Acht Sensitivitaetsfaelle bleiben von der Optimierung getrennt. Sie verwenden
den Referenz-/Dimensionierungsfall 21/24 Grad C und Faktor 1,0 als festen
Elternfall: vier Frankfurt-Jahreswetter sowie die vier Zeitprofile
07:00-18:00, 06:00-17:00, 08:00-19:00 und 06:00-19:00. Eine automatische
Bestvariantenwahl findet in V1 nicht statt.

## Konsolidierter V1-Auswahlablauf 2026-07-27

UD-106 fuehrt Optimierung und Sensitivitaet als gleichzeitig anlegbare,
getrennte StudyDirections. Der aktive StudyCase wird ueber ein Auswahlfeld
gewechselt und zeigt seine wirksamen Regeln schreibgeschuetzt.

Die sichtbare Reihenfolge lautet:

1. `Variationsraum` mit `Kandidatenkombinationen erzeugen`;
2. `Pruefung und Katalog` mit `Gueltigen Katalog bilden`;
3. `Auswahl und Variantenpakete` mit manueller, zufaelliger oder
   vollstaendiger Auswahl, `Namensvorschau erzeugen` und
   `Ausgewaehlte Variantenpakete erzeugen`.

Ungueltige Kandidaten bleiben mit Ausschlussgrund sichtbar. Zufallsauswahl
speichert Anzahl und optionalen Startwert. Ein Naming-Profil ist vor der
Paketerzeugung verpflichtend. Geaenderte Referenzwerte, Regeln oder Spannen
markieren bestehende Kandidaten und Pakete aktualisierungsbeduerftig, loeschen
sie aber nicht.

## UD-106-Umsetzungsstand 2026-07-27

Die UI fuehrt drei sitzungsstabile Schritte und die vereinbarten Buttons:
Kandidatenkombinationen erzeugen, gueltigen Katalog bilden,
Namensvorschau erzeugen und ausgewaehlte Variantenpakete erzeugen.
Optimierung und Sensitivitaet werden gleichzeitig als drei getrennte
StudyCases angelegt. Manuelle, reproduzierbar zufaellige und vollstaendige
Auswahl sind umgesetzt; ungueltige Kandidaten bleiben mit Ausschlussgrund
sichtbar.

Der Quellenfingerprint umfasst nun Studienvertrag, Baseline-ID/-Hash,
5Z-Modell/-Hash, aktuelle Regeln und Variationsspannen sowie den
vollstaendigen IDA-Referenzdatensatz. Kandidaten entstehen nur bei aktueller
Variationsspezifikation und geprueftem 5Z-Stand. Die Faktoren werden nach der
Strategie `fixed_reference_21_24_zonal_capacity` fuer jede Zone auf Heiz- und
Kuehlreferenzlast in W angewandt. Wetter- und Belegungssensitivitaet bleiben
getrennte OFAT-Familien mit `OPT-SB01-F100` als festem Elternfall.
Namensvorschauen sind an Projekt, StudyCase, Auswahl, Quellenfingerprint und
Naming-Profil gebunden.

Die Katalogbildung akzeptiert nur Kandidaten mit dem aktuellen
Quellenfingerprint; ein alter Kandidatenraum kann nicht unter einem neuen
Fachstand neu etikettiert werden. Jede `VSEL`-ID enthaelt einen eigenen
Fingerprint aus StudyCase, Modus, sortierten Kandidaten-IDs, Zufallsseed und
Upstream-Stand. Eine leere manuelle Auswahl erzeugt keine Pakete.

Der SmallOffice-V1-Studienvertrag akzeptiert genau die vier eindeutigen
Dimensionen Temperatur-Sollwertbaender, gekoppelte Heiz-/Kuehlfaktoren,
Wetter-OFAT und Belegungs-OFAT. Unbekannte, fehlende oder doppelte
Dimensionen blockieren die Kandidatenerzeugung. Vor der Setup-Uebergabe
werden Selection-ID, Kandidatenmenge, StudyCase, StudyDirection und
Selection-Fingerprint erneut typgenau gegen alle Variantenpakete geprueft.

## Migrationsstand nach UD-112 2026-08-03

P017-S1 und der anschliessende UI-Gate-Slice sind additiv umgesetzt:
`VverSelectionRecord` speichert die fruehe verbindliche Auswahl vor der
Dimensionierung mit Kandidatenfingerprints, Begruendung, Modus/Seed und einem
eigenen Pre-Dimensioning-Upstream-Fingerprint. Die direkte Variantenansicht
erzeugt Kandidaten und speichert VVER ohne Dimensionierungs-Gate. Eine aktive,
aktuelle VVER-Auswahl ist dagegen vor dem Speichern der manuellen
Referenzdimensionierung und vor dem finalen Katalog verbindlich. Der finale
Katalog beschraenkt sich auf die VVER-Kandidaten; er vergibt in diesem
Uebergang noch keine neue fachliche Auswahl.

VVER-Historie bleibt append-only im Variantenpayload sichtbar. Beschaedigte
Historie blockiert weitere VVER-/Katalogaktionen sichtbar; alte Kandidaten
ohne Pre-Dimensioning-Fingerprint bleiben erhalten, muessen aber fuer eine
neue VVER-Auswahl regeneriert werden. Es gibt weiterhin keinen CASE oder
SimulationCase und keine Vorab-VCAT- oder VAR-ID-Erzeugung durch VVER.

Offen fuer den naechsten Backend-Slice: Der historische SmallOffice-Runner
und `ma_variants.small_office_v1` berechnen noch Kapazitaeten aus
Referenzlast mal Faktor und laufen noch in der alten Reihenfolge. Sie muessen
auf VVER-ausgewaehlte, fingerprintgruppierte Dimensionierungsauftraege an
`ma_dimensionierung` umgestellt werden. Erst danach folgen finaler
VCAT-/VAR-ID- und abbildender VSEL-Slice sowie VGEN/P018.

## Migrationsstand VVER-zu-Dimensionierung 2026-08-03

Der historische SmallOffice-Backendpfad akzeptiert jetzt eine aktuelle,
explizite VVER-Auswahl und erstellt daraus keine Varianten- oder
Katalogobjekte, sondern nur Kandidatenauftraege. Gleiche LoD-1-Eingaben werden
per Owner-Fingerprint gruppiert; nach der Owner-Berechnung werden die
Kapazitaeten den VVER-Kandidaten wieder zugeordnet. Fuer die aktuelle
vereinfachte Methode ergeben die fuenf Sollwertbaender vier Gruppen, weil
zwei Baender dieselben rechenwirksamen LoD-1-Eingaben besitzen.

`ma_variants.small_office_v1` leitet keine Lasten oder Kapazitaeten mehr aus
Referenzlasten mal Faktor ab. Finaler VCAT mit VAR-IDs, rein abbildender VSEL,
VGEN und P018 bleiben nach diesem bewusst isolierten Backend-Slice offen.

## Finaler VCAT-/VSEL-/VGEN-Vertrag 2026-08-03

Der additive Abschlussvertrag erzeugt VCAT erst nach VVER-gebundener
Owner-Dimensionierung und Nachpruefung. Eine projektweite append-only
Registry vergibt sequenzielle VAR-IDs anhand des ID-freien finalen
Inhaltsfingerprints; gleicher finaler Inhalt nutzt projektweit dieselbe
VAR-ID. VSEL ist ausschliesslich die Abbildung von VVER-Kandidat auf finale
VAR-ID, VGEN bindet diese erst danach an `PreprocessVariant`.

Offen: atomare Workspace-Anbindung des Payload-Adapters sowie eigene VVER,
Dimensionierung und Abschluss fuer Wetter-/Belegungs-StudyCases nach UD-117.

## Kapazitaetsstrategie 2026-08-03

Die Kapazitaetsstrategie ist Bestandteil des Studienvertrags vor VVER und
Dimensionierung. `ideal_unlimited` reduziert den SmallOffice-Default auf die
fuenf Sollwertbaender mit dem Referenzfaktor F100; seine Varianten enthalten
keine wirksamen Kapazitaets-Overrides. Nach Abschluss der Owner-
Dimensionierung tragen sie die Referenz-Heiz- und Kuehlleistung ausschliesslich
als Analyseprovenienz. Die bisherige Faktorenreihe F100 bis F050 bleibt unter
`dimensioned_with_factor` erhalten und wird erst nach dem Ergebnis absolut.
