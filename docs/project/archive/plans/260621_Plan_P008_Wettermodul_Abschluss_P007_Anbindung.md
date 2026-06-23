ARCHIVIERT

Archivierungsdatum
2026-06-23

Archivierungsgrund
Dieser bisherige P008-Ausgangsplan wurde mit dem zweiten Ausgangsplan fuer
ma_weather zusammengefuehrt.

Nachfolgeplan
P008 - docs/project/plans/inbox/260623_Plan_P008_ma_weather_Gesamtplan.md

Hinweis
Die Inhalte dieses Dokuments wurden geprueft und in den aktualisierten
Gesamtplan fuer ma_weather integriert. Dieses Dokument dient nur noch der
Nachvollziehbarkeit der Planentwicklung und darf nicht mehr als aktuelle
Umsetzungsgrundlage verwendet werden.

# P008 Wettermodul Abschluss und P007-Anbindung

Stand: 2026-06-22
Status: Aktiv  
Bezug: P007, P010, P021, archivierter P002

## Ziel

Das bestehende Modul `ma_weather` fachlich abschliessen und kontrolliert an
die P007-Zielarchitektur anbinden. Der archivierte P002 bleibt als
Entstehungs- und Umsetzungsnachweis unveraendert erhalten.

## Bestehender Stand

- TRY-Katalog, Import, Validierung und Zeitindex sind vorhanden.
- Wetterkennwerte, sechs Diagramme, Markdown-Bericht und Runner sind vorhanden.
- `TRY_FFM_2015` wurde mit 8760 Stunden erfolgreich real geprueft.
- Echte TRY-Dateien bleiben lokal und werden nicht im Repository versioniert.
- Streamlit kann Wetteranalysen starten und erzeugte Diagramme anzeigen.
- P010 bindet TRY-Import und Wettervalidierung an gemeinsame Quellen-,
  Diagnose- und Freigabevertraege an.
- Wetterlaeufe und Warnungsentscheidungen werden unter
  `logs/sessions/<session_id>.jsonl` nachvollziehbar protokolliert.

## Offene Arbeiten

1. `TRY_FFM_2045`, `TRY_MUC_2015`, `TRY_MUC_2045`, `TRY_HAM_2015` und
   `TRY_HAM_2045` jeweils real ausfuehren und Validierung, Stundenanzahl,
   Diagramme, CSV und Bericht pruefen.
2. Diagrammgestaltung fachlich gegen das Masterarbeitslayout bewerten.
3. `weather_key` als neutrale Ausgabe von `ma_weather` und spaetere Eingabe von
   `ma_parameters` dokumentieren.
4. TRY-Auswahl und Import eigener Wetterdateien als getrennte Quellen
   behandeln und beide auf dasselbe Wettermodell normalisieren.
5. Importierte Wetterdaten unabhaengig von ihrer Quelle validieren.
6. Kritische Ereignisse fuer Hitze, Kaelte, Strahlung und Beleuchtung als
   spaetere Eingabe fuer P021 vorbereiten.
7. Niederschlag nur aufnehmen, wenn ein unterstuetztes Format eine belastbare
   Datenspalte liefert.
8. Sicherstellen, dass `ma_variants` Wetterdaten langfristig nur ueber
   `ma_parameters` erhaelt.
9. Wetterbezogene Modul- und Dashboard-Dokumentation aktualisieren.

Die P010-Grundlage fuer Quelle, Diagnose und Freigabe ist abgeschlossen.
P008 konzentriert sich damit auf reale Datensaetze, eigenen Dateiimport,
Diagrammqualitaet, `weather_key` und kritische Wetterereignisse.

## Abgrenzung

- Keine synthetischen TRY-Dateien anlegen.
- Keine direkte Kopplung von `ma_weather` an `ma_variants`.
- Keine Wetterdiagramme in `ma_analyse` verschieben.
- Keine automatische IDA-ICE-Steuerung.
- Keine stillschweigende Gleichsetzung eigener Wetterdateien mit geprueften
  TRY-Datensaetzen.

## Tests und Abschlusskriterien

- Alle sechs aktiven Jahresdatensaetze sind real dokumentiert geprueft.
- Pflichtspalten, eindeutiger Zeitindex und 8760 Stunden sind je Jahresdatei
  nachvollziehbar.
- Fehlende optionale Spalten fuehren zu Warnungen statt zu unklaren Abbruechen.
- TRY-Auswahl und eigener Dateiimport liefern dasselbe validierte
  Wetterdatenmodell.
- `weather_key` und die geplante P007-Datenflussgrenze sind dokumentiert.
- Kritische Wetterereignisse koennen reproduzierbar als Zeitfenster
  beschrieben werden.
- P008 kann danach archiviert werden.

## Historischer Bezug

Der vollstaendige urspruengliche Wetterplan liegt unveraendert unter
`docs/project/archive/plans/250603_Plan_Wetterdatenanalyse_TRY_Integration.md`.
