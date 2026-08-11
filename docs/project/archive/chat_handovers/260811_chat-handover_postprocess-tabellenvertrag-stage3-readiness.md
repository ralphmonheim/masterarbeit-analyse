# Chat-Handover: PostProcess-Tabellenvertrag und Stage-3-Nachweisbereitschaft

Datum: 2026-08-11
Status: uncommitteter Arbeitsbaum auf `main` nach `73cbd07` (`v0.38.0`,
2026-08-04); kein neuer Commit, Tag oder Push ausgefuehrt

## Kontext und Begriffe

Dieser Snapshot beschreibt den PostProcess-Slice der Analyseausgabe. Die
Analyse-Stufen sind: Stage 1 = Dimensionierung (`ma_dimensionierung`), Stage 2
= Optimierung bzw. vorhandene Analyseergebnisse (`ma_analyse`), Stage 3 =
Norm-/Nachweispruefung und Stage 4 = Sensitivitaet. Ein `Owner` ist das Modul,
das den fachlichen Vertrag und seine Berechnung verantwortet; eine
Owner-Migrationsgrenze trennt diesen Vertrag von noch historischen oder
UI-seitigen Adaptern.

`W` bezeichnet Leistung in Watt, `W/m2` flaechenbezogene Leistung in Watt pro
Quadratmeter. Die prepared-`time`-Achse ist die aufbereitete Zeitreihe der
Analyse und belegt Auswertungsstunden, nicht Nutzungsstunden. Die 156er
SmallOffice-Teststudie ist ein getrennter Variantenraum mit 156 Varianten;
der bestehende SmallOffice-V1-Referenzraum mit 30 Varianten bleibt unveraendert.
Der PRN-Analyseadapter waere ein Importpfad fuer lokale PRN-Wetterdateien und
bleibt gesperrt.

## Fuehrende Referenzen

- [Planstatus](../../plans/PLAN_STATUS.md) und
  [Planindex](../../plans/PLAN_INDEX.md) fuer den aktuellen Gesamtstand.
- [P019 – Analyse Stufe 2 Optimierung](../../plans/inbox/260622_Plan_P019_Stage2_Optimierung.md),
  [P020 – Analyse Stufe 3 Norm-Nachweis](../../plans/inbox/260622_Plan_P020_Stage3_Standards_Verification.md)
  und [P029 – ma_analyse Service- und Runner-Bereinigung](../../plans/inbox/260627_Plan_P029_ma_analyse_Service_Runner_Bereinigung.md)
  fuer die PostProcess-Arbeit.
- [P008 – ma_weather Gesamtplan](../../plans/inbox/260623_Plan_P008_ma_weather_Gesamtplan.md)
  und [P033 – Wetterdaten TRY 2010/2035](../../plans/inbox/260724_Plan_P033_Wetterdaten_TRY_2010_2035_Aufnahme.md)
  fuer Wetterdaten und den gesperrten PRN-Pfad.
- [UD-119 bis UD-121](../../decisions/USER_DECISIONS_MASTERTHESIS_CODE.md)
  sowie [OP-008, OP-009, OP-017 und OP-018](../../decisions/USER_DECISIONS_OPEN_POINTS.md)
  fuer Entscheidungen und offene Nutzerfragen.

## Erledigter und dokumentierter Stand

- UD-119 trennt Projektbilder unter `gallery/` von erzeugten Diagrammen unter
  `diagrams/`.
- UD-120 ordnete lokale Projektinputs anhand einer freigegebenen Zielmatrix:
  Sechs private Dateien wurden ohne Inhaltspruefung aus dem Projektbereich in
  den persoenlichen Downloadordner verschoben, nicht geloescht. 161 Dateien
  wurden lokal und hashgeprueft ihren fachlichen Zielbereichen zugeordnet.
  Der Nachweis liegt unter
  `data/project_inbox/processed/2026-08-11_project_inputs/ROUTING_MANIFEST.md`.
  90 Wetterkatalogreferenzen zeigen nun auf
  `data/ma_weather/input/prn/`; die IDM-Datei liegt unter
  `data/ma_weather/input/idm/`. Die Originaldateien bleiben unversioniert.
- UD-121 und P029-S12 führen `AnalysisTableBundle` als gemeinsamen
  Tabellenvertrag für `analyze-data`, Streamlit und Excel ein. `metrics_v2`
  ist das neue Schema; `metrics` bleibt ein Legacy-Adapter. W oder W/m2 werden
  nur nach bewusster Quelleneinheitenangabe und, für Ableitungen, positiver
  Netto-Raumfläche ausgegeben. Andernfalls bleiben nur einheitenoffene
  Aggregationskennwerte sichtbar. Bei Kühlung bleiben algebraisches Minimum,
  algebraisches Maximum und maximaler Betrag getrennt.
- P029-S11/P019 ordnen die Streamlit-Analyse in `Auswahl & Lauf` und vier
  Stufen. Nur Stage 2 kann ein vorhandenes `AnalysisResult` mit Diagrammen,
  Dateien, Warnungen und Fehlern anzeigen. Stage 1 verweist auf den Owner
  `ma_dimensionierung`; Stage 3 und 4 zeigen den klaren Status
  `NOT_EVALUABLE`, weil jeweils der Ergebnisvertrag beziehungsweise
  Fachkriterien fehlen. Projekt-Workspaces verwenden standardmaessig
  `output/ma_analyse/`; Ergebnisse sind an die Projekt-ID gebunden.
- P020 führt eine rein wertfreie Readiness-Matrix ein. Sie beschreibt Daten-,
  Rechte-, Methoden- und Teststatus, aktiviert jedoch keine Normformel,
  keinen Grenzwert und keine PASS/FAIL-Regel.
- Simulation-Setup-Ausgaben werden lokal nach Teststudien unter
  `data/test_output/<Projekt-ID>/` und regulären Studien unter
  `data/project_output/<Projekt-ID>/` getrennt. `run_summary.yaml` sowie
  `timings.yaml`/`timings.csv` dokumentieren technische Paket- und
  Materialisierungszeiten; manuelle Bearbeitungs- und IDA-Laufzeit sind nicht
  enthalten.

## Gefuehrte Folgearbeit

Die folgende Arbeit steht nicht in diesem Snapshot als eigene Aufgabenliste,
sondern ausschliesslich in den verlinkten Quellen:

- P029 (`ma_analyse`): Import-/PostProcess-Vertrag und physische
  Owner-Migrationsgrenze weiter planen. Abnahmekriterium: ein klarer,
  UI-unabhaengiger Vertrag ohne neue Direktkopplung an historische Runner.
- P019 (`ma_analyse.stage_2_optimization`): neutralen Import- und
  Kennwertvertrag an Varianten-, Raum- und Run-Referenzen binden.
  Abnahmekriterium: jedes Stage-2-Ergebnis ist diesen Referenzen eindeutig
  zugeordnet.
- P020 (`ma_analyse.stage_3_standards_verification`): erst nach Rechte-,
  Methoden- und Fachtestgate ein konkretes Nachweisprofil festlegen.
  Abnahmekriterium: dokumentiertes Dokument, zulässige Datenbasis,
  begrenzter Regeltext und reproduzierbarer Test; bis dahin bleibt
  `NOT_EVALUABLE` verbindlich.
- P008/P033 (`ma_weather`): PRN-Analyseadapter gesperrt lassen und reale
  lokale Datensaetze/Diagramme nur in einem getrennt freigegebenen Slice
  pruefen. Abnahmekriterium: freigegebener Importvertrag und dokumentierter
  lokaler Testnachweis.
- OP-008, OP-009, OP-017 und OP-018 sind Nutzerentscheidungen. Vor weiteren
  Fachslices sind jeweils Quelleneinheiten-/Zeitachsenvertrag,
  Vergleichsprotokoll, neutrales Dateninventar sowie Funktionskriterien und
  Bewertungszeitraum zu entscheiden. Die Entscheidungshoheit liegt beim
  Nutzer; individuelle Bearbeiter oder Termine sind nicht dokumentiert.

## Validierungs- und Sicherheitsstatus

- Der Arbeitsbaum enthält uncommittete Code-, Test- und Dokumentationsänderungen
  in `ma_analyse`, `ma_simulation_setup`, `ma_variants`, der Streamlit-UI und
  den zugehörigen Planungsquellen. Für diesen gesamten Stand liegt in diesem
  Handover kein neuer Ruff- oder Pytest-Nachweis vor; vor einem Release sind
  `.venv\Scripts\python.exe -m ruff check src tests --no-cache` und
  `.venv\Scripts\python.exe -m pytest` auszuführen.
- Geschützte Originaldaten, Normvolltexte, IDA-/EQUA-Dateien und Inhalte der
  Arbeitsablage sind nicht Teil dieses Snapshots. UD-120 dokumentiert nur die
  zulässige lokale Zuordnung und Hashprüfung, nicht die Inhalte dieser Dateien.
- Dieser Handover ist ein historischer Kontext-Snapshot. Die oben verlinkten
  Pläne und Entscheidungsdateien bleiben die alleinigen Quellen für offene
  Arbeit und Entscheidungen.
