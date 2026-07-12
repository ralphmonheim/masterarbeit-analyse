# ma_workflow

`ma_workflow` ist die neutrale Orchestrierungsschicht zwischen Oberflaeche und
Fachmodulen.

## Zweck

Phasen, Module, Status, Workflow-Schritte und UI-Aktionen zentral und
UI-neutral beschreiben.

## Eingaben

- Moduldefinitionen und Umsetzungsstatus
- neutrale Aufrufkonfigurationen aus `ma_ui`

## Ausgaben

- geordnete Phasen und Workflow-Schritte
- Moduldefinitionen, Dashboard-Aktionen und Ruecksprungziele

## Abgrenzung

- keine Fachberechnung
- keine Streamlit- oder Tkinter-Abhaengigkeit
- keine fachliche Iterationsentscheidung

## Abhaengigkeiten

- UI-neutrale Services der Fachmodule

## Status

Geplant. Ein Prototyp des zentralen Katalogs und des Analyseadapters ist
umgesetzt; der durchgaengige fachliche Workflow fehlt.

## Naechster Schritt

Katalog stabil halten und Fachservice-Aufrufe nur mit den jeweiligen
freigegebenen Modulslices ergaenzen.

## Rolle

- beschreibt den Gesamtworkflow der Masterarbeit
- katalogisiert Phase 0 und die sechs fachlichen P007-Hauptphasen
- beschreibt alle Module mit Zweck, Grenzen, Status und naechstem Schritt
- fuehrt `ma_validation` und `ma_feedback` phasenuebergreifend
- stellt Adapter fuer Fachmodulaufrufe bereit
- enthaelt keine Streamlit- oder Tkinter-Abhaengigkeit
- enthaelt keine fachliche Berechnungslogik

## Aktueller Stand

- Phasen-, Modul- und Workflow-Katalog ist umgesetzt und zentrale Quelle fuer
  die Modulumsetzungsstaende in Streamlit.
- Statuswerte werden bei `aktualisieren` gegen Fachpakete, Services, Views,
  Tests und Dokumentation geprueft.
- `workflow_manager.py` stellt den zentralen Zugriff auf Workflow-Schritte bereit.
- `dashboard_actions.py` dokumentiert UI-Aktionen wie `open_weather`,
  `open_simulation_setup`, `run_analysis` und `run_assessment`.
- `pre_process_runner.py` und `post_process_runner.py` bleiben
  Kompatibilitaetswrapper fuer bestehende Aufrufer.
- `feedback_router.py` enthaelt die geplanten Ruecksprungziele fuer Feedback.
- Analyse-Adapter ruft `ma_analyse.services.run_analysis(config)` auf.
- Phase 4 trennt Optimierung, Standards Compliance und Sensitivitaet als
  eigene katalogisierte Analysestufen.
- Weitere Adapter fuer Varianten, Wetterdaten, Simulationsexport/-import und
  Bewertung folgen spaeter nach separaten Slices.
- Fuer P017 koordiniert `ma_workflow` spaeter die technische
  Dimensionierungsunterbrechung innerhalb von `VariantVerification`:
  `VVER -> DimensioningRequest -> ma_analyse -> DimensioningResult -> VVER`.
  Das ist Wiederaufnahme eines laufenden Schritts, keine aktive CaseIteration.

Oeffentliche Katalogfunktionen:

- `list_workflow_phases()`
- `list_module_definitions()`
- `get_module_definition(module_key)`
- `list_workflow_steps()`
- `list_cross_cutting_steps()`

Historische Schluessel fuer IDA-spezifische Hauptmodule werden nur als
Uebergangsaliase auf die allgemeinen Simulationsschnittstellen aufgeloest.

Aktuelle Statusbedeutung:

- `available`: im fachlichen Masterarbeitsworkflow belastbar nutzbar und getestet
- `partial`: wesentliche Fachlogik ist im Zielablauf nutzbar, aber noch
  unvollstaendig
- `planned`: fachlicher Zielablauf fehlt; Gerueste und Prototypen koennen
  bereits vorhanden sein
- `manual`: externer oder bewusst manueller Schritt
