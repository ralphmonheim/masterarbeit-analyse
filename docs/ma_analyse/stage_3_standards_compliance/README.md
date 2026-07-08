# ma_analyse.stage_3_standards_compliance

## Zweck

Varianten durch nachvollziehbare Berechnungen und Grenzwertpruefungen gegen
deutsche Normen nachweisen und spaeter internationale Normenprofile ergaenzen.

## Eingaben

- standardisierte Analysekennwerte
- versioniertes Normenprofil
- Projekt-, Nutzungs- und Systemrandbedingungen
- lokale Normenextrakte und Reviewlisten unter `data/common/normen/`

## Ausgaben

- `ComplianceReport`
- Ergebnis `pass`, `fail`, `warning` oder `not_evaluable` je Nachweis

## Abgrenzung

- keine allgemeine Modellvalidierung
- keine ungepruefte Uebernahme bestehender Komfortzonen oder Grenzwerte
- keine direkte Ausfuehrung automatisch extrahierter Formelkandidaten

## Abhaengigkeiten

- `ma_analyse.stage_2_optimization`
- belastbare Normquellen mit Ausgabe, Abschnitt und Anwendungsbereich

## Status

Geplant. Der fruehere Arbeitsname `stage_3_verification` ist durch
`stage_3_standards_compliance` ersetzt. Lokale Normen- und
Kalenderarbeitsdaten liegen unter `data/common/normen/` als Pruefbestand fuer
P020. Sie sind noch keine produktiven Regeln.

## Naechster Schritt

P020 mit einer Quellen- und Methodenmatrix fuer deutsche Normen beginnen und
die lokalen Extraktionsdaten nur nach fachlicher Pruefung uebernehmen.
