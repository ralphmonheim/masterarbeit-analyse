# P033 Wetterdaten TRY 2010/2035 aufnehmen

Stand: 2026-07-25
Status: Katalogaufnahme umgesetzt; PRN-Adapter und Zeitreihenpruefung zurueckgestellt

## Ziel

Die 90 lokalen TRY-PRN-Dateien und die zugehoerige IDM-Datei werden als
nachvollziehbare Wetterreferenzen fuer `ma_weather` vorbereitet. Der
freigegebene erste Slice beschraenkt sich auf Katalogsicht und korrekte
Referenzstadtzuordnung. Rohdateien bleiben unveraendert.

## Umgesetzter Katalogslice 2026-07-25

- 90 stabile `weather_key`-Eintraege fuer `2 x 15 x 3` im lokalen,
  unversionierten Wetterkatalog
- Zuordnung der Regionen 01-15 zu Bremerhaven, Rostock, Hamburg, Potsdam,
  Essen, Bad Marienberg, Kassel, Braunlage, Chemnitz, Hof, Fichtelberg,
  Mannheim, Muehldorf, Stoetten und Garmisch-Partenkirchen
- Region 13 behaelt `Muehldorf` als sichtbaren PRN-Ort aus der IDM-Datei und
  nutzt fuer die bestehende Regionsfilterung den heutigen TRY13-
  Referenzknoten `Passau`; der 2015/2045-Standortkatalog wird nicht
  umgedeutet
- Anzeige als TRY-Referenzdatensaetze bei der zugehoerigen Stadt und
  Klimaregion
- Kennzeichnung `analysis_supported: false` und sichtbarer Hinweis
  `nur katalogisiert`
- Analysesicherung in Streamlit, Statuspruefung und Runner; kein Durchreichen
  der PRN-Dateien an den bestehenden TRY-`.dat`-Importer
- bestehende DWD-TRY-`.dat`-Analysen bleiben unveraendert verfuegbar

Die Katalogeintraege referenzieren die Originaldateien vorlaeufig an ihrem
bestehenden lokalen Eingangspfad. Es wurden keine Wetterstunden importiert,
normalisiert, gekuerzt oder kopiert.

## Eingang

- `DWD TRY Daten 2011.idm`
- 90 PRN-Dateien:
  - Klimaperioden 2010 und 2035
  - TRY-Regionen 01 bis 15
  - jeweils `Jahr`, `Somm` und `Wint`
- bekannte Namensabweichung: Zone 10 verwendet bei Winterdateien `_wint_`

Die Jahreszahlen bezeichnen Wetterperioden beziehungsweise Szenarien und
werden nicht als Projekt- oder Simulationsjahr interpretiert.

## Abgrenzung

- keine automatische Wetterauswahl allein aus Dateinamen
- keine Veraenderung der Originaldateien
- keine Vermischung unterschiedlicher TRY-Generationen
- keine Freigabe fuer Simulation oder Veroeffentlichung ohne dokumentierte
  Datenrechte und dokumentierte Pruefung bei `update repo`

## Umsetzungsslices

### P033-W1 Metadatenregister und Katalogsicht

1. Datei, Periode, Region, Saison, Groesse und SHA-256 erfassen.
2. Anbieter, Produktbezeichnung, Lizenz-/Belegreferenz und IDM-Zuordnung
   dokumentieren.
3. Originale im lokalen Wettereingang unveraendert erhalten.

Status: fuer Datei, Periode, Region, Datensatztyp, Referenzstadt und lokale
Katalogsicht umgesetzt. Groesse und Hash werden in diesem reduzierten Slice
noch nicht als persistierter Importnachweis
gefuehrt.

Akzeptanz: Alle 90 PRN-Dateien sind eindeutig katalogisiert, lokal vorhanden
und ohne Inhaltsveraenderung ihrer Referenzstadt zugeordnet.

### P033-W2 Importvertrag

Status: bewusst zurueckgestellt; nicht Teil der Freigabe vom 2026-07-25.

1. PRN-Header, Spalten, Einheiten, Zeitschritt, Zeitzone, Kalender und
   Fehlwertkennzeichnung gegen den bestehenden `ma_weather`-Import abgleichen.
2. Region und Standortbezug aus zulaessigen IDM-/Dateimetadaten ableiten.
3. Kanonische Wetter-ID und Importversion definieren.
4. Transformationen und Einheitenumrechnungen protokollieren.

Akzeptanz: Ein einzelner Referenzdatensatz kann reproduzierbar importiert und
mit seiner Quelle ausgegeben werden.

### P033-W3 Matrix- und Datenvalidierung

Status: Matrixvollstaendigkeit auf Katalog-/Dateiebene geprueft;
Zeitreihenvalidierung bleibt bis zum PRN-Adapter zurueckgestellt.

1. Vollstaendigkeit `2 x 15 x 3` pruefen.
2. 8760/8784 Stunden, monotone Zeitachse, Luecken, Duplikate und Fehlwerte
   pruefen.
3. Temperatur, Feuchte, Strahlung und Wind auf plausible Wertebereiche und
   physikalische Konsistenz pruefen.
4. Schreibweisen wie `_Wint_` und `_wint_` explizit testen.

Akzeptanz: Fehler blockieren, Warnungen bleiben sichtbar und kein Datensatz
wird stillschweigend korrigiert.

### P033-W4 Auswahl und Sensitivitaet

Status: Kataloganzeige umgesetzt; Analyse, Simulation und Sensitivitaet bleiben
bis zum PRN-Adapter zurueckgestellt.

1. Zweck je Wetterfall festlegen: typisches Jahr, Dimensionierung,
   sommerlicher Komfort oder Klimasensitivitaet.
2. Basisklima und warmes Szenario getrennt auswaehlen.
3. Wetter-ID in Run-Manifest, Ergebnis und Bericht weiterreichen.
4. Standortpassung und Grenzen synthetischer TRY-Daten dokumentieren.

Akzeptanz: Variantenvergleiche verwenden explizit denselben Wetterstand oder
weisen Wetterunterschiede als eigene Einflussgroesse aus.

## Tests

- Metadaten- und Matrixvalidator mit synthetischer kleiner Fixture
- Parser-Smoke-Test fuer genau einen freigegebenen PRN-Datensatz
- Regression fuer Winter-Schreibvariante der Zone 10
- Fehlerfaelle fuer fehlende Datei, falsche Stundenzahl, Duplikate und
  unbekannte Einheit

## Offene Nachweise

- konkrete DWD-/TRY-Produkt- und Lizenzreferenz
- zulässige lokale Verarbeitung, Repository-Ablage und Veroeffentlichung
- IDM-Semantik und Formatstand
- Auswahlregel fuer Projektstandort und Untersuchungsziel

## Abhaengigkeiten

P008, P018, P021 und P027.

## Konsolidierter UI- und Ablagebezug 2026-07-27

UD-106 uebergibt Land und Stadt aus `ma_project` nur als Vorschlag an
`ma_weather`; fehlt die Stadt im Katalog, bleibt die Auswahl manuell.
Die Wetteransicht wird in `Analyse | Diagramme | Verwaltung` mit
`Import | Scannen | Pruefen` unter Verwaltung gegliedert.

Die getrennte Ablageumsetzung wurde am 2026-08-11 ausdruecklich freigegeben:
90 PRN-Dateien liegen inhaltlich unveraendert unter
`data/ma_weather/input/prn/`, die IDM-Datei unter
`data/ma_weather/input/idm/`. Alle 90 lokalen P033-Katalogreferenzen wurden
atomar aktualisiert und durch SHA-256-Abgleich geprueft. Der weiterhin
gesperrte Analyseadapter wurde dadurch nicht freigegeben oder geaendert.
