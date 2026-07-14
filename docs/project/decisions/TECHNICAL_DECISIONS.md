# Entscheidungen

Stand: 2026-07-13

Dieses Dokument sammelt technische und architektonische Entscheidungen. Echte Nutzerentscheidungen stehen getrennt in `USER_DECISIONS_MASTERTHESIS_CODE.md`.

## Entscheidung 1: Modularer Aufbau

Das Projekt wird modular weiterentwickelt. Der bestehende Analysecode bleibt als eigenes Analyse-Subsystem erhalten. Neue Funktionen fuer Parameterkatalog, Optionskatalog, Variantenmanagement, Auswahl, Naming, IDA-Export, Wirtschaftlichkeit und Reporting werden schrittweise getrennt vorbereitet.

Begruendung:

- Die vorhandene Analysepipeline ist bereits nutzbar und soll nicht durch einen grossen Umbau gefaehrdet werden.
- Neue fachliche Bereiche koennen einzeln getestet und dokumentiert werden.
- Spaetere Erweiterungen wie Produktkatalog, Materialkatalog und Weboberflaeche erhalten klare Grenzen.

## Entscheidung 2: PostgreSQL als spaetere zentrale Datenbank

PostgreSQL bleibt als spaetere zentrale Zieldatenbank vorgesehen. SQLAlchemy-Modelle, Alembic-Migrationen und Repository-Funktionen sind im Variantenkern vorbereitet.

Begruendung:

- Varianten, Parameter, Optionswerte, Systemvorlagen, Importlogs und spaetere Bewertungsergebnisse brauchen stabile Relationen.
- PostgreSQL ist robust fuer strukturierte Projektdaten und spaetere Auswertungen.
- SQLAlchemy und Alembic bilden die technische Grundlage fuer Modelle und Migrationen.

## Entscheidung 3: Bestehende Analysefunktionen bleiben unveraendert

Die vorhandenen Module unter `src/ma_analyse` werden in diesem Schritt nicht umgebaut, verschoben oder geloescht.

Begruendung:

- Sie bilden den aktuellen funktionsfaehigen Kern fuer Simulationsergebnis-Auswertung.
- Der neue Variantenkern soll zunaechst als Erweiterung daneben entstehen.
- Eine spaetere Anbindung erfolgt bewusst ueber Adapter oder klar definierte Schnittstellen.

## Entscheidung 4: Dokumentation vor Fachlogik

Vor der Implementierung neuer Varianten-, Datenbank- oder Exportlogik wird zuerst die Projektstruktur dokumentiert.

Begruendung:

- Die fachlichen Grenzen werden klarer.
- Der Umsetzungsumfang von Version 1 bleibt kontrollierbar.
- Spaetere Codeaenderungen lassen sich gegen Plan, Workflow und Datenmodell pruefen.

## Entscheidung 5: Modulare Dokumentationsstruktur

Die Dokumentation wird nach Projektorganisation und Fachmodulen gegliedert.

Begruendung:

- Das Projekt umfasst inzwischen Analyse, Variantenkern, spaetere Wetterdatenanalyse und Bewertung.
- Eine flache `docs/`-Struktur wuerde Planstatus, Fachworkflow und Entscheidungen vermischen.
- Modulbezogene Dokumente lassen sich gezielter pflegen.

## Entscheidung 6: ma_variants zuerst modular migrieren

Die Konfigurations- und Datenbereiche des neuen Variantenkerns werden zuerst modularisiert.

Begruendung:

- `ma_variants` ist neuer und klarer gekapselt als die bestehende Analysepipeline.
- Die Migration ist risikoaermer als eine sofortige Umstellung von `ma_analyse`.
- Tests koennen die neuen Pfade direkt pruefen.

## Entscheidung 7: ma_analyse-Datenpfade hart migriert

`ma_analyse` nutzt ab dem 2026-06-04 nur noch die Modulpfade `data/ma_analyse/ida_imports`, `data/ma_analyse/database` und `data/ma_analyse/output`.

Begruendung:

- Die Analysepipeline ist damit konsistent zur modularen Datenstruktur.
- Alte Root-Pfade werden nicht als Fallback erhalten.
- `data/test_output/` bleibt bewusst separat als lokaler Smoke-Test- und Arbeitsordner.

## Entscheidung 8: Produkt- und Materialdokumente als Katalogdaten

Produkt- und Materialdokumente liegen unter `data/catalogs/documents/` und nicht direkt im Variantenmodul.

Begruendung:

- Produkt- und Materialdaten betreffen spaeter auch Quellen, Bewertung und Wirtschaftlichkeit.
- PostgreSQL speichert nur Pfade und Metadaten, nicht die Datenblaetter selbst.
- Der Katalogbereich bleibt fachlich klarer als eine Ablage unter `data/ma_variants/`.

## Entscheidung 9: Dokumentierte Codex-Routinen statt Python-CLI fuer Repo-Updates

Repo-Updates, direkte Repo-Updates und Planungsupdates werden als dokumentierte Arbeitsroutinen gefuehrt.

Begruendung:

- Die Ablaeufe betreffen Git, Changelog, Versionierung und Planstatus, nicht die Fachlogik des Python-Pakets.
- Eine Dokumentationsroutine ist fuer den Nutzer transparenter als ein zusaetzlicher CLI-Befehl.
- Die Dateien `pyproject.toml`, `src/ma_analyse/__init__.py`, `CHANGELOG.md`, `PLAN_INDEX.md`, `PLAN_STATUS.md` und die Entscheidungsdateien bleiben explizit als Pruefstellen dokumentiert.

## Entscheidung 10: Plot-Template-Varianten ueber Template-Namen statt Modusoption

Heating-Overlay und Cooling-Absolute werden als eigene Plot-Template-Namen gefuehrt.

Begruendung:

- Die Galerie unter `docs/examples/plot_template_analyse/` kann fuer jede fachliche Darstellung ein stabiles Referenzbild enthalten.
- Die CLI bleibt fuer einzelne Diagrammideen eindeutig: `heating-overlay` und `cooling-absolute-year` beschreiben direkt die gewuenschte Darstellung.
- Bestehende Templates bleiben rueckwaertskompatibel nutzbar, ohne eine zusaetzliche globale Modusoption einzufuehren.

## Entscheidung 11: ma_weather getrennt von ma_analyse

Das Wettermodul wird als eigenes Paket `src/ma_weather/` aufgebaut. TRY-Dateien
bleiben lokale Eingangs- und Randbedingungsdaten unter `data/ma_weather/input/`
und werden nicht mit den IDA-ICE-Zonenwerten aus `ma_analyse` vermischt.

Begruendung:

- Wetterdaten beschreiben Randbedingungen, waehrend `ma_analyse` Simulationsergebnisse auswertet.
- Reale TRY-Dateien sollen lokal bereitgestellt und nicht im Git-Repo versioniert werden.
- Die spaetere Verbindung zu Varianten kann ueber den technischen `weather_key` erfolgen.

## Entscheidung 12: ma_analyse-Service zuerst als Fassade umsetzen

Die UI-neutrale Service-Schnittstelle fuer `ma_analyse` wird zuerst als Fassade
ueber bestehender Logik umgesetzt. `AnalysisConfig`, `AnalysisResult` und
`run_analysis(config)` ermoeglichen die spaetere UI-Anbindung, ohne die
bestehende CLI, Tkinter-GUI oder Fachmodule sofort umzubauen.

Begruendung:

- Die fruehere Tkinter-Hauptdatei war stark mit Tkinter-State, Worker-Thread
  und Pipelineaufrufen gekoppelt; die Datei liegt inzwischen unter
  `src/ma_ui/tkinter_app/module_views/analyse/app.py`.
- `src/ma_analyse/app/commands.py` ist bereits ein guter Einstiegspunkt, aber
  noch CLI-nah durch `argparse.Namespace`, `print()` und `SystemExit`.
- Eine Fassade reduziert Risiko, weil sie bestehende Funktionen nutzt und
  spaeter schrittweise bessere Rueckgabeobjekte ermoeglicht.
- Streamlit kann spaeter ueber `ma_ui` dieselbe Service-Schicht nutzen, ohne
  Fachlogik in der Oberflaeche zu duplizieren.
- P029 fuehrt deshalb zuerst strukturierte Schritt-Ergebnisse ein, bevor
  `heating.py`, `cooling.py` oder die Tkinter-Analyse groesser zerlegt werden.

## Entscheidung 13: ma_workflow und ma_ui zuerst als minimale Shell

`ma_workflow` wird zuerst als neutrale Orchestrierungsschicht mit Workflow-
Katalog und Analyse-Adapter umgesetzt. `ma_ui` wird zuerst als minimale
Streamlit-Shell mit Startseite, Navigation, Projektzustand und Analyse-Seite
umgesetzt.

Begruendung:

- Die neue UI braucht stabile Einstiegspunkte, darf aber keine Fachlogik
  enthalten.
- `ma_workflow` trennt UI-Bedienaktionen von Fachmodulaufrufen.
- Die bestehende Tkinter-GUI bleibt unveraendert, bis ein eigener
  Legacy-Auslagerungsslice freigegeben ist.
- Weitere Fachseiten koennen spaeter einzeln angebunden werden.

## Entscheidung 14: P005-Zielstruktur strenger als aktueller Codezustand

Die aktuelle `ma_ui`- und `ma_workflow`-Implementierung ist ein bewusst kleiner
Zwischenstand. Die Zielstruktur sieht spaeter eine klarere Aufteilung vor:

- `ma_ui/main_dashboard.py`
- `ma_ui/workflow_view.py`
- `ma_ui/pre_process_view.py`
- `ma_ui/post_process_view.py`
- `ma_ui/shared/`
- `ma_ui/module_views/`
- `ma_workflow/workflow_manager.py`
- `ma_workflow/dashboard_actions.py`
- `ma_workflow/pre_process_runner.py`
- `ma_workflow/post_process_runner.py`
- `ma_workflow/feedback_router.py`

Begruendung:

- Die UI soll den Gesamtworkflow fuehren und gemeinsame Komponenten nicht in
  einzelnen Seiten duplizieren.
- `ma_workflow` soll Button-/Dashboard-Aktionen von Fachservices trennen.
- Eine sofortige Umbenennung bestehender Dateien waere unnoetiges Risiko,
  weil Tests und Importpfade betroffen sind.

## Entscheidung 15: Tkinter wird nicht technisch nach Streamlit uebersetzt

Die Tkinter-Analyse in `src/ma_ui/tkinter_app/module_views/analyse/` wird als
fachliche Ablaufquelle genutzt, aber nicht als technische Vorlage fuer
Streamlit.

Begruendung:

- Tkinter-Widgets, Messageboxen, Worker-Threads und GUI-State sind eng mit der
  aktuellen Datei `src/ma_ui/tkinter_app/module_views/analyse/app.py`
  gekoppelt.
- Streamlit braucht eine andere Zustands- und Anzeigeform.
- Die fachliche Analyse muss ueber neutrale Services nutzbar bleiben.

Technische Folge:

- Allgemeine Anzeige- und Bedienbausteine entstehen spaeter in `ma_ui/shared/`.
- Analysebezogene Bedienung entsteht spaeter in
  `ma_ui/module_views/analyse_view.py`.
- Fachliche Analysefunktionen bleiben in `ma_analyse`.
- `ma_analyse` bekommt keine neuen Tkinter-Startpfade oder
  Kompatibilitaetswrapper.

## Entscheidung 16: Plot-Template-Ausgabemodus wird zentral orchestriert

`single` und `compare` werden als fachliche Ausgabemodi der
Plot-Template-Sandbox in der gemeinsamen Template-Orchestrierung umgesetzt.

Technische Regeln:

- `single` verarbeitet jede Variante-Raum-Kombination als eigene Ausgabe.
- Heating-/Cooling-Zeitreihen und Heating-Overlay werden bei `compare`
  datenreihenbasiert in einer gemeinsamen Grafik gerendert.
- Komplexe Sammeltemplates, deren Renderer bereits mehrere fachliche Elemente
  enthalten, werden bei `compare` als beschriftete Teilplots in einer
  gemeinsamen Vergleichsgrafik gebuendelt.
- Die UI gibt Achsen-, Overlay- und Ausgabeeinstellungen ueber die
  UI-neutralen Modelle und Services an die Template-Orchestrierung weiter.

Begruendung:

- Tkinter, Streamlit und Backend sollen dieselbe Bedeutung von
  `single`/`compare` verwenden.
- Bestehende spezialisierte Renderer bleiben erhalten und werden nicht durch
  eine grosse generische Plot-Engine ersetzt.
- Der Ansatz ist fuer den aktuellen Masterarbeitsumfang nachvollziehbar und
  kann spaeter templateweise weiter vereinheitlicht werden.

## Entscheidung 17: ma_workflow ist die zentrale Metadatenquelle

Phasen, Module, Workflow-Schritte, Statuswerte, Abhaengigkeiten und naechste
Schritte werden zentral in `ma_workflow.catalog` gepflegt.

Technische Folgen:

- Navigation und Dashboard leiten ihre Inhalte aus diesem Katalog ab.
- Geplante Module werden nicht mehr ueber getrennte statische UI-Listen
  beschrieben.
- `list_workflow_phases()`, `list_module_definitions()` und
  `get_module_definition()` bilden die oeffentliche Leseschnittstelle.
- Historische IDA-spezifische Modul-, Schritt-, Seiten- und Aktionsschluessel
  werden kontrolliert auf die allgemeinen Simulationsschnittstellen
  abgebildet.

## Entscheidung 18: Geplante Module erhalten leichte Pakete

Ein bestaetigtes Zielmodul darf vor seiner Fachimplementierung als
importierbares Paket mit Modulbeschreibung angelegt werden.

Technische Regeln:

- Keine leeren `services.py`, `models.py`, Konfigurationen oder Tests ohne
  konkrete Verantwortung.
- Der fachliche Status bleibt `planned` oder `partial`, bis belastbare Logik
  und Tests vorhanden sind.
- Modul-Infoseiten lesen ihre Inhalte aus dem zentralen Katalog.
- Die Projektdokumentation bleibt unter `docs` und wird nicht als Python-Paket
  gespiegelt.

## Entscheidung 19: Eingabeformate liegen hinter Adaptern

Externe Dateien werden nicht zu internen Fachmodellen. Ein Adapter erkennt das
Format, liest den vorhandenen Inhalt und erzeugt neutrale Daten plus
`ImportDiagnostic` und Quellenmetadaten.

Technische Folgen:

- Quellenwahl erfolgt je Modul.
- Originaldateien bleiben unveraendert.
- Manuelle Ergaenzungen und Ueberschreibungen werden protokolliert.
- YAML ist der erste menschenlesbare Projektstand, aber keine dauerhaft
  festgeschriebene Formatschnittstelle.
- Datenbanktabellen werden erst nach stabilen Fachmodellen festgelegt.

## Entscheidung 20: Stage 3 verwendet versionierte Standards Profiles

Der kanonische Name lautet
`ma_analyse.stage_3_standards_compliance`. Deutsche Normen bilden die ersten
Profile; internationale Normen koennen spaeter dieselbe Schnittstelle nutzen.

Technische Folgen:

- Jede Regel referenziert Norm, Ausgabe, Abschnitt, Anwendungsbereich,
  Einheit und Berechnungsverfahren.
- Ergebnisse sind `pass`, `fail`, `warning` oder `not_evaluable`.
- `stage_3_verification` bleibt nur als Uebergangsalias.
- Bestehende Komfortzonen und Grenzwerte werden nicht ungeprueft als
  Normregeln uebernommen.

## Entscheidung 21: ParameterSnapshot und RunManifest bilden Freigabegrenzen

`ma_parameters` liefert versionierte, freigegebene Parametersnapshots. Der
`ParameterSnapshot` v1 bleibt der kompatible LoD-1-Eingangsstand; der
`BaselineParameterSnapshot` v2 bildet die stabilere Freigabegrenze mit
Scope, Parameterwert-ID, Quellenreferenzen und Content-Hash.
`ma_simulation_setup` referenziert diese Staende zusammen mit Projekt,
Varianten, Wetter und Modellstand in einem unveraenderlichen Run-Manifest.

Technische Folgen:

- Stage-1-Vorschlaege erzeugen spaeter neue Snapshot-Versionen oder
  referenzierte Ergebnisparameter, ohne die Baseline still zu veraendern.
- `ma_variants` konsumiert Baseline- und Variation-Spezifikationen, erzeugt
  aber keine neuen Eingangsparameter.
- Varianten und Runs bleiben auf ihren Eingabestand rueckfuehrbar.
- P009 darf erst hinter dem validierten Run-Manifest technisch weitergehen.

## Entscheidung 22: Konfiguration folgt fachlicher Verantwortung

`ma_project` besitzt Simulationsprogrammliste und neutrales
Varianten-Benennungsprofil. `ma_parameters` besitzt Parameterdefinitionen,
Optionsgruppen und ausgewaehlte Werte. `ma_variants` konsumiert diese Staende
und erzeugt daraus Varianten.

Technische Folgen:

- Bestehende Parameter-, Options- und Naming-Dateien unter `ma_variants`
  bleiben bis zu einer kontrollierten Migration lesbar.
- Neue fachliche Konfiguration wird nicht dauerhaft unter `ma_variants`
  abgelegt.
- Produkt- und Materialbezeichnungen bleiben in neutralen Katalogen.
- Programmspezifische Objekt- und Exportcodes werden erst in Adaptern
  aufgeloest.

## Entscheidung 23: Vorlagen- und Dateischutz ist moduluebergreifend

Versionierte Vorlagen sind schreibgeschuetzt. Eigene Dateien werden nur in
festgelegten lokalen Modulpfaden gespeichert.

Technische Folgen:

- Bei `Als neue Datei speichern` fuehrt eine Namenskollision zu einem Fehler
  und einer neuen Nutzereingabe; es gibt keinen automatischen Ersatznamen.
- Nur eine bereits geladene eigene Datei darf nach ausdruecklicher
  Bestaetigung ueberschrieben werden.
- Pfadpruefungen verhindern Schreibzugriffe ausserhalb der erlaubten lokalen
  Konfigurationsordner.
- Serializer und Fachmodelle werden so getrennt, dass YAML spaeter um weitere
  Formate ergaenzt oder ersetzt werden kann.

## Entscheidung 24: P028 verwendet einen gemeinsamen UI-Sitzungsstand

`ma_project`, `ma_parameters` und `ma_variants` verwenden in Streamlit ein
gemeinsames, UI-neutrales Zustandsobjekt. Ein Direkteinstieg initialisiert
dieses Objekt aus den versionierten Vorlagen.

Technische Folgen:

- `ma_project` liefert Programmliste und neutrales Benennungsprofil.
- `ma_parameters` liefert die aktive Demo-Optionsauswahl.
- `ma_variants` erzeugt und benennt den Variantenraum, besitzt die beiden
  Konfigurationen aber nicht.
- Fachliche Querverweise speichern ein Ruecksprungziel; normale
  Workflow-Navigation verwirft es.
- Der Sitzungsstand ist keine dauerhafte Persistenz und kein produktiver
  `ParameterSnapshot`.

## Entscheidung 25: P010 trennt Fachpruefung, Freigabe und Sitzungsnachweis

Fachmodule behalten ihre lokalen Pruefregeln. `ma_validation` vereinheitlicht
Diagnosemeldungen und Freigabeentscheidungen. `ma_core` stellt
Quellenmetadaten, IDs und ein append-only JSONL-Sitzungslog bereit.

Technische Folgen:

- Fehler koennen niemals freigegeben werden.
- Warnungen erfordern `keep_blocked` oder `release_with_warnings`.
- Fehler- und warnungsfreie Staende erhalten `automatic_release`.
- Bestehende Fachmodelle bleiben kompatibel und werden nur um neutrale
  Ergebnisse ergaenzt.
- `logs/*.log` bleibt fuer menschenlesbare Analyseausgaben erhalten;
  `logs/sessions/*.jsonl` dokumentiert moduluebergreifende Ereignisse.
- Eine Datenbankmigration ist kein Bestandteil von P010.

## Entscheidung 26: ma_weather-Ereignisse bleiben UI-neutral

Kritische Wetterereignisse werden in `ma_weather` als strukturierte
Fachobjekte berechnet und erst danach in Streamlit dargestellt. Die
Berechnung nutzt ausschliesslich den bewusst ausgewaehlten Wetterdatensatz.

Technische Folgen:

- `weather_events.py` enthaelt die fachliche Ereigniserkennung ohne
  Streamlit-Abhaengigkeit.
- `WeatherAnalysisResult` kann die erkannten Ereignisse mit dem Import- und
  Validierungsergebnis transportieren.
- Die Wetterseite formatiert Ereignisse nur fuer Anzeige und Vormerkung; eine
  automatische P021-Uebergabe ist kein Bestandteil dieses Slices.
- Jahres-, Sommer- und Winterdateien bleiben getrennte Katalogeintraege.
- Die YAML-basierte Katalog- und Statuslogik bleibt bestehen, bis ein
  Datenbankmodell separat freigegeben wird.

## Entscheidung 27: ma_parameters uebernimmt Wetter nur als freigegebenen Verweis

`ma_parameters` importiert oder parst keine TRY-Dateien. Der P015-S3a-
Eingangspaketvertrag uebernimmt Wetter nur als aktivierten Projekt-Default aus
`ma_weather` inklusive `weather_key`, Quellen-/Importreferenz,
Datensatzrolle, Standort, Jahrtyp und Freigabestatus.

Technische Folgen:

- `ma_weather` bleibt Eigentumer von TRY-Dateien, Import, Validierung,
  Aktivierung und Projekt-Default.
- `ma_parameters` braucht fuer Baseline und Varianten nur stabile,
  versionierte Quellenreferenzen und fachliche Parameterwerte.
- Die Grenze verhindert doppelte Wettervalidierung und haelt P015 kompatibel
  mit spaeteren Freshness- und Fingerprint-Slices.

## Entscheidung 28: Projektlokales Codex-Council mit kontrollierter Autonomie

Das Repository verwendet `gpt-5.6-terra` mit mittlerem Reasoning als
wirtschaftlichen Hauptagenten. Spezialisierte Subagenten werden selektiv nach
Aufgabe eingesetzt: Luna fuer read-only Exploration, Tera fuer freigegebene
Umsetzungspakete und Sol fuer technische oder wissenschaftliche
Qualitaetspruefungen.

Technische Folgen:

- Dauerhafte Arbeits- und Freigaberegeln stehen im Root-`AGENTS.md`.
- Projektbezogene Rollen liegen als TOML-Dateien unter `.codex/agents/`.
- Vor einer Umsetzungsfreigabe arbeiten alle Council-Mitglieder read-only.
- Von den Council-Subagenten darf nach der Freigabe nur der
  `implementation_engineer` innerhalb eines eindeutig zugewiesenen Datei-
  oder Modulumfangs schreiben; der Hauptagent darf den freigegebenen Umfang
  weiterhin selbst umsetzen.
- Der Tera-Hauptagent bleibt fuer Integration, Validierung und Abschluss
  verantwortlich; parallele Schreibzugriffe auf dieselben Dateien sind nicht
  erlaubt.
- Sol-Befunde werden als `Blocker`, `Wichtig` oder `Optional` klassifiziert
  und erweitern den freigegebenen Umfang nicht automatisch.
- Dokumentierte Sammelbefehle bleiben vorab freigegebene Ausnahmen.
- GPT-5.5 bleibt Fallback oder ausdrueckliche Vergleichsinstanz und ist kein
  regulaeres Council-Mitglied.
- Node.js wird fuer das Council nicht als Projektabhaengigkeit eingefuehrt,
  weil Codex die Rollen direkt aus TOML-Konfigurationen laden kann.

## Entscheidung 29: Compliance wird vor geschuetzten Operationen technisch erzwungen

`ma_core.compliance` bildet eine eigene rechtlich-technische Schutzgrenze vor
Datei-, Parser-, Upload-, Index- und Simulationsoperationen. Sie bleibt von
der fachlichen Datenvalidierung und Freigabe in `ma_validation` getrennt.

Technische Folgen:

- Ein Metadaten-Preflight erfasst Dateiname, Endung, Groesse, SHA-256,
  Herkunfts- und Lizenzstatus, bevor semantischer Inhalt verarbeitet wird.
- `green` erlaubt nur den dokumentierten Umfang. `yellow` bleibt technisch
  gesperrt, bis Nutzerbestaetigung und alle geforderten Rechte- oder
  Hochschulreferenzen vorliegen. `red` und `unknown` sind nicht
  uebersteuerbar.
- Policies unterscheiden IDA/EQUA, DIN/Nautos, DWD und gemeinsame
  Stop-Regeln. Eine technische Moeglichkeit oder ein No-Training-Angebot
  ersetzt keine Rechtefreigabe.
- Das append-only Audit speichert keine geschuetzten Volltexte, Geheimnisse
  oder absoluten lokalen Pfade.
- Der DWD-TRY-2011-Konverter ist der erste angebundene Adapter. Er verlangt
  vor `.idm`-/`.PRN`-Zugriff Nutzerbestaetigung und Bezugsrechtsreferenz.
- Bestehende Fachmodelle bleiben kompatibel; weitere Adapter werden jeweils
  an ihrer oeffentlichen Modulgrenze angebunden.

## Entscheidung 30: Compliance-Audit ist ein objektbezogenes Council-Gate

Der read-only `compliance_auditor` wendet das projektweite Compliance-System
auf Codex-Arbeitsvorgaenge an. Er ist von `quality_auditor`, `professor` und
der technischen Laufzeitdurchsetzung in `ma_core.compliance` getrennt.

Technische Folgen:

- Die Rolle liegt unter `.codex/agents/`, nutzt Sol mit hohem Reasoning und
  besitzt keinen Schreibzugriff.
- Neue Plaene und Projektinputs durchlaufen vor jedem Inhaltszugriff einen
  Metadaten-Preflight; erst nach belegter Inhalts- und KI-Verarbeitung darf
  der Agent den Inhalt pruefen.
- Ein zulaessiges Plandokument mit einem Umsetzungsrisiko bleibt in Planindex
  und Planstatus sichtbar; der Blocker sperrt die Umsetzung, nicht die
  Dokumentation des Risikos.
- Ein gesperrtes Inbox-Original bleibt unveraendert an seinem aktuellen
  Eingangspfad. `needs_review/` nimmt nur Metadatenhinweise oder freigegebene
  Arbeitskopien auf; unabhaengige, unkritische Objekte koennen weiterlaufen.
- Vor Release oder Veroeffentlichung muss eine gueltige Entscheidung den
  konkreten Stand und die beabsichtigte Weitergabe abdecken.
- Der Hauptagent besitzt und dokumentiert die Prozessentscheidung mit
  Belegreferenz. Materielle oder gelbe Entscheidungen erfordern eine
  dokumentierte menschliche Bestaetigung und alle geforderten Rechtebelege.
- Eine Risikoakzeptanz ersetzt keinen erforderlichen Rechte- oder
  Genehmigungsnachweis. Der Agent erteilt selbst keine Freigabe.

Offener Implementierungspunkt:

- `ComplianceService` gibt aktuell die erste passende Regel zurueck. Trifft
  eine bestaetigte rote Stop-Regel zugleich mit fehlenden Herkunfts- oder
  Lizenzbelegen auf, kann deshalb `unknown` statt `red` protokolliert werden.
  Die Operation bleibt gesperrt, die Klassifikation folgt aber noch nicht der
  dokumentierten Prioritaet `red > unknown > yellow > green`. Eine Korrektur
  in `src/ma_core/compliance/service.py` mit kombiniertem Regressionstest ist
  ein separater Codeumfang.

## Entscheidung 31: Regelwerksrechte werden nach Bezugsweg getrennt

Die Normen-Compliance behandelt eine technische Regel nicht pauschal nach
Dateityp oder Plattform. Vor jeder materiellen Nutzung werden Regelwerk,
Rechteinhaber, Bezugsweg, autorisierter Nutzer und anwendbare
produktspezifische oder individuelle Bedingungen bestimmt.

Technische Folgen:

- DBIS belegt den institutionellen Zugang, aber nicht automatisch einen
  DIN-Media-Vertragstyp oder Maschinenverarbeitungsrechte.
- VDE-Webshop, VDE-NormenBibliothek, VDI ueber DIN Media/Nautos und VDI-VOB
  besitzen getrennte Quellenprofile unter `docs/compliance/din_nautos/`.
- `unknown` bezeichnet fehlenden Vertragsbeleg. Ein ausdrueckliches
  KI-/TDM-Verbot erzeugt `red`; eine potenzielle Einzelgenehmigung aendert den
  aktuellen Stop-Status erst nach passendem schriftlichem Nachweis.
- Nur unabhaengige, begrenzte eigene Fachlogik ohne Uebernahme oder
  Rekonstruktion geschuetzter Regeln kann `green` sein. Normbasierte
  Parameter, Formeln und Softwarelogik bleiben bis zur Einzelfallpruefung
  `yellow`.
- Die Dokumentation erweitert noch keine Laufzeit-Enums. Eigene
  VDE-/VDI-SourceTypes und ihre Regressionstests bleiben ein separater
  freizugebender Code-Slice.
