---
name: prompt-intake
description: "Fuehre neue Arbeitsthemen ueber Prompt-Intake, read-only Sol-Planung und einen getrennten Tera-Umsetzungshandoff. Verwende diesen Skill bei `neues thema`, `neues thema: ...`, `themenwechsel`, `Prompt abschliessen` und `umsetzungsplan erstellen`."
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

## Arbeits-Prompt abschliessen

Bei `Prompt abschliessen` liefere einen eindeutigen finalen Arbeits-Prompt mit:

- Rolle und Kontext
- Ziel und erwartetes Ergebnis
- Scope und Nicht-Ziele
- bekannte Eingaben, Annahmen und Grenzen
- Pruef- und Dokumentationsanforderungen

Wenn eine relevante Angabe weiter unklar ist, benenne sie und frage nach;
schliesse den Prompt nicht mit stillschweigenden Annahmen ab. Der Abschluss
erstellt noch keinen Umsetzungsplan und loest keine Aenderung aus.

## Sol-Planung und Qualitaetspruefung

Bei `umsetzungsplan erstellen` verwende den abgeschlossenen Arbeits-Prompt.
Fehlt er, fordere zuerst `Prompt abschliessen` an.

1. Beauftrage einen getrennten Sol-Agenten auf hoher Stufe
   (`quality_auditor`) ausschliesslich read-only mit Planung und
   Qualitaetspruefung. Er liest nur die fuer den Prompt benoetigten
   Projektquellen und aendert keine Dateien.
2. Lass ihn einen konkreten, kleinen Umsetzungsplan erstellen und auf
   Architekturkonflikte, Regressionen, Testluecken, Risiken, Rechte- und
   Freigabegrenzen pruefen. Sein Ergebnis muss die unten festgelegte
   Planstruktur vollstaendig enthalten; fehlt ein Abschnitt, lasse ihn den
   Plan read-only vervollstaendigen.
3. Speichere das unveraenderte Ergebnis nach seiner Rueckgabe durch den
   koordinierenden Agenten als eigenstaendigen Plan unter
   `docs/project/plans/independent/`. Der Dateiname besteht aus Datum und
   einem frei aus dem Inhalt abgeleiteten Titel; er erhaelt keine `P`-Nummer.
4. Trage diesen unabhaengigen Plan nicht automatisch in `PLAN_INDEX.md` oder
   `PLAN_STATUS.md` ein und arbeite ihn nicht in bestehende Projektplaene ein.

Der Plan muss diese Struktur verwenden:

```text
# Unabhaengiger Umsetzungsplan: <freier Titel>

Datum: <YYMMDD>
Status: Sol-geplant und qualitaetsgeprueft; noch nicht zur Umsetzung freigegeben

## Arbeits-Prompt
<vollstaendiger, durch Prompt abschliessen erzeugter Arbeits-Prompt>

## Ziel
## Scope und Nicht-Ziele
## Betroffene Bereiche
## Umsetzungsschritte
## Pruefungen
## Risiken und offene Entscheidungen
## Tera-Uebergabe
```

Damit liegt der abgeschlossene Arbeits-Prompt nach dem Speichern im
eigenstaendigen Plan vor. Ein kleiner Umsetzungsplan umfasst genau einen
fachlich und technisch begrenzten Umsetzungsscope.

Nutze als Dateinamen `YYMMDD_<freier-inhaltlicher-titel>.md`. Existiert der
Name bereits, verwende den ersten freien Suffix `-v2`, `-v3` und so weiter.

## Tera-Uebergabe

Fuer die Umsetzung in einem neuen Chat uebergibt der Nutzer oder der
koordinierende Agent den konkreten Planpfad mit diesem kurzen Prompt:

```text
Setze den freigegebenen unabhängigen Umsetzungsplan
`<Planpfad>` um.

Lies den Plan vollständig. Prüfe den aktuellen Bestand nur im darin benannten
Scope. Setze ausschließlich die freigegebenen Schritte um, führe die
vorgesehenen Prüfungen aus und dokumentiere Abweichungen. Halte an, falls
eine Scope-Erweiterung, neue Abhängigkeit, Löschung oder externe Aktion nötig
wird.
```

Die Umsetzung beginnt erst nach `Freigabe zur Umsetzung`. Nach ihrem Abschluss
fragt der Tera-Chat den Nutzer nach der Einordnung. Nur auf dessen
ausdrueckliche Entscheidung wird entweder der benannte bestehende formelle
Plan aktualisiert, ueber `plan aufnehmen` ein neuer `P`-Plan angelegt oder
der unabhaengige Plan als abgeschlossener Einzelplan belassen.
