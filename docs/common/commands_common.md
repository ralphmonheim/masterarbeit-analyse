# Allgemeine Befehle

Diese Befehle gelten moduluebergreifend fuer das lokale Projekt.

## Projekt starten

```powershell
cd "C:\Users\ralph\Documents\Master\5.Semester\Masterarbeit - lokal\TEIL1_Fach-Anwendungskompetenz\260524_Masterarbeit_Analyse"
.\.venv\Scripts\Activate.ps1
```

## Installation

```powershell
python -m pip install -e ".[dev]"
```

## Pruefung

```powershell
.\.venv\Scripts\python.exe -m ruff check src tests --no-cache
.\.venv\Scripts\python.exe -m pytest
```

## Git-Status

```powershell
git status --short
git diff --stat
```

## Codex-Kommandos

Diese Ausloesephrasen sind dokumentierte Arbeitsroutinen fuer Codex. Sie sind
keine Python-CLI-Befehle.

- `tagesstart` oder `Guten Morgen, es ist ein neuer Tag.`: Projektstand lesen,
  offene Nutzerentscheidungen bei Bedarf pflegen, `ma_ui` ueber die
  Projekt-venv starten, falls es noch nicht laeuft, und offene Aufgaben nach
  Modulen im Chat ausgeben.
- `tagesende` oder `Gute Nacht.`: Tagesstand dokumentieren, Planstatus und
  Changelog bei Bedarf aktualisieren, laufende Projekt-Streamlit-Prozesse nur
  melden und Terminal-Code fuer Git ausgeben.
- `tagesende direkt` oder `Gute Nacht direkt.`: wie `tagesende`, aber Commit,
  Tag und Push durch Codex ausfuehren, sofern keine Blocker bestehen; laufende
  Projekt-Streamlit-Prozesse werden nur gemeldet.
- `wochenabschluss` oder `Eine schoene Woche.`: Wochenbericht unter
  `docs/project/weekly_reviews/` erstellen und archivierungsfaehige Plaene
  benennen.

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

Details stehen in `docs/project/UPDATE_ROUTINES.md`.

## Dokumentationsbereiche

- `docs/ma_analyse/commands_analyse.md`: Analysepipeline, GUI und Plot-Templates.
- `docs/ma_variants/commands_variants.md`: Variantenkern und Varianten-UI.
- `docs/ma_weather/commands_weather.md`: Wettermodul und lokale TRY-Analyse.
- `docs/ma_ui/commands_ui.md`: zentrale Streamlit-Oberflaeche, aktuell als minimale Shell.
- `docs/ma_workflow/commands_workflow.md`: interne Workflow-Schicht, aktuell ohne eigene CLI.
