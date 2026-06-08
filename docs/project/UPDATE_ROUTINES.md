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
| `tagesstart` / `Guten Morgen, es ist ein neuer Tag.` | Tagesuebersicht erstellen | Codex liest den Projektstand, pflegt bei Bedarf offene Nutzerentscheidungen und gibt offene Aufgaben nach Modulen aus. |
| `tagesende` / `Gute Nacht.` | Tagesstand dokumentieren und Repo-Update vorbereiten | Codex aktualisiert Planstatus, Entscheidungen und Changelog, falls noetig, und gibt Terminal-Code fuer Commit, Tag und Push aus. |
| `tagesende direkt` / `Gute Nacht direkt.` | Tagesstand dokumentieren und Repo direkt aktualisieren | Codex aktualisiert Dokumente und fuehrt Commit, Tag und Push aus, sofern keine Blocker bestehen. |
| `wochenabschluss` / `Eine schoene Woche.` | Wochenstand dokumentieren | Codex erstellt eine Wochenzusammenfassung unter `docs/project/weekly_reviews/` und prueft archivierungsfaehige Plaene. |
| `projektlage` | Kurze Projektlage lesen | Codex berichtet Git-Stand, Version, aktive Plaene, offene Entscheidungen und naechste sinnvolle Schritte. |
| `plan aufnehmen` | neuen Plan einordnen | Codex liest neue Plaene aus der Inbox und aktualisiert Planindex sowie Planstatus. |
| `entscheidung festhalten` | Nutzerentscheidung dokumentieren | Codex dokumentiert echte Nutzerentscheidungen und bereinigt passende offene Punkte. |
| `release check` | Release-Bereitschaft pruefen | Codex prueft Versionen, Changelog, Tags, Tests und offene Aenderungen ohne Release auszufuehren. |

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
| Tagesstart | `docs/project/plans/PLAN_STATUS.md`, `docs/project/plans/PLAN_INDEX.md`, `docs/project/decisions/USER_DECISIONS_OPEN_POINTS.md` | offene Aufgaben, aktive Plaene, offene Entscheidungen | Offene Entscheidungsdatei bereinigen oder ergaenzen; allgemeine Aufgaben nur berichten. |
| Tagesende | `PLAN_STATUS.md`, Nutzerentscheidungen, `CHANGELOG.md`, Git-Arbeitsbaum | Tagesstand, offene Punkte, Release-/Commit-Vorschlag | Dokumente nur bei tatsaechlicher Aenderung aktualisieren. |
| Wochenabschluss | `docs/project/weekly_reviews/` | Wochenbericht `YYYY-KWxx.md` | Erledigte Arbeiten, offene Punkte und naechste Woche dokumentieren. |

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

## Routine `tagesstart`

1. Git-Stand, Branch, letzten Commit und letzten Tag lesen.
2. `CHANGELOG.md` auf offene Eintraege unter `Unreleased` pruefen.
3. `PLAN_INDEX.md` und `PLAN_STATUS.md` lesen.
4. `USER_DECISIONS_OPEN_POINTS.md` bereinigen:
   - geschlossene Punkte entfernen, wenn sie als `UD-*` dokumentiert sind.
   - neue offene Nutzerentscheidungen nur ergaenzen, wenn sie eindeutig sind.
   - allgemeine Aufgaben nicht in diese Datei schreiben.
5. Offene Nutzerentscheidungen im Chat ausgeben.
6. Plan-Inbox auf neue Plaene pruefen.
7. Eine kurze Aufgabenliste nach Modulen im Chat ausgeben.
8. Die wichtigsten ein bis drei Tagesprioritaeten empfehlen.
9. Keine Git-Aktionen ausfuehren.

## Routine `tagesende`

1. Git-Stand und geaenderte Dateien pruefen.
2. Falls Arbeiten abgeschlossen wurden, `PLAN_STATUS.md` aktualisieren.
3. Falls Nutzerentscheidungen getroffen wurden, diese dokumentieren und passende offene Punkte schliessen.
4. Falls Code, Struktur oder Dokumentation geaendert wurden, `CHANGELOG.md` unter `Unreleased` aktualisieren.
5. Tests nur bei Code- oder Testaenderungen ausfuehren.
6. Terminal-Code fuer Commit, Tag und Push ausgeben.
7. Keine Git-Aktionen selbst ausfuehren.

## Routine `tagesende direkt`

1. Dieselben Schritte wie `tagesende` ausfuehren.
2. Bei unklaren, riskanten oder unerwarteten Aenderungen stoppen und Rueckfrage stellen.
3. Wenn der Stand eindeutig ist, Commit, Tag und Push durch Codex ausfuehren.

## Routine `wochenabschluss`

1. Git-Stand, Releases, Tags und Planstatus der Woche pruefen.
2. Erledigte Arbeiten nach Modulen zusammenfassen.
3. Offene Aufgaben, offene Entscheidungen und Risiken dokumentieren.
4. Archivierungsfaehige Plaene benennen und nur nach Freigabe verschieben.
5. Wochenbericht unter `docs/project/weekly_reviews/` als Markdown-Datei ablegen.
6. Naechste Wochenprioritaeten vorschlagen.

## Kurze Zusatzroutinen

- `projektlage`: liest Projektstand und gibt eine kompakte Lage aus.
- `plan aufnehmen`: ordnet neue Plaene aus `docs/project/plans/inbox/` ein.
- `entscheidung festhalten`: dokumentiert echte Nutzerentscheidungen getrennt von technischen Empfehlungen.
- `release check`: prueft Release-Bereitschaft ohne Commit, Tag oder Push.

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
- `tagesstart` darf `USER_DECISIONS_OPEN_POINTS.md` pflegen, fuehrt aber keine Git-Aktionen aus.
- `projektlage` ist eine rein lesende Routine.
- `tagesende direkt` fuehrt Git-Aktionen nur aus, wenn der Arbeitsstand eindeutig ist.
