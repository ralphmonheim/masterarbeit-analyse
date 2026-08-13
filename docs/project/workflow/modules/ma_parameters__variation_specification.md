# Parameter-Variationsspezifikation

Modul-ID: `ma_parameters.variation_specification`  
Prozessbereich: **PreProcess**  
Status: **teilweise umgesetzt**

## Rolle im Ablauf

Freigegebene Regeln und Wertespannen nach der Referenzdimensionierung als aktuelle Variationsspezifikation speichern.

Der Steckbrief macht nur den dokumentierten Fachumfang sichtbar. Nicht vorhandene Fachwerte, Regeln oder Bedienfunktionen werden nicht ergänzt.

## Fachliche Eingänge

- Parameter-Referenzstand
- ReferenceDimensioningResult
- Regeln/Vorgaben

## Ausgänge und Übergaben

- projektbezogene ParameterVariationSpecification

## Bedien- und Ablaufhinweis

Das Modul wird nur genutzt, wenn die genannten Eingänge im jeweiligen Projektkontext vorliegen. Sein Ergebnis wird als benannte Übergabe an die abhängigen Module weitergegeben; Navigation allein löst keine Fachaktion, Auswahl oder Persistenz aus.

## Abgrenzung

- keine Kandidatenerzeugung
- keine Variantenpakete

## Abhängigkeiten

- ma_parameters
- ma_analyse.stage_1_dimensioning

## Nächster dokumentierter Schritt

Variationsraum und Kandidaten in ma_variants erzeugen.

## Quellen und weiterführende Verweise

- `docs/project/workflow/README.md`
- `src/ma_workflow/catalog.py`

> Fachliche Quellen, Normwerte und externe Originaldaten werden nur nach den jeweils dokumentierten Rechte- und Fachgates ergänzt.
