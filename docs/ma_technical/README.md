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
  BusinessIntegration-Testgebaeude bereit:
  `config/ma_technical/examples/business_integration_lod1_technical_spec.yaml`.
- **Uebergangsstand:** Die aktuelle LoD-1-Demo referenziert noch
  `source_zone_model_id` und `served_zone_ids`. Diese Kopplung bleibt
  kompatibel, muss im naechsten P014-Slice aber an P013-S2 angepasst werden.
- **LoD-1-Inhalt:** einfache Referenzannahmen fuer Heizung, Kuehlung und
  Lueftung mit bedienten Zonen, spezifischen Leistungen, Temperaturen,
  Leistungszahlen, Luftwechsel und Regelstrategie.
- **Validierung:** Pflichtfelder, eindeutige IDs, Systemtypen, bediente Zonen,
  positive Leistungs-/Luftwechselwerte und Zonenmodellbezug werden geprueft.
  Fehler blockieren; Warnungen benoetigen eine bewusste Freigabeentscheidung.
- **Streamlit:** Die Modulansicht zeigt Demo-Systeme, Freigabestatus und
  Annahmen.
- **Naechster Schritt:** Zentrale Technik vor `ma_zones` modellieren und
  Referenzsysteme, technische Limits, empfohlene Bereiche und Kurzkennungen
  fuer LoD-2, spaetere Dimensionierung und P017-Regelpruefungen genauer
  abgrenzen.

## Schema v2

P014-S2 fuehrt parallel zur bestehenden LoD-1-Demo ein neues Zielmodell v2 ein.
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
Slices.
