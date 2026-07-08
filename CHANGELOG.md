# Changelog

Alle nennenswerten Aenderungen an `ma_analyse` werden in dieser Datei dokumentiert.

## Unreleased

## 0.24.1 - 2026-07-08

### Added
- Lokalen Normen- und Regelgrundlagenbereich `data/common/normen/` fuer
  Normenextrakte und Reviewlisten sowie getrennten Kalenderbereich
  `data/common/kalender/` angelegt.
- Wochenabschlussbericht fuer KW28 unter
  `docs/project/weekly_reviews/2026-KW28.md` angelegt.
- UI-Command-Dokumentation um einen PowerShell-Befehl zum Schliessen lokaler
  Streamlit-Prozesse ergaenzt.

### Changed
- Projektinput-Dokumentation unter `docs/project/PROJECT_INPUT_WORKFLOW.md`
  zentralisiert; `data/project_inbox/` bleibt der lokale temporaere
  Arbeitsordner.
- P020-Planung und Stage-3-Dokumentation um lokalen Normen- und
  Kalender-Pruefbestand als noch nicht freigegebene Arbeitsgrundlage erweitert.

## 0.24.0 - 2026-07-08

### Added
- BusinessIntegration-LoD-1-Eingabekette erweitert: `ma_zones` enthaelt eine
  validierte Gesamtgebaeudezone mit Buero-Nutzungsprofil, `ma_technical`
  einfache Referenzannahmen fuer Heizung, Kuehlung und Lueftung, und
  `ma_parameters` erzeugt einen validierten `ParameterSnapshot` v1 mit
  Quellenreferenzen.
- Streamlit zeigt fuer `ma_zones` und `ma_technical` jetzt echte
  Pruefansichten mit Freigabestatus, Demo-Daten und Annahmen.
- Streamlit zeigt fuer `ma_parameters` eine Snapshot-Pruefansicht mit
  Freigabestatus, Kopfdaten, Parameterwerten, Quellen und
  Validierungsmeldungen.
- `ma_analyse.stage_1_dimensioning` berechnet eine LoD-1-
  Referenzdimensionierung aus dem validierten `ParameterSnapshot` v1 und zeigt
  Heizlast, interne Kuehllastannahme, Mindest-Luftvolumenstrom, Rechenweg und
  Hinweise in Streamlit.
- Lokale Entwicklungs-Inbox `data/project_inbox/` mit vorsortierten
  Eingangsbereichen und dokumentierter Codex-Routine `projektinput aufnehmen`
  ergaenzt.

## 0.23.0 - 2026-07-05

### Changed
- BusinessIntegration-LoD-1 als versionierte `BuildingModelSpecification`
  ergaenzt: LoD beschreibt den Eingabeumfang; Kubatur, Huellkennwerte,
  U-Werte, Fensteranteil, Validierung, Loader, Streamlit-Auswahl und Tests
  sind fuer den kleinen P012-Einstieg vorhanden.
- Streamlit registriert die vorhandene `ma_building`-Fachansicht und ergaenzt
  einfache geplante Modulansichten fuer `ma_zones` und `ma_technical`.
- Referenzrollen fuer P012 getrennt: `SmallOffice_d_IFC2x3.ifc` fuer den
  fachlichen Teil, Rhino-Testgebaeude fuer BusinessIntegration und
  Softwaretests; P012 startet bewusst mit kleinen Eingabe-LoD-Stufen.
- Alten Kompatibilitaetspfad `docs/examples/plot_templates/` entfernt; die
  Analyse-Referenzgalerie liegt verbindlich unter
  `docs/examples/plot_template_analyse/`.

## 0.22.0 - 2026-07-03

### Changed
- Beispielgalerien unter `docs/examples/` getrennt: Analyse-Plot-Templates
  liegen unter `plot_template_analyse/`, Wetter-Template-Beispiele unter
  `plot_template_weather/`; der Analyse-Galeriegenerator nutzt den neuen
  Zielordner.

## 0.21.0 - 2026-07-02

### Added
- `ma_building` v1 umgesetzt: versionierte Demo-`BuildingModelSpecification`,
  Fachmodelle, Validierung, lokale IFC-/3DM-Quelldiagnose, Arbeitsdatenstruktur
  und Streamlit-Pruefansicht.
- `SmallOffice_d_IFC2x3.ifc` als lokales `ma_building`-Referenzmodell der
  Masterarbeit festgelegt; weitere IDA-ICE-IFCs bleiben Vergleichs-Samples.
- Lokale DWG-Beispieldatei als ungepruefte CAD-Quelle unter
  `data/ma_building/input/cad/` eingeordnet; DWG bleibt ohne Parser kein
  produktiver Importpfad.
- Nutzerentscheidung UD-066 dokumentiert: Kein DWG-Parser, Add-on oder externe
  DWG-Library fuer `ma_building` im aktuellen Masterarbeitsumfang.

## 0.20.2 - 2026-07-01

### Changed
- P012 fuer `ma_building` als vertieften Plan mit
  `BuildingModelSpecification`, einfacher Demo-Spec, lokaler IFC-Diagnose,
  Reifegraden, Raumregister und Schnittstellen zu Nachbarmodulen
  aktualisiert.
- Nutzerentscheidung UD-065 dokumentiert: Relative/absolute Cooling-Trennung
  soll spaeter auch in den regulaeren `cooling`-Befehl und die GUI-Auswahl
  uebernommen werden; OP-006 ist geschlossen.

## 0.20.1 - 2026-06-29

### Added
- BKG-VG250-Gemeindequelle fuer `ma_weather` aktiviert und als lokale
  GeoJSON-Quelle mit `GEN`, `AGS`, `LKZ`, `GF = 4` und `EPSG:4326`
  dokumentiert.
- Reale Berlin-/Potsdam-TRY-Dateien gegen die lokale Gemeindeaufloesung
  getestet: Potsdam `12054000`/`BB`, Berlin `11000000`/`BE`.
- `ma_weather` erkennt geaenderte Wetterdateien im gespeicherten
  Datensatzstatus und markiert veraltete Pruefungen als offen.

### Changed
- Gescannte TRY-Entwuerfe duerfen bei eindeutiger BKG-Gemeindeaufloesung den
  Standort vorbelegen; unsichere Naechstvorschlaege bleiben weiterhin
  bestaetigungspflichtig.
- Erfolgreich gepruefte und bewusst registrierte Wetterentwuerfe werden im
  lokalen Katalog direkt aktiv, setzen aber keinen Projekt-Default.
- Hinweis zur Referenz-/standortgenauen Wetterdatensatzlogik in Streamlit vom
  oberen Auswahlbereich in den Bereich `Wetterdatensaetze` verschoben.
- Tkinter-Analyse delegiert die `AnalysisConfig`-Erzeugung an den gemeinsamen
  UI-neutralen Builder in `ma_analyse.analysis_ui`; Streamlit und Tkinter
  teilen damit den zentralen Analyse-Config-Vertrag.

## 0.20.0 - 2026-06-29

### Added
- Wochenabschlussbericht fuer KW27 unter
  `docs/project/weekly_reviews/2026-KW27.md` angelegt.

### Changed
- Tkinter-Analyse hart aus `ma_analyse` geloest: `ma_analyse gui` und
  `ma_analyse.gui.*` wurden entfernt; kanonischer Start ist
  `python -m ma_ui.tkinter_app.module_views.analyse`.
- Tkinter-Analyse unter `ma_ui` intern in Mixins fuer Initialisierung,
  Fenster/Style, Layout, Schrittfluss, Auswahl-State, Plot-Template-State und
  Pipeline-Runner zerlegt; `app.py` bleibt oeffentliche Fassade.
- Tkinter-Runner nutzt `AnalysisConfig` und
  `ma_workflow.run_analysis_action` statt direkter
  `ma_analyse.app.commands`-Aufrufe; `AnalysisResult` wird ins bestehende
  Protokollfenster geschrieben.
- Wetterdatensatz-Auswahl in Streamlit auf kurze Labels,
  Datensatztyp-Vorfilter und reduzierte Standortkontexte nachgezogen.
- Codex-Sammelbefehle als vorab freigegebene Arbeitsroutinen dokumentiert.

## 0.19.0 - 2026-06-28

### Added
- `ma_weather` um eine optionale Offline-Standortaufloesung fuer TRY-
  Koordinaten mit EPSG:3034-Transformation, Gemeinde-/PLZ-Geodaten-
  Konfiguration und lokalen Geodatenordner erweitert.
- Wetterdateiscan uebernimmt Standortverweise aus TRY-Kopfzeilen, erkennt
  Konflikte zu bestaetigten Ordnerzuordnungen und registriert neue lokale
  Datensaetze zunaechst inaktiv.
- `ma_analyse`-Servicepfad um strukturierte Laufoptionen, Schritt-Ergebnisse,
  Legacy-Ausfuehrungsadapter, Pipeline-Runtime-Argumente und strukturierte
  Datenvorbedingungen erweitert.

### Changed
- Streamlit-Wetteransicht auf eine reduzierte fachliche Pruefansicht mit
  Standortaufloesungsstatus und kompakter aktiver Datensatztabelle nachgezogen.
- P008- und P029-Planung, technische Entscheidungen, Architektur- und
  Command-Dokumentation auf die neuen Wetter- und Analyse-Slices aktualisiert.
- `pyproject.toml` enthaelt jetzt `pyproj` und `shapely` als Abhaengigkeiten
  fuer die optionale lokale Geodatenaufloesung.

## 0.18.0 - 2026-06-27

### Added
- Streamlit-Startbereich um eine getrennte Modul-/Workflow-Ansicht mit
  Workflow-Referenzassets erweitert.
- `plot-template-weather` als eigenen Wetterdiagramm-Befehl mit Auswahl fuer
  alle oder einzelne vorhandene Wetterdiagramme aufgebaut.
- `ma_weather` um lokalen TRY-Dateiscan, Datensatzentwuerfe, Key-Parameter-
  Validierungsmaske und offene Scan-Entwuerfe erweitert.
- TRY-Ordner-zu-Standort-Mapping fuer Wetterdateien versioniert und um
  bestaetigte Mapping-Metadaten sowie koordinatenbasierte Standortvorschlaege
  ergaenzt.

### Changed
- Wetterdatensatzverwaltung in Streamlit auf die drei Schritte `Import`,
  `Scannen` und `Validieren` umgestellt; Validierung startet nur noch nach
  bewusster Nutzeraktion.
- Aktive Wetterdatensaetze zeigen standardmaessig nur die wichtigsten
  fachlichen Spalten, waehrend offene Datensaetze und Entwuerfe detailliert
  bleiben.
- Analyse-Workflow ordnet Overlay-Einstellungen direkt nach
  `Template / Diagramm` ein und dokumentiert die Datenvorbereitung als eigenen
  Workflow-Schritt.
- Dokumentation, Planstatus und Nutzerentscheidungen auf die neue UI-,
  Wetter- und Workflow-Struktur nachgezogen.

## 0.17.0 - 2026-06-24

### Added
- `ma_analyse.data_preparation` als eigener Workflow-Schritt fuer `prepare`
  und `analyze-data` dokumentiert und im Workflow-Katalog vorbereitet.

### Changed
- `ma_ui` strukturell in `streamlit_app` und `tkinter_app` getrennt.
  `src/ma_ui/app.py` bleibt stabiler Streamlit-Einstieg; die Tkinter-Analyse
  liegt unter `ma_ui.tkinter_app.module_views.analyse`.
- Alte `ma_ui.*`- und `ma_analyse.gui.*`-Importpfade bleiben ueber
  Kompatibilitaetswrapper nutzbar.
- Wetterdatensatz-Import und Bestands-/Validierungspruefung stehen in
  Streamlit gemeinsam im Bereich `Wetterdatensaetze`; aktive und offene
  Wetterdatensaetze werden dort gleichwertig getrennt angezeigt.
- Tkinter-Analyse startet den ersten Befehlsschritt der Analyseauswahl jetzt
  standardmaessig mit `plot-template`.

## 0.16.2 - 2026-06-24

### Added
- Streamlit-Wetterseite fuer P008 Slice 5 erweitert: Importbutton im
  Bereich `Wetterdatensaetze`, lokaler Importkatalog fuer eigene TRY-`.dat`
  Dateien und getrennte aktive/offene Datensatzuebersichten.

### Changed
- ma_weather-Planung um den manuellen Download fehlender TRY-Jahres-, Sommer-
  und Winterdateien beim Deutschen Wetterdienst ergaenzt.

## 0.16.1 - 2026-06-24

### Added
- P008-Wetterstatus fuer Datei-, Import-, Warnungs-, Fehler- und
  Freigabestand je `weather_key` eingefuehrt.
- `import_id` fuer Wetteranalyse-Laeufe und lokale Aktivierungs-/
  Projekt-Default-Verwaltung fuer freigegebene Wetterdatensaetze ergaenzt.
- Streamlit-Wetterseite um Bestandspruefung, offene Wetterdatensaetze,
  Aktivierung und Projekt-Default erweitert.
- Wetterkatalog um Sommer- und Winter-TRY-Dateien als eigene Datensaetze
  ergaenzt und kritische Wetterereignisse je bewusst ausgewaehltem
  Wetterdatensatz vorbereitet.

### Changed
- Jahres-Wetterdatensaetze erhalten im `weather_key` die Endung `_JAHR`,
  damit Jahr, Sommer und Winter einheitlich gekennzeichnet sind.
- P008-Planstatus, Nutzerentscheidungen, technische Entscheidungen und
  Workflow-Next-Step auf den aktuellen ma_weather-Stand nachgezogen.

## 0.16.0 - 2026-06-23

### Added
- P010-Vertraege fuer Eingabequellen, Dateipruefsummen, strukturierte
  Diagnosen, Freigabeentscheidungen und eindeutige IDs eingefuehrt.
- Append-only JSONL-Sitzungslogs unter `logs/sessions/` fuer Laeufe,
  Warnungen, Fehler und Freigabeentscheidungen ergaenzt.
- TRY-Wetterimport als ersten P010-Pilotadapter an die gemeinsamen Modelle
  angebunden.
- P008-Gesamtplan fuer `ma_weather` aus den beiden Ausgangsplaenen
  konsolidiert und die Ausgangsplaene nachvollziehbar archiviert.
- YAML-basierten Standort- und Klimaregionskatalog fuer `ma_weather`
  mit Stadtbezug, TRY-Referenzstandort und Datensatzrollen eingefuehrt.
- Streamlit-Wetterseite mit Kartenbereich, Stadtwahl, automatisch
  ermittelter Klimaregion, TRY-Referenzstandort und sortierter
  Wetterdatensatzauswahl erweitert.

### Changed
- Wetteransicht um Quellenmetadaten, Diagnose-IDs, Fundstellen und
  laufgebundene Warnungsfreigabe erweitert.
- Wetterkatalog priorisiert TRY-Referenzdatensaetze vor standortgenauen
  Datensaetzen und vermeidet fachlich unklare Ersatzzuordnungen.
- P010 archiviert und P008, P011, P015 sowie P027 auf die gemeinsamen
  Eingabe- und Freigabevertraege ausgerichtet.

## 0.15.0 - 2026-06-23

### Added
- P028-Fachansichten fuer Simulationsprogramme, neutrale Benennungsprofile,
  Parameterdefinitionen, Optionsauswahl und benannte Varianten ergaenzt.
- Gemeinsamen Streamlit-Sitzungsstand und gezielte Modulverweise mit
  Ruecksprung zur Ausgangsseite eingefuehrt.
- Sichere lokale YAML-Speicherung mit Vorlagenschutz, Pfadpruefung,
  Kollisionsfehlern und bestaetigtem Ueberschreiben eigener Dateien
  umgesetzt.

### Changed
- Bestehende Parameter-, Options-, Naming- und Variantengeneratoren in den
  P028-Datenfluss eingebunden, ohne historische Konfigurationen zu brechen.
- P028 archiviert und P010, P011, P015, P017 sowie P027 auf den erreichten
  Demo-Zwischenstand aktualisiert.

## 0.14.0 - 2026-06-23

### Added
- P010 bis P028 als abgestufte Modul-, Analyse-, Demo-, Konzept-, Research-
  und Querschnittsplaene aufgenommen.
- Leichte Paket- und Dokumentationsgrenzen fuer Analyse Stufe 2 Optimierung,
  Stufe 3 Standards Compliance und Stufe 4 Sensitivitaet ergaenzt.
- Umschaltbare Modul-Infokarte in der Streamlit-Kopfzeile ergaenzt.
- P028 fuer Projektkonfiguration, Demo-Optionsauswahl und neutrale
  Variantenbenennung in Streamlit aufgenommen.

### Changed
- P007 auf die priorisierte Eingabekette bis `ma_simulation_setup`, eine
  optionale IFC-Lite-Entscheidung und die zurueckgestellte P009-Umsetzung
  ausgerichtet.
- Analyse Stufe 3 verbindlich als Norm-Nachweis unter
  `ma_analyse.stage_3_standards_compliance` eingeordnet; der fruehere
  Verification-Name bleibt nur als Uebergangsalias.
- Workflow-Katalog und Dashboard trennen Optimierung, Norm-Nachweis und
  Sensitivitaet als eigene Analysestufen.
- Fachstatus geschaerft: Nur Wetter und Analyse einschliesslich Stage 2 gelten
  als teilweise umgesetzt; vorhandene Gerueste und Prototypen bleiben geplant.
- Verantwortlichkeiten fuer Simulationsprogramme, Parameter, neutrales Naming,
  Vorlagenschutz und spaeter erweiterbare Speicherformate festgelegt.

## 0.13.0 - 2026-06-22

### Added
- Leichte, seiteneffektfreie Gerueste fuer die P007-Zielmodule einschliesslich
  Modul-READMEs und IDA-ICE-Adaptergrenzen unter den allgemeinen
  Simulationsschnittstellen angelegt.
- Zentralen `ma_workflow`-Katalog mit Phase 0, sechs Fachphasen,
  Moduldefinitionen, Workflow-Schritten und phasenuebergreifenden Funktionen
  eingefuehrt.
- P008 fuer den Wettermodulabschluss und P009 fuer die allgemeinen
  Simulationsschnittstellen mit IDA-ICE-Adaptern angelegt.
- Generische, klickbare Modul-Infoseiten und Strukturtests fuer Pakete,
  Dokumentation, Phasen, Module und Kompatibilitaetsaliase ergaenzt.

### Changed
- P007 als verbindlichen Rahmenplan fuer die weitere VS-Code-Umsetzung aufgenommen; Planindex und Planstatus nennen die vorgelagerte Bestandsanalyse sowie den erforderlichen Abgleich mit der bestehenden Zielarchitektur.
- Projektsteuerung mit P007-Nutzerentscheidung, offenen Architekturfragen sowie aktualisierten Beschreibungen von `ma_ui`, `ma_workflow` und dem Leitfaden abgeglichen.
- Strukturreview und zentrale Projektuebersichten an den aktuellen Stand von Wetterpipeline, Streamlit-Oberflaeche, Workflow-Schicht und P007-Priorisierung angepasst.
- P002, P005 und P006 unveraendert archiviert; ihre offenen Entscheidungen und
  Restarbeiten kontrolliert nach P007, P008 und P009 uebernommen.
- Dashboard und Navigation auf Phase 0 bis Phase 6 sowie einen eigenen
  Querschnittsbereich fuer Validierung und Feedback umgestellt.
- `ma_export_simulation` und `ma_import_simulation` als kanonische Namen
  festgelegt; bisherige IDA-Schluessel bleiben dokumentierte
  Kompatibilitaetsaliase.
- Projektsteuerung, Modulstatus und Update-Routine auf den zentralen
  `ma_workflow.catalog` sowie die vollstaendige P007-Komponentenliste
  abgeglichen.

## 0.12.0 - 2026-06-18

### Added
- Plot-Template-Ausgabemodus technisch umgesetzt: `single` erzeugt eine Datei je Variante-Raum-Kombination, `compare` eine gemeinsame Vergleichsausgabe.
- Diagrammanpassung in Streamlit und Tkinter um automatische beziehungsweise manuelle Grenzen der primaeren und sekundaeren Y-Achse sowie ein direktes Mock-up erweitert.
- Eigenen optionalen Overlay-Schritt nach Varianten- und Raumauswahl eingefuehrt; die sichtbare Katalogreferenz nutzt die erste gewaehlte Variante und den ersten Raum.
- Tests fuer Achsenvalidierung, direkte Template-Auswahl sowie Single-/Compare-Ausgaben von Zeitreihen, Balken- und Comfort-Templates ergaenzt.

### Changed
- Plot-Templates werden in Tkinter und Streamlit ohne vorgelagerte Diagrammgruppen direkt als Unterbefehle angeboten.
- Analyse-Wizard neu geordnet: `Template / Diagramm`, Varianten, Raeume, optional Overlay und abschliessend `Export / Ausgabe` vor Vorschau und Analysestart.
- Streamlit-`Erweiterte Pfade` in den abschliessenden Bereich `Export / Ausgabe` verschoben.
- Heating-/Cooling-Zeitreihen werden im Compare-Modus als gemeinsame Datenreihen dargestellt; komplexe Sammeltemplates werden als beschriftete Teilplots in einer Vergleichsgrafik gebuendelt.
- UI-, Architektur-, Planungs-, Entscheidungs- und Befehlsdokumentation an den neuen Plot-Template-Ablauf angepasst.

## 0.11.0 - 2026-06-18

### Changed
- Strukturelle Nutzerentscheidungen dokumentiert: Tkinter-Vorschau soll einen temporaeren Vorschau-/Cachebereich nutzen, Overlays sollen freie Datenreihen aus der Datenbasis plus feste Diagrammoptionen erlauben, und Wetterdiagramme bleiben vorerst im Modul `ma_weather`.
- `ma_ui`-Wetterseite umsortiert: Analyseauswahl und Analyseergebnis stehen vor der Wetterdatensatzuebersicht.
- Normierungsfrage fuer `ma_analyse` verallgemeinert: absolute und flaechenbezogene Werte sollen spaeter als modulweite Ausgabe-/Diagrammstrategie geplant werden, nicht nur als Energy-Balance-Sonderfall.
- Tkinter-Analyse korrigiert: Bei `plot-template` ist der Unterbefehl jetzt die Diagrammgruppe; `single`/`compare` liegt im Schritt `Export / Ausgabe`.
- Tkinter-Plot-Template-Auswahl mit Tests fuer Diagrammgruppenfilterung und den vollstaendigen Fallback vor der Auswahl abgesichert.
- Zentralen Leitfaden `docs/project/MASTERARBEIT_LEITFADEN.md` als Orientierungsdatei fuer Ziel, Workflow, Module, Datenstruktur, UI und offene Strukturpunkte angelegt.
- Leitfaden-Versionierung eingefuehrt: Codex-Erstfassung und ChatGPT-Referenz wurden unter `docs/project/archive/leitfaeden/` archiviert, die aktive Leitfadenversion 0.3.0 fuehrt beide Quellen mit der neuen Bewertungsarchitektur zusammen.
- Bewertungsarchitektur dokumentiert: `ma_economy` und `ma_sustainability` werden als eigene Zielmodule geplant; `ma_assessment` bleibt als Bewertungs-, Scoring- und Berichtsschicht.
- Leitfaden auf Version 0.3.1 aktualisiert: Economy, Sustainability und Assessment gehoeren im Zielworkflow zum Post-Process; Feedback bleibt eigener Block.
- Archivierte Plaene aus `docs/project/plans/archived/` nach `docs/project/archive/plans/` verschoben und aktive Planverweise aktualisiert.
- P006 als Entwurf fuer `ma_export_ida` aufgenommen und Leitfaden auf Version 0.3.2 um Grundsaetze fuer Referenzmodell, Variantenexport, IDM-Sicherheit, Mapping und optionale API-Anbindung erweitert.
- Leitfaden auf Version 0.3.3 erweitert: manueller, softwareunterstuetzter und automatisierter Prozessaufwand soll nach Wissensstand, aktiver Arbeitszeit, Maschinenlaufzeit, Fehlerkorrektur und Personalkosten verglichen werden.
- Leitfaden auf Version 0.3.4 erweitert: einheitlicher Modulkatalog dokumentiert Zweck, Ein- und Ausgaben, Abgrenzung und Status aller bestehenden und geplanten Module.
- Leitfaden auf Version 0.3.5 erweitert und aktuellen Miro-Workflow als Ist-Entwurf fachlich analysiert; Workflow-Review und Ablagestruktur unter `docs/project/architecture/workflow/` ergaenzt.
- Leitfaden auf Version 0.3.6 aktualisiert und Original-JPG des Miro-Workflows unter `docs/project/architecture/workflow/` versioniert sowie direkt verlinkt.
- Leitfaden auf Version 0.3.7 aktualisiert: neu hochgeladenen Miro-Workflow v0.1.1 als aktuellen Ist-Entwurf dokumentiert, Aenderungsreview ergaenzt und die korrigierte Zuordnung von `ma_economy`, `ma_sustainability` und `ma_assessment` festgehalten.
- Leitfaden-Version 0.3.7 unveraendert archiviert und die aktive Version 0.4.0 in acht feste Hauptbereiche gegliedert: Zweck, Gesamtworkflow, Moduluebersicht, Daten-/Dokumentationsstruktur, UI-/Workflow-Struktur, Arbeitsroutinen, wichtigste Entscheidungen und offene Strukturpunkte.
- Workflow-Archiv unter `docs/project/archive/workflow/` angelegt und die ersetzte Grafik-/Review-Fassung v0.1.0 dorthin verschoben; v0.1.1 bleibt die aktive Architekturreferenz.
- Routine `aktualisieren` erweitert: Fachpakete, Services, Views, Tests und Dokumentation werden zur Bewertung der Modulumsetzungsstaende geprueft.
- Streamlit-Statusanzeigen zentralisiert: Navigation, Workflow-Karten, Kennzahlen und Detailtabellen verwenden die Statuswerte aus `ma_workflow`.
- Workflow-Status an den belegbaren Projektstand angepasst und Economy, Sustainability sowie Assessment als getrennte Post-Process-Schritte dargestellt.
- Leitfaden auf Version 0.4.1 aktualisiert und Modulstatus sowie Workflow-Archiv dokumentiert.

## 0.10.0 - 2026-06-17

### Changed
- `ma_ui`-Navigation stabilisiert: Die Sidebar-Auswahl wurde durch eine Kopfzeilen-Navigation mit `Start`, `Zurueck` und `Weiter` ersetzt.
- Streamlit-Tabellen und Buttons auf die aktuelle `width="stretch"`-API umgestellt und gemischte UI-Tabellenspalten fuer Arrow-kompatible Anzeige normalisiert.
- Grafischen Workflow auf der Startseite phasenweise als Kartenraster neu angeordnet.
- Streamlit-Analyse-Wizard weiter an Tkinter-Zustandslogik angepasst: Comfort-Unterbefehle bleiben ohne separate Analyseebene sichtbar; Plot-Template-Overlays erscheinen erst nach Varianten- und Raumauswahl.
- Streamlit-Analyse-Wizard auf eingeklappte Schrittstruktur umgestellt: `Export`, `Template / Diagramm`, `Varianten`, `Raeume` und `Analyse starten` ersetzen den allgemeinen Bereich `Optionen`; Comfort nutzt keine separate Analyseebene mehr.
- Streamlit-Analyse-Wizard weiter strukturiert: `plot-template-analyse` ist der UI-Befehl fuer Analyse-Templates, `single`/`compare` liegt unter `Export / Ausgabe`, Comfort nutzt den Unterbefehl `t_op / rel_hum`, und der Aktionsbereich mit Vorschau und Analyse-Start ist nicht mehr einklappbar.
- Tkinter-Analyse um den Button `Vorschau aktualisieren` zwischen `Zuruecksetzen` und `Start` erweitert; der Button nutzt vorerst den bestehenden Analysepfad mit aktuellen Einstellungen.
- Tkinter-Analyse pragmatisch an dieselbe Fachstruktur angenaehert: Variantenumfang und Raumumfang liegen in den jeweiligen Karten, `plot-template` besitzt einen Unterbefehl `single`/`compare`.
- UI-neutrale Analyse-Helfer fuer Auswahl-, Zeit-, Overlay- und Config-Aufbereitung nach `ma_analyse.analysis_ui` ausgelagert.
- `tagesstart` angepasst: Die Routine startet `ma_ui` nicht mehr automatisch und verweist bei Bedarf nur noch auf den dokumentierten Streamlit-Startbefehl.
- `ma_ui`-Wetterdaten-Seite erweitert: aktive Wetterdatensaetze koennen ausgewaehlt, ueber `ma_weather` analysiert und erzeugte Diagramme direkt angezeigt werden.

## 0.9.2 - 2026-06-16

### Changed
- Nutzerentscheidungen aus dem aktuellen Chat zu `ma_ui`-Modulansichten, Analyse-Wizard, Tkinter-Legacy-Start und `ma_weather`-TRY-Struktur dokumentiert.
- Command-Dokumentation nach Sammelbefehlen, Einzelbefehlen und Test-/Referenzbefehlen strukturiert; `aktualisieren` und `aktualisiere tests` als Codex-Routinen dokumentiert.
- `aktualisieren` erweitert: Command-Dokumentation wird bei geaenderten Befehlen, Routinen oder Startwegen mitgeprueft und bei Bedarf aktualisiert.

## 0.9.1 - 2026-06-15

### Changed
- P002 Real-Testlauf fuer `TRY_FFM_2015_JAHR` dokumentiert: Validierung `ok`, 8760 Stunden, sechs Wetterdiagramme, aufbereitete CSV und Markdown-Bericht wurden lokal erzeugt.

## 0.9.0 - 2026-06-15

### Changed
- `ma_analyse`-Plot-Template-Beispielgalerie unter `docs/examples/plot_templates/` mit aktueller Logik neu erzeugt.
- P005 fortgefuehrt: geplante `ma_ui`-Modulansichten zeigen vorhandene Projektressourcen und relevante Pfade ohne neue Fachlogik.
- P002 fortgefuehrt: `ma_weather` besitzt nun TRY-Import, Validierung, Wetterkennwerte, Diagramme, Markdown-Bericht und einen lokalen Runner.
- `ma_weather` um eine dokumentierte Zuordnung lokaler TRY-Kennungen zu Frankfurt am Main, Muenchen und Hamburg ergaenzt.
- Wetterkatalog um aktive 2015-Jahresdatensaetze fuer Muenchen und Hamburg ergaenzt.
- Wetterkatalog um aktive 2045-Jahresdatensaetze fuer Frankfurt am Main, Muenchen und Hamburg ergaenzt.
- Streamlit-Standardnavigation fuer `ma_ui` ausgeblendet, damit nur die fachliche Projektnavigation sichtbar bleibt.
- Technische Workflow- und Dashboard-Tabellen aus den geplanten `ma_ui`-Modulansichten entfernt und auf der Startseite eingeklappt gebuendelt.
- Ressourcenlisten aus leeren `ma_ui`-Modulansichten entfernt; geplante Module zeigen nur noch Titel, Untertitel und Hinweisbox.
- Regel abgesichert, dass der grafische Workflow nur auf der `ma_ui`-Startseite gerendert wird.
- P005 Analyse-View in Streamlit auf eine schrittweise Wizard-Bedienung nach Tkinter-Zustandslogik umgestellt; technische Pfade liegen nun unter `Erweiterte Pfade`.

## 0.8.0 - 2026-06-15

### Added
- `ma_ui`-Startseite um Statuskennzahlen, Phasenuebersicht und Dashboard-Aktionen aus `ma_workflow` erweitert.
- `ma_ui`-Analyse-Seite um Tkinter-nahe Plot-Template-Auswahl mit dynamischen Zeitfeldern, Single-/Multi-Room-Logik, Template-Defaults, festen/freien Overlays und Bildvorschau erweitert.
- Codex-Routinen aktualisiert: `tagesstart` startet `ma_ui` bei Bedarf ueber die Projekt-venv; `tagesende` und `tagesende direkt` melden laufende Projekt-Streamlit-Prozesse ohne sie automatisch zu beenden.
- `ma_ui`-Startseite zu einem grafischen Workflow-Dashboard mit Phasenkarten, Statusfarben, Iterationspfaden und Navigationsbuttons erweitert.
- `ma_ui`-Analyse-Seite um einen Legacy-Button erweitert, der die bestehende Tkinter-Analyse als separaten Prozess startet.

## 0.7.0 - 2026-06-11

### Added
- P005 `ma_analyse`-Bestandsanalyse und Service-Schnittstellenentwurf unter `docs/project/architecture/` ergaenzt.
- `ma_analyse.models.AnalysisConfig`, `ma_analyse.models.AnalysisResult` und `ma_analyse.services.run_analysis(config)` als erste UI-neutrale Service-Fassade ergaenzt.
- `ma_workflow` als neutrale Workflow-Schicht mit Workflow-Katalog und Analyse-Adapter ergaenzt.
- `ma_ui` als minimale Streamlit-Shell mit Startseite, Analyse-Seite, Navigation und Projektzustand ergaenzt.
- `ma_ui/shared/` und `ma_ui/module_views/` als kompatible Zielstruktur fuer gemeinsame UI-Bausteine und modulbezogene Views vorbereitet.
- `ma_ui/main_dashboard.py`, `ma_ui/workflow_view.py`, `ma_ui/pre_process_view.py` und `ma_ui/post_process_view.py` als vorbereitete Uebersichtshelfer ergaenzt.
- `ma_workflow` um vorbereitete Zielmodule fuer `workflow_manager`, `dashboard_actions`, `pre_process_runner`, `post_process_runner` und `feedback_router` erweitert.
- Varianten-Uebersicht in `ma_ui` ergaenzt; sie nutzt bestehende `ma_variants`-Services fuer Parameter, Optionen, Variantenraum, Auswahlmethoden und Exportdateien.
- Wetter-Uebersicht in `ma_ui` ergaenzt; sie nutzt den bestehenden `ma_weather`-Katalog und importiert keine TRY-Dateien.
- Bewertungs-Uebersicht in `ma_ui` ergaenzt; sie zeigt generische Systemkosten, Energiepreise und Szenarien ohne Variantenkosten in der UI zu berechnen.
- Analyse-View in `ma_ui/module_views/analyse_view.py` um befehlsspezifische Konfiguration fuer Prepare, Comfort, Heating, Cooling und Plot-Templates erweitert.
- Analyse-View um `analyze-data` als eigenen Excel-Auswertungsschritt mit `separate`/`combined` erweitert.
- Analyse-View um Analyseumfang erweitert; `Alle Varianten` wird als automatische Variantenauswahl an `AnalysisConfig` uebergeben.
- `ma_analyse.services` um UI-neutrale Listenfunktionen fuer Varianten und Raeume erweitert; die Analyse-View nutzt diese Listen mit manueller Eingabe als Fallback.
- Analyse-View um freie Plot-Template-Overlay-Linien als einfache Textangabe im Format `source,column,label,axis` erweitert.
- `ma_analyse.services` um eine UI-neutrale Overlay-Katalogfunktion erweitert; die Analyse-View kann CSV-/AUX-Spalten fuer Plot-Template-Overlays aus vorhandenen lokalen Daten anbieten.
- `ma_ui`-Platzhalterseiten fuer Parameter, Gebaeude, Simulation-Setup, IDA-Export, IDA-Import und Feedback zeigen nun Workflow-Kontext aus `ma_workflow`.
- Tests fuer `ma_workflow`, `ma_ui`-Navigation, Projektzustand, Analyse-Ergebnisanzeige sowie Wetter- und Bewertungsuebersichten ergaenzt.

### Changed
- P005-Zielarchitektur nach verschaerfter Nutzer-Ausarbeitung optimiert: `ma_ui` zielt nun dokumentiert auf Dashboard, Workflow-Views, Shared-Komponenten und Module-Views; `ma_workflow` auf Dashboard-Aktionen, Pre-/Post-Process-Runner und Feedback-Routing.
- P005-Planung geschaerft: `ma_simulation_setup` liegt zwischen Variantenbildung und IDA-Export, `ma_assessment` wird als Bewertungsoberstruktur fuer Economics und Sustainability geplant, und die bestehende Tkinter-GUI gilt als fachliche Ablaufvorlage statt technischer Streamlit-Vorlage.
- P005-Inventar und UI-Auslagerungsreview um konkrete Tkinter-Bedienlogik, spaeteres Analyse-View-Mapping und offene Inventarfragen erweitert.
- P005-Planstatus, Architekturunterlagen und Modul-READMEs auf den kompatiblen `ma_ui`-/`ma_workflow`-Struktur-Slice aktualisiert.
- `src/ma_ui/pages/analyse.py` bleibt als Kompatibilitaetswrapper bestehen; die aktive Analyse-View liegt unter `src/ma_ui/module_views/analyse_view.py`.
- P005-Planstatus, Planindex, Strukturreview und Cleanup-Plan nach Umsetzung der ersten Service-Fassade aktualisiert.
- P005-Planstatus und Architekturunterlagen nach Umsetzung der minimalen `ma_ui`-/`ma_workflow`-Shell aktualisiert.
- Die `ma_analyse`-Service-Fassade normalisiert CLI-nahe Schritt-Aliase wie `analyze-data` auf interne Analyse-Schritte.
- Die `ma_analyse`-Service-Fassade sammelt neu erzeugte Dateien aus Datenbank- und Ausgabeordnern fuer die UI-Anzeige.
- Die `ma_ui`-Analyse-Seite zeigt Status, Fehler, Hinweise, erzeugte Dateien und Logs ueber eine eigene Ergebnis-Komponente.
- Die `ma_ui`-Analyse-Seite laedt die optionale Overlay-Katalogfunktion defensiv zur Laufzeit, damit Streamlit-Hot-Reloads mit alten Modulstaenden nicht am Import abbrechen.
- Der empfohlene Startbefehl fuer `ma_ui` nutzt explizit `.\.venv\Scripts\python.exe -m streamlit`.

## 0.6.0 - 2026-06-08

### Added
- Codex-Arbeitsroutinen fuer `tagesstart`, `tagesende`, `tagesende direkt`, `wochenabschluss`, `projektlage`, `plan aufnehmen`, `entscheidung festhalten` und `release check` dokumentiert.
- `docs/project/weekly_reviews/` als Ablage fuer Wochenzusammenfassungen vorbereitet.
- P002 Struktur-Slice fuer `ma_weather` mit Paket-Skeleton, Wetterkatalog, Beispielkatalog, Dokumentation und Katalogtests vorbereitet.
- P005 `Gesamtmodulstruktur, Pre-/Post-Process und Dashboard` in Planindex und Planstatus aufgenommen.
- Architektur-Dokumente fuer P005 unter `docs/project/architecture/` ergaenzt.
- `docs/project/architecture/UI_MIGRATION_PLAN.md` als Phasenplan fuer Streamlit-Ziel-UI, Tkinter-Legacy und UI-neutrale Analyse-Services ergaenzt.

### Changed
- Nutzerentscheidungen zu Website-/Portfolio-Chat-Ausschluss und zum Umgang mit echten Produkt-, Material- und Datenbankinhalten dokumentiert.
- Nutzerentscheidung dokumentiert, dass die relative/absolute Cooling-Trennung vorerst nur in Plot-Templates bleibt und das Hauptportal spaeter geprueft wird.
- `USER_DECISIONS_OPEN_POINTS.md` auf offene Punkte beschraenkt und `tagesstart` um Pflege offener Nutzerentscheidungen ergaenzt.
- P001 `Variantenmodul GUI und Logikpruefung` finalisiert, Planstatus aktualisiert und Plan nach `docs/project/plans/archived/` verschoben.
- PowerShell-Testbefehl fuer komplette `ma_variants`-Tests in der Befehlsdokumentation korrigiert.
- Reale TRY-Dateien als lokale Eingabedaten dokumentiert; der Wetterkatalog darf auf nicht versionierte Dateien unter `data/ma_weather/input/` verweisen.
- `ma_weather`-Datenpfade angepasst: aufbereitete Wetterdaten unter `data/ma_weather/database/`, Wetterdiagramme unter `data/ma_weather/output/`.
- `ma_analyse`-Eingangsordner auf `data/ma_analyse/ida_imports/` umbenannt und aktive Code-, Test- und Dokumentationsverweise aktualisiert.
- Nutzerentscheidungen zur P005-Zielmodulstruktur, UI-/Workflowtrennung und spaeterer Auslagerung der `ma_analyse`-Oberflaeche dokumentiert.
- P005-Zielarchitektur auf Streamlit als verbindliche Zieltechnik fuer `ma_ui`, Tkinter als Legacy-Bestand und eine spaetere `ma_analyse`-Service-Schnittstelle ausgerichtet.
- P005-Planstatus und Planindex auf den naechsten Schritt `ma_analyse`-Bestandsanalyse mit `AnalysisConfig`, `AnalysisResult` und `run_analysis(config)` aktualisiert.

## 0.5.1 - 2026-06-08

### Changed
- `heating-year` ist nun das overlayfreie Plot-Template fuer den normalen Heating-Jahresplot; `heating-overlay` fuehrt Sollwertband, Aussenlufttemperatur und operative Temperatur separat.
- Relative Cooling-Plot-Templates verwenden nun die Rohwerte aus `zone_energy_q_cool`; absolute Cooling-Templates zeigen die Betraege positiv nach oben.
- Cooling-Template-Ausgaben verwenden Blau als Primaerfarbe.
- Planstatus, Planindex und Entscheidungsdokumente wurden auf den aktuellen Plot-Template- und GUI-Fix-Stand aktualisiert.

### Added
- `plot-template-examples` erzeugt zusaetzlich ein Beispielbild fuer `heating-overlay`; die Befehlsdokumentation fuehrt den Kurzbegriff `heating year overlay`.
- Neue Plot-Templates `cooling-absolute-year`, `cooling-absolute-month`, `cooling-absolute-week` und `cooling-absolute-day` ergaenzt.

### Fixed
- GUI-Mousewheel-Handler ignoriert nicht aufloesbare Tkinter-Combobox-Popups robust, statt bei `popdown`-Widgets einen `KeyError` auszugeben.

## 0.5.0 - 2026-06-05

### Changed
- Dokumentation modularisiert: aktive Projektsteuerung liegt nun unter `docs/project/`, Fachdocumentation unter `docs/ma_analyse/`, `docs/ma_variants/`, `docs/ma_weather/` und gemeinsame Hinweise unter `docs/common/`.
- `docs/PLAN.md` aus der aktiven Steuerung geloest und als abgelegter Plan nach `docs/project/plans/archived/PLAN_Projektplan_Version_1_0_0.md` verschoben.
- `PLAN_STATUS.md` nach Modulen neu strukturiert und nach `docs/project/plans/PLAN_STATUS.md` verschoben.
- Umgesetzten Strukturplan P003 nach `docs/project/plans/archived/` verschoben und Planindex/Planstatus entsprechend aktualisiert.
- Plan-Inbox auf konsistente Markdown-Dateinamen fuer P001 und P002 normalisiert.
- `ma_variants`-Konfigurationen nach `config/ma_variants/` verschoben.
- Variantenbezogene Import-, Export- und IDA-Uebergabeordner nach `data/ma_variants/` verschoben.
- `ma_analyse` hart auf modulare Analyse-Datenpfade migriert; alte Root-Pfade werden nicht mehr unterstuetzt.
- Produkt- und Materialdokument-Platzhalter nach `data/catalogs/documents/` verschoben.
- `plot-template-examples` schreibt die Galerie-Dokumentation nun nach `docs/ma_analyse/plot_template_examples.md`.
- `.gitignore` an die neuen Datenbereiche angepasst.
- Variantenoberflaeche unter `src/ma_variants/ui/app.py` nach P001 in getrennte Bereiche fuer Parameter/Optionen, Variantenraum, Auswahl, Namensgebung, Export, Ergebnisse und Status gegliedert.

### Added
- Planindex, Strukturreview, Cleanup-Plan, Implementierungshinweise und getrennte Nutzerentscheidungsdateien unter `docs/project/` ergaenzt.
- Vorbereitete Modulbereiche fuer `ma_weather`, `data/ma_analyse`, `data/ma_weather`, `config/ma_analyse` und `config/ma_weather` angelegt.
- `data/test_output/README.md` dokumentiert den Ordner als lokalen, semi-wichtigen Arbeits- und Smoke-Test-Bereich.
- Testbare UI-Services fuer manuelle Variantenauswahl, reproduzierbare Zufallsauswahl, Filterauswahl und Namensgenerierung ergaenzt.
- Modulbezogene Befehlsuebersichten fuer `ma_variants`, `ma_weather` und gemeinsame Projektbefehle unter `docs/*/commands_<modul>.md` ergaenzt.
- `docs/project/UPDATE_ROUTINES.md` als feste Codex-Routine fuer `update repo`, `direkt update repo` und `update planung` ergaenzt.

### Removed
- Leeren, nicht versionierten Ordner `scripts/` entfernt.
- Alte Root-Datenordner fuer Analyse-Eingaben, Nutzdaten und regulaere Ausgaben nach erfolgreichem Datentransfer entfernt.
- Alten leeren Dokumentenordner `data/documents/` entfernt; aktive Produkt- und Materialdatenblaetter liegen unter `data/catalogs/documents/`.

### Fixed
- `COMMAND_DOC` zeigt nun auf `docs/ma_analyse/commands_analyse.md`.
- GUI-Import korrigiert: `get_heating_year_template_defaults` wird aus `ma_analyse.settings.plot_templates` geladen.
- Falschen relativen Import in `src/ma_analyse/analysis/comfort/plots.py` korrigiert, damit die `ma_analyse`-Tests wieder gesammelt werden koennen.
- Comfort-Template-Builder akzeptiert den vom gemeinsamen Plot-Template-Dispatcher uebergebenen `plot_template_config`-Parameter.

## 0.4.0 - 2026-06-04

### Added
- Projektlokale Codex-Konfiguration unter `.codex/config.toml` ergaenzt, damit dieses Repository mit `workspace-write`, `on-request` und Windows-`unelevated`-Sandbox gestartet werden kann.
- `docs/PLAN.md` als Projektplan Version 1.0.0 fuer den modularen Varianten-, Simulations- und Bewertungskern ergaenzt.
- Projektvorbereitung mit `config/.gitkeep`, `docs/WORKFLOW.md`, `docs/DATA_MODEL.md`, `docs/DECISIONS.md` und Pflege ueber den zentralen Root-`CHANGELOG.md` ergaenzt.
- Abschnitt 1 umgesetzt: neues Paket `ma_variants` mit `parameter_catalog`, `option_catalog`, `variant_manager`, `validation` und zentralen dataclass-Modellen fuer Parameter, Optionen und Varianten ergaenzt.
- Tests fuer die neuen `ma_variants`-Modelle und einfache Pflichtfeldvalidierung ergaenzt.
- Pytest-Cacheprovider deaktiviert und `tmp_path` lokal unter `data/test_output/pytest_runs` bereitgestellt, um gesperrte Windows-Cache- und Tempordner ohne Einfluss auf die Testausfuehrung zu umgehen.
- Abschnitt 2 umgesetzt: kleine YAML-Beispielkonfigurationen fuer Parameter und Optionen sowie dateibasierte Importer mit Validierung und JSON-Importbericht ergaenzt.
- Tests fuer Parameterimport, Optionsimport, doppelte Keys, fehlende Optionsgruppenreferenzen und Importberichte ergaenzt.
- Abschnitt 3 umgesetzt: Variantenzaehlung, einfache In-Memory-Variantenerzeugung und JSON-Export fuer Beispielvarianten ergaenzt.
- Beispielausgabe `data/exports/example_variants.json` und Tests fuer Variantenanzahl, Filterung aktiver Optionen und Variantengenerierung ergaenzt.
- Abschnitt 4 umgesetzt: manuelle Auswahl, Filterauswahl, reproduzierbare Zufallsauswahl und einfache Namensgenerierung mit Duplikatspruefung ergaenzt.
- Beispielregeln `config/naming/example_naming_rules.yaml`, Beispielausgabe `data/exports/example_selected_named_variants.json` und Tests fuer Auswahl/Naming ergaenzt.
- Abschnitt 5 umgesetzt: Basisexporte unter `ma_variants.reporting` mit JSON, CSV und Exportbericht fuer ausgewaehlte Varianten ergaenzt.
- Beispielausgaben `data/exports/example_variant_overview.json`, `data/exports/example_variant_overview.csv` und `data/exports/example_variant_report.json` sowie Tests fuer Export und Reporting ergaenzt.
- Abschnitt 6 umgesetzt: SQLAlchemy-/Alembic-Grundstruktur fuer PostgreSQL unter `ma_variants.database` mit env-basierter Verbindungskonfiguration ergaenzt.
- Datenbankmodelle, erste Migration und Repository-Funktionen fuer `parameters`, `option_sets`, `option_values`, `variants`, `variant_values` und `import_logs` ergaenzt.
- Beispielkonfiguration `config/database/example.env` ohne echte Zugangsdaten sowie lokale SQLite-Tests fuer die DB-Repositorylogik ergaenzt.
- Abschnitt 7 umgesetzt: `system_catalog` mit Systemtemplates, Templatewerten, einfachen Dependency-Regeln und Template-Aufloesung ergaenzt.
- Beispielsysteme `HEAT_01`, `COOL_01`, `PV_01` und `VENT_01` unter `config/systems/example_system_templates.yaml` sowie Tests fuer die Template-Aufloesung ergaenzt.
- Datenbankmodelle, Alembic-Migration und Repository-Funktionen fuer `system_templates`, `system_template_values` und `dependency_rules` ergaenzt.
- Abschnitt 8 umgesetzt: `ida_export` mit vorbereiteter IDA-ICE-Uebergabestruktur je Variante ergaenzt.
- Beispielkonfiguration `config/export/example_ida_export.yaml`, Zielordner `data/ida_exports` und Tests fuer Ordnererzeugung, Metadaten, aufgeloeste Parameter und Exportlog ergaenzt.
- Abschnitt 9 umgesetzt: `simulation_results` als lesender Adapter fuer vorhandene `ma_analyse`-Ergebnisordner ergaenzt.
- Zuordnung von `*_nutzdaten`-Ordnern zu Varianten, Kennwertimport aus Raum-CSV-Dateien und JSON-Export fuer Simulationsergebnisse ergaenzt.
- Schnittstelle zur bestehenden Analysepipeline in `docs/WORKFLOW.md` dokumentiert, ohne bestehende Analysefunktionen umzubauen.
- Abschnitt 10 umgesetzt: `economic_analysis` mit generischen Kostenannahmen, Energiepreisen, Wirtschaftlichkeitsszenarien und einfacher Varianten-Kostenberechnung ergaenzt.
- Beispielannahmen unter `config/economic/example_economic_assumptions.yaml`, JSON-/CSV-Export fuer Kostenergebnisse und `docs/ECONOMIC_MODEL.md` ergaenzt.
- Datenbankmodelle, Alembic-Migration und Repository-Funktionen fuer `generic_system_costs`, `energy_prices`, `economic_scenarios` und `variant_cost_results` ergaenzt.
- Tests fuer Import, Kostenberechnung mit Simulationsergebnissen, Fallback auf Beispielwerte, Systemtemplate-Zuordnung, Export und DB-Speicherung ergaenzt.
- Abschnitt 11 umgesetzt: Produkt-, Material-, Dokument- und Quellenkataloge mit dataclass-Modellen und einfachen Importern ergaenzt.
- Beispielkataloge unter `config/products`, `config/materials`, `config/documents` und `config/sources` sowie Dokumentpfadstruktur unter `data/documents` ergaenzt.
- Datenbankmodelle, Alembic-Migration und Repository-Funktionen fuer `products`, `product_properties`, `materials`, `material_properties`, `documents` und `sources` ergaenzt.
- Tests fuer Produkt-/Materialimport, Dokument-/Quellenimport und DB-Speicherung der neuen Kataloge ergaenzt.
- Abschnitt 12 umgesetzt: lokale Streamlit-Oberflaeche unter `ma_variants.ui` fuer Parameter, Optionen, Variantenanzahl, Variantenauswahl, Basisexport und Ergebnisdateien ergaenzt.
- Streamlit als Projektabhaengigkeit ergaenzt und testbare UI-Servicefunktionen ohne eigene Fachlogik eingefuehrt.
- Startbefehl und manuelle Testhinweise fuer die lokale Oberflaeche in `docs/WORKFLOW.md` dokumentiert.

## 0.3.2 - 2026-05-28

### Changed
- Aktualisiert die Dokumentation der Plot-Template-Beispiele mit stabilen Referenzbildern unter `docs/examples/plot_templates/`.
- Erweitert die Standard-Ausgabeformatverwaltung um kompakte Plot-Template-Formate und neue Internal-Loads-/Energy-Balance-/Thermal-Room-Climate-Ziele.
- Verbessert die Benutzerführung im GUI-Dialog für Ausgabeformate.
- Verfeinert die Beschriftung des Heating-Year-Zeitstrahls.

## 0.3.1 - 2026-05-26

### Added
- `plot-template` um Comfort-PNGs, Comfort-PDF-Uebersichten, Heating-/Cooling-Barplots und Thermisches-Raumklima-Templates erweitert.
- Neuer CLI-Befehl `plot-template-examples` erzeugt die reproduzierbare Dokumentationsgalerie unter `docs/examples/plot_templates/` und aktualisiert `docs/plot_template_examples.md`.

### Changed
- GUI-Fenster bleibt unter Windows auch mit eigener Titelleiste in der Taskleiste sichtbar.

## 0.3.0 - 2026-05-26

### Added
- Plot-Templates fuer interne Lasten aus Licht, Belegung und Equipment ergaenzt.
- Plot-Templates fuer Energiebilanz-Uebersichten in Year/Month/Week/Day ergaenzt.

### Changed
- GUI-Plot-Template-Auswahl erlaubt fuer `internal-loads-room-comparison` mehrere Raeume.
- Internal-Loads-Templates auf drei sichtbare Datenreihen aus Personen, Geraeten und Beleuchtung ausgerichtet; Week/Day nutzen gestapelte Lastprofil-Balken.

## 0.2.3 - 2026-05-26

### Added
- `plot-template` um `heating-month`, `heating-week`, `heating-day`, `cooling-year`, `cooling-month`, `cooling-week` und `cooling-day` erweitert.
- Gemeinsamen Template-Katalog und Timeline-Template-Builder fuer Heating-/Cooling-Zeitansichten ergaenzt.
- Tests fuer neue Plot-Template-Auswahlwerte, Zeitvalidierung und PNG-Smoke-Laeufe ergaenzt.
- `docs/PLAN_STATUS.md` als persoenliche Planungssuebersicht ergaenzt.
- Archivordner `docs/plan_status/` fuer regelmaessige Planstatus-Staende ergaenzt.

### Changed
- GUI-Template-Auswahl zeigt alle Plot-Templates und blendet Zeitdetails fuer Monats-, Wochen- und Tages-Templates ein.
- Professor-Agent unter `.github/agents/Professor.md` auf die Masterarbeits-Auswertungssoftware und Dokumentationsregeln ausgerichtet.
- GUI-Reset springt nach dem Zuruecksetzen wieder auf den ersten Schritt `Befehl`.
- Planungsuebersicht nach `docs/PLAN_STATUS.md` verschoben; `CHANGELOG.md` bleibt im Projekt-Root.
- `docs/PLAN_STATUS.md` auf aktive offene Punkte reduziert; Vollstand nach `docs/plan_status/2026-05-26.md` archiviert.

### Docs
- Plot-Template-Promotion ueber geteilte Helper in `docs/architecture.md` dokumentiert.

## 0.2.2 - 2026-05-25

### Added
- CLI-Befehl `plot-template` fuer manuell anpassbare Diagramm-Vorlagen ergaenzt.
- Erste Vorlage `heating-year` fuer eine oder mehrere Varianten und genau einen Raum eingefuehrt.
- Neues Modul `analysis/templates/` fuer Plot-Templates und Overlay-Logik ergaenzt.
- Plot-Template-Defaults ueber `settings/plot_templates.toml` und Loader `settings.plot_templates` konfigurierbar gemacht.
- Heating-Year-Template um Aussenlufttemperatur, operative Temperatur, Sollwertband und freie Overlay-Linien aus Raum-CSV oder `REPORT-AUX.prn` erweitert.
- GUI um die Schritte `Template` und `Ueberlagerungen` fuer Plot-Templates ergaenzt.
- Rechten GUI-Bereich um einen `summary`-Kasten fuer abgeschlossene vorherige Schritte erweitert.
- Unteren GUI-Bereich um einen `log`-Button neben `settings` erweitert, der die bestehende Protokollansicht oeffnet oder ein laufendes Analyse-Logfenster fokussiert.
- Tests fuer Plot-Template-Validierung, PRN-Stundenaggregation, Overlay-Kataloge, freie Overlays, TOML-Defaults, CLI-Optionen und Logging ergaenzt.

### Changed
- GUI im Wizard-Stil ueberarbeitet: linke Schritt-Navigation, rechter Inhaltsbereich und getrennte Kaesten fuer `summary` und aktuellen Schritt.
- GUI startet ohne vorausgewaehlte sichtbare Auswahl; Pflichtauswahlen werden erst beim Start validiert.
- Aktiver GUI-Schritt wird mit kleinem Punkt markiert, ohne blaue Flaechenmarkierung.
- Nach Auswahl eines Befehls springt die GUI automatisch zum naechsten sichtbaren Schritt.
- Automatisches Weitergehen auf weitere Einzelauswahl-Schritte erweitert; bei mehrteiligen Optionen wartet die GUI bis die Pflichtauswahl vollstaendig ist.
- Drei-Punkte-Menue aus der Titelleiste entfernt; Tools-Menue wird ueber `settings` geoeffnet.
- Rechte GUI-Scrollbar wird nur eingeblendet und per Mausrad genutzt, wenn der rechte Inhalt ueber das sichtbare Feld hinausgeht.
- Temperaturachsen-Eingaben in den Schritt `Ueberlagerungen` verschoben.
- `plot-template` kann nun mehrere Varianten aus der GUI-/CLI-Auswahl verarbeiten und erzeugt pro Variante ein eigenes Template-PNG.
- Heating-Year-Plot-Layout verfeinert: X-Achse naeher am Zeitstrahl, Abstand zur Monatsbeschriftung auf ca. 5 mm gesetzt und Abstand zwischen Zeitstrahl-Beschriftung und `Stunden [h]` auf ca. 3 mm reduziert.
- Positionen von Legende und `Stunden [h]` im Heating-Year-Plot getauscht.
- Jahres-Zeitstrahl trennt Grid-Markierungen oberhalb der Hauptlinie von 1000er-Stundenticks unterhalb der Hauptlinie.
- `plot-template` in die Laufprotokollierung aufgenommen.

### Docs
- `README.md`, `docs/commands.md` und `docs/architecture.md` um `plot-template`, Plot-Template-Config und Setup-/Start-Hinweise erweitert.
- `*.toml` als Package-Daten fuer `ma_analyse.settings` aufgenommen.
- Pytest-Testpfad in `pyproject.toml` dokumentiert.

## 0.2.1 - 2026-05-25

### Changed
- Analysecode weiter modularisiert: gemeinsame Energy-Logik fuer Heating/Cooling, Tabellenpaket fuer Excel-Berichte und Comfort-Module fuer Daten, Zonen, Tabellen und Plots ergaenzt.

## 0.2.0 - 2026-05-24

### Added
- `CHANGELOG.md` als zentrale Aenderungshistorie eingefuehrt.
- Laufprotokolle mit Schritt- und Gesamtlaufzeiten fuer Analysebefehle ergaenzt.
- `data/`-Ordnerstruktur mit versionierten Platzhalterdateien vorbereitet.
- Minimale Tests fuer CLI, Konfiguration, Logging, Varianten und Zeitfenster ergaenzt.

### Changed
- Projekt von losen Skripten zu einem Paket mit `src/ma_analyse` umgebaut.
- Code fachlich in `app`, `core`, `preprocessing`, `analysis`, `analysis/components`, `gui` und `settings` strukturiert.
- CLI-Einstieg auf `python -m ma_analyse ...` und `ma-analyse ...` ausgerichtet.
- Datenordner auf `data/input`, `data/database`, `data/output` und `data/test_output` umgestellt.
- `requirements.txt` auf direkte Runtime-Abhaengigkeiten reduziert.
- GUI so angepasst, dass der `all`-Befehl automatisch alle Raeume auswaehlt.

### Removed
- Alte Skriptstruktur unter `Skripte/` als Hauptschnittstelle entfernt.
- Uebergangsmodul `pipeline.py` entfernt, nachdem CLI, Commands und GUI ausgelagert wurden.
- Alte Root-Module wie `config.py`, `commands.py`, `heating.py`, `cooling.py`, `prepare.py`, `comfort.py` und `analyze.py` durch Paketmodule ersetzt.

## 0.1.0 - 2026-05-24

### Added
- Erster Paketstand fuer `ma_analyse` mit zentralem CLI-Einstieg.
