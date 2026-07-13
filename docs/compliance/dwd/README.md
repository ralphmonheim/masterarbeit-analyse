# DWD-Wetterdaten-Compliance

Stand: 2026-07-13
Status: technische und vertragliche Vorpruefung, keine Rechtsberatung

## Ergebnis

Die DWD-Daten muessen nach ihrem konkreten Bezugsweg getrennt werden:

1. Frei zugaengliche DWD-Geodaten und OpenData-Dienste duerfen nach den
   offiziellen rechtlichen Hinweisen unter CC BY 4.0 mit Quellenvermerk
   weiterverwendet werden.
2. Registrierungspflichtige, bestellte oder individuell bereitgestellte
   Leistungen unterliegen dem konkreten Angebot und den DWD-AGB. Nach
   AGB-Abschnitt 12 sind Weitergabe und Veroeffentlichung auch in bearbeiteter
   Form nur im vereinbarten Nutzungsrahmen zulaessig.

Der registrierungspflichtige TRY-Zugang akzeptiert AGB und Disclaimer. Daher
ist eine TRY-Datei nicht allein wegen ihres DWD-Ursprungs automatisch
OpenData.

## Projektregel fuer den vorhandenen Bestand

Das lokale TRY-2011-/IDA-ICE-Paket besitzt derzeit keinen ausreichend
dokumentierten Bezugs- und Lizenznachweis. Es bleibt:

```yaml
classification: yellow
decision: local_review_only
redistribution_allowed: unknown
cloud_processing_allowed: false
repository_storage_allowed: false
```

Lokales, fachlich begrenztes Lesen oder Konvertieren ist erst nach ausgefuelltem
Preflight zulaessig. Roh- oder konvertierte Wetterdatensaetze werden nicht
versioniert oder weitergegeben.

## Offene DWD-OpenData

Ein konkreter Datensatz kann Gruen werden, wenn offizielle URL, CC-BY-4.0-
Hinweis, Drittanbieterhinweise, Abrufdatum und SHA-256 dokumentiert sind.
Quellenvermerk und Bearbeitungshinweise muessen in Metadaten und Ausgaben
erhalten bleiben.

Die Projektgovernance bleibt strenger als die offene Lizenz: reale
Wetterdateien liegen lokal unter `data/ma_weather/` und nicht im Git-Repo.

## Datenschutz

Die DWD-Datenschutzinformation regelt Kunden-, Registrierungs-, Kontakt- und
Zugangsdaten; sie ist keine Wetterdatenlizenz. Namen, Adressen, E-Mail,
Telefon, Kundenkonto, Kennungen, Passwoerter und Zahlungsdaten duerfen nicht
im Repository oder in Datensatzmetadaten gespeichert werden.
