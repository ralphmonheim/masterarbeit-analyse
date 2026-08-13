# P037 Dokumentationshierarchie, Workflowwissen und UI-Informationsarchitektur

Datum: 2026-08-13  
Status: umgesetzt; P037-A bis P037-C am 2026-08-13 abgeschlossen  
Prioritaet: hoch fuer Dokumentationsqualitaet und UI-Verstaendlichkeit  
Owner: Projektdokumentation, `ma_workflow`, `ma_ui`  
Abhaengigkeiten: P007, P027, P031, UD-112, UD-114, UD-128

## Ziel

Die versionierte Projektdokumentation wird strukturell analysiert und so
geordnet, dass jedes aktuelle Dokument eine eindeutige Aufgabe besitzt und
jedes Thema genau eine fuehrende Quelle hat. Darauf aufbauend werden die
fachlichen Workflowinformationen und die technischen Entwicklungsinformationen
klar getrennt, ohne gemeinsame Stammdaten doppelt zu pflegen.

Der Plan liefert zugleich die Inhaltsgrundlage fuer zwei getrennte
UI-Kontexte:

- Die **Workflowansicht** erklaert dem Nutzer den fachlichen Ablauf, Begriffe,
  Werte, Datenherkunft, Bedienung und Beispiele.
- Die **Bearbeitungsansicht** erklaert die technische Entwicklung eines
  Moduls, seinen Stand, seine Verknuepfungen und seine aktiven Plaene.

P037 konkretisiert P027. Die Prozessgrenzen und die spaete Einordnung der
Workflow-UI aus UD-114 bleiben verbindlich und werden nicht still ersetzt.

## Festgelegte Zielhierarchie

1. **Leitfaden**: Zweck, wissenschaftliche Richtung, Methodenrahmen,
   Systemgrenzen und Erfolgskriterien der Masterarbeit.
2. **Fachlicher Gesamtworkflow**: operative fachliche Hauptquelle mit
   Gesamtuebersicht und Modulsteckbriefen.
3. **Architektur, Entscheidungen und aktive Plaene**: technische Zielstruktur,
   verbindliche Entscheidungen und laufende Umsetzung.
4. **Planstatus, Changelog und offene Punkte**: aktueller Arbeits- und
   Aenderungsstand.
5. **Archiv**: historische Nachweise und abgeloeste Staende; keine aktive
   Inhaltswahrheit.
6. **Navigator**: uebergreifende Auffindbarkeit, Rollenbeschreibung der Ordner
   und Verweise auf die jeweils fuehrende Quelle; keine eigene Fach-, Status-
   oder Entscheidungswahrheit.

## Verbindliche Informationsaufteilung

### Fachlicher Gesamtworkflow und Workflow-Infokarten

Der Gesamtworkflow besteht aus einer zentralen Uebersicht und je einer
eigenen Markdown-Datei pro katalogisiertem Modul. Auch geplante,
konzeptionelle oder zurueckgestellte Module werden angezeigt, weil die
vollstaendige Modulmenge den Projektumfang abbildet.

Jeder Modulsteckbrief soll, soweit fuer das Modul relevant, enthalten:

- Zweck und Rolle im Gesamtprozess;
- Einordnung in PreProcess, Kernprozess, PostProcess oder Querschnitt;
- fachliche Eingaenge, Ausgaenge und Uebergaben;
- erklaerte Begriffe, Abkuerzungen, Kategorien, Werte und Einheiten;
- Herkunft und Bedeutung der verwendeten Daten;
- Bedienablauf und Hinweise fuer typische Fragen waehrend der Nutzung;
- ein kurzes, nachvollziehbares Beispiel;
- kurze wissenschaftliche Quellenangaben in Fussnotenform;
- Statuskennzeichnung fuer umgesetzt, teilweise umgesetzt, geplant,
  konzeptionell oder zurueckgestellt.

Aktive Umsetzungsplaene werden nicht in diesen fachlichen Karten gefuehrt.

### Bearbeitungsansicht und technische Modul-Infokarten

Die technische Modulkarte soll enthalten:

- Anzeigename, stabile Modul-ID und Rolle in der Gesamtarchitektur;
- Implementierungs- und Teststand;
- verantwortliches Paket, wichtige Dateien und Schnittstellen;
- Abhaengigkeiten, Ein- und Ausgaben sowie technische Verknuepfungen;
- relevante Entscheidungen und Dokumente;
- ausschliesslich aktive Plaene und aktuelle technische Restarbeit.

Begriffe duerfen in beiden Ansichten vorkommen, wenn sie sowohl fuer Nutzung
als auch Entwicklung notwendig sind. Die Definition besitzt trotzdem nur
eine fuehrende Quelle; die zweite Ansicht verweist oder uebernimmt sie aus
dem gemeinsamen strukturierten Feld.

### Gemeinsame Datenquelle

Stabile Strukturfelder wie Modul-ID, Anzeigename, Prozessbereich, Status und
technische Paketzuordnung werden aus einem UI-neutralen technischen Katalog
bezogen. Erklaerender Langtext, Beispiele und Quellenhinweise werden in den
Markdown-Modulsteckbriefen gepflegt. Die UI rendert diese Quellen, statt
denselben Inhalt ein zweites Mal im Streamlit-Code zu hinterlegen.

## Festgelegtes Bedienkonzept

- Der normale Anwendungsstart oeffnet die Bearbeitungsansicht.
- Die Workflowansicht wird bewusst ausgewaehlt.
- Die Projektauswahl erscheint nur, wenn innerhalb der Workflowansicht
  `Start` angeklickt wird.
- Die Bearbeitungsansicht zeigt wieder die Struktur
  `PreProcess | Kernprozess | PostProcess | Querschnittsmodule`.
- Auf einer Modulansicht wird der bisherige Infozugang in zwei kleinere,
  eindeutig beschriftete Zugaenge geteilt:
  `Technische Modulinfo` und `Hilfe zum Ablauf`.
- Workflowkarten duerfen kurze Quellenfussnoten und Vergleiche enthalten.
  Ausbaufaehige Hinweisfenster sind eine spaetere Option, nicht Teil des
  ersten Slices.
- Navigation darf keine Fachaktion, Auswahl, Persistenz oder
  Statusaenderung automatisch ausloesen.

## Analysebasis vom 2026-08-13

Die read-only Bestandsaufnahme vor Planerstellung ergab:

- 181 versionierte Markdown-Dateien, davon 109 unter `docs/project/`;
- 30 katalogisierte Module in `src/ma_workflow/catalog.py`;
- getrennte Bearbeitungs- und Workflowansichten sind bereits vorhanden,
  beziehen ihre Erklaerungen aber noch aus gemischten Quellen;
- der normale Start fuehrt derzeit ueber die Projektauswahl;
- die Bearbeitungsansicht gruppiert derzeit nur Fachmodule, Querschnitt und
  Infrastruktur statt der festgelegten vier Prozessbereiche;
- P027 und UD-114 definieren bereits Prozessgrenzen, Workflowebenen und
  Navigationsgrenzen; P037 muss diese Vorgaben abgleichen und erweitern;
- der Navigator verweist fuer UI/Workflow aktuell auf P027 und wird erst nach
  der Dokumentkonsolidierung um P037 und die neue Workflowdokumentation
  ergaenzt.

Diese Zahlen sind ein datierter Analysehinweis und keine dauerhafte
Dokumentgrenze.

## Umsetzungsslices

### P037-S0 Dokumentinventar und Ist-Analyse

1. Alle mit `git ls-files` versionierten Dokumente erfassen, einschliesslich
   Root-Dokumenten, Modul-READMEs, Architektur, Entscheidungen, Plaenen,
   Prompts, Testspezifikationen und Archivordnern.
2. Je Dokument mindestens Pfad, aktueller Zweck, Zielgruppe, Themen,
   Fuehrungsrolle, Aktualitaet, Ueberschneidungen und empfohlene Zukunftsrolle
   dokumentieren.
3. Externe Arbeitsablage nur ueber die vom Navigator erlaubten Metadaten und
   Verweise erfassen. Geschuetzte oder nicht freigegebene Inhalte nicht
   oeffnen.
4. Archivdokumente nicht inhaltlich bereinigen; nur Aufgaben der Archivordner
   und Navigationsrolle festlegen.

Ergebnis: datierter Analysebericht mit Dokumentinventar, Rollenmatrix,
Konfliktliste und Priorisierung.

### P037-S1 Dokumentrollen und fuehrende Wahrheiten festlegen

1. Fuer jedes aktuelle Dokument genau eine Hauptaufgabe festlegen.
2. Pro Thema eine fuehrende Quelle benennen.
3. Doppelungen klassifizieren als bewusstes Kurzreferat, zu ersetzende
   Parallelwahrheit, historische Fassung oder notwendige Schnittstellensicht.
4. Ueberholte aktuelle Dokumente zur Archivierung markieren; keine Datei wird
   ohne gesonderte Freigabe geloescht oder verschoben.
5. Eine Pflegematrix festlegen, die fuer jede Informationsart den ersten
   Aenderungsort und die abgeleiteten Ansichten benennt.

Ergebnis: Sollstruktur und konkrete, dateibezogene Bereinigungsvorschlaege.

### P037-S2 Fachlichen Gesamtworkflow aufbauen

1. Bestehende geeignete Workflowdokumentation konsolidieren; keine parallele
   Dokumentationswurzel anlegen.
2. Eine zentrale Workflowuebersicht fuer PreProcess, Kernprozess,
   PostProcess und Querschnitt erstellen.
3. Unter `docs/project/workflow/modules/` einen Markdown-Steckbrief fuer jedes
   der 30 katalogisierten Module anlegen.
4. Gemeinsames Steckbriefschema, Statusvokabular, Quellenfussnoten und
   Querverweise definieren.
5. Fachliche Aussagen gegen Leitfaden, Entscheidungen, Gesamtplaene und
   Modulplaene pruefen; ungeklärte Aussagen sichtbar als offen markieren,
   nicht erfinden.

Ergebnis: vollstaendige fachliche Workflowquelle fuer Dokumentation und UI.

### P037-S3 Dokumentdoppelungen bereinigen

1. Bestaetigte Parallelbeschreibungen auf die fuehrende Quelle reduzieren.
2. Verbleibende Dokumente mit Zweck, Geltungsbereich, Owner und
   Aktualisierungsregel kennzeichnen.
3. Root-README, Modul-READMEs, Architektur- und Planverweise anpassen.
4. Archivkandidaten erst nach gesonderter Freigabe verschieben; keine
   Loeschungen.

Ergebnis: eine Wahrheit pro Thema mit kurzen, stabilen Verweisen.

### P037-S4 Informationsmodell trennen

1. Bestehende `ModuleDefinition`-Felder und UI-Verbraucher inventarisieren.
2. Gemeinsame stabile Metadaten, technische Entwicklungsinformationen und
   fachliche Workflowtexte als getrennte Modelle bzw. Adapter definieren.
3. Markdown-Schema validierbar machen und fehlende Inhalte kontrolliert
   anzeigen.
4. Abwaertskompatibilitaet fuer bestehende Katalogverbraucher sichern.

Ergebnis: eine UI-neutrale Datenquelle ohne doppelte manuelle Langtexte.

### P037-S5 Bearbeitungsansicht konsolidieren

1. Vier Prozessbereiche wieder sichtbar machen.
2. Alle Module einschliesslich geplanter oder konzeptioneller Module zeigen.
3. Technische Modulkarte auf Status, aktive Plaene, Architektur,
   Schnittstellen, Tests und Restarbeit begrenzen.
4. Bestehenden Infozugang in `Technische Modulinfo` und `Hilfe zum Ablauf`
   teilen; beide erhalten eindeutige Ruecksprungziele.

Ergebnis: technische Entwicklungsansicht ohne fachliche Paralleltexte.

### P037-S6 Workflowansicht aktualisieren

1. Gesamtuebersicht und Bereichsworkflow aus dem zentralen Katalog ableiten.
2. Workflow-Infokarten aus den Markdown-Steckbriefen rendern.
3. Begriffe, Werte, Datenherkunft, Bedienhinweise, Beispiele und kurze
   Quellenfussnoten anzeigen.
4. Geplante Module sichtbar, aber eindeutig als nicht ausfuehrbar markieren.
5. P027-/UD-114-Navigationsebenen und Korrekturpfade erhalten.

Ergebnis: nutzungsorientierte Hilfe, die keine technische Planansicht
dupliziert.

### P037-S7 Start- und Navigationsverhalten korrigieren

1. Normalstart auf Bearbeitungsansicht setzen.
2. Workflowansicht als bewusste Auswahl erhalten.
3. Projektauswahl ausschliesslich an `Start` innerhalb der Workflowansicht
   binden.
4. Sitzungsentwuerfe, aktive Reiter und Ruecksprungziele bei Navigation
   erhalten.

Ergebnis: reproduzierbares, getestetes Start- und Wechselverhalten.

### P037-S8 Navigator, Dokumentation und Abnahme

1. Navigator um Dokumenthierarchie, Ordneraufgaben, P037 und den fachlichen
   Workflow erweitern.
2. PLAN_INDEX, PLAN_STATUS, Entscheidungen, CHANGELOG und betroffene
   Modul-READMEs synchronisieren.
3. Dokumentlinks, Markdown-Schema, Katalogkonsistenz, beide Kartenarten,
   Prozessgruppierung und Startnavigation automatisiert testen.
4. Vollstaendige relevante Testsuite, Ruff und `git diff --check` ausfuehren.
5. Navigator nach den Dokumentaenderungen aktualisieren und validieren.

Ergebnis: nachvollziehbarer, navigierbarer und regressionsgepruefter Stand.

## Aktive Dreipaketstruktur

Die ursprünglichen Slices S1 bis S8 bleiben als fachliche Arbeitsteilung und
Nachweis erhalten. Für die Freigabe und Umsetzung gelten seit dem 2026-08-13
jedoch nur noch diese drei Pakete:

1. **P037-A – Dokumentationswahrheiten und Workflowquelle (S1–S3):**
   Rollenmatrix, Pflegeorte, zentraler Gesamtworkflow und alle
   Modulsteckbriefe sowie Verweise der führenden READMEs.
2. **P037-B – Informationsmodell und Ansichten (S4–S6):** lesender
   Markdown-Adapter, vier Prozessbereiche, getrennte technische Modulinfo
   und Ablaufhilfe sowie Workflowkarten aus den Steckbriefen.
3. **P037-C – Navigation, Abnahme und Navigator (S7–S8):** Normalstart,
   workflowgebundener Projektstart, Tests, Dokumentationsabgleich und
   Navigator-Aktualisierung.

Archivverschiebungen und -löschungen sind von allen drei Paketen ausdrücklich
ausgenommen.

## Reihenfolge und Freigabegrenzen

P037-S0 ist abgeschlossen. Die verbleibenden Arbeiten wurden in der
Dreipaketstruktur P037-A bis P037-C gemeinsam freigegeben und umgesetzt.
Konkrete Archivverschiebungen bleiben separat freigabepflichtig. Neue
Dependencies, Hook-Aenderungen, externe Verarbeitung und geschuetzte Quellen
sind nicht Teil von P037.

Der in diesem Chat erteilte Schreibumfang dokumentiert den Plan und den
Handover. Fuer die Ausfuehrung von P037 im naechsten Chat ist eine frische,
auf P037 bezogene `Freigabe zur Umsetzung` erforderlich.

## Abnahmekriterien

- Jedes aktuelle Dokument besitzt eine dokumentierte Hauptaufgabe.
- Jedes behandelte Thema besitzt genau eine fuehrende Quelle.
- Navigator und Ordnerbeschreibungen zeigen eindeutig, was wo gepflegt wird.
- Der fachliche Gesamtworkflow deckt alle katalogisierten Module ab.
- Workflowkarten beantworten Nutzungsfragen und enthalten keine aktiven
  Umsetzungsplaene.
- Technische Modulkarten zeigen Entwicklungsstand und nur aktive Plaene.
- Gemeinsame Begriffe und Stammdaten werden nicht widerspruechlich doppelt
  gepflegt.
- Bearbeitungsansicht und Workflowansicht sind in Inhalt, Einstieg und
  Navigation klar getrennt.
- Normalstart, Workflow-Start und Projektauswahl entsprechen dem festgelegten
  Bedienkonzept.
- Archivdokumente bleiben historische Nachweise und werden nicht als aktive
  Wahrheit verwendet.
- Alle relevanten Tests, Link-/Schema-Pruefungen, Ruff, `git diff --check`
  sowie Navigator-Validierung bestehen.

## Abschlussstand

P037-A bis P037-C wurden ohne Archivverschiebungen/-löschungen, neue
Dependencies, Hooks, externe Dienste oder geschützte Inhalte umgesetzt. Die
Abnahme umfasst Modulsteckbriefe, Informationsadapter, UI-Navigation,
fokussierte UI-/Workflowtests, Qualitätsprüfungen und Navigator-Validierung.
