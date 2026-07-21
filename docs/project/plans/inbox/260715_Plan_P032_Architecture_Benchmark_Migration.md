# P032 Architecture Benchmark und Migrationsplanung

Stand: 2026-07-18
Status: Audit und Planung abgeschlossen; ADR angenommen; P032-W0, P032-W1a, P032-W2a und P032-W3a-T0 abgeschlossen; volle W3a-Ownership weiter offen
Prioritaet: Hoch fuer Architekturqualitaet, Umsetzung nur MVP-gekoppelt

## Zweck

P032 dokumentiert einen professionellen Benchmark der aktuellen
Repository-Architektur, drei realistische Zieloptionen, die bevorzugte
Zielrichtung und einen inkrementellen Migrationsplan. Der Plan ist der einzige
aktive Traeger fuer diesen datierten Architektur-Audit und dessen Backlog.

P032 ersetzt weder die Zielarchitektur unter `docs/project/architecture/`
noch Planindex, Planstatus, Entscheidungen oder Compliance. Er erteilt keine
Freigabe fuer produktive Moves, Renames, Deletes, Dependencies, Tools,
externe Zugriffe, Commits, Pushes oder Veroeffentlichungen.

## Auftragszuordnung ohne Parallelwahrheit

Der eingereichte Auftrag nannte generische Zielpfade. Wegen der vorhandenen
kanonischen Projektstruktur wurden sie so eingeordnet:

| Angeforderte Ablage | Kanonische Ablage |
| --- | --- |
| `docs/architecture-review/` | datierter, nicht autoritativer Snapshot unter `docs/project/architecture/reviews/2026-07-15/` |
| `docs/decisions/ADR-project-structure.md` | angenommene ADR unter `docs/project/decisions/ADR-P032-project-structure.md` |
| Architektur- und Migrationsstatus | dieser P032-Plan plus `PLAN_INDEX.md` und `PLAN_STATUS.md` |

Es wurden keine parallelen Root-Baeume `docs/architecture-review/` oder
`docs/decisions/` angelegt.

## Auditgrenzen

- Allgemeine Scans wurden auf versionierte Dateien beziehungsweise
  `git ls-files` begrenzt. Zusaetzlich wurden die explizit benannten,
  versionierbaren P031-Arbeitsdateien unter `.agents/` und
  `tests/test_project_agent_system.py` sowie nicht sensible lokale
  Packaging-Metadaten geprueft.
- Inhalte ignorierter Normen-, Literatur-, IDA-/EQUA-, Katalog- und sonstiger
  geschuetzter Arbeitsdateien wurden nicht gelesen.
- Lokale Datenbereiche wurden nur anhand bereinigter Pfad- und
  Trackinginformationen bewertet.
- Graphify, Node.js, Graphviz und `dot` waren nicht vorhanden; es wurde ein
  statischer Python-Importaudit statt eines Graphify-Laufs verwendet.
- Ein Obsidian-Vault-Pfad lag nicht vor; es fand weder Vault-Lese- noch
  Schreibzugriff statt.
- Es wurden keine Produktivdateien verschoben, umbenannt, geloescht oder
  inhaltlich migriert.
- Es wurden keine Hooks, MCP-, CI-, globale Codex- oder externe
  Toolkonfigurationen veraendert.

## Artefakte

| Artefakt | Rolle |
| --- | --- |
| `CURRENT_STATE_INVENTORY.md` | quantitativer und qualitativer Ist-Bestand |
| `MODULE_BOUNDARY_REVIEW.md` | Ownership, Abhaengigkeiten und Zielaktionen aller 22 `ma_*`-Pakete |
| `TARGET_ARCHITECTURE_OPTIONS.md` | drei vollstaendige Optionen und gewichtete Entscheidungsmatrix |
| `RECOMMENDED_TARGET_ARCHITECTURE.md` | professionelle Zielstruktur fuer Option 1 |
| `MIGRATION_MAPPING.csv` | zeilenweises Pfad-, Owner-, Test- und Freigabemapping |
| `MIGRATION_RISK_REGISTER.md` | Risiken, Voraussetzungen, Wellen, Abnahme und Rueckfall |
| `SKEPTICAL_REVIEW.md` | Gegenargumente, verworfene Alternativen und manuelle Entscheidungen |
| `docs/project/decisions/ADR-P032-project-structure.md` | angenommene Zielrichtung; keine Migrationsfreigabe |

Alle Auditdateien unter `reviews/2026-07-15/` sind ein datierter
Evidenzsnapshot. Spaetere reale Entscheidungen werden nur in den kanonischen
Entscheidungsdateien fortgeschrieben.

## Auditbefunde

### Bestaetigte Staerken

- etabliertes `src`-Layout und eine grundsaetzlich passende modulare
  Monolithstruktur;
- vorhandene Zielmodule fuer den geplanten fachlichen Ausbau;
- klare Projekt-, Plan-, Decision- und Compliance-Strukturen;
- umfangreiche lokale Testsuite mit 47 versionierten Python-Dateien unter
  `tests/` (einschliesslich `conftest.py`);
- neutrale Kern- und Validierungsvertraege als gute Ausgangsbasis;
- geschuetzte lokale Daten werden grundsaetzlich vom Git-Tracking getrennt.

### Bestaetigte Architekturprobleme

1. ein echter Runtimezyklus `ma_parameters <-> ma_variants`;
2. eine fachlich falsche Runtimekante `ma_technical -> ma_zones`;
3. zu viele historische Verantwortungen in `ma_variants`;
4. mehrere paketlokale Workspace-Pfadfinder;
5. ungeklaerte Distribution-gegen-Workspace-Semantik;
6. Drift zwischen `pyproject.toml`, `requirements.txt` und Editable-Metadaten;
7. keine automatisierte Importpolitik, kein Build-/Wheel-Vertrag und keine CI;
8. README- und Data-README-Pfaddrift;
9. Defense-in-Depth-Luecken fuer hypothetische Inhalte unter
   `data/catalogs/materials/`, `data/catalogs/products/`,
   `data/catalogs/sources/` sowie einzelnen Norm-Unterpfaden;
10. uneinheitliche Datenlebenszyklen und noch kein kanonischer neutraler
   Run-Root;
11. fehlende objektbezogene Freigaben fuer externe Tools und geschuetzte
    Inhalte.

## Professioneller Benchmark

Verglichen wurden offizielle Strukturen und Praktiken aus Python Packaging,
Pydantic, FastAPI, scikit-learn, SciPy, Cookiecutter Data Science, The Turing
Way, FAIR, Diataxis, GitHub Actions und Git/Git LFS. Uebertragbar sind
insbesondere:

- `src`-Layout und `pyproject.toml` als Build-/Projektbasis;
- klare oeffentliche Paketvertraege statt Import interner Dateipfade;
- kleine deterministische Fixtures, Contract- und Integrationsprofile;
- reproduzierbare Umgebung, Inputs, Konfigurationen, Code- und Run-Metadaten;
- dokumentierte Datenprovenienz und Rechteklassifikation;
- Docs-Typen ohne parallele Statuswahrheit;
- CI nur mit synthetischen oder sicher versionierbaren Daten.

Nicht sinnvoll uebernommen werden die Groesse und Governance grosser
Open-Source-Projekte, ein pauschaler Data-Science-Ordnerbaum, mehrere
Distributionen oder Microservices.

## Council-Ergebnis

Mira inventarisierte den versionierten Bestand und die realen
Abhaengigkeiten. Vera pruefte Zieloptionen, Packaging, Tests und
Migrationsrisiken. Justus pruefte Daten-, Lizenz-, Graphify-, Obsidian- und
Veroeffentlichungsgrenzen. Tera konsolidierte die Ergebnisse.

Der Council empfiehlt einstimmig Option 1: konservative Konsolidierung des
bestehenden modularen Monolithen. Die gewichtete Bewertung lautet:

| Option | Ergebnis |
| --- | ---: |
| Option 1 - bestehende `ma_*`-Pakete professionell haerten | 4,55 / 5 |
| Option 2 - gemeinsamer Namespace | 3,64 / 5 |
| Option 3 - Multi-Package-Monorepository | 3,14 / 5 |

## Beschlossene Ownership-Entscheidungen

- `ma_parameters` besitzt Parameter- und Optionskataloge;
- `ma_project` besitzt das neutrale Namingprofil und seine Konfiguration;
  `ma_variants` besitzt Variantenraum, Auswahl, Generierung, Anwendung des
  Profils und Variantenprovenienz;
- `ma_zones.validation` besitzt den zonenabhaengigen Abgleich zum zuvor
  freigegebenen Technikstand;
- Economics, Reporting und UI ziehen spaeter in ihre vorhandenen Zielmodule;
- Export, Import, Analysemetrik und Datenexport werden am neutralen
  Simulationsvertrag getrennt;
- Datenbank- und mehrdeutige Katalogownership werden nicht nebenbei
  entschieden.

Der Nutzer hat diese Zielrichtung, das Workspace-Betriebsmodell und die
Parameter-/Optionsownership am 2026-07-15 angenommen. UD-089 erlaubt danach
klar abgegrenzte, lokale und reversible Folgeslices mit dokumentierter
Council-Mehrheit; Sondergates bleiben davon unberuehrt.

## Migrationsbacklog

| Welle | Inhalt | Status | Gate |
| --- | --- | --- | --- |
| P032-W0 | ADR, Betriebsmodell, Ownership und Baseline | abgeschlossen | ADR/Ownership angenommen; lokaler Wheel-Smoke `ma_analyse-0.28.0-py3-none-any.whl` gruen |
| P032-W1 | Guardrails, Dokumentpfade, Importtests und Dependency-Klaerung | teilweise umgesetzt | W1a abgeschlossen; W1b nur mit eigenem Scope und Council-Mehrheit |
| P032-W1a | additive Pfad-, Ignore- und Importguardrails | abgeschlossen | einstimmige Mehrheit Mira, Vera und Justus; keine Dependencies, Hooks, CI oder externen Tools |
| P032-W1b | Dependency-Bestandsklaerung und WorkspacePaths-Entwurf | nicht gestartet | keine Dependency- oder Runtimeaenderung; exakter Council-Scope erforderlich |
| P032-W2 | Parameter-/Optionsownership und Zyklusabbau | teilweise umgesetzt: W2a abgeschlossen | W2a: Code-Owner-Transfer/Reexports ohne Config-Move abgeschlossen; W2b und Vollumfang bleiben getrennt freigabepflichtig |
| P032-W3a | Technik-Zonen-Richtung | T0 und Zielrichtung dokumentiert; Kompatibilitaetsslice weiter offen | exakter Council-Scope, P013/P014-Vertrag |
| P032-W3b | begrenzter WorkspacePaths-Slice | nicht freigegeben | beschlossenes Betriebsmodell |
| P032-W4 | Economics, Reporting und UI aus `ma_variants` | nicht freigegeben | je Zielplan und Teilwelle |
| P032-W5a | neutraler Run-Vertrag | nicht freigegeben | P018 |
| P032-W5b | Simulations-Exportadapter | nicht freigegeben | W5a, P009 und objektbezogene Rechte |
| P032-W5c | Ergebnisimport und Normalisierung | nicht freigegeben | stabiler Run-Vertrag und freigegebenes Format |
| P032-W5d | Analysemetrik und Datenexport | nicht freigegeben | stabiler normalisierter Ergebnisvertrag |
| P032-W6 | DB, weitere Kataloge, Research, CI, Graphify oder Obsidian | optional und gesperrt | jeweils eigene Notwendigkeit und Freigabe |

Der exakte Scope, Dry Run, Tests, Abnahme, Rueckfall und Handover jeder Welle
stehen in `MIGRATION_RISK_REGISTER.md`; die betroffenen Pfade in
`MIGRATION_MAPPING.csv`. Das vom Auftrag vorgegebene CSV-Schema bleibt
unveraendert. Spaetere Wellenfreigaben referenzieren seine eindeutigen
`current_path`-Werte und dokumentieren den Umsetzungsstatus in diesem Plan.

## Manuelle Freigabematrix

### P032-W0-Kernentscheidungen vom 2026-07-15

1. ADR-P032 mit Option 1 ist angenommen.
2. Das Projekt bleibt bis zum MVP eine Workspace-Anwendung.
3. `ma_parameters` ist kanonischer Owner der Parameter- und
   Optionskataloge; `ma_variants` konsumiert die Vertraege mit nur
   befristeten, getesteten Kompatibilitaets-Reexports.

Der lokale Build-/Wheel-Smoke-Test ist gruen: Mit der vorhandenen Toolchain
wurde ohne Download und ohne Installation
`ma_analyse-0.28.0-py3-none-any.whl` erzeugt.

### P032-W1a vom 2026-07-15

Mira, Vera und Justus stimmten einstimmig fuer den kleinsten additiven
Guardrail-Slice. Umgesetzt wurden die korrigierten README-Pfade,
synthetische `.gitignore`-Nachweise fuer lokale Katalogunterpfade und ein
AST-basierter Importvertrag. Nicht Teil sind Dependencies, Hooks, CI,
`WorkspacePaths`, Moves, Renames, reale Katalogdaten oder externe Tools.

### P032-W2a vom 2026-07-15 - abgeschlossen

Mira, Vera und Justus stimmen einstimmig fuer den kleinsten
Parameter-/Options-Code-Owner-Transfer. Nur die reinen Python-Vertraege,
Loader und kombinierten Importtypen wechseln nach `ma_parameters`; die alten
`ma_variants`-Pfade bleiben identische getestete Reexports. Der konkrete
Runtime-Zyklus wird dadurch entfernt.

Ausdruecklich nicht Teil sind Config-Moves/-Kopien, Defaultpfadwechsel,
Katalog- oder Datenverarbeitung, UI, DB/Alembic, P015-v2-Werteherkunft,
Parameter-/Baseline-/Checkpoint-Semantik, P017, Dependencies, Hooks, CI,
externe Tools und Git-Aktionen. Neue Tests verwenden ausschliesslich
synthetische Objekte oder `tmp_path`-YAML. Der Nachweis folgt nach Umsetzung;
W2b und der restliche W2-Umfang bleiben eigene menschliche Freigaben.

### P032-W3a-T0 vom 2026-07-18 - abgeschlossen

Mira, Vera und Justus stimmen einstimmig fuer einen rein vorbereitenden
Runtime-Stabilisierungsslice vor P014-v2-S4. `ma_technical.validation` darf
`ZoneModelSpecification` nur fuer Typinformationen unter `TYPE_CHECKING`
importieren. Signatur, Keyword `zone_spec`, Diagnosen und Laufzeitlogik
bleiben unveraendert; die Architekturtests muessen danach keine Runtimekante
`ma_technical -> ma_zones` mehr finden.

Nicht Teil sind die fachlich korrekte spaetere Ownership-Verlagerung nach
`ma_zones.validation`, jede API-Aenderung, P014-S4-Referenz-YAML,
v2-Werteherkunft, Katalog- oder reale Daten, externe Tools, Dependencies,
Hooks, CI, Commit, Push oder Veroeffentlichung. Die anwendbare
`compliance_decision` ist `green` fuer versionierten Eigen-Code,
synthetische Tests und Dokumentation; Belegreferenz:
`SHARED-COMPLIANCE-003` und `SHARED-COMPLIANCE-004` im gemeinsamen
Compliance-Entscheidungsregister.

Umsetzungsnachweis:

- `ma_technical.validation` importiert `ZoneModelSpecification` nur noch
  unter `TYPE_CHECKING`; Signatur, Keyword `zone_spec`, Diagnosen und die
  strukturelle Legacy-Validierung blieben unveraendert.
- Der Architekturguardrail erwartet fuer das Paar keine Runtimeimporte mehr;
  seine Paarliste bleibt als Rueckfallschutz bestehen.
- Der fachuebergreifende Fokuslauf umfasst `58 passed`; die vollstaendige
  lokale Suite umfasst `572 passed`. Zielgerichtete Ruff- und Format-Checks
  sowie `git diff --check` sind gruen.
- Der volle W3a-Ownership-Slice bleibt offen: Die zonenabhaengige
  Legacy-Validierung wurde nicht nach `ma_zones.validation` verschoben.

### Immer konkret und objektbezogen freizugeben

- neue oder geaenderte Dependencies und Environment-Lockstrategie;
- Hooks und externe CI-Ausfuehrung;
- Graphify-Installation, -Scope, -Watch und -Ausgabe;
- Obsidian-/Zotero-Pfad und jeder Schreibumfang;
- Datenbankmigration mit realen Daten;
- Normen-, Literatur-, IDA-/EQUA-, Katalog- oder andere geschuetzte Inhalte;
- Loeschungen, Adapterentfernungen, ungeplante Moves/Renames oder brechende
  API-Umstellungen;
- Commit, Push, Tag oder Veroeffentlichung des P032-Arbeitsstands.

## Abnahme des Audit- und Planungsslices

Der P032-Auditslice ist abgeschlossen, wenn:

1. alle acht Audit-/Planungsartefakte vorhanden und intern konsistent sind;
2. Planindex, Planstatus, offene Entscheidung, Architekturindex und Changelog
   auf P032 verweisen;
3. CSV-Schema und erlaubte Aktionen maschinell validiert sind;
4. `git diff --check`, fokussierter Governance-Test, Ruff und die angemessen
   skalierte Testsuite gruen sind;
5. ein unabhaengiger Qualitaets- und Compliance-Review keine offenen Blocker
   meldet;
6. keine produktive Migration, kein externer Toollauf und keine geschuetzte
   Inhaltsverarbeitung erfolgt ist;
7. kein Commit und kein Push fuer den P032-Arbeitsstand erzeugt wurde.

Die Abnahme dieses Audits war fuer sich keine Abnahme von ADR-P032 oder einer
Migrationswelle. Die spaetere ADR-Annahme ist oben und in den kanonischen
Entscheidungsdateien dokumentiert; eine Migrationswelle bleibt separat.

## Abschlussaudit 2026-07-15

- Alle sieben geforderten Review-/Migrationsartefakte, die ADR-Vorlage und der
  zusaetzliche Snapshot-README sind vorhanden. Der spaetere Annahmestatus ist
  ausschliesslich in den kanonischen Entscheidungs- und Planquellen erfasst.
- Der Modulreview bildet alle 22 vorhandenen `ma_*`-Importpakete genau einmal
  ab und kennzeichnet `research_tools` getrennt als geplantes P030-Paket.
- Das CSV-Mapping besitzt 77 eindeutige atomare `current_path`-Zeilen, exakt
  die elf vorgegebenen Spalten, keine Leerwerte, Duplikate, ungueltigen
  Aktionen oder Delete-Anweisung. Alle nicht vorhandenen Istpfade sind mit
  `[missing]` gekennzeichnet.
- Die Entscheidungsmatrix ist rechnerisch konsistent; ihre Gewichte sind aus
  Einzelentwickler-, Masterarbeits-, Reproduzierbarkeits- und MVP-Risiken
  begruendet.
- Der komplette Working-Tree-Testlauf bestand waehrend des Audits mit
  `496 passed` in 189,59 Sekunden. Darin enthalten sind sechs unversionierte
  P031-Contract-Tests; die versionierte Baseline ohne diese Datei sammelt 490
  Tests.
- Nach allen Dokumentnacharbeiten bestanden der fokussierte Governance-
  Contract mit `6 passed`, der projektweite Ruff-Lauf und
  `git diff --check`.
- Der finale unabhaengige Qualitaets-, Evidenz- und Compliance-Nachreview
  meldete jeweils keine Blocker, wichtigen oder optionalen Restbefunde.
- Der urspruengliche P032-Auditslice veraenderte keine Produkt-, Test-,
  Config-, Daten- oder `.gitignore`-Datei. P032-W1a schloss danach die
  dokumentierte Katalog-Ignore-Luecke mit synthetischen Tests, ohne reale
  Katalog- oder Norminhalte zu lesen.
- Ignorierte Normen-, Literatur-, Katalog-, IDA-/EQUA- und reale
  Projektinhalte wurden nicht gelesen. Graphify und Obsidian wurden nicht
  ausgefuehrt oder geoeffnet.
- Es erfolgten keine Installation, Dependency-, Hook-, MCP-, CI-, globale
  Codex-, externe API-, Commit-, Push-, Tag- oder Veroeffentlichungsaktion.
- Der lokale Build-/Wheel-Smoke-Test der vorhandenen Toolchain bestand danach
  mit `ma_analyse-0.28.0-py3-none-any.whl`; es wurden weder Dependencies
  installiert noch Netzwerkzugriffe verwendet.

### Nachtrag P032-W1a 2026-07-15

- Der neue Architekturcontract prueft aktuelle README-Pfade, synthetische
  Katalog-Ignore-Regeln, konkrete temporaere Importmodule und die einzige
  dokumentierte Runtime-SCC `ma_parameters <-> ma_variants`.
- Der Project-OS-Contract erlaubt in der Tracked-Allowlist nur die expliziten
  Katalogstrukturplatzhalter und prueft die Council-Mehrheitsdelegation gegen
  ihre Sondergates.
- Die fokussierten Architektur- und Project-OS-Tests bestanden mit `6 passed`
  beziehungsweise `7 passed`; die vollstaendige Working-Tree-Suite bestand
  mit `503 passed` in 169,32 Sekunden.
- `ruff check .`, der fokussierte Ruff-Format-Check und `git diff --check`
  sind gruen. Ein zusaetzlicher globaler Format-Check meldet 104 bereits
   bestehende, nicht zu W1a gehoerende Dateien; sie wurden bewusst nicht als
   Massendiff formatiert.

### Nachtrag P032-W2a 2026-07-15

- `ma_parameters.catalogs` besitzt jetzt die reinen Parameter-/Optionsmodelle,
  Loader, kombinierten Import sowie Ergebnis-, Fehler- und Reporttypen.
  `ma_parameters.services` konsumiert ausschliesslich diesen Owner-Vertrag.
- Die bisherigen `ma_variants`-Katalog- und Importpfade bleiben einseitige,
  identitaetsgleiche Reexports. Der Contract-Test deckt auch zuvor direkt aus
  Untermodulen importierbare Modelle, Loader und Reporthelfer ab.
- Es gab keinen Config- oder Datenmove: beide `DEFAULT_*`-Pfade unter
  `config/ma_variants/` und der lokale Legacy-Reportpfad
  `data/ma_variants/imports/import_report.json` bleiben unveraendert.
- Der neue Guardrail beweist auch vor einem spaeteren Staging, dass kein
  Runtime-Import `ma_parameters -> ma_variants` verbleibt. Im tracked
  Source-Set ist die Runtime-SCC damit leer.
- Der Nachweis gilt bewusst nur fuer das mit `git ls-files` erfasste
  Source-Set. Der getrennte P013-/P014-Handover besitzt im Arbeitsbaum eine
  Runtimekante `ma_zones -> ma_technical`, waehrend die bestehende
  `ma_technical.validation -> ma_zones`-Kante fortbesteht. Diese eigene
  Technik-Zonen-SCC ist P032-W3a und wurde nicht im W2a-Scope versteckt oder
  veraendert.
- Nach einem im Review gefundenen und behobenen Legacy-Reexport-Blocker
  bestanden `46 passed` im fokussierten Lauf und `541 passed` in der
  vollstaendigen lokalen Suite. Zielgerichtete Ruff- und Format-Checks sowie
  `git diff --check` sind gruen. Architekturreview: keine Blocker;
  Compliance-Postreview: `green`.

## Naechster Schritt

P032-W0 und der additive Guardrail-Slice P032-W1a sind abgeschlossen. Der
Council hat anschliessend einstimmig den engeren
P014-S3a/P015-S3b-prep-Referenzhandover und danach den
P013-S3c/P015-S3b-T2-Releasecheckpoint vor P032-W2 umgesetzt. Der zweite
Beschluss schloss die vergleichbare P013-Fingerprint-/P015-Checkpoint-Luecke
lokal, ohne P032-W2 vorwegzunehmen. P032-W2a ist jetzt als Code-Owner-Transfer
ohne Config-Move abgeschlossen. Die fachliche Zielrichtung fuer P032-W3a ist
dokumentiert: `ma_building -> ma_technical -> ma_zones -> ma_parameters`.
Der verbleibende Kompatibilitaetsslice braucht einen eigenen Council-Scope;
v2-Werteherkunft, W2b-Konfigurationsownership und jeder weitere W2-Teil
bleiben getrennt.

### Übergabe fuer den naechsten Chat, 2026-07-19

Die Read-only-Inventur fuer P032-W3a ist abgeschlossen. Die direkte
Nutzerentscheidung vom 2026-07-19 legt die fachliche und bedienseitige
Reihenfolge `ma_building -> ma_technical -> ma_zones -> ma_parameters` fest:
Die Technik ist eine eigenstaendig validierbare Vorbedingung; Zonen besitzen
Nutzungs-, Zeit- und Belegungsprofile und ordnen sie freigegebenen
Technikreferenzen zu. UI und `ma_parameters` orchestrieren nur und enthalten
keine duplizierte Cross-Domain-Fachlogik.

P032-W3a-T0 hat nur den Runtime-Importzyklus geloest. Vor der verbleibenden
Legacy-Kompatibilitaetsumsetzung sind exakter Scope, mindestens drei
Council-Voten gemaess UD-089, Paritaetstests fuer alle vier Legacy-Diagnosen,
ein API-/Adaptervertrag fuer `validate_technical_spec(..., zone_spec=...)`
und der Rueckfallvertrag zu dokumentieren. Die bestehende Legacy-Fassade und
ihre Diagnosen bleiben bis zu einem separat freigegebenen Umschalten erhalten.

Zeit- und Belegungsprofile bleiben bis zu einer eigenen P013-/P020-
Werteherkunftsentscheidung synthetische oder manuell bestaetigte Annahmen.
Norminhalte duerfen erst nach dokumentierten Nutzungsrechten sowie Quellen-,
Methoden- und Provenienzmatrix verarbeitet oder als Werte uebernommen werden.

P032-W2b bleibt davon getrennt; keine Config-Moves, Paketumbenennungen,
Dependencies oder externen Aktionen ableiten. Die fuer die V1-UI und P014-S4
erzeugten lokalen Katalogdaten bleiben ignoriert und unpubliziert. Die lokalen
Releases `v0.30.0` und `v0.30.1` sind vorhanden, aber noch nicht zu
`origin/main` gepusht; eine erneute explizite Push-Bestätigung ist erforderlich.

### P032-W3a-T1-Planung vom 2026-07-19

Mira, Vera und Professor Sophia stimmen gemaess UD-089 bedingt fuer den
kleinen, lokalen und reversiblen Legacy-Kompatibilitaetsslice. Vor seiner
Umsetzung ist die Entscheidung 42 in `TECHNICAL_DECISIONS.md` verbindlich:
eine additive zonenseitige Integritaets-API, unveraenderte Legacy-Fassade,
keine Runtimekante `ma_technical -> ma_zones`, synthetische Paritaetstests und
ein Rueckfall ohne Loeschung der Legacy-Fassade.

Der Slice ist kein voller Ownership-Transfer und migriert weder UI noch
`ma_parameters`-Aufrufer. Er erlaubt keine Config-, Daten-, Schema-,
Paket-, Dependency-, W2b- oder externen Aenderungen. Die spaetere
Aufrufermigration und die Entfernung der voruebergehenden
Kompatibilitaetsdoppelung bleiben eigene Freigabewellen.

## Handover-Ergaenzung 2026-07-21

Das technische Handover bestaetigt die bestehende Architekturgrenze: Eine
spaetere `ma_database`-Schicht darf dateibasierte Repositories fuer Drafts,
Revisionen, ChangeSets, Branches und Abhaengigkeitsindizes ersetzen. Sie
uebernimmt dabei weder TGA-Fachklassen noch technische Regeln; deren Ownership
bleibt bei `ma_technical`. Eine Persistenzmigration ist kein Teil des aktuell
freigegebenen P032-W3a-T1-Kompatibilitaetsslices.
