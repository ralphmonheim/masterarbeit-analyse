# P009 Allgemeine Simulationsschnittstellen mit IDA-ICE-Adapter

Stand: 2026-07-12
Status: Zurueckgestellt bis P018; RUN/VAR-Zuordnung fachlich geschaerft
Bezug: P007, P018, archivierter P006

## Ziel

Die allgemeinen Module `ma_export_simulation` und `ma_import_simulation`
schrittweise als programmunabhaengige Schnittstellen aufbauen. IDA ICE wird
ausschliesslich ueber `adapters/ida_ice` angebunden.

P009 wird erst nach der funktionsfaehigen Eingabekette, `ma_parameters`,
Variantenanbindung und einem validierten `RunManifest` aus P018 technisch
fortgesetzt. Die Masterarbeit priorisiert die Schritte bis
`ma_simulation_setup`.

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
4. `RunManifest` aus P018 als verbindliche Eingabegrenze verwenden.
5. Export und Import ueber `RUN-ID + VAR-ID` zuordnen; keine `CASE-ID`
   einfuehren.

## Entwicklungsstufe 2: Kontrollierter IDA-ICE-Exportadapter

1. Bestehenden Basisexport aus `ma_variants.ida_export` ueber eine neutrale
   Fassade wiederverwenden.
2. Geprueftes Referenzmodell pro Exportfall kopieren.
3. Run-Manifest und gemeinsame Simulationskonfiguration dokumentieren.
4. Verifiziertes Parametermapping zwischen zentraler Parameterliste und
   IDA-ICE-Zielen einfuehren.
5. Freigegebene Gebaeudemodellversionen aus P012 als moegliche spaetere
   Geometrie- und Raumquelle beruecksichtigen, ohne daraus vor P018 einen
   produktiven IFC- oder IDA-ICE-Export abzuleiten.
6. IFC als moegliches semantisches Austauschformat zum IDA-ICE-Adapter pruefen,
   sobald der Schnittstellenvertrag und der konkrete Exportweg verifiziert
   sind.
7. Exportindex fuer Projekt, Run und Varianten erzeugen.

Eingang fuer den Export:

- `RUN-ID`
- `VAR-IDs`
- vorbereitete Dateien oder Dateispezifikationen aus P018
- Zielpfad
- Adapterversion

`ma_export_simulation` bestimmt keine fachlichen Variantenwerte und veraendert
keine Selection.

## Entwicklungsstufe 3: Kontrollierter IDA-ICE-Importadapter

1. Ergebnisdateien und Ergebnisordner erkennen.
2. Projekt, Run, Variante, Raum und System eindeutig zuordnen.
3. Rohdaten unveraendert sichern.
4. Namen, Einheiten und Zeitstempel vereinheitlichen.
5. Standardisierte Ergebnisdaten an `ma_analyse` uebergeben.

Simulationsergebnisse werden mindestens ueber `RUN-ID + VAR-ID` zugeordnet.
Ein fehlgeschlagenes Ergebnis erzeugt keinen separaten Case, sondern einen
run-internen Status je `VAR-ID`.

## Sicherheitsgrenzen

- Keine freie Neuerzeugung kompletter IDM-Modelle.
- Keine textbasierte IDM-Manipulation. Ein technisch verifizierter Parser ist
  keine Lizenz- oder Compliance-Freigabe; jede spaetere Ausnahme erfordert
  eine ausdrueckliche schriftliche EQUA-Freigabe.
- Keine erfundenen IDA-ICE-Skript- oder API-Befehle.
- Kein automatischer Simulationsstart, keine automatisierte
  Simulationsausfuehrung und keine Nutzung als Simulationsserver ohne
  ausdrueckliche schriftliche EQUA-Freigabe.
- Keine Fachlogik in Streamlit.
- Keine direkte Uebergabe von unvalidierten IFC-, Rhino- oder
  Demo-Gebaeudedaten an IDA ICE.
- Vollstaendige `.idm`-Dateien, EQUA-Bibliotheken, NMF-Modelle und unbekannte
  Drittdateien sind kein regulaerer Adaptereingang. Sie duerfen nur nach
  dokumentiertem Preflight gemass `docs/compliance/ida_ice/` bewertet werden.

## Tests und Akzeptanzkriterien

- Tests laufen ohne IDA-ICE-Installation mit Dummy-Referenzdateien.
- Bestehende Basisexporttests bleiben gueltig.
- Referenzmodellkopie, Run-Manifest, Parametermapping und Exportindex sind
  reproduzierbar getestet.
- Importzuordnung behandelt fehlende, doppelte und unvollstaendige Ergebnisse
  mit strukturierten Fehlern oder Warnungen.
- Alle erzeugten Artefakte sind Projekt, Run und Variante eindeutig
  zugeordnet.
- Historische oder externe Begriffe wie `CASE` werden nicht als neue
  Hauptobjekte eingefuehrt.

## Historischer Bezug

Der urspruengliche IDA-spezifische Entwurf liegt unveraendert unter
`docs/project/archive/plans/260618_Plan_ma_export_ida_IDM_Exportentwurf.md`.
