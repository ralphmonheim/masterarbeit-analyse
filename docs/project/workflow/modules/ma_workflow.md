# Workflow-Steuerung

Modul-ID: `ma_workflow`  
Prozessbereich: **Querschnitt**  
Status: **geplant**

## Rolle im Ablauf

Phasen, Module, Status und spaetere Serviceaufrufe zentral orchestrieren.

Der Steckbrief macht nur den dokumentierten Fachumfang sichtbar. Nicht vorhandene Fachwerte, Regeln oder Bedienfunktionen werden nicht ergänzt.

## Fachliche Eingänge

- Projektzustand
- Benutzeraktionen

## Ausgänge und Übergaben

- Workflow-Status
- koordinierte Serviceaufrufe

## Bedien- und Ablaufhinweis

Das Modul wird nur genutzt, wenn die genannten Eingänge im jeweiligen Projektkontext vorliegen. Sein Ergebnis wird als benannte Übergabe an die abhängigen Module weitergegeben; Navigation allein löst keine Fachaktion, Auswahl oder Persistenz aus.

## Abgrenzung

- keine Fachberechnung
- keine Darstellung

## Abhängigkeiten

- ma_core

## Nächster dokumentierter Schritt

P027-Checkpoints, Reloads und Abbrueche fuer P017 schrittweise an echte Fachservices anbinden.

## Quellen und weiterführende Verweise

- `docs/project/workflow/README.md`
- `src/ma_workflow/catalog.py`

> Fachliche Quellen, Normwerte und externe Originaldaten werden nur nach den jeweils dokumentierten Rechte- und Fachgates ergänzt.
