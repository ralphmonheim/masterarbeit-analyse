# Allgemeine Befehle

Diese Datei ist der Triggerindex. Die vollstaendigen Schritte stehen nur in
`docs/project/UPDATE_ROUTINES.md`.

## Codex-Kommandos

Council: `council analyse`, `council review`, `council umsetzen`,
`ohne council`, `nur Tera`, `mit Sol-Review`.

Themenstart: `neues thema`, `neues thema: ...`, `themenwechsel`,
`Prompt abschliessen`.

Sammelbefehle: `input aufnehmen`, `aktualisieren und tagesende direkt`,
`aktualisieren und direkt update repo`, `aktualisieren`, `tagesstart`,
`Guten Morgen, es ist ein neuer Tag.`, `tagesende`, `Gute Nacht.`,
`tagesende direkt`, `Gute Nacht direkt.`, `wochenabschluss`,
`Eine schoene Woche.`.

Einzelbefehle: `update repo`, `direkt update repo`, `update planung`,
`projektlage`, `chat-stats`, `chat-handover`, `plan aufnehmen`,
`projektinput aufnehmen`, `entscheidung festhalten`, `release check`.

Test- und Referenzbefehl: `aktualisiere tests`.

## Allgemeine Pruefung

```powershell
.\.venv\Scripts\python.exe -m ruff check src tests --no-cache
.\.venv\Scripts\python.exe -m pytest
```
