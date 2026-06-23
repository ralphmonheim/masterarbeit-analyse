# P008 ma_weather Gesamtplan

Stand: 2026-06-23
Status: Aktiv
Plannummer: P008
Bezug: P007, P010, P015, P018, P021, P027, archivierter P002

## Aenderungsvermerk zur Zusammenfuehrung

Datum der Zusammenfuehrung: 2026-06-23

Dieser Plan fuehrt die bisherige Plannummer `P008` weiter. Es wurde keine neue
Plannummer vergeben.

Zusammengefuehrte Ausgangsplaene:

- `docs/project/plans/inbox/260621_Plan_P008_Wettermodul_Abschluss_P007_Anbindung.md`
- `docs/project/plans/inbox/Implementierungsplan_ma_weather.md`

Archivierte Ausgangsplaene:

- `docs/project/archive/plans/260621_Plan_P008_Wettermodul_Abschluss_P007_Anbindung.md`
- `docs/project/archive/plans/Implementierungsplan_ma_weather.md`

Wesentliche neue Inhalte:

- Stadt als primaerer Auswahlpunkt fuer Wetterdaten.
- Automatische Ableitung von Klimaregion und TRY-Referenzstandort.
- Informative Klimaregionenkarte im UI-Assetbereich.
- Filterung verfuegbarer Wetterdatensaetze ueber den TRY-Referenzstandort.
- Getrennte Behandlung von Standort, Referenzstandort und Wetterdatensatz.
- Eigener Bearbeitungsbereich fuer offene, unvollstaendige und fehlerhafte
  Wetterdatensaetze.
- Dauerhafte Import-Logs mit eindeutiger Verknuepfung zu Import,
  Validierungsbericht und Wetterdatensatz.
- Bewusstes Aktivieren gueltiger Importe und bewusstes Setzen des
  Projekt-Defaults.
- Ziel-Datenmodell mit stabilen IDs und spaeterer Alembic-Migration nach
  vorheriger Seed- und Feldnamenklaerung.

Ersetzte oder entfernte Inhalte:

- Der alte P008-Abschlussplan wird nicht mehr als aktuelle Grundlage genutzt.
- Der unnummerierte Implementierungsplan wird nicht als paralleler Plan
  weitergefuehrt.
- Vorgeschlagene Parallelstrukturen wie `data/weather/` und
  `ui/streamlit/pages/` werden nicht uebernommen.
- `weather_key` bleibt als bestehender Kompatibilitaets- und
  Anzeigeschluessel erhalten, wird aber langfristig nicht als alleiniger
  Primaerschluessel geplant.

Weiterhin offene Entscheidungen:

- Endgueltige Feldnamen und ID-Schreibweise fuer das Datenbankmodell.
- Seed-Quelle fuer Stadt-, Klimaregions- und Referenzstandortdaten.
- Exakte Pflichtspalten, Einheiten und Wertebereiche je Wetterformat.
- Umgang mit Sommer- und Winterdatensaetzen.
- Umfang normalisierter Kopien und spaeterer Exporte.
- Definition kritischer Wetterereignisse fuer P021.

## Ziel

`ma_weather` soll Wetterdaten als eigenstaendiges Eingabemodul verwalten,
validieren, analysieren und nur freigegebene Wetterinformationen an
`ma_parameters` uebergeben.

Der Plan verbindet den bestehenden lauffaehigen TRY-Stand mit dem Zielbild fuer
Standortauswahl, Importverwaltung, Statusmodell, Streamlit-Bedienung,
Datenhaltung und spaetere Parameteruebergabe.

## Bestehender Stand

- `src/ma_weather/` ist als importierbares Paket vorhanden.
- `WeatherDataset` und YAML-Katalog liegen in `src/ma_weather/weather_catalog.py`.
- Der Beispielkatalog liegt unter
  `config/ma_weather/datasets/example_weather_datasets.yaml`.
- Reale TRY-Dateien liegen lokal unter `data/ma_weather/input/` und werden nicht
  versioniert.
- Aufbereitete Wetterdaten, Diagramme, Exporte und Berichte liegen im
  Modulbereich `data/ma_weather/`.
- TRY-Import, Validierung, Kennwerte, Diagramme, Markdown-Bericht und Runner
  sind vorhanden.
- `TRY_FFM_2015` wurde real mit 8760 Stunden erfolgreich geprueft.
- Streamlit kann aktive `weather_key` Werte auswaehlen, Wetteranalysen starten
  und Ergebnisse anzeigen.
- `ma_core` stellt Quellenmodell, SHA-256 und JSONL-Sitzungslogs bereit.
- `ma_validation` stellt strukturierte Diagnosen, Freigabestatus und
  Freigabeentscheidungen bereit.
- Wetterlaeufe und Freigabeentscheidungen werden aktuell unter
  `logs/sessions/<session_id>.jsonl` protokolliert.

## Konsolidierte Entscheidungen

### Stadt ist primaerer Auswahlpunkt

Der Nutzer waehlt in der regulaeren UI zuerst eine Stadt. Die Klimaregion wird
nicht separat ausgewaehlt.

Begruendung: Die Klimaregion ist eine abgeleitete Information. Eine separate
Auswahl wuerde fehlerhafte Kombinationen aus Stadt, Klimaregion und
Referenzstandort ermoeglichen.

Folge: Klimaregion und TRY-Referenzstandort werden angezeigt, aber in der
regulaeren Auswahl nicht direkt editiert.

### Klimaregionenkarte ist informativ

Die Karte der Klimaregionen wird in der ersten Ausbaustufe nur informativ in
Streamlit angezeigt. Sie wird nicht als interaktive Auswahlkomponente geplant.

Asset-Entscheidung: Die Karte liegt im UI-Bereich, voraussichtlich unter
`src/ma_ui/assets/weather/`.

Begruendung: Die UI ist der primaere Nutzungsort. Eine Ablage unter
`docs/ma_weather/` waere fuer Dokumentation geeignet, aber nicht als aktive
UI-Assetstruktur.

### Standort und Wetterdatensatz bleiben getrennt

Standorte, Klimaregionen, Referenzstandorte und Wetterdatensaetze werden
fachlich getrennt geplant. Ein Referenzstandort kann mehrere Datensaetze
besitzen, zum Beispiel Gegenwart, Zukunftsszenario, Sommer- oder Winterfall.

### Nur aktive und validierte Datensaetze sind regulaer auswaehlbar

Die normale Wetterauswahl zeigt nur Datensaetze, die fachlich validiert und
bewusst aktiviert wurden.

Offene, unvollstaendige oder fehlerhafte Datensaetze duerfen nicht an
`ma_parameters`, Varianten oder Simulationen uebergeben werden.

### Import, Validierung, Aktivierung und Projekt-Default sind getrennt

Ein Import setzt keinen Projekt-Default.

Ein gueltiger Import wird auch nicht automatisch aktiviert. Die Zielkette ist:

```text
importiert -> validiert -> aktiv -> Projekt-Default
```

Aktivierung und Projekt-Default sind bewusste Nutzeraktionen. Dadurch bleibt ein
bestehender Projektzustand stabil und neue Importe koennen zuerst geprueft
werden.

### Relative Pfade sind verpflichtend

Datenbank, Kataloge und Konfigurationen speichern relative Projektpfade. Absolute
benutzerspezifische Windows-Pfade duerfen nicht als dauerhafte Referenz
gespeichert werden.

### Bestehende Projektstruktur hat Vorrang

Der Plan erzeugt keine parallele Struktur neben dem Projektbestand.

Verbindliche Zielbereiche:

- Fachlogik: `src/ma_weather/`
- Streamlit UI: `src/ma_ui/`
- Wetterkonfiguration: `config/ma_weather/`
- Wetterdaten: `data/ma_weather/`
- Sitzungs- und Prozesslogs: `logs/`
- Plaene und Doku: `docs/`

Nicht uebernommen werden:

- `data/weather/`
- `ui/streamlit/pages/`

### Datenmodell wird geplant, Migration folgt separat

Das neue Wetter-Datenmodell wird in P008 fachlich verbindlich beschrieben, aber
nicht sofort als Alembic-Migration umgesetzt.

Vor einer Migration sind zu klaeren:

- endgueltige Feldnamen,
- ID-Schreibweise,
- Seed-Quelle fuer Standortdaten,
- Verhaeltnis von YAML-Katalog und Datenbank,
- Statuswerte,
- Projektbezug und spaetere `ma_parameters`-Anbindung.

## Modulgrenzen

### `ma_weather`

`ma_weather` ist verantwortlich fuer:

- Standort- und Wetterdatensatzkatalog,
- TRY-Referenzstandortzuordnung,
- Dateiimport,
- Parser,
- technische und fachliche Validierung,
- Import-Log,
- Validierungsbericht,
- Wetteranalyse,
- Wetterdiagramme,
- Wetterdatensatzvergleich,
- Aktivierung und Projekt-Default fuer Wetterdaten.

### `ma_parameters`

`ma_parameters` uebernimmt spaeter nur freigegebene Wetterdaten aus
`ma_weather`. Die Uebergabe erfolgt nicht direkt von offenen Importen.

Langfristig soll `ma_parameters` eine zentrale Parameterdarstellung erzeugen,
die Wetterparameter, Projektparameter, Gebaeude, Zonen und Technik
zusammenfuehrt.

### `ma_variants`

`ma_variants` greift nicht direkt auf offene Wetterdaten zu.

Varianten duerfen spaeter den Projekt-Default bewusst ueberschreiben, aber nur
mit aktiven und validierten Wetterdatensaetzen. Jeder Override muss
nachvollziehbar dokumentiert werden.

### `ma_validation`

`ma_validation` bleibt fuer strukturierte Meldungen, Freigabestatus und spaetere
Checkpoints zustaendig. `ma_weather` nutzt diese Modelle, statt eigene
inkompatible Freigabelogik einzufuehren.

## Datenmodell Zielbild

Das Zielmodell wird in P008 als fachliche Grundlage geplant. Es ist noch keine
freigegebene Migration.

Geplante Entitaeten:

| Entitaet | Zweck |
|---|---|
| `weather_regions` | Klimaregionen 1 bis 15 mit Referenzstandort |
| `weather_locations` | Stadtliste mit Region und Referenzstandort |
| `weather_datasets` | Wetterdatensaetze je Referenzstandort |
| `weather_imports` | Importvorgaenge mit Log- und Berichtspfaden |
| `project_weather_selection` | aktuelle Projekt-Wetterauswahl |

Geplante stabile IDs:

- `region_id`
- `location_id`
- `reference_location_id`
- `dataset_id`
- `import_id`

Bestehende Schluessel wie `weather_key`, TRY-Ordnungsnummern und Legacy-Codes
bleiben fuer Anzeige, Rueckverfolgbarkeit und Kompatibilitaet erhalten. Sie
werden langfristig nicht als alleinige Primaerschluessel geplant.

## Standort- und Referenzlogik

Regulaerer Ablauf:

```text
Stadt auswaehlen
    ->
Standortdatensatz laden
    ->
Klimaregion ermitteln
    ->
TRY-Referenzstandort ermitteln
    ->
aktive und validierte Wetterdatensaetze laden
    ->
Datensatz auswaehlen
    ->
Szenario und Bezugszeitraum anzeigen
    ->
optional aktivieren oder Projekt-Default setzen
```

Die Klimaregion wird in der UI angezeigt, aber nicht separat ausgewaehlt.

## Import- und Statusmodell

### Workflow-Status

Geplante Statuswerte:

- `uploaded`
- `format_detected`
- `metadata_pending`
- `duplicate_check_pending`
- `validation_pending`
- `validation_running`
- `validation_failed`
- `validated`
- `activation_pending`
- `active`
- `import_incomplete`
- `processing_error`
- `archived`
- `deleted`

### Validierungsstatus

Geplante Statuswerte:

- `not_checked`
- `valid`
- `valid_with_warnings`
- `invalid`
- `check_failed`

### Duplikatstatus

Geplante Statuswerte:

- `not_checked`
- `no_duplicate`
- `exact_duplicate`
- `possible_duplicate`
- `new_version_confirmed`

### Freigaberegel

Ein Datensatz darf nur aktiviert werden, wenn:

- Pflichtmetadaten vollstaendig sind,
- Parser erfolgreich war,
- keine blockierenden Validierungsfehler vorhanden sind,
- Duplikatpruefung abgeschlossen ist,
- Originaldatei dauerhaft gespeichert ist,
- Validierungsbericht vorhanden ist,
- Import-Log vorhanden ist,
- Datenbank- oder Katalogeintrag vollstaendig ist.

## Import-Log und Nachweise

Jeder Import erzeugt ein dauerhaftes Log, auch bei Fehlern oder Abbruch.

Das bestehende `logs/sessions/<session_id>.jsonl` bleibt Grundlage fuer
Sitzungsereignisse. P008 plant darauf aufbauend einen eindeutigeren
Importnachweis mit `import_id`, der Import-Log, Validierungsbericht und
Wetterdatensatz verbindet.

Mindestinhalt:

- Import-ID,
- Start und Ende,
- Nutzer oder Prozess,
- Softwareversion,
- Parser-Version,
- Quelldatei,
- Dateigroesse,
- Dateiformat,
- Kodierung,
- SHA-256,
- erkannte und bestaetigte Metadaten,
- Duplikatpruefung,
- technische und fachliche Validierung,
- Fehler, Warnungen und Hinweise,
- Dateisystemaktionen,
- Datenbank- oder Katalogaktionen,
- Rollback-Aktionen,
- Abschlussstatus.

## Dateisystem

Bestehende Ordner bleiben verbindlich:

| Pfad | Zweck |
|---|---|
| `data/ma_weather/input/` | lokale Originaldateien |
| `data/ma_weather/database/` | aufbereitete Wetterdaten |
| `data/ma_weather/output/` | Wetterdiagramme |
| `data/ma_weather/reports/` | Markdown- und Validierungsberichte |
| `data/ma_weather/exports/` | spaetere strukturierte Exporte |
| `logs/sessions/` | bestehende JSONL-Sitzungslogs |

Bei spaeterem Importausbau koennen innerhalb von `data/ma_weather/` ergaenzt
werden:

- `source/`
- `normalized/`
- `validation_reports/`
- `import_logs/`
- `temporary/`
- `archive/`

Diese Unterordner werden erst angelegt, wenn ein freigegebener Umsetzungsslice
sie benoetigt.

## Streamlit UI Zielbild

Streamlit ist die primaere Benutzeroberflaeche. Fachlogik, Parser,
Validierung, Speicherung und Logging bleiben ausserhalb der UI.

Geplante UI-Bereiche innerhalb der bestehenden `ma_ui`-Struktur:

- Standort und Wetterauswahl,
- Wetteranalyse,
- Wetterdatenkatalog,
- offene Wetterdatensaetze,
- Wetterdatensatz importieren,
- Import- und Validierungsprotokolle.

Die erste Umsetzung soll die vorhandene Wetterseite schrittweise erweitern,
nicht durch eine zweite UI-Struktur ersetzen.

## Offene Wetterdatensaetze

Offene, unvollstaendige und fehlerhafte Datensaetze bleiben sichtbar.

Geplante Funktionen:

- Uebersicht nach Status, Import-ID, Referenzstandort und Fehleranzahl,
- Filter nach Referenzstandort, Klimaregion, Workflow-Status,
  Validierungsstatus und Importdatum,
- Metadaten bearbeiten,
- Datei-Vorschau,
- erneut validieren,
- Duplikatpruefung wiederholen,
- Import fortsetzen,
- Datei ersetzen,
- als neue Version importieren,
- archivieren,
- loeschen nur nach klaren Regeln,
- Import-Log und Validierungsbericht anzeigen.

Offene Datensaetze duerfen nicht als Projekt-Default verwendet, nicht an
`ma_parameters` uebergeben und nicht fuer Varianten oder Simulationen genutzt
werden.

## Wetteranalyse

Bestehende Analysefunktionen bleiben erhalten:

- Jahresverlauf der Aussentemperatur,
- Temperatur-Heatmap,
- monatliche Globalstrahlung,
- monatliche Heiz- und Kuehlgradstunden,
- Windrose,
- Temperatur-Feuchte-Diagramm,
- Kennwerte,
- Markdown-Bericht.

Geplante Erweiterungen:

- Extremtage,
- Vergleich von Gegenwarts- und Zukunftsdatensaetzen,
- Vergleich mehrerer Referenzstandorte,
- fachliche Diagrammpruefung gegen Masterarbeitslayout,
- kritische Wetterereignisse fuer P021.

## Umsetzungsschritte

### Phase 1 Bestandsanalyse und Konsolidierung

- vorhandene Wetterstruktur gegen diesen Plan abgleichen,
- alte Ausgangsplaene archivieren,
- Planindex und Planstatus aktualisieren,
- keine produktive Codeaenderung in diesem Schritt.

### Phase 2 Realtests

- `TRY_FFM_2045`, `TRY_MUC_2015`, `TRY_MUC_2045`, `TRY_HAM_2015` und
  `TRY_HAM_2045` lokal ausfuehren,
- Validierung, Stundenanzahl, CSV, Diagramme, Bericht und Log dokumentieren,
- lokale fehlende TRY-Dateien klar melden, ohne synthetische Dateien anzulegen.

### Phase 3 Standort- und Seed-Konzept

- Standort- und Klimaregionsdaten aus dem Implementierungsplan pruefen,
- Seed-Format festlegen,
- ID-Schreibweise festlegen,
- YAML-/CSV-Zwischenstand planen,
- Migration erst nach Freigabe vorbereiten.

### Phase 4 Streamlit Standortauswahl

- UI-Assetbereich fuer Wetterkarte vorbereiten,
- Stadt-Suchfeld oder Selectbox planen,
- Klimaregion und Referenzstandort automatisch anzeigen,
- aktive und validierte Datensaetze nach Referenzstandort filtern,
- leere Zustaende behandeln.

### Phase 5 Import-Grundlage

- Upload- oder Dateiimport-Slice planen,
- Import-ID erzeugen,
- Datei temporaer ablegen,
- SHA-256 berechnen,
- Format und Metadaten erkennen,
- Import-Log dauerhaft anlegen,
- Fehlerbehandlung dokumentieren.

### Phase 6 Validierung und offene Datensaetze

- technische und fachliche Validierung erweitern,
- Validierungsbericht speichern,
- Statusmodell anwenden,
- offene Datensaetze in Streamlit sichtbar machen,
- erneute Validierung und Metadatenbearbeitung planen.

### Phase 7 Aktivierung und Projekt-Default

- bewusste Aktivierung validierter Datensaetze umsetzen,
- bewusste Auswahl des Projekt-Defaults umsetzen,
- Uebergabegrenze zu `ma_parameters` dokumentieren,
- Sperren fuer offene Datensaetze pruefen.

### Phase 8 Analyse und P021-Ereignisse

- Diagrammgestaltung fachlich pruefen,
- Extremtage und kritische Wetterereignisse definieren,
- Zeitfenster reproduzierbar beschreiben,
- Schnittstelle zu P021 vorbereiten.

### Phase 9 Tests und Dokumentation

- Unit-Tests fuer Parser, Katalog, Validierung, Statuswechsel und Services,
- Integrationstests fuer reale lokale TRY-Dateien, soweit vorhanden,
- UI-Tests fuer Stadtwahl, offene Datensaetze und Default-Wechsel, soweit
  praktikabel,
- Dokumentation unter `docs/ma_weather/` und Planstatus aktualisieren.

## Tests und Abschlusskriterien

- Alle sechs aktiven Jahresdatensaetze sind real dokumentiert geprueft oder
  fehlende lokale Dateien sind nachvollziehbar gemeldet.
- Pflichtspalten, eindeutiger Zeitindex und 8760 Stunden sind je Jahresdatei
  nachvollziehbar.
- Fehlende optionale Spalten fuehren zu strukturierten Warnungen.
- Stadtwahl fuehrt eindeutig zu Klimaregion und Referenzstandort.
- Die regulare Auswahl zeigt nur aktive und validierte Datensaetze.
- Offene Datensaetze besitzen einen eigenen Bearbeitungsbereich.
- Jeder Import erzeugt ein dauerhaftes Log.
- Import-Log, Validierungsbericht und Wetterdatensatz sind eindeutig
  verknuepft.
- Ein neuer Import aktiviert keinen Datensatz automatisch und setzt keinen
  Projekt-Default automatisch.
- `ma_weather` uebergibt nur freigegebene Daten an `ma_parameters`.
- Offene Wetterdatensaetze koennen nicht fuer Varianten oder Simulationen
  genutzt werden.
- Fachlogik bleibt unabhaengig von Streamlit und Tkinter.
- Relative Pfade werden dauerhaft verwendet.

## Abgrenzung

- Keine synthetischen TRY-Dateien anlegen.
- Keine direkte Kopplung von `ma_weather` an `ma_variants`.
- Keine Wetterdiagramme in `ma_analyse` verschieben.
- Keine automatische IDA-ICE-Steuerung.
- Keine parallele Projektstruktur neben `src/ma_weather/` und `src/ma_ui/`.
- Keine Alembic-Migration ohne separaten freigegebenen Umsetzungsslice.
- Keine automatische Aktivierung oder Default-Setzung nach Import.

## Offene fachliche und technische Punkte

- Tatsachliches Format aller vorhandenen TRY-Dateien.
- Notwendige Pflichtspalten je Dateiformat.
- Interne Einheiten und erlaubte Wertebereiche.
- Genaue Definition von Extremtagen und kritischen Wetterereignissen.
- Gewuenschte Klimaszenario-Bezeichnungen.
- Gewuenschte Bezugszeitraeume.
- Umgang mit Sommer- und Winterdatensaetzen.
- Fachliche Pruefung einzelner Stadtzuordnungen.
- Endgueltige ID-Schreibweise.
- Aufbewahrungsdauer temporaerer Dateien.
- Regeln fuer Loeschen und Archivieren.
- Definition von `valid_with_warnings`.
- Umgang mit normalisierten Kopien.
- Umfang von Excel-, PDF- oder weiteren Exporten.

## Herkunft wesentlicher Inhalte

- P008-Ausgangsplan: Realtests, Diagrammpruefung, `weather_key`,
  eigener Dateiimport, kritische Wetterereignisse und Abgrenzung zu
  `ma_variants`.
- Implementierungsplan `ma_weather`: Stadtwahl, Klimaregion,
  Referenzstandort, Datenmodell, Statusmodell, offene Datensaetze,
  Import-Log, Projekt-Default und Streamlit-Zielbild.
- P010: Quellenmodell, strukturierte Diagnosen, Freigaberegeln,
  Dateipruefsummen und JSONL-Sitzungslogs.
- Nutzerentscheidung vom 2026-06-23: Klimaregionenkarte in den UI-Assetbereich,
  Datenmodell zuerst als Plan- und Seed-Konzept, Aktivierung nur bewusst per
  Nutzeraktion.
