# ma_weather Befehle

Das Wettermodul ist aktuell vorbereitet, aber noch nicht fachlich implementiert.

## Aktueller Status

- Es gibt noch kein Paket `src/ma_weather/`.
- Es gibt noch keinen CLI-Befehl fuer TRY-Import oder Wetterauswertung.
- Der Plan liegt unter `docs/project/plans/inbox/250603_Plan_Wetterdatenanalyse_TRY_Integration.md`.

## Aktuelle Pruefung

Bis zur Umsetzung des Wettermoduls gelten nur die allgemeinen Projektpruefungen:

```powershell
.\.venv\Scripts\python.exe -m ruff check src tests --no-cache
.\.venv\Scripts\python.exe -m pytest
```

## Geplante Befehle

Nach Umsetzung von P002 koennen hier Befehle fuer folgende Schritte ergaenzt werden:

- TRY-Datei importieren
- Wetterdatensatz validieren
- Wetterkennwerte berechnen
- Wetterdiagramme erzeugen
- Wetterbericht exportieren
