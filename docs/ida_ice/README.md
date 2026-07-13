# IDA ICE

## Zweck

Externe Simulationsumgebung fuer die manuell ausgefuehrten Gebaeude- und
TGA-Simulationen.

## Eingaben

- geprueftes Referenzmodell
- Exportpaket, Variantenparameter, Wetterdaten und Simulationssetup

## Ausgaben

- Simulationsergebnisse und Simulationsmeldungen

## Abgrenzung

- kein Python-Paket dieses Projekts
- keine ungesicherte IDM-Manipulation oder erfundene API-Steuerung
- manueller Simulationsstart ist eine verbindliche Compliance-Grenze;
  automatisierte Starts, Batch-Laeufe und eine Nutzung als Simulationsserver
  sind ohne ausdrueckliche EQUA-Freigabe ausgeschlossen
- vollstaendige oder unbekannte IDA-Dateien, Bibliotheken und NMF-Modelle
  werden vor einer Verarbeitung nach `docs/compliance/ida_ice/` klassifiziert

## Abhaengigkeiten

- `ma_export_simulation.adapters.ida_ice`
- lokale IDA-ICE-Installation und manueller Simulationslauf

## Status

Manueller externer Schritt.

## Naechster Schritt

Erforderliche Eingabe- und Ergebnisartefakte in P009 verbindlich
dokumentieren.

## Compliance-Pruefung

Die technische und vertragliche Vorpruefung liegt unter
`docs/compliance/ida_ice/`. Vor einer IDA-bezogenen Implementierung wird eine
`compliance_decision` mit Klasse `green`, `yellow` oder `red` dokumentiert.
Bei `yellow` ist der Preflight erforderlich; bei `red` erfolgt keine
Dateioperation oder Implementierung ohne ausdrueckliche EQUA-Freigabe.
