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
| `docs/project/plans/inbox/` | Plan-Inbox fuer intern erstellte oder nach Dokument-Preflight uebernommene Projektplaene | versioniert |

`docs/project/` ist damit der gemeinsame Dokumentationsort fuer die Regeln.
`data/project_inbox/` bleibt der praktische Arbeitsort fuer temporaere Dateien,
weil dort auch grosse, rohe oder noch ungepruefte Dateien liegen koennen.

## Ablauf

1. Neue Dateien in den passendsten Unterordner unter
   `data/project_inbox/new/` legen.
2. Mit `projektinput aufnehmen` den Eingang pruefen lassen.
3. Herkunft, Rechte, Schutzbedarf und beabsichtigte Verarbeitung zunaechst
   anhand bereinigter Metadaten durch den read-only `compliance_auditor`
   pruefen; den Dateiinhalt noch nicht uebergeben.
4. Bei gesperrter oder unbekannter Inhaltsverarbeitung das Original
   unveraendert am aktuellen Eingangspfad belassen. Nach `needs_review/`
   duerfen nur ein Metadatenhinweis oder eine ausdruecklich freigegebene
   Arbeitskopie gelangen.
5. Erst nach bestandenem Dokument-Preflight den minimal notwendigen Inhalt
   pruefen. Nur im dokumentierten `green`-Umfang extrahieren, verschieben oder
   einarbeiten. `yellow` bleibt bis zur dokumentierten Bestaetigung und allen
   geforderten Belegen gesperrt; `red` stoppt und `unknown` bleibt bis zur
   Klaerung gesperrt.
6. Eindeutig zulaessige und zuordenbare Inhalte in bestehende Zielordner
   uebernehmen.
7. Projektplaene erst nach bestandenem Dokument-Preflight nach
   `docs/project/plans/inbox/` uebernehmen und danach mit
   `plan aufnehmen` in Planindex und Planstatus einordnen.
8. Verarbeitete Originale nach `data/project_inbox/processed/` verschieben.
9. Bei unklaren oder blockierten Objekten eine Rueckfrage stellen und das
   Original bis zur Klaerung nicht verschieben.

## Compliance-Preflight

Der Preflight richtet sich nach `docs/compliance/README.md`, den gemeinsamen
Regeln unter `docs/compliance/shared/` und dem betroffenen Fachprofil. Der
`compliance_auditor` prueft read-only und erteilt keine eigene Rechts-,
Vertrags- oder Fachfreigabe.

Geprueft werden mindestens:

- bekannte Herkunft und Eigentum,
- anwendbare Lizenz und erlaubte Verarbeitung,
- personenbezogene oder vertrauliche Inhalte,
- Repository-, Cloud-, Weitergabe- und Veroeffentlichungsrechte,
- Lizenz- oder Zugangsdaten sowie erforderliche externe Genehmigungen.

Der Hauptagent besitzt die Prozessentscheidung, prueft die Agentenempfehlung
und dokumentiert die anwendbare `compliance_decision` mit Belegreferenz im
passenden Fachregister unter `docs/compliance/` oder im Metadaten-Audit unter
`logs/compliance/decisions.jsonl`. Eine Agentenempfehlung allein ist keine
Freigabe. Materielle oder gelbe Entscheidungen benoetigen eine dokumentierte
menschliche Bestaetigung und alle geforderten Rechtebelege.

Ein Compliance-Blocker stoppt nur das betroffene Objekt. Eine blosse
Risikoakzeptanz ersetzt keinen Rechte- oder Freigabenachweis; unabhaengige,
unkritische Dateien derselben Aufnahme duerfen weiterbearbeitet werden.
`unknown` bezeichnet einen gesperrten fehlenden-Nachweis-Status, nicht ein
bestaetigtes Verbot. `red` bezeichnet eine belegte Stop-Regel.

Bei neuen Plaenen wird zwischen Dokument und geplanter Umsetzung
unterschieden: Ein Risiko der spaeteren Umsetzung wird als sichtbare
Voraussetzung in Planindex oder Planstatus dokumentiert. Ist bereits die
Verarbeitung oder Repository-Ablage des Plandokuments selbst gesperrt, wird
seine weitere Aufnahme gestoppt.

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
| `new/unknown/` | nicht eindeutig zuordenbare Dateien | Original bleibt bis zur Klaerung unveraendert; nur Metadatenhinweis oder freigegebene Arbeitskopie nach `needs_review/` |

## Regeln

- Keine Dateien loeschen.
- Keine Fach- oder Compliance-Freigabe automatisch setzen.
- Nur eindeutig zuordenbare Dateien verschieben oder in bestehende Dokumente
  einarbeiten.
- Vor Extraktion, Verschieben, Einarbeiten oder externer Verarbeitung den
  Compliance-Preflight ausfuehren.
- Unklare, nicht ausreichend belegte oder blockierte Originale bleiben
  unveraendert an ihrem aktuellen Eingangspfad.
- `needs_review/` enthaelt nur Metadatenhinweise oder nach ausdruecklicher
  Freigabe erzeugte Arbeitskopien; das Original bleibt erhalten.
- Grosse, lokale oder rohe Eingangsdateien nicht nach `docs/project/`
  verschieben.
- Geschuetzte Volltexte, Lizenz- oder Zugangsdaten und vertrauliche
  Projektdateien nicht in das Repository uebernehmen.
- `CHANGELOG.md` nur aktualisieren, wenn versionierte Struktur,
  Dokumentation oder produktive Dateien geaendert wurden.
