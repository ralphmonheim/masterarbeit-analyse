# Projektinput-Workflow

Diese Datei beschreibt, wie neue Projektdateien in der Entwicklungsphase
aufgenommen werden. Sie buendelt die Dokumentation zur lokalen
Entwicklungs-Inbox, ohne die dauerhafte Projektdokumentation mit temporaeren
Rohdateien zu vermischen.

## Ziel

Neue Dateien sollen zuerst sicher gesammelt, dann fachlich eingeordnet und erst
danach in bestehende Projekt-, Modul- oder lokale Datenordner uebernommen
werden.

## Ordnerrollen

| Bereich | Rolle | Versionierung |
| --- | --- | --- |
| `docs/project/` | dauerhafte Projektsteuerung, Plaene, Entscheidungen, Architektur, Routinen und Leitfaden | versioniert |
| `data/project_inbox/` | lokaler Eingang fuer neue oder unklare Entwicklungsdateien | nur Struktur versioniert, Inhalte ignoriert |
| `docs/project/plans/inbox/` | Plan-Inbox fuer fachlich uebernommene Projektplaene | versioniert |

`docs/project/` ist damit der gemeinsame Dokumentationsort fuer die Regeln.
`data/project_inbox/` bleibt der praktische Arbeitsort fuer temporaere Dateien,
weil dort auch grosse, rohe oder noch ungepruefte Dateien liegen koennen.

## Ablauf

1. Neue Dateien in den passendsten Unterordner unter
   `data/project_inbox/new/` legen.
2. Mit `projektinput aufnehmen` den Eingang pruefen lassen.
3. Eindeutig zuordenbare Inhalte in bestehende Zielordner uebernehmen.
4. Projektplaene nach `docs/project/plans/inbox/` uebernehmen und danach mit
   `plan aufnehmen` in Planindex und Planstatus einordnen.
5. Verarbeitete Originale nach `data/project_inbox/processed/` verschieben.
6. Unklare oder riskante Dateien in `data/project_inbox/needs_review/`
   belassen oder dorthin verschieben und eine Rueckfrage stellen.

## Eingangskategorien

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
| `new/unknown/` | nicht eindeutig zuordenbare Dateien | `needs_review/` nach Sichtung |

## Regeln

- Keine Dateien loeschen.
- Keine Fachfreigabe automatisch setzen.
- Nur eindeutig zuordenbare Dateien verschieben oder in bestehende Dokumente
  einarbeiten.
- Unklare oder riskante Dateien bleiben in `needs_review/`.
- Grosse, lokale oder rohe Eingangsdateien nicht nach `docs/project/`
  verschieben.
- `CHANGELOG.md` nur aktualisieren, wenn versionierte Struktur,
  Dokumentation oder produktive Dateien geaendert wurden.
