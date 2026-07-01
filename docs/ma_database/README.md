# ma_database

- **Zweck:** Spaetere moduluebergreifende Persistenz und Repository-Schnittstellen.
- **Eingaben:** freigegebene fachliche Datenmodelle, spaeter auch
  Gebaeudemodellversionen, Importprotokolle und Katalogversionen aus P012.
- **Ausgaben:** persistierte Projekt-, Modell-, Run- und Ergebnisdaten.
- **Abgrenzung:** bestehende SQLAlchemy-/Alembic-Logik in `ma_variants` wird
  noch nicht verschoben; fachliche Berechnungen bleiben in den Fachmodulen.
- **Abhaengigkeiten:** `ma_core`; Phase 0.
- **Status:** geplant; bestehende Datenbanklogik liegt noch ausserhalb des Zielmoduls.
- **Naechster Schritt:** moduluebergreifenden Persistenzbedarf,
  Modellversionierung, Importprotokolle und Migrationsgrenzen festlegen.
