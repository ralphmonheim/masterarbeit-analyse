# ma_database

- **Zweck:** Spaetere moduluebergreifende Persistenz und Repository-Schnittstellen.
- **Eingaben:** freigegebene fachliche Datenmodelle, spaeter auch
  Gebaeudemodellversionen, Importprotokolle und Katalogversionen aus P012.
- **Ausgaben:** persistierte Projekt-, Modell-, Run- und Ergebnisdaten.
- **Abgrenzung:** bestehende SQLAlchemy-/Alembic-Logik in `ma_variants` wird
  noch nicht verschoben; fachliche Berechnungen bleiben in den Fachmodulen.
- **Abhaengigkeiten:** `ma_core`; Phase 0.
- **Lokaler Katalog:** `src/ma_database/catalog.py` kann einen optionalen,
  hashgeprueften Demo-Katalog aus `config/ma_database/catalogs/` lesen. Dieser
  Pfad ist lokal, Git-ignoriert und nicht Bestandteil oeffentlicher Releases.
  Ein frischer Clone und die manuellen UI-Statusoptionen funktionieren ohne
  diese Daten; Tests erzeugen ausschliesslich neutrale temporaere Fixtures.
- **Status:** teilweise umgesetzt; der optionale lokale Katalog-Loader ist
  vorhanden, die eigentliche moduluebergreifende Persistenz liegt noch
  ausserhalb des Zielmoduls.
- **Naechster Schritt:** moduluebergreifenden Persistenzbedarf,
  Modellversionierung, Importprotokolle und Migrationsgrenzen festlegen.

## Lokales Quellenregister

Die freigegebene Literaturarbeit nutzt einen getrennten lokalen Arbeitsbereich
unter `config/ma_database/literature/`. Er bleibt Git-ignoriert, weil er
interne Pfade, Quellenanalysen und gegebenenfalls lizenz- oder
zugangssensible Arbeitsinformationen enthalten kann.

- `sources_internal.xlsx`: internes Quellenregister mit Verweisen auf
  Originale und Einzelanalysen.
- `sources_public.xlsx`: kuratierte, veröffentlichungsfähige Fassung.
- `analyses/`: eine Markdown-Analyse pro Source-ID.

Die Arbeitsdateien sind kein Laufzeitkatalog und werden nicht durch
`ma_database.catalog` gelesen. Die Struktur und der Arbeitsauftrag sind in
`docs/prompts/MASTER_PROMPT_QUELLENINVENTAR_UND_LERNPAKETE.md` dokumentiert.
