# P013 ma_zones Zonen und Nutzungen

Stand: 2026-07-08
Status: Teilweise umgesetzt, P013-S1 BusinessIntegration-LoD-1
Prioritaet: Mittel
Abhaengigkeiten: P010, P012

## Ziel

Raeume, thermische Zonen, Nutzungen, Sollwerte, interne Lasten und Profile
konzeptuell vollstaendig und mit einer Demo nutzbar beschreiben.

## Reifegrad

Konzept plus umgesetzte LoD-1-Demo fuer die BusinessIntegration-Kette.
Optionale Lite-Zuordnung aus Gebaeudeimporten bleibt Folgeausbau.

## Arbeitspakete

- Raum-zu-Zone-Zuordnung und Nutzungsprofile definieren.
- Bauliches Raumregister und `ImportedZoneHint` aus P012 als Eingangsgrenze
  vorsehen; `ma_zones` bestaetigt daraus erst thermische Zonen.
- Sollwerte, Belegung, Beleuchtung, Geraete und Betriebszeiten abbilden.
- Importierbare YAML-/Tabellenvorlagen plus manuelle UI-Anpassung planen.
- Herkunft und Gueltigkeit jeder Eingabe dokumentieren.
- Automatische IFC-Zuordnung nur fuer nachweisbar vorhandene Felder vorsehen.

## Umsetzungsbezug P012

`ma_building` verwaltet geometrische Raeume und speichert importierte
Zonierungsinformationen nur als Vorschlag. `ma_zones` uebernimmt erst
freigegebene Raumreferenzen, prueft Raum-zu-Zone-Zuordnungen fachlich und
verwaltet Nutzung, Profile, Sollwerte, interne Lasten und Betriebszeiten.

## Umsetzungsstand P013-S1

- Paketstruktur `src/ma_zones/` enthaelt Fachmodelle, Standardpfade,
  YAML-Loader und Validierung.
- Versionierte BusinessIntegration-LoD-1-Demo:
  `config/ma_zones/examples/business_integration_lod1_zone_spec.yaml`.
- LoD-1 beschreibt das Rhino-Testgebaeude als eine Gesamtgebaeudezone mit
  einfachem Buero-Nutzungsprofil, Sollwerten, internen Lasten,
  Betriebszeiten und Mindestluftwechsel.
- Die Validierung prueft Pflichtfelder, eindeutige IDs, Profilreferenzen,
  Flaeche/Volumen, Sollwerte, Betriebszeiten und Bezug zur freigegebenen
  `BuildingModelSpecification`.
- Streamlit zeigt eine echte Pruefansicht mit Freigabestatus, Zonen,
  Nutzungsprofilen und Annahmen.

## Nicht umgesetzt in P013-S1

- automatische Raum-Zonen-Zuordnung
- detaillierte Nutzungsprofilbibliothek
- importierte `ImportedZoneHint`-Bestaetigung
- LoD-2/LoD-3 mit mehreren Raeumen oder orientierten Teilzonen

## Akzeptanzkriterien

- Demo-Zonen liefern validierte Daten an `ma_parameters` und Anforderungen an
  `ma_technical`.
- Profile und Sollwerte sind einheitenklar und versionierbar.
- Fehlende Raum-Zonen-Zuordnungen werden blockierend gemeldet.
- Importierte Zonierungsvorschlaege bleiben von bestaetigten thermischen Zonen
  unterscheidbar.

## Naechster Schritt

LoD-2-Raum-Zonen-Zuordnung und belastbare Nutzungsprofilbibliothek planen.
