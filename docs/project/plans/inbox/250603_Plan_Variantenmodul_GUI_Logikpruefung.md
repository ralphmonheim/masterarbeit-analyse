250603_Plan_Variantenmodul_GUI_Logikpruefung.md

Du arbeitest in einem bestehenden Python Projekt für die Variantenplanung, Simulationsergebnisanalyse und spätere Bewertung von IDA ICE Varianten.

Ziel dieses Abschnitts ist nicht, das Variantenmodul komplett neu zu bauen. Ziel ist zuerst zu prüfen, welche Logik für Varianten, Parameterimport, Variantenzählung, Variantenauswahl und Namensgebung bereits vorhanden ist. Danach soll darauf aufbauend eine erste GUI oder GUI-Vorstruktur für das Variantenmodul erstellt werden.

Wichtig
Es existiert bereits eine GUI für die Analyse der Varianten beziehungsweise Simulationsergebnisse. Diese vorhandene GUI soll als Design-Vorlage dienen. Prüfe daher zuerst, ob Dateien wie `run_pipeline_gui.py`, `run_pipeline_display.py` oder ähnliche GUI-Dateien vorhanden sind. Übernimm Struktur, Bedienlogik und visuelle Grundidee, soweit sinnvoll. Baue aber keine Analysefunktionen in das Variantenmodul ein.

## Aufgabe 1

## Bestand prüfen

Analysiere zuerst die vorhandene Projektstruktur.

Prüfe insbesondere

1. Welche Module oder Dateien bereits für Varianten existieren
2. Welche Module oder Dateien bereits für Parameterimport existieren
3. Welche Module oder Dateien bereits für Optionsimport existieren
4. Welche Module oder Dateien bereits für Variantenzählung existieren
5. Welche Module oder Dateien bereits für Variantenauswahl existieren
6. Welche Module oder Dateien bereits für Namensgebung existieren
7. Welche GUI-Dateien bereits vorhanden sind
8. Welche GUI-Logik als Vorlage verwendet werden kann
9. Welche Datenordner und Konfigurationsordner bereits existieren
10. Welche Beispiel- oder Testdatensätze bereits vorhanden sind

Erstelle danach eine kurze Übersicht mit

* vorhandene relevante Dateien
* vorhandene relevante Funktionen
* fehlende Funktionen
* mögliche Wiederverwendung der bestehenden GUI-Struktur
* Risiken oder Unklarheiten

Nimm bis zu diesem Punkt keine größeren Codeänderungen vor.

## Aufgabe 2

## Ziel für die Variantenoberfläche festlegen

Plane eine erste Oberfläche für das Variantenmodul.

Die Oberfläche soll zunächst nur eine Vorstruktur sein und auf vorhandener Logik aufbauen.

Die GUI soll perspektivisch folgende Bereiche enthalten

1. Parameterimport
2. Optionsimport
3. Anzeige importierter Parameter
4. Anzeige importierter Optionsgruppen
5. Berechnung der theoretischen Variantenanzahl
6. Erzeugung einfacher Varianten
7. Auswahl von Varianten
8. Namensgebung der Varianten
9. Export der Variantenübersicht

Setze nur die Funktionen direkt um, für die bereits Logik vorhanden ist oder die mit einfachen Platzhalterfunktionen sauber vorbereitet werden können.

## Aufgabe 3

## GUI-Struktur erstellen

Erstelle eine neue GUI-Datei für das Variantenmodul.

Bevorzugter Dateiname

`run_variant_manager_gui.py`

Falls im Projekt eine andere Namenslogik verwendet wird, passe den Namen daran an und begründe dies kurz.

Die Oberfläche soll sich optisch und strukturell an der vorhandenen Analyse-GUI orientieren.

Die GUI soll mindestens folgende Bereiche enthalten

### Bereich 1

Parameter und Optionen

* Button zum Laden von Parametern
* Button zum Laden von Optionen
* Anzeige, wie viele Parameter geladen wurden
* Anzeige, wie viele Optionsgruppen geladen wurden
* Anzeige von Warnungen oder Importfehlern

### Bereich 2

Variantenraum

* Button zur Berechnung der theoretischen Variantenanzahl
* Anzeige der theoretischen Variantenanzahl
* Hinweis, ob Regeln und Abhängigkeiten bereits berücksichtigt werden oder noch nicht
* Button zur Erzeugung einfacher Varianten

### Bereich 3

Variantenauswahl

* Auswahlmethode als Dropdown oder Radiobutton

* Methoden vorbereiten

  * manuell
  * vollständig zufällig
  * Monte Carlo
  * Auswahl bestimmter Parameter
  * strukturierte Abdeckung
  * Sensitivitätsvarianten
  * regelbasierte Auswahl

* Zunächst dürfen Methoden, die noch nicht implementiert sind, als deaktiviert oder als Platzhalter angezeigt werden

* Implementierte Methoden sollen ausführbar sein

### Bereich 4

Namensgebung

* Button zur Namensgenerierung
* Anzeige, ob doppelte Namen gefunden wurden
* Vorschau auf einige Variantennamen

### Bereich 5

Export

* Button zum Export der Variantenübersicht
* Export zunächst als JSON, CSV oder Excel, je nachdem was im Projekt bereits vorgesehen ist
* Anzeige des Exportpfads

### Bereich 6

Status und Log

* Textfeld oder Konsolenausgabe innerhalb der GUI
* Anzeige der letzten Aktionen
* Anzeige von Fehlern
* Anzeige von Hinweisen für offene Funktionen

## Aufgabe 4

## Bestehende Logik wiederverwenden

Verwende vorhandene Funktionen, wenn sie bereits existieren.

Beispiele

* vorhandener Parameterimport
* vorhandener Optionsimport
* vorhandene Variantenzählung
* vorhandene Variantenerzeugung
* vorhandene Auswahlfunktionen
* vorhandene Namensgenerierung
* vorhandene Exportfunktionen

Wenn eine Funktion noch nicht existiert, dann

1. keine komplexe Fachlogik improvisieren
2. eine klare Platzhalterfunktion anlegen
3. im GUI-Log anzeigen, dass diese Funktion noch nicht implementiert ist
4. im Kommentar erklären, welche spätere Funktion hier angebunden werden soll

## Aufgabe 5

## Abgrenzung

In diesem Abschnitt nicht umsetzen

* keine vollständige PostgreSQL Integration
* keine vollständige IDA ICE Exportlogik
* kein automatischer Start von IDA ICE
* kein automatischer Import von Simulationsergebnissen
* keine Wirtschaftlichkeitsanalyse
* keine Produkt- oder Materialkataloge
* keine komplexen Optimierungsalgorithmen
* keine vollständige Monte Carlo Implementierung, falls dafür noch keine Grundlage existiert

## Aufgabe 6

## Dokumentation aktualisieren

Aktualisiere oder erstelle folgende Dokumentation

* `docs/WORKFLOW.md`
* `docs/VARIANTENMODUL.md`
* `docs/CHANGELOG.md`

In `docs/VARIANTENMODUL.md` soll dokumentiert werden

* Ziel des Variantenmoduls
* vorhandene Logik
* neu angelegte GUI
* vorgesehene Auswahlmethoden
* aktuell implementierte Funktionen
* Platzhalterfunktionen
* offene Punkte
* nächste sinnvolle Schritte

## Aufgabe 7

## Tests und Startbarkeit

Prüfe, ob die neue GUI startbar ist.

Falls pytest vorhanden ist, ergänze nur einfache Tests für Logikfunktionen, nicht für die komplette GUI.

Falls keine Tests sinnvoll möglich sind, dokumentiere stattdessen eine kurze manuelle Testanleitung.

Die manuelle Testanleitung soll enthalten

1. Befehl zum Starten der GUI
2. erwartete Ansicht
3. erwartetes Verhalten beim Laden von Parametern
4. erwartetes Verhalten bei der Variantenzählung
5. erwartetes Verhalten beim Export

## Wichtige Arbeitsregeln

* Vor größeren Änderungen erst kurz erklären, was geändert werden soll
* Bestehende Analyse-GUI nicht beschädigen
* Bestehende Analysefunktionen nicht ungeprüft ändern
* Keine vorhandenen Dateien löschen
* Neue GUI klar vom Analysemodul trennen
* Gemeinsame Designlogik darf übernommen werden
* Fachlogik soll in Modulen liegen, nicht direkt in der GUI
* Die GUI soll vorhandene Funktionen nur aufrufen
* Platzhalter klar als Platzhalter kennzeichnen
* Nach der Umsetzung eine Zusammenfassung der geänderten und neu angelegten Dateien ausgeben

## Erwartetes Ergebnis

Nach diesem Abschnitt soll das Projekt eine erste Oberfläche für das Variantenmodul besitzen.

Diese Oberfläche soll

* vorhandene Variantenlogik erkennen und nutzen
* Parameter und Optionen laden können, falls die Importlogik vorhanden ist
* die theoretische Variantenanzahl anzeigen können, falls die Zähllogik vorhanden ist
* Auswahlmethoden sichtbar vorbereiten
* Namensgebung und Export sichtbar vorbereiten
* sich gestalterisch an der vorhandenen Analyse-GUI orientieren
* noch nicht implementierte Funktionen sauber als Platzhalter kennzeichnen

Beginne jetzt mit der Analyse der vorhandenen Projektstruktur und gib zuerst eine kurze Bestandsaufnahme aus. Danach schlage die konkrete Umsetzung der Varianten-GUI vor.
