# P014 ma_technical Technische Systeme

Stand: 2026-07-08
Status: Teilweise umgesetzt, P014-S1 BusinessIntegration-LoD-1/Lite; P013-S2-Anpassung offen
Prioritaet: Hoch
Abhaengigkeiten: P010, P012, P013

## Ziel

Zentrale technische Systeme, Kreise, Anlagen, Lueftung, Regelung und
generische technische Datensaetze fuer Referenz und Varianten strukturiert
erfassen.

## Reifegrad

Lite-Implementierung mit versionierter BusinessIntegration-Demo. P013-S2 legt
fachlich fest, dass `ma_technical` vor `ma_zones` bearbeitet wird und zentrale
Systeme bereitstellt, die `ma_zones` spaeter referenziert. Die aktuelle
LoD-1-Demo enthaelt noch Zonenreferenzen und bleibt ein bewusst dokumentierter
Uebergangsvertrag, bis P014 fachlich angepasst wird.

## Arbeitspakete

- Bestehende Systemtemplates aus `ma_variants` inventarisieren.
- Neutrale Referenzsysteme fuer Heizung, Kuehlung und Lueftung planen.
- Zentrale Systeme, Kreise und generische technische Datensaetze von
  zonenbezogenen Uebergabesystemen trennen.
- Aktuelle Felder `source_zone_model_id` und `served_zone_ids` als
  Uebergangsbestand der LoD-1-Demo bewerten.
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
- P013-S2-Zielstruktur mit zentraler Technik vor `ma_zones`

## Akzeptanzkriterien

- Ein Demo-System liefert validierte Technikdaten an `ma_parameters`.
- Bestehende Vorlagen werden wiederverwendet, nicht dupliziert.
- Unvollstaendige Systeme erzeugen nachvollziehbare Warnungen oder Fehler.
- Der naechste P014-Slice trennt zentrale Systemdaten von zonenbezogener
  Uebergabekonfiguration, ohne die bestehende LoD-1-Demo ungeplant zu brechen.

## Naechster Schritt

P014 an P013-S2 anpassen: zentrale Technik vor `ma_zones` modellieren,
aktuelle Zonenreferenzen als Uebergangsvertrag pruefen und Referenzsysteme
fuer LoD-2 sowie spaetere Dimensionierung genauer abgrenzen.
