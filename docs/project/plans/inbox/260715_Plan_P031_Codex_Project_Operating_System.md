# P031 Codex Project Operating System

Stand: 2026-07-22
Status: lokale Baseline umgesetzt und validiert; externe Integrationen gesperrt
Profil: Full Local, repo-lokal und allowlist-basiert

## Zweck

P031 ordnet die bestehende Codex-Steuerung zu einem kleinen, pruefbaren
Project Operating System. Der Plan ist der einzige aktive Traeger fuer den
datierten Repository-Audit, das temporaere Konfliktregister, den
Capability-Snapshot und den Master-System-Backlog.

Dieser Plan erteilt keine technische, fachliche, rechtliche oder
vertragliche Freigabe. Verbindliche Arbeitsregeln bleiben in `AGENTS.md`,
Ablaufregeln in `docs/project/UPDATE_ROUTINES.md`, Entscheidungen in
`docs/project/decisions/` und Rechteentscheidungen in `docs/compliance/`.

Der externe Master-Prompt aus einem lokalen Download-Verzeichnis wird nicht
in das Repository kopiert oder veroeffentlicht. P031 uebernimmt nur den vom
Nutzer im Chat freigegebenen, fuer dieses Repository bereinigten Auftrag.

## Strukturentscheidung des Councils

Der Council hat drei Varianten geprueft:

1. sechs neue dauerhafte Audit- und Betriebsdateien unter einem neuen
   Dokumentationsbaum;
2. Project-OS-Dokumentation unter `.codex/`;
3. ein einziger aktiver P031-Plan mit Verweisen auf bestehende Wahrheiten.

Einstimmig gewaehlt wurde Variante 3. Sie vermeidet eine dritte Status-,
Entscheidungs- oder Compliance-Wahrheit und passt zur bestehenden
Projektorganisation.

## Ownership und Source of Truth

| Gegenstand | Fuehrende Quelle | Abgrenzung |
| --- | --- | --- |
| dauerhafte Arbeits- und Freigaberegeln | `AGENTS.md` | knapper Router, keine Detailroutine |
| Codex-Runtime | `.codex/config.toml` | Modell, Sandbox, Netzwerk und Agentenlimits |
| Codex-Rollen | `.codex/agents/*.toml` | ausfuehrbare projektbezogene Rollen |
| wiederkehrende Workflows | `.agents/skills/*/SKILL.md` | duenne Router auf die Ablaufwahrheit |
| Ablaufwahrheit | `docs/project/UPDATE_ROUTINES.md` | vollstaendige Schritte und Gates |
| Triggerindex | `docs/common/commands_common.md` | Ausloesephrasen und Kurzverweise |
| Planinventar | `docs/project/plans/PLAN_INDEX.md` | genau ein Eintrag je Plan |
| aktive Arbeitslage | `docs/project/plans/PLAN_STATUS.md` | aktueller Gesamtstatus einschliesslich Kontext |
| aktiver Project-OS-Audit und Backlog | dieser P031-Plan | datierter, nicht autorisierender Arbeitsstand |
| Aenderungsgrenzen | `docs/project/plans/CLEANUP_PLAN.md` | sicher, freigabepflichtig, nicht anfassen |
| Nutzer- und Technikentscheidungen | `docs/project/decisions/` | Historie, Rationale und offene Entscheidungen |
| Rechte- und Verarbeitungsgrenzen | `docs/compliance/` | alleinige Compliance-Instanz |
| Modul- und Workflow-Laufzeitstatus | `src/ma_workflow/catalog.py` | UI- und Runtime-Anzeige |
| Orientierung | `docs/project/MASTERARBEIT_LEITFADEN.md` | keine zweite Statusquelle |
| Aenderungshistorie | `CHANGELOG.md` | umgesetzte, versionierbare Aenderungen |
| historische Chat-Uebergaben | `docs/project/archive/chat_handovers/INDEX.md` | archivierte Arbeitsreferenzen, nie aktive Status- oder Entscheidungsquelle |

Die Professor-Rolle besitzt zwei benoetigte Produktoberflaechen:
`.codex/agents/professor.toml` ist fuer Codex fuehrend;
`.github/agents/Professor.md` bleibt ein gekennzeichneter GitHub-Adapter.
Governance und Freigabegrenzen werden nicht in beiden Rollen neu erfunden,
sondern aus `AGENTS.md` abgeleitet.

### Zuordnung der vorgeschlagenen Parallelpfade

| Urspruenglich vorgeschlagener Pruefpfad | Kanonische Loesung |
| --- | --- |
| `AGENT_SYSTEM_OPERATIONS.md` | `AGENTS.md` fuer Governance und `docs/project/UPDATE_ROUTINES.md` fuer Ablaeufe |
| `docs/handover/AGENT_SYSTEM_HANDOVER.md` | P031 fuer Audit/Backlog und `PLAN_STATUS.md` fuer die aktive Arbeitslage |
| `docs/agents/AGENT_TEAM.md` | `AGENTS.md` plus die ausfuehrbaren Rollen unter `.codex/agents/` |
| `.agents/skills/README.md` | wird als reiner Skill-Katalog angelegt |
| `docs/architecture/SOURCE_OF_TRUTH.md` | diese Ownership-Tabelle plus die bestehende `docs/project/architecture/` |
| `docs/architecture/OBSIDIAN_STRATEGY.md` | P031-M3 und OP-016 bleiben bis zur Pfad-/Schreibfreigabe offen |
| `docs/graphify/FIRST_GRAPH_EVALUATION.md` | Tool-Capability-Audit und P031-M4; noch keine Produktauswahl oder Ausfuehrung |
| `graphify-out/graph.html` | nicht erzeugt, weil Graphify fehlt und Scope/Lizenz nicht freigegeben sind |

Die nicht angelegten Pfade sind damit keine fehlenden Ergebnisse, sondern
bewusst vermiedene Parallelwahrheiten oder noch gesperrte externe Artefakte.

## Repository Audit

### Bestaetigter Bestand

- Root-`AGENTS.md` und fuenf projektlokale Agentenrollen sind vorhanden.
- Explorer, Quality, Professor und Compliance sind read-only; nur der
  freigabegebundene Implementation Engineer darf im Workspace schreiben.
- `.codex/config.toml` setzt `max_threads = 3`, `max_depth = 1`,
  `sandbox_mode = "workspace-write"`, `approval_policy = "on-request"` und
  deaktiviert Projekt-Netzwerkzugriff.
- Plan-, Entscheidungs-, Architektur- und Compliance-Strukturen sind bereits
  kanonisch unter `docs/project/` beziehungsweise `docs/compliance/` geordnet.
- Geschuetzte Norm-, IDA-, Katalog- und Projektdaten liegen teilweise lokal
  und ignoriert im Worktree. `.gitignore` verhindert ihre Versionierung, aber
  nicht ihren Zugriff durch einen Scanner.
- Zu Beginn des Audits fehlten repo-lokale Skills und Contract-Tests fuer das
  Agentensystem.

### Strukturelle Bewertung

- Das bestehende fuenfkoepfige Council bleibt die kanonische Teamstruktur.
  Weitere Rollen werden nicht parallel angelegt, solange keine eigenstaendige
  Aufgabe und Freigabe belegt ist.
- Neue Skills muessen auf bestehende Dokumente routen und duerfen keine
  Ablauf- oder Freigabelogik kopieren.
- Allgemeine Scanner, Graphen und Skill-Helfer erhalten standardmaessig nur
  die positive Allowlist aus `git ls-files`.
- Historische Reviews und Weekly Reviews bleiben Snapshots; sie werden nicht
  zur aktuellen Wahrheit hochgestuft.

## Conflict Register

| ID | Konflikt | Beschluss | Status |
| --- | --- | --- | --- |
| P031-C01 | `IMPLEMENTATION_NOTES.md` startete bei `tagesstart` die UI, die aktuelle Routine verbietet dies. | `UPDATE_ROUTINES.md` ist fuehrend; die alte Startregel wird entfernt. | geschlossen |
| P031-C02 | `data/common/normen/README.md` erlaubte ChatGPT-Auswertung und automatische Extraktion entgegen der DIN-/Nautos-Policy. | README auf Metadaten-, Rechte- und Reviewablage begrenzen; KI/OCR/RAG bleiben gesperrt. | geschlossen |
| P031-C03 | Professor-Rolle liegt unter `.codex/agents/` und `.github/agents/`. | Codex-TOML ist fuer Codex fuehrend; GitHub-Datei ist ein gekennzeichneter Surface-Adapter. | geschlossen |
| P031-C04 | Routinen stehen in mehreren Dokumenten. | `UPDATE_ROUTINES.md` ist Ablaufwahrheit; `commands_common.md` ist Triggerindex; Decisions dokumentieren nur das Warum. | geschlossen |
| P031-C05 | `plans/README.md` beschrieb `PLAN_STATUS` und `STRUCTURE_REVIEW` nicht mehr passend. | README auf Gesamtstatus und historischen Strukturreview korrigieren. | geschlossen |
| P031-C06 | Der externe Master-Prompt forderte neue Root-/Parallelpfade. | Anforderungen werden in P031 und bestehenden Pfaden integriert; keine parallelen Status-/Architekturwahrheiten. | geschlossen |
| P031-C07 | Repo-lokale Skills fehlten. | Zwei duenne, offiziell strukturierte Skills unter `.agents/skills/` anlegen. | geschlossen |
| P031-C08 | Contract-Test fuer Runtime, Rollen, Skills und Trigger fehlte. | Allowlist-basierten Test hinzufuegen. | geschlossen |
| P031-C09 | `keine Hooks` kollidiert mit dem bereits lokal aktiven Git-`core.hooksPath=.githooks`. | Bestand weder aktivieren noch deaktivieren; Git- und Codex-Hooks vor jeder Aenderung getrennt freigeben. | manuell offen |
| P031-C10 | Projektconfig hat kein MCP, die aktuelle Sitzung stellt dennoch ein geerbtes OpenAI-Dokumentationswerkzeug bereit. | Projektkonfiguration, effektive Sitzung und externe Aktion getrennt dokumentieren; keine neue MCP-Konfiguration. | manuell offen |

## Tool Capability Audit

Snapshot vom 2026-07-15; ohne Tokens, globale Konfigurationswerte oder
absolute Nutzerpfade.

| Werkzeug oder Grenze | Stand | Project-OS-Folge |
| --- | --- | --- |
| Git | 2.54.0 | lokal verfuegbar |
| Codex CLI | 0.144.2 | verfuegbar; Temp-Alias-Cleanup meldete eine nicht blockierende Berechtigungswarnung |
| Projekt-Python | 3.14.0 in `.venv` | fuer Tests und Validatoren verwenden |
| Ruff | 0.15.14 | verfuegbar |
| Pytest | 9.0.3 | verfuegbar |
| Node.js / npm | nicht gefunden | keine Node-basierte Integration installieren |
| Graphify / Graphviz / `dot` | nicht gefunden | Installation, Lizenz und Scope manuell freigeben |
| GitHub CLI `gh` | nicht gefunden | keine CLI-Abhaengigkeit einfuehren |
| Pandoc / `pdftotext` / Tesseract | nicht gefunden | keine PDF-Pipeline installieren oder starten |
| Obsidian-CLI | nicht gefunden | Vault-Pfad und Schreibstrategie fehlen |
| Zotero-Anbindung | nicht projektkonfiguriert | Schreibzugriff gesperrt |
| Codex-MCP im Repo | nicht konfiguriert | keine neue Projektaktivierung |
| effektives Docs-Werkzeug | in dieser Sitzung bereitgestellt | nicht als Projekt-MCP oder allgemeine Freigabe behandeln |
| Git-Hook | `core.hooksPath=.githooks` lokal aktiv | weder voraussetzen noch aendern |
| `graphify-out/` | nicht vorhanden | kein Graph erzeugt |

## Manuelle Freigabematrix

Die Matrix ist ein Arbeitsrouter und keine `compliance_decision`.

### Frei im bereits freigegebenen Repo-Umfang

- versionierte eigene Dateien lesen und mit `git ls-files` durchsuchen;
- Git-Status, Diff, Log, lokale Runtime- und Hook-Metadaten read-only pruefen;
- eigene Projektplanung, Dokumentation, Skills und Tests innerhalb des
  freigegebenen P031-Slices aendern;
- Projekt-`.venv`, Ruff, Pytest und lokale read-only Validatoren ausfuehren;
- unbekannte Dateien nur anhand bereinigter Metadaten vorpruefen.

### Frische menschliche Freigabe erforderlich

- globale `~/.codex`-Dateien lesen oder aendern;
- Programme, Pakete, Plugins oder neue Abhaengigkeiten installieren;
- Git- oder Codex-Hooks aktivieren, deaktivieren oder veraendern;
- MCP konfigurieren oder aktivieren;
- Graphify installieren, den Eingabe-Scope festlegen, Watch aktivieren oder
  Graphen erzeugen;
- Obsidian- oder Zotero-Pfade festlegen und dort schreiben;
- externe APIs, Cloud-Dienste, Schluessel oder Netzwerkzugriff verwenden;
- einen neuen Project-OS-Stand committen, pushen oder veroeffentlichen;
- bestehende Agentenlimits oder grundlegende fachliche Entscheidungen
  aendern.

### Vorerst blockiert, bis Rechte und Scope belegt sind

- worktree-weites Graphifizieren oder Indexieren ignorierter Daten;
- Normen- oder geschuetzte Literatur-PDFs per KI, OCR, Extraktion,
  Uebersetzung, Graph, Embeddings, RAG oder Cloud verarbeiten;
- vollstaendige `.idm`, IDA-Bibliotheken oder NMF-Dateien analysieren,
  spiegeln, hochladen oder rekonstruieren;
- IDA ICE automatisch starten, im Batch oder als Server betreiben;
- direkte Zotero-Datenbankzugriffe oder bidirektionale Vault-Synchronisation;
- Secrets, Tokens, Lizenzschluessel oder Zugangskennungen in Repo, Prompt,
  Graph oder Audit uebernehmen;
- geschuetzte Volltexte, Rekonstruktionsgraphen, Embeddings oder reale
  Arbeitsdaten veroeffentlichen.

Die im Ausgangsauftrag vorgeschlagene lokale PDF-Analyse ersetzt keinen
Rechtebeleg. Eigene oder passend lizenzierte Literatur kann erst nach einer
objektbezogenen Entscheidung in einen begrenzten lokalen Prozess wechseln.

## Full-Local-Betriebsprofil

| Parameter | Aktueller Beschluss |
| --- | --- |
| Implementierungsprofil | `full_local` fuer eigene versionierte Repo-Inhalte |
| parallele Council-Arbeit | bestehendes `max_threads = 3`; Erhoehung auf 4 bleibt manuell |
| Agententiefe | `max_depth = 1` |
| maximale Council-Diskussionsrunden | 3 fuer diesen Integrationslauf |
| maximale Rueckfragerunden | 3; nur bei echten manuellen Gates |
| maximale Nacharbeitsrunden | 4 |
| Normen-PDF-Analyse | trotz Ausgangsvorschlag gesperrt, bis Rechte belegt sind |
| Literatur-PDF-Analyse | nur objektbezogen nach Rechte- und Inhaltsfreigabe |
| externe PDF-Cloudverarbeitung | deaktiviert |
| Graphify Hooks / Watch | deaktiviert |
| MCP | nicht repo-lokal konfiguriert; effektive Sitzung und geerbte Werkzeuge getrennt betrachten |
| Auto-Commit / Auto-Push | fuer P031 deaktiviert |

## Master-System Backlog

| ID | Paket | Status | Abnahme |
| --- | --- | --- | --- |
| P031-S0 | katalogfreies Release `v0.28.0` | abgeschlossen | Remote-Branch und Tag zeigen auf denselben Commit; Katalogdaten bleiben ignoriert |
| P031-S1 | Audit, Strukturkonsens und Dokumentbereinigung | abgeschlossen | Konflikte C01-C08 geschlossen; C09-C10 bleiben als manuelle Grenzen sichtbar; Planindex, Planstatus, Decisions und Changelog synchron |
| P031-S2 | repo-lokale Skills | abgeschlossen | zwei Skills ohne TODOs; offizieller Validator gruen |
| P031-S3 | Agent-System-Contract-Test | abgeschlossen | TOML, Rollenrechte, Skills, Trigger und Allowlist-Grenzen mit 6 Tests geprueft |
| P031-S4 | read-only Demonstrationslauf | abgeschlossen | beide Skill-Router ohne externe oder geschuetzte Daten erfolgreich vorwaerts getestet |
| P031-S5 | Abschlussaudit | abgeschlossen | Diff, Tests, Council-Reviews, offene Gates und nicht erzeugte externe Artefakte dokumentiert |
| P031-M1 | Bedeutung von `keine Hooks` | manuell | Git- und Codex-Hooks getrennt entschieden |
| P031-M2 | effektive MCP-Grenze | manuell | geerbte Sitzungstools und Projektconfig bewusst abgegrenzt |
| P031-M3 | Obsidian-/Zotero-Strategie | manuell | Vault/Collection, Backup, Richtung und Schreibumfang freigegeben |
| P031-M4 | Graphify-Evaluation | blockiert | Produkt, Version, Lizenz, Datenfluss, Code-Allowlist und Ausgabeort belegt |
| P031-M5 | Normen-/Literatur-PDFs | blockiert | Rechte fuer Maschine, KI, Ablage und Ausgabe objektbezogen belegt |
| P031-M6 | IDA-/Simulationseingaben | blockiert | EQUA-/Drittrechte und erlaubter Parser-/Automatisierungsumfang belegt |
| P031-M7 | Project-OS-Compliance-Fachprofil | spaeter | erst bei konkreter externer Komponente als eigener freigegebener Slice |
| P031-M8 | Council-Mehrheitsfreigabe fuer interne Folgeslices | getroffen | UD-089: mindestens drei von fuenf Council-Rollen empfehlen den exakten lokalen, reversiblen Scope; Sondergates bleiben separat |

## Demonstrationsergebnis 2026-07-15

- Der Governance-Skill ordnete P031, Planindex, Planstatus, Decisions,
  Compliance, Runtime und Rollen korrekt ihren fuehrenden Quellen zu und
  meldete die manuellen Gates, ohne Dateien zu veraendern.
- Der Release-Skill verwendete `UPDATE_ROUTINES.md` statt des Triggerindex als
  Ablaufquelle. Er stoppte den aktuellen unversionierten P031-Arbeitsstand
  korrekt, weil keine neue release-spezifische Compliance-Entscheidung
  vorliegt. Es erfolgte keine Git-Aktion.
- Beide Skill-Verzeichnisse bestanden den offiziellen `quick_validate.py`.
- Der fokussierte Contract-Test bestand mit `6 passed`.
- Der projektweite Ruff-Lauf bestand.
- Die vollstaendige Testsuite bestand mit `496 passed` in 166,68 Sekunden.
- Der Demonstrationslauf las keine ignorierten Norm-, IDA- oder Katalogdaten
  und aktivierte keine externen Komponenten.

## Abschlussaudit 2026-07-15

- Der finale Contract-Test bestand nach allen Nacharbeiten mit `6 passed`;
  der projektweite Ruff-Lauf, beide offiziellen Skill-Validatoren und
  `git diff --check` waren gruen.
- Der unabhaengige Qualitaetsreview meldete nach der Korrektur von
  MCP-Formulierung, Triggervertrag und Einzigkeitspruefung keine verbleibenden
  Blocker, wichtigen oder optionalen Befunde.
- Der unabhaengige Compliance-Review meldete keine materiellen Befunde. Er
  erteilte keine Release-Freigabe und bestaetigte die manuellen sowie
  objektbezogenen Verarbeitungsgrenzen.
- `.codex/`, `.githooks/`, `.gitignore`, `pyproject.toml` und `src/` wurden im
  P031-Slice nicht geaendert. Es wurden weder Graphify-Ausgaben noch neue
  externe Integrationsartefakte erzeugt.
- Inhalte ignorierter Norm-, IDA- und Katalogdaten wurden nicht gelesen. Die
  Katalogdateien bleiben ignoriert und ausserhalb von `git ls-files`.
- Der P031-Arbeitsstand bleibt absichtlich uncommitted und unpushed. Eine
  spaetere Veroeffentlichung benoetigt eine frische `compliance_decision` fuer
  den dann exakten Stand.

## Abnahme und Demonstrationslauf

Die lokale Baseline ist abgenommen, wenn:

1. P031 in Planindex und Planstatus eindeutig gefuehrt wird;
2. alle geschlossenen Konflikte im realen Dateistand behoben sind;
3. Skills formal valide und frei von kopierten Detailroutinen sind;
4. der Contract-Test nur versionierte oder in diesem Slice neu angelegte,
   versionierbare Repo-Pfade prueft und die geschuetzten lokalen Datenbereiche
   explizit ausschliesst;
5. Ruff, fokussierter Pytest-Lauf und `git diff --check` bestehen;
6. ein read-only Forward-Test die kanonischen Wahrheiten korrekt findet;
7. keine globale Konfiguration, Installation, Hook-, MCP-, Graphify-,
   Obsidian-, Zotero- oder PDF-Aktion erfolgt ist;
8. kein Commit und kein Push fuer den P031-Arbeitsstand erzeugt wurde.

Nach Aenderungen an `.codex/agents/` oder `.agents/skills/` ist fuer die
produktive Erkennung ein neuer Codex-Chat oder Projekt-Reload erforderlich.

## Offizielle Codex-Referenzen

- Custom Agents: <https://learn.chatgpt.com/docs/agent-configuration/subagents#custom-agents>
- Skills und repo-lokaler Ablageort:
  <https://learn.chatgpt.com/docs/customization/overview#skills>
