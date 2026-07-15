# Normen-Datenbereich

Dieser Ordner verwaltet lokale Normen- und Regelgrundlagen in der
Entwicklungsphase. Er ist ein Daten- und Pruefbestand, kein Python-Modul und
kein freigegebener Rechenkern.

## Zweck

- Lokale, noch nicht freigegebene Normen-Arbeitsstaende strikt von
  versionierter Projektlogik trennen.
- Bereinigte Metadaten, Rechtebelege und spaetere manuelle Review-Verweise
  nachvollziehbar zuordnen.
- Pruefstatus und Review-Arbeit von produktiver Normlogik trennen.
- Spaetere Plaene wie P020 und `ma_analyse.stage_3_standards_compliance`
  mit belastbaren Eingangslisten versorgen.

## Struktur

```text
data/common/normen/
  rounds/
    round1_v0_1/
      incoming/   # Originalpakete der Auswertungsrunde
      extracted/  # entpackte Extraktionsdaten
      review/     # spaetere fachliche Pruefnotizen
  current/         # spaeter bewusst ausgewaehlter Arbeitsstand
  templates/       # spaetere Review- oder Importvorlagen
```

## Regeln

- Inhalte unter `incoming/`, `extracted/` und `review/` bleiben lokal und
  werden nicht versioniert.
- Ablage oder technischer Zugriff ist keine KI- oder Maschinenfreigabe.
  OCR, automatische Extraktion, Zusammenfassung, Uebersetzung, Graphen,
  Embeddings und RAG bleiben nach
  `docs/compliance/din_nautos/processing_limits.yaml` gesperrt, bis der
  konkrete Rechte- und Verarbeitungsumfang belegt ist.
- Formeln, Grenzwerte und Regeln gelten erst nach fachlicher Pruefung als
  implementierbar.
- Produktive Normlogik entsteht spaeter in
  `src/ma_analyse/stage_3_standards_compliance/`.
- Kalender- und Feiertagsdaten liegen getrennt unter `data/common/kalender/`,
  weil sie mehrere Fachbereiche betreffen koennen.
