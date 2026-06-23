ARCHIVIERT

Archivierungsdatum
2026-06-23

Archivierungsgrund
Dieser unnummerierte Ausgangsplan wurde mit dem bisherigen P008-Plan fuer
ma_weather zusammengefuehrt.

Nachfolgeplan
P008 - docs/project/plans/inbox/260623_Plan_P008_ma_weather_Gesamtplan.md

Hinweis
Die Inhalte dieses Dokuments wurden geprueft und in den aktualisierten
Gesamtplan fuer ma_weather integriert. Dieses Dokument dient nur noch der
Nachvollziehbarkeit der Planentwicklung und darf nicht mehr als aktuelle
Umsetzungsgrundlage verwendet werden.

# Implementierungsplan für `ma_weather`

## 0 Zweck des Dokuments

* Grundlage für die Integration des Wettermoduls in das vorhandene VS-Code-Projekt
* Arbeitsgrundlage für Codex
* Dokumentation der fachlichen, technischen und UI-bezogenen Entscheidungen
* Keine sofortige Vorgabe einer vollständig neuen Projektstruktur
* Zuerst Analyse der vorhandenen Struktur
* Danach Einordnung der neuen Bausteine in das bestehende Projekt
* Fachlogik unabhängig von Streamlit und Tkinter
* Streamlit als primäre Benutzeroberfläche

## 1 Ausgangslage

* Das Gesamtprojekt besitzt bereits eine modulare Architektur
* `ma_weather` ist eines der Eingabemodule
* Weitere Eingabemodule sind `ma_building`, `ma_zones` und `ma_technical`
* `ma_parameters` führt die Ergebnisse der Eingabemodule zusammen
* `ma_variants` verwendet ausschließlich die zentrale Parameterliste aus `ma_parameters`
* Der Wetterdatensatz wird als Projekt-Default festgelegt
* Varianten dürfen den Projekt-Default später bewusst überschreiben
* Die eigentliche Simulation bleibt aktuell ein externer und manueller Prozess
* Die Software soll grundsätzlich programmunabhängig bleiben
* Für die Masterarbeit wird aktuell ausschließlich IDA ICE berücksichtigt

## 2 Zielbild von `ma_weather`

* Auswahl einer Stadt in der Streamlit UI
* Automatische Ermittlung der Klimaregion
* Automatische Ermittlung des TRY-Referenzstandorts
* Filterung der verfügbaren Wetterdatensätze anhand des Referenzstandorts
* Auswahl eines validierten Wetterdatensatzes
* Anzeige von Klimaszenario und Bezugszeitraum
* Festlegung eines Projekt-Defaults
* Import neuer Wetterdatensätze
* Technische und fachliche Validierung
* Dauerhafte Speicherung eines Import-Logs
* Sichtbare Verwaltung noch nicht validierter Datensätze
* Wetterdatenanalyse
* Übergabe der geprüften Auswahl an `ma_parameters`

## 3 Dokumentierte Entscheidungen

### 3.1 Stadt als primärer Auswahlpunkt

**Entscheidung**

* Der Nutzer wählt direkt eine Stadt aus
* Die Klimaregion wird nicht manuell ausgewählt

**Begründung**

* Die Klimaregion ist eine abgeleitete Information
* Eine zusätzliche Auswahl würde den Bedienablauf unnötig verlängern
* Fehlerhafte Kombinationen aus Stadt und Klimaregion werden vermieden
* Die Datenbank besitzt bereits die Zuordnung Stadt zu Klimaregion und Referenzstandort

**Folgen**

* Die Stadt ist das erste aktive Auswahlfeld
* Klimaregion und Referenzstandort werden nur angezeigt
* Beide Felder sind nicht editierbar
* Die Wetterdatensätze werden erst nach der Stadtauswahl gefiltert

### 3.2 Deutschlandkarte zunächst nur informativ

**Entscheidung**

* Die Karte mit den Klimaregionen wird in der Streamlit UI angezeigt
* Die Karte ist in der ersten Ausbaustufe nicht interaktiv

**Begründung**

* Eine interaktive Karte benötigt Vektordaten, GeoJSON und zusätzliche Ereignislogik
* Der fachliche Mehrwert ist für die erste Version begrenzt
* Die Stadt kann zuverlässig über ein Suchfeld ausgewählt werden
* Der Entwicklungsaufwand bleibt kontrollierbar

**Folgen**

* Die Karte dient der Orientierung
* Eine interaktive Kartenfunktion bleibt als spätere Erweiterung dokumentiert
* Die erste Version verwendet ein statisches Bild im Projekt-Asset-Ordner

### 3.3 Trennung von Standort und Wetterdatensatz

**Entscheidung**

* Wetterdatensätze werden nicht direkt als einzelne Dateipfade in der Standorttabelle gespeichert
* Wetterstandorte und Wetterdatensätze werden in getrennten Tabellen verwaltet

**Begründung**

* Ein Referenzstandort kann mehrere Wetterdatensätze besitzen
* Gegenwart, Zukunftsszenarien und unterschiedliche Bezugszeiträume müssen parallel verwaltet werden
* Neue Versionen sollen ergänzt werden können
* Standortdaten ändern sich seltener als Wetterdatensätze

**Folgen**

* Beziehung Stadt zu Klimaregion
* Beziehung Klimaregion zu Referenzstandort
* Beziehung Referenzstandort zu mehreren Wetterdatensätzen
* Die Streamlit UI filtert die Wetterdatensätze anhand der Referenzstandort-ID

### 3.4 Nur validierte Datensätze in der regulären Auswahl

**Entscheidung**

* Im normalen Wetterdatensatz-Dropdown erscheinen nur aktive und gültige Datensätze

**Begründung**

* Unvollständige oder fehlerhafte Datensätze dürfen nicht versehentlich für Simulationen verwendet werden
* Der Projekt-Default muss reproduzierbar und fachlich geprüft sein
* `ma_parameters`, `ma_variants` und spätere Runs dürfen nur freigegebene Datensätze erhalten

**Folgen**

* Validierung und Aktivierung sind getrennte Zustände
* Ein validierter Datensatz wird nicht automatisch Projekt-Default
* Nicht validierte Datensätze erhalten einen eigenen Arbeitsbereich

### 3.5 Eigener Bereich für offene Wetterdatensätze

**Entscheidung**

* Nicht validierte, unvollständige und fehlerhafte Datensätze bleiben sichtbar
* Diese Datensätze können direkt bearbeitet, erneut geprüft, archiviert oder gelöscht werden

**Begründung**

* Fehlgeschlagene Importe dürfen nicht unsichtbar werden
* Bearbeitungsstände müssen nachvollziehbar bleiben
* Nutzer sollen Metadaten ergänzen und Prüfungen erneut ausführen können
* Importfehler müssen ohne erneuten vollständigen Upload analysiert werden können

**Folgen**

* Eigene Streamlit-Ansicht für offene Wetterdatensätze
* Keine Nutzung als Projekt-Default
* Keine Übergabe an `ma_parameters`
* Keine Nutzung in Varianten oder Runs

### 3.6 Jeder Import erzeugt eine Log-Datei

**Entscheidung**

* Jeder Importvorgang erzeugt eine dauerhafte Log-Datei
* Dies gilt auch für fehlgeschlagene oder abgebrochene Importe

**Begründung**

* Reproduzierbarkeit
* Fehleranalyse
* Nachvollziehbarkeit der Datenherkunft
* Dokumentation für die Masterarbeit
* Trennung zwischen erfolgreicher Datenbanktransaktion und dauerhaftem Prozessprotokoll

**Folgen**

* Import-ID wird bereits zu Beginn erzeugt
* Log-Datei wird außerhalb der Haupttransaktion gespeichert
* Import-Log, Validierungsbericht und Wetterdatensatz werden eindeutig verknüpft
* Rollback-Informationen werden protokolliert

### 3.7 Import setzt nicht automatisch den Projekt-Default

**Entscheidung**

* Ein neu importierter Datensatz wird nicht automatisch zum Projekt-Default

**Begründung**

* Ein bestehender Projektzustand darf nicht unbemerkt verändert werden
* Der Import ist eine Verwaltungsfunktion
* Die Auswahl des Projekt-Defaults ist eine bewusste fachliche Entscheidung

**Folgen**

* Nach erfolgreichem Import wird die Aktion `Als Projekt-Default übernehmen` angeboten
* Der bisherige Default bleibt unverändert, bis der Nutzer bestätigt

### 3.8 Relative Dateipfade

**Entscheidung**

* Die Datenbank speichert relative und keine benutzerspezifischen absoluten Dateipfade

**Begründung**

* Übertragbarkeit zwischen Rechnern
* Nutzung in Git oder anderen Projektkopien
* Trennung zwischen Projektkonfiguration und Benutzerverzeichnis
* Vermeidung harter Windows-Pfade

**Folgen**

* Ein zentraler Datenpfad wird in der Projektkonfiguration definiert
* Dateipfade werden zur Laufzeit aufgelöst
* Pfadprüfung erfolgt zentral

### 3.9 Stabile IDs statt bestehender Kürzel als Primärschlüssel

**Entscheidung**

* Bestehende Codes werden als Legacy-Daten erhalten
* Technische Verknüpfungen verwenden stabile IDs

**Begründung**

* Bestehende Kürzel sind teilweise doppelt
* Ein Standort besitzt aktuell keinen Code
* Kürzel können sich ändern
* Datenbankbeziehungen dürfen nicht von Anzeige- oder Kfz-Kürzeln abhängen

**Folgen**

* `location_id`, `region_id`, `reference_location_id`, `dataset_id` und `import_id`
* Legacy-Codes nur zur Anzeige und Rückverfolgbarkeit
* Keine Verwendung der Legacy-Codes als Primär- oder Fremdschlüssel

### 3.10 Trennung zwischen UI und Fachlogik

**Entscheidung**

* Streamlit enthält keine eigentliche Wetterdatenanalyse, Validierungslogik oder Speicherlogik

**Begründung**

* Fachlogik muss testbar sein
* Tkinter soll dieselben Funktionen nutzen können
* Spätere UI-Wechsel sollen möglich bleiben
* Die bestehende Architektur verlangt eine UI-unabhängige Logik

**Folgen**

* Streamlit ruft Services auf
* Parser, Validierung, Analyse, Import, Logging und Datenbankzugriffe liegen außerhalb der UI
* Keine direkten SQL-Abfragen in der Streamlit-Seite

## 4 Fachlicher Funktionsumfang

### 4.1 Standortverwaltung

* Klimaregionen verwalten
* Städte verwalten
* Stadt einer Klimaregion zuordnen
* Stadt einem Referenzstandort zuordnen
* Referenzstandort kennzeichnen
* Standorte aktivieren oder deaktivieren
* Suche nach Stadtname und Legacy-Code
* Optional spätere Ergänzung von Koordinaten

### 4.2 Wetterdatensatzverwaltung

* Wetterdatensätze registrieren
* Datensätze einem Referenzstandort zuordnen
* Klimaszenario speichern
* Bezugszeitraum speichern
* Datenquelle speichern
* Dateiformat speichern
* relativen Dateipfad speichern
* Prüfsumme speichern
* Version speichern
* Status speichern
* Projekt-Default verwalten
* Datensatz archivieren
* Datensatz löschen, sofern keine abhängigen Verwendungen bestehen

### 4.3 Import

* Datei auswählen
* temporär speichern
* Import-ID erzeugen
* Log-Datei anlegen
* Dateiformat erkennen
* Metadaten erkennen
* Datei-Prüfsumme erzeugen
* Duplikate prüfen
* Parser ausführen
* technische Validierung
* fachliche Validierung
* Validierungsbericht speichern
* Originaldatei dauerhaft speichern
* optional normalisierte Datei speichern
* Datenbankeintrag erzeugen
* Log-Datei abschließen
* Importstatus setzen

### 4.4 Validierung

* Dateilesbarkeit
* Formatprüfung
* Zeichenkodierung
* Spaltenstruktur
* Pflichtspalten
* Zeitstempel
* konstante zeitliche Auflösung
* doppelte Zeitstempel
* fehlende Zeitschritte
* fehlende Werte
* plausible Wertebereiche
* Einheiten
* Standortkonsistenz
* Szenario und Zeitraum
* Duplikatstatus
* Vollständigkeit der Pflichtmetadaten

### 4.5 Wetteranalyse

* Jahresverlauf der Außenlufttemperatur
* Monatsmittelwerte
* monatliche Minima und Maxima
* Temperaturdauerlinie
* Häufigkeitsverteilung
* Monats-Stunden-Heatmap
* Solarstrahlungsanalyse
* Windgeschwindigkeitsanalyse
* Feuchteanalyse
* Heizgradtage oder Heizgradstunden
* Kühlgradtage oder Kühlgradstunden
* Erkennung von Extremtagen
* Vergleich von Gegenwarts- und Zukunftsdatensätzen
* Vergleich mehrerer Referenzstandorte

## 5 Streamlit UI

### 5.1 Seitenstruktur

* `Standort und Wetterauswahl`
* `Wetteranalyse`
* `Wetterdatenkatalog`
* `Offene Wetterdatensätze`
* `Wetterdatensatz importieren`
* `Import- und Validierungsprotokolle`

### 5.2 Hauptseite Standort und Wetterauswahl

#### Kopfbereich

* aktueller Projekt-Default
* gewählte Stadt
* Klimaregion
* Referenzstandort
* Datensatzname
* Klimaszenario
* Bezugszeitraum
* Validierungsstatus
* Button `Wetterdatensatz importieren`

#### Linke Spalte

* statische Deutschlandkarte
* Klimaregionen
* Referenzstandorte
* Legende
* Hinweis auf informative Darstellung

#### Rechte Spalte

* Suchfeld oder Selectbox für Stadt
* automatisch ermittelte Klimaregion
* automatisch ermittelter Referenzstandort
* gefilterte Auswahl verfügbarer Wetterdatensätze
* Anzeige des Klimaszenarios
* Anzeige des Bezugszeitraums
* Anzeige der Datenquelle
* Anzeige des Validierungsstatus
* Button `Als Projekt-Default übernehmen`
* Button `Datensatz analysieren`
* Button `Datensatzdetails`
* Button `Datensatz für diesen Referenzstandort importieren`

### 5.3 Ablauf nach Stadtauswahl

```text
Stadt auswählen
    ↓
Standortdatensatz laden
    ↓
Klimaregion ermitteln
    ↓
Referenzstandort ermitteln
    ↓
aktive und validierte Wetterdatensätze laden
    ↓
Wetterdatensatz auswählen
    ↓
Szenario und Bezugszeitraum anzeigen
    ↓
optional Projekt-Default setzen
```

### 5.4 Verhalten ohne verfügbaren Datensatz

* Hinweis anzeigen
* Referenzstandort nennen
* Kontextbezogenen Importbutton anzeigen
* Referenzstandort für den Import vorausfüllen
* Kein leeres oder irreführendes Auswahlfeld

### 5.5 Offene Wetterdatensätze

#### Übersicht

* Status
* Import-ID
* Datensatz-ID
* Referenzstandort
* Dateiname
* Importdatum
* offene Pflichtangaben
* Fehleranzahl
* Warnungsanzahl
* letzte Bearbeitung
* Link zum Import-Log
* Link zum Validierungsbericht

#### Filter

* Referenzstandort
* Klimaregion
* Workflow-Status
* Validierungsstatus
* Importdatum
* nur fehlerhafte Datensätze
* nur unvollständige Datensätze
* nur Datensätze mit Warnungen

#### Aktionen

* öffnen
* Metadaten bearbeiten
* Datei-Vorschau anzeigen
* erneut validieren
* Duplikatprüfung wiederholen
* Import fortsetzen
* Datei ersetzen
* als neue Version importieren
* archivieren
* löschen
* Import-Log anzeigen
* Validierungsbericht anzeigen

### 5.6 Importseite

#### Schritt 1 Datei

* Datei hochladen
* Dateiname
* Dateityp
* Dateigröße
* erkannte Kodierung
* Import-ID anzeigen

#### Schritt 2 automatische Erkennung

* Dateiformat
* Spaltentrennung
* Kopfzeilen
* Wetterparameter
* Einheiten
* zeitliche Auflösung
* Startdatum
* Enddatum
* Anzahl Zeitschritte
* erkannte Standortinformationen

#### Schritt 3 Metadaten

* Datensatzname
* Referenzstandort
* Klimaregion automatisch
* Datensatztyp
* Klimaszenario
* Bezugszeitraum
* Datenquelle
* Version
* Beschreibung
* Lizenzhinweis
* Bearbeiter

#### Schritt 4 Validierung

* technische Prüfung
* fachliche Prüfung
* Duplikatprüfung
* Fehler
* Warnungen
* Hinweise
* Validierungsbericht

#### Schritt 5 Abschluss

* Datensatz speichern
* Log-Datei finalisieren
* Datensatz aktivieren, sofern gültig
* optional Projekt-Default setzen
* Datensatz analysieren
* Wetterdatenkatalog öffnen

## 6 Datenmodell

### 6.1 Tabelle `weather_regions`

| Feld | Zweck |
|---|---|
| `region_id` | stabile interne ID |
| `region_number` | Klimaregion 1 bis 15 |
| `region_code` | zum Beispiel `TRY12` |
| `region_name` | optionale Bezeichnung |
| `reference_location_id` | zugehöriger Referenzstandort |
| `active` | Region aktiv |
| `created_at` | Erstellungszeitpunkt |
| `updated_at` | Änderungszeitpunkt |

### 6.2 Tabelle `weather_locations`

| Feld | Zweck |
|---|---|
| `location_id` | stabile interne ID |
| `location_name` | Stadtname |
| `normalized_name` | Such- und Vergleichswert |
| `legacy_code` | bisheriger Code |
| `region_id` | Fremdschlüssel zur Klimaregion |
| `reference_location_id` | Fremdschlüssel zum Referenzstandort |
| `is_reference_location` | Kennzeichnung |
| `latitude` | optional |
| `longitude` | optional |
| `active` | auswählbar |
| `created_at` | Erstellungszeitpunkt |
| `updated_at` | Änderungszeitpunkt |

### 6.3 Tabelle `weather_datasets`

| Feld | Zweck |
|---|---|
| `dataset_id` | stabile interne ID |
| `import_id` | zugehöriger Importvorgang |
| `reference_location_id` | Filter für die UI |
| `dataset_name` | Anzeigename |
| `dataset_code` | optionaler technischer Code |
| `dataset_type` | typisches Jahr, Extremjahr oder anderer Typ |
| `climate_scenario` | Gegenwart oder Zukunft |
| `climate_period_start` | Beginn des Bezugszeitraums |
| `climate_period_end` | Ende des Bezugszeitraums |
| `source_name` | Datenquelle |
| `source_version` | Versionsangabe |
| `file_format` | TRY, EPW, CSV oder anderes Format |
| `relative_source_path` | Pfad zur Originaldatei |
| `relative_normalized_path` | optionaler normalisierter Datensatz |
| `file_hash_sha256` | Prüfsumme |
| `time_step_minutes` | zeitliche Auflösung |
| `data_start` | Beginn der Zeitreihe |
| `data_end` | Ende der Zeitreihe |
| `record_count` | Anzahl Datensätze |
| `workflow_status` | Bearbeitungsstand |
| `validation_status` | Prüfergebnis |
| `metadata_complete` | Pflichtfelder vollständig |
| `duplicate_status` | Ergebnis der Duplikatprüfung |
| `is_active` | regulär auswählbar |
| `is_archived` | archiviert |
| `created_at` | Erstellungszeitpunkt |
| `updated_at` | Änderungszeitpunkt |

### 6.4 Tabelle `weather_imports`

| Feld | Zweck |
|---|---|
| `import_id` | eindeutige Import-ID |
| `project_id` | optionaler Projektbezug |
| `dataset_id` | erzeugter Datensatz |
| `source_filename` | ursprünglicher Dateiname |
| `file_hash_sha256` | Prüfsumme |
| `started_at` | Start |
| `finished_at` | Ende |
| `import_status` | Ergebnis |
| `validation_status` | Prüfergebnis |
| `error_count` | Anzahl Fehler |
| `warning_count` | Anzahl Warnungen |
| `log_file_path` | relativer Log-Pfad |
| `validation_report_path` | relativer Berichtspfad |
| `imported_by` | Benutzer oder Prozess |
| `software_version` | Version der Anwendung |
| `parser_version` | verwendete Parser-Version |

### 6.5 Tabelle `project_weather_selection`

| Feld | Zweck |
|---|---|
| `project_id` | Projekt |
| `dataset_id` | Projekt-Default |
| `selected_city_id` | fachlich gewählte Stadt |
| `selected_at` | Auswahlzeitpunkt |
| `selected_by` | Bearbeiter |
| `selection_note` | optionale Begründung |
| `is_current` | aktuelle Auswahl |

## 7 Statusmodell

### 7.1 Workflow-Status

* `uploaded`
* `format_detected`
* `metadata_pending`
* `duplicate_check_pending`
* `validation_pending`
* `validation_running`
* `validation_failed`
* `validated`
* `activation_pending`
* `active`
* `import_incomplete`
* `processing_error`
* `archived`
* `deleted`

### 7.2 Validierungsstatus

* `not_checked`
* `valid`
* `valid_with_warnings`
* `invalid`
* `check_failed`

### 7.3 Duplikatstatus

* `not_checked`
* `no_duplicate`
* `exact_duplicate`
* `possible_duplicate`
* `new_version_confirmed`

### 7.4 Freigaberegel

Ein Datensatz darf nur aktiv werden, wenn

* Pflichtmetadaten vollständig
* Parser erfolgreich
* keine kritischen Validierungsfehler
* Duplikatprüfung abgeschlossen
* Originaldatei gespeichert
* Validierungsbericht vorhanden
* Import-Log vorhanden
* Datenbankeintrag vollständig

## 8 Import-Log

### 8.1 Grundregeln

* Log-Datei wird beim Importstart angelegt
* Log-Datei bleibt bei Fehler und Abbruch erhalten
* JSON als primäres Format
* optional zusätzlich menschenlesbare Textansicht
* Log außerhalb der Hauptdatenbanktransaktion
* eindeutige Verknüpfung über `import_id`

### 8.2 Mindestinhalt

* Import-ID
* Projekt-ID
* Startzeit
* Endzeit
* Benutzer oder Prozess
* Softwareversion
* Parser-Version
* Quelldatei
* Dateigröße
* Dateiformat
* Kodierung
* Prüfsumme
* temporärer Pfad
* Zielpfad
* erkannte Metadaten
* Nutzerbestätigte Metadaten
* Duplikatprüfung
* technische Validierung
* fachliche Validierung
* Fehler
* Warnungen
* Hinweise
* Datenbankaktionen
* Dateisystemaktionen
* Rollback-Aktionen
* Abschlussstatus

### 8.3 Log-Ereignisse

* `IMPORT_STARTED`
* `FILE_UPLOADED`
* `HASH_CREATED`
* `FORMAT_DETECTED`
* `METADATA_DETECTED`
* `METADATA_CONFIRMED`
* `DUPLICATE_CHECK_COMPLETED`
* `PARSER_STARTED`
* `PARSER_COMPLETED`
* `VALIDATION_STARTED`
* `VALIDATION_COMPLETED`
* `SOURCE_FILE_STORED`
* `NORMALIZED_FILE_STORED`
* `DATABASE_RECORD_CREATED`
* `DATABASE_RECORD_UPDATED`
* `ROLLBACK_STARTED`
* `ROLLBACK_COMPLETED`
* `IMPORT_COMPLETED`
* `IMPORT_FAILED`
* `IMPORT_ABORTED`

## 9 Dateisystem

```text
data/
└── weather/
    ├── catalog/
    ├── source/
    │   ├── try01/
    │   ├── try02/
    │   └── try15/
    ├── normalized/
    ├── metadata/
    ├── validation_reports/
    ├── import_logs/
    │   └── 2026/
    ├── temporary/
    └── archive/
```

### 9.1 Regeln

* Originaldateien bleiben unverändert erhalten
* normalisierte Daten werden getrennt gespeichert
* Log-Dateien werden nicht überschrieben
* Validierungsberichte werden versioniert
* temporäre Dateien werden nach erfolgreichem Abschluss bereinigt
* fehlgeschlagene Importe behalten Log und Bericht
* relative Pfade werden in der Datenbank gespeichert

## 10 Verbesserte Codierungstabelle

### 10.1 Grundprinzip

* bestehende Tabelle als fachliche Ausgangsbasis behalten
* neue stabile IDs ergänzen
* Legacy-Codes nicht löschen
* doppelte Legacy-Codes zulassen
* Legacy-Codes nicht als Schlüssel verwenden
* fehlende Codes durch leeren Legacy-Wert darstellen
* Referenzstandort über ID statt Freitext verknüpfen
* Klimaregion als eigene Tabelle verwalten

### 10.2 Zuordnung der Klimaregionen

| Region | Region-Code | Referenzstandort laut Ausgangstabelle |
|---:|---|---|
| 1 | TRY01 | Bremerhaven |
| 2 | TRY02 | Rostock |
| 3 | TRY03 | Hamburg |
| 4 | TRY04 | Potsdam |
| 5 | TRY05 | Essen |
| 6 | TRY06 | Bad Marienberg |
| 7 | TRY07 | Kassel |
| 8 | TRY08 | Braunlage |
| 9 | TRY09 | Chemnitz |
| 10 | TRY10 | Hof |
| 11 | TRY11 | Fichtelberg |
| 12 | TRY12 | Mannheim |
| 13 | TRY13 | Mühldorf |
| 14 | TRY14 | Stötten |
| 15 | TRY15 | Garmisch-Partenkirchen |

### 10.3 Datenbereinigung

* Bremen und Bremerhaven besitzen beide `HB`
* Bayreuth und Fichtelberg besitzen beide `BT`
* Wittenberge besitzt keinen Legacy-Code
* Umlaute und Sonderzeichen dürfen in Anzeigenamen bleiben
* technische IDs enthalten keine Umlaute oder Sonderzeichen
* Standortnamen werden zusätzlich normalisiert gespeichert
* `Frankfurt (Main)` und `Frankfurt (Oder)` bleiben fachlich getrennt
* Referenzstandorte werden durch `is_reference_location` gekennzeichnet

### 10.4 Initiale Standortdaten

| Location-ID | Standort | Legacy-Code | Region | Referenzstandort |
|---|---|---|---:|---|
| LOC_001 | Bremen | HB | 1 | Bremerhaven |
| LOC_002 | Bremerhaven | HB | 1 | Bremerhaven |
| LOC_003 | Emden | EMD | 1 | Bremerhaven |
| LOC_004 | Flensburg | FL | 2 | Rostock |
| LOC_005 | Rostock | HRO | 2 | Rostock |
| LOC_006 | Rügen | RÜG | 2 | Rostock |
| LOC_007 | Kiel | KI | 2 | Rostock |
| LOC_008 | Lübeck | HL | 2 | Rostock |
| LOC_009 | Hamburg | HH | 3 | Hamburg |
| LOC_010 | Hannover | H | 3 | Hamburg |
| LOC_011 | Meppen | EL | 3 | Hamburg |
| LOC_012 | Uelzen | UE | 3 | Hamburg |
| LOC_013 | Berlin | B | 4 | Potsdam |
| LOC_014 | Cottbus | CB | 4 | Potsdam |
| LOC_015 | Dessau | DE | 4 | Potsdam |
| LOC_016 | Frankfurt (Oder) | FF | 4 | Potsdam |
| LOC_017 | Leipzig | L | 4 | Potsdam |
| LOC_018 | Magdeburg | MD | 4 | Potsdam |
| LOC_019 | Neubrandenburg | NB | 4 | Potsdam |
| LOC_020 | Potsdam | P | 4 | Potsdam |
| LOC_021 | Schwerin | SN | 4 | Potsdam |
| LOC_022 | Wittenberge |  | 4 | Potsdam |
| LOC_023 | Dresden | DD | 4 | Potsdam |
| LOC_024 | Aachen | AC | 5 | Essen |
| LOC_025 | Bonn | BN | 5 | Essen |
| LOC_026 | Dortmund | DO | 5 | Essen |
| LOC_027 | Düsseldorf | D | 5 | Essen |
| LOC_028 | Essen | E | 5 | Essen |
| LOC_029 | Köln | K | 5 | Essen |
| LOC_030 | Münster | MS | 5 | Essen |
| LOC_031 | Osnabrück | OS | 5 | Essen |
| LOC_032 | Koblenz | KO | 5 | Essen |
| LOC_033 | Bad Marienberg | WW | 6 | Bad Marienberg |
| LOC_034 | Detmold | LIP | 6 | Bad Marienberg |
| LOC_035 | Nordhausen | NDH | 6 | Bad Marienberg |
| LOC_036 | Saarbrücken | SB | 6 | Bad Marienberg |
| LOC_037 | Freiburg | FR | 6 | Bad Marienberg |
| LOC_038 | Kassel | KS | 7 | Kassel |
| LOC_039 | Marburg | MR | 7 | Kassel |
| LOC_040 | Trier | TR | 7 | Kassel |
| LOC_041 | Fulda | FD | 7 | Kassel |
| LOC_042 | Braunlage | BRL | 8 | Braunlage |
| LOC_043 | Chemnitz | C | 9 | Chemnitz |
| LOC_044 | Erfurt | EF | 9 | Chemnitz |
| LOC_045 | Hof | HO | 10 | Hof |
| LOC_046 | Plauen | V | 10 | Hof |
| LOC_047 | Bayreuth | BT | 10 | Hof |
| LOC_048 | Fichtelberg | BT | 11 | Fichtelberg |
| LOC_049 | Frankfurt (Main) | F | 12 | Mannheim |
| LOC_050 | Stuttgart | S | 12 | Mannheim |
| LOC_051 | Baden-Baden | BAD | 12 | Mannheim |
| LOC_052 | Mainz | MZ | 12 | Mannheim |
| LOC_053 | Mannheim | MA | 12 | Mannheim |
| LOC_054 | Wiesbaden | WI | 12 | Mannheim |
| LOC_055 | Würzburg | WÜ | 13 | Mühldorf |
| LOC_056 | Augsburg | A | 13 | Mühldorf |
| LOC_057 | Lindau | LI | 13 | Mühldorf |
| LOC_058 | Mühldorf | MÜ | 13 | Mühldorf |
| LOC_059 | München | M | 13 | Mühldorf |
| LOC_060 | Nürnberg | N | 13 | Mühldorf |
| LOC_061 | Passau | PA | 13 | Mühldorf |
| LOC_062 | Regensburg | R | 13 | Mühldorf |
| LOC_063 | Ulm | UL | 13 | Mühldorf |
| LOC_064 | Stötten | OAL | 14 | Stötten |
| LOC_065 | Berchtesgaden | BGD | 15 | Garmisch-Partenkirchen |
| LOC_066 | Garmisch-Partenkirchen | GAP | 15 | Garmisch-Partenkirchen |

## 11 Modulgrenzen

### 11.1 `ma_weather`

* Standortkatalog
* Wetterdatensatzkatalog
* Import
* Parser
* Validierung
* Wetteranalyse
* Datensatzvergleich
* Projekt-Default
* Import-Logging
* Validierungsberichte

### 11.2 `ma_parameters`

* Übernahme des freigegebenen Projekt-Defaults
* Vereinheitlichung der Wetterparameter
* Prüfung der Parameterverfügbarkeit
* zentrale Bereitstellung für weitere Module

### 11.3 `ma_variants`

* optionale Abweichung vom Projekt-Default
* Auswahl nur aus aktiven und validierten Datensätzen
* Dokumentation des Overrides
* keine direkte Nutzung offener Datensätze

### 11.4 `ma_validation`

* zentrale Zusammenführung von Checkpoints
* Prüfung, ob ein gültiger Wetterdatensatz vorliegt
* Sperre vor Variantenbildung oder Simulation bei ungültigem Status

## 12 Empfohlene technische Struktur

Die folgende Struktur ist ein Vorschlag. Codex soll sie nicht blind erzeugen, sondern zuerst mit dem vorhandenen Projekt vergleichen.

```text
src/
└── ma_weather/
    ├── __init__.py
    ├── models.py
    ├── schemas.py
    ├── repository.py
    ├── config.py
    ├── exceptions.py
    ├── parsers/
    │   ├── __init__.py
    │   ├── base_parser.py
    │   └── try_parser.py
    ├── services/
    │   ├── location_service.py
    │   ├── selection_service.py
    │   ├── import_service.py
    │   ├── duplicate_service.py
    │   ├── validation_service.py
    │   ├── activation_service.py
    │   ├── analysis_service.py
    │   └── comparison_service.py
    ├── logging/
    │   ├── import_logger.py
    │   └── log_schema.py
    ├── reports/
    │   ├── validation_report.py
    │   └── import_report.py
    ├── plotting/
    │   ├── temperature_plots.py
    │   ├── climate_plots.py
    │   └── comparison_plots.py
    └── export/
        └── parameter_export.py

ui/
└── streamlit/
    └── pages/
        ├── weather_selection.py
        ├── weather_analysis.py
        ├── weather_catalog.py
        ├── weather_open_datasets.py
        ├── weather_import.py
        └── weather_logs.py

tests/
└── ma_weather/
    ├── test_location_service.py
    ├── test_try_parser.py
    ├── test_duplicate_service.py
    ├── test_validation_service.py
    ├── test_import_service.py
    ├── test_import_logger.py
    ├── test_activation_service.py
    └── test_selection_service.py

assets/
└── weather/
    └── klimaregionen_deutschland.jpg
```

## 13 Kernfunktionen

```python
get_active_locations()
get_location_by_id()
get_location_assignment()
get_reference_location()
get_active_weather_datasets()
get_open_weather_datasets()
get_weather_dataset_details()
set_project_weather_default()

start_weather_import()
detect_weather_file_format()
extract_weather_metadata()
calculate_file_hash()
check_weather_duplicate()
parse_weather_file()
validate_weather_file()
store_weather_source_file()
store_normalized_weather_data()
register_weather_dataset()
activate_weather_dataset()
archive_weather_dataset()
delete_weather_dataset()

create_import_log()
append_import_event()
log_validation_result()
log_database_action()
log_rollback()
finalize_import_log()

analyze_weather_dataset()
compare_weather_datasets()
identify_extreme_days()
export_weather_parameters()
```

## 14 Importtransaktion und Fehlerbehandlung

### 14.1 Erfolgreicher Ablauf

```text
Import-ID erzeugen
    ↓
Log-Datei anlegen
    ↓
Datei temporär speichern
    ↓
Hash erzeugen
    ↓
Format und Metadaten erkennen
    ↓
Duplikatprüfung
    ↓
Parser
    ↓
Validierung
    ↓
Validierungsbericht speichern
    ↓
Originaldatei dauerhaft speichern
    ↓
Datenbankeintrag erzeugen
    ↓
Datensatz aktivieren
    ↓
Log finalisieren
```

### 14.2 Fehlerhafter Ablauf

```text
Fehler erkennen
    ↓
Fehler protokollieren
    ↓
offene Datenbanktransaktion zurücksetzen
    ↓
unvollständige Zieldateien entfernen oder kennzeichnen
    ↓
temporäre Datei nach Regel behandeln
    ↓
Datensatz als offen oder fehlerhaft speichern
    ↓
Log finalisieren
```

### 14.3 Löschregeln

* Physisches Löschen nur ohne abhängige Projekt-, Varianten- oder Run-Verwendungen
* Sonst Archivierung
* Log-Dateien nicht löschen
* Validierungsberichte nicht löschen
* Löschvorgang ebenfalls protokollieren

## 15 Umsetzungsschritte

### Phase 1 Bestandsanalyse

* aktuelle Projektstruktur untersuchen
* vorhandene Module und Namenskonventionen erfassen
* vorhandene Datenbankmodelle prüfen
* vorhandene Streamlit-Navigation prüfen
* vorhandene Konfigurations- und Logging-Lösung prüfen
* vorhandene Tests prüfen
* bestehende Wetterfunktionen suchen
* Abweichungen zum Zielplan dokumentieren

**Ergebnis**

* Integrationsbericht
* keine Codeänderung ohne Bestätigung

### Phase 2 Datenmodell und Migration

* Tabellenmodell an vorhandene Datenbanktechnik anpassen
* Standortdaten bereinigen
* Klimaregionen anlegen
* Referenzstandorte verknüpfen
* Legacy-Codes übernehmen
* Migration oder Seed-Dateien erstellen
* Eindeutigkeit und Fremdschlüssel testen

**Abnahmekriterium**

* jede Stadt liefert eindeutig Region und Referenzstandort

### Phase 3 Standortauswahl in Streamlit

* Karte als Asset einbinden
* Stadt-Suchfeld
* automatische Region
* automatischer Referenzstandort
* gefilterte Datensatzauswahl
* Statusanzeige
* Projekt-Default setzen
* leere Zustände behandeln

**Abnahmekriterium**

* Auswahl erfolgt ohne manuelle Klimaregionsauswahl

### Phase 4 Import-Grundlage

* Upload
* Import-ID
* temporäre Ablage
* Dateihash
* Formatdetektion
* Metadatenerkennung
* Import-Log
* erste Fehlerbehandlung

**Abnahmekriterium**

* jeder Import erzeugt unabhängig vom Ergebnis ein Log

### Phase 5 Parser und Validierung

* TRY-Parser
* internes Standardschema
* technische Validierung
* fachliche Validierung
* Validierungsbericht
* Duplikatprüfung

**Abnahmekriterium**

* gültige und fehlerhafte Testdateien werden zuverlässig unterschieden

### Phase 6 Offene Wetterdatensätze

* Übersicht
* Filter
* Detailansicht
* Metadatenbearbeitung
* erneute Validierung
* Archivierung
* Löschung nach Regeln
* Log- und Berichtsanzeige

**Abnahmekriterium**

* jeder offene Datensatz ist sichtbar und bearbeitbar

### Phase 7 Aktivierung und Projekt-Default

* Freigaberegeln
* Aktivierungsaktion
* Projekt-Default
* Übergabe an `ma_parameters`
* Sperren für offene Datensätze

**Abnahmekriterium**

* nur aktive und validierte Datensätze gelangen in den regulären Workflow

### Phase 8 Wetteranalyse

* Grundstatistik
* Jahresverlauf
* Monatsauswertung
* Temperaturdauerlinie
* Extremtage
* Vergleichsfunktion
* Export der Analyseergebnisse

**Abnahmekriterium**

* mindestens zwei Datensätze können fachlich verglichen werden

### Phase 9 Tests und Dokumentation

* Unit-Tests
* Integrationstests
* UI-Tests soweit praktikabel
* Testdaten
* Fehlerfälle
* Migrationsdokumentation
* Entwicklerdokumentation
* Anwenderhinweise

## 16 Teststrategie

### 16.1 Parser

* gültige TRY-Datei
* fehlende Kopfzeile
* falsche Kodierung
* beschädigte Zeile
* unbekannte Spalte
* abweichende zeitliche Auflösung

### 16.2 Validierung

* fehlende Werte
* doppelte Zeitstempel
* Zeitlücke
* unplausible Temperatur
* negative Windgeschwindigkeit
* ungültige relative Feuchte
* fehlende Pflichtmetadaten

### 16.3 Duplikate

* gleicher Dateiname
* gleiche Prüfsumme
* gleiche Metadaten und andere Prüfsumme
* neue Version
* bereits archivierter Datensatz

### 16.4 Statuswechsel

* offen zu validiert
* validiert zu aktiv
* aktiv zu archiviert
* fehlerhaft zu erneut geprüft
* Importabbruch
* Rollback

### 16.5 UI

* Stadt ohne Datensatz
* Stadt mit einem Datensatz
* Stadt mit mehreren Datensätzen
* offener Datensatz
* fehlerhafter Datensatz
* Import mit Warnungen
* Import mit Fehlern
* Projekt-Default wechseln

## 17 Abnahmekriterien

* Karte wird in Streamlit angezeigt
* Stadt kann gesucht und ausgewählt werden
* Klimaregion wird automatisch angezeigt
* Referenzstandort wird automatisch angezeigt
* Wetterdatensätze werden korrekt gefiltert
* nur aktive und gültige Datensätze erscheinen regulär
* offene Datensätze besitzen einen eigenen Bereich
* jeder Import erzeugt eine Log-Datei
* jeder Import besitzt eine eindeutige Import-ID
* Validierungsberichte sind erreichbar
* Projekt-Default wird bewusst gesetzt
* offene Datensätze können nicht an `ma_parameters` übergeben werden
* Fachlogik ist unabhängig von Streamlit
* Tkinter kann dieselben Services verwenden
* relative Dateipfade werden genutzt
* Tests für kritische Abläufe bestehen

## 18 Offene fachliche Punkte

* tatsächliches Format der vorhandenen TRY-Dateien
* notwendige Pflichtspalten
* interne Einheiten
* erlaubte Wertebereiche
* genaue Definition der Extremtage
* gewünschte Klimaszenario-Bezeichnungen
* gewünschte Bezugszeiträume
* Umgang mit Sommer- und Winterdatensätzen
* fachliche Prüfung einzelner Stadtzuordnungen
* endgültige ID-Schreibweise
* Aufbewahrungsdauer temporärer Dateien
* Berechtigungen für Löschen und Archivieren
* Definition von `valid_with_warnings`
* Umgang mit normalisierten Kopien
* Umfang des Excel- oder PDF-Exports

## 19 Risiken

* Unterschiede zwischen vorhandenen TRY-Dateiformaten
* inkonsistente Metadaten in Quelldateien
* unvollständige Standortzuordnung
* zu starke Kopplung an Streamlit
* Dateisystem und Datenbank laufen auseinander
* unvollständiger Rollback
* unkontrolliertes Überschreiben bestehender Datensätze
* Verwendung offener Datensätze in Varianten
* zu früher Ausbau der interaktiven Karte
* zu große erste Implementierungsstufe

## 20 Arbeitsauftrag für Codex

### Schritt 1 Analyse

* vorhandenes Repository vollständig analysieren
* relevante Ordner und Dateien identifizieren
* bestehende Architektur und Namenskonventionen dokumentieren
* vorhandene Streamlit-Seiten und Navigationslogik prüfen
* vorhandene Datenbankmodelle und Migrationen prüfen
* vorhandene Logging- und Validierungslösungen prüfen
* vorhandene Tests prüfen
* vorhandene Wetterfunktionen suchen

### Schritt 2 Integrationsvorschlag

* diesen Plan mit der vorhandenen Struktur vergleichen
* keine parallele neue Architektur erzeugen
* vorhandene Komponenten bevorzugt erweitern
* notwendige neue Dateien nennen
* anzupassende bestehende Dateien nennen
* Datenbankmigrationen beschreiben
* Abhängigkeiten und Risiken nennen
* Umsetzung in kleine Arbeitspakete gliedern

### Schritt 3 Bestätigung

* vor größeren Codeänderungen einen konkreten Änderungsplan vorlegen
* betroffene Dateien auflisten
* geplante neue Funktionen auflisten
* Datenbankänderungen erklären
* offene Fragen kennzeichnen
* erst nach Bestätigung implementieren

### Schritt 4 Umsetzung

* Arbeitspakete nacheinander umsetzen
* nach jedem Paket Tests ausführen
* keine bestehende Funktion ohne Begründung entfernen
* Änderungen dokumentieren
* keine UI-Fachlogik vermischen
* keine absoluten Benutzerpfade einbauen
* keine Datensätze automatisch aktivieren oder als Default setzen

## 21 Vorgeschlagene erste Codex-Aufgabe

```text
Analysiere zuerst die vorhandene Projektstruktur und vergleiche sie mit dem beigefügten Implementierungsplan für ma_weather.

Erzeuge noch keinen vollständigen neuen Modulbaum und ändere noch keinen produktiven Code.

Liefere zuerst

1. eine Übersicht der vorhandenen relevanten Dateien und Module
2. eine Zuordnung der vorhandenen Komponenten zu den geplanten Funktionen
3. eine Liste fehlender Komponenten
4. einen Integrationsvorschlag, der die bestehende Architektur erhält
5. einen schrittweisen Änderungsplan
6. eine Liste der betroffenen Dateien
7. offene fachliche und technische Fragen
8. Risiken und mögliche Konflikte

Beachte besonders

* Streamlit ist die primäre UI
* Fachlogik bleibt UI-unabhängig
* die Stadt ist der primäre Auswahlpunkt
* Klimaregion und Referenzstandort werden automatisch ermittelt
* nur aktive und validierte Datensätze sind regulär auswählbar
* offene Datensätze erhalten einen eigenen Bearbeitungsbereich
* jeder Import erzeugt eine dauerhafte Log-Datei
* ein Import setzt nicht automatisch den Projekt-Default
* relative Dateipfade sind verpflichtend
* bestehende Projektstrukturen und Namenskonventionen haben Vorrang vor einer neuen Parallelstruktur
```
