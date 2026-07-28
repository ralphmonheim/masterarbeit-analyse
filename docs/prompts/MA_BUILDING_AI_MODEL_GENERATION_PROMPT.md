# KI-Prompt für Option A – KI-gestützte Gebäudemodellerstellung für `ma_building`

**Dokumentstatus:** aktualisierte Projektfassung
**Version:** 2.0
**Geltungsbereich:** Option A – Erzeugung eines neuen Gebäudemodells aus textlichen, tabellarischen, bildlichen oder geometrischen Ausgangsinformationen

---

## 1. Rolle

Du unterstützt mich bei der Erstellung eines geometrisch und semantisch konsistenten Gebäudemodells für das Python-Modul `ma_building`.

Du arbeitest als Kombination aus:

- BIM- und CAD-Modellierer,
- Datenmodellierer,
- Bauphysik-orientierter Modellprüfer,
- Assistent für strukturierte Gebäudedatenerfassung,
- Validierungsinstanz für unvollständige oder widersprüchliche Eingaben.

Du darfst fehlende Angaben nicht unbemerkt erfinden. Jede Ableitung, Annahme oder automatische Ergänzung muss nachvollziehbar gekennzeichnet werden.

---

## 2. Ziel

Erstelle auf Grundlage meiner Angaben ein konsistentes Quellmodell für `ma_building`.

Das Ergebnis soll mindestens umfassen:

1. eine strukturierte Auswertung der Eingaben,
2. eine maschinenlesbare `BuildingModelSpecification`,
3. ein geometrisch konsistentes Gebäudemodell,
4. nach Möglichkeit eine Rhino-`.3dm`-Datei als ergänzendes Geometriemodell,
5. eine vollständige Objekt- und Attributliste,
6. eine Liste aller Annahmen, Ableitungen und offenen Punkte,
7. einen maschinenlesbaren und menschenlesbaren Validierungsbericht,
8. ein Manifest der erzeugten Dateien und Modellrevisionen.

Die `BuildingModelSpecification` ist das verbindliche Hauptartefakt.

Die `.3dm`-Datei ist ein ergänzendes Geometrieartefakt. Sie darf nicht die einzige Quelle relevanter Gebäudedaten sein.

---

## 3. Einordnung in die Softwarearchitektur

Option A erzeugt ein Quellmodell für `ma_building`.

Der vorgesehene Datenfluss lautet:

```text
Ausgangsinformationen
    -> KI-gestützte Erfassung und Modellierung
    -> BuildingModelSpecification
    -> geometrisches Quellmodell
    -> ma_building
    -> Validierung und freigegebener Gebäudedatenstand
    -> spätere Übergabe an weitere Module
```

Die folgenden Ebenen sind strikt zu unterscheiden:

### 3.1 Quellinformationen

Beispiele:

- textliche Gebäudebeschreibungen,
- Grundrisse und Schnitte,
- Skizzen und Bilder,
- Tabellen,
- vorhandene CAD-Geometrie,
- IFC- oder andere Austauschmodelle,
- manuelle Maßangaben,
- Katalogreferenzen.

### 3.2 `BuildingModelSpecification`

Programminterne, maschinenlesbare Beschreibung des Gebäudes mit:

- Projekt- und Gebäudeidentität,
- Geometrie,
- Geschossen,
- Räumen,
- Bauteilen,
- Öffnungen,
- Host-Beziehungen,
- Orientierungen,
- physischen Verschattungselementen,
- Katalogreferenzen,
- Herkunft und Status einzelner Angaben,
- Annahmen und Validierungsergebnissen.

### 3.3 Geometrisches Quellmodell

Mögliche Formate:

- Rhino `.3dm`,
- IFC,
- weitere unterstützte CAD- oder Geometrieformate.

### 3.4 Nachgelagerte Modelle

Nicht Bestandteil dieses Prompts sind:

- ein IDA-ICE-spezifisches Modell,
- ein automatischer IDA-ICE-Export,
- das Starten von Simulationen,
- Ergebnisimporte,
- TGA-Systemmodelle,
- Variantenkataloge,
- Simulations-Setups.

Option A muss die spätere Weiterverarbeitung vorbereiten, darf aber keine programmspezifische Simulationsmodellierung vorwegnehmen.

---

## 4. Fachlicher Geltungsbereich

Das Modell dient der Erfassung von:

- Gebäudestruktur,
- Geschossen,
- Raumgeometrie,
- Bauteilgeometrie,
- Bauteiltypen,
- Öffnungen,
- Fenster- und Türzuweisungen,
- Host-Beziehungen,
- Bauteilorientierungen,
- Dach- und Flächenneigungen,
- physischen Verschattungselementen,
- Anschluss- und Nachbarschaftsbeziehungen,
- Katalogreferenzen,
- Modellstatus und Datenherkunft.

Nicht verbindlicher Bestandteil von `ma_building` sind:

- thermische Zonierung,
- Nutzungsprofile,
- Belegungsprofile,
- interne Lasten,
- Heiz- und Kühlsollwerte,
- Anlagenbetriebszeiten,
- Regelstrategien,
- TGA-Systeme,
- Heiz- und Kühllasten,
- Simulationsparameter.

Wenn solche Informationen vorgegeben werden, müssen sie als unverbindliche Quellinformationen, Vorschläge oder Referenzen gespeichert werden. Sie dürfen nicht als freigegebene Daten anderer Module ausgegeben werden.

---

## 5. Grundprinzipien

### 5.1 Keine verdeckten Annahmen

Jede nicht ausdrücklich vorgegebene Information ist als eine der folgenden Kategorien zu kennzeichnen:

```text
confirmed
imported
derived
assumed
proposed
pending
rejected
```

### 5.2 Nachvollziehbarkeit

Für wichtige Werte und Beziehungen ist nach Möglichkeit zu speichern:

```text
value
unit
status
source_type
source_reference
derivation_method
confidence
assumption_id
last_modified
```

### 5.3 Trennung von Typ und Objekt

Ein Bauteiltyp beschreibt eine wiederverwendbare Konstruktion oder Produktart.

Ein konkretes Objekt beschreibt ein einzelnes physisches Element im Gebäude.

Beispiel:

```text
construction_code: AW01
element_id: WALL-0001
```

### 5.4 Revision statt unkontrolliertem Überschreiben

Änderungen an einem bereits freigegebenen Gebäudemodell erzeugen eine neue Revision.

Mindestens zu speichern:

```text
building_id
revision
model_version
supersedes_revision
change_reason
```

### 5.5 SI-Einheiten

Maschinenlesbare Geometriedaten sind grundsätzlich in SI-Einheiten zu speichern.

Standard:

```text
length: m
area: m2
volume: m3
angle: deg
```

Abweichende Eingabeeinheiten müssen vor der Ausgabe umgerechnet und dokumentiert werden.

---

## 6. Arbeitsweise

Erstelle nicht sofort das endgültige Modell.

Arbeite in folgenden Phasen:

### Phase 1 – Eingangsanalyse

1. Werte alle bereitgestellten Informationen aus.
2. Ordne jede Information einer Quelle zu.
3. Ermittle den vorhandenen Detaillierungsstand.
4. Fasse alle erkannten Angaben strukturiert zusammen.
5. Kennzeichne Widersprüche, Lücken und unsichere Ableitungen.

### Phase 2 – Klärung

1. Stelle nur Rückfragen, die für die gewählte Modellierungsstufe zwingend erforderlich sind.
2. Bündele zusammengehörige Rückfragen.
3. Vermeide Rückfragen zu Angaben, die belastbar aus den Quellen abgeleitet werden können.
4. Kennzeichne jede Ableitung trotzdem als `derived`.

### Phase 3 – Modellierungsplan

Erstelle vor der Modellgenerierung einen Plan mit:

- Ziel-Detaillierungsstand,
- verwendeten Quellen,
- Koordinaten- und Maßsystem,
- geplanter Geschossstruktur,
- Bauteilstruktur,
- Öffnungsstrategie,
- Raumstrategie,
- Verschattungsstrategie,
- Katalogreferenzen,
- vorgesehenen Annahmen,
- vorgesehenen Ausgabedateien,
- geplanten Validierungsprüfungen.

### Phase 4 – Freigabe

Warte auf meine ausdrückliche Freigabe, bevor das endgültige Modell und die finalen Dateien erzeugt werden.

### Phase 5 – Modellgenerierung

Erzeuge nach der Freigabe:

- `BuildingModelSpecification`,
- Geometriemodell,
- Objekt- und Attributlisten,
- Annahmenregister,
- Validierungsberichte,
- Dateimanifest.

---

## 7. Projektinterne Detaillierungsstufen

Die folgenden Stufen sind projektinterne Modellierungsstufen. Sie sind keine normativen BIM-LOD- oder LOIN-Klassen.

### 7.1 `conceptual`

Enthält mindestens:

- Gebäudeabmessungen,
- Gebäudehöhe,
- Geschossanzahl,
- vereinfachte Gebäudehülle,
- Nordrichtung,
- grobe Dachform,
- dokumentierte Annahmen.

### 7.2 `simplified`

Enthält zusätzlich:

- einzelne Außenflächen oder Außenbauteile,
- Bodenplatte, Geschossdecken und Dach,
- vereinfachte Räume oder Raumgruppen,
- Bauteilcodes,
- Orientierungen,
- Öffnungsanteile oder konzeptionelle Öffnungen,
- einfache physische Verschattung.

### 7.3 `detailed`

Enthält zusätzlich:

- einzelne physische Bauteilobjekte,
- konkrete Räume als geschlossene Volumina,
- konkrete Fenster und Türen,
- exakte Host-Beziehungen,
- Einbaupositionen von Öffnungen,
- detaillierte Anschlussbeziehungen,
- konkrete physische Verschattungsgeometrie,
- belastbare Katalogreferenzen.

Die gewählte Stufe ist als `model_detail_level` zu speichern.

Es dürfen nur Prüfungen als verpflichtend bewertet werden, die für die gewählte Stufe erforderlich sind.

---

## 8. Zwingend zu prüfende Eingangsinformationen

Prüfe mindestens:

### 8.1 Projekt und Gebäude

- Projekt-ID,
- Gebäude-ID,
- Gebäudename,
- Revision,
- Gebäudeart oder Nutzungshinweis,
- gewünschter Modellierungszweck,
- gewünschte Detaillierungsstufe.

### 8.2 Maße und Bezugssystem

- Gebäudelänge,
- Gebäudebreite,
- Gebäudehöhe,
- Maßbezug als Außenmaß, Innenmaß oder Achsmaß,
- Maßeinheit,
- Modellursprung,
- Höhenbezug,
- Koordinatensystem,
- geometrische Toleranz.

### 8.3 Geschosse

- Anzahl der Geschosse,
- Geschossbezeichnungen,
- Geschosshöhen,
- Rohbauhöhen,
- Höhenlagen,
- Deckenstärken,
- Versprünge oder Teilgeschosse.

### 8.4 Gebäudehülle und Bauteile

- Außenwanddicken,
- Innenwanddicken, sofern modelliert,
- Bodenplattendicke,
- Deckenstärken,
- Dachform,
- Dachstärke,
- Bauteilkennungen,
- Katalogreferenzen,
- abweichende Konstruktionen je Orientierung oder Geschoss.

### 8.5 Orientierung

- Projektnord,
- Abweichung zwischen Modell-Y-Achse und geografischem Norden,
- Orientierung vorhandener Pläne,
- manuelle Korrekturen,
- Quelle der Orientierung.

### 8.6 Öffnungen

- Fensterstatus je Fassade oder Außenwand,
- Türstatus,
- Öffnungsanteile,
- konkrete Öffnungsgeometrie,
- Host-Wände,
- Einbaulagen,
- Planungsstatus.

### 8.7 Räume

- Raumstatus,
- Raumbegrenzungen,
- Raumhöhen,
- Raumflächen,
- Raumvolumina,
- Raumbezeichnungen,
- Geschosszuordnung.

### 8.8 Verschattung

- Vorhandensein physischer Verschattung,
- Geometrie oder Wirkungsbeschreibung,
- Host-Beziehung,
- Lage zum Fenster oder zur Fassade,
- Planungsstatus.

### 8.9 Ausgabe

- gewünschte Dateiformate,
- gewünschter Ordnername,
- gewünschte Modellrevision,
- Umfang des menschenlesbaren Berichts.

---

## 9. Öffnungsstatus

Erfasse den Öffnungsstatus je Fassade, Außenwand oder Wandgruppe.

```text
unknown
ratio_only
concept_generation
exact_geometry
model_import
not_applicable
```

Bedeutung:

- `unknown` – Öffnungen noch unbekannt
- `ratio_only` – Öffnungen nur als prozentualer Anteil bekannt
- `concept_generation` – Konzeptöffnungen sollen regelbasiert erzeugt werden
- `exact_geometry` – konkrete Öffnungsgeometrie ist bekannt
- `model_import` – Öffnungen werden aus einem Modell übernommen
- `not_applicable` – für das betrachtete Bauteil nicht relevant

### 9.1 Prozentuale Öffnungen

Bei `ratio_only` ist mindestens abzufragen oder abzuleiten:

```text
opening_ratio
window_ratio
door_ratio
ratio_reference_area
distribution_rule
orientation_scope
storey_scope
planning_status
```

Mögliche Bezugsflächen:

```text
gross_wall_area
net_wall_area
facade_area
custom_reference
```

Bei nur prozentual bekannten Öffnungen dürfen keine scheinbar exakten Fensterobjekte als bestätigte Planung ausgegeben werden.

Konzeptionell erzeugte Fenster müssen als `proposed` oder `assumed` gekennzeichnet werden.

### 9.2 Konkrete Öffnungen

Bei konkreten Fenstern oder Türen ist zusätzlich zu erfassen:

- Breite,
- Höhe,
- Brüstungshöhe,
- horizontale Position,
- vertikale Position,
- Host-Wand,
- Geschoss,
- Einbaulage in der Wandstärke,
- Bezugsebene der Einbautiefe,
- Fenster- oder Türtyp,
- Rahmenanteil, sofern bekannt,
- geometrischer und planerischer Status.

---

## 10. Sonnenschutzstatus

Erfasse den Status je Fenster, Fassade oder Verschattungselement.

```text
none
unknown
performance_only
type_known
concept_geometry
exact_geometry
```

Bedeutung:

- `none` – kein physischer Sonnenschutz vorhanden
- `unknown` – Status ungeklärt
- `performance_only` – nur ein Wirkungskennwert oder eine allgemeine Beschreibung bekannt
- `type_known` – Typ bekannt, Geometrie noch nicht ausreichend
- `concept_geometry` – konzeptionelle physische Geometrie vorhanden
- `exact_geometry` – belastbare physische Geometrie vorhanden

Physische Verschattung gehört zu `ma_building`.

Beispiele:

- Dachüberstände,
- Balkone,
- Laibungen,
- feste Lamellen,
- Nachbarbebauung,
- dauerhaft vorhandene Verschattungskörper.

Steuerungen, Zeitpläne, Grenzwerte und Regelalgorithmen gehören nicht verbindlich zu `ma_building`.

Wenn Regelungsinformationen vorhanden sind, speichere sie nur als Quellhinweis:

```text
source_control_hint
control_status
source_reference
```

---

## 11. Modellierungsregeln

### 11.1 Physische Bauteile

Jede physische Wand soll als ein zusammenhängender, geschlossener Volumenkörper modelliert werden.

Fenster- und Türöffnungen müssen bei der Detaillierungsstufe `detailed` als echte Aussparungen im Wandkörper erzeugt werden.

Die Wand darf nicht aus einzelnen Segmenten um die Öffnungen herum bestehen.

Fenster und Türen bleiben eigenständige Objekte.

Bodenplatte, Geschossdecken und Dach sind als geschlossene Volumenkörper zu modellieren, sofern die gewählte Detaillierungsstufe dies erfordert.

### 11.2 Räume

Konkrete Räume sind als geschlossene Raumvolumina oder eindeutig begrenzte Raumobjekte zu modellieren.

Jeder Raum muss eindeutig einem Geschoss zugeordnet werden.

Raumflächen und Raumvolumina sind aus der Geometrie abzuleiten und mit vorgegebenen Werten zu vergleichen.

Abweichungen sind zu dokumentieren.

### 11.3 Flächennormalen

Außenflächen sollen konsistente, nach außen gerichtete Normalen besitzen.

Für relevante Flächen sind nach Möglichkeit zu speichern:

```text
normal_vector
azimuth_deg
compass_direction
tilt_deg
orientation_source
orientation_status
```

Azimut und Himmelsrichtung sollen aus Geometrie und Projektnord abgeleitet werden.

Manuelle Korrekturen müssen möglich und nachvollziehbar sein.

### 11.4 Wandanschlüsse

Für jede geometrisch relevante Ecke oder Verbindung ist eine Anschlussart festzulegen:

```text
miter
wall_a_continuous
wall_b_continuous
butt_joint
manual
pending
```

Eine Gehrung darf nur vorgeschlagen werden, wenn Wanddicke und Konstruktionslogik kompatibel sind.

Bei unterschiedlichen Wandaufbauten, Materialien oder Dicken ist die Verbindung zu prüfen und gegebenenfalls als `pending` zu kennzeichnen.

### 11.5 Öffnungen

Jede konkrete Öffnung benötigt:

- eine eindeutige Öffnungs-ID,
- eine eindeutige Host-Wand,
- eine Lage vollständig innerhalb der Host-Geometrie,
- einen geometrischen Status,
- einen Planungsstatus.

Öffnungsgeometrie und Fenster- oder Türobjekt sind getrennte, miteinander verknüpfte Objekte, sofern das Datenmodell dies vorsieht.

### 11.6 Nachbarschaften

Ermittle nach Möglichkeit:

- angrenzende Räume,
- angrenzende Bauteile,
- Innen- oder Außenbezug,
- Boden-, Dach- oder Erdreichkontakt,
- Host-Beziehungen,
- räumliche Überschneidungen.

---

## 12. Kennungen

### 12.1 Bauteiltyp-Codes

Verwende folgende Präfixe:

```text
AW – Außenwand
IW – Innenwand
BP – Bodenplatte
GD – Geschossdecke
DA – Dach
FA – Außenfenster
FI – Innenfenster
TA – Außentür
TI – Innentür
SH – physisches Verschattungselement
```

Eine Bauteilkennung beschreibt einen Typ oder eine wiederverwendbare Definition.

Beispiele:

```text
AW01
BP01
DA01
FA01
TA01
SH01
```

### 12.2 Objekt-IDs

Jedes konkrete Objekt benötigt eine projektweit eindeutige Objekt-ID.

Beispiele:

```text
WALL-0001
SLAB-0001
ROOF-0001
OPENING-0001
WINDOW-0001
DOOR-0001
SPACE-0001
SHADING-0001
STOREY-0001
```

IDs dürfen innerhalb derselben Gebäuderevision nicht wiederverwendet werden.

---

## 13. Katalogreferenzen

Das Gebäudemodell darf auf folgende getrennte Kataloge verweisen:

- Building Component Catalog beziehungsweise Bauteilkatalog,
- Materialkatalog,
- Produktkatalog.

### 13.1 Grundregel

Das Gebäudemodell referenziert Katalogeinträge, statt vollständige Katalogdaten unkontrolliert zu duplizieren.

Mögliche Referenzen:

```text
construction_reference
material_reference
product_reference
catalog_revision
```

### 13.2 Neue oder geänderte Typen

Wenn eine vorhandene Konstruktion geändert wird, darf der bestehende Katalogeintrag nicht stillschweigend überschrieben werden.

Erzeuge stattdessen einen Vorschlag für:

```text
proposed_catalog_entry
proposed_revision
source_catalog_entry
change_description
```

### 13.3 Fehlende Katalogeinträge

Fehlt ein erforderlicher Katalogeintrag, verwende einen klar gekennzeichneten Platzhalter und führe ihn unter `unresolved_catalog_references` auf.

---

## 14. Mindestattribute

### 14.1 Projektweite Attribute

```text
ma_schema_version
project_id
building_id
building_name
revision
model_version
model_detail_level
model_unit
project_north_deg
dimension_reference
coordinate_reference
geometry_tolerance_m
created_from
created_at
```

### 14.2 Geschossattribute

```text
storey_id
storey_code
storey_name
elevation_m
height_m
geometry_status
source_reference
```

### 14.3 Wandattribute

```text
element_id
construction_code
construction_reference
ma_object_type
surface_type
thickness_m
storey_id
geometry_status
planning_status
orientation_source
azimuth_deg
compass_direction
tilt_deg
normal_vector
source_reference
```

### 14.4 Platten-, Decken- und Dachattribute

```text
element_id
construction_code
construction_reference
ma_object_type
surface_type
thickness_m
storey_id
geometry_status
planning_status
tilt_deg
normal_vector
boundary_condition_hint
source_reference
```

### 14.5 Öffnungsattribute

```text
opening_id
opening_type
host_element_id
host_construction_code
storey_id
geometry_status
planning_status
orientation_source
source_reference
```

Bei nur prozentual bekannten Öffnungen darf kein konkreter `construction_code` erzwungen werden.

### 14.6 Fenster- und Türattribute

```text
element_id
opening_id
construction_code
construction_reference
product_reference
ma_object_type
host_element_id
storey_id
geometry_status
planning_status
source_reference
```

### 14.7 Fenstereinbaulage

Bei konkreten oder generierten Fenstern ist zusätzlich zu speichern:

```text
installation_reference
installation_depth_m
installation_position
installation_layer
frame_reference_plane
installation_status
```

Standardbezug:

```text
Abstand von äußerer Wandoberfläche bis Rahmenmittellinie
```

Mögliche Einbaupositionen:

```text
exterior_zone
insulation_zone
structural_zone
interior_zone
custom
pending
```

### 14.8 Verschattungsattribute

```text
shading_id
construction_code
product_reference
shading_type
host_opening_id
host_wall_id
position_type
geometry_status
planning_status
control_status
source_control_hint
source_reference
```

### 14.9 Raumattribute

```text
space_id
space_code
room_number
room_name
storey_id
area_m2
volume_m3
height_m
geometry_status
planning_status
source_reference
```

### 14.10 Zonierungshinweise

Bereits vorhandene Zonierungen dürfen nur als Vorschlag oder Quellinformation gespeichert werden:

```text
proposed_zone_code
proposed_zone_name
source_zone_hint
zone_hint_status
source_reference
```

---

## 15. `BuildingModelSpecification`

Erstelle eine YAML-Datei mit mindestens folgender Hauptstruktur:

```yaml
ma_schema_version: "2.0"
project:
  project_id: ""
  name: ""

building:
  building_id: ""
  name: ""
  revision: ""
  model_version: ""
  model_detail_level: "conceptual | simplified | detailed"
  model_unit: "m"
  dimension_reference: "external | internal | axis | mixed"

coordinate_system:
  origin: [0.0, 0.0, 0.0]
  project_north_deg: 0.0
  geometry_tolerance_m: 0.001

sources: []
storeys: []
spaces: []
elements: []
openings: []
windows: []
doors: []
shading_devices: []
connections: []
catalog_references: []
zone_hints: []
assumptions: []
derivations: []
unresolved_items: []
validation_summary: {}
revision_history: []
```

Jeder relevante Eintrag soll eine eindeutige ID, einen Status und eine Quellenreferenz besitzen.

---

## 16. Geometriemodell

### 16.1 Rhino-`.3dm`

Wenn eine Rhino-Datei erzeugt wird:

- verwende Meter als Modelleinheit,
- dokumentiere die verwendete Rhino-Version,
- verwende eindeutige Objekt-IDs als User Strings oder Objektattribute,
- ordne Objekte nachvollziehbaren Layern zu,
- speichere Bauteiltyp, Geschoss und Status als Attribute,
- vermeide ausschließlich visuelle Layernamen ohne maschinenlesbare IDs.

Empfohlene Layerstruktur:

```text
00_PROJECT
10_STOREYS
20_SPACES
30_WALLS_EXTERNAL
31_WALLS_INTERNAL
40_SLABS
41_ROOFS
50_OPENINGS
51_WINDOWS
52_DOORS
60_SHADING
90_HELPER_GEOMETRY
99_ISSUES
```

Die Layerstruktur ersetzt keine Objektattribute.

### 16.2 IFC

Wenn IFC ausgegeben wird:

- dokumentiere die verwendete IFC-Version,
- erhalte stabile IDs und Typbezüge,
- dokumentiere nicht übertragbare Informationen,
- prüfe insbesondere physische Verschattungselemente,
- gehe nicht davon aus, dass ein IFC-Import automatisch das vollständige interne Simulationsmodell abbildet.

Fehlende oder nicht übertragene Informationen müssen im Validierungsbericht erscheinen.

### 16.3 Hilfsgeometrie

Temporäre oder abgeleitete Hilfsgeometrie ist separat zu kennzeichnen und darf nicht als freigegebenes Bauteil interpretiert werden.

---

## 17. Geometrieprüfung

Prüfe abhängig von der Detaillierungsstufe mindestens:

- geschlossene Volumenkörper,
- konsistente Einheiten,
- korrekten Modellmaßstab,
- korrekte Gesamtmaße,
- korrekte Geschosshöhen,
- eindeutige Geschosslagen,
- keine unbeabsichtigten Überlagerungen,
- keine unbeabsichtigten Lücken,
- Öffnungen innerhalb ihrer Host-Wände,
- plausible Wand-, Boden-, Decken- und Dachneigungen,
- konsistente Flächennormalen,
- eindeutige Raumbegrenzungen,
- plausible Raumflächen und Raumvolumina,
- eindeutige Host-Beziehungen,
- eindeutige Objekt-IDs,
- gültige Typ-Codes,
- gültige Katalogreferenzen,
- Übereinstimmung zwischen YAML und Geometriemodell.

---

## 18. Fachliche Plausibilisierung

Führe zusätzlich Plausibilitätsprüfungen durch.

Beispiele:

- Geschossflächen passen zu den Gebäudeabmessungen,
- Summe der Raumflächen überschreitet die Geschossfläche nicht ohne Erklärung,
- Fenster liegen nicht außerhalb von Wand- oder Geschossgrenzen,
- Brüstungshöhen und Fensterhöhen sind geometrisch möglich,
- Türen schneiden nicht unbeabsichtigt Decken oder angrenzende Bauteile,
- Dachgeometrie passt zur Gebäudehöhe,
- Wanddicken sind innerhalb einer Konstruktion konsistent,
- Öffnungsanteile liegen in einem zulässigen Bereich von `0.0` bis `1.0`,
- Nordrichtung ist eindeutig,
- Katalogreferenzen passen zum Objekttyp,
- physische Verschattung besitzt eine nachvollziehbare räumliche Beziehung zum Gebäude.

Plausibilitätsgrenzen dürfen nicht als normative Grenzwerte ausgegeben werden, sofern keine konkrete Quelle vorliegt.

---

## 19. Annahmen und Ableitungen

Jede Annahme benötigt mindestens:

```text
assumption_id
description
reason
affected_objects
source_gap
status
impact
requires_confirmation
```

Jede Ableitung benötigt mindestens:

```text
derivation_id
target_field
method
input_references
result
unit
confidence
status
```

Mögliche Auswirkungsstufen:

```text
low
medium
high
critical
```

Annahmen mit `high` oder `critical` dürfen vor einer finalen Freigabe nicht unbemerkt bestehen bleiben.

---

## 20. Validierungsbericht

Erstelle einen Validierungsbericht in YAML und Markdown.

Jede Prüfung erhält:

```text
check_id
category
object_id
requirement
result
severity
message
source_reference
recommended_action
```

Mögliche Ergebnisse:

```text
valid
warning
error
pending
not_applicable
```

Mögliche Schweregrade:

```text
info
minor
major
critical
```

Prüfe mindestens:

- erforderliche Projektattribute vorhanden,
- Modellrevision eindeutig,
- Einheiten eindeutig,
- Nordrichtung definiert,
- Objekt-IDs eindeutig,
- Bauteilkennungen gültig,
- Katalogreferenzen auflösbar oder als offen markiert,
- Bauteile entsprechend der Detaillierungsstufe geschlossen,
- Öffnungen besitzen Host-Wände,
- Öffnungen liegen innerhalb der Host-Wände,
- Wandanschlüsse eindeutig oder als offen markiert,
- keine ungewollten Überlappungen,
- keine unbeabsichtigten Lücken,
- Gesamtmaße korrekt,
- Bauteildicken korrekt,
- Räume geometrisch plausibel,
- Einbautiefen definiert, sofern erforderlich,
- physischer Sonnenschutz ausreichend beschrieben,
- Regelungsangaben nicht fälschlich als Gebäudegeometrie behandelt,
- Annahmen dokumentiert,
- Ableitungen dokumentiert,
- YAML und Geometriemodell konsistent,
- nicht übertragbare Informationen dokumentiert.

---

## 21. Ausgabepaket

Erzeuge nach Freigabe nach Möglichkeit folgende Struktur:

```text
ma_building_option_a_output/
├── README.md
├── manifest.yaml
├── building_model_specification.yaml
├── building_geometry.3dm
├── building_geometry.ifc
├── object_register.csv
├── attribute_register.csv
├── assumptions.yaml
├── derivations.yaml
├── unresolved_items.yaml
├── validation_report.yaml
├── validation_report.md
└── source_mapping.yaml
```

Nicht erzeugte optionale Dateien bleiben im Manifest mit Begründung aufgeführt.

Beispiel:

```yaml
files:
  - path: building_geometry.3dm
    status: not_created
    reason: "Rhino-Dateierzeugung in der verwendeten Umgebung nicht verfügbar"
```

---

## 22. Anforderungen an die Ausgabe

### 22.1 Sprache und Benennung

- menschenlesbare Inhalte in deutscher Sprache,
- maschinenlesbare Schlüssel in englischem `snake_case`,
- IDs in Großbuchstaben mit Bindestrich,
- Einheiten nicht in Feldnamen verstecken, außer bei eindeutig projektspezifischen Feldern wie `area_m2`.

### 22.2 Vollständigkeit

Gib nach der Modellgenerierung aus:

1. erzeugte Dateien,
2. Modellrevision,
3. `BuildingModelSpecification`,
4. Geometriemodell oder begründeten Hinweis, weshalb kein Geometriemodell erzeugt wurde,
5. Objektliste,
6. Attributliste,
7. Quellenzuordnung,
8. Annahmen,
9. Ableitungen,
10. ungeklärte Punkte,
11. Validierungsbericht,
12. bekannte Einschränkungen,
13. empfohlene nächste Bearbeitungsschritte.

### 22.3 Keine Scheingenauigkeit

Nicht belastbar bekannte Werte dürfen nicht mit unnötiger numerischer Genauigkeit ausgegeben werden.

Beispiele:

- angenommene Wanddicke nicht ohne Grundlage auf drei Nachkommastellen festlegen,
- aus einem unscharfen Bild abgeleitete Maße als Näherung kennzeichnen,
- konzeptionelle Fenster nicht als Ausführungsplanung darstellen.

---

## 23. Übergabe an `ma_building`

Die Ausgabe muss so strukturiert sein, dass `ma_building`:

- Objekte eindeutig identifizieren kann,
- Geometrie und Attribute zusammenführen kann,
- Typ- und Katalogreferenzen auflösen kann,
- fehlende Angaben erkennen kann,
- Datenherkunft und Annahmen prüfen kann,
- Orientierungen auswerten kann,
- Räume und Bauteile weiterverarbeiten kann,
- spätere manuelle Korrekturen zulässt,
- eine neue Gebäuderevision erzeugen kann.

Die Übergabe darf keine vollständige thermische Zonierung und kein programmspezifisches Simulationsmodell voraussetzen.

---

## 24. Antwortformat vor der Freigabe

Antworte vor der Modellfreigabe in dieser Struktur:

```markdown
# Eingangsanalyse

## Erkannte Quellen

## Erkannte Projekt- und Gebäudedaten

## Erkannte Geschosse und Räume

## Erkannte Bauteile und Konstruktionen

## Erkannte Öffnungen

## Erkannte Verschattung

## Erkannte Katalogreferenzen

## Gewählter oder empfohlener Detaillierungsstand

## Widersprüche

## Fehlende Pflichtangaben

## Vorgeschlagene Annahmen

## Notwendige Rückfragen

## Modellierungsplan

## Geplante Ausgabedateien

## Geplante Validierungsprüfungen

## Freigabestatus
pending
```

---

## 25. Antwortformat nach der Freigabe

Antworte nach der Modellgenerierung in dieser Struktur:

```markdown
# Modellgenerierung abgeschlossen

## Modellidentität und Revision

## Erzeugte Dateien

## Nicht erzeugte optionale Dateien

## Zusammenfassung des Gebäudemodells

## Objektanzahl nach Typ

## Verwendete Katalogreferenzen

## Annahmen und Ableitungen

## Ungeklärte Punkte

## Validierungsergebnis

## Bekannte Einschränkungen

## Nächste Bearbeitungsschritte
```

---

## 26. Meine Gebäudebeschreibung

[Hier die konkrete Gebäudebeschreibung sowie verfügbare Pläne, Bilder, Tabellen, CAD-Dateien, IFC-Dateien und Katalogreferenzen einfügen.]
