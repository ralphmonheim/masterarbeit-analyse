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

- Das uebergreifende Befehls- und Ausgabeninventar steht unter
  `docs/project/COMMAND_OUTPUT_INVENTORY.md`.
- `ma_ui` besitzt eine nutzbare Streamlit-Oberflaeche mit Modul-Ansicht,
  Kopfzeilen-Navigation, vorbereiteten Modulansichten und einem umfangreichen
  Analyse-Wizard. Geplante Fachmodule bleiben als klar gekennzeichnete,
  klickbare Modul-Infoseiten sichtbar.
- `src/ma_ui/app.py` bleibt der stabile Streamlit-Einstieg. Die eigentliche
  Streamlit-Logik liegt unter `ma_ui.streamlit_app`.
- Tkinter liegt als eigener UI-Zweig unter `ma_ui.tkinter_app`. `ma_analyse`
  enthaelt keinen Tkinter-Kompatibilitaetspfad mehr.
- Die technische Streamlit-Multipage-Navigation ist ueber
  `.streamlit/config.toml` ausgeblendet. Sichtbar bleiben soll nur die
  fachliche Projektnavigation.
- Die zentrale Navigation liegt oben im Fenster und bietet `Start`, `Zurueck`
  und `Weiter`. Die rechte Aktionsspalte wechselt nur auf den beiden
  Startansichten zwischen `Workflow` und `Bearbeitung`. Auf normalen
  Modulansichten bleibt dort `Infokarte` bzw. `Modulansicht`. Bei Modulen ohne
  eigene Fachansicht ist die Infokarte bereits die Hauptansicht. Seitenwechsel
  ueber die zentrale Navigation und Modul-Links springen beim neuen Rendern
  wieder an den Seitenanfang.
- `Projekt`, `Parameter` und `Varianten` besitzen P028-Fachansichten mit
  gemeinsamem Sitzungsstand. Fachliche Querverweise merken die Ausgangsseite;
  die normale Kopfzeilen-Navigation verwirft diesen Ruecksprungkontext.
- Lokale Arbeitsdateien werden erst durch `Als neue Datei speichern` oder ein
  bestaetigtes Ueberschreiben angelegt. Versionierte Vorlagen bleiben
  unveraendert.
- Die Codex-Routine `tagesstart` startet diese Oberflaeche nicht automatisch.
  Zum Oeffnen den oben genannten venv-basierten Streamlit-Befehl nutzen.
- Die Startseite zeigt eine Modul-Ansicht mit Phasen,
  Statuskarten, Iterationspfaden und Buttons zu allen katalogisierten
  Modulansichten. Dargestellt werden Phase 0 bis Phase 6 sowie ein eigener
  phasenuebergreifender Bereich.
- Das Workflow-Referenzdiagramm liegt unter
  `src/ma_ui/assets/workflow/masterarbeit_workflow.png`; die PDF-Fassung liegt
  daneben als `masterarbeit_workflow.pdf`. Beide werden nur in der
  `ma_workflow`-Workflowansicht referenziert; die Startseite bleibt ohne
  Referenzdiagramm.
- Phase 4 trennt `Optimierung`, `Norm-Nachweis` und `Sensitivitaet`.
- Die Modul-Ansicht bleibt auf der Startseite sichtbar. Die Workflow-Ansicht
  ist eine eigene Startansicht unter `ma_workflow`; normale Modulansichten
  wechseln nicht in einen globalen Workflow-Modus.
- Technische Workflow-Tabellen bleiben auf der Startseite unter
  `Technische Detailtabellen` eingeklappt und werden nicht in jeder
  Modulansicht angezeigt.
- Geplante Modulbereiche ohne eigene Fachlogik zeigen eine neutrale Infoseite
  mit Modulrolle, Grenzen, Status und naechstem Schritt.
- Die Infokarte verwendet ausschliesslich den zentralen Modulkatalog und laedt
  keine README-Dateien dynamisch.
- Fachlogik wird nicht in der UI berechnet.
- Analyseaufrufe laufen ueber `ma_workflow` und die Service-Fassade von
  `ma_analyse`.
- Die getrennte Tkinter-Analyse baut ihren Analyseauftrag ebenfalls als
  `AnalysisConfig` und startet ihn ueber `ma_workflow`; sie bleibt trotzdem ein
  eigener Prozess und wird nicht in Streamlit eingebettet.
- Die Analyse-Seite enthaelt einen Button `Tkinter-Analyse oeffnen`, der die
  Tkinter-Analyse als getrennten Prozess startet:
  `python -m ma_ui.tkinter_app.module_views.analyse`.
- Die Tkinter-Analyse startet im ersten Befehlsschritt standardmaessig mit
  `plot-template`, damit Analyse-Template-Ausgaben direkt sichtbar sind.
- Die Seite `Analyse` ist als sichtbare Schrittstruktur aufgebaut:
  `Befehl`, `Unterbefehl`, `Template / Diagramm`, optional `Overlay`,
  `Varianten`, `Raeume`, `Export / Ausgabe` und einen festen Aktionsbereich.
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
  Run-ID liegen in Streamlit im eingeklappten Bereich `Erweiterte Pfade`
  innerhalb von `Export / Ausgabe`.
- `plot-template-analyse` nutzt den Ablauf `Befehl -> Unterbefehl ->
  Template / Diagramm -> optional Overlay -> Varianten -> Raeume ->
  Export / Ausgabe -> Aktionsbereich`.
- `plot-template-analyse` zeigt alle vorhandenen Diagramme direkt im Bereich
  `Unterbefehl`; eine vorgelagerte Einteilung in Diagrammgruppen gibt es in der
  Template-Sandbox nicht mehr.
- `Template / Diagramm` enthaelt Zeitwahl, Overlay-Aktivierung und den
  ausklappbaren Bereich `Diagrammanpassung`. Dort koennen primaere und
  sekundaere Y-Achsen automatisch oder manuell skaliert werden. Ein Mock-up
  zeigt die Wirkung der Achsengrenzen mit Beispieldaten.
- Der optionale Bereich `Overlay` erscheint direkt nach `Template / Diagramm`,
  wenn das gewaehlte Template Overlays unterstuetzt und die Checkbox aktiviert
  ist. Der Overlay-Katalog wird erst befuellt, sobald Variante und Raum
  verfuegbar sind; manuelle Overlay-Spalten bleiben vorher moeglich.
- Der Aktionsbereich mit `Vorschau aktualisieren` und `Analyse starten` ist
  nicht einklappbar.
- Die Tkinter-Analyse besitzt ebenfalls einen Button
  `Vorschau aktualisieren` zwischen `Zuruecksetzen` und `Start`; er nutzt
  aktuell den normalen `AnalysisConfig`-/`ma_workflow`-Analysepfad mit den
  aktuellen Einstellungen.
- Plot-Template-Overlays werden direkt nach der Templatewahl bedient. Der
  Katalog nutzt weiterhin die erste gewaehlte Variante und den ersten
  gewaehlten Raum, weil die verfuegbaren CSV-/AUX-Spalten aus konkreten
  Ergebnisdateien gelesen werden.
- Als Katalogreferenz dienen die erste gewaehlte Variante und der erste
  gewaehlte Raum. Die Referenz wird sichtbar angezeigt; weitere ausgewaehlte
  Kombinationen werden beim Analysestart validiert.
- Bei Plot-Templates bedeutet `single`: eine eigene Diagrammdatei je
  Variante-Raum-Kombination. `compare` erzeugt eine gemeinsame
  Vergleichsausgabe. Zeitreihen werden gemeinsam auf einer Achse dargestellt;
  komplexe Sammeltemplates werden als beschriftete Teilplots in einer
  Vergleichsgrafik zusammengefuehrt.
- Die Seite `Wetterdaten` erlaubt die Auswahl eines aktiven `weather_key`,
  eines Wetterdiagramms oder `Alle Wetterdiagramme`, startet die lokale
  `ma_weather`-Analyse ueber `plot-template-weather` und zeigt erzeugte
  Wetterdiagramme direkt in Streamlit an. Die Analysebedienung steht oben; die Uebersicht der
  Wetterdatensaetze steht darunter. Im Bereich `Wetterdatensaetze` steht zuerst
  eine Aktionszeile mit den Schritten `Import`, `Scannen` und `Validieren`.
  Import legt TRY-Dateien nur lokal ab, Scannen erzeugt Entwuerfe, Validieren
  erlaubt Anpassung und Registrierung; danach folgen nebeneinander getrennte
  Uebersichten fuer aktive und offene Wetterdatensaetze.
- Wetterdiagnosen zeigen ID, Code, Problem und Fundstelle. Fehler blockieren
  die Freigabe; Warnungen verlangen eine bewusste laufgebundene Entscheidung.
  Lauf und Entscheidung werden unter `logs/sessions/` protokolliert.
- Die Tkinter-Analyse bleibt separat von Streamlit und liegt unter
  `ma_ui.tkinter_app.module_views.analyse`.
- Die Tkinter-Analyse ist intern in kleine Module fuer Start, Initialisierung,
  Layout, Schrittfluss, Auswahl, Plot-Templates und Pipeline-Runner zerlegt;
  `app.py` bleibt der stabile Import- und Startpunkt.
- Wenn Streamlit nach Codeaenderungen alte Importfehler zeigt, den laufenden
  Streamlit-Prozess stoppen und mit dem empfohlenen venv-Befehl neu starten.
- Wenn alte Modul-/Workflow-Darstellungen auf Modulviews sichtbar bleiben, ebenfalls
  Streamlit neu starten.
- Wenn nach einem Update weiterhin Streamlit-Warnungen aus einem alten Prozess
  erscheinen, den laufenden Prozess stoppen und mit dem venv-Befehl neu starten.
