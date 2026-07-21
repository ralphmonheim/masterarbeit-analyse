# Entwicklungs-Inbox

Dieser Ordner ist ein temporaerer Sammelplatz fuer neue Projektdateien in der
Entwicklungsphase. Er ersetzt keine Fachordner. Inhalte unter `new/`,
`processed/` und `needs_review/` bleiben lokal und werden nicht versioniert.

Die zentrale Regelung steht in
`docs/project/PROJECT_INPUT_WORKFLOW.md`. Diese README dient nur als kurzer
lokaler Einstieg fuer den Arbeitsordner.

## Nutzung

1. Alle neuen Dateien direkt unter `new/` ablegen.
2. Codex mit `projektinput aufnehmen` den Ordner scannen lassen.
3. Eindeutige Dateien werden in bestehende Zielordner verteilt.
4. Verarbeitete Originale kommen nach `processed/`.
5. Unklare Dateien bleiben in `needs_review/` und werden erst nach Rueckfrage
   verschoben.

## Eingang

`new/` ist der einzige, unvorsortierte Eingang. Die fachliche Zuordnung
erfolgt erst beim Scan anhand von Dateiname, Erweiterung und zulaessigen
Metadaten nach `docs/project/PROJECT_INPUT_WORKFLOW.md`.

## Grenzen

- Wetterdatensaetze werden nur in den lokalen Wetter-Eingang vorbereitet. Die
  Registrierung und Freigabe bleibt beim bestehenden Wetter-Scan und
  Pruefworkflow.
- Plaene werden nicht automatisch umgesetzt. Sie landen zuerst in der
  Plan-Inbox und werden danach wie bisher geprueft.
- Produktive Projektdateien werden nur bei eindeutiger Zuordnung oder nach
  Rueckfrage geaendert.
