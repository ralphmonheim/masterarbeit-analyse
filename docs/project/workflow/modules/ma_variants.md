# Varianten

Modul-ID: `ma_variants`  
Prozessbereich: **PreProcess**  
Status: **geplant**

## Rolle im Ablauf

Variantenraum, Verifikation, Katalog, Auswahl, Generierung und Benennung verwalten.

Der Steckbrief macht nur den dokumentierten Fachumfang sichtbar. Nicht vorhandene Fachwerte, Regeln oder Bedienfunktionen werden nicht ergänzt.

## Fachliche Eingänge

- BaselineParameterSnapshot
- ReferenceDimensioningResult
- ParameterVariationSpecification
- Benennungsprofil aus ma_project

## Ausgänge und Übergaben

- VariantSpace
- VariantVerification
- VariantCatalog
- VariantSelection
- VariantGeneration

## Bedien- und Ablaufhinweis

Das Modul wird nur genutzt, wenn die genannten Eingänge im jeweiligen Projektkontext vorliegen. Sein Ergebnis wird als benannte Übergabe an die abhängigen Module weitergegeben; Navigation allein löst keine Fachaktion, Auswahl oder Persistenz aus.

## Abgrenzung

- keine direkte Abhaengigkeit von Eingabefachmodulen
- kein Simulationssetup

## Abhängigkeiten

- ma_parameters

## Nächster dokumentierter Schritt

P017-S1: Grundobjekte, IDs, VariantSpace, Zaehlmodell und stabile Eingangsreferenzen planen.

## Quellen und weiterführende Verweise

- `docs/project/workflow/README.md`
- `src/ma_workflow/catalog.py`

> Fachliche Quellen, Normwerte und externe Originaldaten werden nur nach den jeweils dokumentierten Rechte- und Fachgates ergänzt.
