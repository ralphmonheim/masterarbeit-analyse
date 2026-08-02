# Offene Nutzerentscheidungen

Stand: 2026-07-31

Diese Datei enthaelt nur offene Nutzerentscheidungen. Erledigte Entscheidungen
werden nach der Dokumentation als `UD-*` aus dieser Datei entfernt und stehen in
`USER_DECISIONS_MASTERTHESIS_CODE.md`.

## Offene Punkte

### OP-008 ma_analyse-weite Normierungsstrategie

- Thema: ma_analyse Auswertungen und Diagramme
- Status: offen
- Frage: Welche Auswertungen sollen absolute Werte, flaechenbezogene Werte oder beides anbieten, welche Bezugsflaeche soll dafuer verwendet werden und wie werden Zeitintervall, Vorzeichen und Fehlwerte festgelegt? Fuer Gebaeude-Spitzenleistung ist insbesondere zu entscheiden, ob verbindlich `max_t(Summe der zonalen Leistungen zum selben Zeitpunkt)` gilt.
- Auswirkung: Betrifft spaeter `src/ma_analyse/analysis/`, Plot-Templates, Tkinter, Streamlit-Analyse und die Dokumentation der Diagrammeinheiten.
- Teilklaerung 2026-07-31 durch UD-112: Jahresenergie und Leistung bleiben
  fachlich getrennt; Spitzenleistung wird aus gleichzeitigen Zeitreihen
  ermittelt. Welche absoluten und spezifischen Werte gemeinsam erscheinen und
  welche Bezugsflaeche verbindlich ist, bleibt offen.

### OP-009 Methodik fuer Zeit- und Personalkostenvergleich

- Thema: Prozessaufwand und Automatisierungsnutzen
- Status: offen
- Frage: Welche Wissensprofile, Stundensaetze, Prozessgrenzen und Messmethoden sollen fuer den Vergleich zwischen manuellem, softwareunterstuetztem und automatisiertem Ablauf verwendet werden?
- Auswirkung: Beeinflusst die wissenschaftliche Vergleichbarkeit, die Prozesskostenrechnung sowie spaetere Ergebnisse in `ma_economy` und `ma_assessment`.
- Teilklaerung 2026-07-31 durch UD-112: P030 misst PreProcess mit
  Parameter-/Variantenumfang, manuelle IDA-Arbeit je Variante,
  Maschinen-/Simulationsdauer, Pruef-/Korrekturzeit und PostProcess getrennt.
  Personalkosten beruhen primaer auf aktiver Arbeitszeit; Wartezeit wird
  separat berichtet. Offen bleiben das konkrete Wissensprofil,
  Stundensatzquelle, Bezugsjahr, Zuschlaege, Wiederholungen, Lerneffekt und
  das verbindliche Vergleichsprotokoll. Es muss gepaarte Vergleichslaeufe mit
  identischen Eingaben, Varianten, Pruefanforderungen und Ergebnisartefakten,
  festgelegten Parameter-/Variantenstufen sowie eindeutigen Start-/Endpunkten
  definieren. Gemeinsame Setup- und PostProcess-Zeiten duerfen nicht
  unbemerkt jeder Variante voll zugerechnet werden.

### OP-017 Neutraler Ergebnisvertrag und Dateninventar

- Thema: gemeinsamer Importkern, PostProcess und Diagrammfaehigkeit
- Status: offen; Rechte-/Evidenzgate
- Frage: Welcher manuell bereitgestellte, freigegebene neutrale Ergebnisexport
  steht fuer V1 tatsaechlich zur Verfuegung und welche Variablen, Einheiten,
  Vorzeichen, Zeitstempel, Zeitschritte, Zonen-/Systemkennungen, Fehlwerte und
  Hashes enthaelt er? Wie sind Zeitzone, Sommerzeit, Kalender/Schaltjahr,
  Intervallgrenzen und Transformationsversion definiert?
- Auswirkung: Erst das Dateninventar legt den verbindlichen Feldvertrag,
  Datenaufbereitung und die Menge datenkompatibler Diagrammvorlagen fest.
  Vor Ergebnissichtung werden daraus die primaeren Abbildungen der Arbeit und
  ergaenzende/explorative Ausgaben bestimmt, ohne vorhandene Diagrammvorlagen
  stillschweigend zu veraendern.
  Vollstaendige IDA-/EQUA-Dateien, Bibliotheken und automatisierte IDA-Wege
  sind keine zulaessige Zwischenloesung.

### OP-018 Projektbezogene Funktionspruefung und Bewertungszeitraum

- Thema: PostProcess, Funktionsstatus und Einsparungsinterpretation
- Status: offen; fachlich-methodische Entscheidung nach Dateninventar
- Frage: Welche projektbezogenen, nicht normativen Toleranzen,
  Belegungszeiträume, Indikatoren (Sollwerte, Unterdeckung,
  Kapazitaetssaettigung, Verletzungsstunden/Gradstunden) und
  Bewertungsregeln gelten fuer eine funktional ausreichende Variante?
- Auswirkung: Bis dahin zeigt V1 den Funktionsstatus beschreibend und
  nachvollziehbar. Eine geringere Energie oder Leistung darf bei sichtbarer
  Unterversorgung nicht als Verbesserung interpretiert werden; ein
  normativer Komfortnachweis bleibt ausgeschlossen. Ein Pass/Fail-Urteil oder
  eine Einsparungsbewertung ist bis zur Entscheidung nicht zulaessig.

### OP-012 Umfang eines IFC-Lite-Imports

- Thema: ma_building und externe Gebaeudemodelle
- Status: offen
- Frage: Welche Inhalte sind in den konkreten IFC-Arbeitsstaenden belastbar
  vorhanden und koennen ohne umfangreiche Geometrieinterpretation sicher
  uebernommen werden?
- Ergaenzung: Die aktuelle lokale IFC-Arbeitsdatei soll fuer P012 zunaechst
  als Trainings- und Diagnosebasis dienen. Zu klaeren ist, welche
  Metadaten, Entitaeten, Raeume, Bauteile, Oeffnungen und IDs daraus sicher
  auslesbar sind.
- Auswirkung: Entscheidet, ob P012 nur Demo-/YAML-Daten oder zusaetzlich einen
  begrenzten IFC-Lite-Adapter umsetzt.

### OP-012b LoD-2/LoD-3-Inhalte aus dem Rhino-Testgebaeude

- Thema: ma_building, BusinessIntegration-Testmodell und Level of Detail
- Status: offen
- Frage: Welche weiteren Inhalte aus dem Rhino-Testgebaeude werden nach
  LoD-1 fuer LoD-2 oder LoD-3 manuell oder als strukturierte Demo in die
  `BuildingModelSpecification` uebernommen?
- Ergaenzung: UD-068 legt fest, dass LoD den Umfang der Eingabe beschreibt.
  LoD-1 ist mit Kubatur, einfachen Huellkennwerten, U-Werten,
  Fensterflaechenanteil und Annahmen umgesetzt, ohne produktiven
  Rhino-Import.
- Auswirkung: Bestimmt, ob als naechstes Raeume, orientierte Bauteile,
  Oeffnungsobjekte, Host-Beziehungen, Sonnenschutz und weitere
  bauphysikalische Werte als LoD-2/LoD-3 erfasst werden.

### OP-013 Verbindliche Importformate je Eingabemodul

- Thema: Eingabe- und Datenhaltungsarchitektur
- Status: offen
- Frage: Welche Datei- und Programmvorlagen werden fuer Building, Zones,
  Technical, Parameters und Naming im Masterarbeitsumfang verbindlich
  unterstuetzt?
- Ergaenzung: Fuer `ma_building` ist das Rhino-Testgebaeude durch UD-067 als
  BusinessIntegration-Referenz festgelegt. Die daraus abgeleitete
  BusinessIntegration-LoD-1-YAML ist unterstuetzt, aber `.3dm` ist weiterhin
  kein produktives Eingangsformat. DWG ist durch UD-066 fuer den aktuellen
  Masterarbeitsumfang kein produktiver Importpfad und bleibt nur lokale
  ungepruefte CAD-Quelle. Fuer `ma_zones` und `ma_technical` sind
  BusinessIntegration-LoD-1-YAML-Demos durch UD-069 unterstuetzt. Der
  P013-S2-Gesamtplan fuer `ma_zones` ist durch UD-072 fachlich konsolidiert,
  ersetzt aber noch keine produktiven Importprofile. Der
  BusinessIntegration-LoD-1-`ParameterSnapshot` v1 ist durch UD-070
  unterstuetzt; P015-S3a unterstuetzt die Wetteruebergabe als aktivierten,
  freigegebenen `ma_weather`-Projekt-Default im `ParameterInputPackage`.
  Produktive Importprofile, Systemvorlagen, Snapshot-Speicherung,
  Freshness-Abgleich und vollstaendige Quellenfingerprints bleiben offen.
  P016-S1 nutzt den Snapshot v1 fuer eine LoD-1-Referenzdimensionierung;
  Stage-1-Folgesnapshots und normative Verfahren bleiben offen.
- Auswirkung: Wird in P010 als Formatmatrix vorbereitet und vor den jeweiligen
  Fachimplementierungen entschieden.
- Teilklaerung 2026-07-27 durch UD-106: Materialien, Produkte, Bauteile und
  Elemente werden aus Excel-Katalogen gelesen. Simulationsprogramme,
  Naming-Profile, Regeln, Vorlagen und sonstige technische Metadaten duerfen
  Config-basiert bleiben. Projektbezogene Kopien speichern Auswahl und
  Anpassung, nicht eine zweite Katalogwahrheit. Offen bleiben insbesondere
  IFC-Lite und weitere produktive Fremdformate.

### OP-014 ma_zones Folgeentscheidungen aus P013-S2

- Thema: ma_zones, P013-S3 bis P013-S7
- Status: offen
- Frage: Wie werden die in P013-S2 markierten offenen Fachpunkte entschieden:
  Sonderhohlraeume, gleichzeitiger Heiz- und Kuehlbetrieb, Bedeutung des
  Prozentwerts bei Uebergabesystemen, LoD-1-Variantenparameter und konkrete
  DIN-Datenabbildung?
- Ergaenzung: P013-S2 legt die Grundstruktur fest, darf diese offenen Punkte
  aber nicht stillschweigend in Berechnungs- oder UI-Logik uebersetzen.
- Auswirkung: Betrifft `ma_zones`, `ma_technical`, `ma_parameters`,
  `ma_variants`, `ma_validation`, die UI-Reiter und die spaetere
  Normprofil-/Zeitprofilabbildung.
- Teilklaerung 2026-07-27 durch UD-106: 5Z bleibt der aktive
  SmallOffice-V1-Stand. 29Z wird als alternatives thermisches Modell mit
  einer Zone je IFC-Raum, langen IFC-Namen und vollstaendiger manueller
  Bestaetigung der DIN/TS-18599-10:2025-10-Profilvorschlaege vorbereitet.
  Sonderhohlraeume und die weiteren hier genannten Fachfragen bleiben offen.

### OP-015 ma_variants Folgeentscheidungen nach P017-Handover

- Thema: ma_variants, ma_rules, Naming, Exportpfade und Iterationen
- Status: offen
- Frage: Welche der bewusst zurueckgestellten P017-Erweiterungen werden nach
  der ersten Ausbaustufe aufgenommen: projektweiter Regelkatalog, lange
  Variantennamen und Baumdarstellung, Exportpfadprofile, Filter-/Rule-based
  Selection, Monte-Carlo-/Latin-Hypercube-Sampling oder iterative
  StudyCase-Prozesse?
- Ergaenzung: Die aktive erste Ausbaustufe bleibt bewusst klein: Nach VSP und
  VVER liegt die verbindliche Auswahl vor dem tatsaechlichen
  Dimensionierungsauftrag; danach folgen Ergebniszuordnung, Nachpruefung,
  finaler VCAT und VGEN. Die vorhandenen Objekte `VSP`, `VVER`, `VCAT`,
  `VSEL`, `VGEN` bleiben erhalten, `VCAT <= 500` und es gibt keine
  `SimulationCase`-Ebene. Die genaue Speicherung der fruehen Auswahl wird
  im P017-Migrationsslice geklaert.
- Auswirkung: Betrifft `ma_variants`, `ma_parameters`, `ma_rules` als
  moeglichen spaeteren Zielbereich, `ma_validation`, `ma_feedback`,
  `ma_workflow`, `ma_simulation_setup`, Exportpfade und wissenschaftliche
  Dokumentation.
- Teilklaerung 2026-07-27 durch UD-106: `all`, `manual` und reproduzierbares
  `random` bleiben die V1-Auswahlmodi. Projekt-, StudyDirection- und
  StudyCase-Regeln werden in `ma_parameters` gefuehrt und im aktiven
  StudyCase schreibgeschuetzt angezeigt. Namensvorschau und Paketerzeugung
  bleiben getrennte Aktionen. Monte Carlo, Latin Hypercube, allgemeine
  Vorlagenbibliotheken und automatische Study-Iterationen bleiben offen.

### OP-016 P031 externe Project-OS-Aktivierungen

- Thema: Codex Project Operating System, Tools und lokale Datenfluesse
- Status: offen; lokale repo-eigene Baseline ist davon nicht blockiert
- Frage: Welche Aktivierungen werden spaeter bewusst freigegeben: bestehende
  Git-Hooks beibehalten oder deaktivieren, effektive MCP-Werkzeuge begrenzen,
  `max_threads` von 3 auf 4 erhoehen, Graphify mit welchem Code-Scope
  evaluieren, welchen Obsidian-Vault-/Zotero-Zielbereich verwenden und welche
  Normen-, Literatur- oder IDA-Dateien besitzen belegte Maschinen- und
  KI-Verarbeitungsrechte?
- Auswirkung: Ohne Einzelentscheidung bleiben globale Codex-Aenderungen,
  Installationen, Hook-/MCP-Aenderungen, Graphify, externe Schreibpfade und
  geschuetzte Inhaltsverarbeitung gesperrt. P031 dokumentiert die Gates, ist
  aber keine Freigabeinstanz.
