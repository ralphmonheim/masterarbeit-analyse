---
name: project-governance-workflow
description: Gleiche die kanonische Projektplanung, Entscheidungen und dokumentierten Projektzustaende ab. Verwende diesen Skill bei `aktualisieren`, `tagesstart`, `Guten Morgen, es ist ein neuer Tag.`, `projektlage`, `update planung`, `plan aufnehmen`, `projektinput aufnehmen`, `entscheidung festhalten`, `council analyse`, `council review`, `council compliance`, `council umsetzen`, `ohne council`, `nur Tera`, `mit Sol-Review` und bei Fragen nach der fuehrenden Projektwahrheit oder nach Dokumentduplikaten.
---

# Projektsteuerungs-Workflow

1. Lies `docs/project/plans/PLAN_INDEX.md` und `PLAN_STATUS.md` fuer Planinventar und aktive Arbeitslage.
2. Lies bei Strukturfragen den betroffenen Plan sowie `docs/project/architecture/` und die bestehenden Entscheidungsdateien. Behandle `MASTERARBEIT_LEITFADEN.md` als Orientierung, nicht als zweite Statusquelle.
3. Nutze `docs/project/UPDATE_ROUTINES.md` als einzige Ablaufwahrheit und `docs/common/commands_common.md` nur als Triggerindex.
4. Pruefe neue Plaene oder Projektinputs vor dem Inhaltszugriff nach `docs/compliance/` und `docs/project/PROJECT_INPUT_WORKFLOW.md`. Begrenze allgemeine Scans auf `git ls-files`.
5. Fuehre bei Duplikaten zuerst die betroffenen Wahrheiten und ihre Rollen auf. Entscheide dann fuer genau eine kanonische Quelle; erhalte benoetigte Produktoberflaechen nur als klar markierte Adapter.
6. Dokumentiere echte Nutzerentscheidungen, technische Entscheidungen, offene Punkte und Changelog-Eintraege ausschliesslich in den dafuer bestehenden Dateien.
7. Erteile aus Audit-, Plan- oder Capability-Tabellen keine Freigabe. Globale Konfiguration, Installationen, MCP, Hooks, Graphify, Obsidian/Zotero, externe Verarbeitung und geschuetzte Inhalte bleiben gesondert freizugeben.
