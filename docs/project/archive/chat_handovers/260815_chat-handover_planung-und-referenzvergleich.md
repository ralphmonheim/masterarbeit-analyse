# Chat-Handover – Planung und 29Z-/5Z-Referenzvergleich

Stand: 2026-08-15  
Status: Planungs- und Dokumentationsstand; keine Produkt- oder Datenumsetzung freigegeben.

## Abgeschlossener Arbeitsstand

- Der eingegangene Parametergruppenplan ist als Referenzplan zu P015
  eingeordnet. UD-125 und P015-S5A/S5B bleiben fuer Entscheidungen und
  Umsetzung fuehrend.
- UD-129 haelt PostgreSQL ausschliesslich als Post-V1-Folgeoption fest. V1
  bleibt dateibasiert.
- Ein unabhaengiger Sol-Plan und eine nicht autoritative
  Strukturentscheidungsvorlage bereiten die spaetere gemeinsame Besprechung
  der Handover- und Architekturinputs vor.
- Ein zweiter unabhaengiger Sol-Plan beschreibt einen begrenzten
  29Z-/5Z-Referenzvergleich fuer das Referenzfallkapitel. 5Z bleibt das
  Hauptmodell fuer die Optimierung; 29Z wird kein neuer Hauptstrang.

## Fuehrende Nachweise

- `docs/project/plans/inbox/260622_Plan_P015_ma_parameters_Zentrale_Parameter.md`
- `docs/project/plans/inbox/260715_Plan_P032_Architecture_Benchmark_Migration.md`
- `docs/project/decisions/USER_DECISIONS_MASTERTHESIS_CODE.md` (UD-129)
- `docs/project/plans/independent/260815_Handover_Input_Strukturbaseline_Integration.md`
- `docs/project/architecture/reviews/2026-08-15/HANDOVER_STRUCTURE_DECISION_TEMPLATE.md`
- `docs/project/plans/independent/260815_Kontrollierter_29Z-5Z-Referenzvergleich.md`

## Referenzvergleich – abgestimmte Grenze

- Die fuenf lokalen Ergebnisfaelle bleiben unveraendert unter
  `data/ma_analyse/ida_imports/Vergleich der Referenz/`.
- Verglichen werden Simulationszeit, PRN-Anzahl als Ausgabeumfang,
  Datenvolumen, tatsaechliches Zeitraster und spaeter die fachlich
  vergleichbaren Gebaeudekennwerte.
- `weniger Simulation` bezeichnet den reduzierten Berechnungs- und
  Ausgabeumfang. Der IDA-Wert `0.0` bezeichnet beim Ausgabezeitschritt den
  Standardmodus und nicht ein numerisches Intervall von null Stunden.
- Die vorhandenen Laufzeiten sind Einzelmessungen und damit zunaechst
  explorativ. Kausale Einsparungsaussagen benoetigen kontrollierte
  Wiederholungsmessungen.
- ALT bleibt bis zu einer eigenen `Freigabe zur Umsetzung` an seinem
  bisherigen Ort. Der geplante Umzug nach
  `data/ma_analyse/reference_cases/ALT` wurde nicht ausgefuehrt.

## Offene Arbeit und Gates

- Beide unabhaengigen Plaene benoetigen vor jeder Umsetzung die exakte
  Nutzerformulierung `Freigabe zur Umsetzung`.
- Fuer die Handover-Strukturbaseline stehen die in der
  Entscheidungsvorlage genannten Nutzerentscheidungen weiterhin aus.
- Fuer den Referenzvergleich muessen Ausgabeaufloesung, Einheiten,
  Zeitsemantik, Zonenabdeckung und Systemgrenzen vor quantitativen
  Gebaeudevergleichen bestaetigt werden.
- IDM- und IDC-Inhalte, automatische IDA-Simulation, neue Dependencies,
  externe Verarbeitung und Veroeffentlichung bleiben ausgeschlossen.

## Lokale Daten und Repository-Grenze

Die realen IDA-Ergebnisartefakte und Simulationsmodelle sind lokale,
Git-ignorierte Arbeitsdaten. Sie wurden nicht versioniert, nicht verschoben
und nicht inhaltlich in diesen Handover uebernommen. Der Repository-Stand
enthaelt ausschliesslich Planungs-, Entscheidungs- und Nachweisdokumente.

## Release-Pruefung

- Ruff: bestanden (`All checks passed`).
- Vollstaendige Pytest-Suite: `907 passed` in 270,99 s.
- Der lokale semantische Navigationshub wurde nach der Freigabe aktualisiert
  und anschliessend erfolgreich mit `--validate-only` validiert.
- Der Inhaltsdiff wurde geprueft. `git diff --cached --check` meldet ausschliesslich
  Markdown-Hardbreaks mit zwei Leerzeichen in neu aufgenommenen Plan- und
  Handoverdateien; es wurden keine Code- oder Patchfehler festgestellt.
- Quellversion in `pyproject.toml` und `ma_analyse.__version__`: `0.42.1`.
- Die bestehende `.venv` meldet weiterhin die veraltete installierte
  Paketmetadatenversion `0.20.0`. Die Umgebung wurde ohne eigene
  Installationsfreigabe nicht veraendert; der getestete Import verwendet den
  aktuellen Quellstand `0.42.1`.
