# P027 Querschnitt UI, Workflow, Validation und Feedback

Stand: 2026-07-31
Status: Aktiv, begleitend; Workflow-UI nach UD-114 ans Ende der Migration verschoben
Prioritaet: Hoch
Abhaengigkeiten: alle P007-Teilplaene

## Ziel

Quellenwahl, Modulstatus, Warnungen, Freigaben, Rueckspruenge und
Serviceaufrufe ueber alle Fachslices konsistent darstellen und steuern.

## Arbeitspakete

- `ma_ui`: Import, manuell und Demo je Modul auswaehlbar darstellen.
- `ma_workflow`: nur freigegebene Fachservices orchestrieren.
- `ma_validation`: gemeinsames Ergebnis fuer Fehler, Warnungen und Freigaben
  definieren.
- `ma_feedback`: Ruecksprungziel und Korrekturauftrag dokumentieren.
- Tkinter-Vorschau, Streamlit-Abgleich und Vorschau-Cache als getrennte
  spaetere Slices fuehren.
- Gezielte Modulverweise mit Ruecksprungziel fuer zentrale Einstellungen in
  `ma_project` und `ma_parameters` bereitstellen.
- Vorlagen in der UI als schreibgeschuetzt kennzeichnen. Bei kollidierenden
  neuen Dateinamen muss eine neue Nutzereingabe erfolgen.
- P017-Checkpoints `VSP`, `VVER`, `VCAT`, `VSEL` und `VGEN` mit einheitlichen
  Status-, Reload- und Abbruchmeldungen abbilden.
- Dimensionierungsunterbrechung innerhalb von `VVER` ueber `ma_workflow`
  koordinieren, ohne daraus eine fachliche Iteration zu machen.
- Compliance-Warnungen aus `ma_core.compliance` einheitlich anzeigen:
  `green` ausfuehren, `yellow` bis zur dokumentierten Bestaetigung und allen
  erforderlichen Belegen blockieren, `red` und `unknown` stoppen.

## V1-Infokarten- und Bedienansichtsslice 2026-07-18

Die vorhandene zentrale Infokarte zeigt fuer jedes katalogisierte Modul den
V1-Rahmen `Was`, `Wie`, `Warum` und `Wann` ausschliesslich aus
`ma_workflow.ModuleDefinition`. Die praktischen Modulansichten erhalten keine
zweite V1-Infooberflaeche. Der Katalogstatus beschreibt keinen Nachweis einer
ausfuehrbaren Demo.

Als verbindlicher V1-Punkt erklaert jede Infokarte zudem allgemeine Begriffe
wie V1-Rahmen, Freigabestatus, Annahme und Demo-/Uebergangsstand. Fachliche
Begriffe werden zentral nach Modul ergaenzt; `ma_building` erklaert vollstaendig
die BIL-Reifegrade und LoD-Eingabestufen. Die Arbeitsansichten bleiben frei von
duplizierten Erklaerungen.

- `ma_weather` trennt die Bedienung in `Analyse | Verwaltung`; Import, Scan,
  Pruefung und Bestandsuebersicht bleiben in `Verwaltung` auch ohne aktiven
  Wetterdatensatz erreichbar. Die ergebnisgebundene Aktivierung und der
  Projekt-Default verbleiben unveraendert in `Analyse`.
- Der zentral registrierte Wetter-V1-Umfang ist `available`. Die Startkarte
  kennzeichnet den separaten Diagrammausbau mit `Diagramme – Teilweise` in
  der vorhandenen amberfarbenen Statusdarstellung, ohne einen zweiten
  Fachmodulstatus zu erzeugen.
- Die Projektseite ist korrekt auf die vorhandene P028-Fachansicht fuer
  Simulationsprogramme und Varianten-Benennung registriert; Router,
  Seitenregistrierung und Sitzungsmodus verwenden keine zweite Projektansicht.
- `ma_technical` trennt `Technikmodell | Übersicht | Auswahl`. Die Auswahl
  bleibt bis zum expliziten Speichern ein Sitzungsentwurf und aktualisiert
  danach nur die sichtbare technische Auswahluebersicht.
- `ma_zones` zeigt die sechs fachlichen Bereiche `Übersicht | Zone zuweisen |
  Nutzung & interne Lasten | Zeitpläne | Konditionierung & Übergabe |
  Zusammenfassung & Prüfung`. Die vollständige Raum-Zonen-Übersicht ist
  sichtbar; ihre Zuweisung bleibt bis zum Revisionsservice read-only.
- Der erste abgestimmte `ma_building`-Reiter `Übersicht` trennt die
  Gebaeudestammdaten einschliesslich LoD und Reifegrad von den zentralen
  Flaechen- und Volumenkennwerten. Die vorhandene Fachspezifikation und die
  Validierungslogik bleiben read-only.
- `ma_building` erweitert V1 um `Bauteile` mit Übersicht und Typ-Reitern;
  Fenster und Tueren werden dort als Bauteile gezeigt. `Konstruktionen` fasst
  Wandkonstruktionen und `Surfaces` zusammen, Materialien und Produkte liegen
  in eigenen Unterreitern. Die drei lokalen Katalogdateien sind ignoriert,
  werden separat und nur lesend validiert und bleiben von `DemoCatalog`,
  Simulationen und automatischen Zuordnungen getrennt. `Modellquellen` ist
  nicht Teil der V1-UI.
- Nicht Teil sind neue Fachservices, reale Importe, persistente
  Modellzuordnungen, ein v2-Editor, Simulationen, Dependencies oder externe
  Verarbeitung.

Der abschliessende fokussierte Gebaeude-/UI-Testlauf umfasst `124 passed in
6.93s`; die abschliessende vollstaendige lokale Suite umfasst `604 passed in
159.41s`.
Statische Ruff- und Format-Checks der geaenderten UI- und Testdateien sind
gruen.

## P018- und P030-Integration

P027 besitzt den produktiven Querschnittsvertrag, nicht die wissenschaftliche
Prozessmessung:

- P027-S1 definiert strukturierte technische Ereignisse mit Zeitstempel,
  Modul, Operation, Status, Dauer, Objekt-IDs, Warnungs-/Fehlercodes sowie
  Objekt- und Dateianzahlen.
- P027-S2 orchestriert P017 und P018: Selection laden, Run-Entwurf,
  Materialisierung, Validierung, Warnungsbestaetigung und Freigabe.
- P027-S3 zeigt eine minimale Run-Ansicht mit Variantenanzahl,
  Setup, Dateibaum-Vorschau, Validierungsbericht, Freigabestatus und Logpfad.
- P030 liest diese technischen Logs nur lesend und fuegt manuelle Zeiten,
  Simulationsdauer und Prozessvergleiche ausserhalb der Fachsoftware hinzu.

Die Messung wissenschaftlicher Nutzer-, Pruef- und Korrekturzeit wird nicht in
`ma_workflow`, `ma_ui` oder dem Run gespeichert. P027 darf nur technische
Laufzeiten und Statusereignisse protokollieren.

## Masterarbeits-MVP-V1-Workflow

Der minimale durchgehende Workflow lautet: freigegebene Eingaben und Varianten
-> P018-Run-Paket -> manuelle Simulation -> P009-Ergebnisaufnahme ->
`ma_analyse`-Diagramme -> P030-Prozessauswertung. P027 ist fuer die
technischen Checkpoints bis zur P018-Freigabe und fuer die Anzeige der
anschliessenden RUN/VAR-Zuordnung zustaendig. Wissenschaftliche Bewertungen
bleiben ausserhalb dieses Workflows.

## Akzeptanzkriterien

- Keine Fachberechnung liegt in UI oder Workflow.
- Status stammt weiterhin aus dem zentralen Katalog.
- Jede geplante Karte zeigt eine Infoseite statt funktionsloser Bedienung.
- Freigaben und Rueckspruenge sind fuer den Nutzer nachvollziehbar.
- Lokale Candidate-Fehler, Katalogfehler, Selection-Reloads und
  Generation-Fehler werden unterschiedlich erklaert.
- Fehler blockieren immer; Warnungen und Approvals werden dokumentiert.

## Umsetzungsbezug P028

Projekt, Parameter und Varianten besitzen echte Fachansichten, behalten ihre
Infokarten und koennen mit gespeichertem Ruecksprungziel aufeinander
verweisen. Das gespeicherte Ruecksprungziel gilt fuer einen konkreten
Konfigurationskontext; es legt keine globale Start- oder
Weiter-/Zurueck-Navigation fest. Die allgemeine Workflow-Orchestrierung und
zentrale Validierung bleiben offen.

## Umsetzungsbezug P010

Gemeinsame Diagnose-, Validierungs- und Freigabemodelle sind umgesetzt.
Der Wetterpilot zeigt die Meldungen und Entscheidungen in Streamlit und
protokolliert sie im Sitzungslog. P027 fuehrt diese Bedien- und
Orchestrierungsregeln in spaeteren Fachslices weiter.

## Umsetzungsbezug P017

Fuer P017 gelten folgende Checkpoints:

- `VSP Checkpoint`: Dimensionen, Werte, Einheiten, Zielobjekte und
  theoretische Zaehlung pruefen.
- `VVER Checkpoint`: Candidates, Ausschluesse, Dimensionierungsgruppen,
  Fingerprints und Reports pruefen.
- `VCAT Checkpoint`: hoechstens 500 Eintraege, eindeutige `VAR-ID`,
  eindeutige Fingerprints und rekonstruierbare Referenzen pruefen.
- `VSEL Checkpoint`: genau ein Quellkatalog, zulaessiger Auswahlmodus,
  Grenzen und erforderliche Approvals pruefen.
- `VGEN Checkpoint`: alle ausgewaehlten Varianten vollstaendig erzeugt,
  Fingerprints bestaetigt und Alles-oder-nichts-Regel erfuellt.

Reload-Logik:

- `variant_reload` fuer lokale Probleme an einer Variante.
- `selection_reload` fuer mehrere oder strukturelle Probleme.
- `abort`, wenn der Fehler nach vollstaendigem Reload weiter besteht.

Workflow-Zustaende fuer laengere Variantenprozesse:

- `created`
- `running`
- `waiting_for_dimensioning`
- `resuming`
- `completed`
- `failed`
- `cancelled`

Die Dimensionierungsschleife innerhalb von `VVER` ist technische
Wiederaufnahme, keine fachliche CaseIteration.

## Umsetzungsbezug Compliance

`ma_core.compliance` stellt UI-neutrale OperationRequests, Entscheidungen,
Warntexte, sichere Operationswrapper und ein
append-only JSONL-Audit bereit. Der DWD-TRY-2011-Konverter ist der erste
angebundene Fachadapter. Eine spaetere UI darf rote oder unbekannte
Entscheidungen nicht uebersteuern und bei gelben Entscheidungen nur die vom
Service verlangten Referenzen erfassen.

## Handover-Ergaenzung 2026-07-21

Die Querschnitts-Handover konkretisieren die Verantwortungsgrenzen:

- `ma_core` stellt nur neutrale IDs, Referenzen, Revisionen, Hashes,
  `InputSource`/`InputChange`, Konfigurations-I/O sowie Pfad- und
  Loggingkonventionen bereit; keine TGA-Fachlogik.
- `ma_rules` bewertet versionierte Fachregeln in den Phasen von
  Vor-Kombination bis Generation. Harte technische Grenzen blockieren,
  Empfehlungen warnen; eine Regel entscheidet in V1 keine Selection.
- `ma_validation` prueft die VSP-, VVER-, VCAT-, VSEL- und VGEN-Checkpoints.
  Kandidatenfehler koennen lokal ausgeschlossen werden; strukturelle
  Katalog-, Selection- oder Generationsfehler blockieren den jeweiligen
  Uebergang.
- `ma_workflow` orchestriert die lineare Prozesskette und eine technisch
  wiederaufnehmbare Dimensionierungsschleife innerhalb von VVER. Es erzeugt
  keine Fachwerte und keine automatische Study-Iteration.
- `ma_feedback` uebersetzt Pruef- und Statusbefunde in nachvollziehbare
  Meldungen, ohne Regeln oder Selections zu veraendern. `ma_ui` bleibt fuer
  spaetere Draft-, Validierungs- und Revisionsansichten zustaendig.

Die genannten UI-Editoren, Datenbankmigrationen und automatischen Iterationen
sind keine Umsetzungfreigabe und bleiben getrennte Folgeentscheidungen.

## Konsolidierter UI-Zustandsvertrag 2026-07-27

UD-106 legt fuer die weitere V1-UI fest:

- Die sichtbare Reihenfolge wird zu `Projekt -> Wetter -> Gebaeude -> Zonen
  -> Technik -> Parameter -> Referenzdimensionierung -> Varianten ->
  Simulation-Setup` konsolidiert.
- Streamlit-Neulaeufe erhalten aktive Seite, Reiter, Unterreiter, Auswahl
  und Sitzungsentwuerfe.
- Nur eine ausdrueckliche Nutzeraktion darf Navigation oder fachliche Auswahl
  wechseln.
- Entwuerfe werden erst ueber modulbezogene Uebernahmebuttons gespeichert.
- Projektwechsel mit offenen Entwuerfen warnt; alle gueltigen Entwuerfe des
  aktuellen Moduls koennen gesammelt gespeichert werden.
- Aktualisierte vorgelagerte Werte loeschen keine Nachfolger, sondern
  markieren sie nachvollziehbar als aktualisierungsbeduerftig.

P035 konkretisiert Projektstart, lokale Registry und Workspace-Persistenz,
ohne diese Querschnittsregeln zu duplizieren.

## Konsolidierung nach UD-112 2026-07-31

Die sichtbare Zielreihenfolge lautet dauerhaft `Projekt -> Wetter -> Gebaeude
-> Technik -> Zonen -> Parameter -> Varianten-Vorbereitung/-Auswahl ->
Dimensionierung -> finaler VCAT/VSEL/VGEN -> Simulation-Setup -> manuelle
Simulation -> Ergebnisimport -> PostProcess`.
Die verbindliche UI-Abfolge innerhalb dieser Kette lautet nach Parameter
zunaechst `VSP/VVER und fruehe Auswahl -> Dimensionierung als sichtbarer
Unterablauf von ma_variants -> finaler VCAT/VSEL/VGEN -> Simulation-Setup`.
Sie ersetzt in P027 die gegenteilige Reihenfolge aus UD-106. `ma_technical`
liefert Systeme/System-IDs; `ma_zones` zeigt und bearbeitet deren zonale
Zuordnung. Die technische Umstellung wird als eigener, getesteter
Migrationsslice geplant.

Die Prozessbereiche sind nach UD-114 verbindlich abgegrenzt: PreProcess reicht
bis einschliesslich `ma_simulation_setup`; der Kernprozess umfasst Export,
Run-Uebergabe, manuelle Simulation und Ergebnisimport bis
`standardized_ready`; PostProcess beginnt am selben Uebergang mit der
fachlichen Datenverarbeitung `standardized -> prepared`. Review/Iteration,
Validierung und Feedback wirken phasenuebergreifend, ohne eine vierte
Fachphase oder zweite Workflowwahrheit zu bilden.

Jede V1-Fachfunktion erhaelt eine bedienbare UI: Projektanlage, Wetter,
Gebaeude, Technik, Zonen, Parameter, Dimensionierung,
Varianten-Vorbereitung/-Auswahl, Simulation-Setup, Run-UEbergabe,
Ergebnisimport und PostProcess. Die Workflow-Ansicht zeigt PreProcess,
MainProcess und PostProcess als Orientierung; Modulansichten bleiben die
fachliche Arbeitsflaeche und erzeugen keine zweite Persistenzwahrheit.

Die UI zeigt getrennt Import-Mapping, technische Validierung,
Fach-/Funktionsauswertbarkeit und Reviewstatus. PostProcess-Ergebnisse
kennzeichnen `nicht angefordert` und `nicht auswertbar` mitsamt Ursache.
Eine Diagrammvorlage wird nicht ohne gesonderte Nutzerentscheidung optisch
oder fachlich veraendert.

## Workflowansicht und ebenenabhaengige Navigation 2026-07-31

Die Workflowansicht ist eine interaktive Orientierung und Navigation, keine
zweite Daten-, Status- oder Orchestrierungswahrheit neben den Fachmodulen.
Die bisherige globale lineare Kopfzeilenlogik mit `Start`, `Zurueck` und
`Weiter` ist deshalb nicht die Zielbedienung fuer diese Ansicht.

- **Ebene 1 – Gesamtuebersicht:** Sie ist der Einstieg in die
  Workflowansicht und zeigt `PreProcess`, `Kernprozess (MainProcess)` und
  `PostProcess` als drei anklickbare Bereiche. Sie darf verdichtete
  Validierungs- und Reviewhinweise zeigen, zum Beispiel einen
  PostProcess-Rueckschluss auf `ma_technical`, `ma_zones` oder
  `ma_parameters`. Solche Hinweise aendern keine Eingaben automatisch.
- **Ebene 2 – Bereichsworkflow:** Ein geoeffneter Bereich zeigt seine
  Fachmodule in der verbindlichen Prozessreihenfolge, deren Uebergaben und
  konkret beschriftete Validierungs-/Entscheidungsknoten. Die PreProcess-
  Validierung wird hier am passenden Uebergang sichtbar; ein `Nein` hat ein
  eindeutiges Zielmodul statt eines unbenannten Diagrammknotens.
- **Ebene 3 – Facharbeit:** Ein Moduloeffnen fuehrt in die vorhandene
  Fachansicht mit Reitern oder gefuehrten Detailschritten. Die bewährte
  Detailschritt-Navigation aus der Analyseansicht ist das Bedienmuster:
  Weiter bleibt bis zur erforderlichen Vollstaendigkeit gesperrt und Zurueck
  wechselt nur zum vorherigen Detailschritt.
- **Navigation:** Weiter und Zurueck bewegen sich immer nur innerhalb der
  aktuell sichtbaren Ebene: zwischen Prozessbereichen auf Ebene 1, zwischen
  Modulen eines geoeffneten Bereichs auf Ebene 2 und zwischen
  Detailschritten/Reitern des Moduls auf Ebene 3. Eine sichtbare
  Pfadnavigation wie `Gesamtuebersicht > PreProcess > ma_project >
  Randbedingungen` wechselt gezielt in die uebergeordnete Ebene. Sie setzt
  weder das Projekt noch aktive Reiter, Auswahl oder Entwuerfe zurueck.
- **Korrekturpfade:** Validierungs- und Reviewbefunde verlinken mit einer
  ausdruecklich benannten Aktion auf ihr Zielmodul, etwa
  `Gebaeudemodell korrigieren -> ma_building`. Sie sind keine versteckte
  Bedeutung der allgemeinen Zurueck-Taste und starten keine automatische
  Iteration.

Die historische Grafik unter
`docs/project/archive/workflow/WORKFLOW_DIAGRAM_v0.1.0_2026-06-18.jpg`
liefert die fachlichen Beziehungen, Rollen und Rueckkopplungen. Ihre lange
statische Swimlane ist jedoch nicht das Bildschirm-Layout. Die konkrete
interaktive, vektorfaehige Darstellung wird auf Basis des vorhandenen
`workflow_graph.py` geplant; eine neue Grafikbibliothek wird nicht ohne
eigenen Bedarfsnachweis und Freigabe eingefuehrt.

## UI-S1 Workflownavigation: nach UD-114 zurueckgestellt 2026-07-31

Der erste Streamlit-Entwurf wurde nach dem Council-Blocker technisch
zurueckgestellt. Die dreistufige Workflowansicht wird als letzter
Migrationsslice neu aus dem dann zentralen, UI-neutralen Prozess- und
Statusvertrag abgeleitet. Sie darf keine Reihenfolge oder Statuslogik neben
`ma_workflow` fuehren.

Vor der spaeteren Umsetzung wird eine eigene Button- und Sprungzielmatrix fuer
Ebene 1 bis 3 abgestimmt. Diese Navigation darf sich bewusst von der direkten
Arbeits-/Modulansicht unterscheiden. Jeder Button benoetigt jedoch ein
eindeutiges Ziel und darf weder Entwuerfe zuruecksetzen noch Fachwerte,
Selections, Varianten, RUNs oder Reviewzustaende automatisch veraendern.

## Nicht freigegebene Korrekturpunkte der direkten Bearbeitungsansicht 2026-08-19

Die direkte Bearbeitungsansicht braucht auf Fachseiten wieder explizite
Navigation zu `Uebersicht` und `Gesamtworkflow`. In der Workflowansicht soll
die Projektwahl anschliessend direkt `ma_project` oeffnen, nicht die
Bearbeitungsuebersicht. Die Begriffe `Start` und `Uebersicht` sind je Ebene
eindeutig zuzuordnen; die spaetere Button-/Sprungzielmatrix bleibt die
fuehrende Detailplanung.

`Weiter` in der fachlichen PreProcess-Kette soll vor dem Seitenwechsel den
Mindeststand des aktuellen Moduls pruefen. Bei blockierenden Fehlern bleibt
die Fachseite aktiv und nennt die fehlenden Angaben. Bei Erfolg wird der
gueltige Projektentwurf gespeichert, an den Nachfolger uebergeben und
abhaengige Staende als `update_required` markiert. Dies ersetzt keine
expliziten Fachfreigaben oder Release-Handover.

Als separate Fehlerkorrekturen sind der Streamlit-Session-State-Fehler beim
Analyse-Output-Pfad sowie die falsche Anzeige von Wirtschaftsannahmen in
`ma_assessment` aufzunehmen. `ma_assessment` braucht eine eigene, als geplant
gekennzeichnete Ansicht; `ma_economy`-, `ma_sustainability`- und
Bewertungsinhalte bleiben voneinander getrennt. Der Umfang ist noch nicht
freigegeben und wird nicht still mit der letzten Workflow-UI-Migration
vermischt.
