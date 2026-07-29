# Chat-Handover – Prozessmessung und Kostenvergleich

Datum: 2026-07-29
Status: Arbeitsartefakte erstellt; wissenschaftlicher Vergleich noch offen
Arbeitsbereich: P030 `research_tools` Prozessmessung und Vergleichsauswertung

## Zweck

Dieser historische Snapshot sichert den Stand der ersten technischen
PreProcess-Messung und der zugehoerigen editierbaren Kostenvergleichsdatei.
Er ersetzt weder `PLAN_STATUS.md`, P030 noch die offenen Nutzerentscheidungen.
Bei Widerspruechen bleiben diese Quellen fuehrend.

## Kopierfertige Uebergabe fuer den naechsten Chat

```text
Arbeite im Repository 260524_Masterarbeit_Analyse nach AGENTS.md und den
projektlokalen Skills. Fuer Prozessmessung und Kostenvergleich lies zuerst
P030, OP-009, PLAN_STATUS.md und diesen Handover.

Es liegt ein erster technischer Benchmark des SmallOffice-V1-PreProcesses vor:
- Workspace-Anlage: 0,024139 s
- V1-PreProcess bis Simulation-Setup: 1,261857 s
- Gesamt: 1,286002 s
- 30 Optimierungs- plus 8 Sensitivitaetspakete, keine kritischen Fehler

Der Benchmark misst nur die technische Reststrecke mit vorbereiteten,
versionierten Eingaben. Er ist kein vollstaendiger manueller Gegenversuch und
keine IDA-Simulation. Zeit- oder Kosteneinsparungen duerfen daher noch nicht
behauptet werden.

Die editierbare Excel-Datei besitzt die Tabs Manuell, Prozess automatisiert,
Kosten und Vergleich. Quellen und Erlaeuterungen stehen direkt im Tab Kosten.
Der Vergleich ist bewusst auf "Nein" gesetzt, bis Prozessgrenze,
Variantenanzahl, Ergebnisqualitaet und Messherkunft vergleichbar sind.

Kostenwerte sind editierbare Arbeitsannahmen, keine beschlossene Methodik:
- interner fachnaher Vollkostensatz: 57 EUR/h, Sensitivitaet 45–70 EUR/h
- externer Fachplaner Bauphysik: 95 EUR/h netto, Sensitivitaet 80–115 EUR/h
- Strom: 0,4055 EUR/kWh privat beziehungsweise 0,3258 EUR/kWh kleiner
  Nichthaushalt
- Rechnerleistung: 75 W; Hardware-Vollkosten: 0,36 EUR/Maschinenstunde

OP-009 bleibt offen. Vor einer wissenschaftlichen Auswertung sind die
Kostenperspektive, Prozessgrenze, Vergleichseinheit, Wissensprofile,
Qualitaetsgleichheit und echte manuelle Zeiten festzulegen.
```

## Arbeitsartefakte ausserhalb des Repositories

Die Arbeitsartefakte liegen bewusst in der lokalen Schwesterarbeitsablage und
sind nicht Teil des Repositorys:

- `../260524_Masterarbeit_Arbeitsablage/04_Teil2_Prozessinnovation/Prozessmessung/20260729_PreProcess_V1_Benchmark_c278f4cf/`
  - vollstaendiger isolierter Benchmark-Workspace,
  - 10 Modulberichte, 30 Optimierungs- und 8 Sensitivitaetspakete,
  - `timings.csv`, `diagnostics.yaml` und `README.md`.
- `../260524_Masterarbeit_Arbeitsablage/04_Teil2_Prozessinnovation/Prozessmessung/Prozesskostenvergleich_Manuell_vs_Automatisiert.xlsx`
  - editierbare Vergleichsdatei mit vier Registerkarten.

## Mess- und Fachstand

Der Lauf erstellt einen neuen lokalen Projekt-Workspace und fuehrt die
kanonische Kette

`Projekt -> Wetter -> Gebaeude -> Zonen -> Technik -> Parameter -> Referenzdimensionierung -> Parameter-Variationsspezifikation -> Varianten -> Simulation-Setup`

aus. Er verwendet nur lokale Projektsoftware und versionierte
Konfigurationsdaten; weder IDA ICE noch Web-, Cloud- oder externe APIs wurden
gestartet.

Die Referenzdimensionierung lieferte 54,13 kW Heizlast, 9,72 kW interne
Kuehllast und 3.053,88 m3/h Luftvolumenstrom. Diese Ergebnisse sind
LoD-1-Startwerte und keine gemessenen oder dynamisch simulierten Kennwerte.

## Kostenannahmen und Quellenstatus

Die Kostenannahmen dienen ausschliesslich als erste pflegbare Arbeitsbasis in
der Excel-Datei. Sie sind durch Quellenfelder, Links und Erlaeuterungen
dokumentiert:

- Destatis Arbeitskosten 2025 fuer den allgemeinen Kostenrahmen,
- AHO-Stundensatzrechner und Bauphysik-Marktindikator fuer den externen
  Fachplaner-Satz,
- Destatis Strompreisstatistik fuer die Ersatzwerte.

Ein externer Fachplaner-Stundensatz enthaelt regelmaessig Buerogemeinkosten;
Rechner- und Stromkosten duerfen dafuer nicht noch einmal pauschal addiert
werden. Rechner- und Stromkosten betreffen im Vergleich den eigenen
automatisierten Lauf. Grenzkosten und Vollkosten sind getrennt auszuweisen.

## Offene Punkte und naechste Schritte

- OP-009: Methodik fuer Zeit- und Personalkostenvergleich entscheiden.
- Einen echten manuellen und einen softwareunterstuetzten Vergleichslauf mit
  identischer Prozessgrenze, Variantenmenge und Ergebnisqualitaet erfassen.
- Vorbereitung, fachliche Abnahme, Fehlerkorrektur und gegebenenfalls
  Wartezeiten getrennt messen; Kategorien duerfen sich nicht ueberlappen.
- Den Vergleich in der Excel-Datei erst aktivieren, wenn diese Bedingungen
  erfuellt sind.
- IDA-Simulation und Postprocessing bleiben eigene, noch nicht gemessene
  Prozessgrenzen gemaess P030.

## Fuehrende Referenzen

- `../../plans/inbox/260714_Plan_P030_research_tools_Prozessauswertung.md`
- `../../plans/PLAN_STATUS.md`
- `../../plans/PLAN_INDEX.md`
- `../../decisions/USER_DECISIONS_OPEN_POINTS.md` (OP-009)
- `../../decisions/USER_DECISIONS_MASTERTHESIS_CODE.md` (Prozessinnovation)
- `../../UPDATE_ROUTINES.md`

## Git- und Nachweisstand

- Branch: `main`
- HEAD: `ff1d902` (`v0.35.1-dirty`)
- Der Arbeitsbaum enthielt bei Erstellung bereits nicht zugeordnete,
  uncommittete Aenderungen. Dieser Handover ersetzt oder verwirft sie nicht.
- Keine automatische Git-Aktion wurde ausgefuehrt.
