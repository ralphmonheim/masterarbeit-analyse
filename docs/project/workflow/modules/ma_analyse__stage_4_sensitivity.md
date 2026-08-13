# Analyse Stufe 4 - Sensitivitaet

Modul-ID: `ma_analyse.stage_4_sensitivity`  
Prozessbereich: **PostProcess**  
Status: **geplant**

## Rolle im Ablauf

Robustheit und Parametereinfluss fuer kritische Wetter- und Betriebsfaelle untersuchen.

Der Steckbrief macht nur den dokumentierten Fachumfang sichtbar. Nicht vorhandene Fachwerte, Regeln oder Bedienfunktionen werden nicht ergänzt.

## Fachliche Eingänge

- Wetterereignisse
- Varianten
- Zeitfenster
- Parameterstudien

## Ausgänge und Übergaben

- Sensitivitaetsvergleiche
- kritische Zeitraeume
- Robustheitshinweise

## Bedien- und Ablaufhinweis

Das Modul wird nur genutzt, wenn die genannten Eingänge im jeweiligen Projektkontext vorliegen. Sein Ergebnis wird als benannte Übergabe an die abhängigen Module weitergegeben; Navigation allein löst keine Fachaktion, Auswahl oder Persistenz aus.

## Abgrenzung

- keine vollstaendige probabilistische Risikoanalyse

## Abhängigkeiten

- ma_weather
- ma_analyse.stage_2_optimization

## Nächster dokumentierter Schritt

P021: Wetterereigniserkennung mit vorhandenen Tages- und Wochenanalysen verbinden.

## Quellen und weiterführende Verweise

- `docs/project/workflow/README.md`
- `src/ma_workflow/catalog.py`

> Fachliche Quellen, Normwerte und externe Originaldaten werden nur nach den jeweils dokumentierten Rechte- und Fachgates ergänzt.
