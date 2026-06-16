# Update-Routinen

Diese Datei beschreibt feste Codex-Arbeitsroutinen fuer Repo-Updates,
Release-Vorbereitung sowie Planungs- und Entscheidungsupdates. Sie ist eine
Dokumentationsroutine, kein Python-CLI-Befehl.

## Einordnung

- Sammelbefehle buendeln mehrere Routinen oder Arbeitsbereiche.
- Einzelbefehle haben ein klar abgegrenztes Ziel, auch wenn intern mehrere
  Pruefschritte laufen.
- Test-/Referenzbefehle aktualisieren oder pruefen Beispielbilder,
  Referenzoutputs und Tests.

## Sammelbefehle

| Ausloesephrase | Ziel | Ergebnis |
| --- | --- | --- |
| `aktualisieren` | Projektsteuerung und Versionslage aktualisieren | Codex prueft Projektlage, Planung, Entscheidungen, Command-Dokumentation, Changelog und Versionskonsistenz; die naechste Version wird vorgeschlagen, aber nicht automatisch geschrieben. |
| `tagesstart` / `Guten Morgen, es ist ein neuer Tag.` | Tagesuebersicht und UI-Start vorbereiten | Codex liest den Projektstand, pflegt bei Bedarf offene Nutzerentscheidungen, startet `ma_ui` bei Bedarf ueber die Projekt-venv und gibt offene Aufgaben nach Modulen aus. |
| `tagesende` / `Gute Nacht.` | Tagesstand dokumentieren und Repo-Update vorbereiten | Codex meldet laufende Projekt-Streamlit-Prozesse, aktualisiert Planstatus, Entscheidungen und Changelog, falls noetig, und gibt Terminal-Code fuer Commit, Tag und Push aus. |
| `tagesende direkt` / `Gute Nacht direkt.` | Tagesstand dokumentieren und Repo direkt aktualisieren | Codex meldet laufende Projekt-Streamlit-Prozesse, aktualisiert Dokumente und fuehrt Commit, Tag und Push aus, sofern keine Blocker bestehen. |
| `wochenabschluss` / `Eine schoene Woche.` | Wochenstand dokumentieren | Codex erstellt eine Wochenzusammenfassung unter `docs/project/weekly_reviews/` und prueft archivierungsfaehige Plaene. |

## Einzelbefehle

| Ausloesephrase | Ziel | Ergebnis |
| --- | --- | --- |
| `update repo` | Versionen, Changelog und Release-Stand vorbereiten | Codex aktualisiert Dateien und gibt Terminal-Code fuer Commit, Tag und Push aus. |
| `direkt update repo` | Repo-Update vollstaendig durch Codex ausfuehren | Codex aktualisiert Dateien und fuehrt Commit, Tag und Push aus, sofern Git-Zugriff moeglich ist. |
| `update planung` | Plan- und Entscheidungsstruktur aktualisieren | Codex prueft Plan-Inbox, Planindex, Planstatus und offene Entscheidungen. |
| `projektlage` | Kurze Projektlage lesen | Codex berichtet Git-Stand, Version, aktive Plaene, offene Entscheidungen und naechste sinnvolle Schritte. |
| `plan aufnehmen` | Neuen Plan einordnen | Codex liest neue Plaene aus der Inbox und aktualisiert Planindex sowie Planstatus. |
| `entscheidung festhalten` | Nutzerentscheidung dokumentieren | Codex dokumentiert echte Nutzerentscheidungen und bereinigt passende offene Punkte. |
| `release check` | Release-Bereitschaft pruefen | Codex prueft Versionen, Changelog, Tags, Tests und offene Aenderungen ohne Release auszufuehren. |

## Test-/Referenzbefehle

| Ausloesephrase | Ziel | Ergebnis |
| --- | --- | --- |
| `aktualisiere tests` | Beispielbilder, Referenzoutputs und passende Testlaeufe aktualisieren | Codex erzeugt nur die benoetigten Referenzen oder Testoutputs und fuehrt keine Git-Aktionen aus. |

## Betroffene Dateien

| Vorgang | Betroffene Dateien | Abschnitt oder Zeilenlogik | Pruefregel |
| --- | --- | --- | --- |
| Version pruefen | `pyproject.toml`, `src/ma_analyse/__init__.py` | `[project] version = "x.y.z"`, `__version__ = "x.y.z"` | Beide Versionen muessen identisch sein. |
| Version aktualisieren | `pyproject.toml`, `src/ma_analyse/__init__.py` | konkrete Versionsnummer aus Nutzerbefehl | Nur schreiben, wenn der Nutzer eine konkrete Version nennt oder ein Repo-Update ausloest. |
| Changelog vorbereiten | `CHANGELOG.md` | `## Unreleased` und Release-Abschnitte | Root-`CHANGELOG.md` bleibt die einzige aktive Aenderungshistorie. |
| Commit-Text pruefen | `docs/common/commit_message.md` | Release-Muster `Release x.y.z - ...` | Commit-Titel folgt dem dokumentierten Muster. |
| Git-Stand pruefen | Git-Arbeitsbaum | `git status --short`, `git diff --stat`, Branch, Tags | Vor Commit muessen alle gewuenschten Aenderungen sichtbar sein. |
| Planung aktualisieren | `docs/project/plans/inbox/`, `PLAN_INDEX.md`, `PLAN_STATUS.md` | neue Plaene, Status, naechster Schritt | Jeder relevante Plan hat genau einen aktiven Eintrag. |
| Nutzerentscheidungen aktualisieren | `docs/project/decisions/USER_DECISIONS_MASTERTHESIS_CODE.md` | echte Nutzerentscheidungen | Keine technischen Empfehlungen eintragen. |
| Offene Entscheidungen aktualisieren | `docs/project/decisions/USER_DECISIONS_OPEN_POINTS.md` | offene Nutzerentscheidungen | Offene Punkte klar von getroffenen Entscheidungen trennen. |
| Technische Entscheidungen aktualisieren | `docs/project/decisions/TECHNICAL_DECISIONS.md` | Architektur- und Umsetzungsentscheidungen | Nicht mit Nutzerentscheidungen vermischen. |
| Command-Dokumentation aktualisieren | `docs/common/commands_common.md`, `docs/*/commands_*.md`, `docs/project/UPDATE_ROUTINES.md` | Sammelbefehle, Einzelbefehle, Test-/Referenzbefehle | Wenn Befehle, Routinen oder Startwege geaendert wurden, muessen die passenden Command-Dateien aktualisiert werden. |
| Referenzen aktualisieren | `docs/examples/`, modulbezogene Beispielordner | Beispielbilder und Referenzoutputs | Nur durch `aktualisiere tests` oder expliziten Nutzerauftrag erzeugen. |

## Routine `aktualisieren`

1. Git-Status, Branch, letzten Commit und letzten Tag lesen.
2. `PLAN_INDEX.md`, `PLAN_STATUS.md` und Plan-Inbox pruefen.
3. Nutzerentscheidungen und offene Punkte pruefen.
4. Command-Dokumentation pruefen:
   - `docs/common/commands_common.md`
   - modulbezogene `docs/*/commands_*.md`
   - `docs/project/UPDATE_ROUTINES.md`
5. Fehlende oder veraltete Command-Eintraege aktualisieren, wenn Befehle, Routinen oder Startwege geaendert wurden.
6. `CHANGELOG.md` unter `Unreleased` aktualisieren, wenn dokumentierte Aenderungen fehlen.
7. Versionskonsistenz zwischen `pyproject.toml` und `src/ma_analyse/__init__.py` pruefen.
8. Naechste sinnvolle Version vorschlagen.
9. Eine konkrete Version nur schreiben, wenn sie im Nutzerbefehl genannt wird, zum Beispiel `aktualisieren 0.9.2`.
10. Keine Git-Aktionen ausfuehren.
11. Keine Beispielbilder, Wetteroutputs oder Plot-Galerien neu erzeugen.

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
9. Projekt-venv und `ma_ui`-Startbefehl pruefen.
10. Wenn Port `8501` frei ist, `ma_ui` ueber die Projekt-venv starten:

    ```powershell
    .\.venv\Scripts\python.exe -m streamlit run src\ma_ui\app.py --server.headless true --server.port 8501
    ```

11. Wenn `http://localhost:8501` bereits durch die Projekt-App erreichbar ist, nicht neu starten und die URL melden.
12. Wenn Port `8501` durch einen unklaren Prozess belegt ist, nicht ueberschreiben und den Konflikt melden.
13. Keine Git-Aktionen ausfuehren.

## Routine `tagesende`

1. Git-Stand und geaenderte Dateien pruefen.
2. Laufende projektbezogene Streamlit-Prozesse pruefen.
3. Wenn `ma_ui` noch laeuft, Prozess und URL melden; nicht automatisch beenden.
4. Falls Arbeiten abgeschlossen wurden, `PLAN_STATUS.md` aktualisieren.
5. Falls Nutzerentscheidungen getroffen wurden, diese dokumentieren und passende offene Punkte schliessen.
6. Falls Code, Struktur oder Dokumentation geaendert wurden, `CHANGELOG.md` unter `Unreleased` aktualisieren.
7. Tests nur bei Code- oder Testaenderungen ausfuehren.
8. Terminal-Code fuer Commit, Tag und Push ausgeben.
9. Keine Git-Aktionen selbst ausfuehren.

## Routine `tagesende direkt`

1. Dieselben Schritte wie `tagesende` ausfuehren.
2. Laufende projektbezogene Streamlit-Prozesse nur melden, nicht automatisch beenden.
3. Bei unklaren, riskanten oder unerwarteten Aenderungen stoppen und Rueckfrage stellen.
4. Wenn der Stand eindeutig ist, Commit, Tag und Push durch Codex ausfuehren.

## Routine `wochenabschluss`

1. Git-Stand, Releases, Tags und Planstatus der Woche pruefen.
2. Erledigte Arbeiten nach Modulen zusammenfassen.
3. Offene Aufgaben, offene Entscheidungen und Risiken dokumentieren.
4. Archivierungsfaehige Plaene benennen und nur nach Freigabe verschieben.
5. Wochenbericht unter `docs/project/weekly_reviews/` als Markdown-Datei ablegen.
6. Naechste Wochenprioritaeten vorschlagen.

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

## Kurze Einzelroutinen

- `projektlage`: liest Projektstand und gibt eine kompakte Lage aus.
- `plan aufnehmen`: ordnet neue Plaene aus `docs/project/plans/inbox/` ein.
- `entscheidung festhalten`: dokumentiert echte Nutzerentscheidungen getrennt von technischen Empfehlungen.
- `release check`: prueft Release-Bereitschaft ohne Commit, Tag oder Push.

## Routine `aktualisiere tests`

1. Klaeren, welche Referenzen betroffen sind, zum Beispiel Plot-Template-Galerie oder spaetere Modul-Beispielordner.
2. Benoetigte Test- oder Beispielbefehle ausfuehren.
3. Nur die dazugehoerigen Referenzoutputs aktualisieren.
4. Keine Git-Aktionen ausfuehren.
5. `CHANGELOG.md` nur aktualisieren, wenn versionierte Referenzdateien oder Dokumentation geaendert werden.

## Versionslogik

- Patch-Version fuer Dokumentation, Bugfixes und kleine Strukturkorrekturen.
- Minor-Version fuer neue Module, groessere Feature-Bloecke oder neue Bedienbereiche.
- Major-Version nur nach ausdruecklicher Nutzerentscheidung.

## Grundregeln

- Kein `docs/CHANGELOG.md` anlegen; der aktive Changelog bleibt im Projekt-Root.
- Tags folgen dem Format `vX.Y.Z`.
- Nutzerentscheidungen und technische Empfehlungen werden getrennt dokumentiert.
- Plaene werden nicht automatisch geloescht.
- `aktualisieren` macht keine Git-Aktionen und erzeugt keine Beispieloutputs.
- `aktualisiere tests` ist fuer Referenzbilder, Beispieloutputs und passende Testlaeufe zustaendig.
- Git-Push wird nur bei `direkt update repo` oder `tagesende direkt` durch Codex ausgefuehrt.
- `tagesstart` darf `USER_DECISIONS_OPEN_POINTS.md` pflegen und `ma_ui` ueber die Projekt-venv starten, fuehrt aber keine Git-Aktionen aus.
- `projektlage` ist eine rein lesende Routine.
- `tagesende` und `tagesende direkt` melden laufende Projekt-Streamlit-Prozesse, beenden sie aber nicht automatisch.
- `tagesende direkt` fuehrt Git-Aktionen nur aus, wenn der Arbeitsstand eindeutig ist.
