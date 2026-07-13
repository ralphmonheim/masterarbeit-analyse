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

Sammelbefehle gelten als vorab freigegebene Arbeitsroutinen. Wenn der Nutzer
einen Sammelbefehl nennt, fuehrt Codex die dokumentierten Schritte ohne
separate Umsetzungsfreigabe aus. Rueckfragen sind nur bei Blockern, unklaren
oder riskanten Abweichungen und technisch notwendigen Sicherheitsfreigaben
noetig.

| Ausloesephrase | Ziel | Ergebnis |
| --- | --- | --- |
| `aktualisieren` | Projektsteuerung, Modulstatus und Versionslage aktualisieren | Codex prueft Projektlage, Planung, Entscheidungen, Command-Dokumentation, den Umsetzungsstand der Module, Streamlit-Statusanzeigen, Changelog und Versionskonsistenz; neue Plaene durchlaufen den Compliance-Preflight, die naechste Version wird vorgeschlagen, aber nicht automatisch geschrieben. |
| `tagesstart` / `Guten Morgen, es ist ein neuer Tag.` | Tagesuebersicht vorbereiten | Codex liest den Projektstand, pflegt bei Bedarf offene Nutzerentscheidungen und gibt offene Aufgaben nach Modulen aus; `ma_ui` wird nicht automatisch gestartet. |
| `tagesende` / `Gute Nacht.` | Tagesstand dokumentieren und Repo-Update vorbereiten | Codex meldet laufende Projekt-Streamlit-Prozesse, aktualisiert Planstatus, Entscheidungen und Changelog, falls noetig, und gibt Terminal-Code fuer Commit, Tag und Push aus. |
| `tagesende direkt` / `Gute Nacht direkt.` | Tagesstand dokumentieren und Repo direkt aktualisieren | Codex meldet laufende Projekt-Streamlit-Prozesse, aktualisiert Dokumente und fuehrt Commit, Tag und Push aus, sofern keine Blocker bestehen. |
| `wochenabschluss` / `Eine schoene Woche.` | Wochenstand dokumentieren | Codex erstellt eine Wochenzusammenfassung unter `docs/project/weekly_reviews/` und prueft archivierungsfaehige Plaene. |

## Einzelbefehle

| Ausloesephrase | Ziel | Ergebnis |
| --- | --- | --- |
| `update repo` | Versionen, Changelog und Release-Stand vorbereiten | Codex aktualisiert Dateien und prueft vor der beabsichtigten Veroeffentlichung, ob eine gueltige Compliance-Entscheidung den konkreten Stand abdeckt; danach wird Terminal-Code fuer Commit, Tag und Push ausgegeben. |
| `direkt update repo` | Repo-Update vollstaendig durch Codex ausfuehren | Codex aktualisiert Dateien und fuehrt Commit, Tag und Push aus, sofern Git-Zugriff moeglich ist und kein Compliance-Blocker besteht. |
| `update planung` | Plan- und Entscheidungsstruktur aktualisieren | Codex prueft Plan-Inbox, Planindex, Planstatus und offene Entscheidungen; neue Plaene durchlaufen vor der Einordnung den Compliance-Preflight. |
| `projektlage` | Kurze Projektlage lesen | Codex berichtet Git-Stand, Version, aktive Plaene, offene Entscheidungen und naechste sinnvolle Schritte. |
| `plan aufnehmen` | Neuen Plan einordnen | Codex prueft zuerst anhand bereinigter Metadaten, ob das Plandokument gelesen und im Repository verarbeitet werden darf. Erst danach prueft der `compliance_auditor` den Inhalt und trennt Dokumentrisiken von Umsetzungsblockern. |
| `projektinput aufnehmen` | Entwicklungs-Inbox aufraeumen | Codex nutzt `docs/project/PROJECT_INPUT_WORKFLOW.md`, prueft `data/project_inbox/new/` vor jeder Inhaltsverarbeitung auf Compliance und verteilt nur zulaessige sowie eindeutig zuordenbare Inhalte. Blockierte Originale bleiben unveraendert am aktuellen Eingangspfad. |
| `entscheidung festhalten` | Nutzerentscheidung dokumentieren | Codex dokumentiert echte Nutzerentscheidungen und bereinigt passende offene Punkte. |
| `release check` | Release-Bereitschaft pruefen | Codex prueft Versionen, Changelog, Tags, Tests und offene Aenderungen. Bei Veroeffentlichung oder Weitergabe muessen relevante Inhalte und Abhaengigkeiten durch eine gueltige, den konkreten Stand abdeckende Compliance-Entscheidung gedeckt sein. |

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
| Projektinput aufnehmen | `docs/project/PROJECT_INPUT_WORKFLOW.md`, `data/project_inbox/new/`, `data/project_inbox/processed/`, `data/project_inbox/needs_review/` | neue lokale Entwicklungsdateien | Regeln liegen unter `docs/project/`; der Eingang bleibt temporaer und Zielordner bleiben die bestehenden Projekt- und Modulordner. |
| Compliance pruefen | `docs/compliance/`, neue Plaene, Projektinputs, Abhaengigkeiten, externe Daten und Veroeffentlichungsinhalte | Herkunft, Rechte, Schutzbedarf, beabsichtigte Operation, Belege und Entscheidungsreferenz | `green` erlaubt nur den dokumentierten Umfang. `yellow` bleibt bis zur dokumentierten Bestaetigung und allen geforderten Belegen gesperrt. `red` stoppt; `unknown` ist ein gesperrter fehlender-Nachweis-Status und keine Freigabe. |
| Nutzerentscheidungen aktualisieren | `docs/project/decisions/USER_DECISIONS_MASTERTHESIS_CODE.md` | echte Nutzerentscheidungen | Keine technischen Empfehlungen eintragen. |
| Offene Entscheidungen aktualisieren | `docs/project/decisions/USER_DECISIONS_OPEN_POINTS.md` | offene Nutzerentscheidungen | Offene Punkte klar von getroffenen Entscheidungen trennen. |
| Technische Entscheidungen aktualisieren | `docs/project/decisions/TECHNICAL_DECISIONS.md` | Architektur- und Umsetzungsentscheidungen | Nicht mit Nutzerentscheidungen vermischen. |
| Command-Dokumentation aktualisieren | `docs/common/commands_common.md`, `docs/*/commands_*.md`, `docs/project/UPDATE_ROUTINES.md` | Sammelbefehle, Einzelbefehle, Test-/Referenzbefehle | Wenn Befehle, Routinen oder Startwege geaendert wurden, muessen die passenden Command-Dateien aktualisiert werden. |
| Modulstatus pruefen | `src/`, `tests/`, modulbezogene Dokumentation, `src/ma_workflow/catalog.py`, `src/ma_ui/navigation.py` | Fachpakete, Services, Views, Tests und zentrale Statuswerte | Status nur anhand vorhandener Implementierung und belastbarer Tests setzen; Streamlit bezieht Status aus dem Workflow-Katalog. |
| Referenzen aktualisieren | `docs/examples/`, modulbezogene Beispielordner | Beispielbilder und Referenzoutputs | Nur durch `aktualisiere tests` oder expliziten Nutzerauftrag erzeugen. |

## Routine `aktualisieren`

1. Git-Status, Branch, letzten Commit und letzten Tag lesen.
2. `PLAN_INDEX.md`, `PLAN_STATUS.md` und Dateimetadaten der Plan-Inbox
   pruefen; unbekannte Plandokumente noch nicht inhaltlich lesen.
3. Neue, noch nicht eingeordnete Plaene nach der zweistufigen Routine
   `plan aufnehmen` pruefen. Dokumentblocker stoppen den Inhaltszugriff;
   Umsetzungsblocker bleiben in Planindex oder Planstatus sichtbar.
4. Nutzerentscheidungen und offene Punkte pruefen.
5. Command-Dokumentation pruefen:
   - `docs/common/commands_common.md`
   - modulbezogene `docs/*/commands_*.md`
   - `docs/project/UPDATE_ROUTINES.md`
6. Fehlende oder veraltete Command-Eintraege aktualisieren, wenn Befehle,
   Routinen oder Startwege geaendert wurden.
7. Umsetzungsstand aller Workflow-Module pruefen:
   - vorhandene Pakete und zentrale Services unter `src/`
   - nutzbare Modulansichten und Adapter
   - vorhandene Tests und dokumentierte reale Testlaeufe
   - noch ausgelagerte Logik in anderen Modulen
8. Zentrale Statuswerte in `src/ma_workflow/catalog.py` bei nachweisbarer
   Abweichung aktualisieren. `actions.py` bleibt nur
   Kompatibilitaetszugriff. Statusbedeutung:
   - `available`: Fachmodul ist fuer seinen aktuellen Umfang nutzbar und getestet.
   - `partial`: wesentliche Logik existiert, liegt aber noch unvollstaendig oder in einem anderen Modul.
   - `planned`: Zielmodul oder wesentliche Fachlogik fehlt.
   - `manual`: externer oder bewusst manueller Prozessschritt.
9. Pruefen, ob Streamlit-Navigation, Workflow-Karten, Kennzahlen und
   Detailtabellen die zentralen Statuswerte korrekt anzeigen. Keine zweite
   unabhaengige Statusliste pflegen.
10. `CHANGELOG.md` unter `Unreleased` aktualisieren, wenn dokumentierte
    Aenderungen fehlen.
11. Versionskonsistenz zwischen `pyproject.toml` und
    `src/ma_analyse/__init__.py` pruefen.
12. Naechste sinnvolle Version vorschlagen.
13. Eine konkrete Version nur schreiben, wenn sie im Nutzerbefehl genannt
    wird, zum Beispiel `aktualisieren 0.9.2`.
14. Keine Git-Aktionen ausfuehren.
15. Keine Beispielbilder, Wetteroutputs oder Plot-Galerien neu erzeugen.

## Routine `tagesstart`

1. Git-Stand, Branch, letzten Commit und letzten Tag lesen.
2. `CHANGELOG.md` auf offene Eintraege unter `Unreleased` pruefen.
3. `PLAN_INDEX.md` und `PLAN_STATUS.md` lesen.
4. `USER_DECISIONS_OPEN_POINTS.md` bereinigen:
   - geschlossene Punkte entfernen, wenn sie als `UD-*` dokumentiert sind.
   - neue offene Nutzerentscheidungen nur ergaenzen, wenn sie eindeutig sind.
   - allgemeine Aufgaben nicht in diese Datei schreiben.
5. Offene Nutzerentscheidungen im Chat ausgeben.
6. Plan-Inbox nur anhand von Dateinamen und bereinigten Metadaten auf neue
   Plaene pruefen.
7. Bei neuen, noch nicht eingeordneten Plaenen zuerst den Dokument-Preflight
   aus `plan aufnehmen` ausfuehren. Nur bei erlaubter Inhaltsverarbeitung den
   Planinhalt pruefen und Blocker in der Tagesuebersicht nennen; keine Plan-
   oder Inbox-Datei verschieben.
8. Eine kurze Aufgabenliste nach Modulen im Chat ausgeben.
9. Die wichtigsten ein bis drei Tagesprioritaeten empfehlen.
10. `ma_ui` nicht automatisch starten.
11. Bei Bedarf den dokumentierten Startbefehl aus
    `docs/ma_ui/commands_ui.md` nennen.
12. Keine Git-Aktionen ausfuehren.

## Routine `tagesende`

1. Git-Stand und geaenderte Dateien pruefen.
2. Laufende projektbezogene Streamlit-Prozesse pruefen.
3. Wenn `ma_ui` noch laeuft, Prozess und URL melden; nicht automatisch beenden.
4. Falls Arbeiten abgeschlossen wurden, `PLAN_STATUS.md` aktualisieren.
5. Falls Nutzerentscheidungen getroffen wurden, diese dokumentieren und passende offene Punkte schliessen.
6. Falls Code, Struktur oder Dokumentation geaendert wurden, `CHANGELOG.md` unter `Unreleased` aktualisieren.
7. Tests nur bei Code- oder Testaenderungen ausfuehren.
8. Vor der beabsichtigten Veroeffentlichung oder Weitergabe pruefen, ob eine
   gueltige `compliance_decision` den konkreten Stand, relevante externe oder
   geschuetzte Inhalte, personenbezogene oder vertrauliche Daten und neue
   Abhaengigkeiten abdeckt. Fehlende, veraltete oder nicht passende
   Entscheidungen durch den `compliance_auditor` pruefen lassen.
9. Bei einem Compliance-Blocker keinen Release-Befehl fuer den betroffenen
   Stand vorbereiten.
10. Andernfalls Terminal-Code fuer Commit, Tag und Push ausgeben.
11. Keine Git-Aktionen selbst ausfuehren.

## Routine `tagesende direkt`

1. Dieselben Schritte wie `tagesende` ausfuehren.
2. Laufende projektbezogene Streamlit-Prozesse nur melden, nicht automatisch beenden.
3. Bei unklaren, riskanten oder unerwarteten Aenderungen oder einem
   Compliance-Blocker stoppen und Rueckfrage stellen.
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
3. Vor der beabsichtigten Veroeffentlichung oder Weitergabe pruefen, ob eine
   gueltige `compliance_decision` den konkreten Stand, relevante externe oder
   geschuetzte Inhalte, personenbezogene oder vertrauliche Daten und neue
   Abhaengigkeiten abdeckt. Fehlende, veraltete oder nicht passende
   Entscheidungen durch den `compliance_auditor` pruefen lassen und bei einem
   Blocker die Release-Vorbereitung stoppen.
4. `pyproject.toml` und `src/ma_analyse/__init__.py` auf dieselbe Version setzen.
5. `CHANGELOG.md` aktualisieren:
   - `Unreleased` fuer neue offene Aenderungen erhalten oder leeren.
   - neuen Release-Abschnitt mit Datum anlegen.
6. Ruff und Tests ausfuehren, wenn Code oder Tests betroffen sind.
7. Terminal-Code fuer Commit, Tag und Push ausgeben.

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
2. Bei unklaren, riskanten oder unerwarteten Aenderungen oder einem
   Compliance-Blocker stoppen und Rueckfrage stellen.
3. Wenn der Stand eindeutig ist, `git add -A`, Commit, Tag und Push ausfuehren.
4. Ergebnis mit Commit, Tag, Branch und Push-Status melden.

## Routine `update planung`

1. Neue Kandidaten in `docs/project/plans/inbox/` nur anhand von Dateinamen
   und bereinigten Metadaten bestimmen; unbekannte Dokumente noch nicht
   inhaltlich lesen.
2. Neue, noch nicht eingeordnete Plaene vollstaendig nach der Routine
   `plan aufnehmen` pruefen.
3. `PLAN_INDEX.md` pruefen und nur Plandokumente mit zulaessiger
   Inhaltsverarbeitung und Repository-Ablage ergaenzen. Ein Compliance-
   Blocker fuer die geplante Umsetzung bleibt sichtbar, statt den Plan aus
   der Uebersicht zu entfernen.
4. `PLAN_STATUS.md` nach Modulen aktualisieren und Compliance-Voraussetzungen
   als Umsetzungsblocker dokumentieren.
5. Umgesetzte Plaene nur nach Freigabe oder eindeutigem Abschluss nach
   `docs/project/archive/plans/` verschieben.
6. Nutzerentscheidungen in `USER_DECISIONS_MASTERTHESIS_CODE.md` dokumentieren.
7. Offene Entscheidungen in `USER_DECISIONS_OPEN_POINTS.md` festhalten.
8. Technische Entscheidungen getrennt in `TECHNICAL_DECISIONS.md` dokumentieren.
9. `CHANGELOG.md` nur aktualisieren, wenn tatsaechlich Dateien, Struktur, Code
   oder Verhalten geaendert wurden.

## Routine `plan aufnehmen`

1. Neue, noch nicht in `PLAN_INDEX.md` gefuehrte Kandidaten nur anhand von
   Dateiname, Pfad, Groesse, Herkunftsangabe und weiteren bereinigten
   Metadaten bestimmen. Externe oder unbekannte Plaene sollen vor der
   Repository-Aufnahme unter `data/project_inbox/new/docs/` liegen.
2. Fuer jeden Kandidaten zuerst den Dokument-Preflight ausfuehren: Herkunft,
   Recht zur Inhaltsverarbeitung, externen KI-Pruefung und Repository-Ablage
   anhand von Metadaten und Belegreferenzen klaeren. Den Planinhalt in dieser
   Stufe nicht lesen oder an einen Subagenten uebergeben.
3. Bei unbekannter oder gesperrter Dokumentverarbeitung den Kandidaten
   unveraendert am aktuellen Pfad belassen, keinen Inhalt extrahieren und den
   Vorgang zur Klaerung stoppen.
4. Erst nach bestandenem Dokument-Preflight den Planinhalt read-only durch
   den `compliance_auditor` pruefen. Geplante externe Daten,
   Abhaengigkeiten, Automatisierung, Cloud-Verarbeitung und Veroeffentlichung
   bilden eine getrennte Umsetzungspruefung.
5. Den Hauptagenten als Eigentuemer der Prozessentscheidung festhalten. Er
   prueft die Agentenempfehlung und dokumentiert die anwendbare
   `compliance_decision` mit Belegreferenz im passenden Fachregister oder im
   Metadaten-Audit unter `logs/compliance/decisions.jsonl`.
6. Plaene mit zulaessiger Dokumentverarbeitung und Repository-Ablage in
   `PLAN_INDEX.md` und `PLAN_STATUS.md` einordnen. Ein Umsetzungsblocker wird
   dort mit Entscheidungsreferenz als Voraussetzung dokumentiert; der Plan
   bleibt auffindbar und wird nicht geloescht.
7. Materielle oder gelbe Entscheidungen nur nach dokumentierter menschlicher
   Bestaetigung und mit allen geforderten Rechtebelegen fortsetzen. `red` und
   `unknown` bleiben gesperrt.
8. Unabhaengige, unkritische Plaene derselben Aufnahme weiterbearbeiten.

## Routine `projektinput aufnehmen`

1. `docs/project/PROJECT_INPUT_WORKFLOW.md` und `docs/compliance/README.md` als
   zentrale Regelungen lesen.
2. `data/project_inbox/new/` mit den vorsortierten Unterordnern zunaechst auf
   Datei- und Quellenmetadatenebene lesen:
   - `docs/`
   - `weather/`
   - `building/`
   - `analyse/`
   - `variants/`
   - `catalogs/`
   - `parameters/`
   - `zones_technical/`
   - `unknown/`
3. Fuer jedes neue Objekt bereinigte Metadaten, bekannte Herkunft,
   Lizenzangabe, beabsichtigte Operation und vorhandene Belegreferenzen
   zusammenstellen; den Dateiinhalt noch nicht lesen.
4. Den read-only `compliance_auditor` zuerst nur mit diesen bereinigten
   Metadaten pruefen lassen. Er darf in dieser Stufe keinen geschuetzten
   Dateiinhalt erhalten.
5. Bei `unknown`, `red` oder anderweitig gesperrter Inhaltsverarbeitung das
   Original unveraendert am aktuellen Eingangspfad belassen. Nach
   `needs_review/` duerfen nur ein Metadatenhinweis oder eine ausdruecklich
   freigegebene Arbeitskopie gelangen; das Original bleibt erhalten.
6. Erst nach belegter Inhaltsverarbeitung den minimal notwendigen Inhalt fuer
   die konkrete Operation pruefen lassen.
7. Der Hauptagent prueft die Agentenempfehlung und dokumentiert die
   `compliance_decision` mit Belegreferenz im passenden Fachregister oder im
   Metadaten-Audit unter `logs/compliance/decisions.jsonl`.
8. Bei `green` nur den dokumentierten Umfang ausfuehren. `yellow` bleibt bis
   zur dokumentierten menschlichen Bestaetigung und allen geforderten
   Rechtebelegen gesperrt. `red` stoppt; `unknown` bleibt als fehlender-
   Nachweis-Status gesperrt.
9. Dateien nur bei eindeutiger Zuordnung verschieben oder in bestehende
   Dokumente einarbeiten.
10. Projektplaene erst nach bestandenem Dokument-Preflight nach
   `docs/project/plans/inbox/` uebernehmen und danach wie
   bei `plan aufnehmen` in `PLAN_INDEX.md` und `PLAN_STATUS.md` einordnen.
11. Entscheidungsnotizen nach Nutzerentscheidung, offener Nutzerentscheidung
   oder technischer Entscheidung trennen.
12. Wetterdateien nur in lokale Wetterordner wie `data/ma_weather/input/` oder
   `data/ma_weather/geodata/` vorbereiten. Registrierung und Freigabe bleiben
   beim bestehenden Wetter-Scan und Pruefworkflow.
13. Gebaeude-, Analyse-, Varianten-, Katalog-, Parameter-, Zonen- und
   Technikdateien in die bereits dokumentierten Modulordner verteilen.
14. Verarbeitete Originale nach `data/project_inbox/processed/` verschieben.
15. Unabhaengige, unkritische Dateien derselben Aufnahme weiterbearbeiten.
16. Keine Dateien loeschen und keine Fach- oder Compliance-Freigabe
    automatisch setzen.
17. `CHANGELOG.md` nur aktualisieren, wenn versionierte Struktur,
    Dokumentation oder produktive Dateien geaendert wurden.

## Kurze Einzelroutinen

- `projektlage`: liest Projektstand und gibt eine kompakte Lage aus.
- `plan aufnehmen`: prueft zuerst das Plandokument anhand bereinigter
  Metadaten und danach getrennt den Inhalt und die geplante Umsetzung.
- `projektinput aufnehmen`: scannt die lokale Entwicklungs-Inbox und verteilt
  nur zulaessige und eindeutige Inhalte in bestehende Zielordner.
- `entscheidung festhalten`: dokumentiert echte Nutzerentscheidungen getrennt von technischen Empfehlungen.
- `release check`: prueft Release-Bereitschaft und die gueltige
  Compliance-Entscheidung fuer den konkreten Veroeffentlichungsstand, ohne
  Commit, Tag oder Push.

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
- Compliance-Blocker stoppen den betroffenen Vorgang auch innerhalb eines
  vorab freigegebenen Sammelbefehls. Unabhaengige, unkritische Objekte duerfen
  weiterbearbeitet werden.
- `ohne council` und `nur Tera` deaktivieren keinen verpflichtenden
  Compliance-Preflight.
- Der `compliance_auditor` empfiehlt; der Hauptagent besitzt und dokumentiert
  die Prozessentscheidung. Eine gelbe Entscheidung benoetigt die
  dokumentierte menschliche Bestaetigung und alle geforderten Rechtebelege.
- `aktualisieren` macht keine Git-Aktionen und erzeugt keine Beispieloutputs.
- `aktualisiere tests` ist fuer Referenzbilder, Beispieloutputs und passende Testlaeufe zustaendig.
- Git-Push wird nur bei `direkt update repo` oder `tagesende direkt` durch Codex ausgefuehrt.
- `tagesstart` darf `USER_DECISIONS_OPEN_POINTS.md` pflegen, startet aber keine Oberflaeche und fuehrt keine Git-Aktionen aus.
- `projektlage` ist eine rein lesende Routine.
- `tagesende` und `tagesende direkt` melden laufende Projekt-Streamlit-Prozesse, beenden sie aber nicht automatisch.
- `tagesende direkt` fuehrt Git-Aktionen nur aus, wenn der Arbeitsstand eindeutig ist.
