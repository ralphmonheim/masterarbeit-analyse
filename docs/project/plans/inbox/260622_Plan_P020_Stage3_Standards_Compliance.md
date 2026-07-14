# P020 Analyse Stufe 3 Standards Compliance

Stand: 2026-07-14
Status: Research-Plan, Compliance-Vorpruefung integriert
Prioritaet: Hoch
Abhaengigkeiten: P019, P027, ma_core.compliance, bestaetigte Norm-Nutzungsrechte

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
7. Vor jeder maschinellen Normverarbeitung eine `ComplianceDecision` aus
   `ma_core.compliance` verlangen und Quellen-, Lizenz- und Hochschulnachweis
   referenzieren.
8. Regelwerk, Rechteinhaber und Bezugsweg getrennt nachweisen. Fuer DIN,
   VDE-Webshop, VDE-NormenBibliothek, VDI ueber DIN Media/Nautos und VDI-VOB
   gelten unterschiedliche Vertragsgrundlagen.

## Lokaler Pruefbestand Runde 1

Unter `data/common/normen/rounds/round1_v0_1/` liegt die erste lokale
Normenauswertung als Entwicklungs- und Reviewbestand. Sie enthaelt ein
Normenregister, nummerierte und unnummerierte Formelkandidaten,
Symbolabschnitte, Beziehungen, Projektmapping und Review-Hinweise.

Die Runde ist noch keine freigegebene Normlogik. Alle Formeln und Regeln
bleiben `review_required`, bis Quelle, Ausgabe, Abschnitt, PDF-Seite,
Gleichungsnummer, Variablen, Einheiten, Randbedingungen und Tests fachlich
geprueft sind. Ohne bestaetigte KI-/Maschinenverarbeitungsrechte sind OCR,
automatische Extraktion, Embeddings, RAG und produktive Implementierung aus
diesen Extrakten gesperrt. Alte Mapping-Bezeichnungen wie
`stage_3_verification` werden
bei der spaeteren Aufarbeitung auf den kanonischen Namen
`ma_analyse.stage_3_standards_compliance` abgebildet.

Der Frankfurt-UAS-Nautos-Zugang ist fuer autorisierte manuelle Recherche und
Lektuere belegt. Er bestaetigt keine KI- oder Maschinenverarbeitungsrechte.
Die oeffentlichen VDE-VERLAG- und NormenBibliothek-Bedingungen stoppen
derzeit TDM und KI-Verarbeitung. Fuer VDI ist kein vergleichbares
Standard-KI-Angebot identifiziert; konkrete VDI-basierte Softwarelogik bleibt
bis zur Lizenzpruefung `review_required`.

Kalender- und Feiertagsdaten fuer 2025 liegen als gemeinsame Regelgrundlage
unter `data/common/kalender/2025/`. Sie duerfen spaeter Nutzungszeiten,
Bewertungszeitraeume oder Randbedingungen unterstuetzen, ersetzen aber keine
fachliche Kalenderlogik.

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
- Jede produktive Regel besitzt eine gruen freigegebene Quellen- und
  Rechteprovenienz; `yellow`, `red` und `unknown` werden nicht ausgefuehrt.
- Eine Hochschulzugangsberechtigung wird nicht mit Maschinen-,
  Vervielfaeltigungs-, Software- oder Veroeffentlichungsrechten gleichgesetzt.
