# Chat-Handover: MVP-V1-Migration bis P017-Gate

Datum: 2026-08-03
Status: uncommitteter Arbeitsstand; keine Git-Aktion ausgefuehrt

Baseline: `main` bei `0636616` (`v0.37.0`). Der Arbeitsbaum enthaelt die
genannten P013/P016/P017-Aenderungen und weitere vorher vorhandene,
uncommittete Dateien; nichts wurde zurueckgesetzt oder geloescht.

## Fuehrende Referenzen

- `docs/project/plans/inbox/Masterarbeit_VSCode_Projektplan_2026-06-21.md`
  (P007) und `docs/project/decisions/USER_DECISIONS_MASTERTHESIS_CODE.md`
  (UD-112) fuer Zielprozess und Ownership.
- P016, P017 und P018 unter `docs/project/plans/inbox/` sowie
  `docs/project/plans/PLAN_STATUS.md` und `PLAN_INDEX.md`.
- `docs/project/decisions/USER_DECISIONS_OPEN_POINTS.md`: OP-008 Kennwerte,
  OP-009 Prozessmessung, OP-017 neutraler Importvertrag, OP-018 Interpretation.

## Erledigter Stand seit Release 0.37.0

- P013: schreibfreie Zonen-Release-Readiness-/Handover-Vorschau ist im
  Arbeitsbaum vorhanden.
- P016-S2a: `ma_dimensionierung` hat einen validierenden LoD-1-Gateway mit
  kanonischen Einheiten, Annahmen, Methoden-/Rundungsmetadaten und
  Eingangs-/Ergebnisfingerprints; die historische Berechnung bleibt
  kompatibel.
- P016-S2b/S2c: berechnete LoD-1- und manuell aus externen IDA-Laeufen
  uebernommene Ergebnisse besitzen getrennte Owner-Vertraege. Die Manual-
  Entry-Fachvalidierung und Legacy-Payloadbildung liegen in
  `ma_dimensionierung`; UI-Rendering und Workspace-I/O bleiben in `ma_ui`.
- P017-S1: fruehe VVER-Auswahl ist als `VverSelectionRecord` vorhanden.
  Sie bindet Kandidatenfingerprints, Studienkontext, Begruendung, Modus/Seed
  und Pre-Dimensioning-Upstream, aber keine VAR-ID.
- P017-UI-Gate: Kandidaten/VVER sind vor Dimensionierung bedienbar. Eine
  aktuelle aktive VVER ist vor der manuellen Referenzdimensionierung und
  finalem Katalog erforderlich. Der Katalog ist auf VVER-Kandidaten begrenzt.
  VVER-Historie wird erhalten; defekte Historie blockiert sichtbar.

## Begriffe und Durchgaengigkeit

- VSP erzeugt Kandidaten. VVER trifft die einzige verbindliche Auswahl vor
  Dimensionierung. VCAT vergibt danach finale `VAR-ID`s. VSEL bildet nur die
  VVER-Auswahl auf diese IDs ab und trifft keine zweite Auswahl. VGEN erzeugt
  Variantenpakete. `CASE` und `SimulationCase` sind verboten.
- LoD-1 ist die vereinfachte interne Referenzberechnung. Manuelle IDA-Werte
  sind externe Simulationsergebnisse, manuell uebertragen und erst bei
  `reviewed` weitergabefaehig.
- Aktuelle VVER: aktiver Record mit passendem Studienkontext, Pre-Dimensioning-
  Upstream und unveraenderten Kandidatenfingerprints. Legacy-Kandidaten ohne
  diesen Fingerprint bleiben sichtbar, muessen fuer neue VVER aber regeneriert
  werden.

## Nachweise

- Vor P017-Gates: vollstaendige Suite `756 passed`.
- P016-S2a: fokussiert `12 passed`, Ruff und `git diff --check` gruen.
- P016-S2b: fokussiert `14 passed`.
- P016-S2c: fokussierte Ergebnis-/UI-Laeufe bestanden.
- P017 VVER-/UI-/Gate-Laeufe: zuletzt `47` fokussierte Tests bestanden;
  weitere VVER-Haertung `12 passed`; `git diff --check` gruen.

Fokustests: `test_ma_dimensionierung_gateway.py`,
`test_ma_dimensionierung_result_contracts.py`,
`test_ma_variants_vver_selection.py` und `test_ma_variants_vver_ui.py`.

## Uebertragene Restarbeit

Die Restarbeit ist im P016- und P017-Plan dokumentiert. Naechster fachlicher
Slice: den historischen SmallOffice-Backendpfad von
`ma_variants.small_office_v1` und
`ma_workflow.small_office_v1_preprocess` auf VVER-ausgewaehlte,
fingerprintgruppierte Dimensionierungsauftraege an `ma_dimensionierung`
migrieren. `ma_variants` darf danach keine Lasten oder Kapazitaeten aus
Referenzwerten mal Faktoren berechnen. Erst danach folgen finaler
VCAT-/VAR-ID- und rein abbildender VSEL-Slice, VGEN und P018.

Start im neuen Chat: `build_small_office_v1_optimization_cases()` und
`_variants_action()` gegen P016/P017 migrieren. Aus VVER-Kandidaten einen
DimensioningRequest mit kanonischem Gruppenfingerprint bilden, nur im Owner
berechnen und `ma_variants` von Last-/Kapazitaetsprodukten befreien.
Akzeptanz: keine Dimensionierung ohne VVER, keine Kapazitaetsrechnung in
`ma_variants`, testbare Gruppierung/Provenienz und keine finalen VAR-IDs vor
VCAT. Legacy-APIs/Payloads nur kompatibel lesen, nicht loeschen.

## Unveraenderte Grenzen

- Keine CASE- oder SimulationCase-Ebene, kein Vorab-VCAT.
- VVER trifft die verbindliche Auswahl vor Dimensionierung; VSEL trifft keine
  zweite Auswahl.
- IDA-Varianten werden manuell simuliert; keine echten IDA-/EQUA-Dateien oder
  geschuetzten Norminhalte verarbeiten.
- P027-Workflowansicht bleibt der letzte UI-Migrationsslice.
- Kein Commit, Push, Tag oder Release wurde ausgefuehrt.
