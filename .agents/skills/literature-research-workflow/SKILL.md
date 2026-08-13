---
name: literature-research-workflow
description: "Finde, inventarisiere und analysiere Literatur- oder Internetquellen fuer die Masterarbeit. Verwende diesen Skill bei `input aufnehmen`, Quellen-, Literatur-, Inhalte-, Studien-, Normen-, Webquellen- oder Lernpaket-Recherchen sowie bei Fragen nach einer Quelle, ihrer Analyse oder ihrem Fundort."
---

# Literaturrecherche

Nutze zuerst den globalen Skill `masterarbeit-navigator` und seinen
semantischen Hub. Die Quellenmatrix ist ein Register, keine fachliche
Wahrheit; prüfe Aussagen immer am Original.

Die Freigabe- und Aktualisierungsregeln stehen in
`docs/project/UPDATE_ROUTINES.md`.

## Suchreihenfolge

1. Prüfe die interne Quellenmatrix und die verlinkte Markdown-Analyse zur
   Source-ID, sofern sie vorhanden sind.
2. Nutze den Navigator, um lokale Fundorte, den Ablagestatus und die
   zuständige Originalquelle gezielt zu finden.
3. Lies die Originalquelle nur innerhalb ihres dokumentierten Zugriffs- und
   Rechteumfangs. Geschützte oder nicht freigegebene Inhalte bleiben bei
   Metadaten und `requires_manual_review`.
4. Recherchiere im Internet erst für Themenrahmen, Aktualität, Lücken und
   ergänzende Fundstellen. Nutze für inhaltliche Aussagen überprüfbare,
   vorzugsweise primäre Quellen.
5. Gleiche lokale und externe Treffer über Source-ID, DOI, Titel, Autor, Jahr
   und Version ab. Markiere Dubletten, ältere Fassungen und widersprüchliche
   Angaben sichtbar.

## Ergebnisse

- Ergänze nach Freigabe das interne Excel-Register und erstelle oder
  aktualisiere die Markdown-Analyse je Quelle.
- Trenne immer Quelleninhalt, KI-Analyse und Projektübertragung.
- Setze `citation_ready` nur nach manuellem Nachlesen der konkreten
  Originalfundstelle; sonst verwende einen passenden Prüfstatus.
- Übernimm in die öffentliche Quellenmatrix nur überprüfte und zulässige
  Metadaten sowie kurze zulässige Beschreibungen. Keine internen Pfade,
  Volltexte oder ungeprüften KI-Aussagen.

## Grenzen

Originale weder ändern noch weiterveröffentlichen. Keine DOI, Seitenzahl oder
Quellenaussage erraten. Die Arbeitsstruktur und Felder stehen in
`docs/prompts/MASTER_PROMPT_QUELLENINVENTAR_UND_LERNPAKETE.md`.
