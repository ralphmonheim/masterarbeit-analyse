# ma_analyse

Dieser Bereich dokumentiert die bestehende Analysepipeline fuer IDA-ICE-Simulationsergebnisse.

## Zweck

Standardisierte Simulationsergebnisse technisch auswerten und als Kennwerte,
Tabellen, Diagramme und Analyseberichte bereitstellen.

## Eingaben

- standardisierte Simulationsergebnisse
- Projekt-, Varianten-, Raum- und Analysekonfiguration

## Ausgaben

- Kennwerte, Tabellen, Diagramme, Excel-Dateien und Analyseberichte

## Abgrenzung

- keine Kosten-, Nachhaltigkeits- oder Gesamtbewertung
- Stage 1 bleibt bis P016 nur strukturell vorbereitet
- Stage 3 implementiert keine ungeprueften Normregeln

## Abhaengigkeiten

- `ma_import_simulation` als langfristige Ergebnisdatenquelle
- bestehende lokale Analyse-Datenpfade

## Status

Die gemeinsamen Analysefunktionen und Stage 2 sind teilweise vorhanden.
Stage 1, Stage 3 und Stage 4 sind geplant.

## Naechster Schritt

P016 sowie P019 bis P021 getrennt umsetzen und gemeinsame Services
wiederverwenden.

## Dateien

- `architecture.md`: Architektur und Datenfluss der Analysepipeline.
- `commands_analyse.md`: aktive Befehlsreferenz fuer CLI, GUI, Tests und Plot-Templates.
- `plot_template_examples.md`: Referenzgalerie der Plot-Template-Beispiele.
- `stage_1_dimensioning/README.md`: geplanter, noch nicht fachlich
  implementierter Bereich fuer die Referenzdimensionierung.
- `stage_2_optimization/README.md`: vorhandene Analysebefehle als spaeterer
  Optimierungsablauf.
- `stage_3_standards_compliance/README.md`: geplanter Norm-Nachweis mit
  deutschen und spaeter internationalen Normenprofilen.
- `stage_4_sensitivity/README.md`: geplante ereignisbasierte
  Sensitivitaets- und Robustheitsanalyse.

Die verbindlichen Arbeitsordner sind `data/ma_analyse/ida_imports`, `data/ma_analyse/database` und `data/ma_analyse/output`. Die frueheren Root-Datenpfade werden nicht mehr unterstuetzt.
