# Befehle ma_ui

## Zentrale Streamlit-Oberflaeche starten

Empfohlen ist der Modulaufruf ueber die Projekt-venv:

```powershell
.\.venv\Scripts\python.exe -m streamlit run src\ma_ui\app.py
```

Alternative:

```powershell
.\.venv\Scripts\streamlit.exe run src\ma_ui\app.py
```

## Hinweise

- `ma_ui` ist aktuell eine minimale Shell mit Zielstruktur fuer
  `module_views/` und `shared/`.
- Die Codex-Routine `tagesstart` darf diese Oberflaeche automatisch ueber die
  Projekt-venv auf Port `8501` starten, wenn sie noch nicht laeuft.
- Die Startseite zeigt ein grafisches Workflow-Dashboard mit Phasen,
  Statuskarten, Iterationspfaden und Buttons zu den vorhandenen Modulansichten.
- Fachlogik wird nicht in der UI berechnet.
- Analyseaufrufe laufen ueber `ma_workflow` und die Service-Fassade von
  `ma_analyse`.
- Die Analyse-Seite enthaelt einen Button `Tkinter-Analyse oeffnen`, der die
  bestehende `ma_analyse`-GUI als getrennten Legacy-Prozess startet:
  `python -m ma_analyse gui`.
- Die Seite `Analyse` startet standardmaessig mit `plot-template` und bietet
  Template-Auswahl, passende Zeitfelder, Raumlogik, Overlays und Bildvorschau.
- Die bestehende Tkinter-GUI von `ma_analyse` bleibt separat bestehen.
- Wenn Streamlit nach Codeaenderungen alte Importfehler zeigt, den laufenden
  Streamlit-Prozess stoppen und mit dem empfohlenen venv-Befehl neu starten.
