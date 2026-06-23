# P014 ma_technical Technische Systeme

Stand: 2026-06-22
Status: Geplant
Prioritaet: Hoch
Abhaengigkeiten: P010, P013

## Ziel

Erzeugung, Verteilung, Uebergabe, Lueftung, Regelung und relevante
Anlagenparameter fuer Referenz und Varianten strukturiert erfassen.

## Reifegrad

Lite-Implementierung mit importierbaren Systemvorlagen und Demo.

## Arbeitspakete

- Bestehende Systemtemplates aus `ma_variants` inventarisieren.
- Neutrale Referenzsysteme fuer Heizung, Kuehlung und Lueftung planen.
- Importvorlagen und manuelle UI-Anpassung kombinieren.
- Leistungswerte, Temperaturen, Wirkungsgrade, Luftmengen und Regelarten
  einheitenklar validieren.
- Abgrenzung zu Stage 1 und Variantenbildung sichern.

## Akzeptanzkriterien

- Ein Demo-System liefert validierte Technikdaten an `ma_parameters`.
- Bestehende Vorlagen werden wiederverwendet, nicht dupliziert.
- Unvollstaendige Systeme erzeugen nachvollziehbare Warnungen oder Fehler.
