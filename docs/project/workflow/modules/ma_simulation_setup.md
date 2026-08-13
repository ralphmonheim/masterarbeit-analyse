# Simulation konfigurieren

Modul-ID: `ma_simulation_setup`  
Prozessbereich: **PreProcess**  
Status: **geplant**

## Rolle im Ablauf

Neutrales Run-Paket mit Manifest, Setup, Variantenartefakten und technischen Logs fuer erzeugte Varianten vorbereiten.

Der Steckbrief macht nur den dokumentierten Fachumfang sichtbar. Nicht vorhandene Fachwerte, Regeln oder Bedienfunktionen werden nicht ergänzt.

## Fachliche Eingänge

- vollstaendige Varianten nach VGEN
- VariantSelection
- Projekt- und Wetterreferenzen

## Ausgänge und Übergaben

- RunManifest
- SimulationSetup
- RUN-ID
- direkte RUN -> VAR-Zuordnung
- technische Logs

## Bedien- und Ablaufhinweis

Das Modul wird nur genutzt, wenn die genannten Eingänge im jeweiligen Projektkontext vorliegen. Sein Ergebnis wird als benannte Übergabe an die abhängigen Module weitergegeben; Navigation allein löst keine Fachaktion, Auswahl oder Persistenz aus.

## Abgrenzung

- keine Variantenbildung
- keine Simulationsdateibearbeitung
- keine wissenschaftliche Zeitmessung

## Abhängigkeiten

- ma_variants

## Nächster dokumentierter Schritt

P018-S1: Neutrale Modelle, Status und YAML-Schemas fuer das Run-Paket umsetzen.

## Quellen und weiterführende Verweise

- `docs/project/workflow/README.md`
- `src/ma_workflow/catalog.py`

> Fachliche Quellen, Normwerte und externe Originaldaten werden nur nach den jeweils dokumentierten Rechte- und Fachgates ergänzt.
