# Zonen

Modul-ID: `ma_zones`  
Prozessbereich: **PreProcess**  
Status: **teilweise umgesetzt**

## Rolle im Ablauf

Zonen, Nutzungen, Profile, Konditionierung und zonenbezogene Uebergabe verwalten.

Nutzungsprofile und Konditionierung werden fachlich gezeigt; eine automatische Zonenbildung gehört nicht zum V1-Ablauf.

## Fachliche Eingänge

- freigegebene Gebaeude-/Raumdaten
- Nutzungsanforderungen

## Ausgänge und Übergaben

- validierte Zonendaten fuer ma_parameters
- ReleasedZoneHandover als payloadfreier Referenzcheckpoint
- zonenbezogene Uebergabe- und Betriebszuordnungen

## Bedien- und Ablaufhinweis

Das Modul wird nur genutzt, wenn die genannten Eingänge im jeweiligen Projektkontext vorliegen. Sein Ergebnis wird als benannte Übergabe an die abhängigen Module weitergegeben; Navigation allein löst keine Fachaktion, Auswahl oder Persistenz aus.

## Abgrenzung

- keine Gebaeudegeometrie
- keine zentralen Erzeugungsanlagen
- keine automatische Zonenbildung im MVP

## Abhängigkeiten

- ma_building

## Nächster dokumentierter Schritt

Aktives thermisches Modell und validierte Zonen-IDs an ma_technical uebergeben.

## Quellen und weiterführende Verweise

- `docs/project/workflow/README.md`
- `src/ma_workflow/catalog.py`

> Fachliche Quellen, Normwerte und externe Originaldaten werden nur nach den jeweils dokumentierten Rechte- und Fachgates ergänzt.
