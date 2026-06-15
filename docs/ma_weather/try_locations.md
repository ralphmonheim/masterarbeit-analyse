# TRY-Dateien und Standorte

Diese Datei dokumentiert, welche lokalen TRY-Kennungen aktuell welchen
Standorten zugeordnet werden. Die echten TRY-Dateien bleiben lokale
Eingabedaten unter `data/ma_weather/input/` und werden nicht im Git-Repo
versioniert.

Stand: 2026-06-15

| TRY-Ordnerkennung | Standort | Status | Vorhandene Dateitypen | Hinweis |
|---|---|---|---|---|
| `TRY_501262086894` | Frankfurt am Main | bekannt | `2015 Jahr/Somm/Wint`, `2045 Jahr/Somm/Wint` | `2015 Jahr` und `2045 Jahr` sind im Wetterkatalog aktiv. |
| `TRY_481399115778` | Muenchen | bekannt | `2015 Jahr/Somm/Wint`, `2045 Jahr/Somm/Wint` | `2015 Jahr` und `2045 Jahr` sind im Wetterkatalog aktiv. |
| `TRY_535578099766` | Hamburg | bekannt | `2015 Jahr/Somm/Wint`, `2045 Jahr/Somm/Wint` | `2015 Jahr` und `2045 Jahr` sind im Wetterkatalog aktiv. |

## Verwendung im Projekt

- Die fachliche Zuordnung erfolgt ueber den Wetterkatalog unter
  `config/ma_weather/datasets/`.
- Der technische Schluessel im Projekt ist `weather_key`, zum Beispiel
  `TRY_FFM_2015`.
- Die lokale Datei wird ueber `file_path` referenziert.
- Wenn weitere TRY-Dateien genutzt werden, soll diese Liste zusammen mit dem
  Wetterkatalog aktualisiert werden.

## Pflege-Regel

Nach dem Einfuegen oder Importieren neuer TRY-Dateien muessen folgende Punkte
geprueft und bei Bedarf aktualisiert werden:

- diese Zuordnungstabelle mit vollstaendiger TRY-Ordnerkennung
- der Wetterkatalog unter `config/ma_weather/datasets/`
- technische `weather_key` Namen fuer neue Standorte, Jahre oder Szenarien
- Hinweise in `docs/ma_weather/workflow.md`, falls sich der Ablauf aendert
- `CHANGELOG.md`, wenn neue Beispielkonfigurationen, Pfade oder Strukturen
  versioniert werden

## Offene Ergaenzungen

- Entscheidung, ob zusaetzlich `Somm` oder `Wint` in den aktiven
  Wetterkatalog aufgenommen werden sollen.
- Namensschema fuer weitere `weather_key` Werte bestaetigen, zum Beispiel
  `TRY_MUC_2015_SOMM` oder `TRY_HAM_2015_WINT`.
