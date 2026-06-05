# Update-Routinen

Diese Datei beschreibt feste Codex-Arbeitsroutinen fuer Repo-Updates,
Release-Vorbereitung sowie Planungs- und Entscheidungsupdates. Sie ist eine
Dokumentationsroutine, kein Python-CLI-Befehl.

## Ausloesephrasen

| Ausloesephrase | Ziel | Ergebnis |
| --- | --- | --- |
| `update repo` | Versionen, Changelog und Release-Stand vorbereiten | Codex aktualisiert Dateien und gibt Terminal-Code fuer Commit, Tag und Push aus. |
| `direkt update repo` | Repo-Update vollstaendig durch Codex ausfuehren | Codex aktualisiert Dateien und fuehrt Commit, Tag und Push aus, sofern Git-Zugriff moeglich ist. |
| `update planung` | Plan- und Entscheidungsstruktur aktualisieren | Codex prueft Plan-Inbox, Planindex, Planstatus und offene Entscheidungen. |

## Betroffene Dateien

| Vorgang | Betroffene Dateien | Abschnitt oder Zeilenlogik | Pruefregel |
| --- | --- | --- | --- |
| Version aktualisieren | `pyproject.toml` | `[project] version = "x.y.z"` | Version muss zum Release-Tag passen. |
| Version aktualisieren | `src/ma_analyse/__init__.py` | `__version__ = "x.y.z"` | Muss mit `pyproject.toml` identisch sein. |
| Changelog vorbereiten | `CHANGELOG.md` | `## Unreleased` und neuer Release-Abschnitt | Root-`CHANGELOG.md` bleibt die einzige aktive Aenderungshistorie. |
| Commit-Text pruefen | `docs/common/commit_message.md` | Release-Muster `Release x.y.z - ...` | Commit-Titel folgt dem dokumentierten Muster. |
| Git-Stand pruefen | Git-Arbeitsbaum | `git status --short`, `git diff --stat`, Branch, Tags | Vor Commit muessen alle gewuenschten Aenderungen sichtbar sein. |
| Planung aktualisieren | `docs/project/plans/inbox/` | neue oder noch nicht eingeordnete Plaene | Neue Plaene werden in Index und Status eingeordnet. |
| Planung aktualisieren | `docs/project/plans/PLAN_INDEX.md` | Plan-ID, Titel, Modul, Status, Prioritaet, naechster Schritt | Jeder relevante Plan hat genau einen Eintrag. |
| Planung aktualisieren | `docs/project/plans/PLAN_STATUS.md` | offene, blockierte, teilweise umgesetzte und abgeschlossene Punkte nach Modul | Aktive Steuerung bleibt nach Modulen lesbar. |
| Planung archivieren | `docs/project/plans/archived/` | umgesetzte oder ueberholte Plaene | Nur nach Freigabe oder eindeutig abgeschlossenem Plan verschieben. |
| Nutzerentscheidungen aktualisieren | `docs/project/decisions/USER_DECISIONS_MASTERTHESIS_CODE.md` | echte Nutzerentscheidungen | Keine technischen Empfehlungen eintragen. |
| Offene Entscheidungen aktualisieren | `docs/project/decisions/USER_DECISIONS_OPEN_POINTS.md` | offene Nutzerentscheidungen | Offene Punkte klar von getroffenen Entscheidungen trennen. |
| Technische Entscheidungen aktualisieren | `docs/project/decisions/TECHNICAL_DECISIONS.md` | Architektur- und Umsetzungsentscheidungen | Nicht mit Nutzerentscheidungen vermischen. |

## Routine `update repo`

1. Aktuellen Git-Stand pruefen.
2. Relevante Aenderungen und naechste Version bestimmen.
3. `pyproject.toml` und `src/ma_analyse/__init__.py` auf dieselbe Version setzen.
4. `CHANGELOG.md` aktualisieren:
   - `Unreleased` fuer neue offene Aenderungen erhalten oder leeren.
   - neuen Release-Abschnitt mit Datum anlegen.
5. Ruff und Tests ausfuehren, wenn Code oder Tests betroffen sind.
6. Terminal-Code fuer Commit, Tag und Push ausgeben.

Standard-Code fuer den Nutzer:

```powershell
git status --short
git add -A
git diff --cached --stat
git commit -m "Release x.y.z - Kurzbeschreibung"
git tag -a vx.y.z -m "Release x.y.z - Kurzbeschreibung"
$branch = git branch --show-current
git push origin $branch
git push origin vx.y.z
```

## Routine `direkt update repo`

1. Dieselben Pruefschritte wie bei `update repo` ausfuehren.
2. Bei unklaren, riskanten oder unerwarteten Aenderungen stoppen und Rueckfrage stellen.
3. Wenn der Stand eindeutig ist, `git add -A`, Commit, Tag und Push ausfuehren.
4. Ergebnis mit Commit, Tag, Branch und Push-Status melden.

## Routine `update planung`

1. Neue Plaene in `docs/project/plans/inbox/` lesen.
2. `PLAN_INDEX.md` pruefen und fehlende Plaene ergaenzen.
3. `PLAN_STATUS.md` nach Modulen aktualisieren.
4. Umgesetzte Plaene nur nach Freigabe oder eindeutigem Abschluss nach `archived/` verschieben.
5. Nutzerentscheidungen in `USER_DECISIONS_MASTERTHESIS_CODE.md` dokumentieren.
6. Offene Entscheidungen in `USER_DECISIONS_OPEN_POINTS.md` festhalten.
7. Technische Entscheidungen getrennt in `TECHNICAL_DECISIONS.md` dokumentieren.
8. `CHANGELOG.md` nur aktualisieren, wenn tatsaechlich Dateien, Struktur, Code oder Verhalten geaendert wurden.

## Versionslogik

- Patch-Version fuer Dokumentation, Bugfixes und kleine Strukturkorrekturen.
- Minor-Version fuer neue Module, groessere Feature-Bloecke oder neue Bedienbereiche.
- Major-Version nur nach ausdruecklicher Nutzerentscheidung.

## Grundregeln

- Kein `docs/CHANGELOG.md` anlegen; der aktive Changelog bleibt im Projekt-Root.
- Tags folgen dem Format `vX.Y.Z`.
- Nutzerentscheidungen und technische Empfehlungen werden getrennt dokumentiert.
- Plaene werden nicht automatisch geloescht.
- Git-Push wird nur bei `direkt update repo` durch Codex ausgefuehrt.
