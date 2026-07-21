# Projektplan für die VS-Code-Umsetzung der Masterarbeitssoftware

Stand 23. Juni 2026

## Verbindliche Einordnung

Der Projektplan dient als verbindliche Planungsgrundlage für die weitere
Entwicklung der Masterarbeitssoftware.

Vor jeder Umsetzung ist zunächst die vorhandene VS-Code-Projektstruktur zu
analysieren. Die im Projektplan beschriebene Modulstruktur ist eine fachliche
Zielstruktur und darf nicht ungeprüft als parallele neue Ordnerstruktur
angelegt werden.

Die Umsetzung erfolgt schrittweise nach dem Prinzip Analyse, Planung,
Freigabe, Umsetzung, Test und Dokumentation.

## Konsolidierungsstand

P007 ersetzt die strukturellen Zielbilder aus P005 und P006. Die
Originalplaene bleiben unveraendert im Planarchiv. P008 fuehrt
`ma_weather` weiter. P010 bis P028 konkretisieren die Eingabekette,
Analysestufen, Demo-/Konzeptmodule und Querschnittsfunktionen. P009 wird erst
nach dem Run-Manifest aus P018 technisch fortgesetzt.

Die Zielmodule werden frueh als leichte importierbare Pakete, dokumentierte
Moduldefinitionen und klickbare Dashboard-Infoseiten sichtbar gemacht.
Paketexistenz allein bedeutet nicht, dass ein Modul fachlich umgesetzt ist.

## Masterarbeitsprioritaet

Die Masterarbeit verbindet einen manuellen fachlichen Referenzprozess mit der
softwaregestuetzten Prozessinnovation. Bis zum Abschluss haben daher nur
Arbeiten Vorrang, die Baseline oder Varianten, wiederholbare Auswertungen,
Prozessdaten oder direkt verwendbare Tabellen und Abbildungen erzeugen. Der
manuelle IDA-ICE-Ablauf bleibt fachliche Referenz und wird nicht durch
Automatisierung ersetzt.

Der produktive Schwerpunkt reicht bis `ma_simulation_setup`:

- Eingabequellen und Randbedingungen
- Projekt, Gebaeude, Wetter, Zonen und Technik
- zentrale Parameterliste
- vereinfachte Referenzdimensionierung mit Ausbaupfad
- Varianten und Naming
- validiertes Run-Manifest

`ma_building` und `ma_zones` werden mindestens konzeptuell und mit
Demo-Datensaetzen umgesetzt. Ein IFC-Lite-Adapter bleibt bis zur Analyse
konkreter IFC-Arbeitsstaende offen. CAD-Integration, automatische
IDA-Steuerung und ungesicherte Modellmanipulation gehoeren nicht zum
Masterarbeitskern.

## 1. Ziel des Projektplans

Dieser Projektplan beschreibt die schrittweise Überführung der bisher entwickelten fachlichen und organisatorischen Struktur in eine belastbare VS-Code-Projektarchitektur.

Die Software soll den vollständigen Workflow einer simulationsgestützten TGA-Untersuchung unterstützen. Sie umfasst Projektinitialisierung, Eingangsdaten, Referenzdimensionierung, Variantenbildung, Simulationsvorbereitung, manuellen Simulationsdurchlauf in IDA ICE, Ergebnisimport, technische Analyse, Wirtschaftlichkeit, Nachhaltigkeit, Gesamtbewertung, Reporting und Datenexport.

Die Softwarearchitektur soll grundsätzlich simulationsprogrammunabhängig bleiben. Für die Masterarbeit wird zunächst ausschließlich IDA ICE angebunden.

## 2. Projektumfang

### Im aktuellen Kernumfang

- Projektanlage und Projektkonfiguration
- zentrale Benennungs-, Pfad- und ID-Regeln
- Erfassung von Gebäude-, Wetter-, Zonen- und Technikdaten
- Zusammenführung aller Eingaben in einer zentralen Parameterliste
- Referenzdimensionierung
- Variantenbildung und Variantenauswahl
- Run-basierte Simulationskonfiguration
- Vorbereitung des Exports nach IDA ICE
- manuelle Simulation in IDA ICE
- Import und Vereinheitlichung der Simulationsergebnisse
- vierstufige technische Analyse
- Wirtschaftlichkeitsbewertung
- Nachhaltigkeitsbewertung
- Gesamtbewertung
- Reporting
- Datenexport
- Validierung, Feedback und Dokumentation
- Streamlit als Hauptoberfläche
- Tkinter als Ersatzoberfläche für `ma_analyse`

### Nicht im aktuellen Kernumfang

- automatische Steuerung von IDA ICE
- vollständige automatische Bearbeitung aller IDA-ICE-Dateien
- vollständige Unterstützung weiterer Simulationsprogramme
- direkte CAD-Integration und CAD-Modellerstellung
- verpflichtender vollstaendiger IFC-Import
- vollständige Ökobilanz aller Bauteile und Anlagen
- vollständig automatisierter Final Report als fertiger wissenschaftlicher Text

## 3. Architekturgrundsätze

### 3.1 Programmunabhängige Kernstruktur

Die allgemeinen Module bleiben unabhängig vom Simulationsprogramm.

Dazu gehören insbesondere

- `ma_core`
- `ma_project`
- `ma_building`
- `ma_weather`
- `ma_zones`
- `ma_technical`
- `ma_parameters`
- `ma_variants`
- `ma_simulation_setup`
- `ma_analyse`
- `ma_economy`
- `ma_sustainability`
- `ma_assessment`
- `ma_reporting`
- `ma_data_export`
- `ma_validation`
- `ma_feedback`

IDA ICE wird ausschließlich über Adapter innerhalb von `ma_export_simulation` und `ma_import_simulation` angebunden.

### 3.2 Fachlogik unabhängig von der Benutzeroberfläche

Die fachliche Logik darf nicht direkt in Streamlit oder Tkinter liegen.

Streamlit und Tkinter rufen dieselben Funktionen aus den Fachmodulen auf.

```text
Streamlit
→ Fachmodule

Tkinter
→ dieselben Fachmodule
```

### 3.3 Bestehende VS-Code-Struktur zuerst analysieren

Vor jeder größeren Umstrukturierung muss die vorhandene Projektstruktur analysiert werden.

Es soll keine parallele zweite Projektstruktur entstehen.

Neue Unterbereiche werden in die vorhandenen Module, Ordner, Datenpfade und Namenskonventionen eingeordnet.

### 3.4 Manuelle Simulation als externer Prozess

Der Simulationsschritt bleibt zunächst manuell.

```text
ma_export_simulation
→ manuelle Simulation in IDA ICE
→ ma_import_simulation
```

### 3.5 Zentrale Parameterquelle

`ma_parameters` ist die zentrale Quelle für `ma_variants`.

`ma_variants` greift nicht direkt auf `ma_weather`, `ma_building`, `ma_zones` oder `ma_technical` zu.

## 4. Phase 0 und sechs Hauptphasen

### Phase 0 Technische Plattform

Bereiche

- `ma_core`
- `ma_database`
- `ma_ui`
- `ma_workflow`
- Dokumentationsinfrastruktur unter `docs`

Ziele

- gemeinsame technische Regeln und Konfigurationen bereitstellen
- Projektmodule und Status zentral katalogisieren
- Dashboard und Modul-Infoseiten bereitstellen
- Persistenzgrenzen vorbereiten
- Planung, Entscheidungen und Architektur nachvollziehbar dokumentieren

### Phase 1 Projektinitialisierung

Module

- `ma_project`

Ziele

- Projekt anlegen
- Simulationsprogramm festlegen
- Standardvorlagen laden
- Pfade, IDs und Benennungen festlegen
- Untersuchungsrandbedingungen dokumentieren
- Bewertungsziele und Gewichtungsszenarien referenzieren

### Phase 2 Eingangsdaten und Pre-Processing

Module

- `ma_building`
- `ma_weather`
- `ma_zones`
- `ma_technical`
- `ma_parameters`

Ziele

- Eingabedaten vollständig erfassen
- Daten fachlich prüfen
- Daten vereinheitlichen
- zentrale Parameterliste erzeugen
- Freigabe für Dimensionierung und Variantenbildung erzeugen

### Phase 3 Variantenbildung und Simulationsvorbereitung

Module

- `ma_analyse.stage_1_dimensioning`
- `ma_variants`
- `ma_simulation_setup`
- `ma_export_simulation`

Ziele

- Referenz dimensionieren
- Variantenraum definieren
- zulässige Varianten erzeugen
- Varianten auswählen
- Run anlegen
- gemeinsame Simulationskonfiguration festlegen
- Export für IDA ICE vorbereiten

### Festlegung Masterarbeits-MVP V1

Der erste verbindliche Masterarbeits-MVP erzeugt fuer eine freigegebene
Baseline und eine kleine explizite Variantenstudie erste Simulationszahlen,
ein begrenztes Diagrammpaket und einen nachvollziehbaren Zeit-/Aufwands-
vergleich. Er trennt dabei Produktivsoftware, manuelle IDA-ICE-Simulation und
Forschungsauswertung klar.

`Preprocess V1` ist darin der erste Teilmeilenstein. Er endet mit einem
validierten, reproduzierbaren neutralen Run-Paket einschliesslich
`RunManifest`, Setup, Variantenartefakten und technischen Logs sowie einer
dokumentierten manuellen Uebergabe an IDA ICE.

Die verbindliche Reihenfolge lautet:

```text
ma_project
-> ma_weather
-> ma_building
-> ma_technical
-> ma_zones
-> ma_parameters
-> ma_analyse.stage_1_dimensioning
-> ma_variants
-> ma_simulation_setup
-> neutrales Run-Paket
-> manuelle IDA-ICE-Simulation
-> manueller neutraler Ergebnisimport
-> einfache Analyse und Diagramme
-> P030 Prozessauswertung
```

Nicht Teil dieses Meilensteins sind ein produktiver IFC-/Rhino-Import, ein
IDA-ICE-Adapter, automatisierte Modellmanipulation, technische Produktkataloge,
Branches oder ein vollstaendiger Technikeditor. Die manuelle IDA-Uebergabe
referenziert die nach P018 erforderliche Compliance-Entscheidung.

### MVP-V1-Abnahme

- mindestens eine freigegebene Baseline und eine explizite Variante,
- validiertes P018-Run-Paket mit `RUN-ID`, `VAR-ID` und technischen Logs,
- dokumentierte manuelle Simulation,
- ein freigegebenes manuelles Ergebnisformat und neutrale RUN/VAR-Zuordnung,
- drei Diagrammtypen: Heiz-/Kuehllast, Raumklima/Komfort sowie Jahres- oder
  Spitzenwertvergleich,
- getrennte Prozessdaten fuer Preprocessing, Simulation und Postprocessing,
  einschliesslich Nutzer-, Maschinen-, Pruef- und Korrekturzeit.

### Phase 4 Simulation und technische Analyse

Schritte und Module

- manuelle Simulation in IDA ICE
- `ma_import_simulation`
- `ma_analyse.stage_2_optimization`
- `ma_analyse.stage_3_standards_compliance`
- `ma_analyse.stage_4_sensitivity`

Ziele

- Ergebnisse importieren
- Daten vereinheitlichen
- erste Last-, Raumklima- und Spitzenwertdiagramme auswerten
- technische Optimierung erst nach dem MVP auswerten
- Varianten nach deutschen Normen nachweisen
- spaetere internationale Normenprofile ermoeglichen
- Sensitivität und Robustheit untersuchen

### Phase 5 Wirtschaftlichkeit, Nachhaltigkeit und Gesamtbewertung

Module

- `ma_economy`
- `ma_sustainability`
- `ma_assessment`

Ziele

- Kosten bewerten
- ökologische Auswirkungen bewerten
- technische, wirtschaftliche und ökologische Ergebnisse zusammenführen
- Vorzugsvarianten oder Pareto-Lösungen bestimmen

### Phase 6 Reporting, Datenexport und Dokumentation

Module

- `ma_reporting`
- `ma_data_export`
- Projektdokumentation und Archivierung

Ziele

- Berichte und Factsheets erzeugen
- Datenpakete exportieren
- Projektstand archivieren
- Entscheidungen und Änderungen nachvollziehbar dokumentieren

### Phasenübergreifende Funktionen

- `ma_validation` sammelt lokale Prüfergebnisse und verwaltet
  modulübergreifende Freigaben.
- `ma_feedback` klassifiziert Auffälligkeiten und steuert dokumentierte
  Rücksprünge in verantwortliche Module.
- Fachregeln und lokale Validierungen bleiben in den jeweiligen Fachmodulen.

## 5. Fachliche Zielstruktur

```text
src
  ma_core
  ma_database
  ma_ui
  ma_workflow
  ma_project
  ma_building
  ma_weather
  ma_zones
  ma_technical
  ma_parameters
  ma_variants
  ma_simulation_setup
  ma_export_simulation
  ma_import_simulation
  ma_analyse
  ma_economy
  ma_sustainability
  ma_assessment
  ma_reporting
  ma_data_export
  ma_validation
  ma_feedback
```

Diese Darstellung ist eine fachliche Zielstruktur. Die tatsächliche Dateistruktur wird an das bestehende VS-Code-Projekt angepasst.

Die Projektdokumentation bleibt unter `docs` und wird nicht als künstliches
Python-Paket `ma_documentation` angelegt.

## 6. Modulplan

### 6.1 `ma_core`

Aufgaben

- allgemeine Pfadregeln
- Benennungsregeln
- ID-Grundregeln
- Konfiguration
- Logging
- Vorlagenverwaltung
- Adapterregistrierung
- Versionierung
- allgemeine Hilfsfunktionen

Es wird eine Standardvorlage verwendet, die beim Projektstart projektspezifisch kopiert und anschließend angepasst werden kann.

### 6.2 `ma_database`

Aufgaben

- spätere modulübergreifende Persistenz kapseln
- Repository-Schnittstellen vorbereiten
- Projekt-, Run- und Ergebnisbezüge dauerhaft speichern
- bestehende Datenbanklogik erst nach eigenem Migrationsplan übernehmen

Die vorhandene SQLAlchemy- und Alembic-Logik in `ma_variants` bleibt bis zu
einer separaten Freigabe unverändert.

### 6.3 `ma_project`

Aufgaben

- Projektstammdaten
- Untersuchungsziel
- Bilanzgrenzen
- frei erweiterbare Simulationsprogrammliste und aktive Auswahl
- Referenzmodell
- neutrales Varianten-Benennungsprofil
- Projektstatus
- verwendete Vorlagen
- Bewertungsziele
- Gewichtungsszenarien
- Dokumentationspfade

Für die Masterarbeit gilt IDA ICE als Projektstandard.
Weitere Programme duerfen als neutrale Projektprofile erfasst werden, ohne
dass dadurch bereits ein technischer Adapter vorhanden ist.

### 6.4 `ma_building`

Verbindliche Unterstruktur

```text
ma_building
  ma_building_model
  ma_building_components
  ma_building_validation
```

`ma_building_model`

- Gebäudemodell importieren oder erfassen
- SketchUp, IFC, IDA-ICE-Modell oder tabellarische Eingabe
- Gebäude, Geschosse, Räume, Flächen, Volumen
- Orientierung
- Wände und Fenster
- Bauteilreferenzen

`ma_building_components`

- Bauteile
- Schichten
- Materialien
- U-Werte
- bauphysikalische Kennwerte
- projektspezifische Erstellung
- Auswahl aus Vorlagen

`ma_building_validation`

- Geometrieprüfung
- Referenzprüfung
- Material- und Bauteilzuweisung
- Vollständigkeit
- Plausibilität
- Freigabe

### 6.5 `ma_weather`

Verbindliche Unterstruktur

```text
ma_weather
  ma_weather_location
  ma_weather_dataset
  ma_weather_analysis
  ma_weather_validation
```

Aufgaben

- informative Deutschlandkarte anzeigen
- Standort oder meteorologische Zone über Auswahlfeld festlegen
- Wetterdatensätze filtern
- bereitgestellte TRY-Dateien verwalten
- mehrere Standorte berücksichtigen
- Zukunftsklimadaten berücksichtigen
- Wetterdaten analysieren
- Extremtage erkennen
- Default-Datensatz für Referenz und Stufe 1 festlegen
- Varianten dürfen Standort und Wetterdatensatz überschreiben
- spätere Importfunktion vorbereiten

### 6.6 `ma_zones`

Aufgaben

- thermische Zonen definieren
- Räume Zonen zuordnen
- Nutzungen definieren
- Sollwerte definieren
- interne Lasten definieren
- Komfortanforderungen definieren
- Nutzungs- und Betriebsprofile verwalten
- zonenspezifische Anforderungen an `ma_technical` bereitstellen

### 6.7 `ma_technical`

Mögliche Unterstruktur

```text
ma_technical
  ma_technical_generation
  ma_technical_distribution
  ma_technical_zone_supply
  ma_technical_control
  ma_technical_components
  ma_technical_validation
```

Aufgaben

- Referenzsysteme definieren
- Wärmeerzeugung
- Kälteerzeugung
- Lüftung
- Verteilung
- Übergabesysteme
- Steuerung je Zone
- Produkte und Komponenten
- technische Betriebsparameter
- technische Plausibilitätsprüfung

### 6.8 `ma_parameters`

Aufgaben

- Eingaben aus `ma_weather`, `ma_building`, `ma_zones` und `ma_technical` zusammenführen
- IDs vereinheitlichen
- Einheiten vereinheitlichen
- Quellen dokumentieren
- Referenzwerte markieren
- Defaultwerte verwalten
- Vorschlagswerte aus Stufe 1 speichern
- variantentaugliche Parameter markieren
- Optionsgruppen und ausgewaehlte Werte verwalten
- zentrale Parameterliste erzeugen

### 6.9 `ma_variants`

Verbindliche Unterstruktur

```text
ma_variants
  ma_variant_space
  ma_variant_values
  ma_variant_rules
  ma_variant_generation
  ma_variant_selection
  ma_variant_validation
```

Aufgaben

- variierbare Parameter festlegen
- Wertelisten definieren
- Datenbankwerte einlesen
- eigene Werte ergänzen
- Abhängigkeiten definieren
- Ausschlussregeln definieren
- Varianten erzeugen
- Varianten auswählen
- Varianten validieren
- neutrales Benennungsprofil aus `ma_project` anwenden

Eingangsquelle ist ausschließlich `ma_parameters`.
Das Benennungsprofil wird von `ma_project` referenziert. Produkt-,
Material- und programmspezifische Exportbezeichnungen gehoeren nicht zu
`ma_variants`.

### 6.10 `ma_simulation_setup`

Aufgaben

- Run anlegen
- Varianten für den Run auswählen
- gemeinsamen Simulationszeitraum festlegen
- Default Ganzjahressimulation
- Zeitschritt festlegen
- Ausgabeintervall festlegen
- Berichte und Datensätze festlegen
- Untersuchungszweck dokumentieren
- gemeinsame Simulationskonfiguration für alle Varianten des Runs erzeugen

Ein Run umfasst mehrere ausgewählte Varianten und eine gemeinsame Simulationskonfiguration.

### 6.11 `ma_export_simulation`

Mögliche Unterstruktur

```text
ma_export_simulation
  ma_export_preparation
  ma_export_mapping
  adapters
    ida_ice
  ma_export_validation
```

Aufgaben

- Run vorbereiten
- Variantenfälle vorbereiten
- Referenzmodell zuordnen
- Parameterlisten erzeugen
- Änderungslisten erzeugen
- Checklisten erzeugen
- IDA-ICE-Mapping anwenden
- notwendige Berichte dokumentieren
- Export prüfen

### 6.12 `ma_import_simulation`

Mögliche Unterstruktur

```text
ma_import_simulation
  ma_import_discovery
  adapters
    ida_ice
  ma_import_mapping
  ma_import_processing
  ma_import_validation
```

Aufgaben

- Ergebnisdateien finden
- Run und Varianten zuordnen
- IDA-ICE-Dateien einlesen
- Namen und Einheiten vereinheitlichen
- Zeitstempel vereinheitlichen
- Räume, Zonen und Systeme zuordnen
- Rohdaten sichern
- Analysedaten erzeugen
- Import validieren

### 6.13 `ma_analyse`

Verbindliche Struktur

```text
ma_analyse
  stage_1_dimensioning
  stage_2_optimization
  stage_3_standards_compliance
  stage_4_sensitivity
  gemeinsame Bereiche
    analysis_data
    analysis_plots
    analysis_export
    analysis_validation
```

Stufe 1

- vollständige Dimensionierung der Referenz
- Heizlast
- Kühllast
- Luftvolumenströme
- Anlagenleistungen
- Normen und Berechnungsverfahren bleiben offen
- optionale erneute Dimensionierung von Varianten im Post-Processing

Stufe 2

- Variantenvergleich
- Energie
- Leistung
- Komfort
- CO₂
- PMV und PPD
- Übertemperatur
- Anlagen- und Regelungsverhalten
- Optimierungspotenziale

Stufe 3 - Standards Compliance / Norm-Nachweis

- deutsche Normen und normierte Berechnungsverfahren als erster Pflichtumfang
- internationale Normen als spaetere austauschbare Profile
- Quellenmatrix mit Norm, Ausgabe, Abschnitt und Anwendungsbereich
- Norm- und Grenzwertpruefung
- Komfortnachweis
- Temperatur
- CO₂
- PMV und PPD
- Übertemperaturgradstunden
- Heiz-, Kühl- und Lüftungsnachweise
- Ergebnisstatus `pass`, `fail`, `warning` oder `not_evaluable`
- keine allgemeine Modellverifikation

Stufe 4

- Zukunftsklima
- Extremtage
- andere Standorte
- Sollwerte
- Nutzungsprofile
- interne Lasten
- technische Leistungen
- Bauteile und Fenster
- Robustheit
- Parametereinfluss

### 6.14 `ma_economy`

Mögliche Unterstruktur

```text
ma_economy
  ma_economy_inputs
  ma_investment_costs
  ma_operating_costs
  ma_lifecycle_costs
  ma_economy_comparison
  ma_economy_validation
```

### 6.15 `ma_sustainability`

Mögliche Unterstruktur

```text
ma_sustainability
  ma_sustainability_inputs
  ma_operational_emissions
  ma_embodied_impacts
  ma_sustainability_comparison
  ma_sustainability_validation
```

### 6.16 `ma_assessment`

Mögliche Unterstruktur

```text
ma_assessment
  ma_assessment_inputs
  ma_assessment_criteria
  ma_assessment_normalization
  ma_assessment_weighting
  ma_assessment_scoring
  ma_assessment_comparison
  ma_assessment_validation
```

### 6.17 `ma_reporting`

Mögliche Unterstruktur

```text
ma_reporting
  ma_report_templates
  ma_preliminary_reports
  ma_analysis_reports
  ma_factsheets
  ma_final_report
  ma_reporting_validation
```

### 6.18 `ma_data_export`

Mögliche Unterstruktur

```text
ma_data_export
  ma_export_selection
  ma_export_formats
  ma_export_packages
  ma_export_archive
  ma_data_export_validation
```

### 6.19 `ma_validation`

Aufgaben

- lokale Prüfergebnisse sammeln
- modulübergreifende Konsistenz prüfen
- Prozessfreigaben erzeugen
- blockierende Fehler unterscheiden
- Status verwalten

### 6.20 `ma_feedback`

Aufgaben

- Fehler anzeigen
- Warnungen anzeigen
- Hinweise anzeigen
- Bestätigungen einholen
- Rücksprung zum zuständigen Modul ermöglichen
- Freigabestatus darstellen

### 6.21 `ma_ui`

Mögliche Unterstruktur

```text
ma_ui
  streamlit_ui
  tkinter_ui
```

Aufgaben

- Workflow darstellen
- Module aufrufen
- Status anzeigen
- Eingaben verwalten
- Ergebnisse darstellen
- keine eigene Fachlogik

### 6.22 `ma_workflow`

Aufgaben

- Phase 0 und die sechs fachlichen Phasen katalogisieren
- Moduldefinitionen und Umsetzungsstatus zentral bereitstellen
- Dashboard-Aktionen auf Fachservices abbilden
- Phasenfreigaben und Rücksprünge koordinieren
- historische Schlüssel kontrolliert auf kanonische Schlüssel abbilden

`ma_workflow` enthält keine Fachberechnung und keine Streamlit-Darstellung.

### 6.23 Projektdokumentation

Aufgaben

- P007 und aktive Teilpläne pflegen
- technische und fachliche Entscheidungen dokumentieren
- Changelog, Leitfaden, Architektur und Testnachweise aktuell halten
- ersetzte Pläne und Workflowstände unverändert archivieren

Die Projektdokumentation liegt unter `docs` und ist kein Python-Paket.

## 7. Datenfluss

```text
ma_weather
ma_building
ma_zones
ma_technical

→ ma_parameters

→ ma_analyse.stage_1_dimensioning

→ ma_variants

→ ma_simulation_setup

→ ma_export_simulation

→ manuelle IDA-ICE-Simulation

→ ma_import_simulation

→ ma_analyse.stage_2_optimization
→ ma_analyse.stage_3_standards_compliance
→ ma_analyse.stage_4_sensitivity

→ ma_economy
→ ma_sustainability

→ ma_assessment

→ ma_reporting
→ ma_data_export
→ Projektdokumentation und Archivierung
```

`ma_validation` und `ma_feedback` wirken phasenübergreifend auf diesen
Datenfluss und sind keine einmalig zu durchlaufenden Endschritte.

## 8. IDs, Runs und Varianten

Festgelegt

- projektweit eindeutige Varianten-IDs
- projektweit eindeutige Run-IDs
- fortlaufende Nummerierung
- keine Wiederverwendung vergebener IDs
- keine Überschreibung bereits exportierter oder simulierter Inhalte
- neue fachliche Version führt zu neuer Variante oder neuem Run

Noch offen

- konkrete Präfixe
- Stellenzahl
- Statusbezeichnungen
- Case- oder Execution-ID
- konkrete Dateinamenregeln

## 9. Umsetzungspakete für VS Code

### Arbeitspaket 0 Strukturkonsolidierung

Status: abgeschlossen am 2026-06-21

- P002, P005 und P006 unverändert archivieren
- P008 und P009 als neue Teilpläne anlegen
- leichte Zielpakete ohne vorgetäuschte Fachlogik anlegen
- zentralen Phasen-, Modul- und Statuskatalog in `ma_workflow` aufbauen
- Dashboard auf Phase 0 und sechs Hauptphasen umstellen
- für jedes Modul eine klickbare Fach- oder Infoseite bereitstellen

### Arbeitspaket 1 Bestandsanalyse

Status: für die Strukturkonsolidierung aktualisiert; vor jedem weiteren
Fach-Slice erneut auf den betroffenen Bereich begrenzen

- vorhandene Ordnerstruktur erfassen
- bestehende Module identifizieren
- Datenpfade dokumentieren
- Tkinter-Funktionen analysieren
- bestehende Funktionen von `ma_analyse` erfassen
- Import- und Exportlogik prüfen
- Tests und Dokumentation erfassen

Ergebnis

- Ist-Architektur
- Abweichung zur Zielstruktur
- Migrationsplan
- Liste wiederverwendbarer Funktionen

### Arbeitspaket 2 Zentrale Grundlagen

- `ma_core`
- `ma_database`
- `ma_project`
- `ma_workflow`
- `ma_validation`
- `ma_feedback`
- Dokumentationsinfrastruktur

### Arbeitspaket 3 Eingabemodule

- `ma_building`
- `ma_weather`
- `ma_zones`
- `ma_technical`

### Arbeitspaket 4 Zentrale Parameterliste

- `ma_parameters`

### Arbeitspaket 5 Analyse Stufe 1

- `ma_analyse.stage_1_dimensioning`

### Arbeitspaket 6 Varianten

- `ma_variants`

### Arbeitspaket 7 Runs und Simulationssetup

- `ma_simulation_setup`

### Arbeitspaket 8 Allgemeiner Simulationsexport mit IDA-ICE-Adapter

- `ma_export_simulation`

### Arbeitspaket 9 Allgemeiner Simulationsergebnisimport mit IDA-ICE-Adapter

- `ma_import_simulation`

### Arbeitspaket 10 Analyse Stufe 2 bis 4

- `ma_analyse.stage_2_optimization`
- `ma_analyse.stage_3_standards_compliance`
- `ma_analyse.stage_4_sensitivity`

### Arbeitspaket 11 Wirtschaftlichkeit und Nachhaltigkeit

- `ma_economy`
- `ma_sustainability`

### Arbeitspaket 12 Gesamtbewertung

- `ma_assessment`

### Arbeitspaket 13 Reporting und Export

- `ma_reporting`
- `ma_data_export`
- Projektdokumentation und Archivierung

### Arbeitspaket 14 Benutzeroberfläche

- `ma_ui`
- Analyse-View mit realen Projektordnern prüfen
- Vorschau-Cache für Tkinter planen
- Tkinter- und Streamlit-Ablauf fachlich abgleichen
- `ma_workflow` schrittweise mit echten Fachservice-Aufrufen verbinden

### Arbeitspaket 15 Tests und Abnahme

- Unit-Tests
- Integrationstests
- Validierungstests
- Referenzprojekt
- Testvarianten
- Test-Run
- Testimport
- Analyse Stufe 2 bis 4
- Reporting und Export

## 10. Empfohlene Implementierungsreihenfolge

1. P010 Eingabe- und Datenhaltungsarchitektur (umgesetzt)
2. P011 `ma_project`
3. P008 `ma_weather` abschliessen und erweitern
4. P012 `ma_building`
5. P013 `ma_zones`
6. P014 `ma_technical`
7. P015 `ma_parameters`
8. P016 `ma_analyse.stage_1_dimensioning`
9. P017 `ma_variants` und Naming anbinden
10. P018 `ma_simulation_setup` und Run-Manifest
11. P019 `ma_analyse.stage_2_optimization`
12. P020 `ma_analyse.stage_3_standards_compliance`
13. P021 `ma_analyse.stage_4_sensitivity`
14. P022 `ma_economy` Demo und Konzept
15. P023 `ma_sustainability` Demo und Konzept
16. P024 `ma_assessment` Konzept
17. P025 `ma_reporting` Konzept und Demo
18. P026 `ma_data_export` Konzept
19. P009 Export-/Importgrenze nach P018 weiterfuehren
20. P027 Querschnittsfunktionen begleitend pflegen
21. P028 Projekt-, Parameter- und Naming-Demo in Streamlit (umgesetzt)
22. Tests und Abschlusspruefung

## 11. Meilensteine

1. Ist-Architektur dokumentiert und Zielstruktur bestätigt
2. Projektinitialisierung und Validierungsgrundlage funktionieren
3. alle vier Eingabemodule liefern Daten an `ma_parameters`
4. Referenzdimensionierung funktioniert
5. Varianten können erzeugt, ausgewählt und validiert werden
6. Runs koennen als validiertes Manifest angelegt werden
7. Analyse Stufe 2 nutzt die vorhandenen Optimierungswerkzeuge
8. Stufe 3 erzeugt nachvollziehbare deutsche Norm-Nachweise
9. Stufe 4 untersucht kritische Wetter- und Betriebsfaelle
10. IDA-ICE-Uebergabe und Ergebnisimport sind soweit im
    Masterarbeitsrahmen vertretbar dokumentiert oder umgesetzt
11. Economy und Sustainability besitzen Demo und Fachkonzept
12. Assessment, Reporting, Export, Dokumentation und UI sind konzeptuell integriert

## 12. Qualitätsanforderungen

- keine doppelte Fachlogik
- keine Fachlogik in Streamlit oder Tkinter
- keine parallele neue Projektstruktur
- eindeutige Modulgrenzen
- nachvollziehbare Datenquellen
- eindeutige IDs
- reproduzierbare Berechnungen
- dokumentierte Annahmen
- lokale und zentrale Validierung
- Rohdaten bleiben unverändert erhalten
- Ergebnisse sind Projekt, Run und Variante eindeutig zugeordnet
- Änderungen sind dokumentiert

## 13. Entscheidungsdokumentation

### ADR-001 Phase 0 und sechs Hauptphasen

Entscheidung

Die technische Plattform wird als Phase 0 dargestellt. Der fachliche
Gesamtworkflow wird danach in sechs Hauptphasen gegliedert.

Begründung

Die Struktur trennt technische Grundlagen vom fachlichen Ablauf und bleibt
kompakt genug für Workflow, UI und Dokumentation.

### ADR-002 Programmunabhängige Kernarchitektur

Entscheidung

Die allgemeine Struktur bleibt unabhängig vom Simulationsprogramm.

Begründung

Die Masterarbeit verwendet IDA ICE, die Software soll später aber grundsätzlich erweiterbar bleiben.

### ADR-003 IDA ICE als aktueller Projektstandard

Entscheidung

Für die Masterarbeit wird ausschließlich IDA ICE umgesetzt.

Begründung

Eine vollständige Mehrprogrammunterstützung würde den Projektumfang überschreiten.

### ADR-004 Manuelle Simulation

Entscheidung

Die eigentliche Simulation in IDA ICE bleibt zunächst manuell.

Begründung

Der fachliche und softwaretechnische Umfang bleibt kontrollierbar.

### ADR-005 Allgemeine Schnittstellenmodule

Entscheidung

Die Hauptmodule heißen `ma_export_simulation` und `ma_import_simulation`.

Begründung

IDA ICE soll nicht im Namen der allgemeinen Architektur verankert sein.

### ADR-006 Frühzeitige Programmauswahl

Entscheidung

Das Simulationsprogramm wird früh in `ma_project` festgelegt.

Begründung

Diese Entscheidung steuert Parametervorlage, Mapping, Benennung und Adapter.

### ADR-007 Standardvorlagen mit projektspezifischer Kopie

Entscheidung

Benennungs-, Pfad- und Parametervorlagen werden als Standard bereitgestellt und bei Projektstart projektspezifisch kopiert.

Begründung

Ein leeres Startdokument würde zu inkonsistenten Strukturen führen.

### ADR-008 Trennung von Gebäudegeometrie und Bauteilen

Entscheidung

`ma_building` wird in Gebäudemodell, Bauteilzuweisung und Validierung gegliedert.

Begründung

Geometrie und bauphysikalische Eigenschaften haben unterschiedliche Datenlogiken.

### ADR-009 Eigenes Zonenmodul

Entscheidung

Zonen und zonenbezogene Nutzungs- und Betriebsdaten werden in `ma_zones`
definiert. P013-S2 praezisiert dies spaeter als allgemeines Zonenobjekt statt
als ausschliesslich thermische Zone.

Begründung

Räume, zonenspezifische Anforderungen und technische Versorgung sollen getrennt behandelt werden.

### ADR-010 Eigenes Technikmodul

Entscheidung

Technische Referenzsysteme und technische Parameter werden in `ma_technical` erfasst.

Begründung

Standort-, Gebäude-, Zonen- und Technikdaten benötigen getrennte Aufnahmebereiche.

### ADR-011 Zentrale Parameterliste

Entscheidung

`ma_parameters` führt alle Eingaben zusammen.

Begründung

Nachfolgende Module sollen nicht direkt von mehreren Eingabemodulen abhängig sein.

### ADR-012 Sechs Unterbereiche von `ma_variants`

Entscheidung

`ma_variants` wird in Variationsraum, Werte, Regeln, Generierung, Auswahl und Validierung gegliedert.

Begründung

Die Variantenerstellung benötigt eine klare Trennung zwischen möglichen Werten, Zulässigkeit und tatsächlicher Auswahl.

### ADR-013 Stufe 1 nur für die Referenz

Entscheidung

Die erste Dimensionierung wird zunächst nur für die Referenz durchgeführt.

Begründung

Die Referenz bildet die fachliche Ausgangsbasis.

### ADR-014 Vier Analysestufen in `ma_analyse`

Entscheidung

Die vier Stufen werden in einem gemeinsamen Modul geführt.

Begründung

Gemeinsame Fachlogik und einheitlicher Zugriff für Streamlit und Tkinter.

### ADR-015 UI-unabhängige Fachlogik

Entscheidung

Streamlit und Tkinter greifen auf dieselbe Fachlogik zu.

Begründung

Tkinter soll als Ersatzoberfläche nutzbar bleiben.

### ADR-016 Wetterkarte zunächst informativ

Entscheidung

Die Deutschlandkarte wird zunächst nur informativ angezeigt.

Begründung

Die Standortauswahl kann zuerst über ein Auswahlfeld umgesetzt werden.

### ADR-017 Wetterdaten und Standort als Variantenparameter

Entscheidung

Standort und Wetterdatensatz dürfen zwischen Varianten wechseln.

Begründung

Mehrere Standorte und Zukunftsklimadaten sollen untersucht werden.

### ADR-018 Run als Variantenpaket

Entscheidung

Ein Run enthält mehrere ausgewählte Varianten und eine gemeinsame Simulationskonfiguration.

Begründung

Unterschiedliche Untersuchungsrichtungen sollen als eigene Runs behandelt werden.

### ADR-019 Fortlaufende IDs

Entscheidung

Runs und Varianten erhalten projektweit eindeutige und fortlaufende IDs.

Begründung

Ergebnisse und Dateien müssen dauerhaft eindeutig zugeordnet bleiben.

### ADR-020 Vorschlagswerte aus Stufe 1

Entscheidung

Ergebnisse aus Stufe 1 können als Default-Vorschlag in `ma_parameters` gespeichert werden.

Begründung

Die Dimensionierung soll spätere Entscheidungen fachlich unterstützen, ohne `ma_variants` direkt abhängig zu machen.

### ADR-021 Lokale und zentrale Validierung

Entscheidung

Fachmodule prüfen ihre eigenen Inhalte. `ma_validation` prüft Modulübergänge und Gesamtfreigaben.

Begründung

Fachwissen bleibt in den Fachmodulen, während der Workflow zentral gesteuert wird.

### ADR-022 Gewichtung früh dokumentieren

Entscheidung

Bewertungskriterien und Gewichtungsszenarien werden bereits in den Projekt-Randbedingungen referenziert.

Begründung

Die Gewichtung darf nicht erst nach Sichtung der Ergebnisse festgelegt werden.

### ADR-023 Analyseordner an bestehende Struktur anpassen

Entscheidung

Die Struktur von `ma_analyse` wird in die vorhandene VS-Code-Struktur eingeordnet.

Begründung

Eine parallele neue Projektstruktur würde Wartung und Datenhaltung erschweren.

### ADR-024 Validierung und Feedback phasenübergreifend

Entscheidung

`ma_validation` und `ma_feedback` werden als phasenübergreifende
Querschnittsmodule geführt.

Begründung

Prüfungen, Freigaben und Rücksprünge treten mehrfach im iterativen Workflow auf
und sind keine einmaligen Endschritte.

### ADR-025 Leichte Zielpakete

Entscheidung

Bestätigte Zielmodule werden früh als importierbare Pakete, dokumentierte
Moduldefinitionen und Dashboard-Infoseiten angelegt. Leere Service- oder
Modelldateien ohne konkrete Aufgabe werden nicht erzeugt.

Begründung

Die Gesamtstruktur wird sichtbar und erklärbar, ohne einen fachlichen
Umsetzungsstand vorzutäuschen.

### ADR-026 Zentrale Workflow- und Modulmetadaten

Entscheidung

Phasen, Module, Status, Schnittstellen und nächste Schritte werden zentral in
`ma_workflow` katalogisiert.

Begründung

Dashboard, Navigation und technische Übersichten sollen keine voneinander
abweichenden Statuslisten pflegen.

### ADR-027 Trennung von Assessment, Reporting und Datenexport

Entscheidung

`ma_assessment` aggregiert und bewertet Ergebnisse. `ma_reporting` erzeugt
menschlich lesbare Berichte und Factsheets. `ma_data_export` erzeugt
maschinenlesbare Datenpakete.

Begründung

Bewertung, Darstellung und technische Datenweitergabe haben unterschiedliche
Verantwortlichkeiten und Änderungsgründe.

### ADR-028 Dokumentation ohne Python-Paket

Entscheidung

Die Projektdokumentation bleibt unter `docs` und wird als Infrastruktur und
Phase-6-Aktivität im Dashboard dargestellt. Es wird kein leeres
`ma_documentation`-Paket angelegt.

Begründung

Ein Python-Paket ist erst sinnvoll, wenn später echte automatisierte
Dokumentationsfunktionen entstehen.

### ADR-029 Planhistorie unverändert erhalten

Entscheidung

P002, P005 und P006 bleiben unverändert im Archiv. P007 übernimmt die
strukturelle Zielarchitektur; P008 bis P028 konkretisieren die abgestuften
Fach-, Demo-, Konzept-, Research- und Querschnittsarbeiten.

Begründung

Die Entstehungsgeschichte bleibt nachvollziehbar, während aktive Pläne frei von
überholten Strukturentscheidungen bleiben.

### ADR-030 Eingabekette vor Exportautomatisierung

Entscheidung

P010 bis P018 werden vor der technischen Fortsetzung von P009 priorisiert.

Begründung

Funktionsfähige Randbedingungen, Parameter, Dimensionierung, Varianten und
Run-Konfiguration bilden den realistischen Masterarbeitskern.

### ADR-031 Formatneutrale Eingabeadapter

Entscheidung

Import, manuelle Eingabe und Demo-Daten werden je Modul gewählt. Externe
Dateiformate werden über Adapter in neutrale Fachmodelle überführt.

Begründung

IFC, TRY, Excel und programmspezifische Dateien besitzen unterschiedliche
Inhalte und dürfen die Kernmodelle nicht bestimmen.

### ADR-032 Building und Zones mit Demo, IFC-Lite offen

Entscheidung

`ma_building` und `ma_zones` werden mindestens konzeptuell und mit
Demo-Datensätzen umgesetzt. Ein IFC-Lite-Adapter wird erst nach Analyse
konkreter IFC-Arbeitsstände entschieden.

Begründung

Eine allgemeine IFC- oder CAD-Integration würde den Masterarbeitsrahmen
überschreiten.

### ADR-033 Stage 1 mit vereinfachtem Verfahren

Entscheidung

Stage 1 beginnt mit transparenten vereinfachten Verfahren und bereitet einen
späteren Ausbau zu ausführlicheren oder normnäheren Berechnungen vor.

Begründung

Die Lite-Verfahren sind nachvollziehbar, testbar und gegen IDA-Referenzwerte
plausibilisierbar.

### ADR-034 Stage 3 als Standards Compliance

Entscheidung

Der kanonische Name lautet
`ma_analyse.stage_3_standards_compliance`. Deutsche Normen bilden den ersten
Pflichtumfang; internationale Normen werden als spätere Profile ergänzt.

Begründung

Stufe 3 ist ein Norm-Nachweis der Varianten und keine allgemeine
Modellverifikation.

### ADR-035 Projektbezogene neutrale Variantenbenennung

Entscheidung

`ma_project` verwaltet die Simulationsprogrammliste und das neutrale
Varianten-Benennungsprofil. `ma_variants` wendet den referenzierten Regelstand
an. Produkt- und Materialbezeichnungen bleiben neutrale Katalogdaten;
programmspezifische Objekt- und Exportcodes liegen in den Adaptern.

Begründung

Projektkonfiguration, fachliche Katalogbezeichnungen und
programmspezifische Mappings haben unterschiedliche Verantwortlichkeiten.

### ADR-036 Geschuetzte Vorlagen und formaterweiterbare Konfiguration

Entscheidung

Versionierte Vorlagen werden niemals veraendert. Eigene Arbeitsstaende liegen
in lokalen Modulpfaden. Kollidiert ein neuer Dateiname, muss der Nutzer einen
anderen Namen auswaehlen. YAML ist das erste Speicherformat, aber keine
dauerhafte Einschraenkung der Architektur.

Begründung

Vorlagen muessen reproduzierbar bleiben. Fachmodelle duerfen nicht an ein
einzelnes Dateiformat oder automatische, schwer nachvollziehbare
Dateiumbenennungen gekoppelt werden.

## 14. Offene Entscheidungen

- konkrete ausfuehrliche und normnahe Ausbaustufe fuer Stufe 1
- konkrete deutsche Normen, Ausgaben, Abschnitte und Nachweiskriterien fuer
  Stufe 3
- Umfang eines spaeteren IFC-Lite-Adapters
- verbindliche Importformate je Eingabemodul
- verbindliche Varianten-Auswahlmethoden
- genaue ID-Schreibweise
- Case- oder Execution-ID
- genaue IDA-ICE-Dateiformate und Mappings
- Umfang der Wirtschaftlichkeitsberechnung
- Bilanzgrenzen der Nachhaltigkeitsbewertung
- Emissionsfaktoren
- Gesamtscore oder Pareto-Auswertung
- verbindliche Reportingformate
- verbindliche Exportformate
- konkrete Datenbanktechnologie
- konkrete Fachmodelle und Schnittstellen der noch geplanten Module

## 15. Vorgehensregel für Codex und VS Code

Für jede größere Änderung gilt

1. bestehende Struktur analysieren
2. Auswirkungen auf Module und Datenflüsse beschreiben
3. Umsetzungsplan erstellen
4. Zustimmung einholen
5. Änderungen schrittweise umsetzen
6. Tests ausführen
7. Dokumentation und Entscheidungslog aktualisieren
8. keine bestehende Struktur ohne Migrationsplan ersetzen
