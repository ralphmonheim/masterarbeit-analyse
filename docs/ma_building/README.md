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
- **Katalog-V1:** Die Excel-Arbeitsmappen bleiben unveraenderte lokale
  Inhaltsquellen. Ein gemeinsames Register vereinheitlicht Bauteile,
  Materialien und Produkte fuer die Auswahl und verhindert ID-Kollisionen.
  Eigene Eingaben werden projektlokal als `user_unverified`-Entwuerfe mit
  Herkunft, Zeitstempel und optionaler Quellen-URL gespeichert; sie ersetzen
  keine Quellwerte und sind nicht simulationsfreigegeben.
- **SmallOffice V1:** Die versionierte Endvariante 02 uebernimmt 29 Raeume,
  516,842 m2 und 1677,64455 m3 aus der lokalen Arbeitsmappe. Die Lobbyhoehe
  von 8,0 m ist als zweigeschossiger, etwas ueber das zweite Obergeschoss
  hinausreichender Raum fachlich bestaetigt. Unbekannte Innengeometrie wird
  nicht erfunden; Huellflaechen bleiben nachvollziehbar aggregiert.
- **UI-Grenze:** Einzelbauteile werden nur angezeigt, wenn sie in der
  `BuildingModelSpecification` enthalten sind. Die aktuelle IFC-Diagnose
  zaehlt Entity-Typen, liest aber noch keine einzelnen IFC-Bauteile oder
  Attribute aus; eine solche Anzeige bleibt IFC-Lite-Folgearbeit.
- **U-Wert- und Ergebnisansicht:** Der aktivierte Modellstand speist eine
  feste Bauteildetailkarte, eine Tabelle aller vorhandenen Huellbauteile und
  zwei Ergebnisreiter. Oeffnungen bleiben positive Objekte und reduzieren
  ueber `host_element_id` die wirksame Bruttoflaeche ihres Host-Bauteils.
  `ma_building.thermal` berechnet UI-neutral mittlere U-Werte je Kategorie,
  eine vereinfachte Demo-Bilanz fuer `H_T` und den nur informativ gezeigten
  Kennwert `H'_T`.
- **Aktivierung und Bilanzgrenze:** Folgereiter bleiben ohne einen zum
  Auswahl-Schluessel, zur Gebaeude-ID und zur Modellversion passenden
  Projekt-Aktivstand gesperrt. Fehlt in LoD-1 die Fensterflaeche, leitet die
  Thermik sie als `A_Fenster = A_Aussenwand,brutto * Anteil / 100` ab;
  bei doppelter Angabe und beim Aggregatabgleich gilt
  `|A_explizit - A_abgeleitet| <= max(0,10 m2; 1 % * A_abgeleitet)`.
  Explizite Huellen brauchen `thermal_envelope_complete` und werden, sofern
  vorhandene Aggregatflaechen vorliegen, dagegen plausibilisiert.
  Widerspruechliche Angaben, nicht positive/nicht endliche U- oder
  Flaechenwerte sowie unvollstaendige Huellen sperren `H_T` und `H'_T`. Die
  UI zeigt bewusst nur eine sichtbare `Flaeche`; der positive Oeffnungsabzug
  bleibt an der Host-Beziehung nachvollziehbar.
- **Methodengrenze:** Fuer die V1-Demo gelten manuelle, sichtbar
  gekennzeichnete Annahmen `F=1,0` gegen Aussenluft, `F=0,5` gegen Erdreich
  und die feste Pauschale `Delta U_WB=0,10 W/(m2 K)`. Sie dienen weder als Normersatz noch als
  GEG-Nachweis. Grundlage fuer die Einordnung sind die oeffentlich
  zugaenglichen Regelungen in GEG Anlage 3 und GEG Paragraph 24; eine
  belastbare Erdreich-, Waermebruecken- oder Nichtwohngebaeude-Nachweisrechnung
  bleibt Folgearbeit.
  Oeffentliche Einstiege: [GEG Anlage 3](https://www.gesetze-im-internet.de/geg/anlage_3.html),
  [GEG Paragraph 24](https://www.gesetze-im-internet.de/geg/__24.html) und
  [BAFA-Fragenpool Gebaeudetechnik](https://www.bafa.de/SharedDocs/Downloads/DE/Energie/qpeb_uebungsfragen_gebaeudetechnik.pdf?__blob=publicationFile&v=7).
- **Naechster Schritt:** LoD-2-Inhalte fuer Raum-/Bauteilstruktur klaeren und
  reale IFC-Inhalte separat auswerten, bevor ein IFC-Lite-Import freigegeben
  wird. Rhino bleibt ohne aktive Parser-Abhaengigkeit.
