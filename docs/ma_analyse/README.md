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
- Stage 1 bleibt bis zu einem eigenen Fachplan nur strukturell vorbereitet

## Abhaengigkeiten

- `ma_import_simulation` als langfristige Ergebnisdatenquelle
- bestehende lokale Analyse-Datenpfade

## Status

Aktiv fuer Analyse Stufe 2 bis 4. Die Referenzdimensionierung in
`ma_analyse.stage_1_dimensioning` ist geplant.

## Naechster Schritt

Bestehende Service-Fassade stabilisieren und Stage 1 separat fachlich planen.

## Dateien

- `architecture.md`: Architektur und Datenfluss der Analysepipeline.
- `commands_analyse.md`: aktive Befehlsreferenz fuer CLI, GUI, Tests und Plot-Templates.
- `plot_template_examples.md`: Referenzgalerie der Plot-Template-Beispiele.
- `stage_1_dimensioning/README.md`: geplanter, noch nicht fachlich
  implementierter Bereich fuer die Referenzdimensionierung.

Die verbindlichen Arbeitsordner sind `data/ma_analyse/ida_imports`, `data/ma_analyse/database` und `data/ma_analyse/output`. Die frueheren Root-Datenpfade werden nicht mehr unterstuetzt.
