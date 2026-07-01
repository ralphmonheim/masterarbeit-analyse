# ma_zones

- **Zweck:** Thermische Zonen, Nutzungen, Sollwerte, interne Lasten und Profile verwalten.
- **Eingaben:** freigegebene Raumreferenzen aus dem baulichen Raumregister von
  `ma_building`, optionale `ImportedZoneHint`-Vorschlaege und
  Nutzungsanforderungen.
- **Ausgaben:** validierte Zonendaten fuer `ma_parameters` und Anforderungen an `ma_technical`.
- **Abgrenzung:** keine Gebaeudegeometrie und keine Anlagenberechnung.
- **Abhaengigkeiten:** `ma_building`; Phase 2.
- **Status:** geplant.
- **Naechster Schritt:** P013 mit Demo, Importvorlage,
  Raum-Zonen-Zuordnung und klarer Trennung zwischen importierten Vorschlaegen
  und bestaetigten thermischen Zonen umsetzen.
