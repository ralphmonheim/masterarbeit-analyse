# ma_analyse.stage_2_optimization

## Zweck

Varianten mit vorhandenen Energie-, Leistungs-, Komfort- und
Zeitreihenanalysen vergleichen und Optimierungspotenziale sichtbar machen.

## Eingaben

- standardisierte Simulationsergebnisse
- Varianten-, Raum- und Analyseauswahl

## Ausgaben

- Variantenvergleiche, Diagramme, Tabellen und Optimierungshinweise

## Abgrenzung

- kein Norm-Nachweis
- keine Sensitivitaetsbewertung

## Abhaengigkeiten

- `ma_analyse`
- `ma_import_simulation`

## Status

Teilweise vorhanden. Die benoetigten Befehle existieren. `analyze-data`
liefert einen gemeinsamen UI-/Excel-Tabellenvertrag mit Dateninventar,
Berechnungsgrenzen, absoluter und spezifischer Leistung sowie sichtbaren
`nicht auswertbar`-Gruenden. Einheitenoffene Aggregationskennwerte bleiben
sichtbar, solange der Import
keinen maschinenlesbaren Quelleneinheitenvertrag liefert. Algebraisches
Minimum/Maximum der Kuehlreihe und ihr maximaler Betrag sind getrennt benannt;
es erfolgt keine stille Vorzeichenumkehr. Eine automatische
Optimierungsentscheidung fehlt weiterhin bewusst.

## Naechster Schritt

Den neutralen Import- und Kennwertvertrag weiter an Varianten-, Raum- und
Run-Referenzen binden.
