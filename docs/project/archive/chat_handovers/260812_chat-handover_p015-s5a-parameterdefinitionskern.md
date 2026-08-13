# Chat-Handover: P015-S5A Definitionskern und Parameterinventar

Stand: 2026-08-12

## Kontext und Abgrenzung

`P015` ist der führende Plan für die zentrale Parameterverwaltung in
`ma_parameters`. Der vom Nutzer eingebrachte Plan zur Neustrukturierung der
Eingabeparameter und Parametergruppen ist durch `UD-125` als **Erweiterung
und Konkretisierung von P015** entschieden. Er ersetzt weder die bestehenden
Snapshots und Freigabeverträge noch die Verantwortung der Fachmodule
`ma_building`, `ma_zones`, `ma_technical` und `ma_weather` für ihre
Fachobjekte.

`P015-S5A` ist der erste abgeschlossene Umsetzungsslice dieser Erweiterung.
Er schafft ausschließlich eine additive Definitions- und Inventarbasis; der
vollständige hierarchische Katalog mit neuen Gebäudegruppen, Konstruktionen
und Typ-/Instanzzuordnungen ist damit noch kein implementierter Funktionsumfang.
Es wurden keine IFC-Rohdaten, Normprofile, Produktdaten, Fachwerte,
Variantenlogik oder Benutzeroberflächen ergänzt oder verändert.

## Erledigter Stand

- `ParameterDefinition` beschreibt einen fachlichen Parameter ohne
  Projektwert: Modul, Gruppe, Datentyp/Einheit, LoD-Geltung, erlaubte
  Herkunft und Wertebereich.
- `ParameterGroup` beschreibt eine fachlich zusammengehörige, bei Bedarf
  wiederholbare Objektgruppe. `ParameterInstance` bindet eine Definition an
  einen konkreten Wert und eine Gruppe.
- Die Statusachsen bleiben bewusst getrennt: Herkunft (`user`, `ifc`,
  `catalog`, `derived`, `reference_model`, `weather_dataset`), Editierbarkeit
  (`fixed`, `editable`, `conditional`), Variantenfähigkeit
  (`not_capable`, `capable`, `conditional`), Ableitung (`direct`, `derived`)
  und Aktivierung (`required`, `optional_active`, `optional_inactive`).
  Abgeleitete Parameter sind durch Validierung nicht editier- oder
  variantenfähig; variantenfähige Parameter können nicht `fixed` sein.
- Die versionierte Bestandsmatrix
  `config/ma_parameters/inventory/parameter_inventory_v1.yaml` ordnet die am
  2026-08-12 dokumentierten SmallOffice-LoD-1-Vorschauformen einem Zielmodul,
  einer Zielgruppe und einem Zielparameter zu. `EXISTS` bedeutet bereits als
  Zielinformation vorhanden; `PARTIAL` ein vorhandenes, aber noch grobes oder
  unvollständiges Feld; `MISSING` eine im Zielbild benötigte, derzeit nicht
  beobachtete Eingabe; `METADATA` eine Begleitinformation; `DERIVED` einen
  berechneten statt direkt eingegebenen Wert; `REDUNDANT` ist für doppelte
  Altinformationen vorgesehen. Die Summe der `observed_count`-Felder beträgt
  84. Sie ist ausschließlich ein reproduzierbarer Inventurwert, keine
  Programmgrenze und keine Zielanzahl von Parametern.
- Unverändert kompatibel bleiben die bestehenden Verträge
  `ParameterSnapshot`, `BaselineParameterSnapshot` und
  `ParameterVariationSpecification` einschließlich des Übergabepfads an
  `ma_variants`/P017. Der Definitionskern ist weder Wertquelle noch
  Persistenzmigration.

## Artefakte und Prüfungen

- Implementierung: `src/ma_parameters/definitions.py` und
  `src/ma_parameters/inventory.py`; Re-Exports in
  `src/ma_parameters/__init__.py`.
- Inventar: `config/ma_parameters/inventory/parameter_inventory_v1.yaml`.
- Slice-Tests: `tests/test_ma_parameters_definitions.py`; sie prüfen die
  getrennten Statusachsen, fachlich unzulässige Kombinationen, wiederholbare
  Gruppen sowie die Inventursemantik. Die vorhandenen Snapshot-, Input-Paket-,
  Varianten- und Katalogtests liefen im selben fokussierten Durchlauf mit.
- Am 2026-08-12 lief folgender fokussierter Testumfang mit **63 bestanden**:

  ```powershell
  .\.venv\Scripts\python.exe -m pytest tests/test_ma_parameters_baseline.py tests/test_ma_parameters_catalog_owner_transfer.py tests/test_ma_parameters_definitions.py tests/test_ma_parameters_input_package.py tests/test_ma_parameters_preview.py tests/test_ma_parameters_released_technical_handover.py tests/test_ma_parameters_released_zone_checkpoint.py tests/test_ma_parameters_snapshot.py tests/test_ma_parameters_variation_table.py tests/test_ud106_product_slices.py
  ```

  Zusätzlich waren `ruff check src/ma_parameters tests/test_ma_parameters_definitions.py`
  und `git diff --check` fehlerfrei.
- Dokumentiert wurden S5A in `CHANGELOG.md`, `docs/ma_parameters/README.md`,
  dem P015-Plan, `PLAN_STATUS.md` und `UD-125`. Der lokale semantische
  Navigationsindex wurde nach der Umsetzung aktualisiert und vor Abschluss
  dieses Handovers erneut validiert.

## Führende Quellen und nächster Einstieg

Die verbleibende Arbeit wird nicht in diesem Archiv fortgeschrieben:

- [P015-Plan](../../plans/inbox/260622_Plan_P015_ma_parameters_Zentrale_Parameter.md)
  führt den fachlichen Gesamtumfang. Sein nächster, klar abgegrenzter
  Katalogslice ist **P015-S5B**: Gebäudeparametergruppen, Konstruktionen,
  Typ-/Instanzbeziehungen und LoD-1-/LoD-2-Sperrregeln.
- [Planstatus](../../plans/PLAN_STATUS.md) enthält den konsolidierten
  Projektstand und die parallele, unabhängige Restarbeit zur v2-basierten
  Werteherkunft sowie zum P015-S3b-Vollumfang.
- [UD-125](../../decisions/USER_DECISIONS_MASTERTHESIS_CODE.md) ist die
  führende Entscheidung für die Erweiterung und ihre Kompatibilitätsgrenze.

P015-S5B beginnt erst mit einer **neuen ausdrücklichen Freigabe zur
Umsetzung** durch den Projektverantwortlichen. Der Eintrittsscope ist dann
gegen P015 und UD-125 zu prüfen; vorab sind keine neuen Parameterwerte aus
den noch nicht aufgebauten Gruppen zu erfinden.

## Arbeitsbaumgrenze

S5A gehört ausschließlich zu den oben genannten neuen
`ma_parameters`-/Inventarartefakten und den genannten Dokumentationsanteilen.
Im Arbeitsbaum bestehen daneben unabhängige Änderungen, unter anderem in
`ma_building`, `ma_ui` und anderen Planungsdateien. Sie sind nicht Teil dieses
Slices und dürfen bei einer späteren Übernahme oder einem Commit nicht
verworfen werden. Dieser Handover selbst wurde nicht committed, gepusht oder
veröffentlicht.
