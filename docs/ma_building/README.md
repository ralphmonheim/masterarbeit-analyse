# ma_building

- **Zweck:** Programmneutrales Gebaeudemodell mit Gebaeude, Geschossen,
  geometrischen Raeumen, Bauteilen, Flaechen, Oeffnungen, einfachen
  Sonnenschutzinformationen und bauphysikalischen Randbedingungen verwalten.
- **Eingaben:** versionierte Demo-`BuildingModelSpecification` unter
  `config/ma_building/examples/demo_building_spec.yaml`, die
  BusinessIntegration-LoD-1-Spec unter
  `config/ma_building/examples/business_integration_lod1_building_spec.yaml`
  und lokale IFC-/3DM-Arbeitsdateien unter `data/ma_building/input/`.
- **Referenzmodell fachlicher Teil:** Fuer fachliche Aussagen im
  Masterarbeitsteil zu IDA ICE ist das lokale IDA-ICE-Sample
  `data/ma_building/input/ifc/SmallOffice_d_IFC2x3.ifc` massgeblich. Andere
  IFC-Samples bleiben Vergleichsdaten.
- **Referenzmodell BusinessIntegration:** Fuer den Software- und
  BusinessIntegration-Teil wird das lokal erzeugte Rhino-Testgebaeude
  `data/ma_building/input/rhino/ma_building_testgebaeude_6x4x4_oeffnungen_v1.3dm`
  verwendet. Verbindliche Eingabe fuer `ma_building` bleibt eine kleine daraus
  abgeleitete `BuildingModelSpecification`; ein produktiver Rhino-Import ist
  damit nicht freigegeben.
- **LoD-Start:** LoD beschreibt den Umfang der Eingabe. LoD-1 ist umgesetzt:
  Kubatur, einfache Huellkennwerte, U-Werte, Fensterflaechenanteil und
  Annahmen reichen fuer erste Dimensionierungsideen und einfache Analysen.
  Raeume, Einzelfenster und Host-Beziehungen folgen erst in LoD-2/LoD-3.
- **CAD-Beispieldateien:** DWG-Dateien liegen lokal unter
  `data/ma_building/input/cad/` und werden in v1 nicht fachlich interpretiert.
  Ohne externen DWG-Parser gelten sie als ungepruefte CAD-Quellen, nicht als
  Fachteil- oder BusinessIntegration-Referenz. UD-066 schliesst einen
  produktiven DWG-Parser fuer den aktuellen Masterarbeitsumfang aus.
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
- **Status:** teilweise umgesetzt. v1 umfasst Demo-Spec, BusinessIntegration-
  LoD-1-Spec, Fachmodelle, Validierung, lokale IFC-/3DM-Diagnose und eine
  Streamlit-Ansicht fuer vorhandene Bauteile, Oeffnungen sowie die read-only
  lokale Konstruktions- und Materialauswahl. Die Katalogdaten selbst bleiben
  unveroeffentlicht und sind fuer die Ansicht optional.
- **UI-Grenze:** Einzelbauteile werden nur angezeigt, wenn sie in der
  `BuildingModelSpecification` enthalten sind. Die aktuelle IFC-Diagnose
  zaehlt Entity-Typen, liest aber noch keine einzelnen IFC-Bauteile oder
  Attribute aus; eine solche Anzeige bleibt IFC-Lite-Folgearbeit.
- **Naechster Schritt:** LoD-2-Inhalte fuer Raum-/Bauteilstruktur klaeren und
  reale IFC-Inhalte separat auswerten, bevor ein IFC-Lite-Import freigegeben
  wird. Rhino bleibt ohne aktive Parser-Abhaengigkeit.
