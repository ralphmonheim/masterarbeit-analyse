# P018 ma_simulation_setup und Run-Manifest

Stand: 2026-06-22
Status: Geplant
Prioritaet: Hoch
Abhaengigkeiten: P008, P011, P017

## Ziel

Varianten, Wetter, Zeitraum, Zeitschritt, Ausgabeumfang und Modellreferenz als
validierten Simulationslauf festlegen.

## Reifegrad

Produktiver Vorbereitungsschritt ohne Simulationssteuerung.

## Arbeitspakete

- Projektweit eindeutige Run-ID und Statusmodell definieren.
- `RunManifest` mit Projekt, Modellstand, Parametersnapshot, Varianten,
  `weather_key`, Zeitraum, Zeitschritt und Ausgabeanforderungen planen.
- Standard-Jahreslauf und ereignisbezogene Laufarten unterscheiden.
- UI-Eingabe, YAML-Import und Validierungsbericht vorsehen.
- Uebergabegrenze zu P009 dokumentieren.

## Akzeptanzkriterien

- Ein Run ist ohne IDA-Installation vollstaendig beschreibbar.
- Fehlende Referenzen blockieren die Freigabe.
- Manifest ist unveraenderlich versionierbar und reproduzierbar.
- Kein Simulationsstart und keine Modellmanipulation erfolgen.
