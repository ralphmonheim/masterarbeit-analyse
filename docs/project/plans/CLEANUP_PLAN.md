# Cleanup Plan

Stand: 2026-06-08

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

## Aenderungen mit Rueckfragebedarf

- Bestehende Analyse-GUI in mehrere Dateien aufteilen.
- Allgemein nutzbare UI-Bestandteile aus `src/ma_analyse/gui/` nach `ma_ui` auslagern.
- Neue Zielpakete `ma_ui`, `ma_workflow`, `ma_parameters`, `ma_simulation_setup`, `ma_export_ida`, `ma_import_ida`, `ma_assessment`, `ma_building` oder `ma_feedback` anlegen.
- Bestehende Verantwortlichkeiten aus `ma_variants` in neue Zielmodule verschieben.
- Heating-/Cooling-Dateien weiter zerlegen.
- Alte lokale Dateien aus `data/test_output/` loeschen, falls sie nicht vorher gesichtet wurden.

## Spaetere Refactorings

- `src/ma_analyse/gui/app.py` in Layout, State, Dialoge, Runner und Ergebnisanzeige aufteilen.
- `ma_ui` und `ma_workflow` als minimale Shell vorbereiten, sobald die UI-Technik entschieden ist.
- `ma_parameters`, `ma_export_ida` und `ma_assessment` erst nach stabilen Schnittstellen aus bestehenden `ma_variants`-Bereichen extrahieren.
- `src/ma_analyse/analysis/heating.py` und `cooling.py` ueber gemeinsame Energy-Komponenten weiter vereinheitlichen.
- `ma_weather` TRY-Importer, Validierung, Kennwerte, Diagramme und Bericht schrittweise ergaenzen.
- Gemeinsame Code-Komponenten nur dann unter `src/ma_common/` anlegen, wenn echte Wiederverwendung entsteht.

## Nicht anfassen

- Bestehende Simulationsergebnisse und IDA-ICE-Rohdaten ohne Backup.
- Bestehende Analysefunktionen ohne gezielte Pruefung.
- Bestehende `ma_analyse`-GUI ohne eigenen Refactoring-Plan.
- Alembic-Migrationen ohne Datenbankgrund.
- `docs/examples/plot_templates/`, ausser neue Beispielgalerie wird bewusst erzeugt.

## Empfohlene Reihenfolge

1. P003 abgeschlossen halten und bei Strukturentscheidungen pflegen.
2. P005 Architekturreview als Referenz fuer neue Modulentscheidungen verwenden.
3. P002 Wetterdatenanalyse TRY pruefen.
4. Danach entscheiden, ob `ma_ui`/`ma_workflow` als Shell vorbereitet werden oder weitere `ma_analyse`-Refactorings separat geplant werden.
