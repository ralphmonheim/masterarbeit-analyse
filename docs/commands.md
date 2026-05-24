# Befehle

Standard-Einstieg ist:

```powershell
python -m ma_analyse <befehl> [optionen]
```

## Start

```powershell
cd "C:\Users\ralph\Documents\Master\5.Semester\Masterarbeit - lokal\TEIL1_Fach-Anwendungskompetenz\260524_Masterarbeit_Analyse"
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
python -m ma_analyse gui
```

Relative Standardpfade:

- Rohdaten: `data/input/`
- Aufbereitete Daten: `data/database/`
- Ausgaben: `data/output/`
- Testausgaben: `data/test_output/`

## Hauptbefehle

| Befehl | Zweck | Beispiel |
|---|---|---|
| `gui` | Grafische Oberflaeche starten | `python -m ma_analyse gui` |
| `prepare` | Rohdaten aufbereiten | `python -m ma_analyse prepare --export-format both` |
| `comfort` | Komfortplots und Analyseausgaben | `python -m ma_analyse comfort --output-type plot_analysis_overview` |
| `analyze-data` | Excel-Auswertung erstellen | `python -m ma_analyse analyze-data --series-layout separate` |
| `heating` | Heizlastdiagramme | `python -m ma_analyse heating --view year --heating-mode single` |
| `cooling` | Kuehllastdiagramme | `python -m ma_analyse cooling --view year --variant-mode single` |
| `all` | Standardausgaben kombiniert erzeugen | `python -m ma_analyse all` |

Gemeinsame Optionen:

- `--variants "Dimensionierung,I_04_DIM_Heizleistung_60%"`
- `--rooms "101 lobby,109 office"`
- `--output-root "data/test_output/<testart>"`
- `--run-id "<Lauf-ID>"`
- `--debug` / `--no-debug`


## Logs

Analysebefehle wie `prepare`, `comfort`, `analyze-data`, `heating`, `cooling` und `all` schreiben pro Lauf automatisch eine Logdatei nach `logs/`. Die Logdatei enthaelt die Konsolenausgabe, Laufzeiten je Schritt und die Gesamtlaufzeit.
## Settings

```powershell
python -m ma_analyse.settings.naming --dry-run
```

Naming- und Ausgabeformat-Dokumente liegen neben der zugehoerigen Logik unter `src/ma_analyse/settings/`.


