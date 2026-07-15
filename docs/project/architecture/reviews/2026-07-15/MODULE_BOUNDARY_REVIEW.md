# Module Boundary Review

Stand: 2026-07-15
Status: Review-Snapshot, nicht autoritativ

## Methode

Die Abhaengigkeiten wurden aus den versionierten Python-Imports ermittelt.
Imports unter `TYPE_CHECKING` werden als Typkopplung, nicht als Laufzeitkante
bewertet. Das vorhandene Projekt ist eine Distribution mit 22 Importpaketen
und damit bereits ein modularer Monolith.

Die wichtigste Sollrichtung bleibt:

```text
core + validation
  -> project/weather/building/technical/zones
  -> parameters
  -> analyse.stage_1 + variants
  -> simulation_setup
  -> export adapter -> manual simulation -> import adapter
  -> analyse.stage_2..4
  -> economy/sustainability/assessment/reporting/data_export

ui + workflow compose the packages; domain packages never import ui.
```

`ma_zone` existiert nicht; der etablierte Name ist `ma_zones`. `ma_rules` ist
ebenfalls kein vorhandenes Paket. Ein neues Regelpaket ist erst sinnvoll, wenn
Regeln ausserhalb von `ma_analyse.stage_3_standards_compliance` tatsaechlich
wiederverwendet werden.

## Querschnittsbefunde

- Echte Laufzeitzyklus-SCC: `ma_parameters <-> ma_variants`.
- Richtungsverletzung: `ma_technical.validation` importiert
  `ZoneModelSpecification`, obwohl Technik vor Zonen aufgebaut wird.
- `ma_ui` und `ma_workflow` duerfen als Composition Layer mehrere Fachpakete
  kennen; diese hohe Auswaertskopplung ist nicht automatisch ein Domainfehler.
- `ma_variants` besitzt historisch noch Verantwortungen der Zielpakete
  Parameters, Economy, Simulation Import/Export und Reporting.
- Die sieben weitgehend leeren Zielpakete sind Roadmap-Marker, keine
  eigenstaendigen Services. Sie erhalten erst bei konkreter MVP-Arbeit weitere
  Dateien.

## Modulreview

```yaml
module: ma_core
current_responsibilities:
  - Konfigurations-I/O und Hashing
  - InputSource- und Zeit-/Sitzungsmetadaten
  - technische Compliance-Preflights
recommended_responsibilities:
  - fachneutrale Infrastrukturvertraege
  - zentraler WorkspacePaths-Vertrag fuer config, data und logs
should_keep: true
should_move_out: []
should_move_in:
  - verstreute Projektroot- und Standardpfadauflösung
dependencies: []
boundary_problems:
  - Gefahr eines allgemeinen Sammelpakets bei ungeprueften Hilfsfunktionen
recommended_action: keep_and_harden
confidence: high
```

```yaml
module: ma_validation
current_responsibilities:
  - Diagnosen, Schweregrade und ImportDiagnostic
  - fachliche ReleaseDecision und ValidationResult
recommended_responsibilities:
  - ausschliesslich fachneutrale Ergebnis- und Diagnosevertraege
should_keep: true
should_move_out: []
should_move_in: []
dependencies: [ma_core]
boundary_problems:
  - darf keine domänenspezifische Integrationslogik aufnehmen
recommended_action: keep
confidence: high
```

```yaml
module: ma_database
current_responsibilities:
  - kleiner Demo-Katalogloader und Auswahl
recommended_responsibilities:
  - neutrale Katalogzugriffe erst nach stabilen Abfragen
should_keep: true
should_move_out: []
should_move_in:
  - nur spaeter belegte querschnittliche Katalogpersistenz
dependencies: [ma_core]
boundary_problems:
  - Name verspricht mehr als der aktuelle Demo-Scope
recommended_action: keep_small
confidence: medium
```

```yaml
module: ma_project
current_responsibilities:
  - Projektkonfiguration
  - Simulationsprogrammliste und Varianten-Namingprofil
recommended_responsibilities:
  - Projektidentitaet, Untersuchungsrahmen und neutrale Profile
should_keep: true
should_move_out: []
should_move_in:
  - derzeit unter Varianten verbliebene neutrale Namingprofil-Konfiguration
dependencies: [ma_core]
boundary_problems: []
recommended_action: keep_and_complete_via_P011
confidence: high
```

```yaml
module: ma_weather
current_responsibilities:
  - TRY-Erkennung, Import, Auswahl, Ereignisse, Kennwerte, Plots und Bericht
recommended_responsibilities:
  - Wetterquellen bis freigegebener WeatherDataset-Referenz
should_keep: true
should_move_out:
  - keine allgemeinen Reporting- oder UI-Bausteine
should_move_in: []
dependencies: [ma_core, ma_validation]
boundary_problems:
  - mehrere grosse Dateien und lokale optionale Testdaten
recommended_action: keep; split_internally_only_when_touched
confidence: high
```

```yaml
module: ma_building
current_responsibilities:
  - BuildingModelSpecification, Demo-Loader, Diagnosen und Validierung
recommended_responsibilities:
  - gebaeudebezogene Geometrie-, Huell- und Quellenmodelle
should_keep: true
should_move_out: []
should_move_in: []
dependencies: [ma_core, ma_validation]
boundary_problems:
  - Rootpfad wird paketlokal statt ueber zentralen Workspacevertrag bestimmt
recommended_action: keep_and_use_workspace_paths
confidence: high
```

```yaml
module: ma_technical
current_responsibilities:
  - technische Systeme, Topologie, Revisionen, Demos und Validierung
recommended_responsibilities:
  - technischer Systemstand ohne Besitz von Zonenmodellen
should_keep: true
should_move_out:
  - zonenabhaengige Cross-Domain-Validierung
should_move_in: []
dependencies: [ma_core, ma_validation, ma_zones]
boundary_problems:
  - Runtime-Import von ma_zones verletzt die vorgesehene Prozessrichtung
recommended_action: move_zone_contract_check_to_ma_zones_validation
confidence: high
```

```yaml
module: ma_zones
current_responsibilities:
  - Raum-Zonen-Zuordnung, ZoneModelSpecification und ThermalBuildingModel
recommended_responsibilities:
  - Zonen-/Nutzungsmodelle und referenzbasierter Abschluss von Building und Technik
should_keep: true
should_move_out: []
should_move_in:
  - nur die explizit freigegebene Technik-zu-Zonen-Uebergabe
dependencies: [ma_building, ma_validation, ma_technical_type_reference]
boundary_problems:
  - Typkopplung muss ohne Rueckimport aus ma_technical stabil bleiben
recommended_action: keep_as_transition_owner; forbid_reverse_runtime_import
confidence: high
```

```yaml
module: ma_parameters
current_responsibilities:
  - ParameterSnapshot, BaselineSnapshot, Vorschau und Integrationsservices
recommended_responsibilities:
  - alleinige freigegebene Eingangsquelle fuer Varianten
  - Parameter-, Options- und VariationSpecification-Vertraege
should_keep: true
should_move_out:
  - direkte Imports aus ma_variants
should_move_in:
  - Parameter- und Optionsmodelle aus ma_variants
  - zugehoerige Beispielkonfigurationen
dependencies: [ma_core, ma_building, ma_technical, ma_weather, ma_zones, ma_validation, ma_variants]
boundary_problems:
  - echter Laufzeitzyklus mit ma_variants
  - Konfigurationsownership liegt teilweise noch unter config/ma_variants
recommended_action: resolve_cycle_with_compatibility_reexports
confidence: high
```

```yaml
module: ma_variants
current_responsibilities:
  - Kataloge, Auswahl, Naming, Variantenbildung, DB, Economics, IDA-Export und Ergebnisadapter
recommended_responsibilities:
  - VariantSpace, Verification, Catalog, Selection und Generation
should_keep: true
should_move_out:
  - parameter_catalog und option_catalog nach ma_parameters
  - economic_analysis nach ma_economy
  - ida_export nach ma_export_simulation.adapters.ida_ice
  - simulation_results Importanteile nach ma_import_simulation
  - generisches Reporting nach ma_reporting, soweit querschnittlich
should_move_in: []
dependencies: [ma_core, ma_parameters, ma_project]
boundary_problems:
  - echter Zyklus mit ma_parameters
  - geringe Kohäsion durch historische Sammelverantwortung
recommended_action: incremental_extraction_after_contract_tests
confidence: high
```

```yaml
module: ma_analyse
current_responsibilities:
  - Analyse-Service, Datenvorbereitung, Plot-/Tabellenlogik und Stage 1-4
recommended_responsibilities:
  - UI-neutrale Ergebnisvorbereitung und fachliche Analysestufen
should_keep: true
should_move_out:
  - keine UI- oder Run-Orchestrierung
should_move_in:
  - spaeter fachliche Metriken aus ma_variants.simulation_results
dependencies: [ma_parameters, ma_validation]
boundary_problems:
  - sehr grosse Dateien und historische Konfigurationspfade
recommended_action: keep_public_facade; split_internally_by_stage_when_touched
confidence: high
```

```yaml
module: ma_simulation_setup
current_responsibilities:
  - RunManifest und Materialisierung neutraler Run-Pakete
recommended_responsibilities:
  - unveraenderlicher freigegebener Run-Vertrag vor manueller Simulation
should_keep: true
should_move_out: []
should_move_in:
  - ein kanonischer lokaler data/ma_simulation_setup/runs Pfad
dependencies: [ma_analyse, ma_parameters, ma_validation, ma_variants]
boundary_problems:
  - Package- und Provenienzschemas sind noch minimal
recommended_action: keep_and_complete_via_P018
confidence: high
```

```yaml
module: ma_export_simulation
current_responsibilities:
  - vorbereitete neutrale Adaptergrenze fuer IDA ICE
recommended_responsibilities:
  - programmspezifische Materialisierung hinter neutralem Exportport
should_keep: true
should_move_out: []
should_move_in:
  - kontrollierte Teile aus ma_variants.ida_export
dependencies: []
boundary_problems:
  - derzeit Geruest; keine Rechte fuer automatische IDA-Steuerung
recommended_action: defer_to_P009_after_stable_run_package
confidence: high
```

```yaml
module: ma_import_simulation
current_responsibilities:
  - vorbereitete neutrale Ergebnisadaptergrenze
recommended_responsibilities:
  - manuelle, provenance-gepruefte Ergebnisaufnahme und programmspezifische Parser
should_keep: true
should_move_out: []
should_move_in:
  - Import-/Adapteranteile aus ma_variants.simulation_results
dependencies: []
boundary_problems:
  - derzeit Geruest; reale lizenzbeschraenkte Fixtures fehlen bewusst
recommended_action: implement_neutral_manual_MVP_before_automation
confidence: high
```

```yaml
module: ma_economy
current_responsibilities:
  - Paketgeruest
recommended_responsibilities:
  - wirtschaftliche Annahmen und Bewertung
should_keep: true
should_move_out: []
should_move_in:
  - ma_variants.economic_analysis nach stabiler API
dependencies: []
boundary_problems:
  - Zielpaket und aktive Legacy-Implementierung existieren parallel
recommended_action: migrate_only_with_P022_contract
confidence: high
```

```yaml
module: ma_sustainability
current_responsibilities: [Paketgeruest]
recommended_responsibilities: [oekologische Kennwerte und Systemgrenzen]
should_keep: true
should_move_out: []
should_move_in: []
dependencies: []
boundary_problems: [noch kein belegter MVP-Code]
recommended_action: keep_stub_until_P023
confidence: medium
```

```yaml
module: ma_assessment
current_responsibilities: [Paketgeruest]
recommended_responsibilities: [Aggregation und gesamthafte Bewertung]
should_keep: true
should_move_out: []
should_move_in: []
dependencies: []
boundary_problems: [noch kein belegter MVP-Code]
recommended_action: keep_stub_until_P024
confidence: medium
```

```yaml
module: ma_reporting
current_responsibilities: [Paketgeruest]
recommended_responsibilities: [querschnittliche menschlich lesbare Reports und Factsheets]
should_keep: true
should_move_out: []
should_move_in:
  - nur fachuebergreifende Teile aus ma_variants.reporting
dependencies: []
boundary_problems: [Abgrenzung zu fachmodulspezifischen Reports noch zu konkretisieren]
recommended_action: keep_stub_until_P025
confidence: medium
```

```yaml
module: ma_data_export
current_responsibilities: [Paketgeruest]
recommended_responsibilities: [maschinenlesbare Gesamtprojekt-Datenpakete und Exportmanifest]
should_keep: true
should_move_out: []
should_move_in: []
dependencies: []
boundary_problems: [kein stabiler Gesamtbewertungsvertrag]
recommended_action: keep_stub_until_P026
confidence: medium
```

```yaml
module: ma_feedback
current_responsibilities: [Paketgeruest]
recommended_responsibilities: [strukturierte querschnittliche Rueckmeldungen]
should_keep: true
should_move_out: []
should_move_in: []
dependencies: []
boundary_problems: [konkrete Verantwortung noch nicht implementiert]
recommended_action: keep_stub_until_concrete_P027_slice
confidence: medium
```

```yaml
module: ma_workflow
current_responsibilities:
  - zentrale Phasen-, Modul- und Statusmetadaten
  - Analyseadapter, Runner und Dashboardaktionen
recommended_responsibilities:
  - Application Layer und gerichtete Use-Case-Orchestrierung
should_keep: true
should_move_out:
  - jede Fachberechnung
should_move_in:
  - spaetere Cross-Domain-Uebergabeservices, falls sie echte Use Cases sind
dependencies: [ma_analyse]
boundary_problems:
  - direkte Adapterimporte muessen bewusst und getestet bleiben
recommended_action: keep_as_composition_layer
confidence: high
```

```yaml
module: ma_ui
current_responsibilities:
  - Streamlit-Hauptoberflaeche, Tkinter-Analyse und Legacy-Fassaden
recommended_responsibilities:
  - ausschliesslich Darstellung, Sitzungszustand und Use-Case-Aufruf
should_keep: true
should_move_out:
  - jede fachliche Berechnung oder Dateiformatlogik
should_move_in: []
dependencies:
  - ma_workflow
  - mehrere Fachpakete als erlaubte Composition-Layer-Kante
boundary_problems:
  - sehr grosse Dateien, Wildcard-Reexports und mehrere Uebergangsfassaden
recommended_action: preserve_entrypoints; retire_shims_only_with_usage_tests
confidence: high
```

### Geplantes P030-Paket `research_tools`

`research_tools` ist noch kein vorhandenes `ma_*`-Importpaket und zaehlt
deshalb nicht zu den 22 Ist-Modulen dieses Reviews. P030 plant es als
getrennte Forschungsschicht mit folgenden Grenzen:

```yaml
planned_module: research_tools
current_responsibilities: [noch nicht implementiert]
recommended_responsibilities:
  - manuelle Versuchserfassung
  - read-only Import eigener technischer Logs
  - Prozessvergleich und methodische Auswertung
should_keep_separate_from_product_domains: true
should_move_out: []
should_move_in: []
dependencies:
  - stabile IDs und freigegebene technische Logs aus P011 bis P021
boundary_problems:
  - darf keine Rueckabhaengigkeit produktiver Fachmodule erzeugen
  - reale Messdaten benoetigen Schutz- und Versionierungspruefung
recommended_action: create_only_with_approved_P030_slice
confidence: high
```

## Empfohlener Importvertrag

Kurzfristig soll ein AST-basierter Contract-Test mindestens Folgendes
erzwingen:

- `ma_core` und `ma_validation` importieren keine Fachpakete;
- kein Fachpaket importiert `ma_ui`;
- `ma_parameters` importiert nicht `ma_variants`;
- `ma_technical` importiert nicht `ma_zones`;
- Adapter duerfen Fachvertraege importieren, aber Fachkerne keine konkreten
  IDA-Adapter;
- `ma_ui` und `ma_workflow` sind die einzigen breit koppelnden
  Composition-Layer.

Dieser Vertrag wird erst in einer freigegebenen Migrationswelle technisch
erzwungen; der Review veraendert keine produktiven Imports.
