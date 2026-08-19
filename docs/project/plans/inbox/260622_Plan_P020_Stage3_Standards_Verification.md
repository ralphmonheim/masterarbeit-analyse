# P020 Analyse Stufe 3 Norm-Nachweis

Stand: 2026-07-24
Status: Fachlicher Research-Plan
Prioritaet: Hoch
Abhaengigkeiten: P019, P027

## Ziel

Analyse Stufe 3 prueft Gebaeude und technische Systeme gegen fachlich
vorbereitete Normvorlagen. Der Nachweis bewertet Modellannahmen, Eingaben,
Einheiten, Randbedingungen und Ergebnisse; er ist keine Rechte- oder
Freigabepruefung.

## Kanonischer Name

`ma_analyse.stage_3_standards_verification`

Der fruehere Kurzname `stage_3_verification` bleibt als neutraler
Kompatibilitaetsalias. Rechtliche Pruefbegriffe sind kein Bestandteil dieses
Fachmoduls.

## Geplanter Umfang

1. Deutsche Normvorlagen und die jeweils verwendeten Ausgaben fachlich ordnen.
2. Nachweisprofile fuer Gebaeude, Zonen und Technik als nachvollziehbare
   Eingabe- und Ergebnisstruktur festlegen.
3. `NormVerificationReport` mit `pass`, `fail`, `warning` und
   `not_evaluable` modellieren.
4. Einheiten, Randbedingungen, Annahmen und Tests je Regel dokumentieren.
5. Den bereinigten Metadatenindex und das Zonenprofil-Geruest unter
   `data/common/normen/` nur als Planungsgrundlage verwenden.

## Grenzen

Der aktuelle Stand enthaelt keine produktiven Normregeln. Formeln,
Grenzwerte und Nachweisregeln werden erst mit ihrem fachlichen Testfall
implementiert.

## Umsetzungsstand 2026-08-11: wertfreie Nachweisbereitschaft

- `VerificationReadinessItem` beschreibt Kriterium, Regelwerk, Ausgabe,
  erforderliche Daten, Methoden-, Rechte- und Teststatus sowie das naechste
  Gate.
- DIN/TS 18599-10 wird ausschliesslich aus den vorhandenen 43
  Profil-Metadatensaetzen als `schema_ready_values_not_released` gefuehrt.
- Das vorhandene DIN-4108-2-Legacy-Feld ist nur ein
  `data_field_candidate_rule_not_defined`; die fruehere leere Excel-Spalte
  wurde aus der normalen Kennwerttabelle entfernt.
- Beide Kandidaten bleiben `NOT_EVALUABLE`. `ma_validation` prueft spaeter
  Daten-/Vertragsbereitschaft; die fachliche Regel und Berechnung bleibt beim
  Stage-3-Owner.

## Metadatenanalyse der vorhandenen Normquellen 2026-08-11

Die Analyse verwendet ausschliesslich den versionierten Locator
`data/common/normen/source_inventory_metadata.yaml`, den wertfreien
Zonenprofilvertrag und eigene Profilmetadaten. Norm-PDFs und geschuetzte
Inhalte wurden nicht geoeffnet.

- `DIN/TS 18599-10` ist wegen der 43 vorhandenen Profilidentitaeten und des
  wertfreien Zielschemas `schema_ready`; Profilwerte und Regeln sind nicht
  freigegeben.
- `DIN 4108-2` ist nur `data_field_candidate`, weil der Legacy-Bericht eine
  unberechnete Gradstunden-Spalte kannte. Ausgabe, Methode und Kriterien sind
  nicht fachlich bestaetigt.
- Die uebrigen katalogisierten DIN-, DIN-EN-, DIN-EN-ISO-, VDI-, GEG-, HBO-
  und HOAI-Gruppen bleiben `inventory_only`. Aus Dateinamen wird weder
  fachliche Eignung noch Aktualitaet oder Anwendbarkeit abgeleitet.
- Vor jeder Aktivierung sind exaktes Dokument und Ausgabe, Herkunfts- und
  Maschinenverarbeitungsrecht, manuell dokumentierte Fundstelle,
  qualifizierter Fachreview, Einheit und Geltungsbereich, eigener begrenzter
  Regeltext, reproduzierbarer Test und menschliche Bestaetigung erforderlich.

## Quellen- und Rechteklärung 2026-08-13

Eine gezielte externe Orientierung hat die bestehende Rechtegrenze bestätigt,
ohne selbst eine Rechtefreigabe für Projektdateien zu erteilen:

- § 44b UrhG ordnet automatisierte Analysen als Text und Data Mining ein und
  erlaubt die dafür notwendigen Kopien nur bei rechtmäßig zugänglichen Werken
  und ohne entgegenstehenden Nutzungsvorbehalt des Rechteinhabers.
- Die DIN-Media-AGB (Stand Mai 2026) verlangen für die maschinelle oder
  KI-gestützte Verarbeitung technischer Regeln für eigene innerbetriebliche
  Zwecke zusätzlich eine KI-Lizenz. Sie nennen insbesondere Analyse,
  Auswertung, Strukturierung, Extraktion, Verarbeitung, Verknüpfung und
  Indexierung.
- Die Recherche bezieht sich nicht auf den individuellen Bezugsweg der
  vorhandenen DIN-, VDI-, VDE- oder ISO-Dokumente. Sie ist keine Rechtsberatung
  und belegt weder den konkreten Vertrag noch eine zulässige Verarbeitung.

Damit bleibt die bestehende Grenze unverändert: Die im lokalen Normenbestand
liegenden PDFs werden nicht inhaltlich geöffnet oder automatisiert verarbeitet;
Normwerte, Formeln, Tabellen und PASS-/FAIL-Regeln werden nicht übernommen.

Für einen späteren, dokumentbezogenen Start sind in der führenden
Quellen-/Rechteakte mindestens festzuhalten: Dokumentnummer und Ausgabe,
Bezugsweg, autorisierter Nutzer, geltende Lizenzbedingungen, zulässige
Operationen (Öffnen, Extrahieren, Vergleichen, Ableiten, Speichern,
Veröffentlichen) sowie der konkrete schriftliche Nachweis. Erst danach folgen
manuell dokumentierte Fundstelle, Einheit und Geltungsbereich, Fachreview,
Methodenprüfung, reproduzierbarer Test und menschliche Bestätigung.

## Eingangsauswertung 2026-08-13: Technical Standard Proof

Die Stage-2/3-Arbeitsanweisung bestaetigt die fachlich sinnvolle Trennung von
technischer Variante, Ergebniswerten, Bewertungsprofilen und Anforderungen.
`Standard Evaluation Profile`, eine generische Verifikationsstruktur und
sommerlicher Waermeschutz sind nur Kandidaten fuer einen spaeteren P020-Slice.

Sie ersetzen weder den bestehenden `NormVerificationReport` mit
`pass`/`fail`/`warning`/`not_evaluable` noch die Rechte-, Methoden- und
Fachtestgates dieses Plans. Insbesondere wurden keine Normwerte, Formeln,
PASS/FAIL-Regeln oder Literaturinhalte aus dem zugehoerigen Quellenpaket
uebernommen.

## Eingangsauswertung 2026-08-14: Quellenmetadaten

Das Literaturpaket ist nun als internes Quellenregister inventarisiert. Die
Aufnahme beschraenkt sich auf Nutzer-Metadaten und verlinkte Fundstellen; die
enthaltenen PDF-Dateien und Norminhalte wurden nicht extrahiert oder
verarbeitet. Die dort vorgeschlagene Begriffstrennung von `Standard
Evaluation Profile` und `Standard Verification` bleibt ein Kandidat fuer
einen spaeteren P020-Slice und aendert weder den kanonischen Modulnamen noch
die bestehenden Rechte-, Methoden- und Fachtestgates.

## Eingangsauswertung 2026-08-19: Bachelor-Excel zum sommerlichen Waermeschutz

Die nutzereigene Arbeitsmappe `Bachelor_Endpäsentation_221213.xlsx` wurde
read-only als fachlicher Ausgangspunkt analysiert. Fuer P020 sind insbesondere
die drei Register `Sommer. WS Übersicht`, `Sommerl. WS Ist-Zustand` und
`Sommerl. WS verbessert` relevant. Die Register `Flächen & Cwirk neu`,
`Flächenermittelung` und `Zonierung - Argumentation` beschreiben benoetigte
Eingabebezuege, werden aber nicht zu einer zweiten Gebaeude- oder
Zonenwahrheit.

Das vorlaeufige, noch nicht umsetzungsgeplante Zielbild umfasst innerhalb von
`ma_analyse.stage_3_standards_verification` drei Ansichten:

1. `Übersicht` fuer Datenstatus, Annahmen, Quellen, Ergebnisstatus und
   fehlende Nachweise,
2. `Aktueller Zustand` fuer einen nachvollziehbaren Ausgangsfall mit allen
   Zwischenwerten,
3. `Variantenanalyse` fuer die Auswahl und Gegenueberstellung von Varianten
   sowie Raeumen oder Zonen.

Die in der Arbeitsmappe enthaltenen Formeln duerfen in einem spaeteren,
getrennt freizugebenden Slice nur als identifizierte Legacy-Methode
reproduziert werden. `legacy_user_workbook_method`, `DRAFT` und
`NOT_VERIFIED` sind dabei vorlaeufige Fachbegriffe, keine beschlossenen API-
oder Enum-Werte. Bis zur bestaetigten Normausgabe, Methode, Fundstelle,
Rechtebasis und einem reproduzierbaren Fachtest bleibt der bestehende
Verifikationsstatus `NOT_EVALUABLE`; ein normatives `PASS` oder `FAIL` ist
ausgeschlossen.

Die Fachverantwortung bleibt getrennt:

- `ma_building` besitzt Raumgeometrie, Flaechen, Volumen, Bauteile,
  Oeffnungen und Sonnenschutzobjekte,
- `ma_zones` besitzt Raum-Zonen-Zuordnung, Nutzungs- und Betriebsbezug sowie
  die dokumentierte Zuweisungsbegruendung,
- Stage 3 referenziert diese Objekte ueber stabile Projekt-, Varianten-,
  Raum- und Zonenkennungen und besitzt Nachweisannahmen, Berechnung und
  Ergebnis,
- `ma_assessment` darf spaeter nur standardisierte Stage-3-Ergebnisse
  aggregieren und fuehrt keine Primaerberechnung aus.

Der Prompt-Intake ist nicht abgeschlossen. OP-020 fuehrt die noch offenen
Entscheidungen zu Beispielstand, Parameterumfang, Schnittstellenscope,
Quellablage und Auswahlsemantik. Erst `Prompt abschliessen` und danach
`umsetzungsplan erstellen` duerfen aus diesem Eingang einen unabhaengigen,
Sol-geprueften Umsetzungsscope erzeugen.
