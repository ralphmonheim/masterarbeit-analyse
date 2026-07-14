# ma_simulation_setup

- **Zweck:** neutrales Run-Paket mit Variantenmenge, Zeitraum, Zeitschritt,
  Ausgabeanforderungen und Modellreferenzen erzeugen.
- **Eingaben:** vollstaendig erzeugte Varianten aus `ma_variants` nach `VGEN`
  sowie Projekt-, Modell- und Wetterreferenzen.
- **Ausgaben:** versioniertes `RunManifest`, getrennte
  `simulation_setup.yaml`, Variantenkonfigurationen, neutrale
  Simulationseingaben, PreparationReport und technische Logs.
- **Abgrenzung:** keine Variantenbildung, keine Veraenderung fachlicher
  Variantenwerte, keine IDA-Dateibearbeitung, kein Simulationsstart und kein
  Ergebnisimport.
- **Abhaengigkeiten:** `ma_variants`; Phase 3.
- **Status:** geplant; P018 ist als neutrales Run-Paket mit direkter
  P017-Uebergabe fachlich konsolidiert.
- **Run-Zuordnung:** Ein Run referenziert genau eine VariantSelection und
  ordnet Ergebnisse direkt ueber `RUN-ID + VAR-ID` zu. Es gibt keine
  `SimulationCase`-Ebene.
- **Forschungsgrenze:** P018 schreibt technische Logs. Prozesszeitmessung,
  manuelle Zeiten und Vergleichsauswertung liegen getrennt in P030
  `research_tools`.
- **Naechster Schritt:** P018-S1 mit Grundmodellen, Status und YAML-Schemas.
