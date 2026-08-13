# Zentrale Parameter

Modul-ID: `ma_parameters`  
Prozessbereich: **PreProcess**  
Status: **teilweise umgesetzt**

## Rolle im Ablauf

Eingaben vereinheitlichen, Parameter-/Optionskataloge besitzen und als stabile fachliche Quelle fuer ma_variants bereitstellen.

Der Steckbrief macht nur den dokumentierten Fachumfang sichtbar. Nicht vorhandene Fachwerte, Regeln oder Bedienfunktionen werden nicht ergänzt.

## Fachliche Eingänge

- Gebaeude
- Wetter
- Zonen
- Technik
- ReferenceDimensioningResult

## Ausgänge und Übergaben

- validierter ParameterSnapshot v1
- ParameterInputPackage
- BaselineParameterSnapshot
- ParameterVariationSpecification

## Bedien- und Ablaufhinweis

Das Modul wird nur genutzt, wenn die genannten Eingänge im jeweiligen Projektkontext vorliegen. Sein Ergebnis wird als benannte Übergabe an die abhängigen Module weitergegeben; Navigation allein löst keine Fachaktion, Auswahl oder Persistenz aus.

## Abgrenzung

- keine Variantenbildung

## Abhängigkeiten

- ma_weather
- ma_building
- ma_technical
- ma_zones

## Nächster dokumentierter Schritt

P015-S3b-Werteherkunft und den verbleibenden Vollumfang nach dem abgeschlossenen P013-/P014-Checkpoint getrennt abgrenzen.

## Quellen und weiterführende Verweise

- `docs/project/workflow/README.md`
- `src/ma_workflow/catalog.py`

> Fachliche Quellen, Normwerte und externe Originaldaten werden nur nach den jeweils dokumentierten Rechte- und Fachgates ergänzt.
