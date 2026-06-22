# Plan Status

Stand: 2026-06-22

Diese Datei ist die aktive Planungsuebersicht. Sie wird nach Modulen gefuehrt und nach jeder Planumsetzung aktualisiert. Vollstaendige alte Planstaende liegen unter `docs/project/archive/plans/`.

## Projektorganisation

### Abgeschlossen

- P003 Projektstruktur, Planungsbereich und Nutzerentscheidungen: modulare Dokumentationsstruktur, Planindex, Strukturreview, Cleanup-Plan, Implementierungshinweise und getrennter Bereich fuer Nutzerentscheidungen wurden vorbereitet. Betroffen: `docs/project/`, `docs/ma_analyse/`, `docs/ma_variants/`, `docs/ma_weather/`, `docs/common/`.
- `docs/project/archive/plans/250604_Plan_Projektstruktur_Review_Planungsbereich_Nutzerentscheidungen.md` ist nach Umsetzung archiviert.
- `docs/project/archive/plans/250603_Plan_Variantenmodul_GUI_Logikpruefung.md` ist nach Abschluss von P001 archiviert.
- `docs/project/archive/plans/PLAN_Projektplan_Version_1_0_0.md` ist ein abgelegter Plan und nicht mehr die aktive Steuerdatei.
- `data/test_output/` bleibt ein lokaler, semi-wichtiger Arbeits- und Smoke-Test-Ordner. Der Nutzer leert ihn regelmaessig manuell.
- `docs/examples/plot_templates/` bleibt die belastbare Referenzgalerie fuer aktuelle `ma_analyse`-Plot-Template-Beispiele.
- Der leere, nicht versionierte Ordner `scripts/` wurde entfernt.
- `docs/project/UPDATE_ROUTINES.md` dokumentiert die festen Codex-Routinen `update repo`, `direkt update repo` und `update planung`.
- `docs/project/UPDATE_ROUTINES.md` dokumentiert zusaetzlich `tagesstart`, `tagesende`, `tagesende direkt`, `wochenabschluss`, `projektlage`, `plan aufnehmen`, `entscheidung festhalten` und `release check`.
- `docs/project/weekly_reviews/` ist als Ablage fuer Wochenzusammenfassungen vorbereitet.
- Der alte leere Root-Dokumentenordner wurde entfernt; Produkt- und Materialdatenblaetter liegen aktiv unter `data/catalogs/documents/`.
- Nutzerentscheidung dokumentiert: Website- und Portfolio-Chats werden von der Masterarbeits-Entscheidungsanalyse ausgeschlossen.
- Nutzerentscheidung dokumentiert: Echte Produkt-, Material- und Datenbankinhalte werden nicht ins Git-Repo uebernommen; versioniert werden Struktur und klar gekennzeichnete Beispieldaten.
- Nutzerentscheidung dokumentiert: Relative/absolute Cooling-Logik bleibt vorerst nur in Plot-Templates; Hauptportal und regulaerer `cooling`-Befehl werden erst nach Abschluss der Diagrammbearbeitung erneut geprueft.
- Nutzerentscheidungen aus P005 dokumentiert: `ma_parameters` ersetzt `ma_input`, `ma_ui` und `ma_workflow` werden getrennte Zielmodule, `ma_analyse`-Fachlogik bleibt in `ma_analyse`, IDA-Export/-Import, Simulation-Setup, Assessment und Feedback werden getrennt geplant.
- Nutzerentscheidungen aus P005 ergaenzt: Streamlit ist Zieltechnik fuer `ma_ui`; Tkinter bleibt Legacy-Bestand und wird nicht mit Streamlit vermischt; `ma_analyse` soll langfristig eine UI-neutrale Service-Schnittstelle erhalten.
- Nutzerentscheidungen aus P005 verschaerft: `ma_simulation_setup` liegt zwischen Varianten und IDA-Export; die Tkinter-GUI dient als fachliche Ablaufvorlage, nicht als technische Streamlit-Vorlage; `ma_ui` zielt auf Dashboard, Workflow-Views, Shared-Komponenten und Module-Views.
- Nutzerentscheidungen zu den naechsten Strukturpunkten dokumentiert: Tkinter-Vorschau soll ueber einen temporaeren Vorschau-/Cachebereich laufen, freie Overlay-Datenreihen sollen flexibel aus der Datenbasis geladen werden koennen, und Wetterdiagramme bleiben vorerst im Modul `ma_weather`.
- Nutzerentscheidung dokumentiert: Normierungsfragen wie absolute Werte oder flaechenbezogene Werte `[W/m2]` sollen spaeter nicht nur fuer die Energiebilanz, sondern `ma_analyse`-weit fuer passende Auswertungen geplant werden.
- Nutzerentscheidung dokumentiert: `ma_economy` und `ma_sustainability` werden als eigene Zielmodule geplant; `ma_assessment` bleibt als Bewertungs-, Scoring- und Berichtsschicht ueber Analyse, Economy und Sustainability bestehen.
- Historische P005-Entscheidung dokumentiert: `ma_economy`,
  `ma_sustainability` und `ma_assessment` wurden dem damaligen Post-Process
  zugeordnet. P007 ersetzt diese aktive Gliederung durch Phase 5 und einen
  phasenuebergreifenden Feedback-Bereich.
- Leitfaden-Versionierung eingefuehrt: alte Leitfadenfassungen liegen unter
  `docs/project/archive/leitfaeden/`; Version 0.3.7 wurde vor der
  Strukturueberarbeitung unveraendert archiviert. Die aktive Fassung ist
  `MASTERARBEIT_LEITFADEN.md` Version 0.5.0 mit acht festen Hauptbereichen.
- Methodische Untersuchungsdimension aufgenommen: manuellen, softwareunterstuetzten und automatisierten Prozessaufwand nach aktiver Arbeitszeit, Maschinenlaufzeit, Fehlerkorrektur und Wissensstand vergleichen; konkrete Messmethode bleibt offen.
- Vollstaendigen Modulkatalog in den Leitfaden aufgenommen: Zweck, Eingaben, Ausgaben, Abgrenzung und Status sind fuer bestehende und geplante Module dokumentiert.
- Miro-Workflow-Diagramm v0.1.1 als historischen Ist-Entwurf analysiert; die
  korrigierte Zuordnung von `ma_economy`, `ma_sustainability` und
  `ma_assessment` ist im Aenderungsreview dokumentiert. Original-JPG und
  Review liegen versioniert unter `docs/project/architecture/workflow/`.
- Ersetzte Workflow-Fassung v0.1.0 mit Grafik und Review nach
  `docs/project/archive/workflow/` verschoben; v0.1.1 bleibt als
  Diagrammreferenz erhalten, wird strukturell aber durch P007 uebersteuert.
- Routine `aktualisieren` um einen belegbaren Modulstatusabgleich erweitert;
  Streamlit-Navigation, Workflow-Karten, Kennzahlen und Detailtabellen leiten
  ihre Statuswerte zentral aus `src/ma_workflow/catalog.py` ab;
  `actions.py` bleibt Kompatibilitaetszugriff.
- Aktuellen Modulstand abgeglichen:
  - verfuegbar: `ma_analyse`, `ma_variants` und Projektdokumentation;
  - teilweise: `ma_core`, `ma_database`, `ma_ui`, `ma_workflow`,
    `ma_weather`, `ma_parameters`, `ma_export_simulation`,
    `ma_import_simulation`, `ma_economy`, `ma_reporting`,
    `ma_data_export` und `ma_validation`;
  - geplant: `ma_project`, `ma_building`, `ma_zones`, `ma_technical`,
    `ma_analyse.stage_1_dimensioning`, `ma_simulation_setup`,
    `ma_sustainability`, `ma_assessment` und `ma_feedback`;
  - manuell: IDA ICE.
- P005 Phase 1/2 dokumentiert: `ma_analyse`-Bestandsanalyse und Service-Schnittstellenentwurf liegen unter `docs/project/architecture/`.
- P002, P005 und P006 wurden unveraendert archiviert. P007 ist die
  verbindliche strukturelle Grundlage; P008 und P009 fuehren fachliche
  Restarbeiten weiter.
- Phase 0 und die sechs P007-Hauptphasen sind im zentralen Workflow-Katalog
  abgebildet. `ma_validation` und `ma_feedback` werden phasenuebergreifend
  gefuehrt.
- Fehlende Zielmodule sind als leichte importierbare Pakete und dokumentierte
  Infoseiten vorbereitet. Paketexistenz aendert den fachlichen Status nicht.
- Alle 25 katalogisierten Komponenten besitzen einen dokumentierten
  Modulsteckbrief; jede Dashboard-Karte oeffnet eine Fachansicht, eine
  Infoseite oder einen klar gekennzeichneten externen Schritt.

### Aktiver Rahmenplan

- P007 ist als verbindlicher Rahmenplan fuer die weitere VS-Code-Umsetzung
  aufgenommen. Die beschriebene Modulstruktur wurde nach Bestandsanalyse als
  leichtes Geruest umgesetzt; Fachstatus und bestehende Logik bleiben davon
  unberuehrt.
- Vor jeder Umsetzung aus P007 gilt die feste Reihenfolge Analyse, Planung,
  Freigabe, Umsetzung, Test und Dokumentation.
- Die P007-Bestandsanalyse und Strukturkonsolidierung sind abgeschlossen.
  Weitere Fachlogik, Migrationen oder Verschiebungen brauchen weiterhin
  getrennte Teilplaene und Freigaben.
- `ma_export_simulation` und `ma_import_simulation` sind die kanonischen
  allgemeinen Schnittstellenmodule. IDA ICE wird ueber Adapter angebunden;
  historische IDA-spezifische Schluessel bleiben nur als Uebergangsaliase.
- Phase 0 und die sechs P007-Hauptphasen ersetzen die bisherige aktive
  Vierer-Gliederung im Workflow und Dashboard.
- Paketexistenz allein aendert keinen Modulstatus von `planned` oder `partial`
  auf `available`.

### Aktive Teilplaene

- P008 schliesst `ma_weather` mit fuenf realen TRY-Testlaeufen,
  Diagrammpruefung und dokumentierter `weather_key`-Schnittstelle zu
  `ma_parameters` ab.
- P009 plant die allgemeinen Schnittstellen `ma_export_simulation` und
  `ma_import_simulation` mit IDA-ICE-Adaptern. Der vorhandene Basisexport in
  `ma_variants.ida_export` wird wiederverwendet, nicht dupliziert.
- Direkte IDM-Manipulation, erfundene IDA-Befehle und automatischer
  Simulationsstart bleiben bis zur lokalen Verifikation ausgeschlossen.

### Teilweise umgesetzt

- P005 Architektur-Slice umgesetzt: Zielarchitektur und UI-Auslagerungsreview liegen unter `docs/project/architecture/`.
- P005 ordnet den Workflow als Pre-Process, Simulation, Post-Process und Feedback ein.
- P005 bewertet bestehende Oberflaechen: `src/ma_analyse/gui/app.py` bleibt als
  Legacy-Oberflaeche bestehen, wurde aber fachlich an den neuen
  Plot-Template-Ablauf angeglichen; `src/ma_variants/ui/services.py` dient als
  positives Muster fuer Trennung von UI und Fachlogik.
- P005 Streamlit-/Tkinter-Anpassung dokumentiert: `docs/project/architecture/UI_MIGRATION_PLAN.md` beschreibt Bestandsanalyse, Schnittstellenentwurf, Bereinigung, Legacy-Auslagerung, Streamlit-Aufbau und spaetere Modulanbindung.
- P005 Bestandsanalyse dokumentiert: Tkinter sitzt nur in `src/ma_analyse/gui/app.py` und `dialogs.py`; `ma_analyse` hat keine Streamlit-Abhaengigkeit.
- P005 Schnittstellenentwurf dokumentiert: `AnalysisConfig`, `AnalysisResult` und `run_analysis(config)` bilden die UI-neutrale Service-Fassade.
- P005 erster Service-Code-Slice umgesetzt: `src/ma_analyse/models.py` und `src/ma_analyse/services.py` stellen `AnalysisConfig`, `AnalysisResult` und `run_analysis(config)` als UI-neutrale Fassade bereit.
- P005 Workflow-/UI-Shell umgesetzt: `src/ma_workflow/` enthaelt Workflow-Katalog und Analyse-Adapter; `src/ma_ui/` enthaelt eine Streamlit-Shell mit Startseite, Analyse-Seite, Navigation und Projektzustand.
- P005 Startseite erweitert: `ma_ui` zeigt Workflow-Statuskennzahlen,
  Phasenuebersicht, Workflow-Schritte und Dashboard-Aktionen aus
  `ma_workflow`.
- P005 Analyse-Seite erweitert: `ma_analyse` sammelt erzeugte Dateien in `AnalysisResult.created_files`; `ma_ui` zeigt Status, Fehler, Hinweise, erzeugte Dateien und Log strukturiert an.
- P005 Varianten-Uebersicht in `ma_ui` ergaenzt: Parameter, Optionen, Variantenraum, Auswahlmethoden und Exportdateien werden ueber bestehende `ma_variants`-Services angezeigt.
- P005 Wetter-Uebersicht in `ma_ui` ergaenzt: lokale TRY-Datensaetze werden aus dem `ma_weather`-Katalog angezeigt, ohne TRY-Dateien zu importieren.
- P005 Bewertungs-Uebersicht in `ma_ui` ergaenzt: generische Systemkosten, Energiepreise und Szenarien werden aus bestehenden Wirtschaftlichkeitsannahmen angezeigt, ohne Variantenkosten zu berechnen.
- P005 Planoptimierung nach verschaerfter Nutzer-Ausarbeitung umgesetzt: Zielstruktur fuer `ma_ui`, `ma_workflow`, `ma_economy`, `ma_sustainability`, `ma_assessment`, `ma_simulation_setup` und Tkinter-Legacy ist dokumentiert, ohne bestehende Dateien zu verschieben.
- P005 kompatibler Struktur-Slice umgesetzt: `ma_ui/shared/`, `ma_ui/module_views/`,
  `ma_ui/main_dashboard.py`, `ma_ui/workflow_view.py`, `ma_ui/pre_process_view.py`,
  `ma_ui/post_process_view.py` sowie die geplanten `ma_workflow`-Dateien fuer
  Dashboard-Aktionen, Pre-/Post-Process und Feedback sind vorbereitet.
- P005 Analyse-View fachlich erweitert: `ma_ui/module_views/analyse_view.py`
  bildet Prepare-, Comfort-, Heating-/Cooling- und Plot-Template-Optionen auf
  `AnalysisConfig` ab; `pages/analyse.py` bleibt Kompatibilitaetswrapper.
- P005 Analyse-View gegen Tkinter-Ablauf weiter abgeglichen: `analyze-data`
  ist als eigener Excel-Auswertungsschritt mit `separate`/`combined`
  abgebildet.
- P005 Analyseumfang in Streamlit ergaenzt: `Eine Variante`, `Mehrere Varianten`
  und `Alle Varianten` werden erfasst; `Alle Varianten` wird als automatische
  Variantenauswahl an die Service-Fassade uebergeben.
- P005 automatische Analyseauswahl ergaenzt: Variantenlisten fuer Prepare- und
  Datenbankaufrufe sowie Raumlisten werden ueber `ma_analyse.services`
  bereitgestellt; manuelle Texteingabe bleibt als Fallback.
- P005 freie Overlay-Linien in der Analyse-View ergaenzt: einfache Texteingabe
  im Format `source,column,label,axis` wird in Plot-Template-Optionen
  uebersetzt.
- P005 einfache Overlay-Katalogauswahl ergaenzt: `ma_analyse.services`
  stellt CSV-/AUX-Spalten fuer Plot-Template-Overlays bereit; die Analyse-View
  kann daraus eine Overlay-Zeile uebernehmen.
- P005 Streamlit-Importrobustheit ergaenzt: optionale Overlay-Katalogfunktion
  wird in der Analyse-View defensiv zur Laufzeit geladen; Startdokumentation
  empfiehlt den venv-basierten Modulaufruf.
- P005 Plot-Template-Auswahl in Streamlit an Tkinter-Logik angenaehert:
  Nach Auswahl des Befehls `plot-template` werden Zeitfelder aus dem Template
  abgeleitet, Einzelraum-/Mehrraumlogik wird beachtet, Template-Defaults werden
  geladen, feste/freie Overlays sind bedienbar und erzeugte Bilddateien werden
  direkt als Vorschau angezeigt.
- P005 Analyse-Wizard umgesetzt: Die Streamlit-Analyse-Seite startet mit der
  Befehlsauswahl, blendet Folgeschritte nach der vorhandenen Tkinter-
  Zustandslogik ein, fasst vorherige Schritte zusammen und fuehrt technische
  Pfade unter `Erweiterte Pfade`.
- P005 Analyse-Wizard weiter angepasst: Streamlit nutzt eine sichtbare
  Schrittstruktur mit `Befehl`, `Unterbefehl`, `Template / Diagramm`,
  `Varianten`, `Raeume`, optional `Overlay`, abschliessend
  `Export / Ausgabe` und `Analyse starten`.
- P005 Analyse-Wizard bereinigt: Der allgemeine Bereich `Optionen` wurde aus
  der aktiven UI-Struktur entfernt; befehlsspezifische Einstellungen liegen in
  `Export` oder `Template / Diagramm`.
- P005 Comfort-Ablauf angepasst: Die separate Analyseebene wurde entfernt;
  alle vier Comfort-Unterbefehle bleiben sichtbar und Varianten-/Raumumfang
  steuern die Auswahl.
- P005 Varianten- und Raumauswahl angepasst: Variantenumfang und Raumumfang
  liegen in den jeweiligen Bereichen; `Alle Varianten` wird an die
  Service-Fassade als automatische Variantenauswahl uebergeben.
- P005 Plot-Template-Ablauf angepasst: Alle Templates werden direkt als
  Unterbefehle angezeigt. Zeitansicht, Overlay-Aktivierung und ausklappbare
  Diagrammanpassung liegen unter `Template / Diagramm`; der optionale
  Overlay-Schritt folgt nach Varianten und Raeumen.
- P005 Analyse-Wizard weiter strukturiert: `plot-template-analyse` ist in
  Streamlit der UI-Befehl fuer Analyse-Templates, `single`/`compare` liegt
  unter `Export / Ausgabe`, Comfort nutzt `t_op / rel_hum` als Unterbefehl und
  die vier bisherigen Comfort-Ausgaben liegen unter `Template / Diagramm`.
- P005 Aktionsbereich angepasst: In Streamlit stehen `Vorschau aktualisieren`
  und `Analyse starten` sichtbar ausserhalb der Hauptschritte.
- P005 Tkinter-Vorschau vorbereitet: In der Tkinter-Analyse steht
  `Vorschau aktualisieren` zwischen `Zuruecksetzen` und `Start` und nutzt
  vorerst den bestehenden Analysepfad mit aktuellen Einstellungen.
- P005 Tkinter-Analyse pragmatisch angeglichen: Variantenumfang und
  Raumumfang liegen in den jeweiligen Karten, Comfort nutzt keine verpflichtende
  Analyseebene mehr.
- P005 Tkinter-Analyse korrigiert: Bei `plot-template` zeigt eine scrollbare
  Liste alle Diagramme direkt als Unterbefehle. `single`/`compare` liegt wie
  in Streamlit im letzten Schritt `Export / Ausgabe`.
- P005 Plot-Template-Ausgabe erweitert: `single` erzeugt je
  Variante-Raum-Kombination eine eigene Datei. `compare` zeichnet
  Heating-/Cooling-Zeitreihen gemeinsam und buendelt komplexe
  Sammeltemplates als Teilplots in einer Vergleichsgrafik.
- P005 Diagrammanpassung erweitert: Automatische Achsengrenzen sind Standard;
  manuelle Grenzen fuer primaere und sekundaere Y-Achsen werden in einem
  Mock-up sichtbar und an die unterstuetzten Plot-Renderer weitergegeben.
- P005 Overlay-Ablauf erweitert: Der eigene Overlay-Schritt wird ueber eine
  Checkbox aktiviert. Als Katalogreferenz dienen sichtbar die erste Variante
  und der erste Raum; weitere Kombinationen werden beim Lauf validiert.
- P005 Streamlit-Exportbereich verschoben: `Export / Ausgabe` ist die letzte
  Abfrage vor dem Aktionsbereich und enthaelt den Expander
  `Erweiterte Pfade`.
- P005 UI-neutrale Analyse-Helfer ausgelagert: Auswahl-, Zeit-, Overlay- und
  Config-Aufbereitung liegen in `src/ma_analyse/analysis_ui.py`.
- P005 Hybrid-Bedienung vorbereitet: Die Streamlit-Analyse-Seite kann die
  bestehende Tkinter-Analyse als separates Legacy-Fenster starten, ohne Tkinter
  in Streamlit einzubetten.
- P005 grafisches Workflow-Dashboard umgesetzt: Die `ma_ui`-Startseite zeigt
  Phasen, Workflow-Karten, Statusfarben, Iterationspfade und Buttons zu
  vorhandenen Modulansichten; Detailtabellen bleiben im Expander erreichbar.
- Historischer P005-Slice: Die damaligen Platzhalter-Views zeigten
  Workflow-Kontext und vorhandene Projektressourcen. P007 ersetzt sie aktiv
  durch kataloggesteuerte Modul-Infoseiten; historische IDA-Views bleiben
  Kompatibilitaetswrapper auf die allgemeinen Schnittstellen.

### Offen

- P008 liegt als aktiver Abschlussplan fuer das Wettermodul in der Plan-Inbox.
- Aus P005 nach P007 uebernommen: Analyse-View in laufender Streamlit-App manuell gegen
  reale `ida_imports`-/Datenbankordner pruefen.
- Aus P005 nach P007 uebernommen: Schrittweisen Analyse-Wizard in der laufenden
  Streamlit-App fachlich gegen den bisherigen Tkinter-Ablauf pruefen,
  insbesondere Comfort, Heating/Cooling, Plot-Template-Overlays,
  Diagrammbearbeitung und Vorschau.
- Aus P005 nach P007 uebernommen: Comfort-Unterbefehl und
  Comfort-Diagrammauswahl in Tkinter
  noch vollstaendig an die Streamlit-Struktur angleichen.
- Aus P005 nach P007 uebernommen: Eingebettetes Bild-Vorschaufenster fuer den
  Vorschau-Button ergaenzen. Die Vorschau soll einen temporaeren
  Vorschau-/Cachebereich nutzen, damit der regulaere Output-Ordner nicht mit
  fehlerhaften Testdiagrammen gefuellt wird.
- P007 spaeterer Schritt: Tkinter-GUI erst nach separater Freigabe nach
  `ma_ui_legacy` auslagern.
- P007 spaeterer Schritt: `ma_workflow` schrittweise mit echten
  Fachservice-Aufrufen erweitern.
- P007 spaeterer Schritt: `ma_economy`, `ma_sustainability` und
  `ma_assessment` getrennt planen, bevor Wirtschaftlichkeitslogik aus
  `ma_variants` verschoben oder erweitert wird.
- Neue externe Plaene nach manueller Ablage in `docs/project/plans/inbox/` pruefen und in `PLAN_INDEX.md` sowie in diese Statusdatei uebernehmen.
- Nach groesseren Aenderungen pruefen, ob alte Planstaende nach `docs/project/archive/plans/` ausgelagert werden sollen.

## Modul ma_analyse

### Abgeschlossen

- Plot-Template-Katalog aktualisiert: `heating-year` ist overlayfrei, `heating-overlay` fuehrt die festen Heating-Overlays separat.
- Cooling-Plot-Templates getrennt: `cooling-year`, `cooling-month`, `cooling-week` und `cooling-day` verwenden Rohwerte aus `zone_energy_q_cool`; `cooling-absolute-year`, `cooling-absolute-month`, `cooling-absolute-week` und `cooling-absolute-day` zeigen Betraege positiv nach oben.
- Plot-Template-Referenzgalerie unter `docs/examples/plot_templates/` wurde mit 33 aktuellen Beispielen neu erzeugt.
- GUI-Mousewheel-Handler faengt nicht aufloesbare Tkinter-Combobox-Popups robust ab und verhindert `KeyError: 'popdown'`.
- IDA-Importordner umbenannt: `ma_analyse` nutzt fuer Rohdatenvarianten `data/ma_analyse/ida_imports`; der bisherige Eingangsordner wurde entfernt.

### Teilweise umgesetzt

- Plot-Template-Katalog: Referenzbilder liegen unter `docs/examples/plot_templates/`; die Dokumentation liegt unter `docs/ma_analyse/plot_template_examples.md`.
- Heating-Jahresplot nutzt eine gemeinsame Layoutbasis. Absolute Cooling-Jahresplots koennen diese Layoutbasis ebenfalls nutzen; relative Cooling-Templates bleiben als eigene signierte Darstellung erhalten.
- Interne Lasten und Energiebilanz sind als Plot-Template-Experimente vorhanden.

### Offen

- Overlay-Uebernahme in Hauptfunktionen umsetzen: freie Datenreihen sollen aus
  lokalen Analyse-/Datenbankdaten in die aktuelle Ansicht geladen werden
  koennen; feste Additionen wie Temperaturband und Achsenbereiche bleiben
  eigene kontrollierte Diagrammoptionen. Betroffen:
  `src/ma_analyse/analysis/heating.py`, `src/ma_analyse/analysis/cooling.py`,
  `src/ma_analyse/gui/app.py`, `src/ma_analyse/app/cli.py`.
- Nach Abschluss der Diagrammbearbeitung pruefen, ob der normale `cooling`-Befehl und die GUI relative Rohwerte und absolute Betraege als eigene Modi erhalten sollen.
- GUI in kleinere Komponenten fuer Layout, Dialoge, Auswahl und Laufsteuerung aufteilen. Betroffen: `src/ma_analyse/gui/app.py`.
- Heating und Cooling weiter in Datenladen, Runner und Plotmodule zerlegen. Betroffen: `src/ma_analyse/analysis/heating.py`, `src/ma_analyse/analysis/cooling.py`, `src/ma_analyse/analysis/energy/`.

### Unklar

- Soll die relative/absolute Cooling-Logik nach Abschluss der Diagrammbearbeitung auch in den regulaeren `cooling`-Befehl und die GUI uebernommen werden?
- Soll aus den Internal-Loads-Templates ein eigener Befehl entstehen oder eine Integration in bestehende Auswertungen?
- Welche `ma_analyse`-Auswertungen sollen absolute Werte, flaechenbezogene Werte
  wie `[W/m2]` oder beides anbieten, und welche Bezugsflaeche gilt dafuer?

## Modul ma_variants

### Abgeschlossen

- `ma_variants` ist als eigenes Paket unter `src/ma_variants/` vorhanden.
- Variantenbezogene Konfigurationen liegen unter `config/ma_variants/`.
- Variantenbezogene Import-, Export- und IDA-Uebergabeordner liegen unter `data/ma_variants/`.
- Produkt- und Materialdokumente liegen als eigener Katalogbereich unter `data/catalogs/documents/`.
- P001 Bestandspruefung: Import, Optionsimport, Variantenzahlung, Variantenerzeugung, Auswahl, Namensgebung und Export sind bereits als testbare Module vorhanden.
- P001 Variantenoberflaeche: `src/ma_variants/ui/app.py` bildet Parameter/Optionen, Variantenraum, Auswahl, Namensgebung, Export, Ergebnisse und Status getrennt ab.
- P001 UI-Services: `src/ma_variants/ui/services.py` kapselt manuelle Auswahl, reproduzierbare Zufallsauswahl, Filterauswahl und Namensgenerierung ausserhalb der Streamlit-Datei.
- P001 Variantenmodul GUI und Logikpruefung ist abgeschlossen: `tests -k ma_variants` wurde erfolgreich ausgefuehrt und die Streamlit-App wurde headless gestartet.
- P001 wurde nach `docs/project/archive/plans/250603_Plan_Variantenmodul_GUI_Logikpruefung.md` verschoben.

### Offen

- Falls weitere Modulordner unter `data/ma_variants/` gebraucht werden, zuerst im Planstatus dokumentieren.

## Modul ma_weather

### Teilweise umgesetzt

- P002 Struktur-Slice umgesetzt: `src/ma_weather/` ist als importierbares Paket vorbereitet.
- Wetterkatalog mit `WeatherDataset` und YAML-Import liegt unter `src/ma_weather/weather_catalog.py`.
- Beispielkatalog liegt unter `config/ma_weather/datasets/example_weather_datasets.yaml`.
- Reale TRY-Dateien werden lokal unter `data/ma_weather/input/` bereitgestellt und nicht versioniert.
- `data/ma_weather/database/` ist fuer spaeter aufbereitete Wetterdaten vorbereitet.
- `data/ma_weather/output/` ist fuer spaeter erzeugte Wetterdiagramme vorbereitet.
- Dokumentation liegt unter `docs/ma_weather/README.md`, `docs/ma_weather/workflow.md`, `docs/ma_weather/data_model.md` und `docs/ma_weather/commands_weather.md`.
- P002 Analyse-Slice umgesetzt: TRY-Importer, Wettervalidierung, Kennwerte,
  Diagramme, Markdown-Bericht und Runner sind als erste lokale Pipeline
  vorhanden.
- P002 Real-Testlauf fuer `TRY_FFM_2015` erfolgreich: Validierung `ok`, 8760 Stunden,
  sechs Diagramme, aufbereitete CSV und Markdown-Bericht wurden lokal erzeugt.

### Offen

- Weitere aktive Jahresdatensaetze `TRY_FFM_2045`, `TRY_MUC_2015`,
  `TRY_MUC_2045`, `TRY_HAM_2015` und `TRY_HAM_2045` real pruefen.
- Diagrammgestaltung fachlich pruefen und bei Bedarf an Masterarbeitslayout anpassen.
- Offener Strukturpunkt: Wetterdiagramme bleiben vorerst im Modul `ma_weather`;
  spaeter klaeren, ob zusaetzlich ein eigener UI-Hauptbefehl
  `plot-template-weather` eingefuehrt wird.
- P008 erst archivieren, wenn die vorgesehenen realen TRY-Datensaetze lokal
  erfolgreich verarbeitet und die P007-Schnittstelle dokumentiert wurden.

## Offene Nutzerentscheidungen

- Nach Abschluss der Diagrammbearbeitung klaeren, ob relative/absolute Cooling-Logik in den regulaeren `cooling`-Befehl und in die GUI uebernommen wird.
- Klaeren, ob `plot-template-weather` spaeter als eigener UI-Befehl eingefuehrt
  wird oder Wetterdiagramme dauerhaft nur im Modulbereich `ma_weather` bleiben.
- Klaeren, welche `ma_analyse`-Auswertungen absolute Werte, flaechenbezogene
  Werte oder beides anbieten sollen und welche Bezugsflaeche verwendet wird.
- Wissensprofile, Stundensaetze, Prozessgrenzen und Messmethoden fuer den
  Vergleich von manuellem, softwareunterstuetztem und automatisiertem Aufwand
  festlegen.

## Archiv

- `docs/project/archive/plans/2026-05-26.md`: alter Planstatus vor der modularen Struktur.
- `docs/project/archive/plans/250603_Plan_Variantenmodul_GUI_Logikpruefung.md`: abgeschlossener P001-Plan.
- `docs/project/archive/plans/250604_Plan_Projektstruktur_Review_Planungsbereich_Nutzerentscheidungen.md`: umgesetzter Strukturplan P003.
- `docs/project/archive/plans/PLAN_Projektplan_Version_1_0_0.md`: abgelegter Projektplan Version 1.0.0.
- `docs/project/archive/plans/250603_Plan_Wetterdatenanalyse_TRY_Integration.md`: teilweise umgesetzter P002-Ursprungsplan; Restarbeiten stehen in P008.
- `docs/project/archive/plans/250608_Plan_Gesamtmodulstruktur_PreProcess_PostProcess_Dashboard.md.txt`: teilweise umgesetzter P005-Strukturplan; gueltige Inhalte sind in P007 konsolidiert.
- `docs/project/archive/plans/260618_Plan_ma_export_ida_IDM_Exportentwurf.md`: historischer P006-Entwurf; verbleibende Schnittstellenarbeit steht in P009.
