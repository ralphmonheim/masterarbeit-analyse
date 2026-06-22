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

## Abhaengigkeiten

- `ma_export_simulation.adapters.ida_ice`
- lokale IDA-ICE-Installation und manueller Simulationslauf

## Status

Manueller externer Schritt.

## Naechster Schritt

Erforderliche Eingabe- und Ergebnisartefakte in P009 verbindlich
dokumentieren.
