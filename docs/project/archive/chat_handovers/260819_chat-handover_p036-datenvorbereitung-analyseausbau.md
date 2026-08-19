# Chat-Handover – P036 Datenvorbereitung und Analyseausbau

Stand: 2026-08-19
Status: Technischer Prototyp umgesetzt und versioniert; quantitative
Energieaussagen aus IDA-Zeitreihen noch nicht fachlich freigegeben.

## Abgeschlossener Arbeitsstand

- Das eigenstaendige Modul `ma_data_preparation` bereitet standardisierte
  Simulationsergebnisse unabhaengig vom spaeteren Analysezweck auf. Der
  programmspezifische Import bleibt im IDA-Adapter; der Analysebefehl
  `prepare` dient als Kompatibilitaetsfassade.
- Der IDA-ICE-Ergebnisadapter erkennt freigegebene PRN-Zeitreihen sowie
  HTML-Berichte und XLSX-Arbeitsmappen. Vollstaendige IDA-Modellinhalte in
  IDM- oder IDC-Dateien wurden nicht verarbeitet.
- Datenqualitaet, Provenienz, Hashpruefung, lueckensichere
  Zeitreihenaufbereitung und speicherschlanke Wiederaufnahme grosser lokaler
  Laeufe sind umgesetzt.
- Das reduzierte Fuenf-Zonen-Modell (`5Z`) und das detaillierte
  29-Zonen-Modell (`29Z`) besitzen einheitliche Zonenkennwerttabellen. Der
  historische Optimierungsbestand (`ALT`) besitzt einen rein deskriptiven
  Vergleich der Referenz sowie der Heizleistungsvarianten von 90 bis
  50 Prozent; daraus wird keine optimale Variante automatisch ausgewaehlt.
- Analyse-Stufe 2 besitzt ein konfigurierbares Machbarkeitsframework.
  Analyse-Stufe 3 besitzt ein technisch vorbereitetes Nachweisframework,
  jedoch keine produktiven Normgrenzwerte oder Normbewertung.
- Der Diagramm-Slice wurde entsprechend der Nutzerentscheidung nicht
  umgesetzt.

## Methodischer Geltungsbereich

- `PARTIAL` bedeutet technisch verarbeitet, aber noch nicht fuer alle
  vorgesehenen fachlichen Aussagen geeignet. Die oeffentlich auffindbare
  EQUA-Dokumentation belegt nicht eindeutig, ob exportierte PRN-
  Leistungswerte Stuetzstellen oder Intervallmittelwerte sind.
- Erkannte Luecken und nicht eindeutige Reihen werden nicht integriert.
  Fehlende quantitative Energiekennwerte bleiben leer statt geschaetzt zu
  werden.
- Bis zu einer belegten und vom Nutzer bestaetigten Methodenentscheidung zur
  PRN-Zeit-, Perioden-, Leistungs- und Vorzeichenbedeutung sind quantitative
  Energie- und Gebaeudeaussagen aus diesen Reihen gesperrt. Das zugehoerige
  Fachgate und seine Pruefpunkte stehen ausschliesslich in P036 und
  `PLAN_STATUS.md`.
- Die erzeugten Tabellen sind kontrollierte Arbeitsstaende und noch kein
  zitierfaehiger Energie- oder Normnachweis.

## Lokale Arbeitsausgaben

- `data/ma_analyse/output/tables/Zonenkennwerte_5Z.xlsx`: Kennwertstruktur
  fuer die fuenf Zonen des Hauptmodells; PRN-Energieableitungen bleiben
  `PARTIAL`.
- `data/ma_analyse/output/tables/Zonenkennwerte_29Z.xlsx`: Kurzvergleich der
  29 Zonen des detaillierten Referenzmodells; nicht eindeutig integrierbare
  Energiewerte bleiben leer.
- `data/ma_analyse/output/tables/Optimierungsvergleich_ALT.xlsx`:
  30 Vergleichszeilen aus sechs Varianten und fuenf Zonen; deskriptive
  Last-, Temperatur- und Raumluftkennwerte ohne Bestvariantenauswahl.
- Der vorbereitete lokale Datenbestand umfasst 116 Pakete fuer 5Z,
  600 Pakete fuer 29Z und 174 Pakete fuer ALT unter
  `data/ma_analyse/database`. Diese Arbeitsdaten sind Git-ignoriert.

## Technische Nachweise

- 201 Tests aus den Bereichen Datenvorbereitung, IDA-Import, Zonenmetadaten,
  Zonenkennwerttabellen, ALT-Vergleich, zeitgewichtete Kennwerte,
  Stage-2-/Stage-3-Vertraege, Prepare-Fassade, Workflow und UI bestanden.
  Ruff und `git diff --check` waren fuer diesen Scope sauber.
- Der P036-Grundstand wurde im Commit `e573063` (`Release 0.40.0`) versioniert.
  Die spaetere Anzeigeprojektion fuer wiederholte IDA-Stuetzstellen wurde im
  Commit `9f58b57` (`Release 0.42.0`) ergaenzt. Beim Handover ist
  `5562b5d` (`Release 0.42.1`) der aktuelle Repository-HEAD.
- Der Navigator wurde nach der P036-Umsetzung und nach der ausdruecklichen
  Umsetzungsfreigabe am 2026-08-19 erneut auf den aktuellen Projekt- und
  Handover-Stand aktualisiert. Die anschliessende Validierung ist im
  Handover-Abschluss nachgewiesen.

## Fuehrende Referenzen

- `docs/project/plans/inbox/260813_Plan_P036_ma_data_preparation_Analyseausbau.md`
  ist der fuehrende Umsetzungsplan und enthaelt die verbleibenden Fachgates.
- `docs/project/plans/PLAN_STATUS.md` fuehrt den kompakten aktuellen
  Projektstatus und verweist auf die naechste P036-Arbeit.
- UD-126 in
  `docs/project/decisions/USER_DECISIONS_MASTERTHESIS_CODE.md` fuehrt die
  Nutzerentscheidungen zu Modulowner, 5Z-Fokus, ALT-/29Z-Grenze sowie
  Diagramm- und Laufzeitbehandlung.
- `docs/ma_analyse/normen_und_outputkatalog.md` ist das bibliografische
  Regelwerksinventar mit projektseitiger Output-Zuordnung; es ist kein
  Normnachweis.

Dieser historische Snapshot erzeugt keine zusaetzlichen Aufgaben oder
Entscheidungen. Weiterarbeit und offene Fachfragen bleiben ausschliesslich in
den genannten fuehrenden Projektquellen dokumentiert.

## Repository-Grenze beim Handover

Der aktuelle Arbeitsbaum enthaelt bereits vorhandene, nicht aus diesem
P036-Chat stammende uncommittete `ma_core`-/Workflow-
Dokumentationsaenderungen. Sie wurden weder veraendert noch in diesen
Snapshot als P036-Arbeit aufgenommen.
