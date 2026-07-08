# Normen-Datenbereich

Dieser Ordner verwaltet lokale Normen- und Regelgrundlagen in der
Entwicklungsphase. Er ist ein Daten- und Pruefbestand, kein Python-Modul und
kein freigegebener Rechenkern.

## Zweck

- ChatGPT-Auswertungen und automatische Extraktionen nachvollziehbar ablegen.
- Normenregister, Formelkandidaten, Symbolabschnitte und Beziehungen sammeln.
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
- Formeln, Grenzwerte und Regeln gelten erst nach fachlicher Pruefung als
  implementierbar.
- Produktive Normlogik entsteht spaeter in
  `src/ma_analyse/stage_3_standards_compliance/`.
- Kalender- und Feiertagsdaten liegen getrennt unter `data/common/kalender/`,
  weil sie mehrere Fachbereiche betreffen koennen.
