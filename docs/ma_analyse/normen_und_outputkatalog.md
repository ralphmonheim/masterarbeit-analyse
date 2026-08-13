# Normen- und Outputkatalog fuer die Masterarbeit

Stand: 2026-08-13

## Zweck und Status

Der Katalog ordnet die geplanten Analyseausgaben fachlichen Regelwerken zu.
Er ist noch **kein Normnachweis**: Im Projekt liegt aktuell kein aktivierter
Normvolltext vor. Grenzwerte, Kategorien und Berechnungsrandbedingungen
werden erst nach Beschaffung der projektrelevanten Ausgaben, Quelleninventar,
fachlicher Pruefung und Freigabe als Stage-3-Profil hinterlegt.

## Bibliografisches Regelwerksinventar und projektseitige Output-Zuordnung

| Thema | Regelwerkskandidat | Projektseitig vorgesehene Ausgaben (noch nicht aus Volltext verifiziert) |
|---|---|---|
| Sommerlicher Waermeschutz | DIN 4108-2:2026-05 | Uebertemperaturgradstunden je Zone, Bezugsgrenze, Nutzungszeit, Klimarandbedingungen, PASS/FAIL/NOT_EVALUABLE |
| Thermische Behaglichkeit | DIN EN ISO 7730:2025-12 | PMV/PPD, lokale Unbehaglichkeit, belegungs- und personenbezogene Langzeitkennwerte |
| Innenraumklima | DIN EN 16798-1:2021-04 | operative Temperatur, Raumluftqualitaet/CO2, Feuchte, Belegungszeit und Kategorienprofil |
| Heiz-/Kuehlenergie und Temperaturen | DIN EN ISO 52016-1:2018-04 | Heiz-/Kuehlenergie, Innenraumtemperaturen sowie sensible/latente Lasten mit Zeitraum und Bezugsflaeche |
| Heizlast | DIN EN 12831-1:2017-09 mit DIN/TS 12831-1:2020-04 | Raum- und Gebaeudeheizlast, Auslegungsrandbedingungen, Versorgungsluecke |
| Kuehllast/Jahressimulation | VDI 2078:2015-06 | thermische Lasten, Raumtemperaturen, zeitgleicher Anlagenpeak und Auslegungsfaelle |

Die Ausgaben wurden am 2026-08-13 anhand der offiziellen DIN-Media-Seiten
inventarisiert. Besonders zu beachten ist, dass DIN 4108-2:2013-02 inzwischen
durch DIN 4108-2:2026-05 ersetzt wurde. Welche Ausgabe fuer die konkrete
Masterarbeit methodisch gilt, muss vor Aktivierung des Nachweises festgelegt
werden.

## Verbindlicher Tabellenoutput

Die Zonenkennwerttabelle fuehrt mindestens:

- Modell, Variante, Zone, Gruppe, Zonenmultiplikator und Bezugsflaeche,
- Luft- und operative Temperatur als Minima/Maxima,
- Heiz- und Kuehlenergie absolut und spezifisch,
- Heiz-, Kuehl- und Lueftungsleistung absolut beziehungsweise spezifisch,
- Zu-/Abluftvolumenstrom sowie solaren Eintrag,
- relative Feuchte, CO2, PPD und Luftalter,
- Nutzungs-, Uebertemperatur-, Personen- und unerfuellte Stunden,
- Uebertemperaturgradstunden,
- Quelle, Zeitraum, Einheit, Datenabdeckung und Auswertungsstatus.

Gebaeudewerte verwenden fuer Leistungen einen zeitgleichen Peak; individuelle
Zonenmaxima werden nicht addiert. Nicht belegte Werte bleiben leer und werden
nicht geschaetzt.

## Spaeterer Diagrammoutput

- Lasten: Heating und Cooling als Zeitreihen, einzeln und kombiniert.
- Komfort: operative Temperatur mit Sollbereich; optional PMV/PPD und
  Belegung, sofern die erforderlichen Daten vorliegen.
- Wettervergleich: Aussenlufttemperatur als Linie, Niederschlag als Linie auf
  der rechten Sekundaerachse und monatliche Solarstrahlung als Balken oder
  Flaeche auf einer weiteren rechten Achse.
- Belegungsvariation: Tagesgang von Belegung und Energie/Leistung sowie eine
  Kennwerttabelle der verglichenen Varianten.
- Varianten: Delta-Tabelle gegen eine explizite Basis; keine automatische
  Auswahl einer optimalen Variante.

Die Gestaltung wird nach Stabilisierung von Daten und Tabellen anhand von
Beispielen im Q&A festgelegt. Alle 5Z-Zonen koennen ausgegeben werden; fuer
den Haupttext wird spaeter eine fachlich begruendete Zone ausgewaehlt.

## Noch zu beschaffen oder zu entscheiden

1. Projektrelevante Ausgabe der DIN 4108-2 (2013 oder 2026) und der daraus
   anzuwendende Nachweisweg.
2. Volltexte beziehungsweise zulaessige Arbeitskopien der oben genannten
   Regelwerke sowie Eintrag im Normen-Quelleninventar.
3. Komfort-/Raumluftkategorie, Nutzungs- und Belegungsprofil je Zonentyp.
4. Semantik der IDA-Zeitstempel und Leistungswerte fuer die abschliessende
   Reproduzierbarkeitsfreigabe.
5. Kopplung des separat aufgebauten Rechenzeit-Manifests; Dateizeitstempel
   werden nicht als Laufzeitnachweis verwendet.

Die oeffentliche EQUA-Produktdokumentation bestaetigt variable Solver-
Zeitschritte und verweist fuer IDA ICE 5 auf das interne/online Help Center,
belegt aber in der auffindbaren oeffentlichen Dokumentation nicht eindeutig,
ob die exportierten PRN-Leistungswerte Stuetzstellen oder Intervallmittel
darstellen. Dieses Gate kann daher nicht durch eine stille Annahme geschlossen
werden.
