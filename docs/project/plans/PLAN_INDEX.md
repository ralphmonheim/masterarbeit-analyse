# Plan Index

Stand: 2026-06-24

| Plan ID | Titel | Datei | Modul | Status | Prioritaet | Abhaengigkeiten | Naechster Schritt |
|---|---|---|---|---|---|---|---|
| P001 | Variantenmodul GUI und Logikpruefung | `../archive/plans/250603_Plan_Variantenmodul_GUI_Logikpruefung.md` | ma_variants, ma_analyse GUI | Archiviert | Hoch | P003, stabile Pfadstruktur | Nur als Referenz verwenden |
| P002 | Wetterdatenanalyse TRY Modul Integration | `../archive/plans/250603_Plan_Wetterdatenanalyse_TRY_Integration.md` | ma_weather | Archiviert, teilweise umgesetzt | Mittel | P003, P001 | Restarbeiten werden in P008 weitergefuehrt |
| P003 | Projektstruktur Review, Planungsbereich und Nutzerentscheidungen | `../archive/plans/250604_Plan_Projektstruktur_Review_Planungsbereich_Nutzerentscheidungen.md` | Projektorganisation | Archiviert | Hoch | keine | Nur bei Strukturfragen als Referenz verwenden |
| P004 | Projektplan Version 1.0.0 | `../archive/plans/PLAN_Projektplan_Version_1_0_0.md` | ma_variants, Gesamtprojekt | Archiviert | Niedrig | bereits umgesetzt bis Abschnitt 12 | Nur als Referenz verwenden |
| P005 | Gesamtmodulstruktur, Dashboard und UI-Auslagerung | `../archive/plans/250608_Plan_Gesamtmodulstruktur_PreProcess_PostProcess_Dashboard.md.txt` | Gesamtarchitektur, ma_ui, ma_workflow | Archiviert, teilweise umgesetzt | Hoch | P003 | Gueltige Struktur und Restarbeiten wurden in P007 uebernommen |
| P006 | Kontrollierter IDA-ICE-Variantenexport und IDM-Entwurf | `../archive/plans/260618_Plan_ma_export_ida_IDM_Exportentwurf.md` | historisch ma_export_ida | Archiviert, Entwurf | Mittel | ma_variants, Referenzmodell | Verbleibende Arbeit wird in P009 weitergefuehrt |
| P007 | Projektplan fuer die VS-Code-Umsetzung der Masterarbeitssoftware | `inbox/Masterarbeit_VSCode_Projektplan_2026-06-21.md` | Gesamtprojekt, Gesamtarchitektur | Aktiver Rahmenplan | Hoch | bestehender Projektstand und Nutzerentscheidungen | P011 als naechste Fachstufe bearbeiten |
| P008 | ma_weather Gesamtplan | `inbox/260623_Plan_P008_ma_weather_Gesamtplan.md` | ma_weather, ma_parameters, ma_ui, Stage 4 | Aktiv | Hoch | P007, P002, P010, P015, P018, P021, P027 | Reale Jahr-, Sommer- und Winterdatensaetze pruefen, P021-Ereignisdefinition schaerfen und Uebergabe an ma_parameters vorbereiten |
| P009 | Allgemeine Simulationsschnittstellen mit IDA-ICE-Adapter | `inbox/260621_Plan_P009_Simulationsschnittstellen_IDA_Adapter.md` | ma_export_simulation, ma_import_simulation | Zurueckgestellt | Mittel | P007, P018 | Nach validiertem Run-Manifest weiterfuehren |
| P010 | Eingabe- und Datenhaltungsarchitektur | `../archive/plans/260622_Plan_P010_Eingabe_Datenhaltungsarchitektur.md` | alle Eingabemodule, ma_validation | Archiviert, Wetterpilot umgesetzt | Hoch | P007 | Vertraege in P011 bis P015 fachmodulweise anwenden |
| P011 | ma_project Projektinitialisierung | `inbox/260622_Plan_P011_ma_project_Projektinitialisierung.md` | ma_project | Geplant | Hoch | P010 | Projektkonfiguration und Quellenwahl planen |
| P012 | ma_building Gebaeudeinput | `inbox/260622_Plan_P012_ma_building_Gebaeudeinput.md` | ma_building | Geplant, Konzept/Demo | Hoch | P010, P011 | Demo-Fachmodell und IFC-Diagnose planen |
| P013 | ma_zones Zonen und Nutzungen | `inbox/260622_Plan_P013_ma_zones_Zonen_Nutzungen.md` | ma_zones | Geplant, Konzept/Demo | Mittel | P010, P012 | Zonen-, Nutzungs- und Profilmodell planen |
| P014 | ma_technical Technische Systeme | `inbox/260622_Plan_P014_ma_technical_Technische_Systeme.md` | ma_technical | Geplant, Lite/Demo | Hoch | P010, P013 | Bestehende Systemtemplates inventarisieren |
| P015 | ma_parameters Zentrale Parameter | `inbox/260622_Plan_P015_ma_parameters_Zentrale_Parameter.md` | ma_parameters | Geplant | Hoch | P008, P010, P012-P014 | ParameterSnapshot und Importvorlagen planen |
| P016 | Analyse Stufe 1 Dimensionierung | `inbox/260622_Plan_P016_Stage1_Dimensionierung.md` | ma_analyse.stage_1_dimensioning | Geplant | Hoch | P015 | Vereinfachte Verfahren und Referenzfall festlegen |
| P017 | ma_variants und Naming-Anbindung | `inbox/260622_Plan_P017_ma_variants_Naming_Anbindung.md` | ma_variants | Geplant | Hoch | P015, P016 | Snapshot- und Naming-Schnittstelle planen |
| P018 | ma_simulation_setup und Run-Manifest | `inbox/260622_Plan_P018_ma_simulation_setup_Run_Manifest.md` | ma_simulation_setup | Geplant | Hoch | P008, P011, P017 | RunManifest und Freigaberegeln planen |
| P019 | Analyse Stufe 2 Optimierung | `inbox/260622_Plan_P019_Stage2_Optimierung.md` | ma_analyse.stage_2_optimization | Geplant, teilweise vorhanden | Mittel | bestehendes ma_analyse | Vorhandene Befehle als Stufe-2-Ablauf ordnen |
| P020 | Analyse Stufe 3 Standards Compliance | `inbox/260622_Plan_P020_Stage3_Standards_Compliance.md` | ma_analyse.stage_3_standards_compliance | Research-Plan | Hoch | P019 | Deutsche Normen- und Methodenmatrix erstellen |
| P021 | Analyse Stufe 4 Sensitivitaet | `inbox/260622_Plan_P021_Stage4_Sensitivitaet.md` | ma_analyse.stage_4_sensitivity | Geplant | Mittel | P008, P019 | Wetterereignisse und Zeitfenster verbinden |
| P022 | ma_economy Demo und Konzept | `inbox/260622_Plan_P022_ma_economy_Demo.md` | ma_economy | Konzept/Demo | Mittel | P019 | Demo-Umfang und Annahmen festlegen |
| P023 | ma_sustainability Demo und Konzept | `inbox/260622_Plan_P023_ma_sustainability_Demo.md` | ma_sustainability | Konzept/Demo | Mittel | P019 | Emissionsfaktoren und Systemgrenzen festlegen |
| P024 | ma_assessment Konzept | `inbox/260622_Plan_P024_ma_assessment_Konzept.md` | ma_assessment | Konzept | Niedrig | P019, P022, P023 | Kriterien- und Gewichtungsmodell planen |
| P025 | ma_reporting Konzept und Demo-Factsheet | `inbox/260622_Plan_P025_ma_reporting_Konzept.md` | ma_reporting | Konzept | Niedrig | P024 | Berichtsinventar und Factsheet planen |
| P026 | ma_data_export Konzept | `inbox/260622_Plan_P026_ma_data_export_Konzept.md` | ma_data_export | Konzept | Niedrig | P024, P025 | Paketformate und Manifest planen |
| P027 | Querschnitt UI, Workflow, Validation und Feedback | `inbox/260622_Plan_P027_Querschnitt_UI_Workflow_Validation_Feedback.md` | ma_ui, ma_workflow, ma_validation, ma_feedback | Aktiv, begleitend | Hoch | alle Teilplaene | Gemeinsame Quellen-, Status- und Freigabemodelle begleiten |
| P028 | Projekt-, Parameter- und Naming-Demo in Streamlit | `../archive/plans/260623_Plan_P028_Projekt_Parameter_Naming_Streamlit.md` | ma_project, ma_parameters, ma_variants, ma_ui | Archiviert, Demo umgesetzt | Hoch | P010, P011, P015, P017, P027 | ParameterSnapshot und Projektstammdaten ueber P011/P015 weiterfuehren |
