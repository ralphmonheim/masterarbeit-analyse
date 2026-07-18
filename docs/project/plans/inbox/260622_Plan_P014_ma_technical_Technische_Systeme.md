# P014 ma_technical Technische Systeme

Stand: 2026-07-18
Status: Fachlich konsolidiert, P014-S1 Legacy-v1 kompatibel, v2-Kerntypen sowie P014-S1.1/S1.2, P014-S2, P014-S3a und P014-S4 umgesetzt; optionale lokale Katalogauswahl vorhanden; P013/P015-Releasecheckpoint angebunden, v2-Werteherkunft und Restumfang von P015-S3b offen
Prioritaet: Hoch
Abhaengigkeiten: P010, P012, P013, P015, P017, P027

## Ziel

`ma_technical` erfasst zentrale technische Systeme programmneutral,
typisiert, versioniert und manuell bearbeitbar. Das Modul liefert langfristig:

- freigegebene Technikrevisionen,
- zentrale Plant-, Erzeuger-, Speicher-, AHU-, Elektro- und Topologieobjekte,
- Serviceinterfaces fuer `ma_zones`,
- technische Parameter- und Regelquellen fuer `ma_parameters`, `ma_rules` und
  spaeter `ma_variants`,
- reproduzierbare Fachstaende fuer Varianten und Runs.

## Schutzgrenzen

Fuer den aktuellen Masterarbeitsumfang gelten folgende Grenzen:

- kein IDA-ICE-Adapter,
- kein IDA-ICE-Export,
- keine automatische Dimensionierung,
- keine Templates oder Fremdimporte,
- erste UI ausschliesslich manuell,
- keine Variantenbildung in `ma_technical`,
- keine automatische Aenderung von `ma_parameters`, `ma_variants` oder Runs,
- lokale Katalogdaten werden weder versioniert noch veroeffentlicht;
  vorhandene Werte bleiben `draft_unverified` und duerfen nicht automatisch in
  Revisionen, Parameter, Varianten oder Runs uebernommen werden,
- freigegebene Revisionen, historische Varianten und Runs werden nie
  ueberschrieben,
- Kapazitaetsausreichung ist keine blockierende Eingabevalidierung.

Eine bewusst kleine oder unbegrenzte technische Leistung ist als Eingabewert
zulaessig. Ob sie unter Wetter-, Nutzungs- und Gebaeuderandbedingungen
ausreicht, wird erst spaeter durch Simulation und Analyse bewertet.

## Bestehender v1-Vertrag

P014-S1 ist umgesetzt und bleibt als Legacy-v1-Vertrag erhalten:

- Paketstruktur `src/ma_technical/` mit Fachmodellen, Standardpfaden,
  YAML-Loader und Validierung.
- Versionierte BusinessIntegration-LoD-1/Lite-Demo:
  `config/ma_technical/examples/business_integration_lod1_technical_spec.yaml`.
- Demo mit einfachen Referenzannahmen fuer Heizung, Kuehlung und Lueftung.
- Validierung von Pflichtfeldern, eindeutigen IDs, Systemtypen,
  bedienten Zonen, positiven Leistungs-/Luftwechselwerten,
  Waermerueckgewinnung und Zonenmodellbezug.
- Streamlit-Pruefansicht mit Freigabestatus, Systemen und Annahmen.

Die Felder `source_zone_model_id` und `served_zone_ids` sind direkte
Zonenreferenzen und damit Legacy. Sie bleiben kompatibel, bis eine
kontrollierte Migration auf Serviceinterfaces umgesetzt ist.

### Optionaler lokaler Demo-Katalog

Umgesetzt am 2026-07-15: Der Loader kann einen lokal vorhandenen, per
Manifestpruefsumme gesicherten Demo-Katalog unter
`config/ma_database/catalogs/v0.1.0/` lesen. Dieser Pfad ist ignoriert; seine
Daten werden nicht in das Repository oder den oeffentlichen Release
aufgenommen. Die Technikansicht fuehrt nur Heiz-/Kuehlerzeuger und thermische
Speicher in eigenen Fachreitern. Fuer Heizung, Kuehlung, Lueftung, Speicher,
Trinkwarmwasser und Elektrik ist `Nicht vorhanden` ein expliziter
Sitzungsstatus `not_installed`; ohne lokalen Katalog bleibt zusaetzlich eine
neutrale Auswahl ohne Datensatz moeglich. Materialien und Konstruktionen
liegen allein bei `ma_building`. Jede lokale Auswahl bleibt `demo_unverified`;
sie ist kein technisches Modell, keine freigegebene Revision und keine
Simulations- oder Dimensionierungseingabe.

## Zielmodell v2

Das parallele Schema v2 ersetzt v1 nicht sofort, sondern beschreibt die
kuenftige Fachstruktur:

```text
TechnicalModelSpecification
├── building_reference
├── equipment_register
├── distribution_register
├── storage_register
├── domestic_hot_water_register
├── plant (optional)
├── air_handling_unit (optional)
├── electrical_system (optional)
├── schedules
├── topology
├── service_interfaces
├── assumptions
└── source_metadata
```

Kernprinzipien:

- physische Geraete und funktionale Rollen getrennt modellieren,
- reversible Geraete ueber Referenzen mehrfach nutzbar machen,
- IDA-Slot und fachliche Rolle trennen,
- technische Parameter als konkrete Fachfelder, keine IDA-Key-Value-Maps,
- Serviceinterfaces statt direkter Zonenreferenzen,
- Zeitplaene im technischen Register referenzieren,
- Quellen, Annahmen und Entscheidungskontext mitfuehren.

## Slice 0 - Dokumentation und Schutz

Umgesetzt bzw. aufzunehmen:

- P014 mit dem neuen Gesamtplan konsolidieren,
- v1/LoD-1 als Legacy-Vertrag kennzeichnen,
- Planindex und Planstatus aktualisieren,
- Nutzerentscheidungen zum v2-Zielmodell dokumentieren,
- keine alte Demo loeschen oder ungeplant umstellen.

## Slice 1 - Kerntypen und Schema v2

Der erste Code-Slice legt nur typisierte Kerne an:

```text
src/ma_technical/
├── enums.py
├── metadata.py
├── equipment.py
├── plant.py
├── distribution.py
├── domestic_hot_water.py
├── ahu.py
├── electrical.py
├── topology.py
├── schedules.py
└── specification.py
```

Nicht Teil von Slice 1:

- v1-zu-v2-Migration,
- Repository, Working Drafts und Revisionen,
- Parameterexport,
- UI-Editor,
- Topologie-Befehle,
- technische Regelengine,
- IDA-Adapter oder Export.

## Preprocess V1

Der verbindliche erste Zielstand ist eine simulationsbereite
Preprocessing-Kette mit manueller IDA-ICE-Uebergabe. `ma_technical` liefert
darin eine freigegebene, reproduzierbare v2-Technikrevision an `ma_zones` und
`ma_parameters`; ein IDA-Adapter, Produktdaten oder ein Technikeditor gehoeren
nicht dazu.

Die naechste Arbeit beginnt bewusst nicht mit Branches oder einem Editor. Die
v2-Kerntypen muessen zuerst als vollstaendiger, pruefbarer Fachstand vorliegen.

### P014-S1.1 V2-Aggregat und Referenzintegritaet

Umgesetzt am 2026-07-14:

- `TechnicalModelSpecification` buendelt physische Geraete, Heiz- und
  Kuehlverteilungen, thermische Speicher sowie Trinkwarmwassererzeugung in
  unveraenderlichen Registern.
- Die drei Primaerbereiche Plant, AHU und Elektrik sind optional, damit ein
  fachlich nicht benoetigter Bereich nicht durch ein Dummy-Objekt modelliert
  werden muss.
- Die Trinkwarmwassererzeugung besitzt eine eigene ID und kann damit als
  internes Registerobjekt referenziert und in P014-S1.2 validiert werden.
- `object_id_locations()` liefert alle Fundstellen unverkuerzt als Grundlage
  fuer die nachfolgende Duplikat- und Referenzpruefung.

Noch nicht umgesetzt ist bewusst die Fehlerdiagnostik fuer doppelte IDs und
nicht aufloesbare Referenzen; sie gehoert zu P014-S1.2.

- `TechnicalModelSpecification` erhaelt vollstaendige Register fuer
  `PhysicalEquipment`, Heiz- und Kuehlverteilungen, thermische Speicher und
  Trinkwarmwassererzeugung.
- Jede Objekt-ID ist im gesamten Aggregat eindeutig; alle internen
  `ObjectReference`-Ziele sind anhand von ID und Objektart aufloesbar.
- `plant`, `air_handling_unit` und `electrical_system` sind in V1 jeweils
  optionale Primaerbereiche. Ein nicht benoetigter Bereich wird als fehlend
  modelliert, nicht durch ein fachlich falsches Dummy-Objekt ersetzt.
- Serviceinterfaces bleiben zonenfrei. Sie referenzieren nur zentrale
  Technikobjekte und deklarieren Medium, Kapazitaetsmodus sowie
  Terminal-Kompatibilitaet.
- Nicht Teil: YAML-Persistenz, Revisionsverwaltung, UI, Parameterexport oder
  eine fachliche Kapazitaetsausreichungspruefung.

### P014-S1.2 V2-Struktur- und Referenzvalidierung

Umgesetzt am 2026-07-14: separater v2-Validator mit Pruefung von Modellkopf,
doppelten Objekt-IDs, aufloesbaren internen `ObjectReference`-Zielen,
Serviceinterface-Referenzen und leistungswertpflichtigen Kapazitaetsmodi.
Der Legacy-v1-Validator bleibt unveraendert parallel bestehen.

- Eigenen v2-Validator neben `validate_technical_spec` des Legacy-v1-Vertrags
  einfuehren; der v1-Validator wird nicht umgedeutet.
- Pruefen: Modellkopf, Pflichtfelder, eindeutige IDs, gueltige Objektarten,
  aufloesbare Referenzen, Kapazitaetsmodi, Zeitplanreferenzen und Topologie.
- Pruefen: Ein Serviceinterface besitzt keine direkten Zonenreferenzen und
  verweist auf eine passende zentrale Quelle; Medium und deklarierte
  Terminal-Kompatibilitaet sind strukturell plausibel.
- Eine fehlende oder zu kleine Leistung bleibt eine fachliche Annahme und keine
  Eingabeblockade. Unaufloesbare Referenzen oder widerspruechliche Struktur
  blockieren dagegen die Freigabe.

### P014-S2 Persistenz und freigegebene Technikrevision

Umgesetzt am 2026-07-14: Ein fehlerfreies v2-Modell wird als neue YAML-
Revision mit Modell-ID, Revisions-ID, Freigabestatus und Content-Hash
gespeichert. Bestehende Revisionen werden nie ueberschrieben; beim Laden wird
der gespeicherte Hash gegen die YAML-Nutzlast geprueft. Zeitstempel sind nicht
Teil des Content-Hashs.

- YAML-Schema und Roundtrip fuer eine v2-Referenztechnik definieren.
- Ein lokaler Working Draft wird erst nach erfolgreicher v2-Validierung als
  unveraenderliche, freigegebene Technikrevision abgelegt.
- Die Revision fuehrt mindestens technische Modell-ID, Revisions-ID,
  Freigabestatus, Quellen- und Annahmenmetadaten sowie Content-Hash.
- Der Content-Hash entsteht aus einer kanonischen fachlichen Darstellung mit
  stabiler Reihenfolge. Lokale Dateipfade und Erstellungszeitpunkte gehen nicht
  in den Hash ein; Quellenreferenzen und Annahmen dagegen schon.
- Nicht Teil: mehrere Draft-Branches, graphische Bearbeitung oder Migration
  des Legacy-v1-Modells.

### P014-S3 Uebergabevertrag an P013 und P015

- `ma_zones` erhaelt nur stabile Referenzen auf freigegebene
  Serviceinterfaces und zentrale technische Quellen. Lokale
  Uebergabesysteme, Terminalauswahl und konkrete Zonenbelegung bleiben bei
  P013.
- `ma_parameters` uebernimmt nur eine freigegebene Technikrevision mit
  Modell-ID, Revisions-ID, Content-Hash und Freigabestatus.
- Fuer V1 reicht die vom Serviceinterface deklarierte
  Terminal-Kompatibilitaet. Eine weitergehende fachliche Eignungspruefung
  wird als Folgearbeit behandelt.

#### P014-S3a / P015-S3b-prep: ReleasedTechnicalHandover

Council-Beschluss vom 2026-07-15: Mira, Vera und Justus bilden eine
einstimmige 3/5-Mehrheit fuer diesen lokalen, additiven Vorbereitungsslice
vor einem vorgezogenen P032-W2-Zyklusabbau. Der Scope bleibt auf synthetisch
testbare Referenzmetadaten begrenzt.

- `ma_technical` liefert aus einer hashkonsistenten, freigegebenen v2-Revision
  einen unveraenderlichen Handover mit Modell-ID, Revisions-ID, Content-Hash,
  Freigabestatus sowie stabilen Serviceinterface- und Quellobjektreferenzen.
- `ma_parameters` kann diesen Handover in eine bestehende
  `ParameterSourceReference` ueberfuehren. Die bisherige
  `ma_technical:<technical_model_id>`-Quellen-ID bleibt dabei kompatibel;
  Revision, Hash und Freigabestatus werden echt uebernommen.
- Nicht Teil sind die Ableitung oder Aenderung vorhandener v1-Parameterwerte,
  ein P013-Zonenfingerprint, die vollstaendige P015-S3b-Eingangspaketumstellung,
  P014-S4-Referenz-YAML, Persistenz, UI, Katalogdaten und P032-W2.

Umgesetzt am 2026-07-15: `ReleasedTechnicalHandover` und seine
Serviceinterface-Referenzen werden ausschliesslich aus einer freigegebenen,
hashkonsistenten `TechnicalModelRevision` erzeugt. Manipulierte Hashes,
inkonsistente Modell-IDs und nicht freigegebene Revisionen werden blockiert.
Die fokussierten P014-/P015-Tests bestehen mit `28 passed`, die vollstaendige
lokale Suite mit `513 passed`; `ruff check` und `git diff --check` sind gruen.

### P014-S4 V2-Referenzfall und Abnahme

Council-Beschluss vom 2026-07-18: Mira, Vera und Justus bilden gemaess
UD-089 eine einstimmige 3/5-Mehrheit fuer diesen lokalen, reversiblen
Abnahmeslice. Justus bewertet ihn mit Verweis auf
`SHARED-COMPLIANCE-003` und `SHARED-COMPLIANCE-004` in
`docs/compliance/shared/decision_log.yaml` als `green`.

- Eine kleine, ausschliesslich projektseitig erstellte V2-Spezifikation wird
  als versionierte YAML-Eingabe unter `config/ma_technical/examples/`
  hinterlegt. Sie traegt einen sichtbaren Synthetic-Header; alle IDs, Namen
  und Zahlenwerte sind konstruiert, nicht normativ und nicht fuer Entwurf
  oder Simulation bestimmt.
- Ein additiver allgemeiner V2-Parser/Loader bildet YAML-Mappings auf
  `TechnicalModelSpecification` ab. Er erzwingt `schema_version: "2.0"`,
  Pflichtfelder und bekannte Modellstrukturen einschliesslich verschachtelter
  Dataclasses, Enums, `ObjectReference`, optionaler Bereiche und
  Tupelregister. Unbekannte oder strukturell fehlerhafte Eingaben werden
  abgewiesen; anschliessend bleibt `validate_technical_model()` die fachliche
  Freigabepruefung.
- Der Legacy-V1-Loader `load_technical_spec()` und die bestehende
  Revisionsladefunktion bleiben unveraendert. Es wird keine erzeugte Revision
  mit Laufzeitstempel versioniert: Freigabe, Reload und Hash-Pruefung laufen
  ausschliesslich in `tmp_path`.
- Tests decken den allgemeinen Parser, Minimal- und verschachtelte Referenzen,
  optionale Bereiche, Schema-/Pflichtfeld-/Unbekanntfeldfehler, Revision und
  Hash-Stabilitaet, Serviceinterface-Regeln, den unveraenderten V1-Vertrag
  sowie die bestehende P013- und P015-Referenzkette ab.
- Der Abnahmenachweis zeigt: Eine aus der geladenen V2-Spezifikation
  freigegebene P014-Revision ist durch P013 referenzierbar und durch P015 als
  Eingabequelle uebernehmbar.

Ausgeschlossen bleiben V2-Werteherkunft, automatische Revisionen, UI/Editor,
V1-zu-V2-Migration, Katalog-, Produkt-, Normen- und reale Projektdaten,
IDA-Dateien, neue Dependencies, externe Verarbeitung, Hooks, Commits, Pushes
und Veroeffentlichungen.

Umgesetzt am 2026-07-18: `v2_loader.py` liefert einen strikt typisierten,
oeffentlichen V2-Einstieg fuer YAML oder Mapping-Daten. Er lehnt falsche
Schema-Versionen, fehlende oder leere Pflichttexte, unbekannte Felder,
ungueltige Enums und fehlerhafte verschachtelte Strukturen ab. Die
projektseitige Referenzdatei
`config/ma_technical/examples/technical_v2_reference_spec.yaml` bleibt
sichtbar als synthetischer, nicht normativer Testeingang. Ihre Freigabe,
Reload und der P013-/P015-Checkpoint laufen ausschliesslich lokal in
`tmp_path`.

Der Council hat im Abschlussreview einstimmig die zwingende Minimalergänzung
`Path.as_posix()` in der bestehenden Payload-Serialisierung bestaetigt: Damit
wird ein vorhandener relativer `InputSource.source_path` plattformstabil
hash- und YAML-faehig. Sie aendert weder den V1- noch den Revisionsvertrag;
absolute oder reale Pfade bleiben ausgeschlossen. Der abschliessende
relevante P014-Fokuslauf besteht mit `45 passed in 10.61s`, die vollstaendige
lokale Suite mit `591 passed in 193.30s`. Ruff-Check der betroffenen Dateien
sowie `git diff --check` sind gruen.

Nachtrag zum Abschlussreview am 2026-07-18: Vera, Mira und Professor Sophia
stimmen gemaess UD-089 einstimmig fuer eine minimale Vertragshaertung ohne
Architektur- oder Persistenzausbau. Persistierte V2-`input_source`-Objekte
benoetigen eine nichtleere `source_id`, damit der bestehende Content-Hash nicht
durch einen zufaelligen Laufzeitdefault variiert. Der Loader akzeptiert zudem
zeitzonenbehaftete YAML-Datetime-Skalare; naive Zeitpunkte bleiben gesperrt.
Der All-fields-Nachweis durchlaeuft den oeffentlichen YAML-Pfad sowie
Revision, Reload und wiederholte Hash-Gleichheit ausschliesslich mit
synthetischen Daten. Die Testzahlen werden nach dem abschliessenden Volltest
aktualisiert.

## Naechste Slices nach Preprocess V1

1. Mehrere Draft-Branches und weitergehende Revisionsverwaltung.
2. Technische Limits und Empfehlungen als Regelquelle.
3. Gefuehrte Topologie und umfassendere Serviceinterface-Bearbeitung.
4. Erweiterte Parametersicht fuer `ma_parameters`.
5. Manuelle Streamlit-Bearbeitung.
6. Kontrollierte Migration v1 -> v2.

## Abnahmekriterien fuer P014-S1.1

- v2-Kerntypen sind immutable und importierbar.
- `TechnicalModelSpecification` v2 kann ein minimales Modell beschreiben.
- `CapacityMode.ideal_unlimited` benoetigt keine Leistungszahl.
- Serviceinterfaces enthalten keine direkten `served_zone_ids`.
- v1-Demo-Loader und vorhandene P015/UI-Vertraege bleiben gruen.
