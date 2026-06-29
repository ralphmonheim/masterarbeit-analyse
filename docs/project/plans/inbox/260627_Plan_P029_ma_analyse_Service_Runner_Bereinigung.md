# P029 ma_analyse Service- und Runner-Bereinigung

Stand: 2026-06-29
Status: Aktiv
Prioritaet: Hoch
Abhaengigkeiten: P005, P019, P027, bestehendes `ma_analyse`

## Ziel

`ma_analyse` soll schrittweise besser aufgeraeumt werden, ohne bestehende
Analysefunktionen, fachliche CLI-Befehle, getrennte Tkinter-Bedienung oder
Streamlit-Anbindung zu gefaehrden.

Der naechste grosse Schritt ist eine stabilere Service- und Runner-Schicht
zwischen `AnalysisConfig` und den bestehenden Fachfunktionen. Danach koennen
`heating.py`, `cooling.py` und Tkinter gezielter verkleinert werden.

## Ausgangslage

- `ma_analyse.models.AnalysisConfig` und `AnalysisResult` existieren bereits.
- `ma_analyse.services.run_analysis(config)` ist die UI-neutrale Fassade.
- `ma_ui.streamlit_app.module_views.analyse_view` baut bereits
  `AnalysisConfig` und ruft ueber `ma_workflow` den Service auf.
- `ma_analyse.app.commands` ist weiterhin stark CLI-nah:
  `argparse.Namespace`, `print()` und `SystemExit` sind noch Teil des
  internen Ausfuehrungspfads.
- Tkinter liegt inzwischen unter `ma_ui.tkinter_app.module_views.analyse` und
  nutzt fuer den Start ueber den Runner inzwischen `AnalysisConfig` und
  `ma_workflow.run_analysis_action`.
- `heating.py` und `cooling.py` sind gross und aehnlich, sollen aber erst nach
  stabilerer Ausfuehrungsschicht zerlegt werden.

## Leitentscheidung

Zuerst wird der Vertrag zwischen UI, Workflow und Analyse stabilisiert. Die
Fachfunktionen bleiben in diesem Plan zunaechst an Ort und Stelle.

## Arbeitspakete

1. **Ergebnisvertrag erweitern**
   - `AnalysisResult` um strukturierte Schrittinformationen erweitern.
   - Erzeugte Dateien, Fehler, Warnungen und Logtext weiterhin kompatibel auf
     der bisherigen Ebene bereitstellen.
   - Streamlit und bestehende Tests duerfen durch neue Felder nicht brechen.

2. **Interne Runner-Grenze vorbereiten**
   - Eine kleine neutrale Struktur fuer Schrittstatus und spaetere Runner
     einfuehren.
   - Noch keine grosse Zerlegung von `app.commands`.
   - Noch keine Umstellung der CLI-Syntax.

3. **CLI-nahe Runtime-Argumente reduzieren**
   - Aktuellen `argparse.Namespace`-Pfad inventarisieren.
   - Schrittweise durch ein internes Runtime-Modell ersetzen.
   - Bestehende `dispatch_command()`- und CLI-Tests bleiben gruen.

4. **Tkinter-Anbindung entkoppeln**
   - Direkte Tkinter-Aufrufe von `build_runtime_args`, `execute_steps` und
     `run_all` pruefen.
   - Zielpfad: Tkinter baut langfristig ebenfalls einen `AnalysisConfig` oder
     nutzt denselben Runner-Vertrag.
   - Keine grosse Tkinter-Dateiaufteilung in diesem Plan.

5. **Folgearbeit Heating/Cooling vorbereiten**
   - Nach stabilerer Runner-Schicht `heating.py` und `cooling.py` ueber
     gemeinsame Energy-Komponenten weiter zerlegen.
   - Keine fachliche Aenderung der Diagrammlogik ohne eigenen Slice.

## Nicht-Ziele

- Keine Umbenennung bestehender Befehle.
- Keine Aenderung bestehender Ausgabepfade oder Dateinamen.
- Keine grosse Zerlegung von `heating.py` oder `cooling.py` im ersten Slice.
- Keine direkte Uebernahme von Tkinter-Widgets in Streamlit.
- Keine fachliche Kopie von Analysefunktionen nach `ma_ui`; Tkinter nutzt
  weiterhin das `ma_analyse`-Backend.

## Akzeptanzkriterien

- `run_analysis(config)` bleibt der zentrale UI-neutrale Einstieg.
- Bestehende CLI- und UI-Tests bleiben gruen.
- `AnalysisResult` enthaelt strukturierte Schrittinformationen, ohne alte
  Verbraucher zu brechen.
- Fehlende Daten und bestehende `SystemExit`-Fehler werden weiter als
  UI-freundliches Ergebnis zurueckgegeben.
- Die Doku beschreibt klar, dass P029 die Voraussetzung fuer spaetere
  Heating-/Cooling- und Tkinter-Bereinigung ist.

## Erste Umsetzung

Slice 1:

- `AnalysisStepResult` einfuehren.
- `AnalysisResult.step_results` rueckwaertskompatibel ergaenzen.
- `ma_analyse.services.run_analysis()` fuellt fuer aktuelle Legacy-Laeufe eine
  erste strukturierte Schrittuebersicht.
- Tests fuer Validierungsfehler, fehlende Datenbank und erzeugte Dateien
  erweitern.

Slice 2:

- `AnalysisRuntimeOptions` als interne, UI-neutrale Laufstruktur in
  `ma_analyse.services` einfuehren.
- `_build_runtime_options(config)` normalisiert `AnalysisConfig` fuer den
  Servicepfad.
- `_build_legacy_args(runtime_options)` baut daraus nur noch den aktuellen
  Adapter fuer `ma_analyse.app.commands`.
- `_build_args(config)` bleibt als kompatibler Hilfsadapter erhalten.
- `run_analysis(config)` nutzt intern die Runtime-Optionen und uebersetzt
  weiterhin `SystemExit`, Logausgaben und erzeugte Dateien in
  `AnalysisResult`.
- Tests sichern Runtime-Normalisierung und bestehenden Namespace-Vertrag ab.

Slice 3:

- `LegacyExecutionResult` als interne Ergebnisstruktur fuer den aktuellen
  Legacy-Orchestrator einfuehren.
- `_execute_legacy_analysis(runtime_options, normalized_steps)` kapselt
  `run_all()`, `execute_steps()`, stdout-/stderr-Sammlung,
  `SystemExit`-Uebersetzung und unerwartete Exceptions.
- `run_analysis(config)` bleibt die oeffentliche Fassade und fokussiert sich
  auf Validierung, Runtime-Aufbau, Dateisnapshot und Aufbau von
  `AnalysisResult`.
- Tests sichern die Adapterpfade fuer `all`, `comfort`, `plot_template` und
  `SystemExit` ab.

Slice 4:

- `PipelineRuntimeArgs` als internen, typisierten Schrittvertrag in
  `ma_analyse.app.commands` einfuehren.
- `build_runtime_args(...)` behaelt Signatur und Verhalten, gibt aber
  `PipelineRuntimeArgs` statt `argparse.Namespace` zurueck.
- CLI, Tkinter, Streamlit und bestehende Runner nutzen weiter Attributzugriff;
  oeffentliche Befehle und Ausgabepfade bleiben unveraendert.
- Die Runtime bleibt bewusst mutierbar, weil `run_all()` die gemeinsame
  `run_id` im bestehenden Ablauf setzt.
- Tests sichern Typ, Defaults, Optionsueberschreibungen und
  `run_all()`-Kompatibilitaet ab.

Slice 5:

- `PipelinePreconditionResult` als strukturierte Rueckgabe fuer
  Pipeline-Vorbedingungen einfuehren.
- `check_required_data(args, steps)` prueft fehlende Nutzdaten ohne direkte
  Logausgabe und ohne eigenen Prozessabbruch.
- `ensure_required_data(args, steps)` bleibt als Legacy-Wrapper erhalten,
  druckt die bisherigen Meldungen und wirft weiterhin `SystemExit(1)`.
- Tests sichern erlaubte Faelle, fehlende Datenbankmeldungen und den
  kompatiblen Legacy-Abbruch ab.

Slice 6:

- `ma_analyse.services._execute_legacy_analysis(...)` nutzt
  `check_required_data(...)` vor dem aktuellen Legacy-Aufruf.
- Die Service-Fassade loest Sammelbefehle fuer die Vorbedingungspruefung auf:
  `all` prueft die datenbankabhaengigen Analyse-, Heating- und Cooling-
  Schritte; `comfort` prueft die Schritte aus dem gewaehlten Comfort-Profil.
- Fehlende Nutzdaten werden im Service als
  `LegacyExecutionResult(success=False, errors=[...])` zurueckgegeben, ohne
  `run_all()` oder `execute_steps()` aufzurufen.
- CLI und Tkinter bleiben ueber `ensure_required_data(...)` kompatibel.
- Tests sichern strukturierte Servicefehler, Alias-/Sammelbefehlpfade und den
  Nichtaufruf des Legacy-Runners bei fehlenden Nutzdaten ab.

Slice 7:

- Die harte Tkinter-Migration entfernt `ma_analyse.gui.*` und den alten
  CLI-Befehl `python -m ma_analyse gui`.
- `ma_ui.tkinter_app.module_views.analyse` wird alleiniger Eigentumer der
  Tkinter-Analyse und erhaelt einen eigenen kleinen Parser fuer GUI-Startwerte.
- Der Streamlit-Launcher bleibt beim kanonischen Modulstart
  `python -m ma_ui.tkinter_app.module_views.analyse`.
- Tests sichern, dass die `ma_analyse`-CLI keinen `gui`-Befehl mehr anbietet
  und der neue Tkinter-Parser weiter lauffaehig ist.

Slice 8:

- Die Tkinter-Analyse unter `ma_ui.tkinter_app.module_views.analyse` wurde
  intern in Mixins fuer Initialisierung, Fenster/Style, Layout, Schrittfluss,
  Auswahl-State, Plot-Template-State und Pipeline-Runner zerlegt.
- `app.py` bleibt die oeffentliche Fassade mit `PipelineGUI`, `run_gui`,
  `run_gui_refresh` und `run_gui_menu`; die privaten Methodennamen bleiben
  fuer bestehende Tests und interne Aufrufe stabil.
- `restart.py`, `tk_compat.py` und `constants.py` kapseln Restart-Argumente,
  Tkinter-Importe und UI-Konstanten.
- Tests sichern Paketimports, Restart-Argumente, Parser-Defaults und die
  bisherigen GUI-Helfer ab.

Slice 9:

- `pipeline_config.py` baut aus dem Tkinter-Zustand einen UI-neutralen
  `AnalysisConfig`.
- `pipeline_runner.py` ruft die Analyse ueber `ma_workflow.run_analysis_action`
  auf und nutzt nicht mehr direkt `build_runtime_args`, `execute_steps` oder
  `run_all` aus `ma_analyse.app.commands`.
- `AnalysisResult.log_text`, Warnungen, Fehler und erzeugte Dateien werden in
  das bestehende Tkinter-Protokollfenster geschrieben.
- Tests sichern den Config-Adapter und den Worker-Aufruf ueber die
  Workflow-Aktion ab.

## Risiken

- Zu fruehe Zerlegung von `app.commands` koennte CLI, Tkinter und Streamlit
  gleichzeitig treffen.
- Schrittgenaue Dateizuordnung ist mit der aktuellen Legacy-Orchestrierung noch
  nur begrenzt moeglich.
- Heating/Cooling sollten erst nach stabilem Runner-Vertrag weiter
  modularisiert werden.
