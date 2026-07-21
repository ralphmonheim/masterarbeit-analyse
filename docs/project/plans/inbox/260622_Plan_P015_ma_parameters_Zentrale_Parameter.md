# P015 ma_parameters Zentrale Parameter

Stand: 2026-07-15
Status: Fachlich konsolidiert; P015-S1, P015-S2, P015-S3a, P015-S3b-prep und P013-S3c/P015-S3b-T2-Releasecheckpoint umgesetzt; v2-Werteherkunft und Restumfang von P015-S3b offen
Prioritaet: Hoch
Abhaengigkeiten: P008, P010, P012, P013, P014, P016, P017, P027

## Ziel

`ma_parameters` fuehrt freigegebene Eingaben aus Wetter, Gebaeude, Technik und
Zonen zu einem versionierten Baseline-Stand zusammen und stellt danach die
fachlich erlaubten Variationen fuer `ma_variants` bereit.

Das Modul trennt drei Rollen sauber:

- Baseline: freigegebener Ausgangszustand.
- Stage-1-Ergebnisse: Dimensionierungsergebnisse und Vorschlaege, die die
  Baseline nicht still veraendern.
- Variation: explizite Spezifikation, welche Werte, Objekte und Referenzen
  in einer Variantenstudie veraendert werden duerfen.

## Ausgangslage

P015-S1, P015-S2, P015-S3a, P015-S3b-prep und P013-S3c/P015-S3b-T2 sind
umgesetzt. `ma_parameters` enthaelt `ParameterSnapshot`, `ParameterValue`
und `ParameterSourceReference`, baut einen validierten
BusinessIntegration-LoD-1-`ParameterSnapshot` v1 aus `ma_building`,
`ma_zones` und `ma_technical` und leitet daraus einen ersten
`BaselineParameterSnapshot` v2 ab. Dieser Baseline-Stand fuehrt
`parameter_value_id`, Scopes, Parameterklassen, Variierbarkeit, erweiterte
Quellenreferenzen, Referenzversionen, `content_hash`, `release_status` und
`freshness_status` ein. P015-S3a ergaenzt ein `ParameterInputPackage` als
Eingabecheckpoint und uebernimmt Wetterdaten nur ueber den aktivierten,
freigegebenen Projekt-Default aus `ma_weather`. Der getrennte Releasecheckpoint
uebernimmt ein passendes P013-/P014-Paar ohne bestehende Wertquellen zu
veraendern. Streamlit zeigt Snapshot v1, Eingangspaket und Baseline v2
weiterhin getrennt.

Noch offen sind insbesondere:

- vollstaendige Wetterdaten-Persistenz und Freshness-Abgleich nach Dateiaenderung.
- vollstaendiger P013-S2-Zonenlebenszyklus mit Aenderungsstatus jenseits des
  umgesetzten referenz-only Checkpoints.
- Persistenz, Versionierung und Aktualitaetsstatus.
- Stage-1-Ergebnis als Folgesnapshot oder dokumentierter Vorschlag.
- allgemeines Variationsmodell und Uebergabe an `ma_variants`.
- Migration bestehender Parameter- und Optionslogik aus `ma_variants`.

## Verbindlicher Zielworkflow

```text
ma_weather
ma_building
ma_technical
ma_zones
    -> ma_validation Eingabecheckpoint
    -> ma_parameters Teil 1: BaselineParameterSnapshot
    -> ma_validation Parametercheckpoint
    -> ma_analyse.stage_1_dimensioning
    -> ReferenceDimensioningResult
    -> StudyMode waehlen
    -> ma_parameters Teil 2: ParameterVariationSpecification
    -> ma_validation Variation-Checkpoint
    -> ma_variants
    -> ma_simulation_setup
```

`baseline_only` fuehrt die freigegebene Baseline ohne aktive Variation weiter.
`variant_study` benoetigt mindestens eine aktive Variationsdimension und eine
freigegebene `ParameterVariationSpecification`.

## Fachliche Hauptobjekte

### BaselineParameterSnapshot

Der Snapshot beschreibt den vollstaendig aufgeloesten Ausgangszustand. Er
enthaelt mindestens:

- `snapshot_id`, `project_id`, `building_id`
- `parameter_values`
- `source_references`
- `reference_versions`
- `content_hash`
- `release_status`
- `freshness_status`

Die Baseline wird von `ma_variants` nicht veraendert. Aenderungen in Wetter,
Gebaeude, Technik oder Zonen erzeugen einen neuen Stand oder markieren den
bisherigen Stand als veraltet.

### ReferenceDimensioningResult

Stage 1 erzeugt den Referenz-Dimensionierungsstand zur Baseline. Typische
Inhalte sind:

- `dimensioning_result_id`
- Heizlast, Kuehllastannahme, Luftvolumenstrom und weitere Stage-1-Werte
- Rechenweg, Hinweise und Status
- Bezug auf den verwendeten `BaselineParameterSnapshot`

Diese Ergebnisse sind keine stillen Baseline-Aenderungen. Sie koennen in
`ma_parameters` als Ergebnisparameter, Vorschlagswerte oder Referenzen fuer
Variationen verwendet werden.

### ParameterVariationSpecification

Die Spezifikation definiert den erlaubten Variationsraum fuer einen StudyCase:

- aktive Parameter
- Werteformen oder Optionslisten
- Scope und Zielobjekte
- Kopplung mehrerer Zielobjekte
- Dimensionierungsrelevanz
- Referenzstrategien
- technische Kurzkennungen fuer Kataloganzeigen

`ma_parameters` beschreibt den Raum. `ma_variants` erzeugt daraus Candidates,
Kataloge, Selections und vollstaendige Varianten.

## Parameterklassen

| Klasse | Bedeutung |
|---|---|
| `primary_direct` | direkt aus einem Eingabemodul uebernommen |
| `primary_reference` | stabile Referenz auf ein Fachobjekt oder eine Option |
| `primary_derived` | aus freigegebenen Primaerwerten abgeleitet |
| `secondary` | Hilfs- oder Komfortwert ohne eigene fachliche Fuehrungsrolle |
| `variation` | explizit variierbarer Wert oder Optionsbezug |
| `derived_variant_value` | erst bei Variantenaufloesung berechneter Wert |
| `result_parameter` | Ergebnis aus Stage 1, Simulation oder Auswertung |

Relative Faktoren werden intern dimensionslos gespeichert. Die Anzeige darf
Prozentwerte verwenden, muss aber eindeutig zwischen `0.8`, `80 %` und
`-20 %` unterscheiden.

## Scope und Identitaet

P015-S2 fuehrt eine stabilere Parameteridentitaet ein:

- `parameter_value_id` fuer jeden konkreten Wert.
- Eindeutigkeit ueber `parameter_key + scope_type + scope_id`.
- Scope-Typen mindestens `project`, `building`, `zone_group`, `zone` und
  `technical_system`.
- komplexe Fachobjekte werden ueber `reference_id`, `reference_version` und
  `content_hash` referenziert.

Zielobjekte koennen einzeln, gekoppelt oder als Objektgruppe angesprochen
werden. Fuer den ersten produktiven Umfang gelten:

- `single_object`
- `selected_objects_linked`
- `object_group`
- `selected_objects_independent`

Die Kopplung ist entweder `linked` oder `independent`. Bei `linked` erhalten
mehrere Zielobjekte dieselbe Option. Bei `independent` entstehen getrennte
Variationsdimensionen.

## Gebaeudedetailmodus

`ma_parameters` unterscheidet mindestens:

- `simplified`: kompakte LoD-1/LoD-2-Werte fuer fruehe Planung und
  robuste Demo-/Masterarbeitsablaeufe.
- `complete`: detailliertere Raum-, Bauteil-, Oeffnungs- und Systemwerte,
  sobald die vorgelagerten Fachmodule sie belastbar bereitstellen.

Ein Detailstufenwechsel darf keine vorhandenen freigegebenen Staende
ueberschreiben. Er erzeugt einen neuen Snapshot oder eine neue
Variationsspezifikation.

## Allgemeines Variationsmodell

Unterstuetzte Werteformen:

- `none`: nicht variabel.
- `single_value`: ein gesetzter Wert.
- `range`: `min`, `max`, `step`, Einheit und Grenzlogik.
- `explicit_list` oder `discrete_values`: explizite Werteliste.
- `coupled_option`: gekoppelte Werte, zum Beispiel Heiz- und Kuehlsollwert.
- `reference_option` oder `reference_values`: stabile Referenzen auf
  komplexe Optionen.

Variierbarkeit wird getrennt beschrieben:

- `not_variable`
- `direct_variable`
- `reference_variable`
- `factor_variable`
- `structural_variable`

Jede Variation kennzeichnet, ob sie `dimensioning_relevant` ist. Fuer solche
Werte muss definiert werden, welche Eingaben den
`dimensioning_input_fingerprint` bilden.

## Referenzstrategien

Fuer leistungs- und dimensionierungsbezogene Werte sind zwei Strategien
vorgesehen:

- `variant_specific`: Randbedingungen aendern, erforderliche Last neu
  berechnen, Faktor auf die neue Last anwenden.
- `fixed_reference`: erforderliche Last darf neu berechnet werden, die
  verfuegbare oder installierte Leistung bleibt auf einem festen Referenzstand.

Die UI muss diese Strategien spaeter klar erklaeren. `fixed_reference` darf
nicht als automatische Neudimensionierung missverstanden werden.

## Abhaengigkeiten und Regeln

`ma_parameters` darf allgemeine Parameterabhaengigkeiten pruefen:

- `filters_options`
- `derives_value`
- `requires_parameter`
- `excludes_parameter`

Die Grenze zu `ma_variants` bleibt klar:

- `ma_parameters` validiert die fachliche Verwendbarkeit von Parametern,
  Scopes, Zielobjekten und Variationseinstellungen.
- `ma_variants` erzeugt Kombinationen, wendet Variantenregeln an, erkennt
  Duplikate und verwaltet Katalog, Selection und VariantGeneration.

## Uebergabevertrag an ma_variants

Die Uebergabe besteht fachlich aus:

```text
BaselineParameterSnapshot
ReferenceDimensioningResult
ParameterVariationSpecification
AppliedRuleSet oder RuleSet-Referenz
project_id
study_direction_id
study_case_id
input_fingerprint
release_status
```

Nicht Bestandteil von `ma_parameters`:

- Candidate-Erzeugung
- RuleEvaluation auf Variantenkombinationen
- VariantCatalog
- VariantSelection
- vollstaendige VariantGeneration
- Simulationssetup

## Validierung, Status und Aktualitaet

Checkpoints:

- Eingabecheckpoint nach `ma_weather`, `ma_building`, `ma_technical` und
  `ma_zones`.
- Parameter-/Baseline-Checkpoint.
- Variation-Checkpoint vor `ma_variants`.

Freigabestatus:

- `draft`
- `validation_required`
- `review_required`
- `released`
- `blocked`
- `archived`

Aktualitaetsstatus:

- `current`
- `outdated`
- `unknown`

Fehler blockieren die Weitergabe. Warnungen benoetigen eine bewusste
Freigabeentscheidung. Aenderungen an Quellen, P013-S2-Zonenstand,
Techniksystemen, Wetterdaten oder Stage-1-Referenzen koennen einen Snapshot
oder eine VariationSpec als `outdated` markieren.

## Persistenz

Lokale projektbezogene Speicherung ist vorgesehen unter:

```text
data/ma_parameters/snapshots/
data/ma_parameters/variation_specifications/
data/ma_parameters/validation_reports/
data/ma_parameters/comparisons/
data/ma_parameters/exports/
```

Versionierte Vorlagen und allgemeine Definitionen bleiben unter `config/` oder
in fachlich geeigneten Modulkatalogen. Grosse, echte oder noch ungepruefte
Daten werden nicht automatisch ins Git-Repo uebernommen.

## Interne Zielstruktur

Der bestehende einfache Kern bleibt kompatibel. Spaetere Dateien koennen sein:

- `models.py`
- `definitions.py`
- `collection.py`
- `normalization.py`
- `snapshots.py`
- `dimensioning.py`
- `variations.py`
- `resolution.py`
- `dependencies.py`
- `validation.py`
- `freshness.py`
- `persistence.py`
- `comparisons.py`
- `previews.py`
- `services.py`

Diese Struktur ist ein Zielbild, kein Auftrag fuer eine sofortige
Dateiaufspaltung ohne konkreten Slice.

## Umsetzungsslices

### P015-S1 ParameterSnapshot v1

Umgesetzt. BusinessIntegration-LoD-1 erzeugt einen validierten Snapshot aus
`ma_building`, `ma_zones` und `ma_technical`.

### P015-S2 Datenmodell v2 und Scopes

Umgesetzt. Schwerpunkt:

- `parameter_value_id`
- Eindeutigkeit ueber Key und Scope
- Parameterklasse, Herkunft und Variierbarkeit
- Gebaeudedetailmodus
- erweiterte Quellenreferenzen
- Migrationstests ohne Bruch des v1-Snapshots

Der erste produktive Umfang erzeugt den Baseline-v2-Stand additiv aus dem
BusinessIntegration-LoD-1-`ParameterSnapshot` v1. Wetterdaten,
P013-S2-Zonenfingerprints, Persistenz und VariationSpecification bleiben
Folgeslices.

### P015-S3 Vollstaendiges Eingangspaket

Teilweise umgesetzt als P015-S3a:

- `ParameterInputPackage` als separater Eingangspaketvertrag.
- Uebernahme des aktivierten Projekt-Defaults aus `ma_weather` mit
  `weather_key`, Standort, Jahrtyp, Datensatzrolle, Import-/Quellenreferenz
  und Freigabestatus.
- Validierung blockiert fehlendes Wetter, nicht aktivierte Wetterquellen und
  nicht freigegebene Wetterstaende.
- Baseline-v2 kann additiv aus dem Eingangspaket erzeugt werden, ohne den
  bestehenden `ParameterSnapshot` v1 zu brechen.

Weiter offen fuer P015-S3b sind die v2-basierte Herkunft vorhandener
Parameterwerte, ein vollstaendiger Eingabecheckpoint ueber alle
Quellenfingerprints und der breitere P013-S2-Zonenstatus jenseits des
umgesetzten referenz-only Fingerprints.

#### P015-S3b-prep: ReleasedTechnicalHandover

Council-Beschluss vom 2026-07-15: Der erste Teil bleibt bewusst auf die
reine P014-Metadatenuebergabe begrenzt. `ma_parameters` erhaelt eine additive
Konvertierung eines freigegebenen technischen Handovers in eine
`ParameterSourceReference`; bestehende v1-Snapshots, ihre Werte und das
P015-S3a-Eingangspaket werden nicht umgeschrieben.

Damit ist noch kein Vollabschluss von P015-S3b behauptet: Der eigene
P013-Zonenfingerprint, die v2-basierte Herkunft der Parameterwerte und der
vollstaendige Eingabecheckpoint bleiben nachfolgende, getrennt abzugrenzende
Schritte.

Umgesetzt am 2026-07-15: Der Konverter uebernimmt nur Modell-ID,
Revisions-ID, Content-Hash und Freigabestatus aus dem P014-Handover. Er
laesst Werte, bestehende Snapshot-Quellen-IDs und das P015-S3a-Eingangspaket
unveraendert.

#### P013-S3c / P015-S3b-T2 ReleasedZoneCheckpoint

Council-Beschluss vom 2026-07-15: Das Eingangspaket und die daraus gebaute
Baseline erhalten additiv getrennte `checkpoint_references` fuer den
freigegebenen P013- und P014-Handover. Sie sind keine Wertquellen:
`source_references` und alle `ParameterValue.source_reference_id` bleiben
fuer v1 unveraendert.

- Der opt-in-Checkpoint fordert genau ein zueinander passendes, freigegebenes
  und aktuelles P013-/P014-Paar. Fehlende, veraltete, unbekannte oder
  triple-inkonsistente Referenzen blockieren nur den neuen Checkpointmodus.
- Der bestehende Baseline-Content-Hash bindet die getrennten Checkpoint-
  Referenzen ein; das nicht persistierte Eingangspaket bleibt ohne neuen
  Package-Level-Hash. Die Baseline uebernimmt die Referenzen ohne sie als
  Werteherkunft zu deklarieren.
- Nicht Teil sind die v2-Herkunft vorhandener Parameterwerte, UI, Persistenz,
  YAML-/Katalogdaten, P032-W2 und die vollstaendige Behauptung eines
  abgeschlossenen P015-S3b.

Umgesetzt am 2026-07-15: Der explizite Factory-Pfad nimmt die urspruenglichen
P013-/P014-Handover an, prueft Projekt, Gebaeude und das technische Triple und
fuegt genau zwei getrennte `checkpoint_references` hinzu. Sie aendern weder
`source_references` noch `ParameterValue.source_reference_id`; die Baseline
uebernimmt sie und bindet ihre Content-Hashes in ihren bestehenden Hash ein.
Generische Paket- und Baseline-Validierung blockieren fehlende, doppelte,
nicht freigegebene oder nicht aktuelle Checkpoints, auch wenn ein befuelltes
Checkpointfeld nicht den strengen Paarmodus anfordert.

Abschlussnachweis: Der gemeinsame Fokuslauf fuer Zonen-, Parameter-,
Technik-, Workflow- und Architekturcontracts bestand mit `75 passed`; die
vollstaendige lokale Suite bestand mit `536 passed`. Der genaue Auditnachweis
inklusive Ruff- und Diff-Pruefung ist in Entscheidung 34 festgehalten.

### Preprocess V1-Mindestumfang

Preprocess V1 verwendet den umgesetzten freigegebenen P013-/P014-
Releasecheckpoint als getrennte, fingerprintbare Referenz. Damit ist
P015-S3b nicht vollstaendig abgeschlossen: insbesondere die v2-Herkunft der
bestehenden Parameterwerte, Persistenz und der breite Zonenstatus bleiben
Folgeslices. Der Checkpointmodus blockiert fehlende, nicht freigegebene oder
veraltete Referenzen.

Aus P015-S4 ist fuer V1 nur die lokale, unveraenderliche Ablage von
Eingangspaket und Baseline mit `current/outdated`-Pruefung erforderlich.
Die breite Migration alter Variantenkataloge und komplexe
Abhaengigkeitsregeln bleiben Folgeslices.

### P015-S4 Persistenz, Versionierung und Aktualitaet

Lokale Speicherung, `content_hash`, Quellenfingerprint, `current/outdated` und
Aenderungsnachweise.

### P015-S5 Parameterdefinitionen und Migration aus ma_variants

Inventar der bestehenden Parameter-, Options- und Kataloglogik aus
`ma_variants`; kontrollierte Migration ohne harte Importbrueche.

### P015-S6 Stage-1-Einbindung

`ReferenceDimensioningResult` als Ergebnisparameter, Vorschlag oder
Referenzwert anbinden. Keine stille Veraenderung der Baseline.

### P015-S7 Allgemeines Variationsmodell

Range, explizite Listen, gekoppelte Optionen, Referenzoptionen,
relative Faktoren und technische Kurzkennungen.

### P015-S8 Zielobjekte, Kopplung und Abhaengigkeiten

Scopes, Objektgruppen, gekoppelte und unabhaengige Zielobjekte sowie einfache
Abhaengigkeitsregeln.

### P015-S9 VariationSpecification und Uebergabe an ma_variants

Freigegebene `ParameterVariationSpecification` inklusive Handover-Vertrag an
P017.

Fuer Preprocess V1 reicht eine kleine, explizite VariationSpecification mit
ein bis drei Variationsdimensionen. Sie liefert keine technischen Regeln oder
Produktkataloge und veraendert die Baseline nicht.

### P015-S10 Fachmasken und Workflow-Integration

UI fuer Baseline, Stage-1-Vorschlaege, Variationen, Status, Warnungen,
Freigaben und Ruecksprungziele.

## Testkonzept

- Modelltests fuer Parameteridentitaet, Scope und Quellenreferenzen.
- Range- und Resolutionstests fuer Werteformen und Einheiten.
- Abhaengigkeitstests fuer `requires`, `excludes`, `derives` und `filters`.
- Freshness- und Hash-Tests.
- Persistenztests fuer Snapshots und VariationSpecs.
- Integrationstests bis zur P017-Uebergabe.
- Regressionstests fuer den vorhandenen P015-S1-Snapshot.

## Offene Punkte

- genaue Grenze zwischen softwareweiten Parameterdefinitionen und
  projektspezifischen Optionen.
- finale Persistenzformate fuer komplexe Fachobjekte.
- UI-Verhalten bei gleichzeitig veralteter Baseline und vorhandener
  VariationSpec.
- Umgang mit Nachhaltigkeits- und Wirtschaftlichkeitsparametern als Eingabe,
  Ergebnis oder Bewertungsreferenz.

## Definition of Done fuer P015

P015 ist fachlich abgeschlossen, wenn:

- alle freigegebenen Eingabemodule in einen versionierten Baseline-Snapshot
  einfliessen koennen.
- Stage-1-Ergebnisse nachvollziehbar referenziert, aber nicht still in die
  Baseline geschrieben werden.
- Variationsraeume mit Scope, Zielobjekt, Werteform und
  Dimensionierungsrelevanz beschrieben werden koennen.
- der Handover an `ma_variants` validiert, versioniert und reproduzierbar ist.
- veraltete Quellenstaende die Variantenbildung blockieren oder bewusst zur
  Freigabe bringen.

## Naechster Schritt

Die v2-basierte Werteherkunft und den verbleibenden P015-S3b-Vollumfang nach
dem umgesetzten P013-/P014-Releasecheckpoint getrennt abgrenzen.

## Handover-Ergaenzung 2026-07-21

Die Handover aus `ma_variants` und `ma_technical` bestaetigen und
konkretisieren den aktiven P015-Vertrag:

- Die zwei getrennten Artefakte `BaselineParameterSnapshot` und
  `ParameterVariationSpecification` bleiben die einzigen Eingaben an
  `ma_variants`; Candidate-Erzeugung, Regeln, Katalog und Selection gehoeren
  nicht zu P015.
- Technische Parameter werden mit stabilem Pfad, Zielobjekt, Datentyp,
  Einheit, Wert, erlaubten Werten, Variierbarkeit, Grenzen und Quelle
  beschrieben. Eine neue Technikrevision erzeugt einen neuen Snapshot oder
  Zweig und ueberschreibt keinen historischen Stand.
- Ein von `ma_analyse` abgeleiteter `StudyDirectionProposal` bleibt
  nicht-ausfuehrbar, bis eine Nutzerfreigabe ihn in eine
  `ParameterVariationSpecification` ueberfuehrt.
- Kurzkennungen dienen nur der Anzeige; fachliche Identitaet bleibt durch
  stabile Referenzen, Versionen und Content-Hashes gesichert.

Die P015-Quelle vom 2026-07-09 bleibt eine historische Referenz und ersetzt
nicht die in diesem Plan dokumentierten, juengeren Checkpoint-Entscheidungen.
