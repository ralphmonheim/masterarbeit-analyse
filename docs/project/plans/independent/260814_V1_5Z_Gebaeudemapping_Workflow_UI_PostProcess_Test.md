# Unabhaengiger Umsetzungsplan – V1-5Z-Gebaeudemapping, Workflow-UI und PostProcess-Test

Datum: 2026-08-14
Planpfad: \`docs/project/plans/independent/260814_V1_5Z_Gebaeudemapping_Workflow_UI_PostProcess_Test.md\`
Planart: unabhaengiger Sol-Plan, keine P-Nummer
Freigabestatus: \`Freigabe zur Umsetzung\` am 2026-08-14 erteilt
B2-Rechtegate: fuer die konkret genannten Viewer-/IFC-Dateien erfuellt
Umsetzungsstand: in Umsetzung (Baseline, B1/B2, C-Teilslice, H-Reihenfolge und I-Konfliktvertrag am 2026-08-14 umgesetzt; weitere Pakete offen)

## Umsetzungsnachweis 2026-08-14 (Zwischenstand)

- B0: Dirty-Worktree dokumentiert; keine fremden Aenderungen zurueckgesetzt.
- B1: `ma_building.reference_mapping` fuehrt die fuenf direkten IDA-5Z-Zonalsummen mit Vorrang und bewahrt IDM-Segmente nur als Details samt Konfliktstatus.
- B2: Viewer-Excel und bytegleiche IFC werden lokal gehasht und nur ueber einen expliziten GlobalId-Link angereichert; ohne Link erfolgt kein Raten.
- C: OGD von OG West/Ost ist als `uppermost_storey_ceiling` mit Randbedingung `unconditioned_attic` sichtbar. Wegen fehlendem U-Wert/Temperaturfaktor ist die Bilanz korrekt `PARTIAL`.
- H: Der V1-PreProcess folgt `Projekt -> Wetter -> Gebaeude -> Technik -> Zonen`; die Technik-Zonen-Integration wird im Zonen-Gate geprueft.
- I: Widerspruechliche PRN-Stuetzstellen bleiben im Standardvertrag erhalten und blockieren damit Integrationen. Eine getrennte Anzeigeprojektion ist als solche markiert.
- Tests: fokussiert `27 passed`; die UI-Shell `139 passed`. Der Komplettlauf erreichte 100 %, lief im Sandbox-Zeitlimit jedoch ohne abschliessende pytest-Zusammenfassung aus und ist daher nicht als bestanden bewertet.
- Noch offen: eigener 29Z-Building-Quellstand, P018-Run-Manifest-Migration, vollstaendige Workflow-UI, konservativer 29Z/ALT-Prepare-Durchlauf, Tabellen-/Diagramm-Integration, Prozessmessung und Abschlussbericht.

## Qualitaetsbefunde

### Blocker

1. **Der aktuelle Dirty Worktree ueberlappt bereits mit zentralen Zieldateien.**

   Betroffen sind unter anderem:

   - \`config/ma_building/examples/small_office_5z_endvariant_02_building_spec.yaml\`
   - \`config/ma_zones/examples/small_office_5z_endvariant_02_zone_spec.yaml\`
   - \`src/ma_variants/project_studies.py\`
   - \`src/ma_workflow/small_office_v1_preprocess.py\`
   - \`src/ma_data_preparation/ida_ice.py\`
   - \`src/ma_data_preparation/models.py\`
   - \`src/ma_data_preparation/services.py\`
   - \`src/ma_ui/streamlit_app/module_views/parameters_view.py\`
   - \`src/ma_ui/streamlit_app/pages/variants.py\`
   - zugehoerige Tests und Projektdokumente.

   Der Umsetzungs-Chat muss vor jeder Aenderung fuer jede betroffene Datei \`git diff\` pruefen. Ist die Urheberschaft oder Vereinbarkeit einer Ueberlappung nicht eindeutig, stoppt nur das betroffene Paket. Fremde Aenderungen duerfen weder ueberschrieben, zurueckgesetzt noch nebenbei bereinigt werden.

2. **Die aktuelle 29Z-Erzeugung wird durch die bereits begonnenen 5Z-Aenderungen funktional zerstoert.**

   \`src/ma_zones/small_office_29z.py::build_small_office_29z_draft()\` laedt derzeit \`load_small_office_5z_endvariant_02_building_spec()\` und erwartet daraus 29 \`SPACE-SYNTH-*\`-Raeume. Der Dirty-Worktree-Stand derselben 5Z-Spezifikation enthaelt nur noch fuenf direkte IDA-Zonenraeume. Damit erzeugt der angebliche 29Z-Entwurf nur noch fuenf falsch benannte Zonen.

   Vor der 5Z-Migration muss deshalb ein eigener 29Z-Gebaeudequellstand mit eigenem Loader gesichert werden. Ein Test muss exakt 5 beziehungsweise 29 Zonen und getrennte Raumregister nachweisen.

3. **Die obersten Geschossdecken sind geometrisch eingetragen, werden thermisch aber weiterhin ausgeschlossen.**

   Die aktuelle Dirty-Konfiguration fuehrt OG West/Ost als:

   - \`element_type: uppermost_storey_ceiling\`
   - \`construction_code: GD\`

   \`src/ma_building/thermal.py::_EXCLUDED_INTERNAL_CODES\` schliesst jedoch jedes \`GD\` aus. \`_CATEGORY_BY_CODE\`, \`_u_value_for_code()\` und \`_temperature_factor_for_code()\` kennen keine oberste Geschossdecke gegen einen unbeheizten Bereich. Gleichzeitig steht in der Konfiguration \`thermal_envelope_complete: true\`.

   Dadurch kann die Software eine scheinbar vollstaendige Huelle melden, obwohl die oberen thermischen Begrenzungen beider OG-Zonen aus der Bilanz verschwinden. Die Bauteilart muss nach Randbedingung beziehungsweise \`element_type\` unterschieden und sichtbar \`PARTIAL\` bleiben, solange U-Wert oder Temperaturkorrektur nicht bestaetigt sind.

4. **Ein wahrer durchgaengiger Ergebnisnachweis ist mit den vorhandenen Dateien nur ueber ein dokumentiertes manuelles Gate moeglich.**

   Die jetzt erzeugten 30 Optimierungs- und acht Sensitivitaetsfaelle sind nicht die belegte Herkunft der vorhandenen 5Z-, 29Z- oder ALT-PRN-Dateien. Diese Dateien duerfen nicht nachtraeglich mit neuen \`RUN-ID\`/\`VAR-ID\`-Werten etikettiert werden.

   Der Test muss deshalb zwei ehrlich getrennte Nachweise fuehren:

   - PreProcess bis zum manuellen IDA-Gate mit neu erzeugtem RUN-Paket;
   - Main-/PostProcess-Funktionstest mit einem eigenen Importmanifest fuer die bereits vorhandenen Ergebnisse.

   Ohne eine spaetere tatsaechliche Simulation derselben erzeugten Varianten darf der Bericht keinen kausal geschlossenen End-to-End-Lauf behaupten.

### Wichtig

5. **Workflow-Reihenfolge und aktueller Katalog widersprechen dem fuehrenden Zielvertrag.**

   P007/P027 verlangen:

   \`\`\`text
   Projekt → Wetter → Gebaeude → Technik → Zonen → Parameter
   \`\`\`

   \`src/ma_workflow/catalog.py\`, \`src/ma_workflow/small_office_v1_preprocess.py\` und \`tests/test_ma_ui_shell.py\` fuehren aktuell dagegen \`Zonen → Technik\`. Die technische UI besitzt zudem historischen Zonenbezug, obwohl P014 systemweite Technik vor der zonalen Zuordnung vorsieht.

   Der V1-Test darf diese Abweichung nicht als korrekt bestaetigen. Zuerst ist die gerichtete Uebergabe \`ma_technical → ma_zones\` konsistent zu machen; danach werden Workflow- und Direktansicht gegen dieselbe Reihenfolge getestet.

6. **Der historische SmallOffice-Runner nutzt noch nicht durchgehend den finalen P018-Vertrag.**

   \`src/ma_workflow/small_office_v1_preprocess.py::_simulation_setup_action()\` verwendet \`build_run_manifest()\` und \`materialize_run_package()\` je Variante. Der Zielvertrag mit einem wissenschaftlichen RUN, einer VSEL, einem gemeinsamen Setup und mehreren VAR existiert bereits als:

   - \`ma_simulation_setup.models.SimulationRunV1\`
   - \`ma_simulation_setup.models.RunManifestV1\`
   - \`ma_simulation_setup.services.build_run_manifest_v1()\`
   - \`ma_simulation_setup.services.materialize_run_package_v1()\`.

   Der aktive SmallOffice-/UI-Aufrufer muss auf diesen Vertrag migriert werden. Sensitivitaetsfaelle duerfen nur gemeinsam in einen RUN, wenn ihr Setup wirklich identisch ist; insbesondere verschiedene Wetterfaelle duerfen nicht unter einem gemeinsamen Setup zusammengezwungen werden.

7. **Die Dirty-Aenderung der 29Z-Duplikatbehandlung trifft eine unbestaetigte fachliche Annahme.**

   \`src/ma_data_preparation/ida_ice.py::_normalize_ida_records()\` ersetzt bei widerspruechlichen Werten am selben Zeitstempel den frueheren durch den letzten Wert. Diese \`last value wins\`-Regel ist fachlich noch nicht bestaetigt und steht im Konflikt mit P036, wonach nicht eindeutige Reihen nicht integriert werden.

   Bis zur Klaerung der IDA-Ereignis- und Periodensemantik gilt:

   - widerspruechliche Rohstuetzstellen bleiben nachweisbar;
   - eine optionale Anzeigeprojektion darf getrennt erzeugt werden;
   - Energieintegration und belastbare Kennwerte bleiben fuer diese Reihe \`NOT_READY\`;
   - keine Konfliktaufloesung darf als stiller Bestandteil der Standardisierung erfolgen.

8. **IDM/IDC duerfen nicht durch Aufweichen des Ergebnisimport-Schutzes eingelesen werden.**

   \`src/ma_import_simulation/adapters/ida_ice/results.py\` schliesst IDM/IDC bewusst ueber \`PROTECTED_SUFFIXES\` aus. Diese Schutzgrenze bleibt unveraendert.

   Das freigegebene 5Z-Gebaeudemapping und der Technikabgleich benoetigen schmale, getrennte Referenzleser in \`ma_building\` beziehungsweise \`ma_technical\`. Sie sind keine Ergebnisimportadapter und duerfen keine automatische IDA-Modellmanipulation vorbereiten.

9. **Der bestehende Gebaeudevertrag reicht fuer die geforderte Vollprovenienz nicht allein aus.**

   \`ma_building.models.PhysicalElement\` besitzt Orientierung und Raumbezug, aber keine Feldprovenienz oder IFC-ID. \`Opening\` besitzt weder Anzahl noch eigene Orientierung oder Quellenreferenzen.

   Die stabilen B1-Fach-IDs duerfen nicht von optionalen IFC-GlobalIds abhaengen. Fuer B1/B2 ist deshalb ein additiver Mapping-/Provenienzvertrag erforderlich, statt die bestehenden Kernobjekte mit unsicheren Fremdformatdetails zu ueberladen.

10. **Das vorhandene Prozessmappen-Skript ist fuer reale Messdaten potenziell destruktiv.**

    \`Skripte/build_process_measurement_workbook.py::reset_sheet()\` entfernt vorhandene Auswertungsblaetter und erzeugt sie neu. Ein erneuter Lauf kann manuell ergaenzte Zeiten verlieren.

    Vor der Nutzung an der echten Arbeitsmappe muss der Schreiber auf stabile Zeilen-IDs beziehungsweise additive Aktualisierung umgestellt und an einer temporaeren Testmappe geprueft werden. Eine Sicherungskopie ist vor dem ersten externen Schreibzugriff verpflichtend.

11. **Die PRN-Leistungs-, Energie- und Zeitsemantik ist weiterhin offen.**

    \`src/ma_data_preparation/ida_ice.py::read_prn_as_standardized_series()\` klassifiziert derzeit alle Reihen als \`INSTANTANEOUS\`; viele leistungs- oder energienahe IDA-Spalten koennen jedoch Intervallwerte darstellen. \`prn_column_unit()\` leitet fuer zahlreiche \`q*\`-Spalten \`W\` aus dem Namen ab.

    Bis OP-017 geschlossen ist, bleiben daraus abgeleitete Energie- und Leistungsaussagen \`PARTIAL\`. Temperatur- und andere eindeutig lesbare Verlaeufe duerfen fuer einen klar gekennzeichneten Funktionstest verwendet werden.

### Optional

12. **Die 3DM-Datei ist fuer V1 nicht erforderlich.**

    Die Datei kann mit Name, Groesse und SHA-256 im Quellenmanifest erscheinen. Eine Rhino-Bibliothek oder Inhaltsverarbeitung wuerde keinen notwendigen Zusatznutzen gegenueber 5Z-IDM/Excel, Viewer-Excel und IFC liefern und bleibt ausgeschlossen.

## Finaler Arbeits-Prompt

Du agierst als Senior-Python-Entwickler und technischer Architekturberater fuer die V1-Fallstudie der Masterarbeitssoftware.

Setze einen reproduzierbaren, nachvollziehbaren V1-Referenz- und Testlauf auf Basis des bestehenden Codes um. Hauptfall ist das direkte IDA-5Z-Modell. Erfasse fuer alle fuenf Zonen die Aussenbauteile einschliesslich Orientierung, Brutto- und Nettoflaeche, Fenster- und Tueranzahl/-flaeche, Boden sowie oberer thermischer Begrenzung. Die Lobby besitzt ein Dach; OG West und OG Ost besitzen jeweils eine oberste Geschossdecke gegen einen unbeheizten, nicht zur thermischen Huelle gehoerenden Bereich.

Verwende direkte 5Z-IDM und \`Dimensionierung_5Z_Eingabe_Allgemein.xlsx\` als fuehrende thermische Zonenquelle. Verwende die fuer 5Z zugeschnittenen Aussenbauteile der Viewer-Excel und die bytegleiche SmallOffice-IFC nachgelagert zur lokalen GlobalId-, Host- und Beziehungsanreicherung. B1 muss voll funktionsfaehig bleiben, wenn keine IFC-ID vorliegt. Verarbeite die 3DM-Datei nicht inhaltlich.

Pruefe und vervollstaendige danach die V1-Kette:

\`\`\`text
Projekt → Wetter → Gebaeude → Technik → Zonen → Parameter
→ VSP/VVER und fruehe Auswahl
→ Dimensionierung
→ finaler VCAT/VSEL/VGEN
→ Simulation-Setup
→ manuelle IDA-Uebergabe
→ Ergebnisimport
→ standardized → prepared
→ Tabellen, Diagramme und deskriptive Bewertung
→ Prozesszeitvergleich
\`\`\`

Die Optimierung umfasst genau fuenf Temperaturbaender und sechs gemeinsame Leistungsfaktoren:

\`\`\`text
cooling.factor = heating.factor
\`\`\`

Damit entstehen genau 30 Optimierungsfaelle. Die Sensitivitaet umfasst getrennt vier Wetter- und vier Belegungs-OFAT-Faelle. Optimierung und Sensitivitaet werden nicht miteinander gekreuzt. Der vorhandene 156er-Demoraum bleibt isoliert und darf keine wissenschaftliche Referenz oder Simulationsergebnis-Provenienz erhalten.

Teste die komplette Streamlit-UI sowohl ueber die Workflowansicht als auch ueber den direkten Modulzugriff. Beide Ansichten muessen dieselben Backendvertraege und denselben Projektzustand verwenden. Dokumentiere erreichbare Funktionen, Laufzeiten, Warnungen, Fehler, Datenqualitaet, erzeugte Tabellen und Diagramme.

Nutze vorhandene 5Z-PRN fuer den Haupt-PostProcess-Test, 29Z fuer variable Stützstellen und Prepare sowie ALT fuer historische Vergleichsgrafiken. Behaupte keine kausale Verbindung zwischen neu erzeugten Variantenpaketen und bestehenden Ergebnisdateien. Behaupte ohne OP-017/OP-018-Gate weder normativen Komfort noch eine wissenschaftlich belastbare Energie-, Einsparungs- oder Bestvariantenbewertung.

Keine neue Abhaengigkeit, keine automatische IDA-Steuerung, keine 3DM-Inhaltsverarbeitung, keine externe oder Cloud-Verarbeitung, keine Loeschung, kein Commit, Push oder Release.

## Ziel

Der Abschluss liefert:

1. ein reproduzierbares 5Z-Zonen-/Aussenbauteilmapping;
2. einen eigenstaendigen B1-Kernstand ohne IFC-Abhaengigkeit;
3. eine nachvollziehbare B2-Anreicherung mit Viewer-/IFC-IDs;
4. getrennte, funktionsfaehige 5Z- und 29Z-Konfigurationen;
5. sichtbare und technisch erzwungene Kopplungsregeln;
6. die kanonische Varianten-, Dimensionierungs- und Setup-Kette;
7. einen dokumentierten manuellen IDA-Uebergabepunkt;
8. einen getrennt provenienzgesicherten Import-/Prepare-/Analyse-Test mit vorhandenen Daten;
9. datenkompatible Tabellen und Diagramme;
10. eine UI-Funktionsmatrix;
11. eine Laufzeit-, Fehler- und Prozessvergleichstabelle;
12. eine knappe Liste verbleibender fachlicher Gates.

## Verbindliche Quellen- und Konflikthierarchie

### Projekt- und Architekturwahrheit

1. P007 und einschlaegige Nutzerentscheidungen
2. P012 bis P018 sowie P027, P029, P030 und P036 innerhalb ihres jeweiligen Modulscopes
3. \`PLAN_INDEX.md\`, \`PLAN_STATUS.md\` und offene Entscheidungen als Status- und Gatewahrheit
4. aktueller Code, Konfiguration und Tests als Ist-Nachweis, nicht als eigenstaendige Zielarchitektur

### 5Z-Datenwahrheit

| Prioritaet | Quelle | Fuehrende Rolle |
|---:|---|---|
| 1 | \`Dimensionierung_5Z_Eingabe_Allgemein.xlsx\` | zonale Flaechen, Volumen und bestaetigte Huellkategorien/-summen |
| 2 | fuenf direkte 5Z-Zonen-IDM | Segmentierung, Orientierung, Hostbeziehungen, Oeffnungsanzahl und Geometrie |
| 3 | Viewer-Excel | fuer 5Z zugeschnittene Aussenbauteile, GlobalIds, Klassen und explizite Beziehungen |
| 4 | bytegleiche SmallOffice-IFC | Existenz- und Klassenpruefung der Viewer-GlobalIds und Beziehungen |
| 5 | IDC | Struktur-/Formkontext; numerische Werte nur bei eindeutigem Instanzcharakter |
| 6 | versionierte YAML | aktueller Softwarestand und Migrationsausgangspunkt |
| 7 | 29Z und ALT | Vergleich, Plausibilisierung und Funktionstest, nicht 5Z-Quellwahrheit |

Fuer Konflikte innerhalb der ersten beiden Quellen gilt:

- Excel fuehrt die zonale quantitative Gesamtsumme.
- IDM fuehrt die Detailsegmentierung und Hoststruktur.
- Rohwerte beider Quellen bleiben erhalten.
- Abweichungen werden nicht gemittelt oder still skaliert.
- Eine nicht schliessende Detailsumme erhaelt einen Konfliktstatus.
- Ohne bestaetigte Aufloesung darf daraus keine scheinbar exakte orientierte Gesamtsumme erzeugt werden.

## Bereits bestaetigte Referenzwerte

| Zone | Flaeche | Volumen | opake Aussenwand | Fenster | Tueren | obere Begrenzung |
|---|---:|---:|---:|---:|---:|---|
| Lobby | 65,40 m² | 458,1 m³ | 34,49 m² | 72,22 m² | 0,00 m² | Dach 77,95 m² |
| EG West | 162,60 m² | 438,9 m³ | 79,58 m² | 41,51 m² | 3,78 m² | keine Dachflaeche |
| EG Ost | 67,96 m² | 183,5 m³ | 59,72 m² | 11,56 m² | 1,89 m² | keine Dachflaeche |
| OG West | 162,60 m² | 438,9 m³ | 85,94 m² | 41,51 m² | 3,78 m² | oberste Geschossdecke 162,552 m² |
| OG Ost | 67,96 m² | 183,5 m³ | 64,30 m² | 10,71 m² | 1,89 m² | oberste Geschossdecke 67,964 m² |

Die obersten Geschossdecken sind keine Dachflaechen. \`Q_ROOF = 0\` in den OG-Zonen ist deshalb kein Fehler.

## Freigegebene lokale B2-Objekte

- Viewer-Excel:
  \`%USERPROFILE%\Downloads\ifc_properties_46705e9f17.xlsx\`
  SHA-256: \`D7DDBC73D15A8CFF315AADFC42ABEE0877AA09171E5E4CE895F24E8420E1686D\`

- externe SmallOffice-IFC:
  \`%USERPROFILE%\OneDrive - Frankfurt UAS\Master\UAS - 6. Semester\MASTER-THESIS\TEIL1.2_IDA\Gebäude\SmallOffice_d_IFC2x3.ifc\`

- lokale bytegleiche IFC:
  \`data/ma_building/input/ifc/SmallOffice_d_IFC2x3.ifc\`

- IFC-SHA-256:
  \`B933A06810A08EE6114E709861A822A06A778962A01567287CE879413CBB3055\`

- 3DM nur als Metadatenobjekt:
  SHA-256 \`7909142276EF69468DC89A3FB93C604FB136E7C50F42E559EBB702E82383DF52\`

Die Viewer-Arbeitsmappe besitzt das Blatt \`IFC Properties\` mit 278 Zeilen und 5.553 Spalten. Die Basisspalten enthalten unter anderem IFC-Klasse, GlobalId und LocalId. Rohdateien werden nicht versioniert oder unnoetig kopiert.

## Scope

- Dirty-Worktree- und Vertragsaudit
- 5Z-IDM-/Excel-Kernmapping
- Viewer-/IFC-Anreicherung
- 5Z-/29Z-Konfigurationstrennung
- Lobby-Dach und oberste Geschossdecken
- Technik-/Nutzungsquerpruefung
- konkrete Parameter- und Variationsvertraege
- sichtbare Faktorkopplung
- VVER, Dimensionierung, VCAT, VSEL, VGEN
- P018-Multi-VAR-Runvertrag
- Workflow- und Direktansicht
- manueller IDA-Uebergabepunkt
- Ergebnisimport, Standardisierung und Prepare
- 5Z-/29Z-/ALT-Tabellen und Diagramme
- deskriptive Ergebnisbewertung
- Laufzeiten, Fehler und Prozessvergleich
- Tests und bestehende Projektdokumentation

## Nicht-Ziele

- automatische IDA-Ausfuehrung oder Modellmanipulation
- produktiver allgemeiner IFC-Import
- 3DM- oder Rhino-Parser
- neue Python-Abhaengigkeiten
- Cloud- oder externe Datenverarbeitung
- normative Komfortbewertung
- automatische Bestvariantenauswahl
- Kreuzung von Optimierung und Sensitivitaet
- Ersetzung vorhandener Diagrammdesigns
- Loeschung historischer Daten oder Konfigurationen
- Bereinigung fremder Dirty-Worktree-Aenderungen
- Commit, Push, Tag oder Release

## Betroffene bestehende Bereiche

### Gebaeude und Zonen

- \`src/ma_building/models.py\`
- \`src/ma_building/validation.py\`
- \`src/ma_building/thermal.py\`
- \`src/ma_building/demo_loader.py\`
- \`src/ma_building/ifc_lite_import.py\`
- \`src/ma_zones/small_office_29z.py\`
- \`config/ma_building/examples/\`
- \`config/ma_zones/examples/\`
- \`src/ma_ui/streamlit_app/module_views/building_view.py\`
- \`src/ma_ui/streamlit_app/module_views/zones_view.py\`

### Technik, Parameter, Varianten und Dimensionierung

- \`src/ma_technical/\`
- \`src/ma_parameters/\`
- \`src/ma_dimensionierung/\`
- \`src/ma_variants/project_studies.py\`
- \`src/ma_variants/small_office_v1.py\`
- \`src/ma_variants/finalization.py\`
- \`src/ma_variants/vver_selection.py\`
- \`config/ma_variants/studies/small_office_v1.yaml\`
- \`config/ma_variants/studies/small_office_v1_random_156.yaml\`
- \`src/ma_ui/streamlit_app/module_views/parameters_view.py\`
- \`src/ma_ui/streamlit_app/pages/variants.py\`
- \`src/ma_ui/streamlit_app/module_views/dimensioning_view.py\`

### Setup, Import, Prepare und Analyse

- \`src/ma_simulation_setup/\`
- \`src/ma_import_simulation/adapters/ida_ice/\`
- \`src/ma_data_preparation/\`
- \`src/ma_analyse/analysis/master_thesis_dataset.py\`
- \`src/ma_analyse/analysis/tables/\`
- \`src/ma_analyse/stage_2_optimization/historical.py\`
- \`src/ma_ui/streamlit_app/module_views/simulation_setup_view.py\`
- \`src/ma_ui/streamlit_app/module_views/import_ida_view.py\`
- \`src/ma_ui/streamlit_app/module_views/analyse_view.py\`

### Workflow und Prozessmessung

- \`src/ma_workflow/catalog.py\`
- \`src/ma_workflow/small_office_v1_preprocess.py\`
- \`src/ma_ui/streamlit_app/navigation.py\`
- \`src/ma_ui/workflow_view.py\`
- \`Skripte/build_process_measurement_workbook.py\`
- lokale Prozessmappe \`Prozesskostenvergleich_Manuell_vs_Automatisiert.xlsx\`

## Geordnete Umsetzungspakete

### Paket 0 – Preflight, Bestandsschutz und Baseline

1. \`git status --short\` und gezielte Diffs erfassen.
2. Relevante Dirty-Dateien nach Urheberschaft und Ueberlappung klassifizieren.
3. Aktuelle gezielte Tests ausfuehren, ohne Konfiguration oder Daten zu veraendern.
4. Einen Baseline-Testbericht mit:
   - Branch und HEAD,
   - Testkommando,
   - Laufzeit,
   - Fehlern,
   - vorhandenen Dirty-Dateien,
   - erreichbaren lokalen Datenquellen
   erzeugen.
5. Bei unklarer Ueberlappung das betroffene Paket stoppen.

Pruefungen:

- keine Datei wird durch den Preflight veraendert;
- alle spaeteren Aenderungen lassen sich gegen die Baseline abgrenzen.

### Paket A – Quellenmanifest und Reproduzierbarkeit

1. Ein kleines Quellenmanifest im bestehenden Gebaeude-/Testausgabekontext definieren.
2. Je Quelle speichern:
   - logische Quellen-ID,
   - Dateiname,
   - SHA-256,
   - Modellrolle,
   - erlaubte Verwendung,
   - Verifikationsstatus,
   - keine Rohinhalte.
3. 3DM nur mit Metadaten auffuehren.
4. Rohdateien nicht kopieren oder versionieren.

Tests:

- Hashaenderung wird erkannt;
- fehlende Datei erzeugt einen klaren Status;
- absolute externe Pfade erscheinen nicht in veroeffentlichungsfaehigen Ergebnisartefakten.

### Paket B1 – Eigenstaendiges 5Z-Kernmapping aus IDA

1. Einen schmalen Referenzleser in \`ma_building\` anlegen.
2. Nur die fuenf ausdruecklich freigegebenen Zonen-IDM und die 5Z-Eingabe-Excel lesen.
3. Pro Zone erfassen:
   - Wandsegment und Modellorientierung,
   - Bruttoflaeche,
   - Fenster- und Tuerobjekte,
   - Anzahl und Flaeche,
   - Hostbeziehung,
   - opake Nettoflaeche,
   - Boden,
   - Dach oder oberste Geschossdecke,
   - Quelle je Feld,
   - Konfliktstatus.
4. Nur explizit externe vertikale Flaechen als Aussenwand werten.
5. Innenfenster und Innenbauteile ausschliessen.
6. Stabile B1-IDs erzeugen, die ohne IFC-GlobalIds bestehen bleiben.
7. Summen gegen die 5Z-Excel pruefen; keine stille Skalierung.

Vorgesehener Mappingvertrag:

\`\`\`text
zone_id
component_id
component_type
boundary_condition
orientation_model_deg
orientation_label
gross_area_m2
opening_type
opening_count
opening_area_m2
opaque_net_area_m2
host_component_id
ida_source_reference
viewer_global_id optional
ifc_local_id optional
source_hash
mapping_status
diagnostics
\`\`\`

Tests mit kleinen synthetischen IDM-/XLSX-Fixtures:

- genau fuenf Zonen;
- externe/interne Flaechen werden getrennt;
- Fenster und Tueren bleiben beim Host;
- Anzahl und Flaeche werden getrennt;
- Konflikte bleiben sichtbar;
- B1 funktioniert ohne Viewer-Excel und IFC.

### Paket B2 – Viewer-/IFC-Anreicherung

1. Vorhandenen dependency-freien STEP-Leser wiederverwenden beziehungsweise schmal oeffentlich refaktorieren.
2. Viewer-Excel mit \`openpyxl\` im Read-only-Modus lesen.
3. Nur benoetigte Spalten aufloesen:
   - IFC-Klasse,
   - GlobalId,
   - LocalId,
   - Name,
   - explizite Host-/Boundary-/Decomposition-Beziehungen.
4. Viewer-GlobalIds gegen die bytegleiche IFC pruefen.
5. B1-Komponenten nachgelagert anreichern.
6. Automatisches Matching nur bei:
   - exakter GlobalId oder
   - expliziter Viewer-/IFC-Beziehung.
7. Geometrieaehnlichkeit darf nur einen bestaetigungspflichtigen Kandidaten erzeugen.
8. Jede manuelle Bestaetigung speichert Quelle, Datum, bestaetigende Person und Begruendung.
9. Fehlende IFC-ID blockiert nicht B1.

Tests:

- identische GlobalId und Klasse werden uebernommen;
- doppelte GlobalId blockiert B2;
- Klassenkonflikt blockiert die Zuordnung;
- fehlende Beziehung erzeugt nur einen Kandidaten;
- Quellenhash und Bestaetigung sind reproduzierbar;
- keine Rohdatei wird geschrieben oder kopiert.

### Paket C – 5Z-/29Z-Trennung und thermische Bauteilrollen

1. Vor jeder 5Z-Aenderung einen eigenen 29Z-Gebaeudequellstand und Loader schaffen.
2. \`build_small_office_29z_draft()\` auf diesen 29Z-Loader umstellen.
3. Die 5Z-Spezifikation auf fuenf direkte IDA-Zonenraeume umstellen.
4. Orientierte Wandsegmente und Oeffnungen aus B1 statt nur einer Wandaggregation je Zone verwenden.
5. Bauteilrollen trennen:
   - Lobby: \`roof\`, Randbedingung Aussenluft;
   - OG West/Ost: \`uppermost_storey_ceiling\`, Randbedingung unbeheizter Bereich;
   - interne Geschossdecke: weiterhin nicht Teil der thermischen Huelle.
6. \`thermal.py\` nicht mehr allein nach \`construction_code == GD\` entscheiden lassen.
7. Oberste Geschossdecke in Tabellen und Huelle anzeigen.
8. Fehlenden U-Wert oder Temperaturkorrekturfaktor nicht erfinden; betroffene Berechnung bleibt \`PARTIAL\`.
9. Geometrische Vollstaendigkeit und thermische Berechnungsbereitschaft getrennt anzeigen.

Tests:

- 5Z hat exakt fuenf, 29Z exakt 29 Raeume/Zonen;
- beide Loader sind unabhaengig;
- Lobby-Dach wird als Dach bilanziert;
- OG-Decken erscheinen als oberste Geschossdecken;
- interne GD bleibt ausgeschlossen;
- fehlender OGD-U-Wert erzeugt keine scheinbar vollstaendige Transmissionsbilanz;
- Flaechen werden nicht doppelt gezaehlt.

### Paket D – Technik- und Nutzungsquerpruefung

1. Schmalen, read-only Referenzchecker fuer:
   - \`ahu.idm\`
   - \`plant.idm\`
   - \`heating.idm\`
   - \`cooling.idm\`
   - zugehoerige IDC-Strukturen
   erstellen.
2. Vergleichen:
   - Heiz-/Kuehlleistungen,
   - AHU und Volumenstroeme,
   - Systemreferenzen,
   - Zonenversorgung,
   - Sollwerte,
   - Luftwechsel,
   - Betriebszeiten,
   - interne Lasten.
3. IDC nur als Form-/Strukturquelle behandeln, sofern kein eindeutiger Instanzwert vorliegt.
4. Keine automatische Uebernahme bei mehrdeutiger Zuordnung.
5. Berichtsklassen:
   - identisch,
   - Rundung,
   - andere Modellstufe,
   - fehlt in Config,
   - widerspruechlich,
   - semantisch nicht vergleichbar.

Tests:

- eindeutige Instanzwerte werden zugeordnet;
- Formular-Defaults werden nicht als Modellwert uebernommen;
- mehrere moegliche Quellen blockieren nur die automatische Korrektur;
- Rohtext wird nicht im Bericht gespeichert.

### Paket E – Parametervertrag, Spannen und UI-Regel

1. Wissenschaftliche Dimensionen explizit speichern:
   - fuenf gekoppelte Sollwertbaender als Optionsliste;
   - sechs gemeinsame Kapazitaetsfaktoren als diskrete Liste;
   - vier Wetterreferenzen;
   - vier Belegungsreferenzen.
2. Keine freien Min-/Max-Kombinationen erzeugen, die nicht zu den festgelegten Baendern gehoeren.
3. Regel \`cooling.factor = heating.factor\` aus einer Backendwahrheit projizieren.
4. Regel schreibgeschuetzt in Parameter- und Variantenansicht zeigen.
5. Kandidatentabelle flach anzeigen:
   - Heizsollwert,
   - Kuehlsollwert,
   - Heizfaktor,
   - Kuehlfaktor,
   - Kopplungsstatus.
6. Abweichende Faktoren sichtbar blockieren.
7. 156er-Demoraum unveraendert als \`test_only\` halten.

Tests:

- genau 30 wissenschaftliche Optimierungskandidaten;
- genau acht getrennte OFAT-Kandidaten;
- niemals 480 Kombinationen;
- gleiche Faktoren in jeder Optimierungszeile;
- Backend lehnt ungleiche Faktoren ab;
- UI zeigt dieselbe Regel;
- Demo- und Wissenschaftskatalog besitzen getrennte Status-/Provenienzkennzeichnung.

### Paket F – VVER, Dimensionierung und finaler Variantenabschluss

1. Fuer jede StudyDirection beziehungsweise jeden StudyCase eine aktuelle VVER erzeugen.
2. Nur ausgewaehlte, dimensionierungsrelevante Kandidaten dimensionieren.
3. Kandidaten mit gleichem Dimensionierungseingang gruppieren.
4. Dimensionierungswerte ueber \`ma_dimensionierung\` erzeugen.
5. Ergebniszuordnung und Nachpruefung durchfuehren.
6. Finalen VCAT bilden.
7. VSEL nur als Abbildung der fruehen Auswahl auf finale VAR-IDs speichern.
8. VGEN aus dem finalen Katalog erzeugen.
9. Projektweite VAR-ID-Registry atomar und append-only speichern.
10. Optimierungs- und Sensitivitaetsprovenienz getrennt halten.

Tests:

- veralteter Upstream blockiert;
- nur VVER-ausgewaehlte Kandidaten werden dimensioniert;
- Gruppierung ist deterministisch;
- finale IDs entstehen erst nach Dimensionierung;
- VSEL trifft keine zweite Auswahl;
- Reload liefert identische Fingerprints;
- Teilfehler materialisieren keinen scheinbar vollstaendigen Abschluss.

### Paket G – P018-Runvertrag und manuelles IDA-Gate

1. Historischen SmallOffice-Aufrufer auf \`RunManifestV1\` migrieren.
2. Optimierungsvarianten mit identischem Setup in einem wissenschaftlichen RUN fuehren.
3. Sensitivitaeten nur bei identischem Setup gruppieren.
4. Unterschiedliche Wetter-Setups in getrennte RUNs aufteilen.
5. \`OutputRequirementProfile\` aus dem bestehenden \`ma_analyse\`-Katalog uebernehmen.
6. RUN-Paket transaktional materialisieren.
7. Manuelle IDA-Checkliste mit \`(RUN-ID, VAR-ID)\` erzeugen.
8. Keinen Simulationsstart implementieren.

Tests:

- ein RUN, eine VSEL, ein Setup, mehrere VAR;
- Setup-Konflikt blockiert gemeinsames Paket;
- fehlendes Outputprofil blockiert;
- veraltete Selection blockiert;
- keine CASE-ID oder \`SimulationCase\`;
- kein IDA-Prozess wird gestartet.

### Paket H – Workflowkatalog und gemeinsame UI-Anbindung

1. Zielreihenfolge in \`ma_workflow.catalog\` korrigieren:
   \`Gebaeude → Technik → Zonen\`.
2. Technikansicht auf systemweiten Technikstand ohne vorausgesetzte Zonenbearbeitung ausrichten.
3. Zonenansicht fuer die nachgelagerte Technikzuordnung verwenden.
4. Workflow- und Direktansicht auf dieselben Modulrenderer und Services verweisen lassen.
5. Keine zweite Persistenz- oder Statuslogik in der Workflowansicht einfuehren.
6. Projektzustand, Entwuerfe, Fingerprints und Ruecksprungkontext bei Ansichtswechsel erhalten.

Tests:

- Katalog, Navigation und UI besitzen dieselbe Reihenfolge;
- Workflowkarte oeffnet die vorhandene Modulansicht;
- Backendaktion wird nicht dupliziert;
- Ansichtswechsel veraendert keine Fachwerte;
- Reload erhaelt gespeicherte Werte;
- veraltete Nachfolger werden markiert, nicht geloescht.

### Paket I – Bestehende Ergebnisse importieren und vorbereiten

1. Ein getrenntes lokales Importmanifest fuer die vorhandenen Daten erzeugen.
2. Herkunft klar kennzeichnen:
   - 5Z-Dimensionierung,
   - 29Z-Dimensionierung,
   - ALT-Referenz und Faktorenvarianten.
3. Keine neuen Demo-RUN-IDs als Herkunft verwenden.
4. \`ma_import_simulation\` nur fuer PRN/HTML/XLSX nutzen.
5. IDM/IDC-Schutz im Ergebnisimport unveraendert lassen.
6. 5Z:
   - stuendliche Struktur,
   - Abdeckung,
   - Einheiten,
   - Zonenmapping,
   - \`standardized → prepared\`.
7. 29Z:
   - variable Stützstellen,
   - Duplikate,
   - Luecken,
   - \`dt_h\`,
   - konservativer Konfliktstatus.
8. ALT:
   - Dimensionierung,
   - 90/80/70/60/50-Prozent-Zuordnung.
9. Resume-Funktion nur bei uebereinstimmendem Quellenhash verwenden.

Tests:

- Pfadtraversal bleibt blockiert;
- Run-/Var-/Modell-/Zonenreferenzen sind eindeutig;
- 5Z-Stundenraster ist nachvollziehbar;
- 29Z-Konfliktstuetzstellen werden nicht still integriert;
- Luecken bleiben sichtbar;
- Quellenhashaenderung verhindert Resume;
- reale Dateien werden nur im lokalen Integrationslauf, nicht in regulaeren Tests verwendet.

### Paket J – Tabellen, Diagramme und deskriptive Bewertung

1. Vorhandene Verträge weiterverwenden:
   - \`build_model_zone_tables()\`
   - \`export_model_zone_tables()\`
   - bestehende Excel-/CSV-Reports
   - bestehende Plot-Templates.
2. Einen kleinen freigegebenen Diagrammslice aus datenkompatiblen Reihen erzeugen.
3. Mindestens pruefen:
   - 5Z-Zonentabelle,
   - 29Z-Kurzvergleich,
   - ALT-Variantenvergleich,
   - Heiz-/Kuehlverlauf, soweit Einheit und Semantik ausreichen,
   - Temperaturverlauf,
   - Zonenvergleich,
   - Variantenvergleich.
4. Vorhandene Farben, Achsen und Layouts nicht neu gestalten.
5. Jedes Artefakt fuehrt:
   - Quelle,
   - Modell,
   - Run/Var,
   - Zeitraum,
   - Einheit,
   - Bezugsflaeche,
   - Abdeckung,
   - Berechnungsversion,
   - Eignungsstatus.
6. Nicht moegliche Ausgaben als \`nicht auswertbar\` mit Ursache fuehren.
7. Bewertung ausschliesslich deskriptiv formulieren.

Tests:

- Exportdateien existieren und sind lesbar;
- Tabellen enthalten Quellen- und Eignungsspalten;
- fehlende Einheit verhindert spezifische/energetische Aussage;
- nicht angeforderte und nicht auswertbare Themen sind getrennt;
- Diagramme verwenden keine Ersatzwerte;
- kein automatisches Bestvariantenurteil.

### Paket K – Vollstaendiger UI-Test

Die UI wird ueber Workflowansicht und direkten Modulzugriff geprueft.

| Bereich | Happy Path | Fehler-/Zustandspruefung | erwarteter Nachweis |
|---|---|---|---|
| Projekt | Projekt oeffnen und laden | kein Projekt aktiv | stabile Projekt-ID |
| Wetter | Referenzwetter anzeigen | unaufgeloeste 2010/2035-Quelle | sichtbarer Status |
| Gebaeude | 5Z-Mapping anzeigen | Quellenkonflikt/fehlender U-Wert | Bauteiltabelle |
| Technik | Systeme laden | fehlender/mehrdeutiger IDM-Wert | Vergleichsdiagnose |
| Zonen | fuenf Zonen und Zuordnung | 29Z nicht mit 5Z vermischen | 5Z-/29Z-Status |
| Parameter | Referenz und Optionen | ungueltige Spanne | Validierung |
| Varianten | 30 + 8 getrennt | ungekoppelte Faktoren | Ausschlussgrund |
| Dimensionierung | VVER-Gruppen ausfuehren | veraltete Auswahl | Blockierstatus |
| Finalisierung | VCAT/VSEL/VGEN | Registry-/Fingerprintkonflikt | finale IDs |
| Setup | RUN materialisieren | unterschiedliches Setup | kein Teilpaket |
| Run-Uebergabe | Checkliste anzeigen | kein IDA-Start | manuelles Gate |
| Import | Manifest laden | geschuetzte/fehlende Datei | Importdiagnose |
| Prepare | 5Z/29Z vorbereiten | Duplikat/Luecke | Qualitaetsbericht |
| Analyse | Tabelle/Diagramm erzeugen | ungueltige Einheit | Eignungsstatus |
| Navigation | Workflow ↔ Direktansicht | Reload/offener Entwurf | gleicher Zustand |

Automatisierung:

- vorhandene Pytest-UI-Helfertests erweitern;
- Streamlit-App headless starten;
- \`streamlit.testing\` nur verwenden, wenn es mit der vorhandenen Streamlit-Abhaengigkeit ohne Installation nutzbar ist;
- abschliessend manueller Klicktest mit Zeit- und Fehlerprotokoll.

### Paket L – Prozessmessung und Effizienzvergleich

1. Vorhandene Prozessmappe vor dem Schreiben sichern.
2. \`reset_sheet()\` nicht gegen die reale Mappe ausfuehren.
3. Schreiber auf stabile Mess-/Quellen-IDs umstellen.
4. Erfassen:
   - aktive Nutzerzeit,
   - Maschinenzeit,
   - Wartezeit,
   - Pruefzeit,
   - Korrekturzeit,
   - Fehler,
   - Wiederholungen,
   - Variantenanzahl,
   - Eingabeumfang.
5. Fehlende Werte als \`nicht erfasst\`, niemals als null oder Schaetzung darstellen.
6. Zuerst absolute Zeiten vergleichen.
7. Relative Aenderung nur bei gleichen Prozessgrenzen und vorhandenem positiven Referenzwert berechnen:

   \`\`\`text
   relative Aenderung =
   (Softwarezeit - manuelle Referenzzeit) / manuelle Referenzzeit
   \`\`\`

8. Negative Werte als Verbesserung, positive als Verschlechterung eindeutig beschriften.
9. Maschinenzeit nicht als Personalkostenzeit behandeln.
10. 366 s fuer 5Z und 1.045 s fuer 29Z nur als exemplarische Simulationsmaschinenzeiten fuehren.

Tests an einer temporaeren Arbeitsmappe:

- vorhandene Fremdzellen bleiben erhalten;
- stabile IDs werden aktualisiert statt dupliziert;
- fehlende Werte erzeugen keine relative Kennzahl;
- Division durch null ist ausgeschlossen;
- Vergleichbarkeitsstatus steuert die Anzeige;
- Formeln und Quellenregister sind konsistent.

### Paket M – Abschlussbericht und Projektdokumentation

1. Lokalen V1-Testbericht aus den erzeugten Artefakten erstellen.
2. Bericht gliedern in:
   - Quellen,
   - Mapping,
   - Konfigurationsabweichungen,
   - UI-Funktionsmatrix,
   - Datenqualitaet,
   - Tabellen/Diagramme,
   - Laufzeiten,
   - Fehler,
   - offene Gates.
3. Bestehende Dokumentationsorte aktualisieren:
   - \`docs/ma_building/README.md\`
   - passende Modul-READMEs
   - \`CHANGELOG.md\`
   - \`PLAN_STATUS.md\`
   - Nutzerentscheidungen nur fuer tatsaechlich neue Entscheidungen.
4. Den unabhaengigen Plan nicht automatisch in \`PLAN_INDEX.md\` aufnehmen.
5. Navigator nur im freigegebenen Dokumentationsscope aktualisieren und validieren.
6. Bei Ueberlappung mit fremden Dokumentationsaenderungen stoppen.

## Testreihenfolge

1. gezielte Unit-Tests je Paket;
2. Architektur-/Importgrenztests;
3. Gebaeude-/Zonen-/Technik-/Parameterregression;
4. Varianten-/Dimensionierungs-/Setupregression;
5. Import-/Prepare-/Analyse-Tests;
6. UI-Helfer- und Navigationstests;
7. gesamtes \`pytest\`;
8. lokaler 5Z-/29Z-/ALT-Integrationslauf;
9. Streamlit-Headless-Start;
10. manueller Workflow-Klicktest;
11. Artefakt- und Dokumentationspruefung.

Regulaere Tests verwenden synthetische Fixtures. Lokale reale IDA-/IFC-/Excel-Daten werden nur im expliziten Integrationslauf verwendet.

## Abnahmekriterien

Der Umfang ist abgenommen, wenn:

- B1 ohne Viewer-/IFC-Datei funktioniert;
- B2 nur verifizierte oder bestaetigte IDs speichert;
- alle fuenf Zonen ein nachvollziehbares Aussenbauteilmapping besitzen;
- Wandsegmente, Fenster und Tueren nach Host und Orientierung sichtbar sind;
- Lobby-Dach und OG-Geschossdecken getrennt sind;
- oberste Geschossdecken nicht mehr als interne GD verschwinden;
- fehlende thermische Werte sichtbar \`PARTIAL\` bleiben;
- 5Z und 29Z getrennte, funktionsfaehige Quellen besitzen;
- Technik vor Zonen im Zielworkflow steht;
- Kopplungsregel in UI und Backend identisch ist;
- genau 30 Optimierungs- und acht getrennte OFAT-Faelle entstehen;
- der 156er-Demoraum wissenschaftlich isoliert bleibt;
- VVER vor Dimensionierung liegt;
- VCAT/VSEL/VGEN aktuell und reproduzierbar sind;
- P018 einen echten Multi-VAR-RUN-Vertrag nutzt;
- kein automatischer IDA-Start erfolgt;
- vorhandene Ergebnisse ehrlich getrennt importiert werden;
- 5Z den Prepare-/Analyseweg durchlaeuft;
- 29Z variable Stützstellen konservativ behandelt;
- ALT Vergleichstabellen/-grafiken liefert;
- Tabellen und datenkompatible Diagramme erzeugt werden;
- jede nicht auswertbare Ausgabe eine Ursache nennt;
- Workflow- und Direktansicht denselben Zustand verwenden;
- Laufzeiten und Fehler dokumentiert sind;
- relative Prozesskennzahlen nur bei Vergleichbarkeit erscheinen;
- keine normative oder kausal unbelegte Behauptung entsteht;
- relevante Tests erfolgreich sind;
- fremde Dirty-Aenderungen nicht ueberschrieben wurden.

## Risiken und Stopbedingungen

- Unklare Dirty-Worktree-Ueberlappung: betroffenes Paket stoppen.
- Quellenhash weicht ab: Import beziehungsweise B2 stoppen.
- Viewer-GlobalId fehlt oder ist doppelt: keine automatische Anreicherung.
- IDM-Details schliessen nicht zur Excel-Summe: keine stille Skalierung.
- Modellnord ist nicht bestaetigt: Richtungen nur modellrelativ ausgeben.
- OGD-U-Wert oder Temperaturfaktor fehlt: thermische Berechnung \`PARTIAL\`.
- IDA-Zeit-/Leistungssemantik bleibt offen: keine belastbare Energieintegration.
- Vorhandene PRN lassen sich keinem ehrlichen Importmanifest zuordnen: Ergebnislauf stoppen.
- Sensitivitaetsfaelle besitzen unterschiedliche Setups: getrennte RUNs.
- Prozessmappe besitzt unerwartete manuelle Aenderungen: externen Schreibzugriff stoppen.
- Neue Abhaengigkeit, automatische IDA-Aktion, 3DM-Inhaltsverarbeitung, Loeschung oder externe Verarbeitung waere erforderlich: Gesamtumfang anhalten und neue Freigabe einholen.
- Ein fachlicher Blocker verhindert nur den betroffenen Slice; unabhaengige sichere Pakete duerfen fortgesetzt werden.

## Rechte- und Freigabegates

### Erfuellt

- selbst simulierte lokale 5Z-/29Z-/ALT-Daten duerfen lokal verarbeitet werden;
- die genannten 5Z-IDM/IDC duerfen fuer Mapping und Querpruefung gelesen werden;
- Viewer-Excel und bytegleiche SmallOffice-IFC duerfen lokal maschinell ausgewertet werden;
- daraus abgeleitete Bauteil-, Oeffnungs- und GlobalId-Mappings duerfen im Projekt gespeichert werden;
- allgemeine \`Freigabe zur Umsetzung\` liegt vor.

### Weiterhin gesperrt

- Verarbeitung anderer, nicht konkret freigegebener IDA-/EQUA-Dateien;
- Rohdateiversionierung;
- 3DM-Inhaltsverarbeitung;
- neue Dependency oder Installation;
- automatische IDA-Steuerung;
- externe oder Cloud-Verarbeitung;
- normative Regeln ohne Methoden-/Rechtegate;
- Commit, Push, Tag und Release;
- Loeschungen oder irreversible Migrationen.

## Offene Entscheidungen

1. **Nordbezug:** Bis zur Bestaetigung von \`north_angle_deg = 0\` bleiben Richtungen als Modell-Nord/Ost/Sued/West bezeichnet.
2. **IDM-/Excel-Differenzen:** Rohwerte und Differenzen werden gezeigt. Eine eventuelle proportionale Verteilung bedarf einer ausdruecklichen fachlichen Entscheidung.
3. **OGD-Thermik:** Flaechen und Bauteilart sind festgelegt; U-Wert und Temperaturkorrektur bleiben offen.
4. **OP-017:** Zeitstempel, Intervallgrenzen, Warm-up, Vorzeichen sowie Leistungs-/Energiesemantik bleiben Fachgate.
5. **OP-018:** Keine projektbezogenen Pass-/Fail-Schwellen oder Einsparungsbewertung festgelegt.
6. **OP-009:** Manuelle Referenzzeiten, Wissensprofil und Kostenannahmen sind noch nicht belastbar.
7. **Diagrammauswahl:** Nur datenkompatible vorhandene Vorlagen verwenden; ein Designwechsel ist nicht freigegeben.
8. **Vollstaendiger kausaler End-to-End-Nachweis:** Erfordert spaeter die manuelle IDA-Simulation der tatsaechlich erzeugten RUN-/VAR-Pakete.

## Tera-Uebergabe

Setze den freigegebenen unabhaengigen Umsetzungsplan
\`docs/project/plans/independent/260814_V1_5Z_Gebaeudemapping_Workflow_UI_PostProcess_Test.md\` um.

Lies den Plan vollstaendig. Pruefe zuerst den aktuellen Dirty Worktree und alle im Plan benannten Ueberlappungen. Veraendere keine Datei, deren fremde Aenderungen sich nicht eindeutig konfliktfrei erhalten lassen. Setze die Pakete in der vorgesehenen Reihenfolge um, fuehre die jeweiligen Tests aus und dokumentiere Abweichungen.

Das objektbezogene B2-Gate ist fuer die im Plan konkret bezeichnete Viewer-Excel und die bytegleiche SmallOffice-IFC erfuellt. B1 muss trotzdem ohne IFC-GlobalIds eigenstaendig funktionieren. Verarbeite die 3DM-Datei nicht inhaltlich.

Halte an, falls eine Scope-Erweiterung, neue Abhaengigkeit, Loeschung, automatische IDA-Aktion, externe Verarbeitung oder ein Commit/Push/Release erforderlich wird.
