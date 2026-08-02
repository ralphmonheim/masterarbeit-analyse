# P014 ma_technical Technische Systeme

Stand: 2026-08-02
Status: Fachlich konsolidiert, P014-S1 Legacy-v1 kompatibel, v2-Kerntypen sowie P014-S1.1/S1.2, P014-S2, P014-S3a/P013-Assignment-Checkpoint, P014-S4, die projektbezogene UD-115-Freigabekette und die nachgelagerte P013-Assignment-UI umgesetzt; v2-Werteherkunft und Restumfang von P015-S3b offen
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
- Fuer die Masterarbeit ist dieser Satz der feste Referenzweg: eine generische
  Heizung, eine generische Kuehlung und eine zentrale Lueftung mit WRG. Die
  Lueftung stellt keine Heiz- oder Kuehlfunktion bereit. Varianten veraendern
  den Techniksatz nicht, sondern ausschliesslich freigegebene Zonenparameter.
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
7. Einen separaten Katalog-Slice erst nach der fachlichen Bestaetigung von
   Quellen, Einheiten und Einsatzgrenzen planen. Der gesichtete
   `ma_database`-Seed ist ausschliesslich ein `draft_unverified`-
   Referenzkatalog; er liefert weder Simulationswerte noch eine automatische
   lokale Kataloginstallation.

## Abnahmekriterien fuer P014-S1.1

- v2-Kerntypen sind immutable und importierbar.
- `TechnicalModelSpecification` v2 kann ein minimales Modell beschreiben.
- `CapacityMode.ideal_unlimited` benoetigt keine Leistungszahl.
- Serviceinterfaces enthalten keine direkten `served_zone_ids`.
- v1-Demo-Loader und vorhandene P015/UI-Vertraege bleiben gruen.

## Handover-Ergaenzung 2026-07-21

Das Varianten-Handover ergaenzt den bestehenden P014-Vertrag wie folgt:

- Technische Grenzen, Empfehlungen, Kompatibilitaeten und Abhaengigkeiten
  werden als versionierte Fachinformationen an `ma_rules` bereitgestellt;
  harte Grenzen blockieren, Empfehlungen erzeugen Warnungen.
- `ma_parameters` erhaelt eine standardisierte Parametersicht mit stabilen
  Pfaden, Einheit, Wert, erlaubten Werten, Variierbarkeit und Quelle. Es
  interpretiert das Technikmodell nicht neu und aendert es nicht direkt.
- `ideal_unlimited` bleibt ein expliziter Modus und wird nicht durch einen
  kuenstlich grossen Leistungswert ersetzt.
- Konkrete technische Optionen gelangen ausschliesslich ueber freigegebene
  Parameter- und Regelobjekte indirekt zu `ma_variants`.

Diese Punkte konkretisieren Folgeslices; die bestehende P014-v1/v2-Grenze und
alle freigegebenen Handover-Vertraege bleiben unveraendert.

## Umsetzungsstand 2026-07-24: synthetische SmallOffice-LoD-1-Technik

Fuer den ersten lauffaehigen SmallOffice-Durchstich wird der bestehende
Legacy-v1-Vertrag additiv mit einer synthetischen Heizungs-, Kuehlungs- und
Lueftungsreferenz genutzt. Systemtemperaturen und
Waermerueckgewinnungsgrad orientieren sich als vorlaeufige Startwerte an der
oeffentlich zugaenglichen GEG-Anlage 2. Spezifische Leistungen,
Leistungsfaktoren, Luftwechsel und Regelstrategien bleiben eigene
Demo-Annahmen.

Die Konfiguration ist keine Anlagenauslegung und fuehrt weder Hersteller-,
Katalog-, IFC- noch IDA-ICE-Daten. V2-Migration, Dimensionierung,
Produktwahl, automatische Simulation und fachliche Wertevalidierung bleiben
getrennte Folgeslices.

## Umsetzungsstand 2026-07-27: SmallOffice-5Z-Technik

Eine getrennte Endvariante-02-Spezifikation beschreibt Heizung, Kuehlung und
Lueftung fuer alle fuenf Zonen. System- und Zonen-IDs sind ueber die gesamte
V1-Kette konsistent. Die technische Eigenvalidierung bleibt vor der
zonenseitigen Integritaetspruefung ausfuehrbar.

Die Referenzdimensionierung liefert die Ausgangskapazitaeten. Die sechs
gemeinsamen Faktoren 1,0 bis 0,5 werden erst in `ma_variants` auf verfuegbare
Heiz- und Kuehlleistung angewendet; `ma_technical` erzeugt keine Varianten.

## Konsolidierter V1-UI- und Katalogbezug 2026-07-27

UD-106 ordnet den aktiven Zonenstand vor der Technikbearbeitung ein. Die
Technikauswahl erfolgt in V1 als vollstaendiges Techniksystem-Paket aus einem
Excel-Katalog. Auswahl und Vorschau veraendern den Projektstand nicht; erst
`Techniksystem uebernehmen` speichert eine projektbezogene Config. Fehlt der
Excel-Katalog, zeigt die UI einen Quelle-fehlt-Status und erfindet keine
Produktdaten.

Der bekannte Streamlit-Fehler durch das beim lokalen Bau einer
`TechnicalSystemSpecification` fehlende Pflichtfeld `schema_version` ist im
ersten Produkt-Slice zu korrigieren.

## UD-106-Umsetzungsstand 2026-07-27

Der `schema_version`-Fehler ist korrigiert. Technik liest den aktiven
Zonenstand vor der Darstellung. Fehlt der vorgesehene Excel-Katalog unter
`data/catalogs/technical_systems/`, zeigt die UI einen blockierenden
Quelle-fehlt-Status und nur die vorhandene Config-Referenz; sie erzeugt keine
Produktdaten und aktiviert keine Uebernahme.

Ist eine Arbeitsmappe vorhanden, liest die UI ausschliesslich deren
`Uebersicht`, zeigt aktive, validierte und gesperrte Datensaetze und erlaubt
die projektbezogene Uebernahme nur fuer aktive validierte Eintraege.
Projektkopien enthalten Originalzeile, Pfad, Version und SHA-256. Die
Lite-Validierung akzeptiert ausschliesslich Schema-Version `1.0`.

## Konsolidierung nach UD-112 2026-07-31

`ma_technical` liefert im Ziel vor `ma_zones` die systemweiten technischen
Systeme und stabilen System-IDs. `ma_zones` ordnet diese anschliessend zonal
zu. Das ist kein Dimensionierungsowner: Kapazitaeten und deren Ergebnisse
liegen bei `ma_dimensionierung`. Die bisherige Abhaengigkeit der
Technikbearbeitung von einem aktiven Zonenmodell ist Altbestand und wird im
gemeinsamen P013/P014-Migrationsslice ohne zyklische Zielabhaengigkeit
aufgeloest.

## Umsetzungscheckpoint P013/P014-S1 2026-08-01

Der builder-erzeugte `ReleasedTechnicalHandover` fuehrt fuer die nachgelagerte
P013-Pruefung nun zusaetzlich Projekt-ID, Building-Referenz samt Revision,
einen deterministischen Serviceinterface-Referenzhash und einen gemeinsamen
`handover_content_hash`. Dieser bindet Technikmodell-/Revisions-/Content-Hash,
Projekt, Building und die Interfaceprojektion gemeinsam. Der produktive
Builder verlangt den vollstaendigen Kontext einer freigegebenen v2-Revision.

Das v2-Technikmodell und seine Serviceinterfaces bleiben zonenlos.
Zonenbelegung und optionale Terminalwahl liegen ausschliesslich in P013;
Kapazitaetspruefung und Dimensionierung werden durch diesen Checkpoint nicht
eingefuehrt. Direkte Legacy-v1-Konstruktoren und deren Diagnostik bleiben
kompatibel.

## Umsetzungscheckpoint direkte Technikansicht S2a 2026-08-01

Die direkte Streamlit-Fachansicht von `ma_technical` besitzt keine
Voraussetzung aus `ma_zones` mehr. Sie zeigt den fallbezogenen
Legacy-Uebergangsstand mit seinen direkten Zonenreferenzen weiterhin
additiv, kennzeichnet ihn aber ausdruecklich als Nicht-Zielmodell und nicht
als v2-Handover.

Daneben werden zentrale technische Objekt- und Serviceinterface-IDs aus der
bestehenden zonenfreien v2-Referenz sichtbar. Diese Quelle bleibt strikt
synthetisch, read-only, projektunabhaengig, nicht freigegeben und nicht fuer
Dimensionierung oder Simulation bestimmt. `validate_technical_model(...)`
wird als Strukturpruefung dargestellt; es wird weder eine Revision erzeugt
noch ein Projektstand gespeichert. Eine projektkompatible v2-Freigabe- und
Handover-Bedienung sowie die explizite zonale Assignment-Bedienung bleiben
getrennte Folgeslices. Fuer diesen Checkpoint entstand keine neue
Nutzerentscheidung; UD-112 und UD-114 bestimmen Richtung und Abgrenzung
bereits vollstaendig. Die Workflow-Ansicht bleibt gemaess Nutzerauftrag der
letzte UI-Migrationsslice.

## Umsetzungscheckpoint projektbezogene v2-Freigabekette 2026-08-01

UD-115 ist in der direkten Technikansicht umgesetzt. Ein uebernommener
`ma_building`-Stand ist die verbindliche Building-Referenz; Projekt-ID,
Building-ID und `model_version` muessen zum aktiven Workspace passen. Ein noch
nicht vorhandener Building-Content-Hash bleibt leer.

Der Nutzer waehlt eine versionierte Legacy-Quelle ausdruecklich aus.
`v2-Entwurf vorbereiten` erzeugt daraus ueber den versionierten Einwegadapter
nur einen deterministischen Sitzungsentwurf. Quelle, SHA-256, Mappingversion,
verworfene Zonenbindungen und nicht als Kapazitaet darstellbare Legacywerte
bleiben als Provenienz beziehungsweise Annahmen sichtbar. `Struktur pruefen`
validiert ohne Dateischreibzugriff. Warnungen koennen nur ueber die sichtbare
Freigabebestaetigung akzeptiert werden; Code und Fundstelle werden in der
Revision protokolliert, beim Reload erneut abgeglichen und in einem
Freigabenachweis-Hash gesichert.

Erst `Revision freigeben` erzeugt unter
`config/ma_technical/revisions/<building_id>/<technical_model_id>/` eine
atomare, kollisionsgeschuetzte und append-only YAML-Revision mit
systemgenerierter Modell- und Revisions-ID. Dateiname und gespeicherte
Revision-ID muessen uebereinstimmen. Die UI laedt die Datei danach erneut,
prueft Content- und Handover-Hash und speichert in `ma_technical.yaml` nur die
workspace-relative aktive Referenz je Building.

Ein aktiver Technikstand gilt nur fuer die vollstaendig gleiche Building-
Referenz samt `model_version`; ein Wechsel der Building-Version macht den
alten Stand sichtbar ungueltig. Die Workspace-Release-Grenze prueft die
Projekt-ID selbst gegen `project.yaml` und die Building-Referenz gegen den
tatsaechlichen `ma_building.yaml`-Stand. Ein veralteter Technikstand blockiert
nicht die Vorbereitung seiner neuen Revision. Scheitert nach erfolgreichem append-only Schreiben nur die
Aktivierung, benennt die UI die gespeicherte Revision und den getrennten
Aktivierungsfehler. Der aktuell einseitige Mappingstand einer Legacy-Zu-/
Abluftanlage auf `supply_air` wird als Einschraenkung dokumentiert und erzeugt
kein behauptetes `extract_air`-Interface.

Aktivierung und Reload lesen nur aus dem kanonischen UD-115-Revisionspfad;
externe oder falsch einsortierte workspace-interne Pfade werden vor dem
Dateizugriff abgewiesen. Die Revisionswurzel muss ein YAML-Mapping sein.
Warnungsbehaftete v2-Revisionen ohne gueltigen Freigabenachweis werden auch
bei einem vermeintlichen Legacy-Format nicht geladen.

Nicht Teil dieses Checkpoints sind Zonen- oder Terminalzuordnung,
Lastberechnung, Kapazitaetsausreichung, Dimensionierung, automatische
Nachbarmodulaenderungen, reale beziehungsweise geschuetzte Technikquellen und
die Workflow-Ansicht. Der naechste sichere P013/P014-Slice ist die explizite
Assignment-Bedienung in `ma_zones` gegen den aktiven Technik-Handover.

## Nachgelagerter P013-Assignment-Slice 2026-08-01

Die direkte `ma_zones`-Ansicht konsumiert nun den aktiven, projektlokalen
`ReleasedTechnicalHandover` ausschliesslich als hashgebundene Referenz. P014
bleibt Owner der zentralen Systeme und Serviceinterface-IDs; die Zonen- und
optionale Terminalzuordnung wird nur in P013 gespeichert. Ein fehlender,
veralteter oder zum Building unpassender Technikstand sperrt die Bedienung,
ohne P014 automatisch zu veraendern.

Damit ist der fuer diesen Slice erforderliche gerichtete UI-Durchstich
`ma_technical -> ma_zones` hergestellt. Nicht enthalten sind
Kapazitaetsausreichung, Lastberechnung, Dimensionierung, eine automatische
Vollversorgungsannahme oder die Workflowansicht. Die getrennte Klaerung der
v2-Werteherkunft bleibt als P014-Folgearbeit bestehen.
