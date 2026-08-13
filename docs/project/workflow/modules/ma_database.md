# Datenbank

Modul-ID: `ma_database`  
Prozessbereich: **Querschnitt**  
Status: **geplant**

## Rolle im Ablauf

Spaetere moduluebergreifende Persistenz und Datenbankzugriffe kapseln.

Der Steckbrief macht nur den dokumentierten Fachumfang sichtbar. Nicht vorhandene Fachwerte, Regeln oder Bedienfunktionen werden nicht ergänzt.

## Fachliche Eingänge

- fachliche Datenmodelle

## Ausgänge und Übergaben

- persistierte Projektdaten
- Repository-Schnittstellen

## Bedien- und Ablaufhinweis

Das Modul wird nur genutzt, wenn die genannten Eingänge im jeweiligen Projektkontext vorliegen. Sein Ergebnis wird als benannte Übergabe an die abhängigen Module weitergegeben; Navigation allein löst keine Fachaktion, Auswahl oder Persistenz aus.

## Abgrenzung

- bestehende Datenbanklogik in ma_variants bleibt vorerst bestehen

## Abhängigkeiten

- ma_core

## Nächster dokumentierter Schritt

Moduluebergreifenden Persistenzbedarf vor einer Extraktion festlegen.

## Quellen und weiterführende Verweise

- `docs/project/workflow/README.md`
- `src/ma_workflow/catalog.py`

> Fachliche Quellen, Normwerte und externe Originaldaten werden nur nach den jeweils dokumentierten Rechte- und Fachgates ergänzt.
