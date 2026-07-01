# Eingabe- und Formatmatrix

Stand: 2026-07-01
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
| Building | YAML-Demo | planned | P012, erster verbindlicher Demonstrator |
| Building | JSON | planned | Folgeformat zur gleichen BuildingModelSpecification |
| Building | aktuelle lokale IFC-Datei | planned | Diagnose- und Trainingsbasis, kein Vollimport |
| Building | IFC-Lite | planned | Umfang bleibt von OP-012 und realen IFC-Inhalten abhaengig |
| Building | Rhino `.3dm` | out_of_scope | fachlicher Ausbaupfad; direkte CAD-Integration ist im aktuellen Umfang nicht freigegeben |
| Zones | YAML-Demo und spaetere Importprofile | planned | P013 |
| Technical | YAML-Demo und Systemvorlagen | planned | P014 |
| Parameters | YAML-Kataloge und spaetere Importvorlagen | prototype | P028-Demo vorhanden, produktiver Snapshot folgt in P015 |
| Naming | YAML | supported | P028-Demo mit geschuetzter lokaler Speicherung |
| Simulationsadapter | programmspezifische Vorlagen | planned | P009 nach validiertem Run-Manifest |
| CAD-Integration | direkte CAD-Steuerung | out_of_scope | nicht Teil der Masterarbeit |

Import wird je Fachmodul bevorzugt. Manuelle und Demo-Quellen sind durch
`InputSourceKind` vorbereitet, werden aber erst im jeweiligen Fachplan
konkretisiert. Die Matrix legt keine noch ungeprueften Pflichtformate fest.

## Ablagegrenzen

- Originaldateien bleiben unveraendert in lokalen Modul-Eingangsordnern.
- Normalisierte Daten liegen in den jeweiligen lokalen Modul-Datenordnern.
- Fachberichte bleiben von Sitzungs- und Laufprotokollen getrennt.
- Maschinenlesbare Sitzungsereignisse liegen unter
  `logs/sessions/<session_id>.jsonl`.
- Bestehende menschenlesbare Analyse-Logs unter `logs/*.log` bleiben erhalten.
- Datenbanktabellen werden erst nach stabilen Fachmodellen und konkreten
  Abfragen festgelegt.
