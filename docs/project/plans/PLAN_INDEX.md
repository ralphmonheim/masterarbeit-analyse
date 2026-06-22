# Plan Index

Stand: 2026-06-22

| Plan ID | Titel | Datei | Modul | Status | Prioritaet | Abhaengigkeiten | Naechster Schritt |
|---|---|---|---|---|---|---|---|
| P001 | Variantenmodul GUI und Logikpruefung | `../archive/plans/250603_Plan_Variantenmodul_GUI_Logikpruefung.md` | ma_variants, ma_analyse GUI | Archiviert | Hoch | P003, stabile Pfadstruktur | Nur als Referenz verwenden |
| P002 | Wetterdatenanalyse TRY Modul Integration | `../archive/plans/250603_Plan_Wetterdatenanalyse_TRY_Integration.md` | ma_weather | Archiviert, teilweise umgesetzt | Mittel | P003, P001 | Restarbeiten werden in P008 weitergefuehrt |
| P003 | Projektstruktur Review, Planungsbereich und Nutzerentscheidungen | `../archive/plans/250604_Plan_Projektstruktur_Review_Planungsbereich_Nutzerentscheidungen.md` | Projektorganisation | Archiviert | Hoch | keine | Nur bei Strukturfragen als Referenz verwenden |
| P004 | Projektplan Version 1.0.0 | `../archive/plans/PLAN_Projektplan_Version_1_0_0.md` | ma_variants, Gesamtprojekt | Archiviert | Niedrig | bereits umgesetzt bis Abschnitt 12 | Nur als Referenz verwenden |
| P005 | Gesamtmodulstruktur, Dashboard und UI-Auslagerung | `../archive/plans/250608_Plan_Gesamtmodulstruktur_PreProcess_PostProcess_Dashboard.md.txt` | Gesamtarchitektur, ma_ui, ma_workflow | Archiviert, teilweise umgesetzt | Hoch | P003 | Gueltige Struktur und Restarbeiten wurden in P007 uebernommen |
| P006 | Kontrollierter IDA-ICE-Variantenexport und IDM-Entwurf | `../archive/plans/260618_Plan_ma_export_ida_IDM_Exportentwurf.md` | historisch ma_export_ida | Archiviert, Entwurf | Mittel | ma_variants, Referenzmodell | Verbleibende Arbeit wird in P009 weitergefuehrt |
| P007 | Projektplan fuer die VS-Code-Umsetzung der Masterarbeitssoftware | `inbox/Masterarbeit_VSCode_Projektplan_2026-06-21.md` | Gesamtprojekt, Gesamtarchitektur | Aktiver Rahmenplan | Hoch | bestehender Projektstand und Nutzerentscheidungen | P009-Schnittstellenvertrag als naechsten Hochprioritaets-Slice planen |
| P008 | Wettermodul Abschluss und P007-Anbindung | `inbox/260621_Plan_P008_Wettermodul_Abschluss_P007_Anbindung.md` | ma_weather, ma_parameters | Aktiv | Mittel | P007, P002 | Fuenf verbleibende TRY-Jahresdatensaetze real pruefen |
| P009 | Allgemeine Simulationsschnittstellen mit IDA-ICE-Adapter | `inbox/260621_Plan_P009_Simulationsschnittstellen_IDA_Adapter.md` | ma_export_simulation, ma_import_simulation | Aktiv | Hoch | P007, ma_variants, ma_simulation_setup | Schnittstellenvertrag und Wiederverwendung des Basisexports konkret planen |
