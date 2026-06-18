# Befehle ma_ui

## Sammelbefehle

### Zentrale Streamlit-Oberflaeche starten

Empfohlen ist der Modulaufruf ueber die Projekt-venv:

```powershell
.\.venv\Scripts\python.exe -m streamlit run src\ma_ui\app.py
```

Dieser Befehl startet die zentrale Projektoberflaeche mit Startseite,
Kopfzeilen-Navigation und Modulansichten.

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
  fachliche Projektnavigation.
- Die zentrale Navigation liegt oben im Fenster und bietet `Start`, `Zurueck`
  und `Weiter`. Die alte Sidebar-Auswahl ist nicht mehr die Hauptnavigation.
- Die Codex-Routine `tagesstart` startet diese Oberflaeche nicht automatisch.
  Zum Oeffnen den oben genannten venv-basierten Streamlit-Befehl nutzen.
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
- Die Seite `Analyse` ist als sichtbare Schrittstruktur aufgebaut:
  `Befehl`, `Unterbefehl`, `Export / Ausgabe`, `Template / Diagramm`,
  `Varianten`, `Raeume` und einen festen Aktionsbereich.
- Hauptschritte werden nicht wie `Erweiterte Pfade` eingeklappt, sondern als
  klare Auswahlbereiche angezeigt. Nicht relevante Bereiche zeigen nur einen
  kurzen Hinweis.
- `prepare` nutzt `Export / Ausgabe` mit `csv`, `excel` oder `both` und danach
  `Varianten`; Raeume sind nicht relevant.
- `analyze_data` nutzt `Export / Ausgabe` fuer `separate` oder `combined`, danach
  `Varianten` und `Raeume`.
- Bei `comfort` gibt es keine separate Analyseebene mehr. Der Unterbefehl
  `t_op / rel_hum` fuehrt die vier bisherigen Comfort-Ausgaben im Bereich
  `Template / Diagramm`.
- Bei `heating` und `cooling` liegen `single`/`compare` unter
  `Export / Ausgabe`; Zeitansicht, Overlay und Diagrammanpassung liegen im
  Bereich `Template / Diagramm`.
- Technische Pfade wie IDA-Importordner, Datenbankordner, Ausgabeordner und
  Run-ID liegen unter `Erweiterte Pfade`.
- `plot-template-analyse` nutzt den Ablauf `Befehl -> Unterbefehl ->
  Export / Ausgabe -> Template / Diagramm -> Varianten -> Raeume ->
  Aktionsbereich`.
- `plot-template-analyse` fuehrt die Diagrammgruppe im Bereich
  `Unterbefehl`, `single`/`compare` unter `Export / Ausgabe` und Zeitansicht,
  gefilterte Template-Auswahl, Overlay-Aktivierung sowie Diagrammbearbeitung im
  Bereich `Template / Diagramm`.
- Der Aktionsbereich mit `Vorschau aktualisieren` und `Analyse starten` ist
  nicht einklappbar.
- Die Tkinter-Legacy-GUI besitzt ebenfalls einen Button
  `Vorschau aktualisieren` zwischen `Zuruecksetzen` und `Start`; er nutzt
  aktuell den bestehenden Analysepfad mit den aktuellen Einstellungen.
- Plot-Template-Overlays erscheinen erst nach Varianten- und Raumauswahl, damit
  der Overlay-Katalog gezielt aus lokalen CSV-/AUX-Daten gelesen wird.
- Die Seite `Wetterdaten` erlaubt die Auswahl eines aktiven `weather_key`,
  startet die lokale `ma_weather`-Analyse und zeigt erzeugte Wetterdiagramme
  direkt in Streamlit an. Die Analysebedienung steht oben; die Uebersicht der
  Wetterdatensaetze steht darunter.
- Die bestehende Tkinter-GUI von `ma_analyse` bleibt separat bestehen.
- Wenn Streamlit nach Codeaenderungen alte Importfehler zeigt, den laufenden
  Streamlit-Prozess stoppen und mit dem empfohlenen venv-Befehl neu starten.
- Wenn alte Workflow-Darstellungen auf Modulviews sichtbar bleiben, ebenfalls
  Streamlit neu starten.
- Wenn nach einem Update weiterhin Streamlit-Warnungen aus einem alten Prozess
  erscheinen, den laufenden Prozess stoppen und mit dem venv-Befehl neu starten.
