---
name: prompt-intake
description: "Fuehre neue Arbeitsthemen mit einem strukturierten Prompt-Intake ein. Verwende diesen Skill bei `neues thema`, `neues thema: ...`, `themenwechsel` und `Prompt abschliessen`; formuliere den Arbeitsauftrag und frage alle aus Nutzernachrichten nicht klar ableitbaren Angaben nach."
---

# Themenstart und Prompt-Intake

Nutze diesen Skill nur fuer einen ausdruecklichen Themenstart. Normale
Fortsetzungen eines bestehenden Themas bleiben davon unberuehrt.
Lies fuer die anschliessenden Freigabe- und Umsetzungsregeln
`docs/project/UPDATE_ROUTINES.md`.

## Themenstart

1. Behandle den bisherigen Auftrag als abgeschlossen oder pausiert. Nutze ihn
   nur noch, wenn der Nutzer eine Verbindung zum neuen Thema nennt.
2. Formuliere einen vorlaeufigen Arbeitsauftrag mit dem, was bereits klar ist.
3. Stelle Rueckfragen zu jeder Information, die fuer einen guten Auftrag
   relevant ist und nicht klar aus den Nutzernachrichten hervorgeht. Frage in
   Bloecken von hoechstens vier Fragen, damit Antworten einfach bleiben.
4. Wiederhole die Schritte 2 und 3, bis Ziel, Ergebnis, Umfang und Grenzen
   ausreichend beschrieben sind.
5. Fuehre keine Datei- oder Systemaenderungen aus. Die normale Analyse,
   Planung und das Freigabe-Gate gelten erst nach dem Abschluss des Prompts.

## Fragemuster

Pruefe nacheinander diese Punkte und frage jeden unbekannten, relevanten Punkt
nach:

- Ziel und messbares Ergebnis
- Zielgruppe, Nutzung und Erfolgskriterium
- betroffene Dateien, Module, Daten oder Quellen
- Umfang sowie ausdrueckliche Nicht-Ziele
- vorhandene Beispiele, Vorlagen und gewuenschtes Ausgabeformat
- fachliche Annahmen, Randbedingungen und Prioritaeten
- Anforderungen an Nachvollziehbarkeit, Genauigkeit und Erweiterbarkeit
- Risiken, Rechte- oder Freigabegrenzen

Stelle keine Frage erneut, wenn der Nutzer sie bereits klar beantwortet hat.
Leite fehlende Fakten nicht stillschweigend aus aelteren, nicht verknuepften
Themen ab.

## Abschluss

Bei `Prompt abschliessen` liefere einen eindeutigen finalen Arbeits-Prompt mit:

- Rolle und Kontext
- Ziel und erwartetes Ergebnis
- Scope und Nicht-Ziele
- bekannte Eingaben, Annahmen und Grenzen
- Pruef- und Dokumentationsanforderungen

Wenn eine relevante Angabe weiter unklar ist, benenne sie und frage nach;
schliesse den Prompt nicht mit stillschweigenden Annahmen ab. Danach folgt bei
groesseren Aufgaben die normale Analyse und der Umsetzungsplan. Aenderungen
beginnen erst nach `Freigabe zur Umsetzung`.
