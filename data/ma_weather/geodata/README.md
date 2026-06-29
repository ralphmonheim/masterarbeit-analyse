# Lokale Geodaten fuer ma_weather

Dieser Ordner ist fuer lokale Gemeinde- und PLZ-Geodaten vorgesehen.

Die eigentlichen GeoJSON-Dateien werden nicht versioniert. Versioniert werden
nur Quellen-, Feld- und Lizenzmetadaten unter `config/ma_weather/geodata/`.

Geplante Unterordner:

- `_incoming/bkg_vg250_2025_01_01/` fuer den entpackten BKG-VG250-Download
- `germany/` fuer die daraus abgeleiteten Deutschland-Geodaten
- `germany/source_docs/` fuer lokal abgelegte BKG-Begleitdokumente
- `germany/germany_municipalities.geojson` fuer den aus `VG250_GEM`
  exportierten Gemeinde-Grenzdatensatz
- `postal_codes/` fuer optionale PLZ-Gebiete

Vor der Nutzung muessen Quelle, Lizenz, Version, CRS und Feldnamen in der
Geodaten-Konfiguration dokumentiert werden.

Die empfohlene Minimalstrecke ist:

1. BKG-VG250-Download nach `_incoming/bkg_vg250_2025_01_01/` entpacken.
2. Layer `v_vg250_gem` in QGIS oeffnen.
3. Landflaechen filtern: `GF = 4`.
4. Als GeoJSON nach `germany/germany_municipalities.geojson` exportieren.
5. `config/ma_weather/geodata/example_weather_geodata_sources.yaml`
   pruefen und `enabled: true` setzen.

QGIS kann bei Bedarf ueber https://www.qgis.org/download/ bezogen werden. QGIS
ist nur ein lokales Werkzeug zur Datenerzeugung und keine Laufzeitabhaengigkeit
des Projekts.
