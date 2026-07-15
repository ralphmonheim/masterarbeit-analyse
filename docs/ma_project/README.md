# ma_project

- **Zweck:** Projektidentitaet, allgemeiner Untersuchungsrahmen,
  Simulationsprogrammliste, neutrales Varianten-Benennungsprofil und spaeter
  eine kontrollierte digitale Projektakte.
- **Eingaben:** Projektangaben und Standardvorlagen.
- **Ausgaben:** lesender `ProjectContext`, aktive Simulationsprogrammreferenz
  und neutrales Benennungsprofil.
- **Abgrenzung:** keine Fachdatenerfassung, keine Simulation, kein
  Quellenregister und kein fachlicher Projektstatus oder Freigabeprozess.
- **Abhaengigkeiten:** `ma_core`; Phase 1.
- **Status:** P011 ist fachlich konsolidiert; P028 stellt eine getestete
  Demo-Fachansicht fuer Simulationsprogramme und neutrales Naming bereit.
  P011-S1a stellt getestete immutable Projektmodelle und reine Serialisierung
  ohne Dateisystemzugriff bereit.
- **Naechster Schritt:** P011-S1b als separaten Pfad- und Persistenzvertrag
  mit Speicherort- und Ignore-Gate abgrenzen; weiterhin keine Assets, UI,
  Wetteruebergabe oder Naming-Pfadmigration.
