# P017 ma_variants und Naming-Anbindung

Stand: 2026-07-14
Status: Fachlich konsolidiert, Umsetzung geplant
Prioritaet: Hoch
Abhaengigkeiten: P015, P016, P018, P027

## Ziel

`ma_variants` bildet aus freigegebenen Parametern nachvollziehbare,
wissenschaftlich dokumentierte und simulationsbereite Varianten. Das Modul
trennt Variationsraum, Verifikation, Katalog, Auswahl und vollstaendige
Variantenerzeugung.

Der aktive erste Ausbau endet mit vollstaendig erzeugten ausgewaehlten
Varianten und deren Uebergabe an `ma_simulation_setup`.

## Ausgangslage

Ein produktiver Prototyp fuer Varianten, Auswahl, Naming und IDA-Export ist
vorhanden. P028 nutzt bereits die Demo-Optionsauswahl aus `ma_parameters` und
ein neutrales Benennungsprofil aus `ma_project`.

Noch offen ist die verbindliche Umstellung auf:

- versionierte Eingaben aus P015.
- Stage-1-Referenzdimensionierung aus P016.
- getrennte Schritte `VSP`, `VVER`, `VCAT`, `VSEL` und `VGEN`.
- direkte Uebergabe vollstaendiger Varianten an P018.

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
