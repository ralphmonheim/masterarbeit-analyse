# Leitfaden zur Strukturierung der Masterarbeit und der begleitenden Software

## 1. Zweck der Software

Die Software dient als unterstützendes Werkzeug für die Masterarbeit im Bereich simulationsgestützte TGA-Planung mit IDA ICE. Sie soll nicht die eigentliche ingenieurfachliche Bewertung ersetzen, sondern den Prozess der Variantenbildung, Simulation, Auswertung und Dokumentation strukturieren.

Der zentrale Zweck besteht darin, verschiedene Gebäude- und TGA-Varianten nachvollziehbar zu erfassen, für IDA ICE vorzubereiten, Simulationsergebnisse geordnet einzulesen und daraus vergleichbare Auswertungen zu erzeugen. Dadurch wird der gesamte Untersuchungsprozess reproduzierbarer, transparenter und besser dokumentierbar.

Die Software unterstützt insbesondere folgende Aufgaben.

* Erfassung und Verwaltung von Parametern
* Aufbau eines Variantenkatalogs
* Strukturierte Ablage von Simulationsläufen
* Vorbereitung von IDA ICE Varianten
* Dokumentation der Simulationsrandbedingungen
* Import und Auswertung von Simulationsergebnissen
* Erstellung von Diagrammen und Vergleichstabellen
* Ableitung von Factsheets für Variantenkatalog, Wirtschaftlichkeit und Nachhaltigkeit
* Unterstützung der Diskussion zur Prozessinnovation in der simulationsgestützten TGA-Planung

Wichtig ist die Abgrenzung. Die Software ist im Rahmen der Masterarbeit kein vollständiges kommerzielles Planungstool und keine vollständige Automatisierung von IDA ICE. Sie ist ein prototypischer Workflow, der zeigt, wie technische Simulation, Datenstruktur, Variantenmanagement und Bewertung systematisch miteinander verbunden werden können.

Empfehlung für die Formulierung im Projektantrag

* Die Software wird als methodisches Hilfsmittel beschrieben.
* Der wissenschaftliche Schwerpunkt bleibt bei der TGA- und Gebäudesimulationsbewertung.
* Die Software dient der Nachvollziehbarkeit, Wiederholbarkeit und strukturierten Auswertung.
* Automatisierung wird als Potenzial betrachtet, nicht als zwingend vollständig umgesetzter Bestandteil.

## 2. Gesamtworkflow der Masterarbeit

Der Gesamtworkflow der Masterarbeit lässt sich in drei übergeordnete Bereiche gliedern.

* Pre-Processing
* Simulation
* Post-Processing

### 2.1 Pre-Processing

Im Pre-Processing werden alle Grundlagen für die Simulation vorbereitet. Dazu gehören Projektinformationen, Parameter, Varianten, Wetterdaten, Simulationsrandbedingungen und gegebenenfalls Exportstrukturen für IDA ICE.

Typische Arbeitsschritte.

* Definition des Referenzgebäudes
* Festlegung der Untersuchungsräume oder Zonen
* Erfassung der relevanten TGA-Parameter
* Erfassung ergänzender Gebäudedaten
* Aufbau des Variantenkatalogs
* Auswahl relevanter Varianten
* Festlegung der Simulationsrandbedingungen
* Zuordnung von Klimadaten oder TRY-Wetterdaten
* Vorbereitung der IDA ICE Modellstruktur
* Dokumentation aller Eingangsdaten

Beispielhafte Parametergruppen.

* Projektdaten
* Standort und Klima
* Geometrie
* Bauteile
* Fenster und Sonnenschutz
* Nutzung und interne Lasten
* Lüftung
* Heizung
* Kühlung
* Raumkomfort
* Simulationszeitraum
* Zeitschritt und Ausgabeintervall

### 2.2 Simulation

Die Simulation erfolgt in IDA ICE. Die Software unterstützt diesen Schritt durch Vorbereitung, Strukturierung und Dokumentation. Der eigentliche Simulationslauf kann im Rahmen der Masterarbeit manuell durchgeführt werden, wenn eine vollständige Automatisierung zu umfangreich wäre.

Typische Arbeitsschritte.

* Öffnen oder Kopieren eines geprüften IDA ICE Referenzmodells
* Anlegen oder Zuordnen der Variante
* Kontrolle der Eingabeparameter
* Durchführung des Simulationslaufs
* Export der relevanten Ergebnisdaten
* Ablage der Ergebnisdateien in einer festen Ordnerstruktur
* Dokumentation von Auffälligkeiten oder Fehlermeldungen

Empfehlung.

* Für jede Variante sollte ein eindeutiger Variantenname verwendet werden.
* Für jeden Simulationslauf sollte ein Run Identifier vergeben werden.
* Eingabedaten, Randbedingungen und Ergebnisdaten sollten getrennt abgelegt werden.
* Manuelle Schritte sollten dokumentiert werden, damit sie wissenschaftlich nachvollziehbar bleiben.

### 2.3 Post-Processing

Im Post-Processing werden die Simulationsergebnisse importiert, bereinigt, analysiert, visualisiert und bewertet. Dieser Bereich ist für die spätere Auswertung der Masterarbeit besonders wichtig.

Typische Arbeitsschritte.

* Import der IDA ICE Ergebnisdaten
* Prüfung auf Vollständigkeit
* Zuordnung zu Projekt, Variante, Raum und Simulationslauf
* Berechnung technischer Kennwerte
* Komfortbewertung
* Vergleich von Varianten
* Erstellung von Diagrammen
* Wirtschaftlichkeitsbewertung
* Nachhaltigkeitsbewertung
* Ableitung einer Vorzugsvariante
* Dokumentation der Ergebnisse

Mögliche Auswertungen.

* Heizbedarf
* Kühlbedarf
* operative Raumtemperatur
* Übertemperaturstunden
* Übertemperaturgradstunden
* CO₂-Konzentration
* PMV und PPD
* Lüftungsvolumenströme
* Systemleistungen
* Energiebedarf nach Variante
* Kostenvergleich
* CO₂-Bewertung im Betrieb

## 3. Modulübersicht

Die Software sollte modular aufgebaut werden. Dadurch bleibt der Code verständlicher, wartbarer und später erweiterbar.

### 3.1 ma_parameters

Dieses Modul verwaltet die Eingangsparameter der Untersuchung.

Aufgaben.

* Einlesen von Parameterlisten
* Strukturierung nach Kategorien
* Prüfung von Pflichtfeldern
* Vorbereitung für Variantenbildung
* Verbindung zu Excel, Datenbank oder JSON-Strukturen

Beispiele für Inhalte.

* Projektname
* Standort
* Gebäudetyp
* Raumdaten
* Nutzungsprofile
* TGA-Systemparameter
* Bauteilkennwerte
* Fensterparameter
* Sonnenschutzparameter

### 3.2 ma_variants

Dieses Modul erzeugt und verwaltet Varianten.

Aufgaben.

* Aufbau des Variantenkatalogs
* Kombination ausgewählter Parameter
* Vergabe eindeutiger Varianten IDs
* Auswahl relevanter Varianten
* Dokumentation der Variantenlogik

Mögliche Auswahlmethoden.

* Vollständige Kombination aller Parameter
* Manuelle Auswahl bestimmter Varianten
* Zufällige Auswahl
* Monte Carlo Auswahl
* Sensitivitätsvarianten
* Regelbasierte Auswahl

Empfehlung.

* Nicht jede theoretisch mögliche Variante muss simuliert werden.
* Die Auswahlstrategie muss begründet werden.
* Die Masterarbeit sollte erklären, warum bestimmte Varianten untersucht werden und andere nicht.

### 3.3 ma_simulation_setup

Dieses Modul definiert die Randbedingungen für den Simulationslauf.

Aufgaben.

* Festlegung des Simulationszeitraums
* Festlegung des Zeitschritts
* Festlegung des Ausgabeintervalls
* Definition von Warmup Perioden
* Zuordnung von Wetterdaten
* Verwaltung von Run Metadaten

Beispielhafte Standardwerte.

* Simulationszeitraum als Ganzjahressimulation
* Startdatum 1. Januar
* Enddatum 31. Dezember
* Ausgabeintervall nach fachlicher Notwendigkeit
* Klimadatei über Wetterdatenordner referenziert

### 3.4 ma_weather

Dieses Modul behandelt Wetterdaten als eigenständigen Eingabebereich.

Aufgaben.

* Ablage und Referenzierung von Klimadateien
* Analyse von TRY-Wetterdaten
* Prüfung relevanter Wetterkennwerte
* Zuordnung zu Standort und Simulationslauf
* Dokumentation der verwendeten Wetterdatei

Wichtig.

* Wetterdaten sind kein Teil der normalen Zonenwertanalyse.
* Wetterdaten bilden ein eigenes Input- und Analysemodul.
* Die Klimadateien sollten über einen dedizierten Wetterdatenordner verwaltet werden.

### 3.5 ma_export_ida

Dieses Modul bereitet die Übergabe an IDA ICE vor.

Aufgaben.

* Erstellen einer Variantenordnerstruktur
* Kopieren eines geprüften Referenzmodells
* Ablage von JSON Metadaten
* Vorbereitung von Exportdateien
* Dokumentation der zu ändernden Parameter

Wichtig.

* Direkte Änderungen an IDM-Dateien sollten nur erfolgen, wenn das Format ausreichend geprüft wurde.
* Für die Masterarbeit kann zunächst ein sicherer Ansatz genutzt werden.
* Der sichere Ansatz ist die Arbeit mit Referenzmodell, Variantenordnern, Metadaten und dokumentierten manuellen Anpassungen.

### 3.6 ma_import_ida

Dieses Modul liest Simulationsergebnisse nach dem IDA ICE Lauf ein.

Aufgaben.

* Import von Ergebnisdateien
* Prüfung auf Vollständigkeit
* Zuordnung zu Variante, Raum und Simulationslauf
* Speicherung in Datenstruktur oder Datenbank
* Vorbereitung für die Analyse

Empfehlung.

* Der Import sollte tolerant gegenüber fehlenden Dateien sein.
* Fehlerhafte oder unvollständige Simulationen sollten markiert, aber nicht stillschweigend ignoriert werden.

### 3.7 ma_analyse

Dieses Modul wertet die Simulationsergebnisse aus.

Aufgaben.

* Berechnung technischer Kennwerte
* Erstellung von Diagrammen
* Vergleich zwischen Varianten
* Analyse einzelner Räume
* Analyse mehrerer Varianten
* Export von Tabellen und Reports

Mögliche Ausgaben.

* Excel Report
* Diagrammordner
* Vergleichstabellen
* Komfortauswertung
* Energieauswertung
* Raumweise Kennwerte
* Variantenvergleich

### 3.8 ma_economy

Dieses Modul kann für die Wirtschaftlichkeitsbewertung ergänzt werden.

Aufgaben.

* Zuordnung von Kostenkennwerten
* Vergleich von Investitionskosten
* Vergleich von Betriebskosten
* Berechnung vereinfachter Lebenszykluskosten
* Bewertung von Varianten aus wirtschaftlicher Sicht

Mögliche Daten.

* Anlagenkosten
* Energiepreise
* Wartungskosten
* Austauschzyklen
* Betriebskosten
* Kosten je Variante

### 3.9 ma_sustainability

Dieses Modul kann für die Nachhaltigkeitsbewertung ergänzt werden.

Aufgaben.

* Bewertung von CO₂-Emissionen im Betrieb
* Zuordnung von Emissionsfaktoren
* Vergleich ökologischer Auswirkungen
* Ergänzung der technischen und wirtschaftlichen Bewertung

Mögliche Daten.

* Strombedarf
* Wärmebedarf
* Kältebedarf
* Energieträger
* Emissionsfaktoren
* CO₂-Emissionen je Variante

## 4. Daten- und Dokumentationsstruktur

Die Datenstruktur sollte so aufgebaut sein, dass alle Arbeitsschritte nachvollziehbar bleiben. Ziel ist eine klare Trennung zwischen Eingaben, Varianten, Simulationen, Ergebnissen und Dokumentation.

### 4.1 Empfohlene Hauptordner

```text
project_root
  data
    input
    weather
    variants
    simulations
    results
    database_exports
  docs
    project_context
    decisions
    workflows
    module_descriptions
    thesis_notes
  src
    ma_parameters
    ma_variants
    ma_simulation_setup
    ma_weather
    ma_export_ida
    ma_import_ida
    ma_analyse
    ma_economy
    ma_sustainability
  outputs
    diagrams
    reports
    factsheets
    logs
  tests
  README.md
  AGENTS.md
```

### 4.2 Datenstruktur für Varianten

Jede Variante sollte eindeutig identifizierbar sein.

Beispiel.

```text
V001_reference
V002_heating_low_temp
V003_cooling_optimized
V004_solar_shading_variant
V005_ventilation_high_efficiency
```

Für jede Variante sollten mindestens folgende Informationen dokumentiert werden.

* Varianten ID
* Variantenname
* geänderte Parameter
* unveränderte Referenzparameter
* zugehörige Wetterdatei
* Simulationszeitraum
* IDA ICE Modellversion
* Status der Simulation
* Speicherort der Ergebnisse
* Bearbeitungsnotizen

### 4.3 Drei zentrale Factsheets

Für die Masterarbeit sollen drei Factsheets aufgebaut werden.

#### Factsheet Variantenkatalog

Inhalt.

* Varianten ID
* Parametergruppe
* geänderte Parameter
* fachliche Begründung
* Bezug zu Heizung, Kühlung, Lüftung, Sonnenschutz, Bauteil oder Standort
* Simulationsstatus
* Ergebnisstatus

Zweck.

* Übersicht über alle untersuchten Varianten
* Nachvollziehbarkeit der Variantenbildung
* Grundlage für Methodik und Auswertung

#### Factsheet Wirtschaftlichkeit

Inhalt.

* Investitionskosten
* Betriebskosten
* Energiekosten
* Wartungskosten
* Lebenszykluskosten
* Kostenkennwert je Variante
* Wirtschaftliche Bewertung

Zweck.

* Ergänzung der rein technischen Bewertung
* Vergleich von Kosten und Nutzen
* Unterstützung bei der Auswahl einer Vorzugsvariante

#### Factsheet Nachhaltigkeit

Inhalt.

* Energiebedarf
* CO₂-Emissionen im Betrieb
* Emissionsfaktoren
* ökologische Bewertung je Variante
* Zusammenhang zwischen Energieeffizienz und Systementscheidung

Zweck.

* Bewertung ökologischer Potenziale
* Einordnung der Varianten unter Nachhaltigkeitsaspekten
* Verbindung zu DGNB, Betriebsemissionen oder Lebenszyklusbetrachtung, sofern im Bearbeitungsumfang enthalten

### 4.4 Dokumentationsstruktur

Die Dokumentation sollte nicht erst am Ende erstellt werden. Sie sollte parallel zur Softwareentwicklung und Simulation wachsen.

Empfohlene Dokumente.

* Projektbeschreibung
* Modulübersicht
* Entscheidungslog
* Datenmodellbeschreibung
* Workflowbeschreibung
* Simulationsprotokoll
* Fehlerprotokoll
* Variantenprotokoll
* Ergebnisprotokoll
* Offene Fragen

Empfehlung für den Ordner decisions.

```text
docs
  decisions
    2026_06_08_weather_module.md
    2026_06_08_module_names.md
    2026_06_09_ui_strategy.md
    2026_06_17_ida_export_strategy.md
```

Jede Entscheidung sollte kurz dokumentiert werden.

* Datum
* Entscheidung
* Begründung
* betroffene Module
* Auswirkungen auf die Masterarbeit
* offene Folgefragen

## 5. UI- und Workflow-Struktur

Die Benutzeroberfläche sollte den Workflow der Masterarbeit abbilden. Sie sollte nicht nur einzelne Funktionen starten, sondern den gesamten Prozess verständlich führen.

### 5.1 Grundidee der UI

Die UI kann als Startoberfläche aufgebaut werden, auf der die wichtigsten Module als Schaltflächen dargestellt sind.

Mögliche Hauptbereiche.

* Projekt laden
* Parameter prüfen
* Varianten erstellen
* Simulationssetup festlegen
* Wetterdaten prüfen
* IDA ICE Export vorbereiten
* Simulationsergebnisse importieren
* Analyse starten
* Wirtschaftlichkeit auswerten
* Nachhaltigkeit auswerten
* Reports und Factsheets erzeugen

### 5.2 Empfohlene Workflow Darstellung

Der Workflow kann in vier Spalten dargestellt werden.

#### Spalte 1 Eingaben

* Projektdaten
* Parameter
* Wetterdaten
* Referenzmodell

#### Spalte 2 Varianten und Setup

* Variantenkatalog
* Variantenwahl
* Simulationsrandbedingungen
* Exportvorbereitung

#### Spalte 3 Simulation und Import

* IDA ICE Simulation
* Ergebnisexport
* Ergebnisimport
* Datenprüfung

#### Spalte 4 Auswertung und Dokumentation

* Analyse
* Diagramme
* Wirtschaftlichkeit
* Nachhaltigkeit
* Factsheets
* Ergebnisbericht

Diese Vier-Spalten-Struktur eignet sich gut für ein Flowchart, eine Streamlit Oberfläche oder eine Dokumentationsgrafik.

### 5.3 Streamlit als mögliche Oberfläche

Streamlit eignet sich für die Masterarbeit, weil damit schnell eine übersichtliche Oberfläche für Datenanalyse, Diagramme und Workflows erstellt werden kann.

Vorteile.

* Gut für Datenanalyse
* Einfache Bedienoberfläche
* Schnelle Entwicklung
* Gute Darstellung von Tabellen und Diagrammen
* Geeignet für Prototypen

Mögliche Struktur.

```text
Startseite
  Projektübersicht
  Workflowstatus

Parameter
  Eingabedaten prüfen
  Parameter anzeigen

Varianten
  Variantenkatalog
  Variantenfilter
  Variantenexport

Simulation
  Simulationssetup
  Exportvorbereitung
  Importstatus

Analyse
  Raumvergleich
  Variantenvergleich
  Diagramme

Bewertung
  Wirtschaftlichkeit
  Nachhaltigkeit
  Vorzugsvariante

Dokumentation
  Logs
  Entscheidungen
  Reports
```

### 5.4 Tkinter und Streamlit

Die bestehende Tkinter GUI kann weiterhin als Vorlage für Logik und Funktionen genutzt werden. Für eine modernere und besser nachvollziehbare Oberfläche kann Streamlit als übergeordnete UI ergänzt werden.

Empfehlung.

* Fachlogik aus der Tkinter GUI herauslösen.
* Analysefunktionen in ma_analyse zentralisieren.
* UI getrennt von Berechnungslogik halten.
* Streamlit als neue Oberfläche für Navigation, Tabellen und Diagramme prüfen.
* Tkinter nicht sofort löschen, sondern zunächst als bestehende Arbeitsversion erhalten.

## 6. Aktuelle Arbeitsroutinen

Für die weitere Bearbeitung der Masterarbeit sollte eine klare Arbeitsroutine eingehalten werden. Dadurch wird verhindert, dass Software, Simulation und Dokumentation auseinanderlaufen.

### 6.1 Routine für neue Funktionen

Jede neue Funktion sollte nach einem festen Schema entwickelt werden.

Ablauf.

* Ziel der Funktion definieren
* Eingangsdaten festlegen
* Ausgangsdaten festlegen
* betroffene Module prüfen
* bestehenden Code analysieren
* Umsetzungsplan schreiben
* Umsetzung durchführen
* Funktion testen
* Ergebnis dokumentieren
* Entscheidung oder Änderung im Changelog festhalten

Empfehlung für VS Code und Codex.

* Erst planen lassen.
* Dann Code ändern.
* Keine großen Änderungen ohne vorherige Strukturprüfung.
* Bestehende Module nicht unnötig vermischen.
* Kommentare im Code ausreichend, aber nicht überladen.
* Nach größeren Änderungen README oder Projektdokumentation aktualisieren.

### 6.2 Routine für Simulationen

Jeder Simulationslauf sollte dokumentiert werden.

Ablauf.

* Variante auswählen
* Parameter prüfen
* Simulationssetup festlegen
* IDA ICE Modell vorbereiten
* Simulation durchführen
* Ergebnisse exportieren
* Ergebnisdateien ablegen
* Import testen
* Plausibilität prüfen
* Auffälligkeiten dokumentieren

Mindestdokumentation pro Simulationslauf.

* Varianten ID
* Simulationsdatum
* verwendete Wetterdatei
* Simulationszeitraum
* IDA ICE Modellversion
* bearbeitende Person
* Status
* Fehler oder Warnungen
* Speicherort der Ergebnisse

### 6.3 Routine für Auswertungen

Ablauf.

* Ergebnisdaten importieren
* Datenstruktur prüfen
* Kennwerte berechnen
* Diagramme erzeugen
* Vergleichstabellen erstellen
* Auffälligkeiten markieren
* Ergebnisse in Factsheets übertragen
* Interpretation separat notieren

Wichtig.

* Diagramme sollten immer eine klare Beschriftung besitzen.
* Achsen, Einheiten, Legenden und Variantenbezeichnungen müssen eindeutig sein.
* Jede Auswertung sollte auf die Forschungsfrage bezogen werden.
* Nicht jedes Diagramm ist automatisch relevant für die Masterarbeit.

### 6.4 Routine für Dokumentation

Die Dokumentation sollte parallel zur Bearbeitung geführt werden.

Empfohlener Rhythmus.

* Nach jeder größeren Softwareänderung eine kurze Notiz.
* Nach jeder Variantenentscheidung ein Eintrag im Entscheidungslog.
* Nach jeder Simulationsserie ein Simulationsprotokoll.
* Nach jeder Auswertung eine kurze Ergebnisnotiz.
* Offene Fragen sofort notieren, nicht nur im Chat stehen lassen.

## 7. Wichtigste Entscheidungen

Die bisher wichtigsten Strukturentscheidungen sind folgende.

### 7.1 Fokus der Masterarbeit

Der Schwerpunkt liegt auf TGA, Gebäudesimulation und simulationsgestützter Optimierung. Baukonstruktion und Materialparameter sind nur dann zentral, wenn sie das TGA-Verhalten, den Energiebedarf oder den Komfort beeinflussen.

Konsequenz.

* Heizung, Kühlung, Lüftung und relevante Systemparameter haben Priorität.
* Fenster und Sonnenschutz können als wichtige Hüllparameter berücksichtigt werden.
* Bauteile und Materialien bleiben sekundär, sofern sie nicht direkt simulationsrelevant sind.

### 7.2 Drei Factsheets

Die Auswertung wird über drei zentrale Factsheets strukturiert.

* Variantenkatalog
* Wirtschaftlichkeit
* Nachhaltigkeit

Konsequenz.

* Die Datenstruktur muss diese drei Bewertungsbereiche unterstützen.
* Technische Simulationsergebnisse müssen mit wirtschaftlichen und ökologischen Kennwerten verknüpfbar sein.
* Die Factsheets können als Brücke zwischen Software, Auswertung und Masterarbeit dienen.

### 7.3 Modulare Softwarestruktur

Die Software wird in einzelne Module gegliedert.

Festgelegte oder bevorzugte Module.

* ma_parameters
* ma_variants
* ma_simulation_setup
* ma_weather
* ma_export_ida
* ma_import_ida
* ma_analyse

Konsequenz.

* Jedes Modul erhält eine klar abgegrenzte Aufgabe.
* Die Software bleibt erweiterbar.
* UI und Fachlogik sollten getrennt werden.

### 7.4 Wetterdaten als eigenes Modul

Wetterdaten werden nicht als Teil der normalen Ergebnisanalyse behandelt, sondern als eigener Input- und Analysebereich.

Konsequenz.

* Klimadateien werden in einem eigenen Wetterdatenordner abgelegt.
* Die Datenbank oder Projektstruktur referenziert diese Dateien.
* TRY-Auswertungen können unabhängig von Zonenwerten entwickelt werden.

### 7.5 IDA ICE Export und Import getrennt

Export und Import werden als getrennte Module betrachtet.

Konsequenz.

* ma_export_ida behandelt die Vorbereitung vor der Simulation.
* ma_import_ida behandelt die Ergebnisdaten nach der Simulation.
* Dadurch bleibt der Workflow sauber zwischen Pre-Processing, Simulation und Post-Processing getrennt.

### 7.6 Automatisierung mit begrenztem Umfang

Eine vollständige Automatisierung von IDA ICE ist für die Masterarbeit nicht zwingend erforderlich. Manuelle Schritte sind zulässig, wenn sie sauber dokumentiert werden.

Konsequenz.

* Der wissenschaftliche Wert liegt nicht nur in der Automatisierung, sondern in der strukturierten Methodik.
* Automatisierungspotenziale können in Kapitel 4 Prozessinnovation diskutiert werden.
* Kritische Schnittstellen wie IDM-Bearbeitung sollten vorsichtig behandelt werden.

### 7.7 Kapitel 4 als Zukunfts- und Prozesskapitel

Kapitel 4 soll nicht nur Methodik, Auswertung und Ergebnis wiederholen. Es soll zeigen, wie ein zukünftiger simulationsgestützter Workflow aussehen kann.

Inhalte.

* Pre-Processing
* Simulation
* Post-Processing
* Automatisierungspotenziale
* KI-Unterstützung
* Grenzen der Automatisierung
* Nutzen für TGA-Planung
* Risiken und offene Anforderungen

## 8. Offene Strukturpunkte

Es gibt mehrere offene Punkte, die vor oder während der weiteren Bearbeitung geklärt werden sollten.

### 8.1 Umfang der IDA ICE Automatisierung

Offene Frage.

* Soll Python IDM-Dateien direkt schreiben oder nur Variantenordner und Metadaten vorbereiten?

Empfehlung.

* Für die Masterarbeit zunächst den sicheren Workflow verwenden.
* Direkte IDM-Manipulation nur als optionales Potenzial behandeln.
* Vorlagen und Referenzmodelle verwenden, statt unkontrolliert Modellinformationen zu verändern.

### 8.2 Datenbankumfang

Offene Frage.

* Wird PostgreSQL vollständig umgesetzt oder zunächst eine einfachere Dateistruktur genutzt?

Empfehlung.

* Für die Masterarbeit eine klare Datenstruktur definieren.
* PostgreSQL als Zielstruktur oder erweiterbare Option beschreiben.
* Bei begrenzter Zeit JSON, CSV oder Excel als Zwischenschritt nutzen.

### 8.3 Auswahlstrategie der Varianten

Offene Frage.

* Wie viele Varianten werden tatsächlich simuliert und nach welcher Logik werden sie ausgewählt?

Empfehlung.

* Auswahlstrategie schriftlich festlegen.
* Nicht nur technische Machbarkeit, sondern wissenschaftliche Aussagekraft bewerten.
* Sensitivitätsvarianten gezielt einsetzen.

### 8.4 Verbindung zwischen Simulation, Wirtschaftlichkeit und Nachhaltigkeit

Offene Frage.

* Welche technischen Kennwerte fließen konkret in Wirtschaftlichkeit und Nachhaltigkeit ein?

Empfehlung.

* Früh eine Kennwertmatrix erstellen.
* Für jeden Kennwert definieren, aus welcher Quelle er stammt.
* Für jede Bewertung festlegen, ob sie berechnet, geschätzt oder qualitativ bewertet wird.

Beispiel.

```text
Heizenergiebedarf
  Quelle IDA ICE Ergebnis
  Nutzung Wirtschaftlichkeit über Energiekosten
  Nutzung Nachhaltigkeit über CO₂ Faktor

Kühlenergiebedarf
  Quelle IDA ICE Ergebnis
  Nutzung Wirtschaftlichkeit über Stromkosten
  Nutzung Nachhaltigkeit über Stromemissionsfaktor

Anlagenleistung
  Quelle IDA ICE oder Dimensionierung
  Nutzung Wirtschaftlichkeit über Investitionskosten
  Nutzung Nachhaltigkeit optional über Systemvergleich
```

### 8.5 UI Zielbild

Offene Frage.

* Soll die finale Oberfläche in Tkinter, Streamlit oder nur als Skriptstruktur umgesetzt werden?

Empfehlung.

* Für die Masterarbeit ist Streamlit als übersichtliche Prototypoberfläche geeignet.
* Tkinter kann als bestehende Arbeitsversion erhalten bleiben.
* Die Fachlogik sollte unabhängig von der Oberfläche funktionieren.

### 8.6 Dokumentation der eigenen Entscheidungen

Offene Frage.

* Wo werden Entscheidungen dokumentiert, die aus Chats, Codex oder manueller Arbeit entstehen?

Empfehlung.

* Einen festen Ordner docs decisions verwenden.
* Jede wesentliche Entscheidung als kurze Markdown Datei speichern.
* Entscheidungen nicht nur im Chat belassen.

### 8.7 Abgrenzung der Masterarbeit

Offene Frage.

* Wie weit gehen Wirtschaftlichkeit und Nachhaltigkeit?

Empfehlung.

* Wirtschaftlichkeit und Nachhaltigkeit als ergänzende Bewertungsdimensionen behandeln.
* Der Schwerpunkt bleibt technische Simulation und TGA-Optimierung.
* CO₂-Emissionen im Betrieb können sinnvoll ergänzt werden.
* Vollständige Ökobilanz nur aufnehmen, wenn Datenbasis und Zeitrahmen ausreichen.

## 9. Empfohlene nächste Arbeitsschritte

### Schritt 1 Projektstruktur festlegen

Zuerst sollte die endgültige Ordner- und Modulstruktur im Projekt festgelegt werden. Diese Struktur bildet die Grundlage für VS Code, Codex, Dokumentation und spätere Auswertung.

Ergebnis.

* feste Ordnerstruktur
* feste Modulnamen
* README aktualisiert
* AGENTS.md oder Projektanweisung aktualisiert

### Schritt 2 Datenmodell skizzieren

Danach sollte das Datenmodell für Variantenkatalog, Wirtschaftlichkeit und Nachhaltigkeit erstellt werden.

Ergebnis.

* Tabellenstruktur
* Parametergruppen
* Beziehungen zwischen Variante, Simulation, Ergebnis und Bewertung
* eindeutige IDs

### Schritt 3 Workflowdiagramm erstellen

Der Gesamtprozess sollte als Vier-Spalten-Workflow visualisiert werden.

Spalten.

* Eingaben
* Varianten und Setup
* Simulation und Import
* Auswertung und Dokumentation

Ergebnis.

* Flowchart für Masterarbeit
* Grundlage für Kapitel Methodik
* Grundlage für UI Struktur

### Schritt 4 Minimale funktionsfähige Software definieren

Es sollte festgelegt werden, welche Funktionen zwingend umgesetzt werden müssen.

Mindestumfang.

* Parameter einlesen
* Varianten verwalten
* Simulationssetup dokumentieren
* Ergebnisse importieren
* Analyse durchführen
* Diagramme erzeugen
* Factsheets vorbereiten

### Schritt 5 Erweiterungen priorisieren

Erweiterungen sollten erst nach dem Mindestumfang umgesetzt werden.

Mögliche Erweiterungen.

* direkter IDA ICE Export
* automatisierter Import
* PostgreSQL Datenbank
* Streamlit Oberfläche
* Wirtschaftlichkeitsmodul
* Nachhaltigkeitsmodul
* Wetterdatenanalyse

## 10. Kernaussage für die Masterarbeit

Die begleitende Software bildet einen strukturierten Workflow für simulationsgestützte Variantenuntersuchungen in der TGA-Planung ab. Sie verbindet Parameterdefinition, Variantenmanagement, IDA ICE Simulation, Ergebnisanalyse sowie wirtschaftliche und ökologische Bewertung. Damit unterstützt sie nicht nur die fachliche Auswertung der Varianten, sondern zeigt auch, wie zukünftige Planungsprozesse durch strukturierte Datenmodelle, Automatisierung und digitale Workflows verbessert werden können.
