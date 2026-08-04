# Chat-Handover: konsolidiertes Masterarbeits-MVP bis Slice 8

Datum: 2026-08-03
Status: uncommitteter Arbeitsstand auf `main` seit `0636616` (`v0.37.0`);
keine Git-Aktion ausgefuehrt

## Fuehrende Referenzen

- [P007](../../plans/inbox/Masterarbeit_VSCode_Projektplan_2026-06-21.md),
  [UD-112/UD-117](../../decisions/USER_DECISIONS_MASTERTHESIS_CODE.md) fuer
  Zielprozess, Ownership und Identitaet.
- [P016](../../plans/inbox/260622_Plan_P016_Stage1_Dimensionierung.md),
  [P017](../../plans/inbox/260622_Plan_P017_ma_variants_Naming_Anbindung.md),
  [P018](../../plans/inbox/260622_Plan_P018_ma_simulation_setup_Run_Manifest.md),
  [Planstatus](../../plans/PLAN_STATUS.md) und
  [Planindex](../../plans/PLAN_INDEX.md) fuer den Migrationsstand.

## Erledigter Stand

- P016-S2a bis S2c: LoD-1-Gateway, getrennte Ergebnisvertraege und
  UI-neutrale Manual-IDA-Fachvalidierung unter `ma_dimensionierung`.
- P017-S1 und Slice 5: VVER bindet Kandidaten vor der Dimensionierung;
  SmallOffice gruppiert nur diese Auftraege im Owner. `ma_variants` leitet
  im Optimierungspfad keine Lasten oder Kapazitaeten mehr ab.
- P017-S2: finaler VCAT/VSEL/VGEN-Vertrag, VVER-/Gateway-Provenienz und
  append-only VAR-ID-Registry sind implementiert. Erst finaler VCAT vergibt
  `VAR-000001`; VSEL trifft keine zweite Auswahl.
- Slice 7: OutputRequirementProfile liegt unter `ma_analyse`; der frühere
  Stage-1-Pfad ist nur Kompatibilitaetsadapter.
- Slice 8: `SimulationRunV1`/`RunManifestV1` materialisiert einen RUN mit
  einer finalen VSEL, gemeinsamem Setup und mehreren VAR unter `variants/`.
  Keine CASE-/SimulationCase-Ebene und kein Simulationsstart.

VVER ist die frühe verbindliche Kandidatenauswahl. VCAT vergibt erst nach
Dimensionierung finale VAR-IDs; VSEL ist deren reine Abbildung und VGEN
bindet die IDs an Varianten. RUN bezeichnet das gemeinsame Run-Paket. CASE
und SimulationCase sind im MVP verboten.

## Nachweise

- Slice 5: 50 fokussierte Tests bestanden.
- Slice 6: 56 fokussierte Tests bestanden.
- Slice 7: 13 fokussierte Tests bestanden.
- Slice 8: 30 fokussierte Tests bestanden; Ruff und `git diff --check`
  waren jeweils fehlerfrei. Die Befehle nutzten `.venv\Scripts\python.exe`,
  `PYTHONPATH=src` und die Tests zu Analyse-Outputprofil, Simulation-Setup,
  Finalisierung, SmallOffice, VVER und Gateway.

## Uebertragene Restarbeit

Die konkrete Restarbeit ist in P017 und P018 sowie im `PLAN_STATUS.md`
geführt. Startpunkt: den `ma_variants`-Payload-Adapter beim atomaren
`ma_workspace`-Speichern einsetzen und danach Registry, aktiven VCAT und VSEL
erneut laden/hashprüfen. Akzeptanz: keine doppelte VAR-ID und keine
Teilpersistenz. Danach erhält jeder der Wetter- und Belegungs-StudyCases eine
eigene VVER, Owner-Dimensionierung und finalen VCAT/VSEL/VGEN-Abschluss.
Erst dann migrieren `small_office_v1_preprocess.py` und die direkte
Variantenansicht auf `RunManifestV1`; die Workflowansicht bleibt nach UD-112
der letzte UI-Migrationsslice.

## Grenzen

- Vorab-VCAT/VAR-ID, CASE und SimulationCase sind verboten.
- IDA-/EQUA-Dateiverarbeitung und Simulationsstart liegen ausserhalb des
  freigegebenen Scopes.
- Kein Commit, Push, Tag oder Release.
