# Eingabe- und Formatmatrix

Stand: 2026-07-12
Grundlage: P010

## Reifegrade

- `supported`: implementiert und automatisiert getestet
- `prototype`: technisch vorhanden, aber noch keine verbindliche allgemeine
  Eingabeschnittstelle
- `planned`: in einem freigegebenen Fachplan vorgesehen
- `out_of_scope`: fuer den aktuellen Masterarbeitsumfang ausgeschlossen

## Matrix

| Bereich | Format oder Quelle | Reifegrad | Einordnung |
|---|---|---|---|
| gemeinsame Konfiguration | YAML, JSON lesen | supported | technischer Loader in `ma_core` |
| gemeinsame Konfiguration | YAML geschuetzt speichern | supported | Vorlagen- und Kollisionsschutz aus P028 |
| Wetter | TRY importieren und validieren | supported | P010-Pilot mit `InputSource`, Diagnosen und Freigabe |
| Analyse | CSV, XLSX | prototype | vorhandene Analysepfade, keine allgemeine Eingabeschnittstelle |
| Building | YAML-Demo | supported | P012 v1, versionierte `BuildingModelSpecification` mit Tests |
| Building | BusinessIntegration-LoD-1-YAML | supported | P012-S2, minimaler Eingabeumfang aus dem Rhino-Testgebaeude fuer Kubatur, Huellkennwerte, U-Werte und Fensteranteil |
| Building | JSON | planned | Folgeformat zur gleichen BuildingModelSpecification |
| Building | SmallOffice-IFC als Fachteil-Referenz | supported | lokale Metadaten- und Entity-Diagnose, kein Vollimport |
| Building | Rhino-Testgebaeude als BusinessIntegration-Referenz | supported | lokale Metadaten- und Hash-Diagnose; verbindliche Quelle bleibt die daraus abgeleitete kleine `BuildingModelSpecification` |
| Building | weitere lokale IDA-ICE-IFC-Samples | supported | Vergleichs- und Plausibilisierungsdiagnose, kein Vollimport |
| Building | IFC-Lite | planned | Umfang bleibt von OP-012 und realen IFC-Inhalten abhaengig |
| Building | Rhino `.3dm` Quelldiagnose | supported | lokale Metadaten- und Hash-Diagnose, kein Rhino-Parser |
| Building | Rhino `.3dm` Produktivimport | out_of_scope | fachlicher Ausbaupfad; direkte CAD-Integration ist im aktuellen Umfang nicht freigegeben |
| Building | DWG/CAD-Beispieldatei | supported | lokale Metadaten-/Warnungsdiagnose als ungepruefte CAD-Quelle, kein Gebaeudemodellimport |
| Building | DWG-Produktivimport | out_of_scope | UD-066: kein DWG-Parser, Add-on oder externe DWG-Library im aktuellen Masterarbeitsumfang |
| Zones | BusinessIntegration-LoD-1-YAML | supported | P013-S1, eine validierte Gesamtgebaeudezone mit einfachem Buero-Nutzungsprofil; P013-S2 konsolidiert den Zielumfang |
| Zones | P013-S2-Zonenstand | planned | Raum-Zonen-Zuordnung, Nutzung, Profile, Konditionierung, Uebergabe, Feiertage, Parameteruebergabe und Veraltet-Status |
| Zones | spaetere Importprofile | planned | nach P013-S3 bis P013-S7 und konkreter Raum-Zonen-Zuordnung |
| Technical | BusinessIntegration-LoD-1-YAML | supported | P014-S1, validierte Referenzannahmen fuer Heizung, Kuehlung und Lueftung; aktuelle Zonenreferenz bleibt Uebergangsvertrag |
| Technical | zentrale Systemreferenzen fuer ma_zones | planned | P014-Folgeausbau gemaess P013-S2, zentrale Technik vor Zonen |
| Technical | Systemvorlagen und Produktdaten | planned | P014-Folgeausbau |
| Parameters | BusinessIntegration-LoD-1-ParameterSnapshot | supported | P015-S1, validierter Snapshot v1 aus Building, Zones und Technical mit Quellenreferenzen |
| Parameters | ParameterInputPackage mit aktiviertem Wetter-Default | supported | P015-S3a, Eingangspaket-Checkpoint aus Snapshot v1 plus freigegebenem `ma_weather`-Projekt-Default |
| Parameters | P013-S2-Zonenstand mit Status/Fingerprint | planned | `current`, `outdated` und `validation_required` sowie Blockierung der Variantengenerierung bei veraltetem Stand |
| Parameters | BaselineParameterSnapshot v2 aus BusinessIntegration-LoD-1 | supported | P015-S2, Scopes, Parameterklassen, Variierbarkeit, Quellenreferenzen, Referenzversionen und Content-Hash automatisiert getestet |
| Parameters | ReferenceDimensioningResult und ParameterVariationSpecification | planned | P015 konsolidiert; Stage-1-Einbindung und VariationSpecification folgen in P015-S6 bis P015-S9 |
| Parameters | YAML-Kataloge und spaetere Importvorlagen | prototype | P028-Demo vorhanden, Snapshot-Speicherung und Importvorlagen folgen |
| Dimensioning | ParameterSnapshot v1 | supported | P016-S1, LoD-1-Referenzdimensionierung mit Rechenweg und Hinweisen |
| Dimensioning | VariantDimensioningResult fuer P017 | planned | Stage 1 beantwortet spaeter DimensioningRequests aus `VariantVerification` ueber `ma_workflow` |
| Variants | VSP/VVER/VCAT/VSEL/VGEN | planned | P017 konsolidiert; erster Ausbau mit VCAT max 500, Selection all/manual/random und direkter Uebergabe an P018 |
| Normen | CSV, JSON, YAML und Review-Dokumente | prototype | lokaler Pruefbestand unter `data/common/normen/`; keine freigegebene Normlogik |
| Kalender | XLSX, CSV und PDF | prototype | lokale Feiertags- und Kalenderreferenzen unter `data/common/kalender/`; noch keine allgemeine Kalender-API |
| Naming | YAML | supported | P028-Demo mit geschuetzter lokaler Speicherung |
| Simulation setup | RunManifest mit direkter RUN/VAR-Zuordnung | planned | P018 nach P017; kein `SimulationCase`, keine `CASE-ID` |
| Simulationsadapter | programmspezifische Vorlagen | planned | P009 nach validiertem Run-Manifest; Export/Import ueber `RUN-ID + VAR-ID` |
| CAD-Integration | direkte CAD-Steuerung | out_of_scope | nicht Teil der Masterarbeit |

Import wird je Fachmodul bevorzugt. Manuelle und Demo-Quellen sind durch
`InputSourceKind` vorbereitet, werden aber erst im jeweiligen Fachplan
konkretisiert. Die Matrix legt keine noch ungeprueften Pflichtformate fest.

## Ablagegrenzen

- Originaldateien bleiben unveraendert in lokalen Modul-Eingangsordnern.
- Normalisierte Daten liegen in den jeweiligen lokalen Modul-Datenordnern.
- Normenextrakte, Formelkandidaten und Kalenderreferenzen bleiben lokale
  Pruefbestaende, bis sie fachlich validiert und in konkrete Fachmodelle
  ueberfuehrt wurden.
- Fachberichte bleiben von Sitzungs- und Laufprotokollen getrennt.
- Maschinenlesbare Sitzungsereignisse liegen unter
  `logs/sessions/<session_id>.jsonl`.
- Bestehende menschenlesbare Analyse-Logs unter `logs/*.log` bleiben erhalten.
- Datenbanktabellen werden erst nach stabilen Fachmodellen und konkreten
  Abfragen festgelegt.
