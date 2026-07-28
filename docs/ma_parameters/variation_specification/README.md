# ma_parameters.variation_specification

- **Zweck:** Nach der manuellen Referenzdimensionierung die projektbezogenen
  Regeln, Freigaben und Wertespannen als aktuelle
  `ParameterVariationSpecification` festlegen.
- **Eingaben:** Parameter-Referenzstand, wirksame Projekt-, StudyDirection-
  und StudyCase-Regeln sowie die gespeicherte Referenzdimensionierung.
- **Ausgaben:** Gepruefte projektbezogene Variationsspezifikation fuer
  `ma_variants`.
- **Abgrenzung:** keine Kandidatenerzeugung, keine Variantenauswahl und keine
  Variantenpakete.
- **Abhaengigkeiten:** `ma_parameters` und
  `ma_analyse.stage_1_dimensioning`.
- **Status:** V1-Bearbeitungsansicht und projektbezogene Speicherung sind
  umgesetzt. Aenderungen markieren bestehende Kandidaten und Pakete als
  aktualisierungsbeduerftig, ohne sie zu loeschen.
- **Naechster Schritt:** Die aktuelle Spezifikation in `ma_variants` als
  verbindliche Quelle fuer Kandidatenkombinationen verwenden.
