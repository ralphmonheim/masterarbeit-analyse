# P027 Querschnitt UI, Workflow, Validation und Feedback

Stand: 2026-07-12
Status: Aktiv, begleitend
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
