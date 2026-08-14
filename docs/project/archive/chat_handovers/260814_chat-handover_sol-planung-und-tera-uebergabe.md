# Chat-Handover: Sol-Planung und Tera-Uebergabe

Datum: 2026-08-14
Status: Themenroutine erweitert und lokal validiert; kein Commit oder Push
ausgefuehrt.

## Abgeschlossener Stand

- `prompt-intake` fuehrt neue Themen nun durch Q&A zum finalen
  Arbeits-Prompt, danach durch eine getrennte read-only Sol-Planung mit
  Qualitaetspruefung und zuletzt in einen neuen Tera-Umsetzungschat.
- Bei `umsetzungsplan erstellen` erstellt der Sol-Agent auf hoher Stufe
  (`quality_auditor`) einen kleinen, begrenzten Umsetzungsplan. Er aendert
  keine Dateien und prueft Architekturkonflikte, Regressionen, Testluecken,
  Risiken sowie Rechte- und Freigabegrenzen.
- Der koordinierende Agent speichert Sols vollstaendiges Ergebnis unter
  `docs/project/plans/independent/` als
  `YYMMDD_<freier-inhaltlicher-titel>.md`; bei Namensgleichheit folgt der
  erste freie Suffix `-v2`, `-v3` usw. Es gibt keine `P`-Nummer und keine
  automatische Eintragung in `PLAN_INDEX.md`, `PLAN_STATUS.md` oder einen
  bestehenden formellen Plan.
- Jeder unabhaengige Plan speichert den vollstaendigen finalen Arbeits-Prompt
  sowie Ziel, Scope und Nicht-Ziele, betroffene Bereiche,
  Umsetzungsschritte, Pruefungen, Risiken, offene Entscheidungen und die
  `Tera-Uebergabe`. Ein unvollstaendiger Sol-Entwurf wird vor dem Speichern
  read-only vervollstaendigt.
- Der Tera-Chat erhaelt den konkreten Planpfad. Er liest den Plan vollstaendig
  und setzt erst nach `Freigabe zur Umsetzung` ausschliesslich dessen Scope
  um.

## Geaenderte Dateien

- `.agents/skills/prompt-intake/SKILL.md`
- `.agents/skills/prompt-intake/agents/openai.yaml`
- `.agents/skills/README.md`
- `docs/project/UPDATE_ROUTINES.md`
- `docs/common/commands_common.md`
- `docs/project/plans/README.md`
- `docs/project/plans/independent/README.md`
- `CHANGELOG.md`

## Pruefungen

- `.venv\\Scripts\\python.exe C:\\Users\\ralph\\.codex\\skills\\.system\\skill-creator\\scripts\\quick_validate.py .agents/skills/prompt-intake`:
  erfolgreich.
- `git diff --check`: fehlerfrei.
- `py C:\\Users\\ralph\\.codex\\skills\\masterarbeit-navigator\\scripts\\refresh_index.py`
  und anschliessend `--validate-only`: erfolgreich.

## Fuehrende Referenzen

- `docs/project/UPDATE_ROUTINES.md`: verbindlicher Ablauf und
  Freigabegrenzen.
- `.agents/skills/prompt-intake/SKILL.md`: konkrete Q&A-, Sol- und
  Tera-Routine.
- `docs/project/plans/independent/README.md`: Ablage- und
  Einordnungsgrenzen der unabhaengigen Plaene.
- `docs/project/plans/inbox/260715_Plan_P031_Codex_Project_Operating_System.md`:
  Project-OS-Kontext; dieser Handover erzeugt keine neue P031-Restarbeit.

## Anschluss

Es existiert noch kein inhaltlicher unabhaengiger Umsetzungsplan. Beim
naechsten neuen Thema gilt: `neues thema` -> Q&A -> `Prompt abschliessen` ->
`umsetzungsplan erstellen`. Der anschliessende neue Tera-Chat bekommt den
gespeicherten Planpfad mit der dort enthaltenen `Tera-Uebergabe`.

Nach der Umsetzung fragt Tera den Nutzer explizit nach der Einordnung: einen
benannten bestehenden formellen Plan aktualisieren, ueber `plan aufnehmen`
einen neuen `P`-Plan erstellen oder den Einzelplan unveraendert als
abgeschlossen belassen. Andere aktuell uncommittete Worktree-Aenderungen sind
nicht Teil dieses Handovers und wurden weder beschrieben noch veraendert.
