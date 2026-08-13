# Zentrale Validierung

Modul-ID: `ma_validation`  
Prozessbereich: **Querschnitt**  
Status: **geplant**

## Rolle im Ablauf

Lokale Pruefergebnisse sammeln und moduluebergreifende Freigaben verwalten.

Der Steckbrief macht nur den dokumentierten Fachumfang sichtbar. Nicht vorhandene Fachwerte, Regeln oder Bedienfunktionen werden nicht ergänzt.

## Fachliche Eingänge

- lokale Validierungsberichte
- Workflow-Zustand

## Ausgänge und Übergaben

- Freigabestatus
- blockierende Fehler
- Warnungen

## Bedien- und Ablaufhinweis

Das Modul wird nur genutzt, wenn die genannten Eingänge im jeweiligen Projektkontext vorliegen. Sein Ergebnis wird als benannte Übergabe an die abhängigen Module weitergegeben; Navigation allein löst keine Fachaktion, Auswahl oder Persistenz aus.

## Abgrenzung

- Fachregeln bleiben in den Fachmodulen

## Abhängigkeiten

- ma_workflow

## Nächster dokumentierter Schritt

P027-Checkpoints fuer VSP, VVER, VCAT, VSEL und VGEN an Freigabeentscheidungen anbinden.

## Quellen und weiterführende Verweise

- `docs/project/workflow/README.md`
- `src/ma_workflow/catalog.py`

> Fachliche Quellen, Normwerte und externe Originaldaten werden nur nach den jeweils dokumentierten Rechte- und Fachgates ergänzt.
