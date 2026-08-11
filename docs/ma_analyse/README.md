# ma_analyse

Dieser Bereich dokumentiert die bestehende Analysepipeline fuer IDA-ICE-Simulationsergebnisse.

## Zweck

Standardisierte Simulationsergebnisse technisch auswerten und als Kennwerte,
Tabellen, Diagramme und Analyseberichte bereitstellen.

## Eingaben

- standardisierte Simulationsergebnisse
- Projekt-, Varianten-, Raum- und Analysekonfiguration

## Ausgaben

- Kennwerte, Tabellen, Diagramme, Excel-Dateien und Analyseberichte

## Abgrenzung

- keine Kosten-, Nachhaltigkeits- oder Gesamtbewertung
- `ma_analyse.stage_1_dimensioning` ist historischer Implementierungs- und
  Kompatibilitaetspfad. Der vorbereitete Zielnamespace fuer die spaetere
  Fachmigration ist `ma_dimensionierung`.
- `OutputRequirementProfile` bleibt als PostProcess-/Ausgabeanforderung bei
  `ma_analyse` und wird nicht nach `ma_dimensionierung` verschoben.
- Stage 3 implementiert keine ungeprueften Normregeln

## Abhaengigkeiten

- `ma_import_simulation` als langfristige Ergebnisdatenquelle
- bestehende lokale Analyse-Datenpfade

## Status

Die gemeinsamen Analysefunktionen, die Datenvorbereitung und Stage 2 sind
teilweise vorhanden. Die historische Stage-1-Dimensionierung bleibt bis zur
physischen P016-Owner-Migration als Implementierungs- und Legacy-Pfad
erhalten; Stage 3 und Stage 4 sind geplant.

Die Streamlit-Demo zeigt die vorhandene Auswahl sowie Dimensionierung,
Optimierung, Nachweis und Sensitivitaet in einer gemeinsamen Tab-Ansicht.
Stage 2 rendert echte `AnalysisResult`-Inhalte. `analyze-data` befuellt jetzt
auch die Summary-Tabelle sowie die Detailtabellen `Dateninventar`,
`Berechnungsgrenzen` und `Nachweisbereitschaft`. Diagrammdateien, Warnungen und
erzeugte Dateien werden weiterhin wiederverwendet. Stage 3 zeigt die
wertfreie Readiness-Matrix sichtbar `nicht auswertbar`; sie ist kein
Normnachweis. Die uebrigen Tabs zeigen den belegten Fachstand und ihre Grenzen
als separates Modul beziehungsweise `nicht auswertbar`.

Die Ziel-Leistungsdarstellung der Tabellen ist als `W`, `W/m2` oder `Beides`
waehlbar; automatische Ausgaben verwenden `Beides`. Der aktuelle PRN-/CSV-
Import belegt die Quelleneinheit jedoch noch nicht maschinenlesbar. Deshalb
muss sie fuer den Lauf bewusst als `W` oder `W/m2` angegeben werden. Ohne
diese Angabe werden nur einheitenoffene Aggregationskennwerte mit
`Quelleneinheit nicht bestaetigt` ausgegeben; W und W/m2 bleiben leer.
Umrechnungen verwenden nur eine positive,
eindeutig zugeordnete Netto-Raumflaeche des aktiven Building-Stands oder eine
bewusst ergaenzte raumbezogene Flaeche. Die Flaechen-Widgets sind an Projekt
und Building-Version gebunden; mehrdeutige Raumnamen werden nicht automatisch
zugeordnet. Ohne erforderliche Flaeche bleibt der direkt belegte Wert erhalten
und die abgeleitete Darstellung wird als `nicht auswertbar` gekennzeichnet.
Die Excel-Datei behaelt `metrics` als sicheren Legacy-Adapter und schreibt den
neuen Vertrag in `metrics_v2`. `Auswertungsstunden` stammen aus der stundenweise
aufbereiteten `time`-Achse. `Nutzungsstunden` werden erst mit einem
freigegebenen Belegungsprofil berechnet.

Bei aktivem lokalem Projekt-Workspace ist dessen `output/ma_analyse/` die
Standard-Ausgabewurzel. Ohne aktiven Workspace bleibt
`data/ma_analyse/output/` der bestehende Default; eine bewusst manuell
gesetzte Ausgabewurzel wird nicht ueberschrieben. Das letzte UI-Ergebnis ist
an die aktive Projekt-ID gebunden und wird bei einem Projektwechsel verworfen.

## Naechster Schritt

Den neutralen Ergebnisimport und die Raum-/Zonenreferenzen weiter
standardisieren. Produktive Normkriterien und ein formaler Robustheitsvertrag
benoetigen weiterhin eigene fachlich freigegebene Aktivierungen.

## Dateien

- `architecture.md`: Architektur und Datenfluss der Analysepipeline.
- `commands_analyse.md`: aktive Befehlsreferenz fuer CLI, GUI, Tests und Plot-Templates.
- `data_preparation/README.md`: vorbereitender Schritt fuer `prepare` und
  `analyze-data` vor Analyse Stufe 2.
- `plot_template_examples.md`: Referenzgalerie der Plot-Template-Beispiele.
- `stage_1_dimensioning/README.md`: LoD-1-Referenzdimensionierung aus dem
  validierten `ParameterSnapshot` v1.
- `stage_2_optimization/README.md`: vorhandene Analysebefehle als spaeterer
  Optimierungsablauf.
- `stage_3_standards_verification/README.md`: geplanter Norm-Nachweis mit
  deutschen und spaeter internationalen Normenprofilen.
- `stage_4_sensitivity/README.md`: geplante ereignisbasierte
  Sensitivitaets- und Robustheitsanalyse.

Die verbindlichen Arbeitsordner sind `data/ma_analyse/ida_imports`, `data/ma_analyse/database` und `data/ma_analyse/output`. Die frueheren Root-Datenpfade werden nicht mehr unterstuetzt.
