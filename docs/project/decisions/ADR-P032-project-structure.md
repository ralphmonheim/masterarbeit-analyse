---
id: ADR-P032
title: Projektstruktur als konservativ konsolidierter modularer Monolith
status: accepted
date: 2026-07-15
accepted_date: 2026-07-15
decision_owner: user
related_plan: P032
supersedes: []
---

# ADR-P032: Projektstruktur als konservativ konsolidierter modularer Monolith

## Status

**Accepted am 2026-07-15.** Dieses Dokument legt die Zielrichtung fest. Es
erteilt keine Migrations-, Tool-, Datenverarbeitungs-, Commit- oder
Veroeffentlichungsfreigabe.

## Kontext

Das Repository ist eine Python-Workspace-Anwendung mit `src`-Layout, einer
Distribution `ma-analyse` und 22 fachlich benannten `ma_*`-Importpaketen.
Module fuer die vorgesehenen Zielverantwortungen sind bereits vorhanden,
einige enthalten jedoch nur Gerueste, waehrend `ma_variants` weiterhin
Parameter- und Optionskataloge, Persistenz, Economics, IDA-Export,
Simulationsergebnisse, Reporting und UI-Prototypen buendelt.

Der Audit vom 2026-07-15 belegt:

- einen echten Laufzeitzyklus `ma_parameters <-> ma_variants`;
- eine unerwuenschte Runtimekante `ma_technical -> ma_zones`;
- mehrere lokale Pfadfinder statt eines expliziten Workspacevertrags;
- Dependency- und Editable-Metadaten-Drift;
- fehlende automatisierte Import-, Build- und Restricted-CI-Vertraege;
- stabile bestehende Plan-, Entscheidungs-, Architektur- und
  Compliance-Wahrheiten, die nicht dupliziert werden sollen.

Es bestehen keine belegten unabhaengigen Teams, Distributionen,
Deploymentziele oder externen API-Konsumenten, die einen Multi-Package- oder
Microservice-Umbau rechtfertigen.

## Entscheidungstreiber

1. Verstaendlichkeit fuer einen Anfaenger und eine Einzelperson.
2. Fachliche Ownership und testbare Importgrenzen.
3. Erhalt bestehender APIs, Dokumentlinks und Git-Historie.
4. Reproduzierbare Masterarbeitslaeufe und klare Datenprovenienz.
5. Geringes Migrations- und Terminrisiko vor dem MVP.
6. Trennung versionierbarer Beispiele von privaten oder lizenzierten Daten.
7. Erweiterbarkeit ohne vorzeitigen Plattformbau.

## Gepruefte Optionen

### Option 1 - konservative Konsolidierung

Eine Distribution und die bestehenden `ma_*`-Pakete bleiben erhalten.
Ownership, Imports, Pfade, Tests und Provenienz werden inkrementell
professionell gehaertet.

### Option 2 - gemeinsamer Namespace

Alle Pakete ziehen unter einen Namespace wie `masterthesis.*`; Domains,
Application Layer und Adapter werden im Baum neu geordnet.

### Option 3 - Multi-Package-Monorepository

Stabile Domaenen werden eigene Distributionen mit eigenen Builds,
Abhaengigkeiten und Releasezyklen.

Microservices, getrennte Repositories und ein allgemeines Plugin-System
wurden als fuer den aktuellen Bedarf ungeeignet verworfen.

## Entscheidung

Option 1 wird als Zielrichtung angenommen:

1. Das Projekt bleibt bis nach dem MVP ein modularer Monolith mit einer
   Distribution und stabilen `ma_*`-Importpaketen.
2. `ma_parameters` wird kanonischer Owner von Parameter- und
   Optionskatalogen; `ma_variants` konsumiert diese Vertrage und darf nur
   befristete, getestete Kompatibilitaets-Reexports anbieten.
3. Zonenabhaengige Pruefungen technischer Referenzen liegen unter
   `ma_zones.validation`; `ma_technical` importiert zur Laufzeit nicht
   `ma_zones`.
4. `ma_variants` wird nur entlang der bereits vorhandenen Zielmodule
   `ma_economy`, `ma_reporting`, `ma_ui`, `ma_export_simulation`,
   `ma_import_simulation`, `ma_analyse` und `ma_data_export` verkleinert.
5. Ein spaeterer `ma_core.paths.WorkspacePaths`-Vertrag zentralisiert die
   Workspace-Root-Aufloesung; fachliche Dateinamen bleiben bei ihren Owners.
6. Daten bleiben zuerst nach fachlichem Owner gegliedert. Lebenszyklusordner
   werden nur bei realem Bedarf modulweise eingefuehrt.
7. Der neutrale Run-Root wird
   `data/ma_simulation_setup/runs/<run_id>/`.
8. Import-, Schema-, Provenienz-, Build- und Restricted-Profile werden vor
   risikoreichen Verschiebungen als Tests aufgebaut.
9. Neue Verzeichnisse entstehen erst mit dem ersten echten Inhalt.
10. Option 2 wird nach dem MVP nur bei belegter externer Distribution,
    mehreren Konsumenten oder Namenskollisionen erneut bewertet.

## Positive Folgen

- Geringstes Risiko fuer bestehende Imports, Commands und Dokumentlinks.
- Der reale Zyklus wird durch fachliche Ownership statt durch kosmetische
  Umbenennung geloest.
- Zielmodule und bestehende Plaene koennen schrittweise mit Inhalt gefuellt
  werden.
- Migrationswellen bleiben klein, testbar und rueckrollbar.
- Reproduzierbarkeit und Datenprovenienz werden verbessert, ohne
  proprietäre Tools oder Daten vorauszusetzen.
- Die Struktur bleibt fuer die Masterarbeit erklaerbar.

## Negative Folgen und akzeptierte Schulden

- Distribution und mehrere Top-Level-Importpakete bleiben optisch
  uneinheitlich.
- Paketgrenzen muessen durch Contract-Tests statt getrennte Builds erzwungen
  werden.
- Befristete Kompatibilitaetspfade erhoehen waehrend der Migration die
  sichtbare API-Oberflaeche.
- `ma_ui` behaelt zwei getrennte UI-Techniken.
- Test- und Datenstruktur werden nicht sofort vollstaendig vereinheitlicht.
- Ein spaeterer Namespaceumbau waere weiterhin moeglich, aber nicht kostenlos.

## Aufwand

Die Umsetzung wird in Wellen geplant. Der groesste unmittelbare Nutzen liegt
in Guardrails, dem Abbau des Parameter-Varianten-Zyklus und der Korrektur der
Technik-Zonen-Richtung. Economics, Reporting, UI, Simulation, Datenbank und
Kataloge folgen nur, wenn der jeweilige Fachslice sie beruehrt.

Ein Namespaceumbau oder Multi-Package-Monorepository wuerde dagegen
mindestens 365 Importanweisungen in 139 Source-/Testdateien sowie Commands,
Dokumente und Konfiguration betreffen.

## Hauptrisiken

- versteckte Import- oder Config-Aufrufer;
- dauerhafte Altpfade statt befristeter Adapter;
- Drift von Datenreferenzen und Run-Provenienz;
- unlesbare Git-Historie bei kombinierten Moves und Umschreibungen;
- Alembic-Bruch bei vorzeitiger Datenbankzerlegung;
- Architekturarbeit ohne proportionalen MVP-Nutzen;
- versehentliche Verarbeitung oder Veroeffentlichung geschuetzter Inhalte.

Das vollstaendige Register und die Rueckfallregeln stehen im
`MIGRATION_RISK_REGISTER.md` des datierten P032-Reviews.

## Compliance- und externe Grenzen

Diese ADR gibt keine Freigabe fuer globale Codex-Konfiguration,
Installationen, Dependencies, Hooks, MCP, CI-Netzwerkzugriff, Graphify,
Obsidian/Zotero, externe APIs oder geschuetzte Inhalte. Normen-, Literatur-,
IDA-/EQUA- und reale Katalogdaten bleiben objektbezogen zu pruefen und
ausserhalb von Git und Git LFS.

## Entschiedene Kernfragen

1. ADR-P032 mit Option 1 ist angenommen.
2. Das Projekt wird bis zum MVP als Workspace-Anwendung betrieben; eine
   portable Installation bleibt eine spaetere Erweiterung.
3. `ma_parameters` ist kanonischer Owner der Parameter- und
   Optionskataloge. `ma_variants` konsumiert diese Vertraege und darf nur
   befristete, getestete Kompatibilitaets-Reexports anbieten.

CI, Graphify, Obsidian, Hooks, Dependencystrategie, Datenbankmigration und
geschuetzte Inhaltsverarbeitung bleiben spaetere Einzelentscheidungen.

## Annahme

Der Nutzer hat die drei Kernentscheidungen am 2026-07-15 ausdruecklich
bestaetigt. P032-Plan, offene Nutzerentscheidungen und Planstatus werden mit
dieser Annahme synchronisiert. Produktive Migrationswellen bleiben davon
getrennt und brauchen weiterhin eine eigene, konkrete Freigabe.

## Referenzen

- `docs/project/architecture/reviews/2026-07-15/CURRENT_STATE_INVENTORY.md`
- `docs/project/architecture/reviews/2026-07-15/MODULE_BOUNDARY_REVIEW.md`
- `docs/project/architecture/reviews/2026-07-15/TARGET_ARCHITECTURE_OPTIONS.md`
- `docs/project/architecture/reviews/2026-07-15/RECOMMENDED_TARGET_ARCHITECTURE.md`
- `docs/project/architecture/reviews/2026-07-15/MIGRATION_MAPPING.csv`
- `docs/project/architecture/reviews/2026-07-15/MIGRATION_RISK_REGISTER.md`
- `docs/project/architecture/reviews/2026-07-15/SKEPTICAL_REVIEW.md`
