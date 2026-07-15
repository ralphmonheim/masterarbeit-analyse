---
name: repo-release-workflow
description: Fuehre die dokumentierten Repository-, Tagesende- und Release-Routinen dieses Projekts kontrolliert aus. Verwende diesen Skill bei `aktualisieren und tagesende direkt`, `aktualisieren und direkt update repo`, `update repo`, `direkt update repo`, `release check`, `tagesende`, `Gute Nacht.`, `tagesende direkt`, `Gute Nacht direkt.`, `wochenabschluss` und `Eine schoene Woche.`.
---

# Repository-Release-Workflow

1. Lies `docs/project/UPDATE_ROUTINES.md` als einzige Ablaufwahrheit und waehle dort die exakt ausgeloeste Routine.
2. Nutze `docs/common/commands_common.md` nur als Triggerindex. Uebernimm daraus keine abweichende Ablaufregel.
3. Begrenze Bestands- und Inhaltsscans standardmaessig auf `git ls-files`. Lies ignorierte oder unversionierte Arbeitsdaten nur nach einer objektbezogenen Freigabe.
4. Pruefe vor jeder Veroeffentlichung den konkreten Diff gegen `docs/compliance/` und verlange eine passende `compliance_decision` fuer genau diesen Stand.
5. Fuehre Commit, Tag oder Push nur aus, wenn die ausgeloeste Routine dies erlaubt und alle technisch notwendigen Sicherheitsfreigaben vorliegen.
6. Verwende die Projekt-`.venv` fuer Ruff und Pytest. Dokumentiere Version, Tests, Commit, Tag, Remote-Verifikation und ausgeschlossene lokale Daten.
7. Veraendere weder globale Codex-Konfiguration noch MCP, Hooks, externe Dienste oder geschuetzte Daten als Nebeneffekt einer Release-Routine.
