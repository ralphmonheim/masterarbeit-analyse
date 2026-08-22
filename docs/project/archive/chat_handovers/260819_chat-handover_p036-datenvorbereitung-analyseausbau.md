# Chat-Handover – P036 Datenvorbereitung und Analyseausbau

Stand: 2026-08-19
Nachtrag: 2026-08-22 – TODO-Verknuepfung und Klarstellungen aus dem
verbindlichen Blind-Review
Status: Technischer Prototyp umgesetzt und versioniert; quantitative
Energieaussagen aus IDA-Zeitreihen noch nicht fachlich freigegeben.

## Abgeschlossener Arbeitsstand

- Das eigenstaendige Modul `ma_data_preparation` bereitet standardisierte
  Simulationsergebnisse unabhaengig vom spaeteren Analysezweck auf. Der
  programmspezifische Import bleibt im IDA-Adapter; der Analysebefehl
  `prepare` dient als Kompatibilitaetsfassade.
- Der IDA-ICE-Ergebnisadapter erkennt und liest die fuer diesen lokalen
  Arbeitsstand ausdruecklich bereitgestellten PRN-Zeitreihen, HTML-Berichte
  und XLSX-Arbeitsmappen. Er prueft Layout und Provenienz und uebergibt
  auswertbare Inhalte an den standardisierten Ergebnisvertrag. Diese lokale
  Bereitstellung ist keine allgemeine Format- oder Veroeffentlichungsfreigabe.
  Vollstaendige IDA-Modellinhalte in IDM- oder IDC-Dateien wurden nicht
  verarbeitet.
- Datenqualitaet, Provenienz, Hashpruefung, lueckensichere
  Zeitreihenaufbereitung und speicherschlanke Wiederaufnahme grosser lokaler
  Laeufe sind umgesetzt.
- Das reduzierte Fuenf-Zonen-Modell (`5Z`) und das detaillierte
  29-Zonen-Modell (`29Z`) besitzen einheitliche Zonenkennwerttabellen. Der
  historische Optimierungsbestand (`ALT`) besitzt einen rein deskriptiven
  Vergleich der Referenz sowie der Heizleistungsvarianten von 90 bis
  50 Prozent; daraus wird keine optimale Variante automatisch ausgewaehlt.
- Analyse-Stufe 2 kann bereitgestellte Kennwerte gegen explizit konfigurierte
  Machbarkeitsbedingungen pruefen. Sie waehlt keine beste Variante aus.
  Analyse-Stufe 3 besitzt einen technischen Vertrag fuer spaetere
  Nachweisprofile und Kennwertpruefungen; produktive Normprofile,
  Normgrenzwerte und normative PASS-/FAIL-Aussagen bleiben gesperrt.
- Der Diagramm-Slice wurde entsprechend der Nutzerentscheidung nicht
  umgesetzt.

## Methodischer Geltungsbereich

- `PARTIAL` ist zunaechst ein Eignungsstatus einer einzelnen standardisierten
  Zeitreihe. Das JSON-Manifest fuehrt dazu `suitability`,
  `quality_diagnostics` und die Zeitachsendiagnose. In den Zonen- und
  Variantentabellen wird der konservativ abgeleitete Stand je Ergebniszeile
  als `Auswertungsstatus` zusammen mit `Datenabdeckung`,
  `Berechnungsgrundlage` und `Quellenreferenz` ausgegeben. `PARTIAL` bedeutet
  deshalb nicht, dass jede Zelle einer Arbeitsmappe gleichermassen betroffen
  ist.
- Die oeffentlich auffindbare EQUA-Dokumentation belegt nicht eindeutig, ob
  exportierte PRN-Leistungswerte Stuetzstellen oder Intervallmittelwerte
  sind. Erkannte Luecken und nicht eindeutige Reihen werden daher nicht
  integriert. Nicht belastbar ableitbare quantitative Energiewerte bleiben
  leer statt geschaetzt zu werden; leere Zellen sind nur gemeinsam mit
  Auswertungsstatus, Berechnungsgrundlage, Datenabdeckung und den
  Manifestdiagnosen zu interpretieren.
- Bis zu einer belegten und vom Nutzer bestaetigten Methodenentscheidung zur
  PRN-Zeit-, Perioden-, Leistungs- und Vorzeichenbedeutung sind quantitative
  PRN-Energieableitungen und daraus aggregierte Gebaeudeaussagen gesperrt.
  Deskriptive Last-, Temperatur- und Raumluftkennwerte werden dadurch nicht
  automatisch freigegeben oder gesperrt; ihre jeweilige Eignung bleibt am
  Auswertungsstatus und an der Berechnungsgrundlage ablesbar. Die fuenf
  verbleibenden Fachgates stehen in P036 und sind wie folgt gebuendelt:
  Gates 1 und 2 in CT-001, Gate 3 in CT-002 sowie Gates 4 und 5 in CT-003.
  CT-004 und CT-005 sind davon abhaengige, noch nicht freigegebene
  Folgearbeiten fuer Diagrammauswahl und 29Z-/5Z-Vergleich.
- Die erzeugten Tabellen sind kontrollierte Arbeitsstaende und noch kein
  zitierfaehiger Energie- oder Normnachweis.

Zur Begriffsklaerung: Die Anzeigeprojektion fasst wiederholte Zeitstempel nur
fuer eine lesbare Darstellung zusammen und veraendert die Quellreihe nicht.
`Zusammengesetzte Metadatenstrings` sind Textfelder, in denen mehrere
Identitaeten statt in getrennten strukturierten Feldern codiert sind. Die
Gebaeude-Systemgrenze legt fest, welche Zonen, Leistungen und Energiestroeme
in eine Gebaeudeaggregation eingehen. Das Diagramm-Q&A ist eine spaetere
Nutzerauswahl von Beispieldarstellungen und keine bereits freigegebene
Diagrammimplementierung.

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

- Im dokumentierten fokussierten P036-Prueflauf bestanden 201 Tests aus den
  Bereichen Datenvorbereitung, IDA-Import, Zonenmetadaten,
  Zonenkennwerttabellen, ALT-Vergleich, zeitgewichtete Kennwerte,
  Stage-2-/Stage-3-Vertraege, Prepare-Fassade, Workflow und UI.
  Ruff und `git diff --check` waren fuer diesen Umsetzungsscope sauber. Der
  Nachweis ist kein nachtraeglicher Vollsuite-Test des spaeteren
  Dokumentations-Releases 0.42.1.
- Der P036-Grundstand wurde im Commit `e573063` (`Release 0.40.0`) versioniert.
  Die spaetere Anzeigeprojektion fuer wiederholte IDA-Stuetzstellen wurde im
  Commit `9f58b57` (`Release 0.42.0`) ergaenzt. Beim ersten Handover-Entwurf
  war `5562b5d` (`Release 0.42.1`) der aktuelle Repository-HEAD. Dieses
  Release ergaenzte Planungs- und Referenzvergleichsdokumentation, aber keine
  weitere P036-Produktfunktion. Der Handover selbst wurde spaeter mit
  Commit `c6f7f5f` (`Release 0.42.2`) versioniert. Derselbe Commit nahm auch
  andere Dokumentationsslices auf; sie waren fachlich getrennt, nicht als
  getrennte Release-Commits veroeffentlicht.
- Der Navigator wurde nach der P036-Umsetzung und nach der ausdruecklichen
  Umsetzungsfreigabe am 2026-08-19 auf den damaligen Projekt- und
  Handover-Stand aktualisiert. Nach der TODO- und Handover-Praezisierung am
  2026-08-22 wurde der Hub erneut erfolgreich aktualisiert und mit
  `--validate-only` geprueft. Die fokussierten Dokumentations- und
  Architekturtests bestanden mit `19 passed`; `git diff --check` war sauber.

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

## Naechster gemeinsamer Einstieg

Die noch nicht umgesetzte P036-Arbeit wird in dieser Reihenfolge fortgesetzt:

1. CT-001 schliesst P036-Gates 1 und 2: IDA-Zeitstempel, letzte
   Periodengrenze, Warm-up und Leistungssemantik von `q_heat` und `q_cool`
   belegen sowie die Kuehlvorzeichen festlegen.
2. CT-002 schliesst P036-Gate 3: Den strukturierten Vertrag
   `ma_import_simulation -> ma_data_preparation` ohne zusammengesetzte
   Metadatenstrings schliessen.
3. CT-003 schliesst P036-Gates 4 und 5: Nettoflaeche, Zonenmultiplikator,
   Gebaeude-Systemgrenze, zeitgleichen Peak sowie Pflichtvariablen-,
   Perioden- und Zonenabdeckung bestaetigen.

`READY` darf fuer Masterarbeitsergebnisse erst vergeben werden, wenn CT-001
bis CT-003 geschlossen sind: Die fachlichen Methodenentscheidungen sind vom
Nutzer bestaetigt und in der Nutzerentscheidungsdatei sowie P036
dokumentiert, der strukturierte Importvertrag ist implementiert und getestet,
und der konkrete Datensatz erfuellt die danach festgelegten Abdeckungsregeln.

Erst danach koennen zwei getrennte Folgeauftraege beginnen: CT-004 bereitet
zwei bis drei Diagrammbeispiele je Fachthema fuer die Nutzerauswahl im Q&A
vor; CT-005 bindet den kontrollierten 29Z-/5Z-Laufzeit- und
Ergebnisvergleich an. Beide Punkte bleiben bis zu einem eigenen Auftrag und
einer eigenen Freigabe ausserhalb des aktuellen P036-Umfangs.

Der gemeinsame Einstieg liegt in CT-001 der TODO-Sammeluebersicht in
`PLAN_STATUS.md`. Das erwartete Ergebnis der ersten Arbeit ist eine belegte,
vom Nutzer bestaetigte Methodenentscheidung; bis dahin bleiben quantitative
PRN-Energieableitungen und daraus aggregierte Gebaeudeaussagen gesperrt.

## Repository-Grenze beim Handover

Beim ersten Entwurf enthielt der Arbeitsbaum bereits vorhandene, nicht aus
diesem P036-Chat stammende Aenderungen an `CHANGELOG.md`,
`docs/project/architecture/workflow/README.md`, zwei Workflow-HTML-Dateien
und der Ablage von `docs/ma_core/README.md`. Diese Aenderungen wurden nicht
als P036-Arbeit behandelt und spaeter getrennt mit Release 0.42.2
versioniert. `Getrennt` bezeichnet dabei nur den fachlichen Scope innerhalb
desselben Commits `c6f7f5f`, nicht einen eigenen Release-Commit. Die
weiterhin offene fachliche Ablageklaerung der
`ma_core`-README wird in P037 und CT-008 gefuehrt.
