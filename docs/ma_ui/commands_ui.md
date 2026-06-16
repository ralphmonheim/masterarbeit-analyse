# Befehle ma_ui

## Sammelbefehle

### Zentrale Streamlit-Oberflaeche starten

Empfohlen ist der Modulaufruf ueber die Projekt-venv:

```powershell
.\.venv\Scripts\python.exe -m streamlit run src\ma_ui\app.py
```

Dieser Befehl startet die zentrale Projektoberflaeche mit Startseite,
Navigation und Modulansichten.

## Einzelbefehle

### Alternativer Streamlit-Start

Alternative:

```powershell
.\.venv\Scripts\streamlit.exe run src\ma_ui\app.py
```

## Referenz und Hinweise

- `ma_ui` ist aktuell eine minimale Shell mit Zielstruktur fuer
  `module_views/` und `shared/`.
- Die technische Streamlit-Multipage-Navigation ist ueber
  `.streamlit/config.toml` ausgeblendet. Sichtbar bleiben soll nur die
  fachliche Projektnavigation unter `Bereich`.
- Die Codex-Routine `tagesstart` darf diese Oberflaeche automatisch ueber die
  Projekt-venv auf Port `8501` starten, wenn sie noch nicht laeuft.
- Die Startseite zeigt ein grafisches Workflow-Dashboard mit Phasen,
  Statuskarten, Iterationspfaden und Buttons zu den vorhandenen Modulansichten.
- Der grafische Workflow soll nur auf der Startseite sichtbar sein.
- Technische Workflow-Tabellen bleiben auf der Startseite unter
  `Technische Detailtabellen` eingeklappt und werden nicht in jeder
  Modulansicht angezeigt.
- Geplante Modulbereiche ohne eigene Fachlogik zeigen nur Titel, Untertitel
  und eine blaue Hinweisbox.
- Fachlogik wird nicht in der UI berechnet.
- Analyseaufrufe laufen ueber `ma_workflow` und die Service-Fassade von
  `ma_analyse`.
- Die Analyse-Seite enthaelt einen Button `Tkinter-Analyse oeffnen`, der die
  bestehende `ma_analyse`-GUI als getrennten Legacy-Prozess startet:
  `python -m ma_analyse gui`.
- Die Seite `Analyse` startet mit der Befehlsauswahl und blendet danach nur die
  fachlich passenden Folgeschritte ein. Diese Logik orientiert sich an den
  Zustandsaenderungen der bestehenden Tkinter-GUI.
- Technische Pfade wie IDA-Importordner, Datenbankordner, Ausgabeordner und
  Run-ID liegen unter `Erweiterte Pfade`.
- `plot-template` bietet Template-Auswahl, passende Zeitfelder, Raumlogik,
  Overlays und Bildvorschau, sobald dieser Befehl im Wizard gewaehlt wurde.
- Die bestehende Tkinter-GUI von `ma_analyse` bleibt separat bestehen.
- Wenn Streamlit nach Codeaenderungen alte Importfehler zeigt, den laufenden
  Streamlit-Prozess stoppen und mit dem empfohlenen venv-Befehl neu starten.
- Wenn alte Workflow-Darstellungen auf Modulviews sichtbar bleiben, ebenfalls
  Streamlit neu starten.
