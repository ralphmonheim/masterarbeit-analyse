# Wetterdaten

Modul-ID: `ma_weather`  
Prozessbereich: **PreProcess**  
Status: **umgesetzt**

## Rolle im Ablauf

TRY-Datensaetze katalogisieren, importieren, validieren, analysieren und dokumentieren.

Der Steckbrief macht nur den dokumentierten Fachumfang sichtbar. Nicht vorhandene Fachwerte, Regeln oder Bedienfunktionen werden nicht ergänzt.

## Fachliche Eingänge

- lokale TRY-Dateien
- Wetterkatalog

## Ausgänge und Übergaben

- weather_key
- Wetterkennwerte
- Diagnosen
- Freigabestatus
- Berichte

## Bedien- und Ablaufhinweis

Das Modul wird nur genutzt, wenn die genannten Eingänge im jeweiligen Projektkontext vorliegen. Sein Ergebnis wird als benannte Übergabe an die abhängigen Module weitergegeben; Navigation allein löst keine Fachaktion, Auswahl oder Persistenz aus.

## Abgrenzung

- keine IDA-Zonenergebnisanalyse

## Abhängigkeiten

- ma_project

## Nächster dokumentierter Schritt

P008: Reale Wetterdatensaetze pruefen, P021-Ereignisdefinition schaerfen und Freshness-Abgleich fuer ma_parameters vorbereiten.

## Quellen und weiterführende Verweise

- `docs/project/workflow/README.md`
- `src/ma_workflow/catalog.py`

> Fachliche Quellen, Normwerte und externe Originaldaten werden nur nach den jeweils dokumentierten Rechte- und Fachgates ergänzt.
