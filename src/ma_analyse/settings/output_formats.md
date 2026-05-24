# Zentrale Ausgabeformate

Dieses Dokument steuert die Standardgroessen fuer erzeugte Diagramme, PDFs und Excel-Ausgaben.

Regeln:
- Aendere in der Tabelle `Ausgabe-Regeln` die Spalte `Format`.
- Erlaubte Werte stehen unten im `Formatkatalog`.
- Diagrammgroessen werden in Zentimetern angegeben und intern fuer Matplotlib umgerechnet.
- `Keine Größe` wird fuer Ausgaben ohne feste Bild- oder Seitengroesse verwendet.

## Ausgabe-Regeln

| ID | Befehl | Unterbefehl | Ausgabe | Format |
| --- | --- | --- | --- | --- |
| comfort.plot.png | comfort | plot | Einzelraum-Komfortdiagramm | 16x9 cm |
| comfort.plot_analysis.png | comfort | plot_analysis | Einzelraum-Analyse-Diagramm | 16x9 cm |
| comfort.plot_overview.pdf | comfort | plot_overview | Comfort-Uebersicht PDF | A4 Quer |
| comfort.plot_analysis_overview.pdf | comfort | plot_analysis_overview | Analyse-Uebersicht PDF | A4 Quer |
| heating.bar.png | heating | bar | Heating Balkendiagramm | 16x9 cm |
| heating.timeline.single.png | heating | timeline | Heating Zeitdiagramm single | 24x13.5 cm |
| heating.timeline.compare.png | heating | timeline | Heating Zeitdiagramm compare | 24x13.5 cm |
| cooling.bar.png | cooling | bar | Cooling Balkendiagramm | 16x9 cm |
| cooling.timeline.single.png | cooling | timeline | Cooling Zeitdiagramm single | 16x9 cm |
| cooling.timeline.compare.png | cooling | timeline | Cooling Zeitdiagramm compare | 24x13.5 cm |
| analyze_data.excel | analyze_data | - | Excel-Auswertung | Keine Größe |

## Formatkatalog

| Format | Breite cm | Hoehe cm | Verwendung |
| --- | ---: | ---: | --- |
| 16x9 cm | 16 | 9 | Standard fuer Einzel-Diagramme |
| 24x13.5 cm | 24 | 13.5 | Mehr Platz fuer Vergleichsdiagramme |
| A4 Hoch | 21 | 29.7 | PDF-Seite im Hochformat |
| A4 Quer | 29.7 | 21 | PDF-Seite im Querformat |
| Keine Größe |  |  | Fuer Ausgaben ohne feste Bildgroesse |


