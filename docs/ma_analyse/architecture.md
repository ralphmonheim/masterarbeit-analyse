# Architektur

`ma_analyse` ist als Python-Paket unter `src/ma_analyse` aufgebaut. Die CLI,
die Streamlit-Ansicht und die Tkinter-Analyse nutzen dieselben fachlichen
Funktionen, damit Ergebnisse reproduzierbar bleiben. Die Tkinter-Dateien liegen
strukturell unter `ma_ui.tkinter_app`; `ma_analyse.gui` ist nur noch ein
Kompatibilitaetszugriff.

## Datenfluss

1. `prepare` liest Varianten aus `data/ma_analyse/ida_imports/` und schreibt Raumtabellen nach `data/ma_analyse/database/`.
2. `analyze-data` erzeugt als Basisbericht eine Excel-Datenuebersicht aus den vorbereiteten Raumtabellen.
3. `comfort`, `heating` und `cooling` lesen aus `data/ma_analyse/database/`.
4. Regulaere Ergebnisse landen in `data/ma_analyse/output/`, Smoke-Tests und Experimente in `data/test_output/`.
5. CLI-Analysebefehle spiegeln Konsolenausgaben automatisch nach `logs/`.

## Zentrale Pakete

| Paket/Modul | Aufgabe |
|---|---|
| `app/cli.py` | CLI-Parser und Paket-Einstieg |
| `app/commands.py` | Befehlsausfuehrung und Schritt-Orchestrierung |
| `core/config.py` | Pfade, Raeume, Dateinamen und gemeinsame Konstanten |
| `core/logging.py` | automatische Logdateien fuer Analyse-CLI-Laeufe |
| `data_preparation/` | Workflow-Einordnung fuer `prepare` und `analyze-data` vor Analyse Stufe 2 |
| `preprocessing/prepare.py` | Rohdaten aus PRN-Dateien in Raumtabellen ueberfuehren |
| `analysis/excel.py` | Ablauf fuer Kennzahlen- und Excel-Berichte |
| `analysis/heating.py` | Ablauf fuer Heizlast-Zeitreihen und Vergleichsplots |
| `analysis/cooling.py` | Ablauf fuer Kuehllast-Zeitreihen und Vergleichsplots |
| `analysis/templates/` | Manuell anpassbare Diagramm-Vorlagen fuer Plot-Experimente |
| `analysis/comfort/` | Comfort-Ablauf, Datenladen, Zonen, Tabellen und Plotmodule |
| `analysis/components/` | gemeinsame Analyse-Komponenten fuer Raeume, Varianten, Zeitfenster, Laufordner und Figures |
| `analysis/energy/` | gemeinsame Ausgabe-, Zeit- und Dateinamenlogik fuer Heating und Cooling |
| `analysis/tables/` | Schema, Kennwertberechnung und Excel-Schreiben fuer Tabellenberichte |
| `gui/` | Kompatibilitaetswrapper zur Tkinter-Analyse unter `ma_ui.tkinter_app.module_views.analyse` |
| `settings.naming` | Namensmapping lesen und anwenden; Dokument liegt daneben als `naming.md` |
| `settings.formats` | Ausgabeformate lesen und bereitstellen; Dokument liegt daneben als `output_formats.md` |
| `settings.plot_templates` | Plot-Template-Defaults aus `plot_templates.toml` lesen |

## Plot-Template Promotion

`plot-template` ist der Experimentierpfad fuer neue Plot-Ideen. Diese Ausgaben
laufen standardmaessig nach `data/test_output/PlotTemplates/...` und duerfen
schneller veraendert werden als die Hauptbefehle.

Wenn eine Template-Idee in eine Hauptfunktion uebernommen wird, gilt die Methode
**Geteilte Helper**:

1. Neue Darstellung oder Datenlogik zuerst im Template sichtbar testen.
2. Verhalten mit einem fokussierten Test oder Smoke-Test absichern.
3. Wiederverwendbare Logik in ein neutrales Modul auslagern, bevorzugt unter
   `analysis/components/` oder einem passenden Fachpaket.
4. Template und Hauptfunktion nutzen danach denselben Helper.
5. Keine experimentellen Overlay-, CLI- oder GUI-Optionen automatisch in
   Hauptfunktionen uebernehmen; solche Optionen brauchen eine eigene bewusste
   Promotion.

Aktuelle Beispiele:

- `analysis/components/heating_year_layout.py` enthaelt die geteilte
  Jahreslayoutbasis fuer `plot-template heating-year`, `plot-template
  heating-overlay` und die regulaere Heating-Jahresansicht.
- `analysis/templates/catalog.py` und `analysis/templates/timeline.py`
  strukturieren die Template-Sandbox fuer Heating-/Cooling-Zeitansichten.

## Naechste Modularisierung

- P029 stabilisiert zuerst den Service-/Runner-Vertrag mit strukturierten
  Schritt-Ergebnissen, bevor grosse Fachdateien zerlegt werden.
- Heating und Cooling weiter in Energy-Runner, Datenladen und Plotmodule zerlegen.
- Comfort-Runner weiter verkleinern, falls Auswahl- und Prozesslogik wachsen.
- Tkinter-Analyse weiter in kleinere Komponenten fuer Layout, Dialoge und
  Laufsteuerung aufteilen; Zielort bleibt `ma_ui.tkinter_app.module_views/analyse`.
