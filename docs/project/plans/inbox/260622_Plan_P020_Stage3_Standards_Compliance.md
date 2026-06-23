# P020 Analyse Stufe 3 Standards Compliance

Stand: 2026-06-22
Status: Research-Plan
Prioritaet: Hoch
Abhaengigkeiten: P019

## Ziel

Varianten anhand deutscher Normen und normierter Berechnungsverfahren
nachweisen. Internationale Normen sollen spaeter als weitere Profile
ergaenzbar sein.

## Kanonischer Name

`ma_analyse.stage_3_standards_compliance`

Der fruehere Name `stage_3_verification` bleibt nur als Uebergangshinweis.

## Arbeitspakete

1. Quellen- und Methodenmatrix erstellen: Norm, Ausgabe, Abschnitt,
   Anwendungsbereich, benoetigte Eingaben, Verfahren und Ergebniskennwert.
2. Deutsche Normenprofile fuer relevante Themen priorisieren.
3. Maschinenlesbares `StandardsProfile` und einzelne Nachweisregeln planen.
4. Bestehende Kennwerte nur nach fachlicher Quellenpruefung zuordnen.
5. `ComplianceReport` mit `pass`, `fail`, `warning` und `not_evaluable`
   definieren.
6. Erweiterungsmechanismus fuer internationale Profile dokumentieren.

## Moegliche Nachweisbereiche

- thermischer Komfort und operative Temperatur
- CO2, PMV und PPD
- Uebertemperatur und Gradstunden
- Heiz-, Kuehl- und Lueftungsanforderungen

Die konkrete Auswahl wird erst durch die Methodenmatrix verbindlich.

## Akzeptanzkriterien

- Jede Regel nennt Norm, Ausgabe, Abschnitt, Einheit und Rechenweg.
- Fehlende Daten bestehen niemals stillschweigend.
- Bestehende Komfortpolygone gelten nicht ohne Quellenbeleg als Normregel.
- Deutsche und internationale Profile verwenden dieselbe neutrale
  Nachweisschnittstelle.
