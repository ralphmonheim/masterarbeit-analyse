# Changelog

Alle nennenswerten Aenderungen an `ma_analyse` werden in dieser Datei dokumentiert.

## 0.2.0 - 2026-05-24

### Added
- `CHANGELOG.md` als zentrale Aenderungshistorie eingefuehrt.
- Laufprotokolle mit Schritt- und Gesamtlaufzeiten fuer Analysebefehle ergaenzt.
- `data/`-Ordnerstruktur mit versionierten Platzhalterdateien vorbereitet.
- Minimale Tests fuer CLI, Konfiguration, Logging, Varianten und Zeitfenster ergaenzt.

### Changed
- Projekt von losen Skripten zu einem Paket mit `src/ma_analyse` umgebaut.
- Code fachlich in `app`, `core`, `preprocessing`, `analysis`, `analysis/components`, `gui` und `settings` strukturiert.
- CLI-Einstieg auf `python -m ma_analyse ...` und `ma-analyse ...` ausgerichtet.
- Datenordner auf `data/input`, `data/database`, `data/output` und `data/test_output` umgestellt.
- `requirements.txt` auf direkte Runtime-Abhaengigkeiten reduziert.
- GUI so angepasst, dass der `all`-Befehl automatisch alle Raeume auswaehlt.

### Removed
- Alte Skriptstruktur unter `Skripte/` als Hauptschnittstelle entfernt.
- Uebergangsmodul `pipeline.py` entfernt, nachdem CLI, Commands und GUI ausgelagert wurden.
- Alte Root-Module wie `config.py`, `commands.py`, `heating.py`, `cooling.py`, `prepare.py`, `comfort.py` und `analyze.py` durch Paketmodule ersetzt.

## 0.1.0 - 2026-05-24

### Added
- Erster Paketstand fuer `ma_analyse` mit zentralem CLI-Einstieg.
