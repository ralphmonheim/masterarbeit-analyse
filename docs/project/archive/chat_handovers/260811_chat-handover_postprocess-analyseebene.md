# Chat-Handover: PostProcess-Ausrichtung und gemeinsame Analyseebene

Datum: 2026-08-11

Status: Fachliche Orientierung und Planuebertragung abgeschlossen; keine neue
Produktivimplementierung oder Git-Aktion durch diesen Chat.

## Fuehrende Referenzen

- [P007 Gesamtprozess](../../plans/inbox/Masterarbeit_VSCode_Projektplan_2026-06-21.md)
  sowie [UD-112 und UD-114](../../decisions/USER_DECISIONS_MASTERTHESIS_CODE.md)
  definieren die Bereiche PreProcess, MainProcess und PostProcess sowie die
  Ownership von `ma_analyse`.
- [P029](../../plans/inbox/260627_Plan_P029_ma_analyse_Service_Runner_Bereinigung.md)
  ist der aktive Plan fuer den PostProcess-Owner `ma_analyse`; [P019](../../plans/inbox/260622_Plan_P019_Stage2_Optimierung.md)
  beschreibt die vorhandenen Varianten- und Vergleichsfunktionen.
- [P009](../../plans/inbox/260621_Plan_P009_Simulationsschnittstellen_IDA_Adapter.md)
  fuehrt den spaeteren manuellen Ergebnisimport. [OP-008 und OP-017](../../decisions/USER_DECISIONS_OPEN_POINTS.md)
  enthalten die noch offenen Regeln fuer Diagrammnormierung beziehungsweise
  das Dateninventar eines künftigen Imports.
- [P022 und P023](../../plans/PLAN_INDEX.md) sind die separaten Zielmodule
  fuer Kosten- und Nachhaltigkeitsauswertung.

## Begriffe und Prozessgrenze

- **IDA-Ergebnisordner** enthalten nach der manuellen Simulation bereitgestellte
  Ergebnisdaten. Sie sind von vollstaendigen IDA-/EQUA-Quelldateien zu
  unterscheiden; deren automatische Verarbeitung bleibt gesperrt.
- **RUN** bezeichnet im Zielprozess ein gemeinsames Simulationspaket,
  **VAR** eine darin enthaltene Variante. Der künftige Import ordnet Ergebnisse
  ueber diese Referenzen zu.
- **StudyDirection** ist eine im PreProcess angelegte Untersuchungsrichtung.
- `ma_dimensionierung` ist der Owner der Dimensionierung. `ma_analyse` ist
  ausschliesslich der Owner der technischen Ergebnisanalyse. `ma_economy` und
  `ma_sustainability` bewerten spaeter getrennt Kosten bzw. betriebliche
  Emissionen auf Basis technischer Analyseergebnisse.

## Abgeglichener Stand und Nutzerentscheidung

- Die vorhandenen lokalen IDA-Auswertungsdaten mit Referenz und
  Heizleistungsvarianten bleiben ein separater, direkt nutzbarer
  Legacy-/Explorationsbestand. Sie werden nicht rueckwirkend in einen
  RUN-/VAR-Importprozess ueberfuehrt.
- Wenn erstmals neue, manuell bereitgestellte IDA-Ergebnisordner fuer den
  Zielprozess vorliegen, wird P009 einen einfachen Import-Slice anhand ihres
  realen Dateninventars planen. OP-017 ist daher kein Blocker fuer die
  aktuelle Bestandsanalyse.
- Der PostProcess wird fuer die weitere fachliche Diskussion zunaechst als
  **eine gemeinsame Analyseebene** behandelt: aufbereitete Daten erzeugen
  Kennwerte, Vergleiche, Tabellen, Diagramme und eine nachvollziehbare
  technische Interpretation.
- Die vorhandene technische Stage-Struktur bleibt Bestand: Stage 1 wird nach
  `ma_dimensionierung` migriert, Stage 2 traegt die bestehenden
  Ergebnis-/Vergleichsfunktionen, Stage 3 zeigt nur eine wertfreie
  Nachweisbereitschaft und Stage 4 ist geplant. Die Stages sind kein
  verbindlicher Benutzerworkflow. Eine moegliche Konsolidierung der aktuellen
  Mehrtab-Ansicht zu einer Analyseansicht ist nicht umgesetzt und erfordert
  einen eigenen UI-Slice.
- StudyDirections werden spaeter als Untersuchungsrichtung bzw. Filter in die
  Analyseebene uebertragen, nicht als zusaetzliche Analyse-Module oder Stages.
- Die bestehende Analyseebene deckt Datenaufbereitung, Heiz-/Kuehlleistung und
  -energie, Raum- und operative Temperatur, Komfortdarstellungen, IAQ,
  Energiebilanz, interne Lasten, Raum-/Variantenvergleich, Zeitfenster sowie
  Tabellen und Diagramme ab.
- Raumkennwerttabellen koennen bereits W, W/m2 oder beides ausgeben; Cooling
  kann mit Rohvorzeichen oder als Betrag dargestellt werden. Die allgemeine
  Normierung aller Diagrammarten bleibt in OP-008 offen. Bis zu einer eigenen
  Entscheidung bleibt das bisherige Diagrammverhalten erhalten.
- Spaetere Kosten- und Nachhaltigkeitsauswertungen duerfen technische Werte
  verwenden: kleinere erforderliche Heiz-/Kuehlleistungen als Grundlage fuer
  transparente Investitionsannahmen sowie Energieverbraeuche fuer betriebliche
  Kosten und Emissionen. Preisstand, Emissionsfaktor und Systemgrenze liegen
  weiterhin ausserhalb der technischen Analyse in P022/P023.

## Uebertragene Restarbeit

- **P029, fachlich federfuehrend:** eine Planung fuer die gemeinsame
  Analyseebene erstellen. Ergebnis ist ein abgestimmter Katalog von Themen,
  Auswahlfiltern, Kennwerten sowie Tabellen- und Diagrammartefakten; P019
  ordnet darin die vorhandenen Variantenvergleiche ein.
- **P009, bei erstem neuen Ergebnisordner:** Dateninventar mit Ergebnisdateien,
  Feldern, Einheiten und Zuordnung erstellen und daraus einen manuellen
  Importvertrag planen. Akzeptanz ist ein dokumentierter Feldvertrag ohne
  automatische Verarbeitung von IDA-/EQUA-Quelldateien.
- **P022/P023, erst danach:** die technischen Ergebniskennwerte in Kosten- und
  Emissionsannahmen ueberfuehren und Quellen, Preisstand sowie Systemgrenze
  offenlegen.

## Nachweis und Grenzen

Der nach UD-113 erforderliche Blind-Review wurde vor Archivierung
durchgefuehrt; die dort benannten Verstaendlichkeitsluecken sind in diesen
Text eingearbeitet. Es wurden keine Daten, keine IDA-Dateien und keine
Produktivfunktionen veraendert. Der Arbeitsbaum enthielt bereits umfangreiche
uncommittete Aenderungen; sie wurden nicht bereinigt, committed oder gepusht.
