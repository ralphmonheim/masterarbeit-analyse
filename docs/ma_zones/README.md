# ma_zones

- **Zweck:** Thermische Zonen, Nutzungen, Sollwerte, interne Lasten und Profile verwalten.
- **Eingaben:** freigegebene Raumreferenzen aus dem baulichen Raumregister von
  `ma_building`, optionale `ImportedZoneHint`-Vorschlaege und
  Nutzungsanforderungen.
- **Ausgaben:** validierte Zonendaten fuer `ma_parameters` und Anforderungen an `ma_technical`.
- **Abgrenzung:** keine Gebaeudegeometrie und keine Anlagenberechnung.
- **Abhaengigkeiten:** `ma_building`; Phase 2.
- **Status:** teilweise umgesetzt. P013-S1 stellt eine LoD-1-Demo fuer das
  BusinessIntegration-Testgebaeude bereit:
  `config/ma_zones/examples/business_integration_lod1_zone_spec.yaml`.
- **LoD-1-Inhalt:** eine Gesamtgebaeudezone, ein einfaches Buero-Nutzungsprofil,
  Sollwerte, interne Lasten, Betriebszeiten und Mindestluftwechsel.
- **Validierung:** Pflichtfelder, eindeutige IDs, Profilreferenzen,
  Flaeche/Volumen, Sollwerte, Betriebszeiten und Gebaeudebezug werden geprueft.
  Fehler blockieren; Warnungen benoetigen eine bewusste Freigabeentscheidung.
- **Streamlit:** Die Modulansicht zeigt Demo, Nutzungsprofil, Freigabestatus
  und Annahmen.
- **Naechster Schritt:** LoD-2-Raum-Zonen-Zuordnung und belastbare
  Nutzungsprofilbibliothek planen.
