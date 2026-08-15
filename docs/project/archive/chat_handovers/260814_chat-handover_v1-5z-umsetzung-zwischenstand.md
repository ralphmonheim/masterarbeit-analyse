# Chat-Handover – V1-5Z Umsetzung, Zwischenstand

Datum: 2026-08-14  
Git-Stand bei Archivierung: `9f58b57` auf `main`  
Status: Freigegebener unabhaengiger V1-Plan in Umsetzung; kein Commit, Push, Tag oder Release durch diesen Arbeitsstand.

## Fuehrende Quellen

- Aktiver Restumfang und Nachweise: `docs/project/plans/independent/260814_V1_5Z_Gebaeudemapping_Workflow_UI_PostProcess_Test.md`
- Offene fachliche Entscheidungen: `docs/project/decisions/USER_DECISIONS_OPEN_POINTS.md` (OP-009, OP-017, OP-018)
- Lokaler Vergleichs- und Testnachweis: `data/test_output/v1_5z_implementation_20260814.md`

## Erledigter Stand

- **B1 (5Z-Quellenmapping):** Direkte IDA-5Z-Zonalsummen sind die quantitative Vorrangquelle. IDM ist eine IDA-Modellbeschreibung; seine Wandsegmente bleiben als Detailnachweis erhalten, werden bei Abweichung aber nicht skaliert oder gemittelt.
- **B2 (Viewer-/IFC-Anreicherung):** Der IFC-Viewer-Excel-Export wird nur mit der bytegleichen SmallOffice-IFC nachverfolgt. Eine Zuordnung wird ausschließlich bei einem expliziten GlobalId-Feld aus Viewer/Mapping und passender IFC-Klasse akzeptiert; ohne diesen Link erfolgt kein Raten.
- **Thermische Huelle:** OG West und OG Ost enthalten die OGD (oberste Geschossdecke) als `uppermost_storey_ceiling` gegen `unconditioned_attic`. Sie ist kein Dach. Ohne bestaetigten U-Wert und Temperaturfaktor bleibt die thermische Bilanz bewusst `PARTIAL`.
- **Workflow:** Der V1-PreProcess folgt jetzt `Projekt → Wetter → Gebaeude → Technik → Zonen`. Die Technik-Zonen-Integration wird im nachgelagerten Zonengate validiert.
- **PRN-Vertrag:** PRN (IDA-Ergebniszeitreihe) mit widerspruechlichen Stützstellen wird im Standardvertrag nicht mehr automatisch aufgeloest. Eine getrennte „letzter Wert“-Anzeigeprojektion ist ausschließlich visualisierend und nicht energiebilanzfaehig.

## Konkreter Quellenbefund

Die tatsächlichen 5Z-IDM-Wanddetails schliessen nicht auf die führenden 5Z-Excel-Summen:

| Zone | IDA-5Z-Excel, opake Wand | IDM-Segmente | Befund |
|---|---:|---:|---|
| Lobby | 34,490 m² | 124,484 m² | Konflikt, nicht skaliert |
| EG West | 79,580 m² | 89,650 m² | Konflikt, nicht skaliert |
| EG Ost | 59,720 m² | 70,640 m² | Konflikt, nicht skaliert |
| OG West | 85,940 m² | 91,600 m² | Konflikt, nicht skaliert |
| OG Ost | 64,300 m² | 75,170 m² | Konflikt, nicht skaliert |

Der Viewer-Excel-Hash `D7DDBC...` stimmt mit dem im unabhängigen Plan genannten Viewer-Referenzartefakt überein. Der IFC-Hash `B933A0...` stimmt mit der dort genannten externen und lokalen bytegleichen SmallOffice-IFC überein. Die beiden Hashes werden nicht miteinander verglichen; sie kennzeichnen unterschiedliche Quellen.

## Tests

- Fokustests: `27 passed` in 6,73 s.
- UI-Shell: `139 passed` in 8,75 s.
- Die pytest-Fortschrittsanzeige der Vollsuite erreichte 100 %, aber der Sandbox-Prozess lief vor pytest-Abschluss und finalem Exit-Status ins Zeitlimit. Die Vollsuite ist daher **nicht als bestanden nachgewiesen**.

## Uebertragene Restarbeit

Die Restarbeit ist im unabhaengigen V1-Plan als führender Umfang dokumentiert, nicht in diesem Archiv weitergefuehrt. Naechste Reihenfolge:

1. **29Z-Quellstand trennen:** eigener 29Z-Building-Loader und Raumregister; Nachweis: exakt 29 Zonen ohne Zugriff auf die 5Z-Spezifikation.
2. **P018-Multi-VAR-RUN:** den historischen Einzelpaket-Aufrufer auf den gemeinsamen RunManifestV1-Vertrag migrieren; Nachweis: ein identisches Optimierungssetup mit mehreren VAR, getrennte Sensitivitätsruns bei unterschiedlichem Wetter.
3. **Import/Prepare und Analyse:** 5Z vollständig bis `prepared`, 29Z/ALT nur mit konservativem Konfliktstatus; Nachweis: keine Energieintegration bei PRN-Duplikaten und lesbare Tabellen/Diagramme mit Herkunft/Eignung.
4. **UI und Prozessmessung:** Workflow- und Direktansichten gegen identische Services testen sowie die Prozessmappe nur additiv über eine temporäre Testmappe bearbeiten.

## Offene Fachgates

- **Nordbezug:** Nutzerbestaetigung oder nachvollziehbare Modellquellenangabe zu `north_angle_deg`; bis dahin nur Modellrichtungen ausgeben.
- **IDM-vs.-Excel:** fachliche Entscheidung, ob und wie die Segmentkonflikte aufgeloest werden. Ohne Entscheidung bleiben Excel-Summe und IDM-Detail nebeneinander.
- **OGD-Thermik:** bestätigter U-Wert und Temperatur-Randfall für den unbeheizten Dachraum; bis dahin `PARTIAL`.
- **OP-017:** Dateninventar muss Zeitstempel-/Intervall-, Einheiten-, Vorzeichen- und Leistungs-/Energiesemantik verbindlich festlegen.
- **OP-018:** erst nach OP-017 projektbezogene, nicht normative Funktions- und Bewertungsregeln festlegen.
- **OP-009:** Vergleichsprotokoll mit Prozessgrenzen, Wissensprofil, aktiver Zeit, Wartezeit und Kostenannahmen festlegen.

## Grenzen

Keine automatische IDA-Steuerung, keine 3DM-Inhaltsverarbeitung, keine neue Abhaengigkeit, keine Cloud-/externe Verarbeitung und keine normative Komfort- oder Einsparungsbehauptung sind erfolgt.
