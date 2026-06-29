# Cleanup Plan

Stand: 2026-06-28

## Sichere Sofortmassnahmen

- Erledigt: Leeren Ordner `scripts/` entfernen.
- Erledigt: Planungsdokumentation modularisieren.
- Erledigt: Nutzerentscheidungen von technischen Entscheidungen trennen.
- Erledigt: `data/test_output/` als lokalen, semi-wichtigen Arbeitsordner dokumentieren.
- Erledigt: `docs/examples/plot_templates/` als wichtige Referenzgalerie dokumentieren.
- Erledigt: Externe OneDrive-Plaene in die Plan-Inbox uebernehmen und konsistente Markdown-Dateinamen verwenden.
- Erledigt: `ma_analyse` hart auf `data/ma_analyse/ida_imports`, `data/ma_analyse/database` und `data/ma_analyse/output` migrieren.
- Erledigt: Alten leeren Root-Dokumentenordner entfernen; aktive Katalogdokumente liegen unter `data/catalogs/documents/`.
- Erledigt: P001 Variantenmodul GUI und Logikpruefung pruefen und archivieren.
- Erledigt: `src/ma_weather/` als Struktur-Slice nach geprueftem TRY-Plan anlegen.
- Erledigt: P005 Zielarchitektur und UI-Auslagerungsreview dokumentieren, ohne Code zu verschieben.
- Erledigt: P005 `ma_analyse`-Bestandsanalyse und Service-Schnittstellenentwurf dokumentieren.
- Erledigt: P005 minimale `ma_workflow`- und `ma_ui`-Shell anlegen, ohne bestehende GUI-Dateien zu verschieben.
- Erledigt: Erste Code-Fassade `ma_analyse.models` und `ma_analyse.services` anlegen.
- Erledigt: P005-Zielstruktur nach verschaerfter Nutzer-Ausarbeitung
  dokumentieren, ohne Code umzubenennen oder bestehende GUI-Dateien zu
  verschieben.
- Erledigt: `ma_ui/shared/`, `ma_ui/module_views/` und die geplanten
  `ma_workflow`-Aktions-/Runner-Dateien kompatibel vorbereiten, ohne alte
  `pages/`- und `actions.py`-Strukturen zu entfernen.
- Erledigt: P002, P005 und P006 unveraendert archivieren und die verbleibenden
  Aufgaben zunaechst in P007, P008 und P009 konsolidieren.
- Erledigt: P010 bis P027 als abgestufte Modul- und Querschnittsplanserie
  ergaenzen.
- Erledigt: P028 als konkreten Projekt-, Parameter- und Naming-Streamlit-Slice
  aufnehmen.
- Erledigt: P007-Zielpakete als leichte, importierbare Gerueste mit
  Modul-READMEs anlegen, ohne bestehende Fachlogik zu verschieben.
- Erledigt: Allgemeine Schnittstellen `ma_export_simulation` und
  `ma_import_simulation` mit vorbereiteten IDA-ICE-Adaptergrenzen anlegen.
- Erledigt: Tkinter-Analyse hart aus `ma_analyse` loesen; alter
  `ma_analyse.gui`-Pfad und `python -m ma_analyse gui` sind entfernt.

## Aenderungen mit Rueckfragebedarf

- Bestehende Analyse-GUI in mehrere Dateien aufteilen.
- Allgemein nutzbare UI-Bestandteile innerhalb von
  `src/ma_ui/tkinter_app/module_views/analyse/` spaeter weiter aufteilen.
- Bestehende `src/ma_ui/pages/`-Struktur nach und nach durch konkrete
  `src/ma_ui/module_views/` ersetzen.
- Den zentralen Katalog in `src/ma_workflow/catalog.py` stabil halten und
  echte Fachservice-Aufrufe schrittweise ueber die vorhandenen
  Dashboard-Aktionen, Runner und Adapter anbinden.
- `ma_variants.economic_analysis` in ein spaeteres `ma_economy` oder eine
  passende Zwischenstruktur ueberfuehren.
- Service-Fassade fachlich erweitern und Ergebnisobjekte detaillierter fuellen.
  P029 ist dafuer als aktiver Service-/Runner-Aufraeumplan angelegt.
- Bestehende Verantwortlichkeiten aus `ma_variants` in neue Zielmodule verschieben.
- Heating-/Cooling-Dateien weiter zerlegen.
- Alte lokale Dateien aus `data/test_output/` loeschen, falls sie nicht vorher gesichtet wurden.

## Spaetere Refactorings

- `src/ma_ui/tkinter_app/module_views/analyse/app.py` in Layout, State,
  Dialoge, Runner und Ergebnisanzeige aufteilen.
- `ma_ui` und `ma_workflow` schrittweise erweitern, ohne Fachlogik in die UI zu ziehen.
- `ma_parameters`, `ma_export_simulation`, `ma_economy`,
  `ma_sustainability` und `ma_assessment` erst nach stabilen Schnittstellen
  aus bestehenden `ma_variants`-Bereichen extrahieren oder neu aufbauen.
- `ma_simulation_setup` als eigenen Slice zwischen Variantenbildung und
  IDA-Export vorbereiten.
- `src/ma_analyse/analysis/heating.py` und `cooling.py` ueber gemeinsame Energy-Komponenten weiter vereinheitlichen.
  Vorher soll P029 den Service-/Runner-Vertrag stabilisieren.
- `ma_weather` TRY-Importer, Validierung, Kennwerte, Diagramme und Bericht schrittweise ergaenzen.
- Gemeinsame Code-Komponenten nur dann unter `src/ma_common/` anlegen, wenn echte Wiederverwendung entsteht.

## Nicht anfassen

- Bestehende Simulationsergebnisse und IDA-ICE-Rohdaten ohne Backup.
- Bestehende Analysefunktionen ohne gezielte Pruefung.
- Bestehende Tkinter-Analyse unter `ma_ui` ohne eigenen Refactoring-Plan.
- Bestehende Tkinter-GUI nicht direkt nach Streamlit kopieren.
- Aktuelle `ma_ui`- und `ma_workflow`-Zwischenstaende nicht umbenennen, ohne
  Tests und Importpfade im selben Slice anzupassen.
- Alembic-Migrationen ohne Datenbankgrund.
- `docs/examples/plot_templates/`, ausser neue Beispielgalerie wird bewusst erzeugt.

## Empfohlene Reihenfolge

1. P003 abgeschlossen halten und bei Strukturentscheidungen pflegen.
2. P007 als verbindliche Architektur- und Roadmap-Grundlage verwenden.
3. P010 ist umgesetzt; gemeinsame Eingabe- und Freigabevertraege in den
   folgenden Fachplaenen wiederverwenden.
4. P008 fuer Wetterabschluss, Dateiimport und Ereignisse bearbeiten.
5. P011 bis P018 fuer die Eingabekette bis Run-Manifest umsetzen.
6. P009 erst danach fuer Simulationsschnittstellen weiterfuehren.
7. Uebernommene P005-Restarbeiten ueber P027 begleiten.
8. P028 ist als erster gemeinsamer Konfigurations-Slice umgesetzt; seine
   produktiven Folgearbeiten ueber P011, P015 und P017 weiterfuehren.
