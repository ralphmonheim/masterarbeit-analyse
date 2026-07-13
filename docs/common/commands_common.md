# Allgemeine Befehle

Diese Befehle gelten moduluebergreifend fuer das lokale Projekt.

## Grundbefehle

Wenn du morgens VS Code neu oeffnest und im Projekt arbeiten willst:

Die erste Zeile setzt für die aktuelle PowerShell-Sitzung die Ausführungsrichtlinie auf RemoteSigned. Damit dürfen Skripte in dieser Sitzung ausgeführt werden, ohne dass du die Windows-Einstellung dauerhaft ändern musst.

```powershell
(Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned) ; (& "c:\Users\ralph\Documents\Master\5.Semester\Masterarbeit - lokal\TEIL1_Fach-Anwendungskompetenz\260524_Masterarbeit_Analyse\.venv\Scripts\Activate.ps1")
```

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

Die zweite Zeile wechselt in den Projektordner. Dort liegen die Dateien des
Repositories, damit die folgenden Befehle im richtigen Kontext laufen.

```powershell
cd "C:\Users\ralph\Documents\Master\5.Semester\Masterarbeit - lokal\TEIL1_Fach-Anwendungskompetenz\260524_Masterarbeit_Analyse"
```

Die dritte Zeile aktiviert die virtuelle Python-Umgebung aus dem Ordner .venv. Dadurch werden beim Arbeiten mit dem Projekt die dort installierten Abhängigkeiten verwendet, statt globale Python-Pakete.

```powershell
.\.venv\Scripts\Activate.ps1
```

PowerShell aktualisieren:

```powershell
winget upgrade Microsoft.Powershell
```

Dieser Befehl aktualisiert die installierte PowerShell-Version ueber winget.

Installation:

```powershell
python -m pip install -e ".[dev]"
```

Allgemeine Pruefung:

```powershell
.\.venv\Scripts\python.exe -m ruff check src tests --no-cache
.\.venv\Scripts\python.exe -m pytest
```

Git-Status:

```powershell
git status --short
git diff --stat
```

## Codex-Kommandos

Diese Ausloesephrasen sind dokumentierte Arbeitsroutinen fuer Codex. Sie sind
keine Python-CLI-Befehle.

### Council-Routinen

Das Projekt-Council arbeitet mit kontrollierter Autonomie. Tera bleibt als
Hauptagent fuer Planung, Integration und Abschluss verantwortlich. Read-only
Council-Mitglieder duerfen bei klar abgegrenzten Analyse- und Pruefaufgaben
automatisch eingesetzt werden. Schreibende Council-Arbeit setzt einen zuvor
freigegebenen Umsetzungsumfang voraus.

Der read-only `compliance_auditor` wird bei erkennbaren Compliance-Risiken
automatisch einbezogen. Dazu gehoeren insbesondere neue Plaene und
Projektinputs, externe Software, Abhaengigkeiten oder Daten, Lizenzen,
Norminhalte, Bilder, Cloud-Verarbeitung, personenbezogene oder vertrauliche
Daten sowie Veroeffentlichung und Weitergabe.

Neue oder geaenderte Rollen unter `.codex/agents/` werden beim Start einer
Codex-Sitzung geladen. Nach einer Rollenaenderung ist deshalb einmalig ein
neuer Codex-Chat oder Projekt-Reload erforderlich.

- `council analyse`: eine read-only Bestandsaufnahme ausfuehren; Tera darf
  Luna fuer gezielte Codesuche und bei fachlich oder technisch kritischen
  Fragen Sol hinzuziehen; keine Dateien veraendern.
- `council review`: einen read-only Sol-Review ausfuehren; der
  `quality_auditor` prueft technische Qualitaet, der `professor` bei Bedarf
  wissenschaftliche Methodik und Reproduzierbarkeit.
- `council compliance`: eine projektweite read-only Compliance-Vorpruefung
  anhand von `docs/compliance/` ausfuehren. Der `compliance_auditor` erteilt
  keine Freigabe; ein belegter Compliance-Blocker stoppt den betroffenen
  Vorgang.
- `council umsetzen`: einen bereits ausdruecklich freigegebenen Plan oder
  Umfang mit Tera umsetzen; der `implementation_engineer` darf klar
  abgegrenzte Datei- oder Modulbereiche uebernehmen. Der Befehl ersetzt keine
  noch fehlende Umsetzungsfreigabe.
- `ohne council` oder `nur Tera`: die aktuelle Aufgabe ohne optionale
  Subagenten im Hauptagenten bearbeiten. Ein verpflichtender
  Compliance-Preflight bleibt aktiv.
- `mit Sol-Review`: fuer die aktuelle Aufgabe nach der Umsetzung einen
  read-only Qualitaetsreview durch Sol einplanen.

Council-Mitglieder erweitern den freigegebenen Umfang nicht selbststaendig.
Mehrere schreibende Agenten duerfen nicht gleichzeitig dieselben Dateien
bearbeiten. Befunde werden als `Blocker`, `Wichtig` oder `Optional`
klassifiziert. Eine blosse Risikoakzeptanz hebt keinen Compliance-Blocker auf,
wenn ein erforderlicher Rechte- oder Freigabenachweis fehlt.

### Sammelbefehle

Sammelbefehle buendeln mehrere Routinen oder Arbeitsbereiche.
Sie gelten als vorab freigegebene Arbeitsroutinen: Wenn der Nutzer einen
Sammelbefehl nennt, fuehrt Codex die dokumentierten Schritte ohne separate
Umsetzungsfreigabe aus. Rueckfragen sind nur bei Blockern, unklaren oder
riskanten Abweichungen und technisch notwendigen Sicherheitsfreigaben noetig.

- `aktualisieren und tagesende direkt`
- `aktualisieren und direkt update repo`
- `aktualisieren`: Projektlage, Planung, Entscheidungen, Changelog,
  Command-Dokumentation, Modulumsetzungsstaende, zentrale
  Streamlit-Statusanzeigen und Versionskonsistenz pruefen; naechste Version
  nur vorschlagen; neue Plaene durchlaufen den Compliance-Preflight; keine
  Git-Aktionen und keine Beispieloutputs erzeugen.
- `tagesstart` oder `Guten Morgen, es ist ein neuer Tag.`: Projektstand lesen,
  offene Nutzerentscheidungen bei Bedarf pflegen und offene Aufgaben nach
  Modulen im Chat ausgeben; `ma_ui` wird nicht automatisch gestartet.
- `tagesende` oder `Gute Nacht.`: Tagesstand dokumentieren, Planstatus und
  Changelog bei Bedarf aktualisieren, laufende Projekt-Streamlit-Prozesse nur
  melden und Terminal-Code fuer Git ausgeben.
- `tagesende direkt` oder `Gute Nacht direkt.`: wie `tagesende`, aber Commit,
  Tag und Push durch Codex ausfuehren, sofern keine Blocker bestehen; laufende
  Projekt-Streamlit-Prozesse werden nur gemeldet.
- `wochenabschluss` oder `Eine schoene Woche.`: Wochenbericht unter
  `docs/project/weekly_reviews/` erstellen und archivierungsfaehige Plaene
  benennen.

### Einzelbefehle

Einzelbefehle haben ein klar abgegrenztes Ziel, auch wenn sie intern mehrere
Pruefschritte enthalten.

- `update repo`: Versionen, Root-`CHANGELOG.md` und Release-Stand vorbereiten;
  Codex gibt danach den Terminal-Code fuer Commit, Tag und Push aus.
- `direkt update repo`: denselben Repo-Update-Ablauf ausfuehren und Commit, Tag
  sowie Push durch Codex erledigen, sofern Git-Zugriff moeglich ist.
- `update planung`: Plan-Inbox, Planindex, Planstatus, Nutzerentscheidungen und
  technische Entscheidungen pruefen und aktualisieren; neue Plaene werden
  zuerst anhand bereinigter Metadaten und erst nach bestandenem
  Dokument-Preflight inhaltlich durch den `compliance_auditor` geprueft.
- `projektlage`: kompakte Lage zu Git-Stand, Version, Plaenen und offenen
  Entscheidungen ausgeben.
- `plan aufnehmen`: neue Plaene aus `docs/project/plans/inbox/` in Planindex
  und Planstatus einordnen. Vor dem Inhaltszugriff wird die Zulaessigkeit des
  Plandokuments anhand bereinigter Metadaten geprueft. Erst danach wird
  getrennt bewertet, ob ein Compliance-Blocker die geplante Umsetzung sperrt.
- `projektinput aufnehmen`: neue Dateien aus der lokalen Entwicklungs-Inbox
  `data/project_inbox/new/` nach den Regeln in
  `docs/project/PROJECT_INPUT_WORKFLOW.md` zunaechst durch den
  `compliance_auditor` pruefen und nur eindeutig zulaessige sowie zuordenbare
  Inhalte in die bestehenden Projekt-, Modul- oder lokalen Datenordner
  verteilen. Ein blockiertes Original bleibt unveraendert an seinem aktuellen
  Eingangspfad; nur Metadatenhinweise oder ausdruecklich freigegebene
  Arbeitskopien gehoeren nach `data/project_inbox/needs_review/`.
- `entscheidung festhalten`: echte Nutzerentscheidung dokumentieren und
  passende offene Punkte schliessen.
- `release check`: pruefen, ob Version, Changelog, Tags und Tests fuer ein
  Release bereit sind. Vor jeder Veroeffentlichung oder Weitergabe muessen
  externe, geschuetzte, personenbezogene oder vertrauliche Inhalte sowie neue
  Abhaengigkeiten durch eine gueltige, den konkreten Stand abdeckende
  `compliance_decision` gedeckt sein.

### Test-/Referenzbefehle

- `aktualisiere tests`: Beispielbilder, Referenzoutputs und passende Testlaeufe
  gezielt aktualisieren; keine Git-Aktionen ausfuehren.

Details stehen in `docs/project/UPDATE_ROUTINES.md`.

## Klassifikation

- Council-Routine: steuert read-only Analyse, Qualitaetsreview oder eine
  bereits freigegebene Umsetzung mit projektlokalen Codex-Subagenten.
- Sammelbefehl: buendelt mehrere Routinen oder Arbeitsbereiche zu einem
  Tages-, Wochen- oder Gesamtupdate.
- Einzelbefehl: hat einen klar abgegrenzten Zweck, zum Beispiel Repo
  aktualisieren, Planung aktualisieren, Entscheidung festhalten oder Release
  pruefen.
- Test-/Referenzbefehl: aktualisiert oder prueft Referenzbilder,
  Beispieloutputs und Tests.
- Referenz/Optionen: Parameterlisten, Pfade, Hinweise oder Template-Tabellen.

## Dokumentationsbereiche

- `docs/project/COMMAND_OUTPUT_INVENTORY.md`: modulweise Uebersicht der
  aufgebauten Befehle, Ausgaben und Frontend-/Backend-Verbindungen.
- `docs/project/PROJECT_INPUT_WORKFLOW.md`: Regeln fuer die lokale
  Entwicklungs-Inbox und die Uebernahme neuer Projektdateien.
- `docs/ma_analyse/commands_analyse.md`: Analysepipeline, GUI und Plot-Templates.
- `docs/ma_variants/commands_variants.md`: Variantenkern und Varianten-UI.
- `docs/ma_weather/commands_weather.md`: Wettermodul und lokale TRY-Analyse.
- `docs/ma_ui/commands_ui.md`: zentrale Streamlit-Oberflaeche mit Dashboard,
  Modulansichten und Analyse-Wizard.
- `docs/ma_workflow/commands_workflow.md`: interne Workflow-Schicht mit
  zentralem Modulkatalog und Statuswerten, aktuell ohne eigene CLI.
