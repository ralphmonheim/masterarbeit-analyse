# Plan Index

Stand: 2026-06-18

| Plan ID | Titel | Datei | Modul | Status | Prioritaet | Abhaengigkeiten | Naechster Schritt |
|---|---|---|---|---|---|---|---|
| P001 | Variantenmodul GUI und Logikpruefung | `../archive/plans/250603_Plan_Variantenmodul_GUI_Logikpruefung.md` | ma_variants, ma_analyse GUI | Archiviert | Hoch | P003, stabile Pfadstruktur | Nur als Referenz verwenden |
| P002 | Wetterdatenanalyse TRY Modul Integration | `inbox/250603_Plan_Wetterdatenanalyse_TRY_Integration.md` | ma_weather | Teilweise umgesetzt | Mittel | P003, P001, aktueller Release-Stand | TRY-Importer und Validierung als naechsten Slice planen |
| P003 | Projektstruktur Review, Planungsbereich und Nutzerentscheidungen | `../archive/plans/250604_Plan_Projektstruktur_Review_Planungsbereich_Nutzerentscheidungen.md` | Projektorganisation | Archiviert | Hoch | keine | Nur bei Strukturfragen als Referenz verwenden |
| P004 | Projektplan Version 1.0.0 | `../archive/plans/PLAN_Projektplan_Version_1_0_0.md` | ma_variants, Gesamtprojekt | Archiviert | Niedrig | bereits umgesetzt bis Abschnitt 12 | Nur als Referenz verwenden |
| P005 | Gesamtmodulstruktur, Pre-/Post-Process und Dashboard | `inbox/250608_Plan_Gesamtmodulstruktur_PreProcess_PostProcess_Dashboard.md.txt` | Gesamtarchitektur, ma_ui, ma_workflow | Teilweise umgesetzt | Hoch | P003, bestehende ma_analyse GUI, ma_variants, ma_weather | Analyse-View weiter gegen Tkinter-Ablauf pruefen oder Platzhalter-Views mit echten Services befuellen |
| P006 | Kontrollierter IDA-ICE-Variantenexport und IDM-Entwurf | `inbox/260618_Plan_ma_export_ida_IDM_Exportentwurf.md` | ma_export_ida | Entwurf | Mittel | ma_variants, ma_simulation_setup, geprueftes IDA-Referenzmodell | Bestehende Exportlogik und lokale IDA-Schnittstellen zuerst analysieren |
