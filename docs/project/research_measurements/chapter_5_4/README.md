# Kapitel 5.4 – Prozesszeiten und Automatisierungsstand

**Messstand:** 2026-09-06  
**Softwarestand:** Commit `d45bd4783c97af6d65eb8645c4273fba2f010598` (`d45bd47`, v0.42.5)  
**Rohdaten:** [`BENCH-CH5-4-V0425.json`](BENCH-CH5-4-V0425.json)  
**Plot-Rohdaten:** [`BENCH-CH5-4-PLOTS-V0425.json`](BENCH-CH5-4-PLOTS-V0425.json)  
**Runner:** [`Skripte/benchmark_chapter_5_4.py`](../../../../Skripte/benchmark_chapter_5_4.py)

## A. Aktueller Automatisierungsstand

| Prozess | Technischer Stand am Messcommit | Beleg |
| --- | --- | --- |
| Ausgangsmodell / Dimensionierung | Die vereinfachte LoD-1-Referenzdimensionierung wird innerhalb des SmallOffice-V1-PreProcess ausgeführt. Sie ersetzt weder Gebäudeimport noch die fachliche IDA-Modellerstellung. | `src/ma_workflow/small_office_v1_preprocess.py`, Schritt `dimensioning` |
| Optimierungsvarianten | 30 gekoppelte Optimierungsfälle werden erzeugt und zu Draft-Setup-Paketen materialisiert. | `build_small_office_v1_optimization_cases`, `_simulation_setup_action` |
| Sensitivitätsvarianten | Acht Wetter-/Belegungs-Sensitivitätsfälle werden erzeugt und als Draft-Pakete materialisiert. | `build_small_office_v1_sensitivity_cases`, `_simulation_setup_action` |
| Nachweisführung | Keine automatisierte Nachweisführung: Stage 3 validiert nur externe Profilkonfigurationen und ist fachlich `NOT_EVALUABLE`. | `src/ma_analyse/stage_3_standards_verification/services.py` |
| IDA-ICE-Übergabe / Modelländerung / Start | Nicht automatisiert. Setup-Pakete enthalten nur neutrale Eingaben; IDA ICE bleibt ein manueller Prozessschritt. | `docs/ma_simulation_setup/README.md`, `docs/ma_export_simulation/README.md` |
| Ergebnisimport | IDA-Adapter lesen explizit referenzierte `.prn`, `.html`/`.htm` und `.xlsx`; `.idm`/`.idc` werden nicht inhaltlich gelesen. | `src/ma_import_simulation/adapters/ida_ice/results.py` |
| Aufbereitung, Kennwerte, Excel | Vorhanden, aber im Messstand nicht benchmarkbar, weil keine vollständige versionierte IDA-Ergebnisbasis vorliegt. | `src/ma_analyse/preprocessing/prepare.py`, `src/ma_analyse/analysis/excel.py` |
| Diagramme | Jahres- und Vergleichsdarstellungen sind technisch vorhanden. `heating-year` wurde auf reproduzierbarer Testbasis gemessen; produktionsnahe Kapitel-4-Ergebnisdaten bleiben nicht verfügbar. | `src/ma_analyse/analysis/templates/heating_year.py` |

Die in diesem Ordner gemessene Prozessgrenze ist ausdrücklich: Aufruf von
`run_small_office_v1_preprocess` bis zu materialisierten **Draft**-Simulation-Setup-Paketen.
Sie umfasst weder IDA-Export, noch IDA-Simulation oder Ergebnisimport.

## B. Vorhandene historische Benchmarks

| Messwert | Prozessgrenze | Umfang | Zeit | Klassifikation | Verwendbarkeit |
| --- | --- | ---: | ---: | --- | --- |
| `BENCH-C278F4CF` | Workspace anlegen | nicht näher dokumentiert | 0,024139 s | aus bestehendem Log übernommen | eingeschränkt: Einzelwert, Hardware/Wiederholungen fehlen |
| `BENCH-C278F4CF` | PreProcess bis 38 Pakete | 30 Optimierung + 8 Sensitivität | 1,261857 s | aus bestehendem Log übernommen | eingeschränkt: Einzelwert, keine Skalierungsreihe |
| 5Z-Dimensionierung | vier IDA-ICE-Fachläufe: Heizlast, Kühllast, Energie, Überhitzung | 5 Zonen | 366 s | gemessen, manuell aus IDA-Berichten übertragen | nur exemplarische IDA-Systemzeit; keine Wiederholung |
| 29Z-Dimensionierung | dieselben vier IDA-ICE-Fachläufe | 29 Zonen | 1.045 s | gemessen, manuell aus IDA-Berichten übertragen | nur exemplarische IDA-Systemzeit; nicht mit 5Z mitteln |

Die historischen Messwerte stammen aus dem P030-Messstand und dem versionierten
Erzeugungsskript `Skripte/build_process_measurement_workbook.py`. Sie werden
nicht in Sekunden je Variante umgerechnet: Die Prozessgrenzen, Wiederholungen
und Skalierung sind dafür nicht ausreichend belegt.

## C. Neue Messung: SmallOffice-V1-PreProcess

Der Runner führte einen separaten Cold Start und danach zehn Warm-Wiederholungen
durch. Er nutzte den vorhandenen fünfzonigen V1-Workflow mit 30 Optimierungs-
und acht Sensitivitätspaketen. Die Rohwerte, Python-Version und Plattform stehen
vollständig in der JSON-Datei. Plattform: Windows 11, Python 3.14.0; CPU-Modell
und sonstige Hardwaremerkmale wurden nicht automatisch erhoben.

| Teilprozess | n | Mittelwert [s] | Median [s] | Min [s] | Max [s] | Standardabw. [s] | Klassifikation |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| PreProcess gesamt, warm | 10 | 1,715910 | 1,756374 | 1,378093 | 2,009330 | 0,196856 | gemessen |
| Variantenerzeugung (Schritt `variants`) | 10 | 0,073672 | 0,071438 | 0,060521 | 0,088295 | 0,009593 | gemessen |
| Materialisierung Simulation-Setup (Schritt `simulation_setup`) | 10 | 1,170014 | 1,149832 | 0,931787 | 1,415743 | 0,141429 | gemessen |
| Cold Start: Worker-Prozessgrenze | 1 | 2,148409 | — | — | — | — | gemessen |
| Cold Start: gestarteter Prozess gesamt (inkl. Python-Start/Import) | 1 | 7,605141 | — | — | — | — | gemessen |

Die Streuung des warmen Gesamtwerts beträgt rund 11,5 % des Mittelwerts. Sie
wird ohne weitere Messreihe nicht bereinigt; insbesondere Dateisystem- und
Interpretereffekte bleiben enthalten. Cold Start und Warm-Messung sind getrennte
Messarten und dürfen nicht zusammengefasst werden.

### Einzelwerte der Warm-Wiederholungen

| Wiederholung | Gesamt [s] | Varianten [s] | Setup-Materialisierung [s] |
| ---: | ---: | ---: | ---: |
| 1 | 1,804060 | 0,078627 | 1,286983 |
| 2 | 1,861797 | 0,088295 | 1,170342 |
| 3 | 1,854480 | 0,074236 | 1,316841 |
| 4 | 1,604111 | 0,068641 | 1,138134 |
| 5 | 1,479603 | 0,065517 | 1,015846 |
| 6 | 1,378093 | 0,060521 | 0,931787 |
| 7 | 2,009330 | 0,067980 | 1,415743 |
| 8 | 1,855047 | 0,083617 | 1,150157 |
| 9 | 1,708687 | 0,084430 | 1,149506 |
| 10 | 1,603892 | 0,064857 | 1,124796 |

## D. Variantengenerierung und Skalierung

| Paketanzahl | Messstatus | Begründung |
| ---: | --- | --- |
| 1, 5, 10, 25 | nicht gemessen | Der aktuelle V1-Workflow besitzt dafür keinen fachlich definierten Teilfall. |
| 38 | gemessen | Vollständiger, vorhandener SmallOffice-V1-Workflow. |
| 50, 100 | nicht gemessen | Keine künstliche Variantenduplizierung; das wäre kein bestehender Workflowfall. |

Damit stützt der Messstand kein lineares Modell für `T_Generierung(n)`.
Die Messung belegt nur `T_Generierung(38)` innerhalb eines Gesamt-PreProcess;
eine Division durch 38 wäre lediglich eine rechnerische Hilfsgröße und wird
nicht als Kennzahl für Kapitel 5.4 verwendet.

Für die manuelle Arbeitsannahme bleibt dagegen transparent:

`T_manuell(n) = T_Setup + n × 30 min` für zusätzliche Optimierungs- oder
Sensitivitätsvarianten. Die Werte für 1/5/10/25/50/100 Varianten (30/150/300/
750/1.500/3.000 min) sind **rechnerisch hochgerechnet**, nicht gemessen.

## E. Nachweisführung und IDA ICE

Nachweisführung ist kein automatisierter Benchmarkfall. Der aktuelle Stage-3-
Code kann ein extern vorgegebenes Profil technisch prüfen, besitzt aber weder
freigegebene fachliche Regelwerte noch einen produktiven PASS/FAIL-Nachweis.

IDA-ICE-Modellerzeugung, Modelländerung, Übergabe und Simulationsstart wurden
nicht ausgelöst. Die oben genannten 366 s (5Z) und 1.045 s (29Z) werden
ausschließlich als getrennte historische IDA-Systemzeiten geführt. Sie sind
keine eingesparte Personenzeit und kein Solver-Geschwindigkeitsnachweis.

## F. Datenaufbereitung

Die Funktionen existieren, wurden aber nicht mit einer geeigneten,
versionierten vollständigen Ergebnisbasis gemessen. Deshalb fehlen bewusst
Messwerte für Ergebnisimport, Datenprüfung, Zeitreihenzusammenführung,
Kennwertberechnung und Excel-Ausgabe. Das Fehlen ist kein Funktionsdefizit
und wird nicht durch synthetisch hochskalierte Zeitwerte ersetzt.

Für eine spätere Erweiterung muss ein freigegebenes, reproduzierbares
Ergebnisdatenpaket mit Varianten-, Raum-, Zeitreihen- und Ausgabedefinition
bereitgestellt werden. Erst dann kann derselbe Runner um reine Aufrufe der
bereits vorhandenen Funktionen erweitert werden.

## G. Diagrammerzeugung

Gemessen wurde ausschließlich der vorhandene Aufruf
`build_heating_year_template`: von unmittelbar nutzbaren, bereits
aufbereiteten CSV-Dateien bis zur vollständig gespeicherten PNG-Datei.
CSV-Lesen und kleine unmittelbar plotbezogene Transformationen innerhalb der
Plotfunktion sind enthalten. Nicht enthalten sind IDA ICE, Ergebnisimport,
PRN-Parsing, Datenaufbereitung, Variantengenerierung, Simulation-Setup,
manuelle Auswahl und Interpretation.

Die Testbasis entspricht der bestehenden Struktur aus
`tests/test_plot_templates.py`: synthetische, aufbereitete Heizzeitreihen mit
1.200 Zeitpunkten je Datenreihe. Das Template heißt zwar `heating-year`, die
Zeitreihe deckt aber **kein vollständiges Jahr** ab und enthält keine
Kapitel-4-Realwerte. Die Messung belegt deshalb die Plot-Ausführung auf einer
reproduzierbaren Testbasis, nicht die Laufzeit eines realen Jahresdatensatzes.

| Diagrammtyp | Umfang | Wiederholungen | Mittelwert [s] | Median [s] | Min [s] | Max [s] | Standardabw. [s] | Messstatus |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `heating-year`, Einzelplot | 1 Variante, 1 Raum/Zone, 1 Datenreihe à 1.200 Punkte, PNG | 10 warm | 0,567662 | 0,543761 | 0,480899 | 0,711566 | 0,076935 | gemessen auf reproduzierbarer Testbasis |
| `heating-year`, Variantenvergleich | 2 Varianten, 1 Raum/Zone, 2 Datenreihen à 1.200 Punkte, PNG | 10 warm | 0,552689 | 0,545658 | 0,513088 | 0,655219 | 0,042310 | gemessen auf reproduzierbarer Testbasis |

| Diagrammtyp | manuelle Arbeitsannahme | Softwaremessung | Vergleichbarkeit |
| --- | ---: | ---: | --- |
| Jahresdiagramm | ca. 3–5 min | 0,567662 s warm; Cold-Worker 0,970255 s | Nur technische Plotzeit auf Testbasis; manuelle Erstellung enthält wahrscheinlich Auswahl, Prüfung und Interpretation. |
| Variantenvergleich | ca. 5 min je zusätzlich einzubeziehender Variante | 0,552689 s warm für 2 Varianten; Cold-Worker 0,673927 s | Keine lineare Skalierung ableitbar; Testdaten und Prozessgrenzen sind nicht identisch. |

Die gestartete Python-Prozesszeit einschließlich Interpreter- und Modulstart
lag beim Cold Start bei 6,094252 s (Einzelplot) beziehungsweise 5,173171 s
(Vergleich). Sie wird getrennt ausgewiesen und nicht der reinen Plotzeit
zugeschlagen. Die zehn Einzelwerte je Fall stehen in
`BENCH-CH5-4-PLOTS-V0425.json`.

## H. Prozessmatrix manuell – Software

| Prozess | manuelle Personenzeit | Software-Personenzeit | Software-Systemzeit | IDA-Systemzeit | Durchlaufzeit | Automatisierungsgrad |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| Ausgangsmodell / Dimensionierung | ca. 60 min (retrospektiv manuell geschätzt) | nicht gemessen; Start/Konfiguration nötig | nicht gemessen | separat historisch: 366 s (5Z) bzw. 1.045 s (29Z) | nicht vergleichbar | teilweise softwareunterstützt; IDA manuell |
| 5 Optimierungsvarianten | ca. 150 min (rechnerisch aus 5 × 30 min) | nicht gemessen; Start/Konfiguration nötig | 0,073672 s nur für den 38-Paket-Gesamtschritt, nicht übertragbar | nicht gemessen | nicht vergleichbar | Varianten und Draft-Setups automatisiert |
| 5 Sensitivitätsvarianten | ca. 150 min (rechnerisch aus 5 × 30 min) | nicht gemessen; Start/Konfiguration nötig | siehe Optimierung | nicht gemessen | nicht vergleichbar | Varianten und Draft-Setups automatisiert |
| Vollständiger V1-PreProcess | keine vergleichbare Messung | nicht gemessen; Start/Konfiguration nötig | 1,715910 s warm für 38 Pakete | 0 s im Benchmark | 1,715910 s warm | automatisiert bis Draft-Setup |
| Nachweisführung | keine belastbare manuelle Vergleichsmessung | nicht messbar | nicht messbar | nicht gemessen | nicht vergleichbar | nicht automatisiert (`NOT_EVALUABLE`) |
| Diagramme: `heating-year` | Jahresdiagramm 3–5 min bzw. Vergleich 5 min je Variante (retrospektiv manuell geschätzt) | nicht gemessen | 0,567662 s (Einzelplot) bzw. 0,552689 s (2-Variantenvergleich), jeweils warm | 0 s | reine Plotgrenze, nicht mit manueller Gesamtarbeit vergleichbar | automatisiert, auf Testbasis gemessen |

## I. Direkt verwendbare Messwerte für Kapitel 5.4

| Wert | Zeit | Verwendung | Klassifikation |
| --- | ---: | --- | --- |
| Historischer Workspace-Aufbau | 0,024139 s | Kontextwert, nicht hochrechnen | aus bestehendem Log übernommen |
| Historischer PreProcess, 38 Pakete | 1,261857 s | historischer Vergleichswert mit derselben Paketmenge | aus bestehendem Log übernommen |
| Neuer PreProcess, 38 Pakete, warm | 1,715910 s ± 0,196856 s | Hauptwert der neuen Softwaremessung | gemessen |
| Neue Variantenerzeugung, 38-Paket-Workflow | 0,073672 s ± 0,009593 s | Teilzeit, nicht auf Einzelvariante normieren | gemessen |
| Neue Setup-Materialisierung, 38 Pakete | 1,170014 s ± 0,141429 s | Teilzeit, nicht auf Einzelvariante normieren | gemessen |
| `heating-year`, Einzelplot, 1 × 1.200 Punkte | 0,567662 s ± 0,076935 s | reine Plotzeit bis PNG | gemessen auf reproduzierbarer Testbasis |
| `heating-year`, Vergleich, 2 × 1.200 Punkte | 0,552689 s ± 0,042310 s | reine Plotzeit bis PNG | gemessen auf reproduzierbarer Testbasis |
| Cold Start, Worker | 2,148409 s | separat berichten | gemessen |
| Cold Start, Prozess gesamt | 7,605141 s | Start-/Import-Overhead separat berichten | gemessen |
| IDA-ICE 5Z | 366 s | ausschließlich getrennte IDA-Systemzeit | gemessen, manuell übertragen |
| IDA-ICE 29Z | 1.045 s | ausschließlich getrennte IDA-Systemzeit | gemessen, manuell übertragen |
| Manuelle zusätzliche Variante | 30 min | Arbeitsannahme für Szenariorechnung | retrospektiv manuell geschätzt |

## J. Einschränkungen

- Die neue Messung betrifft einen Windows-11-/Python-3.14-Lauf auf unbekanntem
  CPU- und Dateisystemprofil. Sie ist keine allgemeine Performancegarantie.
- Es gibt nur einen fachlich vorhandenen 38-Paket-Fall; keine gemessene
  Skalierungskurve und keine belastbare Sekunde-je-Variante-Kennzahl.
- Der historische Benchmark und die neue Messung haben ähnliche, aber nicht
  vollständig dokumentiert identische Umgebungen. Sie werden nicht als
  Leistungssteigerung interpretiert.
- Manuelle Zeiten sind Arbeitsannahmen, nicht kontrollierte Messungen.
- IDA-Zeiten sind externe Einzelbeobachtungen und nicht Teil der gemessenen
  Softwarezeit. Personen-, Maschinen- und Durchlaufzeit werden nicht addiert,
  wenn sich Aktivitäten überlappen könnten.
- Die Plotzeit bezieht sich auf zwei vorhandene, synthetische Testfälle mit
  1.200 Punkten je Reihe. Sie ist nicht auf ein vollständiges Jahresprofil,
  andere Hardware oder größere Variantensätze übertragbar.
- Keine Zeitersparnis in Prozent wird ausgewiesen, weil manuelle und
  softwaregestützte Prozessgrenzen nicht identisch gemessen wurden.
