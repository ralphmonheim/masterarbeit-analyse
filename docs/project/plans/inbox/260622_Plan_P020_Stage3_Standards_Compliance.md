# P020 Analyse Stufe 3 Norm-Nachweis

Stand: 2026-07-24
Status: Fachlicher Research-Plan
Prioritaet: Hoch
Abhaengigkeiten: P019, P027

## Ziel

Analyse Stufe 3 prueft Gebaeude und technische Systeme gegen fachlich
vorbereitete Normvorlagen. Der Nachweis bewertet Modellannahmen, Eingaben,
Einheiten, Randbedingungen und Ergebnisse; er ist keine Rechte- oder
Freigabepruefung.

## Kanonischer Name

`ma_analyse.stage_3_standards_verification`

Die bisherigen Namen `stage_3_verification` und
`stage_3_standards_compliance` bleiben nur Kompatibilitaetsaliase.

## Geplanter Umfang

1. Deutsche Normvorlagen und die jeweils verwendeten Ausgaben fachlich ordnen.
2. Nachweisprofile fuer Gebaeude, Zonen und Technik als nachvollziehbare
   Eingabe- und Ergebnisstruktur festlegen.
3. `NormVerificationReport` mit `pass`, `fail`, `warning` und
   `not_evaluable` modellieren.
4. Einheiten, Randbedingungen, Annahmen und Tests je Regel dokumentieren.
5. Den bereinigten Metadatenindex und das Zonenprofil-Geruest unter
   `data/common/normen/` nur als Planungsgrundlage verwenden.

## Grenzen

Der aktuelle Stand enthaelt keine produktiven Normregeln. Formeln,
Grenzwerte und Nachweisregeln werden erst mit ihrem fachlichen Testfall
implementiert.
