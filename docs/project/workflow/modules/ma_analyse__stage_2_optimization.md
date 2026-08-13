# Analyse Stufe 2 - Optimierung

Modul-ID: `ma_analyse.stage_2_optimization`  
Prozessbereich: **PostProcess**  
Status: **teilweise umgesetzt**

## Rolle im Ablauf

Varianten mit vorhandenen Energie-, Leistungs-, Komfort- und Zeitreihenanalysen vergleichen.

Der Steckbrief macht nur den dokumentierten Fachumfang sichtbar. Nicht vorhandene Fachwerte, Regeln oder Bedienfunktionen werden nicht ergänzt.

## Fachliche Eingänge

- standardisierte Simulationsergebnisse
- Varianten- und Raumwahl

## Ausgänge und Übergaben

- Variantenvergleiche
- Optimierungshinweise
- Diagramme und Tabellen

## Bedien- und Ablaufhinweis

Das Modul wird nur genutzt, wenn die genannten Eingänge im jeweiligen Projektkontext vorliegen. Sein Ergebnis wird als benannte Übergabe an die abhängigen Module weitergegeben; Navigation allein löst keine Fachaktion, Auswahl oder Persistenz aus.

## Abgrenzung

- kein Norm-Nachweis
- keine Sensitivitaetsbewertung

## Abhängigkeiten

- ma_data_preparation

## Nächster dokumentierter Schritt

P019: vorhandene Analysebefehle nach der Datenvorbereitung zu einem dokumentierten Optimierungsablauf buendeln.

## Quellen und weiterführende Verweise

- `docs/project/workflow/README.md`
- `src/ma_workflow/catalog.py`

> Fachliche Quellen, Normwerte und externe Originaldaten werden nur nach den jeweils dokumentierten Rechte- und Fachgates ergänzt.
