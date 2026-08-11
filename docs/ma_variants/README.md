# ma_variants

Dieser Bereich dokumentiert den modularen Varianten-, Export-, Katalog- und Bewertungskern.

## Zweck

Varianten aus einer validierten zentralen Parameterquelle erzeugen,
auswaehlen, benennen und nachvollziehbar verwalten.

## Eingaben

- `BaselineParameterSnapshot`, `ReferenceDimensioningResult` und
  `ParameterVariationSpecification` aus `ma_parameters`
- Auswahlregeln und neutrales Benennungsprofil aus `ma_project`

## Ausgaben

- verifizierter Variantenkatalog, VariantSelection, vollstaendig erzeugte
  Varianten, Metadaten und wissenschaftliche Reports

## Abgrenzung

- kein eigenes Simulationssetup
- langfristig keine direkte Abhaengigkeit von Gebaeude-, Wetter-, Zonen- oder
  Technikmodulen
- keine Verwaltung von Projekt-, Produkt- oder programmspezifischen
  Exportbezeichnungen
- keine Heiz-/Kuehllastberechnung und keine fachliche Veraenderung von
  Simulationssetup-Werten

## Abhaengigkeiten

- derzeit bestehende Konfigurationen unter `config/ma_variants/`
- spaeter ausschliesslich `ma_parameters` als fachliche Eingangsquelle

## Status

Teilweise umgesetzt und fachlich konsolidiert. Der aktive Zielprozess lautet
`VSP -> VVER -> VCAT -> VSEL -> VGEN -> ma_simulation_setup`. Fuer
SmallOffice V1 erzeugt ein versionierter Studienvertrag aus der
`ma_parameters`-Baseline 30 Optimierungs- und acht Sensitivitaetsfaelle und
uebergibt sie direkt an `ma_simulation_setup`. Der allgemeine P017-Vertrag und
der bestehende Prototyp bleiben kompatibel.

Die Optimierung kombiniert fuenf globale Temperatur-Sollwertbaender mit sechs
gekoppelten Heiz-/Kuehlleistungsfaktoren. Die Sensitivitaet bleibt getrennt
und verwendet den Referenz-/Dimensionierungsfall fuer vier Frankfurt-
Jahreswetter beziehungsweise vier Belegungszeitprofile.

Fuer den manuellen Auswahltest steht zusaetzlich die getrennte, versionierte
Studienconfig `small_office_v1_random_156.yaml` bereit. Sie erzeugt 156
theoretische Optimierungsvarianten und kann in der Variantenansicht mit einem
festen Startwert reproduzierbar auf eine Teilmenge (zum Beispiel 50) reduzieren.
Der 30er-Referenzbenchmark bleibt davon unveraendert.

Nach dem Simulation-Setup fasst `run_summary.yaml` Studienstand, Auswahl,
generierte Varianten und Artefaktpfade zusammen. `timings.yaml` und
`timings.csv` protokollieren Kandidaten-, Auswahl-, Referenzdimensionierungs-,
Katalog- und Paketzeiten sowie die Simulation-Setup-Materialisierung;
manuelle Bearbeitungs- und IDA-Simulationszeiten sind nicht enthalten.

Erzeugte `test_only`-Studien liegen unter `data/test_output/<Projekt-ID>/`;
regulaere Projektstudien liegen getrennt unter `data/project_output/<Projekt-ID>/`.

## Naechster Schritt

Den allgemeinen P017-Vertrag schrittweise auf die mit SmallOffice V1
nachgewiesenen stabilen Eingangsreferenzen und Draft-Run-Uebergaben
konsolidieren, ohne automatische Auswahl oder Simulation einzufuehren.

## Dateien

- `workflow.md`: Ablauf von Parameterimport bis UI und Bewertung.
- `data_model.md`: Datenmodelle, Tabellen und Katalogstruktur.
- `economic_model.md`: Annahmen und Grenzen der generischen Wirtschaftlichkeitsanalyse.
- `commands_variants.md`: lokale Befehle fuer Varianten-UI und Varianten-Tests.

Konfigurationen liegen unter `config/ma_variants/`. Variantenbezogene Arbeitsdaten liegen unter `data/ma_variants/`. Produkt- und Materialdokumente liegen getrennt unter `data/catalogs/documents/`.
