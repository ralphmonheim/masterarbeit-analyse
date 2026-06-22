# ma_database

- **Zweck:** Spaetere moduluebergreifende Persistenz und Repository-Schnittstellen.
- **Eingaben:** freigegebene fachliche Datenmodelle.
- **Ausgaben:** persistierte Projekt-, Run- und Ergebnisdaten.
- **Abgrenzung:** bestehende SQLAlchemy-/Alembic-Logik in `ma_variants` wird noch nicht verschoben.
- **Abhaengigkeiten:** `ma_core`; Phase 0.
- **Status:** teilweise vorhanden, eigenes Zielpaket ist nur strukturell vorbereitet.
- **Naechster Schritt:** moduluebergreifenden Persistenzbedarf und Migrationsgrenzen festlegen.
