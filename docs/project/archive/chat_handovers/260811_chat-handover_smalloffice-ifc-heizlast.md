# Chat-Handover: SmallOffice-IFC-Huelle und Heizlastvorbereitung

Datum: 2026-08-11

Status: lokale Diagnose ausgefuehrt; Ergebnisarbeitsmappe beim Handover nicht
mehr vorhanden, daher vor Wiederverwendung reproduzieren; kein Commit, Push
oder Release ausgefuehrt.

## Fuehrende Referenzen

- [P012](../../plans/inbox/260622_Plan_P012_ma_building_Gebaeudeinput.md)
  und [OP-012](../../decisions/USER_DECISIONS_OPEN_POINTS.md) fuer
  IFC-Lite-Grenze, Raumbegrenzungen und die Wiederherstellung der Diagnose.
- [P016](../../plans/inbox/260622_Plan_P016_Stage1_Dimensionierung.md) fuer
  die Verwendung des mittleren Huelle-U-Werts in der manuellen Heizlast.
- [OP-016](../../decisions/USER_DECISIONS_OPEN_POINTS.md) fuer die begrenzte
  lokale `ifcopenshell`-Installation.
- `config/ma_zones/examples/small_office_5z_endvariant_02_zone_spec.yaml`
  fuer die bestaetigte SmallOffice-5-Zonen-Zuordnung.

## Erledigter Arbeitsstand

- Nach ausdruecklicher Freigabe wurde `ifcopenshell==0.8.5` ausschliesslich
  in die Projekt-`.venv` installiert. Reproduzierbar ist dies mit
  `.\\.venv\\Scripts\\python.exe -m pip install ifcopenshell==0.8.5`.
  Es wurde keine versionierte Dependency-Datei geaendert und kein produktiver
  IFC-Lite-Adapter erstellt.
- Die lokale IFC-Quelle
  `data/ma_building/input/ifc/SmallOffice_d_IFC2x3.ifc` wurde ausgelesen.
  Erkannt wurden 29 `IfcSpace` und 76 `IfcRelSpaceBoundary`. Fuer die
  Ausrichtung galt auf ausdrueckliche Nutzerbestaetigung die Arbeitsannahme
  `IFC-Y = Nord`; eine etwaige Modell-Nordreferenz wurde nicht als
  Produktivnachweis uebernommen.
- Die angefragten vier Darstellungen wurden waehrend des Chats als lokale
  Arbeitsmappe erstellt: Raumansicht, 5-Zonen-Ansicht,
  Gebaeudezusammenfassung und `IFC_Elementliste`. Die Elementliste enthielt
  277 `IfcProduct`-Objekte einschliesslich Projektstruktur, jedoch ohne die
  113 rein technischen `IfcOpeningElement`-Hohlraeume. Diese Zaehlung ist
  eine Darstellungsregel, keine IFC-Vollstaendigkeitsaussage.

## IFC-Diagnosewerte – vor Wiederverwendung pruefen

Die folgenden Werte wurden aus IFC-Mengen und -Geometrie aggregiert: 590.532
m2 Aussenwand brutto, 195.723 m2 Fenster, 20.800 m2 Aussentueren, 374.017 m2
Aussenwand netto, 331.716 m2 Boden und 403.980 m2 Dach. Die Fenster und
Aussentueren wurden vom jeweiligen Bruttowandanteil abgezogen. Die
Bruttowaende sowie Boden/Dach stammen aus Bauteilmengen beziehungsweise
Geometrie; die Raumbegrenzungen dienten nur der raumweisen Plausibilisierung.

Mit den Annahmen Wand `0.28`, Fenster `1.30`, Tuer `1.80`, Dach `0.20` und
Boden `0.35` W/(m2 K) ergab die flaechengemittelte Gebaeudehuelle
`sum(A_i * U_i) / sum(A_i) = 0.448 W/(m2 K)`, also gerundet `0.45 W/(m2 K)`.
Mit Boden `0.28 W/(m2 K)` ergab sich `0.430 W/(m2 K)`. Diese Zahlen sind
nicht erneut nachweisbar, weil die Ergebnisarbeitsmappe beim Abschluss nicht
mehr am erwarteten lokalen Pfad vorhanden war.

## Heizlast-Arbeitsmappe und Quellenlage

Die Nutzer-Arbeitsmappe liegt unter
`C:\\Users\\ralph\\OneDrive - Frankfurt UAS\\Master\\UAS - 6. Semester\\MASTER-THESIS\\TEIL1.2_DimEXCEL\\Masterarbeit_Heizlastberechnung_DIN_EN_12831.xlsx`.
Im Blatt `5Z` verwendet Zelle `B7` den mittleren Huelle-U-Wert; die
Bauteil-Referenzwerte im Blatt sind Wand `0.28`, Fenster `1.30`, Tuer `1.80`,
Dach `0.20` und Boden `0.28` W/(m2 K). Die GEG-Anlage 2 liefert fuer das
Nichtwohngebäude-Referenzgebäude vergleichbare Werte, beim Boden jedoch
`0.35 W/(m2 K)`, und nennt einen Waermebrueckenzuschlag von
`0.05 W/(m2 K)`, nicht pauschal 5 Prozent.

DIN EN 12831-1 beschreibt das Berechnungsverfahren; allgemeingültige
Bauteil-U-Werte sind daraus nicht ableitbar. Die Werte `n50 = 1.5`,
Abschirmung `0.07`, Hoehenkorrektur `1.0` und Waermebrueckenzuschlag `5 %`
sind daher Vereinfachungsannahmen der Arbeitsmappe. Die Auslegungstemperatur
`-12 Grad C` bleibt gegen den fuer Frankfurt geltenden Nationalen Anhang zu
DIN EN 12831-1 zu pruefen. Webquellen der Einordnung:
[GEG Anlage 2](https://www.gesetze-im-internet.de/geg/anlage_2.html) und
[DIN EN 12831-1 bei DIN Media](https://www.dinmedia.de/de/norm/din-en-12831-1/261292587).

## Grenzen und uebertragene Restarbeit

Nur die Raeume 101 und 102 besitzen explizite Aussenwand- und
Oeffnungsbeziehungen. Fuer die anderen 27 Raeume sind in den
Raumbegrenzungen nur Boden oder Dach enthalten. Daraus duerfen keine exakten
raum- oder zonenweisen Huelle-U-Werte abgeleitet werden.

Die konkrete Folgearbeit ist in den oben verlinkten Quellen gefuehrt:

- P012/OP-012: Arbeitsmappe suchen, wiederherstellen oder erneut erzeugen;
  danach die Raumboundary-Qualitaet sowie ein manuell bestaetigtes
  Huelle-/Oeffnungs-Mapping validieren, bevor ein IFC-Lite-Import in Frage
  kommt.
- P016: Fuer die manuelle Heizlast den Boden-U-Wert sowie die Zonenzuordnung
  fachlich festlegen und die Auslegungstemperatur gegen den relevanten
  Nationalen Anhang pruefen. Bis dahin ist `0.45 W/(m2 K)` nur eine
  vereinfachte Gebaeudeannahme, keine zonale IFC-Ableitung.
- OP-016: Vor jeder produktiven Nutzung von `ifcopenshell` entscheiden, ob
  die Bibliothek versionsverwaltet als Abhaengigkeit aufgenommen wird.

## Lokaler Ausgangsstand

Git-Stand bei der Handover-Pruefung: `73cbd07`. Der Arbeitsbaum enthielt
bereits umfangreiche, nicht zu diesem Chat gehoerende uncommittete Aenderungen.
