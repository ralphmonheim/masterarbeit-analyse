# P010 Eingabe- und Datenhaltungsarchitektur

Stand: 2026-06-23
Status: Umgesetzt und archiviert
Prioritaet: Hoch
Bezug: P007

## Ziel

Eine formatneutrale Grundlage fuer alle Randbedingungen schaffen. Jedes
Eingabemodul darf Import, manuelle Eingabe oder Demo-Daten anbieten; Import
wird fuer die Masterarbeit bevorzugt.

## Verbindliche Entscheidungen

- Externe Formate werden ueber Adapter in neutrale Fachmodelle ueberfuehrt.
- Originaldatei, Importzeitpunkt, Adapter, Warnungen und Validierungsstatus
  bleiben nachvollziehbar.
- YAML ist der erste menschenlesbare Projektstand, aber keine dauerhaft
  festgeschriebene oder einzige Formatschnittstelle.
- Eine Datenbank wird erst nach stabilen Fachmodellen und Abfragen festgelegt.
- Die Quellenwahl erfolgt je Modul, nicht projektweit.
- Versionierte Vorlagen bleiben unveraendert. Eigene Arbeitsstaende werden
  ausserhalb der Vorlagen gespeichert.

## Arbeitspakete

1. Gemeinsame Begriffe fuer `InputSource`, `ImportDiagnostic`,
   Quellenmetadaten und Validierungsergebnis festlegen.
2. Formatmatrix fuer YAML, CSV/XLSX, TRY, IFC und programmspezifische Vorlagen
   fuehren.
3. Regeln fuer Pflichtfelder, manuelle Ergaenzung, Ueberschreibung und
   Freigabe dokumentieren.
4. Ablage fuer Originaldateien, normalisierte Daten und Projektsnapshots
   definieren.
5. Auswirkungen auf `ma_database`, UI und Archivierung bewerten.
6. Moduluebergreifende Regeln fuer Vorlagenschutz, neue Dateinamen,
   bestaetigtes Ueberschreiben eigener Dateien und spaetere Formaterweiterung
   definieren.

## Akzeptanzkriterien

- Kein Fachmodell ist von IFC, TRY, Excel oder einem Simulationsprogramm
  abhaengig.
- Fehlende Pflichtdaten blockieren die Freigabe sichtbar.
- Importfehler, Warnungen und manuelle Aenderungen sind nachvollziehbar.
- P011 bis P018 koennen dieselben Quellen- und Validierungsbegriffe verwenden.
- Ein kollidierender neuer Dateiname wird nicht automatisch ersetzt oder
  ueberschrieben; der Nutzer muss einen anderen Namen auswaehlen.

## Nicht enthalten

- produktiver IFC-Parser
- CAD-Integration
- Datenbankmigration
- automatische IDA-Dateibearbeitung

## Umsetzungsbezug P028

P028 setzt einen ersten wiederverwendbaren Teil um: formatneutrale
Konfigurationsquellen, YAML-Schreibadapter, sichere lokale Zielordner,
unveraenderliche Vorlagen, bestaetigtes Ueberschreiben eigener Dateien und
Fehler bei kollidierenden neuen Dateinamen. Allgemeine `InputSource`-,
`ImportDiagnostic`- und Freigabevertraege bleiben Aufgabe von P010.

## Offene Entscheidungen

- konkrete Pflichtformate je Eingabemodul
- Umfang eines spaeteren IFC-Lite-Adapters
- Zeitpunkt und Technik einer zentralen Datenbank

## Umsetzungsergebnis

- Formatneutrale Modelle fuer Eingabequellen, Dateimetadaten, Aenderungen,
  Diagnosen, Validierung und Freigabe sind umgesetzt.
- Fehler blockieren immer; Warnungen benoetigen eine ausdrueckliche
  Entscheidung; fehlerfreie Staende werden automatisch freigegeben.
- Eindeutige Quellen-, Sitzungs-, Lauf-, Ereignis-, Diagnose- und
  Entscheidungs-IDs sind vorhanden.
- Strukturierte Ereignisse werden append-only unter
  `logs/sessions/<session_id>.jsonl` protokolliert.
- TRY-Import und Wettervalidierung bilden den ersten kompatiblen Pilotadapter.
- Die Streamlit-Wetteransicht zeigt Quelle, Diagnosen und Freigabestatus und
  protokolliert beide Warnungsentscheidungen.
- Die Reifegradmatrix liegt unter
  `docs/project/architecture/INPUT_DATA_FORMAT_MATRIX.md`.
- `ma_database` wurde bewusst nicht erweitert.
