# ma_import_simulation

- **Zweck:** Simulationsergebnisse programmunabhaengig erkennen, zuordnen und vereinheitlichen.
- **Eingaben:** Ergebnisdateien sowie Run-, Varianten-, Setup- und
  Raumzuordnungen.
- **Ausgaben:** standardisierte Ergebnisdaten fuer `ma_analyse`.
- **Abgrenzung:** keine fachliche Kennwertberechnung oder Bewertung.
- **Compliance:** Das Modul verarbeitet automatisch nur exportierte,
  zuordenbare Ergebnisartefakte. Vollstaendige IDA-Projektdateien und
  Bibliotheken sind kein regulaerer Importeingang; ihre Repository-Weitergabe
  wird bei `update repo` geprueft.
- **Abhaengigkeiten:** `ma_export_simulation`; Phase 4.
- **Status:** Der erste IDA-ICE-Ergebnisadapter erkennt PRN, HTML und XLSX
  positiv, fuehrt Provenienz und Hash und verarbeitet manifestgebundene
  Pakete. IDM/IDC werden diagnostiziert, aber nicht inhaltlich gelesen.
- **Zuordnung:** Simulationsergebnisse werden mindestens ueber
  `RUN-ID + VAR-ID` zugeordnet. Es gibt keine `CASE-ID`.
- **Naechster Schritt:** Weitere Simulationsprogramme erhalten eigene Adapter,
  ohne den neutralen Ergebnisvertrag oder `ma_data_preparation` zu umgehen.

Historische Bezeichnungen `ma_import_ida` und `import_ida` werden nur als
Uebergangsaliase unterstuetzt.
