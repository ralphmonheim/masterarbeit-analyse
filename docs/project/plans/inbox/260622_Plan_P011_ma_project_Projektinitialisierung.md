# P011 ma_project Projektinitialisierung und digitale Projektakte

Stand: 2026-07-15
Status: Fachlich konsolidiert; P011-S1a als reiner Modell-/Serialisierungsslice umgesetzt
Prioritaet: Hoch
Abhaengigkeiten: P010, P028, P032, P027

## Zweck und kanonische Rolle

`ma_project` initialisiert ein Projekt, stellt eine stabile Projektidentitaet
und einen kleinen lesenden Projektkontext bereit. Spaeter kann es eine
digitale Projektakte fuer zulaessige, beschreibende Unterlagen verwalten.

Es ist weder ein fachliches Workflowregister noch ein zentraler Speicher der
nachfolgenden Fachmodule. Die hier konsolidierte Fassung ersetzt den frueheren
Kurzplan als einzige kanonische P011-Planwahrheit. Der vom Nutzer lokal
freigegebene Gesamtentwurf vom 2026-07-15 wurde read-only ausgewertet; sein
Original bleibt ausserhalb des Repositories unveraendert.

## Council- und Compliance-Entscheidung

Mira, Vera und Justus bewerteten die Planaufnahme einstimmig bedingt positiv.
Die menschliche Freigabe vom 2026-07-15 deckt die lokale Inhaltspruefung und
die kontrollierte Konsolidierung dieses Plans ab. Die konkrete
Implementierungsfreigabe folgt dem nachstehenden P011-S1a-Scope.

Die Konsolidierung ist nur unter diesen verbindlichen Korrekturen zulaessig:

- Die Quellenwahl bleibt pro Fachmodul beim jeweiligen Owner mit
  `InputSource`; P011 besitzt kein globales Quellenregister.
- `ma_project` besitzt weder fachlichen Workflowstatus noch Projektfreigabe,
  Snapshot-Aggregation oder fachliche Modulrevisionen. Lokale Validierung darf
  nur den eigenen Speichervorgang blockieren.
- IFC-, Rhino- und andere maschinenlesbare Gebaeudemodelle bleiben bei
  `ma_building`; IDA-/Run-Referenzen bleiben bei P018, P009 und deren
  Adaptern. P011 darf spaeter nur zulaessige Vorschaubilder oder
  Dokumentationsassets verwalten.
- `ma_project` besitzt weiterhin Simulationsprogrammprofile und das
  kompatible `VariantNamingProfile`; `ma_variants` konsumiert und verwendet
  den Profilstand. Ein Rename zu `VariantDisplayProfile` und jeder
  Konfigurationspfadmove sind getrennte Kompatibilitaetsslices.
- Eine zentrale Ablage `data/projects/<id>/{building,weather,...}` entsteht
  nicht. Jede Fachdatei bleibt owner-first im verantwortlichen Modul.

## Fachliche Abgrenzung

`ma_project` beantwortet:

- Welches Projekt wird bearbeitet und wie lautet seine stabile `PRJ-...`-ID?
- Wie lauten Titel, Kurzname, allgemeiner Untersuchungsrahmen und optionaler
  Projektstandort?
- Welches Simulationsprogramm ist allgemein vorgesehen?
- Welche zulaessigen, beschreibenden Projektassets dokumentieren das Projekt?

Nicht zu P011 gehoeren:

- Gebaeudegeometrie, Gebaeuderevisionen oder Gebaeudelocks;
- Wetterdatenauswahl, Wetterfreigaben oder gemeinsam mutable Standortobjekte;
- Zonen-, Technik- und Parameterstaende, Wertequellen oder Checkpoints;
- Varianten, StudyDirections, StudyCases, Run-Manifeste und Ergebnisse;
- fachliche Freigabe- oder Statusaggregation;
- CAD-/IFC-/Rhino-/IDA-Interpretation, OCR, Cloudspeicherung oder
  Datenbankmigration.

## Bestehender Ausgangspunkt

P028 hat bereits folgende kompatibel zu erhaltende Demo-Funktionen geliefert:

- `SimulationProgramProfile` sowie geschuetztes Laden und Speichern von
  Programmlisten;
- `VariantNamingPart` und `VariantNamingProfile` samt Vorschau;
- Vorlagenschutz, Pfadbegrenzung, Kollisionsschutz und bestaetigtes
  Ueberschreiben eigener lokaler Dateien.

P010 liefert die formatneutralen Grundlagen `InputSource`, Diagnosen,
Freigaberegeln und sichere YAML-Schreibadapter. P011 verwendet diese
Infrastruktur, dupliziert aber weder die fachliche Quellenwahl noch
Freigabeentscheidungen anderer Module.

## Zielvertraege

Der Ausbau bleibt absichtlich in kleine, immutable Vertraege getrennt:

| Vertrag | Verantwortung im ersten Ausbau |
| --- | --- |
| `ProjectIdentity` | `project_id`, Titel, Kurzname und optionale allgemeine Angaben |
| `ProjectLocation` | allgemeiner Standort, kein Wetterdatensatz und keine TRY-Aufloesung |
| `ProjectInvestigation` | menschlich lesbarer Untersuchungsrahmen ohne Varianten- oder Runobjekte |
| `Project` | Projektidentitaet plus optionale Standort- und Untersuchungsangaben |
| `ProjectContext` | kleiner lesender Payload fuer spaetere Initialisierung anderer Module |

`ProjectContext` transportiert `project_id`, Titel, Kurzname und eine
unabhaengige Standortkopie. Eine Standortuebergabe nach
`ma_weather` ist einseitig: `ma_weather` kann daraus einen Vorschlag
uebernehmen und fachlich praezisieren, schreibt aber nicht nach `ma_project`
zurueck.

Ein spaeteres `ProjectSettings` ist ein eigener schemafester Vertrag. Ein
untypisiertes Sammelfeld fuer Quellen, Status oder Fachobjektreferenzen ist
nicht zulaessig.

## P011-S1a: Reines Projektmodell und Serialisierung

### Umgesetzter Umfang

1. Additive, immutable Modelle `ProjectIdentity`, `ProjectLocation`,
   `ProjectInvestigation`, `Project` und `ProjectContext` in `ma_project`.
2. Lokale Validierung fuer `PRJ-xxxxxx`, Pflichttexte, zeitzonenbewusste
   Zeitstempel und `updated_at >= created_at`.
3. Reine dict-/YAML-/JSON-kompatible Serialisierung ohne Datei- oder
   Verzeichnisoperation.
4. Ausschliesslich synthetische Tests mit festen Zeitpunkten fuer
   Validierung, Unveraenderlichkeit, Roundtrip und stabile Nutzlasten.
5. Bestehende P028-Profile, APIs, Konfigurationspfade und UI bleiben
   unveraendert.

### Ausdruecklich ausgeschlossen

- Projektordner, ID-Zaehler, `data/projects/`, WorkspacePaths oder
  `project.yaml`-Speichern;
- Datei-/Assetkopien, PDFs, Bilder, Screenshots und reale Quellen;
- UI-Erweiterung, Standortuebergabe an `ma_weather` und
  Fachmodulreferenzen;
- Naming-Umbenennung oder Move von `config/ma_variants/naming/` nach
  `config/ma_project/naming/`;
- Aenderungen bestehender Building-IDs, InputSource-/Release- oder
  P015-/P032-Vertraege.

### Abnahme

- Gueltige und ungueltige Projekt-IDs, leere Pflichtfelder, naive oder
  zeitlich ruecklaeufige Zeitstempel sind getestet.
- Serialisierung bleibt ohne lokale Arbeitsdateien reproduzierbar.
- `ma_project` importiert weder `ma_weather` noch andere Fachmodule.
- Die P028-Regressionssuite bleibt gruen.

### Umsetzungsnachweis

- `ProjectIdentity`, `ProjectLocation`, `ProjectInvestigation`, `Project`,
  `ProjectContext` und `project_context_from_project` sind immutable und
  additive Modelle in `ma_project`.
- `project_to_payload` und `project_from_payload` bilden eine reine,
  dateisystemfreie Dict-Serialisierung mit ISO-Zeitstempeln ab.
- ASCII-`PRJ-xxxxxx`-IDs, Standortkoordinaten als vollstaendiges Paar und
  zeitlich korrekte Zeitstempel auch an DST-Umstellungen sind getestet.
- Der Abschlusslauf pruefte P011, P028, Workflow und Architekturgrenzen mit
  60 Tests; `ruff check` und Formatcheck sind gruen.

## Nachfolgende, getrennt zu entscheidende Slices

| Slice | Inhalt | Gate |
| --- | --- | --- |
| P011-S1b | Pfad- und Persistenzvertrag fuer eine ausschliesslich eigene Projektdatei | P032-WorkspacePaths-Entscheidung, lokaler Speicherort und Ignore-Regeln |
| P011-S2 | sichere Projektanlage, lokale ID-Vergabe und Speichern | S1b, Kollisions- und Vorlagenschutz |
| P011-S3 | Projektuebersicht in Streamlit | stabile Services aus S1/S2 |
| P011-S4 | einseitiger Standortvorschlag an `ma_weather` | expliziter Payloadvertrag, keine Runtime-Kopplung |
| P011-S5 | digitale Projektakte und Assets | objektbezogene Rechte-/Datenschutz-/Repository-Freigabe je Datei |
| P011-S6 | Galerie und Coverbild | P011-S5, keine automatische physische Loeschung |
| P011-S7 | P028-Integration und Naming-Kompatibilitaet | eigener Pfadmigrations- und API-Kompatibilitaetsscope |

## Digitale Projektakte und Dateigrenzen

Die geplante Projektakte ist eine Dokumentationsschicht, keine Fachdatenbank.
Zulaessig sind spaeter nur nach objektbezogenem Preflight freigegebene
beschreibende Kopien, etwa eigene Skizzen oder Vorschaubilder. Das Original
einer externen Datei bleibt unveraendert, bis Herkunft, Lizenz, Datenschutz,
Repository- und Weitergaberecht geklaert sind.

Fachliche Arbeitsdateien wie IFC, Rhino, DWG, IDA-ICE, Wetterdateien,
Simulationsergebnisse und grosse Datenbanken werden nie in eine P011-Akte
verschoben. Ein `original_source_path` wird nicht in portable oder
versionierte `project.yaml`-Nutzlasten geschrieben; falls spaeter notwendig,
ist er ausschliesslich lokal und getrennt zu behandeln.

Asset-Metadaten, Hashes, relative Pfade, Coverbilder und ein hybrides
Dateimodell bleiben konzeptionell vorgesehen, aber bis P011-S5 kein
Implementierungsauftrag. Eine physische Loeschung ist immer eine eigene,
explizit bestaetigte Operation.

## Naming und Simulationsprogramme

Die bestehende frei erweiterbare Simulationsprogrammliste mit aktivem
Programm bleibt in `ma_project`. Das Naming-Profil bleibt bis zu einem
eigenen Kompatibilitaetsslice `VariantNamingProfile` und beeinflusst weder
`VAR-ID`, Fingerprints noch Study-/Run-Identitaeten. Der derzeitige
Legacy-Konfigurationspfad unter `config/ma_variants/naming/` bleibt
unveraendert, bis eine Migration inklusive Lesekompatibilitaet, lokaler
Arbeitsdateien und Tests beschlossen ist.

## Dokumentation und Nachweis

Jeder umgesetzte Slice aktualisiert diesen Plan, `PLAN_INDEX.md`,
`PLAN_STATUS.md`, die Modul-README, technische Entscheidungen, Changelog und
passende Tests. Die Projektakte darf erst nach einem eigenen Compliance-Gate
reale Dokumente verarbeiten. Commit, Push, externe Tools und Cloudverarbeitung
sind nicht Teil von P011.

## Naechster Schritt

P011-S1a nach dem hier dokumentierten Council-Scope umsetzen. P032-W3a bleibt
davon getrennt und braucht wegen seiner sichtbaren Legacy-API-Aenderung eine
eigene konkrete menschliche Freigabe.
