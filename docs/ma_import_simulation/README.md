# ma_import_simulation

- **Zweck:** Simulationsergebnisse programmunabhaengig erkennen, zuordnen und vereinheitlichen.
- **Eingaben:** Ergebnisdateien sowie Run-, Varianten- und Raumzuordnungen.
- **Ausgaben:** standardisierte Ergebnisdaten fuer `ma_analyse`.
- **Abgrenzung:** keine fachliche Kennwertberechnung oder Bewertung.
- **Abhaengigkeiten:** `ma_export_simulation`; Phase 4.
- **Status:** teilweise vorhanden; Adapter- und Aufbereitungslogik liegt noch in bestehenden Modulen.
- **Naechster Schritt:** bestehende Importlogik inventarisieren und die IDA-ICE-Adaptergrenze planen.

Historische Bezeichnungen `ma_import_ida` und `import_ida` werden nur als
Uebergangsaliase unterstuetzt.
