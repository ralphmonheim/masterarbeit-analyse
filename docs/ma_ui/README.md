# ma_ui

`ma_ui` ist die vorbereitete zentrale lokale Streamlit-Oberflaeche fuer das
Masterarbeitsprojekt.

## Rolle

- `ma_ui` zeigt Navigation, Workflow-Uebersicht und spaeter Modulansichten.
- `ma_ui` enthaelt keine fachliche Berechnungslogik.
- Fachlogik bleibt in `ma_analyse`, `ma_variants`, `ma_weather` und spaeteren
  Fachmodulen.
- Moduluebergreifende Aufrufe laufen ueber `ma_workflow`.

## Aktueller Stand

- Die App nutzt jetzt `module_views/` als Ziel-Einstieg fuer Modulansichten.
- `shared/` enthaelt erste allgemeine Anzeigehelfer fuer Tabellen, Status,
  Logs, Layout, Pfade und Plotdateien.
- `pages/` bleibt vorerst als Kompatibilitaets- und Zwischenstand erhalten.
- Die automatische Streamlit-Multipage-Navigation ist in
  `.streamlit/config.toml` ausgeblendet, damit nur die fachliche
  Projektnavigation unter `Bereich` sichtbar ist.
- Startseite mit grafischem Workflow-Dashboard, Statuskennzahlen,
  Phasenkarten, Navigationsbuttons, Iterationspfaden und optionalen
  technischen Detailtabellen ist vorbereitet.
- Workflow-Karten, Statuskennzahlen, Navigation und Detailtabellen verwenden
  die zentral gepflegten Modulumsetzungsstaende aus `ma_workflow`.
- Der grafische Workflow gehoert ausschliesslich auf die Startseite. Modulviews
  zeigen nur eigene Inhalte oder bei geplantem Stand eine blaue Hinweisbox.
- Analyse-Seite ruft die UI-neutrale `ma_analyse`-Service-Fassade ueber
  `ma_workflow` auf.
- Analyse-Seite kann die bestehende Tkinter-Analyse als separates
  Legacy-Fenster starten, falls eine Bedienfunktion in Streamlit noch fehlt.
- Analyse-Seite nutzt eine sichtbare Schrittstruktur:
  `Befehl`, `Unterbefehl`, `Template / Diagramm`, `Varianten`, `Raeume`,
  optional `Overlay`, `Export / Ausgabe` und einen festen Aktionsbereich.
- Nicht relevante Analyse-Bereiche zeigen nur einen kurzen Hinweis. Technische
  Pfade liegen unter `Export / Ausgabe` im eingeklappten Bereich
  `Erweiterte Pfade`.
- Analyse-Seite bildet die fachlichen Einstellungen aus dem bisherigen
  `ma_analyse`-Ablauf dort ab, wo sie gebraucht werden: Prepare und
  `analyze_data` unter `Export / Ausgabe`, Heating/Cooling mit
  `single`/`compare` unter `Export / Ausgabe` und Diagrammdetails unter
  `Template / Diagramm`.
- Comfort hat keine separate Analyseebene mehr. Der Unterbefehl
  `t_op / rel_hum` fuehrt die vier bisherigen Comfort-Ausgaben im Bereich
  `Template / Diagramm`.
- Variantenumfang wird im Bereich `Varianten` abgebildet: Bei `Alle Varianten`
  uebergibt die UI `variants=None` an die Service-Fassade.
- Raumumfang wird im Bereich `Raeume` abgebildet: `Ein Raum`,
  `Mehrere Raeume` oder `Alle Raeume`.
- Varianten und Raeume werden aus `ma_analyse`-Services gelesen, falls lokale
  Daten vorhanden sind. Manuelle Texteingabe bleibt als Fallback bestehen.
- Plot-Template-Overlays koennen aus einem einfachen Katalog der ersten
  gewaehlten Variante und des ersten Raums ausgewaehlt werden. Freie
  Overlay-Linien koennen ueber Eingabefelder hinzugefuegt und entfernt werden;
  ein Expertenmodus im Format `source,column,label,axis` bleibt als Fallback
  moeglich.
- Plot-Template-Zeitfelder, Single-/Multi-Room-Auswahl und Overlay-Defaults
  werden aus der bestehenden `ma_analyse`-Template-Spezifikation abgeleitet.
- Alle Plot-Templates werden ohne vorgelagerte Diagrammgruppe direkt als
  Unterbefehle angeboten.
- Die Diagrammanpassung bietet automatische Achsengrenzen als Standard und
  optionale manuelle Grenzen fuer primaere und sekundaere Y-Achsen. Ein
  Beispieldiagramm dient als direktes Mock-up.
- `single` erzeugt getrennte Diagramme je Variante-Raum-Kombination;
  `compare` erzeugt eine gemeinsame Vergleichsausgabe.
- Analyse-Ergebnisse zeigen Status, Fehler, Hinweise, erzeugte Dateien,
  Diagrammvorschau fuer Bilddateien und Log.
- Varianten-Seite zeigt Parameter, Optionen, Variantenraum, Auswahlmethoden und
  vorhandene Exportdateien ueber bestehende `ma_variants`-Services.
- Wetter-Seite zeigt zuerst die Analysebedienung fuer einen aktiven
  Wetterdatensatz und darunter die lokalen TRY-Datensaetze aus dem
  `ma_weather`-Katalog inklusive Dateistatus.
- Bewertungsseite zeigt generische Systemkosten, Energiepreise und Szenarien aus
  den vorhandenen Beispielannahmen. Variantenbezogene Kostenberechnung wird dort
  noch nicht gestartet.
- Geplante Zielseiten fuer Parameter, Gebaeude, Simulation-Setup, IDA-Export,
  IDA-Import und Feedback sind als Platzhalter erreichbar. Solange dort keine
  eigene Fach- oder Kataloglogik umgesetzt ist, zeigen sie nur Titel, Untertitel
  und eine blaue Hinweisbox.
- Allgemeine Workflow- und Dashboard-Tabellen werden nicht in jeder
  Modulansicht angezeigt. Sie bleiben nur als eingeklappte technische
  Detailtabellen auf der Startseite erreichbar.

## Start

Empfohlen:

```powershell
.\.venv\Scripts\python.exe -m streamlit run src\ma_ui\app.py
```

Alternativ:

```powershell
.\.venv\Scripts\streamlit.exe run src\ma_ui\app.py
```

Wenn Streamlit nach Codeaenderungen alte Importfehler zeigt, den laufenden
Streamlit-Prozess stoppen und mit dem empfohlenen venv-Befehl neu starten.
Das gilt auch, wenn alte Workflow- oder Navigationsinhalte weiterhin sichtbar
sind.
