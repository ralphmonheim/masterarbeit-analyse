# P018 ma_simulation_setup und neutrales Run-Paket

Stand: 2026-07-27
Status: Teilweise umgesetzt; SmallOffice-V1-Draftpakete nachgewiesen
Prioritaet: Hoch
Abhaengigkeiten: P008, P011-P017, P027; spaeter P009

## Ziel

Vollstaendig erzeugte Varianten aus P017 mit neutralen Simulationsbedingungen,
Ausgabeanforderungen und Modellreferenzen zu einem validierten,
reproduzierbaren `SimulationRun` verbinden. P018 erzeugt ein lokales,
programmunabhaengiges Run-Paket; es erzeugt oder veraendert keine
Simulationsprogrammdatei.

## Reifegrad

Produktiver Vorbereitungsschritt ohne Simulationssteuerung. Ein Run referenziert
genau eine `VariantSelection`, umfasst eine oder mehrere vollstaendige
Varianten und erhaelt eine unveraenderliche `RUN-ID`.

## Preprocess V1-Mindestumfang

P018 bildet den Abschluss von Preprocess V1. Ein Run erhaelt eine
unveraenderliche `RUN-ID`, eine vollstaendige `VariantSelection`, das
aufgeloeste Jahres-Setup, Wetter- und Modellreferenzen sowie die direkte
`RUN -> VAR`-Zuordnung. Das freigegebene `RunManifest` dient als
reproduzierbarer manueller Uebergabestand an ein Simulationsprogramm. Rechte-
und Adapterfreigaben bleiben ausserhalb des fachlichen Run-Manifests.

Nicht Teil von V1 sind ein IDA-ICE-Adapter, das Schreiben oder Veraendern von
IDA-Dateien, ein Simulationsstart, Ergebnisimport und ein separates
`SimulationCase`-Objekt.

## Rolle im Masterarbeits-MVP V1

P018 beendet nur den Preprocess-Teil des Masterarbeits-MVP. Der gesamte
MVP-V1-Durchlauf setzt danach die manuelle Simulation, den P009-MVP-
Ergebnispostprocess, das ausgewaehlte OutputRequirementProfile aus dem von
`ma_analyse` definierten Katalog und die getrennte P030-Prozessauswertung
fort. P018 verwendet dabei die freigegebene Revision des
`ThermalBuildingModel` aus P013 als Gebaeude-/Zonenabschluss.

## Neutrales Run-Paket

Ein Run-Paket enthaelt mindestens:

```text
RUN-<id>/
|-- run_manifest.yaml
|-- simulation_setup.yaml
|-- preparation_report.yaml
|-- referenced_resources/
|-- technical_logs/
`-- variants/
    |-- VAR-<id>/variant_config.yaml
    `-- VAR-<id>/simulation_input.yaml
```

- `run_manifest.yaml` beschreibt Identitaet, Referenzen, Variantenmenge,
  Status und Freigabe.
- `simulation_setup.yaml` bleibt getrennt, weil Zeitraum, Zeitschritt und
  Ausgabeanforderungen keine fachlichen Variantenwerte sind.
- `variant_config.yaml` dokumentiert die vollstaendige fachliche Variante;
  `simulation_input.yaml` ist deren neutrale, simulationsrelevante Sicht.
- Alle Referenzen innerhalb eines freigegebenen Run-Pakets sind relativ und
  ueber ID, Revision und Content-Hash nachvollziehbar.
- Ressourcen werden fuer V1 nur als Referenz oder als begrenzte lokale Kopie
  materialisiert. Programmspezifische Dateien gehoeren nicht in das Paket.

## Status, Validierung und Freigabe

- Vorbereitung: `created`, `preview_prepared`, `prepared`, `blocked`.
- Validierung: `valid`, `valid_with_warnings`, `invalid`.
- Freigabe: bis `released_for_simulation` bearbeitbar; danach unveraenderlich.
- Ein `valid_with_warnings`-Run ist nur freigabefaehig, wenn keine Warnung
  blockiert und alle nicht blockierenden Warnungen bestaetigt sind.
- Die Materialisierung ist Alles-oder-nichts: eine fehlgeschlagene Variante
  blockiert den gesamten Run.

## Technische Logs und Forschungsgrenze

P018 schreibt nur technische Ereignisse: Start/Ende und Dauer von
Materialisierungsschritten, Objekt- und Dateianzahlen, Datenmenge, Status,
Warnungs-/Fehlercodes sowie `RUN-ID` und `VAR-ID`. P027 definiert dafuer den
gemeinsamen Ereignis- und Diagnosevertrag.

Wissenschaftliche Zeitmessung, manuelle Bearbeitungszeiten und Vergleiche von
Prozessmodi liegen ausschliesslich in P030 `research_tools`. Ein produktiver
Run besitzt keine Pflichtreferenz auf eine Forschungsauswertung.

## Adapter- und Rechte-Grenze

P018 bereitet nur neutral beschriebene Laeufe vor. Bis zu einer ausdruecklichen
schriftlichen EQUA-Freigabe erfolgt die Uebergabe an IDA ICE manuell und der
Simulationsstart manuell. P018 startet weder IDA ICE noch eine Simulation,
nutzt IDA ICE nicht als Simulationsserver und verarbeitet keine vollstaendige
`.idm`-Datei. Jede kuenftige IDA-bezogene Erweiterung benoetigt einen
getrennten technischen Scope sowie die erforderlichen Rechte- und
Quellennachweise. Wetterreferenzen werden nur als bereits validierte
`ma_weather`-Quellen uebernommen. P018 liest weder DWD-Rohdaten noch
Norminhalte erneut.

## Arbeitspakete

- Projektweit eindeutige Run-ID und Statusmodell definieren.
- Eingang aus P017 auf vollstaendige Varianten nach `VGEN` begrenzen.
- `RunManifest` mit Projekt, Modellstand, Parametersnapshot, VariantSelection,
  Varianten, `weather_key`, Zeitraum, Zeitschritt und Ausgabeanforderungen
  planen.
- Standard-Jahreslauf und ereignisbezogene Laufarten unterscheiden.
- UI-Eingabe, YAML-Import und Validierungsbericht vorsehen.
- Uebergabegrenze zu P009 dokumentieren.
- Direkte Zuordnung `RUN -> VAR` ohne `SimulationCase` festlegen.
- Rechte- und Adaptergrenzen ausserhalb des fachlichen Run-Manifests
  dokumentieren.
- Run-Paket, getrennte `simulation_setup.yaml`, Variantenkonfigurationen und
  technische Logs materialisieren.
- Analysegeleitete Pflichtausgaben als neutrale OutputRequirementProfiles
  uebernehmen; spaetere Analyseplaene besitzen deren Fachdefinition.

## Eingang aus P017

P018 erhaelt nach erfolgreicher `VariantGeneration`:

- `VAR-ID`
- vollstaendigen fachlichen Parametersatz
- simulationsrelevante Fachwerte
- notwendige Modell- und Projektreferenzen

P018 erhaelt keine gesamte wissenschaftliche Provenienz aus P017. Verifikation,
Regelprotokolle, RejectionReports und Auswahlbegruendungen bleiben in
`ma_variants`.

## Run-Struktur

Fuer den ersten Ausbau gilt:

```text
RUN-000001
|-- VAR-000041
|-- VAR-000043
`-- VAR-000047
```

Jeder Run referenziert genau eine `VariantSelection` und ein aufgeloestes
SimulationSetup. Alle Varianten eines Runs verwenden dasselbe Setup.

Eine Selection wird genau fuer einen Run verwendet. Fuer einen weiteren Run
wird eine neue Selection erzeugt, auch wenn dieselben Varianten ausgewaehlt
werden.

Run-interne Daten je Variante:

- Status
- Exportpfad
- Logpfad
- Ergebnispfad
- Fehlercode
- Start- und Abschlusszeitpunkt

Diese Daten sind Zuordnungen innerhalb des Runs und keine eigenstaendigen
`SimulationCase`-Objekte.

## Akzeptanzkriterien

- Ein Run ist ohne IDA-Installation vollstaendig beschreibbar.
- Ein Run-Paket enthaelt getrennte Manifest-, Setup-, Varianten- und
  technische Logartefakte.
- Fehlende Referenzen blockieren die Freigabe.
- Manifest ist unveraenderlich versionierbar und reproduzierbar.
- Fachliche Variantenwerte werden in P018 nicht neu berechnet oder veraendert.
- Es gibt keine `CASE-ID` und keine `SimulationCase`-Ebene.
- Kein Simulationsstart und keine Modellmanipulation erfolgen.
- Der Run beschreibt die manuelle Uebergabegrenze nachvollziehbar; ein
  automatisierter IDA-Start ist kein gueltiger Run-Schritt.
- Adapteroperationen sind kein Bestandteil der Manifestmaterialisierung und
  benoetigen einen getrennten Freigabe- und Nachweisscope.

## Umsetzungsslices

### P018-S1 Grundmodelle und Schemas

- `SimulationRun`, `RunManifest`, `SimulationSetup`, Statusmodell und
  RUN/VAR-Referenzen.
- YAML-Schemas und strukturiertes Diagnosemodell.

### P018-S2 Run-Materialisierung

- Run-Verzeichnisstruktur, relative Ressourcenreferenzen,
  `variant_config.yaml`, `simulation_input.yaml` und PreparationReport.
- Preview-Beispiel mit explizit nicht aufgeloesten Platzhaltern.

Der V1-Referenzpfad ist am 2026-07-14 umgesetzt: Er erzeugt fuer eine
freigegebene P015-Baseline und eine explizite Variante ein RunManifest sowie
`variant_config.yaml`, `simulation_input.yaml` und `preparation_report.md`.
Er nutzt noch die bestehenden LoD-1-Quellenreferenzen; die spaetere
P013-/P014-Revisionspersistenz bleibt ein getrennter Anschluss.

### P018-S3 Validierung und Freigabe

- Struktur-, Referenz- und modusspezifische Vollstaendigkeitspruefung.
- Warnungsbestaetigung, Neuaufbau vor Freigabe und Freeze bei
  `released_for_simulation`.

### P018-S4 Forschungsdarstellung

- Begrenzter Vergleich von Referenz- und lokaler Ressourcenmaterialisierung.
- Technische Kennzahlen fuer P030, ohne wissenschaftliche Messlogik in P018.

## Handover-Ergaenzung 2026-07-21

Das Handover konkretisiert den bestehenden neutralen Run-Vertrag:

- Ein `RUN` referenziert genau eine `VSEL`, ein aufgeloestes gemeinsames Setup
  und die daraus erzeugten `VAR` direkt; `RUN + VAR-ID` bleibt die eindeutige
  Zuordnung.
- Das Setup ergaenzt ausschliesslich simulationsbezogene Angaben wie Programm,
  Version, Zeitraum, Zeitschritt, Warm-up, Solver und Output-Konfiguration.
  Es berechnet oder veraendert keine fachlichen Variantenwerte.
- Leere `simulation/`- und `results/`-Bereiche sind im MVP zulaessig.
  IDA-Mapping, Dateierzeugung, Programmausfuehrung und Ergebnisimport bleiben
  ausserhalb dieses Plans und folgen erst in P009.
- Der Run dokumentiert Varianten-, Katalog-, Selection-, Quellenrevisions- und
  Hashbezug; eine `CASE-ID` wird nicht eingefuehrt.

## Umsetzungsstand 2026-07-27

- `SimulationSetupSpecification` und `simulation_setup.yaml` sind umgesetzt.
- Der gemeinsame SmallOffice-V1-Service materialisiert 30 Optimierungs- und
  acht Sensitivitaetspakete mit Manifest, Variantenkonfiguration, neutraler
  Simulationseingabe und Vorbereitungsbericht.
- Der manuelle Kandidatenlauf
  `SMALL-OFFICE-V1-MANUAL-20260727-002` bestaetigt 38 vollstaendige
  technische Draft-Pakete des Legacy-Service ohne Simulationsstart und ohne
  kritische Fehler. Er ersetzt nicht den noch ausstehenden entscheidenden
  Projektlauf mit realen geprueften IDA-Lasten.
- Frankfurt 2010/2035 bleiben reine Setup-Metadaten; ihre PRN-Zeitreihen
  werden in diesem Scope nicht verarbeitet.

## Konsolidierter V1-Uebergabebezug 2026-07-27

Nach UD-106 materialisiert `ma_simulation_setup` nur bestaetigte, gueltige
Variantenpakete. Als aktualisierungsbeduerftig markierte Kandidaten,
Selections oder Varianten duerfen nicht still weitergereicht werden. Der
PreProcess endet weiterhin nach dem Simulation-Setup; Simulationsstart,
Ergebnisimport und Ergebnisbewertung bleiben ausserhalb dieses Plans.

## UD-106-Umsetzungsstand 2026-07-27

`ma_simulation_setup` akzeptiert nur bestaetigte Variantenpakete mit
aktuellem Quellenfingerprint. Es schreibt je Variante ein lokales
`run_manifest.yaml`, `variant_package.yaml` und `simulation_setup.yaml` in
den Projekt-Output. Alle Pakete tragen `preparation_only`; eine automatische
Simulation wird nicht gestartet.

Eine Run-Gruppe referenziert genau eine Selection und fuehrt ihre Varianten
als getrennte `RUN + VAR-ID`-Unterordner. Das gemeinsame
`selection_manifest.yaml` sowie Run- und Setup-Dateien enthalten Baseline-,
Parameter-, Zonenmodell-, Dimensionierungs- und Outputreferenzen. Wetter,
Belegungszeit, Jahreszeitraum, Zeitzone, Kapazitaetsstrategie und alle
zonalen Leistungen in W sind materialisiert. Vor dem Schreiben werden alle
Pakete vollstaendig validiert; die Gruppe wird ueber ein temporaeres
Verzeichnis transaktional veroeffentlicht. `ma_simulation_setup` berechnet
den aktuellen Upstream-Fingerprint erneut und sperrt veraltete Pakete auch
dann, wenn die Variantenseite zwischenzeitlich nicht geoeffnet wurde.

Die Run-Gruppe ist der wissenschaftliche Run und referenziert genau eine
Selection; die nummerierten `RUN + VAR-ID`-Unterordner sind dessen manuelle
Ausfuehrungsfaelle, keine zusaetzlichen wissenschaftlichen Runs oder
`SimulationCase`-Objekte. Das Selection-Manifest speichert StudyCase,
StudyDirection, Auswahlmodus, Seed und Selection-Fingerprint. Der
Jahreslauf ist mit Start, Ende, `TRY_non_leap_standard_year_8760`,
deaktivierter Sommerzeit und 3600-s-Zeitschritt festgelegt. Wetterquellen
tragen Pfad, Revision, Studienrecord-Fingerprint und – falls lokal
aufgeloest – den Datei-SHA-256. Die noch nicht konkret aufgeloesten
Frankfurt-2010/2035-Quellen bleiben als
`source_resolution_required_before_simulation` sichtbar.

Die Abschlussvalidierung erzwingt ausserdem `Europe/Berlin` und den
Jahresmodus `annual`. Bei `resolved_local_file` muessen Quelldatei und
gespeicherter SHA-256 zum Materialisierungszeitpunkt uebereinstimmen.
Nicht aufgeloeste Wetterquellen erzeugen Run- und Gruppenstatus
`preparation_incomplete_weather_source` und verlangen als naechste Aktion
die Quellenaufloesung; sie werden nicht als bereit fuer die manuelle
Simulation bezeichnet.

## Konsolidierung nach UD-112 2026-07-31

`ma_simulation_setup` bleibt der sichtbare Abschluss des PreProcess nach
VGEN. Die UI stellt die moeglichen Ausgabethemen mit einfachen Checkboxen
bereit, zum Beispiel Jahresenergie, Heiz-/Kuehlspitzen,
Temperatur/Funktionspruefung und Baseline-/Variantenvergleich. Das
ausgewaehlte `OutputRequirementProfile` beschreibt erwartete Kennwerte und
Daten, erzeugt aber selbst keine Diagramme und besitzt keine
Dimensionierungsfachlogik. Der fachliche Profilkatalog und seine
Datenanforderungen gehoeren zu `ma_analyse`; P018 persistiert ausschliesslich
die vom Nutzer ausgewaehlte Profilinstanz im Setup/Manifest.

UD-114 bestaetigt diese Bereichsgrenze: Der PreProcess endet erst mit einem
validierten, materialisierten und `released_for_simulation` freigegebenen
Run-Paket. Export/Run-Uebergabe gehoeren bereits zum anschliessenden
Kernprozess. Die Workflow-UI wird erst nach der fachlichen und zentralen
Workflowmigration aus diesem Vertrag abgeleitet.

Ein `RUN` ist die wissenschaftliche Einheit: genau eine Selection,
ein gemeinsames Setup und mehrere `VAR`. Jede manuelle IDA-Ausfuehrung und
ihr Ergebnis werden ausschliesslich durch `(RUN-ID, VAR-ID)` adressiert.
Der gegenwaertige Altbestand mit einzelnen Run-Dateien je Variante bzw. einer
`Run-Gruppe` ist daher als Migrationsbedarf markiert; die Gruppe wird zum
kanonischen RUN, nicht zu einer weiteren Objektebene.

Nach dem Import erzeugt `ma_analyse` alle datenkompatiblen Diagramme der
angeforderten Themen. Ungewaehlte Themen bleiben `nicht angefordert`,
ausgewaehlte ohne ausreichende Daten `nicht auswertbar` mit Ursache. Die
alte Beschraenkung auf genau drei Diagrammprofile ist damit abgeloest; die
endgueltige Zuordnung von Datenfeldern zu Vorlagen wartet auf einen
freigegebenen neutralen Ergebnisexport und dessen Dateninventar.
