# Unabhaengiger Umsetzungsplan: Handover-Input aufnehmen, Strukturbaseline entscheiden und kanonisch integrieren

Datum: 260815  
Status: Sol-geplant und qualitaetsgeprueft; noch nicht zur Umsetzung freigegeben

## Arbeits-Prompt

### Rolle und Kontext

Du arbeitest im Masterarbeitsprojekt als Senior-Projektentwickler und technischer Architekturberater. Die Software bleibt in dieser Phase unveraendert. Ziel ist ausschliesslich eine nachvollziehbare Input-Verarbeitung sowie die konsistente Projekt-, Planungs-, Entscheidungs- und Dokumentationsstruktur.

### Ziel und erwartetes Ergebnis

Analysiere alle archivierten Chat-Handover sowie die neuen Eingaenge vom 15.08.2026. Verarbeite die neuen Inputs nach `PROJECT_INPUT_WORKFLOW.md`:

- Eindeutig erkannte Plaene werden regelkonform in die Plan-Inbox verschoben und aufgenommen.
- Neue Nicht-Plan-Inputs werden nach Freigabe ausgewertet.
- Verarbeitete Originale werden anschliessend nach `data/project_inbox/processed/` verschoben, soweit Rechte-, Inhalts- und Schutzgates dies erlauben.
- Geschuetzte oder nicht freigegebene Inhalte bleiben ungeoeffnet und unverarbeitet.

Vor jeder kanonischen Uebernahme struktureller Inhalte muss aus den Handovern und fuehrenden Projektquellen eine vollstaendige Strukturentscheidungsvorlage entstehen. Sie wird gemeinsam mit dem Nutzer besprochen und enthaelt:

- Ist-Stand,
- moegliche Zielstaende,
- Konflikte und Doppelungen,
- zwei bis drei Optionen bei echten Entscheidungen,
- eine begruendete Empfehlung,
- Auswirkungen,
- offene Entscheidungen,
- eine Anti-Regression-Baseline.

Erst ein danach vom Nutzer ausdruecklich bestaetigter Strukturstand darf als neue oder fortgeschriebene Strukturbaseline kanonisch dokumentiert werden. Fuer die anschliessenden strukturellen Dokumentaenderungen ist erneut die exakte Freigabeformulierung `Freigabe zur Umsetzung` erforderlich.

Die spaetere kanonische Zuordnung lautet:

- bestaetigte Nutzerentscheidungen in die Nutzerentscheidungen,
- strukturelle Zielbilder und Restarbeit in die fuehrenden aktiven Plaene,
- Architekturgrenzen in die passende Architekturquelle,
- fachlicher Gesamtworkflow in die dafuer bestaetigte operative Workflowquelle,
- offene Entscheidungen ausschliesslich in `USER_DECISIONS_OPEN_POINTS.md`,
- Status nur in Planindex und Planstatus,
- historische Handover bleiben historische Referenzen.

Alte Handover duerfen die bestaetigte Strukturbaseline niemals stillschweigend zuruecksetzen. Fuehrender Gesamtplan und einschlaegige Nutzerentscheidungen schlagen aeltere oder widersprechende Handover. Abweichungen werden gestoppt und sichtbar als historisch, zurueckgestellt oder konfliktbehaftet markiert.

Nach der kanonischen Integration wird die resultierende Gesamtstruktur noch einmal mit dem Nutzer abgeglichen. Erst danach duerfen spaetere Code- und Funktionsarbeiten geplant werden.

### Scope

Einzubeziehen sind:

- alle Dateien unter `docs/project/archive/chat_handovers/`,
- neue Markdown-Handover und eindeutig erkennbare Plaene unter `data/project_inbox/new/`,
- der bereits aufgenommene Parametergruppen-Referenzplan fuer P015,
- die fuehrenden Plaene P007 bis P037,
- der unabhaengige V1-5Z-Plan,
- offene Nutzerentscheidungen,
- getroffene Nutzerentscheidungen,
- technische Entscheidungen,
- passende Architektur- und Workflow-Dokumente,
- Planindex, Planstatus, Handover-Index und Changelog.

Besonders zu pruefen sind:

- Ergebnisimport, PostProcess und Analyseebene,
- IFC-, Heizlast- und Zonengrenzen,
- Prozessmessung,
- Rechte- und Inhaltsgrenzen,
- V1-5Z-Migration,
- KPI-, Bewertungs-, Workflow- und PostgreSQL-Zielbilder,
- Parametergruppen und P015-Anbindung,
- die gemeinte Rolle einer vom Nutzer als `Workflow_Gesamtplan` bezeichneten Quelle.

### Nicht-Ziele

- Keine Code-, API-, Laufzeit- oder Produktfunktionsaenderungen.
- Keine Aenderungen produktiver Fachdaten oder Ergebnisdaten.
- Keine PostgreSQL-Einfuehrung, neuen Abhaengigkeiten oder Datenbankmigration.
- Keine automatische IDA-/EQUA-Verarbeitung.
- Keine Verarbeitung geschuetzter ZIP-, Norm-, Literatur-, IDM- oder IDA-Inhalte ohne objektbezogene Freigabe.
- Keine neue Architektur oder Modulnamen allein aus einem Handover ableiten.
- Keine neue Datei namens `Workflow_Gesamtplan` erfinden.
- Keine Strukturentscheidung stillschweigend aus einem Handover uebernehmen.
- Keine spaetere Codeplanung vor der gemeinsamen Strukturbesprechung und Baseline-Bestaetigung.

Die Verschiebung eindeutig erkannter Plaene und die regelkonforme Verarbeitung beziehungsweise Verschiebung der Input-Originale nach `processed` sind als begrenzte Input-Governance-Aktionen innerhalb dieses Dokumentationsscopes zulaessig. Sie sind keine produktiven Datenmigrationen.

### Bekannte Eingaben, Annahmen und Grenzen

- Der Parametergruppenplan ist bereits als P015-Ergaenzung ueber UD-125 und P015-S5A/S5B eingeordnet.
- PostgreSQL bleibt gemaess UD-129 eine Post-V1-Option.
- Handover sind keine aktive Projektwahrheit.
- Bei Konflikten sind der fuehrende Gesamtplan, bestaetigte Nutzerentscheidungen und die danach bestaetigte Strukturbaseline massgeblich.
- Neue Handover duerfen nur als bestaetigte Nutzerentscheidung, offene Frage, Folgeoption, methodischer Hintergrund, historische Alternative oder Konflikt eingeordnet werden.
- ZIP-Eingaenge bleiben ungeoeffnet, bis Rechte und Inhaltsscope objektbezogen geklaert sind.
- Im Repository existiert nach aktueller gezielter Suche keine Datei mit dem exakten Namen `Workflow_Gesamtplan`.
- Wahrscheinliche, aber unterschiedlich verantwortliche Kandidaten sind:
  - P007 als fuehrender Gesamt- und Architekturrahmenplan,
  - `docs/project/workflow/README.md` als operative fachliche Workflowquelle,
  - P027 als technischer Querschnitts- und Workflowplan,
  - P037 als Plan zur Dokumentationshierarchie und UI-Informationsarchitektur,
  - `docs/project/architecture/TARGET_ARCHITECTURE.md` als technische Zielarchitektur.
- Diese Rollen duerfen nicht ohne Nutzerentscheidung in einer neuen Gesamtplandatei zusammengezogen werden.

### Pruef- und Dokumentationsanforderungen

- Fuer jeden uebernommenen Punkt Quell-Handover, Zielquelle und Einordnungsart dokumentieren.
- Doppelungen, Architekturkonflikte und zurueckgesetzte Vorschlaege sichtbar markieren.
- Offene Entscheidungen ausschliesslich in `USER_DECISIONS_OPEN_POINTS.md` fuehren.
- Vor jeder strukturellen Festschreibung eine vollstaendige Strukturentscheidungsvorlage mit dem Nutzer besprechen.
- Den bestaetigten Zielstand mit Geltungsbereich als Anti-Regression-Baseline dokumentieren.
- Nach Aenderungen Planindex, Planstatus, Handover-Index und Changelog konsistent halten.
- Den Navigator nach zulaessigen Dokumentations- oder Pfadaenderungen aktualisieren und validieren.
- Abschliessend berichten, welche Handover vollstaendig eingeordnet, bereits abgedeckt, zurueckgestellt, historisch oder konfliktbehaftet sind.
- Erst nach Abschluss der Gesamtstrukturbesprechung spaetere Code- und Funktionsarbeiten planen.

## Ziel

Der begrenzte Umsetzungsscope besteht aus zwei klar getrennten Dokumentationsstufen mit einem menschlichen Strukturentscheidungs-Gate dazwischen.

### Stufe A: Sichere Input- und Planaufnahme

Ergebnis:

1. alle vorhandenen archivierten und neuen Handover sind inventarisiert;
2. eindeutig erkannte Plaene sind nach `PROJECT_INPUT_WORKFLOW.md` aufgenommen;
3. Nicht-Plan-Inputs sind klassifiziert;
4. geschuetzte Inhalte wurden nicht verarbeitet;
5. fuer alle strukturellen Aussagen liegt eine nicht autoritative Strukturentscheidungsvorlage vor;
6. noch keine Architektur-, Workflow-Gesamtplan- oder sonstige Strukturentscheidung wurde kanonisch festgeschrieben.

### Menschliches Strukturentscheidungs-Gate

Der Nutzer bespricht und entscheidet anhand der Vorlage:

- die gewuenschte Gesamtstruktur,
- die fuehrenden Dokumentrollen,
- die Bedeutung des Begriffs `Workflow_Gesamtplan`,
- Modul- und Ownergrenzen,
- Schnittstellen und Prozessgrenzen,
- den Umgang mit widersprechenden Handovern,
- die Anti-Regression-Baseline.

Der Nutzer bestaetigt den gewuenschten Baselinestand ausdruecklich. Danach ist fuer Stufe B erneut die exakte Formulierung `Freigabe zur Umsetzung` erforderlich.

### Stufe B: Kanonische Strukturintegration

Ergebnis:

1. die bestaetigte Baseline ist als Nutzerentscheidung dokumentiert;
2. nur die durch diese Baseline bestaetigten Strukturpunkte sind in fuehrende Plaene, Architektur- und Workflowquellen uebernommen;
3. aeltere widersprechende Handover sind sichtbar historisch oder zurueckgestellt;
4. Planindex, Planstatus, Handover-Index und Changelog sind konsistent;
5. verarbeitete Nicht-Plan-Originale sind regelkonform nach `processed` verschoben;
6. Navigator und Dokumentationspruefungen sind erfolgreich;
7. Code und Softwarefunktionen bleiben unveraendert.

## Scope und Nicht-Ziele

### Umsetzungsscope

Der Scope umfasst ausschliesslich Input-Governance, Markdown-Dokumentation und Navigatorpflege:

- `data/project_inbox/new/`
- `data/project_inbox/processed/`
- `docs/project/plans/inbox/`
- `docs/project/plans/PLAN_INDEX.md`
- `docs/project/plans/PLAN_STATUS.md`
- `docs/project/archive/chat_handovers/`
- `docs/project/archive/chat_handovers/INDEX.md`
- `docs/project/decisions/`
- die betroffenen aktiven Plaene P007 bis P037
- der unabhaengige V1-5Z-Plan
- `docs/project/architecture/`
- `docs/project/workflow/`
- `CHANGELOG.md`
- der lokale semantische Navigator nach erfolgter Freigabe

Die umfangreiche Handover-Menge wird innerhalb dieses einen Integrationsscopes in kontrollierten Dokumentationsslices verarbeitet. Es entsteht kein neuer formeller P-Plan.

### Erlaubte Input-Aktionen

- Eindeutig erkannte Plaene duerfen nach `docs/project/plans/inbox/` verschoben und aufgenommen werden.
- Nicht-Plan-Eingaenge duerfen nach Freigabe gelesen und eingeordnet werden, sofern kein Rechte- oder Inhaltsgate entgegensteht.
- Nach abgeschlossener Verarbeitung duerfen Originale regelkonform in einen datierten Unterordner von `data/project_inbox/processed/` verschoben werden.
- Unklare oder gesperrte Originale bleiben unveraendert unter `new/`.
- Es werden keine Dateien geloescht.

### Ausdrueckliche Nicht-Ziele

- Keine Aenderung unter `src/`, `tests/`, `config/` oder `Skripte/`.
- Keine produktive Datenmodell-, Schema-, Persistenz- oder API-Aenderung.
- Keine Modulverschiebung oder Umbenennung.
- Keine Einfuehrung von `SimulationCase`, `CASE-ID`, `ma_sim_external`, `ma_quantity` oder anderen allein aus Handovern abgeleiteten Strukturen.
- Keine Aktivierung automatischer Simulation, direkter IDA-Steuerung oder externer Connectoren.
- Keine Festlegung von KPI-Gewichten, PASS-/FAIL-Schwellen, Pareto-Algorithmen, Normregeln, Kostenmodellen oder Nachhaltigkeitsmethoden ohne eigene Entscheidung.
- Keine neue Dokumentationswahrheit neben den bestaetigten Rollen.
- Keine Datei namens `Workflow_Gesamtplan`, solange deren Rolle und Zielort nicht eindeutig bestaetigt wurden.
- Keine Aenderung struktureller Wahrheiten vor dem menschlichen Baseline-Gate.
- Kein Commit, Push, Tag oder Release.
- Keine Code- oder Funktionsplanung vor Abschluss dieser Strukturarbeit.

## Betroffene Bereiche

### Input und Handover

- Alle vorhandenen Dateien unter `docs/project/archive/chat_handovers/`
- Alle neuen Markdown-Eingaenge unter `data/project_inbox/new/`
- Eindeutig erkannte Planinputs
- Der bereits aufgenommene P015-Referenzplan
- Der Handover-Index als historischer Routingnachweis

Historische Handover werden nicht inhaltlich umgeschrieben. Neue Nicht-Plan-Inputs werden nach abgeschlossener Verarbeitung nach `processed` verschoben und ueber einen versionierten, kompakten Einordnungssnapshot nachvollziehbar gehalten.

### Strukturentscheidungsvorlage

Die Vorlage wird als nicht autoritativer, datierter Review im bereits vorhandenen Architektur-Reviewbereich abgelegt, beispielsweise:

`docs/project/architecture/reviews/2026-08-15/HANDOVER_STRUCTURE_DECISION_TEMPLATE.md`

Die Vorlage ist keine Freigabe und keine Zielarchitektur. Sie buendelt alle strukturellen Entscheidungspunkte fuer die Nutzerbesprechung.

### Entscheidungen

- `USER_DECISIONS_MASTERTHESIS_CODE.md`
- `USER_DECISIONS_OPEN_POINTS.md`
- `TECHNICAL_DECISIONS.md` nur fuer technische Praezisierungen bereits bestaetigter Nutzerentscheidungen

### Fuehrende Plaene und Dokumentrollen

| Rolle | Derzeit wahrscheinliche Quelle | Vor Festschreibung zu klaeren |
| --- | --- | --- |
| Gesamt- und Architekturrahmen | P007 | aktueller Geltungsbereich gegen spaetere UDs |
| operative fachliche Workflowquelle | `docs/project/workflow/README.md` | ob dies mit `Workflow_Gesamtplan` gemeint ist |
| technischer Workflow-Querschnitt | P027 | keine zweite fachliche Gesamtworkflowquelle |
| Dokumenthierarchie und UI-Informationsrollen | P037 / UD-128 | bestehende Rollentrennung erhalten |
| technische Zielarchitektur | `TARGET_ARCHITECTURE.md` | nur bestaetigte Baseline uebernehmen |
| laufende Architekturmigration | P032 | Optionen nicht als Zielwahrheit ausgeben |
| Status | `PLAN_INDEX.md`, `PLAN_STATUS.md` | keine Fach- oder Architekturentscheidungen duplizieren |

### Fachliche Strukturcluster

| Themencluster | Derzeit fuehrende Quellen |
| --- | --- |
| Ergebnisimport und RUN-/VAR-Vertrag | P009, P018, P029, OP-017 |
| Datenvorbereitung und PostProcess | P019, P029, P036, UD-122, UD-126 |
| KPI, Feasibility und technische Analyse | P019, P020, P021, P024, OP-018 |
| Wirtschaftlichkeit und Nachhaltigkeit | P022, P023, P024 |
| Workflow und Rules | P027, P032, UD-112, UD-114 |
| IFC, Gebaeudehuelle, Heizlast und Zonen | P012, P013, P016, OP-012, OP-014, unabhaengiger V1-5Z-Plan |
| Prozessmessung | P030, OP-009 |
| Rechte, Normen und geschuetzte Inhalte | P020, P031, OP-016 |
| Post-V1-Datenhaltung und PostgreSQL | P032, UD-129 |
| Parametergruppen | P015, UD-125, P015-S5A/S5B |
| Dokumenthierarchie | P037, UD-128 |

## Umsetzungsschritte

### Slice 1: Freigabe- und Arbeitsbaum-Preflight

1. Keine Umsetzung vor der exakten Nutzerformulierung `Freigabe zur Umsetzung`.
2. Nach Freigabe `git status --short --untracked-files=all` erfassen.
3. Alle bereits vorhandenen Aenderungen als fremden beziehungsweise begonnenen Arbeitsstand behandeln.
4. Insbesondere vorhandene Aenderungen an P015, P032, Planindex, Planstatus, Changelog, Entscheidungsdatei und Handover-Index erhalten.
5. Eine konkrete Aenderungs-Allowlist fuer Stufe A festlegen.
6. Keine Datei ausserhalb dieser Allowlist veraendern.

### Slice 2: Input-Inventar und Rechteklassifikation

1. Beide Eingaenge gemaess `PROJECT_INPUT_WORKFLOW.md` erfassen:
   - `data/project_inbox/new/`
   - `docs/project/plans/inbox/`
2. Fuer jede neue Datei dokumentieren:
   - Dateiname,
   - Typ,
   - Groesse,
   - Aenderungsdatum,
   - SHA-256,
   - Plan oder Nicht-Plan,
   - Inhaltsscope,
   - Rechte-/Schutzstatus,
   - vorgesehener Zielbereich.
3. Markdown-Handover duerfen nach Freigabe gelesen werden.
4. ZIP-, PDF-, Norm-, Literatur-, IDM- und IDA-/EQUA-Inhalte nur anhand zulaessiger Metadaten einordnen und nicht oeffnen.
5. Gesperrte oder unklare Dateien bleiben unter `new/`.

### Slice 3: Eindeutige Planaufnahme

1. Eindeutig erkannte Plaene nach `docs/project/plans/inbox/` verschieben.
2. Vor der Aufnahme auf Duplikate, fuehrenden Gesamtplan und bestehende Teilplaene pruefen.
3. Einen Plan nur dann als neuen P-Plan aufnehmen, wenn kein bestehender Plan dieselbe Verantwortung fuehrt.
4. Reine Ergaenzungs- oder Referenzplaene dem fuehrenden Plan zuordnen.
5. Den bereits aufgenommenen Parametergruppenplan weiterhin als P015-Referenz fuehren:
   - UD-125 bleibt die Entscheidung,
   - P015-S5A/S5B bleiben der Umsetzungsscope,
   - keine neue Plan-ID,
   - keine neue Umsetzungsfreigabe.
6. Planindex und Planstatus nur fuer diese eindeutige Planaufnahme aktualisieren.
7. Planaufnahme und Input-Metadaten duerfen vor der Strukturentscheidung erfolgen; sie erteilen keine Architekturfreigabe.

### Slice 4: Vollstaendige Handover-Klassifikation

1. Jeden archivierten und neuen Handover gegen seine genannten fuehrenden Quellen pruefen.
2. Inhalte mit folgenden Klassen erfassen:
   - `BESTAETIGTE_ENTSCHEIDUNG`
   - `BEREITS_ABGEDECKT`
   - `OFFENE_NUTZERENTSCHEIDUNG`
   - `RESTARBEIT_AKTIVER_PLAN`
   - `NICHT_FREIGEGEBENE_FOLGEOPTION`
   - `METHODISCHER_HINTERGRUND`
   - `HISTORISCHE_ALTERNATIVE`
   - `ARCHITEKTURKONFLIKT`
   - `RECHTE_ODER_EVIDENZGATE`
   - `VERWORFEN`
3. Fuer jeden strukturellen Punkt festhalten:
   - Quell-Handover und Abschnitt,
   - neutrale Aussage,
   - heutiger Ist-Stand,
   - fuehrende Quelle,
   - Einordnungsart,
   - moegliche Zielwirkung,
   - Konflikt- und Regressionsrisiko.
4. Noch keine strukturelle Aussage in Architektur, Workflow-Gesamtquelle oder aktive Strukturplaene uebernehmen.

### Slice 5: Governance-Kollisionen als Befund vorbereiten

1. Die doppelte Kennung `OP-017` in `USER_DECISIONS_OPEN_POINTS.md` dokumentieren.
2. `OP-017 Neutraler Ergebnisvertrag und Dateninventar` wegen seiner aktiven Verweise als zu erhaltende Kennung empfehlen.
3. Fuer den Council-Spezialistenpunkt die erste freie eindeutige Kennung, nach aktuellem Bestand voraussichtlich `OP-019`, als mechanische Korrektur vorschlagen.
4. Die Korrektur noch nicht ausfuehren, wenn sie Teil der zu bestaetigenden Strukturbaseline wird.
5. Alle betroffenen Verweise inventarisieren.

### Slice 6: Rolle von `Workflow_Gesamtplan` read-only klaeren

1. Gezielt bestaetigen, dass keine Datei mit dem exakten Namen `Workflow_Gesamtplan` existiert.
2. Die Rollen der Kandidaten read-only gegeneinander abgrenzen:
   - P007,
   - `docs/project/workflow/README.md`,
   - P027,
   - P037,
   - `TARGET_ARCHITECTURE.md`.
3. Pruefen, ob ein weiterer versionierter Kandidat durch aktuelle Dokumente als Workflow-Gesamtquelle bezeichnet wird.
4. Keine neue Datei erfinden.
5. In der Strukturentscheidungsvorlage zwei bis drei Optionen darstellen:
   - Option A: bestehende Rollentrennung gemaess UD-128 erhalten;
   - Option B: eine vorhandene Quelle ausdruecklich als zusaetzlichen Workflow-Gesamteinstieg bestaetigen;
   - Option C: nur bei nachgewiesenem Bedarf einen neuen Gesamtplan separat planen.
6. Empfehlung: Option A, solange der Nutzer keinen nachweisbaren Bedarf fuer eine neue kanonische Quelle bestaetigt. Dadurch bleiben P007, operative Workflowquelle, technische Architektur und Status getrennt.

### Slice 7: Vollstaendige Strukturentscheidungsvorlage erstellen

Die nicht autoritative Vorlage muss fuer jeden Strukturcluster enthalten:

1. Ist-Stand mit fuehrenden Quellen;
2. relevante Handover-Aussagen;
3. bereits abgedeckte Entscheidungen;
4. Konflikte und Doppelungen;
5. zwei bis drei konkrete Zieloptionen bei echten Entscheidungen;
6. Empfehlung mit Begruendung;
7. Auswirkungen auf:
   - Module,
   - Owner,
   - Schnittstellen,
   - Datenvertraege,
   - Workflow,
   - Dokumentrollen,
   - Tests,
   - spaetere Migration;
8. offene Nutzerentscheidungen;
9. Rueckfalloption auf den heutigen kanonischen Stand;
10. vorgeschlagene Anti-Regression-Baseline.

Mindestens zu behandeln sind:

- `SimulationCase` gegen direkte RUN-/VAR-Referenz;
- `ma_sim_external` gegen `ma_export_simulation` und `ma_import_simulation`;
- `ma_analysis` beziehungsweise `ma_analyse_*` gegen `ma_analyse`;
- neue Bewertungsmodule gegen `ma_economy`, `ma_sustainability` und `ma_assessment`;
- `ma_quantity` als eigener Owner oder fachmodulbezogene Mengenermittlung;
- Umfang von `ma_workflow` und `ma_rules`;
- fachliche Workflowquelle und Bedeutung von `Workflow_Gesamtplan`;
- KPI, Feasibility, Pareto und Gewichtung;
- Prozessmessung und Forschungsgrenze;
- PostgreSQL, Repository-Grenze und Zeitreihenspeicherung;
- IFC-, Heizlast-, Zonen- und V1-5Z-Grenzen;
- Parametergruppen und P015;
- Rechte-, Methoden- und Inhaltsgates.

### Slice 8: Gemeinsame Nutzerbesprechung und Baseline-Entscheidung

1. Die Strukturentscheidungsvorlage dem Nutzer vollstaendig, aber kompakt strukturiert vorstellen.
2. Zuerst Ist-Stand und Konflikte zeigen.
3. Danach fuer echte Entscheidungen zwei bis drei Optionen und eine Empfehlung darstellen.
4. Keine strukturelle Option vorwegnehmen.
5. Der Nutzer entscheidet mindestens:
   - welche Gesamtstruktur gelten soll;
   - welche Dokumentrollen fuehrend bleiben;
   - was mit `Workflow_Gesamtplan` gemeint ist;
   - welche Modul- und Ownergrenzen gelten;
   - welche Handover-Vorschlaege historisch oder zurueckgestellt bleiben;
   - welche offenen Fragen nur als Folgeoption fortgefuehrt werden.
6. Den gewuenschten Zielstand als eindeutigen Baseline-Entwurf wiederholen.
7. Die Baseline muss enthalten:
   - Geltungsbereich,
   - fuehrender Gesamtplan,
   - einschlaegige Nutzerentscheidungen,
   - fuehrende Architekturquelle,
   - fuehrende Workflowquelle,
   - bestaetigte Modul- und Ownerliste,
   - bestaetigte Schnittstellengrenzen,
   - explizit ausgeschlossene oder zurueckgestellte Alternativen,
   - offene Folgeentscheidungen,
   - Rueckfallstand.
8. Der Nutzer bestaetigt diesen Baseline-Entwurf ausdruecklich.
9. Vor kanonischen Strukturanderungen ist danach erneut die exakte Formulierung `Freigabe zur Umsetzung` erforderlich.

### Slice 9: Anti-Regression-Gate vor kanonischer Umsetzung

Nach Baseline-Bestaetigung und erneuter Freigabe:

1. Die bestaetigte Baseline gegen P007 und einschlaegige UDs pruefen.
2. Jede geplante strukturelle Aenderung muss auf einen bestaetigten Baseline-Punkt verweisen.
3. Es gilt folgende Prioritaet:
   1. ausdruecklich bestaetigte neue Strukturbaseline,
   2. einschlaegige Nutzerentscheidungen,
   3. fuehrender Gesamtplan,
   4. bestaetigte aktive Teilplaene,
   5. Architektur- und Workflowquellen entsprechend ihrer Rolle,
   6. aktueller Code nur als Ist-Nachweis,
   7. alte Handover ausschliesslich als historische Quelle.
4. Widerspricht ein Handover einer hoeheren Ebene:
   - keine Uebernahme,
   - betroffenen Punkt stoppen,
   - als historisch, zurueckgestellt oder konfliktbehaftet markieren.
5. Keine aeltere Modulbezeichnung, Prozessreihenfolge oder Schnittstellenidee darf unqualifiziert als neuer Zielstand erscheinen.
6. Eine nicht durch die Baseline gedeckte Strukturanderung erfordert eine neue Nutzerentscheidung und neue Freigabe.

### Slice 10: Bestaetigte Baseline kanonisch dokumentieren

1. Die bestaetigte Strukturbaseline als neue Nutzerentscheidung mit Datum, Scope und Quellenbezug in `USER_DECISIONS_MASTERTHESIS_CODE.md` dokumentieren.
2. Echte verbleibende Nutzerentscheidungen ausschliesslich in `USER_DECISIONS_OPEN_POINTS.md` fuehren.
3. Die doppelte OP-Kennung mechanisch bereinigen, sofern dies durch die Baseline bestaetigt ist.
4. `TECHNICAL_DECISIONS.md` nur fuer technische Praezisierungen der bestaetigten Baseline ergaenzen.
5. Bereits bestehende Entscheidungen nicht duplizieren.
6. Historische Alternativen nicht als offene Entscheidung fuehren, wenn sie ausdruecklich zurueckgestellt wurden.

### Slice 11: Plaene und Restarbeit aktualisieren

Nur durch die Baseline bestaetigte Inhalte uebernehmen:

1. P009/P018:
   - neutraler Ergebnisimport,
   - RUN-/VAR-Vertrag,
   - manuelle Simulationsgrenze,
   - bestaetigte Adapter-Folgeoptionen.
2. P019/P020/P021/P029/P036:
   - technische Analyse,
   - Feasibility-Grenze,
   - Kennwert- und Provenienzvertraege,
   - Datenvorbereitung.
3. P022/P023/P024:
   - bestaetigte Economics-, Sustainability- und Assessment-Grenzen.
4. P027:
   - bestaetigte Workflow-/Rules-Verantwortung.
5. P030:
   - Prozessmessung und Vergleichsmethodik.
6. P032:
   - bestaetigte Architekturfolgeoptionen und PostgreSQL-Post-V1-Grenze.
7. P012/P013/P016 und unabhaengiger V1-Plan:
   - IFC-, Heizlast-, Zonen- und V1-5Z-Restarbeit.
8. P015:
   - nur bestaetigte Einordnung des bereits aufgenommenen Referenzplans;
   - UD-125 und S5A/S5B bleiben fuehrend.
9. P007 nur aendern, wenn die bestaetigte Baseline seinen Geltungsbereich ausdruecklich fortschreibt.

### Slice 12: Architektur- und Workflowquellen aktualisieren

1. Erst jetzt die durch die Baseline bestaetigte Architekturquelle aktualisieren.
2. `TARGET_ARCHITECTURE.md` nur fuer bestaetigte technische Zielgrenzen aendern.
3. Die vom Nutzer bestaetigte operative Workflowquelle aktualisieren.
4. Keine Datei namens `Workflow_Gesamtplan` erzeugen, sofern der Nutzer dies nicht ausdruecklich als neue Quelle entschieden und freigegeben hat.
5. P027 und P037 nur entsprechend ihrer bestehenden Rollen aktualisieren.
6. Das Strukturreview bleibt historischer Entscheidungsnachweis und wird nicht zur zweiten Zielarchitektur.
7. Jede geaenderte Strukturquelle verweist auf die neue Baseline-UD.
8. Zurueckgestellte Handover-Alternativen werden sichtbar als nicht geltend markiert.

### Slice 13: Handover-Nachweis und Input-Verarbeitung abschliessen

1. Fuer die drei neuen Handover kompakte versionierte Einordnungssnapshots im bestehenden Handover-Archiv erstellen.
2. Snapshots enthalten:
   - Originalname,
   - SHA-256,
   - Themencluster,
   - Einordnungsstatus,
   - kanonische Ziele,
   - zurueckgestellte Konflikte,
   - keine eigene offene Aufgabenliste.
3. `docs/project/archive/chat_handovers/INDEX.md` ergaenzen.
4. Fuer jeden Handover einen Status ausweisen:
   - vollstaendig eingeordnet,
   - bereits abgedeckt,
   - historisch,
   - zurueckgestellt,
   - konfliktbehaftet,
   - Rechte-/Evidenzgate.
5. Verarbeitete Nicht-Plan-Originale in einen datierten Ordner unter `data/project_inbox/processed/` verschieben.
6. Ein lokales Routing-Manifest mit Originalname, Hash, Zielstatus und kanonischen Verweisen erzeugen.
7. Gesperrte oder unklare Originale nicht verschieben.
8. Keine Datei loeschen.

### Slice 14: Statusquellen und Changelog

1. `PLAN_INDEX.md` nur fuer Status, Abhaengigkeiten und naechsten Schritt aktualisieren.
2. `PLAN_STATUS.md` nur fuer aktive Arbeitslage und Gates aktualisieren.
3. Keine Architekturentscheidung in Statusdateien duplizieren.
4. `CHANGELOG.md` mit einer kompakten Unreleased-Notiz ergaenzen.
5. Keine Versionsaenderung und keinen Releaseeintrag erzeugen.

### Slice 15: Validierung und Abschlussabgleich

1. Alle Dokumentations- und Referenzpruefungen ausfuehren.
2. Die bestaetigte Anti-Regression-Baseline gegen alle geaenderten Strukturquellen pruefen.
3. Den Navigator nach den freigegebenen Dokument- und Pfadaenderungen aktualisieren und mit `--validate-only` validieren.
4. Abschliessend berichten:
   - aufgenommene Plaene,
   - verarbeitete Nicht-Plan-Inputs,
   - vollstaendig eingeordnete Handover,
   - bereits abgedeckte Inhalte,
   - historisch oder zurueckgestellt markierte Vorschlaege,
   - verbleibende offene Entscheidungen,
   - Rechte- und Evidenzgates,
   - bestaetigte Gesamtstruktur.
5. Keine Codeplanung automatisch anschliessen.
6. Fuer spaetere Code- oder Funktionsarbeit einen neuen, getrennten Prompt-Intake beginnen.

## Pruefungen

### Input- und Planaufnahme

- Jeder neue Input besitzt Kategorie, Hash, Rechte-/Schutzstatus und Zielstatus.
- Jeder eindeutig erkannte Plan wurde nach `PROJECT_INPUT_WORKFLOW.md` behandelt.
- Kein bestehender Plan wurde durch einen Referenz- oder Duplikatplan stillschweigend ersetzt.
- P015, UD-125 und P015-S5A/S5B bleiben gegenueber dem Parametergruppen-Referenzplan fuehrend.
- Verarbeitete Nicht-Plan-Originale liegen nach Abschluss unter `processed`.
- Unklare oder gesperrte Dateien bleiben unter `new`.
- Kein Original wurde geloescht.

### Strukturentscheidung und Baseline

- Vor strukturellen Aenderungen existiert eine vollstaendige, nicht autoritative Strukturentscheidungsvorlage.
- Die Vorlage enthaelt fuer jeden echten Entscheidungspunkt Ist-Stand, Optionen, Empfehlung, Auswirkungen und offene Fragen.
- Die Nutzerbesprechung fand vor jeder kanonischen Strukturfestschreibung statt.
- Der bestaetigte Baselinestand ist eindeutig und besitzt einen bezeichneten Geltungsbereich.
- Eine neue Baseline-UD verweist nachvollziehbar auf die Nutzerbestaetigung.
- Alle kanonischen Strukturanderungen sind durch die Baseline gedeckt.
- Nicht gedeckte Aenderungen wurden gestoppt.

### Workflow-Gesamtplan-Rolle

- Es wurde keine bestehende Datei mit dem exakten Namen `Workflow_Gesamtplan` vorausgesetzt.
- Es wurde keine solche Datei ohne Nutzerentscheidung erzeugt.
- P007, operative Workflowquelle, P027, P037 und `TARGET_ARCHITECTURE.md` sind nach ihrer bestaetigten Rolle getrennt.
- Die vom Nutzer gemeinte Workflow-Gesamtquelle ist eindeutig dokumentiert.
- Es existiert keine parallele, widersprechende Workflowwahrheit.

### Entscheidungs- und Referenzintegritaet

- Jede `UD-*`-Kennung kommt genau einmal als Entscheidungsueberschrift vor.
- Jede `OP-*`-Kennung kommt genau einmal als offene Entscheidungsueberschrift vor.
- Jeder Planverweis auf `UD-*` und `OP-*` ist eindeutig aufloesbar.
- Die doppelte OP-017-Kennung ist beseitigt, ohne den neutralen Ergebnisvertrag umzudeuten.
- Erledigte Entscheidungen stehen nicht zugleich als offen.
- Echte offene Nutzerentscheidungen stehen nicht ausschliesslich in Plaenen oder Handovern.

### Anti-Regression-Pruefung

- Fuehrender Gesamtplan und einschlaegige Nutzerentscheidungen wurden vor jedem Handover herangezogen.
- Alte Handover erscheinen nicht unqualifiziert als aktuelle Zielquelle.
- Widersprechende Vorschlaege sind sichtbar als historisch, zurueckgestellt oder konfliktbehaftet markiert.
- `SimulationCase` und `CASE-ID` werden nur dann als Ziel verwendet, wenn die neue Baseline die bisherige Gegenentscheidung ausdruecklich revidiert; andernfalls bleiben sie ausgeschlossen.
- Die direkte P018-Zuordnung `RUN-ID + VAR-ID` bleibt ohne ausdrueckliche Revision bestehen.
- Bestehende Owner und Modulnamen werden nicht stillschweigend umbenannt.
- UD-129 bleibt ohne ausdrueckliche Revision die PostgreSQL-Grenze.
- P007, P027, P037, Architektur- und Workflowquellen widersprechen der bestaetigten Baseline nicht.

### Rechte- und Scopepruefung

- Keine geschuetzten ZIP-, PDF-, Norm-, Literatur-, IDM- oder IDA-/EQUA-Inhalte wurden ohne objektbezogene Freigabe geoeffnet.
- Keine externe API, Cloud-Verarbeitung oder automatische Simulation wurde verwendet.
- Keine Datei unter `src/`, `tests/`, `config/` oder `Skripte/` wurde veraendert.
- Keine produktiven Fach- oder Ergebnisdaten wurden veraendert.
- Kein Commit, Push, Tag oder Release wurde erzeugt.

### Technische Dokumentationspruefungen

- `git diff --check`
- gezielte Markdown-Pfad- und Referenzpruefung
- eindeutige UD-/OP-ID-Pruefung
- Handover-Index gegen tatsaechliche Archivdateien
- Planindex gegen tatsaechliche Planpfade
- `pytest -q tests/test_architecture_guardrails.py tests/test_p037_workflow_information.py`
- Navigator-Aktualisierung nach freigegebenen Dokument- und Pfadaenderungen
- Navigator-Validierung mit `--validate-only`
- abschliessendes `git status --short --untracked-files=all`
- abschliessender Abgleich der Aenderungsdateien gegen die jeweilige Stufen-Allowlist
- gezielte Suche nach alten oder widersprechenden Strukturbezeichnungen in geaenderten kanonischen Quellen

Eine vollstaendige Produkt-Testsuite ist fuer diesen Dokumentationsscope nicht erforderlich. Schlagen die gezielten Guardrail-Tests aufgrund der Dokumentationsaenderungen fehl, ist der Abschluss blockiert.

## Risiken und offene Entscheidungen

### Blocker

1. **Strukturelle Festschreibung ohne bestaetigte Baseline**

   Fuer Architektur, Workflow-Gesamtquelle und alle sonstigen strukturellen Punkte fehlt vor der Nutzerbesprechung ein eindeutig bestaetigter Zielstand. Jede kanonische Strukturanderung vor dieser Bestaetigung waere eine unautorisierte Architekturentscheidung.

2. **Mehrdeutige Rolle von `Workflow_Gesamtplan`**

   Im Repository existiert keine Datei mit diesem exakten Namen. P007, `docs/project/workflow/README.md`, P027, P037 und `TARGET_ARCHITECTURE.md` besitzen unterschiedliche kanonische Rollen. Eine Datei oder Rolle darf nicht geraten werden. Die Mehrdeutigkeit muss in der Strukturbesprechung entschieden werden.

3. **Doppelte offene Entscheidungs-ID**

   `USER_DECISIONS_OPEN_POINTS.md` verwendet `OP-017` sowohl fuer den neutralen Ergebnisvertrag als auch fuer den Council-Spezialistenpool. Verweise sind dadurch mehrdeutig. Die mechanische Korrektur muss durch die bestaetigte Strukturpflege gedeckt sein.

4. **Direkter Konflikt um `SimulationCase`**

   Der neue Simulationsarchitektur-Handover fordert `SimulationCase`. UD-112, P018, die bestehende Zielarchitektur und der unabhaengige V1-Plan schliessen diese Ebene ausdruecklich aus. Ohne bewusste Revision durch den Nutzer bleibt der Vorschlag historisch oder zurueckgestellt.

5. **Automatisierungs- und Rechtegate**

   Direkte API-, Connector- und Simulationsstart-Vorschlaege kollidieren mit der manuellen V1-Grenze und dem EQUA-Rechtegate. Sie duerfen nicht als Zielarchitektur uebernommen oder technisch aktiviert werden.

6. **Zweites Freigabe-Gate**

   Eine erste `Freigabe zur Umsetzung` erlaubt sichere Inputaufnahme, Klassifikation und Erstellung der Strukturentscheidungsvorlage. Kanonische strukturelle Aenderungen beginnen erst nach Nutzerbestaetigung der Baseline und erneuter exakter `Freigabe zur Umsetzung`.

### Wichtig

1. **Modul- und Ownerkonflikte**

   Die neuen Handover verwenden unter anderem `ma_zone`, `ma_technology`, `ma_analysis`, `ma_analyse_energy`, `ma_analyse_economics`, `ma_analyse_sustainability`, `ma_sim_external` und `ma_quantity`. Die bestehenden kanonischen Owner und Namen weichen davon ab. Ohne Baseline-Entscheidung drohen Parallelmodule und doppelte Verantwortlichkeiten.

2. **KPI-Handover teilweise bereits eingeordnet**

   P019, P020, P021, P024 und P029 enthalten bereits Teile des KPI-Diskussionsprozesses als nicht-kanonischen Hintergrund. Neue Entscheidungen muessen von bereits abgedeckten Aussagen getrennt werden.

3. **PostgreSQL-Handover weitgehend durch UD-129 und P032 abgedeckt**

   Das Handover darf keine zweite Datenbankentscheidung, keine neue CASE-Ebene und keine vorgezogene Repository-Architektur erzeugen.

4. **Dirty-Worktree-Überlappung**

   Zentrale Plan-, Status-, Entscheidungs- und Handover-Dateien besitzen bereits Aenderungen. Diese sind vor jedem Slice zu sichern und duerfen nicht ueberschrieben werden.

5. **Input-Verschiebung und Nachvollziehbarkeit**

   Nicht-Plan-Originale duerfen erst nach abgeschlossener Verarbeitung nach `processed` verschoben werden. Hash und Routing-Manifest muessen die Herkunft erhalten. Gesperrte Inhalte bleiben unter `new`.

6. **Navigatorzugriff**

   Der semantische Navigator war waehrend der read-only Planung nicht lesbar. Aktualisierung und Validierung muessen nach Freigabe erneut versucht werden. Es darf kein alternativer paralleler Index erfunden werden.

7. **Methodische Entscheidungsgrenzen**

   Referenzzone, Unmet Hours, Energieebenen, Feasibility-Schwellen, Mengengrenzen, Kostenumfang, Umweltindikatoren, Unsicherheitsmodell, Pareto und Gewichtung bleiben fachlich offen, sofern der Nutzer sie nicht in der Strukturbesprechung ausdruecklich einordnet.

### Optional

1. Ein spaeterer Dokumentationstest kann doppelte UD-/OP-IDs und ungueltige Planverweise automatisiert erkennen. Dies ist nicht Bestandteil dieses Scopes.

2. Eine spaetere Archivbereinigung kann historische Vollhandover, kompakte Einordnungssnapshots und lokale Inputoriginale klarer trennen. Dafuer ist eine eigene Freigabe erforderlich.

3. Eine neue Datei mit der Rolle eines Workflow-Gesamtplans kann spaeter separat geplant werden, falls die bestehende Rollentrennung nach der Nutzerbesprechung nachweislich nicht ausreicht.

## Tera-Uebergabe

Vorgesehener Planpfad:

`docs/project/plans/independent/260815_Handover_Input_Strukturbaseline_Integration.md`

### Erste Freigabestufe

Die Ausfuehrung von Inputaufnahme, Planaufnahme, Klassifikation und Strukturentscheidungsvorlage beginnt erst nach:

`Freigabe zur Umsetzung`

Uebergabeprompt:

```text
Setze Stufe A des freigegebenen unabhaengigen Umsetzungsplans
`docs/project/plans/independent/260815_Handover_Input_Strukturbaseline_Integration.md`
um.

Lies den Plan vollstaendig. Sichere zuerst den Dirty-Worktree. Nimm eindeutig
erkannte Plaene gemaess PROJECT_INPUT_WORKFLOW auf, klassifiziere alle
archivierten und neuen Handover und erstelle die vollstaendige, nicht
autoritative Strukturentscheidungsvorlage.

Veraendere noch keine kanonische Architektur-, Workflow-Gesamtplan- oder
sonstige Strukturquelle. Erfinde keine Datei namens Workflow_Gesamtplan.
Verarbeite keine geschuetzten Inhalte. Stoppe bei Rechte-, Inhalts-,
Scope- oder Regressionskonflikten.

Besprich anschliessend mit dem Nutzer Ist-Stand, Zieloptionen, Konflikte,
Empfehlung, Auswirkungen und offene Entscheidungen. Formuliere daraus einen
eindeutigen Anti-Regression-Baseline-Entwurf und warte auf seine
ausdrueckliche Bestaetigung.
```

### Zweite Freigabestufe

Nach ausdruecklicher Nutzerbestaetigung der Strukturbaseline wartet Tera erneut auf:

`Freigabe zur Umsetzung`

Erst dann gilt:

```text
Setze Stufe B des freigegebenen unabhaengigen Umsetzungsplans
`docs/project/plans/independent/260815_Handover_Input_Strukturbaseline_Integration.md`
auf Basis der vom Nutzer bestaetigten Strukturbaseline um.

Dokumentiere die Baseline als Nutzerentscheidung. Aktualisiere ausschliesslich
die dadurch gedeckten Plaene, Architektur-, Workflow-, Entscheidungs-,
Status- und Handover-Dokumente. Fuehrender Gesamtplan, einschlaegige
Nutzerentscheidungen und die neue Baseline schlagen alte Handover.

Markiere widersprechende oder aeltere Vorschlaege sichtbar als historisch,
zurueckgestellt oder konfliktbehaftet. Lasse keine alte Struktur
stillschweigend zurueckkehren. Schliesse die regelkonforme Verarbeitung der
Nicht-Plan-Inputs ab, verschiebe zulaessige Originale nach processed und
fuehre alle vorgesehenen Pruefungen sowie die Navigatorvalidierung aus.

Aendere keinen Code, keine API, keine Produktfunktion und keine produktiven
Fachdaten. Plane Code und Funktionen erst in einem spaeteren, getrennten
Thema.
```
