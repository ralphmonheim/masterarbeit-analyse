# Referenzdimensionierung

Modul-ID: `ma_analyse.stage_1_dimensioning`  
Prozessbereich: **PreProcess**  
Status: **teilweise umgesetzt**

## Rolle im Ablauf

Heizlast, Kuehllast und Luftmengen fuer die Referenz fachlich dimensionieren.

Der Steckbrief macht nur den dokumentierten Fachumfang sichtbar. Nicht vorhandene Fachwerte, Regeln oder Bedienfunktionen werden nicht ergänzt.

## Fachliche Eingänge

- validierter ParameterSnapshot v1
- Norm- und Auslegungsannahmen

## Ausgänge und Übergaben

- LoD-1-Referenzdimensionierung
- ReferenceDimensioningResult
- Dimensionierungshinweise

## Bedien- und Ablaufhinweis

Das Modul wird nur genutzt, wenn die genannten Eingänge im jeweiligen Projektkontext vorliegen. Sein Ergebnis wird als benannte Übergabe an die abhängigen Module weitergegeben; Navigation allein löst keine Fachaktion, Auswahl oder Persistenz aus.

## Abgrenzung

- keine Variantenbildung
- kein normatives Lastverfahren
- keine Ergebnisanalyse der Simulationslaeufe

## Abhängigkeiten

- ma_parameters

## Nächster dokumentierter Schritt

VariantVerification-Anfragen ueber ma_workflow und spaetere IDA-Plausibilisierung planen.

## Quellen und weiterführende Verweise

- `docs/project/workflow/README.md`
- `src/ma_workflow/catalog.py`

> Fachliche Quellen, Normwerte und externe Originaldaten werden nur nach den jeweils dokumentierten Rechte- und Fachgates ergänzt.
