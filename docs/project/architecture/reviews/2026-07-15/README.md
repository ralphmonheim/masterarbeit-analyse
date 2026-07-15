# Architecture Benchmark 2026-07-15

Status: Review-Snapshot, nicht autoritativ
Plan: P032

## Zweck und Einordnung

Dieser Ordner dokumentiert den professionellen Architecture Benchmark und den
Migrationsentwurf fuer das Masterarbeitsprojekt. Er ersetzt weder die
verbindliche `docs/project/architecture/TARGET_ARCHITECTURE.md` noch
Entscheidungen, Planstatus oder Compliance-Regeln. Eine Zielarchitektur wird
erst durch eine angenommene ADR verbindlich.

Die im Auftrag vorgeschlagenen Parallelpfade `docs/architecture-review/` und
`docs/decisions/` werden bewusst nicht angelegt. Der Review liegt als datierter
Snapshot in der bestehenden Architekturstruktur; die ADR-Vorlage liegt unter
`docs/project/decisions/`.

## Artefakte

- `CURRENT_STATE_INVENTORY.md`: Bestand, professionelle Benchmarks und
  klassifizierte Probleme.
- `MODULE_BOUNDARY_REVIEW.md`: Verantwortung und Abhaengigkeiten aller
  vorhandenen Python-Pakete.
- `TARGET_ARCHITECTURE_OPTIONS.md`: drei Zielvarianten und gewichteter
  Vergleich.
- `RECOMMENDED_TARGET_ARCHITECTURE.md`: kleinste empfohlene professionelle
  Zielstruktur.
- `MIGRATION_MAPPING.csv`: Pfad- und Verantwortungsmapping ohne Loeschaktion.
- `MIGRATION_RISK_REGISTER.md`: Risiken, Kontrollen und Rollback-Signale.
- `SKEPTICAL_REVIEW.md`: Gegenpruefung auf Overengineering und
  Masterarbeitstauglichkeit.

## Auditgrenze

Analysiert wurden eigene versionierte Repo-Dateien, die explizit benannten
versionierbaren P031-Arbeitsdateien unter `.agents/` und
`tests/test_project_agent_system.py`, Git-Metadaten, nicht sensible lokale
Packaging-Metadaten und oeffentliche Primaerquellen. Kennzahlen unterscheiden
deshalb zwischen versionierter Baseline, aktuellem Working Tree und lokaler
Environment-Beobachtung. Ignorierte Norm-, Literatur-, Katalog-, IDA- und
reale Projektinhalte wurden nicht gelesen. Obsidian wurde mangels
freigegebenem Vault-Pfad nur konzeptionell bewertet. Graphify war lokal nicht
verfuegbar; die Abhaengigkeiten wurden deshalb deterministisch aus Python-
Imports und expliziten Repo-Referenzen abgeleitet.

## Entscheidungsstatus

Empfohlen wird Option 1, eine konservative Konsolidierung des vorhandenen
modularen Monolithen. Paket- oder Datenverschiebungen beginnen erst nach
Annahme der vorgeschlagenen ADR und einer separaten Wellenfreigabe.
