# Chat-Handover – Projektinput: Literatur, KPI und Datenhaltung

Stand: 2026-08-14

## Abgeschlossener Arbeitsstand

Mit `input aufnehmen` wurden vier Eingänge geprüft. Drei zuerst vorliegende
Dateien wurden nach
`data/project_inbox/processed/2026-08-14_project_inputs/` überführt:

- `Literaturpaket_Simulationsstufen_AKTUELL_2026-08-13.zip`;
- `annotations.txt`;
- `Kompletter_Diskussionsprozess_KPI_Bewertung_Architektur.md`.

Das Literaturregister unter `config/ma_database/literature/` enthält 21
Metadatensätze, eine Excel-Arbeitsmappe und 21 Einzelanalysen. Es entstand
aus der Quellenmatrix und den Markdown-Metadaten des Nutzerpakets; die im ZIP
enthaltenen PDF-Dateien wurden weder entpackt noch inhaltlich verarbeitet.
Alle Einträge führen `verification_basis: user-described`,
`review_status: requires_manual_review` und sind nicht `citation_ready`.
`citation_ready` bedeutet, dass eine konkrete Originalfundstelle manuell
gelesen und für eine Zitation bestätigt wurde.

`annotations.txt` wurde als IDA-ICE-Quellkonfiguration eingeordnet. Es ist
weder ein freigegebener neutraler Ergebnisexport noch eine Quelle für
Normnachweise. Die darin enthaltenen Angaben wurden deshalb nicht in die
Import- oder Analysepipeline übernommen.

Der KPI-Diskussionsprozess wurde durch neue Abschnitte in den führenden Plänen
eingeordnet. Er dient als Methodenhintergrund, entscheidet aber weder
Kriterien, Gewichte, PASS/FAIL-Schwellen noch Modulnamen.

Der nachgereichte Handover zur Datenbanktransformation und PostgreSQL wurde
ebenfalls in den Verarbeitungsordner überführt. Seine V1-/Post-V1-Grenze ist
als UD-129 und in P032 dokumentiert: V1 bleibt dateibasiert; PostgreSQL ist
eine spätere Option und keine beauftragte Migration.

## Führende Quellen

- Das lokale Routing-Manifest unter
  `data/project_inbox/processed/2026-08-14_project_inputs/ROUTING_MANIFEST.md`
  ordnet die vier Eingänge und ihren Verarbeitungsstatus zu.
- [P019 – Analyse Stufe 2 Optimierung](../../plans/inbox/260622_Plan_P019_Stage2_Optimierung.md) führt die offene Stage-2-Feasibility und Optimierungsgrenzen.
- [P020 – Analyse Stufe 3 Norm-Nachweis](../../plans/inbox/260622_Plan_P020_Stage3_Standards_Verification.md) führt Nachweis-, Methoden- und Rechtegates.
- [P021 – Analyse Stufe 4 Sensitivität](../../plans/inbox/260622_Plan_P021_Stage4_Sensitivitaet.md) führt offene Sensitivitätsmetriken und Ereignisdefinitionen.
- [P024 – ma_assessment Konzept](../../plans/inbox/260622_Plan_P024_ma_assessment_Konzept.md) führt die getrennte Entscheidungsvorlage ohne Fachberechnung.
- [P029 – ma_analyse Service- und Runner-Bereinigung](../../plans/inbox/260627_Plan_P029_ma_analyse_Service_Runner_Bereinigung.md) führt die technische PostProcess-Grenze.
- [P032 – Architecture Benchmark und Migrationsplanung](../../plans/inbox/260715_Plan_P032_Architecture_Benchmark_Migration.md) führt die spätere Datenbankoption.
- [UD-129](../../decisions/USER_DECISIONS_MASTERTHESIS_CODE.md) ist die Nutzerentscheidung zur V1-/Post-V1-Grenze.

## Übertragene offene Punkte

- Vor einer Thesis-Zitation, Quellenbehauptung oder Regelimplementierung
  prüft der Nutzer die Originalfundstelle, Ausgabe und zulässige Verarbeitung
  manuell. Der Prüfstand wird im internen Quellenregister unter
  `config/ma_database/literature/` dokumentiert.
- Der neutrale Ergebnisvertrag bleibt OP-017; projektbezogene Kriterien und
  der Bewertungszeitraum bleiben OP-018. Beide stehen in
  `docs/project/decisions/USER_DECISIONS_OPEN_POINTS.md`.
- Eine PostgreSQL- oder sonstige Persistenzmigration bleibt P032-W6 und wird
  erst nach V1 als eigener, freigegebener Planungsslice aufgenommen.

## Prüfung und Abgrenzung

- Die Excel-Arbeitsmappe enthält die fünf Blätter `Quellenmatrix`,
  `Themenlandkarte`, `Prüfwarteschlange`, `Fehlende Quellen` und
  `Abgleichprotokoll` sowie 21 Quellen- und 21 Prüfwarteschlangeneinträge.
- 21 Metadatenanalysen, die Syntax des lokalen Register-Importers und
  `git diff --check` wurden geprüft.
- Der lokale Navigator wurde aktualisiert und anschließend erfolgreich
  validiert.
- Es wurde kein Commit, Tag oder Push erzeugt.
- Bereits vorhandene, nicht zu diesem Projektinput gehörende Änderungen im
  Arbeitsbaum wurden weder geprüft noch verändert. Nachfolgende Bearbeitung
  bewahrt sie und grenzt diesen Projektinput über das Routing-Manifest ab.
