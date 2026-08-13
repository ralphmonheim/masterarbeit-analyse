# Chat-Handover – Quellenregister und gesteuerte Inhaltssuche

**Datum:** 2026-08-13
**Arbeitsbereich:** Literaturarbeit / P031 Project Operating System
**Status:** Prompt-, Ablage- und Suchroutinen umgesetzt; Quelleninventarisierung
und Inhaltsanalyse noch nicht begonnen.

## Ergebnis

- Die unveränderte Nutzereingabe ist als Referenz unter
  `docs/prompts/MASTER_PROMPT_LERNPAKETE_ORIGINAL_REFERENZ.md` dokumentiert.
  Sie verweist auf den Chat-Anhang `pasted-text.txt` und dessen SHA-256.
- Der ausführbare Arbeitsauftrag steht in
  `docs/prompts/MASTER_PROMPT_QUELLENINVENTAR_UND_LERNPAKETE.md`.
- Die Quellenarchitektur ist festgelegt: Originale bleiben am Fundort; jede
  inventarisierte Quelle erhält eine interne Markdown-Einzelanalyse; das
  interne Excel-Register verweist per Source-ID auf Original und Analyse; eine
  getrennte öffentliche Excel-Datei enthält nur zulässige, überprüfte Angaben.
- Der lokale, Git-ignorierte Arbeitsbereich ist
  `config/ma_database/literature/` mit `sources_internal.xlsx`,
  `sources_public.xlsx` und `analyses/`. Die Erläuterung steht in
  `docs/ma_database/README.md`.
- Der projektlokale Skill
  `.agents/skills/literature-research-workflow/SKILL.md` führt Quellen- und
  Inhaltssuchen: Register/Einzelanalyse → Navigator/Fundort →
  Rechte-/Zugriffsprüfung → gezielte Internetrecherche und Abgleich →
  Originalprüfung.
- `docs/project/UPDATE_ROUTINES.md` und `.agents/skills/README.md` führen
  diese Route. Der persönliche, nicht versionierte Skill
  `C:\Users\ralph\.codex\skills\masterarbeit-navigator\SKILL.md` wurde mit
  ausdrücklicher Nutzerfreigabe ergänzt. Diese globale Änderung wird weder
  durch einen Repository-Diff noch durch einen späteren Checkout gesichert.
- UD-127 dokumentiert die Entscheidung; `PLAN_STATUS.md` ordnet sie P031 zu.

## Begriffe und Prüfgates

- **Source-ID:** stabile Kennung einer Quelle im Register.
- **Einzelanalyse:** interne Markdown-Datei mit Quelleneinordnung und
  Arbeitsanalyse; sie ersetzt niemals das Original.
- **Navigator:** semantischer Wegweiser in der Arbeitsablage, kein
  Inhalts- oder Freigabenachweis.
- **Lernpaket:** spätere vertiefte, quellenbezogene Aufbereitung nach den
  Pilotläufen.
- **Rechte-/Zugriffsprüfung:** Originale dürfen erst geöffnet oder inhaltlich
  verarbeitet werden, wenn Source-ID, Fundort, Zugriffsstatus und zulässiger
  Verarbeitungsumfang je Quelle dokumentiert und erforderlichenfalls vom
  Nutzer freigegeben sind.
- **Öffentliche Fassung:** Ein Eintrag darf erst nach manueller
  Quellenprüfung, Status `citation_ready`, bestätigter öffentlicher
  Zugänglichkeit und bestätigter Zulässigkeit der vorgesehenen Darstellung in
  `sources_public.xlsx` übernommen werden. Die abschließende Freigabe für
  eine Veröffentlichung bleibt beim Nutzer.

## Prüfung

- `git diff --check` für die einschlägigen Projektdateien war fehlerfrei.
- Der semantische Navigationshub wurde über
  `refresh_index.py` aktualisiert und mit `refresh_index.py --validate-only`
  erfolgreich validiert.
- Der offizielle Skill-Validator `quick_validate.py` konnte nicht starten,
  weil in der vorhandenen Python-Umgebung das Modul `yaml` fehlt. Es wurde
  keine Abhängigkeit installiert. Die Skill-Frontmatter- und
  `agents/openai.yaml`-Struktur ist manuell geprüft und vorläufig plausibel.
  Nach einer gesonderten Freigabe für die benötigte Abhängigkeit ist die
  offizielle Validatorprüfung nachzuholen.
- Ein unabhängiger Blind-Review dieses Handover-Texts wurde vor der Ablage
  durchgeführt; die darin festgestellten Kontext-, Gate- und Restarbeitslücken
  sind in diese Fassung übernommen.

## Umfang und Grenzen

- Es wurden keine Originalquellen oder geschützten Literaturinhalte geöffnet,
  kopiert oder verarbeitet.
- Es wurden noch keine Excel-Register, Source-IDs oder Einzelanalysen erstellt.
- Der Worktree enthielt bereits zahlreiche fremde Änderungen. Dieser Chat
  änderte oder legte ausschließlich folgende Repository-Dateien an:
  `.gitignore`, `docs/ma_database/README.md`, die zwei genannten Prompt-Dateien,
  `.agents/skills/README.md`,
  `.agents/skills/literature-research-workflow/`,
  `docs/project/UPDATE_ROUTINES.md`,
  `docs/project/decisions/USER_DECISIONS_MASTERTHESIS_CODE.md`,
  `docs/project/plans/PLAN_STATUS.md` und diesen Handover mit seinem
  Indexeintrag. Zusätzlich wurde ausschließlich die oben genannte globale
  Navigator-Skill-Datei außerhalb des Repositorys geändert.

## Führende Referenzen

- `docs/project/decisions/USER_DECISIONS_MASTERTHESIS_CODE.md` – UD-127
- `docs/project/plans/PLAN_STATUS.md` – Abschnitt
  „Projektorganisation: Quellenregister und Inhaltssuche“
- `docs/project/UPDATE_ROUTINES.md` – Abschnitt „Quellen- und Inhaltssuche“
- `.agents/skills/literature-research-workflow/SKILL.md`
- `docs/prompts/MASTER_PROMPT_QUELLENINVENTAR_UND_LERNPAKETE.md`
- `docs/ma_database/README.md`

## Nächster Schritt

Vor der Vollinventarisierung drei konkrete Pilotquellen auswählen und ihre
Bearbeitung freigeben: **ein Buch oder Buchkapitel**, **ein Whitepaper oder
Forschungsbericht** und **eine öffentlich zugängliche Webquelle**. Je Pilot
sind Registerfelder, Source-ID, Einzelanalyse, Rechtekennzeichnung,
intern/öffentlich-Trennung und Abnahmekriterien zu prüfen. Erst nach der
Nutzerbestätigung des Schemas wird der Gesamtbestand inventarisiert.
