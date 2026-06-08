# Datenbankmigrationen

Dieser Ordner gehoert zu Alembic und versioniert die PostgreSQL-Datenbankstruktur
fuer den Variantenkern. Er ist kein Datenordner fuer Analyseausgaben,
IDA-Importe oder Ergebnisdateien.

`alembic.ini` verweist mit `script_location = migrations` auf diesen Ordner.
Die Laufumgebung in `env.py` laedt die SQLAlchemy-Metadaten aus
`ma_variants.database.models`.

## Struktur

```text
migrations/
  env.py              Alembic-Laufumgebung
  script.py.mako      Vorlage fuer neue Migrationen
  versions/           versionierte Datenbankmigrationen
```

`versions/` enthaelt die einzelnen Migrationen fuer die Kern-, Systemtemplate-,
Wirtschaftlichkeits- und Katalogtabellen.

Migrationen sollen nicht manuell geloescht oder umbenannt werden, weil Alembic
die Reihenfolge ueber Revisionen und `down_revision` verfolgt. `__pycache__/`
ist nur Python-Cache und fachlich unwichtig.

## Typische Befehle

```powershell
alembic upgrade head
alembic downgrade -1
alembic history
alembic current
```
