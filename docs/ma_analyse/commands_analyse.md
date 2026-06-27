# Befehle

Standard-Einstieg ist:

```powershell
python -m ma_analyse <befehl> [optionen]
```

## Einmaliges Setup

```powershell
cd "C:\Users\ralph\Documents\Master\5.Semester\Masterarbeit - lokal\TEIL1_Fach-Anwendungskompetenz\260524_Masterarbeit_Analyse"
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
```

Diesen Installationsbefehl brauchst du nur beim ersten Einrichten, nach dem Neuerstellen der virtuellen Umgebung oder wenn sich Abhaengigkeiten in `pyproject.toml` geaendert haben.

## Taeglicher Start

```powershell
cd "C:\Users\ralph\Documents\Master\5.Semester\Masterarbeit - lokal\TEIL1_Fach-Anwendungskompetenz\260524_Masterarbeit_Analyse"
.\.venv\Scripts\Activate.ps1
python -m ma_analyse gui
```

Relative Standardpfade:

- IDA-Importdaten: `data/ma_analyse/ida_imports/`
- Aufbereitete Daten: `data/ma_analyse/database/`
- Ausgaben: `data/ma_analyse/output/`
- Testausgaben: `data/test_output/`

## Sammelbefehle

Diese Befehle starten eine Oberflaeche, eine kombinierte Pipeline oder erzeugen
mehrere Referenzartefakte.

| Befehl | Zweck | Beispiel |
|---|---|---|
| `gui` | Grafische Oberflaeche starten | `python -m ma_analyse gui` |
| `all` | Standardausgaben kombiniert erzeugen | `python -m ma_analyse all` |
| `plot-template-examples` | Erzeugt die Beispielgalerie fuer alle Plot-Template-Werte | `python -m ma_analyse plot-template-examples` |

## Einzelbefehle

Diese Befehle fuehren einen konkreten Analyse-, Import-, Auswertungs- oder
Plot-Schritt aus.

| Befehl | Zweck | Beispiel |
|---|---|---|
| `prepare` | Rohdaten aufbereiten | `python -m ma_analyse prepare --export-format both` |
| `comfort` | Komfortplots und Analyseausgaben | `python -m ma_analyse comfort --output-type plot_analysis_overview` |
| `analyze-data` | Excel-Auswertung erstellen | `python -m ma_analyse analyze-data --series-layout separate` |
| `heating` | Heizlastdiagramme | `python -m ma_analyse heating --view year --heating-mode single` |
| `cooling` | Kuehllastdiagramme | `python -m ma_analyse cooling --view year --variant-mode single` |
| `plot-template` | Manuell anpassbare Diagramm-Vorlagen | `python -m ma_analyse plot-template --template heating-year --variants Dimensionierung --rooms "101 lobby"` |

## Referenz und Optionen

Das uebergreifende Befehls- und Ausgabeninventar steht unter
`docs/project/COMMAND_OUTPUT_INVENTORY.md`.

Gemeinsame Optionen:

- `--variants "Dimensionierung,I_04_DIM_Heizleistung_60%"`
- `--rooms "101 lobby,109 office"`
- `--output-root "data/test_output/<testart>"`
- `--run-id "<Lauf-ID>"`
- `--debug` / `--no-debug`

## GUI-Struktur

Die grafischen Oberflaechen fuer `ma_analyse` werden fachlich nach denselben
Bereichen sortiert:

- `Befehl`
- `Unterbefehl`
- `Template / Diagramm`
- optional `Overlay`
- `Varianten`
- `Raeume`
- `Export / Ausgabe`
- `Analyse starten`

`Optionen` ist kein eigener allgemeiner Bereich mehr. Einstellungen liegen dort,
wo sie fachlich gebraucht werden:

- `prepare`: Exportformat `csv`, `excel` oder `both`; danach Varianten.
- `analyze_data`: Excel-Ausgabe `separate` oder `combined`; danach Varianten
  und Raeume.
- `comfort`: Unterbefehl `t_op / rel_hum`; die vier bisherigen
  Comfort-Ausgaben `plot`, `plot_analysis`, `plot_overview` und
  `plot_analysis_overview` liegen unter `Template / Diagramm`.
- `heating` und `cooling`: Unterbefehl `bar` oder `timeline`;
  `single`/`compare` liegt unter `Export / Ausgabe`; Zeitansicht, Overlay und
  Diagrammanpassung liegen unter `Template / Diagramm`.
- `plot-template` in Tkinter und `plot-template-analyse` in Streamlit:
  alle Diagramme direkt unter `Unterbefehl`, `single`/`compare` unter
  `Export / Ausgabe`; Zeitansicht, Overlay-Aktivierung und die ausklappbare
  Diagrammanpassung liegen unter `Template / Diagramm`. Der eigene
  Overlay-Bereich erscheint direkt danach; der Overlay-Katalog wird erst nach
  Varianten- und Raumauswahl befuellt.
  Intern nutzt die Streamlit-Variante weiter den bestehenden Backend-Befehl
  `plot-template`.
- `single` erzeugt fuer jede ausgewaehlte Variante-Raum-Kombination ein
  eigenes Diagramm. `compare` erzeugt eine gemeinsame Vergleichsausgabe.
  Zeitreihen werden als gemeinsame Datenreihen gezeichnet; komplexe
  Sammeltemplates werden als Teilplots in einer Vergleichsgrafik gebuendelt.
- Achsengrenzen stehen standardmaessig auf `Automatisch`. Bei `Manuell`
  koennen Minimum und Maximum fuer primaere und – sofern vorhanden –
  sekundaere Y-Achsen gesetzt werden.
- Die Tkinter-GUI besitzt unten die Reihenfolge `Zuruecksetzen`,
  `Vorschau aktualisieren`, `Start`. Der Vorschau-Button nutzt aktuell den
  bestehenden Analysepfad mit den aktuellen Einstellungen; ein eingebettetes
  Bild-Vorschaufenster bleibt ein geplanter Folgeschritt.

Varianten werden als `Eine Variante`, `Mehrere Varianten` oder `Alle Varianten`
gewaehlt. Raeume werden als `Ein Raum`, `Mehrere Raeume` oder `Alle Raeume`
gewaehlt.

`plot-template` nutzt standardmaessig `data/test_output/` und startet mit `heating-year`.
Option `--plot-template-config <path>` erlaubt die Angabe eines benutzerdefinierten Plot-Template-Config-Verzeichnisses oder einer TOML-Datei.
Verfuegbare Templates sind:

- Heating: `heating-year`, `heating-overlay`, `heating-month`, `heating-week`, `heating-day`
- Cooling relativ: `cooling-year`, `cooling-month`, `cooling-week`, `cooling-day`
- Cooling absolut: `cooling-absolute-year`, `cooling-absolute-month`, `cooling-absolute-week`, `cooling-absolute-day`
- Barplots: `heating-bar`, `cooling-bar`
- Comfort: `comfort-plot`, `comfort-analysis`, `comfort-plot-overview`, `comfort-analysis-overview`
- Energiebilanz: `energy-balance-year`, `energy-balance-month`, `energy-balance-week`, `energy-balance-day`
- Interne Lasten: `internal-loads-year`, `internal-loads-month`, `internal-loads-week`, `internal-loads-day`, `internal-loads-monthly-sum`, `internal-loads-room-comparison`
- Raumklima: `thermal-room-climate-year`, `thermal-room-climate-month`, `thermal-room-climate-week`, `thermal-room-climate-day`

Dokumentierte Kurzbefehle:

| Kurzname | Technischer Befehl |
|---|---|
| `heating year` | `python -m ma_analyse plot-template --template heating-year --variants Dimensionierung --rooms "208 office"` |
| `heating year overlay` | `python -m ma_analyse plot-template --template heating-overlay --variants Dimensionierung --rooms "208 office"` |
| `cooling year` | `python -m ma_analyse plot-template --template cooling-year --variants Dimensionierung --rooms "208 office"` |
| `cooling year absolute` | `python -m ma_analyse plot-template --template cooling-absolute-year --variants Dimensionierung --rooms "208 office"` |

Beispiele:

```powershell
python -m ma_analyse plot-template --template heating-year --variants Dimensionierung --rooms "208 office"
python -m ma_analyse plot-template --template heating-overlay --variants Dimensionierung --rooms "208 office"
python -m ma_analyse plot-template --template heating-month --variants Dimensionierung --rooms "101 lobby" --month Jan
python -m ma_analyse plot-template --template heating-week --variants Dimensionierung --rooms "101 lobby" --week 7
python -m ma_analyse plot-template --template heating-day --variants Dimensionierung --rooms "101 lobby" --month Feb --day 15
python -m ma_analyse plot-template --template heating-bar --variants Dimensionierung --rooms "101 lobby,109 office,113 meeting"
python -m ma_analyse plot-template --template cooling-year --variants Dimensionierung --rooms "101 lobby"
python -m ma_analyse plot-template --template cooling-absolute-year --variants Dimensionierung --rooms "101 lobby"
python -m ma_analyse plot-template --template cooling-day --variants Dimensionierung --rooms "101 lobby" --month Jul --day 10
python -m ma_analyse plot-template --template cooling-absolute-day --variants Dimensionierung --rooms "101 lobby" --month Jul --day 10
python -m ma_analyse plot-template --template cooling-bar --variants Dimensionierung --rooms "101 lobby,109 office,113 meeting"
python -m ma_analyse plot-template --template comfort-plot --variants Dimensionierung --rooms "101 lobby"
python -m ma_analyse plot-template --template comfort-plot-overview --variants Dimensionierung --rooms "101 lobby,109 office,113 meeting,208 office,214 meeting"
python -m ma_analyse plot-template --template comfort-analysis --variants Dimensionierung --rooms "101 lobby"
python -m ma_analyse plot-template --template comfort-analysis-overview --variants Dimensionierung --rooms "101 lobby,109 office,113 meeting,208 office,214 meeting"
python -m ma_analyse plot-template --template energy-balance-day --variants Dimensionierung --rooms "101 lobby" --month Jul --day 20
python -m ma_analyse plot-template --template internal-loads-year --variants Dimensionierung --rooms "101 lobby"
python -m ma_analyse plot-template --template internal-loads-week --variants Dimensionierung --rooms "101 lobby" --week 7
python -m ma_analyse plot-template --template internal-loads-monthly-sum --variants Dimensionierung --rooms "101 lobby"
python -m ma_analyse plot-template --template internal-loads-room-comparison --variants Dimensionierung --rooms "101 lobby,109 office,113 meeting"
python -m ma_analyse plot-template --template thermal-room-climate-day --variants Dimensionierung --rooms "208 office" --month Jul --day 20
```

`heating-year` erzeugt den normalen Heating-Jahresplot nur mit Heizleistung.
`heating-overlay` ergaenzt den Heating-Jahresplot um Aussenlufttemperatur,
operative Temperatur und ein Sollwertband von 21 bis 26 °C. Per CLI koennen
die festen Overlays bei `heating-overlay` mit `--no-setpoint-band`,
`--no-outdoor-temperature` und `--no-operative-temperature` ausgeblendet werden.
Die weiteren Heating-Templates erzeugen technische Einzelraum-Zeitplots ohne
Overlays. Die relativen Cooling-Templates `cooling-year`, `cooling-month`,
`cooling-week` und `cooling-day` plotten `zone_energy_q_cool` exakt wie in
der CSV-Datei, inklusive Vorzeichen. Die absoluten Cooling-Templates
`cooling-absolute-year`, `cooling-absolute-month`, `cooling-absolute-week`
und `cooling-absolute-day` plotten den Betrag `abs(zone_energy_q_cool)` nach
oben.
`heating-bar` und `cooling-bar` bilden die Barplot-Ausgaben der Hauptbefehle
als Template-Ausgaben nach und erlauben mehrere Raeume. Comfort-Templates
erzeugen Einzelraum-PNGs oder PDF-Uebersichten aus den bestehenden
Behaglichkeitsdiagrammen.
Energy-Balance-Templates nutzen die Bilanzspalten `zone_energy_q_heat`,
`zone_energy_q_cool`, `zone_energy_qventil`, `zone_energy_qwcb`,
`zone_energy_ql_a`, `zone_energy_qintw`, `zone_energy_qwind`,
`zone_energy_q_occ`, `zone_energy_q_equip` und `zone_energy_q_light`.
Zusätzlich werden `temperatures_tairmean` aus der Raum-CSV und `tair` aus
`REPORT-AUX.prn` als gestrichelte Temperaturkurven geplottet.
Internal-Loads-Templates nutzen `zone_energy_q_occ`, `zone_energy_q_equip`
und `zone_energy_q_light` als Personen, Geraete und Beleuchtung. Year und
Month erzeugen Liniendiagramme mit diesen drei Datenreihen; Week und Day
erzeugen gestapelte Lastprofil-Balken in derselben Farbfolge. Das Template
`internal-loads-monthly-sum` erzeugt gestapelte Monatsenergien und
`internal-loads-room-comparison` vergleicht mehrere Raeume als gestapelte
Jahresenergien. Die Achse zeigt aktuell absolute Leistung `[W]`, keine
spezifische Leistung `[W/m²]`.
Thermal-Room-Climate-Templates kombinieren Sollwertband, interne Lasten total,
Lueftung, Raumkaelte, Raumlufttemperatur und Aussenlufttemperatur als feste
Raumklima-Vorlage. Die Leistungsachse zeigt aktuell absolute Leistung `[W]`.
Die Frage nach absoluten oder flaechenbezogen normierten Werten wird spaeter
nicht nur fuer einzelne Energy-Balance-Templates, sondern als allgemeine
`ma_analyse`-Normierungsstrategie fuer passende Auswertungen geplant.
Die Defaultwerte fuer Achsen, Sollwertband und Standard-Overlays liegen in
`src/ma_analyse/settings/plot_templates.toml` oder in separaten Dateien im
`src/ma_analyse/settings/plot_templates/`-Verzeichnis. Dort koennen einzelne
Template-Dateien wie `heating_year.toml` gepflegt werden. Nach Aenderungen
dort die GUI neu starten oder ueber `GUI aktualisieren` neu laden.

## Logs

Analysebefehle wie `prepare`, `comfort`, `analyze-data`, `heating`, `cooling`, `plot-template` und `all` schreiben pro Lauf automatisch eine Logdatei nach `logs/`. Die Logdatei enthaelt die Konsolenausgabe, Laufzeiten je Schritt und die Gesamtlaufzeit.
## Settings

```powershell
python -m ma_analyse.settings.naming --dry-run
```

Naming-, Ausgabeformat- und Plot-Template-Einstellungen liegen neben der zugehoerigen Logik unter `src/ma_analyse/settings/`.
