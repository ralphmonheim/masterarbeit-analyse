# Current State Inventory

Stand: 2026-07-15
Status: Review-Snapshot, nicht autoritativ

## Executive Summary

Das Repository ist bereits ein installierbares Python-Projekt im `src/`-
Layout und besitzt fachlich erkennbare Paketgrenzen, zentrale Planung,
technische Decisions sowie starke Compliance-Vertraege. Eine grundlegende
Repository- oder Multi-Package-Neustruktur ist fuer die Masterarbeit nicht
erforderlich.

Die wichtigsten realen Architekturprobleme sind:

1. ein nachgewiesener Laufzeit-Paketzyklus `ma_parameters <-> ma_variants`
   sowie eine gegenlaeufige Zonen-/Technikgrenze mit Runtime-Import
   `ma_technical -> ma_zones` und Typreferenz in Gegenrichtung;
2. Packaging-Drift: `pyproject.toml` und Modul melden `0.28.0`, die lokale
   editable Distribution-Metadaten noch `0.20.0`; `requirements.txt` bildet
   nicht alle Runtime-Abhaengigkeiten aus `pyproject.toml` ab;
3. keine versionierte CI-Pipeline und keine reproduzierbar gesperrte
   Entwicklungsumgebung;
4. Modul-, Lebenszyklus- und Schutzklassifikation der Daten werden noch nicht
   als ein gemeinsamer Provenienzvertrag gefuehrt;
5. mehrere Zielpakete sind bewusst nur einzeilige Gerueste, waehrend
   `ma_ui`, `ma_analyse` und `ma_variants` den Grossteil des Codes tragen;
6. der flache Testordner ist aktuell handhabbar, trennt Contract-,
   Integrations- und Regressionstests aber nicht sichtbar.

## Quantitativer Snapshot

| Kennzahl | Bestand | Scope | Bewertung |
| --- | ---: | --- | --- |
| Python-Importpakete unter `src/` | 22 | versionierte Baseline; `.egg-info` ausgeschlossen | fachlich lesbar, aber teilweise nur Geruest |
| Python-Dateien im Repo | 363 | versionierte Baseline | drei grosse Schwerpunkte: UI, Analyse, Varianten |
| Dokumentationsdateien `.md` | 146 | versionierte Baseline vor P031/P032 | reichhaltig, erfordert klare Ownership |
| Bild-/PDF-Dateien | 44 | versionierte Baseline | groesste Datei 911.327 Bytes; aktuell kein LFS-Bedarf |
| Testfaelle | 490 / 496 | versionierte Baseline ohne P031-Contract / aktueller Working Tree mit sechs P031-Contracts | gute Basis; keine CI-Ausfuehrung im Repo |
| erkannte Laufzeit-Paketzyklen | 1 | Sourcecode der versionierten Baseline | hoher Handlungsbedarf vor Namespace-Migration |
| Git-LFS | installiert, ungenutzt | lokale Environment-Beobachtung | fuer aktuelle Dateigroessen nicht erforderlich |
| Graphify | nicht installiert | lokale Environment-Beobachtung | statischer Import-/Referenzgraph als Ersatz |
| Obsidian | kein Vault-Pfad bereitgestellt | aktuelle Projektsitzung | nur konzeptionell bewertet |

## Professionelle Referenzprojekte

| Referenz | Beobachtetes Prinzip | Uebertragbar | Nicht blind uebertragbar |
| --- | --- | --- | --- |
| Python Packaging User Guide | `pyproject.toml`, explizites Buildsystem und `src/`-Layout verhindern zufaellige Root-Imports | `src/` beibehalten, Wheel-/Installations-Smoke-Test ergaenzen, Metadaten zu einer Wahrheit machen | Buildsystemwechsel ohne konkreten Nutzen |
| Pydantic | stabile oeffentliche Modelle, dokumentierte Breaking Changes und Uebergangsimporte (`pydantic.v1`) | bei spaeterer Umbenennung Aliase und Deprecation-Fenster | dessen Groesse, Rust-Unterbau und Releaseapparat |
| FastAPI | ein klarer Produktkern, explizite optionale Abhaengigkeiten, Docs/Tests/CI als Teil des Produkts | optionale GUI-/Datenbankgruppen pruefen; stabile CLI-Fassade | Webframework- oder Deployment-Struktur |
| scikit-learn | Tests gegen installierten Code, Entwicklungsleitfaden, Kompatibilitaets- und Changelogdisziplin | installierte Distribution testen; Contract-/Regressionstests benennen | umfangreiche Maintainer- und Plattformmatrix |
| SciPy | Submodule mit klaren Scopes; groessere Aenderungen werden diskutiert, getestet und dokumentiert | Paketgrenzen an Verantwortung statt Dateityp ausrichten; Migration per ADR/Welle | Governance eines internationalen Grossprojekts |
| Cookiecutter Data Science | unveraenderliche Rohdaten, getrennte externe/interim/processed Daten und generierte Reports | Lebenszyklusbegriffe und Unveraenderlichkeit in Modulpfaden verwenden | globalen Musterbaum ungeprueft ueber die fachliche Modulownership legen |
| The Turing Way | Reproduzierbarkeit verbindet Daten, Code, Umgebung und Ergebnisse | Run-Manifest, Environment-Lock, Provenienz und Git-Commit verbinden | Oeffentlichkeit geschuetzter Forschungsobjekte voraussetzen |
| FAIR | findable, accessible, interoperable, reusable und maschinenlesbare Metadaten | stabile IDs, Provenienz und explizite Zugriffsbedingungen | FAIR mit offen oder veroeffentlichbar gleichsetzen |
| Diataxis | Tutorials, How-to, Referenz und Erklaerung bedienen verschiedene Beduerfnisse | Dokumenttyp in Indexen kennzeichnen und neue Inhalte passend einordnen | leere Quadranten oder sofortige Massenverschiebung erzeugen |

Primaerquellen, abgerufen am 2026-07-15. Repository-Links zeigen auf den zu
diesem Datum sichtbaren Default-Branch und sind deshalb als datierte
Webbeobachtung, nicht als gepinnter Commit, zu verstehen:

- <https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/>
- <https://packaging.python.org/en/latest/guides/writing-pyproject-toml/>
- <https://github.com/pydantic/pydantic>
- <https://github.com/fastapi/fastapi>
- <https://scikit-learn.org/stable/developers/index.html>
- <https://docs.scipy.org/doc/scipy/dev/core-dev/index.html>
- <https://cookiecutter-data-science.drivendata.org/>
- <https://book.the-turing-way.org/reproducible-research/reproducible-research/>
- <https://doi.org/10.1038/sdata.2016.18>
- <https://diataxis.fr/>

## Bestandsinventar

| Bereich | vorhandener Pfad | Verantwortung | Zustand | Problem | Abhaengigkeiten |
| --- | --- | --- | --- | --- | --- |
| Python-Code | `src/ma_*` | Fach- und Querschnittspakete | aktiv, `src/`-Layout | 22 Top-Level-Pakete, davon mehrere Gerueste; ein Runtimezyklus plus eine Richtungsverletzung | `pyproject.toml`, Tests |
| Analyse | `src/ma_analyse/` | Importvorbereitung, Diagramme, Stage 1-4 | umfangreich, teilweise legacy-gepraegt | 10.870 nichtleere physische Zeilen in versionierten `.py`-Dateien; mehrere Verantwortungen | parameters, validation |
| UI | `src/ma_ui/` | Streamlit, Tkinter und Kompatibilitaetsfassaden | umfangreich | 10.858 nichtleere physische Zeilen in versionierten `.py`-Dateien; viele direkte Fachpaketimporte | workflow und fast alle Fachmodule |
| Varianten | `src/ma_variants/` | Varianten, Kataloge, Alt-DB, Exporte | umfangreich, im Umbau | besitzt noch Parameter-, Wirtschafts-, IDA- und Ergebnislogik anderer Zielmodule | core, parameters, project |
| Kern | `src/ma_core/` | Konfiguration, Quellen, Sitzungslog, Compliance | aktiv | gute neutrale Basis; darf kein Sammelbecken werden | keine Fachpakete |
| Validierung | `src/ma_validation/` | fachneutrale Diagnosen und Releaseentscheidungen | aktiv | klein und passend; Trennung zu Compliance erhalten | core |
| Workflow | `src/ma_workflow/` | Phasen-/Modulkatalog und Orchestrierungsfassaden | aktiv | importiert Analyse direkt; bei Ausbau Ports statt Fachlogik bevorzugen | analyse |
| Eingabemodule | `src/ma_weather`, `ma_building`, `ma_zones`, `ma_technical`, `ma_parameters` | validierte Eingabekette | unterschiedlich reif | gegenlaeufige Zonen-/Technikgrenze und Parameter-/Variantenzyklus | core, validation und untereinander |
| Simulation | `ma_simulation_setup`, `ma_export_simulation`, `ma_import_simulation` | neutrales Run-Paket und Adaptergrenzen | Setup minimal aktiv, Adapter Gerueste | IDA-Altlogik liegt noch in `ma_variants` | parameters, variants, analyse |
| Bewertung/Export | `ma_economy`, `ma_sustainability`, `ma_assessment`, `ma_reporting`, `ma_data_export` | spaetere Ergebnisbewertung | weitgehend Gerueste | Paketanzahl erzeugt vor Nutzen Kontextkosten | P022-P026 |
| Datenmodelle | modulbezogene `models.py`, Dataclasses | Fachvertraege | ueberwiegend klar | Schema-/Versionsstrategie nicht fuer alle Grenzen einheitlich | Config, YAML, Tests |
| Schemas | `ma_core/compliance/schemas`, Compliance-YAML | Compliance-Vertraege | strukturiert | Fachschemas fuer Run-/Snapshot-Austausch noch nicht durchgaengig extern validierbar | core, parameters, simulation setup |
| Tests | `tests/test_*.py`, `tests/conftest.py` | Unit-, Integrations- und Regressionstests | 490 versionierte Baseline-Tests; 496 im aktuellen Working Tree mit sechs P031-Contracts | Testart und Modulvertrag nicht sichtbar; keine CI | editable Installation |
| Build/Packaging | `pyproject.toml`, `requirements.txt` | Distribution und Umgebung | installierbar | lokale Editable-Metadaten 0.20.0 vs. versionierter Code 0.28.0; zwei Abhaengigkeitswahrheiten | setuptools, pip |
| Daten | `data/<modul>/` | lokale Inputs, Outputs, Reports | modulbezogen und meist ignoriert | Lebenszyklus/Schutzklasse nicht einheitlich; Beispieloutputs im Outputpfad versioniert | `.gitignore`, Modulservices |
| Konfiguration | `config/<modul>/` | versionierte Beispiele/Vorlagen | gut nachvollziehbar | Parameter/Optionen liegen noch unter Varianten statt Parameters | Fachpakete |
| Simulationsinputs | `data/ma_variants/ida_exports`, `data/ma_analyse/ida_imports` | lokale IDA-Uebergabe | ignoriert | historische Ownership; kein einheitlicher Run-Root | P009, P018 |
| Simulationsergebnisse | lokale Analyse-/Variantenpfade | Ergebnisaufnahme | nicht inhaltlich geprueft | Provenienz und Run-Zuordnung muessen vor Migration belegt werden | RunManifest, IDA |
| Normen | `data/common/normen/`, `docs/compliance/din_nautos/` | lokale Originale vs. Rechte-/Metadatenregeln | Inhalte nicht geprueft | `current/` und `templates/` haben noch keine robuste Ignore-Regel | objektbezogene Rechte |
| Literatur | kein kanonischer versionierter Volltextbereich | Quellen/Methodik | nur konzeptionell | Metadaten- und Volltextgrenze noch nicht als Repovertrag beschrieben | Zotero/Obsidian spaeter |
| Projektdokumentation | `docs/project/` | Planung, Architektur, Decisions, Routinen | stark strukturiert | Breite und historische Kontexte erfordern klare fuehrende Quellen | P007, P031 |
| Modul-Dokumentation | `docs/ma_*/` | Modulzweck und Bedienung | vorhanden | Dokumenttypen teilweise gemischt | Fachpakete und Plaene |
| Handover | Plan-/Statusabschnitte und Modulplaene | Uebergaben zwischen Slices | verteilt, aber referenziert | kein eigener Handoverbaum; derzeit kein belegter Zusatznutzen | Planindex/-status |
| Decisions | `docs/project/decisions/` | Nutzer-, Technik- und offene Entscheidungen | kanonisch | kein ADR-Einzelformat fuer grosse Strukturentscheidung | P031-Ownership |
| Obsidian | nicht konfiguriert | private Wissensarbeit | nicht geprueft | Vault-Pfad, Attachment- und Schreibrichtung fehlen | manuelle Freigabe |
| Agenten | `.codex/agents/`, `AGENTS.md` | Runtime-Rollen und Governance | fuenf Rollen | ausreichend; weitere Rollen waeren Overhead | Codex Runtime |
| Skills | `.agents/skills/` | duenne Workflow-Router | zwei versionierbare Skills im uncommitted P031-Working-Tree | passend klein; keine Skillvermehrung ohne Wiederholung | UPDATE_ROUTINES |
| Graphify | nicht vorhanden | spaetere Architekturbeobachtung | nicht ausgefuehrt | Produkt/Version/Lizenz fehlen | positive Allowlist erforderlich |
| Skripte | kein versionierter `scripts/`-Ordner | Hilfsautomation | bewusst entfernt | kein Problem; Skripte nur bei echtem Wiedergebrauch | Projekt-Routinen |
| Notebooks | nicht vorhanden | explorative Forschung | kein Bestand | kein leerer Zielordner erforderlich | spaetere konkrete Analyse |
| generierte Artefakte | `docs/examples/`, lokale `data/*/output` | Referenzgalerien bzw. Ergebnisse | gemischt versioniert/lokal | Referenz, Golden Fixture und Laufoutput klarer kennzeichnen | Plot-/Reporttests |
| GitHub/CI | `.github/agents/` | GitHub-Agentadapter | ohne Workflows | lokale Qualitaet ist nicht remote reproduzierbar | GitHub Actions spaeter |

## Klassifizierte Strukturprobleme

| ID | Kategorie | Befund | Schweregrad | Erwarteter Nutzen einer Korrektur |
| --- | --- | --- | --- | --- |
| AR-01 | falsche fachliche Verantwortung / zu starke Kopplung | `ma_technical` validiert gegen `ma_zones`, waehrend `ma_zones` eine Typreferenz auf Technikrevisionen besitzt | high | gerichtete Uebergabe und isolierbare Tests |
| AR-02 | zyklische Abhaengigkeit / falsche Ownership | `ma_parameters` importiert Katalogmodelle aus `ma_variants`, waehrend Varianten Parameters konsumiert | high | Zielrichtung `parameters -> variants` wird technisch erzwungen |
| AR-03 | nicht reproduzierbarer Prozess | editable Metadatenversion ist veraltet; keine Lock-/Constraints-Datei | high | nachvollziehbare Forschungsumgebung und Releases |
| AR-04 | konkurrierende Source of Truth | Runtime-Abhaengigkeiten stehen abweichend in `pyproject.toml` und `requirements.txt` | high | identische lokale, CI- und Buildumgebung |
| AR-05 | fehlende Tests/Automation | keine `.github/workflows`-Qualitaetspipeline | medium | unabhaengige Reproduktion von Ruff, Tests und Wheel-Smoke-Test |
| AR-06 | Forschung/Produktcode vermischt | Prozessmessung P030 ist geplant, aber noch ohne eigenen versionierten Bereich | medium | Messmethodik beeinflusst keine Fachobjekte |
| AR-07 | falsche fachliche Verantwortung | Economics, Parameterkataloge, IDA-Export und Simulationsergebnisse liegen teilweise in `ma_variants` | high | weniger Kopplung und klarere Evolutionspfade |
| AR-08 | Dokumentationstypen vermischt | Modul-README, How-to, Architektur und Status stehen teilweise nebeneinander | medium | schnellere Orientierung ohne Massenmigration |
| AR-09 | Rohdaten/Ergebnisse vermischt | Modulpfade verwenden unterschiedliche Lebenszyklusbegriffe | medium | reproduzierbare Ableitung und klare Git-Regeln |
| AR-10 | fehlende Provenienz | Run-/Output-Vertraege tragen nicht durchgaengig Parent-Hashes, Tool- und Commitversion | high | belastbarer Vergleich von Dimensionierung und Simulation |
| AR-11 | unnötige Komplexitaet | mehrere Einzeilen-Zielpakete sind vor ihrem MVP-Nutzen sichtbar | low | weniger Kontext; Entscheidung erst nach MVP treffen |
| AR-12 | veraltete Struktur | UI-Kompatibilitaetsfassaden spiegeln Streamlit-Unterpakete per Wildcard | medium | eindeutigere API und weniger versteckte Exporte |
| AR-13 | fehlende Schutzgrenze | Ignore-Luecken bei hypothetischen Analyseinputs, Norm-Unterpfaden sowie `data/catalogs/materials/`, `data/catalogs/products/` und `data/catalogs/sources/` | high | Defense in Depth gegen versehentliches Staging |
| AR-14 | generierte/manuelle Dateien vermischt | versionierte Beispieloutputs liegen in regulaeren Exportpfaden | medium | klare Golden-/Beispiel-/Laufergebnisrollen |
| AR-15 | vorzeitige Abstraktion | Multi-Package-, Plugin- oder Microservice-Umbau hat keinen aktuellen Betriebsgrund | informational | bewusste Nicht-Migration spart Masterarbeitszeit |

## Staerken des aktuellen Systems

- `src/`-Layout, `pyproject.toml`, CLI-Einstiege und Projekt-`.venv` sind eine
  solide Packaging-Basis.
- Fachmodelle, Adaptergrenzen, Diagnosen, Freigabeobjekte und RunManifest
  bilden bereits professionelle Ports-and-Adapters-Bausteine, ohne ein
  Framework aufzuzwingen.
- Planindex, Planstatus, Decisions, Compliance und P031 besitzen geklaerte
  Source-of-Truth-Rollen.
- Versionierte Beispiele sind von den meisten realen Arbeitsdaten getrennt;
  Katalog-, IDA- und Outputpfade sind ueberwiegend ignoriert.
- Die vorhandene Testsuite ist fuer eine Einzelperson und Masterarbeit
  ueberdurchschnittlich breit.

## Audit-Einschraenkungen

- Ignorierte oder proprietaere Inhalte wurden nicht gelesen oder gehasht.
- Der reale Obsidian-Vault wurde mangels Pfad und Attachment-Allowlist nicht
  untersucht.
- Graphify war nicht installiert. Alle Importkanten wurden statisch aus dem
  versionierten Python-Code ermittelt; semantische Kanten sind Empfehlungen,
  keine gemessenen Fakten.
- Der Arbeitsbaum enthielt vor P032 bereits den uncommitted P031-Slice. Der
  P032-Abschluss verwendet deshalb einen pfadspezifischen Diff. Die
  Working-Tree-Testzahl 496 enthaelt sechs noch unversionierte P031-
  Contract-Tests; die versionierte Baseline ohne diese Datei umfasst 490.
