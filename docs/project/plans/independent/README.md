# Unabhaengige Umsetzungsplaene

Dieser Ordner enthaelt kleine, eigenstaendige Umsetzungsplaene aus der Routine
`umsetzungsplan erstellen`.

## Rolle

- Ein read-only Sol-Agent auf hoher Stufe (`quality_auditor`) erstellt und
  qualitaetssichert den Plan aus einem abgeschlossenen Arbeits-Prompt. Der
  koordinierende Agent speichert das Ergebnis unveraendert.
- Der Plan wird hier mit Datum und frei gewaehltem inhaltlichem Dateinamen
  gespeichert (`YYMMDD_<freier-inhaltlicher-titel>.md`); er erhaelt keine
  `P`-Nummer. Bei einem Namenskonflikt wird der erste freie Suffix `-v2`,
  `-v3` usw. verwendet.
- Er wird weder automatisch in `PLAN_INDEX.md` oder `PLAN_STATUS.md`
  eingetragen noch bestehenden Plaenen zugeordnet.
- Ein neuer Tera-Chat setzt ihn erst nach `Freigabe zur Umsetzung` um.

Jeder Plan speichert den durch `Prompt abschliessen` erzeugten Arbeits-Prompt
und gliedert sich in Ziel, Scope und Nicht-Ziele, betroffene Bereiche,
Umsetzungsschritte, Pruefungen, Risiken und offene Entscheidungen sowie eine
`Tera-Uebergabe`. Der neue Chat erhaelt den konkreten Planpfad und setzt nur
diesen Plan um.

Nach der Umsetzung entscheidet der Nutzer ausdruecklich, ob Inhalte in einen
benannten bestehenden formellen Plan uebernommen, ueber `plan aufnehmen` als
neuer `P`-Plan angelegt oder als abgeschlossener unabhaengiger Plan belassen
werden.
