# Masterarbeit Leitfaden

Leitfaden-Version: 0.5.6
Stand: 2026-06-29

Diese Datei ist der zentrale Orientierungsleitfaden fuer die Masterarbeit und
die begleitende Software. Sie ersetzt keine aktive Steuerdatei. Der operative
Projektstand bleibt in `docs/project/plans/PLAN_STATUS.md`; die Zielarchitektur
bleibt in `docs/project/architecture/TARGET_ARCHITECTURE.md`.

Der Leitfaden fuehrt zwei Quellen zusammen:

- `docs/project/archive/leitfaeden/MASTERARBEIT_LEITFADEN_v0.1.0_codex_2026-06-17.md`
- `docs/project/archive/leitfaeden/MASTERARBEIT_LEITFADEN_v0.2.0_chatgpt_2026-06-18.md`

**Versionshistorie**

| Version | Datum | Bedeutung |
|---|---|---|
| 0.1.0 | 2026-06-17 | Erste Codex-Fassung auf Basis des aktuellen VS-Code-Projektstands |
| 0.2.0 | 2026-06-18 | Externe ChatGPT-Referenzfassung |
| 0.3.0 | 2026-06-18 | Zusammengefuehrte aktive Fassung mit aktueller Modulentscheidung |
| 0.3.1 | 2026-06-18 | Post-Process um Economy, Sustainability und Assessment erweitert; Feedback als eigener Block bestaetigt |
| 0.3.2 | 2026-06-18 | Leitlinien fuer einen kontrollierten IDA-ICE-Variantenexport ergaenzt |
| 0.3.3 | 2026-06-18 | Vergleich von manuellem und automatisiertem Prozessaufwand als Untersuchungsdimension ergaenzt |
| 0.3.4 | 2026-06-18 | Einheitlichen Modulkatalog mit Zweck, Ein- und Ausgaben, Abgrenzung und Status ergaenzt |
| 0.3.5 | 2026-06-18 | Aktuelles Miro-Workflow-Diagramm fachlich eingeordnet und Review verlinkt |
| 0.3.6 | 2026-06-18 | Originalgrafik des aktuellen Miro-Workflows versioniert und direkt verlinkt |
| 0.3.7 | 2026-06-18 | Aktualisierten Miro-Workflow v0.1.1 mit korrigierter Bewertungs- und Berichtszuordnung dokumentiert |
| 0.4.0 | 2026-06-18 | Leitfaden in acht feste Hauptbereiche umgegliedert; Version 0.3.7 zuvor unveraendert archiviert |
| 0.4.1 | 2026-06-18 | Workflow-Archiv und zentral gepruefte Modulumsetzungsstaende ergaenzt |
| 0.4.2 | 2026-06-18 | Plot-Template-Wizard, Overlay-Schritt, Achsenanpassung und Single-/Compare-Ausgabe aktualisiert |
| 0.4.3 | 2026-06-21 | P007 als verbindlichen Rahmenplan aufgenommen und offene Architekturabgleiche dokumentiert |
| 0.5.0 | 2026-06-21 | Phase 0 bis Phase 6, allgemeine Simulationsschnittstellen, Modulgerueste und Planarchivierung konsolidiert |
| 0.5.1 | 2026-06-22 | Eingabekette priorisiert, Modulplanserie P010-P027 und Standards-Compliance-Stufe aufgenommen |
| 0.5.2 | 2026-06-22 | Fachlichen Reifegrad vereinheitlicht und Infokarten-Navigation aufgenommen |
| 0.5.3 | 2026-06-23 | P028, neutrale Benennungsverantwortung und geschuetzte formaterweiterbare Konfiguration aufgenommen |
| 0.5.4 | 2026-06-24 | Datenvorbereitung als eigenen Workflow-Schritt und UI-Struktur mit Streamlit-/Tkinter-Zweigen unter `ma_ui` aufgenommen |
| 0.5.5 | 2026-06-26 | Entscheidungen zu P010/P008, `plot-template-weather`, lokaler TRY-Dateisuche, UI-Modul-/Workflow-Ansicht und Befehlsinventar nachgezogen |
| 0.5.6 | 2026-06-29 | Harten Tkinter-Schnitt aus `ma_analyse`, P029-Fortschritt und Sammelbefehl-Freigaberegel nachgezogen |

## 1. Zweck der Software

Die Software ist ein methodisches Hilfsmittel fuer die Masterarbeit im Bereich
simulationsgestuetzte TGA-Planung mit IDA ICE. Sie ersetzt keine
ingenieurfachliche Bewertung und ist kein vollstaendiges kommerzielles
Planungstool.

Der wissenschaftliche Wert liegt in der strukturierten Methodik:

- Parameter und Randbedingungen nachvollziehbar erfassen
- Varianten systematisch bilden und dokumentieren
- IDA-ICE-Simulationen vorbereiten und Ergebnisse strukturiert ablegen
- Simulationsergebnisse reproduzierbar analysieren
- technische, wirtschaftliche und oekologische Bewertung anschlussfaehig machen
- Berichte, Factsheets und Entscheidungsgrundlagen vorbereiten

Automatisierung ist ein Potenzial, aber nicht zwingend der Kern der Arbeit. Ein
manueller IDA-ICE-Simulationsschritt ist zulaessig, wenn Eingaben, Modellstand,
Variante, Wetterdatensatz, Run-ID und Ergebnisablage sauber dokumentiert sind.

### Prozessaufwand und Automatisierungsnutzen

Neben der technischen Variantenbewertung soll untersucht werden, welchen
Zeitaufwand ein Mitarbeiter fuer den gesamten Ablauf manuell benoetigt und wie
sich dieser Aufwand durch den softwareunterstuetzten oder automatisierten
Workflow veraendert. Aus der aktiven Arbeitszeit kann unter dokumentierten
Annahmen ein Personalkostenvergleich abgeleitet werden.

Der Vergleich soll mindestens drei Ausfuehrungsarten unterscheiden:

1. Manueller Ablauf ohne Projektsoftware.
2. Softwareunterstuetzter Ablauf mit manuellen Zwischenschritten.
3. Soweit umgesetzt: automatisierter Ablauf mit der entwickelten Software.

Zusaetzlich koennen unterschiedliche Wissensstaende betrachtet werden:

- Einsteiger mit grundlegender Projekt- und IDA-ICE-Einarbeitung
- erfahrener Anwender mit Kenntnis des normalen Planungsablaufs
- Experte mit vertiefter IDA-ICE-, TGA- und Auswertungserfahrung

Die Wissensstaende duerfen nicht nur ueber pauschale Faktoren angesetzt werden.
Annahmen, Messwerte, Erfahrungswerte oder Experteneinschaetzungen muessen
getrennt gekennzeichnet werden.

#### Zu erfassende Zeitarten

| Zeitart | Bedeutung |
|---|---|
| aktive Arbeitszeit | Zeit fuer Eingaben, Kontrollen, Exporte, Auswertungen und Dokumentation |
| Maschinenlaufzeit | Laufzeit von Python, IDA ICE oder anderen Prozessen ohne aktive Bearbeitung |
| Wartezeit | Zeit zwischen Arbeitsschritten, in der ein Prozess abgeschlossen werden muss |
| Fehlerkorrektur | Aufwand fuer falsche Eingaben, unvollstaendige Daten, fehlgeschlagene Simulationen oder Nachbearbeitung |
| Einarbeitungszeit | zusaetzlicher Aufwand aufgrund des jeweiligen Wissensstands |
| Wiederholungsaufwand | Aufwand pro weiterer Variante, Raumgruppe, Simulation oder Auswertung |

Aktive Arbeitszeit und reine Maschinenlaufzeit werden getrennt ausgewiesen.
Eine schnellere Rechenzeit ist nicht automatisch gleichbedeutend mit einer
entsprechenden Personalkosteneinsparung.

#### Vorgesehene Auswertung

Der Prozess wird in vergleichbare Arbeitsschritte zerlegt:

- Parameter und Randbedingungen erfassen
- Varianten bilden und kontrollieren
- Simulationssetup dokumentieren
- IDA-ICE-Modell oder Exportstruktur vorbereiten
- Simulation ausfuehren und kontrollieren
- Ergebnisse importieren
- Kennwerte und Diagramme erzeugen
- Wirtschaftlichkeit und Nachhaltigkeit bewerten
- Berichte und Factsheets erstellen

Fuer jeden Arbeitsschritt sollen nach Moeglichkeit dokumentiert werden:

- manuelle und softwareunterstuetzte aktive Arbeitszeit
- Maschinen- und Wartezeit
- Zahl der Wiederholungen
- Fehler- oder Korrekturaufwand
- Wissensstand der ausfuehrenden Person
- Datenquelle und Qualitaet der Schaetzung

Ein vereinfachter Personalkostenansatz kann verwendet werden:

```text
Personalkosten = aktive Arbeitszeit in Stunden * angesetzter Stundensatz
```

Optional koennen Einarbeitung, Fehlerkorrektur und wiederkehrende
Softwarepflege getrennt ausgewiesen werden. Stundensaetze und Zeitannahmen
muessen transparent dokumentiert und als Messwert, Schaetzung oder Szenario
gekennzeichnet werden.

#### Ziel der Untersuchung

Die Untersuchung soll nicht nur zeigen, ob einzelne Befehle schneller laufen.
Sie soll beurteilen:

- ab welcher Varianten- oder Wiederholungszahl Automatisierung Zeit spart
- welche Arbeitsschritte besonders zeitintensiv oder fehleranfaellig sind
- welchen Einfluss der Wissensstand auf den manuellen Aufwand hat
- wie viel aktive Arbeitszeit gegen Maschinenlaufzeit getauscht wird
- welche Qualitaets- und Nachvollziehbarkeitsvorteile neben der Zeitersparnis
  entstehen
- welcher Entwicklungs-, Pflege- und Einfuehrungsaufwand der Automatisierung
  gegenuebersteht

Die Ergebnisse koennen spaeter in `ma_economy` als Prozesskostenbetrachtung
und in `ma_assessment` als Bestandteil eines Gesamtberichts verwendet werden.

### Grundregeln

- Fachlogik bleibt in Fachmodulen.
- `ma_ui` ist der gemeinsame lokale UI-Bereich. Streamlit bleibt der aktuelle
  Haupteinstieg; Tkinter liegt als getrennter UI-Zweig unter `ma_ui`.
- `ma_workflow` vermittelt zwischen Oberflaeche und Fachmodulen.
- Tkinter und Streamlit werden nicht technisch vermischt.
- Echte lokale Daten, TRY-Dateien, IDA-Ergebnisdaten und Produktdatenblaetter
  werden nicht als Projektinhalt versioniert.
- Die modulare Datenstruktur unter `data/<modul>/input`, `database`, `output`
  usw. bleibt erhalten.
- Dokumentation, Nutzerentscheidungen, technische Entscheidungen und offene
  Punkte werden getrennt gefuehrt.

### Mindestumfang und optionale Erweiterungen

Der Leitfaden trennt Mindestumfang und optionale Erweiterungen.

Mindestumfang:

- Parameter- und Variantenstruktur nachvollziehbar dokumentieren
- Wetterdaten referenzieren und fuer TRY-Datensaetze analysieren
- IDA-Ergebnisdaten importieren oder strukturiert ablegen
- zentrale Analysekennwerte und Diagramme erzeugen
- Varianten vergleichbar machen
- Factsheets oder Ergebnisberichte vorbereiten
- offene Annahmen und Grenzen dokumentieren

Optionale Erweiterungen:

- direkter IDA-ICE-Export in Eingabedateien
- automatisierter Simulationsstart
- vollstaendige PostgreSQL-Nutzung
- detaillierte Produktdatenbank
- vollstaendige Oekobilanz
- automatisches Ranking mit frei gewichteten Kriterien

## 2. Gesamtworkflow der Masterarbeit

Die technische Plattform wird als Phase 0 dargestellt. Danach folgen die
sechs fachlichen P007-Hauptphasen:

0. Technische Plattform
1. Projektinitialisierung
2. Eingangsdaten und Pre-Processing
3. Variantenbildung und Simulationsvorbereitung
4. Simulation und technische Analyse
5. Wirtschaftlichkeit, Nachhaltigkeit und Gesamtbewertung
6. Reporting, Datenexport und Dokumentation

`ma_validation` und `ma_feedback` wirken phasenuebergreifend.

Das aktuelle Miro-Workflow-Diagramm und sein fachliches Review werden unter
`docs/project/architecture/workflow/` gefuehrt. Das Diagramm ist ein
Ist-Entwurf; verbindliche Zielmodule und Modulgrenzen stehen weiterhin in
`docs/project/architecture/TARGET_ARCHITECTURE.md`.

- [Aktuelles Workflow-Diagramm](architecture/workflow/WORKFLOW_DIAGRAM_v0.1.1_2026-06-18.jpg)
- [Fachliches Workflow-Review](architecture/workflow/WORKFLOW_DIAGRAM_REVIEW_v0.1.1_2026-06-18.md)

| Phase | Module und Bereiche | Aufgabe |
|---|---|---|
| 0 | `ma_core`, `ma_database`, `ma_ui`, `ma_workflow`, Dokumentationsinfrastruktur | technische und organisatorische Grundlage |
| 1 | `ma_project` | Projekt und Untersuchungsrahmen initialisieren |
| 2 | `ma_building`, `ma_weather`, `ma_zones`, `ma_technical`, `ma_parameters` | Eingaben erfassen und vereinheitlichen |
| 3 | `ma_analyse.stage_1_dimensioning`, `ma_variants`, `ma_simulation_setup`, `ma_export_simulation` | Referenz dimensionieren, Varianten und Run vorbereiten |
| 4 | IDA ICE, `ma_import_simulation`, `ma_analyse.data_preparation`, `ma_analyse.stage_2_optimization`, `ma_analyse.stage_3_standards_compliance`, `ma_analyse.stage_4_sensitivity` | simulieren, Daten vorbereiten, optimieren, Norm-Nachweise und Sensitivitaet auswerten |
| 5 | `ma_economy`, `ma_sustainability`, `ma_assessment` | wirtschaftlich, oekologisch und gesamthaft bewerten |
| 6 | `ma_reporting`, `ma_data_export`, Projektdokumentation | Berichte, Datenpakete und Archivierung |

### Allgemeine Simulationsschnittstellen

`ma_export_simulation` und `ma_import_simulation` sind programmunabhaengige
Hauptmodule. Die IDA-ICE-Anbindung liegt jeweils unter `adapters/ida_ice`.

Sicherheitsregeln:

- keine freie Neuerzeugung kompletter IDM-Modelle
- keine IDM-Manipulation ohne geprueften Parser
- keine erfundenen IDA-ICE-Skript- oder API-Befehle
- kein automatischer Simulationsstart in der ersten Zielstufe
- bestehende Export- und Importlogik erst nach Schnittstellenplan migrieren

P009 beschreibt die weitere Umsetzung, bleibt aber bis zum validierten
`RunManifest` aus P018 zurueckgestellt. Der historische P006-Entwurf liegt
unveraendert im Planarchiv.

### Fachliche Rollen nach der Simulation

- `ma_analyse`: technische Ergebnisse und Auffaelligkeiten
- `ma_analyse.stage_2_optimization`: Variantenoptimierung mit vorhandenen
  Analysewerkzeugen
- `ma_analyse.stage_3_standards_compliance`: Norm-Nachweis deutscher und
  spaeter internationaler Normenprofile
- `ma_analyse.stage_4_sensitivity`: kritische Wetter- und Betriebsfaelle
- `ma_economy`: wirtschaftliche Auswirkungen
- `ma_sustainability`: Umweltwirkungen
- `ma_assessment`: zusammenfassende Bewertung
- `ma_reporting`: lesbare Berichte und Factsheets
- `ma_data_export`: maschinenlesbare Datenpakete

## 3. Moduluebersicht

### Statusuebersicht

| Modul | Status | Rolle |
|---|---|---|
| `ma_core` | geplant, P010-Pilot nutzbar | Quellen-, ID- und Sitzungslog-Basiskontrakte sind im Wetterpilot vorhanden |
| `ma_database` | geplant | Datenbanklogik liegt derzeit vor allem in `ma_variants` |
| `ma_project` | geplant | Projektstammdaten, Randbedingungen und Projektstatus |
| `ma_analyse` | teilweise | Analyse von IDA-ICE-Ergebnisdaten, CLI, UI-neutrale Services, Plot-Templates |
| `ma_variants` | geplant | Prototyp fuer Variantenkern, Datenmodelle, Auswahl, Naming, Export und Kataloge vorhanden |
| `ma_weather` | teilweise | TRY-Katalog, Import, Scan, Validierung, Freigabe, Diagramme, Bericht und kritische Ereignisse |
| `ma_ui` | geplant | Streamlit-Prototyp mit Modul-/Workflow-Ansicht, Referenzdiagramm und getrenntem Tkinter-Zweig vorhanden |
| `ma_workflow` | geplant | Katalog- und Orchestrierungsprototyp vorhanden |
| `ma_parameters` | geplant | Parameter- und Optionslogik liegt noch in `ma_variants` |
| `ma_building` | geplant | Gebaeudemodell, Bauteile und bauphysikalische Randbedingungen |
| `ma_zones` | geplant | thermische Zonen, Nutzungen, Sollwerte und Profile |
| `ma_technical` | geplant | technische Systeme, Komponenten und Regelung |
| `ma_analyse.stage_1_dimensioning` | geplant | Referenzdimensionierung vor der Variantenbildung |
| `ma_analyse.stage_2_optimization` | teilweise | vorhandene Analysebefehle, gemeinsamer Stufenablauf fehlt |
| `ma_analyse.stage_3_standards_compliance` | geplant | Norm-Nachweis, deutsche Normenprofile zuerst |
| `ma_analyse.stage_4_sensitivity` | geplant | Vorarbeiten fuer Zeitfenster und Wetterkennwerte vorhanden, Ereignisverknuepfung fehlt |
| `ma_simulation_setup` | geplant | Simulationsrandbedingungen und Run-Definition |
| `ma_export_simulation` | geplant | Basisexport liegt noch in `ma_variants`; IDA ICE wird Adapter |
| `ma_import_simulation` | geplant | Ergebnisadapter und Aufbereitung existieren noch ausserhalb des Zielmoduls |
| `ma_economy` | geplant | Wirtschaftlichkeitsprototyp liegt noch in `ma_variants` |
| `ma_sustainability` | geplant | Nachhaltigkeitsbewertung als eigenes Fachmodul |
| `ma_assessment` | geplant | Bewertungs- und Scoringschicht ueber Analyse, Wirtschaft und Nachhaltigkeit |
| `ma_reporting` | geplant | Reportfunktionen liegen noch in Fachmodulen |
| `ma_data_export` | geplant | Exporte liegen noch verteilt in Fachmodulen |
| `ma_validation` | geplant, P010-Pilot nutzbar | Diagnose- und Freigabevertraege sind im Wetterpilot vorhanden |
| `ma_feedback` | geplant | phasenuebergreifende Ruecksprungsteuerung |

### Vollstaendiger Modulkatalog

Der Modulkatalog beschreibt die fachliche Zielrolle der Module. Bei geplanten
Modulen ist dies noch kein Implementierungsnachweis. Bestehende Logik wird erst
nach einem eigenen Plan und stabilen Schnittstellen verschoben.
Der Status bewertet den fachlichen Reifegrad im Gesamtworkflow. Ein
Paketgeruest, eine Infoseite oder vorhandener Prototypcode genuegt nicht fuer
`teilweise` oder `verfuegbar`.

#### ma_core

- **Zweck:** Gemeinsame Pfad-, Konfigurations-, Logging-, ID- und
  Vorlagenregeln.
- **Status:** Als Gesamtmodul geplant; P010 stellt bereits
  `InputSource`, `InputChange`, eindeutige IDs und lokale append-only
  Sitzungslogs fuer den Wetterpilot bereit.

#### ma_database

- **Zweck:** Spaetere moduluebergreifende Persistenz kapseln.
- **Status:** Geplant; bestehende Datenbanklogik bleibt vorerst in
  `ma_variants`.

#### ma_project

- **Zweck:** Projektstammdaten, Untersuchungsrahmen und Projektstatus
  verwalten sowie Simulationsprogramme und neutrale
  Varianten-Benennungsprofile referenzieren.
- **Status:** Geplant; P028-Demo fuer Simulationsprogramme und neutrales
  Benennungsprofil umgesetzt.

#### ma_parameters

- **Zweck:** Zentrale Verwaltung technischer Parameter, Optionsgruppen,
  Pflichtfelder, Einheiten und Kategorien.
- **Eingaben:** YAML als erstes Format sowie spaeter JSON-, CSV-, Excel- oder
  Datenbankdaten.
- **Ausgaben:** validierte Parameter- und Optionsobjekte fuer Varianten,
  Simulation-Setup und Export.
- **Abgrenzung:** Das Modul bildet keine Varianten und schreibt keine
  IDA-ICE-Dateien.
- **Status:** Geplant; P028-Demo fuer schreibgeschuetzte Parameteranzeige und
  aktive Optionsauswahl umgesetzt. Der produktive `ParameterSnapshot` fehlt.

#### ma_weather

- **Zweck:** Wetterdateien katalogisieren, TRY-Daten importieren, validieren,
  analysieren und dokumentieren.
- **Eingaben:** lokale TRY-Dateien, Wetterkatalog und Standortzuordnungen.
- **Ausgaben:** aufbereitete Wetterdaten, Kennwerte, Diagramme, Berichte,
  Datensatzstatus, Freigaben und kritische Wetterereignisse.
- **Abgrenzung:** Wetterdaten sind eigene Randbedingungen und keine normalen
  IDA-Zonenergebnisdaten.
- **Status:** Teilweise aktiv; Import, Validierung, Kennwerte, Diagramme,
  Bericht, lokale Runner, `plot-template-weather`, lokale TRY-Dateisuche
  und bewusste Katalogregistrierung sind vorhanden.

#### ma_building

- **Zweck:** Gebaeude-, Raum-, Zonen- und Modellrandbedingungen strukturiert
  bereitstellen.
- **Eingaben:** Geometrie, Flaechen, Zonen, Bauteile, Fenster, Nutzung und
  Referenzmodellinformationen.
- **Ausgaben:** neutrale Gebaeude- und Zonenobjekte fuer Varianten,
  Normierungen, Simulation-Setup und Export.
- **Abgrenzung:** Keine Variantenkombination, Simulation oder
  Ergebnisanalyse.
- **Status:** Geplant; vor Implementierung muessen Datenumfang und Bezug zum
  IDA-ICE-Modell definiert werden.

#### ma_zones

- **Zweck:** Thermische Zonen, Nutzungen, Sollwerte, interne Lasten und
  Profile verwalten.
- **Ausgaben:** validierte Zonendaten fuer `ma_parameters`.
- **Abgrenzung:** Keine Gebaeudegeometrie und keine Anlagenberechnung.
- **Status:** Geplant.

#### ma_technical

- **Zweck:** Erzeugung, Verteilung, Uebergabe, Regelung und Komponenten
  beschreiben.
- **Ausgaben:** validierte Technikdaten fuer `ma_parameters`.
- **Abgrenzung:** Keine Variantenbildung.
- **Status:** Geplant.

#### ma_analyse.stage_1_dimensioning

- **Zweck:** Heizlast, Kuehllast und Luftmengen fuer die Referenz
  nachvollziehbar dimensionieren.
- **Eingaben:** validierte zentrale Parameterliste sowie dokumentierte Norm-
  und Auslegungsannahmen.
- **Ausgaben:** Dimensionierungsvorschlaege fuer die Referenz.
- **Abgrenzung:** Keine Variantenbildung und keine Analyse von
  Simulationsergebnissen.
- **Status:** Geplant; Paket und Dokumentation bilden nur die Modulgrenze ab.

#### ma_variants

- **Zweck:** Varianten erzeugen, auswaehlen, benennen und nachvollziehbar
  verwalten.
- **Eingaben:** validierte Parameter, Optionsgruppen, Auswahlregeln und
  ein neutrales Benennungsprofil aus `ma_project`.
- **Ausgaben:** Variantenobjekte, Variantenwerte, Auswahlmengen,
  Variantenuebersichten und Exporte.
- **Abgrenzung:** Das Modul soll langfristig weder Simulationsrandbedingungen
  noch Wirtschaftlichkeits- oder IDA-Dateilogik besitzen.
- **Status:** Geplant; ein Prototyp ist vorhanden, enthaelt aber noch spaetere
  Extraktionsquellen fuer Parameter, IDA-Export, Ergebnisadapter und
  Wirtschaftlichkeit.

#### ma_simulation_setup

- **Zweck:** Festlegen, wie eine Variante simuliert wird.
- **Eingaben:** Varianten, Wetterdatensatz, Zeitraum, Zeitschritt,
  Ausgabeintervall und Szenario.
- **Ausgaben:** validierte Run-Definition mit Run-ID und
  Simulationsmetadaten.
- **Abgrenzung:** Das Modul erzeugt keine Varianten und veraendert keine
  IDA-ICE-Dateien.
- **Status:** Geplant; es liegt bewusst zwischen `ma_variants` und
  `ma_export_simulation`.

#### ma_export_simulation

- **Zweck:** Varianten und Simulationssetup programmunabhaengig fuer
  Simulationsadapter vorbereiten.
- **Eingaben:** Variante, aufgeloeste Parameter, Run-Definition, geprueftes
  Referenzmodell und verifiziertes Mapping.
- **Ausgaben:** Exportordner, Modellkopie, Parameter- und Metadaten-JSON,
  Exportindex und spaeter optional verifizierte Skripte.
- **Abgrenzung:** Keine freie Neuerzeugung kompletter IDM-Modelle, keine
  ungesicherte Textmanipulation und kein Simulationsstart.
- **Status:** Geplant; eine erste Uebergabestruktur existiert noch
  in `ma_variants.ida_export`. P009 beschreibt die weitere Schnittstelle und
  den IDA-ICE-Adapter.

#### IDA ICE

- **Zweck:** Externe Simulationsumgebung fuer Gebaeude- und
  TGA-Simulationen.
- **Eingaben:** geprueftes Referenzmodell, Variantenparameter,
  Simulationssetup und Wetterdaten.
- **Ausgaben:** IDA-ICE-Ergebnisdateien und Simulationsmeldungen.
- **Abgrenzung:** IDA ICE ist kein Python-Modul dieses Projekts. Manuelle
  Arbeitsschritte bleiben zulaessig und muessen dokumentiert werden.
- **Status:** Externer Prozess zwischen den IDA-ICE-Adaptern von
  `ma_export_simulation` und `ma_import_simulation`.

#### ma_import_simulation

- **Zweck:** Simulationsergebnisse programmunabhaengig erkennen, pruefen,
  zuordnen und standardisieren.
- **Eingaben:** lokale Ergebnisordner, Run-Metadaten, Varianten- und
  Raumzuordnungen.
- **Ausgaben:** validierte und standardisierte Ergebnisdaten fuer
  `ma_analyse`.
- **Abgrenzung:** Keine fachliche Kennwertberechnung, Diagrammerzeugung oder
  Bewertung.
- **Status:** Geplant; Ergebnisadapter und Aufbereitung liegen
  derzeit in `ma_variants.simulation_results` und in der
  Import-/Aufbereitungslogik von `ma_analyse`.

#### ma_analyse

- **Zweck:** IDA-ICE-Simulationsergebnisse technisch auswerten.
- **Eingaben:** standardisierte Ergebnisdaten, Varianten- und Raumwahl sowie
  Analyse- und Diagrammkonfiguration.
- **Ausgaben:** Kennwerte, Tabellen, Diagramme, Excel-Dateien und
  Analyseberichte.
- **Abgrenzung:** Keine Kosten-, Nachhaltigkeits- oder
  Gesamtbewertungslogik; die UI soll langfristig ausserhalb des Fachkerns
  liegen.
- **Status:** Teilweise; CLI, Tkinter-GUI, Service-Fassade, Analysen und
  Plot-Templates sind vorhanden.

#### ma_analyse.stage_2_optimization

- **Zweck:** Varianten mit vorhandenen Energie-, Leistungs-, Komfort- und
  Zeitreihenanalysen vergleichen.
- **Status:** Teilweise vorhanden; P019 buendelt die bestehenden Befehle.

#### ma_analyse.stage_3_standards_compliance

- **Zweck:** Varianten anhand dokumentierter deutscher Normen und normierter
  Rechenverfahren nachweisen.
- **Erweiterung:** Internationale Normen werden spaeter als weitere
  Standards-Profile angebunden.
- **Abgrenzung:** Keine allgemeine Modellverifikation; keine ungeprueften
  Grenzwerte.
- **Status:** Geplant; P020 beginnt mit Quellen- und Methodenrecherche.

#### ma_analyse.stage_4_sensitivity

- **Zweck:** Kritische Wetter- und Betriebsfaelle, Robustheit und
  Parametereinfluss untersuchen.
- **Status:** Geplant; P021 verbindet vorhandene Vorarbeiten fuer Wetterereignisse mit
  bestehenden Tages- und Wochenanalysen.

#### ma_economy

- **Zweck:** Wirtschaftliche Auswirkungen von Varianten und auch den
  Prozessaufwand bewerten.
- **Eingaben:** technische Kennwerte, Investitions- und Wartungskosten,
  Energiepreise, Lebensdauern, Arbeitszeiten und Stundensaetze.
- **Ausgaben:** Investitions-, Betriebs-, Lebenszyklus- und Prozesskosten
  sowie wirtschaftliche Vergleichsergebnisse.
- **Abgrenzung:** Keine technische Simulation, keine Nachhaltigkeitsbewertung
  und kein abschliessendes Gesamt-Ranking.
- **Status:** Geplant; generische Wirtschaftlichkeitslogik liegt
  derzeit in `ma_variants.economic_analysis`, das eigene Zielpaket ist nur
  als leichtes Geruest angelegt.

#### ma_sustainability

- **Zweck:** Umweltwirkungen und Nachhaltigkeitskennwerte von Varianten
  bewerten.
- **Eingaben:** Energiekennwerte, Energietraeger, Emissionsfaktoren,
  Produkt-/Materialdaten, Quellen und Systemgrenzen.
- **Ausgaben:** CO2-, GWP- und weitere dokumentierte
  Nachhaltigkeitsergebnisse.
- **Abgrenzung:** Keine Wirtschaftlichkeitsrechnung und keine automatische
  Gesamtbewertung.
- **Status:** Geplant; Datenbasis, Systemgrenzen und fachlicher Umfang sind
  noch festzulegen.

#### ma_assessment

- **Zweck:** Ergebnisse aus Analyse, Economy und Sustainability zu einer
  nachvollziehbaren Gesamtbewertung zusammenfuehren.
- **Eingaben:** technische, wirtschaftliche und oekologische Ergebnisse sowie
  spaeter Gewichtungen oder Bewertungsregeln.
- **Ausgaben:** Scores, Ampeln, Rankings, Pareto-Loesungen und
  Entscheidungsvorlagen.
- **Abgrenzung:** Keine primaere Rechenlogik fuer Simulation,
  Wirtschaftlichkeit oder Nachhaltigkeit und keine Berichtserzeugung.
- **Status:** Geplant; Bewertungsregeln muessen separat definiert werden.

#### ma_reporting

- **Zweck:** Menschlich lesbare Berichte, Factsheets und
  Ergebnisdarstellungen erzeugen.
- **Eingaben:** Analyse- und Bewertungsergebnisse sowie Berichtsvorlagen.
- **Ausgaben:** Berichte, Factsheets und Abbildungen.
- **Abgrenzung:** Keine primaere Berechnung und keine technische
  Datenpaketierung.
- **Status:** Geplant; Reportfunktionen liegen noch verteilt in
  Fachmodulen.

#### ma_data_export

- **Zweck:** Maschinenlesbare Projektergebnisse auswaehlen, paketieren und
  archivieren.
- **Eingaben:** Fachmodul-Exporte und Projektmetadaten.
- **Ausgaben:** CSV-, JSON-, Excel- und Archivpakete.
- **Abgrenzung:** Fachmodulspezifische Exporte bleiben in den Fachmodulen.
- **Status:** Geplant; eine zentrale Paketierung fehlt.

#### ma_validation

- **Zweck:** Lokale Pruefergebnisse sammeln und moduluebergreifende Freigaben
  verwalten.
- **Eingaben:** Validierungsberichte der Fachmodule und Workflow-Zustand.
- **Ausgaben:** Freigaben, Warnungen und blockierende Fehler.
- **Abgrenzung:** Fachregeln bleiben in den Fachmodulen.
- **Status:** Als Gesamtmodul geplant; P010 stellt bereits
  `DiagnosticMessage`, `ImportDiagnostic`, `ReleaseStatus`,
  `ReleaseChoice` und `ReleaseDecision` fuer den Wetterpilot bereit.

#### ma_feedback

- **Zweck:** Auffaelligkeiten, Fehler und Optimierungspotenziale in fruehere
  Workflow-Schritte zurueckfuehren.
- **Eingaben:** Import-, Analyse- und Bewertungsergebnisse sowie Warnungen und
  offene Punkte.
- **Ausgaben:** dokumentierte Rueckspruenge, Korrekturauftraege und
  Folgeentscheidungen.
- **Abgrenzung:** Das Modul veraendert nicht automatisch Parameter, Varianten
  oder Modelle.
- **Status:** Geplant; phasenuebergreifende Ruecksprungregeln fehlen.

#### ma_workflow

- **Zweck:** UI-Aktionen und Fachmodule in der richtigen Reihenfolge
  orchestrieren.
- **Eingaben:** Projektzustand, Benutzeraktionen und neutrale
  Service-Konfigurationen.
- **Ausgaben:** koordinierte Service-Aufrufe, Statusinformationen und
  Workflow-Ergebnisse.
- **Abgrenzung:** Keine eigene Fachberechnung und keine Darstellung.
- **Status:** Geplant; ein Prototyp fuer Phasen-, Modul- und Statuskatalog,
  Dashboard-Aktionen und Analyse-Adapter ist vorbereitet.

#### ma_ui

- **Zweck:** Zentrale lokale Bedienoberflaeche fuer den Gesamtworkflow.
- **Eingaben:** Benutzerauswahl, Projektzustand und Ergebnisse neutraler
  Services.
- **Ausgaben:** Navigation, Tabellen, Diagrammvorschauen, Statusanzeigen und
  Downloads.
- **Abgrenzung:** Keine Fach-, Analyse-, Varianten- oder Bewertungslogik in
  Streamlit-Komponenten.
- **Status:** Geplant; ein Streamlit-Prototyp mit Modul-Ansicht,
  separater Workflow-Ansicht, Referenzdiagramm, Analyse- und Wetterseiten
  sowie getrenntem Tkinter-Zweig ist vorhanden.

### Bewertungslogik

Die Bewertungsmodule werden getrennt geplant, weil der spaetere Umfang noch
nicht sicher abschaetzbar ist.

```text
ma_analyse
  technische Kennwerte, Diagramme, Analyseberichte

ma_economy
  Investitionskosten, Betriebskosten, Energiepreise, Lebensdauer,
  Szenarien, Lebenszykluskosten

ma_sustainability
  CO2, GWP, Emissionsfaktoren, Produkt-/Materialbezug,
  Systemgrenzen, Nachhaltigkeitskennwerte

ma_assessment
  Bewertungslogik, Gewichtungen, Ampeln, Scores, Rankings,
  Pareto-Loesungen, Entscheidungsvorlagen

ma_reporting
  Berichte, Factsheets, Abbildungen

ma_data_export
  maschinenlesbare Daten- und Archivpakete
```

`ma_assessment` enthaelt also nicht die primaere Rechenlogik fuer Kosten oder
Nachhaltigkeit. Es sammelt Ergebnisse aus `ma_analyse`, `ma_economy` und
`ma_sustainability` und erzeugt daraus eine zusammenfassende Bewertung.

### Factsheets

Fuer die Masterarbeit sind drei zentrale Factsheet-Typen sinnvoll.

#### Factsheet Variantenkatalog

Zweck:

- Variantenbildung nachvollziehbar machen
- untersuchte und ausgeschlossene Varianten begruenden
- Simulationsstatus und Ergebnisstatus dokumentieren

Typische Inhalte:

- Varianten-ID
- Variantenname
- geaenderte Parameter
- unveraenderte Referenzparameter
- Wetterdatensatz
- IDA-Modellversion
- Simulationsstatus
- Ergebnisstatus

#### Factsheet Wirtschaftlichkeit

Zweck:

- technische Ergebnisse mit wirtschaftlichen Annahmen verbinden
- Varianten aus Kostensicht vergleichen
- Annahmen transparent dokumentieren

Typische Inhalte:

- Investitionskosten
- Wartungskosten
- Energiepreise
- Lebensdauer
- Betrachtungszeitraum
- Betriebskosten
- Lebenszykluskosten

#### Factsheet Nachhaltigkeit

Zweck:

- Energie- und Systementscheidungen oekologisch einordnen
- CO2-/GWP-Werte nachvollziehbar dokumentieren
- Grenzen der Bewertung sichtbar machen

Typische Inhalte:

- Energiebedarf
- Energietraeger
- Emissionsfaktoren
- CO2-Emissionen im Betrieb
- Produkt- oder Materialbezug, falls Datenbasis vorhanden ist
- Datenqualitaet und Quellen

## 4. Daten- und Dokumentationsstruktur

### Datenstruktur

Die aktuelle modulare Datenstruktur bleibt verbindlich. Die generische Struktur
aus der ChatGPT-Referenz wird nicht uebernommen, weil das Projekt bereits eine
modulare Ablage besitzt.

| Bereich | Zweck |
|---|---|
| `data/ma_analyse/ida_imports/` | lokale IDA-Rohdaten und Ergebnisordner |
| `data/ma_analyse/database/` | aufbereitete Analyse-Datenbankdateien |
| `data/ma_analyse/output/` | regulaere Analyseausgaben |
| `data/ma_weather/input/` | lokale TRY-Eingangsdateien |
| `data/ma_weather/database/` | aufbereitete Wetterdaten |
| `data/ma_weather/output/` | Wetterdiagramme |
| `data/ma_weather/reports/` | Wetterberichte |
| `data/ma_variants/` | Variantenimporte, Exporte und IDA-Uebergaben |
| `data/ma_project/config/` | lokale Simulationsprogramm- und Naming-Profile |
| `data/ma_parameters/config/` | lokale Parameter- und Optionsarbeitsstaende |
| `data/catalogs/documents/` | Struktur fuer Produkt- und Materialdokumente |
| `data/test_output/` | lokaler Arbeits- und Smoke-Test-Bereich |
| `logs/sessions/` | lokale strukturierte Lauf-, Diagnose- und Freigabeereignisse |

Echte Projekt-, Ergebnis- und Katalogdaten werden nicht automatisch versioniert.
Die Ordnerstruktur bleibt reproduzierbar; Inhalte koennen lokal entstehen.

### Dokumentationsstruktur

| Datei oder Ordner | Zweck |
|---|---|
| `docs/project/plans/PLAN_STATUS.md` | aktive Steuerdatei nach Modulen |
| `docs/project/plans/PLAN_INDEX.md` | Uebersicht ueber Plaene |
| `docs/project/decisions/USER_DECISIONS_MASTERTHESIS_CODE.md` | Nutzerentscheidungen |
| `docs/project/decisions/USER_DECISIONS_OPEN_POINTS.md` | offene Nutzerentscheidungen |
| `docs/project/decisions/TECHNICAL_DECISIONS.md` | technische Entscheidungen |
| `docs/project/architecture/TARGET_ARCHITECTURE.md` | Zielarchitektur |
| `docs/project/architecture/UI_MIGRATION_PLAN.md` | UI-Migration, Streamlit und Tkinter |
| `docs/project/architecture/workflow/` | aktuelle Workflow-Grafik und aktuelles Review |
| `docs/project/archive/leitfaeden/` | archivierte Leitfadenfassungen |
| `docs/project/archive/workflow/` | ersetzte Workflow-Grafiken und Reviews |
| `docs/project/UPDATE_ROUTINES.md` | Codex-Routinen und Updateablaeufe |
| `CHANGELOG.md` | tatsaechlich umgesetzte Aenderungen |

### Archivierungsregel

- Die aktive Leitfadenfassung liegt unter
  `docs/project/MASTERARBEIT_LEITFADEN.md`.
- Eine unveraenderte Archivkopie wird erstellt, bevor die Leitfadenstruktur
  grundlegend umgebaut wird.
- Alte oder externe Leitfadenfassungen liegen unter
  `docs/project/archive/leitfaeden/`.
- Archivfassungen bleiben Referenzen und werden nicht als aktive
  Steuerdokumente verwendet.

## 5. UI- und Workflow-Struktur

### UI-Zielstruktur

`ma_ui` ist die Zieloberflaeche. Die Startseite zeigt aktuell eine
Modul-Ansicht mit Phasen und Umsetzungsstand. Die Workflow-Ansicht ist eine
eigene Startansicht unter `ma_workflow`. Modulseiten zeigen nur
modulbezogene Inhalte.

Aktueller Stand:

- `Start`: Modul-Ansicht, Workflow-Referenzdiagramm und technische
  Detailtabellen im Expander
- `ma_workflow`: eigene Workflow-Ansicht mit demselben Referenzdiagramm
- `Analyse`: Streamlit-Wizard fuer `ma_analyse`, orientiert an Tkinter-Ablauf
- `Analyse`: Overlay-Schritt direkt nach `Template / Diagramm`; der
  Overlay-Katalog wird erst nach Varianten- und Raumauswahl befuellt.
- `Wetterdaten`: Analysebereich oben, Wetterdatensatzuebersicht darunter
- `Wetterdaten`: Datensatzverwaltung mit `Import`, `Scannen` und
  `Validieren`; neue TRY-Dateien werden erst nach bewusster Nutzeraktion im
  lokalen Katalog registriert.
- Wetterlaeufe zeigen Quellen-ID, Dateipruefsumme, strukturierte Diagnosen und
  Freigabestatus. Warnungen koennen bewusst blockiert oder freigegeben werden.
- Wetterdiagramme laufen ueber `plot-template-weather <diagramm>
  --weather-key ...`; `all` erzeugt alle vorhandenen Wetterdiagramme.
- `Projekt`: Simulationsprogramme und neutrales Benennungsprofil
- `Parameter`: schreibgeschuetzte Definitionen und aktive Demo-Optionswerte
- `Varianten`: gemeinsamer Variantenraum mit angewendetem Benennungsprofil
- P028-Querverweise merken die Ausgangsseite; die normale Navigation beendet
  den speziellen Ruecksprungkontext.
- `Bewertung`: erste Uebersicht ueber Annahmen; langfristig Aufteilung in
  Economy, Sustainability und Assessment
- leere Zielmodule: Titel, Untertitel und blaue Hinweisbox

Das Workflow-Referenzdiagramm liegt als PNG und PDF unter
`src/ma_ui/assets/workflow/`. Das uebergreifende Befehls- und
Ausgabeninventar steht unter `docs/project/COMMAND_OUTPUT_INVENTORY.md`.

Tkinter bleibt nutzbar, liegt aber als eigener UI-Zweig unter
`ma_ui.tkinter_app`. Entscheidungen aus Tkinter werden fachlich ausgewertet
und schrittweise in UI-neutrale Logik ueberfuehrt. Der alte
`ma_analyse.gui`-Pfad und `python -m ma_analyse gui` sind entfernt.

### Workflow-Orchestrierung

`ma_workflow` vermittelt zwischen `ma_ui` und den Fachmodulen. Das Modul
koordiniert Reihenfolge, Projektzustand und neutrale Service-Aufrufe, enthaelt
aber keine eigene Fachberechnung und keine Streamlit-Darstellung.

### Eingabe, Diagnose und Freigabe

- `ma_core` stellt `InputSource`, `InputChange`, eindeutige IDs und das
  append-only Sitzungslog bereit.
- Fachmodule behalten ihre lokalen Pruefregeln.
- `ma_validation` vereinheitlicht Meldungsschwere, Diagnosecodes und
  Freigabeentscheidungen.
- Fehler blockieren immer. Warnungen benoetigen eine dokumentierte
  Entscheidung. Fehler- und warnungsfreie Staende werden automatisch
  freigegeben.
- P010 verwendet TRY-Wetterdaten als ersten Pilotadapter; weitere
  Eingabemodule folgen in P011 bis P015.

Der vorgesehene Aufrufpfad lautet:

```text
ma_ui
  -> ma_workflow
    -> UI-neutrale Services der Fachmodule
```

Workflow-Schritte duerfen in der UI sichtbar sein, ihre Fachlogik bleibt
jedoch in den zustaendigen Modulen.

### Trennung von UI und Fachlogik

- Streamlit-Komponenten enthalten keine Analyse-, Varianten- oder
  Bewertungslogik.
- Tkinter und Streamlit werden nicht direkt miteinander vermischt.
- Wiederverwendbare Auswahl-, Validierungs- und Konfigurationslogik wird in
  UI-neutrale Services oder Helfer ausgelagert.
- Neue Tkinter-Fachansichten werden spaeter nur ueber eigene Fachslices unter
  `ma_ui.tkinter_app.module_views/` ergaenzt.

## 6. Aktuelle Arbeitsroutinen

Wichtige Codex-Routinen:

- `aktualisieren`: Projektlage, Planung, Entscheidungen, Changelog,
  Versionen und Command-Dokumentation pruefen.
- `tagesstart`: Projektstand und offene Aufgaben anzeigen.
- `tagesende`: Dokumentation pruefen und Terminal-Code fuer Git vorbereiten.
- `tagesende direkt`: Tagesende plus Commit, Tag und Push durch Codex, wenn
  keine Blocker bestehen.
- `wochenabschluss`: Wochenstand dokumentieren und archivierungsfaehige
  Plaene pruefen.
- `projektlage`: Git-Stand, Version, aktive Plaene und offene Entscheidungen
  kompakt ausgeben.
- `update planung`: Plan-Inbox, Planindex, Planstatus und Entscheidungen
  pruefen.
- `plan aufnehmen`: einen neuen Plan aus der Plan-Inbox einordnen.
- `entscheidung festhalten`: eine Nutzerentscheidung dokumentieren und
  passende offene Punkte bereinigen.
- `release check`: Versionen, Changelog, Tags, Tests und offene Aenderungen
  pruefen, ohne ein Release auszufuehren.
- `aktualisiere tests`: benoetigte Referenzen oder Testoutputs aktualisieren,
  ohne Git-Aktionen auszufuehren.

Details stehen in `docs/project/UPDATE_ROUTINES.md`.

### Pflege- und Ueberfuehrungsregeln

Diese Datei ist fuer Orientierung und Kommunikation gedacht. Sie kann als
Grundlage fuer externe Abstimmungen, ChatGPT-Zusammenfassungen oder eigene
Notizen genutzt werden.

Wenn hier neue fachliche Punkte entstehen, werden sie nicht direkt umgesetzt,
sondern in die passenden Dateien ueberfuehrt:

- Aufgaben und Status nach `PLAN_STATUS.md`
- Nutzerentscheidungen nach `USER_DECISIONS_MASTERTHESIS_CODE.md`
- offene Entscheidungen nach `USER_DECISIONS_OPEN_POINTS.md`
- technische Entscheidungen nach `TECHNICAL_DECISIONS.md`
- umgesetzte Aenderungen nach `CHANGELOG.md`

## 7. Wichtigste Entscheidungen

Die vollstaendige Entscheidungshistorie steht unter
`docs/project/decisions/`. Fuer die Orientierung im Leitfaden gelten besonders
folgende Entscheidungen:

| Thema | Verbindliche Entscheidung | Nachweis |
|---|---|---|
| Projektstruktur | Das Projekt bleibt modular; aktive Planung, Entscheidungen, Architektur und Changelog werden getrennt gefuehrt. | UD-001, UD-002 |
| Rahmenplanung | P007 ist die verbindliche Planungsgrundlage; Zielstrukturen werden erst nach Bestandsanalyse, Planung und Freigabe umgesetzt. | UD-041 |
| Phasenmodell | Phase 0 und sechs fachliche P007-Phasen ersetzen die bisherige aktive Vierer-Gliederung. | UD-042 |
| Simulationsschnittstellen | `ma_export_simulation` und `ma_import_simulation` sind allgemein; IDA ICE liegt in Adaptern. | UD-043 |
| Eingabemodule | Gebaeude, Wetter, Zonen und Technik bleiben getrennt und liefern ueber `ma_parameters` an `ma_variants`. | UD-044 |
| Strukturaufbau | Zielmodule werden als leichte Pakete und klickbare Infoseiten sichtbar, ohne Fachreife vorzutäuschen. | UD-045 |
| Validierung und Feedback | Lokale Pruefungen bleiben fachlich; zentrale Freigaben und Rueckspruenge wirken phasenuebergreifend. | UD-046 |
| Ergebnisverarbeitung | Assessment, Reporting, Datenexport und Projektdokumentation bleiben getrennte Verantwortlichkeiten. | UD-047 |
| UI und Workflow | `ma_ui` ist der gemeinsame UI-Bereich; Streamlit bleibt Haupteinstieg, Tkinter liegt als getrennter UI-Zweig daneben. `ma_workflow` bleibt eine getrennte Orchestrierungsschicht. | UD-015, UD-018, UD-062 |
| Fachlogik | Fachlogik von `ma_analyse` bleibt in `ma_analyse` und wird ueber UI-neutrale Services bereitgestellt. | UD-016, UD-020 |
| Tkinter | Tkinter wird nicht technisch mit Streamlit vermischt; die Tkinter-Analyse liegt unter `ma_ui.tkinter_app` und kann spaeter um weitere Fachansichten ergaenzt werden. | UD-019, UD-022, UD-062 |
| Simulationskette | `ma_simulation_setup` liegt zwischen Variantenbildung und allgemeinem Simulationsexport; Export, Import und Feedback bleiben getrennte Zielbereiche. | UD-021, UD-043 |
| Bewertung | `ma_economy` und `ma_sustainability` rechnen fachlich; `ma_assessment` bewertet, `ma_reporting` berichtet. | UD-036, UD-047 |
| Datenhaltung | Echte Projekt-, Produkt-, Material-, Datenbank- und TRY-Inhalte bleiben lokal; versioniert werden Struktur und gekennzeichnete Beispiele. | UD-012, UD-029 |
| Eingabe, Diagnose und Freigabe | P010 trennt Fachpruefung, Freigabe und Sitzungsnachweis; Fehler blockieren, Warnungen brauchen eine bewusste Entscheidung mit ID und Sitzungslog. | UD-057 |
| Wetterauswahl | Stadtwahl, Klimaregion, Referenzstandort, Datensatzstatus, Aktivierung und Projekt-Default bleiben bewusst sichtbare Entscheidungen. | UD-058 |
| Wetterdatensaetze | Jahres-, Sommer- und Winter-TRY-Dateien sind eigene Datensaetze; kritische Ereignisse beziehen sich auf den bewusst gewaehlten Datensatz. | UD-059 |
| Wetterimport | Import, Scan und Validierung lokaler TRY-Dateien sind getrennt; Registrierung erfolgt erst nach Nutzeraktion im lokalen Katalog. | UD-060 |
| Wetterdiagramme | Wetterdiagramme bleiben fachlich in `ma_weather`; `plot-template-weather` ist der eigene CLI-/UI-Befehl fuer `all` oder einzelne Wetterdiagramme. | UD-063 |
| Datenvorbereitung | `prepare` und `analyze-data` bilden einen eigenen Workflow-Schritt zwischen Simulationsergebnisimport und Analyse Stufe 2. | UD-061 |
| Prozessvergleich | Manueller, softwareunterstuetzter und automatisierter Aufwand wird getrennt nach Arbeitszeit, Laufzeit, Fehlerkorrektur und Wissensstand betrachtet. | UD-038 |

Technische Detailentscheidungen stehen in
`docs/project/decisions/TECHNICAL_DECISIONS.md`. Offene Nutzerentscheidungen
stehen ausschliesslich in
`docs/project/decisions/USER_DECISIONS_OPEN_POINTS.md`.

## 8. Offene Strukturpunkte

- Tkinter-Vorschau soll einen temporaeren Vorschau- oder Cachebereich nutzen,
  damit der regulaere Output-Ordner nicht mit Testdiagrammen gefuellt wird.
- Overlay-Bedienung erlaubt in der Plot-Template-Sandbox freie Datenreihen aus
  lokalen Analyse-/Datenbankdaten; feste Additionen wie Temperaturband bleiben
  eigene Optionen. Die bewusste Uebernahme in regulaere Hauptbefehle bleibt
  offen.
- Cooling-Trennung relativ/absolut bleibt vorerst in Plot-Templates und wird
  spaeter fuer Hauptbefehl und GUI erneut bewertet.
- Normierung wird `ma_analyse`-weit geplant: absolute Werte, flaechenbezogene
  Werte oder beides brauchen spaeter eine konsistente Strategie.
- `ma_workflow` soll spaeter echte Fachservice-Aufrufe koordinieren.
- P010 bis P018 priorisieren die funktionsfaehige Eingabekette bis
  `ma_simulation_setup`.
- `ma_economy` und `ma_sustainability` erhalten kleine Demos mit
  vollstaendigem Fachkonzept; `ma_assessment`, `ma_reporting` und
  `ma_data_export` bleiben zunaechst konzeptuell.
- Fuer den Vergleich von Zeit- und Personalkosten sind Wissensprofile,
  Stundensaetze, Prozessgrenzen und Messmethoden noch festzulegen.
- P008 muss weitere Realtests, fachliche Wetterereignisdefinitionen fuer P021
  und die Uebergabe an `ma_parameters` abschliessen.
- P009 wird erst nach P018 weitergefuehrt.
- P020 darf Normregeln erst nach dokumentierter Quellen- und Methodenmatrix
  implementieren.
