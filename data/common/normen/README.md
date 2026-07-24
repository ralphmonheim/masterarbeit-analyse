# Normen-Datenbereich

Dieser Ordner verwaltet lokale Normen- und Regelgrundlagen in der
Entwicklungsphase. Er ist ein Daten- und Pruefbestand, kein Python-Modul und
kein freigegebener Rechenkern.

## Zweck

- Lokale, noch nicht freigegebene Normen-Arbeitsstaende strikt von
  versionierter Projektlogik trennen.
- Bereinigte Metadaten und spaetere manuelle Review-Verweise
  nachvollziehbar zuordnen.
- Pruefstatus und Review-Arbeit von produktiver Normlogik trennen.
- Spaetere Plaene wie P020 und `ma_analyse.stage_3_standards_verification`
  mit belastbaren Eingangslisten versorgen.

## Struktur

```text
data/common/normen/
  source_inventory_metadata.yaml  # bereinigter Quellen-Metadatenindex
  rounds/
    round1_v0_1/
      incoming/   # Originalpakete der Auswertungsrunde
      extracted/  # entpackte Extraktionsdaten
      review/     # spaetere fachliche Pruefnotizen
  current/         # spaeter bewusst ausgewaehlter Arbeitsstand
  templates/       # spaetere Review- oder Importvorlagen
    din18599_zone_profile_contract.yaml  # wertfreier Planungsvertrag
```

## Regeln

- Inhalte unter `incoming/`, `extracted/` und `review/` bleiben lokal und
  werden nicht versioniert.
- Formeln, Grenzwerte und Regeln gelten erst nach fachlicher Pruefung als
  implementierbar.
- Produktive Normlogik entsteht spaeter in
  `src/ma_analyse/stage_3_standards_verification/`.
- `source_inventory_metadata.yaml` bleibt ein Navigationsindex: Es enthaelt
  keine semantischen Inhaltszusammenfassungen oder Quellenwerte.
- `templates/din18599_zone_profile_contract.yaml` beschreibt nur die spaetere
  Anbindung an die bestehenden `ma_zones`-Felder und wird nicht vom aktuellen
  Loader eingelesen.
- Kalender- und Feiertagsdaten liegen getrennt unter `data/common/kalender/`,
  weil sie mehrere Fachbereiche betreffen koennen.
