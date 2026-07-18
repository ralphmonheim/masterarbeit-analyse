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
`ma_ui.tkinter_app.module_views.analyse` verschoben. `ma_analyse` fuehrt
keinen Tkinter-Kompatibilitaetspfad mehr.

## Naechster Schritt

Analyse-UI real testen, Vorschau-Cache planen und weitere echte
Workflow-Service-Aufrufe getrennt anbinden.

## Rolle

- `ma_ui` zeigt Navigation, Modul-Uebersicht und spaeter echte Workflow-Ansichten.
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
- Startseite mit `Modul-Ansicht` fuer Phase 0 bis Phase 6,
  Statuskennzahlen, Phasenkarten, Navigationsbuttons, Iterationspfaden und optionalen
  technischen Detailtabellen ist vorbereitet. Die Workflow-Ansicht ist eine
  eigene Startansicht unter `ma_workflow`; normale Modulansichten wechseln
  nicht in einen globalen Workflow-Modus.
- Das Workflow-Referenzdiagramm liegt unter
  `src/ma_ui/assets/workflow/masterarbeit_workflow.png`; die PDF-Referenz liegt
  daneben unter `src/ma_ui/assets/workflow/masterarbeit_workflow.pdf`. Beide
  werden nur in der `ma_workflow`-Workflowansicht eingebunden; die Startseite
  bleibt als leichte Modul-Uebersicht ohne Referenzdiagramm.
- Workflow-Karten, Statuskennzahlen, Navigation und Detailtabellen verwenden
  die zentral gepflegten Modulumsetzungsstaende aus `ma_workflow`.
- Die Kopfzeile kann eine vorhandene Fachansicht mit `Infokarte` durch die
  zentrale Modulbeschreibung ersetzen und mit `Modulansicht` wieder
  herstellen. Auf den beiden Startansichten nutzt dieselbe rechte
  Aktionsspalte den Wechsel `Workflow` bzw. `Bearbeitung`. Ein Seitenwechsel
  beendet den Infokartenmodus und springt beim neuen Rendern wieder an den
  Seitenanfang. Die zentrale Infokarte erlaeutert den V1-Rahmen mit `Was`,
  `Wie`, `Warum` und `Wann` aus dem kanonischen `ma_workflow`-Modulkatalog;
  der Status ist kein Nachweis einer ausfuehrbaren Demo.
- Jede V1-Infokarte erlaeutert zentrale Begriffe. Allgemeine Begriffe wie
  V1-Rahmen, Freigabestatus, Annahme und Demo-/Uebergangsstand gelten fuer
  alle Module; fachliche Begriffe werden zentral je Modul ergaenzt. Fuer
  Gebaeude sind dies insbesondere alle BIL-Reifegrade und LoD-Eingabestufen.
- Die Modul-Uebersicht gehoert ausschliesslich auf die Startseite. Modulviews
  zeigen nur eigene Inhalte oder bei geplantem Stand eine blaue Hinweisbox.
- Analyse-Seite ruft die UI-neutrale `ma_analyse`-Service-Fassade ueber
  `ma_workflow` auf.
- `ma_building`, `ma_technical` und `ma_zones` sind als echte
  Streamlit-Modulansichten registriert. `ma_zones` und `ma_technical` zeigen
  die BusinessIntegration-LoD-1-Demos mit Freigabestatus statt nur
  Infokarten; P013-S2 ordnet `ma_technical` fachlich vor `ma_zones` ein.
  `ma_technical` trennt `Technikmodell | Technik-Katalog`; die sechs
  Katalogthemen bleiben unter dem Katalogreiter, waehrend Einordnung und
  V1-Rahmen nur in der zentralen Infokarte stehen.
- `ma_parameters` zeigt den BusinessIntegration-LoD-1-`ParameterSnapshot` v1,
  das P015-S3a-`ParameterInputPackage` mit Wetter-Default-Status und den
  daraus beziehungsweise aus v1 abgeleiteten `BaselineParameterSnapshot` v2
  mit Freigabestatus, Scopes, Parameterwerten, Quellen, Referenzen und
  Validierungsmeldungen.
- `ma_analyse.stage_1_dimensioning` zeigt die LoD-1-Referenzdimensionierung
  mit Ergebniswerten, Rechenweg und Hinweisen.
- Analyse-Seite kann die Tkinter-Analyse als separates Fenster starten, falls
  eine Bedienfunktion in Streamlit noch fehlt.
- Analyse-Seite nutzt eine sichtbare Schrittstruktur:
  `Befehl`, `Unterbefehl`, `Template / Diagramm`, optional `Overlay`,
  `Varianten`, `Raeume`, `Export / Ausgabe` und einen festen Aktionsbereich.
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
- Plot-Template-Overlays werden direkt nach der Templatewahl bedient. Der
  Katalog wird erst befuellt, sobald Variante und Raum verfuegbar sind.
  Freie Overlay-Linien koennen vorher und nachher ueber Eingabefelder
  hinzugefuegt und entfernt werden; ein Expertenmodus im Format
  `source,column,label,axis` bleibt als Fallback moeglich.
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
- Wetter-Seite trennt `Analyse | Verwaltung`: Analyse zeigt Standort- und
  Wetterauswahl sowie Ergebnisse; Verwaltung zeigt die lokalen
  TRY-Datensaetze aus dem `ma_weather`-Katalog inklusive Dateistatus,
  Import, Scan und Pruefung.
- Die Wetterkarte auf der Startseite zeigt den Modulstatus `Verfuegbar` und
  zusaetzlich `Diagramme – Teilweise` in der bestehenden amberfarbenen
  Statusdarstellung.
- Projekt bleibt auf der registrierten P028-Fachansicht fuer
  Simulationsprogramme und Varianten-Benennung; ein Cache oder Routerwechsel
  ist nicht die Ursache einer vermeintlich alten Projektansicht.
- Projekt ergaenzt diese Konfigurationsreiter um die lesende
  `Projektübersicht`. Sie verbindet synthetische P011-Stammdaten mit dem
  aktuellen Sitzungsstand, ohne Projektstammdaten zu speichern.
- Technik trennt `Technikmodell | Übersicht | Auswahl`. Katalog- und
  `Nicht vorhanden`-Angaben bleiben ein synthetischer Sitzungsentwurf und
  werden nur mit `Technikauswahl speichern` uebernommen.
- Zonen trennt `Übersicht | Nutzungsprofile zuweisen`. Die Übersicht zeigt
  gespeicherte Zuordnungen; erweiterte Demo-Profile sind ausschliesslich
  synthetische Annahmen und werden nur nach explizitem Speichern uebernommen.
- Gebaeude zeigt im Reiter `Übersicht` getrennte Tabellen fuer
  Gebaeudestammdaten einschliesslich LoD und Reifegrad sowie fuer zentrale
  Flaechen- und Volumenkennwerte. Die Ansicht bleibt pruefend und veraendert
  keine Gebaeudespezifikation.
- Gebaeude gliedert die weiteren Ansichten in `Bauteile` und
  `Konstruktionen`: Die Bauteilübersicht und die Typ-Reiter zeigen erkannte
  Bauteile einschliesslich Fenster und Tueren mit ID, Typ, Code und
  Konstruktion. Konstruktionen und `Surfaces` werden zusammen dargestellt;
  Materialien und Produkte besitzen eigene Unterreiter. Die lokalen
  Referenzkataloge bleiben read-only, ignoriert und ohne automatische
  Modellzuordnung. `Modellquellen` ist in V1 ausgeblendet.
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
