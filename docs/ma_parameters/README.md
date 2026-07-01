# ma_parameters

- **Zweck:** Eingaben aus Gebaeude, Wetter, Zonen und Technik vereinheitlichen.
- **Eingaben:** validierte Fachmoduldaten und Vorschlagswerte aus der
  Referenzdimensionierung. Gebaeudedaten aus `ma_building` werden nur als
  freigegebene und versionierte `BuildingModelSpecification` beziehungsweise
  Gebaeudemodellversion uebernommen.
- **Ausgaben:** versionierter `ParameterSnapshot` als einzige fachliche Eingangsquelle fuer `ma_variants`.
- **Abgrenzung:** keine Variantenbildung und keine direkte Simulationsdateibearbeitung.
- **Abhaengigkeiten:** `ma_building`, `ma_weather`, `ma_zones`, `ma_technical`; Phase 2.
- **Status:** geplant; P028 stellt eine getestete Demo-Fachansicht und
  geschuetzte Optionsauswahl bereit. Die Kataloglogik wird kompatibel aus
  `ma_variants` wiederverwendet.
- **Naechster Schritt:** P015 um Herkunft, Versionierung, Freigabe,
  Gebaeudeparameter aus P012 und den produktiven `ParameterSnapshot`
  erweitern.
