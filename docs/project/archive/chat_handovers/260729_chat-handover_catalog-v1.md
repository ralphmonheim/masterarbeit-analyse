# Chat-Handover – Katalog-V1

Datum: 2026-07-29
Status: aktueller Arbeitsstand
Arbeitsbereich: P012, P034, `ma_building` und Streamlit-Gebaeudeansicht

## Zweck

Dieser historische Snapshot fasst den Katalog-V1-Schnitt zusammen. Er ersetzt
weder `PLAN_STATUS.md`, P034 noch die Nutzerentscheidungen. Bei Widerspruechen
sind diese kanonischen Quellen fuehrend.

## Kopierfertige Uebergabe fuer den naechsten Chat

```text
Arbeite im Repository 260524_Masterarbeit_Analyse nach AGENTS.md und den
projektlokalen Skills. Lies zuerst PLAN_INDEX.md, PLAN_STATUS.md, UD-106 und
UD-109 sowie P034.

Katalog-V1:
- `src/ma_building/catalog_registry.py` liefert eine gemeinsame, lesende
  Sicht auf lokale Excel-Quellen fuer Bauteile, Materialien und Produkte.
- Datensatz-IDs duerfen bei der Zusammenfuehrung nicht kollidieren; es gibt
  kein stilles Ueberschreiben.
- Die Excel- und Herstellerwerte bleiben unveraenderte Inhaltsquellen.
- Die Streamlit-Gebaeudeansicht speichert eigene Werte projektlokal als
  `user_unverified`-Entwuerfe mit ID, Zeitstempel, Herkunft und optionaler
  Quellen-URL. Sie sind nicht simulations-, kosten- oder oekobilanzfreigegeben.
- Fehlende Quellen-URL: Warnung. Fehlende Herkunft: keine fachliche Freigabe.

Noch nicht erledigt:
- Neue Pakete unter `data/project_inbox/new/` nicht verschieben, entpacken
  oder fachlich importieren, bevor je Objekt Quelleninventar, Feldmapping und
  Freigabestatus dokumentiert sind.
- Wetterdaten sind nicht Teil dieser Katalog-V1; sie sollen spaeter denselben
  Herkunfts- und Release-Mechanismus nutzen.

Freigaberegel:
Read-only Analyse und Planung sind erlaubt. Aenderungen an Code,
Konfiguration, Daten oder Dokumentation erst nach der exakten Formulierung
„Freigabe zur Umsetzung“. Commit, Tag und Push bleiben den dokumentierten
Direktbefehlen vorbehalten.
```

## Nachweisstand

- Fokussierte Prüfung nach dem Schnitt: 31 Tests bestanden, einschliesslich
  Excel-Katalog-Regressionen; die betroffenen Python-Dateien wurden kompiliert.
- Der letzte Release-Commit ist `ff1d902` (`v0.35.1`).
- Der Arbeitsbaum war bei Erstellung dieses Handovers bereits mit mehreren
  parallelen, noch nicht committeten Änderungen belegt. Dieser Handover löst
  keine Git-Aktion aus.

## Führende Referenzen

- `../../plans/PLAN_INDEX.md`
- `../../plans/PLAN_STATUS.md`
- `../../decisions/USER_DECISIONS_MASTERTHESIS_CODE.md` (UD-106, UD-109)
- `../../plans/inbox/260622_Plan_P012_ma_building_Gebaeudeinput.md`
- `../../plans/inbox/260724_Plan_P034_Endvarianten_Kataloge_Excel_Aufnahme.md`
- `../../UPDATE_ROUTINES.md`
