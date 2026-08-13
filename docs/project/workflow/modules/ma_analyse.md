# Analyse-Grundlagen

Modul-ID: `ma_analyse`  
Prozessbereich: **Querschnitt**  
Status: **teilweise umgesetzt**

## Rolle im Ablauf

Gemeinsame Services, Datenzugriffe, Diagramme und Exporte fuer die Analysestufen bereitstellen.

Der Steckbrief macht nur den dokumentierten Fachumfang sichtbar. Nicht vorhandene Fachwerte, Regeln oder Bedienfunktionen werden nicht ergänzt.

## Fachliche Eingänge

- standardisierte Simulationsergebnisse
- Projekt- und Variantenmetadaten

## Ausgänge und Übergaben

- Kennwerte
- Diagramme
- Tabellen
- Analyseberichte

## Bedien- und Ablaufhinweis

Das Modul wird nur genutzt, wenn die genannten Eingänge im jeweiligen Projektkontext vorliegen. Sein Ergebnis wird als benannte Übergabe an die abhängigen Module weitergegeben; Navigation allein löst keine Fachaktion, Auswahl oder Persistenz aus.

## Abgrenzung

- keine Kosten- oder Nachhaltigkeitsrechnung

## Abhängigkeiten

- ma_import_simulation

## Nächster dokumentierter Schritt

Gemeinsame Analysefunktionen stabil halten und ueber die Stufenplaene weiterentwickeln.

## Quellen und weiterführende Verweise

- `docs/project/workflow/README.md`
- `src/ma_workflow/catalog.py`

> Fachliche Quellen, Normwerte und externe Originaldaten werden nur nach den jeweils dokumentierten Rechte- und Fachgates ergänzt.
