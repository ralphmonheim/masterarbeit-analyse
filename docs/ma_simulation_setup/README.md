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
- **Status:** teilweise umgesetzt. P018 materialisiert neutrale Run-Manifeste,
  ein getrenntes `simulation_setup.yaml`, Variantenkonfigurationen,
  Simulationseingaben und Vorbereitungsberichte. Der SmallOffice-V1-Nachweis
  erzeugt 30 Optimierungs- und acht Sensitivitaetspakete.
- **Run-Zuordnung:** Ein Run referenziert genau eine VariantSelection und
  ordnet Ergebnisse direkt ueber `RUN-ID + VAR-ID` zu. Es gibt keine
  `SimulationCase`-Ebene.
- **Forschungsgrenze:** P018 schreibt technische Logs. Prozesszeitmessung,
  manuelle Zeiten und Vergleichsauswertung liegen getrennt in P030
  `research_tools`.
- **Naechster Schritt:** Die 38 Draft-Pakete manuell gegen die spaetere
  Simulationsuebergabe pruefen. IDA-Dateierzeugung, Simulationsstart und
  Ergebnisimport bleiben ausserhalb von P018.
