# Planungsbereich

Dieser Bereich steuert die Umsetzung. Er ersetzt keine Fachlogik und ist keine Ausgabedokumentation.

## Nutzung

- Neue Plaene werden zuerst in `inbox/` abgelegt.
- Kleine, aus `umsetzungsplan erstellen` erzeugte und noch nicht formell
  einzuordnende Einzelplaene liegen getrennt unter `independent/`.
- `PLAN_INDEX.md` fuehrt alle bekannten Plaene.
- `PLAN_STATUS.md` ist die aktive Gesamtuebersicht. Sie fuehrt offene und
  teilweise umgesetzte Punkte sowie den fuer die Einordnung notwendigen
  Abschluss- und Archivkontext.
- `STRUCTURE_REVIEW.md` ist eine historische Strukturmomentaufnahme. Der
  aktuelle Agenten- und Project-OS-Audit steht im aktiven P031-Plan.
- `CLEANUP_PLAN.md` trennt sichere Massnahmen von Aenderungen mit Rueckfragebedarf.
- `IMPLEMENTATION_NOTES.md` enthaelt Regeln fuer spaetere Umsetzungen.
- Alte Planstaende kommen nach `docs/project/archive/plans/`.

Nicht alle Plaene werden gleichzeitig umgesetzt. Vor jeder Umsetzung wird der ausgewaehlte Plan gelesen, bewertet und erst danach umgesetzt.

`independent/` ist keine zweite Planserie: Diese Plaene erhalten keine
`P`-Nummer und werden nicht automatisch im Planindex oder Planstatus gefuehrt.
Erst nach der Umsetzung entscheidet der Nutzer, ob ihr Inhalt in einen
bestehenden Plan uebernommen, als neuer formeller Plan angelegt oder als
abgeschlossener Einzelplan belassen wird.
