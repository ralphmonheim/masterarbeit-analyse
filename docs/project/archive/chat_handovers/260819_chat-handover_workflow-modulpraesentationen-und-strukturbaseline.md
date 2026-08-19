# Chat-Handover – Workflow-Modulpraesentationen und offene Strukturbaseline

Stand: 2026-08-19
Status: uncommitteter Dokumentationsstand; die Strukturbaseline ist noch nicht
bestaetigt.

## Abgeschlossener Arbeitsstand

- Unter `docs/project/architecture/workflow/` wurden zwei eigenstaendige
  HTML-Darstellungen vorbereitet:
  `WORKFLOW_MODULE_PRESENTATION_v0.2.0_2026-08-19.html` als filterbare
  Uebersicht der 30 katalogisierten Komponenten und
  `WORKFLOW_MODULE_DETAILS_v0.2.0_2026-08-19.html` als fachliche Vertiefung.
- `docs/project/architecture/workflow/README.md` und der Unreleased-Abschnitt
  von `CHANGELOG.md` verweisen auf beide Dateien. Die HTML-Dateien sind nur
  Darstellungen; sie ersetzen keine Architektur-, Workflow-, Status- oder
  Entscheidungsquelle.
- Die Stufe-A-Auswertung vom 2026-08-15 hat die archivierten Handover und die
  neuen Markdown-Eingaenge klassifiziert. Der dort bezeichnete
  PostgreSQL-Eingang ist die Datei
  `Chat-Handover – Vollständiger Arbeitsprozess zur Datenbanktransformation und PostgreSQL.md`.
  Sie war bytegleich mit dem bereits am 2026-08-14 aufgenommenen
  Konzeptdokument. Es wurden weder PostgreSQL noch eine Datenbank oder
  Fachdaten importiert.

## Fuehrende Quellen und Rollen

- P007,
  `docs/project/plans/inbox/Masterarbeit_VSCode_Projektplan_2026-06-21.md`,
  fuehrt den Gesamt- und Architekturrahmen sowie den nach UD-112
  konsolidierten V1-Prozess.
- `docs/project/workflow/README.md` fuehrt den fachlichen Gesamtworkflow.
- `docs/project/architecture/TARGET_ARCHITECTURE.md` fuehrt die technische
  Zielstruktur.
- P027,
  `docs/project/plans/inbox/260622_Plan_P027_Querschnitt_UI_Workflow_Validation_Feedback.md`,
  fuehrt den technischen Workflow-Querschnitt.
- P037,
  `docs/project/plans/inbox/260813_Plan_P037_Dokumentationshierarchie_Workflowwissen_UI_Informationsarchitektur.md`,
  und UD-128 fuehren Dokumenthierarchie und UI-Informationsrollen.
- `docs/project/architecture/reviews/2026-08-15/HANDOVER_STRUCTURE_DECISION_TEMPLATE.md`
  ist nur die nicht autoritative Gespraechsvorlage.

## Uebertragung der offenen Inhalte

- OP-019 in
  `docs/project/decisions/USER_DECISIONS_OPEN_POINTS.md` fuehrt nun die
  gemeinsame Entscheidung ueber die Strukturpunkte S-01 bis S-13 und die
  Anti-Regression-Baseline. Bis zu ihrer Bestaetigung werden Vorschlaege wie
  eine zusaetzliche `SimulationCase`-Identitaet, neue Module
  `ma_sim_external` oder `ma_quantity`, neue Stage-Top-Level-Module und eine
  verbindliche Pareto-/Gewichtungsmethode nicht uebernommen.
- Der P037-Abschnitt `Nachlauf 2026-08-19: HTML-Modulpraesentationen` fuehrt
  die konkrete Restarbeit: Quellenabgleich, Link-/HTML-Pruefung,
  Browser-/Filter-Smoke-Test, Lesbarkeits- und Barrierefreiheitspruefung sowie
  die Klaerung der README-Ablage.
- Der Nachlauf benennt zwei bereits sichtbare Inhaltskonflikte: Der
  HTML-Entwurf verwendet noch `ma_analyse.stage_1_dimensioning` statt des
  Ziel-Owners `ma_dimensionierung` und nennt Pareto/Ranking als Ausgabe,
  obwohl diese Bewertungsmethode noch offen ist.
- `docs/ma_core/README.md` erscheint im Arbeitsbaum als geloescht; derselbe
  Inhalt liegt unversioniert unter `docs/ma_data_export/ma_core/README.md`.
  P037 dokumentiert die erforderliche Klaerung. Dieser Handover bestaetigt
  die Verschiebung nicht und nimmt sie nicht zurueck.

## Freigabegrenze

Die inhaltliche Bestaetigung der Baseline und ihre Umsetzung sind zwei
getrennte Schritte. Erst nachdem der Nutzer die Baseline bestaetigt hat, darf
eine danach erneut und exakt erteilte `Freigabe zur Umsetzung` strukturelle
Aenderungen an P007, Zielarchitektur, fachlicher Workflowquelle, P027/P037
oder den Entscheidungen ausloesen. Bis dahin gilt der neuere kanonische Stand;
alte Handover- oder historische P007-Abschnitte duerfen ihn nicht ersetzen.

## Repository-Snapshot und Nachweise

- Snapshot-Zeitpunkt: 2026-08-19; Branch `main`; Ausgangs-HEAD `5562b5d`
  (`Release 0.42.1 - Planung und Referenzvergleich`).
- Vor dem Handover waren `CHANGELOG.md` und
  `docs/project/architecture/workflow/README.md` geaendert,
  `docs/ma_core/README.md` geloescht und die alternative README-Ablage sowie
  beide HTML-Dateien unversioniert. Die Handover-Routine ergaenzt
  ausschliesslich die fuehrenden Planungs-/Entscheidungsquellen, diesen
  Snapshot und den Handover-Index.
- Die beiden HTML-Dateien enthalten jeweils ein eingebettetes Skript; die
  Uebersichtsdatei enthaelt 30 Komponenteneintraege. Es wurden keine
  `TODO`-/`FIXME`-/`TBD`-Marker gefunden.
- `git diff --check` war vor der finalen Archivierung sauber. Produkt-, UI-,
  Browser- und vollstaendige Pytest-Pruefungen waren fuer diesen
  Dokumentationsstand zu diesem Zeitpunkt noch nicht ausgefuehrt.
- Der vorgeschriebene Blind-Review wurde vor der Archivierung durchgefuehrt;
  seine Verstaendlichkeitsbefunde zu Pfaden, Begriffen und Freigabestufen
  wurden in diesen Snapshot eingearbeitet.
- Die abschliessende fokussierte Pruefung
  `tests/test_architecture_guardrails.py` und
  `tests/test_p037_workflow_information.py` bestand mit `11 passed`.
  `git diff --check` und die schreibfreie Navigator-Validierung mit
  `--validate-only` bestanden ebenfalls. Der Navigator wurde ohne neue exakte
  `Freigabe zur Umsetzung` nicht aktualisiert.

## Nicht Bestandteil dieses Handovers

Der Handover implementiert keine Produktfunktion, importiert keine Datenbank,
verarbeitet keine geschuetzten IDA-/EQUA-Inhalte, bestaetigt keine
Architekturbaseline und korrigiert die beiden HTML-Praesentationen oder die
README-Ablage nicht. Die genannten offenen Inhalte werden ausschliesslich in
OP-019 und P037 weitergefuehrt.

Dieser Snapshot ist historisch. Fuehrend bleiben die oben genannten
kanonischen Quellen.
