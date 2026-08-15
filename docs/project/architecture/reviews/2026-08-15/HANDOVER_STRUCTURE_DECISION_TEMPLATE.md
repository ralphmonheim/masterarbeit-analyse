# Handover-Strukturentscheidungsvorlage

Stand: 2026-08-15  
Status: nicht autoritative Entscheidungs- und Gespraechsgrundlage; Stufe A  
Freigabe: keine kanonische Strukturfestlegung; keine Code- oder Produktarbeit

## Zweck und Schutzregel

Diese Vorlage klassifiziert die vorhandenen Chat-Handover und die neuen
Projektinputs gegen die aktuell fuehrenden Projektquellen. Sie bereitet die
gemeinsame Strukturentscheidung vor, ersetzt aber weder P007 noch eine
Nutzerentscheidung, Zielarchitektur, aktive Plaene oder den Planstatus.

Vor jeder spaeteren strukturellen Dokumentaenderung gelten zwei Gates:

1. Der Nutzer bestaetigt nach der gemeinsamen Besprechung einen eindeutigen
   Baselinestand mit Geltungsbereich.
2. Danach erteilt der Nutzer fuer Stufe B erneut exakt
   `Freigabe zur Umsetzung`.

Bis dahin bleiben P007, die einschlaegigen Nutzerentscheidungen und die
heutigen Dokumentrollen fuehrend. Ein Handover darf keinen aelteren oder
widersprechenden Stand stillschweigend reaktivieren.

## Pruefbasis und Arbeitsbaumgrenze

Geprueft wurden:

- 32 Markdown-Handover unter `docs/project/archive/chat_handovers/`;
- der Handover-Index;
- drei neue Markdown-Handover und zwei ZIP-Eingaenge unter
  `data/project_inbox/new/`;
- P007 bis P037 in den fuer die Themen relevanten Bereichen;
- der unabhaengige V1-5Z-Plan;
- Nutzerentscheidungen UD-112 bis UD-129 und die offenen Punkte;
- `TARGET_ARCHITECTURE.md`, P027, P037 und
  `docs/project/workflow/README.md`;
- der Navigator als nicht kanonischer Einstieg und danach die jeweils
  genannten kanonischen Quellen.

Der Arbeitsbaum enthielt vor Stufe A bereits Aenderungen an Changelog,
Handover-Index, Nutzerentscheidungen, Planindex, Planstatus, P015 und P032
sowie unversionierte Handover. Diese vorhandenen Aenderungen werden nicht
ueberschrieben oder fremden Slices zugerechnet.

## Klassifikationsschluessel

| Klasse | Bedeutung |
| --- | --- |
| `BESTAETIGTE_ENTSCHEIDUNG` | explizite, kanonisch nachweisbare Nutzerentscheidung |
| `BEREITS_ABGEDECKT` | Inhalt steht bereits in einer fuehrenden Quelle |
| `OFFENE_NUTZERENTSCHEIDUNG` | echte, noch zu treffende Nutzerwahl |
| `RESTARBEIT_AKTIVER_PLAN` | konkrete Folgearbeit wird in einem aktiven Plan gefuehrt |
| `NICHT_FREIGEGEBENE_FOLGEOPTION` | moegliche spaetere Erweiterung ohne aktuellen Scope |
| `METHODISCHER_HINTERGRUND` | Diskussions- oder Forschungsgrundlage, keine Entscheidung |
| `HISTORISCHE_ALTERNATIVE` | frueherer oder abgeloester Zielvorschlag |
| `ARCHITEKTURKONFLIKT` | Widerspruch zu einer hoeheren Projektwahrheit |
| `RECHTE_ODER_EVIDENZGATE` | Verarbeitung oder Aussage ist bis zu einem Nachweis gesperrt |
| `VERWORFEN` | im Handover selbst oder durch spaetere Entscheidung abgelehnt |

## Input-Inventar und Routing

| Eingang | Typ / Groesse | SHA-256 | Klassifikation | Stufe-A-Umgang |
| --- | ---: | --- | --- | --- |
| `Chat_Handover_KPI_Variantenbewertung_2026-08-15.md` | Markdown / 39.253 B | `EAA1016F273704A7EAA80030FF01619905F47551C49EDB3B0ECE7998AEF17310` | Nicht-Plan; Methodik, offene Entscheidungen und Strukturvorschlaege | gelesen und klassifiziert; Original bleibt bis Stufe B unter `new/` |
| `Chat_Handover_Simulationsarchitektur_Assessment_Workflow_2026-08-15.md` | Markdown / 30.012 B | `D5EB42A6CA19E33D41ECFDD56DBC38EB7598C2B5E128358026ECB5250E7DBBAE` | Nicht-Plan; Architekturvorschlaege mit Teilkonflikten | gelesen und klassifiziert; Original bleibt bis Stufe B unter `new/` |
| `Chat-Handover – Vollständiger Arbeitsprozess zur Datenbanktransformation und PostgreSQL.md` | Markdown / 37.299 B | `F82A4170D311F6859D55DA8D095B1DE2619C7777BF098E0A8E7322C3BB961582` | bytegleiches Duplikat des bereits am 14.08. verarbeiteten Originals | keine zweite fachliche Aufnahme; Original bleibt kollisionsfrei unter `new/` bis zur Stufe-B-Entscheidung |
| `IDA_ICE_Annotations_Handover.zip` | ZIP / 0 B | `E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855` | leerer, nicht verarbeitbarer Container | nicht geoeffnet; Rueckfrage beziehungsweise spaetere Bereinigung erforderlich |
| `IDA_ICE_Annotations_Handover(1).zip` | ZIP / 21.680 B | `52C85DA71BC3141EFD75777779DD642A7DEF9E65A0C406BD1636226B47E9702A` | moeglicher IDA-/EQUA-Inhalt | `RECHTE_ODER_EVIDENZGATE`; nicht geoeffnet und nicht verschoben |
| `260815_Plan_Parametergruppen_Neustrukturierung.md` | Plan / 48.113 B | unveraendert aus Eingang uebernommen | Referenzplan zu P015 | bereits regelkonform aufgenommen; UD-125 und P015-S5A/S5B bleiben fuehrend |

Der neue PostgreSQL-Eingang ist bytegleich mit
`data/project_inbox/processed/2026-08-14_project_inputs/Chat-Handover – Vollständiger Arbeitsprozess zur Datenbanktransformation und PostgreSQL.md`.
Er erzeugt daher keine zweite Entscheidung und keinen neuen Plan.

## Vollstaendige Klassifikation der 32 archivierten Handover

| Handover | Gesamtklassifikation | Fuehrende Ziele / Befund |
| --- | --- | --- |
| `260722_chat-handover_archivierung-einrichtung.md` | `BEREITS_ABGEDECKT` | P031, UD-100 und Update-Routinen fuehren; abgeschlossen |
| `260728_chat-handover_preprocess-v1-projektworkspace.md` | `RESTARBEIT_AKTIVER_PLAN` | P008, P011-P018, P027, P034 und P035 fuehren den fortgeschriebenen Stand |
| `260729_chat-handover_pseudonymisierung-und-katalogregister.md` | `BEREITS_ABGEDECKT`, `RESTARBEIT_AKTIVER_PLAN` | P012, P013, P034, P035 und UD-106 bis UD-108 fuehren |
| `260729_chat-handover_catalog-v1.md` | `BEREITS_ABGEDECKT` | P012, P034 und UD-109 fuehren |
| `260729_chat-handover_prozessmessung-kostenvergleich.md` | `RESTARBEIT_AKTIVER_PLAN`, `OFFENE_NUTZERENTSCHEIDUNG` | P030 und OP-009 fuehren Vergleichsmethodik und offene Messgrenzen |
| `260729_chat-handover_studydirection-preprocess.md` | `METHODISCHER_HINTERGRUND`, `BEREITS_ABGEDECKT` | P015-P018 sowie spaetere UD-112/P017-Vertraege ersetzen den fruehen Orientierungsstand |
| `260729_chat-handover_codex-navigation-und-chatabschluss.md` | `BEREITS_ABGEDECKT` | P031, Update-Routinen und spaeter UD-124 fuehren |
| `260729_chat-handover_postprocess-ideen-und-gespraech.md` | `METHODISCHER_HINTERGRUND`, `HISTORISCHE_ALTERNATIVE` | P009, P019-P027 und spaeter UD-122 fuehren; offene Methoden nicht als Entscheidung uebernehmen |
| `260729_chat-handover_ui-ansichten-wetter-korrekturen.md` | `RESTARBEIT_AKTIVER_PLAN`, `BEREITS_ABGEDECKT` | P008, P027, P035 und spaetere UI-Entscheidungen fuehren |
| `260731_chat-handover_konsolidierter-mvp-gesamtprozess.md` | `BESTAETIGTE_ENTSCHEIDUNG`, `BEREITS_ABGEDECKT` | UD-112 und P007 sind die kanonische Uebernahme; Restarbeit steht in P009/P016-P018/P027/P029/P030 |
| `260803_chat-handover_mvp-v1-migration.md` | `RESTARBEIT_AKTIVER_PLAN`, `BEREITS_ABGEDECKT` | P016-P018 und Planstatus fuehren die fortgeschriebene Migration |
| `260803_chat-handover_mvp-v1-migration-v2.md` | `RESTARBEIT_AKTIVER_PLAN`, `BEREITS_ABGEDECKT` | P016-P018, UD-117 und Planstatus fuehren |
| `260811_chat-handover_preprocess-output-snapshots.md` | `RESTARBEIT_AKTIVER_PLAN` | P017, P018, P035 und UD-119 fuehren; lokale Snapshots sind keine neue Struktur |
| `260811_chat-handover_smalloffice-ifc-heizlast.md` | `RESTARBEIT_AKTIVER_PLAN`, `RECHTE_ODER_EVIDENZGATE` | P012, P016, OP-012 und OP-016 fuehren; Diagnosewerte vor Nutzung reproduzieren |
| `260811_chat-handover_postprocess-analyseebene.md` | `BESTAETIGTE_ENTSCHEIDUNG`, `RESTARBEIT_AKTIVER_PLAN` | UD-122 fuehrt die gemeinsame Analyseebene; P009, P019 und P029 fuehren Folgearbeit |
| `260811_chat-handover_smalloffice-kapazitaetsstrategie.md` | `BESTAETIGTE_ENTSCHEIDUNG`, `BEREITS_ABGEDECKT` | UD-118 und P015/P017/P018 fuehren; produktiver Durchlauf bleibt Restarbeit |
| `260811_chat-handover_postprocess-tabellenvertrag-stage3-readiness.md` | `BEREITS_ABGEDECKT`, `RESTARBEIT_AKTIVER_PLAN` | P019, P020, P029 und UD-121 fuehren; spaeter final validiert |
| `260812_chat-handover_postprocess-s12-finalvalidierung.md` | `BEREITS_ABGEDECKT`, `RECHTE_ODER_EVIDENZGATE` | P019/P020/P029 und UD-121 fuehren; produktive Normnachweise bleiben gesperrt |
| `260812_chat-handover_parameter-variations-table.md` | `BEREITS_ABGEDECKT` | P015 und der Variationsspezifikationsvertrag fuehren |
| `260812_chat-handover_project-inbox-semantic-navigation.md` | `BESTAETIGTE_ENTSCHEIDUNG`, `BEREITS_ABGEDECKT` | UD-120, UD-124, P031 und Update-Routinen fuehren |
| `260812_chat-handover_p015-s5a-parameterdefinitionskern.md` | `BESTAETIGTE_ENTSCHEIDUNG`, `RESTARBEIT_AKTIVER_PLAN` | UD-125/P015-S5A fuehren; S5B bleibt getrennt freizugeben |
| `260813_chat-handover_quellenregister-und-inhaltssuche.md` | `BESTAETIGTE_ENTSCHEIDUNG`, `RECHTE_ODER_EVIDENZGATE` | UD-127 und P031 fuehren; Inhaltsanalyse bleibt objektbezogen freizugeben |
| `260813_chat-handover_normenbestand-und-ki-verarbeitungsgrenze.md` | `RECHTE_ODER_EVIDENZGATE`, `BEREITS_ABGEDECKT` | P020, OP-016 und UD-121 fuehren; keine Norminhaltsverarbeitung |
| `260813_chat-handover_p030-prozessmessung-arbeitsmappe.md` | `RESTARBEIT_AKTIVER_PLAN`, `OFFENE_NUTZERENTSCHEIDUNG` | P030 und OP-009 fuehren; Vergleichbarkeit noch nicht gegeben |
| `260813_chat-handover_eingangszuordnung-und-routinenkorrektur.md` | `BEREITS_ABGEDECKT`, `RECHTE_ODER_EVIDENZGATE` | P007/P009/P019/P020/P031 und UD-127 fuehren; Literaturcontainer blieb gesperrt |
| `260813_chat-handover_eingangszuordnung-und-routinenkorrektur-v2.md` | `BESTAETIGTE_ENTSCHEIDUNG`, `BEREITS_ABGEDECKT` | Update-Routinen und Projektinput-Workflow fuehren die direkte Planaufnahme |
| `260813_chat-handover_dokumentationshierarchie-workflow-ui.md` | `BESTAETIGTE_ENTSCHEIDUNG`, `BEREITS_ABGEDECKT` | UD-128 und P037 fuehren; UD-114/P027 bleiben Prozess- und UI-Grenze |
| `260814_chat-handover_p037-release-und-navigatorstatus.md` | `BEREITS_ABGEDECKT` | P037/UD-128 abgeschlossen; Navigatorfolgepunkt liegt in P031 |
| `260814_chat-handover_sol-planung-und-tera-uebergabe.md` | `BEREITS_ABGEDECKT` | Update-Routinen und Prompt-Intake fuehren |
| `260814_chat-handover_v1-5z-ausfuehrungsplan-und-b2-freigabe.md` | `BEREITS_ABGEDECKT`, `RESTARBEIT_AKTIVER_PLAN` | unabhaengiger V1-Plan fuehrt den Ausfuehrungsscope; keine neue Gesamtarchitektur |
| `260814_chat-handover_projektinput-literatur-kpi-und-datenhaltung.md` | `BEREITS_ABGEDECKT`, `METHODISCHER_HINTERGRUND` | UD-127/UD-129 und P019-P021/P024/P029/P032 fuehren |
| `260814_chat-handover_v1-5z-umsetzung-zwischenstand.md` | `RESTARBEIT_AKTIVER_PLAN`, `OFFENE_NUTZERENTSCHEIDUNG` | unabhaengiger V1-Plan sowie OP-009/017/018 fuehren |

Ergebnis: Keines der 32 archivierten Handover muss selbst zur aktiven
Projektwahrheit erhoben oder inhaltlich umgeschrieben werden. Offene Arbeit
und Entscheidungen besitzen bereits kanonische Zielorte. Zu pruefen bleibt,
ob einzelne neue Aussagen vom 15.08. nach der Baseline-Entscheidung diese
Ziele ergaenzen.

## Detailklassifikation der neuen Markdown-Handover

### KPI, Variantenbewertung und Bewertungsarchitektur

| Handover-Aussage | Einordnung | Heutige fuehrende Quellen | Baseline-Frage |
| --- | --- | --- | --- |
| Leistung, Energie, Temperatur, Komfort und Unmet Hours als Kennwertgruppen | `METHODISCHER_HINTERGRUND`, teilweise `BEREITS_ABGEDECKT` | P019, P029, UD-121, OP-008/017/018 | Welche Kennwerte und Einheiten werden spaeter fachlich verbindlich? |
| Zielgroessen von Feasibility-Constraints trennen | kompatibler Zielvorschlag, noch keine vollstaendige Methode | UD-112, UD-121, P019/P020, OP-018 | Soll diese Trennung als verbindliche Bewertungsregel gelten? |
| nur fachlich zulaessige Varianten bewerten | kompatibler Vorschlag, Schwellen offen | P020, P024, OP-018 | Wer erzeugt den Zulaessigkeitsstatus und nach welchen Regeln? |
| drei Fachbereiche Energie, Nachhaltigkeit, Wirtschaftlichkeit | konzeptionell `BEREITS_ABGEDECKT`, Namen teils konfliktbehaftet | UD-036, P019, P022-P024 | Bestehende Owner behalten oder neue Analyse-Unterteilung schaffen? |
| gemeinsame Mengenermittlung / `ma_quantity` | `NICHT_FREIGEGEBENE_FOLGEOPTION`, moeglicher `ARCHITEKTURKONFLIKT` | P012/P014/P022/P023/P024 | Eigener Owner, gemeinsamer Service oder Fachmodulverantwortung? |
| Pareto vor Gewichtung | `METHODISCHER_HINTERGRUND`, `OFFENE_NUTZERENTSCHEIDUNG` | P024, OP-018 | Option, Standardmethode oder nicht Teil von V1? |
| feste Gewichte nicht hardcoden | kompatible Schutzregel | P024, OP-018 | Spaetere Szenariogewichte nur explizit und versioniert? |
| Stage-Historie je Variante | teilweise kompatibel, Datenvertrag offen | P017-P021, P024, P032 | Wo liegt die Historie und welche Identitaeten werden verwendet? |
| externe Programme liefern Daten, eigene Software bewertet | kompatibel | P009, P019/P024, UD-112 | Keine neue Programmbewertungsarchitektur erforderlich |

### Simulation, Assessment und Workflow

| Handover-Aussage | Einordnung | Heutige fuehrende Quellen | Baseline-Frage |
| --- | --- | --- | --- |
| projektroot-relative Pfade und zentrale Pfadauflösung | `BEREITS_ABGEDECKT` | P035, P007, TARGET_ARCHITECTURE | keine neue Struktur erforderlich |
| manueller Simulationsschritt ist regulaerer Modus | `BEREITS_ABGEDECKT` | UD-112, P009, P018 | V1 bleibt manuell |
| `ma_sim_external` als neue Integrationsschicht | `ARCHITEKTURKONFLIKT` / Post-V1-Option | P009, P018, `ma_export_simulation`, `ma_import_simulation` | bestehende Owner behalten oder spaeteren Umbau separat planen? |
| neutrales `SimulationCase` | `ARCHITEKTURKONFLIKT` | UD-112, UD-117, P007, P018, TARGET_ARCHITECTURE | bestehende direkte `RUN-ID + VAR-ID`-Zuordnung bewusst revidieren oder erhalten? |
| Mapper und Connector trennen; Capability-Modell | `NICHT_FREIGEGEBENE_FOLGEOPTION`, Rechtegate | P009, P032, OP-016 | nur Post-V1 und erst nach API-/EQUA-Rechten |
| `ma_rules` fuehrt Entscheidungsregeln | weitgehend `BEREITS_ABGEDECKT` | P027, UD-112 | fachliche Regelownership je Modul weiterhin abgrenzen |
| `ma_workflow/orchestrator` fuehrt Entscheidungen technisch aus | kompatible Praezisierung, Ausbau offen | P027, P007, UD-114 | Umfang des Orchestrators ohne zweite Fachlogik festlegen |
| vier neue Stage-Top-Level-Module | `ARCHITEKTURKONFLIKT` / historische Alternative | P016, P019-P021, UD-112/122/126 | bestehende Owner und Migrationsgrenzen behalten? |
| `ma_reporting` als eigenes Modul | `BEREITS_ABGEDECKT` | P025, P007 | keine neue Struktur erforderlich |

### Datenbanktransformation und PostgreSQL

Der Eingang ist bytegleich mit dem bereits verarbeiteten Dokument. Seine
strukturellen Kernaussagen sind durch UD-129 und P032 eingeordnet:

| Aussage | Einordnung | Baseline-Folge |
| --- | --- | --- |
| nicht Dateien direkt durch PostgreSQL ersetzen | `BESTAETIGTE_ENTSCHEIDUNG`, `BEREITS_ABGEDECKT` | dateibasierte V1-Persistenz bleibt |
| zuerst Domainmodell, dann Repository-Grenzen und Schema | Post-V1-Planungsprinzip | in P032 als Folgeplanung, keine V1-Implementierung |
| grosse Zeitreihen relational, dateibasiert oder hybrid speichern | `OFFENE_NUTZERENTSCHEIDUNG` fuer Post-V1 | erst nach realem Dateninventar entscheiden |
| PostgreSQL lokal/Server, Version, Migrationstool | `NICHT_FREIGEGEBENE_FOLGEOPTION` | keine Technologieentscheidung in diesem Scope |
| Provenienz, Einheiten, IDs und Portabilitaet erhalten | kompatible Querschnittsanforderung | spaeteren Domain-/Repositoryvertrag daran pruefen |

## Derzeitige Dokumentrollen

| Informationsart | Heute fuehrende Quelle | Befund |
| --- | --- | --- |
| Gesamt- und Architekturrahmen | P007 | Navigator und UD-038 bestaetigen P007 als fuehrenden Gesamtplan |
| technische Zielstruktur | `docs/project/architecture/TARGET_ARCHITECTURE.md` | technische Architektur, nicht Arbeitsstatus oder Fachablauf |
| fachlicher Gesamtworkflow | `docs/project/workflow/README.md` und Modulsteckbriefe | nach P037/UD-128 operative fachliche Hauptquelle |
| technischer Workflow-Querschnitt | P027 | Orchestrierung, UI, Validation und Feedback |
| Dokumenthierarchie und UI-Informationsrollen | P037 und UD-128 | trennt Workflowwissen, technische Info, Status und Entscheidungen |
| verbindliche Entscheidungen | `docs/project/decisions/` | fuehrt das Warum und die Gueltigkeit |
| aktive Umsetzung | jeweiliger aktiver Plan | fuehrt das Wie und die Restarbeit |
| aktueller Stand | `PLAN_STATUS.md` | keine Architektur- oder Entscheidungsquelle |
| historischer Nachweis | Handover-Archiv und Reviews | keine aktive Projektwahrheit |

Eine Datei mit dem exakten Namen `Workflow_Gesamtplan` existiert nicht. Die
vom Nutzer gemeinte Rolle muss vor Stufe B eindeutig einer bestehenden Quelle
zugeordnet oder als eigener spaeterer Planungsbedarf entschieden werden.

## Strukturentscheidungen fuer die gemeinsame Besprechung

### S-01 Dokumentrollen und `Workflow_Gesamtplan`

**Ist-Stand:** P007 fuehrt den Gesamt- und Architekturrahmen;
`docs/project/workflow/README.md` fuehrt den fachlichen Ablauf; P027 fuehrt den
technischen Workflow-Querschnitt; P037/UD-128 fuehren die Rollentrennung;
`TARGET_ARCHITECTURE.md` fuehrt die technische Zielstruktur.

- **Option A – bestehende Rollentrennung erhalten:** Der Begriff
  `Workflow_Gesamtplan` bezeichnet im Gespraech die Kombination aus P007 und
  der operativen Workflowquelle, ohne neue Datei.
- **Option B – vorhandenen Workfloweinstieg staerken:**
  `docs/project/workflow/README.md` wird nach Bestaetigung ausdruecklich als
  Workflow-Gesamteinstieg bezeichnet, waehrend P007 und Architektur getrennt
  bleiben.
- **Option C – neuen Gesamtplan spaeter planen:** nur wenn die vorhandene
  Trennung nachweislich nicht ausreicht; neue kanonische Quelle und
  Migrationsregeln waeren separat freizugeben.

**Empfehlung:** Option A. Sie entspricht UD-128/P037 und verhindert eine
weitere Dokumentationswahrheit.  
**Rueckfall:** heutige Rollentrennung unveraendert.  
**Nutzerentscheidung:** offen.

### S-02 Run-, Varianten- und Simulationsfallmodell

**Ist-Stand:** Ein wissenschaftlicher RUN enthaelt ein gemeinsames Setup und
mehrere Varianten; der manuelle Ausfuehrungs-/Ergebnisfall ist
`RUN-ID + VAR-ID`. `SimulationCase` und separate `CASE-ID` sind durch UD-112,
UD-117, P007, P018 und TARGET_ARCHITECTURE ausgeschlossen.

- **Option A – direkte RUN-/VAR-Zuordnung erhalten.**
- **Option B – `SimulationCase` nur als Post-V1-Forschungsoption notieren,**
  ohne V1-Vertrag oder Modulstruktur zu aendern.
- **Option C – bestehende Entscheidung bewusst revidieren** und eine neue
  Ebene planen; dies waere eine eigene Architektur- und Migrationsentscheidung.

**Empfehlung:** Option A fuer V1; Option B lediglich als zurueckgestellte
Post-V1-Alternative.  
**Auswirkung:** Option C wuerde P017/P018, IDs, Persistenz, Import und UI
breit betreffen.  
**Rueckfall:** direkter P018-Vertrag.  
**Nutzerentscheidung:** offen.

### S-03 Externe Simulation und Adapter

**Ist-Stand:** `ma_export_simulation` und `ma_import_simulation` sind neutrale
Owner; IDA ICE bleibt Adapter. V1 nutzt manuelle Ausfuehrung.

- **Option A – bestehende Owner und manuellen V1-Weg erhalten.**
- **Option B – spaetere gemeinsame Integrationsfassade planen,** ohne die
  beiden Owner zu ersetzen.
- **Option C – neues Top-Level-Modul `ma_sim_external` einfuehren.**

**Empfehlung:** Option A; Option B erst Post-V1 bei echtem Mehrprogramm- oder
Connectorbedarf. Option C erzeugt derzeit Doppellogik.  
**Rechtegate:** direkte API, Simulationsstart und EQUA-Verarbeitung bleiben
gesperrt.  
**Rueckfall:** P009/P018 und die vorhandenen Adaptergrenzen.  
**Nutzerentscheidung:** offen.

### S-04 Analyse-, Stage- und Bewertungsowner

**Ist-Stand:** `ma_dimensionierung` besitzt Dimensionierung; `ma_analyse`
besitzt technische PostProcess-Analyse; `ma_data_preparation` besitzt
`standardized -> prepared`; `ma_economy`, `ma_sustainability` und
`ma_assessment` besitzen getrennte Bewertungsrollen.

- **Option A – bestehende Owner erhalten** und Inhalte innerhalb dieser
  Grenzen ausbauen.
- **Option B – interne Unterbereiche/Profile einfuehren,** ohne neue
  Top-Level-Module oder Datenownership.
- **Option C – neue Top-Level-Module wie `ma_analyse_energy`,
  `ma_optimization`, `ma_standard_proof` und `ma_sensitivity` einfuehren.**

**Empfehlung:** Option A; Option B spaeter bei nachgewiesener Groesse. Option C
widerspricht aktuellen Owner- und Migrationsentscheidungen.  
**Rueckfall:** UD-112/122/126 und P016/P019-P024/P029/P036.  
**Nutzerentscheidung:** offen.

### S-05 Feasibility, KPI und Bewertungsmethode

**Ist-Stand:** technische Analyse und wertfreie Nachweisbereitschaft sind
teilweise umgesetzt. Quelleneinheiten, Dateninventar, Funktionskriterien,
Schwellen, Gewichte und Gesamtmethode sind offen.

- **Option A – neutrales Bewertungsprofil:** technische Kennwerte,
  Feasibility getrennt, Pareto und Gewichtung nur optionale spaetere Sichten.
- **Option B – Feasibility plus Pareto als verbindliche Hauptmethode.**
- **Option C – gewichteter Gesamtscore als Hauptmethode.**

**Empfehlung:** Option A fuer die Struktur. Sie entscheidet noch keine
Schwellen oder Methode, bewahrt aber Provenienz und verhindert versteckte
Wertentscheidungen.  
**Methodengates:** OP-008, OP-017 und OP-018; Norm- und Komfortaussagen bleiben
gesperrt.  
**Rueckfall:** beschreibende technische Analyse ohne Ranking.  
**Nutzerentscheidung:** offen.

### S-06 Mengenermittlung

**Ist-Stand:** Mengen entstehen fachnah in Gebaeude-, Bauteil- und
Technikdaten; ein eigener Gesamtowner ist nicht entschieden.

- **Option A – Fachowner behalten** und einen gemeinsamen, neutralen
  Mengenvertrag fuer Economy/Sustainability bereitstellen.
- **Option B – gemeinsamen Service unter einer bestehenden Querschnitts- oder
  Bewertungsgrenze planen.**
- **Option C – neues Top-Level-Modul `ma_quantity`.**

**Empfehlung:** Option A. Sie verhindert doppelte Ermittlung und erhaelt die
fachliche Verantwortung. Ein eigener Owner ist fuer V1 nicht nachgewiesen.  
**Rueckfall:** bestehende Fachmodulgrenzen.  
**Nutzerentscheidung:** offen.

### S-07 Workflow und Rules

**Ist-Stand:** Fachmodule validieren und berechnen; `ma_rules` bewertet
versionierte Fachregeln; `ma_workflow` orchestriert freigegebene Services und
enthaelt keine Fachberechnung; die UI visualisiert und startet bewusste
Aktionen.

- **Option A – bestehende Verantwortungsgrenze bestaetigen.**
- **Option B – einen internen `ma_workflow.orchestrator`-Bereich spaeter
  ausbauen,** ohne neue Top-Level-Infrastruktur.
- **Option C – einen parallelen Workflow-Orchestrator einfuehren.**

**Empfehlung:** Option A; Option B nur als interne Weiterentwicklung. Option C
erzeugt eine zweite Workflowwahrheit.  
**Rueckfall:** P027/UD-112/UD-114.  
**Nutzerentscheidung:** offen.

### S-08 Datenhaltung und PostgreSQL

**Ist-Stand:** V1 bleibt dateibasiert; PostgreSQL ist durch UD-129 eine
Post-V1-Option. Domainmodell, Repository-Grenze, Zeitreihenhaltung,
Portabilitaet und Migration sind nicht final.

- **Option A – V1 unveraendert; Post-V1 zuerst Domain- und
  Repositoryvertrag planen.**
- **Option B – nach V1 einen begrenzten lokalen PostgreSQL-Pilot planen.**
- **Option C – Datenbankmigration vor V1-Abschluss beginnen.**

**Empfehlung:** Option A. Option B kann danach ein kleiner, reversibler
Forschungsslice werden. Option C widerspricht UD-129.  
**Rueckfall:** dateibasierter Workspace.  
**Nutzerentscheidung:** nur die genaue Post-V1-Tiefe bleibt offen; die
V1-Grenze ist bereits entschieden.

### S-09 Prozessmessung und Forschungsgrenze

**Ist-Stand:** P030 und OP-009 fuehren Prozessgrenzen, Messmethode,
Wissensprofile, Wiederholungen und Kostenannahmen. Vorhandene Werte sind
Fallwerte, kein allgemeiner Einsparungsnachweis.

- **Option A – P030 als einzige Forschungsschicht bestaetigen.**
- **Option B – Kennwerte spaeter in `ma_economy` spiegeln,** P030 bleibt
  Methodenowner.
- **Option C – Prozessbewertung in die Produktbewertung integrieren.**

**Empfehlung:** Option A; Option B nur als referenzierte Ergebnisuebergabe.
Option C vermischt Forschungs- und Produktlogik.  
**Rueckfall:** P030/OP-009.  
**Nutzerentscheidung:** offen.

### S-10 Gebaeude, IFC, Heizlast, Zonen und V1-5Z

**Ist-Stand:** P012/P013/P016 und der unabhaengige V1-Plan fuehren die
Restarbeit. IFC-Beziehungen sind unvollstaendig; Nordbezug, IDM-/Excel-
Konflikt, Dachraumthermik, 29Z-Trennung und neutrale Ergebnissemantik besitzen
offene Evidenz- oder Fachgates.

- **Option A – bestehende V1-5Z-Baseline konservativ erhalten** und jeden
  Evidenzkonflikt sichtbar `PARTIAL` lassen.
- **Option B – einzelne bestaetigte Quellkorrekturen additiv uebernehmen,**
  ohne 5Z/29Z oder Quellen zu vermischen.
- **Option C – Struktur aus IFC/IDM automatisch neu ableiten.**

**Empfehlung:** Option A plus gezielte Option-B-Korrekturen nach Nachweis.
Option C ist fachlich und rechtlich nicht freigegeben.  
**Rueckfall:** aktuelle 5Z-Baseline und getrennte 29Z-Vergleichsquelle.  
**Nutzerentscheidung:** zu Nordbezug, IDM-/Excel-Konflikt und Dachraumthermik
offen.

### S-11 Parametergruppen

**Ist-Stand:** Der Referenzplan ist als P015-Ergaenzung aufgenommen. UD-125
sowie P015-S5A/S5B fuehren Definitionen, Gruppen, Instanzen und die getrennten
Statusachsen.

- **Option A – bestehende P015-Einordnung bestaetigen.**
- **Option B – Referenzplan als neuen P-Plan behandeln.**

**Empfehlung:** Option A. Option B wuerde denselben Scope duplizieren.  
**Rueckfall:** P015/UD-125.  
**Nutzerentscheidung:** nur erforderlich, falls die bestehende Einordnung
bewusst revidiert werden soll.

### S-12 Rechte-, Inhalts- und Automatisierungsgrenzen

**Ist-Stand:** geschuetzte Normen, Literatur, vollstaendige IDA-/EQUA-Inhalte,
externe APIs und automatische Simulation besitzen eigene Rechte- und
Freigabegates.

- **Option A – bestehende Gates unveraendert erhalten.**
- **Option B – einzelne Objekte nach dokumentiertem Rechte- und
  Verarbeitungsscope freigeben.**
- **Option C – aus Dateibesitz oder `.gitignore` eine generelle Freigabe
  ableiten.**

**Empfehlung:** Option A; Option B nur objektbezogen. Option C ist unzulaessig.
Der leere ZIP-Eingang ist kein auswertbarer Inhalt; der zweite ZIP-Eingang
bleibt ungeoeffnet.  
**Rueckfall:** AGENTS.md, OP-016 und Projektinput-Workflow.  
**Nutzerentscheidung:** derzeit keine generelle Freigabe.

### S-13 Governance-ID-Kollision

**Ist-Stand:** `USER_DECISIONS_OPEN_POINTS.md` verwendet `OP-017` zweimal:
fuer den neutralen Ergebnisvertrag und fuer den Council-Spezialistenpool.
`OP-012b` ist dagegen eine absichtliche Unterkennung und keine zweite
`OP-012`-Ueberschrift.

- **Option A – Ergebnisvertrag als OP-017 erhalten und Council-Punkt auf die
  erste freie ID umnummerieren.**
- **Option B – Ergebnisvertrag umnummerieren.**
- **Option C – Kollision bestehen lassen.**

**Empfehlung:** Option A, weil P009/P018/P029/P036 und der V1-Plan bereits auf
den Ergebnisvertrag als OP-017 verweisen. Die erste freie ID ist vor Stufe B
erneut mechanisch zu pruefen.  
**Rueckfall:** keine inhaltliche Aenderung, nur eindeutige Kennungen.  
**Nutzerentscheidung:** als Governance-Korrektur in der Baseline bestaetigen.

## Vorgeschlagene Anti-Regression-Baseline

Diese Baseline ist ein Entwurf und noch nicht bestaetigt:

1. P007 bleibt der fuehrende Gesamt- und Architekturrahmenplan.
2. Neuere ausdrueckliche Nutzerentscheidungen praezisieren P007 innerhalb
   ihres bezeichneten Scopes.
3. `TARGET_ARCHITECTURE.md` fuehrt die technische Zielstruktur.
4. `docs/project/workflow/README.md` und seine Modulsteckbriefe fuehren den
   fachlichen Gesamtworkflow; P027 fuehrt den technischen Workflow-
   Querschnitt; P037/UD-128 fuehren die Dokumentrollen.
5. Planindex und Planstatus bleiben reine Inventar- und Statusquellen.
6. `ma_dimensionierung`, `ma_data_preparation`, `ma_analyse`, `ma_economy`,
   `ma_sustainability`, `ma_assessment`, `ma_rules` und `ma_workflow` behalten
   ihre bestaetigten Ownergrenzen, bis eine neue Nutzerentscheidung sie
   gezielt revidiert.
7. P018 behaelt fuer V1 `RUN-ID + VAR-ID` ohne `SimulationCase`/`CASE-ID`.
8. `ma_export_simulation` und `ma_import_simulation` bleiben neutrale
   Simulationsschnittstellen; V1 bleibt manuell.
9. PostgreSQL und Repository-Migration bleiben Post-V1 nach UD-129.
10. Pareto, Gewichtung, neue Top-Level-Module, `ma_quantity`, automatische
    Simulation und Connectoren bleiben Folgeoptionen, nicht aktive
    Zielarchitektur.
11. Alte Handover stehen unterhalb von Gesamtplan, Nutzerentscheidungen,
    bestaetigten aktiven Plaenen und den Quellen entsprechend ihrer
    Dokumentrolle.
12. Widersprueche werden gestoppt und als historisch, zurueckgestellt oder
    konfliktbehaftet dokumentiert; sie duerfen keine stille Rueckmigration
    ausloesen.

## Entscheidungen fuer das Gespraech

Der Nutzer soll die Punkte S-01 bis S-13 besprechen. Fuer eine kompakte
Baseline sind insbesondere explizit zu bestaetigen:

1. Dokumentrollen und Bedeutung von `Workflow_Gesamtplan`;
2. RUN-/VAR-Modell ohne oder mit spaeterem `SimulationCase`;
3. bestehende Simulations-, Analyse-, Bewertungs-, Workflow- und Rules-Owner;
4. Strukturrolle von Feasibility, Pareto, Gewichtung und Mengenermittlung;
5. Post-V1-Grenze fuer PostgreSQL und Repository-Layer;
6. konservative V1-5Z- und Evidenzgrenzen;
7. Rechte- und Automatisierungsgates;
8. Anti-Regression-Prioritaet und Governance-ID-Korrektur.

Nach der Besprechung wird der bestaetigte Baseline-Entwurf wiederholt. Erst
nach ausdruecklicher Bestaetigung und einer erneuten
`Freigabe zur Umsetzung` beginnt Stufe B.
