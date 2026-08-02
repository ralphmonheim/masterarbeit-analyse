# Chat-Handover: Konsolidierte erste Funktionsversion und Gesamtprozess

Stand: 2026-07-31

## Zweck und Abschlussstatus

Dieser Snapshot schliesst die in diesem Chat erarbeitete Grundlagen- und
Entscheidungsarbeit ab. Alle getroffenen Nutzerentscheidungen wurden vor der
Archivierung in UD-112 und die zuständigen aktiven Plaene uebertragen. Dieses
Dokument ist deshalb nur historische Kontextreferenz und keine zweite
Planungs- oder Aufgabenwahrheit.

## Fuehrende Quellen ab diesem Handover

- Gesamtziel und uebergreifender Prozess: P007,
  `docs/project/plans/inbox/Masterarbeit_VSCode_Projektplan_2026-06-21.md`
- Nutzerentscheidungen und Ersetzungsvermerke: UD-112,
  `docs/project/decisions/USER_DECISIONS_MASTERTHESIS_CODE.md`
- aktive Umsetzungs- und Migrationsplanung: P009, P013, P014, P016-P018,
  P027, P029 und P030 im Planindex
- offengebliebene echte Nutzergates: OP-008, OP-009, OP-017 und OP-018 in
  `docs/project/decisions/USER_DECISIONS_OPEN_POINTS.md`
- zusammenfassender Arbeitsstand: `docs/project/plans/PLAN_STATUS.md`

## Dokumentierte Entscheidungen

- Die Arbeit vergleicht den fachlichen Mehrwert dynamischer Simulation und
  den Zeit-/Kostenaufwand eines softwaregestuetzten Workflows mit dem
  manuellen Referenzprozess.
- SmallOffice mit Endvariante 02 und fuenf Zonen ist der erste
  Demonstrator, aber kein Sonderworkflow. Alle durch VGEN erzeugten Varianten
  werden manuell in IDA ICE ausgefuehrt und als Zeitwerte erfasst.
- Die dauerhafte PreProcess-Reihenfolge ist Projekt, Wetter, Gebaeude,
  Technik, Zonen und Parameter. Technik besitzt systemweite Systeme und IDs;
  Zonen ordnen diese zonal zu.
- `ma_dimensionierung` ist ein eigenes Kernmodul. `ma_variants` erkennt nur
  Bedarf/Gruppen; `ma_analyse` ist ausschliesslich PostProcess.
- Die verbindliche Varianten-Auswahl liegt vor der tatsaechlichen
  Dimensionierung; VSP, VVER, VCAT, VSEL und VGEN bleiben die vorhandenen
  Begriffe, ohne CASE-/SimulationCase-Parallelmodell.
- Ein wissenschaftlicher RUN hat eine Selection, ein Setup und mehrere VAR.
  `(RUN-ID, VAR-ID)` ist der manuelle Ausfuehrungs- und Ergebnisbezug.
- `ma_simulation_setup` speichert per Themen-Checkbox angeforderte Outputs.
  `ma_analyse` liefert alle datenkompatiblen Diagramme der gewaehlten Themen;
  nicht gewaehlte bzw. nicht auswertbare Themen bleiben sichtbar getrennt.
- Heating-Diagramme werden ohne eigene Nutzerabstimmung weder optisch noch
  fachlich veraendert. Jede V1-Funktion muss in der UI sichtbar und bedienbar
  sein.
- Die UI besitzt eine direkte Modulansicht und eine getrennte, interaktive
  Workflowansicht. Deren Einstieg ist eine Gesamtuebersicht mit PreProcess,
  Kernprozess und PostProcess. Sie zoomt in Bereichsmodule und danach in die
  jeweilige Fachansicht; Weiter und Zurueck bleiben dabei jeweils auf der
  aktuellen Ebene. PostProcess-Rueckschluesse und PreProcess-Validierungen
  werden sichtbar, loesen aber keine automatische Aenderung oder Iteration
  aus.
- P030 misst PreProcess-Skalierung, manuelle IDA-Arbeit, Maschinenzeit,
  Korrektur und PostProcess getrennt. Aktive Arbeitszeit und Wartezeit bleiben
  fuer Kosten getrennt; Entwicklung, Einarbeitung und Lizenz sind nur ein
  separates Adoptionsszenario.
- Lokale Tests duerfen mit synthetischen Daten und freigegebenen neutralen
  Ergebnisexports arbeiten. Vollstaendige IDA-/EQUA-Dateien, Bibliotheken,
  automatischer IDA-Start und IDM-Manipulation bleiben ohne Rechtebeleg
  gesperrt.

## Nachweis des Ziel-Ist-Abgleichs

Die dokumentierten Ziele weichen bewusst sichtbar vom bisherigen Bestand ab:

- UD-106 fuehrte bisher Zonen vor Technik.
- P016 und der Bestand fuehren Dimensionierung noch unter `ma_analyse`.
- Der Bestand materialisiert noch Varianten-nahe Einzelruns bzw. Run-Gruppen.

UD-112, P007 und die betroffenen Teilplaene markieren diese Punkte als
Migrationsbedarf. Dieser Chat hat keine Code-, Konfigurations- oder
Datenschnittmigration ausgefuehrt. Die konkreten Folgeschritte stehen damit
ausschliesslich in den genannten aktiven Plaenen; die offenen fachlichen
Entscheidungen ausschliesslich in den genannten OPs.

## Nachtrag: Workflowansicht und Navigation

Die historische Referenzgrafik liegt unter
`docs/project/archive/workflow/WORKFLOW_DIAGRAM_v0.1.0_2026-06-18.jpg`. Sie
bleibt die fachliche Quelle fuer Rollen, Informationsobjekte,
Entscheidungsknoten und Rueckkopplungen, ist aber nicht das kuenftige
Bildschirm-Layout.

Der verbindliche UI-Vertrag wurde nach diesem Handover in UD-112, P027 und
den Planstatus uebertragen:

1. Die **Modulansicht** ist der schnelle, direkte Einstieg in eine
   Fachfunktion und zeigt nur deren konkrete Arbeit.
2. Die **Workflowansicht** startet auf **Ebene 1** in einer
   Gesamtuebersicht der drei anklickbaren Bereiche `PreProcess`,
   `Kernprozess (MainProcess)` und `PostProcess`. Sie zeigt nur verdichtete
   Validierungs- und Reviewhinweise; zum Beispiel kann ein
   PostProcess-Befund auf ein Eingabemodul zurueckweisen.
3. **Ebene 2** zoomt in den gewaehlten Prozessbereich: Module,
   Uebergaben und konkret beschriftete Validierungs-/Entscheidungsknoten
   werden sichtbar. PreProcess-Pruefschritte liegen hier am fachlich
   passenden Uebergang.
4. **Ebene 3** oeffnet die reale Fachansicht mit ihren Reitern oder
   Detailschritten.
5. Weiter und Zurueck bewegen sich nur auf der gerade sichtbaren Ebene;
   die Pfadnavigation wechselt gezielt eine Ebene nach oben. Aktive Seite,
   Unteransicht und Entwuerfe bleiben dabei erhalten.
6. Ein Ruecksprung wegen Validierung oder PostProcess-Review ist ein
   ausdruecklicher, benannter Link zum Zielmodul und nie eine automatische
   Aenderung, Bestvariantenauswahl oder Iteration.

Die konkrete Darstellung soll interaktiv und vektorfaehig sein. Ob die
frueher diskutierte Bezeichnung `G2` zutrifft oder eine andere Technik besser
passt, wird erst bei der Bestandsanalyse entschieden; es wird keine neue
Bibliothek allein aus diesem Handover eingefuehrt.

## Aktualisierter Startprompt fuer den naechsten Umsetzungs-Chat

```text
Arbeite im Repository 260524_Masterarbeit_Analyse weiter.

Lies zuerst AGENTS.md sowie den aktuellen Gesamtprozess in UD-112, P007,
P027 und PLAN_STATUS. Lies ausserdem dieses Handover und die historische
Workflowgrafik unter docs/project/archive/workflow/. Gesamtplan und
Nutzerentscheidungen sind vor Einzelplaenen und vor dem bestehenden Code
massgeblich.

Ziel: Setze die bereits freigegebene Workflow- und Modulnavigation in ma_ui
als eigenen, getesteten UI-Slice um. Die Fachlogik bleibt unveraendert in den
Fachmodulen; ma_ui zeigt und navigiert nur.

Verbindlicher Bedienvertrag:
- Es gibt eine direkte Modulansicht fuer den schnellen Sprung in ein
  Fachmodul und eine getrennte Workflowansicht.
- Die Workflowansicht startet in einer Gesamtuebersicht, nicht an einem
  erzwungenen linearen Startpunkt. Ebene 1 zeigt die anklickbaren Bereiche
  PreProcess, Kernprozess (MainProcess) und PostProcess.
- Ebene 1 darf verdichtete PreProcess-Validierungs- sowie
  PostProcess-Reviewhinweise zu betroffenen Eingabemodulen zeigen. Hinweise
  duerfen keine Eingaben, Varianten, Selections oder Runs automatisch aendern.
- Ebene 2 zeigt innerhalb des gewaehlten Bereichs die verbindliche
  Modulreihenfolge, Uebergaben und benannte Entscheidungsknoten mit klaren
  Ruecksprungzielen.
- Ebene 3 ist die vorhandene Fachansicht eines Moduls mit ihren Reitern oder
  Wizard-Schritten.
- Weiter und Zurueck bewegen sich ausschliesslich innerhalb der aktiven
  Ebene. Eine sichtbare Pfadnavigation fuehrt eine Ebene zurueck, ohne
  Projektzustand, Unteransichten, Auswahlen oder Entwuerfe zu verlieren.
- Korrekturpfade sind ausdrueckliche, benannte Links zum Zielmodul und keine
  versteckte Bedeutung der Zurueck-Taste. Es gibt keine automatische
  Review-Iteration oder Bestvariantenauswahl.
- Nutze die vorhandene Detailschritt-Logik der Analyseansicht als
  Bedienvorbild. Behalte die vorhandene Zustands- und Draft-Sicherheit bei.
- Die historische Workflowgrafik ist fachliche Referenz, aber nicht das
  direkte Bildschirm-Layout. Eine neue Abhaengigkeit oder Grafikbibliothek
  darf nicht eingefuehrt werden, ohne vorherige Analyse und ausdrueckliche
  neue Freigabe.

Pruefe zuerst src/ma_ui/streamlit_app/app.py, navigation.py,
workflow_graph.py und workflow_view.py sowie die vorhandenen UI-Tests.
Lege dann einen kurzen Umsetzungsplan mit Dateien, Zustandsmodell,
Navigationsregeln und Tests vor. Die Freigabe zur Umsetzung gilt fuer genau
diesen UI-Navigationsscope. Keine fachlichen Modul-, Diagramm-, Datenformat-
oder Abhaengigkeitsaenderungen ohne neue Freigabe. Dokumentiere den Abschluss
in P027, PLAN_STATUS und CHANGELOG und fuehre passende Tests aus.
```
