# Generisches Wirtschaftlichkeitsmodell

Stand: 2026-06-03

Dieses Dokument beschreibt die erste, bewusst einfache Wirtschaftlichkeitsanalyse fuer Varianten. Sie dient als pruefbare Bewertungslogik und nicht als vollstaendige produktspezifische Kostenberechnung.

## Ziel

Abschnitt 10 ergaenzt `ma_variants.economic_analysis`. Das Modul kann fuer Varianten generische Kosten berechnen, ohne Produktdatenbank, Materialdatenbank oder detaillierte LCA zu erzwingen.

Die Berechnung nutzt:

- generische Systemkosten
- generische Energiepreise
- ein Wirtschaftlichkeitsszenario mit Betrachtungszeitraum
- optional bereits eingelesene Simulationsergebnisse

Wenn keine Simulationsergebnisse vorhanden sind, werden Beispiel-Energiebedarfe aus dem Szenario verwendet. Diese Ergebnisse werden mit `uses_example_energy_values = true` und Hinweisen in `assumption_notes` gekennzeichnet.

## Eingaben

Die Beispielannahmen liegen unter:

```text
config/economic/example_economic_assumptions.yaml
```

### Generische Systemkosten

`generic_system_costs` beschreibt Kosten je Systemtyp:

- `system_type`
- `display_name`
- `investment_cost_eur`
- `maintenance_cost_eur_per_year`
- `lifetime_years`
- `is_example_value`

Die Beispielsystemtypen sind:

- `heating`
- `cooling`
- `pv`
- `ventilation`

### Energiepreise

`energy_prices` beschreibt einfache Energiepreisannahmen:

- `energy_carrier`
- `price_eur_per_kwh`
- `is_example_value`

### Wirtschaftlichkeitsszenarien

`economic_scenarios` beschreibt den Betrachtungszeitraum und Fallback-Energiebedarfe:

- `scenario_key`
- `display_name`
- `observation_period_years`
- `heating_energy_carrier`
- `cooling_energy_carrier`
- `default_heating_energy_kwh_per_year`
- `default_cooling_energy_kwh_per_year`
- `is_example_value`

## Berechnung

Die aktuelle Rechnung ist statisch und nicht abgezinst.

Formeln:

```text
investment_cost = Summe der Investitionskosten aller ausgewaehlten Systemtypen
maintenance_cost_total = Summe der Wartungskosten pro Jahr * Betrachtungszeitraum
replacement_cost = Summe je System: Investitionskosten * floor((Betrachtungszeitraum - 1) / Lebensdauer)
energy_cost_per_year = Heizenergie * Heizenergiepreis + Kuehlenergie * Kuehlenergiepreis
energy_cost_total = energy_cost_per_year * Betrachtungszeitraum
total_cost = investment_cost + maintenance_cost_total + replacement_cost + energy_cost_total
```

Simulationsergebnisse aus `ma_variants.simulation_results` werden verwendet, wenn `heating_energy_kwh` und/oder `cooling_energy_kwh` in den `summary_metrics` vorhanden sind. Fehlende Energiewerte fallen einzeln auf die Szenario-Beispielwerte zurueck.

## Ausgaben

Die Ergebnisse werden als `VariantCostResult` bereitgestellt und koennen exportiert werden:

- JSON: `data/exports/variant_cost_results.json`
- CSV: `data/exports/variant_cost_results.csv`

Wichtige Ergebnisfelder:

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
- `uses_simulation_results`
- `uses_example_energy_values`
- `assumption_notes`

## Datenbankvorbereitung

Die Alembic-Migration `20260603_0003_create_economic_tables` bereitet optionale Tabellen vor:

- `generic_system_costs`
- `energy_prices`
- `economic_scenarios`
- `variant_cost_results`

Die Berechnung ist nicht von PostgreSQL abhaengig. Die Tabellen dienen der spaeteren zentralen Speicherung.

## Grenzen

- Keine produktspezifischen Kosten.
- Keine Materialdatenbank.
- Keine detaillierte LCA.
- Keine Preissteigerungen, Diskontierung oder Restwertberechnung.
- Keine automatische Produktzuordnung.
- Keine Ableitung vollstaendiger Investitionskosten aus IDA-ICE-Dateien.

Alle Beispielwerte muessen vor einer belastbaren Bewertung fachlich ersetzt oder freigegeben werden.
