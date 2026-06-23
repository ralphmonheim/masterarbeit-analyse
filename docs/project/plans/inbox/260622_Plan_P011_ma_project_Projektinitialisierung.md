# P011 ma_project Projektinitialisierung

Stand: 2026-06-23
Status: Geplant
Prioritaet: Hoch
Abhaengigkeiten: P010

## Ziel

Projektstammdaten, Untersuchungsziel, Modellreferenzen und die je Modul
gewaehlten Eingabequellen in einer validierbaren Projektkonfiguration
zusammenfassen.

## Reifegrad

Lite-Implementierung fuer die Masterarbeit.

## Arbeitspakete

- Projekt-ID, Titel, Standort, Untersuchungsziel und Modellstand definieren.
- Frei erweiterbare Simulationsprogrammliste mit Programmschluessel,
  Anzeigename, Version und optionaler Notiz verwalten.
- Aktives Simulationsprogramm auswaehlen.
- Neutrales Varianten-Benennungsprofil verwalten und referenzieren.
- Quellenwahl fuer Building, Weather, Zones, Technical und Parameters
  referenzieren.
- IFC-/IDA-Modell nur als externe Referenz mit Pfad, Version und Notiz fuehren.
- Projektkonfiguration als YAML laden, in der UI bearbeiten und speichern.
- Freigabestatus fuer die nachfolgenden Eingabemodule erzeugen.

## Akzeptanzkriterien

- Projektkonfiguration ist ohne Datenbank reproduzierbar.
- Fehlende Pflichtangaben erzeugen strukturierte Fehler.
- Quellen koennen je Modul unterschiedlich gewaehlt werden.
- Keine CAD- oder IDA-Software muss installiert sein.
- Produkt- und Materialbezeichnungen bleiben neutrale Katalogdaten.
- Programmspezifische Objekt- und Exportcodes bleiben Aufgabe der
  Simulationsadapter.
