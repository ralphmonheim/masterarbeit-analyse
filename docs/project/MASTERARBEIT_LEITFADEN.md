# Masterarbeit Leitfaden

Leitfaden-Version: 0.4.2
Stand: 2026-06-18

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
- `ma_ui` ist die zentrale lokale Streamlit-Oberflaeche.
- `ma_workflow` vermittelt zwischen Oberflaeche und Fachmodulen.
- Tkinter bleibt vorerst Legacy-Bestand in `ma_analyse`.
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

Der Workflow der Masterarbeit ist in vier Hauptbereiche gegliedert:

1. Pre-Process
2. Simulation
3. Post-Process
4. Feedback

Das aktuelle Miro-Workflow-Diagramm und sein fachliches Review werden unter
`docs/project/architecture/workflow/` gefuehrt. Das Diagramm ist ein
Ist-Entwurf; verbindliche Zielmodule und Modulgrenzen stehen weiterhin in
`docs/project/architecture/TARGET_ARCHITECTURE.md`.

- [Aktuelles Workflow-Diagramm](architecture/workflow/WORKFLOW_DIAGRAM_v0.1.1_2026-06-18.jpg)
- [Fachliches Workflow-Review](architecture/workflow/WORKFLOW_DIAGRAM_REVIEW_v0.1.1_2026-06-18.md)

### Pre-Process

Im Pre-Process werden alle Grundlagen vorbereitet, die fuer die Simulation
erforderlich sind.

| Reihenfolge | Zielmodul | Aufgabe |
|---|---|---|
| 1 | `ma_parameters` | Parameter, Optionsgruppen und Eingabekataloge |
| 2 | `ma_weather` | Wetterdaten, TRY-Dateien und klimatische Randbedingungen |
| 3 | `ma_building` | Gebaeude-, Zonen- und Modellrandbedingungen |
| 4 | `ma_variants` | Varianten bilden, auswaehlen und benennen |
| 5 | `ma_simulation_setup` | Zeitraum, Zeitschritt, Szenario und Run-Metadaten |
| 6 | `ma_export_ida` | IDA-ICE-Uebergabestruktur vorbereiten |

Typische Inhalte:

- Referenzgebaeude
- Untersuchungsraeume oder Zonen
- TGA-relevante Parameter
- Wetterdateien und Standort
- Variantenkatalog
- Simulationszeitraum und Ausgabeintervall
- IDA-Modellversion und manuelle Anpassungshinweise

### Simulation

IDA ICE bleibt der externe Simulationsschritt. Python bereitet Daten vor,
strukturiert die Ablage und wertet Ergebnisse aus. Der automatische Start von
IDA ICE ist aktuell kein stabiler Bestandteil des Workflows.

Pro Simulationslauf sollten mindestens dokumentiert werden:

- Run-ID
- Variante
- IDA-ICE-Modellversion
- Wetterdatensatz
- Simulationszeitraum
- bearbeitende Person oder Arbeitsstand
- Ergebnisordner
- Warnungen, Fehler oder Auffaelligkeiten

### Leitlinie fuer ma_export_ida

`ma_export_ida` ist ein kontrolliertes Pre-Processing-Modul zwischen
`ma_simulation_setup` und der externen IDA-ICE-Simulation. Python soll kein
vollstaendiges IDM-Modell frei neu erzeugen. Ausgangspunkt ist ein in IDA ICE
erstelltes und geprueftes Referenzmodell.

Kernaufgaben:

- ein geprueftes Referenzmodell erkennen und als Vorlage nutzen
- pro Variante einen eindeutig zugeordneten Exportordner erzeugen
- aufgeloeste Variantenparameter vor dem Export validieren
- eine technische Mapping-Struktur zwischen Projektparametern und
  IDA-ICE-Zielparametern fuehren
- Parameter, Quellen, Modellstand und Exportmetadaten nachvollziehbar speichern
- eine Exportuebersicht fuer alle verarbeiteten Varianten erzeugen
- Fehler und Warnungen sichtbar dokumentieren

Sicherheits- und Architekturregeln:

- Keine IDM-Datei wird ohne geprueften Parser oder bestaetigte Schnittstelle
  strukturell veraendert.
- Eine lokal verfuegbare und dokumentierte IDA-ICE-API oder Skriptschnittstelle
  wird gegenueber unsicherer Textmanipulation bevorzugt.
- IDA-ICE-Befehle, Attribute oder API-Funktionen duerfen nicht erfunden werden.
- Skriptvorlagen bleiben Platzhalter, bis reale Befehle lokal verifiziert sind.
- Pfade, Mappings und Standardeinstellungen werden konfiguriert und nicht hart
  im Code hinterlegt.
- UI-Logik bleibt ausserhalb von `ma_export_ida`; CLI und Streamlit greifen
  spaeter ueber eine neutrale Service-Schnittstelle zu.

Vorgesehene Ausbaustufen:

1. Sicheres Exportgeruest: Referenzmodell kopieren, Variantenordner,
   Parameter-JSON, Metadaten-JSON und Exportindex.
2. Fachlich gepruefte Parameter-Mappings und Plausibilitaetsvalidierung.
3. Verifizierte IDA-ICE-Skriptvorlagen.
4. Optionale API-Anbindung ueber einen austauschbaren Adapter.
5. Einbindung in `ma_workflow` und `ma_ui`.

Der zugehoerige Entwurfsplan ist P006:
`docs/project/plans/inbox/260618_Plan_ma_export_ida_IDM_Exportentwurf.md`.

### Post-Process

Im Post-Process werden IDA-Ergebnisse importiert, standardisiert, analysiert
und bewertet. Economy, Sustainability und Assessment gehoeren damit zum
Post-Process, weil sie auf aufbereiteten Simulations- und Varianteninformationen
aufbauen.

| Reihenfolge | Zielmodul | Aufgabe |
|---|---|---|
| 1 | `ma_import_ida` | IDA-Ergebnisordner erkennen, pruefen und standardisieren |
| 2 | `ma_analyse` | Simulationsergebnisse analysieren, Diagramme und Reports erzeugen |
| 3 | `ma_economy` | Wirtschaftlichkeit, Kosten, Energiepreise, Lebensdauer und Szenarien bewerten |
| 4 | `ma_sustainability` | CO2, GWP, Nachhaltigkeitskennwerte, Quellen und Produkt-/Materialbezug bewerten |
| 5 | `ma_assessment` | Ergebnisse aus Analyse, Economy und Sustainability zusammenfuehren und Berichte erzeugen |

`ma_analyse` beantwortet fachlich vor allem:

- Was zeigen die Simulationsergebnisse?
- Welche technischen Kennwerte entstehen?
- Welche Diagramme und Reports koennen daraus erzeugt werden?
- Welche Auffaelligkeiten gibt es in Komfort, Energie, Leistung oder Raumklima?

### Feedback

Feedback bleibt ein eigener Block nach dem Post-Process. Hier werden
Auffaelligkeiten, Rueckspruenge und offene Folgearbeiten dokumentiert.

| Zielmodul | Rolle |
|---|---|
| `ma_feedback` | Auffaelligkeiten und Rueckspruenge in Pre-Process-Module dokumentieren |

Damit gilt:

- `ma_analyse`: Was ist passiert?
- `ma_economy`: Was kostet die Variante?
- `ma_sustainability`: Welche Umweltwirkung hat die Variante?
- `ma_assessment`: Wie ist die Variante insgesamt zu bewerten und zu dokumentieren?

## 3. Moduluebersicht

### Statusuebersicht

| Modul | Status | Rolle |
|---|---|---|
| `ma_analyse` | aktiv | Analyse von IDA-ICE-Ergebnisdaten, CLI, Tkinter-GUI, Plot-Templates |
| `ma_variants` | aktiv | Variantenkern, Datenmodelle, Auswahl, Naming, Export, Kataloge |
| `ma_weather` | teilweise aktiv | TRY-Katalog, Import, Validierung, Kennwerte, Diagramme, Bericht |
| `ma_ui` | teilweise aktiv | Zentrale Streamlit-Oberflaeche mit Startseite und Modulansichten |
| `ma_workflow` | teilweise aktiv | Workflow-Katalog und Adapter zwischen UI und Fachmodulen |
| `ma_parameters` | teilweise vorhanden | Parameter- und Optionslogik liegt noch in `ma_variants` |
| `ma_building` | geplant | Gebaeude-, Zonen- und Modellrandbedingungen |
| `ma_simulation_setup` | geplant | Simulationsrandbedingungen und Run-Definition |
| `ma_export_ida` | teilweise vorhanden | Uebergabestruktur liegt noch in `ma_variants` |
| `ma_import_ida` | teilweise vorhanden | Ergebnisadapter und Aufbereitung existieren noch ausserhalb des Zielmoduls |
| `ma_economy` | teilweise vorhanden | Wirtschaftlichkeitslogik liegt noch in `ma_variants` |
| `ma_sustainability` | geplant | Nachhaltigkeitsbewertung als eigenes Fachmodul |
| `ma_assessment` | geplant | Bewertungs-, Scoring- und Berichtsschicht ueber Analyse, Wirtschaft und Nachhaltigkeit |
| `ma_feedback` | geplant | Rueckfuehrung von Auffaelligkeiten in den Pre-Process |
| `ma_ui_legacy` | geplant | Spaeterer Ort fuer Tkinter-Legacy, falls ausgelagert |
| `ma_shared` | geplant | Gemeinsame technische Grundlagen nur bei echter Wiederverwendung |

### Vollstaendiger Modulkatalog

Der Modulkatalog beschreibt die fachliche Zielrolle der Module. Bei geplanten
Modulen ist dies noch kein Implementierungsnachweis. Bestehende Logik wird erst
nach einem eigenen Plan und stabilen Schnittstellen verschoben.

#### ma_parameters

- **Zweck:** Zentrale Verwaltung technischer Parameter, Optionsgruppen,
  Pflichtfelder, Einheiten und Kategorien.
- **Eingaben:** YAML-, JSON-, CSV-, Excel- oder spaeter Datenbankdaten.
- **Ausgaben:** validierte Parameter- und Optionsobjekte fuer Varianten,
  Simulation-Setup und Export.
- **Abgrenzung:** Das Modul bildet keine Varianten und schreibt keine
  IDA-ICE-Dateien.
- **Status:** Teilweise vorhanden; wesentliche Parameterlogik liegt derzeit in
  `ma_variants.parameter_catalog` und `ma_variants.option_catalog`, das eigene
  Zielpaket fehlt noch.

#### ma_weather

- **Zweck:** Wetterdateien katalogisieren, TRY-Daten importieren, validieren,
  analysieren und dokumentieren.
- **Eingaben:** lokale TRY-Dateien, Wetterkatalog und Standortzuordnungen.
- **Ausgaben:** aufbereitete Wetterdaten, Kennwerte, Diagramme und Berichte.
- **Abgrenzung:** Wetterdaten sind eigene Randbedingungen und keine normalen
  IDA-Zonenergebnisdaten.
- **Status:** Teilweise aktiv; Import, Validierung, Kennwerte, Diagramme,
  Bericht und lokale Runner sind vorhanden.

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

#### ma_variants

- **Zweck:** Varianten erzeugen, auswaehlen, benennen und nachvollziehbar
  verwalten.
- **Eingaben:** validierte Parameter, Optionsgruppen, Auswahlregeln und
  Namensregeln.
- **Ausgaben:** Variantenobjekte, Variantenwerte, Auswahlmengen,
  Variantenuebersichten und Exporte.
- **Abgrenzung:** Das Modul soll langfristig weder Simulationsrandbedingungen
  noch Wirtschaftlichkeits- oder IDA-Dateilogik besitzen.
- **Status:** Aktiv; derzeit enthaelt es zusaetzlich noch spaetere
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
  `ma_export_ida`.

#### ma_export_ida

- **Zweck:** Varianten und Simulationssetup kontrolliert fuer IDA ICE
  vorbereiten.
- **Eingaben:** Variante, aufgeloeste Parameter, Run-Definition, geprueftes
  Referenzmodell und verifiziertes Mapping.
- **Ausgaben:** Exportordner, Modellkopie, Parameter- und Metadaten-JSON,
  Exportindex und spaeter optional verifizierte Skripte.
- **Abgrenzung:** Keine freie Neuerzeugung kompletter IDM-Modelle, keine
  ungesicherte Textmanipulation und kein Simulationsstart.
- **Status:** Teilweise vorhanden; eine erste Uebergabestruktur existiert noch
  in `ma_variants.ida_export`. P006 beschreibt den weiteren Entwurf.

#### IDA ICE

- **Zweck:** Externe Simulationsumgebung fuer Gebaeude- und
  TGA-Simulationen.
- **Eingaben:** geprueftes Referenzmodell, Variantenparameter,
  Simulationssetup und Wetterdaten.
- **Ausgaben:** IDA-ICE-Ergebnisdateien und Simulationsmeldungen.
- **Abgrenzung:** IDA ICE ist kein Python-Modul dieses Projekts. Manuelle
  Arbeitsschritte bleiben zulaessig und muessen dokumentiert werden.
- **Status:** Externer Prozess zwischen `ma_export_ida` und `ma_import_ida`.

#### ma_import_ida

- **Zweck:** IDA-ICE-Ergebnisordner erkennen, pruefen, zuordnen und
  standardisieren.
- **Eingaben:** lokale Ergebnisordner, Run-Metadaten, Varianten- und
  Raumzuordnungen.
- **Ausgaben:** validierte und standardisierte Ergebnisdaten fuer
  `ma_analyse`.
- **Abgrenzung:** Keine fachliche Kennwertberechnung, Diagrammerzeugung oder
  Bewertung.
- **Status:** Teilweise vorhanden; Ergebnisadapter und Aufbereitung liegen
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
- **Status:** Aktiv; CLI, Tkinter-GUI, Service-Fassade, Analysen und
  Plot-Templates sind vorhanden.

#### ma_economy

- **Zweck:** Wirtschaftliche Auswirkungen von Varianten und auch den
  Prozessaufwand bewerten.
- **Eingaben:** technische Kennwerte, Investitions- und Wartungskosten,
  Energiepreise, Lebensdauern, Arbeitszeiten und Stundensaetze.
- **Ausgaben:** Investitions-, Betriebs-, Lebenszyklus- und Prozesskosten
  sowie wirtschaftliche Vergleichsergebnisse.
- **Abgrenzung:** Keine technische Simulation, keine Nachhaltigkeitsbewertung
  und kein abschliessendes Gesamt-Ranking.
- **Status:** Teilweise vorhanden; generische Wirtschaftlichkeitslogik liegt
  derzeit in `ma_variants.economic_analysis`, das eigene Zielpaket fehlt noch.

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
- **Ausgaben:** Scores, Ampeln, Rankings, Factsheets, Ergebnisberichte und
  Entscheidungsvorlagen.
- **Abgrenzung:** Keine primaere Rechenlogik fuer Simulation,
  Wirtschaftlichkeit oder Nachhaltigkeit.
- **Status:** Geplant; Bewertungsregeln und Berichtsumfang muessen separat
  definiert werden.

#### ma_feedback

- **Zweck:** Auffaelligkeiten, Fehler und Optimierungspotenziale in fruehere
  Workflow-Schritte zurueckfuehren.
- **Eingaben:** Import-, Analyse- und Bewertungsergebnisse sowie Warnungen und
  offene Punkte.
- **Ausgaben:** dokumentierte Rueckspruenge, Korrekturauftraege und
  Folgeentscheidungen.
- **Abgrenzung:** Das Modul veraendert nicht automatisch Parameter, Varianten
  oder Modelle.
- **Status:** Geplant; zunaechst als dokumentierter Workflow-Schritt.

#### ma_workflow

- **Zweck:** UI-Aktionen und Fachmodule in der richtigen Reihenfolge
  orchestrieren.
- **Eingaben:** Projektzustand, Benutzeraktionen und neutrale
  Service-Konfigurationen.
- **Ausgaben:** koordinierte Service-Aufrufe, Statusinformationen und
  Workflow-Ergebnisse.
- **Abgrenzung:** Keine eigene Fachberechnung und keine Darstellung.
- **Status:** Teilweise aktiv; Workflow-Katalog, Aktionen und Analyse-Adapter
  sind vorbereitet.

#### ma_ui

- **Zweck:** Zentrale lokale Bedienoberflaeche fuer den Gesamtworkflow.
- **Eingaben:** Benutzerauswahl, Projektzustand und Ergebnisse neutraler
  Services.
- **Ausgaben:** Navigation, Tabellen, Diagrammvorschauen, Statusanzeigen und
  Downloads.
- **Abgrenzung:** Keine Fach-, Analyse-, Varianten- oder Bewertungslogik in
  Streamlit-Komponenten.
- **Status:** Teilweise aktiv; Startdashboard sowie Ansichten fuer Analyse,
  Wetterdaten, Varianten und Bewertung sind vorhanden.

#### ma_ui_legacy

- **Zweck:** Spaeterer Uebergangsbereich fuer bestehende Tkinter-Oberflaechen.
- **Eingaben:** dieselben neutralen Service-Konfigurationen wie `ma_ui`.
- **Ausgaben:** lokale Legacy-Bedienoberflaechen.
- **Abgrenzung:** Keine neue Fachlogik; Tkinter und Streamlit werden nicht
  direkt gekoppelt.
- **Status:** Geplant; die bestehende Tkinter-GUI liegt vorerst weiterhin
  unter `ma_analyse.gui`.

#### ma_shared

- **Zweck:** Wirklich moduluebergreifende technische Hilfen bereitstellen.
- **Eingaben und Ausgaben:** gemeinsame Pfadtypen, Exceptions, Konstanten oder
  neutrale Ergebnisgrundtypen.
- **Abgrenzung:** Kein Sammelordner fuer beliebige Hilfsfunktionen und keine
  Fachlogik.
- **Status:** Geplant; wird nur angelegt, wenn nachweisbare Wiederverwendung
  zwischen mehreren Modulen entsteht.

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
  Factsheets, Ergebnisberichte, Entscheidungsvorlagen
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
| `data/catalogs/documents/` | Struktur fuer Produkt- und Materialdokumente |
| `data/test_output/` | lokaler Arbeits- und Smoke-Test-Bereich |

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

`ma_ui` ist die Zieloberflaeche. Die Startseite zeigt den grafischen Workflow.
Modulseiten zeigen nur modulbezogene Inhalte.

Aktueller Stand:

- `Start`: grafischer Workflow und technische Detailtabellen im Expander
- `Analyse`: Streamlit-Wizard fuer `ma_analyse`, orientiert an Tkinter-Ablauf
- `Wetterdaten`: Analysebereich oben, Wetterdatensatzuebersicht darunter
- `Varianten`: Uebersicht ueber bestehende `ma_variants`-Services
- `Bewertung`: erste Uebersicht ueber Annahmen; langfristig Aufteilung in
  Economy, Sustainability und Assessment
- leere Zielmodule: Titel, Untertitel und blaue Hinweisbox

Tkinter bleibt nutzbar, aber als Legacy-Bestand. Entscheidungen aus Tkinter
werden fachlich ausgewertet und schrittweise in UI-neutrale Logik ueberfuehrt.

### Workflow-Orchestrierung

`ma_workflow` vermittelt zwischen `ma_ui` und den Fachmodulen. Das Modul
koordiniert Reihenfolge, Projektzustand und neutrale Service-Aufrufe, enthaelt
aber keine eigene Fachberechnung und keine Streamlit-Darstellung.

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
- Tkinter bleibt vorerst unter `ma_analyse.gui`; eine Auslagerung nach
  `ma_ui_legacy` erfolgt nur nach separater Freigabe.

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
| Parameter | `ma_parameters` ist das langfristige Zielmodul fuer Parameter- und Optionslogik. | UD-014 |
| UI und Workflow | `ma_ui` ist die Streamlit-Zieloberflaeche; `ma_workflow` bleibt eine getrennte Orchestrierungsschicht. | UD-015, UD-018 |
| Fachlogik | Fachlogik von `ma_analyse` bleibt in `ma_analyse` und wird ueber UI-neutrale Services bereitgestellt. | UD-016, UD-020 |
| Tkinter | Tkinter bleibt Legacy-Bestand und wird nicht technisch mit Streamlit vermischt; es dient nur als fachliche Ablaufvorlage. | UD-019, UD-022 |
| Simulationskette | `ma_simulation_setup` liegt zwischen Variantenbildung und kontrolliertem IDA-Export; Export, Import und Feedback bleiben getrennte Zielbereiche. | UD-017, UD-021 |
| Bewertung | `ma_economy` und `ma_sustainability` sind eigene Fachmodule; `ma_assessment` fuehrt ihre Ergebnisse mit `ma_analyse` zu Bewertung und Berichten zusammen. | UD-036, UD-037 |
| Datenhaltung | Echte Projekt-, Produkt-, Material-, Datenbank- und TRY-Inhalte bleiben lokal; versioniert werden Struktur und gekennzeichnete Beispiele. | UD-012, UD-029 |
| Wetterdiagramme | Wetterdiagramme bleiben vorerst in `ma_weather` und werden nicht sofort in die Analyse-Template-Struktur integriert. | UD-034 |
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
- `plot-template-weather` bleibt offen: Wetterdiagramme bleiben vorerst in
  `ma_weather`, ein eigener UI-Befehl kann spaeter geplant werden.
- Cooling-Trennung relativ/absolut bleibt vorerst in Plot-Templates und wird
  spaeter fuer Hauptbefehl und GUI erneut bewertet.
- Normierung wird `ma_analyse`-weit geplant: absolute Werte, flaechenbezogene
  Werte oder beides brauchen spaeter eine konsistente Strategie.
- `ma_workflow` soll spaeter echte Fachservice-Aufrufe koordinieren.
- `ma_economy`, `ma_sustainability` und `ma_assessment` brauchen vor Codeaufbau
  jeweils eigene Plaene.
- Fuer den Vergleich von Zeit- und Personalkosten sind Wissensprofile,
  Stundensaetze, Prozessgrenzen und Messmethoden noch festzulegen.
