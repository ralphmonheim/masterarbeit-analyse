250603_Plan_Wetterdatenanalyse_TRY_Integration.md

Du arbeitest in einem bestehenden Python Projekt zur Auswertung und Weiterverarbeitung von IDA ICE Varianten und Simulationsergebnissen.

Ziel dieses Abschnitts ist die Integration eines eigenständigen Wetterdatenmoduls für TRY-Wetterdaten. Es soll kein neues separates Projekt erstellt werden. Das Modul soll sich in die vorhandene Projektstruktur einfügen und bestehende Konventionen für Ordner, Pfade, Ausgabeordner, Logging, Reports und Tests übernehmen.

Wichtig

Die Wetterdatenanalyse ist fachlich eigenständig. TRY-Wetterdaten sind Eingangs- und Randbedingungsdaten. Die vorhandene Analyse der Zonenwerte behandelt Simulationsergebnisse aus IDA ICE. Beide Bereiche dürfen in dieser Umsetzung nicht vermischt werden. Eine spätere Verbindung zwischen Wetterdaten, Varianten und Simulationsergebnissen darf vorbereitet und dokumentiert werden, soll aber noch nicht vollständig programmiert werden.

Außerdem gilt

Der automatische Export von Varianten nach IDA ICE und der automatische Import von Simulationsergebnissen sind aktuell nicht Kern dieser Umsetzung. Diese Schritte werden für die Masterarbeit voraussichtlich händisch durchgeführt. Dokumentiere nur, wo spätere Automatisierung möglich wäre.

## Aufgabe 1

## Bestehende Projektstruktur analysieren

Analysiere zuerst die vorhandene Projektstruktur.

Prüfe insbesondere

1. Welche Ordner für Eingabedaten existieren
2. Welche Ordner für Ausgabedaten existieren
3. Welche Ordner für Diagramme und Reports existieren
4. Welche Ordner für Konfigurationen existieren
5. Welche Ordner für Tests existieren
6. Welche zentrale Pfadlogik bereits vorhanden ist
7. Ob Funktionen wie get_run_id, OUTPUT_DIR, INPUT_DIR oder DATENBANK_DIR existieren
8. Welche bestehenden Auswertungsskripte für Zonenwerte existieren
9. Welche bestehende GUI oder Displaylogik vorhanden ist
10. Welche Namenskonventionen im Projekt bereits verwendet werden

Nimm bis zu diesem Punkt keine größeren Codeänderungen vor.

Gib zuerst eine kurze Bestandsaufnahme aus mit

* relevanten vorhandenen Dateien
* relevanten vorhandenen Funktionen
* vorhandenen Pfadkonventionen
* geeigneter Stelle für das neue Wettermodul
* Risiken oder Unklarheiten

## Aufgabe 2

## Zielstruktur für das Wettermodul vorschlagen

Schlage nach der Analyse eine passende Zielstruktur vor.

Orientiere dich an der bestehenden Projektstruktur. Wenn es noch keine passende Struktur gibt, verwende diese Zielstruktur als Vorschlag

src/weather/
**init**.py
try_importer.py
weather_validation.py
weather_metrics.py
weather_plots.py
weather_report.py
weather_catalog.py
run_weather_analysis.py

Datenordner

data/weather/raw/
data/weather/processed/
data/weather/plots/
data/weather/reports/

Falls das Projekt bereits andere Ordnernamen nutzt, passe die Struktur daran an und begründe die Entscheidung kurz.

## Aufgabe 3

## Wetterdatensatz-Ordner und Wetterkatalog vorbereiten

Lege einen eigenen Bereich für reale Wetterdatensätze an.

Die Wetterdateien sollen nicht direkt in der Datenbank gespeichert werden. Die Datenbank oder spätere Konfigurationsdateien sollen nur auf die Dateien verweisen.

Bereite dafür eine einfache Kataloglogik vor.

Ziel ist eine spätere Struktur wie

weather_key
display_name
file_path
file_format
source
location
year_type
climate_scenario
is_active
notes

Wenn PostgreSQL im aktuellen Projekt noch nicht stabil angebunden ist, dann erstelle zunächst eine YAML oder JSON Vorlage, zum Beispiel

config/weather/example_weather_datasets.yaml

Die Datei soll Wetterdatensätze über einen weather_key beschreiben und auf Dateien in data/weather/raw verweisen.

## Aufgabe 4

## TRY Importmodul erstellen

Erstelle ein Importmodul für TRY-Wetterdaten.

Datei

src/weather/try_importer.py

Die Importfunktion soll eine TRY-Datei einlesen können, bei der der eigentliche Datenblock nach einer Zeile mit drei Sternen beginnt.

Die Importfunktion soll folgende Aufgaben erfüllen

1. Datenblock automatisch erkennen
2. stündliche Daten einlesen
3. Spalten korrekt zuordnen
4. kurze TRY-Spaltennamen in verständliche interne Namen übersetzen
5. Zeitindex erzeugen
6. TRY-Stunde 1 bis 24 in eine pandas-kompatible Zeitlogik überführen
7. fehlende Werte prüfen
8. Pflichtspalten prüfen
9. Daten als pandas DataFrame zurückgeben
10. Importinformationen strukturiert zurückgeben

Verwende verständliche interne Spaltennamen, soweit die Spalten vorhanden sind

temperature_c
relative_humidity_pct
wind_direction_deg
wind_speed_m_s
direct_radiation_w_m2
diffuse_radiation_w_m2
global_radiation_w_m2

Die Globalstrahlung soll aus direkter und diffuser Strahlung berechnet werden, sofern beide Spalten vorhanden sind.

## Aufgabe 5

## Plausibilitätsprüfung ergänzen

Erstelle ein eigenes Validierungsmodul.

Datei

src/weather/weather_validation.py

Die Prüfung soll deutliche Warnungen erzeugen, aber nicht unnötig abbrechen.

Prüfe mindestens

1. Anzahl der Stundenwerte
2. Erwartungswert 8760 Stunden für ein vollständiges Jahr
3. fehlende Werte
4. doppelte Zeitstempel
5. fehlende Pflichtspalten
6. unplausible Temperaturwerte
7. negative Strahlungswerte
8. relative Feuchte außerhalb von 0 bis 100 Prozent
9. Windgeschwindigkeit kleiner 0

Das Ergebnis soll als strukturierter Validierungsbericht zurückgegeben werden, zum Beispiel als Dictionary oder dataclass.

Der Bericht soll mindestens enthalten

* status
* warnings
* errors
* row_count
* missing_columns
* missing_values
* duplicate_timestamps

## Aufgabe 6

## Wetterkennwerte berechnen

Erstelle ein eigenes Modul für Wetterkennwerte.

Datei

src/weather/weather_metrics.py

Die Kennwerte sollen getrennt von den Diagrammen berechnet werden. Diagrammfunktionen dürfen keine versteckten Kennwertberechnungen enthalten.

Berechne in der ersten Version mindestens

1. Jahresmitteltemperatur
2. minimale Außentemperatur
3. maximale Außentemperatur
4. mittlere relative Feuchte
5. mittlere Windgeschwindigkeit
6. maximale Windgeschwindigkeit
7. Globalstrahlungssumme in kWh pro Quadratmeter und Jahr
8. Stunden über 25 Grad Celsius
9. Stunden über 30 Grad Celsius
10. Heizgradstunden
11. Kühlgradstunden

Die Grenzwerte für Heizgradstunden und Kühlgradstunden sollen als Parameter übergeben werden können. Verwende sinnvolle Standardwerte, aber schreibe sie nicht fest in Diagrammfunktionen.

## Aufgabe 7

## Wetterdiagramme erzeugen

Erstelle ein eigenes Diagrammmodul.

Datei

src/weather/weather_plots.py

Jede Diagrammfunktion soll genau ein Diagramm erzeugen und speichern.

Die Diagramme sollen klare Achsenbeschriftungen, Einheiten, lesbare Skalierung und mindestens 300 dpi haben.

Erstelle in Version 1 diese Diagramme, sofern die benötigten Spalten vorhanden sind

1. Temperatur Jahresverlauf
2. Temperatur Heatmap mit Tag des Jahres und Stunde des Tages
3. monatliche Einstrahlung
4. monatliche Heiz- und Kühlgradstunden
5. Windrose
6. Temperatur-Feuchte-Streudiagramm

Wenn für ein Diagramm erforderliche Daten fehlen, soll die Funktion nicht abstürzen, sondern eine verständliche Warnung zurückgeben.

Die Dateinamen sollen reproduzierbar sein und den weather_key enthalten.

Beispiel

TRY_FFM_2015_temperature_year.png
TRY_FFM_2015_temperature_heatmap.png
TRY_FFM_2015_monthly_radiation.png

## Aufgabe 8

## Wetterbericht erzeugen

Erstelle ein Berichtsmodul.

Datei

src/weather/weather_report.py

Der Bericht soll zunächst als Markdown-Datei ausgegeben werden.

Der Bericht soll enthalten

1. Name der verwendeten TRY-Datei
2. weather_key
3. Dateipfad
4. Anzahl der eingelesenen Stundenwerte
5. Zeitraum oder abgeleiteter Zeitindex
6. wichtigste Wetterkennwerte
7. Hinweise aus der Plausibilitätsprüfung
8. Liste der erzeugten Diagramme
9. Ausgabeordner
10. offene Punkte oder Warnungen

Der Bericht soll so aufgebaut sein, dass er später in ein größeres Projektreporting übernommen werden kann.

## Aufgabe 9

## Zentrales Ausführungsskript erstellen

Erstelle ein zentrales Skript für die Wetteranalyse.

Datei

src/weather/run_weather_analysis.py

Dieses Skript soll nur die Wetteranalyse ausführen und keine Zonenwertanalyse starten.

Das Skript soll folgende Schritte ausführen

1. Wetterdatensatz aus dem Wetterkatalog auswählen
2. TRY-Datei einlesen
3. Daten validieren
4. abgeleitete Größen ergänzen
5. Wetterkennwerte berechnen
6. Diagramme erzeugen
7. Markdown-Bericht schreiben
8. kurze Zusammenfassung in der Konsole ausgeben

Falls im Projekt bereits eine zentrale Ausführungslogik existiert, passe das Skript an diese Logik an. Bestehende Analysefunktionen dürfen dadurch nicht verändert werden.

## Aufgabe 10

## Schnittstelle zum Variantenmodul vorbereiten

Bereite eine einfache spätere Verbindung zum Variantenmodul vor.

Das Wettermodul soll keine Varianten erzeugen.

Es soll nur geprüfte Wetterdatensätze bereitstellen.

Die spätere Verbindung soll über weather_key erfolgen.

Zielstruktur

weather_datasets
↓
climate_file_options
↓
PROJECT_DATA_CLIMATE
↓
Variante

Dokumentiere diese Verbindung in der Dokumentation. Implementiere nur einfache Datenstrukturen oder Konfigurationsdateien, falls sie ohne großen Umbau möglich sind.

## Aufgabe 11

## Tests ergänzen

Prüfe, ob im Projekt bereits pytest oder eine andere Teststruktur vorhanden ist.

Wenn ja, ergänze einfache Tests.

Wenn nein, schlage eine minimale Teststruktur vor und lege sie nur an, wenn es zur Projektstruktur passt.

Tests sollen mindestens prüfen

1. TRY-Datei wird eingelesen
2. 8760 Stundenwerte werden erkannt, wenn ein vollständiger Testdatensatz vorhanden ist
3. Pflichtspalten sind vorhanden
4. Zeitindex ist eindeutig
5. Globalstrahlung wird berechnet
6. Heizgradstunden sind nicht negativ
7. Kühlgradstunden sind nicht negativ
8. Kennwerte werden als strukturierte Ausgabe zurückgegeben

Falls kein echter TRY-Testdatensatz vorhanden ist, erstelle einen kleinen künstlichen Testdatensatz mit wenigen Stunden und dokumentiere, dass der 8760-Test erst mit einer echten TRY-Datei aktiviert werden kann.

## Aufgabe 12

## Dokumentation ergänzen

Erstelle oder aktualisiere

docs/WEATHER_MODULE.md
docs/WORKFLOW.md
docs/CHANGELOG.md

Die Dokumentation soll erklären

1. Ziel des Wettermoduls
2. warum Wetterdaten getrennt von Zonenwerten analysiert werden
3. wo TRY-Dateien abgelegt werden
4. wie Wetterdatensätze registriert werden
5. welches Skript gestartet wird
6. welche Kennwerte berechnet werden
7. welche Diagramme erzeugt werden
8. wo Ergebnisse gespeichert werden
9. wie weather_key später mit Varianten verbunden werden kann
10. welche Punkte noch offen sind

## Aufgabe 13

## Abgrenzung beachten

In diesem Abschnitt nicht umsetzen

1. keine Änderung der bestehenden Zonenwertanalyse
2. keine vollständige Kopplung mit Simulationsergebnissen
3. kein automatischer IDA ICE Export
4. kein automatischer IDA ICE Import
5. kein automatischer Start von IDA ICE
6. keine Wirtschaftlichkeitsanalyse
7. keine Produkt- oder Materialkataloge
8. keine vollständige PostgreSQL Pflichtintegration, wenn diese noch nicht stabil vorhanden ist
9. keine komplexe GUI, sofern diese nicht bereits vorgesehen ist

## Aufgabe 14

## Abschlussübersicht ausgeben

Gib am Ende eine Übersicht aus mit

1. neu angelegten Dateien
2. geänderten Dateien
3. kurzer Begründung je Änderung
4. Startbefehl für die Wetteranalyse
5. erzeugten Ausgabeordnern
6. offenen Punkten
7. nächsten sinnvollen Erweiterungen

## Arbeitsregeln

Vor größeren Änderungen zuerst kurz erklären, was geändert werden soll.

Bestehende Dateien nicht löschen.

Bestehende Analysefunktionen für Zonenwerte nicht ungeprüft ändern.

Fachlogik in Modulen halten, nicht direkt in Ausführungsskripten verstecken.

Jede neue Funktion soll kurz und verständlich kommentiert sein.

Fehler und Warnungen sollen verständlich ausgegeben werden.

Beginne jetzt mit Aufgabe 1 und gib zuerst eine Bestandsaufnahme der vorhandenen Projektstruktur aus. Danach schlage die konkrete Integration des Wettermoduls vor.
