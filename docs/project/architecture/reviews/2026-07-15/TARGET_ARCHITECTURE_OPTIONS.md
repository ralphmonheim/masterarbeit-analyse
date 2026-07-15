# Target Architecture Options

Stand: 2026-07-15
Status: Vorschlag, keine Migrationsfreigabe

## Bewertungsgrundlage

Alle Optionen erhalten dieselben professionellen Mindestmassnahmen:

- `pyproject.toml` als manuelle Dependency-Wahrheit;
- reproduzierbarer Environment-Snapshot;
- lokaler und spaeter minimaler CI-Qualitaetslauf;
- Import-, Schema-, Contract- und Run-Provenienztests;
- klare Trennung versionierter Beispiele von lokalen oder geschuetzten Daten;
- bestehende Plan-, Decision- und Compliance-Wahrheiten.

Ein gemeinsamer Namespace oder mehrere Distributionen erhalten keinen Bonus
fuer Massnahmen, die der bestehende modulare Monolith ebenfalls umsetzen kann.

## Option 1 - Konservative Konsolidierung

Die vorhandenen `ma_*`-Importpakete bleiben stabil. Verantwortungen werden
entlang bestehender Zielplaene schrittweise korrigiert; neue Verzeichnisse
entstehen nur bei realem Inhalt.

```text
repository/
|-- pyproject.toml
|-- README.md
|-- src/
|   |-- ma_core/
|   |-- ma_validation/
|   |-- ma_database/
|   |-- ma_project/
|   |-- ma_weather/
|   |-- ma_building/
|   |-- ma_technical/
|   |-- ma_zones/
|   |-- ma_parameters/
|   |-- ma_variants/
|   |-- ma_simulation_setup/
|   |-- ma_export_simulation/adapters/ida_ice/
|   |-- ma_import_simulation/adapters/ida_ice/
|   |-- ma_analyse/
|   |-- ma_economy/
|   |-- ma_sustainability/
|   |-- ma_assessment/
|   |-- ma_reporting/
|   |-- ma_data_export/
|   |-- ma_feedback/
|   |-- ma_workflow/
|   `-- ma_ui/
|-- config/<fachlicher-eigentuemer>/
|-- data/<fachlicher-eigentuemer>/
|-- docs/
|   |-- project/architecture/
|   |-- project/decisions/
|   |-- project/plans/
|   |-- compliance/
|   `-- ma_*/
|-- tests/
|   |-- test_*.py
|   |-- contracts/       # nur wenn erste Contract-Datei entsteht
|   |-- integration/     # nur wenn erster echter Integrationsfall entsteht
|   |-- fixtures/        # synthetisch und veroeffentlichbar
|   `-- golden/          # kleine deterministische neutrale Exporte
|-- migrations/
`-- .github/workflows/   # spaetere, separat freizugebende CI-Welle
```

Staerken:

- geringstes Risiko fuer 365+ bestehende Importstellen und viele Dokumentlinks;
- vorhandene Fachsprache bleibt sichtbar;
- Zyklen und Ownership koennen direkt statt ueber Alias-Massenarbeit geloest
  werden;
- fuer eine Einzelperson gut erklaerbar.

Schwaechen:

- Distribution `ma-analyse` und mehrere `ma_*`-Importpakete bleiben optisch
  uneinheitlich;
- Importgrenzen muessen durch Tests statt durch separate Builds erzwungen
  werden;
- einige historische Kompatibilitaetsfassaden bleiben temporaer bestehen.

## Option 2 - Professioneller modularer Monolith mit Namespace

Alle Pakete werden Subpackages eines gemeinsamen Namespaces. Ports,
Application Layer und Adapter werden expliziter benannt.

```text
repository/
|-- pyproject.toml
|-- src/
|   `-- masterthesis/
|       |-- core/
|       |-- validation/
|       |-- domains/
|       |   |-- project/
|       |   |-- weather/
|       |   |-- building/
|       |   |-- technical/
|       |   |-- zones/
|       |   |-- parameters/
|       |   |-- variants/
|       |   |-- analysis/
|       |   |-- economy/
|       |   |-- sustainability/
|       |   `-- assessment/
|       |-- application/
|       |   |-- workflow/
|       |   `-- simulation_setup/
|       |-- adapters/
|       |   |-- persistence/
|       |   |-- simulation/ida_ice/
|       |   `-- reporting/
|       `-- ui/
|           |-- streamlit/
|           `-- tkinter/
|-- tests/
|   |-- unit/
|   |-- contracts/
|   |-- integration/
|   `-- regression/
|-- config/
|-- data/
`-- docs/
```

Staerken:

- klare Trennung von Distribution und internem Namespace;
- Ports-and-Adapters-Richtung wird im Verzeichnisbaum sichtbar;
- weniger globale Namenskollisionen bei spaeterer externer Nutzung.

Schwaechen:

- betrifft mindestens 365 Importanweisungen in 139 Source-/Testdateien plus
  Commands, Docs und Konfiguration;
- Alias- und Deprecation-Layer waeren fuer den Masterarbeitszeitraum zusaetzliche
  Komplexitaet;
- loest weder Dependency-Drift noch bestehende fachliche Zyklen automatisch.

## Option 3 - Multi-Package-Monorepository

Jede stabile Domaene wird eine eigene Distribution mit eigenem Build und
eigenen Abhaengigkeiten; das Repository stellt gemeinsames Tooling bereit.

```text
repository/
|-- pyproject.toml                 # Workspace-/Toolingebene
|-- packages/
|   |-- ma-core/
|   |   |-- pyproject.toml
|   |   `-- src/ma_core/
|   |-- ma-validation/
|   |   |-- pyproject.toml
|   |   `-- src/ma_validation/
|   |-- ma-inputs/
|   |   |-- pyproject.toml
|   |   `-- src/ma_weather|ma_building|ma_technical|ma_zones|ma_parameters/
|   |-- ma-variants/
|   |-- ma-simulation/
|   |-- ma-analysis/
|   `-- ma-application/
|-- tests/
|   |-- cross_package_contracts/
|   `-- end_to_end/
|-- docs/
|-- config/
`-- data/
```

Staerken:

- technische Erzwingung von Abhaengigkeiten und Package-Ownership;
- unabhaengige Wiederverwendung und Versionierung waeren moeglich;
- klare Build- und Releaseoberflaechen.

Schwaechen:

- mehrere Builds, Versionen, Lock-/Releasewege und Cross-Package-Tests;
- die Fachpakete werden derzeit gemeinsam entwickelt und deployed;
- es gibt weder mehrere Teams noch unabhaengige externe Konsumenten;
- hoechster Aufwand ohne proportionalen wissenschaftlichen Nutzen.

## Namensvarianten

| Variante | Verstaendlichkeit | Packaging | Wartung | Migrationskosten | Empfehlung |
| --- | --- | --- | --- | --- | --- |
| A: `ma_*` behalten | unmittelbar zum Projekt passend | eine Distribution mit mehreren Importpaketen | fuer aktuellen Umfang gut | niedrig | jetzt beibehalten |
| B: `masterthesis.*` | technisch geschlossen, aber generischer Name | sauberer Namespace | langfristig gut | sehr hoch | nach MVP nur bei echtem Publikationsbedarf neu bewerten |
| C: mehrere Distributionen | Paketgrenzen maximal sichtbar | komplexes Monorepo | fuer mehrere Teams geeignet | extrem hoch | verwerfen |

Distribution Name, Repositoryname und Importpakete sind unterschiedliche
Begriffe. Der aktuelle Distribution Name `ma-analyse` muss nicht allein wegen
mehrerer `ma_*`-Importpakete geaendert werden. Vor einer oeffentlichen
allgemeinen Distribution waere jedoch eine eigene Naming-ADR sinnvoll.

## Weitere Architekturformen

| Form | Bewertung fuer dieses Projekt |
| --- | --- |
| aktueller modularer Monolith | passende Ausgangsbasis; Grenzen muessen getestet werden |
| Ports and Adapters / Hexagonal | selektiv sinnvoll an Datei-, DB-, UI- und IDA-Grenzen; kein Frameworkumbau noetig |
| Plugin-Architektur | erst bei mehreren austauschbaren Simulationsprogrammen oder externen Erweiterern; heute vorzeitig |
| getrennte Repositories | verschlechtert atomare Fachmigrationen und Reproduzierbarkeit; kein Bedarf |
| Microservices | kein unabhaengiges Deployment, Skalierungs- oder Teamproblem; klar ungeeignet |

## Gewichtete Entscheidungsmatrix

Skala 1 bis 5. Bei `Migrationsrisiko` und `Aufwand` bedeutet ein hoher Wert
geringes Risiko beziehungsweise geringen Aufwand.

Die Gewichte folgen dem konkreten Projektziel, nicht einer allgemeinen
Enterprise-Matrix:

- 44 % fuer Verstaendlichkeit, fachliche Trennung und Eignung fuer die
  Masterarbeit, weil eine Einzelperson den MVP entwickeln und erklaeren muss;
- 24 % fuer Testbarkeit und Reproduzierbarkeit, weil Ergebnisse
  wissenschaftlich nachvollziehbar bleiben muessen;
- 22 % fuer Migrationsrisiko und Aufwand, weil Strukturarbeit den MVP nicht
  verdraengen darf;
- 10 % fuer spaetere Erweiterbarkeit sowie Codex-, Obsidian- und
  Graphify-Nutzbarkeit, weil diese nuetzlich, aber keine aktuellen
  Produktanforderungen sind.

| Kriterium | Gewicht | Option 1 | Option 2 | Option 3 |
| --- | ---: | ---: | ---: | ---: |
| Verstaendlichkeit | 14 % | 4,5 | 4,0 | 3,0 |
| fachliche Trennung | 15 % | 4,0 | 4,5 | 5,0 |
| Testbarkeit | 12 % | 4,5 | 4,5 | 4,5 |
| Reproduzierbarkeit | 12 % | 4,5 | 4,5 | 4,5 |
| Migrationsrisiko | 12 % | 5,0 | 2,0 | 1,0 |
| Aufwand | 10 % | 5,0 | 2,0 | 1,0 |
| Eignung fuer Masterarbeit | 15 % | 5,0 | 3,0 | 1,5 |
| spaetere Erweiterbarkeit | 5 % | 3,5 | 4,5 | 5,0 |
| Codex-Nutzbarkeit | 2 % | 4,5 | 4,0 | 3,0 |
| Obsidian-Nutzbarkeit | 1 % | 4,0 | 4,0 | 3,0 |
| Graphify-Nutzbarkeit | 2 % | 4,0 | 4,5 | 5,0 |
| **gewichtetes Ergebnis** | **100 %** | **4,55** | **3,64** | **3,14** |

## Empfehlung

Option 1 ist die kleinste professionelle Struktur fuer den realen Bestand.
Sie wird um Importvertraege, zentrale Pfadauflösung, reproduzierbare
Umgebungsmetadaten, Run-Provenienz und inkrementelle Verantwortungsmigrationen
ergaenzt. Option 2 bleibt eine spaetere ADR-Option, falls nach dem MVP mehrere
externe Konsumenten, eine allgemeine Distribution oder Namenskollisionen
tatsaechlich auftreten.
