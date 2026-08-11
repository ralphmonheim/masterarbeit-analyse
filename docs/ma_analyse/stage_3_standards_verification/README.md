# ma_analyse.stage_3_standards_verification

## Zweck

Analyse Stufe 3 bereitet die spaetere Bewertung von Gebaeude- und Technikdaten
gegen fachlich freigegebene Kriterien vor. Der aktuelle Stand ist eine
Readiness-Pruefung, kein fachlicher Nachweis und keine Rechtefreigabe.

## Eingaben

Gebaeude-, Zonen- und Technikdaten sowie fachlich vorbereitete Normvorlagen.

## Ausgaben

Aktuell: Readiness-Tabelle mit Daten-, Methoden-, Rechte- und Teststatus.
Spaeter: Nachweisberichte mit bewerteten Regeln, Annahmen und offenen Punkten.

## Abgrenzung

Keine Rechtefreigabe, keine automatische Normtextextraktion und derzeit keine
fachliche PASS-/FAIL-Bewertung.

## Abhaengigkeiten

`ma_analyse.stage_2_optimization`, `ma_zones` und `ma_technical`.

## Status

Vorbereitet. Eine UI-neutrale Readiness-Matrix fuehrt derzeit zwei belegte
Kandidaten: den wertfreien DIN/TS-18599-10-Profilvertrag und das vorhandene
Legacy-Datenfeld fuer Uebertemperatur-Gradstunden. Beide bleiben
`NOT_EVALUABLE`: Es werden weder geschuetzte Norminhalte gelesen noch
Grenzwerte, Formeln oder PASS-/FAIL-Regeln erzeugt. `ma_validation` darf
Daten- und Vertragsdiagnosen sammeln; die spaetere Fachberechnung bleibt in
dieser Stage.

## Naechster Schritt

Ein erstes fachliches Nachweisprofil erst nach bestaetigtem Dokument,
Ausgabe, Fundstelle, Verarbeitungsrecht, Einheit, Geltungsbereich und
reproduzierbarem Fachtest aktivieren.
