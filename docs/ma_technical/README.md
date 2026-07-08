# ma_technical

- **Zweck:** Erzeugung, Verteilung, Uebergabe, Regelung und technische Komponenten beschreiben.
- **Eingaben:** Zonenanforderungen, Systemvorlagen und Produktdaten.
- **Ausgaben:** validierte Technikdaten fuer `ma_parameters`.
- **Abgrenzung:** keine Variantenbildung und keine Simulationsergebnisanalyse.
- **Abhaengigkeiten:** `ma_zones`; Phase 2.
- **Status:** teilweise umgesetzt. P014-S1 stellt eine LoD-1/Lite-Demo fuer das
  BusinessIntegration-Testgebaeude bereit:
  `config/ma_technical/examples/business_integration_lod1_technical_spec.yaml`.
- **LoD-1-Inhalt:** einfache Referenzannahmen fuer Heizung, Kuehlung und
  Lueftung mit bedienten Zonen, spezifischen Leistungen, Temperaturen,
  Leistungszahlen, Luftwechsel und Regelstrategie.
- **Validierung:** Pflichtfelder, eindeutige IDs, Systemtypen, bediente Zonen,
  positive Leistungs-/Luftwechselwerte und Zonenmodellbezug werden geprueft.
  Fehler blockieren; Warnungen benoetigen eine bewusste Freigabeentscheidung.
- **Streamlit:** Die Modulansicht zeigt Demo-Systeme, Freigabestatus und
  Annahmen.
- **Naechster Schritt:** Referenzsysteme fuer LoD-2 und spaetere
  Dimensionierung genauer abgrenzen.
