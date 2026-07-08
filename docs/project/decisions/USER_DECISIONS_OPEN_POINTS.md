# Offene Nutzerentscheidungen

Stand: 2026-07-08

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

### OP-012b LoD-2/LoD-3-Inhalte aus dem Rhino-Testgebaeude

- Thema: ma_building, BusinessIntegration-Testmodell und Level of Detail
- Status: offen
- Frage: Welche weiteren Inhalte aus dem Rhino-Testgebaeude werden nach
  LoD-1 fuer LoD-2 oder LoD-3 manuell oder als strukturierte Demo in die
  `BuildingModelSpecification` uebernommen?
- Ergaenzung: UD-068 legt fest, dass LoD den Umfang der Eingabe beschreibt.
  LoD-1 ist mit Kubatur, einfachen Huellkennwerten, U-Werten,
  Fensterflaechenanteil und Annahmen umgesetzt, ohne produktiven
  Rhino-Import.
- Auswirkung: Bestimmt, ob als naechstes Raeume, orientierte Bauteile,
  Oeffnungsobjekte, Host-Beziehungen, Sonnenschutz und weitere
  bauphysikalische Werte als LoD-2/LoD-3 erfasst werden.

### OP-013 Verbindliche Importformate je Eingabemodul

- Thema: Eingabe- und Datenhaltungsarchitektur
- Status: offen
- Frage: Welche Datei- und Programmvorlagen werden fuer Building, Zones,
  Technical, Parameters und Naming im Masterarbeitsumfang verbindlich
  unterstuetzt?
- Ergaenzung: Fuer `ma_building` ist das Rhino-Testgebaeude durch UD-067 als
  BusinessIntegration-Referenz festgelegt. Die daraus abgeleitete
  BusinessIntegration-LoD-1-YAML ist unterstuetzt, aber `.3dm` ist weiterhin
  kein produktives Eingangsformat. DWG ist durch UD-066 fuer den aktuellen
  Masterarbeitsumfang kein produktiver Importpfad und bleibt nur lokale
  ungepruefte CAD-Quelle. Fuer `ma_zones` und `ma_technical` sind
  BusinessIntegration-LoD-1-YAML-Demos durch UD-069 unterstuetzt. Der
  P013-S2-Gesamtplan fuer `ma_zones` ist durch UD-072 fachlich konsolidiert,
  ersetzt aber noch keine produktiven Importprofile. Der
  BusinessIntegration-LoD-1-`ParameterSnapshot` v1 ist durch UD-070
  unterstuetzt; produktive Importprofile, Systemvorlagen,
  Snapshot-Speicherung und Wetteruebernahme bleiben offen. P016-S1 nutzt den
  Snapshot v1 fuer eine LoD-1-Referenzdimensionierung; Stage-1-Folgesnapshots
  und normative Verfahren bleiben offen.
- Auswirkung: Wird in P010 als Formatmatrix vorbereitet und vor den jeweiligen
  Fachimplementierungen entschieden.

### OP-014 ma_zones Folgeentscheidungen aus P013-S2

- Thema: ma_zones, P013-S3 bis P013-S7
- Status: offen
- Frage: Wie werden die in P013-S2 markierten offenen Fachpunkte entschieden:
  Sonderhohlraeume, gleichzeitiger Heiz- und Kuehlbetrieb, Bedeutung des
  Prozentwerts bei Uebergabesystemen, LoD-1-Variantenparameter und konkrete
  DIN-Datenabbildung?
- Ergaenzung: P013-S2 legt die Grundstruktur fest, darf diese offenen Punkte
  aber nicht stillschweigend in Berechnungs- oder UI-Logik uebersetzen.
- Auswirkung: Betrifft `ma_zones`, `ma_technical`, `ma_parameters`,
  `ma_variants`, `ma_validation`, die UI-Reiter und die spaetere
  Normprofil-/Zeitprofilabbildung.
