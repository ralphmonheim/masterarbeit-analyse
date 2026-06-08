# Offene Nutzerentscheidungen

Stand: 2026-06-08

## Geschlossene Punkte

### OP-001 Migration ma_analyse Datenpfade

- Thema: Datenstruktur
- Status: geschlossen
- Entscheidung: Harte Migration auf `data/ma_analyse/input`, `data/ma_analyse/database` und `data/ma_analyse/output` am 2026-06-04 umsetzen.
- Auswirkung: Betrifft CLI, GUI, Tests und bestehende Arbeitsablaeufe.
- Dokumentiert als: `UD-007`

### OP-002 Externe Plaene einordnen

- Thema: Planmanagement
- Status: geschlossen
- Entscheidung: Die Plaene P001 `250603_Plan_Variantenmodul_GUI_Logikpruefung.md` und P002 `250603_Plan_Wetterdatenanalyse_TRY_Integration.md` liegen in der Plan-Inbox und sind in `PLAN_INDEX.md` sowie `PLAN_STATUS.md` eingeordnet.
- Auswirkung: P001 bleibt bis zur manuellen UI-Pruefung teilweise umgesetzt; P002 bleibt Entwurf.
- Dokumentiert als: `UD-003`

## Offene Punkte

### OP-003 Chat-Analyse

- Thema: Nutzerentscheidungen
- Status: offen
- Frage: Welche Chat-Exporte gehoeren zur Masterarbeit und welche muessen ausgeschlossen werden?
- Auswirkung: Nur eindeutig masterarbeitsbezogene Chats werden fuer Entscheidungen ausgewertet.

### OP-004 Produkt- und Materialdatenblaetter

- Thema: Katalogdaten
- Status: offen
- Frage: Sollen echte Produkt- und Materialdatenblaetter ins Git-Repo aufgenommen oder ausserhalb des Repos abgelegt und nur referenziert werden?
- Auswirkung: Betrifft `data/catalogs/documents/`, `.gitignore` und spaetere Produkt-/Materialkataloge.

### OP-005 Relative/absolute Cooling-Logik im regulaeren Cooling-Befehl

- Thema: ma_analyse Cooling-Auswertung
- Status: offen
- Frage: Soll die neue Trennung aus den Plot-Templates auch in den normalen Befehl `python -m ma_analyse cooling ...` und die GUI-Auswahl uebernommen werden?
- Auswirkung: Betrifft `src/ma_analyse/analysis/cooling.py`, `src/ma_analyse/app/cli.py` und `src/ma_analyse/gui/app.py`.
