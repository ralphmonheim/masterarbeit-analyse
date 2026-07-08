# P017 ma_variants und Naming-Anbindung

Stand: 2026-07-08
Status: Geplant
Prioritaet: Hoch
Abhaengigkeiten: P015-S1, P016

## Ziel

Den bestehenden Variantenkern kontrolliert auf freigegebene
`ParameterSnapshot`-Eingaben umstellen und das von `ma_project` bereitgestellte
neutrale Benennungsprofil reproduzierbar anwenden.

## Reifegrad

Weiterentwicklung des vorhandenen produktiven Kerns.

## Arbeitspakete

- Bestehende Parameter-, Options-, Naming- und Variantenimporte als
  Uebergangsbestand abbilden.
- Snapshot-Version in Variantenmetadaten speichern.
- Benennungsprofil und Regelstand aus `ma_project` referenzieren.
- Neutrale Variantennamen erzeugen und auf Eindeutigkeit pruefen.
- In der Variantenansicht auf die verantwortlichen Projekt- und
  Parameteransichten verweisen.
- Bestehende Auswahl- und Exportfunktionen kompatibel halten.

## Akzeptanzkriterien

- Jede Variante ist einem Parametersnapshot und Naming-Regelstand zugeordnet.
- Gleiche Eingaben erzeugen reproduzierbare Varianten und Namen.
- Historische Konfigurationen bleiben lesbar.
- Produkt-, Material- und programmspezifische Exportbezeichnungen werden nicht
  in `ma_variants` verwaltet.

## Umsetzungsbezug P028

Der Demo-Variantenraum konsumiert bereits die aktuelle Optionsauswahl aus
`ma_parameters` und das neutrale Benennungsprofil aus `ma_project`.
Fehlende Tokens und doppelte Namen blockieren die Anwendung. Die dauerhafte
Zuordnung zu versionierten `ParameterSnapshot`- und Naming-Regelstaenden
bleibt Aufgabe von P017.

## Umsetzungsbezug P015-S1

P015-S1 stellt einen validierten `ParameterSnapshot` v1 mit Snapshot-ID,
Version, Quellenreferenzen, Einheiten und Freigabestatus bereit. P017 soll
den bestehenden Variantenkern schrittweise so anbinden, dass Varianten ihre
fachlichen Eingaben aus einem freigegebenen Snapshot referenzieren, ohne die
bisherigen Kataloge und Exportfunktionen abrupt zu brechen.

## Umsetzungsbezug P016-S1

P016-S1 liefert ein LoD-1-`ReferenceDimensioningResult` mit Heizlast,
Lueftungs-Heizlast, interner Kuehllastannahme, Luftvolumenstrom, Rechenweg
und Hinweisen. P017 darf diese Ergebnisse spaeter nicht direkt als stille
Variantenparameter verwenden; sie muessen ueber einen freigegebenen
Folgesnapshot oder einen dokumentierten Stage-1-Vorschlag angebunden werden.
