# ma_variants

Dieser Bereich dokumentiert den modularen Varianten-, Export-, Katalog- und Bewertungskern.

## Zweck

Varianten aus einer validierten zentralen Parameterquelle erzeugen,
auswaehlen, benennen und nachvollziehbar verwalten.

## Eingaben

- zentrale Parameterliste aus `ma_parameters`
- Options-, Auswahl- und Namensregeln

## Ausgaben

- Varianten, Auswahlmengen, Metadaten und Variantenuebersichten

## Abgrenzung

- kein eigenes Simulationssetup
- langfristig keine direkte Abhaengigkeit von Gebaeude-, Wetter-, Zonen- oder
  Technikmodulen

## Abhaengigkeiten

- derzeit bestehende Konfigurationen unter `config/ma_variants/`
- spaeter ausschliesslich `ma_parameters` als fachliche Eingangsquelle

## Status

Aktiv fuer den bestehenden Umfang. Spaetere Zielverantwortlichkeiten werden
nur ueber eigene Plaene extrahiert.

## Naechster Schritt

Bestehenden Kern stabil halten und die Anbindung an `ma_parameters` separat
planen.

## Dateien

- `workflow.md`: Ablauf von Parameterimport bis UI und Bewertung.
- `data_model.md`: Datenmodelle, Tabellen und Katalogstruktur.
- `economic_model.md`: Annahmen und Grenzen der generischen Wirtschaftlichkeitsanalyse.
- `commands_variants.md`: lokale Befehle fuer Varianten-UI und Varianten-Tests.

Konfigurationen liegen unter `config/ma_variants/`. Variantenbezogene Arbeitsdaten liegen unter `data/ma_variants/`. Produkt- und Materialdokumente liegen getrennt unter `data/catalogs/documents/`.
