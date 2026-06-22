# Zielarchitektur

Stand: 2026-06-22
Grundlage: P007

## Zweck

Dieses Dokument beschreibt die verbindliche technische Einordnung der
P007-Zielstruktur. Fachliche Detailumsetzungen werden weiterhin ueber
gesonderte Teilplaene analysiert, freigegeben und getestet.

## Architekturregeln

- Phase 0 bildet die technische Plattform; danach folgen sechs fachliche Phasen.
- Fachlogik bleibt UI-neutral und liegt in den Fachmodulen.
- `ma_workflow` ist die zentrale Quelle fuer Phasen, Module und Status.
- `ma_ui` zeigt Fachansichten oder neutrale Modul-Infoseiten.
- Paketexistenz bedeutet nicht automatisch fachliche Verfuegbarkeit.
- Bestehende Logik wird nicht ohne Migrationsplan verschoben.
- IDA ICE bleibt der manuelle externe Simulationsschritt.

## Phase 0 und sechs Hauptphasen

| Phase | Module und Bereiche | Ziel |
|---|---|---|
| Phase 0 | `ma_core`, `ma_database`, `ma_ui`, `ma_workflow`, Dokumentationsinfrastruktur | technische und organisatorische Plattform |
| Phase 1 | `ma_project` | Projekt und Untersuchungsrahmen initialisieren |
| Phase 2 | `ma_building`, `ma_weather`, `ma_zones`, `ma_technical`, `ma_parameters` | Eingaben erfassen, validieren und vereinheitlichen |
| Phase 3 | `ma_analyse.stage_1_dimensioning`, `ma_variants`, `ma_simulation_setup`, `ma_export_simulation` | Referenz dimensionieren, Varianten und Run vorbereiten |
| Phase 4 | IDA ICE, `ma_import_simulation`, `ma_analyse` Stufe 2 bis 4 | simulieren, importieren und technisch analysieren |
| Phase 5 | `ma_economy`, `ma_sustainability`, `ma_assessment` | wirtschaftlich, oekologisch und gesamthaft bewerten |
| Phase 6 | `ma_reporting`, `ma_data_export`, Projektdokumentation | Berichte, Datenpakete und Archivierung |

`ma_validation` und `ma_feedback` wirken phasenuebergreifend.

## Verbindlicher Datenfluss

```text
ma_building
ma_weather
ma_zones
ma_technical
    -> ma_parameters
    -> ma_analyse.stage_1_dimensioning
    -> ma_variants
    -> ma_simulation_setup
    -> ma_export_simulation
       -> adapters.ida_ice
    -> manuelle IDA-ICE-Simulation
    -> ma_import_simulation
       -> adapters.ida_ice
    -> ma_analyse Stufe 2 bis 4
    -> ma_economy
    -> ma_sustainability
    -> ma_assessment
    -> ma_reporting
    -> ma_data_export
    -> Projektdokumentation und Archivierung
```

`ma_parameters` ist die einzige fachliche Eingangsquelle fuer
`ma_variants`. Direkte Abhaengigkeiten von `ma_variants` zu Gebaeude, Wetter,
Zonen oder Technik sind im Zielbild nicht vorgesehen.

## Simulationsschnittstellen

Die kanonischen Hauptmodule sind:

- `ma_export_simulation`
- `ma_import_simulation`

Programmspezifische Logik liegt ausschliesslich unter:

```text
ma_export_simulation/adapters/ida_ice/
ma_import_simulation/adapters/ida_ice/
```

Historische Schluessel `ma_export_ida`, `ma_import_ida`, `export_ida` und
`import_ida` werden voruebergehend als Aliase aufgeloest. Neue Fachlogik darf
diese Namen nicht als neue Hauptmodule verwenden.

Der vorhandene Basisexport unter `ma_variants.ida_export` bleibt bestehen, bis
P009 einen sicheren Schnittstellenvertrag und Migrationsweg definiert.

## UI- und Workflow-Vertrag

- Das Dashboard zeigt Phase 0 bis Phase 6 in dieser Reihenfolge.
- `ma_validation` und `ma_feedback` stehen in einem eigenen
  phasenuebergreifenden Bereich.
- Jedes katalogisierte Modul besitzt eine klickbare Seite.
- Nutzbare Module behalten ihre Fachansicht.
- Geplante Module zeigen Zweck, Ein- und Ausgaben, Abgrenzung,
  Abhaengigkeiten, Status und naechsten Schritt.
- Geplante Seiten enthalten keine funktionslosen Fachbedienelemente.
- Tkinter bleibt Legacy-Oberflaeche von `ma_analyse` und wird nicht technisch
  mit Streamlit vermischt.

## Ergebnisverarbeitung

- `ma_assessment` aggregiert und bewertet Ergebnisse.
- `ma_reporting` erzeugt menschlich lesbare Reports und Factsheets.
- `ma_data_export` erzeugt maschinenlesbare Datenpakete.
- Fachmodulspezifische Exporte bleiben in ihren Fachmodulen.
- Die Projektdokumentation bleibt unter `docs` und ist kein Python-Paket.

## Aktueller Umsetzungsstand

| Status | Module |
|---|---|
| verfuegbar | `ma_analyse`, `ma_variants`, Projektdokumentation |
| teilweise | `ma_core`, `ma_database`, `ma_ui`, `ma_workflow`, `ma_weather`, `ma_parameters`, `ma_export_simulation`, `ma_import_simulation`, `ma_economy`, `ma_reporting`, `ma_data_export`, `ma_validation` |
| geplant | `ma_project`, `ma_building`, `ma_zones`, `ma_technical`, `ma_analyse.stage_1_dimensioning`, `ma_simulation_setup`, `ma_sustainability`, `ma_assessment`, `ma_feedback` |
| manuell | IDA ICE |

Die Statuswerte werden zentral in `ma_workflow` gepflegt und von Navigation
und Dashboard uebernommen.

## Aktive Teilplaene

- P008: Wettermodul abschliessen und `weather_key` an die P007-Grenzen anbinden.
- P009: allgemeine Simulationsschnittstellen und sichere IDA-ICE-Adapter planen.

## Migrationsgrundsaetze

- Leichte Pakete duerfen frueh angelegt werden.
- Fachservices, Modelle und Konfigurationen entstehen erst mit konkretem Bedarf.
- Bestehende Importpfade werden bei Umbenennungen ueber Aliase oder
  Kompatibilitaetswrapper abgesichert.
- Verschiebungen von Fachlogik benoetigen Tests vor und nach der Migration.
- P002, P005 und P006 bleiben als unveraenderte historische Quellen archiviert.
