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

1. Stadt in der Streamlit-Oberflaeche auswaehlen.
2. Klimaregion und TRY-Referenzstandort automatisch aus dem Standortkatalog
   ableiten.
3. TRY-Referenzdatensatz zuerst empfehlen, sofern er katalogisiert ist.
4. Standortgenaue Datensaetze fuer die gewaehlte Stadt zusaetzlich anbieten.
5. Datensatz ueber `weather_key` aus dem Katalog auswaehlen.
6. Fehlende TRY-Jahres-, Sommer- und Winterdateien beim Deutschen
   Wetterdienst herunterladen.
7. Eigene entpackte TRY-`.dat`-Datei in Streamlit im Bereich
   `Wetterdatensaetze` importieren oder manuell unter
   `data/ma_weather/input/` bereitstellen.
8. Manuell abgelegte TRY-Dateien ueber `Lokale TRY-Dateien scannen` als
   Datensatzentwuerfe erkennen und vollstaendige Entwuerfe bewusst in den
   lokalen Katalog uebernehmen.
9. TRY-Datei importieren und validieren.
10. Import-ID, Quellenmetadaten, Validierungsstatus und Sitzungslog
   miteinander verknuepfen.
11. Wetterkennwerte berechnen.
12. Aufbereitete Wetterdaten unter `data/ma_weather/database/` schreiben.
13. Diagramme unter `data/ma_weather/output/` schreiben.
14. Bericht unter `data/ma_weather/reports/` schreiben.
15. Freigegebene Datensaetze bewusst aktivieren.
16. Einen aktivierten Datensatz bewusst als Projekt-Default setzen.
17. Kritische Wetterereignisse aus genau diesem ausgewaehlten Datensatz
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

## Status und Aktivierung

Die reduzierte P008-Umsetzung fuehrt drei operative Slices:

1. Bestand, Realtests und Auswahlstatus.
2. Importnachweis und offene Datensaetze.
3. Aktivierung, Projekt-Default und Uebergabegrenze.

Die lokale UI kann den Bestand pruefen und zeigt pro `weather_key`, ob die
Datei fehlt, vorhanden ist, Warnungen besitzt, fehlerhaft ist oder freigegeben
wurde. Jeder Analyseimport erzeugt eine `import_id`, die mit `session_id`,
`run_id`, Quelle, Validierung und Sitzungslog verbunden wird.

Die Streamlit-Schritte `Import`, `Scannen` und `Validieren` sitzen unten im
Bereich `Wetterdatensaetze`. `Import` legt Dateien nur ab, `Scannen` erzeugt
Datensatzentwuerfe und `Validieren` erlaubt Anpassung und bewusste
Registrierung. Ohne aktive Funktion zeigt der Bereich die getrennten
Uebersichten `Aktive Wetterdatensaetze` und `Offene Wetterdatensaetze`. Bei
`Validieren` gibt es die Ansichten `Offene Datensaetze` und
`Key-Parameter pruefen`. Die Key-Parameter-Maske zeigt gelesene Dateiwerte,
Mapping-Hinweise und bearbeitbare Zielwerte direkt zusammen. Offene
Datensaetze sind sichtbar, aber nicht regulaer auswaehlbar.

Das Standort-Mapping nutzt zuerst die versionierte TRY-Ordner-Zuordnung. Nur
bestaetigte Zuordnungen duerfen automatisch vorbelegen. Rechtswert, Hochwert
und Hoehenlage aus dem TRY-Kopf erzeugen hoechstens einen Standortvorschlag,
der bewusst uebernommen werden muss.

Aktivierung und Projekt-Default werden lokal unter
`data/ma_weather/database/weather_selection_state.yaml` gespeichert. Diese Datei
ist lokale Arbeitskonfiguration und wird nicht versioniert. Ein Import setzt
weder Aktivierung noch Projekt-Default automatisch.

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
