# Chat-Handover: Varianten-Test, Setup-Ausgaben und lokale Projekt-Snapshots

Datum: 2026-08-11

Status: lokaler, uncommitteter Arbeitsstand auf `main` seit `73cbd07`; keine
Git-Aktion ausgefuehrt. Dieser Handover beschreibt nur den unten abgegrenzten
Chat-Scope. Weitere uncommittete Aenderungen im Arbeitsbaum gehoeren nicht
zu diesem Handover.

## Fuehrende Referenzen

- [P017 Varianten und Naming](../../plans/inbox/260622_Plan_P017_ma_variants_Naming_Anbindung.md):
  verbindliche Kette `VSP -> VVER -> VCAT -> VSEL -> VGEN`; insbesondere
  Abschnitt *Verbindliche Hierarchie* und `VGEN`.
- [P018 Simulation-Setup](../../plans/inbox/260622_Plan_P018_ma_simulation_setup_Run_Manifest.md):
  kanonisches neutrales `RUN`-Paket mit gemeinsamem Setup und mehreren
  `VAR`; Abschnitte *Neutrales Run-Paket* und *Eingang aus P017*.
- [P035 Projekt-Workspace](../../plans/inbox/260727_Plan_P035_Projekt_Workspace_Lokale_Projektablage.md):
  aktiver Workspace-Pfadvertrag und die hier uebertragene Galerie-Folgearbeit.
- [UD-119](../../decisions/USER_DECISIONS_MASTERTHESIS_CODE.md):
  lokale Snapshot-Trennung `gallery/` (Projektbilder) und `diagrams/`
  (Auswertungsbilder).

## Abgegrenzter Aenderungsumfang

### Git-Status und Scope-Dateien

Zum Handover-Zeitpunkt sind folgende Scope-Dateien uncommittet:

- `??` neu: `config/ma_variants/studies/small_office_v1_random_156.yaml`.
- `M`: `src/ma_variants/small_office_v1.py`, `src/ma_variants/__init__.py`,
  `src/ma_ui/streamlit_app/pages/variants.py`,
  `src/ma_ui/streamlit_app/module_views/dimensioning_view.py`,
  `src/ma_simulation_setup/project_packages.py`,
  `src/ma_ui/streamlit_app/module_views/simulation_setup_view.py` und
  `tests/test_ud106_product_slices.py`.
- `M`: `docs/ma_variants/README.md`; zugehörig sind ausschließlich die zwei
  Absätze ab *„Fuer den manuellen Auswahltest …“* und
  *„Nach dem Simulation-Setup …“* sowie der Pfadabsatz zu `test_only`.
- `M`: `.gitignore`; zugehörig sind ausschließlich die drei Zeilen für
  `data/project_output/`.

Zwei Dateien sind mit anderen Arbeitssträngen gemischt und dürfen bei einer
Git-Aktion **nicht als Ganzes** diesem Scope zugeordnet werden:

- `M CHANGELOG.md`: nur die drei `Unreleased / Added`-Einträge, die mit
  *„Simulation-Setup-Ausgaben werden nun …“*, *„Das Simulation-Setup ergänzt
  jede Run-Gruppe …“* und *„Die Variantenansicht kann zwischen …“* beginnen.
  Die vorstehenden Analyse-/Tabellen-Einträge und der nachfolgende
  Inbox-Eintrag gehören nicht zu diesem Handover.
- `M docs/project/decisions/USER_DECISIONS_MASTERTHESIS_CODE.md`: nur der
  vollständige Abschnitt `## UD-119 Projektlokale Galerie und
  Auswertungsdiagramme trennen`. Die Abschnitte `UD-120` und `UD-121` gehören
  nicht dazu.

Die hier neu erstellten Handover-Dateien und der P035-Folgehinweis sind
ebenfalls uncommittet und nur diesem Handover zugeordnet:
`docs/project/archive/chat_handovers/260811_chat-handover_preprocess-output-snapshots.md`,
`docs/project/archive/chat_handovers/INDEX.md` und
`docs/project/plans/inbox/260727_Plan_P035_Projekt_Workspace_Lokale_Projektablage.md`.

### Lokale, ignorierte Snapshot-Artefakte

`data/project_output/masterarbeit/` und
`data/project_output/testvariante_156/` enthalten statische, manuell in diesem
Chat zusammengestellte Nachweisordner. Die Struktur ist:

```text
<snapshot>/
|-- project.yaml
|-- gallery/                 # leer; fuer kuenftige ma_project-Bilder
|-- diagrams/                # vier markierte Beispielgrafiken
|-- settings/                # Quellkonfigurationen und Snapshot-Kontext
|-- variants/
|   |-- variant_tree.yaml
|   |-- variant_tree.txt
|   `-- selection/
|       |-- selection_manifest.yaml
|       `-- selection_overview.txt
`-- logs/
    |-- timings.yaml
    |-- timings.csv
    `-- run_summary.yaml
```

Die Snapshot-Dateien werden nicht durch einen Generator erzeugt. Bei einer
fachlichen Konfigurationsaenderung muessen sie bewusst gegen die referenzierten
Quelldateien aktualisiert und erneut geprueft werden. Sie enthalten keine
Wetterrohdaten, keine IDA-Dateien und keine Simulationsergebnisse. Die vier
Diagramme sind in `diagrams/README.md` ausdrücklich als versionierte
Beispielgrafiken aus `docs/examples/` markiert.

Die Snapshot-Inhalte selbst sind wegen `.gitignore` nicht versioniert. Der
Eintrag `?? data/project_output/` bezeichnet nur die freigegebenen
Strukturdateien `.gitkeep` und `README.md`; die übrigen Artefakte bleiben lokal.

## Erledigter Stand

- Der bestehende SmallOffice-V1-Referenzraum bleibt bei 30 theoretischen
  Optimierungsvarianten; seine vollständige Auswahl umfasst dieselben 30.
- Die neue, versionierte Konfiguration `small_office_v1_random_156.yaml`
  definiert einen getrennten `test_only`-Testraum mit 13 Sollwertbändern und
  12 Leistungsfaktoren, also 156 theoretischen Varianten.
- Die Variantenansicht speichert die gewaehlte Studienconfig. Die Auswahl ist
  reproduzierbar ueber den Seed `20260806`, den zugehörigen Auswahlmodus und
  die Kandidaten-IDs in
  `data/project_output/testvariante_156/variants/selection/selection_manifest.yaml`.
  Die deterministische Kandidatenreihenfolge folgt dem kartesischen Produkt
  der in `settings/study_config.yaml` dokumentierten Bänder und Faktoren.
- Der Test-Snapshot enthält 50 markierte Auswahleinträge. Der vollständige
  156er-Baum liegt in `variants/variant_tree.txt`; die ausgewählten Varianten
  mit Sollwerten und Faktor stehen in `variants/selection/selection_overview.txt`.
- Die produktive Routing-Regel im Simulation-Setup lautet weiterhin:
  `test_only` nach `data/test_output/<Projekt-ID>/simulation_setup/<Run-ID>`
  und reguläre Studien nach
  `data/project_output/<Projekt-ID>/simulation_setup/<Run-ID>`.
  `data/project_output/testvariante_156/` ist eine vom Nutzer verlangte,
  statische Dokumentationsausnahme und kein produktiver `test_only`-Run.
  Der Ordner `masterarbeit/` ist entsprechend ein statischer Referenz-Snapshot.
- Materialisierte Run-Gruppen erhalten zusätzlich `run_summary.yaml`,
  `timings.yaml` und `timings.csv`. Die Zeiten sind Sekundenwerte für
  technische Variantenaktionen, Paketmaterialisierung und deren Gesamtzeit;
  manuelle Bearbeitungszeit sowie IDA-Laufzeit sind nicht Teil dieser Messung.

## Strukturgrenze fuer fortsetzbare Varianten

`selection/` dokumentiert nur die Auswahl. Es ist weder ein zweiter Katalog
noch ein neues Übergabeobjekt. Insbesondere wurde kein `VariantHandover`
eingeführt: P017 schließt dieses Objekt aus.

Eine transportierbare Variante entsteht erst nach vollständigem VGEN innerhalb
eines kanonischen P018-RUNs. Der minimale Zielbestand ist:

```text
simulation_setup/RUN-<id>/
|-- run_manifest.yaml
|-- simulation_setup.yaml
`-- variants/VAR-<id>/
    |-- variant_config.yaml
    `-- simulation_input.yaml
```

`simulation_setup.yaml` bleibt einmal je RUN gemeinsam; Variantenwerte,
Provenienz und neutraler Simulationseingang gehören unter die jeweilige
`VAR-<id>`. Die bisherigen statischen Snapshots sind dafür kein Ersatz.

## Uebertragene Restarbeit

- P017/P018 führen die bereits dokumentierte Aufrufermigration fort. Für die
  50er-Testmenge lautet die spätere Abfolge: aktuelle Auswahlbasis laden,
  VGEN vollständig für alle 50 Einträge abschließen, genau einen RUN mit
  diesen 50 `VAR-<id>` materialisieren und dessen Manifest, Setup,
  Variantenartefakte sowie technische Logs validieren. Akzeptanz: kein
  fehlender Parametersatz, keine fehlende Referenz und keine Teilübergabe.
- P035 führt die Galeriepfadfrage weiter: Für aktive Workspaces bleibt bis zu
  einer separaten Migration `assets/gallery/` verbindlich. Die lokalen
  Snapshot-Ordner verwenden nach UD-119 `gallery/` und `diagrams/`. Es gibt
  aktuell keinen Fallback und keine automatische Verschiebung zwischen beiden
  Layouts.

## Pruefung

- `python -m pytest tests/test_ud106_product_slices.py -q` mit
  `.venv\\Scripts\\python.exe`: **21 passed** in 6.56 s am 2026-08-11.
- Die lokalen Snapshot-Checks bestätigten: 30 Varianten im Referenzbaum,
  156 Varianten im Testbaum, 50 markierte Testauswahlen; die YAML-Dateien sind
  parsebar. Beide Galerien enthalten nur ihre README; je Snapshot liegen vier
  gekennzeichnete Diagramm-Beispiele vor.
- `git diff --check` für die oben abgegrenzten versionierten Dateien war
  fehlerfrei.

## Grenzen

- Kein IDA-Export, keine IDA-Dateiverarbeitung, kein Simulationsstart und
  kein Ergebnisimport.
- Kein Commit, Push, Tag oder Release.
- Dieser Handover ersetzt weder die aktiven Pläne noch Entscheidungen und
  führt keine eigene offene Aufgabenliste.
