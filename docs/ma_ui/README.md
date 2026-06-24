# ma_ui

`ma_ui` ist der gemeinsame lokale UI-Bereich fuer das Masterarbeitsprojekt.
Streamlit bleibt der aktuelle Haupteinstieg; Tkinter liegt als zweiter,
technisch getrennter UI-Zweig daneben.

## Zweck

Den Gesamtworkflow, Fachansichten und Modulinformationen in lokalen
Oberflaechen zugaenglich machen, ohne Fachlogik in die UI zu verschieben.

## Eingaben

- zentrale Phasen-, Modul- und Statusmetadaten aus `ma_workflow`
- UI-neutrale Ergebnisse und Services der Fachmodule

## Ausgaben

- Streamlit-Dashboard, Navigation, Fachansichten und Modul-Infoseiten
- Tkinter-Fenster fuer Analyse und spaetere fachliche Zusatzansichten

## Abgrenzung

- keine fachliche Berechnungslogik
- keine direkte Vermischung von Streamlit und Tkinter

## Abhaengigkeiten

- `ma_workflow`
- angebundene Fachservices

## Status

Geplant. Ein nutzbarer Streamlit-Prototyp mit Dashboard, Navigation und
mehreren Fachansichten ist vorhanden. Die bestehende Tkinter-Analyse ist nach
`ma_ui.tkinter_app.module_views.analyse` verschoben und ueber
`ma_analyse.gui` weiterhin kompatibel erreichbar.

## Naechster Schritt

Analyse-UI real testen, Vorschau-Cache planen und weitere echte
Workflow-Service-Aufrufe getrennt anbinden.

## Rolle

- `ma_ui` zeigt Navigation, Workflow-Uebersicht und spaeter Modulansichten.
- `ma_ui.streamlit_app` enthaelt die Streamlit-Oberflaeche.
- `ma_ui.tkinter_app` enthaelt getrennte Tkinter-Ansichten.
- `ma_ui` enthaelt keine fachliche Berechnungslogik.
- Fachlogik bleibt in `ma_analyse`, `ma_variants`, `ma_weather` und spaeteren
  Fachmodulen.
- Moduluebergreifende Aufrufe laufen ueber `ma_workflow`.

## Aktueller Stand

- Die Streamlit-App nutzt `streamlit_app/module_views/` als Ziel-Einstieg fuer
  Modulansichten. `src/ma_ui/app.py` bleibt der stabile Startpunkt und
  delegiert dorthin.
- `streamlit_app/shared/` enthaelt erste allgemeine Anzeigehelfer fuer Tabellen, Status,
  Logs, Layout, Pfade und Plotdateien.
- `streamlit_app/pages/` bleibt fuer bestehende Seiten erhalten.
- Kompatibilitaetswrapper unter `ma_ui.pages`, `ma_ui.module_views`,
  `ma_ui.shared`, `ma_ui.state` und `ma_ui.components` halten alte
  Importpfade vorerst lauffaehig.
- Die automatische Streamlit-Multipage-Navigation ist in
  `.streamlit/config.toml` ausgeblendet, damit nur die fachliche
  Projektnavigation unter `Bereich` sichtbar ist.
- Startseite mit grafischem Workflow-Dashboard fuer Phase 0 bis Phase 6,
  Statuskennzahlen, Phasenkarten, Navigationsbuttons, Iterationspfaden und optionalen
  technischen Detailtabellen ist vorbereitet.
- Workflow-Karten, Statuskennzahlen, Navigation und Detailtabellen verwenden
  die zentral gepflegten Modulumsetzungsstaende aus `ma_workflow`.
- Die Kopfzeile kann eine vorhandene Fachansicht mit `Infokarte` durch die
  zentrale Modulbeschreibung ersetzen und mit `Modulansicht` wieder
  herstellen. Ein Seitenwechsel beendet diesen Modus.
- Der grafische Workflow gehoert ausschliesslich auf die Startseite. Modulviews
  zeigen nur eigene Inhalte oder bei geplantem Stand eine blaue Hinweisbox.
- Analyse-Seite ruft die UI-neutrale `ma_analyse`-Service-Fassade ueber
  `ma_workflow` auf.
- Analyse-Seite kann die Tkinter-Analyse als separates Fenster starten, falls
  eine Bedienfunktion in Streamlit noch fehlt.
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
- Projekt-, Parameter- und Varianten-Seite teilen einen Sitzungsstand.
  Projekt verwaltet Simulationsprogramme und neutrales Naming, Parameter die
  aktive Demo-Optionsauswahl, Varianten den daraus erzeugten und benannten
  Variantenraum.
- Gezielte Querverweise zwischen diesen Seiten merken die Ausgangsseite. Ein
  normaler Wechsel ueber Start, Zurueck oder Weiter beendet den Ruecksprung.
- Eigene Programmlisten, Naming-Profile und Optionsauswahlen werden nur nach
  Nutzeraktion lokal gespeichert; Vorlagen und kollidierende neue Dateinamen
  sind technisch geschuetzt.
- Wetter-Seite zeigt zuerst die Analysebedienung fuer einen aktiven
  Wetterdatensatz und darunter die lokalen TRY-Datensaetze aus dem
  `ma_weather`-Katalog inklusive Dateistatus.
- Wetter-Seite rendert die informative Klimaregionenkarte aus
  `src/ma_ui/assets/weather/klimaregionen_deutschland.png`; alternativ werden
  `.jpg` und `.jpeg` mit demselben Basisnamen erkannt.
- Wetter-Seite kann den lokalen Wetterbestand pruefen, offene Datensaetze
  separat anzeigen und freigegebene Datensaetze bewusst aktivieren oder als
  Projekt-Default setzen.
- Wetter-Seite fuehrt Import und Bestands-/Validierungspruefung gemeinsam im
  unteren Bereich `Wetterdatensaetze`; aktive und offene Datensaetze stehen
  dort als getrennte Uebersichten nebeneinander.
- Wetter-Seite zeigt nach der Analyse kritische Wetterereignisse fuer den
  aktuell ausgewaehlten Jahr-, Sommer- oder Winterdatensatz.
- Wetter-Seite zeigt Quellenmetadaten, strukturierte Diagnosen und den
  Freigabestatus. Warnungen koennen laufgebunden blockiert oder bestaetigt
  werden; die Entscheidung wird im Sitzungslog dokumentiert.
- Bewertungsseite zeigt generische Systemkosten, Energiepreise und Szenarien aus
  den vorhandenen Beispielannahmen. Variantenbezogene Kostenberechnung wird dort
  noch nicht gestartet.
- Jedes katalogisierte Modul ist klickbar. Module ohne eigene Fachansicht
  zeigen eine generische Infoseite mit Zweck, Ein- und Ausgaben, Abgrenzung,
  Abhaengigkeiten, Status und naechstem Schritt.
- `ma_validation` und `ma_feedback` werden in einem eigenen
  phasenuebergreifenden Dashboard-Bereich angezeigt.
- Phase 4 zeigt Optimierung, Norm-Nachweis und Sensitivitaet als getrennte
  Karten. Die vorhandene Analyseansicht bleibt Einstieg fuer Stage 2.
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
