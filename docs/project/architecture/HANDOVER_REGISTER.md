# Handover-Register

Stand: 2026-07-21

Dieses Register uebernimmt die freigegebenen lokalen Handover-Pakete als
nachvollziehbare Arbeitsreferenz. Es verteilt keine Roharchive in das
Repository und ersetzt weder die aktiven Modulplaene noch bestehende
Entscheidungen. Bei Konflikten sind `PLAN_INDEX.md`, `PLAN_STATUS.md` und die
jeweiligen aktiven Plaene fuehrend.

## Quellen und Grenzen

- `ma_variants_handover_aktualisiert_2026-07-12.zip`
- `P015_ma_parameters_konsolidierter_Gesamtplan_2026-07-09.md`
- `ma_technical_Gesamtplan_Handovers_2026-07-13.zip`
- `ma_technical_Handovers_andere_Module_2026-07-13.zip`

Die Originale bleiben unveraendert in `data/project_inbox/processed/`. Nur
ihre inhaltlichen Arbeitsauftraege werden ueber dieses Register an die
zuständigen Modulplaene weitergegeben. Bilder, externe Quellmaterialien und
Archivinhalte werden nicht in das Repository uebernommen.

Die fachlich kompatiblen Anforderungen wurden am 2026-07-21 als datierte
Handover-Ergaenzungen in die unten genannten fuehrenden Plaene eingearbeitet.
Ueberholte, optionale oder nicht freigegebene Vorschlaege bleiben explizit
ausserhalb des aktiven Umsetzungsumfangs.

## Übergabe an Module

| Empfaengermodul | Zustaendiger aktiver Plan | Eingegangene Handover-Quellen | Umgang |
| --- | --- | --- | --- |
| `ma_variants` | P017 | Variantenpaket; Technikpaket | P017-S1 und Folgeslices konkretisiert. |
| `ma_parameters` | P015 | Variantenpaket; P015-Gesamtplan; Technikpaket | Nur offene P015-Slices ergaenzt; der Stand vom 2026-07-09 bleibt nicht kanonisch. |
| `ma_technical` | P014 | Variantenpaket; Technik-Gesamtplan | Parameter-, Regel- und Variantenuebergabe konkretisiert. |
| `ma_building` | P012 | Technikpaket | Geometrie-Ownership und Referenzpruefungen ergaenzt. |
| `ma_zones` | P013 | Technikpaket | Serviceinterface-Zuordnung und v2-Migration ergaenzt. |
| `ma_analyse` | P016, P021 | Variantenpaket; Technikpaket | Dimensionierungsvertrag und Robustheitsbewertung konkretisiert. |
| `ma_simulation_setup` | P018 | Variantenpaket; Technikpaket | Neutraler Run- und Setup-Vertrag konkretisiert. |
| `ma_export_simulation`, `ma_import_simulation` | P009 | Variantenpaket | Spaeterer Adaptervertrag eingeordnet; kein IDA-Slice freigegeben. |
| `ma_rules`, `ma_validation`, `ma_workflow`, `ma_ui`, `ma_feedback`, `ma_core` | P027 | Variantenpaket; Technikpaket | Querschnittsgrenzen und Checkpoints ergaenzt. |
| `ma_database` | P014, P032 | Technikpaket | Spaetere Repository-Migration als nicht freigegebene Architekturfolge festgehalten. |

## Nicht uebernommen

- Die veraltete P015-Fassung vom 2026-07-09 ersetzt nicht den aktiven,
  konsolidierten P015-Plan.
- Vorschlaege fuer automatische Iterationen, erweitertes Sampling, eine
  `SimulationCase`-Ebene oder lernende Regelkataloge sind keine Freigabe zur
  Umsetzung.
- Die in den Technikarchiven enthaltenen Bilder und moegliche externe
  Referenzen bleiben ausserhalb des versionierten Projekts.
