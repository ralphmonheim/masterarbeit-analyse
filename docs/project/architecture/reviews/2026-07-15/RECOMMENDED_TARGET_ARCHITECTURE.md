# Recommended Target Architecture

Stand: 2026-07-15  
Status: Empfehlung, keine Migrationsfreigabe  
Empfohlene Option: Option 1 - konservative Konsolidierung

## 1. Architekturprinzipien

1. Das Repository bleibt eine Anwendung, eine Distribution und ein modularer
   Monolith mit stabilen `ma_*`-Importpaketen.
2. Jedes Fachobjekt besitzt genau einen fachlichen Owner. Andere Pakete
   konsumieren dessen oeffentlichen Vertrag oder einen zeitlich begrenzten,
   getesteten Kompatibilitaetsadapter.
3. Abhaengigkeiten zeigen vom Workflow und von Adaptern zu Fachvertraegen,
   niemals von Fachkernen zur UI oder zu konkreten Simulationsadaptern.
4. `ma_core` und `ma_validation` bleiben klein und fachneutral. Sie sind kein
   Ablageort fuer schwer zuzuordnende Fachlogik.
5. Datei-, Datenbank-, UI- und Simulationsgrenzen erhalten schmale Ports und
   Adapter, ohne ein zusaetzliches Architekturframework einzufuehren.
6. Neue Verzeichnisse werden erst mit dem ersten echten Inhalt angelegt.
7. Migrationen erfolgen in kleinen, einzeln pruef- und rueckrollbaren Wellen.
8. Reproduzierbarkeit umfasst Umgebung, Eingaben, Konfiguration, Codeversion,
   Run-ID, Ergebnisse und Freigabestatus.
9. Versionierbare Beispiele, lokale Arbeitsdaten, generierte Ergebnisse und
   geschuetzte Inhalte bleiben sichtbar getrennt.
10. Planung, Architektur, Entscheidungen, Compliance und Laufzeitstatus
    behalten ihre bereits festgelegten kanonischen Quellen.

Das `src`-Layout wird beibehalten. Es verhindert versehentliche Imports aus
dem Repository-Root und entspricht der Empfehlung des Python Packaging User
Guide: <https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/>.

## 2. Vollstaendiger Zielbaum

`[planned]` bedeutet Zielbild, aber noch kein Auftrag zum Anlegen.

```text
repository/
|-- AGENTS.md
|-- CHANGELOG.md
|-- README.md
|-- pyproject.toml
|-- requirements.txt                 # spaeter abgeleitet oder klar begrenzt
|-- alembic.ini
|-- migrations/
|-- src/
|   |-- ma_core/
|   |   `-- paths.py                 # [planned] WorkspacePaths
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
|   |-- ma_export_simulation/
|   |   `-- adapters/ida_ice/        # [planned]
|   |-- ma_import_simulation/
|   |   `-- adapters/ida_ice/        # [planned]
|   |-- ma_analyse/
|   |-- ma_economy/
|   |-- ma_sustainability/
|   |-- ma_assessment/
|   |-- ma_reporting/
|   |-- ma_data_export/
|   |-- ma_feedback/
|   |-- ma_workflow/
|   |-- ma_ui/
|   |   |-- streamlit_app/
|   |   `-- tkinter_app/
|   `-- research_tools/              # [planned durch P030]
|-- config/
|   `-- <fachlicher-owner>/
|-- data/
|   |-- common/
|   |-- catalogs/                    # bestehende querschnittliche Decision-Ausnahme
|   |-- <fachlicher-owner>/
|   `-- ma_simulation_setup/
|       `-- runs/<run_id>/
|-- docs/
|   |-- common/
|   |-- compliance/
|   |-- examples/
|   |-- project/
|   |   |-- architecture/
|   |   |-- decisions/
|   |   |-- plans/
|   |   `-- weekly_reviews/
|   `-- ma_*/
|-- research_measurements/           # [planned durch P030]
|   `-- EVAL-<id>/
|       |-- evaluation.yaml
|       |-- manual_measurements/
|       |-- referenced_logs/
|       |-- derived_metrics/
|       `-- notes/
|-- tests/
|   |-- test_*.py                    # bestehende Modultests bleiben zunaechst flach
|   |-- contracts/                   # [planned]
|   |-- integration/                 # [planned]
|   |-- fixtures/                    # [planned, nur synthetisch/veroeffentlichbar]
|   `-- golden/                      # [planned, klein und deterministisch]
|-- logs/                            # lokale Laufzeit- und Sitzungslogs
|-- .agents/skills/
|-- .codex/agents/
|-- .github/workflows/               # [planned, gesonderte CI-Freigabe]
`-- graphify-out/                    # [planned, lokal und ignoriert]
```

## 3. Zweck der Hauptordner

| Ordner | Aufgabe | Darf nicht werden |
| --- | --- | --- |
| `src/` | importierbarer Produkt- und Research-Code | Ablage fuer Laufdaten |
| `config/` | versionierbare Konfiguration nach fachlichem Owner | zweite Datenbank oder Secret-Ablage |
| `data/` | fachlich zugeordnete Inputs, Arbeitsstaende und Runs | pauschal veroeffentlichter Datenpool |
| `docs/` | kanonische Projekt-, Fach-, Entscheidungs- und Compliance-Dokumentation | parallele Statuswahrheit |
| `research_measurements/` | P030-Versuchsdaten ausserhalb produktiver Run-Pakete | Kopie der Produktlogik oder ungeprueft versionierter Messdaten |
| `tests/` | Unit-, Contract-, Integrations- und Regressionstests | Produktivdatenarchiv |
| `migrations/` | Alembic-Historie der bestehenden Datenbank | allgemeiner Dateimigrationsordner |
| `logs/` | lokale technische Sitzungs- und Laufprotokolle | versionierte Ergebniswahrheit |
| `.agents/`, `.codex/` | repo-lokale Agentenrollen und duenne Workflow-Router | duplizierte Projektplanung |

## 4. Python-Paketstruktur

- Eine Distribution `ma-analyse` enthaelt weiterhin mehrere `ma_*`-
  Importpakete. Distribution und Importpaket sind unterschiedliche Konzepte:
  <https://packaging.python.org/en/latest/discussions/distribution-package-vs-import-package/>.
- `pyproject.toml` wird die manuelle Build-, Projekt- und
  Abhaengigkeitswahrheit. `requirements.txt` soll spaeter entweder
  reproduzierbar daraus erzeugt oder auf einen klar dokumentierten Zweck
  begrenzt werden.
- Ein spaeterer `ma_core.paths.WorkspacePaths`-Vertrag loest Root-, Config-,
  Data-, Log- und Run-Pfade zentral auf. Bis zur Entscheidung zwischen
  Workspace-Anwendung und portabler Installation darf er keine neue
  Installationssemantik vortaeuschen.
- Paketinterne, mit der Distribution ausgelieferte Ressourcen werden bei
  Bedarf ueber `importlib.resources` gelesen; externe Arbeitsdaten bleiben
  unter einem expliziten Workspace-Root.
- Oeffentliche Vertrage werden ueber kleine `models`, `contracts` oder
  bestehende Facade-Module exportiert. Interne Dateipfade sind keine API.
- Kompatibilitaets-Reexports benoetigen Contract-Tests und ein dokumentiertes
  Ausstiegsdatum; sie sind kein dauerhafter zweiter Owner.

## 5. Modulverantwortungen und Importvertrag

| Bereich | Kanonische Verantwortung |
| --- | --- |
| `ma_core`, `ma_validation` | fachneutrale Basistypen, Pfade, Diagnosen, Freigabe- und Compliance-Grundvertraege |
| `ma_project` bis `ma_parameters` | jeweils eigener Eingabestand; `ma_project` besitzt das neutrale Namingprofil und dessen Konfiguration; `ma_parameters` besitzt Parameter- und Optionskataloge |
| `ma_variants` | VariantSpace, Auswahl, Generierung, Anwendung des Namingprofils und Variantenprovenienz; konsumiert Projekt- und Parametervertraege |
| `ma_simulation_setup` | neutraler Run-Vertrag, Materialisierung und Run-Manifest |
| `ma_export_simulation`, `ma_import_simulation` | neutrale Ports und produktspezifische Adapter, einschliesslich spaeterem IDA-ICE-Adapter |
| `ma_analyse` | UI-neutrale Ergebnisanalyse und Fachservices |
| `ma_economy`, `ma_sustainability`, `ma_assessment` | getrennte Bewertungsdomaenen |
| `ma_reporting`, `ma_data_export` | Berichts- beziehungsweise Datenpaket-Erzeugung aus stabilen Ergebnisvertraegen |
| `ma_workflow`, `ma_ui` | Composition Layer und Oberflaechen; keine Ownership von Fachmodellen |
| `research_tools` | spaetere P030-Mess- und Vergleichslogik, getrennt von Produktivdiensten |

Verbindliche Zielrichtung:

- `ma_core` und `ma_validation` importieren keine Fachpakete;
- kein Fachpaket importiert `ma_ui`;
- `ma_parameters` importiert nicht `ma_variants`;
- Parameter- und Optionskataloge ziehen aus `ma_variants` nach
  `ma_parameters`; `ma_variants` darf zeitlich begrenzte Reexports anbieten;
- `ma_project` besitzt das neutrale Benennungsprofil; `ma_variants` erzeugt
  damit konkrete Variantennamen, besitzt das Profil aber nicht;
- `ma_technical` importiert nicht `ma_zones`;
- der zonenabhaengige Technikabgleich liegt in `ma_zones.validation`, weil
  Zonen den zuvor freigegebenen Technikstand referenzieren;
- Fachkerne importieren keine konkreten IDA-ICE-Adapter;
- `ma_ui` und `ma_workflow` duerfen als Composition Layer mehrere Fachpakete
  kennen.

## 6. Datenstruktur

Es erfolgt keine pauschale Big-Bang-Umstellung auf globale Ordner wie
`raw/interim/processed`. Die erste Gliederung bleibt der fachliche Owner.
`data/catalogs/` bleibt gemaess technischer Entscheidung 8, UD-006 und
UD-012 die bewusst querschnittliche Ausnahme fuer Produkt- und
Materialkatalogstruktur; reale Inhalte werden nicht versioniert.

```text
data/<owner>/
|-- input/          # lokale oder freigegebene Eingaben, wenn fachlich passend
|-- working/        # [planned] reproduzierbare Zwischenstaende
|-- output/         # lokale Ergebnisse, sofern kein Run-Paket
`-- registry/       # [planned] Metadaten, Checksummen, Quellen- und Rechtebezug
```

Die Unterteilung wird nur dort eingefuehrt, wo der reale Lebenszyklus sie
braucht. Jedes verarbeitete Artefakt soll mindestens Owner, Quelle,
Checksumme, Erzeugungszeitpunkt, Tool-/Schema-Version, Schutzklasse und
Freigabestatus referenzieren. Kleine synthetische Beispiele liegen unter
`tests/fixtures/` oder `docs/examples/`, nicht neben realen Arbeitsdaten.

## 7. Simulationsstruktur

Der neutrale Zielort ist `data/ma_simulation_setup/runs/<run_id>/`:

```text
<run_id>/
|-- manifest.yaml
|-- inputs/                 # referenzierte oder materialisierte neutrale Inputs
|-- variants/<var_id>/
|-- export/                 # adapterbezogene Uebergabeartefakte
|-- import/                 # unveraenderte Ergebnisuebernahme plus Checksumme
|-- results/                # normalisierte Ergebnisse
|-- logs/                   # technische Run-Logs
`-- provenance.json
```

Das Manifest referenziert Codeversion, Konfigurationsfingerprint,
Inputchecksummen, Varianten-IDs, Adapter-/Programmversion, Freigaben und
Ergebnischecksummen. Proprietäre Systemdateien koennen lokal referenziert,
aber nicht automatisch gelesen, kopiert oder versioniert werden. Der
bestehende manuelle IDA-ICE-Schritt bleibt bis zu einer gesonderten
Rechte- und Automatisierungsfreigabe erhalten.

## 8. Research-Struktur

P030 bleibt fachlich getrennt: Produktivcode erzeugt technische Ereignisse;
`research_tools` wertet freigegebene Messdaten aus. Der bereits in P030
geplante kanonische Datenpfad bleibt
`research_measurements/EVAL-<id>/`. Dort liegen `evaluation.yaml`, getrennte
manuelle Messwerte, referenzierte oder freigegeben kopierte Logs, abgeleitete
Kennzahlen und Notizen. `src/research_tools/` enthaelt die getestete Mess- und
Vergleichslogik. Der Bereich wird erst mit dem ersten freigegebenen P030-Slice
angelegt; reale Messdaten sind standardmaessig lokal und werden vor einer
Versionierung auf Personen-, Projekt- und Rechtebezug geprueft.

Notebooks sind kein Standardpfad. Falls sie wissenschaftlich erforderlich
werden, bleiben sie duenne Explorationen und rufen getestete Funktionen auf.
Reproduzierbare Forschung verlangt dokumentierte Daten, Software,
Abhaengigkeiten und Schritte; als methodische Referenz dient
<https://book.the-turing-way.org/reproducible-research/reproducible-research/>.

## 9. Dokumentationsstruktur

Die bestehende Struktur bleibt kanonisch:

- `docs/project/plans/PLAN_INDEX.md`: Planinventar;
- `docs/project/plans/PLAN_STATUS.md`: aktive Arbeitslage;
- `docs/project/architecture/`: Zielarchitektur und datierte Reviews;
- `docs/project/decisions/`: Nutzerentscheidungen, technische Entscheidungen
  und ADRs;
- `docs/compliance/`: Rechte- und Verarbeitungsvorpruefung;
- `docs/ma_*/`: modulbezogene Nutzung und Fachhinweise;
- `CHANGELOG.md`: umgesetzte, versionierbare Aenderungen.

Die Diataxis-Typen Tutorial, How-to, Reference und Explanation koennen in
Indizes markiert werden, ohne den Bestand massenhaft zu verschieben:
<https://diataxis.fr/>. Datierte Reviews sind Beleg-Snapshots und duerfen
nicht zur zweiten Architektur- oder Statuswahrheit werden.

## 10. Teststruktur

Die 47 bestehenden Testdateien bleiben zunaechst an ihren Pfaden. Neue
Unterordner entstehen mit dem ersten passenden Test:

- `tests/contracts/`: Importregeln, oeffentliche DTOs, Schema- und
  Kompatibilitaetsvertraege;
- `tests/integration/`: moduluebergreifende Ketten und Run-Pakete;
- `tests/fixtures/`: kleine synthetische, publizierbare Eingaben;
- `tests/golden/`: kleine deterministische Referenzausgaben mit erklaerter
  Aktualisierung;
- bestehende `test_*.py`: schnelle modulnahe Unit- und Regressionstests.

Vorgesehene Profile:

| Profil | Inhalt | Zweck |
| --- | --- | --- |
| Local Fast | Contract-Tests, betroffene Unit-Tests, Ruff | jede kleine Welle |
| Local Full | komplette Suite plus Build-/Wheel-Smoke-Test | Wellenabnahme und Release |
| Restricted | nur synthetische/versionierte Daten, kein Netzwerk | CI-faehige Baseline |
| Licensed Local | objektbezogen freigegebene lokale Daten | manuell, nie allgemeine CI |

Ein spaeterer minimaler Python-CI-Workflow soll nur das Restricted-Profil
ausfuehren. Offizielle GitHub-Grundlage:
<https://docs.github.com/en/actions/tutorials/build-and-test-code/python>.

## 11. Agents und Skills

| Teamprofil | Rollen | Einsatz |
| --- | --- | --- |
| Minimalteam | Tera | kleine, eindeutig begrenzte Analyse, Integration und Abschluss |
| Standardteam | Tera, Mira, Vera | Architektur-, Struktur- und groessere Implementierungsslices mit Inventar und unabhaengigem Qualitaetsreview |
| erweitertes Reviewteam | Standardteam plus Professor Sophia und/oder Justus | Methodik, Reproduzierbarkeit, Normen, Daten, Lizenzen, externe Verarbeitung oder Veroeffentlichung |

Ada ist kein zusaetzlicher Review-Layer, sondern der Implementation Engineer
nach konkreter Freigabe und mit eindeutigem Dateibesitz. Tera bleibt Owner
fuer Integration, Validierung und Abschluss. Mira inventarisiert read-only;
Vera prueft Qualitaet und Regressionen; Professor Sophia wissenschaftliche
Methodik und Justus Rechte-, Daten- und Veroeffentlichungsgrenzen.
- `repo-release-workflow` und `project-governance-workflow` bleiben duenne
  Router. Neue Skills sind nur gerechtfertigt, wenn ein wiederkehrender
  Ablauf nicht bereits durch diese Router und die kanonischen Dokumente
  abgedeckt ist.
- Allgemeine Scans bleiben standardmaessig auf `git ls-files` begrenzt.
- Agenten erzeugen keine Freigabe aus Audit-, Plan- oder Capability-Tabellen.

Damit bleibt das System fuer eine Einzelperson erklaerbar und verhindert,
dass Agentendokumente eine eigene Projektwahrheit bilden.

## 12. Graphify-Strategie

Graphify ist optional und derzeit weder installiert noch freigegeben. Ein
spaeterer Pilot verwendet eine positive Allowlist:

```text
src/**/*.py
tests/**/*.py
pyproject.toml
docs/project/architecture/**/*.md
docs/project/decisions/**/*.md
docs/compliance/**/*.{md,yaml,yml,json}
config/**/example*.{yaml,yml,json}
```

Ausgeschlossen bleiben `data/`, `logs/`, Archive, PDFs, `.idm`, `.nmf`,
`.prn`, Secrets, virtuelle Umgebungen, ignorierte und unversionierte Dateien.
Deterministische Kanten werden als Fakten gespeichert; inferierte Kanten
benoetigen Beleg, Konfidenz und Toolversion. `graphify-out/graph.json` bleibt
lokal und ignoriert. Nur ein manuell gepruefter, bereinigter
`GRAPH_REPORT.md` waere spaeter versionierbar. Watch, Hook, Installation und
Scope benoetigen jeweils eine gesonderte Freigabe.

## 13. Git-Strategie

- `main` bleibt der kanonische Integrationszweig; Releases erhalten einen
  eindeutigen Tag und einen vorab geprueften Scope.
- Architekturwellen werden nach Freigabe einzeln umgesetzt, validiert und
  commitbar gemacht. Riskante Wellen koennen auf kurzlebigen Branches
  vorbereitet werden; langfristige Parallelzweige sind nicht erforderlich.
- Spaetere echte Verschiebungen verwenden `git mv`, getrennt von
  Inhaltsaenderungen, damit Historie und Review nachvollziehbar bleiben.
- Kein generierter Massendiff, keine Secrets und keine geschuetzten Daten.
- Git LFS ist aktuell nicht erforderlich: die groesste versionierte Datei
  liegt deutlich unter 1 MB. LFS waere nur fuer grosse, veroeffentlichbare
  Binaerartefakte nach eigener Entscheidung geeignet, niemals als Umgehung
  von Schutz- oder Lizenzgrenzen. Referenzen:
  <https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-git-large-file-storage>
  und <https://docs.github.com/en/repositories/creating-and-managing-repositories/repository-limits>.

## 14. Generierte Dateien

Standardmaessig lokal und ignoriert:

- Lauf-, Cache-, Temp-, Log-, Coverage-, Build- und Graphify-Ausgaben;
- komplette Simulationsexporte und -ergebnisse;
- Research-Ausgaben, die aus versionierten Inputs regeneriert werden koennen;
- lokale Environment-Snapshots mit Rechnerpfaden.

Versionierbar sind nur kleine, deterministische und fachlich erklaerte
Referenzartefakte, beispielsweise synthetische Fixtures, Golden Files oder
bereinigte Beispielgrafiken. Jedes versionierte Golden File benoetigt
Erzeugungsbefehl, Eingabe, Toolversion und Abnahmetest.

## 15. Private und lizenzierte Inhalte

- Reale Katalog-, Projekt-, Normen-, Literatur-, IDA-/EQUA- und andere
  geschuetzte Inhalte bleiben ausserhalb von Git und Git LFS.
- `.gitignore` ist nur technische Abwehr und kein Verarbeitungsrecht.
- Vor Lesen, Parsen, OCR, KI-Analyse, Embeddings, Graph, RAG, Cloud-Upload,
  Weitergabe oder Veroeffentlichung sind Quelle, Rechteinhaber,
  Maschinen-/KI-Rechte, Schutzklasse und erlaubte Ausgabe objektbezogen zu
  belegen.
- Manifeste duerfen bereinigte Metadaten, Checksummen und lokale Referenzen
  fuehren, aber keine Geheimnisse, Lizenzschluessel oder rekonstruierbaren
  Vollinhalte.
- Ein allgemeiner Nutzerauftrag ersetzt keine fehlenden Rechte oder
  vertraglichen Genehmigungen.

## 16. Rationale gegenueber den Alternativen

Option 1 erzielt in der gewichteten Matrix 4,55 von 5 Punkten, Option 2 3,64
und Option 3 3,14. Entscheidend sind nicht kosmetische Paketnamen, sondern
die realen Risiken: mindestens 365 Importanweisungen, bestehende
Dokumentlinks, eine gemeinsam entwickelte Anwendung und keine unabhaengig
versionierten Konsumenten.

Die Empfehlung lehnt deshalb vor dem MVP ab:

- einen neuen gemeinsamen Namespace nur fuer optische Einheitlichkeit;
- mehrere Distributionen ohne getrennte Teams oder Releasezyklen;
- Microservices ohne unabhaengiges Deployment- oder Skalierungsproblem;
- eine Plugin-Architektur ohne mehrere stabile austauschbare Anbieter;
- einen Big-Bang-Umbau von Daten-, Test- und Dokumentationspfaden.

Option 2 wird nach dem MVP nur neu bewertet, wenn eine allgemeine externe
Distribution, mehrere externe Konsumenten oder echte Namenskollisionen
auftreten. Option 3 setzt unabhaengige Versionierung, Teams oder
Releasezyklen voraus. Bis dahin verbessert die konservative Konsolidierung
Testbarkeit, Reproduzierbarkeit und Ownership mit dem geringsten Risiko fuer
die Masterarbeit.
