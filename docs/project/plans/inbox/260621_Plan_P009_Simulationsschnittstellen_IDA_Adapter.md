# P009 Allgemeine Simulationsschnittstellen mit IDA-ICE-Adapter

Stand: 2026-06-21  
Status: Aktiv  
Bezug: P007, archivierter P006

## Ziel

Die allgemeinen Module `ma_export_simulation` und `ma_import_simulation`
schrittweise als programmunabhaengige Schnittstellen aufbauen. IDA ICE wird
ausschliesslich ueber `adapters/ida_ice` angebunden.

## Wiederzuverwendender Bestand

- `ma_variants.ida_export` erzeugt bereits Variantenordner,
  `metadata.json`, `resolved_parameters.json` und `export_log.txt`.
- Die Exportkonfiguration liegt unter
  `config/ma_variants/export/example_ida_export.yaml`.
- Tests sichern Ordnernamen, Parameterauflosung, Metadaten und die
  Nichtveraenderung vorhandener IDA-Dateien.
- `ma_variants.simulation_results` und `ma_analyse` enthalten bereits
  Ergebniszuordnung und Aufbereitung.

Diese Logik wird in P009 nicht kopiert oder ungeprueft verschoben.

## Entwicklungsstufe 1: Schnittstellenvertrag

1. Neutrale Ein- und Ausgabeobjekte fuer Exportpaket, Run-Manifest,
   Adapterergebnis und Importergebnis planen.
2. Verantwortlichkeiten zwischen `ma_variants`, `ma_simulation_setup`,
   `ma_export_simulation`, `ma_import_simulation` und `ma_analyse`
   dokumentieren.
3. Historische Schluessel `ma_export_ida`, `ma_import_ida`, `export_ida` und
   `import_ida` nur als Uebergangsaliase behandeln.

## Entwicklungsstufe 2: Kontrollierter IDA-ICE-Exportadapter

1. Bestehenden Basisexport aus `ma_variants.ida_export` ueber eine neutrale
   Fassade wiederverwenden.
2. Geprueftes Referenzmodell pro Exportfall kopieren.
3. Run-Manifest und gemeinsame Simulationskonfiguration dokumentieren.
4. Verifiziertes Parametermapping zwischen zentraler Parameterliste und
   IDA-ICE-Zielen einfuehren.
5. Exportindex fuer Projekt, Run und Varianten erzeugen.

## Entwicklungsstufe 3: Kontrollierter IDA-ICE-Importadapter

1. Ergebnisdateien und Ergebnisordner erkennen.
2. Projekt, Run, Variante, Raum und System eindeutig zuordnen.
3. Rohdaten unveraendert sichern.
4. Namen, Einheiten und Zeitstempel vereinheitlichen.
5. Standardisierte Ergebnisdaten an `ma_analyse` uebergeben.

## Sicherheitsgrenzen

- Keine freie Neuerzeugung kompletter IDM-Modelle.
- Keine textbasierte IDM-Manipulation ohne verifizierten Parser.
- Keine erfundenen IDA-ICE-Skript- oder API-Befehle.
- Kein automatischer Simulationsstart in der ersten Zielstufe.
- Keine Fachlogik in Streamlit.

## Tests und Akzeptanzkriterien

- Tests laufen ohne IDA-ICE-Installation mit Dummy-Referenzdateien.
- Bestehende Basisexporttests bleiben gueltig.
- Referenzmodellkopie, Run-Manifest, Parametermapping und Exportindex sind
  reproduzierbar getestet.
- Importzuordnung behandelt fehlende, doppelte und unvollstaendige Ergebnisse
  mit strukturierten Fehlern oder Warnungen.
- Alle erzeugten Artefakte sind Projekt, Run und Variante eindeutig
  zugeordnet.

## Historischer Bezug

Der urspruengliche IDA-spezifische Entwurf liegt unveraendert unter
`docs/project/archive/plans/260618_Plan_ma_export_ida_IDM_Exportentwurf.md`.
