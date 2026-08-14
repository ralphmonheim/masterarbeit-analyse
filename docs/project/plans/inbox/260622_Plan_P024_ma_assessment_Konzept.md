# P024 ma_assessment Konzept

Stand: 2026-06-22
Status: Konzeptplan
Prioritaet: Niedrig
Abhaengigkeiten: P019, P022, P023

## Ziel

Technische, wirtschaftliche und oekologische Ergebnisse ohne eigene
Fachberechnung zu einer Entscheidungsvorlage zusammenfuehren.

## Arbeitspakete

- Kriterien, Normalisierung, Gewichtung und Ausschlusskriterien planen.
- Gewichtung vor Sichtung der Ergebnisse versionieren.
- Scoring und Pareto-Darstellung als getrennte Methoden behandeln.
- Fehlende oder nicht vergleichbare Ergebnisse sichtbar kennzeichnen.

## Akzeptanzkriterien

- Keine Primaerberechnung liegt in `ma_assessment`.
- Jede Bewertung ist auf Kriterien- und Gewichtungsstand zurueckfuehrbar.

## Eingangsauswertung 2026-08-14: Bewertungsarchitektur

Der KPI-Diskussionsprozess stuetzt die bestehende Zieltrennung: technische
Analyse liefert nachvollziehbare Eingaben; `ma_economy` und
`ma_sustainability` behalten ihre Fachberechnungen; `ma_assessment` fasst
Ergebnisse erst danach als Entscheidungsvorlage zusammen. Pareto, Scoring und
Gewichtung bleiben getrennte, optionale Verfahren. Das Eingangsdokument ist
kein Architekturentscheid: Modulnamen, feste Gewichte, ein Gesamtscore sowie
endgueltige Kriterien bleiben offen und werden nicht in den bestehenden Plan
hineininterpretiert.
