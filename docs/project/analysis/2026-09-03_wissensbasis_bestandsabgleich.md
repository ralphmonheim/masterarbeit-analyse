# Bestandsabgleich der Wissensbasis fuer die KI-gestuetzte Softwareentwicklung

- **Analyse- und Nachweisstand:** 03.09.2026
- **Repositorybasis:** aktueller Git-Index und lokaler Arbeitsbaum auf Branch
  `main`; Referenz-HEAD `5f9c52d20834dc45db42be663a214aae0f74ff6c`
- **Untersuchungsbasis:** aktueller lokaler Projektbestand einschliesslich
  Git-ignorierter Projekt-Inbox, Quellenbestand der getrennten Arbeitsablage
  und vorhandene Quellenregister
- **Arbeitsablage-Alias:** `WORK/01_Quellen` bezeichnet in diesem Bericht den
  Quellenordner der getrennten `260524_Masterarbeit_Arbeitsablage`.

> Dieser Bericht ist eine datierte Bestandsaufnahme, keine Bibliografie, keine
> neue Literaturrecherche und keine Rechtefreigabe. Original-PDFs und Archive
> wurden weder kopiert noch verschoben. Normen und Regelwerke wurden nur anhand
> von Dateimetadaten, relativer Ablage und Pruefsummen erfasst. Vorhandene
> Paketanalysen und KI-Voranalysen gelten als Sekundaerartefakte und nicht als
> unabhaengig verifizierte Quellenaussagen.

## A. Kurzfazit zur Wissensbasis

Der konsolidierte Quellenbestand unter `WORK/01_Quellen` umfasst 325
PDF-Vorkommen. Nach Entfernung exakter Dateidubletten bleiben 270 eindeutige
SHA-256-Objekte. Davon sind 103 direkt abgelegte Normen- und
Regelwerksdateien, die ausschliesslich metadatenbasiert behandelt wurden. Die
222 nichtnormativen PDF-Vorkommen reduzieren sich auf 167 eindeutige
Binärobjekte und nach einem zusaetzlichen Titel-/DOI-Abgleich auf 166 derzeit
belegbare bibliografische Quellen.

Die Zahl 166 beschreibt lokal vorhandene nichtnormative PDF-Quellen, nicht 166
im Audit inhaltlich ausgewertete oder nachweisbar fuer die Entwicklung
verwendete Quellen. Fuer 143 davon melden vorhandene technische
Paketpruefungen maschinenlesbaren Text; bei den uebrigen 23 ist die
Textlesbarkeit nicht einheitlich belegt. Fuer den weit ueberwiegenden
Drittbestand fehlt weiterhin ein objektbezogener Nachweis des zulaessigen
KI-Verarbeitungsumfangs. Deshalb wurden physische Verfuegbarkeit, technische
Lesbarkeit, inhaltliche Freigabe und tatsaechliche Nutzung getrennt bewertet.

Der vollstaendige lokale Projekt-Inbox-Baum enthaelt weitere 151 eindeutige
PDF-Objekte: 142 unter `new`, acht unter `processed` und eines unter
`needs_review`. Sechs stimmen exakt mit Objekten aus `WORK/01_Quellen`
ueberein; 145 Binärobjekte sind gegenueber der Arbeitsablage neu. Darunter
liegen 149 Literatur- oder technische Quellenkandidaten, ein projektinternes
Plandokument und ein Kalender-Datenartefakt. Diese Objekte wurden inventarisiert,
aber nicht automatisch in den konsolidierten Quellenbestand verschoben oder
als inhaltlich gepruefte Literatur eingestuft.

Das staerkste nachweisbar genutzte Wissen ist derzeit die projektinterne
Wissensbasis: 894 versionierte Dateien, darunter 252 Markdown- und 470
Python-Dateien sowie 96 Python-Testdateien. Externe Literatur und Normen sind
im Projekt auf Metadaten- und Planungsebene referenziert; fuer eine konkrete
Uebernahme externer Volltextaussagen in Entscheidungen oder Implementierung
liegt kein belastbarer Nachweis vor.

## B. Bestand und Zugaenglichkeit der Quellen

### B.1 Untersuchte Bestaende

| Bestand | Ergebnis | Zugriffs- und Auswertungsstatus |
|---|---:|---|
| Versioniertes Repository | 894 Dateien | Code, Tests und Projektdokumentation lesbar |
| `WORK/01_Quellen`, direkte PDFs | 127 | 103 Norm-/Regelwerksdateien; 24 sonstige PDFs |
| `WORK/01_Quellen`, archivierte PDFs | 198 Vorkommen | 100 in Literaturarchiven; 98 in verschachtelten Konferenzarchiven |
| `WORK/01_Quellen`, ZIP-Dateien | 15 direkt, 16 eingebettet | rekursiv bis zu den eingebetteten Konferenz-ZIPs erfasst |
| Projekt-Inbox, alle Stufen | 151 PDF-Objekte | Metadaten-/Hashpruefung; 145 gegenueber `WORK` neu |
| Internes Quellenregister | 21 Metadatensaetze | `user-described`, `requires_manual_review`, keine Quelle `citation_ready` |

Die drei versionierten PDFs des Repositorys sind projektgenerierte
Diagramm-/Workflowartefakte. Sie sind keine externe Fachliteratur. Im
Repository ist kein externes Literatur- oder Norm-PDF versioniert.

### B.2 Transparente Zaehlweise

Die Auswertung unterscheidet fuenf Ebenen:

1. **PDF-Vorkommen:** Jede direkte Datei und jedes PDF-Mitglied eines Archivs
   wird an seinem Ablageort gezaehlt.
2. **Binär eindeutiges Objekt:** Identische Bytes werden anhand von SHA-256
   zusammengefuehrt.
3. **Bibliografische Quelle/Ausgabe:** Nicht identische Dateien werden ueber
   normalisierten Titel, DOI, Autor, Jahr und Ausgabe abgeglichen.
4. **Dokumentfamilie:** Verschiedene Ausgaben, Normteile, Beiblaetter und
   Berichtigungen bleiben als eigene Manifestationen erhalten, werden aber
   einer Familie zugeordnet.
5. **Nutzung:** Verfuegbarkeit, Referenzierung und konkrete Verwendung werden
   unabhaengig von der Dateizaehlung bewertet.

ZIP-Dateien, Indizes, extrahierte Texte, Analysen, Vorschaubilder und
Pruefsummenlisten sind Container oder Derivate und keine zusaetzlichen
externen Quellen. Eine Dublettenbeziehung ist zudem kein eigener
Zugangsstatus: Eine Mehrfachablage kann zugleich einen lokal vorhandenen
Volltext repraesentieren.

### B.3 Direkte PDFs gegenueber Archiv-PDFs

| Ebene in `WORK/01_Quellen` | PDF-Vorkommen | eindeutige SHA-256 | Bemerkung |
|---|---:|---:|---|
| direkte Norm-/Regelwerksdateien | 103 | 103 | Inhalt nicht geoeffnet oder analysiert |
| direkte sonstige PDFs | 24 | 24 | 8 Leitfaeden, 5 Praesentationen, 11 wissenschaftliche Arbeiten |
| PDFs in Literaturarchiven | 100 | 60 | starke Mehrfachablage zwischen Gesamt- und Teilpaketen |
| PDFs in verschachtelten Konferenzarchiven | 98 | 98 | 16 eingebettete ZIPs rekursiv beruecksichtigt |
| archivierte PDFs insgesamt | 198 | 157 | eine exakte Ueberschneidung zwischen Literatur- und Konferenzkorpus |
| Gesamtbestand | 325 | 270 | 14 direkte/archivierte Ueberschneidungen; 55 entfernte Mehrfachvorkommen |

Fuer die nichtnormativen Quellen gilt reproduzierbar:

`24 direkte + 157 archivierte - 14 direkte/archivierte Ueberschneidungen = 167 Binärobjekte`.

Ein ScienceDirect-PDF und der Datensatz `A01` bezeichnen nach Titel und DOI
dieselbe Publikation, besitzen aber unterschiedliche Bytes. Nach dieser
bibliografischen Zusammenfuehrung verbleiben 166 nichtnormative Quellen.

### B.4 Zugaenglichkeitsklassen des konsolidierten WORK-Bestands

Die Klassen A bis D gelten hier fuer nichtnormative Quellenrecords. Normen
werden wegen der verbindlichen Inhaltsgrenze separat ausgewiesen.

| Klasse | Bedeutung | bereinigter Befund |
|---|---|---:|
| A | lokales PDF und positiver technischer Nachweis fuer maschinenlesbaren Text | 143 bibliografische Quellen |
| A0, nicht als A gezaehlt | lokales PDF nachgewiesen, aber Textlesbarkeit nur eingeschraenkt oder nicht einheitlich belegt | 23 bibliografische Quellen |
| B | bibliografische Metadaten, aber kein bestaetigtes lokales PDF und kein belastbarer externer Volltextzugang | 37 Records |
| C | externer Quellen-/Beschaffungsverweis, aber kein lokales PDF | 35 Records |
| D | Quelle weder identifizierbar noch technisch zugaenglich | 0 bestaetigte Literaturrecords; ein PDF-loses Inbox-Archiv ist technisch defekt |
| E | Dublette/Mehrfachablage | 55 exakte Mehrfachvorkommen im WORK-Gesamtbestand; zusaetzlich eine bibliografische Nicht-Byte-Dublette |

Die Klasse A wird nicht pauschal mit „inhaltlich gelesen“ gleichgesetzt. Die 143
technisch gestuetzten Records ergeben sich aus 96 Konferenzdokumenten mit
guter Textqualitaet und 47 Hauptkorpus-PDFs mit Textnachweis auf der ersten
Seite. Zwei Konferenzdokumente sind nur als eingeschraenkt textlesbar
klassifiziert; bei einem Hauptkorpus-PDF fehlt Text auf der ersten Seite. Fuer
die weiteren lokalen Sammlungen liegt kein einheitlicher technischer
Textqualitaetsnachweis vor. Keine dieser technischen Klassen ist ein
Rechte-, Inhalts- oder Nutzungsnachweis.

Die 72 Records der Klassen B und C entstehen aus 74 Paketrecords ohne
beigefuegtes PDF abzueglich zweier bestaetigter Querverweise auf bereits lokal
vorhandene Quellen. Ein dritter als `existing` markierter Software-Record ist
nicht eindeutig auf eine konkrete lokale Datei aufgeloest und bleibt Klasse B.

### B.5 Projekt-Inbox als getrennte Kandidatenschicht

| Inbox-Stufe | PDF-Vorkommen | eindeutige SHA-256 | Einordnung |
|---|---:|---:|---|
| `new` | 142 | 142 | 24 direkte PDFs und 118 PDFs in vier Literaturarchiven |
| `processed` | 8 | 8 | 7 PDFs in einem Literaturpaket und 1 internes Plandokument |
| `needs_review` | 1 | 1 | Kalender-/Feiertags-Datenartefakt |
| gesamt | 151 | 151 | keine exakte Inbox-interne Dublette |
| davon bereits in `WORK` | 6 | 6 | nicht erneut als neue Quelle zu zaehlen |
| gegenueber `WORK` neu | 145 | 145 | bibliografische Bereinigung und Einzelrechtepruefung noch offen |

Die vier PDF-haltigen ZIPs unter `new` enthalten sieben K04-Dokumente und 111
ScienceDirect-PDFs. Fuenf weitere gueltige ZIPs enthalten keine PDFs; das
Archiv `IDA_ICE_Annotations_Handover.zip` ist technisch kein gueltiges ZIP.
Der Fehler betrifft kein nachweisbares PDF-Vorkommen. Mindestens sechs direkt
abgelegte Inbox-PDFs sind am Dateinamen als DIN-/VDI-Dokumente erkennbar und
bleiben ohne Inhaltszugriff. Weitere Leitfaeden, gesetzliche Texte und
Regelwerksnahe Dokumente muessen bei der Einzelaufnahme ebenfalls konservativ
klassifiziert werden.

Die sechs exakten WORK-/Inbox-Ueberschneidungen betreffen:

- zwei Nachhaltigkeits-/BIM2SIM-Dokumente,
- einen Leitfaden zum wissenschaftlichen Arbeiten mit generativer KI,
- ein BauSIM-Konferenzpaper,
- einen Leitfaden zur DIN-V-18599-Bilanzierung und
- ein Paper zur Zonierungsstrategie.

## C. Abgeleitete Wissensbereiche

Die Bereiche wurden aus Dokumenttypen, Titeln, Paketkategorien und
projektinternen Modulbeziehungen abgeleitet. Die Themenzaehlungen sind
Mehrfachzuordnungen und daher nicht addierbar.

- Gebaeudeenergie- und Gebaeudeperformance-Simulation
- BIM/BEM, IFC, Interoperabilitaet und automatisierte Modellbildung
- Bauphysik, thermischer Komfort und Zonierung
- TGA, HVAC, Heiz-/Kuehllast, Regelung und Dimensionierung
- Wetter-, Klima-, Zeitreihen- und Sensitivitaetsdaten
- Optimierung, Validierung, Unsicherheit und Post-Processing
- Nachhaltigkeit, Lebenszyklusbezug, Dekarbonisierung und Energiesysteme
- technische Simulationswerkzeuge, Modelica, EnergyPlus und IDA ICE
- Python, Datenmodelle, Datenverarbeitung und Softwarequalitaet
- KI/LLM, Coding Agents und agentische Softwareentwicklung
- wissenschaftliches Schreiben, Zitieren und KI-Nutzung in Hochschularbeiten
- Normen, Richtlinien, Gesetze und technische Regelwerke
- Projektarchitektur, Workflows, Entscheidungen, Planung, Git und Tests

Im Konferenzindex sind beispielsweise 24 Dokumente mit BIM/IFC, 22 mit
HVAC-Systemen, je 21 mit Workflowautomatisierung beziehungsweise
Wetter/Klima, 15 mit Regelung, 15 mit Surrogatmodellen/ML/AI, 14 mit
Optimierung und zehn mit Komfort/Innenraumqualitaet verschlagwortet. Diese
Werte stammen aus vorhandenen Paketmetadaten und sind keine unabhaengige
inhaltliche Neubewertung der Volltexte.

## D. Fachliteratur und wissenschaftliche Quellen

### D.1 Konsolidierter Literaturkorpus

Die 166 bibliografisch bereinigten nichtnormativen WORK-Quellen lassen sich
ueber ihre primaeren Sammlungen nachvollziehen:

| Sammlung | bibliografische PDF-Quellen | Abgrenzung |
|---|---:|---|
| Konferenzkorpus | 98 | 98 eindeutige PDF-Objekte |
| Haupt-Literaturpaket | 48 | lokale Records des 74er-Indexes |
| Nachhaltigkeit/BIM2SIM | 8 | eine Quelle zugleich im Konferenzkorpus |
| Softwaregrundlagen | 3 | drei tatsaechlich beigefuegte PDFs |
| direkte Leitfaeden | 8 | keine exakte Ueberschneidung mit WORK-Archiven |
| zusaetzliche direkte Fachquellen | 2 | zwei nicht bereits archivierte Einzeldokumente |
| Summe nach Dublettenbereinigung | 166 | `98 + 48 + 8 + 3 + 8 + 2 - 1` |

Der 74er-Hauptindex umfasst 48 lokale PDFs und 26 reine
Metadaten-/Beschaffungsrecords. Bei den lokalen PDFs dominieren 16
Energiesystem-Fachartikel, sechs Forschungsberichte, drei Dissertationen,
drei JRC-Berichte, zwei weitere Fachartikel, zwei Validierungsberichte und
zwei Konferenzpaper. Die restlichen 14 Records verteilen sich auf Reviews,
Fachbuch-/Vorschaumaterial, Roadmaps, Leitfaeden, Tutorials und
Praesentationsmaterial. Diese Typisierung stammt aus dem Paketindex.

Der Konferenzbestand enthaelt 98 lokale Dokumente sowie 36 fehlende oder nur
bibliografisch erfasste Beitraege. Die vorhandenen Validierungsdaten des
Pakets melden 98 von 98 PDFs als gueltig und unverschluesselt, davon 96 mit
guter und zwei mit eingeschraenkter Textqualitaet. Dieser Befund wurde als
Paketmetadatum uebernommen und nicht durch eine erneute Volltextpruefung aller
98 Dokumente ersetzt.

Auch die Validierungsdaten des Haupt-Literaturpakets melden alle 48 lokalen
PDFs als gueltig und unverschluesselt. Bei 47 ist Text auf der ersten Seite
verzeichnet; bei einem Dokument nicht. Das ist ein technischer Paketnachweis,
keine erneute inhaltliche Pruefung oder Rechtefreigabe.

### D.2 Fachliche Tragfaehigkeit

Die Metadaten zeigen eine breite Grundlage fuer Stand der Technik,
Workflowgestaltung, Interoperabilitaet, Modellierungsvarianten,
Ergebnisanalyse, Optimierung und Validierung des Softwareprototyps. Sie koennen
grundsaetzlich Entscheidungen zu Import-/Exportgrenzen, Simulationsmodellen,
Zonenbildung, KPI-Auswahl, Variantenstudien und Ergebnisinterpretation
unterstuetzen.

Nicht belastbar sind derzeit konkrete Methoden-, Kennwert-, Schwellen- oder
Wirkungsbehauptungen aus dem Korpus. Dafuer fehlen quellenweise dokumentierte
Rechtepruefung, manuelle Fundstellenkontrolle und ein Nachweis, dass die
jeweilige Aussage tatsaechlich in die Entwicklung eingeflossen ist.

## E. Normen und Regelwerke

Unter `WORK/01_Quellen/Normen` liegen 103 physische PDF-Dateien mit 103
unterschiedlichen SHA-256-Pruefsummen. Sie wurden nicht inhaltlich geoeffnet,
extrahiert, verglichen oder analysiert. Fuer die Wissensbilanz gilt daher:

- Normen-/Regelwerksdateien physisch nachgewiesen: **103**
- inhaltlich zugaengliche beziehungsweise ausgewertete Normen: **0**
- Metadaten-Dateirecords des physischen Bestands: **103**
- bibliografisch unterschiedliche Dokument-/Ausgabe-Manifestationen: **102**
- Records im versionierten Normmetadatenregister: **102**
- eindeutige Dokument-/Ausgabe-Schluessel im Register: **101**

Die Differenz entsteht durch zwei Befunde: `DIN-TS 18599 Beiblatt 3`, Ausgabe
2021-09, liegt in zwei Ordnern und in zwei binär unterschiedlichen Dateien
vor, repraesentiert bibliografisch aber dieselbe Ausgabe. Umgekehrt fehlt fuer
die physisch vorhandene `DIN EN ISO 7817-1`, Ausgabe 2024-11, ein Record im
versionierten Metadatenregister.

| Registergruppe | Metadatenrecords |
|---|---:|
| DIN/TS 18599, aktuell | 13 |
| DIN/V/TS 18599, historisch | 15 |
| DIN 276 | 1 |
| DIN 4108 | 10 |
| DIN EN 12831 | 3 |
| weitere DIN-EN-Bau-/Nachhaltigkeitsdokumente | 8 |
| DIN EN 16798 | 10 |
| DIN EN ISO | 18 |
| VDI 2067 | 9 |
| weitere VDI-Dokumente | 10 |
| weitere Quelldokumente im Regelwerksordner | 5 |
| Summe | 102 |

Die Ordnergruppe enthaelt neben Normen im engen Sinn auch Gesetze,
Verordnungen, Broschueren und Leitfaeden. Die korrekte Sammelbezeichnung ist
daher **Normen- und Regelwerksdateien**, nicht 103 Normvolltexte. Das
versionierte Register dient nach eigener Zweckangabe nur als Locator und
darf weder als Runtime-Input noch als Quelle fuer fachliche PASS/FAIL-Regeln
verwendet werden.

## F. Technische und IDA-ICE-Dokumentationen

Der konsolidierte Literaturindex weist eine lokale technische
Softwaredokumentation als PDF aus: ein Modelica-Buildings-Tutorial. Zehn
weitere technische Records (`F01` bis `F10`) verweisen auf EnergyPlus,
Modelica/AixLib, buildingSMART IDS, Standard-209-Ressourcen sowie IDA ICE,
ohne dem Paket lokale PDFs beizufuegen. Diese zehn Records sind externe
Referenzen, keine gelesenen Dokumentationen.

Fuer IDA ICE bestehen zwei explizite externe Metadatenreferenzen (`F09` und
`F10`) und **keine** als externer IDA-Volltext verifizierte PDF-Quelle. Im
Repository existieren zwei dedizierte projektinterne IDA-Dokumente:

- `docs/ida_ice/README.md`
- `docs/project/workflow/modules/ida_ice.md`

Sie dokumentieren die projektspezifische Schnittstelle und den manuellen
MainProcess, sind aber keine Herstellerdokumentation. P036 schliesst
IDA-Modell-/Bibliotheksinhalte fuer den betrachteten Umsetzungsslice
ausdruecklich aus.

In der Projekt-Inbox liegen zusaetzliche Hersteller-, Waermepumpen-,
U-Wert- und Rechenleitfaeden. Sie sind als Aufnahmekandidaten nachgewiesen,
aber weder bibliografisch konsolidiert noch rechtebezogen inhaltlich
freigegeben. Die beiden IDA-Annotationsarchive enthalten keine PDFs; eines
davon ist technisch defekt.

## G. Software-, KI-, Agenten- und Skill-Wissen

Das Softwaregrundlagenpaket fuehrt 15 Referenzen:

- drei im Paket vorhandene PDFs zu robuster Forschungssoftware, SWE-agent und
  OpenHands,
- zwei bestaetigte Querverweise auf bereits lokal vorhandene Quellen,
- einen weiteren, noch nicht auf eine konkrete Datei aufgeloesten
  `existing`-Record und
- neun externe Referenzen, darunter Python-, Packaging-, VS-Code-,
  SWEBOK-, Teststandard- und Agent-Skill-Quellen.

Die direkte Leitfadensammlung enthaelt nach Titel- und Dateimetadaten acht
PDFs zu wissenschaftlichem Arbeiten, generativer KI, Zitieren,
Normungs-/KI-Fragen und einem BIM-Workshop. Fuer diese Gruppe wird im Bericht
nur die lokale Datei- und Hashverfuegbarkeit, nicht extrahierter Text oder
eine inhaltliche Auswertung als Evidenz verwendet.

Im Repository ist Softwarewissen unmittelbar in Code und Tests nachweisbar:

- 470 Python-Dateien,
- 96 Python-Testdateien,
- elf deklarierte Laufzeitabhaengigkeiten und drei Entwicklungswerkzeuge in
  `pyproject.toml`,
- vier projektlokale Skills,
- versionierte Agentenrollen, Freigabe- und Council-Vertraege sowie
- automatisierte Tests fuer Agentenrollen, Skill-Router und Governance-Gates.

Die Abhaengigkeitsdeklaration und Importe belegen die Verwendung der
Bibliotheken im Softwareprojekt. Sie belegen nicht, welche externe
Python-/API-Dokumentation historisch gelesen wurde.

## H. Projektinterne Wissensbasis

### H.1 Quantitativer Bestand

| Projektwissen | aktueller Bestand | Einordnung |
|---|---:|---|
| versionierte Dateien insgesamt | 894 | primaere technische Bestandsbasis |
| Markdown-Dokumente | 252 | Dokumentation, Planung, Entscheidungen und Historie |
| Python-Dateien | 470 | Implementierungswissen einschliesslich Tests |
| Python-Testdateien unter `tests/` | 96 | ausfuehrbare Qualitaets- und Vertragsnachweise |
| README-Dateien | 64 | Modul-, Ordner- und Bedienwissen |
| Plan-Markdowns | 42 | aktive, vorbereitete und historische Planung |
| Entscheidungs-Markdowns | 9 | Nutzer- und Architekturentscheidungen |
| Workflow-Markdowns | 32 | fachlicher Gesamtworkflow und Modulsteckbriefe |
| Markdown-Dokumente mit `handover` im Pfad oder Dateinamen | 41 | vorwiegend historische Uebergaben |
| Wochenreviews | 7 | zeitgebundene Statusnachweise |
| Prompts | 4 | wiederverwendbare Arbeits- und Qualitaetsvertraege |
| projektlokale Skills | 4 | aktive Router fuer Projektablaeufe |

Die Untergruppen der Markdown-Dokumente ueberlappen und duerfen nicht zur Zahl
252 addiert werden. Die Kennzahlen stammen aus `git ls-files` zu Beginn des
Audits und beziehen damit den damaligen Git-Index ein; der neu erstellte,
zu diesem Zeitpunkt noch unversionierte Auditbericht selbst ist in 894 nicht
enthalten. Der angegebene HEAD dient nur als Referenz fuer den Ausgangspunkt
des lokalen Arbeitsstands.

### H.2 Wiederverwendbares und historisches Wissen

Als aktuell wiederverwendbar gelten insbesondere:

- Quellcode, Tests und Konfiguration als aktueller technischer Bestand,
- fuehrende Gesamtplaene und ausdrueckliche Nutzerentscheidungen,
- `PLAN_INDEX.md`, `PLAN_STATUS.md` und `UPDATE_ROUTINES.md`,
- der fachliche Gesamtworkflow und die Modulsteckbriefe,
- aktuelle Modul-READMEs, Architekturvertraege und Datenmodelle,
- aktive Skills, Agentendefinitionen und ihre Tests.

Handovers, archivierte Plaene, Wochenreviews und alte Chatrekonstruktionen sind
wichtige Provenienz. Sie werden jedoch nicht ohne Abgleich mit den fuehrenden
aktuellen Wahrheiten als gegenwaertige Projektanweisung behandelt.

## I. Nachweisbare Nutzung der Wissensquellen

Fuer die Nutzungsevidenz gelten vier Stufen:

| Stufe | Bedeutung |
|---|---|
| U0 | vorhanden, aber keine Verwendung nachweisbar |
| U1 | bibliografisch, als Paket oder in Planung/Metadaten referenziert |
| U2 | projektintern verarbeitet oder in Implementierung/Entscheidung nachweisbar verwendet |
| U3 | konkrete externe Volltextaussage nachweisbar in Entscheidung, Methode oder Implementierung uebernommen |

| Wissensgruppe | Stufe | Beleg und Grenze |
|---|---|---|
| Literaturpakete | U1 | P019 fuehrt sie als internes Metadatenregister; konkrete Quellenaussagen bleiben offen |
| Normen/Regelwerke | U1 | P020 verwendet den Metadaten-Locator und schliesst Normwerte, Formeln und Regeln aus |
| Sensitivitaetsliteratur | U1 | P021 nennt einzelne Quellen nur zur Metadaten-/Methodikzuordnung; Schwellenwerte bleiben offen |
| P036-Literaturbezug | U1 | der Plan dokumentiert ausdruecklich, dass das Literaturpaket im Slice nicht geoeffnet wurde |
| Projektinterne Daten und Dokumente | U2 | PRN-/Excel-Rollen, Workflows, Plaene, Entscheidungen und Tests sind konkret umgesetzt oder geprueft |
| Python-Bibliotheken | U2 fuer Implementierung, U0/U1 fuer externe Dokumentation | Manifest, Importe und Code belegen Bibliotheksnutzung, nicht gelesene Dokumentationsseiten |
| Agenten und Skills | U2 | Agentenrollen, Router und Freigabegates sind versioniert und automatisiert getestet |
| externe Volltextaussagen | U3 = 0 belegt | keine belastbare Rueckverfolgung von Quellenaussage zu Implementierung oder Fachentscheidung |

Zentrale Evidenz:

- `docs/project/plans/inbox/260622_Plan_P019_Stage2_Optimierung.md`
- `docs/project/plans/inbox/260622_Plan_P020_Stage3_Standards_Verification.md`
- `docs/project/plans/inbox/260622_Plan_P021_Stage4_Sensitivitaet.md`
- `docs/project/plans/inbox/260813_Plan_P036_ma_data_preparation_Analyseausbau.md`
- `data/common/normen/source_inventory_metadata.yaml`
- `pyproject.toml`
- `tests/test_project_agent_system.py`
- `docs/project/decisions/TECHNICAL_DECISIONS.md`

## J. Empfohlene Tabelle fuer Kapitel 5.3

| Wissensbereich | Umfang |
|---|---|
| Fach- und Forschungsliteratur | 166 bibliografisch bereinigte, lokal vorhandene nichtnormative PDF-Quellen im konsolidierten WORK-Bestand; fuer 143 liegt ein technischer Paketnachweis maschinenlesbaren Texts vor; inhaltliche Nutzung nicht pauschal belegt |
| Metadaten- und Beschaffungsbestand | 37 reine Metadatenrecords und 35 externe Referenzen ohne bestaetigtes lokales PDF |
| Normen und Regelwerke | 103 lokal nachgewiesene Dateien beziehungsweise 102 bibliografische Dokument-/Ausgabe-Manifestationen; 0 inhaltlich ausgewertet |
| Technische Simulationsdokumentation | 1 lokales Tutorial-PDF und 10 externe technische Referenzen; davon 2 IDA-ICE-Metadatenreferenzen, 0 verifizierte externe IDA-Volltexte |
| Software, KI und agentische Entwicklung | 3 lokale Forschungssoftware-/Agenten-PDFs, 8 direkte Leitfaeden sowie projektintern 470 Python- und 96 Testdateien und 4 Skills |
| Projektinterne Wissensbasis | 252 Markdown-Dokumente, darunter 64 READMEs, 42 Plan-, 9 Entscheidungs- und 32 Workflowdokumente; Untergruppen nicht additiv |
| Noch nicht konsolidierte Projekt-Inbox | 151 eindeutige PDF-Objekte, davon 6 bereits in WORK und 145 binär neu; bibliografische und rechtliche Einzelpruefung offen |

Empfohlene Fussnote fuer den Haupttext:

> Umfang nach Bestandsstand 03.09.2026; exakte Dateidubletten per SHA-256
> bereinigt, nicht binär identische Titel-/DOI-Dubletten zusaetzlich
> zusammengefuehrt und unterschiedliche Ausgaben getrennt gefuehrt.
> Themenzuordnungen koennen sich ueberlappen. Normen und Regelwerke wurden
> ausschliesslich metadatenbasiert erfasst und nicht inhaltlich ausgewertet.
> Verfuegbarkeit ist kein Nachweis tatsaechlicher Entwicklungsnutzung.

## K. Erweiterte Tabelle fuer den Anhang

| Wissensbereich | eindeutige Volltextquellen | reine Metadatensaetze | projektinterne Dokumente | nachweisbare Verwendung | zentrale Inhalte | Evidenz |
|---|---:|---:|---:|---|---|---|
| Gebaeude-/Energiesimulation, BIM/BEM und TGA im Konferenzkorpus | 98 lokal vorhandene PDF-Quellen; 96 mit guter, 2 mit eingeschraenkter Textqualitaet laut Paketpruefung | 36 | 0 | U1 | BIM/IFC, HVAC, Automatisierung, Wetter/Klima, Regelung, Optimierung, Komfort; Paket-Tags nicht additiv | Konferenz-Masterindex, rekursive ZIP- und Hashpruefung |
| Hauptkorpus Bau-/Energiesimulation und Energiesysteme | 48 lokal vorhandene PDF-Quellen; 47 mit Textnachweis auf Seite 1, 1 ohne diesen Nachweis | 26 externe Records | 0 | U1 | Simulation, Interoperabilitaet, Modellierung, Validierung, Energie- und Flexibilitaetsthemen | 74er-Dokumentindex und PDF-Manifeste |
| Nachhaltigkeit und BIM2SIM-Prozess | 8 lokal vorhandene PDF-Quellen, davon 1 Dublette zum Konferenzkorpus; kein einheitlicher Textqualitaetsnachweis | 0 | 0 | U0/U1 | digitale Prozessintegration, Nachhaltigkeit/LCA, BIM2SIM und Surrogatmodelle auf Metadatenebene | `documents_index.json`, `source_relationships.json`, SHA-256 |
| Forschungssoftware und Coding Agents | 3 lokal vorhandene PDF-Quellen; kein einheitlicher Textqualitaetsnachweis | 1 unaufgeloester lokaler Pointer und 9 externe Referenzen; 2 weitere Pointer lokal aufgeloest | 4 Skills sowie Agenten-/Testartefakte | externe Quellen U0/U1; Projektvertraege U2 | robuste Forschungssoftware, SWE-agent, OpenHands, Python/Packaging, Skill-Benchmarks | Softwarepaket-`sources.csv`, `pyproject.toml`, `tests/test_project_agent_system.py` |
| Wissenschaftliches Arbeiten und KI-Leitfaeden | 8 lokal vorhandene PDF-Quellen; Textqualitaet nicht als Evidenz verwendet | 0 | 4 Projektprompts | U0/U1, Projektprompts U2 | wissenschaftliches Schreiben, Zitieren, generative KI und Normungsfragen | direkte PDF-/Hashinventur, `docs/prompts/` |
| Zusaetzliche direkte wissenschaftliche Einzeldokumente | 2 lokal vorhandene PDF-Quellen; Textqualitaet nicht als Evidenz verwendet | 0 | 0 | U0 | dynamische thermische Simulation und Sensitivitaets-/Quartierssimulation nach Titelmetadaten | direkter Hashabgleich gegen alle Archive |
| Normen und Regelwerke | 0 | 103 physische Dateirecords; 102 bibliografische Manifestationen | 1 versioniertes Normmetadatenregister | U1 nur auf Metadatenebene | DIN-/VDI-Familien, Gesetze, Verordnungen und Leitfaeden; keine Norminhalte | `data/common/normen/source_inventory_metadata.yaml`, Pfad-/Hashpruefung |
| Technische Simulations- und IDA-Dokumentation | 1 lokales Modelica-Tutorial im Hauptkorpus | 10 externe technische Referenzen, davon 2 zu IDA ICE | 2 dedizierte IDA-Dokumente | extern U0/U1; Projektworkflow U2 | Werkzeug-/Schnittstellenbezug; manueller IDA-MainProcess | Hauptindex F01-F10, `docs/ida_ice/README.md`, Workflowsteckbrief |
| Lokales Simulationsstufen-Register | 7 PDFs im zugehoerigen Inbox-Paket, noch nicht als Inhaltswissen freigegeben | 21 user-described Records insgesamt | Register-README und 21 interne Analyse-Metadateien | U1 | Simulationsstufen, Optimierung, Sensitivitaet und offene Beschaffung | `config/ma_database/literature/README.md`, Inbox-Paketmanifest |
| Weitere Projekt-Inbox-Kandidaten | 142 PDFs unter `new`; bibliografische Eindeutigkeit offen | nicht abschliessend bestimmt | 1 internes Plandokument und 1 Kalender-Datenartefakt ausserhalb der Literaturzaehlung | U0 | ScienceDirect-Korpus, K04-Zonierung/Sonnenschutz, Norm-/VDI-Kandidaten, Hersteller- und Nachhaltigkeitsdokumente | rekursive Inbox-Inventur und WORK-/Inbox-Hashabgleich |
| Projektarchitektur, Workflows und Entscheidungen | nicht als externe Volltextquellen gezaehlt | 0 | 252 Markdown-Dokumente insgesamt; darunter 64 READMEs, 42 Plaene, 9 Entscheidungen und 32 Workflowdokumente | U2 fuer aktuelle kanonische Dokumente | Architektur, Module, Datenfluesse, Governance, Freigaben und Status | `git ls-files`, fuehrende Projektwahrheiten und Tests |
| Implementierung, Datenverarbeitung und Qualitaet | nicht als externe Volltextquellen gezaehlt | 0 | 470 Python-Dateien, davon 96 Tests | U2 | Import, Verarbeitung, Analyse, UI, Datenmodelle, Tests und Qualitaetsgates | Quellcode, `pyproject.toml`, Testbestand |

Die Spalte „eindeutige Volltextquellen“ weist deshalb sowohl die lokale
PDF-Verfuegbarkeit als auch den jeweils belegbaren technischen
Textlesbarkeitsstatus aus. Nur 143 Quellen besitzen im aktuellen Nachweisstand
einen positiven Maschinenlesbarkeitsnachweis. Keine Angabe bedeutet
automatisch rechtegeprueft, im Audit semantisch gelesen, `citation_ready` oder
fuer eine konkrete Implementierungsentscheidung verwendet.

## L. Nicht belastbar quantifizierbare oder nicht zugaengliche Bestaende

Folgende Aussagen sind mit dem aktuellen Nachweisstand nicht belastbar:

- wie viele der 145 gegenueber WORK neuen Inbox-Objekte nach vollstaendiger
  Titel-/DOI-/Ausgabenpruefung bibliografisch eindeutig bleiben,
- welche geschuetzten oder lizenzierten Drittquellen objektbezogen fuer eine
  KI-Volltextverarbeitung freigegeben sind,
- ob alle von Paketindizes als lesbar bezeichneten PDFs unabhaengig dieselbe
  Textqualitaet aufweisen,
- ob als `existing` markierte, aber nicht auf eine konkrete Datei abgebildete
  Records tatsaechlich lokal vorhanden sind,
- welche Quellen zu einem historischen Zeitpunkt der Entwicklung bereits
  vorhanden waren; der aktuelle Bestand belegt keine rueckwirkende
  Verfuegbarkeit,
- welche konkrete externe Quellenaussage eine Entscheidung oder Codezeile
  verursacht hat,
- ob inhaltlich aehnliche Handovers oder Dokumentversionen ohne identische
  Bytes als vollstaendige oder nur teilweise Dubletten gelten,
- der Inhalt des technisch defekten, PDF-losen
  `IDA_ICE_Annotations_Handover.zip`,
- externe Webinhalte hinter Referenzen, da keine Internetrecherche Teil des
  Auftrags war.

Auch die vorhandenen extrahierten Texte, Markdown-Analysen und
KI-Voranalysen in Literaturpaketen wurden nicht als neue Quellen oder als
verifizierte Aussagen gezaehlt. Sie koennen erst nach quellenweiser
Rechtepruefung und Originalabgleich als Arbeitsnotiz verwendet werden.

## M. Abschliessende Bewertung

Die Wissensbasis ist quantitativ breit und strukturell gut auffindbar. Der
konsolidierte WORK-Bestand deckt Gebaeudesimulation, BIM/BEM, TGA,
Optimierung, Validierung, Nachhaltigkeit, Energiesysteme, Softwareentwicklung
und agentische KI ab. Die rekursive Archivpruefung und SHA-256-Bereinigung
verhindern, dass Gesamtpakete, Teilpakete und direkte Kopien mehrfach als
Quellen gezaehlt werden. Die Projekt-Inbox erweitert den potentiellen Bestand
erheblich, ist aber noch keine konsolidierte Wissensbasis.

Qualitativ ist die projektinterne Wissensbasis derzeit belastbarer als die
externe Fachquellennutzung: Code, Tests, Architektur, Workflows, Plaene,
Entscheidungen, Skills und Agentenvertraege sind konkret im Projekt vorhanden
und teilweise automatisiert geprueft. Bei externer Literatur sind
Verfuegbarkeit und thematische Relevanz gut dokumentiert, konkrete
Fundstellen, Rechteumfang, Zitationsreife und Entwicklungswirkung jedoch
ueberwiegend offen. Bei Normen ist die Grenze eindeutig: 103 Dateien sind
lokal nachgewiesen, aber null Normvolltexte wurden inhaltlich ausgewertet.

Fuer Kapitel 5.3 ist deshalb eine kompakte, statusbewusste Darstellung
vertretbar. Sie sollte die 166 konsolidierten nichtnormativen PDF-Quellen, den
getrennten Metadatenbestand, die rein metadatenbasierte Normensammlung und die
starke projektinterne Dokumentationsbasis nennen. Sie darf daraus weder eine
vollstaendige Literaturauswertung noch einen kausalen Nachweis ableiten, dass
die KI alle vorhandenen Quellen tatsaechlich fuer die Softwareentwicklung
verwendet hat.

## Qualitaetspruefung

- [x] Volltextbestand, Metadaten, externe Verweise und unzugaengliche Objekte getrennt
- [x] direkte PDFs und Archiv-PDFs separat ausgewiesen
- [x] verschachtelte ZIPs rekursiv beruecksichtigt
- [x] exakte Dubletten per SHA-256 bereinigt
- [x] eine nicht binär identische bibliografische Dublette zusaetzlich zusammengefuehrt
- [x] Verfuegbarkeit und tatsaechliche Nutzung getrennt
- [x] Normen und Regelwerke nur metadatenbasiert behandelt
- [x] Projektwissen und externe Fachquellen getrennt
- [x] Inbox-Kandidaten nicht stillschweigend in den konsolidierten Bestand uebernommen
- [x] keine Internetrecherche und keine neu erfundenen Quellen
- [x] keine Originaldatei kopiert, verschoben oder veraendert
