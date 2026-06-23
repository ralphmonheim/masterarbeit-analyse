# P012 ma_building Gebaeudeinput

Stand: 2026-06-22
Status: Geplant
Prioritaet: Hoch
Abhaengigkeiten: P010, P011

## Ziel

Gebaeudestruktur, Flaechen, Bauteile und bauphysikalische Randbedingungen
konzeptuell vollstaendig und mit einem Demo-Datensatz nutzbar machen.

## Reifegrad

Konzept plus Demo; optional spaeter Lite-Import.

## Arbeitspakete

- Neutrales Gebaeude-, Geschoss-, Raum-, Flaechen- und Bauteilmodell planen.
- Manuellen YAML-Demo-Datensatz und UI-Darstellung vorsehen.
- Dateityp und erkennbaren Inhalt vor einem Import diagnostizieren.
- IFC-Dateien nach vorhandenem Inhalt und Arbeitsstand klassifizieren.
- Sichere IFC-Felder erst nach Analyse realer Beispieldateien fuer einen
  optionalen Lite-Adapter freigeben.

## Akzeptanzkriterien

- Demo-Gebaeude liefert validierte Daten an `ma_parameters`.
- Unbekannte oder unvollstaendige Dateien erzeugen Diagnose statt Absturz.
- Importierte und manuell ergaenzte Werte bleiben unterscheidbar.
- Kein vollstaendiger IFC- oder CAD-Workflow wird vorgetaeuscht.

## Nicht enthalten

- CAD-Modellerstellung
- allgemeingueltige IFC-Geometrieinterpretation
- direkte Aenderung des IDA-Modells
