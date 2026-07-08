# Kalender-Datenbereich

Dieser Ordner verwaltet lokale Kalender- und Feiertagsdaten in der
Entwicklungsphase. Er ist ein gemeinsamer Datenbereich und kein Python-Modul.

## Struktur

```text
data/common/kalender/
  2025/
    incoming/   # Originalpakete
    extracted/  # entpackte Kalender-/Feiertagsdaten
```

## Regeln

- Inhalte unter `incoming/` und `extracted/` bleiben lokal und werden nicht
  versioniert.
- Kalenderdaten koennen spaeter Nutzungszeiten, Bewertungszeitraeume oder
  Randbedingungen unterstuetzen.
- Eine allgemeine Kalender-API ist noch nicht umgesetzt.
