# Skeptical Review

Stand: 2026-07-15  
Status: unabhaengige Gegenpruefung der Empfehlung, keine Freigabe

## Kurzurteil

Option 1 ist fuer den belegten Projektstand die beste Wahl, aber nicht die
technisch reinste. Sie akzeptiert bewusst mehrere Top-Level-Importpakete,
temporäre Kompatibilitaetsfassaden und Grenzen, die durch Tests statt durch
getrennte Builds erzwungen werden. Diese Nachteile sind real. Sie wiegen
derzeit weniger schwer als ein Namespace- oder Multi-Package-Umbau, der den
MVP risikoreich verzoegern wuerde.

Der Council-Konsens lautet:

- die vorhandene Struktur konsolidieren statt neu erfinden;
- Duplikate durch einen kanonischen Owner plus befristeten Adapter loesen;
- zuerst den echten Importzyklus und die falsche Technik-Zonen-Richtung
  beheben;
- `ma_variants` nur entlang bereits vorhandener Zielmodule verkleinern;
- keine produktive Migration aus diesem Audit ableiten.

## Staerkste Einwaende gegen Option 1

### 1. Mehrere `ma_*`-Pakete wirken wie mehrere Produkte

Das ist fuer neue Entwickler weniger selbsterklaerend als ein gemeinsamer
Namespace. Distribution `ma-analyse`, Repository und Importpakete haben
unterschiedliche Namen. Dieses Problem verschwindet nicht durch Tests.

**Antwort:** Das Projekt ist eine gemeinsam entwickelte Workspace-Anwendung.
Ein Namespaceumbau wuerde mindestens 365 Imports plus Dokumentation,
Entrypoints und Konfiguration betreffen, ohne den gefundenen Zyklus oder die
Dependency-Drift automatisch zu loesen. Eine spaetere allgemeine Distribution
braucht ohnehin eine eigene Naming-Entscheidung.

### 2. Paketgrenzen bleiben weich

In einem Monolithen kann jedes Fachpaket technisch jedes andere importieren.
Separate Distributionen wuerden Grenzen wirksamer erzwingen.

**Antwort:** Import-Contract-Tests sind schwächer als Buildgrenzen, fuer eine
Einzelperson und eine gemeinsam ausgelieferte Anwendung aber angemessen. Wenn
mehrere Teams oder unabhaengige Releasezyklen entstehen, muss Option 3 neu
bewertet werden.

### 3. Kompatibilitaetsadapter koennen dauerhaft bleiben

Reexports reduzieren kurzfristiges Risiko, schaffen aber zwei sichtbare
Importpfade. Ohne Ausstiegsregel werden sie zur neuen Altlast.

**Antwort:** Jeder Adapter braucht Owner, Contract-Test, Nutzungsinventar und
separate spaetere Entfernung. Neue Aufrufer duerfen nur den kanonischen Pfad
verwenden. Der Adapter besitzt nie die Modelle oder Implementierung.

### 4. Die Zielstruktur koennte zu vorsichtig sein

`ma_ui` mit zwei UI-Techniken, ein flacher Testordner und moduleigene
Datenbaeume bleiben uneinheitlich. Eine konsequentere Neuordnung waere auf dem
Papier sauberer.

**Antwort:** Die Uneinheitlichkeit ist lokal beherrschbar. Ein massenhafter
Move erzeugt hohen Review-Laerm und gefaehrdet Git-Historie, Links und
Reproduzierbarkeit. Neue Unterstrukturen entstehen mit dem ersten echten
Contract-, Integration- oder Research-Artefakt.

## Staerkste Argumente fuer Option 2

Ein gemeinsamer Namespace wuerde Produktzugehoerigkeit, Ports und Adapter im
Baum sichtbarer machen. Er waere vorzuziehen, wenn mindestens einer dieser
Faelle eintritt:

- das Projekt wird als allgemeine Bibliothek ausserhalb des Workspace
  installiert;
- mehrere externe Anwendungen konsumieren stabile Teil-APIs;
- globale `ma_*`-Namen kollidieren mit Fremdpaketen;
- mehrere Entwickler brauchen eine strengere, neue Paketkonvention;
- der MVP ist abgeschlossen und es existiert Zeit fuer einen kontrollierten
  Deprecation-Zyklus.

Keiner dieser Trigger ist im Audit ausreichend belegt.

## Warum Option 3 derzeit scheitert

Das Multi-Package-Monorepository bietet die staerksten technischen Grenzen,
erzeugt aber mehrere Builds, Dependency-Grenzen, Versionen, Releasewege und
Cross-Package-Tests. Es fehlen unabhaengige Teams, Konsumenten und
Releasezyklen. Der Aufwand waere Architekturarbeit um ihrer selbst willen und
fuer die Masterarbeit unverhaeltnismaessig.

## Was bewusst verworfen wird

| Vorschlag | Entscheidung | Grund |
| --- | --- | --- |
| alle `ma_*` unter `masterthesis.*` verschieben | vor dem MVP verworfen | hoher Import- und Linkumbau ohne direkte Problemlösung |
| jedes Fachmodul als eigene Distribution | verworfen | keine unabhaengigen Teams oder Releases |
| Microservices | verworfen | kein Deployment-, Skalierungs- oder Teamproblem |
| Plugin-System als Grundarchitektur | vorerst verworfen | keine stabilen externen Plugin-Autoren oder mehrere Adapter |
| globaler `raw/interim/processed`-Datenbaum | verworfen | verschleiert Fachownership und passt nicht zu jedem Lebenszyklus |
| komplette Testordner-Neusortierung | vorerst verworfen | hoher Diff ohne zusaetzliche Testabdeckung |
| allgemeines `utils`- oder `shared`-Paket | verworfen | foerdert unklare Ownership |
| `ma_validation` als Ablage fuer Cross-Domain-Fachlogik | verworfen | das Paket muss fachneutral bleiben |
| reale Katalog-, Normen- oder IDA-Dateien in Git LFS | verworfen | LFS ersetzt keine Rechte oder Vertraulichkeit |
| Graphify-Scan des gesamten Worktrees | verworfen | ignorierte und geschuetzte Inhalte waeren nicht sicher begrenzt |
| parallele `docs/architecture-review/`- und `docs/decisions/`-Baeume | verworfen | bestehende kanonische Quellen liegen unter `docs/project/` |

## Pruefbefunde nach Kritikalitaet

### Blocker vor einer produktiven Strukturmigration

1. ADR-P032 ist nur vorgeschlagen.
2. Workspace-Anwendung versus portable Installation ist noch nicht bewusst
   entschieden; davon haengt die Pfadstrategie ab.
3. Die Parameter-/Optionsownership muss vor Welle 2 fachlich bestaetigt sein.
4. Datenbank-, Graphify-, Obsidian-, CI-, Hook-, Dependency- und geschuetzte
   Inhaltsslices brauchen eigene Freigaben.
5. Der bestehende uncommittete P031-Arbeitsstand muss bei jeder spaeteren
   Welle als fremder Ausgangsdiff erhalten bleiben.

### Wichtig

- Stale Editable-Metadaten melden 0.20.0, waehrend Quellcode und
  `pyproject.toml` 0.28.0 fuehren.
- `requirements.txt` deckt den aktuellen Runtimebestand nicht vollstaendig ab
  und dupliziert `pyproject.toml` ohne erklaerte Erzeugungsregel.
- Es fehlt eine automatisierte Importpolitik.
- README und Data-README enthalten belegte Pfaddrifts.
- Die Variantenzerlegung darf Alembic- und Persistenzownership nicht nebenbei
  veraendern.

### Optional

- gemeinsamer Namespace nach dem MVP erneut benchmarken;
- Restricted-CI nach stabiler lokaler Befehlswahrheit aktivieren;
- Graphify erst nach einem statisch belegten Nutzen pilotieren;
- Diataxis-Klassifikation in Dokumentindizes ergaenzen;
- LFS nur bei spaeteren grossen und tatsaechlich veroeffentlichbaren
  Artefakten neu pruefen.

## Verbleibende Evidenzluecken

- Kein realer Clean-Environment- oder Wheel-Installationslauf wurde in diesem
  Audit erzeugt.
- Es gibt keinen CI-Lauf als Vergleich zur lokalen Windows-Umgebung.
- Graphify, Node.js und Graphviz sind nicht vorhanden; die Graphify-Bewertung
  ist daher eine Scope- und Risikobewertung, kein Produktbenchmark.
- Ein Obsidian-Vault-Pfad und ein Linkinventar fehlen. Es wurde kein Vault
  gelesen.
- Geschuetzte Normen-, Literatur-, IDA-/EQUA- und lokale Kataloginhalte wurden
  nicht gelesen; ihre Verarbeitbarkeit ist nicht aus Metadaten ableitbar.
- Die genaue Zahl externer API-Konsumenten ist nicht formal erhoben; im
  versionierten Projektbestand ist kein unabhaengiger Konsument belegt.

## Entscheidungen vor Welle 1 und 2

| Entscheidung | Empfehlung | Auswirkung bei Zustimmung |
| --- | --- | --- |
| ADR-P032 Zieloption | Option 1 annehmen | konservative Wellenplanung wird verbindliche Zielrichtung |
| Betriebsmodell | zunaechst Workspace-Anwendung | expliziter Workspace-Root; portable Installation bleibt spaetere Erweiterung |
| Parameter-/Optionskataloge | `ma_parameters` als kanonischer Owner | Zyklus kann mit Reexports unter `ma_variants` abgebaut werden |

Spaetere Einzelentscheidungen zu CI, Graphify, Obsidian, Hooks, Dependencies,
Datenbankmigration und geschuetzten Inhalten werden dadurch nicht
vorweggenommen.

## Stop-/Go-Regeln

**Go** fuer eine Teilwelle nur, wenn Owner, Scope, Tests, Rueckfall und
Freigaben exakt benannt sind. **Stop**, wenn eine Welle neue Domaenen
mitnimmt, geschuetzte Inhalte benoetigt, eine oeffentliche API ungeplant
bricht, Daten loeschen soll oder den MVP ohne belegten Nutzen verzoegert.
