# P030 research_tools Prozessmessung und Vergleichsauswertung

Stand: 2026-07-14
Status: Fachlich geplant, von der Produktivsoftware getrennt
Prioritaet: Hoch fuer die Methodik der Masterarbeit
Abhaengigkeiten: technische Logs aus P011-P021; keine Rueckabhaengigkeit der Fachmodule

## Ziel

`research_tools` ist die getrennte Forschungsschicht der Masterarbeit. Sie
erfasst und vergleicht Preprocessing-, Simulations- und Postprocessing-Zeit,
aktive Nutzerzeit, Maschinenzeit, Pruef-/Korrekturzeit, Fehler und
Wiederholungen. Sie erzeugt daraus Tabellen, Diagrammdaten und methodische
Vergleichsberichte.

Die produktive Fachsoftware bleibt davon unabhaengig: Ein Run, eine Variante
oder eine Freigabe haengen nie von einer Prozessmessung ab.

## Grenzen und Prozessmodi

Gemessen werden drei getrennte Prozessgrenzen:

- Preprocessing: von der Projekterstellung bis zum dokumentierten
  P018-Runstatus, mindestens `preview_prepared`.
- Simulation: vom manuellen Start bis zum Abschluss im Zielprogramm.
- Postprocessing: von bereitstehenden Ergebnissen bis zum definierten
  Analyse-, Diagramm- oder Berichtsartefakt.

Die Prozessmodi sind `manual`, `software_assisted` und
`automated_concept`. Der konzeptionell automatisierte Modus wird klar als
Schätzung oder Zielwert gekennzeichnet und nicht als beobachtete Messung
ausgegeben.

## Datenmodell

Ein `ProcessEvaluation` referenziert optional `PRJ`, `SDIR`, `STC`, `RUN` und
`VAR`, ohne deren Fachwerte zu kopieren. Es enthält:

- Prozessmodus und explizite Prozessgrenze,
- Zeitwerte für aktive Nutzerzeit, Maschinenzeit, Pruefzeit, Korrekturzeit
  und verstrichene Gesamtzeit,
- Herkunft jedes Messwerts: `observed`, `manual_entry`, `log_derived`,
  `calculated` oder `estimated`,
- Fehler-, Warnungs-, Wiederholungs- und Dateimetriken,
- Versuchskonfiguration, Notizen und Referenzen auf technische Logs.

Die Forschungsdaten liegen ausserhalb produktiver Run-Ordner, etwa unter
`research_measurements/EVAL-<id>/`. Sie bestehen aus `evaluation.yaml`,
manuellen Messwerten, referenzierten oder kopierten Logs, abgeleiteten
Kennzahlen und Notizen.

## Log-Anforderungen

P030 liest technische Logs nur lesend. P027 stellt dafuer, soweit sinnvoll,
Zeitstempel, Modul, Operation, Status, Dauer, betroffene Objekt-IDs,
Warnungs-/Fehlercodes sowie Objekt-, Datei- und Datenmengen bereit.

P030 speichert manuelle Eingaben getrennt von Logdaten. Ohne auswertbares
Simulationslog darf die Simulationsdauer manuell eingegeben werden, muss dann
aber als `manual_entry` gekennzeichnet sein.

## Vergleichskennzahlen

- aktive Nutzer-, Maschinen-, Pruef-, Korrektur-, Simulations- und
  Postprocessing-Zeit,
- Zeit je Variante, Anzahl Arbeitsschritte, manuelle Eingriffe,
  Medienbrueche und Wiederholungen,
- erkannte/korrigierte Fehler, offene Warnungen, Vollstaendigkeit und
  Reproduzierbarkeit,
- Dateianzahl, Speicherbedarf und Packaging-Aufwand.

Abgeleitete Kennzahlen wie Zeitersparnis und Beschleunigungsfaktor duerfen nur
berechnet werden, wenn Prozessgrenze und Messherkunft vergleichbar sind.

## Umsetzungsslices

### P030-S1 Datenmodell

- `ProcessEvaluation`, Prozessgrenzen, Prozessmodi und Messwertherkunft.
- YAML-/CSV-Schemas und Validierung eindeutiger Referenzen.

### P030-S2 Manuelle Versuchserfassung

- Pre-, Simulations- und Postprocessing-Zeiten, Notizen und
  Versuchskonfiguration.
- Referenzen auf Projekt-, Study- und Run-IDs.

### P030-S3 Log-Import

- generische Schnittstelle fuer eigene technische JSONL-/Textlogs,
- Zuordnung zu Prozessabschnitten und Ableitung der Maschinenzeit.

### P030-S4 Vergleich und Reporting

- mindestens zwei vergleichbare Versuche,
- CSV-Ausgabe, Tabellen, Diagrammdaten und Kennzeichnung geschaetzter Werte.

## Akzeptanzkriterien

- Preprocessing, Simulation und Postprocessing sind getrennt auswertbar.
- Aktive Nutzerzeit und Maschinenzeit werden getrennt ausgewiesen.
- Messwerte sind nach Herkunft eindeutig gekennzeichnet.
- Mindestens ein manueller und ein softwareunterstuetzter Versuch sind
  vergleichbar.
- Forschungsergebnisse veraendern keine Fachobjekte, Varianten, Runs oder
  Freigaben.

## Nicht Teil der Masterarbeit

- Bildschirmaufzeichnung und vollautomatische Erfassung aller
  Nutzerinteraktionen,
- Auswertung fremder proprietaerer Logs ohne dokumentiertes Format,
- produktive Telemetrie, Cloud-Dashboard und Prozesszeitprognosen.
