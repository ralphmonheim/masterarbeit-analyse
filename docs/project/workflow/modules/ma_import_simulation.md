# Simulationsergebnisimport

Modul-ID: `ma_import_simulation`  
Prozessbereich: **Kernprozess**  
Status: **geplant**

## Rolle im Ablauf

Ergebnisdateien programmunabhaengig erkennen, zuordnen und vereinheitlichen.

Der Import ordnet bereitgestellte Ergebnisse zu, bewertet sie aber nicht fachlich.

## Fachliche Eingänge

- Simulationsergebnisse
- RUN-ID
- VAR-ID
- Run-Manifest

## Ausgänge und Übergaben

- standardisierte Ergebnisdaten fuer ma_analyse

## Bedien- und Ablaufhinweis

Das Modul wird nur genutzt, wenn die genannten Eingänge im jeweiligen Projektkontext vorliegen. Sein Ergebnis wird als benannte Übergabe an die abhängigen Module weitergegeben; Navigation allein löst keine Fachaktion, Auswahl oder Persistenz aus.

## Abgrenzung

- keine fachliche Ergebnisbewertung

## Abhängigkeiten

- ma_export_simulation

## Nächster dokumentierter Schritt

P009-MVP: Manuell bereitgestellte Ergebnisdateien neutral ueber RUN-ID und VAR-ID zuordnen.

## Quellen und weiterführende Verweise

- `docs/project/workflow/README.md`
- `src/ma_workflow/catalog.py`

> Fachliche Quellen, Normwerte und externe Originaldaten werden nur nach den jeweils dokumentierten Rechte- und Fachgates ergänzt.
