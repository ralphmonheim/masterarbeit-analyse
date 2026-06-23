# ma_database

- **Zweck:** Spaetere moduluebergreifende Persistenz und Repository-Schnittstellen.
- **Eingaben:** freigegebene fachliche Datenmodelle.
- **Ausgaben:** persistierte Projekt-, Run- und Ergebnisdaten.
- **Abgrenzung:** bestehende SQLAlchemy-/Alembic-Logik in `ma_variants` wird noch nicht verschoben.
- **Abhaengigkeiten:** `ma_core`; Phase 0.
- **Status:** geplant; bestehende Datenbanklogik liegt noch ausserhalb des Zielmoduls.
- **Naechster Schritt:** moduluebergreifenden Persistenzbedarf und Migrationsgrenzen festlegen.
