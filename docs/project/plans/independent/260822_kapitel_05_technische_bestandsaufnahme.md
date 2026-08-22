# Unabhaengiger Umsetzungsplan: Technische Bestandsaufnahme fuer Kapitel 5

Datum: 260822
Status: Sol-geplant und qualitaetsgeprueft; noch nicht zur Umsetzung freigegeben

## Arbeits-Prompt

# Finaler Arbeits-Prompt: Technische Bestandsaufnahme für Kapitel 5

## Rolle und Kontext

Du analysierst das bestehende Python-Softwareprojekt der Masterarbeit ausschließlich read-only. Ziel ist eine belastbare, technische Evidenzgrundlage für Kapitel 5 „Prozessoptimierung“. Die wissenschaftliche Einordnung, Priorisierung und endgültige Kapitelstruktur erfolgen anschließend gemeinsam mit ChatGPT.

## Ziel und erwartetes Ergebnis

Erstelle einen vollständigen technischen Bestandsbericht zum aktuellen HEAD-Commit. Der Bericht dokumentiert nachvollziehbar:

- den untersuchten Repository-Stand,
- die aktuelle Projektstruktur und tatsächlich umgesetzte Funktionen,
- die softwaretechnische Abbildung des fachlichen Untersuchungsprozesses,
- Architektur, Datenstruktur, Steuerungslogik, Simulation, Analyse, Bewertung, Reporting und Benutzeroberfläche,
- Entwicklungsprozess, Git-Historie, ChatGPT-/Codex-Rollen sowie agentische Entwicklungsstrukturen,
- Tests, Reproduzierbarkeit, Dependencies, Konfiguration und offene bzw. unfertige Funktionen,
- eine klare Trennung zwischen aktuellem Zustand, historischem/verworfenem Zustand, Planung und unklaren Befunden.

Das Ergebnis wird als eigenständige, datierte Markdown-Datei abgelegt:

`docs/project/analysis/2026-08-22_kapitel_05_technische_bestandsaufnahme.md`

Der Bericht enthält direkt integrierte Tabellen und, wo fachlich sinnvoll, Mermaid-Diagramme. Er soll zugleich als vollständiges, strukturiertes Übergabematerial für ChatGPT nutzbar sein.

## Scope

Untersucht werden:

- der aktuelle HEAD-Commit einschließlich Branch, Commit-Hash, Datum, Tags und Releases,
- die versionierte Repository-Struktur,
- Produktionscode, UI, Tests, Konfiguration, Datenmodelle, Datenhaltung, Workflows, Skripte, Dokumentation, Agents, Skills und Instructions,
- die vollständige versionierte Git-Historie, insbesondere Entwicklungsiterationen, Architekturentscheidungen, Datenhaltung, Modulumbauten, Tests sowie die Entwicklung Tkinter → Streamlit,
- tatsächlich dokumentierte oder technisch belegbare Rollen von Benutzer, ChatGPT und Codex,
- vorhandene agentische Strukturen, Guardrails, Freigaben, Rechte, Tests und technische Nachweise,
- vorhandene Konfiguration und Dependencies ohne Ausgabe sensitiver Werte.

Die vollständige versionierte Git-Historie wird einbezogen, jedoch zielgerichtet hinsichtlich der für Kapitel 5 relevanten Entwicklungsentscheidungen, Architekturänderungen, Funktionsentwicklungen und verworfenen Ansätze ausgewertet.

Historische Befunde werden datensparsam belegt: Commit-Hash, Datum, Commit-Message, betroffene Bereiche und sachliche Zusammenfassung. Kurze nicht-sensitive Auszüge sind nur zulässig, wenn ein Verweis auf Commit, Datei und Funktion nicht genügt.

## Nicht-Ziele und Grenzen

- Keine Änderungen an Produktivcode, Architektur, Daten, Konfiguration oder bestehenden Dokumenten.
- Keine Implementierung fehlender Funktionen und keine Umbenennungen oder Löschungen.
- Keine Ausgabe von Secrets, Tokens, Passwörtern, Zugangsdaten, personenbezogenen oder anderen sensitiven Inhalten.
- Keine Aussagen allein aus Datei-, Modulnamen oder Kommentaren.
- Keine unbelegte Behauptung über MCP, RAG, Memory, VectorDB, Council-Nutzung oder formale Entwicklungsmethodiken.
- Unklare oder nur teilweise belegte Sachverhalte werden ausdrücklich entsprechend gekennzeichnet.
- Historische oder verworfene Funktionen werden nicht als aktueller HEAD-Zustand dargestellt.

## Nachweis- und Qualitätsanforderungen

Jede wesentliche Aussage wird möglichst mit Datei, Klasse, Funktion, Test, Konfiguration, Dokumentation oder Commit belegt. Statusangaben unterscheiden mindestens:

- umgesetzt und funktionsgeprüft
- umgesetzt, Prüfung unvollständig
- teilweise umgesetzt
- strukturell vorbereitet
- geplant / Stub
- nicht mehr verwendet
- unklar

Tests dürfen ausgeführt werden, sofern sie keine persistenten Änderungen an Produktivcode, Konfiguration oder produktiven Daten verursachen. Temporäre Testartefakte sind zulässig, sofern sie anschließend entfernt beziehungsweise durch die Testumgebung verwaltet werden.

## Berichtsinhalte

Der Bericht deckt die im eingereichten Auftrag definierten Bereiche ab, insbesondere Repository-Stand und -Struktur, Entwicklungsprozess, agentische Struktur, Entwicklungswerkzeuge, Reproduzierbarkeit, Libraries, Prozess-Software-Mapping, Datenarchitektur, Stage/Wave/Case/Run-Logik, Module, Simulation, Analyse, Assessment, Reporting, UI, Tkinter → Streamlit, Tests, offene Funktionen, Prozesskennwerte, Anlagenempfehlungen, Haupttext-vs.-Anlage-Empfehlungen und eine abschließende Evidenztabelle.

## Ziel

### Qualitätsbefunde zur Planbarkeit

- **Blocker:** Der Bericht ist ausdrücklich auf einen Commit-Snapshot festgelegt, während der geprüfte Arbeitsbaum bereits nicht zugehörige Änderungen an `CHANGELOG.md`, `docs/project/plans/PLAN_STATUS.md` und einem archivierten Chat-Handover enthält. Eine Auswertung direkt aus dem Arbeitsbaum könnte unversionierte Inhalte als HEAD-Bestand ausgeben. Sämtliche technischen und dokumentarischen Ist-Nachweise müssen deshalb aus dem festgeschriebenen Commit über `git show`, `git grep <Commit>` und `git ls-tree` gelesen oder explizit gegen diesen abgeglichen werden. Die vorhandenen Nutzeränderungen dürfen nicht verändert werden.
- **Blocker:** Die Erstellung des neuen Berichts ist eine Dokumentationsänderung. Sie darf erst nach der wörtlichen Nutzerfreigabe `Freigabe zur Umsetzung` beginnen. Bis dahin bleiben auch das Anlegen von `docs/project/analysis/` und der Berichtsdatei gesperrt.
- **Wichtig:** Zielarchitektur, Planstatus, technische Kataloge und aktueller Code besitzen unterschiedliche Rollen und teilweise unterschiedliche Reifestände. Beispielsweise kennzeichnet `docs/project/architecture/TARGET_ARCHITECTURE.md` zahlreiche Pakete konzeptionell als geplant, während spätere Pläne, Code und Tests bereits Teilumsetzungen belegen. Dokumentstatus darf daher nie ungeprüft als technischer HEAD-Status übernommen werden.
- **Wichtig:** Der Bestand umfasst am geprüften HEAD 67 Commits, 374 Dateien unter `src/` und 95 Testdateien. Der Bericht ist machbar, benötigt aber eine zweistufige Historienanalyse, ein Evidenzregister und feste Qualitäts-Checkpoints, damit die 47 Punkte des Originalauftrags vollständig und zeitlich korrekt abgedeckt werden.
- **Wichtig:** Der lokale semantische Navigationshub war nicht zugänglich. Gemäß `masterarbeit-navigator` wird dies nicht durch einen Scan der externen Arbeitsablage ersetzt. Der Bericht muss diese Nachweisgrenze nennen und darf keine Aussagen über nicht gelesene externe Arbeitsartefakte ableiten.
- **Wichtig:** Die Testsuite verwendet über `tests/conftest.py` temporäre Ordner unter `data/test_output/pytest_runs/`. Die einzelnen Laufordner werden durch die Fixture entfernt; der ignorierte Basisordner kann bestehen bleiben. Vor und nach Tests ist der Dateisystem- und Git-Status zu vergleichen, ohne vorhandene Nutzerartefakte zu löschen.
- **Optional:** Für Mermaid ist im Repository kein verbindlicher Renderer nachgewiesen. Die Diagramme können syntaktisch einfach gehalten und textuell gegengeprüft werden; eine echte Rendering-Prüfung erfolgt nur mit bereits verfügbarer lokaler Technik, ohne Installation oder neue Abhängigkeit.
- **Optional:** Vollständige Lizenz- und Referenzangaben aller Libraries können aus lokalen Metadaten nicht zwingend belastbar abgeleitet werden. Nicht lokal belegbare Angaben bleiben `unklar`; eine Web- oder Literaturrecherche ist nicht stillschweigend Teil dieses Plans.

Ziel ist genau ein deutschsprachiger, technisch belastbarer Bericht:

`docs/project/analysis/2026-08-22_kapitel_05_technische_bestandsaufnahme.md`

Er dokumentiert den festgeschriebenen HEAD-Zustand, rekonstruiert die für Kapitel 5 relevante Entwicklungsgeschichte und stellt alle Aussagen so bereit, dass ChatGPT sie anschließend wissenschaftlich ordnen kann. Der Bericht ist Nachweisstand, keine neue Projektwahrheit und keine ungeprüfte Übertragung der bestehenden Kapitelgliederung auf das Repository.

Als bei der Planung geprüfter Ausgangspunkt gilt:

- Branch: `main`
- HEAD: `c6f7f5fd6c1f712a34e50f3d654525d73966a858`
- Commit-Datum: `2026-08-20T01:11:55+02:00`
- Commit-Message: `Release 0.42.2 - Tagesend-Dokumentation`
- Tag am HEAD: `v0.42.2`

Dieser Bezug wird zu Beginn der späteren Umsetzung erneut read-only geprüft. Ist HEAD dann abweichend, wird nicht stillschweigend auf den neuen Stand gewechselt, sondern angehalten und der Bezugsstand mit dem Nutzer geklärt.

## Scope und Nicht-Ziele

### Scope

Der Auftrag bildet einen einzigen begrenzten Umsetzungsscope:

1. read-only Analyse des festgeschriebenen Repository- und Git-Stands,
2. zulässige lokale Prüfungen ohne persistente Änderungen an Produktivcode, Konfiguration oder produktiven Daten,
3. Erstellung genau des neuen Bestandsberichts.

Untersucht werden ausschließlich erforderliche versionierte Quellen des Repositorys:

- Git-Metadaten: Branches, HEAD, Tags, Releases, lokale Remote-Konfiguration und vollständige Commit-Historie;
- Root- und Build-Dateien: `README.md`, `CHANGELOG.md`, `pyproject.toml`, `requirements.txt`, `.gitignore`, `.gitattributes`, `.pre-commit-config.yaml`, `.streamlit/`, `alembic.ini`;
- Projektsteuerung: `AGENTS.md`, `docs/project/UPDATE_ROUTINES.md`, Planindex, Planstatus, führender Rahmenplan P007, einschlägige P008–P037-Pläne und unabhängige Pläne;
- Entscheidungen und Architektur: `docs/project/decisions/`, `docs/project/architecture/`, `docs/project/workflow/` und Modulsteckbriefe;
- agentische Strukturen: `.agents/`, `.codex/`, `.github/agents/`, `.githooks/` und zugehörige Vertragstests;
- Produktionscode: alle fachlich relevanten Pakete unter `src/`, einschließlich `ma_ui`, `ma_workflow`, Eingabe-, Varianten-, Simulations-, Datenvorbereitungs-, Analyse-, Bewertungs-, Reporting-, Export- und Infrastrukturpakete;
- Daten- und Konfigurationsverträge: versionierte Dateien unter `config/`, `data/`, `migrations/` und `Skripte/`, jedoch keine unversionierten produktiven oder geschützten Daten;
- Tests: vollständiges Inventar unter `tests/` sowie gezielte Zuordnung zu Funktionen, Schnittstellen, Guardrails und Agentensystem;
- historische Quellen: archivierte versionierte Pläne, frühere UI-Dateien und relevante Zustände einzelner Dateien direkt aus Git-Objekten.

### Nicht-Ziele

- keine Änderung von Produktivcode, Architektur, Konfiguration, Daten, Tests, Planindex, Planstatus, Changelog oder bestehenden Dokumenten;
- keine Implementierung, Fehlerbehebung, Refaktorierung, Migration, Umbenennung oder Löschung;
- keine neue Dependency, Installation, Hook-, CI-, MCP-, RAG-, Graph-, Obsidian-, Zotero-, Cloud- oder externe API-Aktion;
- keine Ausführung oder Automatisierung von IDA ICE;
- kein Öffnen vollständiger IDA-/EQUA-Dateien, geschützter Literatur, Normen, Bibliotheken oder externer Arbeitsablagen;
- keine wissenschaftliche Festlegung einer Entwicklungsmethodik oder eines Agenten-Reifegrads;
- keine eigenmächtige Änderung der vorhandenen Kapitel-5-Arbeitsgliederung;
- keine Aufnahme des unabhängigen Plans in `PLAN_INDEX.md` oder `PLAN_STATUS.md`;
- kein Commit, Tag, Push oder Release;
- keine Aussage über ChatGPT-/Codex-Aktivitäten, die nicht durch versionierte Artefakte oder die sichtbare Auftragskette belegt sind.

Die einzige spätere Schreibänderung ist die neue Berichtsdatei einschließlich des vom Nutzer gewünschten neuen Ordners `docs/project/analysis/`. Temporäre, eindeutig testbezogene Artefakte sind nur im ausdrücklich zulässigen Umfang erlaubt.

## Betroffene Bereiche

| Bereich | Primäre Quellen | Untersuchungsziel | Zeitliche Einordnung |
|---|---|---|---|
| Repository-Stand | lokale Git-Metadaten, `pyproject.toml`, Tags | eindeutiger Softwarestand, Version, Sprache, Einstieg, Build | HEAD |
| Repository-Struktur | `git ls-tree`, Root-README | abstrahierter, funktionsbezogener Baum | HEAD |
| Projektwahrheit | P007, `PLAN_INDEX.md`, `PLAN_STATUS.md`, Entscheidungen | Zielbild, aktive Restarbeit, ersetzte Entscheidungen | HEAD-Dokumentstand |
| Architektur | `TARGET_ARCHITECTURE.md`, ADR-P032, Architekturreviews | Ziel-Ist-Grenzen, Owner und Migrationsbedarf | geplant und HEAD getrennt |
| Fachworkflow | `docs/project/workflow/`, `src/ma_workflow/` | Prozessabbildung, Übergänge, Statuskatalog | HEAD |
| Eingaben und Projekt | `ma_project`, `ma_weather`, `ma_building`, `ma_zones`, `ma_technical`, `ma_parameters` | Datenobjekte, Validierung, Snapshots, UI | HEAD |
| Varianten und Runs | `ma_dimensionierung`, `ma_variants`, `ma_simulation_setup` | VSP/VVER/VCAT/VSEL/VGEN, RUN–VAR-Verträge | HEAD |
| Simulation | `ma_export_simulation`, `ma_import_simulation`, IDA-Adapter | manuelle Grenze, Übergabe, Ergebnisaufnahme | HEAD und historisch |
| Datenverarbeitung und Analyse | `ma_data_preparation`, `ma_analyse` | Rohdaten, Normalisierung, KPI, Stages, Diagramme | HEAD |
| Bewertung und Ausgabe | `ma_economy`, `ma_sustainability`, `ma_assessment`, `ma_reporting`, `ma_data_export` | tatsächliche Funktion gegenüber Konzept/Stub | HEAD |
| UI | `ma_ui.streamlit_app`, `ma_ui.tkinter_app` | vollständige Seiten-/Reiterliste und Backend-Bezug | HEAD |
| UI-Historie | Git-Pfade, UD-062, UD-064, P005/P029 | Tkinter → Streamlit/Hybridentwicklung | historisch und HEAD |
| Infrastruktur | `ma_core`, `ma_database`, Konfiguration, Logging, Workspace | Pfade, Persistenz, Fehler, Sessions, Dependencies | HEAD |
| Agentensystem | `AGENTS.md`, `.agents/`, `.codex/`, Hooks, Tests | Rollen, Skills, Rechte, tatsächliche Nutzungsnachweise | HEAD und historisch |
| Qualität | `tests/`, Ruff-/Pytest-Konfiguration | Testtypen, Abdeckung, Ergebnisse, Lücken | HEAD |
| Historie | alle 67 Commits, relevante Pfadhistorien | Entwicklungsphasen, Entscheidungen, Umbauten, verworfene Ansätze | historisch |
| Bericht | neuer Pfad unter `docs/project/analysis/` | vollständige ChatGPT-Übergabe | neuer Nachweisstand |

## Umsetzungsschritte

### 1. Freigabe- und Snapshot-Preflight

1. Auf die ausdrückliche Nutzerformulierung `Freigabe zur Umsetzung` warten.
2. Prüfen, ob der Zielplan vollständig gelesen wurde und der Zielbericht noch nicht existiert.
3. Mit read-only Git-Befehlen erneut Branch, vollständigen HEAD-Hash, Commit-Datum, Commit-Message, Tags, Remotes und Arbeitsbaumstatus erfassen.
4. HEAD gegen `c6f7f5fd6c1f712a34e50f3d654525d73966a858` prüfen. Bei Abweichung anhalten.
5. Den vorhandenen Dirty-Worktree als Arbeitsumgebungsbefund dokumentieren, unversionierte Änderungen aber aus der technischen HEAD-Analyse ausschließen.
6. Eine Baseline aller vorhandenen geänderten und unversionierten Pfade aufnehmen, damit spätere Testartefakte eindeutig von Nutzerdateien unterschieden werden können.
7. Alle folgenden Git-Abfragen mit dem festgeschriebenen Commit ausführen. Aktuelle Dateien aus dem Arbeitsbaum nur für die neue Berichtsdatei verwenden.

### 2. Evidenzschema und Statusregeln festlegen

Der Bericht erhält zu Beginn eine Methodik- und Statuslegende. Jeder wesentliche Befund wird intern nach folgendem Schema geführt:

| Feld | Inhalt |
|---|---|
| Evidenz-ID | fortlaufend `E-001`, `E-002`, … |
| Aussage | knappe technische Aussage |
| Zeitebene | `HEAD-IST`, `HISTORISCH`, `GEPLANT`, `UNKLAR` |
| Umsetzungsstatus | einer der sieben vorgegebenen Statuswerte |
| Evidenztyp | Code, Test, Konfiguration, Dokumentation, Entscheidung, Plan, Commit |
| Primärbeleg | Pfad plus Symbol, Testname oder Commit |
| Ergänzungsbeleg | optionaler zweiter unabhängiger Nachweis |
| Prüfart | statisch geprüft, Aufrufpfad geprüft, Test ausgeführt, historisch rekonstruiert |
| Grenze | Unsicherheit, fehlender Laufzeitnachweis oder Rechtebeschränkung |

Regeln:

- Codeexistenz allein belegt keine Erreichbarkeit oder Funktionsfähigkeit.
- Tests belegen nur den konkret getesteten Vertrag.
- Modulnamen, Kommentare und Pläne belegen keinen aktuellen Funktionsstatus.
- Zielarchitektur und Pläne werden als `GEPLANT` behandelt, bis Code, Aufrufpfad und gegebenenfalls Test den HEAD-Stand bestätigen.
- Historische Dateien werden nur über Commit-Belege als `HISTORISCH` beschrieben.
- Widersprüche bleiben sichtbar; die führende Plan- oder Entscheidungsquelle darf den tatsächlichen Codebestand nicht ersetzen.
- Die abschließende Evidenztabelle verwendet zusätzlich ausschließlich `bestätigt`, `teilweise bestätigt`, `nicht bestätigt` oder `unklar`.

### 3. HEAD-Inventar erheben

1. Mit `git ls-tree -r --name-only <HEAD>` die gesamte versionierte Struktur erfassen.
2. Eine abstrahierte Baumstruktur nach Produktionscode, UI, Tests, Datenmodellen, Datenhaltung, Konfiguration, Dokumentation, Workflow, Agents/Skills, Schnittstellen, Skripten und Archiv bilden.
3. `pyproject.toml`, `requirements.txt`, Startmodule, CLI-Einstiege, Streamlit-Einstiege, Python-Anforderung und direkte Dependencies aus HEAD prüfen.
4. Imports, öffentliche Modelle, Services, Adapter, Persistenzfunktionen, UI-Aufrufe und Tests symbolbezogen untersuchen.
5. Für jeden relevanten Funktionsbereich mindestens einen realen Aufrufpfad von Eingang über Verarbeitung bis Ausgabe rekonstruieren.
6. Nicht eingebundene Pakete, Stubs, `NotImplementedError`, TODO/FIXME, Platzhalter und reine Infoseiten getrennt erfassen.
7. Konfiguration nur strukturell analysieren: Schlüsselname, Kategorie, Speicherort, Zugriff und Sensitivitätsklasse; keine geheimen Werte lesen oder ausgeben.

### 4. Projektwahrheiten und Architektur abgleichen

Die Quellen werden in dieser Reihenfolge bewertet:

1. führender Rahmenplan P007,
2. einschlägige gültige Nutzerentscheidungen und ADRs,
3. aktive Einzelpläne und `PLAN_STATUS.md`,
4. aktueller Code, Konfiguration, Tests und Laufzeitkataloge als Ist-Nachweis,
5. historische und archivierte Quellen nur für Entwicklungsgeschichte.

Für jede behauptete Architekturbeziehung wird dokumentiert:

- Zielowner und aktueller Ist-Owner,
- tatsächliche Imports und Aufrufer,
- Datenvertrag und Persistenzgrenze,
- Testnachweis,
- bekannte Migration oder offene Restarbeit,
- Konflikt zwischen Zielbild und HEAD.

Besonders zu prüfen sind:

- P007-/UD-112-Prozessfolge gegenüber dem realen Aufrufpfad;
- `ma_dimensionierung` gegenüber historischem Stage-1-Owner;
- `ma_parameters` → `ma_variants` → `ma_simulation_setup`;
- direkte `RUN-ID + VAR-ID`-Zuordnung ohne `CASE`;
- `ma_export_simulation`/`ma_import_simulation` und bestehende IDA-Legacypfade;
- `ma_data_preparation` gegenüber älterer Datenvorbereitung in `ma_analyse`;
- geplante beziehungsweise teilweise umgesetzte Economy-, Sustainability-, Assessment- und Reporting-Verträge;
- Workflowstatus gegenüber technischer Paketexistenz;
- UI-neutrale Fachlogik gegenüber UI-eigenen Hilfsfunktionen.

### 5. Vollständige Git-Historie zielgerichtet auswerten

Die Historienanalyse erfolgt zweistufig:

#### Stufe A: vollständige Breitenaufnahme

Alle 67 Commits werden über Hash, Datum, Message, Eltern, Tags, Dateistatistik und betroffene Top-Level-Bereiche aufgenommen. Daraus entsteht eine Chronologie mit Entwicklungsphasen, ohne jeden Commit inhaltlich gleich tief zu prüfen.

Die Chronologie wird mindestens nach folgenden Themen codiert:

- anfängliche Modularisierung und Analysepipeline;
- Plot-Templates und frühe GUI;
- Variantenkern;
- Workflow- und UI-Aufbau;
- Streamlit-Einführung und Tkinter-Auslagerung;
- Eingabe- und Datenhaltungsarchitektur;
- Building/Zones/Technical/Parameters;
- Dimensionierung, Variantenverträge und Run-Paket;
- Simulationsschnittstellen und manuelle IDA-Grenze;
- Datenvorbereitung und PostProcess;
- Agenten-, Skill-, Council- und Freigabestrukturen;
- Tests, Guardrails, Dokumentationshierarchie und Reproduzierbarkeit.

#### Stufe B: vertiefte Entscheidungsanalyse

Nur kapitelrelevante Schlüsselcommits und Pfade werden mit `git show --stat`, `git diff-tree --name-status`, `git log --follow` und gezielten Diffs vertieft. Historische Inhalte werden ohne Checkout direkt aus Git-Objekten gelesen.

Vertieft werden insbesondere:

- Entstehung, Auslagerung und heutiger Restbestand von Tkinter;
- Einführung und Ausbau von Streamlit;
- Verschiebung von UI-Logik aus `ma_analyse` nach `ma_ui`;
- Änderungen an Datenhaltung, Snapshots, Workspace und Katalogen;
- Entstehung von Stage/Wave/Case/Run/Variant-Verträgen und spätere Ablösungen;
- Modulumbauten und Kompatibilitätsadapter;
- Test- und Guardrail-Ausbau;
- Entwicklung von `AGENTS.md`, Skills, Council-Rollen und Freigabegates;
- dokumentierte verworfene Datenbank-, Simulations- oder Automatisierungsansätze.

Für historische Befunde werden standardmäßig nur Hash, Datum, Message, Bereiche und sachliche Änderung ausgegeben. Codeauszüge bleiben Ausnahme.

### 6. Fachprozess, Datenarchitektur und Steuerungslogik rekonstruieren

1. Fachprozessschritte aus dem realen HEAD-Aufrufpfad den Softwarefunktionen zuordnen.
2. Automatisierung, Benutzerinteraktion, manuellen IDA-Schritt, vorbereitete Übergänge und Stubs getrennt markieren.
3. Stage, Wave, Case, Run, Variant, Simulation, Analyse, Verification, Rules, Next Wave und Next Stage einzeln auf Definition, Erzeuger, Verbraucher und Persistenz prüfen.
4. Die tatsächlichen Datenobjekte Project, Building, Zone, Technology, Product, Material, Parameter, Variant, Case, Run, Simulation, Result, KPI, Energy, Economics, Sustainability und Assessment inventarisieren.
5. Produkt- und Materialkataloge auf IDs, Provenienz, Version, Gültigkeit und fachübergreifende Verknüpfung untersuchen.
6. Referenzdaten, Projektdaten, Snapshots, Kopien und mögliche Veränderungswirkungen auf alte Projekte prüfen.
7. Originaldaten, Rohdaten, normalisierte Daten, Zeitreihen, Aggregationen, KPI und Assessment-Ergebnisse als Datenebenen darstellen.
8. Mindestens einen realen Entscheidungsweg von Analyse über Verification/Rules bis Workflow nachvollziehen; existiert kein vollständiger Weg, Teilketten und Lücken getrennt ausgeben.

### 7. Module, Simulation, Analyse, Bewertung und Reporting untersuchen

Für jedes relevante Modul werden Aufgabe, Inputs, Outputs, Abhängigkeiten, Schnittstellen, UI-Bezug, Tests, Status und Belege erhoben.

Schwerpunkte:

- interne Modelle → Adapter → manuelle IDA-ICE-Übergabe → Simulation → Ergebnisimport;
- Bedeutung von Pre-Export, Pre-Simulation, Pre-Simulation-Export, Simulation, Post-Simulation-Export und Post-Simulation-Import;
- Data Preparation, Energie, Komfort, Heating/Cooling, Zeitgewichtung, Tabellen und Visualisierungen;
- Economy, Sustainability, Eligibility, Normalisierung, Scoring, Ranking, Robustheit und Gewichtung;
- Reports, Factsheets, Excel, CSV, PDF, Diagramme, UI-Ergebnisansichten und Datenpakete;
- tatsächlich automatisierte Funktion und Prozesswirkung statt bloßer Librarybeschreibung.

### 8. Benutzeroberfläche und UI-Historie vollständig aufnehmen

1. Alle aktuellen Streamlit-Seiten, Reiter, Unterreiter, Eingabemasken, Aktionen, Ergebnisansichten und Backends erfassen.
2. Alle noch vorhandenen Tkinter-Einstiege, Dialoge und Analyseansichten getrennt erfassen.
3. UI-Infoseiten von ausführbaren Fachansichten unterscheiden.
4. Eine vollständige Screenshot-Checkliste mit stabilen Screenshot-IDs erstellen.
5. Tkinter → Streamlit anhand von Commit-Historie, UD-062, UD-064, P005/P029 und tatsächlichen Pfaden rekonstruieren.
6. Den aktuellen Zustand korrekt als Streamlit-Haupteinstieg mit getrenntem Tkinter-Zweig beschreiben, sofern HEAD dies bestätigt; nicht pauschal von vollständiger Verwerfung sprechen.
7. Technische Vor- und Nachteile nur nennen, wenn sie durch Entscheidungen, Codegrenzen oder Tests belegbar sind.

### 9. Tests und Qualitätssicherung erheben

1. Testdateien und Testfunktionen vollständig inventarisieren und fachlichen Bereichen zuordnen.
2. Unit-, Integrations-, Workflow-, UI-, Regression-, Agent-/Skill-, Rollen-/Berechtigungs- und manuelle Tests unterscheiden.
3. Statische Nachweise von tatsächlich ausgeführten Tests trennen.
4. Testlücken dort ausweisen, wo ein wichtiger Vertrag keine direkte oder nur indirekte Absicherung besitzt.
5. Manuelle Prüfbedarfe nicht als bestandene Tests ausgeben.
6. Die unter `Pruefungen` festgelegte gestufte Testsuite ausführen und Ergebnisse mit Befehl, Zahl der erkannten Tests, bestanden, fehlgeschlagen, übersprungen und Warnungen dokumentieren.

### 10. Tabellenprogramm des Berichts

Der Bericht enthält mindestens folgende Tabellen; ähnliche Tabellen dürfen zusammengeführt werden, wenn alle geforderten Spalten erhalten bleiben:

1. Repository- und Softwarestand;
2. abstrahierte Repository-Bereiche;
3. Entwicklungsartefakte und tatsächliche Nutzung;
4. Merkmale des Entwicklungsprozesses;
5. Rollenabgrenzung Benutzer/ChatGPT/Codex;
6. Agenten-, Skill-, Council-, Hook- und Guardrail-Inventar;
7. Evidenz für 3–5 repräsentative agentengestützte Aufgaben;
8. Entwicklungswerkzeuge;
9. Versionskontrolle und Reproduzierbarkeit;
10. direkte projektrelevante Libraries mit Version, Quelle, Lizenz, Referenz und Nachweis;
11. Konfiguration und Environment ohne Werte;
12. Fachprozess-zu-Software-Mapping;
13. Stage/Wave/Case/Run/Variant/Simulation/Verification/Rules;
14. relevante Datenobjekte und Beziehungen;
15. Produktdaten und fachübergreifende Verknüpfungen;
16. Energy/Economics/Sustainability-Verknüpfung;
17. Factsheet- und Ergebnisblatt-Inventar;
18. Datenhaltungshistorie einschließlich Excel, CSV, JSON, Parquet, SQLite, PostgreSQL, VectorDB und lokaler Dateien;
19. Referenzdaten und Projektsnapshots;
20. Rohdaten-, Normalisierungs-, Zeitreihen-, KPI- und Assessment-Ebenen;
21. Datenprovenienz;
22. Steuerungsebenen und realer Entscheidungsweg;
23. Verification-Strukturen;
24. Rules-Inventar;
25. große Systemarchitekturblöcke;
26. vollständige Modul-Anlagentabelle;
27. Simulationsbegriffe und reale Schnittstellen;
28. Analyseinventar;
29. Assessment-Inventar;
30. Reporting- und Exportfunktionen;
31. vollständige UI- und Screenshot-Anlagentabelle;
32. Tkinter-/Streamlit-Vergleich;
33. technische Infrastruktur;
34. Tests und Testergebnisse;
35. offene, unfertige, experimentelle oder nicht eingebundene Funktionen;
36. Prozesskennwerte und Datenlücken;
37. Haupttext-/Anlage-/Beides-/Nicht-relevant-Empfehlungen;
38. abschließende Evidenztabelle.

Die Library-, Agenten-/Skill-, Modul- und UI-Tabellen erfüllen zugleich die geforderten Anlagentabellen. Redundante Parallelversionen werden vermieden; zusätzliche Spalten wie `Nachweis` bleiben erhalten.

### 11. Mermaid-Diagramme

Nur belegbare Ist-Beziehungen werden als durchgezogene Verbindungen dargestellt. Historische, geplante und unklare Elemente erhalten sichtbare Präfixe oder eine Legende.

Vorgesehen sind:

1. abstrahierte HEAD-Systemarchitektur;
2. fachlicher Prozess → Softwareprozess mit Benutzerinteraktion und manueller IDA-Grenze;
3. ER-Diagramm der tatsächlich vorhandenen zentralen Datenobjekte;
4. realer Datenfluss Product/Variant/Simulation → Energy/Economics/Sustainability → Assessment;
5. Stage/Wave/Case/Run/Variant-Lebenszyklus einschließlich fehlender oder verworfener Konzepte;
6. Simulationsschnittstelle vom internen Modell bis zur Ergebnisrückführung;
7. real belegter Steuerungs- beziehungsweise Entscheidungsweg;
8. Entwicklungszeitstrahl Tkinter → Streamlit/getrennter Hybridstand;
9. belegbarer Entwicklungszyklus Benutzer/ChatGPT/Codex/Tests/UI-Prüfung.

Kann eine Beziehung nicht ausreichend belegt werden, wird kein scheinbar vollständiges Diagramm erzeugt; stattdessen wird die Lücke textlich und tabellarisch ausgewiesen.

### 12. Bericht aufbauen

Der Bericht wird in folgender Hauptstruktur erstellt:

1. Untersuchungsrahmen, Snapshot und Evidenzmethodik
2. Repository-Struktur
3. Entwicklungsprozess
4. Agentische Entwicklungsstruktur
5. Entwicklungswerkzeuge
6. Reproduzierbarkeit, Git und GitHub
7. Libraries und Konfiguration
8. Fachlicher Prozess → Softwareprozess
9. Datenarchitektur
10. Produktdaten
11. Energy, Economics und Sustainability
12. Factsheets
13. Datenhaltung und Datenbankhistorie
14. Datenprovenienz
15. Prozesssteuerung, Verification und Rules
16. Stage-, Wave-, Case- und Run-Logik
17. Modul- und Systemarchitektur
18. Simulationsanbindung
19. Analyse
20. Assessment
21. Reporting und Export
22. Benutzeroberfläche
23. Entwicklung Tkinter → Streamlit
24. Tests und Qualitätssicherung
25. Offene, unfertige und verworfene Funktionen
26. Prozesskennwerte
27. Vorgeschlagene Anlagen
28. Haupttext-vs.-Anlage-Empfehlungen
29. Offene technische Fragen
30. Abschließende Evidenztabelle

Die bestehende Kapitel-5-Arbeitsstruktur wird lediglich in Abschnitt 28 gespiegelt. Falls der technische Bestand eine andere Gruppierung nahelegt, wird diese als Alternativvorschlag gekennzeichnet und nicht als neue Kapitelentscheidung ausgegeben.

### 13. Checkpointing und Qualitätssicherung

Der umfangreiche Bericht wird in kontrollierten Paketen erstellt:

- **Checkpoint A:** Snapshot, Evidenzschema, Repository-Struktur und Quellenhierarchie;
- **Checkpoint B:** Entwicklungsprozess, Agentensystem, Werkzeuge und Reproduzierbarkeit;
- **Checkpoint C:** Prozessabbildung, Datenobjekte, Datenhaltung und Provenienz;
- **Checkpoint D:** Module, Steuerung, Simulation, Analyse, Assessment und Reporting;
- **Checkpoint E:** UI, UI-Historie, Tests, offene Funktionen und Prozesskennwerte;
- **Checkpoint F:** Anlagenempfehlungen, Evidenztabelle und Gesamtprüfung.

Nach jedem Checkpoint:

1. nur den neuen Berichtsabschnitt gegen die Evidenzmatrix prüfen;
2. jeden Pfad gegen den festgeschriebenen Commit validieren;
3. aktuelle, historische, geplante und unklare Aussagen auf Vermischung prüfen;
4. Tabellen auf vollständige Pflichtspalten prüfen;
5. Mermaid-Knoten gegen die zugehörigen Tabellen abgleichen;
6. Wiederholungen reduzieren, ohne geforderte Inhalte zu verlieren;
7. `git diff --check` und einen gezielten Diff nur für die Berichtsdatei prüfen;
8. sicherstellen, dass vorhandene Nutzeränderungen unverändert geblieben sind.

Am Ende folgt eine Claim-by-Claim-Stichprobe: jede Hauptschlussfolgerung benötigt mindestens einen Primärbeleg; Architektur- und Funktionsaussagen möglichst Code plus Test beziehungsweise Code plus Aufrufpfad.

## Pruefungen

### Read-only Bestandsprüfungen

- `git rev-parse HEAD`
- `git show -s --format=... <HEAD>`
- `git tag --points-at <HEAD>`
- `git branch --all`
- `git remote -v`
- `git status --short --branch`
- `git ls-tree -r --name-only <HEAD>`
- `git rev-list --count <HEAD>`
- vollständiges `git log` in chronologischer Reihenfolge
- gezielte `git log --follow`, `git show` und `git diff-tree` für Schlüsselpfade
- symbolbezogene Suche mit `git grep <HEAD>` und gezieltes Lesen über `git show <HEAD>:<Pfad>`

### Gestufte Code- und Testprüfung

Vor jedem Testlauf wird der vorhandene Git- und Artefaktstatus gespeichert.

1. Laufzeitumgebung prüfen:
   - `py --version` beziehungsweise verfügbarer lokaler Python-Aufruf;
   - deklarierte Python-Version aus `pyproject.toml`;
   - installierte Versionen direkter Dependencies über lokale Paketmetadaten, soweit verfügbar.
2. Testsammlung:
   - `py -m pytest --collect-only -q`
3. Fokussierte Struktur- und Agententests:
   - `tests/test_architecture_guardrails.py`
   - `tests/test_project_agent_system.py`
   - `tests/test_target_module_structure.py`
   - `tests/test_ma_workflow.py`
   - `tests/test_p037_workflow_information.py`
4. Fokussierte UI-/Migrationsverträge:
   - `tests/test_ma_ui_shell.py`
   - `tests/test_ma_analyse_services.py`
   - `tests/test_ma_analyse_commands.py`
5. Fokussierte Daten-, Varianten-, Run- und Simulationsverträge:
   - relevante Tests zu `ma_core`, `ma_project`, `ma_parameters`, `ma_variants`, `ma_simulation_setup`, `ma_import_simulation`, `ma_data_preparation` und `ma_analyse`.
6. Vollständige Suite:
   - `py -m pytest -q`
7. Statische Prüfungen, sofern Ruff bereits installiert ist:
   - `py -m ruff check src tests --no-cache`
   - `py -m ruff format --check src tests --no-cache`

Ein fehlendes lokales Tool oder eine nicht passende Python-Version wird als Prüfgrenze dokumentiert; es wird nichts installiert.

### Umgang mit temporären Testartefakten

- Pytest verwendet gemäß `tests/conftest.py` `data/test_output/pytest_runs/`.
- Vorhandene Test- oder Nutzerartefakte werden nicht gelöscht.
- Die Fixture verwaltet und entfernt ihre UUID-Laufordner selbst.
- Nach jedem Lauf werden Git-Status und neu entstandene Pfade gegen die Baseline verglichen.
- Nur eindeutig durch diesen Lauf neu erzeugte, nicht von der Testumgebung entfernte temporäre Artefakte dürfen innerhalb des freigegebenen Umfangs gezielt entfernt werden.
- Produktivcode, Konfiguration, produktive Daten, bestehende lokale Testdaten und Nutzeränderungen bleiben unberührt.
- Testfehler oder Cleanup-Probleme werden dokumentiert und nicht durch Codeänderungen behoben.

### Berichtsprüfung

- Zieldatei existiert genau einmal am vereinbarten Pfad.
- Markdown-Überschriften und Tabellen sind strukturell vollständig.
- Mermaid-Blöcke verwenden einfache, konsistente Syntax.
- Alle sieben Umsetzungsstatus und alle vier Evidenzstatus sind eindeutig definiert.
- Jede aktuelle Funktionsaussage verweist auf HEAD-Code und, wo vorhanden, Test oder Aufrufpfad.
- Jede historische Aussage verweist auf Commit und Datum.
- Kein historischer oder geplanter Zustand wird als HEAD-Funktion ausgegeben.
- Keine sensitiven Werte, Volltexte, personenbezogenen Angaben oder geschützten Inhalte werden reproduziert.
- Keine externen Pfade werden in das für ChatGPT bestimmte Übergabematerial aufgenommen.
- `git diff --check -- docs/project/analysis/2026-08-22_kapitel_05_technische_bestandsaufnahme.md`
- abschließender `git status --short` gegen die Preflight-Baseline;
- abschließender Diff bestätigt, dass aus diesem Auftrag ausschließlich die neue Berichtsdatei hinzugekommen ist.

## Risiken und offene Entscheidungen

- **Blocker – Freigabe fehlt:** Ohne `Freigabe zur Umsetzung` darf der Bericht nicht angelegt werden.
- **Blocker – Snapshot-Drift:** Weicht HEAD bei Umsetzungsbeginn vom festgeschriebenen Hash ab, muss der Nutzer entscheiden, ob der ursprüngliche Snapshot oder der neue HEAD untersucht wird.
- **Blocker – Arbeitsbaumvermischung:** Die bereits vorhandenen Änderungen dürfen weder in den HEAD-Bericht einfließen noch überschrieben werden. Ist die Zieldatei bei Umsetzungsbeginn bereits anderweitig vorhanden oder verändert, muss angehalten werden.
- **Blocker – Rechtegrenze:** Erfordert eine Aussage das Öffnen geschützter Normen, vollständiger IDA-/EQUA-Dateien, Bibliotheken oder nicht freigegebener externer Inhalte, bleibt sie `unklar`. Der Berichtsumfang wird nicht durch einen unzulässigen Zugriff erweitert.
- **Wichtig – Quellenkonflikte:** Zielarchitektur, Workflowstatus, Pläne und Code können abweichen. Der Bericht muss Ziel, dokumentierten Planstand und tatsächlichen HEAD-Bestand nebeneinander zeigen.
- **Wichtig – Funktionsstatus:** Paketexistenz, Streamlit-Infoseite oder Testdateiname sind kein Funktionsnachweis. Erreichbarkeit, Verarbeitung und Ausgabe müssen symbol- und aufrufpfadbezogen geprüft werden.
- **Wichtig – Historienselektivität:** Die vollständige Historie wird erfasst, aber nur kapitelrelevante Schlüsselcommits werden tief analysiert. Das Auswahlkriterium und ausgelassene Detailtiefe werden transparent beschrieben.
- **Wichtig – ChatGPT/Codex-Nachweis:** Versionierte Entscheidungen können Chatbezüge enthalten, belegen aber nicht automatisch vollständige Chatverläufe oder konkrete Tool-Orchestrierung. Nicht belegbare Rollenanteile bleiben `unklar`.
- **Wichtig – Reifegradmodell:** Technische Merkmale dürfen gesammelt werden; eine endgültige wissenschaftliche Einstufung bleibt ChatGPT und der späteren Ausarbeitung vorbehalten.
- **Wichtig – GitHub/CI:** Lokale Git-Remotes und versionierte GitHub-Artefakte belegen keine tatsächliche Remote-Nutzung, CI-Ausführung, PR- oder Issue-Praxis. Ohne lokalen Nachweis wird dies nicht behauptet.
- **Wichtig – Testreichweite:** Automatisierte Tests ersetzen keine manuelle Streamlit-, Tkinter- oder IDA-Prüfung. Fehlende manuelle Prüfungen werden als solche ausgewiesen.
- **Wichtig – Prozesskennwerte:** Vorhandene Logs und Messvorlagen dürfen nicht zu erfundenen Zeit- oder Effizienzkennwerten verdichtet werden. Fehlende Messdaten bleiben Lücke.
- **Wichtig – Umfang:** Ein einzelner umfangreicher Bericht birgt Inkonsistenz- und Redundanzrisiko. Die sechs Checkpoints und die abschließende Evidenztabelle sind verbindlich.
- **Optional – Diagrammrendering:** Ohne vorhandenen Renderer bleibt die Prüfung auf einfache Mermaid-Syntax und Konsistenz mit den Tabellen beschränkt.
- **Optional – Librarylizenzen:** Lokal nicht sicher belegbare Lizenzen und Referenzen bleiben `unklar`. Eine separate Quellenrecherche kann später beauftragt werden.
- **Optional – Alternativgliederung:** Eine technisch günstigere Gruppierung darf ergänzend empfohlen werden, ändert aber nicht die bestehende Arbeitsgliederung.

Es bestehen keine offenen fachlichen Entscheidungen, die die read-only Bestandsaufnahme selbst verhindern. Die zwei operativen Voraussetzungen sind die ausdrückliche Freigabe und der unveränderte Snapshot.

## Tera-Uebergabe

Vorgesehener Planpfad:

`docs/project/plans/independent/260822_kapitel_05_technische_bestandsaufnahme.md`

Übergabeprompt für einen neuen Tera-Chat:

```text
Setze den freigegebenen unabhängigen Umsetzungsplan
`docs/project/plans/independent/260822_kapitel_05_technische_bestandsaufnahme.md` um.

Lies den Plan vollständig. Prüfe den aktuellen Bestand nur im darin benannten
Scope. Setze ausschließlich die freigegebenen Schritte um, führe die
vorgesehenen Prüfungen aus und dokumentiere Abweichungen. Halte an, falls
eine Scope-Erweiterung, neue Abhängigkeit, Löschung oder externe Aktion nötig
wird.
```

Die Umsetzung beginnt ausschließlich nach `Freigabe zur Umsetzung`. Nach Abschluss fragt Tera den Nutzer, ob der unabhängige Plan als abgeschlossener Einzelplan bestehen bleibt, einem benannten formellen Plan zugeordnet oder über `plan aufnehmen` in die formelle Planstruktur überführt werden soll.
