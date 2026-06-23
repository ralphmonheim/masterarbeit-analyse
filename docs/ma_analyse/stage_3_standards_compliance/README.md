# ma_analyse.stage_3_standards_compliance

## Zweck

Varianten durch nachvollziehbare Berechnungen und Grenzwertpruefungen gegen
deutsche Normen nachweisen und spaeter internationale Normenprofile ergaenzen.

## Eingaben

- standardisierte Analysekennwerte
- versioniertes Normenprofil
- Projekt-, Nutzungs- und Systemrandbedingungen

## Ausgaben

- `ComplianceReport`
- Ergebnis `pass`, `fail`, `warning` oder `not_evaluable` je Nachweis

## Abgrenzung

- keine allgemeine Modellvalidierung
- keine ungepruefte Uebernahme bestehender Komfortzonen oder Grenzwerte

## Abhaengigkeiten

- `ma_analyse.stage_2_optimization`
- belastbare Normquellen mit Ausgabe, Abschnitt und Anwendungsbereich

## Status

Geplant. Der fruehere Arbeitsname `stage_3_verification` ist durch
`stage_3_standards_compliance` ersetzt.

## Naechster Schritt

P020 mit einer Quellen- und Methodenmatrix fuer deutsche Normen beginnen.
