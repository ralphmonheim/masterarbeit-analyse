# IDA ICE

Modul-ID: `ida_ice`  
Prozessbereich: **Kernprozess**  
Status: **manuell / extern**

## Rolle im Ablauf

Externe Simulationsumgebung fuer den manuellen Simulationslauf.

Dieser Schritt bleibt bewusst manuell und extern. Der Steckbrief beschreibt nur die Übergabe, nicht die Bedienung oder Inhalte der externen Software.

## Fachliche Eingänge

- IDA-ICE-Exportpaket

## Ausgänge und Übergaben

- Simulationsergebnisse
- Simulationsmeldungen

## Bedien- und Ablaufhinweis

Das Modul wird nur genutzt, wenn die genannten Eingänge im jeweiligen Projektkontext vorliegen. Sein Ergebnis wird als benannte Übergabe an die abhängigen Module weitergegeben; Navigation allein löst keine Fachaktion, Auswahl oder Persistenz aus.

## Abgrenzung

- kein Python-Paket dieses Projekts

## Abhängigkeiten

- ma_export_simulation

## Nächster dokumentierter Schritt

Manuellen Ablauf und erforderliche Ergebnisdateien dokumentieren.

## Quellen und weiterführende Verweise

- `docs/project/workflow/README.md`
- `src/ma_workflow/catalog.py`

> Fachliche Quellen, Normwerte und externe Originaldaten werden nur nach den jeweils dokumentierten Rechte- und Fachgates ergänzt.
