# Simulationsexport

Modul-ID: `ma_export_simulation`  
Prozessbereich: **Kernprozess**  
Status: **geplant**

## Rolle im Ablauf

Varianten und Run-Konfiguration programmunabhaengig fuer Simulationsadapter vorbereiten.

Der Steckbrief macht nur den dokumentierten Fachumfang sichtbar. Nicht vorhandene Fachwerte, Regeln oder Bedienfunktionen werden nicht ergänzt.

## Fachliche Eingänge

- VariantGeneration
- RunManifest
- Referenzmodell
- Parametermapping

## Ausgänge und Übergaben

- Exportpaket
- Run-Manifest
- Adapterartefakte

## Bedien- und Ablaufhinweis

Das Modul wird nur genutzt, wenn die genannten Eingänge im jeweiligen Projektkontext vorliegen. Sein Ergebnis wird als benannte Übergabe an die abhängigen Module weitergegeben; Navigation allein löst keine Fachaktion, Auswahl oder Persistenz aus.

## Abgrenzung

- kein Simulationsstart
- keine ungesicherte IDM-Manipulation

## Abhängigkeiten

- ma_variants
- ma_simulation_setup

## Nächster dokumentierter Schritt

P009 nach P018 ueber RUN-ID und VAR-ID weiterfuehren.

## Quellen und weiterführende Verweise

- `docs/project/workflow/README.md`
- `src/ma_workflow/catalog.py`

> Fachliche Quellen, Normwerte und externe Originaldaten werden nur nach den jeweils dokumentierten Rechte- und Fachgates ergänzt.
