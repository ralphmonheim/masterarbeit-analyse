# Chat-Handover: SmallOffice-V1-Kapazitaetsstrategie

Datum: 2026-08-11

Status: Entscheidung und SmallOffice-V1-Durchstich umgesetzt; produktiver
Preprocess-Durchlauf weiterhin offen

Lokaler Git-Stand: `73cbd07`; keine Git-Aktion ausgefuehrt

## Fuehrende Referenzen

- [UD-118](../../decisions/USER_DECISIONS_MASTERTHESIS_CODE.md) ist die
  führende Nutzerentscheidung zur Kapazitätsstrategie vor der Dimensionierung.
- [P015](../../plans/inbox/260622_Plan_P015_ma_parameters_Zentrale_Parameter.md),
  [P017](../../plans/inbox/260622_Plan_P017_ma_variants_Naming_Anbindung.md),
  [P018](../../plans/inbox/260622_Plan_P018_ma_simulation_setup_Run_Manifest.md)
  sowie der [Planstatus](../../plans/PLAN_STATUS.md) führen den aktiven
  Umsetzungs- und Migrationsstand.

## Getroffene und umgesetzte Entscheidung

Die Kapazitätsstrategie wird als Studienentscheidung vor der Dimensionierung
gespeichert. Der SmallOffice-V1-Default `ideal_unlimited` bedeutet: Die
wirksame Heiz- und Kühlleistung ist unbegrenzt. Vor einem
Dimensionierungsergebnis wird daher kein Leistungswert behauptet, sondern
`unbegrenzt (Referenzdimensionierung ausstehend)` angezeigt.

Liegt ein zu Variante und Eingabefingerprint passendes Ergebnis der getrennten
Dimensionierung vor, wird dessen Heiz- bzw. Kühllast nur als Referenzwert für
Analyse und Vergleich ausgegeben. Sie ist im idealen Modus keine wirksame
Leistungsgrenze und erzeugt keinen Kapazitäts-Override in der Variante.

Die alternativen Strategien sind klar getrennt:

- `reference_dimensioned`: wirksame Heiz- und Kühlgrenze jeweils 100 Prozent
  der berechneten Referenzleistung;
- `dimensioned_with_factor`: wirksame Grenze aus Referenzleistung mal dem
  jeweiligen Studienfaktor.

Die Studienfaktoren gehören zum gekoppelten Heiz-/Kühl-Kapazitätsfaktor der
SmallOffice-Studie. Sie werden erst nach einem gültigen
Dimensionierungsergebnis materialisiert. Die technischen LoD-1-Startannahmen
sind Herkunftsinformationen, keine Variantengrenzen. Ideale Heiz- und
Kühlübergaben bleiben zonal; die drei technischen Referenzsysteme bezeichnen
zentral Heizung, Kühlung und Lüftung und ersetzen keine reale Produkttechnik.

## Nachweis des implementierten Durchstichs

- `src/ma_variants/small_office_v1.py` speichert die Strategie,
  `dimensioning_status` und die Referenzlasten in den Variantenartefakten.
  Bei `ideal_unlimited` werden die zentralen Felder
  `available_capacity_w` nicht als Variationswerte materialisiert.
- `tests/test_small_office_v1_preprocess.py` prüft für den idealen Referenzfall
  `OPT-SB01-F100`, dass keine Kapazitäts-Overrides enthalten sind, Strategie
  und Dimensionierungsstatus korrekt gespeichert werden und Referenzwerte
  vorhanden sind. `SB01` bezeichnet das Referenz-Sollwertband, `F100` den
  Faktor 1,0.

Dieser Nachweis belegt den SmallOffice-V1-Durchstich, nicht einen produktiven
Projektlauf und nicht die vollständige Migration aller Aufrufer.

## Nächster konkreter Arbeitsschritt

1. Eine konkrete VVER-Auswahl (verbindliche Auswahl der zu bearbeitenden
   Varianten) für den produktiven SmallOffice-Preprocess bereitstellen.
2. Den Preprocess mit dieser Auswahl ausführen und die erzeugten
   Varianten-/Run-Artefakte prüfen.
3. Akzeptanz: Jede Variante enthält eine Strategie, einen nachvollziehbaren
   Dimensionierungsstatus und nur bei gültigem, fingerprintgebundenem Ergebnis
   Referenzwerte; ideale Varianten enthalten keine wirksamen
   Kapazitäts-Overrides.

## Grenzen

- Dieser Handover überträgt keine neue Entscheidung: UD-118 und die genannten
  Pläne enthalten den führenden Stand bereits.
- Es wurde kein produktiver Draft-Run, keine IDA-/EQUA-Verarbeitung und kein
  Simulationsstart durchgeführt.
- Kein Commit, Push, Tag oder Release.
