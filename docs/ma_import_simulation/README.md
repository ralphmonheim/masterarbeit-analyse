# ma_import_simulation

- **Zweck:** Simulationsergebnisse programmunabhaengig erkennen, zuordnen und vereinheitlichen.
- **Eingaben:** Ergebnisdateien sowie Run-, Varianten-, Setup- und
  Raumzuordnungen.
- **Ausgaben:** standardisierte Ergebnisdaten fuer `ma_analyse`.
- **Abgrenzung:** keine fachliche Kennwertberechnung oder Bewertung.
- **Compliance:** Das Modul verarbeitet automatisch nur exportierte,
  zuordenbare Ergebnisartefakte. Vollstaendige IDA-Projektdateien und
  Bibliotheken sind kein regulaerer Importeingang und bleiben dem
  Compliance-Preflight unter `docs/compliance/ida_ice/` vorbehalten.
- **Abhaengigkeiten:** `ma_export_simulation`; Phase 4.
- **Status:** geplant; Adapter- und Aufbereitungslogik liegt noch in bestehenden Modulen.
- **Zuordnung:** Simulationsergebnisse werden mindestens ueber
  `RUN-ID + VAR-ID` zugeordnet. Es gibt keine `CASE-ID`.
- **Naechster Schritt:** bestehende Importlogik inventarisieren und die
  IDA-ICE-Adaptergrenze planen.

Historische Bezeichnungen `ma_import_ida` und `import_ida` werden nur als
Uebergangsaliase unterstuetzt.
