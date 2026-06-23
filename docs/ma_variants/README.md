# ma_variants

Dieser Bereich dokumentiert den modularen Varianten-, Export-, Katalog- und Bewertungskern.

## Zweck

Varianten aus einer validierten zentralen Parameterquelle erzeugen,
auswaehlen, benennen und nachvollziehbar verwalten.

## Eingaben

- zentrale Parameterliste aus `ma_parameters`
- Auswahlregeln und neutrales Benennungsprofil aus `ma_project`

## Ausgaben

- Varianten, Auswahlmengen, Metadaten und Variantenuebersichten

## Abgrenzung

- kein eigenes Simulationssetup
- langfristig keine direkte Abhaengigkeit von Gebaeude-, Wetter-, Zonen- oder
  Technikmodulen
- keine Verwaltung von Projekt-, Produkt- oder programmspezifischen
  Exportbezeichnungen

## Abhaengigkeiten

- derzeit bestehende Konfigurationen unter `config/ma_variants/`
- spaeter ausschliesslich `ma_parameters` als fachliche Eingangsquelle

## Status

Geplant. Ein umfangreicher Prototyp ist vorhanden, aber die verbindliche
Eingangsquelle `ma_parameters` und die Integration bis `ma_simulation_setup`
fehlen. P028 bindet die Demo-Optionsauswahl und das neutrale Benennungsprofil
bereits ueber einen gemeinsamen Streamlit-Sitzungsstand an.

## Naechster Schritt

Bestehenden Kern stabil halten und die P028-Demo ueber P017 auf versionierte
`ParameterSnapshot`- und Naming-Regelstaende umstellen.

## Dateien

- `workflow.md`: Ablauf von Parameterimport bis UI und Bewertung.
- `data_model.md`: Datenmodelle, Tabellen und Katalogstruktur.
- `economic_model.md`: Annahmen und Grenzen der generischen Wirtschaftlichkeitsanalyse.
- `commands_variants.md`: lokale Befehle fuer Varianten-UI und Varianten-Tests.

Konfigurationen liegen unter `config/ma_variants/`. Variantenbezogene Arbeitsdaten liegen unter `data/ma_variants/`. Produkt- und Materialdokumente liegen getrennt unter `data/catalogs/documents/`.
