# ma_dimensionierung

## Ziel

`ma_dimensionierung` wird nach UD-112 der alleinige Fachowner fuer
Referenz- und variantenspezifische Dimensionierung. Das Modul erzeugt keine
Varianten und trifft keine Auswahlentscheidung.

## Aktueller Migrationsstand

Der oeffentliche Python-Namespace ist vorbereitet; die fachliche Owner-
Migration ist noch nicht abgeschlossen. `src/ma_dimensionierung/__init__.py`
re-exportiert die vorhandenen Dimensionierungsmodelle und -services direkt
und objektidentisch aus dem historischen
`ma_analyse.stage_1_dimensioning`-Pfad. Es existieren weder Wrapper noch
kopierte Modelle, Konstanten oder Gleichungen und damit keine zweite
Dimensionierungslogik.

P016-S2a ergaenzt daneben einen additiven LoD-1-Owner-Gateway. Er validiert
den bestehenden `ParameterSnapshot` v1, prueft die kanonischen Einheiten und
bildet Methoden-, Annahmen-, Rundungs- und Fingerprintdaten ab, bevor er an
die unveraenderte historische Berechnung delegiert. Der Gateway ersetzt noch
kein historisches Ergebnisobjekt und keine Persistenz.

Direkte Verbraucher in der Dimensionierungsansicht, im SmallOffice-
PreProcess und in der SmallOffice-Variantenhilfe importieren bereits ueber
`ma_dimensionierung`. Der historische Workspace-Schluessel
`ma_analyse_stage_1_dimensioning`, gespeicherte Payloads und der
Workflow-Katalog bleiben in diesem Prep-Slice unveraendert.

## Ownergrenzen

- `OutputRequirementProfile` und dessen Katalog verbleiben bei
  `ma_analyse`; sie werden nicht ueber `ma_dimensionierung` exportiert.
- `ma_variants` darf Varianten und dimensionierungsrelevante Anfragen
  bilden, aber keine Lasten berechnen.
- `ma_import_simulation` uebernimmt externe Ergebnisse technisch nur bis
  `standardized`; die spaetere fachliche Annahme fuer Dimensionierungszwecke
  gehoert zu `ma_dimensionierung`.
- UI-Rendering und Workspace-I/O bleiben in `ma_ui`; fachliche Manual-Entry-
  Regeln muessen im physischen Migrationsslice aus der UI herausgeloest
  werden.

## Noch erforderliche fachliche Migration

Vor der Behauptung eines abgeschlossenen Fachowners sind mindestens
erforderlich:

- getrennte Ergebnisvertraege fuer berechnete LoD-1-Naeherungen und manuell
  uebernommene externe IDA-Referenzwerte;
- UI-neutrale Validierung und Payloadbildung der manuellen Referenzwerte;
- historischer Pfad nur noch als identitaetsgleicher Legacy-Reexport;
- spaeterer P016/P017-Slice fuer Auswahl vor Dimensionierung und Entfernung
  fachlicher Kapazitaetsableitungen aus `ma_variants`.

## Aussagegrenzen

Die vorhandene LoD-1-Berechnung ist eine transparente Naeherung. Ihre
Kuehllastgroesse bildet nur interne sensible Gewinne ab und ist weder eine
dynamische noch eine normative Kuehllast. Manuell eingetragene IDA-Werte
sind externe beziehungsweise beobachtete Ergebnisse; ein eingegebener
SHA-256-Wert ist bislang nur Nutzerangabe und kein technisch verifizierter
Dateihash.
