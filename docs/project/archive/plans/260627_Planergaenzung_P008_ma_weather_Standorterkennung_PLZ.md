# ARCHIVIERT

Archivierungsdatum: 2026-06-27

Archivierungsgrund:
Dieser Plan wurde mit dem aktiven Gesamtplan fuer `ma_weather` zusammengefuehrt.

Nachfolgeplan:
P008 ma_weather Gesamtplan

Nachfolgeplan-Speicherort:
`docs/project/plans/inbox/260623_Plan_P008_ma_weather_Gesamtplan.md`

Hinweis:
Die Inhalte dieses Dokuments wurden geprueft und in den aktualisierten
Gesamtplan fuer `ma_weather` integriert. Dieses Dokument dient nur noch der
Nachvollziehbarkeit der Planentwicklung und darf nicht mehr als aktuelle
Umsetzungs- oder Planungsgrundlage verwendet werden.

---

# Planergänzung P008 – Offline-Standorterkennung und PLZ-Zuordnung für `ma_weather`

## Dokumentstatus

- **Typ:** Integrations- und Umsetzungsplan
- **Zielplan:** `P008 ma_weather Gesamtplan`
- **Stand:** 2026-06-27
- **Status:** Zur Analyse und Integration vorgesehen
- **Wichtig:** Dieses Dokument ist kein dauerhaft paralleler Plan. Nach der bestätigten Integration in P008 soll es mit Archivierungsvermerk archiviert werden.

---

## 1. Anlass

Die aktuelle Implementierung von `ma_weather` kann Wetterstandorte über einen statischen Standort- und Klimaregionskatalog verwalten. Eine automatische Verortung importierter ortsgenauer TRY-Dateien anhand der im Header enthaltenen Rechts- und Hochwerte ist noch nicht umgesetzt.

Die geprüften TRY-Dateien enthalten:

- Rechtswert und Hochwert,
- Koordinatensystem EPSG:3034,
- Höhenlage,
- TRY-Art,
- Bezugszeitraum,
- 8.760 stündliche Datensätze.

Das TRY-Handbuch beschreibt ortsgenaue Datensätze für beliebige Punkte in Deutschland mit etwa 1 km² räumlicher Auflösung. Der frühere technische Bezug auf 15 Klimaregionen mit festen Repräsentanzstationen ist für diese ortsgenauen TRY-Dateien nicht mehr die maßgebende Auswahl- und Zuordnungslogik.

Zusätzlich soll die automatische Verortung optional um eine Postleitzahlzuordnung erweitert werden.

---

## 2. Ziel

`ma_weather` soll einen importierten TRY-Datensatz vollständig offline verorten können.

Aus den TRY-Koordinaten sollen automatisch ermittelt werden:

1. transformierte geographische Koordinaten,
2. Prüfung, ob der Punkt innerhalb Deutschlands liegt,
3. Gemeinde oder Stadt,
4. amtlicher Gemeindeschlüssel,
5. Bundesland,
6. optional die fünfstellige Postleitzahl,
7. Qualität und Methode der Zuordnung.

Das Ergebnis wird:

- in der Streamlit UI angezeigt,
- im Validierungsbericht gespeichert,
- im Import-Log dokumentiert,
- mit einer eventuell zuvor gewählten Stadt oder PLZ verglichen,
- erst nach erfolgreicher oder bestätigter Zuordnung zur Aktivierung zugelassen.

---

## 3. Analyse des aktuellen Projektstands

### 3.1 Bereits vorhanden

Im Projekt bestehen bereits:

- Paket `src/ma_weather/`,
- Standort- und Klimaregionskatalog,
- stabile IDs für Regionen und Standorte,
- YAML-basierter Standortkatalog,
- TRY-Import und Wettervalidierung,
- Streamlit-Anbindung,
- strukturierte Validierungsdiagnosen,
- SHA-256-Prüfsummen,
- JSONL-Sitzungslogs,
- aktiver Gesamtplan `P008`.

### 3.2 Aktuelle Begrenzung

Das bestehende Modell `WeatherLocation` enthält aktuell insbesondere:

- `location_id`,
- `location_name`,
- `normalized_name`,
- `region_id`,
- `reference_location_id`,
- `legacy_code`,
- Kennzeichnungen für Referenzstandort und Aktivität.

Noch nicht enthalten sind:

- Rechtswert,
- Hochwert,
- EPSG-Code,
- Breitengrad,
- Längengrad,
- amtlicher Gemeindeschlüssel,
- Bundesland,
- Postleitzahl,
- Geometrie,
- automatische Punkt-in-Polygon-Zuordnung,
- Zuordnungsstatus,
- manuell bestätigte Standortabweichung.

### 3.3 Korrekturbedarf im bisherigen P008

Der bestehende P008 beschreibt derzeit als regulären Ablauf:

```text
Stadt
→ Klimaregion
→ TRY-Referenzstandort
→ Wetterdatensatz
```

Für ältere regionsbezogene Datensätze kann diese Logik als Kompatibilitätsweg erhalten bleiben.

Für ortsgenaue TRY-Dateien muss der Hauptweg jedoch ergänzt beziehungsweise ersetzt werden durch:

```text
TRY-Datei
→ Headerkoordinaten
→ Koordinatentransformation
→ Gemeinde/Stadt
→ optional PLZ
→ Wetterdatensatzstandort
```

Die 15 Klimaregionen dürfen weiterhin informativ angezeigt werden. Sie dürfen für ortsgenaue TRY-Dateien jedoch nicht mehr als primäre technische Standortauflösung verwendet werden.

---

## 4. Verbindliche Entscheidungen

### 4.1 Offline-Verarbeitung

**Entscheidung**

Die reguläre Standort- und PLZ-Erkennung erfolgt vollständig offline.

**Begründung**

- reproduzierbare Ergebnisse,
- keine Abhängigkeit von externen APIs,
- keine wechselnden Online-Antworten,
- keine Übermittlung von Projektkoordinaten,
- Funktionsfähigkeit ohne Internet,
- bessere Eignung für automatisierte Tests.

**Folge**

Gemeinde- und PLZ-Flächen werden als versionierte lokale Geodatensätze eingebunden.

---

### 4.2 TRY-Header ist die primäre Koordinatenquelle

**Entscheidung**

Rechtswert und Hochwert aus dem TRY-Header sind maßgeblich.

**Begründung**

- der Header ist Bestandteil der eigentlichen Wetterdatei,
- EPSG:3034 ist dort fachlich festgelegt,
- der Dateiname kann zusätzlich kodierte Koordinaten enthalten, ist aber nur Kontrollquelle.

**Folge**

Dateinamenkoordinaten werden zur Konsistenzprüfung verwendet, nicht als alleinige Verortungsgrundlage.

---

### 4.3 Deutschland ist der aktuelle Geltungsbereich

**Entscheidung**

Die Standortauflösung akzeptiert aktuell nur Punkte innerhalb Deutschlands.

**Begründung**

- Projektumfang der Masterarbeit,
- TRY-Datensätze sind für Deutschland vorgesehen,
- geringere technische Komplexität,
- klarere Validierungsregeln.

**Folge**

Punkte außerhalb Deutschlands erhalten einen blockierenden Status.

---

### 4.4 Gemeinde und PLZ sind getrennte räumliche Zuordnungen

**Entscheidung**

Gemeindezuordnung und Postleitzahlzuordnung werden unabhängig voneinander durchgeführt.

**Begründung**

- PLZ-Gebiete entsprechen nicht zwingend Gemeindegrenzen,
- eine Gemeinde kann mehrere PLZ besitzen,
- ein PLZ-Gebiet kann räumlich anders zugeschnitten sein,
- Gemeinde und PLZ haben unterschiedliche fachliche Funktionen.

**Folge**

Es gibt zwei getrennte Resolver:

- Municipality Resolver,
- Postal Code Resolver.

---

### 4.5 PLZ ist eine optionale Ergänzung, Gemeinde bleibt führend

**Entscheidung**

Die Gemeinde- oder Stadtzuordnung mit amtlichem Schlüssel ist die führende administrative Standortangabe. Die PLZ ergänzt den Datensatz.

**Begründung**

- amtliche Gemeindeschlüssel sind geeigneter für stabile Verknüpfungen,
- Postleitzahlen können sich ändern,
- PLZ-Flächen sind keine Verwaltungseinheiten,
- ein TRY-Rasterpunkt beschreibt eine Position, nicht zwingend eine postalische Adresse.

**Folge**

Fehlende PLZ blockiert den Import nicht, sofern Gemeinde und Deutschlandprüfung erfolgreich sind. Dies kann später konfigurierbar gemacht werden.

---

### 4.6 Keine direkte Kopplung der Fachlogik an Streamlit

**Entscheidung**

Koordinatentransformation und räumliche Zuordnung liegen in `ma_weather`, nicht in der UI.

**Begründung**

- Testbarkeit,
- Wiederverwendung durch CLI oder Tkinter,
- spätere Austauschbarkeit der UI,
- Vermeidung direkter GIS-Logik in Streamlit-Seiten.

---

### 4.7 Manuelle Korrekturen bleiben nachvollziehbar

**Entscheidung**

Automatisch erkannte Gemeinde und PLZ dürfen manuell bestätigt oder korrigiert werden. Die automatische Erkennung wird dabei nicht überschrieben, sondern getrennt gespeichert.

**Begründung**

- Grenzfälle,
- generalisierte Geometrien,
- unvollständige PLZ-Daten,
- Nachvollziehbarkeit.

**Folge**

Automatische und bestätigte Werte werden getrennt geführt. Jede Änderung benötigt eine Begründung und einen Log-Eintrag.

---

## 5. Zielprozess

```text
TRY-Datei hochladen
    ↓
Header lesen
    ↓
Rechtswert/Hochwert und EPSG prüfen
    ↓
Dateinamenkoordinaten optional lesen
    ↓
EPSG:3034 → Ziel-CRS/WGS84 transformieren
    ↓
Deutschlandprüfung
    ↓
Gemeinde-Polygon bestimmen
    ↓
PLZ-Polygon optional bestimmen
    ↓
mit vorausgewählter Stadt/PLZ vergleichen
    ↓
Status und Diagnosen erzeugen
    ↓
Ergebnis in UI anzeigen
    ↓
Nutzerbestätigung bei Warnung oder Mehrdeutigkeit
    ↓
Validierungsbericht und Import-Log speichern
    ↓
Datensatz freigeben oder offen halten
```

---

## 6. Lokale Geodaten

### 6.1 Erforderliche Datensätze

Mindestens erforderlich:

1. deutsche Staatsgrenze oder aus Gemeindegeometrien abgeleitete Gesamtfläche,
2. Gemeindegrenzen mit:
   - Gemeindename,
   - amtlichem Gemeindeschlüssel,
   - Bundesland,
   - Geometrie,
3. optional PLZ-Gebiete mit:
   - fünfstelliger PLZ,
   - Flächengeometrie.

### 6.2 Ablage

Die konkrete Ablage muss an die vorhandene Projektstruktur angepasst werden. Zielbereich:

```text
data/ma_weather/geodata/
├── administrative/
│   └── germany_municipalities.gpkg
├── postal_codes/
│   └── germany_postal_codes.gpkg
└── metadata/
    ├── municipalities.json
    └── postal_codes.json
```

Die Geodaten selbst sollen nur dann versioniert werden, wenn Dateigröße, Lizenz und Repository-Regeln dies zulassen. Andernfalls:

- lokale Ablage,
- `.gitignore`,
- reproduzierbare Bezugsanleitung,
- Prüfsumme,
- Versions- und Lizenzmetadaten.

### 6.3 Metadaten je Geodatensatz

- Quellenname,
- Produktname,
- Bezugsdatum,
- Versionsstand,
- Lizenz,
- Download- oder Bezugsdatum,
- lokaler relativer Pfad,
- Layername,
- ursprüngliches CRS,
- SHA-256-Prüfsumme,
- erwartete Feldnamen,
- Geltungsbereich Deutschland.

### 6.4 Datenquellenentscheidung

Codex soll keine Datenquelle ungeprüft fest einbauen.

Vor Umsetzung muss geklärt werden:

- welche Gemeindegrenzen verwendet werden,
- welche PLZ-Flächen rechtlich und technisch verfügbar sind,
- ob die Lizenz eine Ablage im Projekt zulässt,
- welche Version für die Masterarbeit eingefroren wird,
- ob die PLZ-Daten frei weitergegeben werden dürfen.

Die Fachlogik wird quellenunabhängig aufgebaut, sodass die konkrete lokale Datei austauschbar bleibt.

---

## 7. Technische Architektur

### 7.1 Vorgeschlagene Komponenten

Die genaue Dateieinordnung ist nach Bestandsanalyse festzulegen.

```text
src/ma_weather/
├── parsers/
│   └── try_header_parser.py
├── geodata/
│   ├── geodata_repository.py
│   ├── geodata_config.py
│   └── geodata_models.py
├── services/
│   ├── coordinate_transform_service.py
│   ├── germany_boundary_service.py
│   ├── municipality_resolution_service.py
│   ├── postal_code_resolution_service.py
│   └── location_validation_service.py
└── validation/
    └── location_diagnostics.py
```

Diese Struktur ist ein Integrationsvorschlag und darf nicht blind als Parallelstruktur erzeugt werden.

### 7.2 Bibliotheken

Voraussichtlich:

- `pyproj`,
- `geopandas`,
- `shapely`,
- `pyogrio`.

Vor Aufnahme ist zu prüfen:

- vorhandenes Dependency-Management,
- Python-Version,
- Installierbarkeit unter Windows,
- mögliche Konflikte mit bestehenden Paketen,
- Größe der zusätzlichen Abhängigkeiten.

### 7.3 Fachliche Schnittstellen

```python
parse_try_header(file_path)
transform_try_coordinates(easting, northing, source_crs)
check_point_in_germany(point)
resolve_municipality(point)
resolve_postal_code(point)
validate_location_resolution(result, expected_location=None, expected_postal_code=None)
```

---

## 8. Datenmodelle

### 8.1 Automatisch ermitteltes Ergebnis

```text
TryLocationResolution
- status
- source_easting
- source_northing
- source_crs
- latitude
- longitude
- elevation_m
- country_code
- municipality_name
- municipality_code
- federal_state_name
- federal_state_code
- postal_code
- municipality_match_method
- postal_code_match_method
- municipality_distance_m
- postal_code_distance_m
- coordinate_consistency_status
- messages
```

### 8.2 Erweiterung Wetterdatensatz

Für `weather_datasets` beziehungsweise das bestehende Katalogmodell:

- `source_easting`,
- `source_northing`,
- `source_crs_epsg`,
- `resolved_latitude`,
- `resolved_longitude`,
- `elevation_m`,
- `detected_municipality_name`,
- `detected_municipality_code`,
- `detected_federal_state`,
- `detected_postal_code`,
- `confirmed_location_id`,
- `confirmed_postal_code`,
- `location_resolution_status`,
- `location_resolution_method`,
- `location_confirmed_at`,
- `location_confirmed_by`,
- `location_confirmation_note`.

### 8.3 Erweiterung Standortkatalog

Optional für `WeatherLocation`:

- `municipality_code`,
- `federal_state_code`,
- `postal_codes`,
- `latitude`,
- `longitude`.

Die PLZ-Liste im Standortkatalog dient nur dem Abgleich. Die primäre PLZ des konkreten TRY-Punktes stammt aus der räumlichen Zuordnung.

---

## 9. Statusmodell

### 9.1 Standortauflösung

- `not_checked`
- `matched`
- `matched_with_warning`
- `review_required`
- `municipality_not_found`
- `postal_code_not_found`
- `multiple_municipality_matches`
- `multiple_postal_code_matches`
- `outside_germany`
- `invalid_coordinates`
- `unknown_crs`
- `geodata_missing`
- `geodata_invalid`
- `manual_override`

### 9.2 Blockierende Zustände

Blockierend:

- `outside_germany`,
- `invalid_coordinates`,
- `unknown_crs`,
- `geodata_missing`,
- `geodata_invalid`,
- keine Gemeinde ohne bestätigte manuelle Zuordnung.

Nicht zwingend blockierend:

- `postal_code_not_found`,
- Abweichung zwischen Dateiname und Header innerhalb definierter Toleranz,
- PLZ-Abweichung bei eindeutigem Gemeindetreffer,
- Grenzfall mit bestätigter Nutzerentscheidung.

---

## 10. Räumliche Zuordnungslogik

### 10.1 Koordinatentransformation

- TRY-Quelle: EPSG:3034,
- Reihenfolge: Rechtswert als X/Easting, Hochwert als Y/Northing,
- `always_xy=True`,
- Transformation wird zentral gekapselt,
- transformierte Werte auf Endlichkeit und Deutschlandnähe prüfen.

### 10.2 Deutschlandprüfung

Primär:

- Punkt liegt innerhalb oder auf der deutschen Gesamtgeometrie.

Für Grenzfälle:

- `covers` statt ausschließlich `contains`,
- konfigurierbarer kleiner Toleranzbereich,
- Toleranz darf nicht automatisch eine ausländische Position als gültig erklären,
- Toleranztreffer erhalten mindestens eine Warnung.

### 10.3 Gemeindezuordnung

Primär:

- Punkt-in-Polygon.

Fallback:

- nächstes Gemeindepolygon innerhalb konfigurierbarer Maximaldistanz,
- Fallback niemals automatisch als vollständig bestätigt behandeln,
- Status `review_required`.

### 10.4 PLZ-Zuordnung

Primär:

- Punkt-in-Polygon auf lokalem PLZ-Datensatz.

Grenzfälle:

- mehrere PLZ-Flächen,
- Punkt auf Grenze,
- keine PLZ-Fläche,
- Inseln oder Wasserbereiche,
- Geometriefehler.

Bei Mehrdeutigkeit:

- Kandidaten anzeigen,
- Nutzerentscheidung verlangen,
- Entscheidung protokollieren.

### 10.5 Dateinamenprüfung

Bei kompatibler Namenskonvention:

```text
TRY2045_525331134258_Jahr.dat
```

werden Dateinamenkoordinaten separat gelesen und mit den transformierten Headerkoordinaten verglichen.

Ergebnis:

- `consistent`,
- `within_tolerance`,
- `inconsistent`,
- `not_available`.

Der Header bleibt maßgeblich.

---

## 11. Vergleich mit Nutzereingaben

Falls vor dem Import bereits Stadt oder PLZ gewählt wurden:

| Automatisches Ergebnis | Nutzereingabe | Reaktion |
|---|---|---|
| gleiche Gemeinde | gleiche Gemeinde | gültig |
| gleiche Gemeinde | andere PLZ | Warnung oder Prüfung |
| andere Gemeinde, gleiche PLZ-Region | Prüfung |
| andere Gemeinde | blockierende Abweichung bis Bestätigung |
| PLZ fehlt | PLZ eingegeben | Warnung |
| außerhalb Deutschland | beliebig | blockieren |

Die Anwendung darf eine Benutzervorauswahl nicht still überschreiben.

---

## 12. Streamlit UI

### 12.1 Importansicht

Neuer Abschnitt:

**Automatische Standorterkennung**

Anzeigen:

- Rechtswert,
- Hochwert,
- EPSG-Code,
- Breitengrad,
- Längengrad,
- Höhe,
- erkannte Gemeinde,
- amtlicher Gemeindeschlüssel,
- Bundesland,
- erkannte PLZ,
- Zuordnungsmethode,
- Status,
- Warnungen,
- Datenquelle und Version der Geodaten.

### 12.2 Aktionen

- automatische Zuordnung bestätigen,
- andere vorhandene Stadt wählen,
- Gemeinde manuell zuordnen,
- PLZ manuell korrigieren,
- Geodatenprüfung erneut starten,
- Karten- oder Tabellenansicht öffnen,
- Import offen speichern,
- Import abbrechen.

### 12.3 Offene Wetterdatensätze

Ergänzende Spalten:

- Standortauflösung,
- Gemeinde,
- PLZ,
- Koordinatenstatus,
- Geodatenversion,
- Bestätigung erforderlich.

### 12.4 Darstellung im Wetterdatenkatalog

Zusätzliche Informationen:

- Koordinaten,
- Gemeinde,
- AGS,
- Bundesland,
- PLZ,
- automatische oder manuelle Zuordnung,
- Geodatenquelle,
- Zeitpunkt der letzten Standortprüfung.

---

## 13. Import-Log und Validierungsbericht

### 13.1 Neue Log-Ereignisse

- `TRY_COORDINATES_EXTRACTED`
- `FILENAME_COORDINATES_EXTRACTED`
- `COORDINATE_TRANSFORMATION_COMPLETED`
- `GERMANY_BOUNDARY_CHECK_COMPLETED`
- `MUNICIPALITY_RESOLUTION_COMPLETED`
- `POSTAL_CODE_RESOLUTION_COMPLETED`
- `LOCATION_COMPARISON_COMPLETED`
- `LOCATION_CONFIRMATION_REQUIRED`
- `LOCATION_MANUALLY_CONFIRMED`
- `LOCATION_OVERRIDE_APPLIED`
- `LOCATION_RESOLUTION_FAILED`

### 13.2 Zu protokollierende Angaben

- Originalkoordinaten,
- Quell-CRS,
- transformierte Koordinaten,
- Geodatendatei und Prüfsumme,
- Gemeinde-Kandidaten,
- PLZ-Kandidaten,
- Distanzwerte bei Fallback,
- automatisches Ergebnis,
- bestätigtes Ergebnis,
- Nutzer,
- Zeitpunkt,
- Begründung manueller Änderungen.

---

## 14. Tests

### 14.1 Reale Referenzdateien

Mindestens:

- TRY2045-Datei im Berliner Stadtgebiet,
- TRY2015-Datei im Potsdamer Stadtgebiet.

Zu prüfen:

- Headerkoordinaten,
- Transformation,
- Deutschlandtreffer,
- erwartete Gemeinde,
- erwartete PLZ nach ausgewähltem PLZ-Datensatz,
- Konsistenz mit Dateinamenkoordinaten.

### 14.2 Unit-Tests

- gültige EPSG:3034-Koordinate,
- fehlender Rechtswert,
- fehlender Hochwert,
- nicht numerische Koordinate,
- unbekanntes CRS,
- Punkt außerhalb Deutschlands,
- Punkt auf Gemeindegrenze,
- Punkt in eindeutigem PLZ-Gebiet,
- Punkt auf PLZ-Grenze,
- keine PLZ gefunden,
- mehrere PLZ-Treffer,
- fehlende lokale Geodatendatei,
- falscher Layername,
- ungültige Geometrien,
- manuelle Bestätigung,
- manuelle Abweichung.

### 14.3 Integrationstests

- kompletter Import mit Standorterkennung,
- offener Import bei Mehrdeutigkeit,
- Aktivierung wird bei blockierendem Status verhindert,
- PLZ-Fehler blockiert gemäß Konfiguration nicht,
- Log enthält alle Standortereignisse,
- erneute Validierung mit neuer Geodatenversion.

### 14.4 Regressionstests

- bestehender TRY-Import bleibt funktionsfähig,
- bestehende Wetteranalyse bleibt unverändert,
- alte regionsbasierte Katalogeinträge bleiben lesbar,
- Streamlit-Auswahl aktiver Wetterdatensätze bleibt funktionsfähig.

---

## 15. Umsetzungsschritte

### Phase 1 – Bestandsanalyse

- aktuelle Parser prüfen,
- Headerauslesung prüfen,
- aktuelle Standortmodelle prüfen,
- aktuelle Streamlit-Importseite prüfen,
- Logging und Validierungsmodelle prüfen,
- vorhandene PLZ-Notizen im Repository suchen,
- bestehende Dependency-Verwaltung prüfen.

**Ergebnis:** Integrationsbericht, noch keine Codeänderung.

### Phase 2 – P008 aktualisieren

- ortsgenaue TRY-Logik aufnehmen,
- alte Klimaregionslogik als Kompatibilitätsweg kennzeichnen,
- Offline-Gemeindeauflösung ergänzen,
- PLZ-Erweiterung ergänzen,
- Entscheidungen und Begründungen dokumentieren,
- diesen Ergänzungsplan nach Integration archivieren.

### Phase 3 – Geodatenkonzept

- Gemeindequelle auswählen,
- PLZ-Quelle auswählen,
- Lizenz prüfen,
- Version festlegen,
- lokale Pfade und Metadaten definieren,
- Prüfsummen erstellen,
- Konfiguration aufbauen.

### Phase 4 – Koordinatenparser und Transformation

- Headerkoordinaten robust lesen,
- EPSG:3034 prüfen,
- Dateinamenkoordinaten optional lesen,
- Transformation kapseln,
- Diagnoseobjekte erzeugen.

### Phase 5 – Gemeindeauflösung

- lokale Geodaten laden,
- Deutschlandprüfung,
- Punkt-in-Polygon,
- Grenzfallbehandlung,
- AGS und Bundesland ausgeben.

### Phase 6 – PLZ-Auflösung

- PLZ-Geodaten laden,
- Punkt-in-Polygon,
- Mehrdeutigkeit behandeln,
- PLZ-Ergebnis getrennt speichern.

### Phase 7 – Validierung und Logging

- neue Statuswerte,
- blockierende Regeln,
- Log-Ereignisse,
- Validierungsbericht,
- manuelle Bestätigung.

### Phase 8 – Streamlit UI

- Standortergebnis darstellen,
- PLZ anzeigen,
- Warnungen und Kandidaten anzeigen,
- manuelle Bestätigung,
- offene Datensätze erweitern.

### Phase 9 – Tests und Dokumentation

- Referenzdateien,
- Unit-Tests,
- Integrationstests,
- Lizenz- und Quellenhinweise,
- Anwenderdokumentation,
- Entwicklerdokumentation.

---

## 16. Abnahmekriterien

Die Erweiterung ist fachlich abgeschlossen, wenn:

- TRY-Rechtswert und -Hochwert automatisch gelesen werden,
- EPSG:3034 korrekt verarbeitet wird,
- die Deutschlandprüfung offline funktioniert,
- Berlin- und Potsdam-Testdatei korrekt erkannt werden,
- Gemeinde und amtlicher Schlüssel offline bestimmt werden,
- die PLZ offline bestimmt oder als nicht verfügbar gekennzeichnet wird,
- Gemeinde und PLZ getrennt gespeichert werden,
- Mehrdeutigkeiten nicht stillschweigend aufgelöst werden,
- manuelle Änderungen protokolliert werden,
- blockierende Standortfehler eine Aktivierung verhindern,
- die Standortauflösung im Import-Log enthalten ist,
- die Standortauflösung im Validierungsbericht enthalten ist,
- Streamlit das Ergebnis verständlich darstellt,
- bestehende Wetterfunktionen nicht beschädigt werden,
- der aktualisierte P008 die neue Logik enthält.

---

## 17. Offene Entscheidungen

Vor der Implementierung zu klären:

1. Welche Gemeinde-Geodatenquelle wird verbindlich genutzt?
2. Welche PLZ-Geodatenquelle ist verfügbar und lizenzrechtlich geeignet?
3. Werden die Geodaten im Repository versioniert oder lokal bereitgestellt?
4. Welche PLZ-Feldnamen und Layernamen liegen tatsächlich vor?
5. Soll eine fehlende PLZ nur warnen oder in bestimmten Workflows blockieren?
6. Welche Distanz ist für einen Gemeinde-Fallback zulässig?
7. Welche Toleranz gilt beim Vergleich Header gegen Dateiname?
8. Wie werden Orte mit mehreren PLZ in der normalen Standortauswahl dargestellt?
9. Sollen PLZ-Daten in `WeatherLocation` gespeichert oder nur dynamisch aufgelöst werden?
10. Wie werden Geodatenupdates versioniert und bestehende Zuordnungen erneut geprüft?
11. Wie werden manuelle Überschreibungen in späteren Varianten und Runs behandelt?

---

## 18. Risiken

- PLZ-Datenquelle ist nicht frei weitergebbar,
- Gemeinde- und PLZ-Geometrien stammen aus unterschiedlichen Ständen,
- generalisierte Flächen erzeugen Grenzabweichungen,
- zusätzliche GIS-Abhängigkeiten erschweren Windows-Installation,
- große Geodatendateien verlangsamen die UI,
- alte P008-Referenzstandortlogik widerspricht ortsgenauen TRY-Dateien,
- automatische PLZ-Zuordnung wird fälschlich als postalische Adresse interpretiert,
- manuelle Korrekturen werden nicht ausreichend protokolliert.

Gegenmaßnahmen:

- Datenquellen abstrahieren,
- Version und Prüfsumme speichern,
- Geodaten einmal laden und cachen,
- Gemeinde als führende Zuordnung verwenden,
- PLZ ausdrücklich als flächenbezogene Zusatzinformation kennzeichnen,
- Tests mit Grenz- und Realfällen,
- alte und neue TRY-Logik im Plan klar trennen.

---

## 19. Auftrag für Codex

Analysiere das vorhandene Repository und den aktiven Plan:

```text
docs/project/plans/inbox/260623_Plan_P008_ma_weather_Gesamtplan.md
```

Analysiere zusätzlich diese Planergänzung zur Offline-Standorterkennung und PLZ-Zuordnung.

### Zuerst nur analysieren

Nimm noch keine Codeänderungen und keine Planänderungen vor.

Liefere:

1. vorhandene Dateien für TRY-Parsing, Standortkatalog, Validierung, Logging und Streamlit,
2. aktuellen Funktionsumfang der Standorterkennung,
3. vorhandene, aber noch nicht umgesetzte PLZ-Notizen,
4. Widersprüche zwischen P008 und ortsgenauen TRY-Dateien,
5. Integrationsvorschlag in die bestehende Architektur,
6. benötigte neue und anzupassende Dateien,
7. benötigte Abhängigkeiten,
8. mögliche Gemeinde- und PLZ-Datenquellen einschließlich Lizenzrisiken,
9. Datenmodelländerungen,
10. Status- und Validierungsänderungen,
11. Testplan,
12. konkrete Aktualisierungsvorschläge für P008,
13. Archivpfad und Archivierungsvermerk für diese Planergänzung.

### Planintegration

Nach meiner Bestätigung:

- aktualisiere den vorhandenen P008,
- behalte die Plannummer P008 bei,
- dokumentiere die Zusammenführung im Änderungsvermerk,
- kennzeichne die alte Klimaregions-/Referenzstandortlogik als Kompatibilitätsweg,
- ergänze die ortsgenaue TRY-Standorterkennung,
- ergänze die optionale PLZ-Auflösung,
- archiviere diese Planergänzung mit Verweis auf den aktualisierten P008.

### Erst danach Implementierungsplan

Lege anschließend einen kleinen, dateibezogenen Implementierungsplan vor.

Implementiere erst nach einer weiteren ausdrücklichen Bestätigung.

### Verbindliche technische Regeln

- keine Online-Geocoding-API im regulären Workflow,
- TRY-Headerkoordinaten sind führend,
- EPSG:3034 wird zentral verarbeitet,
- Deutschland ist der aktuelle Geltungsbereich,
- Gemeinde und PLZ werden getrennt ermittelt,
- Gemeinde beziehungsweise AGS ist die führende administrative Zuordnung,
- PLZ ist zunächst eine optionale Ergänzung,
- automatische und manuell bestätigte Werte bleiben getrennt,
- jede manuelle Abweichung wird begründet und protokolliert,
- keine GIS-Fachlogik direkt in Streamlit,
- bestehende Projektstruktur hat Vorrang,
- keine parallele Modulstruktur erzeugen.
