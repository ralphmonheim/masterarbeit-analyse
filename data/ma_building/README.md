# ma_building Arbeitsdaten

Dieser Ordner ist fuer lokale Gebaeude-Testdaten vorbereitet.

- IDA-ICE-IFC-Dateien liegen lokal unter `data/ma_building/input/ifc/`.
- Das Masterarbeits-Referenzmodell fuer `ma_building` ist
  `data/ma_building/input/ifc/SmallOffice_d_IFC2x3.ifc`.
- Weitere IDA-ICE-IFC-Dateien in diesem Ordner dienen nur als Vergleichs- und
  Plausibilisierungs-Samples.
- ChatGPT-/Rhino-3DM-Dateien liegen lokal unter `data/ma_building/input/rhino/`.
- DWG-/CAD-Beispieldateien liegen lokal unter `data/ma_building/input/cad/`.
  Sie werden in v1 nur als ungepruefte CAD-Quellen mit Metadaten behandelt.
- Diagnoseausgaben koennen lokal unter `data/ma_building/diagnostics/` abgelegt werden.

Echte Modell- und Diagnosearbeitsdateien werden nicht versioniert. Versioniert
werden nur diese Struktur, `.gitkeep`-Dateien und die kleine Demo-Spezifikation
unter `config/ma_building/examples/`.
