# Datenmodell

Stand: 2026-06-03

Dieses Dokument beschreibt das Datenmodell auf konzeptioneller Ebene, die implementierten Python-Modelle und die erste vorbereitete Datenbankstruktur.

## Grundsaetze

- Fachliche Namen und Anzeigenamen werden nicht als technische Verknuepfung verwendet.
- Jedes zentrale Objekt erhaelt spaeter einen stabilen technischen Key.
- PostgreSQL ist als zentrale Zieldatenbank vorgesehen.
- SQLAlchemy und Alembic bilden die vorbereitete Datenbankschicht.
- Das bestehende Analyseprojekt `ma_analyse` bleibt von diesem Datenmodell zunaechst getrennt.

## Implementierte Python-Struktur

Die ersten Modelle liegen im neuen Paket `ma_variants`:

```text
src/ma_variants/
  parameter_catalog/
  option_catalog/
  variant_manager/
  system_catalog/
  economic_analysis/
  product_catalog/
  material_catalog/
  document_catalog/
  source_catalog/
  database/
  validation/
```

Die Modelle sind als `dataclasses` umgesetzt. Sie nutzen technische Keys und pruefen einfache Pflichtfelder direkt bei der Instanziierung.

## Beispielkonfigurationen

Abschnitt 2 fuehrt kleine YAML-Konfigurationen als erste Importquelle ein:

```text
config/parameters/example_parameters.yaml
config/options/example_options.yaml
```

Die Parameterdatei enthaelt eine Liste `parameters`. Jeder Eintrag bildet direkt die Felder des Modells `Parameter` ab.

Die Optionsdatei enthaelt eine Liste `option_sets`. Jede Optionsgruppe enthaelt die Felder des Modells `OptionSet` sowie eine nicht leere Liste `values`. Jeder Wert in `values` bildet die Felder des Modells `OptionValue` ab; `option_set_key` wird dabei aus der umgebenden Optionsgruppe uebernommen.

Der Importbericht wird als JSON geschrieben und enthaelt Status, Quelldateien, Objektzaehler und Validierungsfehler.

Abschnitt 11 fuehrt kleine Beispielkataloge ein:

```text
config/products/example_products.yaml
config/materials/example_materials.yaml
config/documents/example_documents.yaml
config/sources/example_sources.yaml
```

Produkt- und Materialimporte unterstuetzen YAML, JSON und einfache CSV-Dateien. Dokument- und Quellenimporte sind als YAML-/JSON-Importe vorbereitet.

Dokumente und Datenblaetter werden nur ueber Pfade referenziert. Die vorbereitete Ordnerstruktur liegt unter:

```text
data/documents/products/
data/documents/materials/
```

## Kernobjekte

### Parameter

Beschreibt eine veraenderbare fachliche Groesse, zum Beispiel Heizleistungsfaktor, Raumtyp, Systemauspraegung oder Regelstrategie.

Implementiert als `ma_variants.parameter_catalog.Parameter`.

Felder:

- `parameter_key`
- `display_name`
- `category`
- `parameter_class`
- `option_set_key`
- `unit`
- `is_variant_relevant`
- `is_naming_relevant`
- `is_export_relevant`

### Optionsgruppe

Buendelt moegliche Auspraegungen fuer einen Parameter.

Implementiert als `ma_variants.option_catalog.OptionSet`.

Felder:

- `option_set_key`
- `display_name`
- `description`

### Optionswert

Beschreibt einen konkret waehlbaren Wert innerhalb einer Optionsgruppe.

Implementiert als `ma_variants.option_catalog.OptionValue`.

Felder:

- `option_key`
- `option_set_key`
- `label`
- `value`
- `unit`
- `is_active`

### Variante

Beschreibt eine konkrete Kombination ausgewaehlter Optionswerte.

Implementiert als `ma_variants.variant_manager.Variant`.

Felder:

- `variant_key`
- `variant_name`
- `status`

### Variantenwert

Verknuepft eine Variante mit einem Parameter und einem gewaehleten Optionswert oder Rohwert.

Implementiert als `ma_variants.variant_manager.VariantValue`.

Felder:

- `variant_key`
- `parameter_key`
- `option_key`
- `resolved_value`

### Systemtemplate

Beschreibt eine wiederverwendbare technische Systemvorlage, zum Beispiel eine Waermepumpe, ein Kuehlsystem, eine PV-Anlage oder eine Lueftungsvorlage.

Implementiert als `ma_variants.system_catalog.SystemTemplate`.

Felder:

- `system_template_key`
- `display_name`
- `system_type`
- `description`
- `is_active`

### Systemtemplate-Wert

Beschreibt einen konkreten Parameterwert, der aus einer Systemvorlage aufgeloest wird.

Implementiert als `ma_variants.system_catalog.SystemTemplateValue`.

Felder:

- `system_template_key`
- `parameter_key`
- `value`
- `unit`
- `value_source`

### Abhaengigkeitsregel

Beschreibt eine einfache Template-zu-Template-Abhaengigkeit. In Abschnitt 7 wird nur geprueft, ob ein Template ein weiteres Template voraussetzt.

Implementiert als `ma_variants.system_catalog.DependencyRule`.

Felder:

- `rule_key`
- `system_template_key`
- `required_system_template_key`
- `description`
- `is_active`

### Generische Systemkosten

Beschreibt eine einfache Kostenannahme je technischem Systemtyp.

Implementiert als `ma_variants.economic_analysis.GenericSystemCost`.

Felder:

- `system_type`
- `display_name`
- `investment_cost_eur`
- `maintenance_cost_eur_per_year`
- `lifetime_years`
- `is_example_value`

### Energiepreis

Beschreibt eine generische Energiepreisannahme.

Implementiert als `ma_variants.economic_analysis.EnergyPrice`.

Felder:

- `energy_carrier`
- `price_eur_per_kwh`
- `is_example_value`

### Wirtschaftlichkeitsszenario

Beschreibt Betrachtungszeitraum, Energiepreisreferenzen und Fallback-Energiebedarfe.

Implementiert als `ma_variants.economic_analysis.EconomicScenario`.

Felder:

- `scenario_key`
- `display_name`
- `observation_period_years`
- `heating_energy_carrier`
- `cooling_energy_carrier`
- `default_heating_energy_kwh_per_year`
- `default_cooling_energy_kwh_per_year`
- `is_example_value`

### Varianten-Kostenergebnis

Beschreibt das Ergebnis einer generischen Wirtschaftlichkeitsbewertung je Variante und Szenario.

Implementiert als `ma_variants.economic_analysis.VariantCostResult`.

Felder:

- `variant_key`
- `variant_name`
- `scenario_key`
- `selected_system_types`
- `investment_cost_eur`
- `maintenance_cost_eur_per_year`
- `maintenance_cost_total_eur`
- `energy_cost_eur_per_year`
- `energy_cost_total_eur`
- `replacement_cost_eur`
- `total_cost_eur`
- `observation_period_years`
- `heating_energy_kwh_per_year`
- `cooling_energy_kwh_per_year`
- `uses_simulation_results`
- `uses_example_energy_values`
- `assumption_notes`

### Produkt

Beschreibt ein Produkt fuer spaetere detaillierte Bewertungen ausgewaehlter Varianten. Abschnitt 11 nutzt nur kleine Beispielwerte und fuehrt keine automatische Produktrecherche durch.

Implementiert als `ma_variants.product_catalog.Product`.

Felder:

- `product_key`
- `product_type`
- `manufacturer`
- `product_name`
- `nominal_power`
- `price`
- `currency`
- `gwp_value`
- `gwp_unit`
- `product_url`
- `document_path`
- `source`
- `data_quality`

### Produkteigenschaft

Beschreibt flexible Detailwerte, ohne die Produkttabelle fuer jeden spaeteren Fachwert zu erweitern.

Implementiert als `ma_variants.product_catalog.ProductProperty`.

Felder:

- `product_key`
- `property_key`
- `value`
- `unit`
- `source`
- `data_quality`

### Material

Beschreibt ein Material fuer spaetere Bauteil-, Kosten- und Umweltbewertungen.

Implementiert als `ma_variants.material_catalog.Material`.

Felder:

- `material_key`
- `material_group`
- `material_name`
- `density`
- `lambda_value`
- `specific_heat_capacity`
- `price`
- `gwp_value`
- `gwp_unit`
- `document_path`
- `source`
- `data_quality`

### Materialeigenschaft

Beschreibt flexible Detailwerte zu Materialien.

Implementiert als `ma_variants.material_catalog.MaterialProperty`.

Felder:

- `material_key`
- `property_key`
- `value`
- `unit`
- `source`
- `data_quality`

### Dokument

Referenziert Datenblaetter, Nachweise oder andere Dokumente ueber Dateipfade. Die Dateien selbst werden nicht in PostgreSQL gespeichert.

Implementiert als `ma_variants.document_catalog.Document`.

Felder:

- `document_key`
- `document_type`
- `title`
- `document_path`
- `related_key`
- `source`
- `data_quality`

### Quelle

Beschreibt die Herkunft von Produkt-, Material- oder Dokumentdaten.

Implementiert als `ma_variants.source_catalog.Source`.

Felder:

- `source_key`
- `source_type`
- `title`
- `url`
- `citation`
- `accessed_at`
- `data_quality`

## Variantenzaehlung und Export

Abschnitt 3 ergaenzt eine einfache Kombinatorik auf Basis der bestehenden Modelle.

Die Variantenzaehlung nutzt:

- `Parameter.is_variant_relevant`
- `Parameter.option_set_key`
- `OptionValue.option_set_key`
- `OptionValue.is_active`

Erzeugte Varianten werden als Tupel aus `Variant` und Liste von `VariantValue` im Speicher gehalten. Der JSON-Export schreibt diese Struktur als Objekt mit `variant_count` und `variants`. Jede Variante enthaelt ihre Stammdaten und eine Liste `values`.

Beispielausgaben:

- `data/exports/example_variants.json`
- `data/exports/example_variant_overview.json`
- `data/exports/example_variant_overview.csv`
- `data/exports/example_variant_report.json`

## Systemtemplate-Aufloesung

Abschnitt 7 fuehrt `ma_variants.system_catalog` ein. Systemtemplates erlauben, dass Varianten nur noch auf eine generische Systementscheidung verweisen, waehrend die konkreten Detailwerte im Systemkatalog liegen.

Beispiel:

- Eine Variante enthaelt einen `VariantValue` mit `option_key = PV_01`.
- Der Resolver erkennt `PV_01` als aktives `SystemTemplate`.
- `PV_01` wird zu konkreten `SystemTemplateValue` Eintraegen aufgeloest, zum Beispiel `pv_area_m2`, `pv_tilt_deg`, `pv_azimuth_deg` und `pv_peak_power_kwp`.

Die Beispielsysteme liegen unter `config/systems/example_system_templates.yaml`:

- `HEAT_01`
- `COOL_01`
- `PV_01`
- `VENT_01`

`resolve_system_templates_for_variant` liefert `ResolvedSystemTemplateValue` Objekte mit `variant_key`, `system_template_key`, `parameter_key`, `resolved_value`, `unit` und `value_source`.

Aktive `DependencyRule` Eintraege pruefen einfache Template-Abhaengigkeiten. Im Beispiel benoetigt `COOL_01` das Template `VENT_01`.

## Pflichtfeldvalidierung

Die Validierung liegt unter `ma_variants.validation`.

Aktuell umgesetzt:

- Textfelder muessen als String gesetzt und duerfen nicht leer sein.
- Wertfelder wie `value` und `resolved_value` muessen gesetzt sein; `0` und `False` bleiben gueltige Werte.
- Bool-Felder muessen echte boolesche Werte sein.

Diese Validierung ersetzt noch kein vollstaendiges fachliches Regelwerk. Sie dient nur dazu, die zentrale Modellstruktur stabil und testbar zu machen.

## Importvalidierung

Die Importer liegen in:

- `ma_variants.parameter_catalog.importer`
- `ma_variants.option_catalog.importer`
- `ma_variants.importing.catalog`

Aktuell umgesetzt:

- Pflichtfeldpruefung fuer Parameter, Optionsgruppen und Optionswerte.
- Doppelte `parameter_key` Werte werden gemeldet.
- Doppelte `option_key` Werte werden gemeldet.
- Parameterreferenzen auf nicht vorhandene `option_set_key` Werte werden gemeldet.
- Leere Werte werden gemeldet, waehrend `0` als gueltiger Wert erhalten bleibt.

## Produkt- und Materialimportvalidierung

Die neuen Katalogimporte liegen in:

- `ma_variants.product_catalog.importer`
- `ma_variants.material_catalog.importer`
- `ma_variants.document_catalog.importer`
- `ma_variants.source_catalog.importer`

Aktuell umgesetzt:

- Pflichtfeldpruefung fuer Produkte, Materialien, Dokumente und Quellen.
- Doppelte `product_key`, `material_key`, `document_key` und `source_key` Werte werden gemeldet.
- Doppelte flexible Properties je Objekt und `property_key` werden gemeldet.
- ProductProperties mit unbekanntem `product_key` werden gemeldet.
- MaterialProperties mit unbekanntem `material_key` werden gemeldet.
- Negative Kosten-, Leistungs-, Dichte-, Lambda-, Waermekapazitaets- und GWP-Werte werden gemeldet.
- CSV-Import fuer Produkte und Materialien erwartet eine Kopfzeile mit den jeweiligen Pflichtfeldern.

## Implementierte Datenbankstruktur

Abschnitt 6 fuehrt die vorbereitete SQLAlchemy-/Alembic-Struktur unter `ma_variants.database` ein. Die Datenbankverbindung wird ueber Umgebungsvariablen konfiguriert. Es werden keine Zugangsdaten im Code gespeichert.

Konfigurationsvarianten:

- `MA_VARIANTS_DATABASE_URL` fuer eine vollstaendige SQLAlchemy-Verbindungs-URL.
- Alternativ `MA_VARIANTS_DB_DIALECT`, `MA_VARIANTS_DB_HOST`, `MA_VARIANTS_DB_PORT`, `MA_VARIANTS_DB_NAME`, `MA_VARIANTS_DB_USER` und optional `MA_VARIANTS_DB_PASSWORD`.

Eine Beispielvorlage ohne echte Zugangsdaten liegt unter `config/database/example.env`.

Die Alembic-Migration `20260603_0001_create_ma_variants_core_tables` legt diese Tabellen an:

- `parameters`
- `option_sets`
- `option_values`
- `variants`
- `variant_values`
- `import_logs`

Die Alembic-Migration `20260603_0002_create_system_template_tables` ergaenzt:

- `system_templates`
- `system_template_values`
- `dependency_rules`

Die Alembic-Migration `20260603_0003_create_economic_tables` ergaenzt:

- `generic_system_costs`
- `energy_prices`
- `economic_scenarios`
- `variant_cost_results`

Die Alembic-Migration `20260603_0004_create_catalog_tables` ergaenzt:

- `sources`
- `documents`
- `products`
- `product_properties`
- `materials`
- `material_properties`

### Tabelle `option_sets`

Primaerschluessel:

- `option_set_key`

Spalten:

- `display_name`
- `description`
- `created_at`
- `updated_at`

### Tabelle `parameters`

Primaerschluessel:

- `parameter_key`

Spalten:

- `display_name`
- `category`
- `parameter_class`
- `option_set_key`
- `unit`
- `is_variant_relevant`
- `is_naming_relevant`
- `is_export_relevant`
- `created_at`
- `updated_at`

Beziehungen:

- `parameters.option_set_key` referenziert `option_sets.option_set_key`.

### Tabelle `option_values`

Primaerschluessel:

- `option_key`

Spalten:

- `option_set_key`
- `label`
- `value`
- `unit`
- `is_active`
- `created_at`
- `updated_at`

Beziehungen:

- `option_values.option_set_key` referenziert `option_sets.option_set_key`.

`value` wird als JSON-Feld gespeichert, damit Zahlen, Textwerte und einfache strukturierte Werte ohne Produkt- oder Materialtabellen abbildbar bleiben.

### Tabelle `variants`

Primaerschluessel:

- `variant_key`

Spalten:

- `variant_name`
- `status`
- `created_at`
- `updated_at`

### Tabelle `variant_values`

Primaerschluessel:

- Kombination aus `variant_key` und `parameter_key`

Spalten:

- `option_key`
- `resolved_value`
- `created_at`
- `updated_at`

Beziehungen:

- `variant_values.variant_key` referenziert `variants.variant_key`.
- `variant_values.parameter_key` referenziert `parameters.parameter_key`.
- `variant_values.option_key` referenziert `option_values.option_key`.

`resolved_value` wird als JSON-Feld gespeichert, damit importierte Beispielwerte unveraendert uebernommen werden koennen.

### Tabelle `import_logs`

Primaerschluessel:

- `id`

Spalten:

- `source_name`
- `status`
- `message`
- `error_count`
- `details`
- `created_at`

`details` ist ein optionales JSON-Feld fuer kleine Importmetadaten. Es ersetzt keine fachlichen Produkt-, Material- oder Simulationstabellen.

### Tabelle `system_templates`

Primaerschluessel:

- `system_template_key`

Spalten:

- `display_name`
- `system_type`
- `description`
- `is_active`
- `created_at`
- `updated_at`

### Tabelle `system_template_values`

Primaerschluessel:

- Kombination aus `system_template_key` und `parameter_key`

Spalten:

- `value`
- `unit`
- `value_source`
- `created_at`
- `updated_at`

Beziehungen:

- `system_template_values.system_template_key` referenziert `system_templates.system_template_key`.

### Tabelle `dependency_rules`

Primaerschluessel:

- `rule_key`

Spalten:

- `system_template_key`
- `required_system_template_key`
- `description`
- `is_active`
- `created_at`
- `updated_at`

Beziehungen:

- `dependency_rules.system_template_key` referenziert `system_templates.system_template_key`.
- `dependency_rules.required_system_template_key` referenziert `system_templates.system_template_key`.

### Tabelle `generic_system_costs`

Primaerschluessel:

- `system_type`

Spalten:

- `display_name`
- `investment_cost_eur`
- `maintenance_cost_eur_per_year`
- `lifetime_years`
- `is_example_value`
- `created_at`
- `updated_at`

### Tabelle `energy_prices`

Primaerschluessel:

- `energy_carrier`

Spalten:

- `price_eur_per_kwh`
- `is_example_value`
- `created_at`
- `updated_at`

### Tabelle `economic_scenarios`

Primaerschluessel:

- `scenario_key`

Spalten:

- `display_name`
- `observation_period_years`
- `heating_energy_carrier`
- `cooling_energy_carrier`
- `default_heating_energy_kwh_per_year`
- `default_cooling_energy_kwh_per_year`
- `is_example_value`
- `created_at`
- `updated_at`

Beziehungen:

- `economic_scenarios.heating_energy_carrier` referenziert `energy_prices.energy_carrier`.
- `economic_scenarios.cooling_energy_carrier` referenziert `energy_prices.energy_carrier`.

### Tabelle `variant_cost_results`

Primaerschluessel:

- Kombination aus `variant_key` und `scenario_key`

Spalten:

- `variant_name`
- `selected_system_types`
- `investment_cost_eur`
- `maintenance_cost_eur_per_year`
- `maintenance_cost_total_eur`
- `energy_cost_eur_per_year`
- `energy_cost_total_eur`
- `replacement_cost_eur`
- `total_cost_eur`
- `observation_period_years`
- `heating_energy_kwh_per_year`
- `cooling_energy_kwh_per_year`
- `uses_simulation_results`
- `uses_example_energy_values`
- `assumption_notes`
- `created_at`
- `updated_at`

Beziehungen:

- `variant_cost_results.scenario_key` referenziert `economic_scenarios.scenario_key`.

`selected_system_types` und `assumption_notes` werden als JSON-Felder gespeichert. `variant_key` ist bewusst nicht zwingend als Fremdschluessel modelliert, damit erste Ergebnisimporte auch dann moeglich bleiben, wenn noch nicht alle Varianten zentral gespeichert sind.

### Tabelle `sources`

Primaerschluessel:

- `source_key`

Spalten:

- `source_type`
- `title`
- `url`
- `citation`
- `accessed_at`
- `data_quality`
- `created_at`
- `updated_at`

### Tabelle `documents`

Primaerschluessel:

- `document_key`

Spalten:

- `document_type`
- `title`
- `document_path`
- `related_key`
- `source`
- `data_quality`
- `created_at`
- `updated_at`

`document_path` ist ein Dateipfad. Das Dokument selbst wird nicht als Binaerdaten in PostgreSQL gespeichert.

### Tabelle `products`

Primaerschluessel:

- `product_key`

Spalten:

- `product_type`
- `manufacturer`
- `product_name`
- `nominal_power`
- `price`
- `currency`
- `gwp_value`
- `gwp_unit`
- `product_url`
- `document_path`
- `source`
- `data_quality`
- `created_at`
- `updated_at`

### Tabelle `product_properties`

Primaerschluessel:

- Kombination aus `product_key` und `property_key`

Spalten:

- `value`
- `unit`
- `source`
- `data_quality`
- `created_at`
- `updated_at`

Beziehungen:

- `product_properties.product_key` referenziert `products.product_key`.

`value` wird als JSON-Feld gespeichert, damit Zahlen, Texte und einfache strukturierte Detailwerte abbildbar bleiben.

### Tabelle `materials`

Primaerschluessel:

- `material_key`

Spalten:

- `material_group`
- `material_name`
- `density`
- `lambda_value`
- `specific_heat_capacity`
- `price`
- `gwp_value`
- `gwp_unit`
- `document_path`
- `source`
- `data_quality`
- `created_at`
- `updated_at`

### Tabelle `material_properties`

Primaerschluessel:

- Kombination aus `material_key` und `property_key`

Spalten:

- `value`
- `unit`
- `source`
- `data_quality`
- `created_at`
- `updated_at`

Beziehungen:

- `material_properties.material_key` referenziert `materials.material_key`.

`value` wird als JSON-Feld gespeichert. Die Tabelle ist fuer spaetere Zusatzwerte gedacht und ersetzt keine vollstaendige Materialdatenbank.

## Repository-Funktionen

Die ersten Repository-Funktionen liegen in `ma_variants.database.repositories`:

- `save_parameters`
- `save_option_sets`
- `save_option_values`
- `save_variants`
- `save_variant_values`
- `save_generated_variants`
- `save_system_templates`
- `save_system_template_values`
- `save_dependency_rules`
- `save_generic_system_costs`
- `save_energy_prices`
- `save_economic_scenarios`
- `save_variant_cost_results`
- `save_sources`
- `save_documents`
- `save_products`
- `save_product_properties`
- `save_materials`
- `save_material_properties`
- `save_import_log`

Die Funktionen speichern die bestehenden Python-Modelle in SQLAlchemy-Sessions. Sie loeschen keine vorhandenen Daten.

## Abgrenzung

In diesem Abschnitt werden nur die zentralen Katalog-, Varianten-, Systemtemplate-, Wirtschaftlichkeits- und Importlog-Tabellen vorbereitet. Excel- und Prisma-Importe sind weiterhin nur als spaetere Importquellen vorgesehen. Es wurden keine vollstaendige technische Systembibliothek, keine automatische Produktzuordnung, keine automatische Produktrecherche, keine vollstaendige Herstellerdatenbank, keine detaillierten Simulationsergebnistabellen, keine produktspezifische Wirtschaftlichkeitsbewertung und keine IDA-ICE-Exportmodelle implementiert.

Die Produkt- und Materialdaten in den Beispielkatalogen sind Platzhalter. Sie dienen nur dazu, die Struktur fuer ausgewaehlte Varianten vorzubereiten. Datenblaetter werden nicht in PostgreSQL gespeichert, sondern ueber Pfade in `data/documents` referenziert.
