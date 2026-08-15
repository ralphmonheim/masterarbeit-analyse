# Unabhaengiger Umsetzungsplan: Kontrollierter 29Z-5Z-Referenzvergleich

Datum: 260815  
Status: Sol-geplant und qualitaetsgeprueft; noch nicht zur Umsetzung freigegeben

## Arbeits-Prompt

Rolle und Kontext:

Als Senior-Python-Entwickler und technischer Architekturberater wird ein begrenzter 29Z-/5Z-Vergleich für das Referenzfallkapitel der Masterarbeit vorbereitet. Der Vergleich ist kein neuer Hauptuntersuchungs- oder Optimierungsstrang. Das 5Z-Modell bleibt der fachliche Hauptaufbau für die spätere Optimierung.

Ziel und erwartetes Ergebnis:

Der Vergleich soll nachvollziehbar begründen,

- weshalb das 5Z-Modell wegen des geringeren Rechen- und Datenumfangs für die Optimierung eingesetzt wird;
- welche groben Auswirkungen die Reduktion von 29 auf 5 thermische Zonen auf Gebäudeebene haben kann;
- welche verfügbaren fachlichen Ergebniskennwerte tatsächlich vergleichbar sind;
- welche Aussagen wegen unterschiedlicher Simulations- oder Ausgabeeinstellungen nur explorativ oder nicht auswertbar bleiben.

Der Arbeitsstand soll umfassen:

- einen Vergleich der dokumentierten Simulationszeiten;
- den Ausgabeumfang anhand der PRN-Dateianzahl;
- ergänzend Dateigröße, Datenzeilen, Zeitraster und verfügbare Variablen, damit eine geänderte Ausgabeauflösung messbar wird;
- eine Inventarisierung aller verfügbaren Ergebniskennwerte;
- eine kompakte Vergleichsarbeitsmappe;
- eine erste Prozessabbildung zu Laufzeit und Ausgabeumfang;
- eine Kandidatenliste für eine spätere fachliche Ergebnistabelle und höchstens ein weiteres Ergebnisdiagramm;
- eine knappe methodische Einordnung für das Referenzfallkapitel.

Scope:

- `data/ma_analyse/ida_imports` bleibt der führende fachliche Importordner.
- Die fünf aktiven Fälle bleiben unverändert unter `data/ma_analyse/ida_imports/Vergleich der Referenz/`:
  - 29Z;
  - 29Z, weniger Simulation;
  - 29Z, weniger Simulation plus geänderte Ausgabeauflösung;
  - 5Z;
  - 5Z, weniger Simulation.
- „Weniger Simulation“ bezeichnet ausschließlich die Reduktion der in IDA berechneten beziehungsweise ausgegebenen Themen. Dieser Faktor wird nicht mit der Zonenzahl oder Ausgabeauflösung gleichgesetzt. :codex-annotation{index="2"}
- „Zeitschritt“ bezeichnet hier die Auflösung der ausgegebenen Simulationsdaten. Der IDA-Wert `0.0` ist als Standardmodus und nicht als numerischer Zeitschritt von null Stunden zu behandeln. Es wird ein reproduzierbarer manueller Testentwurf vorgesehen, mit dem geprüft werden kann, ob Daten- und Zeitersparnisse bereits in IDA statt erst in `prepare` entstehen. Codex startet keine IDA-Simulation automatisch. :codex-annotation{index="1"}
- 5Z und 29Z werden grob auf Gebäudeebene verglichen. Eine detaillierte Zuordnung der 29 Räume zu den fünf Sammelzonen ist nicht Teil des Auftrags.
- Die PRN-Dateianzahl wird als eigener Kennwert `Ausgabeumfang` geführt. Sie ist kein Qualitäts- oder Genauigkeitsmaß.
- Ausschließlich `data/ma_analyse/ida_imports/ALT` wird unverändert nach `data/ma_analyse/reference_cases/ALT` verschoben.
- ALT bleibt historische lokale Referenz- und Testbasis und darf von `prepare` standardmäßig nicht verarbeitet werden.
- IDM- und IDC-Dateien dürfen beim ALT-Umzug verschoben und ausschließlich über Dateimetadaten verifiziert, aber nicht inhaltlich geöffnet, gehasht oder verarbeitet werden.
- Bestehende öffentliche APIs und Befehle bleiben kompatibel.

Nicht-Ziele:

- keine Verschiebung oder Umbenennung der fünf aktiven Referenz-Runs;
- keine neuen oder automatischen IDA-Simulationen;
- keine detaillierte Raum-zu-Zone-Zuordnung;
- keine inhaltliche Verarbeitung von IDM/IDC;
- keine automatische Norm-, Kosten-, Nachhaltigkeits- oder Gesamtbewertung;
- keine automatische Wahl „besserer“ Simulations- oder Ausgabeeinstellungen;
- keine Vermischung von ALT und Referenzvergleich;
- keine neue Dependency, externe API, Cloud-Verarbeitung, Installation, Veröffentlichung, Commit oder Push;
- keine abschließende fachliche Auswahl der Ergebniskennwerte ohne Sichtung des Inventars;
- keine Streamlit- oder Tkinter-Erweiterung.

Bekannte Eingaben, Annahmen und Grenzen:

- IDA ICE 5.1.0;
- Time-Split-Parallelisierung aktiv;
- dokumentierte Laufzeiten in der Reihenfolge Heizlast, Kühllast, Energie und Überhitzung:
  - 29Z: 107 / 121 / 926 / 118 s;
  - 29Z, weniger Simulation: 133 / 145 / 942 / 106 s;
  - 29Z, weniger Simulation plus Ausgabeauflösung: 178 / 212 / 1082 / 215 s;
  - 5Z: 24 / 24 / 294 / 24 s;
  - 5Z, weniger Simulation: 44 / 53 / 532 / 52 s;
- beobachtete PRN-Anzahlen in derselben Fallreihenfolge: 917 / 596 / 596 / 184 / 116;
- die Laufzeiten sind manuell bereitgestellte Prozessdaten und dürfen nicht aus Datei- oder Simulationszeitstempeln rekonstruiert werden;
- die vorhandenen Einzelmessungen zeigen keine belastbare Laufzeitersparnis durch „weniger Simulation“ oder die geänderte Ausgabeauflösung. Kausale Aussagen benötigen kontrollierte Wiederholungsmessungen;
- gleiche PRN-Anzahl bedeutet nicht gleiche Ausgabeauflösung. Dafür müssen mindestens Datenzeilen, Dateigröße und tatsächliche Zeitabstände geprüft werden;
- PRN-Dateien sind zulässige Ergebnisartefakte;
- Einheiten, Zeitraster, Variablensemantik, Zonenabdeckung und Systemgrenze werden vor fachlichen Kennwertvergleichen geprüft;
- nicht belegte oder nicht eindeutig vergleichbare Kennwerte bleiben sichtbar `nicht auswertbar`;
- die finalen fachlichen Ergebniskennwerte und das Ergebnisdiagramm werden erst nach Sichtung des Inventars ausgewählt.

Prüf- und Dokumentationsanforderungen:

- explizite, kataloggebundene Discovery statt eines breiten Verzeichnisscans;
- fünf getrennte Run- und Variantenidentitäten;
- keine Paket-, Serien- oder Dateinamenskollisionen;
- ALT standardmäßig ausgeschlossen;
- geschützte IDM-/IDC-Inhalte bleiben ungelesen;
- Tests für Discovery, Pfadgrenzen, ALT-Ausschluss, Kollisionsfreiheit, Metadatenvalidierung, Zeitraster, Einheitenstatus und Vergleichbarkeit;
- bestehende CLI-, Service- und Prepare-Verträge bleiben regressionsfrei;
- sicherer ALT-Umzug mit Vorprüfung, Nachprüfung und umkehrbarem Rückfallweg;
- bestehende Modul- und Entscheidungsdokumentation knapp aktualisieren;
- jede Umsetzung beginnt erst nach der ausdrücklichen Formulierung `Freigabe zur Umsetzung`.

## Ziel

Es wird ein kleiner, reproduzierbarer Referenzvergleich-Slice umgesetzt, der die fünf bereits korrekt abgelegten IDA-Ergebnisfälle eindeutig entdeckt, getrennt vorbereitet und als methodisch kontrolliertes Vergleichspaket ausgibt.

Der Slice trennt vier Aussageebenen:

1. Zonierungswirkung: 29Z gegenüber 5Z nur bei bestätigten gleichen übrigen Einstellungen.
2. Berechnungsumfang: vollständig gegenüber „weniger Simulation“ innerhalb derselben Zonierung.
3. Ausgabeauflösung: gleicher Berechnungsumfang mit unterschiedlichem IDA-Ausgabemodus.
4. PostProcess-Aufwand: Rohdatenumfang und spätere `prepare`-Verarbeitung, getrennt von der IDA-Rechenzeit.

Erfolg liegt vor, wenn die fünf Fälle kollisionsfrei vorbereitet werden, ALT ausgeschlossen bleibt, die vorhandenen Laufzeiten und Datenumfänge reproduzierbar inventarisiert werden und jede fachliche Vergleichszeile einen eindeutigen Status `vergleichbar`, `explorativ`, `nicht auswertbar` oder `Metadatenbestätigung ausstehend` erhält.

## Scope und Nicht-Ziele

Der Umsetzungsscope umfasst:

- den unveränderten Erhalt der fünf aktiven Run-Verzeichnisse unter `ida_imports/Vergleich der Referenz`;
- die Trennung des historischen ALT-Bestands vom aktiven Importordner;
- einen kleinen versionierten Metadatenvertrag für die fünf Runs;
- explizite PRN-Discovery innerhalb der fünf freigegebenen Run-Wurzeln;
- run-sichere Vorbereitung und ein Run-Inventar;
- einen begrenzten Analyse-Service mit additivem CLI-Einstieg `reference-compare`;
- XLSX-/CSV-Ausgaben für Laufzeiten, Ausgabeumfang, Kennwertinventar, Vergleichbarkeit und auswertbare Gebäudekennwerte;
- eine vorläufige Prozessabbildung für Laufzeit und Datenumfang;
- einen manuellen Testentwurf für Berechnungsumfang und Ausgabeauflösung;
- gezielte Tests und knappe Dokumentationsanpassungen.

Nicht Teil dieses Slices sind:

- Änderungen an Namen, Inhalt oder Ablage der fünf aktiven Referenz-Runs;
- eine Änderung der fachlichen Optimierungslogik;
- eine Erweiterung der Streamlit- oder Tkinter-Oberfläche;
- ein automatischer IDA-Aufruf;
- eine neue Raumaggregation oder 29Z-zu-5Z-Mappinglogik;
- die Aktivierung bislang offener IDA-Semantik-, Norm- oder Flächengates aus P036;
- eine finale Auswahl oder Interpretation fachlicher Ergebniskennwerte ohne Nutzersichtung;
- die automatische Einordnung dieses unabhängigen Plans in P029, P036, `PLAN_INDEX.md` oder `PLAN_STATUS.md`.

## Betroffene Bereiche

### Qualitätsbefunde vor der Umsetzung

- **Blocker – Aktive Referenzstruktur wird derzeit nicht entdeckt:** `discover_known_ida_prn()` kennt nur die beiden direkten Modellordner und ALT (`src/ma_data_preparation/ida_ice.py:93`). Die fünf aktiven Runs unter `ida_imports/Vergleich der Referenz` werden damit nicht als getrennte Vergleichsfälle erkannt.

- **Blocker – Nach dem ALT-Umzug droht der Legacy-Fallback:** Solange ALT unter `ida_imports` liegt, kann es als bekannte Quelle erkannt werden, während der aktive Vergleich unberücksichtigt bleibt. Nach seinem Umzug könnte die aktuelle Discovery keine bekannten Quellen mehr finden. `run_prepare()` würde dann auf `process_all_variants()` wechseln (`src/ma_analyse/app/commands.py:140`). Bei vorhandenem Referenzvergleich muss die neue Discovery deshalb fail-closed arbeiten und darf nicht auf den Legacy-Pfad zurückfallen.

- **Blocker – Run-Kollisionen bei einer naiven Discovery-Erweiterung:** `_series_id()` und `_package_id()` verwenden den vorhandenen `run_id` nicht als Identitätsbestandteil (`src/ma_data_preparation/ida_ice.py:171` und `src/ma_data_preparation/ida_ice.py:183`). Gleich benannte PRNs aus mehreren 5Z- oder 29Z-Runs könnten Prepared-Pakete überschreiben oder beim Resume irrtümlich wiederverwendet werden.

- **Blocker – Bestehende fachliche Tabelle vermischt mehrere Runs derselben Kohorte:** `build_model_zone_tables()` filtert nur nach `cohort` und `result_kind` (`src/ma_analyse/analysis/master_thesis_dataset.py:32`). `_zone_values()` hält je Metrik nur eine Serie, sodass spätere gleichnamige Reihen vorherige still ersetzen (`src/ma_analyse/analysis/master_thesis_dataset.py:91`). Der neue Vergleich darf diese Funktion nicht ohne expliziten Run-Selektor verwenden.

- **Wichtig – ALT ist derzeit standardmäßig aktiv:** `prepare_known_ida_results()` besitzt `("5Z", "29Z", "ALT")` als Default (`src/ma_data_preparation/ida_ice.py:129`), und `run_prepare()` schränkt ihn nicht ein. Das widerspricht der neuen Datenrolle von ALT.

- **Wichtig – PRN-Anzahl misst keine Ausgabeauflösung:** Die beiden 29Z-Fälle „weniger Simulation“ besitzen jeweils 596 PRNs, obwohl die Ausgabeauflösung abweichen soll. Für diesen Faktor sind Gesamtzeilen, Zeitabstandverteilung und Dateigröße erforderlich. `parse_prn_file()` erhält die variable Zeitspalte bereits unverändert (`src/ma_import_simulation/adapters/ida_ice/results.py:163`).

- **Wichtig – `0.0` darf nicht als Intervallwert interpretiert werden:** Der Wert bezeichnet laut Nutzer den IDA-Standardmodus. Der Metadatenvertrag muss Modus und gegebenenfalls bestätigtes effektives Intervall trennen.

- **Wichtig – aktuelle Laufzeiten sind explorativ:** Bei 29Z ist „weniger Simulation“ in Summe langsamer als der volle Lauf; dasselbe gilt für 5Z. Auch der Fall mit geänderter Ausgabeauflösung ist langsamer als „weniger Simulation“. Eine einzelne Messung darf deshalb nur die beobachtete Dauer, nicht die Ursache oder erwartete Einsparung belegen.

- **Wichtig – offene Fachgates bleiben bestehen:** Unbekannte Einheiten werden aktuell als `unverified` geführt, und PRN-Reihen werden zunächst als momentane Werte behandelt (`src/ma_data_preparation/ida_ice.py:43` und `src/ma_data_preparation/ida_ice.py:54`). P036 sperrt quantitative Energie- und Gebäudekennwerte bis zur Bestätigung von Zeit-, Leistungs-, Vorzeichen-, Flächen- und Abdeckungssemantik.

- **Wichtig – Git-Arbeitsstand ist bereits verändert:** Unter anderem `CHANGELOG.md` und die zentrale Nutzerentscheidungsdatei besitzen fremde Änderungen. Eine spätere Umsetzung muss vor jeder überlappenden Dokumentationsänderung den aktuellen Diff prüfen und ausschließlich ergänzend patchen.

- **Optional – Bedienoberflächen:** Ein Streamlit- oder Tkinter-Ausbau würde den begrenzten Referenzvergleich unnötig mit P029-UI-Arbeiten koppeln und bleibt ausgeschlossen.

### Dateien und Module

Voraussichtlich betroffen:

- `config/ma_analyse/reference_comparison.json`
  - neuer Run-, Faktor- und Laufzeitvertrag;
- `src/ma_data_preparation/ida_ice.py`
  - kataloggebundene Discovery, Run-Identität, ALT-Ausschluss und Run-Inventar;
- `src/ma_analyse/app/commands.py`
  - fail-closed `prepare`-Delegation und begrenzter Vergleichs-Runner;
- `src/ma_analyse/app/cli.py`
  - additiver Befehl `reference-compare`;
- `src/ma_analyse/analysis/reference_case_comparison.py`
  - neuer Vergleichsservice;
- `tests/test_ma_data_preparation_ida.py`;
- `tests/test_ma_analyse_prepare_owner.py`;
- `tests/test_ma_analyse_commands.py`;
- neue gezielte Tests für den Referenzvergleich;
- `docs/ma_analyse/README.md`;
- `docs/ma_analyse/data_preparation/README.md`;
- `docs/ma_import_simulation/README.md`;
- `docs/project/decisions/USER_DECISIONS_MASTERTHESIS_CODE.md`;
- `CHANGELOG.md`.

Unveränderte aktive Datenstruktur:

- `data/ma_analyse/ida_imports/Vergleich der Referenz/<fünf aktive Runs>`.

Einzige lokale Datenbewegung:

- `data/ma_analyse/ida_imports/ALT`
  nach
  `data/ma_analyse/reference_cases/ALT`.

P029 bleibt für den UI-neutralen Service- und Runner-Vertrag maßgeblich. UD-126 bleibt für Ownergrenzen und den 5Z-Hauptfokus gültig; seine Aussage zum kurzen 29Z-Vergleich wird durch eine neue Entscheidung nur dahingehend präzisiert, dass ein begrenzter Bestätigungs- und Auswirkungsvergleich vorgesehen ist.

## Umsetzungsschritte

1. **Preflight und Schutz des vorhandenen Arbeitsstands**

   - Aktuellen `git status --short` und die Diffs aller später berührten versionierten Dateien lesen.
   - Fremde Änderungen markieren und nicht zurücksetzen oder überschreiben.
   - Bestätigen, dass `data/ma_analyse/ida_imports/Vergleich der Referenz` existiert und genau die fünf vereinbarten Run-Verzeichnisse enthält.
   - Die fünf aktiven Run-Verzeichnisse ausschließlich read-only inventarisieren; sie werden weder verschoben noch umbenannt.
   - Quelle und Ziel des ALT-Umzugs mit vollständig aufgelösten absoluten Pfaden prüfen.
   - Bestätigen, dass beide Pfade innerhalb `data/ma_analyse` liegen und `data/ma_analyse/reference_cases/ALT` nicht existiert.
   - Für ALT einen Metadaten-Snapshot aus relativen Pfaden, Dateigröße, Endung und Änderungszeit erstellen; keine IDM-/IDC-Inhalte und keine Hashes dieser Dateien lesen.

2. **Expliziten Run- und Faktorenvertrag einführen**

   - `config/ma_analyse/reference_comparison.json` mit Schema-Version und genau fünf stabilen `run_id`-Werten anlegen.
   - Verzeichnisnamen und Anzeigenamen getrennt halten, damit Leerzeichen keine technische Identität bestimmen.
   - Pro Run mindestens führen:
     - `run_id`;
     - Anzeigename;
     - relativer erlaubter Quellpfad unter `Vergleich der Referenz`;
     - Modell `5Z` oder `29Z`;
     - Berechnungsumfang `full_topics` oder `reduced_topics`;
     - Ausgabeauflösungsmodus `ida_default`, `explicit` oder `unconfirmed`;
     - bestätigtes Ausgabeintervall nur als optionalen Wert;
     - IDA-Version;
     - Time-Split-Status;
     - Laufzeiten je Simulationstyp;
     - Messstatus `single_observation`;
     - Quelle der Zeitangabe `user_documented`;
     - Vergleichsgruppen für Zonierung, Berechnungsumfang und Ausgabeauflösung.
   - Für den IDA-Wert `0.0` den Modus `ida_default` speichern; kein tatsächliches Intervall `0.0 h` ausgeben.
   - Noch nicht eindeutig zuordenbare Einstellungen als `unconfirmed` führen.

3. **Discovery fail-closed und kollisionsfrei umbauen**

   - Die fünf Run-Wurzeln ausschließlich aus dem versionierten Vertrag auflösen.
   - Bestätigen, dass jede aufgelöste Run-Wurzel innerhalb `ida_imports/Vergleich der Referenz` liegt.
   - Innerhalb der erlaubten Run-Wurzeln ausschließlich PRNs aus den definierten Ergebnisordnern `heating`, `cooling`, `energy`, `summer-peak` sowie ausdrücklich zugelassene PRNs direkt unter der Run-Wurzel erfassen.
   - Keine Geschwisterverzeichnisse, `reference_cases` oder ALT durchsuchen.
   - IDM/IDC ignorieren und niemals an Parser oder Hashfunktion übergeben.
   - `IdaSeriesSelection` um einen stabilen Vergleichs-Run-Schlüssel ergänzen oder den vorhandenen `run_id` durchgängig verwenden.
   - Paket- und Serienkennungen in einem neuen Namensraum aus Schema-Version, Run-ID, Ergebnisart, Zone, Artefakt und Spalte bilden.
   - Doppelte Package- und Series-IDs vor dem Schreiben erkennen und verständlich abbrechen.
   - `discover_known_ida_prn()` und `prepare_known_ida_results()` als kompatible Fassaden erhalten.
   - ALT aus der Standardauswahl von `prepare_known_ida_results()` entfernen.
   - Wenn der Vergleichsordner oder Vertrag vorhanden, aber unvollständig oder ungültig ist, muss `run_prepare()` abbrechen. Der Legacy-Fallback darf dann nicht anspringen.
   - Der Legacy-Fallback bleibt ausschließlich für einen klar erkannten alten Bestand ohne Vergleichsvertrag bestehen.

4. **Run-Inventar während `prepare` erzeugen**

   - Pro Run ein strukturiertes Inventar neben den Prepared-Referenzen schreiben.
   - Ermitteln:
     - PRN-Anzahl;
     - Gesamtgröße der PRNs;
     - Anzahl Dateien je Ergebnisart und Artefakttyp;
     - vorhandene Metriken und Spalten;
     - belegte oder `unverified` Einheiten;
     - Zahl der Datenzeilen;
     - Zeitbeginn und Zeitende;
     - häufigste und abweichende Zeitabstände;
     - Duplikate, Lücken und Parserfehler;
     - Zahl erzeugter Prepared-Pakete und Datensätze;
     - Auswertbarkeit und Diagnosen.
   - Die PRN-Anzahl dynamisch bestimmen. Die genannten Werte 917 / 596 / 596 / 184 / 116 dienen als dokumentierter Ausgangsstand und erzeugen bei Abweichung eine sichtbare Datenstandsdiagnose.
   - Parserfehler pro Datei sichtbar machen; keine Datei still auslassen.
   - Keine fachlichen Kennwerte im Importadapter berechnen.

5. **Begrenzten Vergleichsservice aufbauen**

   - `src/ma_analyse/analysis/reference_case_comparison.py` als kleinen Service anlegen.
   - Der Service liest den Run-Vertrag und die Run-Inventare, nicht IDM-/IDC-Dateien.
   - Er erzeugt stabile Tabellen:
     - `Fallübersicht`;
     - `Simulationszeiten`;
     - `Ausgabeumfang`;
     - `Kennwertinventar`;
     - `Vergleichbarkeit`;
     - `Gebäudekennwerte`;
     - `Methodische Grenzen`.
   - Laufzeitwerte je Simulationstyp und als Summe ausgeben. Quotienten und Einsparungen als deskriptiv kennzeichnen.
   - Nur dann `vergleichbar` melden, wenn außer dem untersuchten Faktor alle kontrollierten Metadaten bestätigt gleich sind.
   - Direkte Gebäude- oder Anlagenreihen nur verwenden, wenn Semantik und Einheit belegt sind.
   - Zonenwerte nur bei bestätigter Vollständigkeit, Multiplikatoren, Einheit und Systemgrenze zu Gebäudegrößen aggregieren.
   - Keine Summe individueller Zonenmaxima als Gebäudepeak verwenden.
   - Gleiche Metriknamen mit unterschiedlichen Einheiten, Zeitrastern oder Abdeckungen nicht automatisch zusammenführen.
   - Die bestehende cohort-basierte Zonentabellenfunktion nicht für den Mehrfachrun-Vergleich verwenden.

6. **Additiven Bedien- und Berichtspfad ergänzen**

   - Einen neuen Befehl `reference-compare` ergänzen, der vorhandene Prepared-Run-Inventare voraussetzt.
   - Fehlende oder veraltete Vorbereitung klar melden; keine stillschweigende Rohdatenanalyse durchführen.
   - Standardausgabe unter `data/ma_analyse/reports/reference_comparison/`:
     - eine XLSX-Arbeitsmappe;
     - CSV-Dateien je Tabelle;
     - eine PNG-Abbildung mit getrennten Teilflächen für Simulationszeit und Rohdatenumfang.
   - Kein GUI-Ausbau.
   - Das fachliche Ergebnisdiagramm bleibt deaktiviert, bis der Nutzer aus dem Inventar wenige vergleichbare Kennwerte ausgewählt hat.

7. **Manuellen kontrollierten Testentwurf dokumentieren**

   - Drei getrennte Vergleichsachsen definieren:
     - Zonierung: 29Z vollständig gegen 5Z vollständig;
     - Berechnungsumfang: vollständig gegen reduzierte Themen innerhalb derselben Zonierung;
     - Ausgabeauflösung: gleicher Run mit identischem Berechnungsumfang im IDA-Standardmodus gegen eine explizit bestätigte Ausgabeauflösung.
   - Für jede Achse gleiche IDA-Version, Time-Split-Einstellung, Hardware, Hintergrundlast, Modellstand und Simulationskonfiguration verlangen.
   - Mindestens drei Wiederholungen je Simulationsart empfehlen; Median, Minimum, Maximum und Streuung dokumentieren.
   - Pro manueller Ausführung die IDA-Dauer übernehmen und anschließend PRN-Anzahl, Bytes, Zeilen und effektive Zeitabstände durch den Softwarepfad inventarisieren.
   - Getrennt bewerten:
     - Einsparung innerhalb der IDA-Simulation;
     - Reduktion des Rohdatenumfangs;
     - mögliche Reduktion des späteren Prepare-Aufwands.
   - Der Testentwurf startet IDA nicht und verändert keine Modelldatei.

8. **Ausschließlich ALT kontrolliert verschieben**

   - Diesen Schritt erst nach bestandenen synthetischen Discovery- und ALT-Ausschlusstests ausführen.
   - `data/ma_analyse/reference_cases` anlegen, sofern der Elternordner fehlt.
   - Vor dem Umzug bestätigen:
     - Quelle `data/ma_analyse/ida_imports/ALT` vorhanden;
     - Ziel `data/ma_analyse/reference_cases/ALT` abwesend;
     - Quelle und Ziel auf demselben Datenlaufwerk;
     - die fünf aktiven Referenz-Runs liegen außerhalb von ALT.
   - ALT als Ganzes mit einer einzelnen, exakt adressierten Verschiebung umziehen.
   - Den Vorher-/Nachher-Snapshot aus relativen Pfaden, Dateianzahl, Endung, Größe und Änderungszeit vergleichen.
   - Bestätigen, dass `ida_imports/ALT` danach nicht mehr existiert und `reference_cases/ALT` vollständig vorhanden ist.
   - Die fünf aktiven Run-Verzeichnisse unter `ida_imports/Vergleich der Referenz` bleiben während dieses Schritts unangetastet.
   - Keine Datei löschen, zusammenführen oder inhaltlich öffnen.

9. **Dokumentation und Entscheidung knapp aktualisieren**

   - In den Modul-READMEs die aktive Referenzstruktur, den ALT-Ausschluss und die Trennung von Simulationszeit, Berechnungsumfang, Ausgabeauflösung und PostProcess dokumentieren.
   - Eine neue Nutzerentscheidung ergänzen, die UD-126 nur im Vergleichsumfang präzisiert:
     - 5Z bleibt Hauptmodell;
     - 29Z wird nicht zum neuen Hauptstrang;
     - der begrenzte Vergleich dient der Begründung und Wirkungskontrolle der Zonierungsreduktion.
   - Die offenen P036-Fachgates unverändert sichtbar lassen.
   - `CHANGELOG.md` ergänzend patchen.
   - Den unabhängigen Plan nicht automatisch in formelle Planindizes eintragen.
   - Den lokalen Navigator erst innerhalb des freigegebenen Umsetzungsumfangs aktualisieren und validieren.

## Pruefungen

### Automatisierte Tests

- Discovery findet in einer synthetischen Struktur unter `ida_imports/Vergleich der Referenz` exakt die fünf konfigurierten Runs.
- Unbekannte Geschwisterordner werden nicht verarbeitet.
- `ida_imports/ALT` und `reference_cases/ALT` werden vom Standard-Prepare nicht erfasst.
- Ein vorhandener, aber fehlerhafter Vergleichsvertrag führt zum kontrollierten Abbruch und nicht zum Legacy-Fallback.
- IDM-/IDC-Dateien werden weder gelesen noch gehasht; die Tests instrumentieren die entsprechenden Lese- und Hashpfade.
- Zwei Runs mit identischen PRN-Namen erzeugen unterschiedliche Paket- und Serien-IDs.
- Doppelte Run-IDs, Verzeichnisse oder Ziel-IDs werden vor dem Schreiben abgelehnt.
- Resume verwendet nur ein Prepared-Paket desselben Run- und Quellstands.
- Der Metadatenvertrag lehnt ungültige Simulationstypen, negative Dauer und widersprüchliche Ausgabeauflösung ab.
- `ida_default` wird nicht als numerisches Intervall `0 h` ausgegeben.
- PRN-Anzahl, Gesamtbytes, Zeilen und Zeitabstände werden mit synthetischen variablen Zeitreihen korrekt inventarisiert.
- Gleiche PRN-Anzahl bei unterschiedlicher Zeilenzahl bleibt als unterschiedliche Datendichte sichtbar.
- Metriken mit unbekannter Einheit bleiben `unverified`.
- Mehrere Runs derselben Kohorte werden im Vergleich nicht vermischt.
- Die Vergleichsmatrix sperrt einen kausalen Vergleich bei unbestätigten oder unterschiedlichen Kontrollfaktoren.
- Unvollständige Zonenabdeckung erzeugt keinen Gebäudepeak oder Gebäudeenergiewert.
- Bestehende Tests für PRN-Parser, `run_prepare()`, CLI und Legacy-Fallback bleiben grün.
- Keine regulären Tests verwenden die lokalen realen IDA-Dateien.

### Lokale Integrationsprüfungen nach Freigabe

- Vor jedem Schreibzugriff bestätigen, dass genau fünf aktive Runs unter `ida_imports/Vergleich der Referenz` liegen.
- Vor-/Nachinventar ausschließlich für ALT vergleichen.
- Bestätigen, dass die fünf aktiven Runs vor und nach dem ALT-Umzug dieselben Pfade, Dateianzahlen und Größen besitzen.
- Bestätigen, dass `reference_cases` nicht durch `prepare` durchsucht wird.
- `prepare` einmal gegen die aktive Referenzstruktur ausführen und Run-Anzahl, Package-IDs sowie Resume-Verhalten prüfen.
- `reference-compare` ausführen und alle Tabellen auf fünf getrennte Runs prüfen.
- Die PRN-Zahlen 917 / 596 / 596 / 184 / 116 gegen den aktuellen Bestand abgleichen; Abweichungen als Datenstandsänderung dokumentieren.
- Sicherstellen, dass die Zeitdaten 107/121/926/118, 133/145/942/106, 178/212/1082/215, 24/24/294/24 und 44/53/532/52 korrekt zugeordnet sind.
- Prüfen, dass keine Aussage die langsameren „weniger Simulation“-Einzelmessungen als bewiesene Einsparung interpretiert.
- Zieltests ausführen:
  - `tests/test_ma_data_preparation_ida.py`;
  - `tests/test_ma_analyse_prepare_owner.py`;
  - `tests/test_ma_analyse_commands.py`;
  - neue Referenzvergleichstests.
- Anschließend die vollständige Testsuite ausführen, sofern keine unabhängige bekannte Störung entgegensteht.
- Abschließend `git diff --check`, `git status --short` und den gezielten Diff prüfen; fremde Änderungen bleiben unangetastet.

### Akzeptanzkriterien

- Die fünf aktiven Referenz-Runs verblieben unverändert an ihrem bisherigen Ort.
- Genau fünf stabile Referenz-Run-Identitäten sind vorbereitet.
- ALT liegt vollständig unter `data/ma_analyse/reference_cases/ALT`.
- ALT wird standardmäßig nicht entdeckt oder verarbeitet.
- Kein Run überschreibt einen anderen.
- PRN-Anzahl, Datenvolumen und Ausgabeauflösung werden als getrennte Größen geführt.
- Simulationszeiten werden ausschließlich aus dem dokumentierten Prozessvertrag übernommen.
- Das Vergleichspaket trennt beobachtete Werte, bestätigte Vergleiche und offene Metadaten.
- Nicht belegte Gebäudekennwerte bleiben sichtbar `nicht auswertbar`.
- Eine erste Prozessabbildung und eine Kandidatenliste für den späteren fachlichen Ergebnisvergleich liegen vor.
- Bestehende APIs und Befehle funktionieren unverändert weiter.
- Keine IDM-/IDC-Inhalte wurden gelesen.
- Keine Datei wurde gelöscht.

## Risiken und offene Entscheidungen

- **Blocker:** Die genaue Zuordnung des geänderten Ausgabeauflösungsmodus zum Run `29Z weniger Simulation plus Zeitschritt` ist noch manuell zu bestätigen. Bis dahin bleibt die Ursache des Unterschieds `Metadatenbestätigung ausstehend`.

- **Blocker:** Wenn `data/ma_analyse/reference_cases/ALT` bei der Umsetzung bereits existiert, erfolgt keine Zusammenführung und kein Überschreiben. Der ALT-Umzug stoppt zur Klärung.

- **Blocker:** Wenn die aktive Referenzstruktur bei der Umsetzung nicht mehr genau die fünf vereinbarten Run-Verzeichnisse enthält, wird weder Discovery-Konfiguration noch ALT-Umzug auf Basis veralteter Annahmen fortgesetzt.

- **Wichtig:** Die aktuellen Einzelmessungen reichen nicht für eine statistisch belastbare Kausalbehauptung. Im Referenzfallkapitel dürfen sie zunächst nur als explorative Prozessbeobachtung erscheinen.

- **Wichtig:** Eine verringerte Anzahl ausgegebener Themen reduziert die PRN-Anzahl deutlich, hat in den vorhandenen Einzelmessungen aber keine Laufzeitverkürzung gezeigt. Datenmenge und Rechenzeit müssen getrennt argumentiert werden.

- **Wichtig:** Der IDA-Standardmodus `0.0` kann intern eine programmgesteuerte Ausgabe bedeuten. Das effektive Raster wird aus den PRN-Zeitachsen inventarisiert, aber nicht ohne IDA-Bestätigung als Konfiguration behauptet.

- **Wichtig:** Direkte Gebäudegrößen können im Datenbestand fehlen. Ohne belegte Systemgrenze und vollständige Zonendaten darf der Service keine Ersatzaggregation erzeugen.

- **Wichtig:** Die bestehende `build_model_zone_tables()`-Logik ist nicht für fünf gleichzeitige Runs ausgelegt. Der neue Slice verwendet deshalb einen getrennten, run-bewussten Vergleichsservice.

- **Wichtig:** Die neue Paketidentität kann zusätzliche Prepared-Ausgabeverzeichnisse erzeugen. Bestehende Legacy-Pakete werden nicht gelöscht.

- **Wichtig:** Änderungen an bereits modifizierten Entscheidungs- und Changelog-Dateien bergen Konfliktrisiko. Der aktuelle Diff ist unmittelbar vor dem Patch erneut zu lesen.

- **Optional:** Nach Sichtung des Kennwertinventars entscheidet der Nutzer, welche wenigen fachlichen Größen in die endgültige Tabelle und das zweite Diagramm kommen.

- **Optional:** Erst nach kontrollierten Wiederholungsmessungen kann entschieden werden, ob zusätzlich ein realer `prepare`-Benchmark pro Run dokumentiert wird. Dieser darf keine automatische IDA-Simulation und keine Vermischung mit der produktiven Datenbank auslösen.

Rückfallweg:

- Der einzige Datenumzug betrifft ALT und erfolgt über exakt aufgelöste Pfade auf demselben Datenlaufwerk.
- Schlägt die Nachprüfung fehl, wird `data/ma_analyse/reference_cases/ALT` auf den protokollierten Ursprung `data/ma_analyse/ida_imports/ALT` zurückverschoben.
- Die Rückverschiebung beginnt nur, wenn der Ursprungspfad abwesend und der Zielpfad eindeutig vollständig vorhanden ist.
- Die fünf aktiven Referenz-Runs sind nicht Teil des Rückfallvorgangs.
- Es werden keine Dateien gelöscht oder zusammengeführt.
- Additiv erzeugte Prepared- und Reportdaten werden bei einem Rückfall nicht automatisch entfernt; sie werden als nicht aktiv gekennzeichnet.
- Code- und Dokumentationsänderungen werden bei Bedarf durch einen gezielten Gegenpatch zurückgenommen, nicht durch `git reset`, `git checkout` oder das Überschreiben fremder Änderungen.

## Tera-Uebergabe

Der koordinierende Agent speichert diesen vollständigen Plan unverändert unter `docs/project/plans/independent/` und ersetzt anschließend im Umsetzungshandoff den Platzhalter `<Planpfad>` durch den tatsächlichen Pfad.

Die Umsetzung darf ausschließlich nach der ausdrücklichen Nutzerformulierung `Freigabe zur Umsetzung` beginnen.

```text
Setze den freigegebenen unabhängigen Umsetzungsplan
`<Planpfad>` um.

Lies den Plan vollständig. Prüfe den aktuellen Bestand nur im darin benannten
Scope. Setze ausschließlich die freigegebenen Schritte um, führe die
vorgesehenen Prüfungen aus und dokumentiere Abweichungen. Halte an, falls
eine Scope-Erweiterung, neue Abhängigkeit, Löschung oder externe Aktion nötig
wird.
```

Tera prüft vor dem ersten Schreibzugriff insbesondere:

- den aktuellen Git-Diff und fremde Änderungen;
- die unveränderte Existenz der fünf aktiven Runs unter `ida_imports/Vergleich der Referenz`;
- die tatsächlichen Quell- und Zielpfade des ALT-Umzugs;
- die weiterhin gültige Rechte- und Schutzgrenze für IDM/IDC;
- die noch offene manuelle Bestätigung der Ausgabeauflösung.

Nach der Umsetzung fragt Tera den Nutzer, ob der Stand P036 zugeordnet, als neuer formeller P-Plan aufgenommen oder als abgeschlossener unabhängiger Einzelplan belassen werden soll.
