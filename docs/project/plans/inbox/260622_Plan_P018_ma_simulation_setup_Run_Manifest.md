# P018 ma_simulation_setup und Run-Manifest

Stand: 2026-07-14
Status: Geplant, Schnittstelle aus P017 fachlich konsolidiert
Prioritaet: Hoch
Abhaengigkeiten: P008, P011, P017, P027

## Ziel

Vollstaendig erzeugte Varianten aus P017 mit Simulationsprogramm, Zeitraum,
Zeitschritt, Ausgabeumfang und Modellreferenz zu einem validierten
Simulationslauf verbinden.

## Reifegrad

Produktiver Vorbereitungsschritt ohne Simulationssteuerung.

## Preprocess V1-Mindestumfang

P018 bildet den Abschluss von Preprocess V1. Ein Run erhaelt eine
unveraenderliche `RUN-ID`, eine vollstaendige `VariantSelection`, das
aufgeloeste Jahres-Setup, Wetter- und Modellreferenzen sowie die direkte
`RUN -> VAR`-Zuordnung. Das freigegebene `RunManifest` dient als
reproduzierbarer manueller Uebergabestand an IDA ICE und referenziert die
nach der Compliance-Grenze erforderliche Entscheidung.

Nicht Teil von V1 sind ein IDA-ICE-Adapter, das Schreiben oder Veraendern von
IDA-Dateien, ein Simulationsstart und ein separates `SimulationCase`-Objekt.

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
- Fehlende Referenzen blockieren die Freigabe.
- Manifest ist unveraenderlich versionierbar und reproduzierbar.
- Fachliche Variantenwerte werden in P018 nicht neu berechnet oder veraendert.
- Es gibt keine `CASE-ID` und keine `SimulationCase`-Ebene.
- Kein Simulationsstart und keine Modellmanipulation erfolgen.
- Der Run beschreibt die manuelle Uebergabegrenze nachvollziehbar; ein
  automatisierter IDA-Start ist kein gueltiger Run-Schritt.
- Eine rote, unbekannte oder nicht vollstaendig freigegebene gelbe
  Compliance-Entscheidung blockiert das Manifest vor jeder Adapteroperation.
