# P027 Querschnitt UI, Workflow, Validation und Feedback

Stand: 2026-07-18
Status: Aktiv, begleitend; V1-Infokarten- und Bedienansichtsslice umgesetzt
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
verweisen. Start, Zurueck und Weiter beenden diesen Sonderkontext. Eine
allgemeine Workflow-Orchestrierung und zentrale Validierung bleiben offen.

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

`ma_core.compliance` stellt UI-neutrale OperationRequests, Metadaten-
Preflights, Entscheidungen, Warntexte, sichere Operationswrapper und ein
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
