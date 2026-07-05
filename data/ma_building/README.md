# ma_building Arbeitsdaten

Dieser Ordner ist fuer lokale Gebaeude-Testdaten vorbereitet.

- IDA-ICE-IFC-Dateien liegen lokal unter `data/ma_building/input/ifc/`.
- Das Referenzmodell fuer den fachlichen Teil ist
  `data/ma_building/input/ifc/SmallOffice_d_IFC2x3.ifc`.
- Weitere IDA-ICE-IFC-Dateien in diesem Ordner dienen nur als Vergleichs- und
  Plausibilisierungs-Samples.
- ChatGPT-/Rhino-3DM-Dateien liegen lokal unter `data/ma_building/input/rhino/`.
- Das BusinessIntegration-Testgebaeude fuer die Softwareentwicklung ist
  `data/ma_building/input/rhino/ma_building_testgebaeude_6x4x4_oeffnungen_v1.3dm`.
  Verbindlich fuer `ma_building` bleibt daraus eine kleine strukturierte
  `BuildingModelSpecification`, nicht die Rhino-Datei selbst.
- Die versionierte LoD-1-Ableitung aus dem Rhino-Testgebaeude liegt unter
  `config/ma_building/examples/business_integration_lod1_building_spec.yaml`.
  Sie enthaelt Kubatur, einfache Huellkennwerte, U-Werte, Fensteranteil und
  Annahmen fuer erste Dimensionierungsideen.
- DWG-/CAD-Beispieldateien liegen lokal unter `data/ma_building/input/cad/`.
  Sie werden in v1 nur als ungepruefte CAD-Quellen mit Metadaten behandelt.
- Diagnoseausgaben koennen lokal unter `data/ma_building/diagnostics/` abgelegt werden.

Echte Modell- und Diagnosearbeitsdateien werden nicht versioniert. Versioniert
werden nur diese Struktur, `.gitkeep`-Dateien und die kleine Demo-Spezifikation
unter `config/ma_building/examples/`.
