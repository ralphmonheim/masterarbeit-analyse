# Offene Nutzerentscheidungen

Stand: 2026-07-02

Diese Datei enthaelt nur offene Nutzerentscheidungen. Erledigte Entscheidungen
werden nach der Dokumentation als `UD-*` aus dieser Datei entfernt und stehen in
`USER_DECISIONS_MASTERTHESIS_CODE.md`.

## Offene Punkte

### OP-008 ma_analyse-weite Normierungsstrategie

- Thema: ma_analyse Auswertungen und Diagramme
- Status: offen
- Frage: Welche Auswertungen sollen absolute Werte, flaechenbezogene Werte oder beides anbieten, und welche Bezugsflaeche soll dafuer verwendet werden?
- Auswirkung: Betrifft spaeter `src/ma_analyse/analysis/`, Plot-Templates, Tkinter, Streamlit-Analyse und die Dokumentation der Diagrammeinheiten.

### OP-009 Methodik fuer Zeit- und Personalkostenvergleich

- Thema: Prozessaufwand und Automatisierungsnutzen
- Status: offen
- Frage: Welche Wissensprofile, Stundensaetze, Prozessgrenzen und Messmethoden sollen fuer den Vergleich zwischen manuellem, softwareunterstuetztem und automatisiertem Ablauf verwendet werden?
- Auswirkung: Beeinflusst die wissenschaftliche Vergleichbarkeit, die Prozesskostenrechnung sowie spaetere Ergebnisse in `ma_economy` und `ma_assessment`.

### OP-012 Umfang eines IFC-Lite-Imports

- Thema: ma_building und externe Gebaeudemodelle
- Status: offen
- Frage: Welche Inhalte sind in den konkreten IFC-Arbeitsstaenden belastbar
  vorhanden und koennen ohne umfangreiche Geometrieinterpretation sicher
  uebernommen werden?
- Ergaenzung: Die aktuelle lokale IFC-Arbeitsdatei soll fuer P012 zunaechst
  als Trainings- und Diagnosebasis dienen. Zu klaeren ist, welche
  Metadaten, Entitaeten, Raeume, Bauteile, Oeffnungen und IDs daraus sicher
  auslesbar sind.
- Auswirkung: Entscheidet, ob P012 nur Demo-/YAML-Daten oder zusaetzlich einen
  begrenzten IFC-Lite-Adapter umsetzt.

### OP-013 Verbindliche Importformate je Eingabemodul

- Thema: Eingabe- und Datenhaltungsarchitektur
- Status: offen
- Frage: Welche Datei- und Programmvorlagen werden fuer Building, Zones,
  Technical, Parameters und Naming im Masterarbeitsumfang verbindlich
  unterstuetzt?
- Ergaenzung: Fuer `ma_building` ist `.3dm` fachlich als spaeterer
  Ausbaupfad dokumentiert, aber wegen der bestehenden CAD-Grenze noch kein
  verbindliches Eingangsformat. DWG ist durch UD-066 fuer den aktuellen
  Masterarbeitsumfang kein produktiver Importpfad und bleibt nur lokale
  ungepruefte CAD-Quelle.
- Auswirkung: Wird in P010 als Formatmatrix vorbereitet und vor den jeweiligen
  Fachimplementierungen entschieden.
