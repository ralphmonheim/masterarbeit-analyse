# P008 ma_weather Gesamtplan

Stand: 2026-07-13
Status: Aktiv
Plannummer: P008
Bezug: P007, P010, P015, P018, P021, P027, archivierter P002

## Aenderungsvermerk Compliance

Datum: 2026-07-13

DWD-Daten werden nach ihrem konkreten Bezugsweg klassifiziert. Offizielle
OpenData-Datensaetze koennen nur mit datensatzbezogener CC-BY-4.0-Quelle,
Attribution und geklaerten Drittrechten freigegeben werden. Registrierte oder
bestellte TRY-Leistungen richten sich nach Angebot und DWD-AGB. Der vorhandene
TRY-2011-/IDA-Bestand bleibt `yellow`, lokal und unversioniert.

Der bestehende Konverter ist an `ma_core.compliance` angebunden. Vor dem
Lesen von `.idm` oder `.PRN` verlangt er eine Nutzerbestaetigung und eine
Referenz auf die produktspezifischen Bezugsrechte. Das Audit speichert nur
Metadaten und Entscheidungen.

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
- Erweiterung weiterer Sommer- und Winterdatensaetze ausserhalb der aktuell
  katalogisierten drei Standorte.
- Umfang normalisierter Kopien und spaeterer Exporte.
- Fachliche Feinschaerfung kritischer Wetterereignisse fuer P021.

## Aenderungsvermerk zur Planergaenzung Standorterkennung und PLZ

Datum der Integration: 2026-06-27

Dieser Plan fuehrt weiterhin die Plannummer `P008`. Die Planergaenzung
`docs/project/plans/inbox/260627_Planergaenzung_P008_ma_weather_Standorterkennung_PLZ.md`
wurde fachlich in diesen Gesamtplan integriert und unter
`docs/project/archive/plans/260627_Planergaenzung_P008_ma_weather_Standorterkennung_PLZ.md`
archiviert.

Uebernommene Inhalte:

- TRY-Headerkoordinaten als fuehrende Quelle fuer ortsgenaue TRY-Dateien.
- EPSG:3034 als verbindliche technische Interpretation der TRY-Rechts- und
  Hochwerte.
- Offline-Standorterkennung ueber Gemeinde, amtlichen Gemeindeschluessel und
  Bundesland.
- Optionale, getrennte PLZ-Aufloesung.
- Deutschlandpruefung als blockierender Validierungsschritt.
- Trennung zwischen automatisch erkannten und bewusst bestaetigten
  Standortdaten.
- Geodatenquellen, Lizenzpruefung, Versionierung und lokale Ablage als
  eigener Planungspunkt.
- Vereinfachte Streamlit-Pruefansicht fuer lokale TRY-Entwuerfe.

Ersetzte oder korrigierte Inhalte:

- Die bisherige Logik `Stadt -> Klimaregion -> TRY-Referenzstandort` bleibt
  fuer bestehende Katalogeintraege und alte regionsbezogene Annahmen erhalten,
  ist fuer ortsgenaue TRY-Dateien aber nur noch Kompatibilitaetsweg.
- Die Klimaregion bleibt informativ und als Fallback nutzbar, ist aber nicht
  mehr die primaere technische Standortaufloesung fuer importierte
  ortsgenaue TRY-Dateien.
- Der vorhandene Koordinaten-Naechstvorschlag gegen bestaetigte TRY-Ordner ist
  nur ein Uebergangshinweis und darf keine finale Standortzuordnung ersetzen.

Weiterhin offene Entscheidungen:

- Verbindliche PLZ-Geodatenquelle, Lizenz und Feldnamen.
- Ob Geodaten selbst versioniert werden duerfen oder nur lokal mit
  Quellenmetadaten abgelegt werden.
- Maximaldistanz fuer Gemeinde-Fallbacks bei Grenzfaellen.
- Darstellung von PLZ in der normalen Standortauswahl.
- Endgueltige Benennung der UI-Aktion: fachlich `Pruefen`, bei spaeterer
  UI-Umsetzung ggf. mit Umlaut als `Prüfen`.

## Aenderungsvermerk zur Aktivierung der VG250-Gemeindequelle

Datum der Aktualisierung: 2026-06-29

Die lokale Gemeinde-Geodatenquelle fuer P008 wurde auf Basis des BKG-VG250-
Downloads vom Stand 01.01.2025 konkretisiert und aktiviert.

Umgesetzte Festlegungen:

- BKG VG250 ist die verbindliche lokale Gemeindequelle fuer diesen Slice.
- Der lokale Eingangsordner ist
  `data/ma_weather/geodata/_incoming/bkg_vg250_2025_01_01/`.
- Der aktive GeoJSON-Zielpfad ist
  `data/ma_weather/geodata/germany/germany_municipalities.geojson`.
- Die Quelle nutzt den Layer `v_vg250_gem`, Filter `GF = 4`, Ziel-CRS
  `EPSG:4326`, `GEN` als Gemeindenamen, `AGS` als Gemeindeschluessel und
  `LKZ` als Bundeslandkennung.
- QGIS ist als lokales Exportwerkzeug dokumentiert, bleibt aber keine
  Laufzeitabhaengigkeit des Projekts.
- Die Laufzeit nutzt `pyproj` fuer EPSG-Transformationen und `shapely` fuer
  Punkt-in-Polygon-Pruefungen.

Realer Teststand:

- `TRY2015_524031130658_Jahr.dat` wird ueber die TRY-Koordinate als
  `Potsdam`, AGS `12054000`, LKZ `BB` erkannt.
- `TRY2045_525331134258_Jahr.dat` wird ueber die TRY-Koordinate als `Berlin`,
  AGS `11000000`, LKZ `BE` erkannt.

Weiterhin offen:

- PLZ-Aufloesung bleibt optional und benoetigt eine getrennt freigegebene
  Geodatenquelle.
- Eine eindeutige BKG-Gemeindeaufloesung darf den Entwurf vorbelegen, wenn die
  Gemeinde im Standortkatalog existiert. Die Registrierung und der
  Projekt-Default bleiben weiterhin bewusste Nutzeraktionen.

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
- `TRY_FFM_2015_JAHR` wurde real mit 8760 Stunden erfolgreich geprueft.
- Streamlit kann aktive `weather_key` Werte auswaehlen, Wetteranalysen starten
  und Ergebnisse anzeigen.
- Der lokale TRY-Dateiscan liest bereits Rechtswert, Hochwert, Hoehenlage,
  Art des TRY und Bezugszeitraum aus dem TRY-Kopf.
- Jahr, Szenario und Datensatztyp werden beim Scan bereits aus dem Dateinamen
  abgeleitet.
- Zwei neue lokale TRY-Ordner fuer Berlin/Potsdam-nahe Testdateien sind
  vorhanden und werden ueber die lokale BKG-VG250-Gemeindequelle als Potsdam
  beziehungsweise Berlin erkannt.
- EPSG:3034-Transformation, lokale Gemeindegrenzen und
  Punkt-in-Polygon-Aufloesung sind technisch umgesetzt. PLZ-Polygone bleiben
  optional und sind noch nicht freigegeben.
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

Diese Entscheidung gilt fuer die manuelle Auswahl und fuer bestehende
Katalogeintraege. Fuer importierte ortsgenaue TRY-Dateien sind die
Headerkoordinaten der Wetterdatei fuehrend.

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

### TRY-Headerkoordinaten sind fuehrend

Fuer ortsgenaue TRY-Dateien werden Rechtswert und Hochwert aus dem TRY-Kopf
als primaere Standortquelle geplant. Der Dateiname darf zur Konsistenzpruefung
genutzt werden, ersetzt aber nicht den Header.

Die TRY-Koordinaten werden als EPSG:3034 interpretiert. Die Transformation und
raeumliche Zuordnung liegen in `ma_weather`, nicht in Streamlit oder Tkinter.

### Gemeinde ist fuehrend, PLZ ist optional

Die automatische Standorterkennung soll offline Gemeinde oder Stadt,
amtlichen Gemeindeschluessel und Bundesland bestimmen. Diese administrative
Zuordnung ist fuehrend.

Die PLZ wird getrennt und optional bestimmt. Eine fehlende PLZ blockiert den
Import nicht, sofern Gemeinde und Deutschlandpruefung erfolgreich sind oder
bewusst bestaetigt wurden.

### Klimaregion und Referenzstandort sind Kompatibilitaetsweg

Die Klimaregions- und Referenzstandortlogik bleibt fuer bestehende
Katalogeintraege, Anzeige, Fallbacks und Altdaten kompatibel erhalten. Fuer
ortsgenaue TRY-Dateien ist sie nicht mehr die primaere technische
Standortaufloesung.

Die Klimaregion kann aus dem bestaetigten Standort weiterhin abgeleitet und
informativ angezeigt werden.

### Nur aktive und validierte Datensaetze sind regulaer auswaehlbar

Die normale Wetterauswahl zeigt nur Datensaetze, die fachlich validiert,
freigegeben und in der Katalogsicht aktiv sind.

Offene, unvollstaendige oder fehlerhafte Datensaetze duerfen nicht an
`ma_parameters`, Varianten oder Simulationen uebergeben werden.

### Import, Pruefung, Katalogaktivitaet und Projekt-Default sind getrennt

Ein Import setzt keinen Projekt-Default.

Ein Import wird nicht automatisch katalogisiert oder aktiv gesetzt. Ein
gepruefter Entwurf wird erst durch bewusste Uebernahme registriert und dann in
der Katalogsicht aktiv. Die Zielkette ist:

```text
importiert -> gescannt -> geprueft -> aktiv im Katalog -> Projekt-Default
```

Die Uebernahme eines geprueften Entwurfs und der Projekt-Default sind bewusste
Nutzeraktionen. Dadurch bleibt ein bestehender Projektzustand stabil und neue
Importe koennen zuerst geprueft werden.

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

`ma_parameters` uebernimmt seit P015-S3a nur aktivierte und freigegebene
Wetterdaten aus `ma_weather` als Metadaten- und Quellenreferenz im
`ParameterInputPackage`. Die Uebergabe erfolgt nicht direkt von offenen
Importen; TRY-Import und Wettervalidierung bleiben in `ma_weather`.

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
| `weather_geodata_sources` | lokale Geodatenquellen mit Version, Lizenz und Pruefsumme |
| `weather_location_resolution` | Ergebnis der automatischen Standort- und PLZ-Aufloesung |

Geplante stabile IDs:

- `region_id`
- `location_id`
- `reference_location_id`
- `dataset_id`
- `import_id`
- `geodata_source_id`
- amtlicher Gemeindeschluessel fuer externe Verwaltungsdaten

Bestehende Schluessel wie `weather_key`, TRY-Ordnungsnummern und Legacy-Codes
bleiben fuer Anzeige, Rueckverfolgbarkeit und Kompatibilitaet erhalten. Sie
werden langfristig nicht als alleinige Primaerschluessel geplant.

## Standort- und Referenzlogik

Hauptweg fuer ortsgenaue TRY-Dateien:

```text
TRY-Datei importieren oder lokal ablegen
    ->
TRY-Kopf lesen
    ->
Rechtswert, Hochwert und EPSG:3034 pruefen
    ->
Koordinaten transformieren
    ->
Deutschlandpruefung ausfuehren
    ->
Gemeinde, amtlichen Gemeindeschluessel und Bundesland offline ermitteln
    ->
PLZ optional offline ermitteln
    ->
Abweichungen zu Nutzereingaben oder Mapping anzeigen
    ->
Nutzerbestaetigung bei Warnung, Mehrdeutigkeit oder manueller Korrektur
    ->
Wetterdatensatzstandort speichern
    ->
validieren, aktivieren oder offen halten
```

Kompatibilitaetsweg fuer bestehende Katalogeintraege:

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
Bei ortsgenauen TRY-Dateien wird sie aus dem bestaetigten Standort abgeleitet.

## Offline-Standorterkennung und PLZ-Aufloesung

Die Standorterkennung arbeitet regulaer offline und nutzt lokale Geodaten.
Externe Online-APIs werden nicht fuer die regulaere Validierung geplant.

Geplante Erkennung:

- TRY-Rechtswert und TRY-Hochwert aus dem Header lesen,
- EPSG:3034 zentral verarbeiten,
- transformierte Koordinaten pruefen,
- Punkt innerhalb Deutschlands pruefen,
- Gemeinde/Stadt per Punkt-in-Polygon bestimmen,
- amtlichen Gemeindeschluessel und Bundesland uebernehmen,
- PLZ optional ueber getrennten PLZ-Geodatensatz bestimmen,
- automatische und manuell bestaetigte Werte getrennt speichern,
- jede manuelle Korrektur mit Grund protokollieren.

Blockierend:

- fehlende oder ungueltige Koordinaten,
- unbekanntes oder nicht verarbeitbares CRS,
- Punkt ausserhalb Deutschlands,
- fehlende Gemeinde ohne bestaetigte manuelle Zuordnung,
- fehlende oder ungueltige Geodaten fuer eine verpflichtende Pruefung.

Nicht zwingend blockierend:

- fehlende PLZ,
- PLZ-Mehrdeutigkeit,
- geringe Abweichung zwischen Dateiname und Header,
- Grenzfall mit bewusster Nutzerbestaetigung.

## Geodatenquellen und Lizenzstatus

Die konkrete Quelle wird vor der Implementierung freigegeben und in lokalen
Metadaten dokumentiert.

Geeigneter Kandidat fuer Gemeindegrenzen:

- BKG VG250, voraussichtlich unter Datenlizenz Deutschland Namensnennung 2.0.

Moegliche Kandidaten fuer PLZ-Daten:

- OSM-/Geofabrik-basierte PLZ-Grenzen,
- OpenPLZ oder daraus ableitbare PLZ-Referenzen,
- andere lokale PLZ-Datensaetze nur nach Lizenzpruefung.

PLZ-Daten werden wegen Lizenz- und Abgrenzungsrisiken zunaechst als optionale
Ergaenzung geplant. Gemeinde beziehungsweise amtlicher Gemeindeschluessel
bleiben fuehrend.

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
| `data/ma_weather/input/custom/` | lokal importierte TRY-Dateien |
| `data/ma_weather/config/datasets/` | lokaler, nicht versionierter Importkatalog |
| `data/ma_weather/database/` | aufbereitete Wetterdaten |
| `data/ma_weather/output/` | Wetterdiagramme |
| `data/ma_weather/reports/` | Markdown- und Validierungsberichte |
| `data/ma_weather/exports/` | spaetere strukturierte Exporte |
| `data/ma_weather/geodata/` | lokale Gemeinde- und PLZ-Geodaten |
| `data/ma_weather/geodata/_incoming/bkg_vg250_2025_01_01/` | entpackter lokaler BKG-VG250-Download |
| `data/ma_weather/geodata/germany/germany_municipalities.geojson` | GeoJSON-Export des Layers `v_vg250_gem` |
| `data/ma_weather/geodata/germany/source_docs/` | lokale BKG-Begleitdokumente |
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

Versionierte Quellen- und Feldmetadaten fuer lokale Geodaten sollen unter
`config/ma_weather/geodata/` liegen. Die grossen Geodaten selbst bleiben lokal,
wenn Dateigroesse, Lizenz oder Repository-Regeln gegen Versionierung sprechen.
Fuer BKG VG250 01.01.2025 liegt die versionierte Metadatenbeschreibung unter
`config/ma_weather/geodata/bkg_vg250_2025_01_01.yaml`.

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

Im Bereich `Wetterdatensaetze` werden die Arbeitsschritte gefuehrt:

- `Import`: DWD-Hinweis und Ablage lokaler TRY-Dateien, noch ohne
  Katalogregistrierung,
- `Scannen`: lokale TRY-Dateien finden und Datensatzentwuerfe erzeugen,
- `Pruefen`: gefundene Entwuerfe fachlich kontrollieren, Parameter
  ergaenzen, technisch pruefen und bewusst registrieren.

Wenn keine Funktion aktiv ist, zeigt die Seite die normalen Uebersichten fuer
aktive und offene Wetterdatensaetze.

### Pruefansicht fuer lokale TRY-Entwuerfe

Der bisherige UI-Schritt `Validieren` wird fachlich als `Pruefen` gefuehrt.
Die katalogisierte Bestandspruefung bleibt technisch erhalten, steht aber nicht
mehr in dieser Entwurfspruefung. Sie kann spaeter als eigener
Bestandspruefungsbereich eingeordnet werden.

Innerhalb von `Pruefen` gibt es einen Umschalter zwischen:

- `Gefundene lokale TRY-Dateien`,
- `Parameter pruefen`.

`Gefundene lokale TRY-Dateien` ersetzt dort die bisherige offene
Entwurfsliste. Die reduzierte Tabelle zeigt nur:

- `Datei`,
- `Status`,
- `Ort / Vorschlag`,
- `Jahr`,
- `Typ`,
- `Szenario`,
- `Offene Punkte`.

`Parameter pruefen` zeigt fuer den ausgewaehlten Entwurf eine reduzierte
Detailtabelle mit:

- `Feld`,
- `Wert`.

Im Feld `Wert` steht der gelesene Wert, ein eindeutig abgeleiteter Wert, ein
manuell ergaenzter Wert oder ein leerer Wert, wenn nichts sicher erkannt wurde.
Sichtbar geprueft werden Stadt, Bezugsjahr, Datensatztyp und Szenario. Rolle,
`weather_key` und Anzeigename werden nach gesetztem Standort automatisch
abgeleitet und nicht als eigene Eingabefelder angezeigt.
Technische Zusatzinformationen wie Quelle, Bearbeitung, TRY-ID, Rechtswert,
Hochwert und Hoehenlage werden nicht in der Haupttabelle angezeigt. Sie koennen
spaeter in einem ausklappbaren Bereich `Technische Details` folgen.

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

Unregistrierte Scan-Entwuerfe bleiben ebenfalls sichtbar, aber nicht regulaer
auswaehlbar. Sie werden in der Pruefansicht unter `Gefundene lokale
TRY-Dateien` bearbeitet und erst nach bewusster Registrierung Teil des lokalen
Wetterkatalogs.

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

- fachliche Feinschaerfung der Extremtag- und Ereignisdefinitionen,
- Vergleich von Gegenwarts- und Zukunftsdatensaetzen,
- Vergleich mehrerer Referenzstandorte,
- fachliche Diagrammpruefung gegen Masterarbeitslayout,
- spaetere P021-Anbindung fuer ausgewaehlte kritische Wetterereignisse.

## Umsetzungsschritte

Die weitere Umsetzung wird ab 2026-06-24 in reduzierten, groesseren Slices
gefuehrt. Die fruehere Neun-Phasen-Gliederung bleibt fachlich im Plan
enthalten, wird aber nicht mehr als operative Reihenfolge verwendet.

### Slice 1 Bestand, Realtests und Auswahlstatus

- fehlende TRY-Jahres-, Sommer- und Winterdateien beim Deutschen
  Wetterdienst herunterladen und lokal unter `data/ma_weather/input/`
  bereitstellen,
- alle katalogisierten Wetterdatensaetze gegen lokale TRY-Dateien pruefen,
- pro `weather_key` Datei-, Import-, Warnungs-, Fehler- und Freigabestatus
  ermitteln,
- Status direkt in Wetterauswahl und Kataloguebersicht anzeigen,
- TRY-Referenzdatensaetze weiter vor standortgenauen Datensaetzen priorisieren,
- keine fachlich unklare Ersatzzuordnung einfuehren,
- lokale fehlende TRY-Dateien klar melden, ohne synthetische Dateien anzulegen.

### Slice 2 Importnachweis und offene Datensaetze

- jeden Analyseimport mit stabiler `import_id` versehen,
- Import-Log, Validierungsbericht, Wetterdatensatz, `session_id` und `run_id`
  verknuepfen,
- offene, fehlende, fehlerhafte oder noch freizugebende Datensaetze in
  Streamlit separat anzeigen,
- offene Datensaetze nicht als regulaere Auswahl fuer Varianten,
  Simulationen oder `ma_parameters` bereitstellen.

### Slice 3 Aktivierung, Projekt-Default und Uebergabegrenze

- Statuskette `importiert -> validiert -> aktiv -> Projekt-Default` umsetzen,
- gueltige Importe nicht automatisch katalogisieren oder aktivieren,
- gepruefte Entwuerfe erst nach bewusster Uebernahme aktiv in den Katalog
  schreiben,
- aktive Datensaetze nicht automatisch als Projekt-Default setzen,
- Uebernahme und Projekt-Default als bewusste Streamlit-Aktionen fuehren,
- lokale YAML-Grundlage bis zur spaeteren Datenbankmigration verwenden,
- Uebergabe an `ma_parameters` nur fuer aktive, validierte und freigegebene
  Wetterdatensaetze vorbereiten; P015-S3a konsumiert diesen Vertrag bereits
  als `ParameterInputPackage`.

### Slice 4 Wetterdatensatztyp und kritische Ereignisse

- Sommer- und Winter-TRY-Dateien als eigene Wetterdatensaetze katalogisieren,
- Datensatztyp Jahr, Sommer oder Winter in Streamlit sichtbar machen,
- Ereignisberechnung immer aus dem bewusst ausgewaehlten Datensatz ableiten,
- heisseste und kaelteste Tage sowie 3-Tage-Perioden erkennen,
- strahlungsreichsten und windstaerksten Tag erkennen, falls die jeweiligen
  Spalten vorhanden sind,
- strukturierte Ereignisobjekte fuer die spaetere P021-Nutzung bereitstellen,
- keine automatische Uebergabe an P021 einfuehren.

### Slice 5 Wetterdatenimport und DWD-Beschaffung

- Importbutton unten im Bereich `Wetterdatensaetze` vor der aktiven
  Datensatzuebersicht anzeigen,
- DWD-Link zur manuellen TRY-Beschaffung im Importdialog bereitstellen,
- entpackte TRY-`.dat`-Dateien lokal unter
  `data/ma_weather/input/custom/<weather_key>/` ablegen,
- lokale Importdatensaetze im nicht versionierten YAML-Katalog
  `data/ma_weather/config/datasets/weather_datasets_local.yaml` registrieren,
- Beispielkatalog und lokalen Importkatalog gemeinsam laden,
- aktive und offene Wetterdatensaetze getrennt anzeigen,
- offene, fehlerhafte oder noch freizugebende Datensaetze nicht regulaer
  auswaehlbar machen,
- keine automatische Aktivierung und keinen automatischen Projekt-Default nach
  Import ausloesen.

### Slice 6 Pruefansicht und ortsgenaue Standorterkennung

- UI-Schritt `Validieren` fachlich zu `Pruefen` weiterentwickeln,
- katalogisierte Bestandspruefung aus der Entwurfspruefung entfernen und fuer
  spaetere Einordnung erhalten,
- `Gefundene lokale TRY-Dateien` als reduzierte Entwurfsliste anzeigen,
- `Parameter pruefen` als reduzierte Detailtabelle mit `Feld` und `Wert`
  aufbauen,
- Rolle, `weather_key` und Anzeigename aus Standort, Jahr, Typ und Szenario
  generieren und nicht als eigene Eingabefelder anzeigen,
- fehlende Werte leer lassen und keine kuenstlichen Defaults setzen,
- Pruefung und Registrierung nur nach Nutzeraktion starten,
- Rechtswert, Hochwert und Hoehenlage weiter lesen, aber technische Details
  nicht in der Haupttabelle anzeigen,
- EPSG:3034-Verarbeitung und Koordinatentransformation in `ma_weather`
  vorbereiten,
- Offline-Gemeindeaufloesung mit amtlichem Gemeindeschluessel planen,
- optionale PLZ-Aufloesung getrennt vorbereiten,
- Berlin- und Potsdam-TRY-Dateien als reale Testfaelle verwenden,
- bestehende Klimaregions- und Referenzstandortlogik als
  Kompatibilitaetsweg erhalten.

### Spaetere Folgeschritte

- Diagrammgestaltung fachlich pruefen,
- Zeitfenster reproduzierbar beschreiben,
- Schnittstelle zu P021 vorbereiten.

## Tests und Abschlusskriterien

- Alle 18 aktiven Jahr-, Sommer- und Winterdatensaetze sind real dokumentiert geprueft oder
  fehlende lokale Dateien sind nachvollziehbar gemeldet.
- Fehlende TRY-Dateien sind als manueller DWD-Downloadschritt dokumentiert und
  werden nicht synthetisch ersetzt.
- Pflichtspalten, eindeutiger Zeitindex und 8760 Stunden sind je Jahresdatei
  nachvollziehbar.
- Fehlende optionale Spalten fuehren zu strukturierten Warnungen.
- Stadtwahl fuehrt eindeutig zu Klimaregion und Referenzstandort.
- Ortsgenaue TRY-Dateien koennen ueber Headerkoordinaten geprueft und spaeter
  offline einer Gemeinde zugeordnet werden.
- EPSG:3034 wird zentral verarbeitet, sobald die Geodatenlogik umgesetzt wird.
- Berlin- und Potsdam-Testdateien werden als offene Entwuerfe erkannt und
  duerfen ohne bestaetigte Zuordnung nicht automatisch Hamburg oder einem
  anderen Ersatzstandort zugeordnet werden.
- PLZ-Aufloesung ist optional und blockiert nicht, solange Gemeinde und
  Deutschlandpruefung erfolgreich oder bewusst bestaetigt sind.
- Die regulare Auswahl zeigt nur aktive und validierte Datensaetze.
- Offene Datensaetze besitzen einen eigenen Bearbeitungsbereich.
- Jeder Import erzeugt ein dauerhaftes Log.
- Import-Log, Validierungsbericht und Wetterdatensatz sind eindeutig
  verknuepft.
- Ein neuer Import aktiviert keinen Datensatz automatisch und setzt keinen
  Projekt-Default automatisch; ein gepruefter Entwurf wird erst nach bewusster
  Uebernahme aktiv registriert.
- `ma_weather` uebergibt nur aktivierte und freigegebene Daten als
  Quellenreferenz an `ma_parameters`.
- Offene Wetterdatensaetze koennen nicht fuer Varianten oder Simulationen
  genutzt werden.
- Kritische Wetterereignisse werden nur aus dem bewusst ausgewaehlten
  Wetterdatensatz berechnet.
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
- Keine Online-Geocoding- oder PLZ-API als regulaere Standortpruefung.
- Keine stille Uebernahme von Koordinatenvorschlaegen als finaler Standort.

## Offene fachliche und technische Punkte

- Tatsachliches Format aller vorhandenen TRY-Dateien.
- Notwendige Pflichtspalten je Dateiformat.
- Interne Einheiten und erlaubte Wertebereiche.
- Fachliche Feinschaerfung der aktuell technischen Definition von Extremtagen
  und kritischen Wetterereignissen.
- Gewuenschte Klimaszenario-Bezeichnungen.
- Gewuenschte Bezugszeitraeume.
- Erweiterung weiterer Sommer- und Winterdatensaetze ausserhalb der aktuell
  katalogisierten drei Standorte.
- Fachliche Pruefung einzelner Stadtzuordnungen.
- Endgueltige ID-Schreibweise.
- Aufbewahrungsdauer temporaerer Dateien.
- Regeln fuer Loeschen und Archivieren.
- Definition von `valid_with_warnings`.
- Umgang mit normalisierten Kopien.
- Umfang von Excel-, PDF- oder weiteren Exporten.
- Verbindliche PLZ-Geodatenquelle, Version, Lizenz und Feldnamen.
- Regel, ob Geodaten versioniert werden duerfen oder nur lokal mit
  Pruefsumme und Bezugsanleitung abgelegt werden.
- Maximaldistanz fuer Gemeinde-Fallbacks bei Grenzfaellen.
- Umgang mit PLZ-Gebieten, die mehrere Gemeinden schneiden.
- Endgueltige UI-Schreibweise `Pruefen` oder `Prüfen`.

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
- Planergaenzung vom 2026-06-27:
  Offline-Standorterkennung, EPSG:3034, Gemeinde-/PLZ-Aufloesung,
  Geodatenquellen und Korrektur der Klimaregionslogik zum Kompatibilitaetsweg.
- Nutzerentscheidung vom 2026-06-27: Die Wetter-Entwurfspruefung wird als
  `Pruefen` gefuehrt; die Ansicht wechselt zwischen `Gefundene lokale
  TRY-Dateien` und `Parameter pruefen`; die Detailtabelle zeigt nur
  `Feld` und `Wert`.
