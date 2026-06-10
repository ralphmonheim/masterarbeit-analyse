# Cleanup Plan

Stand: 2026-06-10

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

## Aenderungen mit Rueckfragebedarf

- Bestehende Analyse-GUI in mehrere Dateien aufteilen.
- Allgemein nutzbare UI-Bestandteile aus `src/ma_analyse/gui/` nach `ma_ui` auslagern.
- Neue Zielpakete `ma_parameters`, `ma_simulation_setup`, `ma_export_ida`, `ma_import_ida`, `ma_assessment`, `ma_building` oder `ma_feedback` anlegen.
- Bestehende `src/ma_ui/pages/`-Struktur nach und nach durch konkrete
  `src/ma_ui/module_views/` ersetzen.
- Bestehendes `src/ma_workflow/actions.py` nach und nach durch echte
  Dashboard-Aktionen, Runner und Feedback-Routing ergaenzen.
- `ma_variants.economic_analysis` in ein spaeteres `ma_assessment/economics/`
  ueberfuehren.
- Service-Fassade fachlich erweitern und Ergebnisobjekte detaillierter fuellen.
- Bestehende Verantwortlichkeiten aus `ma_variants` in neue Zielmodule verschieben.
- Heating-/Cooling-Dateien weiter zerlegen.
- Alte lokale Dateien aus `data/test_output/` loeschen, falls sie nicht vorher gesichtet wurden.

## Spaetere Refactorings

- `src/ma_analyse/gui/app.py` in Layout, State, Dialoge, Runner und Ergebnisanzeige aufteilen.
- `ma_ui` und `ma_workflow` schrittweise erweitern, ohne Fachlogik in die UI zu ziehen.
- `ma_parameters`, `ma_export_ida` und `ma_assessment` erst nach stabilen Schnittstellen aus bestehenden `ma_variants`-Bereichen extrahieren.
- `ma_simulation_setup` als eigenen Slice zwischen Variantenbildung und
  IDA-Export vorbereiten.
- `src/ma_analyse/analysis/heating.py` und `cooling.py` ueber gemeinsame Energy-Komponenten weiter vereinheitlichen.
- `ma_weather` TRY-Importer, Validierung, Kennwerte, Diagramme und Bericht schrittweise ergaenzen.
- Gemeinsame Code-Komponenten nur dann unter `src/ma_common/` anlegen, wenn echte Wiederverwendung entsteht.

## Nicht anfassen

- Bestehende Simulationsergebnisse und IDA-ICE-Rohdaten ohne Backup.
- Bestehende Analysefunktionen ohne gezielte Pruefung.
- Bestehende `ma_analyse`-GUI ohne eigenen Refactoring-Plan.
- Bestehende Tkinter-GUI nicht direkt nach Streamlit kopieren.
- Aktuelle `ma_ui`- und `ma_workflow`-Zwischenstaende nicht umbenennen, ohne
  Tests und Importpfade im selben Slice anzupassen.
- Alembic-Migrationen ohne Datenbankgrund.
- `docs/examples/plot_templates/`, ausser neue Beispielgalerie wird bewusst erzeugt.

## Empfohlene Reihenfolge

1. P003 abgeschlossen halten und bei Strukturentscheidungen pflegen.
2. P005 Architekturreview als Referenz fuer neue Modulentscheidungen verwenden.
3. P005 naechster technischer Slice: Analyse-Seite fachlich erweitern oder
   vorbereitete Platzhalter-Views mit echten Services befuellen.
4. Danach entscheiden, ob P002 TRY-Importer/Validierung oder eine konkrete `ma_ui`-Fachseite folgt.
