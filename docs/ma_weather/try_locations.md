# TRY-Dateien und Standorte

Diese Datei dokumentiert, welche lokalen TRY-Kennungen aktuell welchen
Standorten zugeordnet werden. Die echten TRY-Dateien bleiben lokale
Eingabedaten unter `data/ma_weather/input/` und werden nicht im Git-Repo
versioniert.

Stand: 2026-06-26

| TRY-Ordnerkennung | Standort | Status | Vorhandene Dateitypen | Hinweis |
|---|---|---|---|---|
| `TRY_501262086894` | Frankfurt am Main | bekannt | `2015 Jahr/Somm/Wint`, `2045 Jahr/Somm/Wint` | Alle sechs Dateien sind im Wetterkatalog aktiv. |
| `TRY_481399115778` | Muenchen | bekannt | `2015 Jahr/Somm/Wint`, `2045 Jahr/Somm/Wint` | Alle sechs Dateien sind im Wetterkatalog aktiv. |
| `TRY_535578099766` | Hamburg | bekannt | `2015 Jahr/Somm/Wint`, `2045 Jahr/Somm/Wint` | Alle sechs Dateien sind im Wetterkatalog aktiv. |
| `TRY_494997084777` | Mannheim | bekannt | `2015 Jahr/Somm/Wint`, `2045 Jahr/Somm/Wint` | Lokale Dateien werden ueber den TRY-Dateiscan als Datensatzentwuerfe erkannt. |

## Verwendung im Projekt

- Die fachliche Zuordnung fuer bereits katalogisierte Datensaetze erfolgt ueber
  den Wetterkatalog unter `config/ma_weather/datasets/`.
- Die TRY-Ordnerkennung-zu-Standort-Zuordnung fuer neue lokale Dateien liegt
  versioniert unter
  `config/ma_weather/try_locations/example_try_file_locations.yaml`.
- Der technische Schluessel im Projekt ist `weather_key`, zum Beispiel
  `TRY_FFM_2015_JAHR`.
- Die lokale Datei wird ueber `file_path` referenziert.
- Neue lokale TRY-Dateien werden zuerst als Entwuerfe erkannt und erst nach
  Nutzeraktion in den lokalen Katalog unter
  `data/ma_weather/config/datasets/weather_datasets_local.yaml` geschrieben.
- Bestaetigte Mapping-Eintraege duerfen Standort, Rolle und Referenzstandort
  vorbelegen. Candidate- oder offene Zuordnungen bleiben offene Entwuerfe.
- Rechtswert, Hochwert und Hoehenlage aus dem TRY-Kopf duerfen nur einen
  Standortvorschlag erzeugen. Dieser Vorschlag wird erst nach bewusster
  Nutzeraktion uebernommen.

## Pflege-Regel

Nach dem Einfuegen oder Importieren neuer TRY-Dateien muessen folgende Punkte
geprueft und bei Bedarf aktualisiert werden:

- diese Zuordnungstabelle mit vollstaendiger TRY-Ordnerkennung
- die versionierte Mapping-Datei unter `config/ma_weather/try_locations/`
- der Wetterkatalog unter `config/ma_weather/datasets/`
- technische `weather_key` Namen fuer neue Standorte, Jahre oder Szenarien
  mit eindeutiger Endung fuer den Datensatztyp: `_JAHR`, `_SOMM` oder `_WINT`
- Hinweise in `docs/ma_weather/workflow.md`, falls sich der Ablauf aendert
- `CHANGELOG.md`, wenn neue Beispielkonfigurationen, Pfade oder Strukturen
  versioniert werden

## Offene Ergaenzungen

- Weitere Standorte oder Szenarien erst nach fachlicher Zuordnung zu Standort,
  Klimaregion und Referenzstandort aufnehmen. Ohne Mapping erzeugt der Scanner
  offene Entwuerfe statt einer stillen Falschzuordnung.
- Die spaetere PLZ- oder Kartenauswahl soll auf derselben Mapping-Schicht
  aufbauen, ohne Koordinatenvorschlaege automatisch als finale Zuordnung zu
  verwenden.
