# P030 research_tools Prozessmessung und Vergleichsauswertung

Stand: 2026-07-31
Status: Fachlich geplant, von der Produktivsoftware getrennt
Prioritaet: Hoch fuer die Methodik der Masterarbeit
Abhaengigkeiten: technische Logs aus P011-P021; keine Rueckabhaengigkeit der Fachmodule

## Ziel

`research_tools` ist die getrennte Forschungsschicht der Masterarbeit. Sie
erfasst und vergleicht Preprocessing-, Simulations- und Postprocessing-Zeit,
aktive Nutzerzeit, Maschinenzeit, Pruef-/Korrekturzeit, Fehler und
Wiederholungen. Sie erzeugt daraus Tabellen, Diagrammdaten und methodische
Vergleichsberichte.

Die produktive Fachsoftware bleibt davon unabhaengig: Ein Run, eine Variante
oder eine Freigabe haengen nie von einer Prozessmessung ab.

Der Referenzprozess der Fachkompetenz bleibt manuell: statische
Dimensionierung, Excel-Vorbereitung, IDA-ICE-Modellierung und dynamische
Simulation. P030 bewertet ausschliesslich die Prozessinnovation der
Projektsoftware gegenüber diesem Referenzprozess; sie ersetzt keine
fachliche IDA-ICE-Bewertung.

## Grenzen und Prozessmodi

Gemessen werden drei getrennte Prozessgrenzen:

- PreProcess: vom fuer beide Vergleichswege identisch freigegebenen
  Eingabepaket und Beginn der ersten aktiven Bearbeitung bis zum validierten,
  materialisierten P018-Run-Paket mit `released_for_simulation`.
- Kernprozess (MainProcess): von der ersten Export-/Uebergabehandlung ueber
  manuelle Bearbeitung und Simulation bis zum technisch validierten
  Ergebnisimport mit `standardized_ready`.
- PostProcess: ab demselben Ereignis `standardized_ready`; erster Schritt ist
  `standardized -> prepared`, Ende ist das vor dem Versuch festgelegte,
  vollstaendig erzeugte Analyse-, Diagramm- und Berichtsartefaktpaket.

Innerhalb des Kernprozesses bleiben Export-/Uebergabezeit, aktive
IDA-Bearbeitung, Maschinen-/Simulationszeit, Wartezeit,
Import-/Mappingzeit sowie Pruef-/Korrekturzeit getrennte Unterkategorien.
Wiederholungen und Fehlversuche bleiben in der Messung und werden nach Ursache
gekennzeichnet.

Die Prozessmodi sind `manual`, `software_assisted` und
`automated_concept`. Der konzeptionell automatisierte Modus wird klar als
Schätzung oder Zielwert gekennzeichnet und nicht als beobachtete Messung
ausgegeben.

## Datenmodell

Ein `ProcessEvaluation` referenziert optional `PRJ`, `SDIR`, `STC`, `RUN` und
`VAR`, ohne deren Fachwerte zu kopieren. Es enthält:

- Prozessmodus und explizite Prozessgrenze,
- Zeitwerte für aktive Nutzerzeit, Maschinenzeit, Pruefzeit, Korrekturzeit
  und verstrichene Gesamtzeit,
- Herkunft jedes Messwerts: `observed`, `manual_entry`, `log_derived`,
  `calculated` oder `estimated`,
- Fehler-, Warnungs-, Wiederholungs- und Dateimetriken,
- Versuchskonfiguration, Notizen und Referenzen auf technische Logs.

Die Forschungsdaten liegen ausserhalb produktiver Run-Ordner, etwa unter
`research_measurements/EVAL-<id>/`. Sie bestehen aus `evaluation.yaml`,
manuellen Messwerten, referenzierten oder kopierten Logs, abgeleiteten
Kennzahlen und Notizen.

## Log-Anforderungen

P030 liest technische Logs nur lesend. P027 stellt dafuer, soweit sinnvoll,
Zeitstempel, Modul, Operation, Status, Dauer, betroffene Objekt-IDs,
Warnungs-/Fehlercodes sowie Objekt-, Datei- und Datenmengen bereit.

P030 speichert manuelle Eingaben getrennt von Logdaten. Ohne auswertbares
Simulationslog darf die Simulationsdauer manuell eingegeben werden, muss dann
aber als `manual_entry` gekennzeichnet sein.

## Vergleichskennzahlen

- aktive Nutzer-, Maschinen-, Pruef-, Korrektur-, Simulations- und
  Postprocessing-Zeit,
- Zeit je Variante, Anzahl Arbeitsschritte, manuelle Eingriffe,
  Medienbrueche und Wiederholungen,
- erkannte/korrigierte Fehler, offene Warnungen, Vollstaendigkeit und
  Reproduzierbarkeit,
- Dateianzahl, Speicherbedarf und Packaging-Aufwand.

Abgeleitete Kennzahlen wie Zeitersparnis und Beschleunigungsfaktor duerfen nur
berechnet werden, wenn Prozessgrenze und Messherkunft vergleichbar sind.

## Umsetzungsslices

### P030-S1 Datenmodell

- `ProcessEvaluation`, Prozessgrenzen, Prozessmodi und Messwertherkunft.
- YAML-/CSV-Schemas und Validierung eindeutiger Referenzen.

### P030-S2 Manuelle Versuchserfassung

- Pre-, Simulations- und Postprocessing-Zeiten, Notizen und
  Versuchskonfiguration.
- Referenzen auf Projekt-, Study- und Run-IDs.

### P030-S3 Log-Import

- generische Schnittstelle fuer eigene technische JSONL-/Textlogs,
- Zuordnung zu Prozessabschnitten und Ableitung der Maschinenzeit.

### P030-S4 Vergleich und Reporting

- mindestens zwei vergleichbare Versuche,
- CSV-Ausgabe, Tabellen, Diagrammdaten und Kennzeichnung geschaetzter Werte.

## Akzeptanzkriterien

- Preprocessing, Simulation und Postprocessing sind getrennt auswertbar.
- Aktive Nutzerzeit und Maschinenzeit werden getrennt ausgewiesen.
- Messwerte sind nach Herkunft eindeutig gekennzeichnet.
- Mindestens ein manueller und ein softwareunterstuetzter Versuch sind
  vergleichbar.
- Forschungsergebnisse veraendern keine Fachobjekte, Varianten, Runs oder
  Freigaben.

## Masterarbeits-MVP V1

Der erste Vergleich umfasst mindestens einen softwareunterstuetzten
Referenzdurchlauf und einen dokumentierten manuellen Vergleichsdurchlauf. Er
verwendet dieselbe Prozessgrenze und dieselben angeforderten,
datenkompatiblen Ergebnisartefakte. Die frueher beispielhaft genannten drei
Diagrammarten sind kein abschliessendes V1-Paket mehr. Vor Ergebnissichtung
werden aus dem freigegebenen Dateninventar primaere Abbildungen fuer die
Arbeit und ergaenzende/explorative Ausgaben festgelegt, ohne vorhandene
Diagrammvorlagen stillschweigend zu veraendern. Abweichende Messherkunft oder
abweichende Grenzen werden nicht zu einer scheinbaren Zeitersparnis
zusammengefasst.

## Nicht Teil der Masterarbeit

- Bildschirmaufzeichnung und vollautomatische Erfassung aller
  Nutzerinteraktionen,
- Auswertung fremder proprietaerer Logs ohne dokumentiertes Format,
- produktive Telemetrie, Cloud-Dashboard und Prozesszeitprognosen.

## Konsolidierung nach UD-112 2026-07-31

Der Vergleichsfall ist SmallOffice als erster Demonstrator. Alle in VGEN
erzeugten Varianten werden danach manuell in IDA ICE bearbeitet und liefern
damit die Beobachtungswerte fuer den Simulationsschritt. Ein Ergebnis darf
nicht als allgemeingueltige Gebaeudewirkung ausgegeben werden, sondern als
nachvollziehbare Fallstudie.

`observed` bezeichnet in P030 ausschliesslich Prozesszeiten und andere direkt
erfasste Prozessdaten. IDA-Ausgaben sind simulierte Modellergebnisse;
Energie, Leistungsspitzen, Zeitersparnis und Kosten sind daraus abgeleitete
Berechnungen, eine fachliche Verbesserung bleibt Interpretation. Varianten
eines RUN sind Arbeitsmengen und keine voneinander unabhaengigen
Wiederholungen eines Zeitversuchs.

PreProcess wird nicht nur als Gesamtzeit gemessen. Das Messprotokoll erfasst
mindestens Anzahl und Komplexitaet der Parameter, Anzahl geaenderter Werte je
Variante und Variantenanzahl; Zonen- und Ausgabemenge werden konstant gehalten
oder separat dokumentiert. Die Zeitgrenzen sind: PreProcess bis zum Setup,
manuelle IDA-Arbeit je `(RUN, VAR)`, Maschinen-/Simulationsdauer je
`(RUN, VAR)`, Pruef-/Korrekturzeit sowie PostProcess je Variante und gesamt.

Aktive Eingabe-, Pruef- und Korrekturzeit bildet die spaetere Personalkosten-
Basis. Maschinen- und Wartezeit werden getrennt berichtet. Entwicklung,
Einarbeitung und Lizenzkosten duerfen nur in einem deutlich getrennten
Adoptionsszenario erscheinen. Rollen/Wissensprofil, Stundensatzquelle,
Bezugsjahr, Zuschlaege, Wiederholungen und der Umgang mit Lerneffekten bleiben
in OP-009 vor dem Kostenvergleich zu entscheiden.

Manueller und softwaregestuetzter Ablauf muessen dieselben Eingaben,
Varianten, Prozessgrenzen, Pruefanforderungen und Ergebnisartefakte besitzen.
`automated_concept` bleibt Schaetzung und wird nicht mit beobachteter
Zeitersparnis vermischt.
