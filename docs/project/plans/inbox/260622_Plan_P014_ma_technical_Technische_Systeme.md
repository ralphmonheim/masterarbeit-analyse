# P014 ma_technical Technische Systeme

Stand: 2026-07-13
Status: Fachlich konsolidiert, P014-S1 Legacy-v1 kompatibel, P014-S2 Slice 0/1 gestartet
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

## Zielmodell v2

P014-S2 fuehrt ein paralleles Schema v2 ein. Es ersetzt v1 nicht sofort,
sondern beschreibt die kuenftige Fachstruktur:

```text
TechnicalModelSpecification
├── building_reference
├── plant
├── air_handling_unit
├── electrical_system
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

## Naechste Slices

1. Serialisierung und lokale Speicherung mit Working Drafts, Revisionen,
   Branches und Content-Hash.
2. Strukturvalidierung, technische Limits und Empfehlungen ohne
   Kapazitaetsausreichungsblockade.
3. Gefuehrte Topologie und Serviceinterfaces.
4. Parametersicht fuer `ma_parameters`.
5. Manuelle Streamlit-Bearbeitung.
6. Kontrollierte Migration v1 -> v2.

## Abnahmekriterien fuer Slice 1

- v2-Kerntypen sind immutable und importierbar.
- `TechnicalModelSpecification` v2 kann ein minimales Modell beschreiben.
- `CapacityMode.ideal_unlimited` benoetigt keine Leistungszahl.
- Serviceinterfaces enthalten keine direkten `served_zone_ids`.
- v1-Demo-Loader und vorhandene P015/UI-Vertraege bleiben gruen.
