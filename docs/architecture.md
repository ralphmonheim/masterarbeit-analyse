# Architektur

`ma_analyse` ist als Python-Paket unter `src/ma_analyse` aufgebaut. Die CLI und GUI nutzen dieselben fachlichen Funktionen, damit Ergebnisse reproduzierbar bleiben.

## Datenfluss

1. `prepare` liest Varianten aus `data/input/` und schreibt Raumtabellen nach `data/database/`.
2. `comfort`, `heating`, `cooling` und `analyze-data` lesen aus `data/database/`.
3. Regulaere Ergebnisse landen in `data/output/`, Smoke-Tests und Experimente in `data/test_output/`.
4. CLI-Analysebefehle spiegeln Konsolenausgaben automatisch nach `logs/`.

## Zentrale Pakete

| Paket/Modul | Aufgabe |
|---|---|
| `app/cli.py` | CLI-Parser und Paket-Einstieg |
| `app/commands.py` | Befehlsausfuehrung und Schritt-Orchestrierung |
| `core/config.py` | Pfade, Raeume, Dateinamen und gemeinsame Konstanten |
| `core/logging.py` | automatische Logdateien fuer Analyse-CLI-Laeufe |
| `preprocessing/prepare.py` | Rohdaten aus PRN-Dateien in Raumtabellen ueberfuehren |
| `analysis/excel.py` | Ablauf fuer Kennzahlen- und Excel-Berichte |
| `analysis/heating.py` | Ablauf fuer Heizlast-Zeitreihen und Vergleichsplots |
| `analysis/cooling.py` | Ablauf fuer Kuehllast-Zeitreihen und Vergleichsplots |
| `analysis/comfort/` | Comfort-Ablauf, Datenladen, Zonen, Tabellen und Plotmodule |
| `analysis/components/` | gemeinsame Analyse-Komponenten fuer Raeume, Varianten, Zeitfenster, Laufordner und Figures |
| `analysis/energy/` | gemeinsame Ausgabe-, Zeit- und Dateinamenlogik fuer Heating und Cooling |
| `analysis/tables/` | Schema, Kennwertberechnung und Excel-Schreiben fuer Tabellenberichte |
| `gui/` | Grafische Oberflaeche, Dialoge, GUI-Worker und Singleton-Steuerung |
| `settings.naming` | Namensmapping lesen und anwenden; Dokument liegt daneben als `naming.md` |
| `settings.formats` | Ausgabeformate lesen und bereitstellen; Dokument liegt daneben als `output_formats.md` |

## Naechste Modularisierung

- Heating und Cooling weiter in Energy-Runner, Datenladen und Plotmodule zerlegen.
- Comfort-Runner weiter verkleinern, falls Auswahl- und Prozesslogik wachsen.
- GUI weiter in kleinere Komponenten fuer Layout, Dialoge und Laufsteuerung aufteilen.
