# ma_zones

- **Zweck:** Zonen, Nutzungen, Profile, Konditionierung, interne Lasten,
  Zeitprofile und zonenbezogene Uebergabesysteme verwalten.
- **Eingaben:** freigegebene Raumreferenzen aus `ma_building`, zentrale
  technische Systemreferenzen aus `ma_technical` und Nutzungsanforderungen.
- **Ausgaben:** validierte Zonendaten fuer `ma_parameters` sowie
  zonenbezogene Betriebs-, Konditionierungs- und Uebergabezuordnungen.
- **Abgrenzung:** keine Gebaeudegeometrie, keine zentralen Erzeugungsanlagen
  und keine automatische Zonenbildung im MVP.
- **Abhaengigkeiten:** `ma_building`, `ma_technical`; Phase 2.
- **Status:** teilweise umgesetzt. P013-S1 stellt eine LoD-1-Demo fuer das
  BusinessIntegration-Testgebaeude bereit:
  `config/ma_zones/examples/business_integration_lod1_zone_spec.yaml`.
- **Planstand:** P013-S2 ist fachlich konsolidiert. Der Zielworkflow lautet
  `ma_weather -> ma_building -> ma_technical -> ma_zones -> ma_validation ->
  ma_parameters`.
- **LoD-1-Inhalt:** eine Gesamtgebaeudezone, ein einfaches Buero-Nutzungsprofil,
  Sollwerte, interne Lasten, Betriebszeiten und Mindestluftwechsel.
- **Validierung:** Pflichtfelder, eindeutige IDs, Profilreferenzen,
  Flaeche/Volumen, Sollwerte, Betriebszeiten und Gebaeudebezug werden geprueft.
  Fehler blockieren; Warnungen benoetigen eine bewusste Freigabeentscheidung.
- **Streamlit:** Die Modulansicht zeigt Demo, Nutzungsprofil, Freigabestatus
  und Annahmen.
- **Naechster Schritt:** P013-S3 Raum-Zonen-Grundmodell vorbereiten:
  eindeutige Raum-Zonen-Zuordnung, vollstaendige Raumabdeckung und
  Blockierung nicht zugeordneter Raeume.
