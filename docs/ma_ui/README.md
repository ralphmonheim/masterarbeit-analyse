# ma_ui

`ma_ui` ist die vorbereitete zentrale lokale Streamlit-Oberflaeche fuer das
Masterarbeitsprojekt.

## Rolle

- `ma_ui` zeigt Navigation, Workflow-Uebersicht und spaeter Modulansichten.
- `ma_ui` enthaelt keine fachliche Berechnungslogik.
- Fachlogik bleibt in `ma_analyse`, `ma_variants`, `ma_weather` und spaeteren
  Fachmodulen.
- Moduluebergreifende Aufrufe laufen ueber `ma_workflow`.

## Aktueller Stand

- Die App nutzt jetzt `module_views/` als Ziel-Einstieg fuer Modulansichten.
- `shared/` enthaelt erste allgemeine Anzeigehelfer fuer Tabellen, Status,
  Logs, Layout, Pfade und Plotdateien.
- `pages/` bleibt vorerst als Kompatibilitaets- und Zwischenstand erhalten.
- Startseite mit Workflow-Uebersicht ist vorbereitet.
- Analyse-Seite ruft die UI-neutrale `ma_analyse`-Service-Fassade ueber
  `ma_workflow` auf.
- Analyse-Seite bildet die wichtigsten fachlichen Optionen aus dem bisherigen
  `ma_analyse`-Ablauf ab: Prepare-Format, Comfort-Profil, Heating-/Cooling-
  Ansicht, Variantenmodus, Reihenlayout, `analyze-data`-Excel-Ausgabe und
  Plot-Template-Optionen.
- Analyseumfang wird abgebildet: Bei `Alle Varianten` uebergibt die UI
  `variants=None` an die Service-Fassade, damit die bestehende Analyse-Logik
  alle verfuegbaren Varianten nutzen kann.
- Varianten und Raeume werden aus `ma_analyse`-Services gelesen, falls lokale
  Daten vorhanden sind. Manuelle Texteingabe bleibt als Fallback bestehen.
- Plot-Template-Overlays koennen aus einem einfachen Katalog der ersten
  gewaehlten Variante und des ersten Raums ausgewaehlt werden. Freie
  Overlay-Linien im Format `source,column,label,axis` bleiben als Fallback
  moeglich.
- Analyse-Ergebnisse zeigen Status, Fehler, Hinweise, erzeugte Dateien und Log.
- Varianten-Seite zeigt Parameter, Optionen, Variantenraum, Auswahlmethoden und
  vorhandene Exportdateien ueber bestehende `ma_variants`-Services.
- Wetter-Seite zeigt lokale TRY-Datensaetze aus dem `ma_weather`-Katalog und ob
  die referenzierten Dateien lokal vorhanden sind.
- Bewertungsseite zeigt generische Systemkosten, Energiepreise und Szenarien aus
  den vorhandenen Beispielannahmen. Variantenbezogene Kostenberechnung wird dort
  noch nicht gestartet.
- Geplante Zielseiten fuer Parameter, Gebaeude, Simulation-Setup, IDA-Export,
  IDA-Import und Feedback sind als Platzhalter erreichbar und zeigen ihren
  aktuellen Workflow-Kontext aus `ma_workflow`.

## Start

Empfohlen:

```powershell
.\.venv\Scripts\python.exe -m streamlit run src\ma_ui\app.py
```

Alternativ:

```powershell
.\.venv\Scripts\streamlit.exe run src\ma_ui\app.py
```

Wenn Streamlit nach Codeaenderungen alte Importfehler zeigt, den laufenden
Streamlit-Prozess stoppen und mit dem empfohlenen venv-Befehl neu starten.
