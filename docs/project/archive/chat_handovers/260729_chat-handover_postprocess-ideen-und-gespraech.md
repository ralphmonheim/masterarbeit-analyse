# Chat-Handover – PostProcess-Ideen und Vorbereitung der Konzeptdiskussion

Datum: 2026-07-29
Status: Analyse abgeschlossen; fachliche Entscheidungen stehen aus
Arbeitsbereich: PostProcess, P009, P019–P027 und P030

## Zweck

Dieser historische Snapshot sichert die im Chat erarbeitete Bestandsanalyse
und die Ideen fuer ein anschliessendes, umfangreiches Fachgespraech zum
PostProcess. Er ersetzt weder aktive Plaene noch Nutzerentscheidungen.
Bei Widerspruechen bleiben insbesondere `PLAN_STATUS.md`, P009, P019–P027,
P030 und die Entscheidungsdateien fuehrend.

## Kopierfertige Uebergabe fuer den naechsten Chat

```text
Arbeite im Repository 260524_Masterarbeit_Analyse nach AGENTS.md und den
projektlokalen Skills. Das Thema ist der fachliche Zuschnitt des
PostProcess; noch keine Produktivimplementierung beginnen.

Die aktuelle sichtbare Workflowdefinition lautet:
Pre-Process | Main-Process | Post-Process. Export, manuelle Simulation und
Ergebnisimport gehoeren zum Main-Process; ab Datenvorbereitung beginnt der
Post-Process. Validierung und Feedback bleiben Querschnittsmodule.

Der PostProcess ist keine einzelne Funktion, sondern soll in vier klar
getrennte Ebenen gegliedert werden:
1. Ergebnisbasis: manueller neutraler Ergebnisimport, RUN-ID-/VAR-ID-
   Zuordnung, Rohdaten unveraendert sichern, Einheiten/Zeitreihen
   normalisieren, Daten vorbereiten.
2. Fachliche Auswertung: Kennwerte, Diagramme, Variantenvergleich,
   Optimierung sowie spaeter Normnachweis und Sensitivitaet.
3. Entscheidungsausgabe: Wirtschaftlichkeit, betriebliche Emissionen,
   transparente Bewertung, Factsheet und maschinenlesbarer Export.
4. Forschungsebene: getrennte P030-Prozessmessung fuer Zeiten, Fehler,
   Wiederholungen und Vergleich des manuellen mit dem
   softwareunterstuetzten Prozess.

Der kleinste belastbare Masterarbeitskern bleibt:
manuelle Simulation -> Ergebnisaufnahme -> Datenvorbereitung -> drei
Artefakte (Heiz-/Kuehllastdiagramm, Raumklima-/Komfortdiagramm,
Jahres- oder Spitzenwertvergleich) -> P030-Prozessvergleich.

Noch nicht entschieden ist, ob die erste PostProcess-Ausbaustufe neben den
drei Kernartefakten bereits eine kleine Kosten- und CO2-Entscheidungsvorlage
enthalten soll. Diese Frage soll im naechsten Fachgespraech bewusst
entschieden werden.
```

## Dokumentierter Bestandsbefund

- Der Code fuehrt den PostProcess als Katalogphase mit zehn Schritten. Es
  existieren Kompatibilitaetslisten und UI-Statuszeilen, aber kein zentraler
  PostProcess-Runner und kein Sammel-CLI-Befehl.
- Teilweise vorhanden sind Datenvorbereitung sowie Analyse Stufe 2. Die
  uebrigen fachlichen Bausteine sind ueberwiegend geplant oder als Konzept
  beschrieben.
- Der entscheidende technische Einstieg ist P009: ein kleiner,
  programmunabhaengiger manueller Ergebnisimport nach einem stabilen
  P018-Run-Paket. Automatische Simulation, IDA-Dateibearbeitung und ein
  vollstaendiger IDA-Adapter sind nicht Teil dieses MVP-Slices.
- P030 misst den Prozess getrennt von der Produktivsoftware. Es bewertet den
  Arbeitsablauf, nicht die fachliche Guete eines IDA-Modells.

## Ideen und Diskussionsfelder

| Bereich | Vorschlag fuer das Fachgespraech | Bestehende Grenze |
| --- | --- | --- |
| Ergebnisimport | Welches minimale, manuell bereitgestellte Exportformat liefert die drei Kernartefakte? | Rohdaten bleiben unveraendert; Zuordnung ausschliesslich ueber `RUN-ID + VAR-ID`. |
| Datenqualitaet | Welche Pflichtpruefungen gelten fuer Zeitstempel, Einheiten, Vollstaendigkeit und Variantenbezug? | Keine automatische IDA- oder Modellmanipulation. |
| Analyse | Welche Kennwerte und Diagramme beantworten die Masterarbeitsfrage wirklich? | Bestehende `ma_analyse`-Services wiederverwenden, nicht kopieren. |
| Optimierung | Welche Variantenhypothesen, Vergleichsmetriken und fachlichen Pruefschritte sind erforderlich? | Kein Normnachweis und keine automatische Entscheidungsfindung in Stufe 2. |
| Sensitivitaet | Welche Wetter- und Betriebsfaelle sowie Robustheitsmetriken sind relevant? | Ereignisse reproduzierbar; Umnutzung und neuer Zonenzuschnitt bleiben getrennte spaetere Fragen. |
| Normnachweis | Welche fachlichen Nachweisprofile und Testfaelle werden spaeter benoetigt? | Keine produktiven Regeln ohne Quellen-, Methoden- und Rechteklaerung. |
| Kosten und CO2 | Reicht eine kleine, transparente Demo mit klaren Annahmen? | Keine vollstaendige Wirtschaftlichkeitsrechnung oder LCA vortaeuschen. |
| Bewertung | Sollen Gewichtung, Ausschlusskriterien, Scoring und Pareto als Entscheidungshilfe dienen? | Keine Primaerberechnung in `ma_assessment`; Gewichte vor Ergebnissichtung festlegen. |
| Reporting/Export | Welche Ausgabe ist fuer Thesis, Fachentscheidung und Reproduzierbarkeit notwendig? | Fehlende Ergebnisse sichtbar machen; Fachwerte nicht durch Exporte veraendern. |
| Prozessmessung | Welche Prozessgrenze, Wissensprofile, Stundensaetze und Vergleichseinheit gelten? | P030 bleibt getrennt; nur vergleichbare Messungen duerfen zu Zeit- oder Kostenaussagen fuehren. |

## Neue Arbeitsanweisung fuer weitere Handover

Weitere vom Nutzer bereitgestellte ChatGPT-Handover werden zunaechst als
Eingaben gesammelt und gemeinsam mit diesem Snapshot verglichen. Sie werden
nicht automatisch als aktive Projektwahrheit, Entscheidung oder
Umsetzungsfreigabe uebernommen. Der Abgleich soll mindestens unterscheiden:

- bereits dokumentierte Entscheidung,
- kompatible neue Idee,
- offener Entscheidungsbedarf,
- Widerspruch zu einer fuehrenden Quelle,
- moeglicher neuer Plan- oder Umsetzungsslice.

## Fuehrende Referenzen

- `../../plans/inbox/260621_Plan_P009_Simulationsschnittstellen_IDA_Adapter.md`
- `../../plans/inbox/260622_Plan_P019_Stage2_Optimierung.md`
- `../../plans/inbox/260622_Plan_P020_Stage3_Standards_Verification.md`
- `../../plans/inbox/260622_Plan_P021_Stage4_Sensitivitaet.md`
- `../../plans/inbox/260622_Plan_P022_ma_economy_Demo.md` bis
  `../../plans/inbox/260622_Plan_P026_ma_data_export_Konzept.md`
- `../../plans/inbox/260622_Plan_P027_Querschnitt_UI_Workflow_Validation_Feedback.md`
- `../../plans/inbox/260714_Plan_P030_research_tools_Prozessauswertung.md`
- `../../plans/PLAN_STATUS.md`
- `../../decisions/USER_DECISIONS_MASTERTHESIS_CODE.md` (UD-082, UD-083,
  UD-099)
- `../../decisions/USER_DECISIONS_OPEN_POINTS.md` (OP-008, OP-009)
- `../../UPDATE_ROUTINES.md`

## Git- und Nachweisstand

- Branch: `main`
- HEAD: `ff1d902` (`v0.35.1-dirty`)
- Der Arbeitsbaum enthielt bei Erstellung zahlreiche bereits bestehende,
  nicht diesem Handover zugeordnete Aenderungen. Dieser Snapshot ersetzt,
  verwirft oder integriert sie nicht.
- Keine Tests, Installation, Git-Aktion oder externe Verarbeitung wurde durch
  diesen Handover ausgeloest.
