# ma_simulation_setup

- **Zweck:** Run, Variantenmenge, Zeitraum, Zeitschritt, Ausgabeintervall und
  Szenario festlegen.
- **Eingaben:** vollstaendig erzeugte Varianten aus `ma_variants` nach `VGEN`
  sowie Projekt-, Modell- und Wetterreferenzen.
- **Ausgaben:** validiertes, versioniertes `RunManifest`.
- **Abgrenzung:** keine Variantenbildung, keine Veraenderung fachlicher
  Variantenwerte, keine Dateibearbeitung und kein Simulationsstart.
- **Abhaengigkeiten:** `ma_variants`; Phase 3.
- **Status:** geplant; P018 ist auf die direkte P017-Uebergabe geschaerft.
- **Run-Zuordnung:** Ein Run referenziert genau eine VariantSelection und
  ordnet Ergebnisse direkt ueber `RUN-ID + VAR-ID` zu. Es gibt keine
  `SimulationCase`-Ebene.
- **Naechster Schritt:** RunManifest mit direkter RUN/VAR-Zuordnung planen.
