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
  ohne Dateisystemzugriff bereit. P035 fuehrt die technische Persistenz in
  der separaten Arbeitsablage.
- **Projektablage:** Aktive Projektordner und die lokale Registry liegen unter
  `../260524_Masterarbeit_Arbeitsablage/04_Teil2_Prozessinnovation/Projekt_Workspaces/`.
  `config/ma_project/examples/` enthaelt nur versionierte Seed-Vorlagen.
- **Naechster Schritt:** Den externen Projektstart und die Bearbeitungsansicht
  im manuellen V1-Smoke-Test pruefen.
