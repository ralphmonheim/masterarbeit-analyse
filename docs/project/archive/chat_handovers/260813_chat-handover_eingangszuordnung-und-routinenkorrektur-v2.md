# Chat-Handover: Eingangsroutinen und direkte Planaufnahme

Datum: 2026-08-13
Status: Arbeitsstand dokumentiert; keine offenen Punkte nur in diesem Snapshot

## Abgeschlossener Stand

- Im Repository-Stammverzeichnis erfasst `input aufnehmen` die Eingänge
  `data/project_inbox/new/` und `docs/project/plans/inbox/`.
- Als Plan-Dokument gilt eine im allgemeinen Eingang eindeutig als Projektplan
  erkannte Datei. Die Zuordnung erfolgt aus Dateiname, Erweiterung und den
  erforderlichen Metadaten nach `PROJECT_INPUT_WORKFLOW.md`; bei Zweifel bleibt
  die Datei unverändert und wird als Rückfrage berichtet.
- Eindeutig erkannte Plan-Dokumente dürfen ohne weitere
  `Freigabe zur Umsetzung` aus `data/project_inbox/new/` nach
  `docs/project/plans/inbox/` verschoben werden. `plan aufnehmen` ordnet sie
  direkt in `PLAN_INDEX.md` und `PLAN_STATUS.md` ein. Diese Ausnahme gilt nur
  für die Ablage und Planungseinordnung, nicht für eine darin beschriebene
  technische Umsetzung.
- Für alle Nicht-Plan-Dateien erstellt `input aufnehmen` zunächst einen
  Bericht mit Kategorie, Zielvorschlag, Literaturbezug und offenen Punkten.
  Eine Datei ist nur dann eindeutig zuordenbar, wenn die Kategorien- und
  Zielordnerregel aus `PROJECT_INPUT_WORKFLOW.md` genau einen bestehenden
  Zielbereich ergibt. Verschieben oder inhaltliches Einarbeiten erfordert
  weiterhin `Freigabe zur Umsetzung`.
- Nach einer freigegebenen Literaturübernahme läuft
  `literature-research-workflow`: Quellenregister und Einzelanalyse werden
  ergänzt; die Projektübertragung wird getrennt in die zuständige kanonische
  Plan- oder Dokumentquelle eingetragen.
- Nach jeder Planaufnahme sowie jeder Erstellung, Verschiebung oder
  inhaltlichen Änderung eines Dokuments wird der lokale Navigator zwingend
  aktualisiert und danach validiert. Betroffen ist
  `WORK/04_Teil2_Prozessinnovation/Codex_Navigation/semantic_topics.md` mit
  seinen generierten Katalogen; die Ausführung erfolgt über
  `LOCAL_SKILL/masterarbeit-navigator/scripts/refresh_index.py` und danach
  `--validate-only`.
- `aktualisieren` führt die feste Reihenfolge aus: Projektstand prüfen,
  festgestellte Änderungen in den zuständigen Dokumentationsstrukturen
  ausführen, Navigator aktualisieren, Navigator validieren.
- Die Vertragsprüfung wurde am 2026-08-13 mit
  `.venv\Scripts\python.exe -m pytest tests/test_project_agent_system.py`
  ausgeführt: 8 Tests bestanden. `git diff --check` war fehlerfrei.

## Führende Referenzen und Anschluss

- `docs/project/UPDATE_ROUTINES.md` ist die Ablaufwahrheit für Reihenfolge,
  Freigabegrenzen und Navigatorpflege.
- `docs/project/PROJECT_INPUT_WORKFLOW.md` definiert Erkennung, Kategorien,
  Zielordner und die Behandlung unklarer Eingänge.
- `docs/project/plans/PLAN_INDEX.md` und `docs/project/plans/PLAN_STATUS.md`
  sind die führenden Ziele jeder Planaufnahme.
- `docs/common/commands_common.md` ist ausschließlich der Triggerindex.

Nächster Schritt für die fortsetzende Person: Bei neuem Eingang `input
aufnehmen` ausführen, den Bericht prüfen und ausschließlich für Nicht-Plan-
Dateien gegebenenfalls `Freigabe zur Umsetzung` einholen. Prioritäten und
weitere fachliche Arbeit werden ausschließlich aus den oben genannten
kanonischen Quellen abgeleitet; dieser Snapshot ersetzt keine Freigabe.
