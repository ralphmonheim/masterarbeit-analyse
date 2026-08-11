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

Der fruehere Kurzname `stage_3_verification` bleibt als neutraler
Kompatibilitaetsalias. Rechtliche Pruefbegriffe sind kein Bestandteil dieses
Fachmoduls.

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

## Umsetzungsstand 2026-08-11: wertfreie Nachweisbereitschaft

- `VerificationReadinessItem` beschreibt Kriterium, Regelwerk, Ausgabe,
  erforderliche Daten, Methoden-, Rechte- und Teststatus sowie das naechste
  Gate.
- DIN/TS 18599-10 wird ausschliesslich aus den vorhandenen 43
  Profil-Metadatensaetzen als `schema_ready_values_not_released` gefuehrt.
- Das vorhandene DIN-4108-2-Legacy-Feld ist nur ein
  `data_field_candidate_rule_not_defined`; die fruehere leere Excel-Spalte
  wurde aus der normalen Kennwerttabelle entfernt.
- Beide Kandidaten bleiben `NOT_EVALUABLE`. `ma_validation` prueft spaeter
  Daten-/Vertragsbereitschaft; die fachliche Regel und Berechnung bleibt beim
  Stage-3-Owner.

## Metadatenanalyse der vorhandenen Normquellen 2026-08-11

Die Analyse verwendet ausschliesslich den versionierten Locator
`data/common/normen/source_inventory_metadata.yaml`, den wertfreien
Zonenprofilvertrag und eigene Profilmetadaten. Norm-PDFs und geschuetzte
Inhalte wurden nicht geoeffnet.

- `DIN/TS 18599-10` ist wegen der 43 vorhandenen Profilidentitaeten und des
  wertfreien Zielschemas `schema_ready`; Profilwerte und Regeln sind nicht
  freigegeben.
- `DIN 4108-2` ist nur `data_field_candidate`, weil der Legacy-Bericht eine
  unberechnete Gradstunden-Spalte kannte. Ausgabe, Methode und Kriterien sind
  nicht fachlich bestaetigt.
- Die uebrigen katalogisierten DIN-, DIN-EN-, DIN-EN-ISO-, VDI-, GEG-, HBO-
  und HOAI-Gruppen bleiben `inventory_only`. Aus Dateinamen wird weder
  fachliche Eignung noch Aktualitaet oder Anwendbarkeit abgeleitet.
- Vor jeder Aktivierung sind exaktes Dokument und Ausgabe, Herkunfts- und
  Maschinenverarbeitungsrecht, manuell dokumentierte Fundstelle,
  qualifizierter Fachreview, Einheit und Geltungsbereich, eigener begrenzter
  Regeltext, reproduzierbarer Test und menschliche Bestaetigung erforderlich.
