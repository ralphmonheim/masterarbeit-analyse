# P014 ma_technical Technische Systeme

Stand: 2026-07-08
Status: Teilweise umgesetzt, P014-S1 BusinessIntegration-LoD-1/Lite
Prioritaet: Hoch
Abhaengigkeiten: P010, P013

## Ziel

Erzeugung, Verteilung, Uebergabe, Lueftung, Regelung und relevante
Anlagenparameter fuer Referenz und Varianten strukturiert erfassen.

## Reifegrad

Lite-Implementierung mit versionierter BusinessIntegration-Demo. Importierbare
Systemvorlagen und Produktdaten bleiben Folgeausbau.

## Arbeitspakete

- Bestehende Systemtemplates aus `ma_variants` inventarisieren.
- Neutrale Referenzsysteme fuer Heizung, Kuehlung und Lueftung planen.
- Importvorlagen und manuelle UI-Anpassung kombinieren.
- Leistungswerte, Temperaturen, Wirkungsgrade, Luftmengen und Regelarten
  einheitenklar validieren.
- Abgrenzung zu Stage 1 und Variantenbildung sichern.

## Umsetzungsstand P014-S1

- Paketstruktur `src/ma_technical/` enthaelt Fachmodelle, Standardpfade,
  YAML-Loader und Validierung.
- Versionierte BusinessIntegration-LoD-1/Lite-Demo:
  `config/ma_technical/examples/business_integration_lod1_technical_spec.yaml`.
- Die Demo beschreibt einfache Referenzannahmen fuer Heizung, Kuehlung und
  Lueftung bezogen auf die validierte LoD-1-Zone.
- Validiert werden Pflichtfelder, eindeutige IDs, Systemtypen, bediente Zonen,
  positive Leistungs-/Luftwechselwerte, Waermerueckgewinnung und
  Zonenmodellbezug.
- Streamlit zeigt eine echte Pruefansicht mit Freigabestatus, Systemen und
  Annahmen.

## Nicht umgesetzt in P014-S1

- automatische Anlagenauslegung
- Produktdatenbank oder Herstellerdaten
- Variantenbildung
- IDA-ICE-spezifische Systemtemplates
- Kopplung an Stage-1-Dimensionierung

## Akzeptanzkriterien

- Ein Demo-System liefert validierte Technikdaten an `ma_parameters`.
- Bestehende Vorlagen werden wiederverwendet, nicht dupliziert.
- Unvollstaendige Systeme erzeugen nachvollziehbare Warnungen oder Fehler.

## Naechster Schritt

Referenzsysteme fuer LoD-2 und spaetere Dimensionierung genauer abgrenzen.
