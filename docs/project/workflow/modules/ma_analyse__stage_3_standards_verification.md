# Analyse Stufe 3 - Norm-Nachweis

Modul-ID: `ma_analyse.stage_3_standards_verification`  
Prozessbereich: **PostProcess**  
Status: **geplant**

## Rolle im Ablauf

Varianten gegen nachvollziehbare deutsche und spaeter internationale Normenprofile pruefen.

Normprofile werden bis zum Methoden-, Rechte- und Fachtestgate nur als Nachweisbereitschaft gezeigt; keine PASS/FAIL-Regel wird daraus abgeleitet.

## Fachliche Eingänge

- Analysekennwerte
- Normenprofil
- Projekt- und Nutzungsrandbedingungen

## Ausgänge und Übergaben

- NormVerificationReport
- Pass/Fail/Warnung/Not-evaluable je Nachweis

## Bedien- und Ablaufhinweis

Das Modul wird nur genutzt, wenn die genannten Eingänge im jeweiligen Projektkontext vorliegen. Sein Ergebnis wird als benannte Übergabe an die abhängigen Module weitergegeben; Navigation allein löst keine Fachaktion, Auswahl oder Persistenz aus.

## Abgrenzung

- keine ungeprueften Grenzwerte
- keine allgemeine Modellvalidierung

## Abhängigkeiten

- ma_analyse.stage_2_optimization

## Nächster dokumentierter Schritt

P020: deutsche Normen, Ausgaben, Abschnitte und Berechnungsmethoden recherchieren.

## Quellen und weiterführende Verweise

- `docs/project/workflow/README.md`
- `src/ma_workflow/catalog.py`

> Fachliche Quellen, Normwerte und externe Originaldaten werden nur nach den jeweils dokumentierten Rechte- und Fachgates ergänzt.
