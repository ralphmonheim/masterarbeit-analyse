# Allgemeine Befehle

Diese Befehle gelten moduluebergreifend fuer das lokale Projekt.

## Grundbefehle

Wenn du morgens VS Code neu oeffnest und im Projekt arbeiten willst:

Die erste Zeile setzt für die aktuelle PowerShell-Sitzung die Ausführungsrichtlinie auf RemoteSigned. Damit dürfen Skripte in dieser Sitzung ausgeführt werden, ohne dass du die Windows-Einstellung dauerhaft ändern musst.

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

### Sammelbefehle

Sammelbefehle buendeln mehrere Routinen oder Arbeitsbereiche.

- `aktualisieren und tagesende direkt`
- `aktualisieren`: Projektlage, Planung, Entscheidungen, Changelog,
  Command-Dokumentation, Modulumsetzungsstaende, zentrale
  Streamlit-Statusanzeigen und Versionskonsistenz pruefen; naechste Version
  nur vorschlagen; keine Git-Aktionen und keine Beispieloutputs erzeugen.
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
  technische Entscheidungen pruefen und aktualisieren.
- `projektlage`: kompakte Lage zu Git-Stand, Version, Plaenen und offenen
  Entscheidungen ausgeben.
- `plan aufnehmen`: neue Plaene aus `docs/project/plans/inbox/` in Planindex
  und Planstatus einordnen.
- `entscheidung festhalten`: echte Nutzerentscheidung dokumentieren und
  passende offene Punkte schliessen.
- `release check`: pruefen, ob Version, Changelog, Tags und Tests fuer ein
  Release bereit sind.

### Test-/Referenzbefehle

- `aktualisiere tests`: Beispielbilder, Referenzoutputs und passende Testlaeufe
  gezielt aktualisieren; keine Git-Aktionen ausfuehren.

Details stehen in `docs/project/UPDATE_ROUTINES.md`.

## Klassifikation

- Sammelbefehl: buendelt mehrere Routinen oder Arbeitsbereiche zu einem
  Tages-, Wochen- oder Gesamtupdate.
- Einzelbefehl: hat einen klar abgegrenzten Zweck, zum Beispiel Repo
  aktualisieren, Planung aktualisieren, Entscheidung festhalten oder Release
  pruefen.
- Test-/Referenzbefehl: aktualisiert oder prueft Referenzbilder,
  Beispieloutputs und Tests.
- Referenz/Optionen: Parameterlisten, Pfade, Hinweise oder Template-Tabellen.

## Dokumentationsbereiche

- `docs/ma_analyse/commands_analyse.md`: Analysepipeline, GUI und Plot-Templates.
- `docs/ma_variants/commands_variants.md`: Variantenkern und Varianten-UI.
- `docs/ma_weather/commands_weather.md`: Wettermodul und lokale TRY-Analyse.
- `docs/ma_ui/commands_ui.md`: zentrale Streamlit-Oberflaeche mit Dashboard,
  Modulansichten und Analyse-Wizard.
- `docs/ma_workflow/commands_workflow.md`: interne Workflow-Schicht mit
  zentralem Modulkatalog und Statuswerten, aktuell ohne eigene CLI.
