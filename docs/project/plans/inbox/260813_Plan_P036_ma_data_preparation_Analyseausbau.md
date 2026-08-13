# P036 ma_data_preparation und fachlicher Analyseausbau

Stand: 2026-08-13
Status: Technischer Prototyp umgesetzt; Fachfreigabe der IDA-Semantik offen
Prioritaet: Hoch
Abhaengigkeiten: P009, P019, P020, P021, P029, UD-112, UD-126

## Ziel

Ein eigenes, programmneutrales Modul `ma_data_preparation` uebernimmt die
kontrollierte Ueberfuehrung standardisierter Simulationsergebnisse in eine
gepruefte Analysedatenbasis. `ma_analyse` verwendet diese Basis fuer
Kennwerte, Tabellen, Variantenvergleiche und spaetere Diagramme.

Der erste produktive Datenbestand umfasst:

- das aktuelle 5Z-Dimensionierungsmodell als fachlichen Hauptaufbau,
- das 29Z-Dimensionierungsmodell fuer einen kurzen Kennwertvergleich,
- `ALT` als historische Heizleistungsoptimierung mit Referenz sowie
  90-, 80-, 70-, 60- und 50-Prozent-Varianten.

## Fuehrende Datenkette

```text
IDA-Ergebnisartefakt
  -> ma_import_simulation: raw -> standardized
  -> ma_data_preparation: standardized -> prepared + Qualitaetsbericht
  -> data/ma_analyse/database
  -> ma_analyse: metric/table/comparison/interpretation
```

Der bestehende Analysebefehl `prepare` bleibt als befristete
Kompatibilitaetsfassade erhalten und delegiert an den neuen Owner. Es wird
keine zweite fachliche Aufbereitungslogik gepflegt.

## Umsetzungsslices

### S1 Vertrage und Datenqualitaet

- versionierte standardisierte Serien mit Run, Variante, Modell, Zone,
  Ergebnisart, Variable, Einheit, Vorzeichen, Zeitbasis und Provenienz,
- getrennte Statusachsen fuer Import, Mapping, Qualitaet und fachliche
  Eignung,
- Eignungsstatus `READY`, `PARTIAL`, `NOT_READY` mit Diagnosen,
- keine stillen Ersatzwerte, kein stilles Abschneiden auf 8760 Zeilen.

### S2 IDA-Ergebnisadapter

- positive Auswahl belegter PRN-, HTML- und Excel-Layouts,
- PRN als primaere Zeitreihenquelle,
- HTML-Berichtswerte als importierte Kontrollwerte,
- Excel als Zonen- und Eingabemetadatenquelle,
- keine inhaltliche Verarbeitung von IDM/IDC oder IDA-Bibliotheken.

### S3 Zeitreihenaufbereitung

- variable Zeitschritte, Duplikate, Luecken und Kalender explizit pruefen,
- Intervalllaengen `dt_h` fuehren,
- zeitgewichtete Mittel, Energien, Verletzungs- und Gradstunden,
- Rohspitzen und Spitzen der aufbereiteten Reihe getrennt benennen,
- optionales Stundenraster fuer vergleichbare Ausgaben.

### S4 Kennwerte und Tabellen

- deutscher, versionierter Kennwertkatalog fuer Zonen, Gebaeude und Anlagen,
- absolute und spezifische Werte mit belegter Bezugsflaeche,
- zeitgleicher Gebaeudepeak statt Summe individueller Zonenmaxima,
- Excel-/CSV-Paket mit Kennwerten, Dateninventar, Berechnungsgrenzen,
  Provenienz, Variantenvergleich und Nachweisbereitschaft.

### S5 Historische Optimierung

- `ALT/Dimensionierung` als zu bestaetigender Referenzfall,
- neutrale Vergleiche der Leistungsfaktoren 90 bis 50 Prozent,
- Leistung, Energie, Temperatur, Unterversorgung und Komfort,
- Feasibility nur mit explizitem Projektprofil; sonst `NOT_EVALUABLE`,
- keine automatische Wahl einer optimalen Variante.

### S6 Vierstufige 5Z-Untersuchung

- 5Z ist der fachliche Hauptaufbau fuer Dimensionierung, Optimierung,
  Nachweis und Sensitivitaet,
- Stage 2 erhaelt ein konfigurierbares Feasibility-Framework,
- Stage 3 erhaelt Profil-, Requirement- und Ergebnisvertraege mit
  `PASS`, `FAIL`, `INVALID`, `NOT_EVALUABLE`,
- produktive Normregeln bleiben bis zum Methoden- und Fachtestgate inaktiv,
- Stage 4 verwendet spaeter Wetter-, Belegungs- und weitere
  Sensitivitaetseingaenge.

### S7 29Z-Kurzvergleich und spaetere Laufzeitkopplung

- kurzer Vergleich zentraler Flaechen-, Last-, Energie- und Temperaturwerte,
- keine ausfuehrliche 29Z-zu-5Z-Raumabbildung in diesem Plan,
- Rechenzeiten werden nicht aus Dateizeitstempeln abgeleitet,
- eine spaetere Schnittstelle nimmt die Laufzeitergebnisse des getrennten
  Prozessmessungs-Slices auf.

### S8 Service, UI und Dokumentation

- bestehende `AnalysisConfig`-/`AnalysisResult`-Vertraege kompatibel halten,
- Streamlit zeigt Eignung, Tabellen und nicht auswertbare Gruende,
- CLI und bestehende Exporte regressionssicher anbinden,
- Navigator, Moduldokumentation, Planstatus und Changelog aktualisieren.

## Zurueckgestellter Diagramm-Slice

Die endgueltige Diagrammgestaltung ist nicht Teil der ersten Umsetzung.
Zunaechst werden Datenbasis, Kennwerte und Tabellen stabilisiert. Danach
werden je Fachthema zwei bis drei Beispiele erzeugt und im Q&A entschieden.

Bereits festgelegt:

- Zeitachsen richten sich nach Jahr, Monat, Woche oder Tag,
- Farben werden fachthemenbezogen vergeben,
- alle 5Z-Zonen erhalten Ausgaben; der Haupttext verwendet begruendet eine
  repraesentative Zone,
- Cooling-Rohvorzeichen und positive Betraege bleiben getrennt,
- Wettersensitivitaet: Temperatur als Linie, Niederschlag als Linie auf der
  rechten Sekundaerachse, Solarstrahlung monatlich als Balken oder Flaeche
  auf einer zusaetzlichen rechten Achse,
- argumentationstragende Diagramme kommen in den Haupttext, vollstaendige
  Zonenserien in den Anhang.

## Tests und Akzeptanz

- synthetische Tests fuer variable Zeitschritte, Duplikate, Luecken,
  Energieintegration, gewichtete Kennwerte und zeitgleiche Peaks,
- Parser- und Signaturtests fuer jedes belegte Ergebnislayout,
- keine regulaeren Tests mit lokalen realen IDA-Dateien,
- Kompatibilitaet fuer CLI, Service, `metrics` und `metrics_v2`,
- unvollstaendige Zonen- oder Flaechenabdeckung sperrt Gebaeudewerte sichtbar,
- jedes Artefakt nennt Quelle, Run, Variante, Modell, Zeitraum, Einheit,
  Bezugsflaeche, Datenabdeckung und Berechnungsversion.

## Stopbedingungen trotz Gesamtfreigabe

Unabhaengige Slices werden fortgesetzt. Nur der konkret betroffene Slice
stoppt bei neuer Dependency, geschuetztem Volltext, externer Verarbeitung,
brechender oeffentlicher API oder fachlich unbelegbarer Variablensemantik.
Norm- und Literaturfragen werden gesammelt; sie verhindern nicht die
technische Datenaufbereitung und deskriptive Analyse.

## Planinput und Freigabe

Der Plan synthetisiert die vom Nutzer bereitgestellten Dokumente
`Finaler Codex-Konzeptplan.md` und `Arbeitsanweisung fuer Codex - Stage 2
Optimization Feasibility und Stage 3 Technical Standard Proof.md` mit dem
kanonischen Stand P009/P019/P020/P029. Die Originale bleiben nicht-kanonische
lokale Eingaben. Das Literaturpaket wurde nicht geoeffnet.

Freigabe zur Umsetzung erteilt am 2026-08-13.

## Umsetzungsstand 2026-08-13

- S1 bis S3: Datenvertraege, Eignungspruefung, IDA-Adapter und
  Zeitreihenaufbereitung als technischer Prototyp umgesetzt und synthetisch
  getestet; die strukturierte Importgrenze und IDA-Semantik bleiben offen.
- S4: Zonenkennwerttabelle sowie 5Z-/29Z-XLSX/CSV technisch umgesetzt;
  noch nicht ableitbare Berichtsfelder bleiben sichtbar leer und PRN-
  Energieableitungen bis zur Semantikbestaetigung `PARTIAL`.
- S5: ALT-Variantenvergleich mit expliziter Basis und Deltas umgesetzt;
  Feasibility bleibt ohne Profil wertfrei.
- S6: konfigurierbare Stage-2- und Stage-3-Frameworks umgesetzt, ohne
  produktive Normgrenzwerte.
- S7: 29Z-Kennwerttabelle umgesetzt; Rechenzeitkopplung bleibt vereinbart
  zurueckgestellt.
- S8: Prepare-Kompatibilitaetsfassade, Workflow-Katalog, Moduldokumentation,
  Planstatus und Tests aktualisiert. Die vorhandene Streamlit-Prepare-Aktion
  nutzt die Fassade; eine eigene Tabellenansicht folgt mit dem Diagramm-Q&A.
- Diagramm-Slice bleibt entsprechend Nutzerentscheidung zurueckgestellt.

## Council-Review und verbleibende Fachgates

Der technische Review hat folgende Befunde unmittelbar gehaertet:

- erkannte Luecken werden bei bekanntem Sollschritt nicht mehr interpoliert
  oder integriert,
- nicht eindeutige Reihen werden nicht integriert,
- lange Prepare-Laeufe halten nur speicherschlanke Ergebnisreferenzen und
  koennen quellhashgeprueft fortgesetzt werden,
- fehlerhafte PRN-Zeilen werden nicht mehr still verworfen,
- nicht endliche Stage-2-/Stage-3-Werte bleiben nicht auswertbar,
- Tabellen fuehren absolute und spezifische Leistungen getrennt; HTML-
  Quellen werden in der Provenienz ergaenzt,
- reale PRN-Ableitungen werden bis zur Semantikbestaetigung nur `PARTIAL`.

Vor wissenschaftlicher Verwendung der berechneten Energie- und
Gebaeudekennwerte bleiben als Fachgates offen:

1. IDA-Zeitstempel, letzte Periodengrenze, Warm-up und Leistungssemantik
   (`q_heat`, `q_cool`) bestaetigen.
2. Vorzeichenkonvention und erforderliche absolute/algebraische
   Kuehlkennwerte festlegen.
3. Den strukturierten Vertrag `ma_import_simulation -> ma_data_preparation`
   ohne zusammengesetzte Metadatenstrings durchgaengig machen.
4. Nettoflaeche, Zonenmultiplikator und Systemgrenze fuer Gebaeudeenergie und
   zeitgleichen Peak fachlich bestaetigen.
5. Pflichtvariablen-, Perioden- und Zonenabdeckung getrennt definieren; erst
   danach darf `READY` fuer Masterarbeitsergebnisse vergeben werden.

Die erzeugten Tabellen sind daher ein kontrollierter Arbeitsstand fuer die
weitere Methodenentscheidung, noch kein freigegebener quantitativer Nachweis.
