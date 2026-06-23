# ma_parameters

- **Zweck:** Eingaben aus Gebaeude, Wetter, Zonen und Technik vereinheitlichen.
- **Eingaben:** validierte Fachmoduldaten und Vorschlagswerte aus der Referenzdimensionierung.
- **Ausgaben:** versionierter `ParameterSnapshot` als einzige fachliche Eingangsquelle fuer `ma_variants`.
- **Abgrenzung:** keine Variantenbildung und keine direkte Simulationsdateibearbeitung.
- **Abhaengigkeiten:** `ma_building`, `ma_weather`, `ma_zones`, `ma_technical`; Phase 2.
- **Status:** geplant; Parameter- und Optionslogik liegt noch in `ma_variants`.
- **Naechster Schritt:** P015 und P028 mit Herkunft, Einheiten, geschuetzter
  Demo-Optionsauswahl, Freigabe und Importvorlagen konkretisieren.
