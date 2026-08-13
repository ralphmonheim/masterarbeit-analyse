# Feedback und Rueckspruenge

Modul-ID: `ma_feedback`  
Prozessbereich: **Querschnitt**  
Status: **geplant**

## Rolle im Ablauf

Auffaelligkeiten klassifizieren und Rueckspruenge in verantwortliche Module steuern.

Der Steckbrief macht nur den dokumentierten Fachumfang sichtbar. Nicht vorhandene Fachwerte, Regeln oder Bedienfunktionen werden nicht ergänzt.

## Fachliche Eingänge

- Fehler
- Warnungen
- Analyse- und Bewertungsergebnisse
- P017-Checkpointstatus

## Ausgänge und Übergaben

- Ruecksprungziel
- Reload- oder Abort-Entscheidung
- dokumentierte Iteration

## Bedien- und Ablaufhinweis

Das Modul wird nur genutzt, wenn die genannten Eingänge im jeweiligen Projektkontext vorliegen. Sein Ergebnis wird als benannte Übergabe an die abhängigen Module weitergegeben; Navigation allein löst keine Fachaktion, Auswahl oder Persistenz aus.

## Abgrenzung

- keine automatische Aenderung von Fachmoduldaten

## Abhängigkeiten

- ma_validation
- ma_workflow

## Nächster dokumentierter Schritt

P027-Problemtypen, Reload-Regeln und Abbruchgrenzen fuer Variantenlaeufe ausarbeiten.

## Quellen und weiterführende Verweise

- `docs/project/workflow/README.md`
- `src/ma_workflow/catalog.py`

> Fachliche Quellen, Normwerte und externe Originaldaten werden nur nach den jeweils dokumentierten Rechte- und Fachgates ergänzt.
