# Datenvorbereitung

Modul-ID: `ma_data_preparation`  
Prozessbereich: **PostProcess**  
Status: **teilweise umgesetzt**

## Rolle im Ablauf

Standardisierte Simulationsergebnisse programmunabhaengig pruefen und in eine belastbare Analysebasis ueberfuehren.

Zeit- und Leistungssignaturen bleiben bis zum dokumentierten Fachgate als offene Ergebnissemantik gekennzeichnet.

## Fachliche Eingänge

- standardisierte Simulationsergebnisse

## Ausgänge und Übergaben

- aufbereitete Zeitreihen
- Qualitaetsbericht
- Eignungsstatus

## Bedien- und Ablaufhinweis

Das Modul wird nur genutzt, wenn die genannten Eingänge im jeweiligen Projektkontext vorliegen. Sein Ergebnis wird als benannte Übergabe an die abhängigen Module weitergegeben; Navigation allein löst keine Fachaktion, Auswahl oder Persistenz aus.

## Abgrenzung

- keine Variantenoptimierung
- kein Norm-Nachweis
- keine Sensitivitaetsbewertung

## Abhängigkeiten

- ma_import_simulation

## Nächster dokumentierter Schritt

P036: standardisierte IDA-Ergebnisreihen pruefen und nach data/ma_analyse/database aufbereiten.

## Quellen und weiterführende Verweise

- `docs/project/workflow/README.md`
- `src/ma_workflow/catalog.py`

> Fachliche Quellen, Normwerte und externe Originaldaten werden nur nach den jeweils dokumentierten Rechte- und Fachgates ergänzt.
