# ma_parameters

- **Zweck:** Eingaben aus Gebaeude, Wetter, Zonen und Technik vereinheitlichen.
- **Eingaben:** validierte Fachmoduldaten und Vorschlagswerte aus der
  Referenzdimensionierung. Gebaeudedaten aus `ma_building` werden nur als
  freigegebene und versionierte `BuildingModelSpecification` beziehungsweise
  Gebaeudemodellversion uebernommen.
- **Ausgaben:** versionierter `ParameterSnapshot` als einzige fachliche Eingangsquelle fuer `ma_variants`.
- **Abgrenzung:** keine Variantenbildung und keine direkte Simulationsdateibearbeitung.
- **Abhaengigkeiten:** `ma_building`, `ma_weather`, `ma_zones`, `ma_technical`; Phase 2.
- **Status:** teilweise umgesetzt. P028 stellt eine getestete Demo-Fachansicht
  und geschuetzte Optionsauswahl bereit; P015-S1 stellt einen validierten
  `ParameterSnapshot` v1 fuer die BusinessIntegration-LoD-1-Kette bereit.
- **BusinessIntegration-LoD-1:** Der Snapshot sammelt Parameterwerte aus
  `ma_building`, `ma_zones` und `ma_technical` mit Quellenreferenz, Einheit,
  Version und Freigabestatus.
- **Naechster Schritt:** Stage-1-Ergebnisse als Folgesnapshot oder Vorschlag
  modellieren und Variantenanbindung auf `ParameterSnapshot` v1 vorbereiten.
