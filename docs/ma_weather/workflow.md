# ma_weather Workflow

## Ziel

`ma_weather` bereitet die getrennte Analyse von TRY-Wetterdaten vor. Wetterdaten
sind Eingangs- und Randbedingungsdaten. Sie werden nicht mit den
IDA-ICE-Zonenwerten aus `ma_analyse` vermischt.

## P002 Stand

Der aktuelle Stand umfasst:

- importierbares Paket `src/ma_weather/`
- Wetterkatalog unter `config/ma_weather/datasets/`
- lokale Eingabeordner unter `data/ma_weather/`
- Tests fuer Katalogstruktur und Pflichtfelder
- TRY-Datei einlesen
- Plausibilitaetspruefung
- Wetterkennwerte berechnen
- Wetterdiagramme erzeugen
- Markdown-Wetterbericht schreiben
- Runner fuer die lokale Wetteranalyse

## Geplanter Ablauf

1. Stadt in der Streamlit-Oberflaeche auswaehlen oder eine lokale TRY-Datei
   importieren.
2. Fuer bestehende Katalogeintraege Klimaregion und TRY-Referenzstandort
   automatisch aus dem Standortkatalog ableiten.
3. Fuer ortsgenaue TRY-Dateien Rechtswert und Hochwert aus dem TRY-Kopf als
   fuehrende Standortquelle verwenden.
4. Datensatztyp `Jahr`, `Sommer` oder `Winter` in der UI vorfiltern.
5. TRY-Referenzdatensatz zuerst anbieten, sofern er katalogisiert ist.
6. Standortgenaue Datensaetze fuer die gewaehlte Stadt zusaetzlich anbieten.
7. Wetterdatensatz ueber den Anzeigenamen auswaehlen; `weather_key`, Rolle
   und Status bleiben technische Detaildaten.
8. Fehlende TRY-Jahres-, Sommer- und Winterdateien beim Deutschen
   Wetterdienst herunterladen.
9. Eigene entpackte TRY-`.dat`-Datei in Streamlit im Bereich
   `Wetterdatensaetze` importieren oder manuell unter
   `data/ma_weather/input/` bereitstellen.
10. Manuell abgelegte TRY-Dateien ueber `Lokale TRY-Dateien scannen` als
   Datensatzentwuerfe erkennen und vollstaendige Entwuerfe bewusst in den
   lokalen Katalog uebernehmen.
11. TRY-Datei pruefen und validieren.
12. Import-ID, Quellenmetadaten, Validierungsstatus und Sitzungslog
   miteinander verknuepfen.
13. Wetterkennwerte berechnen.
14. Aufbereitete Wetterdaten unter `data/ma_weather/database/` schreiben.
15. Diagramme unter `data/ma_weather/output/` schreiben.
16. Bericht unter `data/ma_weather/reports/` schreiben.
17. Freigegebene und bewusst uebernommene Entwuerfe im Katalog aktiv fuehren.
18. Einen aktiven Datensatz bewusst als Projekt-Default setzen.
19. Kritische Wetterereignisse aus genau diesem ausgewaehlten Datensatz
    erkennen und fuer spaetere P021-Nutzung anzeigen.

Der DWD-Download bleibt ein manueller Vorbereitungsschritt. Die TRY-Dateien
werden nicht versioniert; im Repo liegen nur Katalogeintraege, Pfade und
Dokumentation.

Lokale UI-Imports werden unter
`data/ma_weather/input/custom/<weather_key>/` abgelegt. Der zugehoerige lokale
Katalog liegt unter
`data/ma_weather/config/datasets/weather_datasets_local.yaml` und wird nicht
versioniert.

Manuell abgelegte TRY-Dateien unter `data/ma_weather/input/TRY_*` werden nicht
automatisch katalogisiert. Die Streamlit-Wetterseite bietet dafuer den Button
`Lokale TRY-Dateien scannen`. Der Scanner liest Dateiname und TRY-Kopf, nutzt
die versionierte Standortzuordnung unter
`config/ma_weather/try_locations/example_try_file_locations.yaml` und zeigt
vollstaendige oder offene Datensatzentwuerfe an.

Unsichere Standortvorschlaege aus TRY-Koordinaten werden in der Fundliste nicht
als erkannte Stadt angezeigt. Ein Standort darf automatisch vorbelegt werden,
wenn ein bestaetigter Dateiverweis, eine bestaetigte TRY-Ordner-Zuordnung oder
eine eindeutige BKG-Gemeindeaufloesung vorliegt und die Gemeinde im
Standortkatalog existiert. Berlin-/Potsdam-nahe TRY-Dateien duerfen ohne diese
belastbare Aufloesung nicht als Hamburg oder anderer Ersatzstandort erscheinen.

## Verbindung zu Varianten

Das Wettermodul erzeugt keine Varianten. Die spaetere Verbindung soll ueber den
technischen `weather_key` laufen:

```text
weather_datasets
climate_file_options
PROJECT_DATA_CLIMATE
Variante
```

Damit bleibt das Wettermodul eigenstaendig und kann gepruefte Wetterdatensaetze
bereitstellen, ohne IDA ICE automatisch zu starten.

## Standortlogik

Die erste P008-Umsetzung nutzt einen YAML-Standortkatalog unter
`config/ma_weather/locations/`. Die Klimaregion wird nicht manuell gewaehlt,
sondern aus der Stadt abgeleitet. Die Klimaregionenkarte wird in Streamlit links
angezeigt, sobald das Bild unter `src/ma_ui/assets/weather/` vorhanden ist.
Der bevorzugte versionierte Dateiname ist
`src/ma_ui/assets/weather/klimaregionen_deutschland.png`; alternativ erkennt die
UI auch die Endungen `.jpg` und `.jpeg` mit demselben Basisnamen.

Fuer ortsgenaue TRY-Dateien ist die Klimaregionslogik nur noch
Kompatibilitaetsweg. Der neue Zielweg liest Rechtswert und Hochwert aus dem
TRY-Kopf, interpretiert sie als EPSG:3034 und loest den Punkt offline ueber
lokale Gemeinde-Geodaten auf. Gemeinde beziehungsweise amtlicher
Gemeindeschluessel sind fuehrend; PLZ-Gebiete sind optional und werden getrennt
behandelt.

Die versionierte Geodatenkonfiguration liegt unter
`config/ma_weather/geodata/example_weather_geodata_sources.yaml`. Lokale
GeoJSON-Dateien liegen unter `data/ma_weather/geodata/` und werden nicht
versioniert. Die Gemeindequelle `bkg_vg250_municipalities` ist aktiviert,
sobald `data/ma_weather/geodata/germany/germany_municipalities.geojson`
vorliegt. Sie nutzt `GEN` als Gemeindenamen, `AGS` als Gemeindeschluessel,
`LKZ` als Bundeslandkennung, `GF = 4` als Flaechenfilter und `EPSG:4326` als
GeoJSON-Koordinatensystem.

Realer Teststand mit lokaler BKG-VG250-Datei:

- `TRY2015_524031130658_Jahr.dat` wird als `Potsdam`, AGS `12054000`,
  LKZ `BB` erkannt.
- `TRY2045_525331134258_Jahr.dat` wird als `Berlin`, AGS `11000000`,
  LKZ `BE` erkannt.

## Status und Aktivierung

Die reduzierte P008-Umsetzung fuehrt drei operative Slices:

1. Bestand, Realtests und Auswahlstatus.
2. Importnachweis und offene Datensaetze.
3. Aktivierung, Projekt-Default und Uebergabegrenze.

Die lokale UI kann den Bestand pruefen und zeigt pro `weather_key`, ob die
Datei fehlt, vorhanden ist, Warnungen besitzt, fehlerhaft ist oder freigegeben
wurde. Jeder Analyseimport erzeugt eine `import_id`, die mit `session_id`,
`run_id`, Quelle, Validierung und Sitzungslog verbunden wird.

Die Streamlit-Schritte `Import`, `Scannen` und `Pruefen` sitzen unten im
Bereich `Wetterdatensaetze`. `Import` legt Dateien nur ab, `Scannen` erzeugt
Datensatzentwuerfe und `Pruefen` erlaubt Anpassung und bewusste
Registrierung. Erfolgreich gepruefte und bewusst uebernommene Entwuerfe werden
im Katalog direkt aktiv, setzen aber keinen Projekt-Default. Unter den drei
Schritten steht die separate Aktion `Datensatzbestand pruefen`; sie laedt den
Katalog neu, validiert die Dateien und aktualisiert die Statusanzeige. Ohne
aktive Funktion zeigt der Bereich die getrennten
Uebersichten `Aktive Wetterdatensaetze` und `Offene Wetterdatensaetze`.
Bei `Pruefen` gibt es die Ansichten `Gefundene lokale TRY-Dateien` und
`Parameter pruefen`. Die Fundliste ist reduziert; die Parameter-Maske
zeigt nur `Feld` und `Wert` fuer Stadt, Bezugsjahr, Datensatztyp und
Szenario. Rolle, `weather_key` und Anzeigename werden aus diesen Angaben
generiert und nicht als eigene Eingabefelder angezeigt. Offene Datensaetze
sind sichtbar, aber nicht regulaer auswaehlbar.

Die obere Wetterauswahl bleibt bewusst schlank und unterscheidet zwischen den
Modi `Stadt` und `Klimaregion`. Im Stadtmodus wird eine konkrete Stadt
gewaehlt; standortgenaue Datensaetze werden dann bevorzugt und der
Referenzdatensatz der Klimaregion bleibt als Vergleich/Fallback verfuegbar. Im
Klimaregionsmodus wird keine Stadt angenommen; regulaer angeboten werden nur
TRY-Referenzdatensaetze des Referenzstandorts der gewaehlten Klimaregion. In
beiden Modi wird der Datensatztyp ueber eine segmentierte Auswahl `Jahr`,
`Sommer` oder `Winter` gewaehlt. Aktuell ist genau ein Datensatztyp aktiv. Die
anschliessende Datensatzliste zeigt nur Anzeigenamen; technische Details wie
`weather_key`, Rolle, Dateistatus und Aktivierungsstatus bleiben in den
Tabellen und Pruefbereichen sichtbar.

Eine spaetere Mehrfachauswahl mehrerer Wetterdatensaetze fuer Vergleichsanalysen
bleibt als Ziel vorgemerkt. Dafuer muessen Analyseausfuehrung,
Diagrammaufbau, Ergebniszustand und Ereignisauswertung separat erweitert
werden.

Das Standort-Mapping nutzt zuerst die versionierte TRY-Ordner-Zuordnung. Nur
bestaetigte Zuordnungen duerfen automatisch vorbelegen. Danach kann eine
eindeutige lokale BKG-Gemeindeaufloesung aus Rechtswert, Hochwert und
Hoehenlage den Standort vorbelegen, wenn die Gemeinde im Standortkatalog
vorhanden ist. Reine Naechstvorschlaege ohne Gemeinde-Treffer bleiben
Vorschlaege und muessen bewusst uebernommen werden.

Projekt-Default und Auswahlstatus werden lokal unter
`data/ma_weather/database/weather_selection_state.yaml` gespeichert. Diese Datei
ist lokale Arbeitskonfiguration und wird nicht versioniert. Ein Import setzt
keinen Katalogeintrag, keine Aktivierung und keinen Projekt-Default automatisch.
Ein erfolgreich gepruefter Entwurf wird erst durch die bewusste Uebernahme
registriert und aktiv; der Projekt-Default bleibt danach eine getrennte
Nutzeraktion.

## Kritische Wetterereignisse

Sommer- und Winter-TRY-Dateien werden als eigene Wetterdatensaetze katalogisiert
und nicht aus Jahresdatensaetzen gefiltert. Die Ereignisanalyse arbeitet immer
auf dem aktuell ausgewaehlten `weather_key`.

Erkannt werden:

- heissester Tag,
- kaeltester Tag,
- heisseste Drei-Tage-Periode,
- kaelteste Drei-Tage-Periode,
- strahlungsreichster Tag, falls Globalstrahlung vorhanden ist,
- windstaerkster Tag, falls Windgeschwindigkeit vorhanden ist.

Die Ereignisse werden in Streamlit angezeigt und koennen fuer eine spaetere
P021-Anbindung vorgemerkt werden. In diesem Slice erfolgt noch keine
automatische Uebergabe an P021.
