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

Ein UI-neutrales Feasibility-Framework bewertet explizit konfigurierte Ziele
und Nebenbedingungen als `PASS`, `FAIL` oder `NOT_EVALUABLE`; es waehlt keine
Variante automatisch aus. Der historische ALT-Bestand kann je Variante und
Zone deskriptiv gegen `Dimensionierung` verglichen und als XLSX/CSV exportiert
werden. `analyze-data`
liefert einen gemeinsamen UI-/Excel-Tabellenvertrag mit Dateninventar,
Berechnungsgrenzen, absoluter und spezifischer Leistung sowie sichtbaren
`nicht auswertbar`-Gruenden. Einheitenoffene Aggregationskennwerte bleiben
sichtbar, solange der Import
keinen maschinenlesbaren Quelleneinheitenvertrag liefert. Algebraisches
Minimum/Maximum der Kuehlreihe und ihr maximaler Betrag sind getrennt benannt;
es erfolgt keine stille Vorzeichenumkehr. Eine automatische
Optimierungsentscheidung fehlt weiterhin bewusst.

## Naechster Schritt

Projektbezogene Ziele und Grenzwerte erst nach fachlicher Entscheidung als
explizites Feasibility-Profil hinterlegen.
