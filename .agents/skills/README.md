# Projektlokale Codex-Skills

Dieser Ordner enthaelt duenne Workflow-Router fuer wiederkehrende
Projektaufgaben. Die Skills duplizieren keine Prozessbeschreibung:
`docs/project/UPDATE_ROUTINES.md` bleibt die einzige Ablaufwahrheit.

## Verfuegbare Skills

- `repo-release-workflow`: Repo-, Release-, Tagesende- und
  Wochenabschlussroutinen mit Compliance- und Remote-Pruefung.
- `project-governance-workflow`: Plan-, Entscheidungs-, Projektlage- und
  Duplikatabgleich entlang der kanonischen Projektdokumentation.

## Regeln

- Allgemeine Scans standardmaessig auf `git ls-files` begrenzen.
- Ignorierte oder unversionierte Arbeitsdaten nicht als implizit freigegeben
  behandeln.
- Globale Konfiguration, Installationen, MCP, Hooks, externe Dienste und
  geschuetzte Inhalte nicht aus einem Skill heraus aktivieren.
- Nach Aenderungen beide Skill-Verzeichnisse mit dem offiziellen
  `quick_validate.py` aus der lokalen Codex-`skill-creator`-Installation
  pruefen.
- Neue oder geaenderte Skills werden erst nach einem neuen Codex-Chat oder
  Projekt-Reload sicher erkannt.

