# ma_technical

- **Zweck:** Zentrale technische Systeme, Kreise, Anlagen, Lueftung,
  Regelung und generische technische Datensaetze beschreiben.
- **Eingaben:** freigegebene Gebaeudedaten, zentrale Systemannahmen,
  Systemvorlagen und spaeter Produktdaten.
- **Ausgaben:** validierte Technikdaten fuer `ma_parameters` und zentrale
  Systemreferenzen fuer `ma_zones`.
- **Abgrenzung:** keine Variantenbildung, keine Simulationsergebnisanalyse
  und keine zonenbezogene Uebergabekonfiguration.
- **Abhaengigkeiten:** `ma_building`; Phase 2. P013-S2 ordnet
  `ma_technical` fachlich vor `ma_zones` ein.
- **Status:** teilweise umgesetzt. P014-S1 stellt eine LoD-1/Lite-Demo fuer das
  BusinessIntegration-Testgebaeude bereit; P014-S1.1 ergaenzt das v2-Aggregat
  um die zentralen technischen Register:
  `config/ma_technical/examples/business_integration_lod1_technical_spec.yaml`.
  P014-S2 speichert freigegebene v2-Revisionen hashgesichert; P014-S3a stellt
  daraus einen kleinen, referenzbasierten Handover fuer nachgelagerte Module
  bereit. P014-S4 fuegt einen strikten, typisierten V2-YAML-Einstieg und eine
  ausschliesslich synthetische Referenzdatei hinzu.
- **Uebergangsstand:** Die aktuelle LoD-1-Demo referenziert noch
  `source_zone_model_id` und `served_zone_ids`. Diese Kopplung bleibt
  kompatibel, muss im naechsten P014-Slice aber an P013-S2 angepasst werden.
- **LoD-1-Inhalt:** einfache Referenzannahmen fuer Heizung, Kuehlung und
  Lueftung mit bedienten Zonen, spezifischen Leistungen, Temperaturen,
  Leistungszahlen, Luftwechsel und Regelstrategie.
- **Validierung:** Pflichtfelder, eindeutige IDs, Systemtypen, bediente Zonen,
  positive Leistungs-/Luftwechselwerte und Zonenmodellbezug werden geprueft.
  Fehler blockieren; Warnungen benoetigen eine bewusste Freigabeentscheidung.
- **Streamlit:** Die Modulansicht trennt Heizung, Kuehlung, Lueftung,
  Speicher, Trinkwarmwasser und Elektrik in eigene Reiter. Jeder Reiter bietet
  explizit `Nicht vorhanden`; ein lokal vorhandener Heiz-, Kuehl- oder
  Speicherkatalog bleibt `demo_unverified` und wird nicht veroeffentlicht.
  Ohne lokale Katalogdaten bleibt die manuelle Statusauswahl nutzbar.
  Materialien und Konstruktionen gehoeren in die Gebaeudeansicht und
  veraendern keine Technikrevision.
- **Naechster Schritt:** Die V2-Werteherkunft und den verbleibenden
  P015-S3b-Umfang getrennt abgrenzen. Die v1-Demo bleibt bis zu einer
  getrennten, nachweisbaren Werteherkunft unveraendert.

## Schema v2

P014-S1 fuehrt parallel zur bestehenden LoD-1-Demo ein neues Zielmodell v2 ein.
Die alte Demo bleibt kompatibel; sie ist ein Legacy-v1-Vertrag mit direkten
Zonenreferenzen. Das v2-Modell beschreibt zentrale Technik ueber Plant,
physische Geraete, Heizung, Kuehlung, Verteilungen, Speicher/DHW, AHU,
Elektrik, Zeitplaene, Topologie und Serviceinterfaces.

Schutzgrenzen fuer den aktuellen Stand:

- kein IDA-ICE-Adapter oder Export,
- keine automatische Dimensionierung,
- keine Templates oder Fremdimporte,
- keine Variantenbildung in `ma_technical`,
- Kapazitaetsausreichung ist keine blockierende Eingabevalidierung.

Die ersten v2-Kerntypen liegen in separaten Dateien wie `enums.py`,
`metadata.py`, `plant.py`, `topology.py` und `specification.py`. Migration,
Revisionen, Repository, Parameterexport und UI-Editor folgen in spaeteren
Slices. P014-S1.1 buendelt physische Geraete, Heiz-/Kuehlverteilungen,
thermische Speicher und Trinkwarmwassererzeugung als Register; Plant, AHU und
Elektrik sind dabei optional. Die v2-Struktur- und Referenzvalidierung folgt
mit P014-S1.2.

## Strikter V2-YAML-Einstieg

P014-S4 stellt `load_technical_model_specification(path)` und
`technical_model_specification_from_dict(data)` bereit. Beide akzeptieren nur
Schema `2.0` und bekannte, vollständig typisierte V2-Strukturen; unbekannte,
leere oder falsch verschachtelte Eingaben werden vor der Fachvalidierung
abgewiesen. Die Referenzdatei
`config/ma_technical/examples/technical_v2_reference_spec.yaml` ist sichtbar
als `SYNTHETIC TEST/REFERENCE DATA` gekennzeichnet und kein Entwurfs-,
Simulations-, Katalog- oder Normdatensatz.

Bei einer Freigabe werden vorhandene `Path`-Werte ausschliesslich als
kanonische POSIX-Zeichenfolge in die Payload geschrieben. Versionierte
Beispiele verwenden deshalb nur relative synthetische Platzhalterpfade;
reale oder absolute Arbeits-, Netzwerk- und Nutzerpfade gehoeren nicht in
eine Technikrevision.

## Freigegebener Technik-Handover

P014-S3a ergaenzt `ReleasedTechnicalHandover` und
`ReleasedTechnicalServiceInterfaceReference`. Der Builder akzeptiert nur eine
freigegebene, hashkonsistente `TechnicalModelRevision` mit passender Modell-ID
in der Revisionsnutzlast. Der Handover fuehrt ausschliesslich Modell-ID,
Revisions-ID, Content-Hash, Freigabestatus sowie deterministisch sortierte
Serviceinterface- und Quellobjektreferenzen.

Der vollstaendige technische Payload verbleibt in `ma_technical`. Der Handover
ist weder ein Editor noch eine v1-zu-v2-Migration und erzeugt keine
Parameterwerte, Dateien, UI- oder Katalogaenderungen.
