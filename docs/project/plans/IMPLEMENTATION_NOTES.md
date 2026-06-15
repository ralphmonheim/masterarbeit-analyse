# Implementation Notes

Diese Regeln gelten fuer spaetere Umsetzungen.

- Vor Umsetzung immer den ausgewaehlten Plan aus `docs/project/plans/inbox/` lesen.
- Vor Umsetzung `PLAN_STATUS.md` und `PLAN_INDEX.md` pruefen.
- Vor fachlichen Entscheidungen `docs/project/decisions/USER_DECISIONS_MASTERTHESIS_CODE.md` und `USER_DECISIONS_OPEN_POINTS.md` pruefen.
- Vor Repo-Updates immer `docs/project/UPDATE_ROUTINES.md` pruefen.
- Vor Planungs- und Entscheidungsupdates immer `PLAN_INDEX.md`, `PLAN_STATUS.md`, `USER_DECISIONS_MASTERTHESIS_CODE.md` und `USER_DECISIONS_OPEN_POINTS.md` pruefen.
- Bei `tagesstart` `USER_DECISIONS_OPEN_POINTS.md` bereinigen oder eindeutig offene Nutzerentscheidungen ergaenzen; allgemeine Aufgaben bleiben in `PLAN_STATUS.md`.
- Bei `tagesstart` `ma_ui` ueber die Projekt-venv vorbereiten und bei freiem Port `8501` automatisch starten; kein globales `streamlit` verwenden.
- Geschlossene Nutzerentscheidungen nicht dauerhaft in `USER_DECISIONS_OPEN_POINTS.md` fuehren, sondern als `UD-*` in `USER_DECISIONS_MASTERTHESIS_CODE.md` dokumentieren.
- Bei `tagesende` Planstatus, Entscheidungen und Changelog nur aktualisieren, wenn sich tatsaechlich etwas geaendert hat.
- Bei `tagesende` und `tagesende direkt` laufende projektbezogene Streamlit-Prozesse nur melden und nicht automatisch beenden.
- Bei `tagesende direkt` vor Commit, Tag und Push stoppen, wenn der Arbeitsstand unklar oder riskant ist.
- Bei `wochenabschluss` eine Wochenzusammenfassung unter `docs/project/weekly_reviews/` erstellen und Plaene nur nach Freigabe archivieren.
- Bestehende Analysefunktionen nicht ungeprueft aendern.
- Bestehende GUI nicht parallel zu Datenpfadmigrationen umbauen.
- Keine grossen Umbauten ohne Begruendung.
- Neue Module klar von bestehenden Modulen trennen.
- Nach jeder Umsetzung geaenderte Dateien dokumentieren.
- `CHANGELOG.md` aktualisieren, wenn Projektstruktur, Code oder Verhalten geaendert wurden.
- Offene Punkte in `PLAN_STATUS.md` festhalten.
- Vor Aufraeumarbeiten zuerst `CLEANUP_PLAN.md` pruefen.
- Keine Dateien loeschen ohne Freigabe.
- Keine Importpfade aendern ohne Tests.
- Bei Unsicherheit erst Struktur pruefen, dann Rueckfrage stellen.
