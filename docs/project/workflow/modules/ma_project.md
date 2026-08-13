# Projektinitialisierung

Modul-ID: `ma_project`  
Prozessbereich: **PreProcess**  
Status: **geplant**

## Rolle im Ablauf

Projektidentitaet, Untersuchungsrahmen, Simulationsprogramme und neutrales Naming ohne fachlichen Projektstatus verwalten.

Der Steckbrief macht nur den dokumentierten Fachumfang sichtbar. Nicht vorhandene Fachwerte, Regeln oder Bedienfunktionen werden nicht ergänzt.

## Fachliche Eingänge

- Projektangaben
- Standardvorlagen
- Simulationsprogrammprofile

## Ausgänge und Übergaben

- ProjectContext
- aktive Simulationsprogrammreferenz
- Benennungsprofil

## Bedien- und Ablaufhinweis

Das Modul wird nur genutzt, wenn die genannten Eingänge im jeweiligen Projektkontext vorliegen. Sein Ergebnis wird als benannte Übergabe an die abhängigen Module weitergegeben; Navigation allein löst keine Fachaktion, Auswahl oder Persistenz aus.

## Abgrenzung

- Keine eigene Übergabe definiert.

## Abhängigkeiten

- ma_core

## Nächster dokumentierter Schritt

P011-S1b als separaten Pfad- und Persistenzvertrag mit Speicherort- und Ignore-Gate abgrenzen.

## Quellen und weiterführende Verweise

- `docs/project/workflow/README.md`
- `src/ma_workflow/catalog.py`

> Fachliche Quellen, Normwerte und externe Originaldaten werden nur nach den jeweils dokumentierten Rechte- und Fachgates ergänzt.
