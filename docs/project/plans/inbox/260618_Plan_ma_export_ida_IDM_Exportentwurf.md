# Entwurfsplan für Python Export von IDA ICE Varianten und IDM Dateien

Plan-ID: P006
Modul: `ma_export_ida`
Status: Entwurf
Stand: 2026-06-18

Dieser externe Entwurf wurde in die Plan-Inbox aufgenommen. Vor einer
Umsetzung muessen der bestehende Export unter `ma_variants`, vorhandene
Konfigurationen, Datenmodelle, Pfade und Tests analysiert werden. Der Plan ist
keine Freigabe fuer direkte IDM-Manipulation oder eine ungepruefte
IDA-ICE-API-Anbindung.

## Ziel des Arbeitspakets

Ziel ist die Entwicklung eines kontrollierten Python Workflows, mit dem Varianten aus dem Variantenkatalog in Richtung IDA ICE vorbereitet werden können. Python soll dabei nicht als vollständiger Generator für komplette IDM Modelle verstanden werden, sondern als Pre-Processing Werkzeug zur kontrollierten Variantenbildung auf Basis eines geprüften IDA ICE Referenzmodells.

Das Referenzmodell wird in IDA ICE erstellt und geprüft. Python soll daraus Varianten ableiten, Parameter dokumentieren, Dateien strukturiert ablegen und später eine Schnittstelle zur teilautomatisierten oder automatisierten Übergabe an IDA ICE vorbereiten.

Der Fokus liegt zunächst auf einem robusten Entwurf. Es soll nicht direkt eine vollständige IDA ICE Automatisierung umgesetzt werden, solange nicht geprüft wurde, welche API Funktionen, Lizenzen und Dateiformate lokal verfügbar sind.

## Grundannahmen

1. Es existiert ein geprüftes IDA ICE Referenzmodell als Ausgangsdatei.

2. Der Variantenkatalog existiert bereits in Excel oder wird später über eine Datenbank bereitgestellt.

3. Varianten werden nicht frei in eine IDM Datei geschrieben, sondern aus einem validierten Referenzmodell abgeleitet.

4. Die direkte Bearbeitung von IDM Dateien wird nur dann umgesetzt, wenn die jeweilige Datei als textbasiertes Format vorliegt und die Struktur sicher verarbeitet werden kann.

5. Wenn eine IDA ICE API oder eine Skriptschnittstelle lokal verfügbar ist, soll diese bevorzugt genutzt werden.

6. Die Automatisierung soll modular aufgebaut werden, damit spätere Änderungen an IDA ICE, Datenbank, Streamlit UI oder Variantenlogik möglich bleiben.

## Einordnung in die bestehende Projektstruktur

Der Workflow soll in die bestehende Modulstruktur der Masterarbeit integriert werden.

Vorgesehene Modulabfolge

```text
ma_parameters
ma_variants
ma_simulation_setup
ma_export_ida
IDA ICE Simulation
ma_import_ida
ma_analyse
```

Die Aufgabe dieses Arbeitspakets liegt primär im Modul `ma_export_ida`.

Zusätzlich müssen Schnittstellen zu `ma_parameters`, `ma_variants` und `ma_simulation_setup` vorbereitet werden.

## Zielstruktur für das Modul ma_export_ida

Vorgeschlagene Ordnerstruktur

```text
ma_export_ida/
    __init__.py
    config.py
    models.py
    services.py
    validators.py
    template_renderer.py
    export_variants.py
    ida_api_client.py
    ida_text_tools.py
    README.md

    templates/
        baseline_reference/
            README.md
            baseline_reference.idm

        ida_scripts/
            set_zone_parameters.lsp.j2
            set_system_parameters.lsp.j2
            set_simulation_setup.lsp.j2

    mappings/
        ida_parameter_map.json
        ida_parameter_map.xlsx

    exports/
        .gitkeep

    logs/
        .gitkeep

    tests/
        test_models.py
        test_validators.py
        test_template_renderer.py
        test_export_variants.py
```

## Aufgaben des Moduls

Das Modul `ma_export_ida` soll folgende Aufgaben übernehmen.

1. Ein geprüftes IDA ICE Referenzmodell als Vorlage erkennen.

2. Für jede Variante einen eigenen Exportordner erzeugen.

3. Die Referenzdatei in den Exportordner kopieren.

4. Variantenparameter aus einer strukturierten Quelle einlesen.

5. Die Variantenparameter gegen fachliche Wertebereiche prüfen.

6. Eine technische Mapping Tabelle zwischen Variantenkatalog und IDA ICE Zielparametern verwenden.

7. Optional IDA ICE Skripte aus Templates erzeugen.

8. Optional eine spätere API Anbindung vorbereiten.

9. Für jede exportierte Variante eine Metadatendatei erzeugen.

10. Eine Exportübersicht als CSV oder JSON erzeugen.

11. Fehler und Warnungen nachvollziehbar dokumentieren.

## Abgrenzung

In dieser ersten Entwicklungsstufe soll nicht umgesetzt werden

1. Vollständiges Schreiben einer IDM Datei von null.

2. Direkte Veränderung beliebiger IDM Inhalte ohne Parser und Validierung.

3. Vollautomatisches Starten von IDA ICE Simulationen.

4. Automatischer Import von Simulationsergebnissen.

5. Vollständige Datenbankintegration.

Diese Punkte können später ergänzt werden, wenn die Grundstruktur stabil ist.

## Entwicklungsstufe 1

Ziel dieser Stufe ist eine stabile Projektstruktur ohne direkte IDA ICE Bearbeitung.

Umzusetzen sind

1. Ordnerstruktur für `ma_export_ida` anlegen.

2. Datenmodelle für Variantenparameter definieren.

3. Validierung der Eingabewerte erstellen.

4. Konfigurationsdatei für Pfade und Standardeinstellungen erstellen.

5. Exportordner pro Variante erzeugen.

6. Basismodell in Exportordner kopieren.

7. Metadaten je Variante speichern.

8. Exportübersicht erzeugen.

Erwartetes Ergebnis

```text
exports/
    V001/
        V001.idm
        variant_parameters.json
        export_metadata.json

    V002/
        V002.idm
        variant_parameters.json
        export_metadata.json

    export_index.csv
```

## Entwicklungsstufe 2

Ziel dieser Stufe ist die Vorbereitung der fachlichen Parameterübergabe.

Umzusetzen sind

1. Mapping Datei `ida_parameter_map.json` erstellen.

2. Struktur für Variantenparameter erweitern.

3. Parametergruppen anlegen.

4. Heizungsparameter.

5. Kühlungsparameter.

6. Lüftungsparameter.

7. Fensterparameter.

8. Sonnenschutzparameter.

9. Simulationssetup.

10. Standort und Wetterdatensatz als Referenz.

Beispielhafte Parametergruppen

```text
heating
    supply_temperature_c
    return_temperature_c
    system_type
    energy_carrier

cooling
    supply_temperature_c
    return_temperature_c
    system_type

ventilation
    air_change_rate_1h
    supply_air_temperature_c
    heat_recovery_efficiency
    co2_control_enabled

windows
    u_value
    g_value
    window_to_wall_ratio

shading
    shading_type
    activation_temperature_c
    activation_solar_radiation_w_m2

simulation_setup
    start_date
    end_date
    timestep_minutes
    weather_file_id
```

Erwartetes Ergebnis

1. Variantenparameter können strukturiert geladen werden.

2. Werte werden vor dem Export validiert.

3. Für jede Variante wird nachvollziehbar gespeichert, welche Werte verwendet wurden.

## Entwicklungsstufe 3

Ziel dieser Stufe ist die Erzeugung von IDA ICE Skriptvorlagen.

Umzusetzen sind

1. Jinja2 als Template Engine prüfen und einbinden.

2. Templates für IDA ICE Skripte vorbereiten.

3. Pro Variante ein Skript erzeugen.

4. Skript im Exportordner der Variante speichern.

5. Noch keine ungetesteten IDA Befehle fest einbauen.

6. Platzhalter und Kommentare verwenden, bis echte IDA ICE Befehle verifiziert sind.

Beispielhafte Ausgabestruktur

```text
exports/
    V001/
        V001.idm
        V001_set_parameters.lsp
        variant_parameters.json
        export_metadata.json
```

Wichtiger Hinweis für Codex

Die konkreten IDA ICE Befehle dürfen nicht erfunden werden. Falls keine lokalen Beispiele oder keine API Dokumentation im Projekt vorhanden sind, soll Codex Platzhalter verwenden und die Stellen eindeutig markieren.

## Entwicklungsstufe 4

Ziel dieser Stufe ist die Prüfung einer IDA ICE API Anbindung.

Umzusetzen sind

1. Prüfen, ob im Projekt bereits Hinweise auf eine IDA ICE API, icepy oder lokale Skriptbeispiele vorhanden sind.

2. Prüfen, ob lokale IDA ICE Installationspfade oder Dokumentationen vorhanden sind.

3. Keine API Funktionen hart codieren, solange die lokale Verfügbarkeit nicht bestätigt ist.

4. Eine Adapter Klasse vorbereiten.

5. Die Adapter Klasse so schreiben, dass sie später echte API Funktionen kapseln kann.

Beispielhafte Architektur

```text
ida_api_client.py

class IdaApiClient
    connect
    open_document
    set_attribute
    save_document
    run_script
    close
```

In der ersten Version dürfen diese Funktionen noch als nicht implementiert markiert werden. Wichtig ist die Architektur, nicht die sofortige Funktionalität.

## Entwicklungsstufe 5

Ziel dieser Stufe ist die Integration in den gesamten Workflow.

Umzusetzen sind

1. Schnittstelle zu `ma_variants` vorbereiten.

2. Schnittstelle zu `ma_simulation_setup` vorbereiten.

3. Exportfunktion über eine zentrale Funktion aufrufbar machen.

4. Optional später Streamlit Button vorbereiten.

5. Keine UI Logik direkt in `ma_export_ida` einbauen.

6. UI und Fachlogik trennen.

Vorgeschlagene Hauptfunktion

```python
export_ida_variants(
    variants_source,
    baseline_model_path,
    output_dir,
    mapping_path,
    simulation_setup
)
```

Die Funktion soll später aus einer CLI, aus Streamlit oder aus einem anderen Modul aufgerufen werden können.

## Technische Leitlinien

1. Klare Trennung zwischen Datenmodell, Validierung, Exportlogik und späterer IDA ICE Kommunikation.

2. Keine Pfade hart im Code hinterlegen.

3. Pfade über `config.py` oder eine externe Konfigurationsdatei steuern.

4. Jede Variante muss eine eindeutige Varianten ID besitzen.

5. Jede erzeugte Datei muss nachvollziehbar einer Variante zugeordnet werden können.

6. Alle automatisch erzeugten Dateien müssen in einem Exportordner landen.

7. Jede Variante erhält eine eigene JSON Datei mit allen Eingangsparametern.

8. Jede Variante erhält eine eigene JSON Datei mit Exportmetadaten.

9. Fehler sollen nicht still ignoriert werden.

10. Bei unklaren IDA ICE Parametern soll Codex nicht raten, sondern eine klar markierte offene Stelle dokumentieren.

## Validierung

Die Validierung soll mindestens folgende Prüfungen enthalten.

1. Varianten ID vorhanden.

2. Varianten ID enthält keine problematischen Zeichen für Dateinamen.

3. Basismodell existiert.

4. Exportordner ist beschreibbar.

5. Pflichtparameter vorhanden.

6. Temperaturwerte liegen in plausiblen Bereichen.

7. Luftwechselwerte liegen in plausiblen Bereichen.

8. Simulationszeitraum ist logisch.

9. Wetterdatensatz ist referenziert.

10. Mapping Datei ist vorhanden und lesbar.

Beispielhafte fachliche Grenzwerte

```text
heating_supply_temperature_c
    Minimum 25
    Maximum 80

heating_return_temperature_c
    Minimum 20
    Maximum 70

cooling_supply_temperature_c
    Minimum 6
    Maximum 22

cooling_return_temperature_c
    Minimum 10
    Maximum 28

air_change_rate_1h
    Minimum 0
    Maximum 10

timestep_minutes
    Erlaubt 5, 10, 15, 30, 60
```

Diese Grenzwerte sind als erste technische Plausibilitätsprüfung zu verstehen und müssen später fachlich geprüft werden.

## Teststrategie

Für die erste Umsetzung sollen Unit Tests erstellt werden.

Zu testen sind

1. Laden einer Beispielvariante.

2. Validierung gültiger Parameter.

3. Ablehnung ungültiger Parameter.

4. Erzeugung eines Exportordners.

5. Kopieren einer Dummy IDM Datei.

6. Schreiben einer Parameter JSON Datei.

7. Schreiben einer Metadaten JSON Datei.

8. Erzeugung eines Skripts aus Template.

9. Erstellung einer Exportübersicht.

Es soll mit Dummy Dateien getestet werden, damit die Tests ohne IDA ICE Installation laufen.

## Dokumentation

Im Modul `ma_export_ida` soll eine README Datei erstellt werden.

Die README soll erklären

1. Zweck des Moduls.

2. Rolle im Gesamtworkflow.

3. Erwartete Eingangsdaten.

4. Erzeugte Ausgangsdaten.

5. Grenzen der aktuellen Umsetzung.

6. Umgang mit IDM Dateien.

7. Unterschied zwischen Dateikopie, Skripterzeugung und späterer API Anbindung.

8. Offene Punkte für IDA ICE Tests.

Zusätzlich soll eine Datei `OFFENE_PUNKTE.md` angelegt werden.

Dort sollen alle Punkte gesammelt werden, die nicht ohne lokale IDA ICE Prüfung entschieden werden können.

## Akzeptanzkriterien für die erste Version

Die erste Version gilt als erfolgreich, wenn folgende Punkte erfüllt sind.

1. Das Modul `ma_export_ida` ist angelegt.

2. Eine Beispielvariante kann verarbeitet werden.

3. Ein Dummy Basismodell wird kopiert.

4. Ein Exportordner pro Variante wird erzeugt.

5. Parameter und Metadaten werden als JSON gespeichert.

6. Eine Exportübersicht wird erzeugt.

7. Ungültige Varianten werden abgefangen.

8. Es gibt erste Unit Tests.

9. Es gibt eine README.

10. Es werden keine ungesicherten Änderungen direkt in IDM Dateien vorgenommen.

## Vorgehen für Codex

Codex soll zuerst den bestehenden Projektstand analysieren.

Dabei prüfen

1. Gibt es bereits ein Modul `ma_export_ida`.

2. Gibt es bereits Konfigurationsdateien.

3. Gibt es bereits zentrale Pfadlogik.

4. Gibt es bereits Datenmodelle für Varianten.

5. Gibt es bereits Tests.

6. Gibt es bereits eine Dokumentationsstruktur.

7. Gibt es bereits Hinweise auf IDA ICE Export, IDM Dateien oder API Nutzung.

Danach soll Codex einen konkreten Umsetzungsplan für die erste Entwicklungsstufe vorschlagen.

Codex soll noch keinen Code ändern, bevor der Plan bestätigt wurde.

## Konkreter Arbeitsauftrag an Codex

Bitte analysiere den aktuellen Projektstand und erstelle einen konkreten Umsetzungsplan für das Modul `ma_export_ida`.

Ziel ist ein kontrollierter Python Exportworkflow für IDA ICE Varianten auf Basis eines geprüften Referenzmodells. Python soll zunächst keine vollständigen IDM Dateien neu erzeugen und keine ungesicherten Änderungen in IDM Dateien schreiben. In der ersten Stufe soll ein robustes Exportgerüst entstehen, das Variantenparameter validiert, pro Variante einen Exportordner erzeugt, ein Basismodell kopiert, Parameter und Metadaten als JSON speichert und eine Exportübersicht erzeugt.

Bitte prüfe zuerst die bestehende Projektstruktur. Falls passende Module, Konfigurationslogik, Datenmodelle oder Tests bereits existieren, sollen diese wiederverwendet werden. Falls nicht, schlage eine saubere neue Struktur vor.

Bitte liefere zuerst nur einen Plan mit Dateien, Funktionen, Verantwortlichkeiten, Tests und offenen Punkten. Setze noch nichts um, bevor ich den Plan bestätigt habe.
