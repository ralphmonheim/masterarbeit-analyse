# ma_parameters

- **Zweck:** Freigegebene Eingaben aus Wetter, Gebaeude, Technik und Zonen
  vereinheitlichen.
- **Eingaben:** validierte Fachmoduldaten und Vorschlagswerte aus der
  Referenzdimensionierung. Gebaeudedaten aus `ma_building` werden nur als
  freigegebene und versionierte `BuildingModelSpecification` beziehungsweise
  Gebaeudemodellversion uebernommen.
- **Ausgaben:** versionierter `BaselineParameterSnapshot`,
  `ReferenceDimensioningResult`-Bezug und
  `ParameterVariationSpecification` als fachliche Eingangsquelle fuer
  `ma_variants`.
- **Abgrenzung:** keine Variantenbildung und keine direkte Simulationsdateibearbeitung.
- **Abhaengigkeiten:** `ma_weather`, `ma_building`, `ma_technical`, `ma_zones`; Phase 2.
- **Status:** teilweise umgesetzt und fachlich konsolidiert. P028 stellt eine
  getestete Demo-Fachansicht und geschuetzte Optionsauswahl bereit; P015-S1
  stellt einen validierten `ParameterSnapshot` v1 fuer die
  BusinessIntegration-LoD-1-Kette bereit. P015-S2 erzeugt daraus einen ersten
  `BaselineParameterSnapshot` v2 mit `parameter_value_id`, Scopes,
  Parameterklassen, Variierbarkeit, Quellenreferenzen und Validierung.
  P015-S3a fuehrt ein `ParameterInputPackage` als Eingangspaket-Checkpoint
  ein und uebernimmt Wetter nur als aktivierten, freigegebenen
  Projekt-Default aus `ma_weather`. P015-S3b-prep kann einen
  `ReleasedTechnicalHandover` als echte technische
  `ParameterSourceReference` mit Revisions-ID und Content-Hash abbilden.
  P013-S3c/P015-S3b-T2 fuehrt zusaetzlich getrennte
  `checkpoint_references` fuer das zusammengehoerige P013-/P014-Paar ein.
  Sie sind keine Wertquellen, werden auf Freigabe/Aktualitaet geprueft und
  werden bei Nutzung im bestehenden Baseline-Content-Hash gebunden.
- **P032-W2a-Katalogownership:** Die reinen Python-Katalogvertraege liegen
  unter `ma_parameters.catalogs`. Bestehende `ma_variants`-Importpfade sind
  identitaetsgleiche Kompatibilitaets-Reexports. Die Demo-Defaultpfade unter
  `config/ma_variants/` sowie der lokale Reportpfad bleiben bewusst
  Legacy-Pfade; W2a hat keine Konfigurationen oder Daten bewegt.
- **BusinessIntegration-LoD-1:** Der Snapshot sammelt Parameterwerte aus
  `ma_building`, `ma_zones` und `ma_technical` mit Quellenreferenz, Einheit,
  Version und Freigabestatus. Der Baseline-v2-Stand leitet daraus stabile
  Werte mit Scope-Typen `building`, `zone_group`, `zone` und
  `technical_system` ab.
- **P013-S2-Folge:** Der Zielworkflow lautet `ma_weather -> ma_building ->
  ma_technical -> ma_zones -> ma_validation -> ma_parameters`. Ein
  veraenderter Zonenstand soll spaeter den Parameterstand als `outdated`
  markieren und die Variantengenerierung bis zur Aktualisierung blockieren.
- **P017-Uebergabe:** `ma_parameters` erzeugt den Variationsraum nicht selbst,
  sondern liefert eine freigegebene `ParameterVariationSpecification` mit
  Scope, Zielobjekten, Werteformen, Dimensionierungsrelevanz und
  Referenzstrategien.
- **Naechster Schritt:** Die v2-basierte Herkunft bestehender Parameterwerte
  und der verbleibende Vollumfang von P015-S3b bleiben getrennte Slices.
  Der abgeschlossene P013-/P014-Checkpoint aendert keine v1-Parameterwerte,
  keine Wertquellen-IDs und keine Persistenz.
