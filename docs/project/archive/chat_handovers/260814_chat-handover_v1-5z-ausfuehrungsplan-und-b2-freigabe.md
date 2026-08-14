# Chat-Handover: V1-5Z-Ausfuehrungsplan und B2-Freigabe

Datum: 2026-08-14
Status: Prompt-Intake und unabhaengige Sol-Planung abgeschlossen; Umsetzung
fuer einen neuen Tera-Chat freigegeben, aber noch nicht begonnen.

## Abgeschlossener Stand

- Der V1-Umfang zu 5Z-Gebaeudemapping, Workflow-UI, Varianten, manuellem
  IDA-Gate, Ergebnisimport, Datenvorbereitung, Tabellen, Diagrammen und
  Prozessmessung wurde zu einem vollstaendigen Arbeits-Prompt konsolidiert.
- Ein separater `quality_auditor` hat den Planinhalt read-only erarbeitet und
  geprueft. Der Hauptchat hat das Ergebnis unveraendert als
  `docs/project/plans/independent/260814_V1_5Z_Gebaeudemapping_Workflow_UI_PostProcess_Test.md`
  gespeichert.
- Der Plan ist gemaess Themenroutine ohne P-Nummer gespeichert und wurde
  nicht automatisch in `PLAN_INDEX.md`, `PLAN_STATUS.md` oder einen
  bestehenden formellen Plan eingearbeitet.
- Der Nutzer hat am 2026-08-14 mit der exakten Formulierung
  `Freigabe zur Umsetzung` den beschriebenen Umfang freigegeben und danach
  mit `mit B2` die objektbezogene B2-Verarbeitung ausdruecklich
  eingeschlossen.
- Produktcode, Produktkonfigurationen und Testdaten wurden in diesem
  Planungsabschnitt nicht veraendert. Es erfolgte kein Commit oder Push.

## Einordnung und Quellenhierarchie

Der unabhaengige Plan ist der freigegebene Ausfuehrungs- und Uebergabeplan,
aber keine neue Architekturwahrheit. Fuer Zielarchitektur und
Fachentscheidungen gilt seine Sektion `Verbindliche Quellen- und
Konflikthierarchie`: zuerst P007 und einschlaegige Nutzerentscheidungen,
danach P012 bis P018 sowie P027, P029, P030 und P036 innerhalb ihres
jeweiligen Modulscopes; `PLAN_INDEX.md`, `PLAN_STATUS.md` und die offenen
Entscheidungen bleiben Status- und Gatewahrheit. Bei einem Widerspruch wird
nur der betroffene Slice gestoppt.

Die folgende Kurzorientierung ist nicht fuehrend und erweitert oder ersetzt
weder den Ausfuehrungsplan noch dessen kanonische Fachquellen und Gates:

- Hauptfall ist der vollstaendige 5Z-Softwarepfad bis zur
  PostProcess-Ausgabe; IDA bleibt der manuelle Zwischenschritt. Vorhandene
  29Z- und historische Ergebnisse dienen getrennt dem Prepare- beziehungsweise
  Vergleichstest und werden nicht als Ergebnisse neu erzeugter Varianten
  ausgegeben.
- Die 5Z-Datenhierarchie und die bestaetigten Zonenwerte stehen in den
  gleichnamigen Plansektionen. Fuer OG West und OG Ost gilt die oberste
  Geschossdecke, fuer die Lobby das Dach; der Zwischenbereich gehoert nicht
  zur thermischen Huelle.
- Die wissenschaftliche Optimierung umfasst 30 Kandidaten aus fuenf
  Temperaturbaendern und sechs gekoppelten Leistungsfaktoren mit
  `cooling.factor = heating.factor`. Acht OFAT-Faelle bleiben eine getrennte
  Einfaktor-Sensitivitaet. Der groessere Variantenraum ist nur eine als
  `test_only` markierte Funktionsdemo.
- Gebaeude, Technik und Zonen bilden in dieser Reihenfolge drei
  UI-Hauptschritte. Workflow- und Direktansicht bleiben Oberflaechen auf
  denselben Backendvertraegen und demselben gespeicherten Projekt-Workspace;
  die Workflowansicht erhaelt keine zweite Persistenz- oder Fachlogik.
- Prozesszeiten werden zuerst absolut verglichen. Relative Verbesserungen
  oder Verschlechterungen erscheinen nur bei gleicher Prozessgrenze und
  belastbarer manueller Referenz.

## B2-Nachweis und Grenzen

B1 bezeichnet das eigenstaendige 5Z-Kernmapping aus den freigegebenen
IDA-/Excel-Quellen. B2 bezeichnet die nachgelagerte Viewer-/IFC-Anreicherung;
B1 bleibt auch ohne IFC-GlobalIds funktionsfaehig.

Die Rechteprovenienz und Objektgrenzen stehen in den Plansektionen
`Freigegebene lokale B2-Objekte` sowie `Rechte- und Freigabegates`.
Freigegeben sind die lokale maschinelle Auswertung der konkret genannten
Viewer-Excel und der SmallOffice-IFC sowie die Speicherung abgeleiteter
Bauteil-, Oeffnungs- und GlobalId-Mappings. Die externe und die lokale IFC
sind durch denselben SHA-256
`B933A06810A08EE6114E709861A822A06A778962A01567287CE879413CBB3055`
als bytegleich belegt. Die Viewer-Excel ist mit SHA-256
`D7DDBC73D15A8CFF315AADFC42ABEE0877AA09171E5E4CE895F24E8420E1686D`
gebunden.

Nicht freigegeben sind insbesondere Rohdateiversionierung,
3DM-Inhaltsverarbeitung, neue Abhaengigkeiten oder Installationen,
automatische IDA-Steuerung, externe beziehungsweise Cloud-Verarbeitung,
Loeschungen sowie Commit, Push, Tag oder Release.

## Nachweise und aktueller Zustand

- Der gespeicherte Plan umfasst 882 Zeilen und enthaelt den finalen
  Arbeits-Prompt, die geordneten Umsetzungspakete, UI-Testmatrix,
  Abnahmekriterien, Risiken und Stopbedingungen, Rechtegates, offene
  Entscheidungen und eine konkrete `Tera-Uebergabe`.
- Im aktuellen Worktree bestehen bereits zahlreiche, teilweise fachlich
  ueberlappende Aenderungen. `Paket 0 - Preflight, Bestandsschutz und
  Baseline` ist deshalb der verpflichtende Dirty-Worktree-, Scope- und
  Vertragsaudit vor Produktarbeit.
- Zum Einstieg in Paket 0 ist keine weitere globale Vorabentscheidung
  erforderlich. Fuer jedes spaetere Paket gelten jedoch die Plansektionen
  `Risiken und Stopbedingungen`, `Rechte- und Freigabegates` und `Offene
  Entscheidungen`; sie legen fest, wann ein Slice blockiert, nur `PARTIAL`
  ausweisbar oder spaeter gesondert freizugeben ist.
- Die schreibfreie Navigatorvalidierung meldete am 2026-08-14 einen
  veralteten Stand mit vier fehlenden und vier zusaetzlichen beziehungsweise
  geaenderten lokalen Metadatenzeilen. Die getrennte Navigator-Folgearbeit
  bleibt in P031; im Handover wurde keine Navigatoraktualisierung
  ausgefuehrt.

## Fuehrende Referenzen

- `docs/project/plans/independent/260814_V1_5Z_Gebaeudemapping_Workflow_UI_PostProcess_Test.md`:
  freigegebener Ausfuehrungs- und Uebergabeplan; insbesondere die Sektionen
  `Verbindliche Quellen- und Konflikthierarchie`, `Geordnete
  Umsetzungspakete`, `Risiken und Stopbedingungen`, `Rechte- und
  Freigabegates`, `Offene Entscheidungen` und `Tera-Uebergabe`.
- P007 und die im unabhaengigen Plan bezeichneten Nutzerentscheidungen:
  fuehrende Gesamtarchitektur.
- P012 bis P018, P027, P029, P030 und P036: fuehrende Modulplaene innerhalb
  ihres jeweiligen Scopes.
- `PLAN_INDEX.md`, `PLAN_STATUS.md` und
  `docs/project/decisions/USER_DECISIONS_OPEN_POINTS.md`: Status- und
  Gatewahrheit.
- `docs/project/UPDATE_ROUTINES.md` und
  `.agents/skills/prompt-intake/SKILL.md`: Themenroutine und
  Freigabeprozess.
- P031: fuehrende Quelle fuer die getrennte Navigator-Folgearbeit.

## Umsetzungseinstieg im neuen Chat

Der neue Tera-Chat liest den unabhaengigen Plan vollstaendig und beginnt mit
`Paket 0 - Preflight, Bestandsschutz und Baseline`. Er setzt nur den dort
freigegebenen Umfang einschliesslich B2 um und beachtet die im Plan
dokumentierte Quellenhierarchie. Bei einem Konflikt mit einer fuehrenden
Quelle, einer Scope-Erweiterung, neuen Abhaengigkeit, Loeschung,
automatischen IDA-Aktion, externen Verarbeitung oder Git-Veroeffentlichung
wird der betroffene Umfang angehalten.

Startformulierung:

> Setze den freigegebenen unabhaengigen Umsetzungsplan
> `docs/project/plans/independent/260814_V1_5Z_Gebaeudemapping_Workflow_UI_PostProcess_Test.md`
> einschliesslich B2 um. Lies den Plan vollstaendig und beginne mit Paket 0.

Alle verbleibenden Arbeiten, Entscheidungen und Gates stehen ausschliesslich
in den genannten fuehrenden Quellen; dieser Snapshot fuehrt keine eigene
offene Aufgabenliste.
