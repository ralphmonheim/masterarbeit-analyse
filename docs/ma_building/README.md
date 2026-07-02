# ma_building

- **Zweck:** Programmneutrales Gebaeudemodell mit Gebaeude, Geschossen,
  geometrischen Raeumen, Bauteilen, Flaechen, Oeffnungen, einfachen
  Sonnenschutzinformationen und bauphysikalischen Randbedingungen verwalten.
- **Eingaben:** versionierte Demo-`BuildingModelSpecification` unter
  `config/ma_building/examples/demo_building_spec.yaml` und lokale
  IFC-/3DM-Arbeitsdateien unter `data/ma_building/input/`.
- **Referenzmodell Masterarbeit:** Fuer fachliche Aussagen und weitere
  `ma_building`-Tests ist das lokale IDA-ICE-Sample
  `data/ma_building/input/ifc/SmallOffice_d_IFC2x3.ifc` massgeblich. Andere
  IFC-Samples bleiben Vergleichsdaten.
- **CAD-Beispieldateien:** DWG-Dateien liegen lokal unter
  `data/ma_building/input/cad/` und werden in v1 nicht fachlich interpretiert.
  Ohne externen DWG-Parser gelten sie als ungepruefte CAD-Quellen, nicht als
  Masterarbeitsreferenz. UD-066 schliesst einen produktiven DWG-Parser fuer
  den aktuellen Masterarbeitsumfang aus.
- **Ausgaben:** validierbare Demo-Gebaeudedaten, strukturierte
  Quelldiagnosen mit `InputSource`, IFC-Entity-Zaehlern und
  `ma_validation`-Meldungen; spaeter freigegebene Gebaeudedaten fuer
  `ma_parameters`, Raumregister fuer `ma_zones` und Mengeninformationen fuer
  Bewertung und Simulationsadapter.
- **Abgrenzung:** Nutzungsprofile und thermische Zonen liegen in `ma_zones`;
  technische Anlagen und Regelung in `ma_technical`; technische Datenhaltung
  in `ma_database`; IDA-ICE-Uebergabe in `ma_export_simulation`.
- **Abhaengigkeiten:** `ma_project`, P010/P027-Diagnose- und
  Freigabevertraege; Phase 2.
- **Status:** teilweise umgesetzt. v1 umfasst Demo-Spec, Fachmodelle,
  Validierung und lokale IFC-/3DM-Diagnose ohne produktiven Geometrieimport.
- **Naechster Schritt:** reale IFC-Inhalte auswerten und separat entscheiden,
  ob ein IFC-Lite-Import fachlich noetig und im Masterarbeitsumfang tragbar
  ist. Rhino bleibt ein Ausbaupfad ohne aktive Parser-Abhaengigkeit.
