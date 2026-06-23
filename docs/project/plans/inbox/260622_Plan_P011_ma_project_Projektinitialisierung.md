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

## Umsetzungsbezug P028

Bereits als Demo umgesetzt sind die frei verwaltbare Simulationsprogrammliste,
das aktive Programm, neutrale Benennungsprofile, Vorschau, Eindeutigkeitspruefung
und geschuetzte lokale Speicherung. Projekt-ID, Standort, Untersuchungsziel,
Modellreferenzen, Quellenwahl und Freigabestatus bleiben fuer P011 offen.

## Umsetzungsbezug P010

P011 verwendet `InputSource` fuer die Quellenwahl je Modul, strukturierte
Diagnosen fuer fehlende Pflichtangaben und die gemeinsame Freigabelogik.
Projektbezogene Entscheidungen sollen in den append-only Sitzungslogs
referenzierbar bleiben. Eine Datenbank ist dafuer nicht erforderlich.
