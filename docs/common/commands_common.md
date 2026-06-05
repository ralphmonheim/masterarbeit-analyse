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

- `update repo`: Versionen, Root-`CHANGELOG.md` und Release-Stand vorbereiten;
  Codex gibt danach den Terminal-Code fuer Commit, Tag und Push aus.
- `direkt update repo`: denselben Repo-Update-Ablauf ausfuehren und Commit, Tag
  sowie Push durch Codex erledigen, sofern Git-Zugriff moeglich ist.
- `update planung`: Plan-Inbox, Planindex, Planstatus, Nutzerentscheidungen und
  technische Entscheidungen pruefen und aktualisieren.

Details stehen in `docs/project/UPDATE_ROUTINES.md`.

## Dokumentationsbereiche

- `docs/ma_analyse/commands_analyse.md`: Analysepipeline, GUI und Plot-Templates.
- `docs/ma_variants/commands_variants.md`: Variantenkern und Varianten-UI.
- `docs/ma_weather/commands_weather.md`: Wettermodul, aktuell vorbereitet.
