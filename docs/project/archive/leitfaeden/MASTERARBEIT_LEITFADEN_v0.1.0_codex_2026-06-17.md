# Masterarbeit Leitfaden

Stand: 2026-06-17

Diese Datei ist ein zentraler Orientierungsleitfaden fuer das Projekt. Sie
ersetzt keine aktive Steuerdatei. Der operative Projektstand bleibt in
`docs/project/plans/PLAN_STATUS.md`; die Zielarchitektur bleibt in
`docs/project/architecture/TARGET_ARCHITECTURE.md`.

## Zweck der Software

Das Projekt ist eine lokale Python-Software fuer die Masterarbeit. Ziel ist ein
modulares System fuer:

- Variantenplanung und Variantenuebersicht
- Wetterdatenanalyse und TRY-Integration
- Simulationsergebnisanalyse aus IDA ICE
- spaetere Bewertung von Energie, Komfort, TGA-Leistung, Kosten und optional
  Nachhaltigkeit
- eine zentrale lokale Bedienoberflaeche ueber Streamlit

Die Software soll fuer die Masterarbeit nachvollziehbar bleiben und trotzdem
modular genug sein, um spaeter erweitert werden zu koennen.

## Grundregeln

- Fachlogik bleibt in Fachmodulen.
- `ma_ui` ist die zentrale Streamlit-Oberflaeche.
- `ma_workflow` vermittelt zwischen Oberflaeche und Fachmodulen.
- Tkinter bleibt vorerst Legacy-Bestand in `ma_analyse`.
- Tkinter und Streamlit werden nicht technisch vermischt.
- Echte lokale Daten, TRY-Dateien, IDA-Ergebnisdaten und Produktdatenblaetter
  werden nicht als Projektinhalt versioniert.
- Dokumentation, Entscheidungen und offene Punkte werden getrennt gefuehrt.

## Gesamtworkflow

Der Gesamtworkflow ist in vier Hauptbereiche gegliedert.

### Pre-Process

| Reihenfolge | Zielmodul | Aufgabe |
|---|---|---|
| 1 | `ma_parameters` | Parameter, Optionsgruppen und Eingabekataloge |
| 2 | `ma_weather` | Wetterdaten, TRY-Dateien und Randbedingungen |
| 3 | `ma_building` | Gebaeude-, Zonen- und Modellrandbedingungen |
| 4 | `ma_variants` | Varianten bilden, auswaehlen und benennen |
| 5 | `ma_simulation_setup` | Zeitraum, Zeitschritt, Szenario und Run-Metadaten |
| 6 | `ma_export_ida` | IDA-ICE-Uebergabestruktur vorbereiten |

### Simulation

IDA ICE bleibt der externe Simulationsschritt. Python bereitet Daten vor und
wertet Ergebnisse aus. Der automatische Start von IDA ICE ist aktuell nicht
Bestandteil des stabilen Workflows.

### Post-Process

| Reihenfolge | Zielmodul | Aufgabe |
|---|---|---|
| 1 | `ma_import_ida` | IDA-Ergebnisordner erkennen und standardisieren |
| 2 | `ma_analyse` | Simulationsergebnisse analysieren, Diagramme und Reports erzeugen |
| 3 | `ma_assessment` | Wirtschaftlichkeit und spaeter Nachhaltigkeit bewerten |
| 4 | `ma_feedback` | Auffaelligkeiten und Rueckspruenge dokumentieren |

### Feedback

Rueckspruenge aus Post-Process und Bewertung koennen spaeter wieder in
Parameter, Wetterdaten, Gebaeudemodell, Varianten oder Simulation-Setup fuehren.

## Aktuelle Module

| Modul | Status | Rolle |
|---|---|---|
| `ma_analyse` | aktiv | Analyse von IDA-ICE-Ergebnisdaten, CLI, Tkinter-GUI, Plot-Templates |
| `ma_variants` | aktiv | Variantenkern, Datenmodelle, Auswahl, Naming, Export, Kataloge |
| `ma_weather` | teilweise aktiv | TRY-Katalog, Import, Validierung, Kennwerte, Diagramme, Bericht |
| `ma_ui` | teilweise aktiv | Zentrale Streamlit-Oberflaeche mit Startseite und Modulansichten |
| `ma_workflow` | teilweise aktiv | Workflow-Katalog und Adapter zwischen UI und Fachmodulen |
| `ma_assessment` | geplant | Bewertung fuer Economics und Sustainability |
| `ma_parameters` | geplant | Zukuenftiger eigenstaendiger Parameterbereich |
| `ma_simulation_setup` | geplant | Simulationsrandbedingungen und Run-Definition |
| `ma_export_ida` | geplant | IDA-Export als eigener Zielbereich |
| `ma_import_ida` | geplant | IDA-Import als eigener Zielbereich |
| `ma_ui_legacy` | geplant | Spaeterer Ort fuer Tkinter-Legacy, falls ausgelagert |

## Datenstruktur

| Bereich | Zweck |
|---|---|
| `data/ma_analyse/ida_imports/` | lokale IDA-Rohdaten und Ergebnisordner |
| `data/ma_analyse/database/` | aufbereitete Analyse-Datenbankdateien |
| `data/ma_analyse/output/` | regulaere Analyseausgaben |
| `data/ma_weather/input/` | lokale TRY-Eingangsdateien |
| `data/ma_weather/database/` | aufbereitete Wetterdaten |
| `data/ma_weather/output/` | Wetterdiagramme |
| `data/ma_weather/reports/` | Wetterberichte |
| `data/ma_variants/` | Variantenimporte, Exporte und IDA-Uebergaben |
| `data/catalogs/documents/` | Struktur fuer Produkt- und Materialdokumente |
| `data/test_output/` | lokaler Arbeits- und Smoke-Test-Bereich |

Echte Projekt-, Ergebnis- und Katalogdaten werden nicht automatisch versioniert.
Die Ordnerstruktur bleibt reproduzierbar; Inhalte koennen lokal entstehen.

## Dokumentationsstruktur

| Datei oder Ordner | Zweck |
|---|---|
| `docs/project/plans/PLAN_STATUS.md` | aktive Steuerdatei nach Modulen |
| `docs/project/plans/PLAN_INDEX.md` | Uebersicht ueber Plaene |
| `docs/project/decisions/USER_DECISIONS_MASTERTHESIS_CODE.md` | Nutzerentscheidungen |
| `docs/project/decisions/USER_DECISIONS_OPEN_POINTS.md` | offene Nutzerentscheidungen |
| `docs/project/decisions/TECHNICAL_DECISIONS.md` | technische Entscheidungen |
| `docs/project/architecture/TARGET_ARCHITECTURE.md` | Zielarchitektur |
| `docs/project/architecture/UI_MIGRATION_PLAN.md` | UI-Migration, Streamlit und Tkinter |
| `docs/project/UPDATE_ROUTINES.md` | Codex-Routinen und Updateablaeufe |
| `CHANGELOG.md` | tatsaechlich umgesetzte Aenderungen |

## UI-Leitlinie

`ma_ui` ist die Zieloberflaeche. Die Startseite zeigt den grafischen Workflow.
Modulseiten zeigen nur modulbezogene Inhalte.

Aktueller Stand:

- `Start`: grafischer Workflow und technische Detailtabellen im Expander
- `Analyse`: Streamlit-Wizard fuer `ma_analyse`, orientiert an Tkinter-Ablauf
- `Wetterdaten`: Analysebereich oben, Wetterdatensatzuebersicht darunter
- `Varianten`: Uebersicht ueber bestehende `ma_variants`-Services
- `Bewertung`: erste Uebersicht ueber Annahmen
- leere Zielmodule: Titel, Untertitel und blaue Hinweisbox

Tkinter bleibt nutzbar, aber als Legacy-Bestand. Entscheidungen aus Tkinter
werden fachlich ausgewertet und schrittweise in UI-neutrale Logik ueberfuehrt.

## Aktuelle offene Strukturpunkte

- Tkinter-Vorschau soll einen temporaeren Vorschau- oder Cachebereich nutzen,
  damit der regulaere Output-Ordner nicht mit Testdiagrammen gefuellt wird.
- Overlay-Bedienung soll freie Datenreihen aus lokalen Analyse-/Datenbankdaten
  erlauben; feste Additionen wie Temperaturband bleiben eigene Optionen.
- `plot-template-weather` bleibt offen: Wetterdiagramme bleiben vorerst in
  `ma_weather`, ein eigener UI-Befehl kann spaeter geplant werden.
- Cooling-Trennung relativ/absolut bleibt vorerst in Plot-Templates und wird
  spaeter fuer Hauptbefehl und GUI erneut bewertet.
- Normierung wird `ma_analyse`-weit geplant: absolute Werte, flaechenbezogene
  Werte oder beides brauchen spaeter eine konsistente Strategie.
- `ma_workflow` soll spaeter echte Fachservice-Aufrufe koordinieren.
- `ma_assessment` soll vor einer Verschiebung der Wirtschaftlichkeitslogik
  separat geplant werden.

## Arbeitsroutinen

Wichtige Codex-Routinen:

- `aktualisieren`: Projektlage, Planung, Entscheidungen, Changelog,
  Versionen und Command-Dokumentation pruefen.
- `tagesstart`: Projektstand und offene Aufgaben anzeigen.
- `tagesende`: Dokumentation pruefen und Terminal-Code fuer Git vorbereiten.
- `tagesende direkt`: Tagesende plus Commit, Tag und Push durch Codex, wenn
  keine Blocker bestehen.
- `update planung`: Plan-Inbox, Planindex, Planstatus und Entscheidungen
  pruefen.

Details stehen in `docs/project/UPDATE_ROUTINES.md`.

## Nutzung als Leitfaden

Diese Datei ist fuer Orientierung und Kommunikation gedacht. Sie kann als
Grundlage fuer externe Abstimmungen, ChatGPT-Zusammenfassungen oder eigene
Notizen genutzt werden.

Wenn hier neue fachliche Punkte entstehen, werden sie nicht direkt umgesetzt,
sondern in die passenden Dateien ueberfuehrt:

- Aufgaben und Status nach `PLAN_STATUS.md`
- Nutzerentscheidungen nach `USER_DECISIONS_MASTERTHESIS_CODE.md`
- offene Entscheidungen nach `USER_DECISIONS_OPEN_POINTS.md`
- technische Entscheidungen nach `TECHNICAL_DECISIONS.md`
- umgesetzte Aenderungen nach `CHANGELOG.md`
