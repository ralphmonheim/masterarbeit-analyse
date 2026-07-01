# ma_building

- **Zweck:** Programmneutrales Gebaeudemodell mit Gebaeude, Geschossen,
  geometrischen Raeumen, Bauteilen, Flaechen, Oeffnungen, einfachen
  Sonnenschutzinformationen und bauphysikalischen Randbedingungen verwalten.
- **Eingaben:** einfache Demo-`BuildingModelSpecification`, manuelle oder
  textliche YAML-/JSON-Daten und lokale Importdiagnosen. Die aktuelle
  IFC-Arbeitsdatei ist als lokale Trainings- und Diagnosebasis vorgesehen,
  nicht als zugesagter Vollimport.
- **Ausgaben:** freigegebene, versionierte Gebaeudedaten fuer
  `ma_parameters`; bauliches Raumregister und Zonierungsvorschlaege fuer
  `ma_zones`; spaeter Mengen- und Modellinformationen fuer Bewertung und
  Simulationsadapter.
- **Abgrenzung:** Nutzungsprofile und thermische Zonen liegen in `ma_zones`;
  technische Anlagen und Regelung in `ma_technical`; technische Datenhaltung
  in `ma_database`; IDA-ICE-Uebergabe in `ma_export_simulation`.
- **Abhaengigkeiten:** `ma_project`, P010/P027-Diagnose- und
  Freigabevertraege; Phase 2.
- **Status:** geplant.
- **Naechster Schritt:** P012 mit einfacher Demo-Spec, lokaler
  IFC-Inhaltsdiagnose, Reifegradbewertung und `BuildingModelSpecification`
  vorbereiten; IFC-Lite und Rhino bleiben offene Ausbaupfade.
