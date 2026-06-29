# ma_analyse Service-Schnittstelle

Stand: 2026-06-10

Aktueller Nachtrag 2026-06-28: Die Service-Schnittstelle bleibt fachlich
gueltig. Die Tkinter-Analyse liegt inzwischen ausschliesslich unter
`ma_ui.tkinter_app.module_views.analyse`; der alte Kompatibilitaetspfad
`ma_analyse.gui` und der CLI-Befehl `python -m ma_analyse gui` wurden entfernt.

## Zweck

Dieses Dokument ist Phase 2 von P005. Es definiert den Zielvertrag fuer eine
UI-neutrale Service-Schicht in `ma_analyse`.

Status: Der erste Code-Slice ist umgesetzt. `src/ma_analyse/models.py` enthaelt
`AnalysisConfig` und `AnalysisResult`. `src/ma_analyse/services.py` enthaelt
`run_analysis(config)` als Fassade ueber bestehender Logik.

P029-Zwischenstand vom 2026-06-27: `services.py` trennt inzwischen die
serviceinternen Runtime-Werte vom aktuellen Legacy-Argumentobjekt. Intern
normalisiert `_build_runtime_options(config)` die `AnalysisConfig`; erst
`_build_legacy_args(runtime_options)` baut das fuer `ma_analyse.app.commands`
noch notwendige `argparse.Namespace`.

P029-Fortschreibung vom 2026-06-27: Der eigentliche Legacy-Aufruf ist zusaetzlich
in `_execute_legacy_analysis(runtime_options, normalized_steps)` gekapselt.
`run_analysis(config)` bleibt dadurch die schmale Fassade fuer Validierung,
Dateisnapshot und Aufbau von `AnalysisResult`.

P029-Fortschreibung 2 vom 2026-06-27: `ma_analyse.app.commands.build_runtime_args`
erzeugt fuer interne Pipeline-Schritte jetzt `PipelineRuntimeArgs` statt eines
freien `argparse.Namespace`. Das Namespace-Objekt bleibt damit auf die
CLI-/Legacy-Eingangsgrenze beschraenkt.

P029-Fortschreibung 3 vom 2026-06-27: Datenvorbedingungen koennen mit
`check_required_data(args, steps)` strukturiert geprueft werden. Der bisherige
Wrapper `ensure_required_data(args, steps)` bleibt fuer CLI, Tkinter und
Legacy-Orchestrierung erhalten und wirft weiter `SystemExit(1)`.

P029-Fortschreibung 4 vom 2026-06-27: Der Servicepfad nutzt
`check_required_data(...)` jetzt vor dem Legacy-Aufruf. Fehlende Nutzdaten
werden als strukturierte Servicefehler in `AnalysisResult.errors`
zurueckgegeben; CLI und Tkinter bleiben ueber `ensure_required_data(...)`
kompatibel.

P029-Fortschreibung 5 vom 2026-06-28: Tkinter ist nicht mehr Teil von
`ma_analyse`. Das Fachmodul stellt weiterhin Services, Runner, Templates und
Konfigurationen bereit; der Tkinter-Startpfad und der lokale GUI-Parser liegen
unter `ma_ui.tkinter_app.module_views.analyse`.

P029-Fortschreibung 6 vom 2026-06-28: Die Tkinter-Analyse baut ihren
Analyseauftrag ueber `pipeline_config.py` als `AnalysisConfig` und startet ihn
ueber `ma_workflow.run_analysis_action`. Direkte Tkinter-Runner-Aufrufe von
`build_runtime_args`, `execute_steps` und `run_all` sind entfernt.

P029-Fortschreibung 7 vom 2026-06-29: `pipeline_config.py` delegiert die
eigentliche `AnalysisConfig`-Erzeugung an
`ma_analyse.analysis_ui.build_analysis_config`. Dieser UI-neutrale Builder
akzeptiert sowohl Textwerte aus Streamlit als auch Listenwerte aus der
Tkinter-Auswahl und setzt `load_kind` fuer Heating-/Cooling-Laeufe.

## Ziel

Die zentrale Oberflaeche `ma_ui` soll `ma_analyse` ohne Tkinter,
Streamlit-Importe im Fachmodul oder CLI-Argumentobjekte nutzen koennen.

Ziel-Schnittstelle:

```python
from ma_analyse.models import AnalysisConfig, AnalysisResult

def run_analysis(config: AnalysisConfig) -> AnalysisResult:
    ...
```

## Modelle

### AnalysisConfig

`AnalysisConfig` beschreibt einen fachlichen Analyseauftrag.

| Feld | Typ | Bedeutung |
|---|---|---|
| `steps` | `tuple[str, ...]` | Pipeline-Schritte, z. B. `prepare`, `plots`, `overview`, `analysis`, `analyze`, `heating`, `cooling`, `plot_template`, `all` |
| `input_dir` | `Path` | IDA-Importordner, Standard spaeter `data/ma_analyse/ida_imports` |
| `database_dir` | `Path` | aufbereitete Nutzdaten, Standard spaeter `data/ma_analyse/database` |
| `output_root` | `Path` | Ausgabewurzel, Standard spaeter `data/ma_analyse/output` |
| `run_id` | `str | None` | optionale Laufkennung |
| `variants` | `list[str] | None` | Varianten ohne `_rohdaten` oder `_nutzdaten` |
| `rooms` | `list[str]` | Raeume fuer Analyse und Plots |
| `debug` | `bool` | Debug-/Protokollausgabe aktivieren |
| `export_format` | `str` | Prepare-Export: `csv`, `excel` oder `both` |
| `comfort_output_type` | `str | None` | Comfort-Profil wie `plot`, `plot_overview`, `plot_analysis`, `plot_analysis_overview` |
| `load_kind` | `str | None` | `heating` oder `cooling` fuer Lastvergleiche |
| `view` | `str | None` | `bar`, `year`, `month`, `week` oder `day` |
| `month` | `str | None` | Monatsfilter |
| `week` | `int | None` | Kalenderwoche |
| `day` | `int | None` | Tag im Monat |
| `variant_mode` | `str | None` | `single` oder `compare` |
| `series_layout` | `str | None` | `separate` oder `combined` |
| `plot_template` | `str | None` | Plot-Template-Name |
| `plot_template_options` | `dict[str, object]` | Template-spezifische Optionen, Overlays und Achsen |

Defaults sollen aus `ma_analyse.core.config` und den bestehenden Settings-Modulen
kommen. Die UI soll keine Pfad- oder Plot-Defaults duplizieren.

### AnalysisResult

`AnalysisResult` beschreibt das Ergebnis eines Service-Aufrufs.

| Feld | Typ | Bedeutung |
|---|---|---|
| `success` | `bool` | Gesamtergebnis des Laufs |
| `steps` | `tuple[str, ...]` | tatsaechlich ausgefuehrte Schritte |
| `run_id` | `str | None` | verwendete Laufkennung |
| `created_files` | `list[Path]` | bekannte erzeugte Dateien, soweit ermittelbar |
| `summary_table` | `pd.DataFrame | None` | zentrale Ergebnistabelle, z. B. Comfort-Analyse |
| `detail_tables` | `dict[str, pd.DataFrame]` | optionale Detailtabellen |
| `warnings` | `list[str]` | fachliche Warnungen ohne Abbruch |
| `errors` | `list[str]` | Fehlertexte bei fehlgeschlagenem Lauf |
| `log_text` | `str` | gesammelte stdout-/stderr-Ausgabe aus bestehender Logik |
| `step_results` | `list[AnalysisStepResult]` | strukturierte Schrittuebersicht fuer UI, Workflow und spaetere Runner |

### AnalysisStepResult

`AnalysisStepResult` ist der P029-Einstieg in eine sauberere Runner-Schicht.
Die aktuelle Legacy-Orchestrierung kann Dateien und Logtext noch nicht in allen
Faellen schrittgenau zuordnen. Einzelschritt-Laeufe werden bereits direkt
zugeordnet; Mehrschritt-Laeufe werden zunaechst als strukturierte
Schrittuebersicht abgebildet und spaeter schrittweise verfeinert.

| Feld | Typ | Bedeutung |
|---|---|---|
| `step` | `str` | normalisierter Analyseschritt |
| `success` | `bool` | aktueller Erfolgsstatus im bestehenden Legacy-Lauf |
| `created_files` | `list[Path]` | bekannte erzeugte Dateien, soweit bereits zuordenbar |
| `warnings` | `list[str]` | Warnungen fuer diesen Schritt |
| `errors` | `list[str]` | Fehler fuer diesen Schritt |
| `log_text` | `str` | Logauszug fuer diesen Schritt, soweit bereits zuordenbar |

## Verhalten von run_analysis

Die erste Code-Umsetzung startet als Fassade ueber bestehender Logik, nicht als
Neuschreibung.

- `run_analysis(config)` validiert die Konfiguration.
- Die Funktion erzeugt intern `AnalysisRuntimeOptions` und uebersetzt diese
  anschliessend in das bisherige Runtime-Argumentobjekt, solange die
  bestehenden Funktionen dieses noch benoetigen.
- `_execute_legacy_analysis(...)` kapselt den aktuellen Aufruf von
  `run_all()` und `execute_steps()`.
- `build_runtime_args(...)` erzeugt fuer die interne Pipeline eine typisierte
  Runtime-Struktur; Attributzugriff und bestehende Runner bleiben kompatibel.
- Datenvorbedingungen sind mit `check_required_data(...)` ohne direkten
  Prozessabbruch pruefbar; der Legacy-Wrapper bleibt kompatibel.
- Fehlende Nutzdaten werden im Service vor dem Legacy-Aufruf erkannt; dadurch
  entsteht fuer diesen Fall kein interner `SystemExit` mehr.
- stdout/stderr werden gesammelt und in `AnalysisResult.log_text` abgelegt.
- Neue Dateien unter `database_dir` und `output_root` werden nach dem Lauf in
  `AnalysisResult.created_files` gelistet.
- P029 ergaenzt parallel `AnalysisResult.step_results` als ersten
  strukturierten Schrittvertrag; die bisherige Gesamtausgabe bleibt
  rueckwaertskompatibel erhalten.
- `SystemExit` aus bestehender CLI-naher Logik wird abgefangen und in
  `AnalysisResult(success=False, errors=[...])` uebersetzt.
- Tkinter und Streamlit werden in dieser Schicht nicht importiert.
- Die Funktion zeigt keine Messageboxen an und ruft keine UI-Funktionen auf.
- Bestehende Funktionen werden nicht in diesem Schritt verschoben.

Die aktuelle Grenze ist bewusst pragmatisch: `AnalysisRuntimeOptions` ist noch
keine oeffentliche API, sondern ein interner Zwischenschritt. Dadurch bleiben
CLI, Streamlit, `ma_workflow` und die getrennte Tkinter-Analyse kompatibel,
waehrend spaetere Slices `ma_analyse.app.commands`, `heating.py`,
`cooling.py` und die Tkinter-Datei unter `ma_ui` gezielter entkoppeln koennen.

## Einbindung in ma_ui

`ma_ui/pages/analyse.py` soll nur:

- Nutzereingaben erfassen.
- `AnalysisConfig` bauen.
- `run_analysis(config)` aufrufen.
- `AnalysisResult` anzeigen.

Die UI soll keine PRN-Dateien lesen, keine Plotdaten berechnen und keine
Excel-Reports direkt erzeugen.

Ziel nach der P005-Verschaerfung: Die bestehende `pages/`-Analyse-Seite ist ein
Zwischenstand. Spaeter wird die Analysebedienung nach
`ma_ui/module_views/analyse_view.py` ueberfuehrt. Der Aufruf laeuft dann ueber
eine Workflow-Aktion, zum Beispiel:

```python
result = run_analysis(config)
```

oder auf Workflow-Ebene:

```python
result = run_analysis_action(config)
```

`ma_ui` baut nur die Konfiguration und zeigt `AnalysisResult` an.
`ma_workflow` koordiniert den Aufruf. `ma_analyse` fuehrt die fachliche Arbeit
aus.

## Nicht-Ziele des ersten Code-Slices

- Keine Aufteilung der Tkinter-Hauptdatei unter `ma_ui`.
- Keine fachlich vollstaendige Streamlit-Analyseoberflaeche.
- Keine Neuschreibung von Heating, Cooling oder Comfort.
- Keine Aenderung der bestehenden CLI.
- Keine Umbenennung der bestehenden `ma_ui/pages/`-Shell ohne eigenen
  Migrationsslice.
- Keine direkte Uebernahme von Tkinter-Widgets oder Tkinter-Dialogen in
  Streamlit.

## Akzeptanzkriterien fuer den ersten Code-Slice

- `ma_analyse.services.run_analysis(config)` ist importierbar.
- `AnalysisConfig` und `AnalysisResult` sind UI-neutral.
- `run_analysis(config)` funktioniert ohne Tkinter und ohne Streamlit.
- Bestehende CLI-Tests bleiben gruen.
- Ein einfacher Service-Test kann mindestens einen bestehenden Schritt ueber die
  Fassade ausfuehren und ein `AnalysisResult` zurueckgeben.
