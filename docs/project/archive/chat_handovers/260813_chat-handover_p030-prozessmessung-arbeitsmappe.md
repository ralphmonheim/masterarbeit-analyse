# Chat-Handover – P030 Prozessmessung: Arbeitsmappe und Quellenregister

Datum: 2026-08-13
Status: Arbeitsmappe und Erzeugungsskript erweitert; wissenschaftlicher Vergleich weiterhin offen
Arbeitsbereich: P030 `research_tools` Prozessmessung und Vergleichsauswertung

## Zweck und führende Quellen

Dieser historische Snapshot dokumentiert ausschliesslich den Ausbau der lokalen P030-Arbeitsmappe. Führend bleiben `docs/project/plans/inbox/260714_Plan_P030_research_tools_Prozessauswertung.md` und `docs/project/decisions/USER_DECISIONS_OPEN_POINTS.md` (OP-009). P030 ist die Forschungsschicht für Prozesszeiten; PreProcess umfasst die Vorbereitung bis zum Simulations-Setup, Kernprozess Export, Simulation und Ergebnisimport, PostProcess die anschliessende Auswertung.

## Erreichter Stand

In der Schwesterarbeitsablage liegt unter `04_Teil2_Prozessinnovation/Prozessmessung/Prozesskostenvergleich_Manuell_vs_Automatisiert.xlsx` eine editierbare Messvorlage. Die vier historischen Register `Manuell`, `Prozess automatisiert`, `Kosten` und `Vergleich` bleiben erhalten. Neu hinzugefügt sind neun Register: `00_Gesamtübersicht`, `01_PreProcess_Detail`, `02_PreProcess_Übersicht`, `03_Kernprozess_Übersicht`, `04_Kernprozess_Einzelwerte`, `05_PostProcess_Vorlage`, `06_Kosten`, `08_Messannahmen` und `09_Quellenregister`.

`Skripte/build_process_measurement_workbook.py` aktualisiert diese neun neuen Register, ohne die historischen Register zu löschen. Ausführung: `py Skripte/build_process_measurement_workbook.py`. In der aktuellen Umgebung wurde `openpyxl 3.1.5` verwendet; Blattstruktur, Summen, Kostenformeln, Quellenregister und Register-Verweise wurden danach automatisiert geprüft.

## Erfasste Fallwerte und Nachweise

Die aktuellen Simulationswerte sind manuell aus bereitgestellten IDA-ICE-Berichtsansichten eingetragene reine PC-Dauern. Sie stammen aus vier getrennten Berechnungsbereichen und werden je Variante addiert:

| Variante | Heizlast | Kühllast | Energie | Überhitzung | Summe |
| --- | ---: | ---: | ---: | ---: | ---: |
| 5Z-Dimensionierung | 24 s | 24 s | 294 s | 24 s | 366 s / 6:06 min |
| 29Z-Dimensionierung | 109 s | 117 s | 701 s | 118 s | 1.045 s / 17:25 min |

`5Z` und `29Z` bezeichnen Varianten mit fünf beziehungsweise 29 thermischen Zonen. Die Werte sind `manual_entry`-Maschinenzeiten, keine unabhängigen Wiederholungen und kein allgemeingültiger Leistungs-, Zeit- oder Kostenersparnisnachweis.

`09_Quellenregister` verknüpft jede relevante Zeile über Q-IDs: Q-001/Q-002 sind die 5Z-/29Z-Berichtsansichten, Q-003 die Nutzerangabe von 1–4 h aktiver Eingabe für eine neue Variante, Q-004 offene Messpunkte, Q-005 der PreProcess-Benchmark `BENCH-C278F4CF` mit `timings.csv`, Q-006 P030 als Methodikquelle und Q-007 ausschliessliche Kosten-Testwerte. 150 min ist nur ein gelb markierter Rechentest-Mittelwert der Q-003-Spanne. Kopierte Folgevarianten sind als „reduziert durch Kopie, noch nicht separat gemessen“ geführt.

## Methodische Grenze und führende offene Entscheidung

Der Kernprozess-Zielablauf ist `Export/Uebergabe -> Simulation -> Import/Standardisierung`; Prüfung/Korrektur wird nur bei tatsächlichem Anfall erfasst. Die PostProcess-Modulstruktur bleibt offen. Die Werte in `06_Kosten` für Stundensatz, Strompreis und PC-Leistung sind Testwerte, nicht zitierfähige Masterarbeitsannahmen.

OP-009 bleibt führend: Für vergleichbare Zeit- oder Kostenwirkungen sind gepaarte Durchläufe mit identischen Prozessgrenzen, Varianten-/Parameterumfang, Prüfanforderungen und Ergebnisartefakten erforderlich. Vorher fehlen Messmethode und Start-/Endpunkt der PC-Zeit, IDA-/Hardwareumgebung, Wiederholungsumfang, Behandlung von Wartezeit/Überlappung sowie ein objektives Kriterium für Prüfung/Korrektur. Die Vergleichbarkeit ist daher „noch nicht gegeben“.

## Git- und Arbeitsstand

Branch: `main`; letzter Commit bei Erstellung: `1169fc0` (`Release 0.39.0`). Das P030-Skript sowie die P030-/OP-009- und Handover-Dokumentation sind uncommittete Arbeitsänderungen. Daneben existieren zahlreiche fremde uncommittete Änderungen; sie wurden nicht verändert. Die Arbeitsmappe liegt ausserhalb des Repositories und wird nicht versioniert. Kein Commit, Tag oder Push wurde ausgeführt.
