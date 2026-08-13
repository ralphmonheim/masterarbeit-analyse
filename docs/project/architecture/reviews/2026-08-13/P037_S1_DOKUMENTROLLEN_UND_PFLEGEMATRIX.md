# P037-S1 Dokumentrollen und Pflegematrix

Stand: 2026-08-13  
Status: umgesetzt; Sollzuordnung aus P037-S0

## Führende Quellen je Informationsart

| Informationsart | Führende Quelle | Abgeleitete Ansichten / Verweise | Pflegeort |
|---|---|---|---|
| Masterarbeitszweck, Methodenrahmen, Systemgrenzen | `docs/project/MASTERARBEIT_LEITFADEN.md` | Gesamtworkflow, Architektur, Pläne | Leitfaden |
| Fachlicher Ablauf und Nutzungswissen | `docs/project/workflow/README.md` und Modulsteckbriefe | Workflowansicht, Hilfe zum Ablauf | Workflowdokumentation |
| Stabile Modulstruktur | `src/ma_workflow/catalog.py` | Workflowdokumentation, beide UI-Ansichten | Technischer Katalog |
| Technische Zielstruktur und Schnittstellen | `docs/project/architecture/` | Technische Modulinfo | Architektur |
| Verbindliche Nutzer- und technische Entscheidungen | `docs/project/decisions/` | Pläne, Architektur, technische Karte | Entscheidungen |
| Geplante und laufende Umsetzung | `docs/project/plans/inbox/` | Planindex, Planstatus, technische Karte | Aktiver Plan |
| Aktueller Arbeitsstand | `docs/project/plans/PLAN_STATUS.md` | Planindex, technische Karte | Planstatus |
| Änderungshistorie | `CHANGELOG.md` | keine Statusableitung | Changelog |
| Ablauf von Codex-Routinen | `docs/project/UPDATE_ROUTINES.md` | `docs/common/commands_common.md`, Skills | UPDATE_ROUTINES |
| Historische Nachweise | `docs/project/archive/` | Archivindizes | Archiv, nicht als aktive Quelle |
| Auffindbarkeit | lokaler `semantic_topics.md`-Navigator | Verweise auf obige Quellen | Navigator, keine Inhaltswahrheit |

## Vollständige Rollenregel für den versionierten Dokumentbestand

Die P037-S0-Matrix klassifiziert jeden versionierten Markdown-Pfad genau einmal anhand seiner ersten zutreffenden Pfadklasse. Diese Reihenfolge ist verbindlich: `docs/project/archive/**` → `docs/project/plans/inbox/**` → `docs/project/decisions/**` → `docs/project/architecture/**` → Leitfaden/Status/Routinen → übrige `docs/project/**` → Moduldokumentation → Prompts → gemeinsame Dokumentation → lokale READMEs → Agentenanweisungen.

Damit sind Archiv-, Plan-, Entscheidungs-, Architektur-, Arbeitsstand-, Fach-, Einstiegs- und Anweisungsdokumente eindeutig getrennt. Die zugehörige Ist-Matrix steht in `P037_S0_DOKUMENTINVENTAR_IST_ANALYSE.md`.

## Behandlung von Überschneidungen

| Überschneidung | Klassifikation | Regel |
|---|---|---|
| Leitfaden und Workflow | notwendige Schnittstellensicht | Leitfaden führt Rahmen; Workflow führt Ablauf. |
| Katalog und Modulsteckbrief | notwendige Schnittstellensicht | Katalog führt Struktur; Steckbrief führt Erklärung. |
| Plan, Entscheidung und Planstatus | notwendige Schnittstellensicht | Entscheidung führt „warum“, Plan „wie“, Status „wo stehen wir“. |
| Architektur-Review und Zielarchitektur | historische bzw. zeitgebundene Review | Review bleibt Nachweis; Zielarchitektur führt. |
| README und Spezialdokumentation | bewusstes Kurzreferat | README verweist, die Spezialquelle führt. |

Archivverschiebungen und Löschungen sind nicht Bestandteil dieser Zuordnung.

