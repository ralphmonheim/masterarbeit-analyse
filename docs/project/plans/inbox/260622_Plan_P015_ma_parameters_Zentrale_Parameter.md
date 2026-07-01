# P015 ma_parameters Zentrale Parameter

Stand: 2026-06-23
Status: Geplant
Prioritaet: Hoch
Abhaengigkeiten: P010, P008, P012, P013, P014

## Ziel

Alle freigegebenen Randbedingungen als einzige fachliche Eingangsquelle fuer
`ma_variants` vereinheitlichen.

## Reifegrad

Produktiver Kern fuer die Masterarbeit.

## Arbeitspakete

- Bestehende Parameter- und Optionskataloge aus `ma_variants` inventarisieren.
- `ParameterSnapshot` mit Schluessel, Wert, Einheit, Herkunft, Status und
  Version planen.
- Programm- und projektspezifische Importvorlagen zulassen.
- Vorhandene Demo-Parameter schreibgeschuetzt in Streamlit anzeigen und
  aktive Optionswerte als gemeinsamen Sitzungsstand auswaehlen.
- Eigene Optionskonfigurationen lokal unter
  `data/ma_parameters/config/options/` speichern.
- Manuelle UI-Ueberschreibung mit Aenderungsnachweis vorsehen.
- Baseline-Snapshot von spaeteren Stage-1-Vorschlaegen trennen.
- Gebaeudedaten aus P012 nur nach freigegebener
  `BuildingModelSpecification` beziehungsweise freigegebener
  Gebaeudemodellversion uebernehmen.
- Nur freigegebene Snapshots an `ma_variants` uebergeben.

## Akzeptanzkriterien

- Direkte Eingabeabhaengigkeiten von `ma_variants` zu Building, Weather,
  Zones oder Technical entfallen.
- Einheiten- und Pflichtfeldfehler blockieren die Freigabe.
- Snapshot und Herkunft sind reproduzierbar exportierbar.
- Stage-1-Ergebnisse erzeugen einen neuen Vorschlag statt stille Aenderungen.
- Versionierte Demo-Vorlagen koennen weder direkt noch ueber eine
  Namenskollision ueberschrieben werden.

## Umsetzungsbezug P028

Bereits als Demo umgesetzt sind die schreibgeschuetzte Parameteranzeige,
Optionsgruppen, aktive Optionswerte, Vollstaendigkeitspruefung,
Variantenanzahl und geschuetzte lokale Speicherung. Ein versionierter,
freigegebener `ParameterSnapshot` mit Herkunft und Aenderungsnachweis bleibt
der produktive Kern von P015.

## Umsetzungsbezug P010

`ParameterSnapshot` soll die P010-Quellen-IDs, strukturierte Diagnosen,
manuelle `InputChange`-Eintraege und eine gueltige Freigabe referenzieren.
Fehler bleiben blockierend; Warnungen benoetigen eine dokumentierte
Entscheidung.

## Umsetzungsbezug P012

`ma_parameters` darf keine unvalidierten IFC-, Rhino-, YAML-, JSON- oder
Textdaten direkt verwenden. P012 liefert nur freigegebene und versionierte
Gebaeudeparameter, zum Beispiel Flaechen, Volumen, Bauteilkennwerte,
Orientierungen, Oeffnungsanteile, Raumreferenzen und Modellreifegrade.
