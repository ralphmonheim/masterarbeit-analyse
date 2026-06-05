# Cleanup Plan

Stand: 2026-06-05

## Sichere Sofortmassnahmen

- Erledigt: Leeren Ordner `scripts/` entfernen.
- Erledigt: Planungsdokumentation modularisieren.
- Erledigt: Nutzerentscheidungen von technischen Entscheidungen trennen.
- Erledigt: `data/test_output/` als lokalen, semi-wichtigen Arbeitsordner dokumentieren.
- Erledigt: `docs/examples/plot_templates/` als wichtige Referenzgalerie dokumentieren.
- Erledigt: Externe OneDrive-Plaene in die Plan-Inbox uebernehmen und konsistente Markdown-Dateinamen verwenden.
- Erledigt: `ma_analyse` hart auf `data/ma_analyse/input`, `data/ma_analyse/database` und `data/ma_analyse/output` migrieren.
- Erledigt: Alten leeren Root-Dokumentenordner entfernen; aktive Katalogdokumente liegen unter `data/catalogs/documents/`.

## Aenderungen mit Rueckfragebedarf

- Bestehende Analyse-GUI in mehrere Dateien aufteilen.
- Heating-/Cooling-Dateien weiter zerlegen.
- Alte lokale Dateien aus `data/test_output/` loeschen, falls sie nicht vorher gesichtet wurden.

## Spaetere Refactorings

- `src/ma_analyse/gui/app.py` in Layout, State, Dialoge, Runner und Ergebnisanzeige aufteilen.
- `src/ma_analyse/analysis/heating.py` und `cooling.py` ueber gemeinsame Energy-Komponenten weiter vereinheitlichen.
- `src/ma_weather/` erst nach geprueftem TRY-Plan anlegen.
- Gemeinsame Code-Komponenten nur dann unter `src/ma_common/` anlegen, wenn echte Wiederverwendung entsteht.

## Nicht anfassen

- Bestehende Simulationsergebnisse und IDA-ICE-Rohdaten ohne Backup.
- Bestehende Analysefunktionen ohne gezielte Pruefung.
- Alembic-Migrationen ohne Datenbankgrund.
- `docs/examples/plot_templates/`, ausser neue Beispielgalerie wird bewusst erzeugt.

## Empfohlene Reihenfolge

1. P003 abgeschlossen halten und bei Strukturentscheidungen pflegen.
2. P001 Variantenmodul GUI und Logikpruefung manuell pruefen und danach archivieren.
3. P002 Wetterdatenanalyse TRY pruefen.
4. Danach weitere `ma_analyse`-Refactorings separat planen.
