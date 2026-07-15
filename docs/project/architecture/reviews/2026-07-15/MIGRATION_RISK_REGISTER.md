# Migration Risk Register

Stand: 2026-07-15  
Status: Vorschlag, keine Migrationsfreigabe

## Leitplanken

- Kein Big Bang, kein Loeschen und keine produktive Verschiebung aus diesem
  Audit heraus.
- Jede Welle braucht einen eigenen freigegebenen Umfang, eine saubere
  Ausgangsbasis und eine unabhaengige Abnahme.
- Kompatibilitaetsadapter werden vor dem Umstellen der Aufrufer eingefuehrt
  und erst nach belegter Nichtnutzung separat entfernt.
- Datenpfade werden spaeter nach dem Muster `copy -> checksum -> validate ->
  switch reference -> retain source` migriert. Ein Delete ist keine
  Rueckrollstrategie.
- Geschuetzte Inhalte werden weder fuer Dry Runs noch fuer allgemeine Tests
  benoetigt. Synthetische Fixtures bilden nur Struktur und Verhalten nach.
- Git-Rueckrollen erfolgen ueber einen nachvollziehbaren Gegencommit oder
  einen neuen Korrekturcommit, nicht ueber destruktives Zuruecksetzen.

## Risikoregister

| ID | Risiko | Wkt. | Auswirkung | Fruehwarnsignal | Vorbeugung | Reaktion / Rueckfall | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MR-01 | Imports brechen nach Ownership-Wechsel | hoch | hoch | Collection-Fehler, fehlende Symbole | oeffentliche Facade und Contract-Tests vor Aufruferwechsel | Aufrufer auf Adapter zurueckstellen; Zielimplementierung korrigieren | jeweilige Fachmodule |
| MR-02 | Der Zyklus `ma_parameters <-> ma_variants` bleibt ueber Reexports verdeckt bestehen | mittel | hoch | Importgraph zeigt Rueckkante | verbotene Importkante automatisiert testen | Reexport nur im konsumierenden Altpfad; Modelle beim Owner belassen | ma_parameters, ma_variants |
| MR-03 | `ma_technical -> ma_zones` wird durch neue Hilfsimporte erneut eingefuehrt | mittel | hoch | Importvertrag scheitert | zonenabhaengige Pruefung eindeutig `ma_zones.validation` zuordnen | betroffene Pruefung auf stabilen technischen Vertrag umstellen | ma_technical, ma_zones |
| MR-04 | Alias-Layer wird zum dauerhaften zweiten Owner | hoch | mittel | neue Aufrufer verwenden weiterhin Altpfad | Deprecation-Hinweis, Nutzungsinventar und Ausstiegsdatum je Alias | Alias nicht erweitern; Entfernung als eigene spaetere Welle | Architektur-Owner |
| MR-05 | Daten- oder Ergebnisreferenzen zeigen nach Pfadwechsel ins Leere | mittel | hoch | fehlende Dateien, Checksum mismatch | copy-first, Manifest, relative Referenzen und Dry Run | Referenz auf Quellpfad zurueckschalten; Kopie behalten | Datenowner |
| MR-06 | Git-Historie wird durch gleichzeitige Moves und Umschreibungen unlesbar | mittel | mittel | Review zeigt komplette Dateien als neu | `git mv` und Inhaltsaenderung in getrennten Wellen | Welle abbrechen und als getrennte, additive Aenderung neu vorbereiten | Integrator |
| MR-07 | Alembic-Revisionen oder persistierte Daten verlieren Modellbezug | mittel | sehr hoch | Upgrade-/Downgrade- oder Repository-Test scheitert | DB-Ownership zuletzt; Revisionen nie umnummerieren; Backup vor Lauf | alte Importfacade wiederherstellen; keine produktive DB migrieren | ma_database |
| MR-08 | Run-Pakete sind trotz neuer Ordner nicht reproduzierbar | mittel | hoch | Ergebnisse ohne Code-/Inputfingerprint | Manifestpflicht und deterministische synthetische Referenzlaeufe | Run als `incomplete` markieren; Freigabe sperren | ma_simulation_setup |
| MR-09 | Environment-Drift bleibt zwischen `pyproject.toml`, `requirements.txt` und Editable-Metadaten | hoch | hoch | Version 0.20.0 statt 0.28.0; fehlende Imports | klare Dependency-Wahrheit, frische Testumgebung, Build-Smoke-Test | Environment neu aus definierter Quelle erstellen; keine Releasefreigabe | Repository-Owner |
| MR-10 | CI unterscheidet sich vom lokalen Windows-Ablauf | mittel | mittel | lokal gruen, CI rot oder umgekehrt | Restricted-Profil, plattformneutrale Befehle, gleiche Pythonmatrix | CI zunaechst advisory; Abweichung dokumentieren und lokal reproduzieren | Quality-Owner |
| MR-11 | Geschuetzte oder private Inhalte gelangen in Git, LFS, Graph oder Logs | niedrig | sehr hoch | unerwartete Binaerdateien, Pfade oder Textfragmente im Diff | positive Allowlist, Ignore-Tests, Compliance-Preflight, Sanitization | Vorgang stoppen; keine Veroeffentlichung; Rechte- und Incident-Pruefung | Compliance-Owner |
| MR-12 | `.gitignore` wird faelschlich als Verarbeitungsrecht interpretiert | mittel | sehr hoch | Scanner greift auf ignorierte Dateien zu | dokumentierte Objektfreigabe und `git ls-files` als Standardscope | Verarbeitung abbrechen; Artefakte lokal sicher entfernen lassen | Compliance-Owner |
| MR-13 | Obsidian-Links und externe Notizen brechen nach Dateiverschiebungen | unbekannt | mittel | Vault enthaelt alte Repo-Pfade | Vault-Pfad und Linkinventar vor jeder Doku-Migration; Adapterlinks | Doku-Pfad beibehalten oder Linkmapping ausspielen | Nutzer, Governance |
| MR-14 | Datierter Audit wird zur zweiten Architektur- oder Statuswahrheit | mittel | hoch | aktive Regeln werden nur im Review gepflegt | Snapshot-Kennzeichnung; Entscheidungen und Status in kanonischen Dateien | Review korrigieren und kanonische Quelle explizit verlinken | Governance |
| MR-15 | Codex folgt veralteten Pfaden, Befehlen oder doppelten Anweisungen | mittel | hoch | Aenderungen landen beim falschen Owner | P032-Mapping, Contract-Tests und Update der kanonischen Router je Welle | Agentenlauf stoppen; Pfad- und Truth-Mapping aktualisieren | Tera |
| MR-16 | Graphify erzeugt veraltete oder unbelegte Abhaengigkeiten | hoch | mittel | Graph und Python-Importtest widersprechen sich | Toolversion, Commit, Scope, Fakt/Inferenz und Timestamp speichern | Graph verwerfen und deterministische Analyse neu erzeugen | Architektur-Owner |
| MR-17 | Zu viele leere Zielordner und Abstraktionen erhoehen Wartungsaufwand | mittel | mittel | Gerueste ohne Aufrufer oder Tests | Ordner erst mit erstem realen Inhalt; kein Frameworkumbau | ungenutzten Vorschlag nicht umsetzen; keine Datei loeschen ohne Freigabe | Integrator |
| MR-18 | Fachlogik wird bei der Variantenzerlegung falsch einem Zielmodul zugeordnet | mittel | hoch | Zielmodul importiert wieder `ma_variants` oder dupliziert Modelle | Ownership vor jeder Extraktion fachlich bestaetigen | Altimplementierung hinter Facade weiterverwenden; Entscheidung erneut oeffnen | Fachowner, Nutzer |
| MR-19 | Golden Files konservieren einen Fehler statt eine Referenz | mittel | mittel | Test besteht trotz fachlich falschem Ergebnis | fachliche Abnahme, Erzeugungsbefehl und kleine lesbare Artefakte | Golden File nicht blind aktualisieren; Ursache und Erwartung pruefen | Fachowner, Professor Sophia |
| MR-20 | Architekturarbeit verdraengt den MVP | hoch | hoch | mehrere Wellen ohne fachlichen Durchstich | Wellen an P011-P030 koppeln; nur Blocker und beruehrte Bereiche migrieren | Architekturwelle pausieren; MVP-Slice priorisieren | Projektowner |

## Voraussetzungen fuer jede Welle

1. Freigegebener Scope und benannter Datei-/Modulowner.
2. Sauber inventarisierter Ausgangsdiff; fremde Arbeitsstaende bleiben
   unberuehrt.
3. Bestehende Tests fuer den betroffenen Vertrag sind gruen.
4. Neue Contract- und Regressionstests sind vor dem Umschalten definiert.
5. Daten-, Lizenz-, externe Tool- und Veroeffentlichungsgates sind fuer den
   exakten Gegenstand belegt.
6. Rueckfallpfad benoetigt weder Dateiloeschung noch geschuetzte Datenkopie.
7. Plan, ADR-Status, Mappingzeilen und Changelogrolle sind bekannt.

Das vom Auftrag vorgegebene CSV-Schema besitzt bewusst keine zusaetzlichen
ID-, Wellen- oder Statusspalten. `current_path` ist deshalb je Zeile eindeutig
und enthaelt nur einen realen Pfad oder einen klaren `[missing]`-Platzhalter.
Eine spaetere Wellenfreigabe nennt die betroffenen Zeilen ueber diesen Wert;
Umsetzungsstatus gehoert in den P032-Plan und das Changelog, nicht rueckwirkend
in den datierten Mapping-Snapshot.

## Vorgeschlagene Migrationswellen

### Welle 0 - Entscheidung und belastbare Baseline

**Voraussetzungen:** keine produktive Migration; dieser Audit liegt vor.

**Exakter Umfang:**

- ADR-P032 entweder annehmen, aendern oder ablehnen;
- Workspace-Anwendung versus portable Distribution entscheiden;
- Ownership der Parameter-/Optionskataloge bestaetigen;
- Ausgangsstand von Imports, Tests, Build-Metadaten und dokumentierten
  Entrypoints erfassen;
- fuer die erste geplante Welle die betroffenen Mappingzeilen eindeutig ueber
  `current_path` benennen.

**Dry Run:** statischer Importgraph nur ueber `git ls-files`; CSV maschinell
parsen; dokumentierte Befehle read-only gegen Entrypoints pruefen.

**Tests:** komplette bestehende Suite, Ruff, `git diff --check` und ein
Build-/Wheel-Smoke-Test in der vorhandenen Umgebung, beispielsweise
`.\.venv\Scripts\python.exe -m pip wheel --no-deps --no-build-isolation --wheel-dir <temp> .`,
sofern die dafuer bereits vorhandenen Buildwerkzeuge ausreichen.

**Abnahme:** ADR-Status und offene Entscheidungen sind eindeutig; Baseline
ist reproduzierbar protokolliert; keine Produktdatei wurde verschoben.

**Rueckfall:** nicht erforderlich, weil nur Entscheidung und Audit.

**Handover:** P032 verweist auf Baseline, freigegebene Welle und genaue
Mappingzeilen.

### Welle 1 - Guardrails, Pfad- und Dokumentationswahrheit

**Voraussetzungen:** Welle 0 abgenommen; Hook-, CI- und Dependency-Aenderungen
jeweils separat freigegeben.

**Exakter Umfang:**

- Root- und Data-README an reale Entrypoints und Pfade angleichen;
- Ignore-Defense fuer geschuetzte Zielbereiche mit synthetischen Pfadtests,
  einschliesslich der derzeit nicht robust abgedeckten Katalog-Unterpfade
  `data/catalogs/materials/`, `products/` und `sources/`;
- Importregeln als Contract-Test abbilden;
- Zweck von `requirements.txt` und stale Editable-Metadaten klaeren;
- Entwurf fuer `WorkspacePaths` anhand realer Aufrufer, noch ohne breite
  Umstellung.

**Dry Run:** `git check-ignore --no-index` nur mit erfundenen Dateinamen;
Entrypoint- und Pfadreferenzsuche auf versionierten Dateien.

**Tests:** Project-Agent- und Architektur-Contracts, dokumentierte Command-
Smokes, vorhandene Suite, Build-/Version-Smoke-Test.

**Abnahme:** keine README zeigt auf entfernte Pfade; verbotene Importkanten
werden erkannt; keine geschuetzte Datei wurde gelesen.

**Rueckfall:** additive Tests und Dokumentation korrigieren; bestehende
Runtimepfade bleiben bis zur naechsten Welle aktiv.

**Handover:** neue Guardrails in `UPDATE_ROUTINES.md` nur dann aufnehmen,
wenn sie tatsaechlich Teil einer Routine werden.

### Welle 2 - Parameter-/Optionsownership und Zyklusabbau

**Voraussetzungen:** ADR akzeptiert; `ma_parameters` als Owner bestaetigt;
alle aktuellen Katalognutzer inventarisiert.

**Exakter Umfang:**

- Parameter- und Optionsmodelle samt Loader nach `ma_parameters` verschieben;
- alte `ma_variants.*_catalog`-Importpfade als getestete Reexports erhalten;
- `ma_parameters.services` auf eigene Vertrage umstellen;
- Beispielkonfiguration nach `config/ma_parameters/` verschieben und
  Altpfadkompatibilitaet begrenzen;
- keine weiteren Kataloge in dieser Welle.

**Dry Run:** Importersetzungsliste und Config-Aufloesung mit synthetischen
Beispielen; alter und neuer Import liefern identische Vertragstypen.

**Tests:** Katalogschema, Loader, ParameterSnapshot, Preprocess, alle
Importpfade, statischer Nachweis ohne `ma_parameters -> ma_variants`.

**Abnahme:** echter Laufzeitzyklus ist entfernt; alter API-Pfad bleibt
funktional und eindeutig als Adapter markiert; Full Suite ist gruen.

**Rueckfall:** interne Aufrufer wieder auf Alt-Facade richten; neue
Owner-Implementierung nicht loeschen, bis Ursache geklaert ist.

**Handover:** P015/P017, Modul-READMEs und Mappingstatus aktualisieren; Alias-
Ausstieg als eigener spaeterer Punkt.

### Welle 3a - Technik-Zonen-Richtung

**Voraussetzungen:** P013/P014-Uebergabevertrag stabil.

**Exakter Umfang:** nur den zonenabhaengigen Technikabgleich nach
`ma_zones.validation` verlagern und `ma_technical -> ma_zones` als verbotene
Runtimekante testen. Keine Pfad- oder Datenmigration.

**Dry Run:** alte und vorgeschlagene Pruefung mit identischen synthetischen
P013/P014-Vertraegen vergleichen.

**Tests:** P013/P014-Regressionen, ThermalBuildingModel, Importvertrag und
Full Suite.

**Abnahme:** keine Reverse-Runtimekante; identische Freigabeentscheidungen
und Referenzmodelle.

**Rueckfall:** Aufrufer auf die alte Prueffassade zurueckstellen; neue
zonenbezogene Implementierung bis zur Ursachenpruefung erhalten.

**Handover:** P013/P014 und Architekturvertrag synchronisieren.

### Welle 3b - Begrenzter WorkspacePaths-Slice

**Voraussetzungen:** explizite Workspace-Semantik aus Welle 0 entschieden;
Welle 3a ist keine technische Voraussetzung.

**Exakter Umfang:** zentrale Workspace-Root-Aufloesung einfuehren und nur die
Building-, Technical- und Zones-Pfadhelfer kontrolliert anbinden. Fachliche
relative Pfade bleiben in ihren Modulen; keine allgemeine Pfadmigration.

**Dry Run:** bestehende Demo- und Referenzpfade gegen alten und neuen Resolver
auflisten; keine Nutzdatei verschieben.

**Tests:** Pfadvertraege aus Checkout und explizitem Workspace, bestehende
Building-/Technical-/Zones-Loader und Full Suite.

**Abnahme:** identische Pfadauflosung fuer den freigegebenen Scope; keine
lokalen Nutzdaten veraendert.

**Rueckfall:** Modulpfadhelfer verwenden wieder ihre bisherige Rootauflosung;
der neue neutrale Resolver bleibt ungenutzt, bis die Ursache geklaert ist.

**Handover:** betroffene Modul-READMEs und Workspace-Entscheidung
synchronisieren.

### Welle 4 - Variantenpaket fachlich verkleinern

**Voraussetzungen:** Welle 2 gruen; je Zielbereich stabiler Vertrag und
fachlicher Owner; keine DB-Migration in dieser Welle.

**Exakter Umfang:** in getrennten Teilwellen Economics, Reporting und UI aus
`ma_variants` nach `ma_economy`, `ma_reporting` und `ma_ui` ueberfuehren;
`naming`, `selection` und `variant_manager` bleiben im Variantenpaket.

**Dry Run:** Aufruferliste und API-Gleichheit je Teilwelle; alte und neue
Services mit identischen synthetischen Inputs vergleichen.

**Tests:** bestehende Economic-, Reporting-, Varianten-UI- und Entry-Point-
Tests plus neue Facade-Contracts; Full Suite je Teilwelle.

**Abnahme:** Zielpaket besitzt Implementierung und Tests; Altpfad ist nur
Adapter; kein Zielpaket importiert die Altimplementierung zyklisch.

**Rueckfall:** Composition Layer auf Alt-Facade zurueckstellen; keine
gleichzeitige Aliasentfernung.

**Handover:** P017, P022, P025 und P027 jeweils nur fuer ihre abgeschlossene
Teilwelle aktualisieren.

### Welle 5a - Neutraler Run-Vertrag

**Voraussetzungen:** P018-Vertraege umgesetzt; keine IDA-/EQUA-Datei
erforderlich.

**Exakter Umfang:** nur das neutrale Run-Paket unter
`data/ma_simulation_setup/runs/<run_id>/`, Manifest, Status und Provenienz mit
synthetischen Inputs implementieren.

**Dry Run:** Manifest in einem temporaeren Testverzeichnis erzeugen; keine
externe Anwendung starten.

**Tests:** Run-Provenienz, Checksummen, Statusmaschine und deterministische
Materialisierung.

**Abnahme:** synthetischer Run ist reproduzierbar und referenziert Code,
Konfiguration und Eingaben eindeutig.

**Rueckfall:** Run als `incomplete` sperren und bisherigen P018-Vertrag weiter
verwenden.

**Handover:** P018, Run-Schema und Benutzeranleitung synchronisieren.

### Welle 5b - Simulations-Exportadapter

**Voraussetzungen:** Welle 5a stabil; P009-Exportscope und objektbezogene
IDA-/EQUA-Grenzen geklaert. Kein automatischer Simulationsstart.

**Exakter Umfang:** nur den bestehenden IDA-Exportprototyp hinter
`ma_export_simulation` einordnen und den Altpfad als getestete Fassade
erhalten.

**Dry Run:** synthetisches Exportartefakt im Tempbereich erzeugen; keine
proprietaere Datei lesen und IDA ICE nicht starten.

**Tests:** neutraler Exportport, Adapterkonfiguration, Golden File und
Altpfadkompatibilitaet.

**Abnahme:** Export ist ohne externe Anwendung deterministisch; keine
geschuetzten Inhalte im Diff oder Log.

**Rueckfall:** Run-Setup wieder auf die Alt-Facade richten; neuen Adapter
nicht loeschen, bis die Ursache geklaert ist.

**Handover:** P009, P018 und Compliance-Belegreferenzen synchronisieren.

### Welle 5c - Ergebnisimport und Normalisierung

**Voraussetzungen:** stabiler neutraler Run-Vertrag; freigegebenes
synthetisches Ergebnisformat. Ein realer IDA-Import bleibt objektbezogen.

**Exakter Umfang:** nur Adapter und Ergebnisvertraege nach
`ma_import_simulation` ueberfuehren; keine Analyse- oder Exportlogik.

**Dry Run:** synthetische Ergebnisdatei einlesen, unveraenderten Inputhash und
normalisierten Output vergleichen.

**Tests:** Importdiagnosen, Provenienz, Schemas, Fehlerfaelle und Altpfad-
Facade.

**Abnahme:** Ergebnis ist eindeutig `RUN` und `VAR` zugeordnet; Rohinput und
Normalisierung sind getrennt.

**Rueckfall:** Ergebnisaufnahme auf Alt-Facade zurueckstellen und neuen Import
fuer weitere Runs sperren.

**Handover:** P009/P018 und Importdokumentation synchronisieren.

### Welle 5d - Analysemetrik und Datenexport

**Voraussetzungen:** Welle 5c liefert einen stabilen normalisierten Vertrag;
fachliche Metriken und Ausgabeformat sind bestaetigt.

**Exakter Umfang:** in zwei einzeln abnehmbaren Teilwellen zuerst Metriken
nach `ma_analyse`, danach Ergebnisverpackung nach `ma_data_export`
ueberfuehren. Ein Commit bleibt eine separate Freigabeentscheidung.

**Dry Run:** alte und neue Metriken beziehungsweise Exporte mit identischem
synthetischem Normalergebnis vergleichen.

**Tests:** numerische Regressionen, Einheiten, deterministische Exportschemas,
Golden Files und Altpfadkompatibilitaet.

**Abnahme:** Ergebnisgleichheit ist belegt; Analyse und Export importieren
nicht die Altimplementierung zyklisch.

**Rueckfall:** je Teilwelle den Composition Layer auf die Alt-Facade
zurueckstellen; keine gemeinsame Ruecknahme beider Owner erzwingen.

**Handover:** P009, P019, P026 und P030 nur fuer den real umgesetzten
Teilschritt aktualisieren.

### Welle 6 - Spaete und optionale Strukturbereiche

**Voraussetzungen:** MVP-Bedarf nachgewiesen; eigene Freigaben fuer DB,
Katalogownership, Research, CI, Graphify oder Obsidian.

**Exakter Umfang:** jeweils als separate Teilwelle:

- Datenbankmodelle und Repositories fachlich trennen, Alembic-Historie
  erhalten;
- Material-, System-, Produkt-, Quellen- und Dokumentkataloge einzeln
  zuordnen;
- P030-Code unter `src/research_tools/` und Messpakete unter dem bestehenden
  Zielpfad `research_measurements/EVAL-<id>/` mit echtem Inhalt anlegen;
- Restricted-CI einrichten;
- optionaler Graphify-Pilot oder Obsidian-Adapter nach eigener Freigabe.

**Dry Run:** pro Teilwelle; externe Tools nur in bereinigtem Testsandbox-Scope.

**Tests:** DB-Migrationen, Katalogschemata, Research-Reproduzierbarkeit,
CI-Paritaet beziehungsweise Graph-/Vault-Sanitization passend zur Teilwelle.

**Abnahme:** keine Teilwelle wird allein wegen des Zielbaums umgesetzt; ihr
fachlicher Nutzen, Scope, Rechte und Wartungsowner sind belegt.

**Rueckfall:** Teilwelle separat per Gegencommit zuruecknehmen oder Adapter
reaktivieren; Datenquellen und Alembic-Historie bleiben erhalten.

**Handover:** kanonischen Fachplan, ADR-Nachtrag, Entscheidungen und
Changelog nur fuer die tatsaechlich umgesetzte Teilwelle aktualisieren.

## Wellenuebergreifende Abnahme

Eine Welle gilt erst als abgeschlossen, wenn:

1. alle in der Wellenfreigabe ueber `current_path` genannten Mappingzeilen
   einen im P032-Plan belegten Ist- und Zielstatus besitzen;
2. fokussierte Tests, Full Suite, Ruff und `git diff --check` gruen sind;
3. neue Imports, Pfade und Konfigurationen dokumentiert sind;
4. kein unerwarteter Zugriff auf ignorierte oder geschuetzte Inhalte
   stattgefunden hat;
5. ein unabhaengiger Qualitaetsreview keine offenen Blocker meldet;
6. bei Daten, externen Tools oder Veroeffentlichung der konkrete
   Compliance-Preflight dokumentiert ist;
7. Planstatus, Entscheidung und Changelog die reale Umsetzung beschreiben,
   nicht nur das Zielbild.
