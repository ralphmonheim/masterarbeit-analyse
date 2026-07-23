# Chat-Handover – Archivierung einrichten

Datum: 2026-07-22
Status: abgeschlossen
Arbeitsbereich: Projektsteuerung / P031

## Ziel und Anlass

Der Nutzer hat entschieden, dass jede Chat-Uebergabe gespeichert wird. Auch
kleinere Arbeitsstaende sollen dadurch als nachvollziehbarer Projektverlauf
erhalten bleiben und einen spaeteren Kontextwechsel erleichtern.

## Umgesetzter Stand

- `chat-handover` erstellt die kopierfertige Uebergabe und archiviert sie
  anschliessend immer in diesem Verzeichnis.
- `INDEX.md` erschliesst die archivierten Handover nach Datum,
  Arbeitsbereich und fuehrenden Referenzen.
- Jeder Snapshot ist historische Arbeitsreferenz und keine Status-, Freigabe-
  oder Entscheidungsquelle.

## Referenzen

- Aktiver Project-OS-Plan:
  `../../plans/inbox/260715_Plan_P031_Codex_Project_Operating_System.md`
- Aktive Projektlage: `../../plans/PLAN_STATUS.md`
- Planinventar: `../../plans/PLAN_INDEX.md`
- Nutzerentscheidung: `../../decisions/USER_DECISIONS_MASTERTHESIS_CODE.md`
  (UD-100)
- Aenderungshistorie: `../../../CHANGELOG.md`
- Ablaufroutine: `../../UPDATE_ROUTINES.md`

## Feste Grenzen

- Keine geschuetzten, personenbezogenen oder vertraulichen Inhalte in einen
  Handover uebernehmen.
- Keine automatische Git-Aktion oder externe Verarbeitung ausloesen.
- Bei Widerspruechen gelten die referenzierten aktiven Quellen.

## Naechster Schritt

Bei jedem kuenftigen `chat-handover` wird ein weiterer Snapshot archiviert.
