# P018 ma_simulation_setup und neutrales Run-Paket

Stand: 2026-07-14
Status: Fachlich konsolidiert, Umsetzung geplant
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
reproduzierbarer manueller Uebergabestand an IDA ICE und referenziert die
nach der Compliance-Grenze erforderliche Entscheidung.

Nicht Teil von V1 sind ein IDA-ICE-Adapter, das Schreiben oder Veraendern von
IDA-Dateien, ein Simulationsstart, Ergebnisimport und ein separates
`SimulationCase`-Objekt.

## Rolle im Masterarbeits-MVP V1

P018 beendet nur den Preprocess-Teil des Masterarbeits-MVP. Der gesamte
MVP-V1-Durchlauf setzt danach die manuelle Simulation, den P009-MVP-
Ergebnispostprocess, die drei OutputRequirementProfiles aus P016 und die
getrennte P030-Prozessauswertung fort. P018 verwendet dabei die freigegebene
Revision des `ThermalBuildingModel` aus P013 als Gebaeude-/Zonenabschluss.

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

## Compliance-Grenze

P018 bereitet nur neutral beschriebene Laeufe vor. Bis zu einer ausdruecklichen
schriftlichen EQUA-Freigabe erfolgt die Uebergabe an IDA ICE manuell und der
Simulationsstart manuell. P018 startet weder IDA ICE noch eine Simulation,
nutzt IDA ICE nicht als Simulationsserver und verarbeitet keine vollstaendige
`.idm`-Datei. Jede kuenftige IDA-bezogene Erweiterung dokumentiert vorher eine
`ComplianceDecision` nach `docs/compliance/ida_ice/` und erzwingt sie ueber
`ma_core.compliance`. `red` und `unknown` stoppen; `yellow` erfordert die
dokumentierte Bestaetigung sowie alle vom Service geforderten Rechtebelege.
Wetterreferenzen werden nur als bereits freigegebene `ma_weather`-Quellen
uebernommen. P018 liest weder DWD-Rohdaten noch Norminhalte erneut.

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
- Compliance-Entscheidungs-ID fuer geschuetzte Adapteroperationen und die
  manuelle IDA-Uebergabe in das Run-Manifest aufnehmen.
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
- Eine rote, unbekannte oder nicht vollstaendig freigegebene gelbe
  Compliance-Entscheidung blockiert das Manifest vor jeder Adapteroperation.

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
