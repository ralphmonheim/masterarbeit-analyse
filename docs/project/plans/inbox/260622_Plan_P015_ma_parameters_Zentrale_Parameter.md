# P015 ma_parameters Zentrale Parameter

Stand: 2026-07-08
Status: Teilweise umgesetzt, P015-S1 ParameterSnapshot v1; P013-S2-Zonenstand als Folgearbeit
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
  Version bereitstellen.
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
- Zonenstaende aus P013-S2 nur nach abgeschlossenem Eingabecheckpoint
  uebernehmen.
- Status `current`, `outdated` und `validation_required` fuer spaetere
  Zonen- und Parameterstaende vorbereiten.
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
freigegebener `ParameterSnapshot` mit Herkunft ist fuer die
BusinessIntegration-LoD-1-Kette umgesetzt. Aenderungsnachweis und lokale
Snapshot-Speicherung bleiben Folgeausbau.

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

## Umsetzungsbezug P013-S2

P013-S2 legt den Zielvertrag fuer `ma_zones` fachlich neu fest:

- `ma_zones` liegt nach `ma_technical` und vor dem Eingabecheckpoint von
  `ma_validation`.
- `ma_parameters` uebernimmt erst danach den freigegebenen vollstaendigen
  Zonenstand.
- Aenderungen in `ma_zones` muessen spaeter den Parameterstand als veraltet
  markieren und die Variantengenerierung blockieren, bis `ma_parameters` und
  der Parametercheckpoint aktualisiert sind.
- `ma_variants` greift weiterhin nicht direkt auf `ma_zones` zu.

Der bestehende BusinessIntegration-LoD-1-Snapshot bleibt kompatibel. Die
konkrete Status-/Fingerprint-Logik gehoert in einen Folgeslice.

## Umsetzungsbezug BusinessIntegration-LoD-1

P015-S1 setzt einen ersten produktiven `ParameterSnapshot` v1 fuer die
validierte BusinessIntegration-LoD-1-Kette um:

- `ma_building`: Kubatur, einfache Huellkennwerte, U-Werte und Fensteranteil
- `ma_zones`: Zonenanzahl, Flaeche, Volumen, Sollwerte, interne Lasten und
  Nutzungsprofilwerte
- `ma_technical`: einfache spezifische Heiz-/Kuehlleistungen,
  geschaetzte Leistungen, Luftwechsel und Leistungszahlen

Der Snapshot enthaelt Snapshot-ID, Version, Projekt- und Gebaeudebezug,
Quellenreferenzen, Parameterwerte, Einheiten, Status und eine eigene
Validierung. Nur freigegebene Fachquellen werden akzeptiert. Fehler
blockieren, Warnungen benoetigen eine bewusste Freigabeentscheidung.

## Umsetzungsstand P015-S1

- `ParameterSnapshot`, `ParameterValue` und `ParameterSourceReference` sind
  als Fachmodelle umgesetzt.
- `build_business_integration_lod1_parameter_snapshot()` baut den Snapshot
  aus den validierten Demos von `ma_building`, `ma_zones` und `ma_technical`.
- `validate_parameter_snapshot()` prueft Pflichtfelder, eindeutige
  Parameter-Keys, Einheiten, Quellenreferenzen, freigegebene Quellen und
  erforderliche LoD-1-Schluessel.
- Streamlit zeigt eine Snapshot-Pruefansicht mit Freigabestatus, Kopfdaten,
  Parameterwerten, Quellen und Validierungsmeldungen.

## Nicht umgesetzt in P015-S1

- persistente lokale Snapshot-Speicherung
- manuelle Ueberschreibung mit `InputChange`-Aenderungsnachweis
- Wetterdaten-Uebernahme in den Snapshot
- vollstaendiger P013-S2-Zonenstand mit Aenderungsfingerprint
- Status `current/outdated/validation_required`
- Stage-1-Ergebnis als neuer Snapshot-Vorschlag
- direkte Umstellung von `ma_variants` auf den Snapshot

## Naechster Schritt

P013-S2-Zonenstand, Stage-1-Ergebnisse als Folgesnapshot beziehungsweise
Vorschlag und Variantenanbindung auf `ParameterSnapshot` v1 vorbereiten.
