# Gebaeude

Modul-ID: `ma_building`  
Prozessbereich: **PreProcess**  
Status: **teilweise umgesetzt**

## Rolle im Ablauf

Gebaeudemodell, Bauteile und bauphysikalische Randbedingungen verwalten.

Begriffe wie BIL und LoD werden im Steckbrief nur als Nutzungshilfe erklärt; konkrete Fachwerte und Importverfahren bleiben in ihren freigegebenen Fachquellen.

## Fachliche Eingänge

- BuildingModelSpecification
- BusinessIntegration-LoD-1
- SmallOffice-IFC
- Rhino-Testgebaeude

## Ausgänge und Übergaben

- validierbare Demo-Gebaeudedaten
- LoD-1-Huellkennwerte
- strukturierte Quelldiagnosen

## Bedien- und Ablaufhinweis

Das Modul wird nur genutzt, wenn die genannten Eingänge im jeweiligen Projektkontext vorliegen. Sein Ergebnis wird als benannte Übergabe an die abhängigen Module weitergegeben; Navigation allein löst keine Fachaktion, Auswahl oder Persistenz aus.

## Abgrenzung

- kein produktiver IFC-/Rhino-Import
- keine Zonenprofile
- keine technische Anlagenlogik

## Abhängigkeiten

- ma_project

## Nächster dokumentierter Schritt

LoD-2-Raum-/Bauteilumfang klaeren und IFC-Lite-Umfang getrennt freigeben.

## Quellen und weiterführende Verweise

- `docs/project/workflow/README.md`
- `src/ma_workflow/catalog.py`

> Fachliche Quellen, Normwerte und externe Originaldaten werden nur nach den jeweils dokumentierten Rechte- und Fachgates ergänzt.
