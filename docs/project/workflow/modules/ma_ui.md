# Benutzeroberflaeche

Modul-ID: `ma_ui`  
Prozessbereich: **Querschnitt**  
Status: **geplant**

## Rolle im Ablauf

Den Gesamtworkflow, Modulansichten und neutrale Serviceergebnisse in Streamlit darstellen.

Der Steckbrief macht nur den dokumentierten Fachumfang sichtbar. Nicht vorhandene Fachwerte, Regeln oder Bedienfunktionen werden nicht ergänzt.

## Fachliche Eingänge

- Workflow-Katalog
- neutrale Serviceergebnisse

## Ausgänge und Übergaben

- Benutzerauswahl
- Status- und Ergebnisdarstellung

## Bedien- und Ablaufhinweis

Das Modul wird nur genutzt, wenn die genannten Eingänge im jeweiligen Projektkontext vorliegen. Sein Ergebnis wird als benannte Übergabe an die abhängigen Module weitergegeben; Navigation allein löst keine Fachaktion, Auswahl oder Persistenz aus.

## Abgrenzung

- keine Fachlogik

## Abhängigkeiten

- ma_workflow

## Nächster dokumentierter Schritt

Startseite als Moduluebersicht leicht halten und Workflow-Referenz nur in ma_workflow pflegen.

## Quellen und weiterführende Verweise

- `docs/project/workflow/README.md`
- `src/ma_workflow/catalog.py`

> Fachliche Quellen, Normwerte und externe Originaldaten werden nur nach den jeweils dokumentierten Rechte- und Fachgates ergänzt.
