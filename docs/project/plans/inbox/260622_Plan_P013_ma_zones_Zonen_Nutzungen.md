# P013 ma_zones Zonen und Nutzungen

Stand: 2026-06-22
Status: Geplant
Prioritaet: Mittel
Abhaengigkeiten: P010, P012

## Ziel

Raeume, thermische Zonen, Nutzungen, Sollwerte, interne Lasten und Profile
konzeptuell vollstaendig und mit einer Demo nutzbar beschreiben.

## Reifegrad

Konzept plus Demo; optionale Lite-Zuordnung aus Gebaeudeimporten.

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

## Akzeptanzkriterien

- Demo-Zonen liefern validierte Daten an `ma_parameters` und Anforderungen an
  `ma_technical`.
- Profile und Sollwerte sind einheitenklar und versionierbar.
- Fehlende Raum-Zonen-Zuordnungen werden blockierend gemeldet.
- Importierte Zonierungsvorschlaege bleiben von bestaetigten thermischen Zonen
  unterscheidbar.
