# Update-Routinen

Diese Datei ist die einzige Ablaufwahrheit fuer dokumentierte Codex-Routinen.
`docs/common/commands_common.md` ist ausschliesslich der Triggerindex.

## Council-Routinen

- `council analyse`: read-only Bestandsaufnahme.
- `council review`: read-only Qualitaetsreview.
- `council umsetzen`: bereits freigegebenen Umfang umsetzen.
- `ohne council` oder `nur Tera`: optionale Council-Arbeit auslassen.
- `mit Sol-Review`: read-only Abschlussreview vormerken.

## Sammelbefehle

- `aktualisieren und tagesende direkt`: zuerst `aktualisieren`, dann
  `tagesende direkt` ausfuehren.
- `aktualisieren und direkt update repo`: zuerst `aktualisieren`, dann
  `direkt update repo` ausfuehren.
- `aktualisieren`: Git-Stand, Planung, Entscheidungen, Command-Dokumentation,
  Modulumsetzungsstand, zentrale Statusanzeigen, Changelog und Versionen
  pruefen. Neue Plaene und Projektinputs nur anhand ihrer Metadaten erfassen.
- `tagesstart` oder `Guten Morgen, es ist ein neuer Tag.`: Projektstand und
  offene Entscheidungen lesen; keine Oberflaeche automatisch starten.
- `tagesende` oder `Gute Nacht.`: Tagesstand dokumentieren und den Git-Stand
  vorbereiten.
- `tagesende direkt` oder `Gute Nacht direkt.`: Tagesstand dokumentieren und
  bei eindeutigem Stand Commit, Tag und Push ausfuehren.
- `wochenabschluss` oder `Eine schoene Woche.`: Wochenbericht erstellen und
  archivierungsfaehige Plaene benennen.

## Einzelbefehle

- `update repo`: Version, Changelog und Release-Stand vorbereiten.
- `direkt update repo`: Version, Changelog, Commit, Tag und Push ausfuehren,
  sofern der Arbeitsstand eindeutig ist.
- `update planung`: Planindex, Planstatus, Entscheidungen und Plan-Inbox
  abgleichen.
- `projektlage`: Git-Stand, Version, Plaene und offene Entscheidungen lesen.
- `chat-stats`: den sichtbaren Arbeitsstand read-only bewerten.
- `chat-handover`: eine Uebergabe erstellen und als historischen Snapshot
  archivieren.
- `plan aufnehmen`: neue Plan-Metadaten einordnen.
- `projektinput aufnehmen`: neue Projektinput-Metadaten erfassen und bei
  eindeutiger Zuordnung in bestehende Strukturen einordnen.
- `entscheidung festhalten`: echte Nutzerentscheidungen dokumentieren.
- `release check`: Version, Changelog, Tags, Tests und offene Aenderungen
  pruefen.

## Test- und Referenzbefehl

- `aktualisiere tests`: benoetigte Referenzoutputs und Tests aktualisieren;
  keine Git-Aktionen ausfuehren.

## Grundregeln

- Root-`CHANGELOG.md` bleibt die einzige aktive Aenderungshistorie.
- Tags folgen `vX.Y.Z`; Patch-Versionen gelten fuer Dokumentation und kleine
  Korrekturen, Minor-Versionen fuer neue Fachbereiche oder Bedienbereiche.
- Plaene werden nicht automatisch geloescht.
- Git-Push wird nur bei `direkt update repo` oder `tagesende direkt` durch
  Codex ausgefuehrt.
