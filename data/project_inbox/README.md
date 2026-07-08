# Entwicklungs-Inbox

Dieser Ordner ist ein temporaerer Sammelplatz fuer neue Projektdateien in der
Entwicklungsphase. Er ersetzt keine Fachordner. Inhalte unter `new/`,
`processed/` und `needs_review/` bleiben lokal und werden nicht versioniert.

## Nutzung

1. Neue Dateien in den passendsten Unterordner unter `new/` legen.
2. Codex mit `projektinput aufnehmen` den Ordner scannen lassen.
3. Eindeutige Dateien werden in bestehende Zielordner verteilt.
4. Verarbeitete Originale kommen nach `processed/`.
5. Unklare Dateien bleiben in `needs_review/` und werden erst nach Rueckfrage
   verschoben.

## Eingangsordner

| Ordner | Typische Inhalte | Zielbereich |
| --- | --- | --- |
| `new/docs/` | Plaene, Entscheidungsnotizen, Architektur- oder Moduldoku | `docs/project/`, `docs/*/` |
| `new/weather/` | TRY-Dateien, Wetter-Handbuecher, lokale Geodaten | `data/ma_weather/input/`, `data/ma_weather/geodata/` |
| `new/building/` | IFC, Rhino, CAD, Gebaeudeinput-Notizen | `data/ma_building/input/` |
| `new/analyse/` | IDA-ICE-Analyse-Rohdaten | `data/ma_analyse/ida_imports/` |
| `new/variants/` | Variantenimporte und Simulationsuebergaben | `data/ma_variants/imports/`, `data/ma_variants/ida_exports/` |
| `new/catalogs/` | Produkt-, Material-, Quellen- und Datenblattdateien | `data/catalogs/`, `config/ma_variants/` |
| `new/parameters/` | Parameterkonzepte, Snapshots, lokale Parameterdateien | `config/ma_parameters/`, `data/ma_parameters/config/` |
| `new/zones_technical/` | Zonen-, Nutzungs- und Techniksystemdaten | `config/ma_zones/`, `config/ma_technical/` |
| `new/unknown/` | Nicht eindeutig zuordenbare Dateien | `needs_review/` nach Sichtung |

## Grenzen

- Wetterdatensaetze werden nur in den lokalen Wetter-Eingang vorbereitet. Die
  Registrierung und Freigabe bleibt beim bestehenden Wetter-Scan und
  Pruefworkflow.
- Plaene werden nicht automatisch umgesetzt. Sie landen zuerst in der
  Plan-Inbox und werden danach wie bisher geprueft.
- Produktive Projektdateien werden nur bei eindeutiger Zuordnung oder nach
  Rueckfrage geaendert.
