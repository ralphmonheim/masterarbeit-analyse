# Datenexport

Modul-ID: `ma_data_export`  
Prozessbereich: **PostProcess**  
Status: **geplant**

## Rolle im Ablauf

Maschinenlesbare Ergebnisdaten auswaehlen, paketieren und archivieren.

Der Steckbrief macht nur den dokumentierten Fachumfang sichtbar. Nicht vorhandene Fachwerte, Regeln oder Bedienfunktionen werden nicht ergänzt.

## Fachliche Eingänge

- fachmodulspezifische Exporte
- Projektmetadaten

## Ausgänge und Übergaben

- CSV-, JSON-, Excel- und Archivpakete

## Bedien- und Ablaufhinweis

Das Modul wird nur genutzt, wenn die genannten Eingänge im jeweiligen Projektkontext vorliegen. Sein Ergebnis wird als benannte Übergabe an die abhängigen Module weitergegeben; Navigation allein löst keine Fachaktion, Auswahl oder Persistenz aus.

## Abgrenzung

- fachmodulspezifische Exporte bleiben in den Fachmodulen

## Abhängigkeiten

- ma_reporting

## Nächster dokumentierter Schritt

Zentrale Paketformate und Auswahlregeln planen.

## Quellen und weiterführende Verweise

- `docs/project/workflow/README.md`
- `src/ma_workflow/catalog.py`

> Fachliche Quellen, Normwerte und externe Originaldaten werden nur nach den jeweils dokumentierten Rechte- und Fachgates ergänzt.
