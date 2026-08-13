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
| `docs/project/plans/inbox/` | Plan-Inbox fuer intern erstellte oder aus der Entwicklungs-Inbox uebernommene Projektplaene | versioniert |

`docs/project/` ist damit der gemeinsame Dokumentationsort fuer die Regeln.
`data/project_inbox/` bleibt der praktische Arbeitsort fuer temporaere Dateien,
weil dort auch grosse, rohe oder noch ungepruefte Dateien liegen koennen.

## Ablauf

1. Alle neuen Dateien direkt unter `data/project_inbox/new/` ablegen.
2. Mit `input aufnehmen` beide Eingaenge pruefen lassen.
3. Dateiname, Erweiterung und die fuer die Zuordnung erforderlichen Metadaten
   erfassen.
4. Eindeutig erkannte Projektplaene sofort aus `data/project_inbox/new/` nach
   `docs/project/plans/inbox/` verschieben und mit `plan aufnehmen` in
   Planindex und Planstatus einordnen. Diese Planaufnahme benoetigt keine
   weitere Umsetzungsfreigabe.
5. Danach den Zuordnungsbericht mit allen Dateien, Kategorien,
   Zielvorschlaegen, Planaufnahmen, Literaturbezug und offenen Punkten
   erstellen.
6. Eindeutig zuordenbare Nicht-Plan-Dateien erst nach ausdruecklicher
   Umsetzungsfreigabe in bestehende Zielordner uebernehmen oder in passende
   Dokumente einarbeiten.
7. Uebernommene Literatur anschliessend ueber den Literatur-Workflow
   inventarisieren, analysieren und als Projektuebertragung einordnen.
8. Verarbeitete Originale nach `data/project_inbox/processed/` verschieben.
9. Bei unklarer Zuordnung eine Rueckfrage stellen und das Original bis zur
   Klaerung nicht verschieben.
10. Nach jeder Planaufnahme oder Dokumentaenderung den Navigator aktualisieren
    und validieren.
11. Vor `update repo` den gesamten vorgesehenen Repository-Stand auf Rechte,
   Schutzbedarf und Veroeffentlichungsgrenzen pruefen.

## Eingangskategorien

| Ermittelte Kategorie | Typische Inhalte | Zielbereich |
| --- | --- | --- |
| Dokumentation | Plaene, Entscheidungsnotizen, Architektur- oder Moduldoku | `docs/project/`, `docs/*/` |
| Wetter | TRY-Dateien, Wetter-Handbuecher, lokale Geodaten | `data/ma_weather/input/`, `data/ma_weather/geodata/` |
| Gebaeude | IFC, Rhino, CAD, Gebaeudeinput-Notizen | `data/ma_building/input/` |
| Analyse | IDA-ICE-Analyse-Rohdaten | `data/ma_analyse/ida_imports/` |
| Varianten | Variantenimporte und Simulationsuebergaben | `data/ma_variants/imports/`, `data/ma_variants/ida_exports/` |
| Kataloge | Produkt-, Material-, Quellen- und Datenblattdateien | `data/catalogs/`, `config/ma_variants/` |
| Parameter | Parameterkonzepte, Snapshots, lokale Parameterdateien | `config/ma_parameters/`, `data/ma_parameters/config/` |
| Zonen und Technik | Zonen-, Nutzungs- und Techniksystemdaten | `config/ma_zones/`, `config/ma_technical/` |
| Unklar | nicht eindeutig zuordenbare Dateien | Original bleibt bis zur Klaerung unter `new/`; nur Metadatenhinweis oder freigegebene Arbeitskopie nach `needs_review/` |

## Regeln

- Keine Dateien loeschen.
- Keine Fach- oder Compliance-Freigabe automatisch setzen.
- Nur eindeutig erkennbare Plan-Dateien duerfen ohne weitere Freigabe
  verschoben und eingeordnet werden. Alle anderen Dateien duerfen erst nach
  `Freigabe zur Umsetzung` verschoben oder eingearbeitet werden.
- Die Zuordnung erfolgt erst beim Scan aus Dateiname, Erweiterung und
  zulaessigen Metadaten; `new/` enthaelt keine Kategorie-Unterordner.
- Unklare Originale bleiben
  unveraendert an ihrem aktuellen Eingangspfad.
- `needs_review/` enthaelt nur Metadatenhinweise oder nach ausdruecklicher
  Freigabe erzeugte Arbeitskopien; das Original bleibt erhalten.
- Grosse, lokale oder rohe Eingangsdateien nicht nach `docs/project/`
  verschieben.
- Die Pruefung auf geschuetzte Volltexte, Lizenz- oder Zugangsdaten und
  vertrauliche Projektdateien erfolgt beim `update repo`.
- `CHANGELOG.md` nur aktualisieren, wenn versionierte Struktur,
  Dokumentation oder produktive Dateien geaendert wurden.
