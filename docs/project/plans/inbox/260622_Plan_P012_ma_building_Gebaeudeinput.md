# P012 ma_building Gebaeudeinput

Stand: 2026-07-02
Status: Teilweise umgesetzt
Prioritaet: Hoch
Abhaengigkeiten: P010, P011, P013, P015, P027

## Ziel

`ma_building` soll Gebaeudestruktur, geometrische Raeume, Flaechen, Bauteile,
Oeffnungen, einfache Sonnenschutzinformationen und bauphysikalische
Randbedingungen als neutrales, validierbares Gebaeudemodell bereitstellen.

Alle Eingabewege fuehren in dieselbe interne Struktur:

```text
Eingabequelle
    -> BuildingModelSpecification
    -> fachliche Validierung
    -> freigegebene Gebaeudemodellversion
    -> Uebergabe an ma_zones, ma_parameters und spaetere Adapter
```

Die Eingabequelle darf die nachgelagerte Datenstruktur nicht veraendern.

## Reifegrad

Konzept plus v1-Demo. Eine versionierte Demo-`BuildingModelSpecification`,
lokale IFC-Entity-Diagnose und lokale 3DM-Metadatendiagnose sind umgesetzt.
Ein produktiver IFC-Lite- oder Rhino-Import wird erst nach gesonderter Analyse
und Freigabe umgesetzt.

## Trainings- und Diagnosebasis

- Die aktuelle IFC-Datei des Projekts soll lokal als reale Arbeitsdatei fuer
  `ma_building` bereitgestellt werden. Sie dient zunaechst zur Diagnose:
  Dateityp, Dateigroesse, Pruefsumme, erkennbare IFC-Entitaeten, Einheiten,
  Geschosse, Raeume, Bauteile, Oeffnungen und vorhandene IDs.
- Echte IFC-Arbeitsdateien bleiben lokale Projektdaten und werden nicht
  automatisch versioniert. Vorgesehener lokaler Pfad:
  `data/ma_building/input/ifc/`.
- Fuer die Masterarbeit ist `SmallOffice_d_IFC2x3.ifc` das fachliche
  Referenzmodell. Die weiteren IDA-ICE-Sample-IFCs dienen nur als Vergleichs-
  und Plausibilisierungsdateien.
- 3DM-Arbeitsdateien bleiben ebenfalls lokale Projektdaten und werden in v1
  nur als Quelle mit Dateimetadaten diagnostiziert. Vorgesehener lokaler Pfad:
  `data/ma_building/input/rhino/`.
- DWG-Beispieldateien bleiben lokale CAD-Arbeitsdaten. Ohne DWG-Parser kann
  `ma_building` v1 nicht belastbar pruefen, ob daraus ein Gebaeudemodell
  ableitbar ist. Vorgesehener lokaler Pfad:
  `data/ma_building/input/cad/`.
- Nutzerentscheidung UD-066 legt fest: Ein DWG-Parser, Add-on oder eine
  externe DWG-Library wird fuer den aktuellen Masterarbeitsumfang nicht als
  produktiver Importpfad aufgenommen. Falls CAD-Daten fachlich gebraucht
  werden, sollen sie zuerst bewusst nach IFC oder DXF exportiert und separat
  bewertet werden.
- Zusaetzlich wird eine einfache, klar gekennzeichnete Demo geplant. Sie soll
  klein genug sein, um das Modul zu trainieren, Tests zu schreiben und die UI
  zu pruefen. Vorgeschlagener versionierter Zielpfad:
  `config/ma_building/examples/demo_building_spec.yaml`.
- Die Demo soll mindestens ein Gebaeude, ein Geschoss, wenige Raeume,
  Aussenwaende, Innenwaende, Bodenplatte, Dach oder Decke, Fenster, Tuer,
  Bauteilcodes, Objekt-IDs, Flaechenorientierungen und offene Annahmen
  enthalten.

## Modulabgrenzung

`ma_building` verwaltet:

- Gebaeude, Gebaeudeteile, Geschosse und geometrische Raeume
- physische Bauteile wie Waende, Bodenplatten, Decken, Daecher
- Oeffnungen wie Fenster und Tueren inklusive Host-Beziehung
- einfache geometrische Sonnenschutzinformationen
- Bauteilcodes, Objekt-IDs, Flaechen, Volumen, Massen und Orientierungen
- Importinformationen, Modellversionen, Reifegrade und Validierungsstatus
- bauliches Raumregister und unverbindliche Zonierungsvorschlaege

Nicht in `ma_building` gehoeren:

- Nutzungsprofile, Sollwerte, Belegung und Betriebszeiten; diese liegen in
  `ma_zones`
- technische Anlagen und Regelungslogik; diese liegen in `ma_technical`
- zentrale technische Datenhaltung; diese liegt spaeter in `ma_database`
- direkte Variantenbildung; diese laeuft ueber `ma_parameters` und
  `ma_variants`
- direkte Aenderung von IDA-ICE-Modellen

## BuildingModelSpecification

Die erste fachliche Zielstruktur ist eine
`BuildingModelSpecification`. Sie ist programmneutral und kann aus Demo,
manueller Eingabe, YAML/JSON oder spaeteren Importadaptern erzeugt werden.

Mindestinhalte:

- `schema_version`
- Projekt-, Gebaeude- und Modellversionsdaten
- Einheit, Nordrichtung und Massbezug
- Gebaeudeabmessungen
- Geschosse
- Raeume und Raumregister
- Bauteile und Begrenzungsflaechen
- Oeffnungen mit `host_element_id`
- einfache Sonnenschutzobjekte
- Bauteilcodes und konkrete Objekt-IDs
- Import- und Quelleninformationen
- Reifegrad, Annahmen, offene Punkte und Validierungsstatus

## Eingabewege

### Option A - KI-gestuetzte Modellerstellung

Die KI darf strukturierte Gebaeudebeschreibungen, Annahmenlisten,
Objektlisten und optional Austauschdateien vorbereiten. Verbindliche Quelle
fuer `ma_building` bleibt die strukturierte `BuildingModelSpecification`,
nicht eine alleinige CAD-Datei.

### Option B - vorhandenes Modell importieren

Geplanter Umgang nach Reife:

| Format oder Quelle | Einordnung fuer P012 |
|---|---|
| YAML-Demo | erster verbindlicher Demonstrator |
| JSON | vorbereitet als textliches Folgeformat |
| aktuelle IFC-Datei | lokale Metadaten- und Entity-Diagnose, kein Vollimport |
| IFC-Lite | offen bis OP-012 anhand realer Inhalte entschieden ist |
| Rhino `.3dm` | lokale Metadatendiagnose; produktiver Parser bleibt Ausbaupfad |
| DWG/CAD-Beispiel | lokale Ablage als ungepruefte CAD-Quelle, kein Vollimport; UD-066 schliesst produktiven DWG-Parser fuer den aktuellen Umfang aus |
| DXF/SKP/OBJ/STL | spaetere Option, derzeit nicht verbindlich |

Wichtig: Der ChatGPT-Input nennt `.3dm` als moegliches bevorzugtes
Geometrieformat. Die bestehende Zielarchitektur schliesst eine direkte
CAD-Integration fuer den aktuellen Masterarbeitsumfang aus. Deshalb wird
`.3dm` hier als spaeterer Ausbaupfad dokumentiert, nicht als freigegebene
MVP-Pflicht.

### Option C - manuelle oder textliche Eingabe

P012 sieht eine einfache manuelle beziehungsweise YAML-basierte Eingabe vor:

- gefuehrte Minimaldaten fuer Gebaeude, Geschosse, Waende, Raeume,
  Oeffnungen und Nordrichtung
- YAML-/JSON-Editor oder Dateiimport
- Validierung vor Freigabe
- klare Kennzeichnung manuell ergaenzter Werte

## Fachliche Grundobjekte

Geplante Kernobjekte:

- `BuildingModel`
- `BuildingModelVersion`
- `Building`
- `BuildingSection`
- `Storey`
- `Space`
- `PhysicalElement`
- `Surface`
- `Opening`
- `ShadingDevice`
- `ElementJunction`
- `ConstructionAssignment`
- `ImportedZoneHint`

## Kennungs- und ID-Konzept

Bauteilcodes beschreiben wiederverwendbare Typen, zum Beispiel:

- `AW` Aussenwand
- `IW` Innenwand
- `BP` Bodenplatte
- `GD` Geschossdecke
- `DA` Dach
- `FA` Aussenfenster
- `FI` Innenfenster
- `TA` Aussentuer
- `TI` Innentuer

Jedes konkrete Objekt erhaelt zusaetzlich eine eindeutige Objekt-ID, zum
Beispiel `WALL-0001`, `SLAB-0001`, `OPENING-0001`, `SPACE-0001` oder
`SHADING-0001`. Technische Datenbank-IDs bleiben davon getrennt.

## Reifegrade

Der Eingangsmodell-Reifegrad wird nach Informationsgehalt bewertet, nicht nach
Dateiformat:

| Stufe | Bedeutung |
|---|---|
| BIL-0 | 2D-Referenzmodell mit Linien, Grundrissen oder Schnitten |
| BIL-1 | geometrisches Oberflaechenmodell |
| BIL-2 | objektbasiertes Gebaeudemodell mit Waenden, Daechern, Fenstern und Raeumen |
| BIL-3 | bauteildefiniertes Architekturmodell mit Typen, Schichten und Materialien |
| BIL-4 | analysefaehiges Gebaeudemodell mit validierter Geometrie und Pflichtdaten |
| BIL-5 | koordiniertes Gesamtmodell mit Architektur, Raeumen, Zonierung und ggf. Technik |

Zu speichern sind mindestens:

- `source_input_level`
- `detected_input_level`
- `confirmed_input_level`
- `current_maturity_level`
- `target_maturity_level`

BIL-4 ist der regulaere Freigabestatus von `ma_building`. BIL-5 verteilt seine
Informationen auf mehrere Module und ist kein zwingender naechster Schritt.

## Geometrie- und Bauteilregeln

- Physische Waende, Bodenplatten, Decken und Daecher werden fachlich als
  zusammenhaengende Bauteilobjekte behandelt.
- Fenster und Tueren bleiben eigene Objekte und verweisen ueber
  `host_element_id` auf ihre Host-Wand.
- Oeffnungen duerfen in fruehen Staenden auch nur als Flaechenanteil vorliegen.
- Wandanschluesse werden als `miter`, `wall_a_continuous`,
  `wall_b_continuous`, `manual` oder `pending` dokumentiert.
- Orientierungen werden primaer aus Geometrie abgeleitet; die Nordrichtung ist
  projektweit erforderlich.
- Fenster-Einbaulagen werden bei konkreten oder generierten Fenstern gesondert
  erfasst.
- Sonnenschutz kann als unbekannt, Kennwert, Typ, Konzeptgeometrie oder
  detaillierte Geometrie vorliegen.

## Raumregister und Zonierungsvorschlaege

`ma_building` fuehrt ein bauliches Raumregister mit Raum-ID, Raumcode,
Geschoss, Geometrie, Flaeche, Volumen, Begrenzungsflaechen, Herkunft und
Validierungsstatus.

Importierte Zonierungsinformationen werden in `ma_building` nur als
`ImportedZoneHint` gespeichert. Die fachliche Zonierung, Nutzung und
Betriebsinterpretation erfolgt in `ma_zones`.

## Bauteilkatalog, Mengen und Bewertung

P012 plant nur die Gebaeude-bezogene Anwendung von Bauteiltypen. Eine spaetere
Katalogbasis enthaelt Materialien, Schichten, Bauteiltypen, U-Werte, Massen,
GWP- und Kostendaten. Fachliche Berechnungen bleiben in den Fachmodulen;
`ma_database` speichert spaeter technische Daten, Versionen und Beziehungen.

Fuer `ma_assessment` sollen aus `ma_building` spaeter mindestens
Bauteilflaechen, Materialvolumen, Materialmassen, Oeffnungsflaechen und
Bauteilanzahlen bereitstehen.

## Validierung und Freigabe

P012 verwendet die P010/P027-Grundsaetze:

- Fehler blockieren immer.
- Warnungen benoetigen eine bewusste Freigabeentscheidung.
- Quelle, Fundstelle, Problem und gewaehlte Handlung werden protokolliert.
- Importierte, manuelle und generierte Werte bleiben unterscheidbar.

Zu pruefen sind mindestens:

- eindeutige Objekt-IDs
- gueltige Bauteilcodes
- Einheiten und Nordrichtung
- Pflichtfelder der `BuildingModelSpecification`
- Raeume, Geschosse und Bauteilzuordnungen
- Host-Beziehungen von Oeffnungen
- Plausibilitaet von Flaechen, Volumen, Orientierungen und Reifegraden
- Analysebereitschaft fuer Energie, Tageslicht, Blendung, Nachhaltigkeit und
  Kosten nach jeweils benoetigtem Datenumfang

## Arbeitspakete

1. Bestehende Repository-, Daten-, UI- und Planstruktur pruefen. Umgesetzt in
   P012 v1.
2. Aktuelle IFC-Datei lokal als Diagnosequelle einplanen und klare Ablagegrenze
   dokumentieren. Umgesetzt ueber `data/ma_building/input/ifc/`.
3. Einfache versionierte Demo-`BuildingModelSpecification` planen und
   bereitstellen. Umgesetzt unter
   `config/ma_building/examples/demo_building_spec.yaml`.
4. YAML-Demo-Schema und spaetere JSON-Kompatibilitaet beschreiben. YAML ist in
   v1 umgesetzt; JSON bleibt vorbereitetes Folgeformat.
5. Fachmodelle fuer Gebaeude, Geschosse, Raeume, Bauteile, Oeffnungen,
   Sonnenschutz und Reifegrade entwerfen. Umgesetzt als kompakte
   `ma_building`-Dataclasses.
6. Quellen-, Diagnose-, Validierungs- und Freigabeprotokoll nach P010 anbinden.
   Umgesetzt mit `InputSource`, `ImportDiagnostic` und `ValidationResult`.
7. Schnittstellen zu `ma_zones`, `ma_parameters`, `ma_assessment` und
   `ma_export_simulation` dokumentieren. In v1 nur als Zielrichtung
   dokumentiert; keine produktive Uebergabe.
8. IFC-Inhaltsdiagnose mit realem Arbeitsstand auswerten, bevor ein
   IFC-Lite-Adapter freigegeben wird. Diagnosewerkzeug ist umgesetzt; die
   fachliche Auswertung realer IFC-Dateien bleibt naechster Schritt.
9. UI-Darstellung als geplante Modulansicht vorbereiten, ohne Fachreife
   vorzutaueschen. Umgesetzt als Streamlit-Pruefansicht fuer Demo und
   Quelldiagnosen.
10. Offene Entscheidungen vor produktivem IFC-/Rhino-Import in den
    Entscheidungsdokumenten fuehren.

## Umsetzungsstand v1

- Paketstruktur: `src/ma_building/` enthaelt Fachmodelle, Standardpfade,
  Demo-Lader, Quelldiagnose und Validierung.
- Versionierte Demo: `config/ma_building/examples/demo_building_spec.yaml`.
- Lokale Arbeitsdatenstruktur: `data/ma_building/input/ifc/`,
  `data/ma_building/input/rhino/`, `data/ma_building/input/cad/` und
  `data/ma_building/diagnostics/`.
- Masterarbeits-Referenzmodell: lokal
  `data/ma_building/input/ifc/SmallOffice_d_IFC2x3.ifc`.
- UI: `ma_ui` zeigt eine einfache Pruefansicht fuer Demo-Validierung und
  lokale Modellquellen.
- Tests: Demo-Lader, Fachmodelle, Validierung und Diagnose sind automatisiert
  abgedeckt.

## Akzeptanzkriterien

- Eine einfache Demo kann als `BuildingModelSpecification` beschrieben und
  validiert werden.
- Die aktuelle IFC-Datei wird als lokale Trainings- und Diagnosequelle im Plan
  beruecksichtigt, ohne einen Vollimport zu behaupten.
- Unbekannte oder unvollstaendige Dateien erzeugen strukturierte Diagnosen
  statt Absturz.
- Importierte, generierte und manuell ergaenzte Werte bleiben unterscheidbar.
- Demo-Gebaeudedaten koennen nach Freigabe an `ma_parameters` uebergeben
  werden.
- Raeume und importierte Zonierungsvorschlaege sind klar von `ma_zones`
  getrennt.
- Kein vollstaendiger IFC-, Rhino-, CAD- oder IDA-ICE-Workflow wird
  vorgetaeuscht.
- Offene Warnungen und Annahmen sind nachvollziehbar dokumentiert.

## Nicht enthalten

- produktiver vollstaendiger IFC-Import
- produktiver Rhino- oder CAD-Workflow
- produktiver DWG-Parser oder DWG-Importadapter
- CAD-Modellerstellung
- allgemeingueltige Geometrieinterpretation externer Modelle
- direkte Aenderung des IDA-ICE-Modells
- technische Datenbankmigration ohne stabile Fachmodelle

## Offene Entscheidungen

- OP-012: Welche Inhalte sind in den konkreten IFC-Arbeitsstaenden belastbar
  vorhanden und fuer IFC-Lite sicher uebernehmbar?
- OP-012a: Welche Inhalte aus `SmallOffice_d_IFC2x3.ifc` sollen in eine
  spaetere IFC-Lite-`BuildingModelSpecification` uebernommen werden?
- Soll `.3dm` nach dem Demo-/IFC-Diagnose-Slice als bevorzugter
  Geometrieimport weiter geplant werden oder bewusst Zukunftspfad bleiben?
- Welche lokalen IFC-Dateien duerfen als Trainingsdaten verwendet werden und
  welche Metadaten duerfen dokumentiert werden?
- Welche Demo-Geometrie ist klein genug fuer Tests, aber fachlich ausreichend
  fuer Raumregister, Oeffnungen und Bauteilzuweisung?
- Welche Analyseziele benoetigen in der Masterarbeit BIL-4 und welche duerfen
  mit frueheren Reifegraden arbeiten?
