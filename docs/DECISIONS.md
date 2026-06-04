# Entscheidungen

Stand: 2026-06-02

Dieses Dokument sammelt Architekturentscheidungen fuer die Projektvorbereitung.

## Entscheidung 1: Modularer Aufbau

Das Projekt wird modular weiterentwickelt. Der bestehende Analysecode bleibt als eigenes Analyse-Subsystem erhalten. Neue Funktionen fuer Parameterkatalog, Optionskatalog, Variantenmanagement, Auswahl, Naming, IDA-Export, Wirtschaftlichkeit und Reporting werden schrittweise getrennt vorbereitet.

Begruendung:

- Die vorhandene Analysepipeline ist bereits nutzbar und soll nicht durch einen grossen Umbau gefaehrdet werden.
- Neue fachliche Bereiche koennen einzeln getestet und dokumentiert werden.
- Spaetere Erweiterungen wie Produktkatalog, Materialkatalog und Weboberflaeche erhalten klare Grenzen.

## Entscheidung 2: PostgreSQL als spaetere zentrale Datenbank

PostgreSQL wird als spaetere zentrale Zieldatenbank vorgesehen. In diesem Vorbereitungsschritt wird noch keine Datenbanklogik implementiert.

Begruendung:

- Varianten, Parameter, Optionswerte, Systemvorlagen, Importlogs und spaetere Bewertungsergebnisse brauchen stabile Relationen.
- PostgreSQL ist robust fuer strukturierte Projektdaten und spaetere Auswertungen.
- SQLAlchemy und Alembic koennen spaeter fuer Modelle und Migrationen eingesetzt werden.

## Entscheidung 3: Bestehende Analysefunktionen bleiben unveraendert

Die vorhandenen Module unter `src/ma_analyse` werden in diesem Schritt nicht umgebaut, verschoben oder geloescht.

Begruendung:

- Sie bilden den aktuellen funktionsfaehigen Kern fuer Simulationsergebnis-Auswertung.
- Der neue Variantenkern soll zunaechst als Erweiterung daneben entstehen.
- Eine spaetere Anbindung erfolgt bewusst ueber Adapter oder klar definierte Schnittstellen.

## Entscheidung 4: Dokumentation vor Fachlogik

Vor der Implementierung neuer Varianten-, Datenbank- oder Exportlogik wird zuerst die Projektstruktur dokumentiert.

Begruendung:

- Die fachlichen Grenzen werden klarer.
- Der Umsetzungsumfang von Version 1 bleibt kontrollierbar.
- Spaetere Codeaenderungen lassen sich gegen Plan, Workflow und Datenmodell pruefen.
