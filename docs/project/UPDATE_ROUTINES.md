# Update-Routinen

Diese Datei ist die einzige Ablaufwahrheit fuer dokumentierte Codex-Routinen.
`docs/common/commands_common.md` ist ausschliesslich der Triggerindex.

## Verbindliches Freigabe-Gate

- Read-only Analyse, Planung und Statuspruefungen sind ohne
  Umsetzungsfreigabe zulaessig.
- Jede Aenderung an Code, Konfiguration, Daten oder Dokumentation beginnt erst
  nach der ausdruecklichen Nutzerformulierung `Freigabe zur Umsetzung`.
- Eine Council-Empfehlung oder Council-Mehrheit ersetzt diese menschliche
  Freigabe nicht.
- Nach einer solchen Freigabe sind lokale Tests und Aenderungen innerhalb des
  exakt abgestimmten Umfangs ohne weitere Rueckfrage zulaessig.
- Die Direktbefehle `direkt update repo`, `tagesende direkt` und ihre
  Sammelbefehle committen, taggen und pushen einen bereits freigegebenen und
  vorbereiteten Arbeitsstand ohne zweite Freigabe.
- Ein Direktbefehl erteilt keine Freigabe fuer neue Produkt-, Config- oder
  Dokumentationsaenderungen. Technische Sicherheitsabfragen und besondere
  Rechtegates bleiben unberuehrt.

## Council-Routinen

- `council analyse`: read-only Bestandsaufnahme.
- `council review`: read-only Qualitaetsreview.
- `council umsetzen`: bereits freigegebenen Umfang umsetzen.
- `ohne council` oder `nur Tera`: optionale Council-Arbeit auslassen.
- `mit Sol-Review`: read-only Abschlussreview vormerken.

Bei materiellem Erkenntnisgewinn wird das Council themenbezogen erweitert:
Professor Sophia prueft Methodik und Reproduzierbarkeit, Justus prueft
Rechte-, Daten-, Lizenz- und Veroeffentlichungsgrenzen. Die fuenf
Review-Rollen (Tera, Mira, Vera, Professor Sophia, Justus) geben getrennte
Erstvoten ab; Ada setzt nur nach Nutzerfreigabe um und zaehlt nicht als
Review-Stimme. Eine risikoreichere Variante darf empfohlen werden, wenn ihre
ueberlegene Passung zum fuehrenden Gesamtplan belegt und ihr Restrisiko,
Rueckfallweg, Pruefstrategie sowie alle Sondergates sichtbar sind.

## Themenstart

- `neues thema`, `neues thema: ...` oder `themenwechsel`: vorheriges Thema
  pausieren und den neuen Auftrag mit dem projektlokalen Skill `prompt-intake`
  schrittweise praezisieren. Der Skill fragt alle noch nicht klaren
  relevanten Angaben nach.
- `Prompt abschliessen`: den vollstaendigen Arbeits-Prompt ausgeben. Danach
  gelten die normalen Regeln fuer Analyse, Planung und `Freigabe zur Umsetzung`.

## Quellen- und Inhaltssuche

- Literatur-, Quellen-, Normen-, Studien-, Inhalts- und Webquellensuchen
  nutzen zuerst den Skill `literature-research-workflow` und damit den
  semantischen Navigationshub.
- Die Reihenfolge lautet: vorhandenes Quellenregister und Einzelanalyse,
  gezielte lokale Fundortsuche, Rechte-/Zugriffsprüfung, danach Internetrahmen
  und Abgleich. Breite lokale Scans bleiben ohne ausdrückliche Nachfrage
  ausgeschlossen.
- Die interne Quellenmatrix ist ein Register. Fachliche Aussagen, aktuelle
  Stände und Zitationsfundstellen werden immer gegen die jeweilige
  Originalquelle geprüft. Erst manuell nachgelesene Fundstellen erhalten
  `citation_ready`.
- Öffentliche Quellenregister enthalten nur zulässige und überprüfte Angaben;
  Originale, Volltexte, interne Pfade und ungeprüfte KI-Analysen bleiben
  intern.

## Sammelbefehle

- `input aufnehmen`: beide Eingaenge `data/project_inbox/new/` und
  `docs/project/plans/inbox/` erfassen. Eindeutig erkannte Plan-Dokumente
  werden sofort in die Plan-Inbox verschoben und mit `plan aufnehmen`
  eingeordnet; diese Ausnahme benoetigt keine weitere Freigabe. Danach einen
  Zuordnungsbericht erstellen. Nicht-Plan-Dateien erst nach Freigabe
  uebernehmen; Literatur anschliessend ueber den Literatur-Workflow
  analysieren. Nach Planaufnahme oder Dokumentaenderung den Navigator
  aktualisieren und validieren.
- `aktualisieren und tagesende direkt`: zuerst `aktualisieren`, dann
  `tagesende direkt` ausfuehren.
- `aktualisieren und direkt update repo`: zuerst `aktualisieren`, dann
  `direkt update repo` ausfuehren.
- `aktualisieren`: Git-Stand, Planung, Entscheidungen, Command-Dokumentation,
  Modulumsetzungsstand, zentrale Statusanzeigen, Changelog und Versionen
  pruefen, festgestellte Aktualisierungen in den zustaendigen
  Dokumentationsstrukturen ausfuehren und danach den lokalen semantischen
  Navigationshub gemaess der unten definierten Navigator-Routine aktualisieren
  und validieren.
- `tagesstart` oder `Guten Morgen, es ist ein neuer Tag.`: Projektstand und
  offene Entscheidungen ueber den lokalen Navigationshub auffinden und aus
  den dort genannten kanonischen Quellen frisch lesen; keine Oberflaeche
  automatisch starten.
- `tagesende` oder `Gute Nacht.`: Tagesstand dokumentieren und den Git-Stand
  vorbereiten.
- `tagesende direkt` oder `Gute Nacht direkt.`: Tagesstand dokumentieren und
  bei eindeutigem Stand Commit, Tag und Push ausfuehren.
- `wochenabschluss` oder `Eine schoene Woche.`: Wochenbericht erstellen und
  archivierungsfaehige Plaene benennen.

## Einzelbefehle

- `update repo`: Version, Changelog und Release-Stand vorbereiten sowie den
  vorgesehenen Repository-Stand auf Rechte, Schutzbedarf und
  Veroeffentlichungsgrenzen pruefen.
- `direkt update repo`: Version, Changelog, Commit, Tag und Push ausfuehren,
  sofern der Arbeitsstand eindeutig ist.
- `update planung`: Planindex, Planstatus, Entscheidungen und Plan-Inbox
  abgleichen.
- `projektlage`: Den lokalen Navigationshub als Einstieg verwenden und
  Git-Stand, Version, Plaene und offene Entscheidungen aus ihren kanonischen
  Quellen lesen.
- `chat-stats`: den sichtbaren Arbeitsstand read-only bewerten.
- `chat-handover`: offene Inhalte vor der Archivierung in ihre fuehrende
  Projektquelle uebertragen und erst danach eine Uebergabe als historischen
  Snapshot archivieren. Die Zuordnung ist verpflichtend: konkrete Restarbeit
  in den zustaendigen aktiven Plan und bei Bedarf kompakt in `PLAN_STATUS.md`,
  echte offene Entscheidungen in `USER_DECISIONS_OPEN_POINTS.md` und noch
  nicht zu entscheidende Ideen als klar markierte, nicht freigegebene
  Folgeoption im zustaendigen aktiven Plan. Der Snapshot enthaelt danach nur
  erledigten Stand, Nachweise und Verweise auf die uebertragenen offenen
  Punkte; er fuehrt keine eigene offene Aufgabenliste. Besteht der gewuenschte
  Dateiname bereits, wird kein Snapshot ueberschrieben: Fuer einen neuen oder
  abweichenden Stand wird der erste freie fortlaufende Suffix `-v2`, `-v3`
  usw. verwendet und als eigener Eintrag im Handover-Index erfasst.
  Inhaltlich identische Snapshots werden nicht erneut angelegt. Eine spaetere
  Bereinigung ist nur nach gezielter Nutzerfreigabe zulaessig. Vor der
  Archivierung prueft ein separater Blind-Review-Agent den Entwurf zunaechst
  ausschliesslich anhand des Handover-Texts und ohne Recherche im Repository.
  Er benennt unverstaendliche Begriffe, fehlenden Kontext, mehrdeutige
  Verweise sowie unklare offene Punkte und naechste Schritte. Bleiben Punkte
  offen, darf der Agent gezielt den bisherigen Chatverlauf nachschlagen. Sind
  sie danach weiterhin unklar oder widerspruechlich, stellt er dem Nutzer
  konkrete Rueckfragen im Chat. Erst nach dieser Klaerung wird der Snapshot
  final archiviert.
- `plan aufnehmen`: neue Plan-Metadaten einordnen.
- `projektinput aufnehmen`: neue Projektinput-Metadaten erfassen und bei
  eindeutiger Zuordnung in bestehende Strukturen einordnen.
- `entscheidung festhalten`: echte Nutzerentscheidungen dokumentieren.
- `release check`: Version, Changelog, Tags, Tests und offene Aenderungen
  pruefen.

## Lokaler semantischer Navigationshub

- Einziger Navigationseinstieg ist
  `WORK/04_Teil2_Prozessinnovation/Codex_Navigation/semantic_topics.md`.
  `WORK` bezeichnet die lokale Masterarbeits-Arbeitsablage. Der Hub ist ein
  nicht-kanonischer Wegweiser; er ersetzt weder Plaene, Entscheidungen,
  Rechtevermerke noch Quelldokumente.
- Die generierten Dateien `repository_catalog.md`, `workspace_catalog.md` und
  `local_repository_catalog.md` sind Hintergrundindizes. Sie werden nur bei
  Bedarf gezielt durchsucht und bilden keine parallele Dokumentationswahrheit.
- `tagesstart`, `projektlage` und fachliche Analysen beginnen mit einer
  gezielten Suche im Hub. Status, Freigaben und fachliche Aussagen werden
  danach immer aus der dort verlinkten fuehrenden Originalquelle gelesen.
- `aktualisieren` aktualisiert den Hub mit dem skill-relativen Skript
  `LOCAL_SKILL/masterarbeit-navigator/scripts/refresh_index.py` und validiert
  ihn anschliessend mit `--validate-only`. Die weiteren genannten Routinen
  pruefen den Hub schreibfrei mit `--validate-only`; `input aufnehmen`
  aktualisiert und validiert ihn nach freigegebenen Dokumentaenderungen.
  `LOCAL_SKILL` bezeichnet den persoenlichen Skill-Ordner und ist kein Pfad
  innerhalb des Repositorys.
- Nach jeder Erstellung, Verschiebung oder inhaltlichen Aenderung eines
  Dokuments wird der Hub mit dem tatsaechlichen Ablageort und der kanonischen
  Referenz aktualisiert und anschliessend validiert. `aktualisieren` fuehrt
  diese Aktualisierung stets aus.
- Ein fehlender oder veralteter Hub wird sichtbar gemeldet. Er blockiert
  Produkt- oder Releasearbeiten nur dann, wenn seine Pflege zum freigegebenen
  Umfang gehoert; die kanonischen Projektquellen bleiben weiterhin direkt
  nutzbar.
- Der Generator erfasst versionierte Projektdokumente sowie Metadaten der
  Arbeitsablage und einer positiven Allowlist lokaler, Git-ignorierter
  Projektpfade. Der Validator gleicht alle fuenf Hub-Dateien bidirektional
  gegen den aktuellen Metadatenstand ab und arbeitet im Modus
  `--validate-only` schreibfrei. Lauf-, Ergebnis-, Cache- und
  Datenbankbereiche sowie Reparse-Punkte bleiben ausgeschlossen. Geschuetzte
  Inhalte werden nicht extrahiert. Hooks, Watcher, Embeddings, RAG, Graphen,
  Cloud-Dienste oder Veroeffentlichungen werden dadurch nicht aktiviert.

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
- Commit, Tag und Push benoetigen innerhalb dieser Direktbefehle keine
  zusaetzliche Bestaetigung.
