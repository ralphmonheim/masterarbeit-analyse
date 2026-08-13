# Technische Systeme

Modul-ID: `ma_technical`  
Prozessbereich: **PreProcess**  
Status: **teilweise umgesetzt**

## Rolle im Ablauf

Zentrale technische Systeme, Kreise, Anlagen und generische technische Datensaetze beschreiben.

Die technische Auswahl ist ein getrennt validierter Fachschritt; Produktdatenbanken und zonale Übergabekonfiguration werden nicht aus diesem Ablauf abgeleitet.

## Fachliche Eingänge

- freigegebene Gebaeudedaten
- aktives thermisches Modell
- validierte Zonen-IDs

## Ausgänge und Übergaben

- validierte LoD-1-Technikdaten fuer ma_parameters
- zentrale Systemreferenzen fuer ma_zones

## Bedien- und Ablaufhinweis

Das Modul wird nur genutzt, wenn die genannten Eingänge im jeweiligen Projektkontext vorliegen. Sein Ergebnis wird als benannte Übergabe an die abhängigen Module weitergegeben; Navigation allein löst keine Fachaktion, Auswahl oder Persistenz aus.

## Abgrenzung

- keine Variantenbildung
- keine zonenbezogene Uebergabekonfiguration
- keine Produktdatenbank

## Abhängigkeiten

- ma_building
- ma_zones

## Nächster dokumentierter Schritt

P014-S4-Persistenz/YAML und eine v2-Werteherkunft nur in getrennt freigegebenen Folgeslices behandeln.

## Quellen und weiterführende Verweise

- `docs/project/workflow/README.md`
- `src/ma_workflow/catalog.py`

> Fachliche Quellen, Normwerte und externe Originaldaten werden nur nach den jeweils dokumentierten Rechte- und Fachgates ergänzt.
