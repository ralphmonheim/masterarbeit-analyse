# Entscheidungen

Stand: 2026-07-15

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

## Entscheidung 32: Project-OS nutzt geschichtete Wahrheiten und positive Scan-Allowlists

Das repo-lokale Codex Project Operating System erweitert die vorhandene
Governance, ohne eine zweite Ablauf-, Status- oder Compliance-Architektur zu
erzeugen.

Technische Folgen:

- P031 ist der einzige aktive Plan fuer den datierten Repository-Audit, das
  temporaere Konfliktregister, den Tool-Capability-Snapshot und den Backlog.
- `AGENTS.md`, `.codex/config.toml`, `.codex/agents/*.toml`,
  `docs/project/UPDATE_ROUTINES.md`, die Decision-Dateien und
  `docs/compliance/` behalten jeweils eine klar getrennte Aufgabe.
- `.agents/skills/` enthaelt nur duenne Router. Ablaufdetails bleiben in
  `UPDATE_ROUTINES.md` und werden nicht in Skills kopiert.
- Allgemeine Bestands-, Skill- und spaetere Graph-Scans verwenden positiv
  `git ls-files`. Ignorierte Dateien gelten nicht als lesefreigegeben.
- Ein Contract-Test prueft Runtime-Grenzen, Agentensandboxes, Skills,
  Triggerownership und ausgeschlossene geschuetzte Arbeitsdaten.
- `.codex/agents/professor.toml` ist fuer Codex fuehrend;
  `.github/agents/Professor.md` bleibt ein gekennzeichneter Surface-Adapter.
- Graphify, neue MCPs, globale Codex-Aenderungen, Hook-Aenderungen,
  Obsidian-/Zotero-Schreibwege und geschuetzte Inhaltsverarbeitung werden
  nicht Teil der lokalen Baseline und brauchen einen eigenen freigegebenen
  Folgeslice.

## Entscheidung 33: Delegierter P014-S3a/P015-S3b-prep-Referenzhandover

Gemass UD-089 wird der lokale, reversible Vorbereitungsslice
`P014-S3a/P015-S3b-prep: ReleasedTechnicalHandover` vor P032-W2 umgesetzt.
Er ist keine neue Nutzerentscheidung ueber Architektur, Daten oder externe
Systeme, sondern die dokumentierte Ausfuehrung innerhalb der delegierten
Council-Mehrheitsfreigabe.

Council-Vote und Scope:

- Mira empfiehlt den engen Referenzhandover vor P032-W2, weil die vollstaendige
  P015-S3b-Werteherkunft noch nicht vorliegt.
- Vera bestaetigt den additiven Vertrag mit Hash-/Modell-ID-Pruefung,
  unveraenderlichen Interface-Referenzen und kompatibler Quellen-ID.
- Justus bestaetigt den reinen lokalen Metadatenumfang ohne reale oder
  geschuetzte Daten, externe Verarbeitung oder weitere Spezialgates.
- Damit liegt eine einstimmige 3/5-Mehrheit fuer genau diesen Scope vor.

Technische Folgen:

- `ma_technical` besitzt `ReleasedTechnicalHandover` als unveraenderlichen,
  payloadfreien Verweis auf eine freigegebene, hashkonsistente v2-Revision.
- `ma_parameters` bildet ausschliesslich Modell-ID, Revisions-ID, Content-Hash
  und Freigabestatus in eine bestehende `ParameterSourceReference` ab. Die
  kompatible Quellen-ID `ma_technical:<technical_model_id>` bleibt erhalten.
- P013-Zonenfingerprint, v2-Herkunft der vorhandenen Parameterwerte,
  vollstaendiges P015-S3b-Eingangspaket, P014-S4-YAML, UI, Persistenz,
  Katalogdaten, P032-W2, Dependencies, Hooks, externe Tools und
  Veroeffentlichungen bleiben ausgeschlossen.

Validierung und Ergebnis:

- Die fokussierten P014-/P015-Tests bestehen mit `28 passed`.
- Die vollstaendige lokale Testsuite besteht mit `513 passed`.
- `ruff check` fuer die geaenderten Python-Dateien und `git diff --check` sind
  gruen. Der Formatcheck fuer neue Dateien und geaenderte Exporte ist gruen;
  `snapshots.py` und `ma_workflow/catalog.py` enthalten bereits bestehende,
  ausserhalb dieses Slices liegende Formatabweichungen.
- Der Slice ist umgesetzt. Er schliesst P015-S3b nicht ab und beansprucht
  keine Freigabe fuer die ausgeschlossenen Folgearbeiten.

## Entscheidung 34: Delegierter P013-S3c/P015-S3b-T2-Zonencheckpoint

Gemass UD-089 wird nach Entscheidung 33 ein zweiter, strikt lokaler und
reversibler P013-/P015-Slice vor P032-W2 umgesetzt. Er schliesst die fehlende
Kontextprovenienz, ohne bestehende v1-Parameterwerte als v2-abgeleitet
umzudeuten.

Council-Vote und exakter Scope:

- Mira priorisiert den P013-Zonenfingerprint und getrennte
  `checkpoint_references`, weil `source_references` der Werteherkunfts-
  Namespace bleibt.
- Vera fordert einen kanonischen, reihenfolgeunabhaengigen Zonenfingerprint,
  der den vollstaendigen Zonenstand, Building-Revision und das exakte
  P014-Referenztriple bindet.
- Justus bestaetigt den rein synthetischen Metadatenumfang ohne Rechte- oder
  externe Spezialgates.
- Damit liegt eine einstimmige 3/5-Mehrheit fuer exakt diesen Scope vor.

Technische Folgen:

- `ma_zones` ergaenzt einen payloadfreien `ReleasedZoneHandover`, der nur nach
  erfolgreicher P013- und P014-Konsistenzpruefung erzeugt wird.
- `ParameterInputPackage` und `BaselineParameterSnapshot` erhalten opt-in und
  getrennt von Wertquellen gefuehrte `checkpoint_references`. Ein neuer
  Checkpoint-Validator prueft das passende freigegebene und aktuelle
  P013-/P014-Paar.
- Bestehende `source_references`, `ParameterValue.source_reference_id`,
  Legacy-Builder, UI und Persistenz bleiben kompatibel. Die neuen Referenzen
  werden in den bestehenden Baseline-Hash eingebunden, aber nicht als
  Wertquelle benutzt; ein neuer Package-Level-Hash ist nicht Teil des Slices.
- P032-W2, P032-W3a, v2-Wertableitung, UI, Persistenz, YAML-/Katalogdaten,
  reale oder geschuetzte Daten, externe Tools, Dependencies, Hooks, CI,
  Commit, Push und Veroeffentlichung bleiben ausgeschlossen.

Ergebnis und Validierung:

- Der Scope ist umgesetzt: P013 exportiert nur den frozen, payloadfreien
  `ReleasedZoneHandover`; P015 fuehrt `checkpoint_references` als getrennten
  opt-in-Namespace und prueft im Factory-Pfad das urspruengliche P013-/P014-
  Triple.
- Bestehende Werte, `source_references`, Wertquellen-IDs, Legacy-Builder,
  UI und Persistenz blieben unveraendert; ein Package-Level-Hash wurde nicht
  eingefuehrt. Nur eine Baseline mit Checkpoints bindet deren vollstaendige
  Referenzmetadaten einschliesslich Content-Hashes in ihren vorhandenen
  Content-Hash ein.
- Synthetische Tests pruefen Reihungsstabilitaet, fachliche Hash-Aenderungen,
  fehlende/nicht freigegebene/nicht zusammengehoerige Handover, stale und
  fehlende Checkpoint-Paare, Legacy-Kompatibilitaet sowie die
  Paket-zu-Baseline-Weitergabe. Der nachtraegliche Vera-Review deckte einen
  zu lockeren P014-Typuebergang auf; er ist durch einen Laufzeit-Typcheck und
  Negativtests fuer rohe Revisionen und Duck-Typen behoben.
- Abschlussaudit 2026-07-15: gemeinsamer Fokuslauf `75 passed in 8.62s`,
  vollstaendige lokale Suite `536 passed in 151.25s`; `ruff check` fuer die
  betroffenen Code- und Testdateien, Formatcheck fuer neue/gezielt geaenderte
  Dateien sowie `git diff --check` sind gruen. Bestehende, nicht zum Slice
  gehoerende Formatabweichungen in `models.py`, `validation.py`,
  `snapshots.py` und `ma_workflow/catalog.py` wurden nicht massenformatiert.
- Der Nachweis verwendet ausschliesslich synthetische In-Memory-Testdaten.
  Eine spaetere Anwendung des Hashbuilders auf reale oder geschuetzte
  Zoneninhalte bleibt ein eigener Rechte- und Freigabeumfang.

## Entscheidung 35: Delegierter P032-W2a-Parameter-/Options-Code-Owner-Transfer

Gemass UD-089 wird nach dem abgeschlossenen P013-/P015-Referenzcheckpoint nur
der kleinste, nicht bewegende Teil von P032-W2 umgesetzt. Er beseitigt die
konkrete Runtime-Rueckkante `ma_parameters -> ma_variants`, ohne eine
fachliche P015-v2-Werteherkunft, Konfigurationsownership oder den Vollumfang
von P032-W2 vorwegzunehmen.

Council-Vote und exakter Scope:

- Mira bestaetigt den dokumentierten SCC aus `ma_parameters.services` und
  `ma_variants.preprocess` und verlangt identische Altpfad-Reexports.
- Vera empfiehlt den reinen Owner-Transfer vor P015-v2-Werteherkunft, weil
  er die spaetere Regressionsflaeche reduziert und die API erhalten kann.
- Justus klassifiziert den auf versionierten Python-Code und synthetische
  `tmp_path`-Tests begrenzten Umfang als `green`.
- Damit liegt eine einstimmige 3/5-Mehrheit fuer exakt P032-W2a vor.

Technische Folgen und Grenzen:

- `ma_parameters.catalogs` wird kanonischer Owner von `Parameter`,
  `OptionSet`, `OptionValue`, ihren Loadern sowie kombiniertem
  Katalogimport inklusive Ergebnis-, Fehler- und Reporttypen.
- `ma_parameters.services` darf anschliessend keinen Runtime-Import aus
  `ma_variants` besitzen. Die bisherigen Pfade
  `ma_variants.parameter_catalog`, `ma_variants.option_catalog` und
  `ma_variants.importing` bleiben als identische, getestete Einweg-Reexports
  fuer bestehende Konsumenten erhalten.
- Neue Owner-Module duerfen weder `ma_variants.validation` noch
  `ma_variants.importing.*` importieren. Sie nutzen nur neutrale lokale oder
  `ma_core`-Hilfen; die Runtime-SCC muss danach leer sein.
- Die bestehenden `DEFAULT_*`-Pfade unter `config/ma_variants/` bleiben
  unveraendert als expliziter Legacy-Konfigurationspfad. Es gibt keine
  Config-Moves, -Kopien, -Leseerweiterungen oder Datenverarbeitung.
- Ausgeschlossen sind P015-v2-Werteherkunft, `ParameterValue`-,
  `ParameterSourceReference`-, Baseline-, Hash-, Freshness- und
  Checkpoint-Aenderungen sowie UI, DB, Alembic, weitere Kataloge, P017,
  Hooks, CI, Dependencies, externe Tools, Commits, Pushes und
  Veroeffentlichungen.

Ergebnis und Abschlussaudit:

- Der neue kanonische Namespace `ma_parameters.catalogs` enthaelt Modelle,
  Loader, kombinierten Import sowie Resultat-, Fehler- und Reporttypen.
  `ma_parameters.services` importiert nur noch aus diesem Owner-Namespace.
- Alle bisherigen Katalog- und Importpfade in `ma_variants` bleiben reine,
  identitaetsgleiche Einweg-Reexports. Ein Postreview fand zunaechst fehlende
  direkte Untermodul-Reexports; sie wurden ohne Owner- oder Fachlogikaenderung
  ergaenzt und durch den Contract-Test abgesichert.
- Beide `DEFAULT_*`-Konfigurationspfade unter `config/ma_variants/` und der
  Legacy-Reportpfad `data/ma_variants/imports/import_report.json` blieben
  exakt unveraendert. Es gab keinen Config-, Daten- oder Kataloginhaltszugriff.
- Der neue gezielte Guardrail prueft auch ungestagte `ma_parameters`-Dateien
  auf Runtime-Imports nach `ma_variants`; im mit `git ls-files` erfassten
  Source-Set ist die Runtime-SCC leer.
- Abschlussnachweis: `46 passed` im fokussierten Lauf, danach `541 passed` in
  der vollstaendigen lokalen Suite; zielgerichtete Ruff- und Format-Checks
  sowie `git diff --check` sind gruen. Mira und Vera melden nach der
  Korrektur keine Blocker; Justus bewertet den Scope `green`.
- Bekannte, getrennte Restschuld: Der Arbeitsbaum-P013-/P014-Handover erzeugt
  eine Runtimekante `ma_zones -> ma_technical`, waehrend die vorhandene
  `ma_technical.validation -> ma_zones`-Kante fortbesteht. Das ist ein
  transparenter P032-W3a-Folgepunkt und keine Behauptung eines global leeren
  SCC-Graphen.

P032-W2b (Konfigurationsownership) und der restliche P032-W2-Umfang bleiben
gesondert menschlich freizugeben.

## Entscheidung 36: P011 als schlanke Projektidentitaet und spaetere Projektakte

Der vom Nutzer lokal freigegebene P011-Gesamtentwurf wird kontrolliert in den
bestehenden kanonischen P011-Plan uebernommen. Er erzeugt keine zweite
P011-Planwahrheit.

Council- und Compliance-Preflight:

- Der Dokument-Preflight pruefte den vom Nutzer bereitgestellten lokalen
  Markdown-Kandidaten anhand von Herkunft, Metadaten und SHA-256
  `4D6782E8CD35C902CED72BA858972B79BEFBC6E1F9D39B4B2332FA80860BE955`.
  Nach der ausdruecklichen menschlichen Freigabe vom 2026-07-15 war die lokale
  Inhaltsanalyse `green`; die Uebernahme realer Assets bleibt `yellow` bis zu
  objektbezogenen Rechte- und Datenschutzbelegen.
- Mira, Vera und Justus stimmen bedingt fuer den kontrollierten Ersatz des
  frueheren Kurzplans und fuer genau P011-S1a. Damit liegt eine 3/5-Mehrheit
  gemaess UD-089 vor.

Verbindliche Ownership:

- `ma_project` besitzt Projektidentitaet, allgemeinen Untersuchungsrahmen,
  optionalen Standort, allgemeine Simulationsprogramm- und Namingprofile sowie
  spaeter zulaessige beschreibende Projektassets.
- Quellenwahl bleibt mit `InputSource` beim jeweiligen Fachmodul; P011 besitzt
  kein projektweites Quellenregister. Fachfreigaben verbleiben bei den
  Artefakt-Ownern und Modulstatus bei `ma_workflow`.
- IFC-/Rhino-Modelle bleiben bei `ma_building`, IDA-/Run-Referenzen bei P018,
  P009 und den Adaptern. P011 speichert keine Fachmodelle, Revisionen oder
  nachgelagerten Fachobjektreferenzen.
- `VariantNamingProfile` und seine Konfiguration bleiben bei `ma_project`,
  `ma_variants` konsumiert sie. Rename und Pfadmigration sind kein Bestandteil
  von P011-S1a.

P011-S1a umfasst ausschliesslich additive immutable Projektmodelle,
Validierung und reine Serialisierung mit synthetischen Tests. Nicht Teil sind
Projektordner, `data/projects`, Assets oder Dateikopien, UI, Wetteruebergabe,
Config-Moves, reale Daten, externe Modelle, Dependencies oder Git-Aktionen.

Umsetzungsnachweis 2026-07-15:

- `ma_project` exportiert nun die immutable Modelle `ProjectIdentity`,
  `ProjectLocation`, `ProjectInvestigation`, `Project` und `ProjectContext`
  sowie eine reine Dict-Serialisierung ohne Datei- oder Verzeichnisoperation.
- ASCII-IDs, vollstaendige Koordinatenpaare, zeitzonenbewusste und auch an
  DST-Umstellungen chronologisch korrekte Zeitstempel, Payload-Roundtrips und
  die P028-Kompatibilitaet sind automatisiert getestet. Der Abschlusslauf
  (`P011`, P028, Workflow, Architekturgrenzen) umfasst 60 gruene Tests.
- Vera bestaetigte den Abschluss ohne Blocker oder wichtige Restmaengel;
  Justus bestaetigte die unveraenderte Green-Abgrenzung ohne reale Daten,
  Assets, externe Verarbeitung oder neue Abhaengigkeiten.

Die spaetere Projektakte braucht vor jeder realen Dateioperation einen eigenen
Compliance- und Speicherortscope. Absolute `original_source_path`-Angaben
werden nicht in portable oder versionierte Projektnutzlasten persistiert.

## Entscheidung 37: Zentrale V1-Infokarten und getrennte Bedienansichten

Der lokale V1-UI-Slice setzt UD-091 um, ohne einen neuen Modul- oder
Demo-Wahrheitsstand einzufuehren.

Technische Festlegung:

- `ma_workflow.ModuleDefinition` bleibt die alleinige Quelle fuer den
  zentralen V1-Rahmen. Die bestehende Infokarte erlaeutert daraus `Was`,
  `Wie`, `Warum` und `Wann` mit Zweck, Ein-/Ausgaben, Abgrenzungen und
  naechstem Schritt.
- Der Katalogstatus ist kein Nachweis einer ausfuehrbaren Demo. Insbesondere
  beschreibt `partial` nur den dokumentierten Rahmen; massgeblich bleiben die
  sichtbar verfuegbaren Funktionen der jeweiligen Fachansicht.
- Modulansichten bleiben von V1-Infokarten frei. Die Wetteransicht trennt
  Auswahl und Ergebnis einschliesslich der ergebnisgebundenen Aktivierung und
  des Projekt-Defaults in `Analyse` von Import, Scan, Pruefung und
  Bestandsuebersicht in `Verwaltung`; die Verwaltung bleibt auch ohne aktiven
  Datensatz erreichbar.
- Die Technikansicht trennt `Technikmodell` von `Technik-Katalog`. Die sechs
  bestehenden Katalogthemen und ihre Session-Schluessel bleiben erhalten.
  Der historische Helper `technical_scope_rows()` wird weder geloescht noch
  als kanonische Quelle oder sichtbarer `Einordnung`-Reiter verwendet.

Ausgeschlossen bleiben reale Datenverarbeitung, neue Dependencies, Services,
Persistenz, v2-Editoren, Imports oder Simulationen. Begleitende read-only
Reviews von Mira und Vera bestaetigten diesen begrenzten Scope; die Umsetzung
beruht auf der direkten Nutzerfreigabe aus UD-091, nicht auf einer delegierten
Council-Freigabe.

Der fokussierte UI-Lauf `tests/test_ma_ui_shell.py` endet mit `112 passed`;
Ruff-Check und Format-Check fuer die geaenderten UI- und Testdateien sind
gruen. Der vollstaendige Lauf endet mit `1 failed, 571 passed`; der einzige
Fehler ist der unveraenderte P032-W3a-Guardrail fuer den Runtime-Zyklus
`ma_technical <-> ma_zones` und liegt ausserhalb dieses UI-Slices. P014-v2
ist als hoch priorisierter, weiterhin getrennter Folgeslice vorgemerkt.

## Entscheidung 38: Delegierter P032-W3a-T0-Runtime-Stabilisierungsslice

Vor dem priorisierten P014-v2-S4-Referenzfall wird der kleinste moegliche,
lokale P032-W3a-Teilslice umgesetzt. Er beseitigt ausschliesslich die
Runtime-Importkante `ma_technical -> ma_zones`; die fachliche Ownership der
zonenabhaengigen Legacy-Validierung bleibt bewusst offen.

Council- und Compliance-Preflight:

- Mira bestaetigt, dass `ZoneModelSpecification` in
  `ma_technical.validation` nur fuer Annotationen genutzt wird. P014-S4
  braucht danach einen eigenen YAML- und Abnahmescope.
- Vera bestaetigt, dass ein `TYPE_CHECKING`-Import die aktuelle Signatur,
  das Keyword `zone_spec`, alle Diagnosecodes und die strukturelle
  Validierungslogik unveraendert laesst. Eine SCC-Allowlist ist kein Fix.
- Justus bewertet den auf versionierten Eigen-Code, synthetische Tests und
  Dokumentation begrenzten Umfang als `green`; Belegreferenz:
  `docs/compliance/shared/decision_log.yaml`,
  `SHARED-COMPLIANCE-003` und `SHARED-COMPLIANCE-004`.
- Damit liegt gemaess UD-089 eine einstimmige 3/5-Mehrheit fuer genau T0 vor.

Exakter Scope:

- In `ma_technical.validation` den Import von `ZoneModelSpecification` nur
  unter `TYPE_CHECKING` vorhalten.
- Den Architekturguardrail auf keine verbleibende Runtimekante dieses Paares
  einstellen und die vorhandenen synthetischen P013-/P014-Verhaltens- und
  Importtests ausfuehren.
- Keine Funktion verschieben, duplizieren oder loeschen; die oeffentliche
  Funktion `validate_technical_spec(..., zone_spec=...)`, ihre Diagnosen und
  ihr Laufzeitverhalten bleiben erhalten.

Ausgeschlossen sind der vollstaendige Ownership-Transfer nach
`ma_zones.validation`, die Entfernung oder Aenderung von `zone_spec`,
P014-S4-Referenz-YAML, v2-Werteherkunft, UI, Kataloge, reale Daten,
Dependencies, externe Tools, Commits, Pushes und Veroeffentlichungen.
Der T0-Slice beansprucht deshalb keinen Abschluss von P032-W3a.

Umsetzungsnachweis: Der Import steht nun nur unter `TYPE_CHECKING`; die
P013-/P014-/P015-Fokusgruppe besteht mit `58 passed`, die vollstaendige lokale
Suite mit `572 passed`. Ruff- und Format-Check der betroffenen Dateien sowie
`git diff --check` sind gruen. Die volle W3a-Ownership-Migration bleibt offen.

## Entscheidung 39: Delegierter P014-S4-V2-Referenz- und Loader-Slice

Nach dem abgeschlossenen P032-W3a-T0 wird der priorisierte, lokale und
reversible P014-S4-Slice gemaess UD-089 umgesetzt. Er liefert keinen neuen
fachlichen Werteherkunftsvertrag, sondern einen nachvollziehbaren,
synthetischen V2-Eingabe- und Abnahmenachweis auf den bereits vorhandenen
V2-Modellen, Revisionen und Handovern.

Council- und Compliance-Preflight:

- Mira bestaetigt einen allgemeinen, nicht beispielspezifischen Parser fuer
  `TechnicalModelSpecification`: fruehe V2-Schemapruefung, Pflichtfelder,
  unbekannte Felder, verschachtelte Dataclasses, Enums, Referenzen, optionale
  Bereiche und Tupelregister muessen strukturell behandelt werden.
- Vera stimmt zu, wenn der additive Loader den Legacy-V1-Loader nicht aendert,
  keine erzeugten Revisionen versioniert und die echte P013-/P015-Kette nur in
  Contracttests durchlaeuft.
- Justus bewertet ausschliesslich selbst erstellte synthetische YAML, Tests
  und Dokumentation als `green`; die Synthetic-Kennzeichnung und die
  Ausschlussgrenzen folgen `SHARED-COMPLIANCE-003` und
  `SHARED-COMPLIANCE-004` in `docs/compliance/shared/decision_log.yaml`.
- Damit liegt eine einstimmige 3/5-Mehrheit fuer genau diesen Scope vor.

Exakter Scope:

- Eine sichtbare, projektseitig erstellte und nicht normative V2-Referenz-YAML
  unter `config/ma_technical/examples/` mit ausschliesslich synthetischen IDs,
  Namen und konstruierten Werten anlegen.
- Einen additiven allgemeinen YAML-zu-`TechnicalModelSpecification`-Parser
  und Loader mit strikter Strukturpruefung ergaenzen. Die anschliessende
  fachliche Freigabe bleibt bei `validate_technical_model()`.
- Die geladene Spezifikation ausschliesslich in `tmp_path` freigeben,
  hashgesichert erneut laden und aus der Revision den bestehenden
  `ReleasedTechnicalHandover`, die P013-Referenz und den P015-Checkpoint
  pruefen.
- Negative Parserfaelle, Serviceinterface-Zonenfreiheit, Legacy-V1-
  Kompatibilitaet, Architekturguardrail sowie Format-, Lint-, Diff- und
  vollstaendige Suite pruefen und die bestehenden Plan-/Moduldokumente
  aktualisieren.

Ausgeschlossen bleiben Änderungen am V1-Loader oder am Revisionsvertrag,
V1-zu-V2-Migration, Werteherkunft, automatische Revisionen, UI/Editor,
Katalog-, Produkt-, Normen- und reale Projektdaten, IDA-Dateien, neue
Dependencies, externe Verarbeitung, Hooks, Commits, Pushes und
Veroeffentlichungen. Eine naechste Entscheidung ist erforderlich, sobald
dieser Scope erweitert werden soll.

Umsetzungs- und Abschlussnachweis:

- Der additive `v2_loader` ist als Paket-API verfuegbar und rekonstruiert die
  bekannten V2-Dataclasses strikt. Leere Pflichttexte, unbekannte Felder,
  ungueltige Enums und fehlerhafte YAML-Strukturen blockieren vor der
  fachlichen V2-Validierung.
- Das Sol-Abschlussreview fand eine notwendige Luecke fuer das vorhandene
  Feld `InputSource.source_path`. Mira, Vera und Justus bestaetigten daraufhin
  einstimmig die kleinste Scope-Ergaenzung: `_to_payload` normalisiert nur
  `Path` als `as_posix()`; keine API, kein Revisionsschema, kein bisheriger
  Hash und keine externe Verarbeitung aendern sich. Der Test verwendet
  ausschliesslich einen relativen synthetischen Demo-Pfad. Absolute oder reale
  Arbeits-, Netzwerk-, Nutzer- oder Projektpfade bleiben ausgeschlossen.
- Der allgemeine Aggregate-Payload-Roundtrip, verschachtelte Negativfaelle,
  UTC-Provenienzdefaults, `InputSource`-Pfad, Revision/Hash, Handover,
  P013-/P015-Checkpoint und Legacy-V1 sind abgedeckt. Der abschliessende
  relevante P014-Fokuslauf besteht mit `45 passed in 10.61s`, die
  vollstaendige lokale Suite mit `591 passed in 193.30s`; Ruff-Check und
  `git diff --check`
  sind gruen.

### P014-S4-Nachtrag: reproduzierbarer YAML-Provenienzvertrag

Das Abschlussreview fand zwei lokale Luecken im bereits freigegebenen
V2-YAML-Nachweis: Ein fehlendes persistiertes `InputSource.source_id` erzeugte
einen zufaelligen Laufzeitwert und unquotierte YAML-Zeitstempel wurden nicht
als YAML-Datetime verarbeitet. Vera, Mira und Professor Sophia stimmen am
2026-07-18 einstimmig gemaess UD-089 fuer den kleinsten lokalen und
reversiblen Nachtrag.

- Nur der persistierbare V2-Loader verlangt nun eine nichtleere
  `source_id`; der allgemeine `InputSource`-Default und der V1-Vertrag bleiben
  unveraendert.
- Zeitzonenbehaftete YAML-Datetime-Skalare werden wie ISO-8601-Text geladen;
  naive Zeitpunkte bleiben unzulaessig.
- Ein ausschliesslich synthetischer Vollfixture-Test prueft den oeffentlichen
  YAML-Pfad, Revision/Reload und den identischen Content-Hash zweier Laeufe.

Nicht Teil sind Werteherkunft, Revisionsschema, neue Persistenzorte,
Abhaengigkeiten, reale Daten, externe Verarbeitung oder Git-Aktionen.

## Entscheidung 40: Lokale Gebaeude-Referenzkataloge bleiben vom DemoCatalog getrennt

Am 2026-07-18 wird gemaess UD-089 ein eng abgegrenzter, lokaler und
reversibler P012/P027-V1-Slice umgesetzt. Er verarbeitet nach dokumentierter
Gruen-Entscheidung ausschliesslich die vom Nutzer freigegebenen Arbeitsmappe-
Abschnitte `Materials`, `Wall constructions` und `Surfaces` und erzeugt daraus
drei ignorierte lokale Dateien: `building_materials.yaml`,
`building_wall_constructions.yaml` und `building_surfaces.yaml`.

- Die Kataloge werden ausschliesslich durch ein neues, lesendes
  `ma_building`-Modul geladen. `ma_database.DemoCatalog`, dessen Manifest,
  Bundle- und Simulationslogik bleiben unveraendert.
- Jede Datei erhaelt einen kleinen Schemaheader und dauerhaft gespeicherte,
  innerhalb der Datei eindeutige IDs. Die UI setzt die sichtbare Reihenfolge
  explizit auf Name, ID und weitere Eigenschaften; die YAML-Reihenfolge ist
  kein UI-Vertrag.
- Wandkonstruktionen duerfen eingebettete Schichten fuer eine breite
  Nur-Lese-Tabelle enthalten. Es findet weder eine fachliche U-Wert- noch
  Simulationsvalidierung oder automatische Modellzuordnung statt.
- Fehlende Dateien werden je Katalog getrennt angezeigt; fehlerhafte
  vorhandene Dateien erzeugen eine lokale Diagnose und werden nicht als
  fehlend verborgen.

Mira (Bestandsaufnahme), Vera (Qualitaet) und Justus (Compliance) haben den
genauen Scope einstimmig freigegeben. Der Compliance-Nachweis
`COMPLIANCE-2026-07-18-BUILDING-CATALOGS-001` begrenzt die Verarbeitung auf
die drei genannten Abschnitte und schliesst Originaldatei, weitere
Arbeitsmappeninhalte, Abhaengigkeiten, externe Verarbeitung und die
Veroeffentlichung abgeleiteter Katalogdaten aus. Die ignorierten Daten bleiben
auch bei einem spaeteren Repository-Update ausgeschlossen.
