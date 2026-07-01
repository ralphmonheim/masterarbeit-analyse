# ma_export_simulation

- **Zweck:** Varianten und Run-Konfiguration programmunabhaengig fuer Simulationsadapter vorbereiten.
- **Eingaben:** Varianten, Simulationssetup, Referenzmodell,
  Parametermapping und spaeter freigegebene Gebaeudemodellversionen aus
  `ma_building`.
- **Ausgaben:** Exportpaket, Run-Manifest und programmspezifische Adapterartefakte.
- **Abgrenzung:** kein Simulationsstart, keine ungesicherte IDM-Manipulation
  und keine direkte Uebergabe unvalidierter IFC-, Rhino- oder
  Demo-Gebaeudedaten.
- **Abhaengigkeiten:** `ma_variants`, `ma_simulation_setup`; Phase 3.
- **Status:** geplant; der Basisexport liegt noch unter `ma_variants.ida_export`.
- **Naechster Schritt:** P009 nach validiertem Run-Manifest umsetzen,
  freigegebene P012-Gebaeudedaten beruecksichtigen und den IDA-ICE-Adapter
  kontrolliert anbinden.

Der erste programmspezifische Adapter liegt unter
`ma_export_simulation.adapters.ida_ice`. Historische Bezeichnungen
`ma_export_ida` und `export_ida` werden nur als Uebergangsaliase unterstuetzt.
