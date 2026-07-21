# P013 - Gesamtkonzept `ma_zones`

**Stand:** 15. Juli 2026
**Status:** Fachlich konsolidiert; LoD-1-Demo, P013-S3b-Abschlussvertrag und P013-S3c-Releasecheckpoint umgesetzt
**Modul:** `ma_zones`
**UI-Bezeichnung:** Zonen
**Prioritaet:** hoch innerhalb der Eingangsdatenkette
**Bestehender Umsetzungsstand:** LoD-1-Demo und referenz-only P013-/P014-Handover vorhanden; vor jeder Aenderung ist der vorhandene Code zu analysieren
**Ersetzt beziehungsweise erweitert:** bisherigen Kurzplan P013 zu Zonen und Nutzungen

---

# 1. Kennzeichnungssystem dieses Plans

Zur eindeutigen Pflege durch Codex werden folgende Markierungen verwendet:

* **[ENTSCHEIDUNG]** verbindlich festgelegter Projektstand
* **[OFFEN]** noch nicht abschliessend entschiedener Punkt
* **[ZUKUNFT]** bewusst zurueckgestellte Erweiterung
* **[UMSETZUNG]** daraus abzuleitendes Arbeitspaket
* **[MODULWIRKUNG: Modulname]** Entscheidung betrifft zusaetzlich ein anderes Modul
* **[DOKUMENTATION]** Leitfaeden, Plaene oder Entscheidungsregister muessen angepasst werden

Neue Entscheidungen und offene Fragen sollen mit fortlaufenden IDs ergaenzt werden:

```text
ZON-DEC-001
ZON-OPEN-001
ZON-FUT-001
```

Entscheidungen duerfen nicht nur im Fliesstext geaendert werden. Sie sind zusaetzlich im Entscheidungsregister dieses Plans und gegebenenfalls in den zentralen Nutzerentscheidungen zu dokumentieren.

---

# 2. Ziel des Moduls

`ma_zones` bildet die fachliche Verbindung zwischen:

* dem geometrischen Gebaeudemodell aus `ma_building`,
* den zentralen technischen Systemen und verfuegbaren technischen Datensaetzen aus `ma_technical`,
* den Nutzungs- und Betriebsbedingungen,
* den zonenbezogenen Uebergabesystemen,
* und der spaeteren Parameter- und Variantenbildung.

Das Modul verwaltet insbesondere:

* Raum-Zonen-Zuordnung,
* Nutzungsprofile,
* Personenbelegung,
* Geraete und interne Lasten,
* Beleuchtung,
* Zeitprofile,
* Heiz- und Kuehlsollwerte,
* Konditionierungsarten,
* zonenbezogene Waerme-, Kaelte- und Luftuebergabe,
* Zuordnung zu zentralen technischen Systemen,
* Fensteroeffnungs- und Sonnenschutzprofile,
* projektweite Feiertagseinstellungen, solange noch keine zentrale Kalenderverwaltung existiert.

`ma_zones` erzeugt keine Gebaeudegeometrie und definiert keine zentralen Erzeugungsanlagen.

---

# 3. Verbindlicher Gesamtworkflow

## 3.1 Reihenfolge der Eingangsmodule

**[ENTSCHEIDUNG ZON-DEC-001]**

Die Eingangsmodule werden in folgender Reihenfolge bearbeitet:

```text
ma_weather
-> ma_building
-> ma_technical
-> ma_zones
-> ma_validation - Eingabecheckpoint
-> ma_parameters
-> ma_validation - Parametercheckpoint
-> ma_variants
-> ma_simulation_setup
-> ma_export_simulation
-> externe Simulation
-> ma_import_simulation
-> ma_analyse
```

Begruendung:

* `ma_weather` stellt Standort- und Wetterdaten bereit.
* `ma_building` stellt Gebaeude, Raeume, Bauteile, Fenster und Sonnenschutz bereit.
* `ma_technical` definiert zentrale Systeme, Kreise, AHU, Plant, Electrical und verfuegbare generische technische Datensaetze.
* `ma_zones` verbindet Raeume, Nutzung, Konditionierung und zonenbezogene Uebergabe mit den bereits definierten technischen Systemen.
* `ma_parameters` sammelt erst danach alle freigegebenen Eingabedaten.

**[MODULWIRKUNG: ma_workflow, ma_ui, ma_technical, ma_parameters, zentrale Projektplaene]**

Die bisherige Modulreihenfolge ist in Workflow-Katalog, Dashboard, Gesamtprojektplan und Modulabhaengigkeiten zu aktualisieren.

---

## 3.2 Beziehung zwischen Projekt, Gebaeude, Zone, Raum, Run und Variante

**[ENTSCHEIDUNG ZON-DEC-002]**

Fuer den aktuellen Projektumfang gilt:

```text
Ein Projekt
+-- ein Gebaeude
    +-- mehrere Zonen
        +-- jeweils ein oder mehrere Raeume
```

Zusaetzlich gilt:

* Ein Raum gehoert innerhalb eines Zonenstands genau einer Zone an.
* Eine Zone besteht aus mindestens einem vollstaendigen Raum.
* Ein Raum wird im MVP nicht auf mehrere Zonen aufgeteilt.
* Ein Run enthaelt eine festgelegte Menge vollstaendiger Gebaeudevarianten.
* Jede Variante beschreibt das gesamte Gebaeude einschliesslich aller Zonen.
* Eine Variante simuliert nicht nur eine einzelne Zone.
* Die Raum-Zonen-Zuordnung bleibt innerhalb eines Runs unveraendert.
* Eine Aenderung der Zonenzuordnung erfordert einen neuen Zonenstand und grundsaetzlich einen neuen Run.

---

# 4. Modulabgrenzung

## 4.1 `ma_building`

`ma_building` ist zustaendig fuer:

* Gebaeudegeometrie,
* Geschosse,
* Raeume,
* Raumflaechen und Raumvolumen,
* Bauteile,
* Fenster,
* Tueren,
* Sonnenschutzeinrichtungen,
* Bauteil- und Oeffnungsgeometrie,
* geometrische Raumvalidierung,
* Festlegung, ob ein Objekt ein Raum oder ein Hohlraum ist.

`ma_zones` erhaelt ausschliesslich durch `ma_building` freigegebene Raumobjekte.

**[ENTSCHEIDUNG ZON-DEC-003]**

Der Status `invalid` ist kein regulaerer Raumstatus in `ma_zones`. Geometrisch oder strukturell ungueltige Raeume muessen bereits im Validierungsschritt von `ma_building` geklaert werden.

---

## 4.2 `ma_technical`

`ma_technical` ist zustaendig fuer gebaeudeweite und zentrale technische Systeme:

* Plant,
* AHU,
* Electrical,
* zentrale Waerme- und Kaelteerzeugung,
* zentrale Anlagenleistungen,
* Speicher,
* Verteilsysteme und Kreise,
* Vor- und Ruecklauftemperaturen,
* Energietraeger,
* zentrale Lueftungsanlagen,
* verfuegbare generische technische System- und Komponentendaten.

`ma_technical` wird vor `ma_zones` bearbeitet.

`ma_zones` referenziert anschliessend:

* Heizkreise,
* Kuehlkreise,
* AHU,
* zentrale Versorgungssysteme,
* verfuegbare Uebergabesysteme und generische Datensaetze.

**[ENTSCHEIDUNG ZON-DEC-004]**

Zentrale Anlagenleistungen werden ausschliesslich in `ma_technical` festgelegt.

Zonenbezogene Uebergabesysteme, lokale Leistungen, Mengen und Zuordnungen werden in `ma_zones` bearbeitet.

---

## 4.3 `ma_parameters`

`ma_parameters` uebernimmt alle freigegebenen Werte aus:

* `ma_weather`,
* `ma_building`,
* `ma_technical`,
* `ma_zones`.

`ma_parameters` hat anschliessend einen zweiten Bearbeitungsschritt, in dem festgelegt wird:

* welche Werte fuer den Run konstant bleiben,
* welche Werte fuer Varianten freigegeben werden,
* welche zulaessigen Werte oder Wertebereiche gelten,
* welcher LoD-Umfang verwendet wird.

`ma_variants` greift nicht direkt auf `ma_zones` zu.

---

## 4.4 `ma_validation`

`ma_zones` prueft ausschliesslich eigene Moduleingaben.

Moduluebergreifende Pruefungen erfolgen ueber `ma_validation` an definierten Checkpoints.

---

## 4.5 `ma_analyse`

`ma_analyse` verarbeitet die spaeteren Ergebnisse und vergleicht insbesondere:

```text
statische Dimensionierung
-> statische oder vereinfachte Simulation
-> dynamische Simulation
-> dynamische simulationsgestuetzte Optimierung
```

Moegliche Vergleichswerte:

* Heizlast,
* Kuehllast,
* Uebergabeleistung,
* zentrale Erzeugerleistung,
* Luftvolumenstrom,
* Lastspitzen,
* Betriebsstunden,
* Energiebedarf,
* Sollwertabweichungen,
* Ueber- und Unterdimensionierung,
* thermischer Komfort.

**[MODULWIRKUNG: ma_analyse]**

Die Herkunft eines Wertes muss spaeter unterscheidbar sein, beispielsweise:

* statisch berechnet,
* extern importiert,
* dynamisch simuliert,
* ideales System,
* fest vorgegeben,
* generisches System,
* optimierte Auslegung.

---

# 5. Zonenverstaendnis

## 5.1 Einheitliches Zonenobjekt

**[ENTSCHEIDUNG ZON-DEC-005]**

Im Modul werden keine getrennten Objekttypen wie thermische Zone, Lueftungszone, Beleuchtungszone oder Versorgungszone eingefuehrt.

Es gibt ein allgemeines Zonenobjekt.

Dieses Zonenobjekt enthaelt beziehungsweise referenziert:

* Nutzung,
* Konditionierung,
* Sollwerte,
* interne Lasten,
* Zeitprofile,
* Lueftung,
* Beleuchtung,
* Fensterbetrieb,
* Sonnenschutzbetrieb,
* lokale Uebergabesysteme,
* zentrale Systemzuordnungen.

Die UI-Bezeichnung bleibt zunaechst **"Zonen"**.

---

## 5.2 Raum und Zone

Ein Raum ist das physische und geometrische Objekt aus `ma_building`.

Eine Zone ist eine fachliche Zusammenfassung eines oder mehrerer vollstaendiger Raeume, fuer die gemeinsame zonenbezogene Parameter gelten.

```text
Raum R-101 \
Raum R-102 +-> Zone Z-001
Raum R-103 /
```

Alle zonenbezogenen Werte werden ausschliesslich auf Zonenebene gespeichert.

Innerhalb einer Zone sind keine abweichenden Raumwerte vorgesehen.

Soll ein Raum abweichende Nutzungs-, Sollwert-, Profil- oder Konditionierungsdaten erhalten, muss er einer anderen oder neuen Zone zugeordnet werden.

---

## 5.3 Regel fuer die Zonenbildung

**[ENTSCHEIDUNG ZON-DEC-006]**

Raeume mit unterschiedlicher Nutzung oder unterschiedlicher Konditionierung bilden grundsaetzlich unterschiedliche Zonen.

Eine Zusammenfassung kann nur erfolgen, wenn:

* Nutzung und Konditionierung ausreichend gleichartig sind,
* oder eine fuer den Untersuchungszweck zulaessige normative Vereinfachung angewendet wird.

Normative Vereinfachungen muessen spaeter dokumentieren:

* angewandte Norm und Ausgabe,
* Regel beziehungsweise Ausnahme,
* betroffene Raeume,
* Begruendung,
* verwendete Ersatz- oder Mittelwerte,
* Gueltigkeit fuer den konkreten Untersuchungszweck.

Die geringe Raumgroesse allein ist keine automatische Begruendung fuer eine Zusammenfassung.

---

## 5.4 Keine Raumteilung im MVP

**[ENTSCHEIDUNG ZON-DEC-007]**

Ein Raum wird im MVP immer vollstaendig einer Zone zugeordnet.

Nicht vorgesehen:

```text
50 % von Raum R-101 -> Zone Z-001
50 % von Raum R-101 -> Zone Z-002
```

Ist eine physische oder simulationsrelevante Unterteilung erforderlich, muss sie zunaechst in `ma_building` als eigener Raum oder Teilraum erzeugt werden.

**[ZUKUNFT ZON-FUT-001]**

Raumstempel oder virtuelle Teilraeume koennen spaeter geprueft werden, beispielsweise fuer:

* Buehne,
* Zuschauerbereich,
* Eingangsbereich eines Saals.

Ein solcher Raumstempel muesste bei simulationswirksamer Nutzung mindestens Flaeche, Volumen, Begrenzungsflaechen und Elementzuordnungen abbilden.

---

# 6. Vollstaendigkeit der Raumzuordnung

## 6.1 Alle Raeume werden beruecksichtigt

**[ENTSCHEIDUNG ZON-DEC-008]**

In der ersten Programmversion werden alle durch `ma_building` freigegebenen Raeume betrachtet.

Jeder Raum muss einer Zone zugeordnet werden.

Nicht vorgesehen sind im MVP:

* ausgeschlossene Raeume,
* ignorierte Raeume,
* nicht simulierte Raeume,
* freie Ersatzrandbedingungen fuer entfernte Raeume.

Nicht konditionierte Raeume bleiben Bestandteil des Modells und erhalten eine passende Zone.

Waehrend der Bearbeitung darf ein Raum voruebergehend den Zustand "nicht zugeordnet" besitzen. Dieser Zustand verhindert den Abschluss von `ma_zones`.

---

## 6.2 Installationsschaechte und Hohlraeume

**[ENTSCHEIDUNG ZON-DEC-009]**

Die Behandlung ergibt sich aus `ma_building`:

```text
In ma_building als Raum definiert
-> Uebergabe an ma_zones
-> Zonenzuordnung erforderlich

Nicht als Raum definiert
-> Hohlraum oder Konstruktionsbestandteil
-> keine Uebergabe an ma_zones
```

Ein als Raum modellierter Installationsschacht muss ausgewaehlt und zoniert werden.

Ein nicht als Raum modellierter Bereich wird als Hohlraum behandelt und verbleibt in der Zustaendigkeit von `ma_building`.

**[MODULWIRKUNG: ma_building]**

`ma_building` muss eindeutig unterscheiden koennen zwischen:

* Raumobjekt,
* Installationsschacht als Raum,
* Konstruktionshohlraum,
* Luftschicht,
* Deckenhohlraum,
* Doppelbodenhohlraum.

**[OFFEN ZON-OPEN-001]**

Die detaillierte physikalische Behandlung beluefteter Schaechte, grosser Hohlraeume, Doppelboeden und abgehaengter Decken ist noch nicht geklaert. Die Grundregel Raum oder Hohlraum ist jedoch verbindlich.

---

# 7. Nutzung und Nutzungsprofile

## 7.1 Normative Profilgrundlagen

**[ENTSCHEIDUNG ZON-DEC-010]**

Es werden zwei Normfassungen parallel gefuehrt:

* DIN V 18599-10:2018-09,
* DIN/TS 18599-10:2025-10.

Projektregel:

* allgemeine und aktuelle fachliche Analysen verwenden primaer die Fassung 2025,
* eine ausdruecklich als GEG-Analyse gekennzeichnete Untersuchung verwendet die dafuer vorgesehene Fassung 2018,
* beide Fassungen bleiben unveraenderlich und ueberschreiben sich nicht.

Jedes Normprofil benoetigt mindestens:

```text
norm_series
norm_part
norm_edition
profile_number
profile_name
usage_category
source_table
source_reference
application_context
editable = false
```

---

## 7.2 Auswahl der Nutzungsprofile

Alle vorhandenen Nutzungsprofile bleiben grundsaetzlich auswaehlbar.

Beispiele:

* Einzelbuero,
* Gruppenbuero,
* Grossraumbuero,
* Besprechungsraum,
* Verkehrsflaeche,
* Lager,
* Sanitaer,
* Unterricht,
* Veranstaltung.

Es gibt keine Filterlogik, die ein Profil aufgrund eines vorher eingegebenen Raumtitels vollstaendig ausblendet.

Die Auswahl eines Nutzungsprofils laedt aber ausschliesslich die zu diesem Profil gehoerenden Daten.

---

## 7.3 Profilpaket und getrennte Einzelprofile

**[ENTSCHEIDUNG ZON-DEC-011]**

Ein ausgewaehltes Nutzungsprofil bildet den fachlichen Zuordnungsrahmen.

Es enthaelt beziehungsweise referenziert:

* skalare Nutzungswerte,
* Personenkennwerte,
* Geraetekennwerte,
* Beleuchtungskennwerte,
* Sollwerte,
* Aussenluftanforderungen,
* Belegungszeitprofil,
* Geraetezeitprofil,
* Beleuchtungszeitprofil.

Die Zeitprofile werden technisch als getrennte Einzelprofile gespeichert, bleiben aber eindeutig dem Nutzungsprofil zugeordnet.

```text
Nutzungsprofil Einzelbuero
+-- occupancy_schedule_id
+-- equipment_schedule_id
+-- lighting_schedule_id
+-- occupancy_density
+-- equipment_power_density
+-- lighting_power_density
+-- heating_setpoint
+-- cooling_setpoint
+-- weitere Profilparameter
```

Unbeabsichtigte Mischungen unterschiedlicher Normprofile sind zu verhindern.

Eine bewusste Abweichung erzeugt ein benutzerdefiniertes Projektprofil.

---

## 7.4 Benutzerdefinierte Profile

**[ENTSCHEIDUNG ZON-DEC-012]**

Benutzerdefinierte Profile werden primaer projektbezogen gespeichert.

Moeglicher Ablauf:

```text
Normprofil kopieren
-> Projektprofil bearbeiten
-> im Projekt verwenden
```

Ein Projektprofil kann zusaetzlich bewusst in eine zentrale Vorlagenbibliothek uebernommen werden:

```text
[Als zentrale Vorlage speichern]
```

Zentrale Vorlagen werden bei Nutzung in ein anderes Projekt kopiert. Es besteht keine veraenderliche Live-Verknuepfung zu bestehenden Projekten.

Normprofile bleiben unveraenderlich.

**[ZUKUNFT ZON-FUT-002]**

Die Uebertragbarkeit vollstaendiger Profil-, Geraete- und Variantendaten auf andere Arbeitsplaetze wird nur als langfristige Erweiterung gefuehrt. Portable Projektsnapshots sind nicht Bestandteil des MVP.

---

# 8. Personen und Aktivitaet

Fuer jede Zone werden mindestens benoetigt:

* Eingabemethode,
* Personenanzahl oder Belegungsdichte,
* Belegungszeitprofil,
* Aktivitaetsklasse.

Moegliche Eingabemethoden:

```text
absolute Personenzahl
Personen je m2
m2 je Person
```

Intern wird daraus eine eindeutige maximale Personenzahl berechnet.

Die wirksame Personenanzahl ergibt sich aus:

```text
maximale Personenanzahl x Zeitprofilwert
```

Beispiel:

```text
20 Personen x 0,75 = 15 anwesende Personen
```

**[UMSETZUNG]**

Fuer Aktivitaetsklassen sind normativ oder fachlich belegte Tabellenwerte zu uebernehmen. Zu klaeren und zu dokumentieren sind:

* metabolische Rate,
* sensible Waermeabgabe,
* latente Waermeabgabe,
* gegebenenfalls CO2- und Feuchteabgabe,
* Quelle und Normausgabe.

Freie manuelle Einzelwerte sind nicht Schwerpunkt des MVP.

---

# 9. Geraete und interne Lasten

## 9.1 Generische Geraeteeintraege

**[ENTSCHEIDUNG ZON-DEC-013]**

Fuer den MVP werden typische generische Geraete bereitgestellt.

Mindestfelder:

```text
Bezeichnung
Eingabemethode
Leistung [W] oder Leistungsdichte [W/m2]
Anzahl, soweit erforderlich
Zeitprofil
```

Moegliche generische Beispiele:

* Arbeitsplatz-PC,
* Notebook,
* Monitor,
* Drucker,
* Kopierer,
* Server beziehungsweise IT-Geraet,
* Kuechengeraet,
* sonstiges Geraet.

Eingabemethoden:

```text
unit_power:
Leistung [W] x Anzahl

power_density:
Leistungsdichte [W/m2] x Zonenflaeche
```

Eine Zone darf mehrere Geraete beziehungsweise Geraetegruppen enthalten.

Die maximal wirksame Geraetelast wird automatisch berechnet.

---

## 9.2 Datenverwaltung

Generische Geraete werden in einer zentral verwalteten technischen beziehungsweise fachlichen Datenquelle bereitgestellt.

In `ma_zones` erfolgt:

* Auswahl,
* Anzahl oder Leistungsdichte,
* Zeitprofilzuordnung,
* gegebenenfalls Anlage eines neuen projektbezogenen Datensatzes.

**[MODULWIRKUNG: ma_database, ma_core, ma_technical oder zentraler Katalogbereich]**

Vor der Implementierung ist zu pruefen, welche vorhandene Katalog- und Datenbankstruktur fuer generische Geraete verwendet werden soll. Es darf keine parallele Geraetebibliothek ausschliesslich innerhalb der UI entstehen.

---

# 10. Beleuchtung

Fuer den MVP werden gespeichert:

* Bezeichnung,
* Gesamtleistung oder Leistungsdichte,
* Bezugsflaeche,
* eigenes Beleuchtungszeitprofil,
* Steuerungsart.

**[ENTSCHEIDUNG ZON-DEC-014]**

Die Beleuchtung arbeitet im MVP zunaechst binaer:

```text
0 = aus
1 = an
```

Das Beleuchtungsprofil darf vom Belegungsprofil abweichen.

Nicht Bestandteil des MVP:

* detaillierte Tageslichtsimulation,
* kontinuierliche Dimmung,
* lichttechnische Leuchtenmodelle,
* Beleuchtungsstaerkeberechnung,
* vollstaendige tageslichtabhaengige Regelung.

**[ZUKUNFT ZON-FUT-003]**

Tageslicht und detaillierte Beleuchtungsanalyse werden spaeter im Analysekontext geprueft. Bei wachsendem Umfang koennen daraus eigene Analysebereiche oder Module entstehen.

---

# 11. Zeitprofile

## 11.1 Zeitprofilarten des MVP

Mindestens vorgesehen:

* Belegung,
* Geraete,
* Beleuchtung,
* Fensteroeffnung,
* Sonnenschutz.

Wertebereiche:

| Profil         | MVP-Werte |
| -------------- | --------- |
| Belegung       | 0 bis 1   |
| Geraete         | 0 bis 1   |
| Beleuchtung    | 0 oder 1  |
| Fensteroeffnung | 0 oder 1  |
| Sonnenschutz   | 0 oder 1  |

---

## 11.2 Tagestypen

**[ENTSCHEIDUNG ZON-DEC-015]**

Jedes Zeitprofil enthaelt:

* Werktag: Montag bis Freitag,
* Samstag,
* Sonntag.

Die zeitliche Aufloesung betraegt im MVP 30 Minuten.

Jeder Tagestyp enthaelt 48 Werte:

```text
00:00
00:30
01:00
...
23:30
```

Ein vollstaendiges Zeitprofil enthaelt damit zunaechst:

```text
3 Tagestypen x 48 Werte = 144 Werte
```

---

## 11.3 Eingabe und Mehrfachbearbeitung

Die Eingabe erfolgt tabellarisch mit festen Halbstundenschritten.

Die UI muss ermoeglichen:

* mehrere Zellen auszuwaehlen,
* mehrere zusammenhaengende Zeilen auszuwaehlen,
* einen Wert auf alle markierten Zellen anzuwenden,
* Zeitbereiche gemeinsam zu bearbeiten,
* einen Tagestyp zu kopieren,
* Werte zurueckzusetzen,
* Normwerte sichtbar, aber schreibgeschuetzt anzuzeigen.

Beispiel:

```text
08:00 bis 12:00 markieren
-> Wert 1,0 eingeben
-> alle betroffenen Halbstundenwerte werden gesetzt
```

---

## 11.4 Speicherung

Ein Zeitprofil besteht aus Profilkopf und Zeitwerten.

```text
Schedule
+-- schedule_id
+-- name
+-- schedule_type
+-- source_type
+-- source_reference
+-- resolution_minutes = 30
+-- editable
+-- version
```

```text
ScheduleValue
+-- schedule_id
+-- day_type
+-- time_index
+-- time
+-- value
```

`time_index` laeuft von 0 bis 47.

---

## 11.5 Ablageort

**[ENTSCHEIDUNG ZON-DEC-016]**

Zeitprofile werden im MVP innerhalb des fachlichen Bereichs von `ma_zones` verwaltet.

Das Datenmodell soll eine spaetere Verlagerung in eine zentrale Zeitprofilverwaltung ermoeglichen.

**[ZUKUNFT ZON-FUT-004]**

Bei wachsender Mehrfachnutzung koennen Zeitprofile spaeter beispielsweise unter `ma_core.schedules` oder in einer zentralen Datenbank gefuehrt werden.

---

# 12. Feiertage

## 12.1 Abfrage

**[ENTSCHEIDUNG ZON-DEC-017]**

In `ma_zones` wird einmal projektweit abgefragt:

```text
Feiertage beruecksichtigen?
[Ja]
[Nein]
```

Bei "Nein" erfolgt keine Feiertagszuordnung.

Bei "Ja" folgt:

```text
Welche Feiertage sollen beruecksichtigt werden?
[Deutschlandweit]
[Bundeslandspezifisch]
```

---

## 12.2 Bundeslandspezifische Feiertage

Bei bundeslandspezifischer Auswahl wird der Standort aus `ma_weather` verwendet.

Das Bundesland soll automatisch aus den Standortdaten ermittelt und in `ma_zones` angezeigt werden.

**[MODULWIRKUNG: ma_weather, ma_database]**

Erforderliche Standortdaten koennen sein:

* Gemeinde oder Stadt,
* Postleitzahl,
* Koordinaten,
* Bundesland,
* amtlicher Schluessel.

Langfristig ist eine koordinatenbasierte Zuordnung robuster als eine reine Staedtenamenliste.

---

## 12.3 Behandlung erkannter Feiertage

Im MVP werden erkannte Feiertage wie Sonntage behandelt.

```text
holiday_day_type = sunday
```

Die Feiertagseinstellung wird zunaechst in der Oberflaeche von `ma_zones` bearbeitet, gilt aber nur einmal fuer das gesamte Projekt.

**[ZUKUNFT ZON-FUT-005]**

Eine spaetere zentrale Projektkalenderverwaltung kann diese Daten aus `ma_zones` herausloesen.

---

# 13. Konditionierung

Fuer jede Zone wird festgelegt, welche Funktionen vorhanden sind:

* Heizung,
* Kuehlung,
* natuerliche Lueftung,
* mechanische Lueftung,
* kombinierte Lueftung,
* Beleuchtung,
* Fensteroeffnung,
* Sonnenschutz.

Es werden keine getrennten Zonentypen erzeugt. Die Konditionierung ist eine Eigenschaft der Zone.

---

# 14. Heiz- und Kuehlsollwerte

## 14.1 MVP

**[ENTSCHEIDUNG ZON-DEC-018]**

Heiz- und Kuehlsollwerte werden im MVP zunaechst als feste Werte gespeichert.

```text
setpoint_mode = fixed
```

Ein Heizsollwert ist nur erforderlich, wenn Heizung aktiv ist.

Ein Kuehlsollwert ist nur erforderlich, wenn Kuehlung aktiv ist.

Es gibt keine pauschale Validierungsregel, die unabhaengig vom Simulationszeitraum immer beide Sollwerte verlangt.

---

## 14.2 Validierung

Die Validierung beruecksichtigt:

* aktivierte Konditionierungsart,
* Simulationszeitraum,
* saisonale Betriebsfreigabe,
* moegliche zeitliche Ueberschneidung von Heiz- und Kuehlbetrieb.

```text
Heizung aktiv
-> Heizsollwert erforderlich

Kuehlung aktiv
-> Kuehlsollwert erforderlich

Nur Sommerbetrachtung
-> Heizsollwert nicht zwingend erforderlich

Nur Winterbetrachtung
-> Kuehlsollwert nicht zwingend erforderlich
```

**[OFFEN ZON-OPEN-002]**

Die konkrete Regel fuer gleichzeitig freigegebenen Heiz- und Kuehlbetrieb ist noch festzulegen. Es soll keine ungepruefte allgemeine Totzonenregel in das MVP eingebaut werden.

---

## 14.3 Spaetere Sollwertprofile

**[ZUKUNFT ZON-FUT-006]**

Spaeter sollen zeitabhaengige Sollwerte unterstuetzt werden koennen, beispielsweise:

* ausserhalb der Oeffnungszeit,
* Vorheiz- oder Vorkuehlphase,
* regulaere Nutzungszeit,
* Absenkphase,
* Nachlaufphase.

```text
setpoint_mode:
- fixed
- scheduled
```

Fuer `scheduled` ist spaeter zu entscheiden, ob Halbstundentabellen oder definierte Betriebsphasen verwendet werden.

---

# 15. Zonenbezogene Uebergabesysteme

## 15.1 Bearbeitung in `ma_zones`

**[ENTSCHEIDUNG ZON-DEC-019]**

Zonenbezogene Uebergabesysteme werden in einem eigenen Reiter in `ma_zones` ausgewaehlt und konfiguriert.

Moegliche Bereiche:

### Heizung

* Heizkoerper,
* Konvektor,
* Fussbodenheizung,
* Wandheizung,
* Deckenheizung,
* Luftheizung,
* Bauteilaktivierung,
* generisches benutzerdefiniertes System.

### Kuehlung

* Kuehldecke,
* Kuehlsegel,
* Fussbodenkuehlung,
* Bauteilaktivierung,
* Umluftkuehlgeraet,
* Luftkuehlung,
* generisches benutzerdefiniertes System.

### Lueftung

* natuerliche Lueftung,
* mechanische Lueftung,
* kombinierte Lueftung,
* Zu- und Abluft,
* AHU-Zuordnung,
* zonenbezogener Volumenstrom.

---

## 15.2 Auslegungsarten

Fuer den MVP werden drei grundlegende Modi benoetigt:

```text
ideal
fixed_capacity
generic_system
```

### `ideal`

* keine explizite Leistungsbegrenzung,
* Simulation ermittelt erforderlichen Bedarf,
* geeignet fuer dynamische Last- und Dimensionierungsanalysen.

### `fixed_capacity`

* Nutzer gibt eine maximale Zonenleistung vor,
* geeignet zur Pruefung von Unter- und Ueberdimensionierung.

### `generic_system`

* Auswahl eines generischen Systemdatensatzes,
* Verwendung vereinfachter technischer Kennwerte.

Konkrete Herstellerprodukte werden fuer den MVP nicht benoetigt.

---

## 15.3 Ideales System

**[ENTSCHEIDUNG ZON-DEC-020]**

Wird keine explizite Leistung oder kein generisches System ausgewaehlt, kann ein ideales Uebergabesystem verwendet werden.

Ein ideales System ist kein reales Produkt, sondern ein nicht oder ausreichend hoch leistungsbegrenztes Simulationssystem zur Bedarfsermittlung.

---

## 15.4 Generische technische Datensaetze

**[ENTSCHEIDUNG ZON-DEC-021]**

Fuer alle relevanten Bereiche werden generische Datensaetze bereitgestellt.

Moegliche Mindestfelder eines generischen Uebergabesystems:

```text
Bezeichnung
Systemart
Anwendungsbereich
Nennleistung oder Leistungskennwert
Bezugsbedingungen
zulaessige Betriebsbedingungen
Anzahl
Gesamtleistung
Quelle beziehungsweise Demo-Kennzeichnung
```

Generische Datensaetze muessen ausdruecklich als generisch oder beispielhaft gekennzeichnet werden.

Keine vollstaendige Hersteller-, Kosten- oder Umweltproduktdatenbank im MVP.

---

## 15.5 Mehrere Systeme und Produkttypen

Eine Zone darf mehrere unterschiedliche Uebergabesystemeintraege besitzen.

Begruendung:

* unter verschiedenen Fenstern koennen unterschiedlich lange Heizkoerper erforderlich sein,
* mehrere Systemarten koennen gemeinsam wirken,
* spaetere Produktkombinationen muessen strukturell moeglich bleiben.

Beispiel:

```text
Zone Z-001

Heizkoerper Typ A - 1.000 mm - Anzahl 2
Heizkoerper Typ B - 1.400 mm - Anzahl 1
```

Die physischen Fenster und Wandflaechen werden aus `ma_building` referenziert.

---

## 15.6 Prozentanteil

**[ENTSCHEIDUNG ZON-DEC-022]**

Jeder Uebergabesystemeintrag muss bei Bedarf einen Prozentwert aufnehmen koennen.

```text
share_percent
```

Bei einem einzelnen System kann automatisch 100 % gesetzt werden.

Bei mehreren Systemen muss die Summe innerhalb der jeweiligen Konditionierungsart grundsaetzlich pruefbar sein.

**[OFFEN ZON-OPEN-003]**

Die fachliche Bezugsgroesse des Prozentwertes ist noch nicht abschliessend entschieden:

* Anteil am Leistungsbedarf,
* Anteil an der installierten Leistung,
* Anteil an der versorgten Flaeche,
* oder anderer projektspezifischer Anteil.

Diese Entscheidung ist vor Implementierung der Berechnungslogik erforderlich. Das Feld kann bereits strukturell vorgesehen werden, darf aber nicht ohne definierte Bedeutung ausgewertet werden.

---

## 15.7 Spaetere Produktlogik

**[ZUKUNFT ZON-FUT-007]**

Spaeter koennen konkrete Produkte ergaenzt werden mit:

* Hersteller,
* Typ,
* Abmessungen,
* Nennleistung,
* Leistung bei Systemtemperaturen,
* Kosten,
* GWP,
* EPD,
* verfuegbare Einbauflaeche,
* Produktkombinationen,
* Optimierung nach Leistung, Kosten oder Nachhaltigkeit.

Die Produktauswahl kann spaeter passende Kombinationen fuer eine Zone vorschlagen.

---

# 16. Fensteroeffnung und Sonnenschutz

## 16.1 Physische Elemente

**[ENTSCHEIDUNG ZON-DEC-023]**

Fenster und Sonnenschutzelemente werden physisch und geometrisch in `ma_building` gespeichert.

`ma_zones` speichert keine Kopie der Bauteile.

---

## 16.2 Referenzen und Betrieb

`ma_zones` referenziert:

* Fenster-IDs,
* oeffenbare Elemente,
* Sonnenschutz-IDs,
* zugehoerige Zeitprofile.

Beispiel:

```text
Zone Z-001
+-- Fenstergruppe
|   +-- F-001
|   +-- F-002
|   +-- window_opening_schedule_id
+-- Sonnenschutzgruppe
    +-- SH-001
    +-- SH-002
    +-- shading_schedule_id
```

Die Zeitprofile werden zunaechst in `ma_zones` gespeichert.

**[MODULWIRKUNG: ma_building]**

Fenster und Sonnenschutz benoetigen stabile IDs und eine eindeutige Raum- beziehungsweise Zonenreferenzierung.

---

# 17. Manuelle Zonenbildung

## 17.1 MVP

**[ENTSCHEIDUNG ZON-DEC-024]**

Im MVP erfolgt keine automatische Raum-Zonen-Zuordnung.

Der Nutzer:

1. legt eine Zone an,
2. waehlt einen oder mehrere Raeume,
3. ordnet diese der Zone zu,
4. waehlt Nutzung und Profile,
5. definiert Konditionierung und Uebergabesysteme.

Unterstuetzende UI-Funktionen:

* Mehrfachauswahl,
* Filter nach Geschoss,
* Filter nach Raumname,
* Filter nach Zuordnungsstatus,
* Sortierung,
* gemeinsame Zuordnung ausgewaehlter Raeume.

---

## 17.2 Zukunftsidee Zonierungsvorschlag

**[ZUKUNFT ZON-FUT-008]**

Spaeter kann ein unverbindlicher Erstvorschlag erstellt werden.

Dieser darf keine automatische verbindliche Zuordnung durchfuehren.

Moegliche Datenbasis:

* explizite Raumnutzungsart aus Raumbuch oder `ma_building`,
* Raumname als unterstuetzender Hinweis,
* Geschoss,
* Konditionierungsvorlage,
* technische Versorgung,
* gleiche Profile,
* raeumliche Naehe.

Personenwerte bleiben in `ma_zones` und werden nicht dauerhaft in `ma_building` dupliziert.

Die Konditionierung kann nicht zuverlaessig allein aus dem Raumnamen abgeleitet werden.

---

# 18. Benutzeroberflaeche

## 18.1 Hauptreiter

**[ENTSCHEIDUNG ZON-DEC-025]**

Fuer die erste Version sind folgende Hauptreiter vorgesehen:

```text
1. Uebersicht
2. Raumzuordnung
3. Nutzung und interne Lasten
4. Zeitprofile
5. Konditionierung und Uebergabe
6. Zusammenfassung und Pruefung
```

Produkte beziehungsweise generische Systemdaten werden zunaechst im jeweiligen fachlichen Reiter bearbeitet und erhalten keinen eigenen Hauptreiter.

---

## 18.2 Uebersicht

Anzeigen:

* Raeume insgesamt,
* zugeordnete Raeume,
* nicht zugeordnete Raeume,
* Anzahl Zonen,
* Bearbeitungsstatus,
* modulinterne Fehler und Warnungen.

---

## 18.3 Raumzuordnung

Tabellarische Darstellung:

| Auswahl | Raum-ID | Raumname | Geschoss | Flaeche | Zone |
| ------- | ------- | -------- | -------- | -----: | ---- |

Funktionen:

* mehrere Raeume auswaehlen,
* Zone neu anlegen,
* Zone zuordnen,
* Raeume verschieben,
* Zone umbenennen,
* Zone loeschen,
* nicht zugeordnete Raeume hervorheben.

---

## 18.4 Nutzung und interne Lasten

Anzeigen und bearbeiten:

* Nutzungsprofil,
* Normfassung,
* Personen,
* Aktivitaetsklasse,
* Geraete,
* Beleuchtung,
* zugehoerige Quellen,
* uebernommene Normwerte,
* projektbezogene Abweichungen.

---

## 18.5 Zeitprofile

Fuer jede Profilart:

* Tabelle mit 48 Halbstundenschritten,
* Spalten Werktag, Samstag, Sonntag,
* Mehrfachbearbeitung,
* Kopieren,
* Zuruecksetzen,
* Quellen- und Versionsanzeige.

Die Feiertagseinstellung wird in diesem Bereich einmal projektweit angezeigt.

---

## 18.6 Konditionierung und Uebergabe

Anzeigen und bearbeiten:

* Heizung aktiv,
* Kuehlung aktiv,
* Lueftungsart,
* feste Sollwerte,
* Uebergabesysteme,
* Auslegungsmodus,
* Leistung,
* generischer Datensatz,
* Anzahl,
* Prozentanteil,
* Heiz- beziehungsweise Kuehlkreis,
* AHU,
* referenzierte Fenster und Sonnenschutzelemente.

---

## 18.7 Zusammenfassung und Pruefung

Je Zone:

* Raeume,
* Nutzung,
* Normprofil,
* Personen und Lasten,
* Zeitprofile,
* Konditionierung,
* Uebergabesysteme,
* zentrale Systemzuordnungen,
* Herkunft der Werte.

Abschlussfunktion:

```text
[Moduleingaben pruefen]
```

---

# 19. Modulinterne Pruefung

## 19.1 Zustaendigkeit

**[ENTSCHEIDUNG ZON-DEC-026]**

`ma_zones` prueft ausschliesslich eigene Eingaben.

Geprueft werden unter anderem:

* jeder Raum ist genau einer Zone zugeordnet,
* keine Zone ist leer,
* Zonen-IDs sind eindeutig,
* Nutzungsprofil vorhanden,
* Pflichtwerte der aktiven Konditionierung vorhanden,
* Zeitprofile vollstaendig,
* Wertebereiche gueltig,
* generische Geraeteangaben vollstaendig,
* Referenzen auf Fenster und Sonnenschutz formal vorhanden,
* Referenzen auf ausgewaehlte technische Systeme vorhanden,
* Auslegungsmodus und erforderliche Felder passen zusammen.

Nicht geprueft werden in `ma_zones`:

* ausreichende zentrale Anlagenleistung,
* vollstaendige moduluebergreifende Konsistenz,
* normativer Gesamtnachweis,
* Eignung des Variantenraums,
* tatsaechliche Unter- oder Ueberdimensionierung nach Simulation.

---

## 19.2 Validierungscheckpoint vor `ma_parameters`

Nach Abschluss aller Eingangsmodule erfolgt:

```text
ma_weather
ma_building
ma_technical
ma_zones
        v
ma_validation - Eingabecheckpoint
        v
ma_parameters
```

Pruefinhalte:

* moduluebergreifende IDs und Referenzen,
* Standort- und Wetterkonsistenz,
* Gebaeude- und Raumreferenzen,
* technische Systemreferenzen,
* vollstaendige Zonenversorgung,
* LoD-Pflichtdaten,
* Einheiten,
* grundsaetzliche Simulationsbereitschaft.

---

## 19.3 Validierungscheckpoint vor `ma_variants`

Nach `ma_parameters` erfolgt:

```text
ma_parameters
        v
ma_validation - Parametercheckpoint
        v
ma_variants
```

Pruefinhalte:

* aktueller Parameterstand,
* gueltige Wertebereiche,
* gueltige Auswahlmengen,
* Abhaengigkeiten zwischen Parametern,
* LoD-Konformitaet,
* Vollstaendigkeit eines Einvariantenfalls,
* keine veralteten Eingangsdaten.

**[MODULWIRKUNG: ma_validation]**

`ma_validation` ist als wiederverwendbarer Pruefservice an mehreren Workflow-Entscheidungspunkten zu behandeln.

---

# 20. Uebergabe an `ma_parameters`

## 20.1 Vollstaendiger Zonenstand

An `ma_parameters` werden mindestens uebergeben:

### Struktur

* Zone-ID,
* Zonenname,
* Raum-IDs,
* Zonenflaeche,
* Zonenvolumen,
* Nutzungsprofil,
* Konditionierungsstatus.

### Personen

* Eingabemethode,
* maximaler Wert,
* berechnete Personenzahl,
* Aktivitaetsklasse,
* Zeitprofil.

### Geraete

* Geraeteeintraege,
* Leistungen,
* Anzahl,
* Leistungsdichten,
* berechnete Gesamtleistung,
* Zeitprofil.

### Beleuchtung

* Leistung oder Leistungsdichte,
* Zeitprofil,
* Steuerungsart.

### Sollwerte

* Heizsollwert, wenn erforderlich,
* Kuehlsollwert, wenn erforderlich,
* Sollwertmodus.

### Lueftung

* Lueftungsart,
* Aussenluftwert und Bezugsart,
* Zeitprofil,
* AHU-Referenz.

### Uebergabesysteme

* Systemart,
* Auslegungsmodus,
* Leistung,
* generischer Datensatz,
* Anzahl,
* Prozentanteil,
* zentrale Systemreferenz.

### Fenster und Sonnenschutz

* referenzierte Element-IDs,
* Zeitprofile.

### Projektkalender

* Feiertage aktiv,
* Geltungsbereich,
* Bundesland,
* Feiertags-Tagestyp.

---

## 20.2 LoD-1-Variantenparameter

**[OFFEN ZON-OPEN-004]**

Die endgueltige Whitelist der in LoD 1 variierbaren Zonenparameter ist noch verbindlich festzulegen.

Als fachlich geeignete Kandidaten gelten derzeit:

* Belegungsdichte oder maximale Personenzahl,
* Geraetelast in W/m2,
* Beleuchtungsleistung in W/m2,
* Heizsollwert,
* Kuehlsollwert,
* Aussenluftvolumenstrom,
* feste Heizleistung,
* feste Kuehlleistung.

Vorerst nicht als strukturelle LoD-1-Variantenparameter vorgesehen:

* Raum-Zonen-Zuordnung,
* Anzahl Zonen,
* vollstaendige Aenderung der Zonierungsstruktur,
* Austausch der Gebaeudeelemente,
* freie Kombination beliebiger Normprofile.

Fensteroeffnungs- und Sonnenschutzprofile koennen spaeter oder optional variabel werden.

---

# 21. Varianten, Runs und Einfrieren

## 21.1 Einvariantenfall

Auch bei nur einer untersuchten Konfiguration wird ein vollstaendiger Variantendatensatz erzeugt.

```text
Run R-001
+-- Variante V-001
    +-- vollstaendiges Gebaeude
```

`ma_variants` bleibt daher auch bei nur einer Variante Bestandteil des Workflows.

---

## 21.2 Einfrieren des Zonenstands

**[ENTSCHEIDUNG ZON-DEC-027]**

Der verwendete Zonenstand wird eingefroren, wenn:

* die konkrete Variante generiert wird,
* beziehungsweise der dazugehoerige Run- oder Variantenordner erzeugt wird.

Der fachlich massgebende Ausloeser soll die Generierung des Variantendatensatzes sein. Die Ordnererstellung basiert anschliessend auf diesem Stand.

Bereits erzeugte Varianten duerfen durch spaetere Aenderungen in `ma_zones` nicht veraendert werden.

---

## 21.3 Aenderungen nach Uebergabe an `ma_parameters`

**[ENTSCHEIDUNG ZON-DEC-028]**

Wird `ma_zones` nach der Uebergabe an `ma_parameters` veraendert:

```text
ma_parameters.status = outdated
```

Folgen:

* Variantengenerierung wird blockiert.
* `ma_variants` zeigt eine Warnung.
* `ma_parameters` muss aktualisiert werden.
* der Parametercheckpoint von `ma_validation` muss erneut durchlaufen werden.

Moegliche Statuswerte:

```text
current
outdated
validation_required
```

Die Warnung soll mindestens anzeigen:

* welches Eingabemodul veraendert wurde,
* wann die Aenderung erfolgte,
* dass `ma_parameters` aktualisiert werden muss,
* dass keine neue Variante generiert werden darf.

**[MODULWIRKUNG: ma_parameters, ma_variants, ma_validation, ma_workflow]**

---

## 21.4 Aenderungen nach Variantenbildung

Bestehende Varianten bleiben unveraendert.

Eine Aenderung eines als variabel freigegebenen Parameters erzeugt eine neue Variante.

Eine Aenderung der Raum-Zonen-Struktur erzeugt einen neuen Zonenstand und grundsaetzlich einen neuen Run.

---

# 22. Externe Heiz- und Kuehllasten

**[ZUKUNFT ZON-FUT-009]**

Extern berechnete statische Heiz- und Kuehllasten koennen spaeter importiert werden.

Moegliche Quellen:

* externe Heizlastsoftware,
* Kuehllastsoftware,
* Hottgenroth,
* Excel,
* Fachplanungssoftware,
* manuelle Planungswerte.

Erforderliche Metadaten:

```text
value
unit
calculation_type
calculation_method
source_system
source_file
source_date
import_date
zone_reference
validation_status
```

Moegliche Statuswerte:

```text
imported_unchecked
imported_validated
manually_entered
internally_calculated
simulation_result
superseded
```

**[MODULWIRKUNG: ma_analyse, ma_import_simulation oder spaeterer Fachimport]**

---

# 23. Datenmodell - konzeptionelle Objekte

Die konkrete technische Struktur ist an den vorhandenen Code anzupassen.

Vorgesehene Fachobjekte:

```text
Zone
RoomZoneAssignment
UsageProfile
ProfileParameter
ZoneOccupancy
ZoneEquipment
ZoneLighting
Schedule
ScheduleValue
ZoneHeating
ZoneCooling
ZoneVentilation
ZoneEmissionSystem
ZoneBuildingElementScheduleAssignment
ProjectHolidaySettings
```

## 23.1 `Zone`

```text
zone_id
project_id
building_id
name
description
usage_profile_id
status
created_at
updated_at
```

## 23.2 `RoomZoneAssignment`

```text
assignment_id
zone_id
room_id
```

## 23.3 `ZoneEquipment`

```text
zone_equipment_id
zone_id
equipment_id
input_method
unit_power
power_density
quantity
schedule_id
calculated_total_power
source
```

## 23.4 `ZoneEmissionSystem`

```text
zone_emission_system_id
zone_id
conditioning_type
system_type
sizing_mode
fixed_capacity
generic_system_id
quantity
share_percent
central_system_reference
referenced_building_element_id
source
```

## 23.5 `Schedule`

```text
schedule_id
name
schedule_type
source_type
source_reference
resolution_minutes
editable
version
```

## 23.6 `ScheduleValue`

```text
schedule_id
day_type
time_index
time
value
```

## 23.7 Herkunftsangaben

Wichtige Werte erhalten eine Herkunft:

```text
norm_profile
user_profile
manual_input
generic_database
technical_database
calculated
imported
variant_override
```

---

# 24. MVP-Umfang

## 24.1 Verbindlich im MVP

* Modulname `ma_zones`
* UI-Bezeichnung "Zonen"
* manuelle Raum-Zonen-Zuordnung
* genau eine Zone je Raum
* mehrere Raeume je Zone
* alle Raeume muessen beruecksichtigt werden
* keine Raumteilung
* Nutzungsauswahl
* Normprofile 2018 und 2025 parallel
* Personen und Aktivitaetsklasse
* generische Geraete
* Beleuchtung
* Zeitprofile mit 48 Halbstundenwerten
* Werktag, Samstag, Sonntag
* Feiertage Ja/Nein
* deutschlandweite oder bundeslandspezifische Feiertage
* Feiertage wie Sonntag
* feste Heiz- und Kuehlsollwerte
* zonenbezogene Konditionierung
* ideales System
* feste Leistung
* generisches Uebergabesystem
* mehrere Uebergabesystemeintraege je Zone
* Referenz auf zentrale technische Systeme
* Fenster- und Sonnenschutzreferenzen
* modulinterne Pruefung
* Uebergabe an `ma_parameters`
* Veraltet-Status nach Aenderungen
* Sperre der Variantengenerierung bei veralteten Parametern
* Einfrieren des Zonenstands bei Variantengenerierung.

---

## 24.2 Nicht Bestandteil des MVP

* automatische Zonenbildung,
* verbindliche Zonierungsvorschlaege,
* Teilung eines Raumes,
* Tageslichtsimulation,
* kontinuierliche Beleuchtungsregelung,
* zeitabhaengige Sollwertprofile,
* vollstaendige Herstellerproduktdatenbank,
* optimierte Produktkombination,
* Import externer Lastberechnungen,
* portable Projektpakete fuer andere Arbeitsplaetze,
* zentrale allgemeine Zeitprofilverwaltung,
* vollstaendige normative Ausnahmepruefung,
* detaillierte Behandlung aller Hohlraum- und Schachtarten.

---

# 25. Umsetzungsphasen

## Phase P013-S2 - Plan- und Datenkonsolidierung

**[UMSETZUNG]**

* bestehenden Code und P013-S1 analysieren,
* diesen Gesamtplan mit dem Ist-Stand abgleichen,
* alte Aussagen zu rein thermischen Zonen korrigieren,
* Workflowreihenfolge aktualisieren,
* vorhandene DIN-Profildateien pruefen,
* Datenobjekte und Schnittstellen dokumentieren,
* LoD-1-Whitelist entscheiden.

Ergebnis:

* aktualisierter P013-Plan,
* aktualisiertes Entscheidungsregister,
* aktualisierte Modulabhaengigkeiten,
* keine ungepruefte Codeaenderung.

---

## Preprocess V1-Mindestumfang

Preprocess V1 benoetigt P013-S3 sowie eine bewusst kleine Teilmenge der
nachfolgenden Phasen: ein einfaches Nutzungs- und Zeitprofil, die Zuordnung zu
freigegebenen P014-Serviceinterfaces und einen fingerprintbaren Zonenstand
fuer P015. Die vollstaendige DIN-Profilbibliothek, Feiertagslogik,
Mehrfachbearbeitung und weitergehende Konditionierungsoptionen bleiben
Folgeslices.

## Phase P013-S3 - Raum-Zonen-Grundmodell

* mehrere Raeume und Zonen unterstuetzen,
* eindeutige Raum-Zonen-Zuordnung,
* manuelle Mehrfachauswahl,
* Zonenuebersicht,
* Blockierung nicht zugeordneter Raeume,
* Anbindung an freigegebene `ma_building`-Raeume.

---

## Phase P013-S4 - Nutzung und Normprofile

* DIN-Profile 2018 und 2025 importieren,
* Profilparameter vereinheitlichen,
* Normprofile schreibschuetzen,
* projektbezogene Profilkopien ermoeglichen,
* Personen, Aktivitaet, Geraete und Beleuchtung integrieren.

---

## Phase P013-S5 - Zeitprofile und Feiertage

* 48 Halbstundenwerte,
* Werktag, Samstag, Sonntag,
* Mehrfachbearbeitung,
* Feiertage Ja/Nein,
* Deutschland/Bundesland,
* Standortreferenz aus `ma_weather`,
* Feiertag wie Sonntag.

---

## Phase P013-S6 - Konditionierung und Uebergabe

* Heiz- und Kuehlsollwerte,
* Lueftungsart,
* ideale Systeme,
* feste Leistungen,
* generische Systeme,
* mehrere Systemeintraege,
* Prozentfeld,
* zentrale Systemreferenzen,
* Fenster- und Sonnenschutzgruppen.

---

## Phase P013-S7 - Parameter- und Workflowintegration

* vollstaendige Uebergabe an `ma_parameters`,
* Aenderungsfingerprint oder Versionskennung,
* Status `current/outdated`,
* Blockierung in `ma_variants`,
* Validierungscheckpoints,
* Einfrieren bei Variantengenerierung,
* Run- und Variantenreferenzen.

---

# 26. Akzeptanzkriterien

## Raum-Zonen-Zuordnung

* Jeder freigegebene Raum ist genau einer Zone zugeordnet.
* Keine Zone ist leer.
* Nicht zugeordnete Raeume blockieren den Abschluss.
* Raumteilung ist nicht moeglich.
* Aenderungen an der Zonenstruktur sind nachvollziehbar.

## Nutzung

* Profile aus 2018 und 2025 sind eindeutig getrennt.
* Normprofile sind unveraenderlich.
* Zugehoerige Einzelprofile werden korrekt geladen.
* Projektprofile koennen erstellt werden.
* Norm- und Quelleninformationen sind sichtbar.

## Zeitprofile

* Werktag, Samstag und Sonntag enthalten jeweils 48 Werte.
* Mehrere Werte koennen gemeinsam bearbeitet werden.
* Wertebereiche werden geprueft.
* Beleuchtung kann von Belegung abweichen.
* Feiertage koennen deaktiviert oder nach Deutschland/Bundesland aktiviert werden.
* Feiertage nutzen im MVP das Sonntagsprofil.

## Konditionierung

* Nur aktive Funktionen verlangen zugehoerige Sollwerte.
* Ideale, feste und generische Systeme sind unterscheidbar.
* Mehrere Uebergabesystemeintraege sind moeglich.
* zentrale technische Systeme koennen referenziert werden.
* Prozentanteile koennen gespeichert werden.
* die noch offene fachliche Bedeutung des Prozentwerts wird nicht stillschweigend angenommen.

## Workflow

* `ma_zones` liegt nach `ma_technical`.
* `ma_validation` prueft vor `ma_parameters`.
* `ma_validation` prueft erneut vor `ma_variants`.
* Aenderungen in `ma_zones` markieren `ma_parameters` als veraltet.
* `ma_variants` blockiert die Generierung bei veraltetem Parameterstand.
* bestehende Varianten bleiben unveraendert.
* jede Variante beschreibt das vollstaendige Gebaeude.

---

# 27. Auswirkungen auf andere Module und Dokumente

## 27.1 `ma_building`

**Zu aktualisieren:**

* Raumvalidierung verbleibt vollstaendig in `ma_building`.
* eindeutige Unterscheidung Raum oder Hohlraum,
* Installationsschacht als Raum wird an `ma_zones` uebergeben,
* Fenster und Sonnenschutz bleiben physische Building-Objekte,
* stabile IDs fuer Raeume, Fenster und Sonnenschutz,
* optionale Raumnutzungs-Hinweise nur fuer spaetere Zonierungsvorschlaege.

**Betroffene Plaene und Leitfaeden:**

* P012 beziehungsweise aktueller `ma_building`-Plan,
* Building-Datenmodell,
* Validierungsbeschreibung,
* Schnittstellenbeschreibung zu `ma_zones`.

---

## 27.2 `ma_technical`

**Zu aktualisieren:**

* Modul wird vor `ma_zones` eingeordnet.
* zentrale Anlagen und zentrale Leistungen bleiben in `ma_technical`.
* Plant, AHU und Electrical werden gebaeudeweit definiert.
* verfuegbare Kreise und Systeme muessen stabile Referenzen besitzen.
* generische Systemdaten muessen fuer `ma_zones` auswaehlbar sein.
* lokale Uebergabesystemkonfiguration erfolgt in `ma_zones`.

Der bisherige Rueckfluss "Zonenanforderungen an `ma_technical`" ist im Plan zu ueberpruefen und an den neuen Workflow anzupassen.

---

## 27.3 `ma_weather`

**Zu aktualisieren:**

* Standortdaten muessen fuer Bundeslandermittlung nutzbar sein.
* Bundesland oder eindeutige raeumliche Zuordnung ergaenzen.
* Schnittstelle fuer projektweiten Feiertagskalender vorbereiten.
* Deutschland bleibt raeumlicher Geltungsbereich der aktuellen Version.

---

## 27.4 `ma_parameters`

**Zu aktualisieren:**

* uebernimmt `ma_zones` nach dem ersten Validierungscheckpoint,
* sammelt den vollstaendigen Zonenstand,
* zweiter Schritt definiert feste und variable Parameter,
* LoD-1-Whitelist ergaenzen,
* Status `current`, `outdated`, `validation_required`,
* Aenderungen in `ma_zones` machen den Parameterstand ungueltig,
* Versions- oder Fingerprintvergleich vorsehen.

---

## 27.5 `ma_variants`

**Zu aktualisieren:**

* jede Variante enthaelt das vollstaendige Gebaeude,
* eine Variante ist auch bei nur einem Simulationsfall erforderlich,
* kein direkter Zugriff auf `ma_zones`,
* Generierung blockieren, wenn `ma_parameters` veraltet ist,
* verwendeten Zonenstand bei Generierung einfrieren,
* bestehende Varianten nicht nachtraeglich veraendern,
* Aenderung der Zonenstruktur fuehrt zu neuem Run.

---

## 27.6 `ma_validation`

**Zu aktualisieren:**

Zwei verbindliche Checkpoints:

```text
Checkpoint 1:
Eingabemodule -> ma_validation -> ma_parameters

Checkpoint 2:
ma_parameters -> ma_validation -> ma_variants
```

`ma_validation` uebernimmt:

* moduluebergreifende Konsistenz,
* technische Referenzen,
* Parameterraum,
* LoD-Vollstaendigkeit,
* Simulationsbereitschaft.

Normative Pruefungen koennen als eigener Pruefbereich ergaenzt und spaeter gegebenenfalls ausgelagert werden.

---

## 27.7 `ma_core`, `ma_database` und Kataloge

**Zu pruefen:**

* Ablage generischer Geraete,
* Ablage generischer Uebergabesysteme,
* zentrale Vorlagenbibliothek fuer Benutzerprofile,
* Standort-Bundesland-Zuordnung,
* spaetere zentrale Zeitprofilverwaltung,
* Parameterwoerterbuch fuer Normdaten.

Keine parallelen Datenbanken nur fuer die `ma_zones`-UI anlegen.

---

## 27.8 `ma_analyse`

**Zu ergaenzen beziehungsweise vorzumerken:**

* Vergleich statischer Dimensionierung,
* vereinfachte oder statische Simulation,
* dynamische Simulation,
* dynamische Optimierung,
* Herkunftsstatus von Leistungswerten,
* ideale Zonenleistungen,
* feste Leistungen,
* generische Systeme,
* spaeter externe Lastimporte,
* spaeter Tageslichtanalyse.

---

## 27.9 `ma_ui` und `ma_workflow`

**Zu aktualisieren:**

* neue Reihenfolge der Eingangsmodule,
* Hauptreiter von `ma_zones`,
* zwei Validierungsentscheidungspunkte,
* Statusanzeige fuer veraltete Parameter,
* blockierte Variantengenerierung,
* Ruecksprung zum betroffenen Modul,
* Fortschrittsstatus fuer vollstaendige Raumzuordnung.

---

## 27.10 Dokumentationsstruktur

Codex soll mindestens pruefen und gegebenenfalls aktualisieren:

* bestehenden P013-Plan,
* verbindlichen Gesamtprojektplan,
* `PLAN_STATUS.md`,
* `PLAN_INDEX.md`,
* Workflow-Katalog,
* technische Entscheidungen,
* Nutzerentscheidungen,
* offene Nutzerentscheidungen,
* Modulabhaengigkeiten,
* UI-Plan,
* `CHANGELOG.md`,
* relevante Modul-READMEs und Leitfaeden.

Es soll kein zweiter widerspruechlicher `ma_zones`-Hauptplan parallel zum bestehenden P013 angelegt werden, ohne den Planindex und den Status eindeutig anzupassen.

---

# 28. Entscheidungsregister

## Verbindliche Entscheidungen

| ID          | Entscheidung                                                                               |
| ----------- | ------------------------------------------------------------------------------------------ |
| ZON-DEC-001 | Workflow: weather -> building -> technical -> zones -> validation -> parameters                 |
| ZON-DEC-002 | Ein Projekt, ein Gebaeude, mehrere Zonen, mehrere vollstaendige Gebaeudevarianten je Run      |
| ZON-DEC-003 | Ungueltige Raeume werden in `ma_building` geklaert                                            |
| ZON-DEC-004 | Zentrale Leistungen in `ma_technical`, lokale Uebergabe in `ma_zones`                       |
| ZON-DEC-005 | Ein allgemeines Zonenobjekt, keine getrennten Zonentypen                                   |
| ZON-DEC-006 | Unterschiedliche Nutzung oder Konditionierung erzeugt grundsaetzlich unterschiedliche Zonen |
| ZON-DEC-007 | Keine Raumteilung im MVP                                                                   |
| ZON-DEC-008 | Alle freigegebenen Raeume muessen zoniert werden                                             |
| ZON-DEC-009 | Installationsschacht als Raum wird zoniert; sonst Hohlraum                                 |
| ZON-DEC-010 | Normfassungen 2018 und 2025 parallel                                                       |
| ZON-DEC-011 | Nutzungsprofil laedt eindeutig zugehoerige Einzelprofile                                     |
| ZON-DEC-012 | Benutzerprofile projektbezogen, optional kontrolliert zentralisierbar                      |
| ZON-DEC-013 | Generische Geraete mit Leistung oder Leistungsdichte und Anzahl                             |
| ZON-DEC-014 | Beleuchtung im MVP an/aus und unabhaengig von Belegung                                      |
| ZON-DEC-015 | Zeitprofile: Werktag, Samstag, Sonntag, 30 Minuten                                         |
| ZON-DEC-016 | Zeitprofile zunaechst in `ma_zones`                                                         |
| ZON-DEC-017 | Feiertage Ja/Nein; Deutschland/Bundesland; wie Sonntag                                     |
| ZON-DEC-018 | Sollwerte im MVP zunaechst fest                                                             |
| ZON-DEC-019 | Lokale Uebergabesysteme in eigenem `ma_zones`-Reiter                                        |
| ZON-DEC-020 | Ideales System ohne explizite Leistung moeglich                                             |
| ZON-DEC-021 | Generische technische Datensaetze im MVP                                                    |
| ZON-DEC-022 | Prozentfeld fuer Uebergabesysteme vorsehen                                                   |
| ZON-DEC-023 | Fenster und Sonnenschutz physisch in `ma_building`, Betrieb in `ma_zones`                  |
| ZON-DEC-024 | Keine automatische Zonenbildung im MVP                                                     |
| ZON-DEC-025 | Sechs Hauptreiter der UI                                                                   |
| ZON-DEC-026 | `ma_zones` prueft nur eigene Eingaben                                                       |
| ZON-DEC-027 | Zonenstand wird bei Variantengenerierung eingefroren                                       |
| ZON-DEC-028 | Zonenaenderung setzt `ma_parameters` auf veraltet und blockiert Varianten                   |

---

# 29. Offene Entscheidungen

## ZON-OPEN-001 - Sonderhohlraeume

Zu klaeren:

* detaillierte Behandlung beluefteter Schaechte,
* Doppelboeden,
* Deckenhohlraeume,
* groessere technische Hohlraeume,
* IDA-ICE-Abbildung dieser Faelle.

Die Grundregel Raum oder Hohlraum ist bereits entschieden.

---

## ZON-OPEN-002 - Gleichzeitiger Heiz- und Kuehlbetrieb

Zu klaeren:

* welche Regel gilt bei zeitlich ueberlappender Freigabe,
* ob eine Mindesttotzone geprueft wird,
* wie saisonale und zeitliche Betriebsprofile beruecksichtigt werden.

Keine pauschale Regel ohne Kontext implementieren.

---

## ZON-OPEN-003 - Bedeutung des Prozentwertes

Zu klaeren:

* Leistungsbedarfsanteil,
* installierter Leistungsanteil,
* versorgter Flaechenanteil,
* andere fachliche Bezugsgroesse.

Diese Entscheidung ist vor Berechnungslogik und automatischer Summenpruefung erforderlich.

---

## ZON-OPEN-004 - LoD-1-Variantenparameter

Die endgueltige Whitelist ist festzulegen.

Dabei ist zu entscheiden:

* welche Zonenparameter im ersten MVP variabel sein duerfen,
* welche nur als feste Eingabewerte uebergeben werden,
* welche Wertebereiche und Auswahlmengen gelten,
* ob Zeitprofilwechsel bereits LoD 1 sind.

---

## ZON-OPEN-005 - Konkrete DIN-Datenabbildung

Die bereits aufbereiteten DIN-Daten sind zu pruefen auf:

* vorhandene Zeitprofile,
* Profilparameter,
* Tabellen 2018 und 2025,
* 48 Halbstundenwerte,
* Aktivitaetsdaten,
* Einheiten,
* Quellen,
* Unterschiede der Normfassungen,
* eindeutige Zuordnung zu Profil-IDs.

Dies ist ueberwiegend ein Analyse- und Umsetzungsauftrag, kann aber neue fachliche Entscheidungen erzeugen.

---

# 30. Vorgaben fuer Codex

Vor jeder Umsetzung:

1. vorhandenen Code unter `src/ma_zones/` analysieren,
2. bestehende LoD-1-Demo und YAML-Struktur pruefen,
3. Abweichungen zwischen Ist-Stand und diesem Plan dokumentieren,
4. betroffene Fremdmodule identifizieren,
5. einen Umsetzungsplan vorlegen,
6. erst nach Freigabe Code aendern.

Codex darf:

* Entscheidungen dieses Plans nicht stillschweigend umdeuten,
* offene Entscheidungen nicht eigenstaendig als verbindlich festlegen,
* keine parallelen Datenmodelle oder Ordnerstrukturen anlegen,
* keine UI-Fachlogik implementieren, die nicht in den Fachservices vorhanden ist,
* keine bestehenden Varianten durch Aenderungen ueberschreiben.

Bei einer offenen Entscheidung soll Codex:

1. die konkrete technische Auswirkung erklaeren,
2. sinnvolle Alternativen nennen,
3. eine Empfehlung geben,
4. den Punkt als offen dokumentieren,
5. auf eine Nutzerentscheidung warten.

Neue Entscheidungen sind sowohl im Plan als auch im zustaendigen zentralen Entscheidungsdokument einzutragen.

---

# 31. Handover-Abgleich und Masterarbeits-MVP V1

## P013-S3b ThermalBuildingModel als Abschlussvertrag

Umgesetzt am 2026-07-14: `ThermalBuildingModel` referenziert die Building-
Revision, das Zonenmodell und eine freigegebene P014-Technikrevision nur ueber
stabile IDs, Revisionen und Content-Hash. Die Validierung blockiert
unzugeordnete oder unbekannte Raeume, unbekannte Zonen und unvollstaendige
oder nicht freigegebene Technikreferenzen.

Nach dem manuellen Raumregister und der validierten Zonenbildung liefert P013
ein kleines, neutrales `ThermalBuildingModel` als Abschlussobjekt fuer P018.
Es fasst nur bereits freigegebene Building- und Zonenreferenzen zusammen:

- Projekt-, Gebaeude-, Raum- und Zonen-IDs mit Revision und Content-Hash,
- Raum-zu-Zone-Zuordnung und thermische Nutzungs-/Konditionierungsangaben,
- Referenzen auf physische Fenster- und Sonnenschutzobjekte aus P012,
- Referenzen auf zentrale Serviceinterfaces aus P014,
- Quellen, Annahmen und Validierungsstatus.

Das Objekt dupliziert weder Geometrie noch Konstruktionen, technische
Nennleistungen oder Parameterwerte. Es ist keine neue Zonenbildung und kein
IDA-Exportmodell. P018 referenziert ausschliesslich eine freigegebene Revision
dieses Abschlussobjekts.

## P013-S3c / P015-S3b-T2 ReleasedZoneCheckpoint

Council-Beschluss vom 2026-07-15: Mira, Vera und Justus bilden eine
einstimmige 3/5-Mehrheit fuer einen kleinen, lokalen Referenzcheckpoint vor
P032-W2. P013 liefert daraus einen unveraenderlichen, payloadfreien
`ReleasedZoneHandover`.

- Der Fingerprint bindet den kanonischen vollstaendigen Zonenstand,
  sortierte Raum-Zonen-Zuordnungen, Building-ID/-Revision sowie die exakte
  P014-Modell-/Revisions-/Hash-Referenz. Reine Tuple-Reihenfolge aendert den
  Fingerprint nicht, jede fachliche Aenderung dagegen schon.
- P013 validiert Building-, Zone-, ThermalBuilding- und P014-Handover vor der
  Uebergabe und blockiert unvollstaendige, nicht freigegebene oder nicht
  zusammenpassende Referenzen.
- Der Handover enthaelt keine Raum-, Zonen-, Nutzungsprofil- oder technische
  Revisionsnutzlast. Er ist weder Persistenz noch ein P013-UI- oder
  P032-W3a-Slice.

Umgesetzt am 2026-07-15: `build_released_zone_handover(...)` erzeugt den
frozen `ReleasedZoneHandover` erst nach erfolgreicher Building-, Zone-,
ThermalBuilding- und P014-Pruefung. Die Revision wird deterministisch als
`ZONE-HANDOVER-<16 hex>` aus dem kanonischen Content-Hash abgeleitet. Die
synthetischen Tests decken Reihungsstabilitaet sowie fachliche Aenderungen an
Zone, Building und passendem P014-Triple ab; P015 uebernimmt nur dessen
Referenzmetadaten.

Abschlussnachweis: Der gemeinsame Fokuslauf fuer Zonen-, Parameter-,
Technik-, Workflow- und Architekturcontracts bestand mit `75 passed`; die
vollstaendige lokale Suite bestand mit `536 passed`. Der genaue Auditnachweis
inklusive Ruff- und Diff-Pruefung ist in Entscheidung 34 festgehalten.

## MVP-V1-Grenze

P013-S3b bleibt auf den Referenzfall mit wenigen manuell gepflegten Raeumen
und Zonen begrenzt. Automatische IFC-/BIM-Zonierung, vollstaendige
Sonnenschutzbibliotheken und weitergehende Komfortregelung bleiben
Folgeslices.

Der erste Referenzfall ist am 2026-07-14 als Einraum-Einzonenmodell
konkretisiert: `SPACE-BI-OFFICE-0001` wird vollstaendig der bestehenden Zone
`ZONE-BI-LOD1-0001` zugeordnet. Flaeche, Volumen und Buero-Nutzungsprofil
bleiben mit dem Building-LoD-1-Stand konsistent.

## Handover-Ergaenzung 2026-07-21

Die v2-Zielrichtung wird durch das technische Handover praezisiert:

- `ma_zones` besitzt die konkrete Zuordnung von Zonen zu
  `Heating`-, `Cooling`-, Luft- und DHW-Serviceinterfaces sowie lokale
  Uebergabesysteme und Regelung.
- `ma_technical` besitzt zentrale Erzeugung, Verteilung, AHU und
  DHW-Erzeugung; direkte `served_zone_ids` bleiben nur ein
  Migrationshinweis und werden nicht in einem v2-Technikmodell persistiert.
- Ein spaeterer Cross-Module-Checkpoint prueft Interfaceexistenz,
  Medien-/Terminalkompatibilitaet und die Zusammenfuehrung von DHW-Bedarf
  und Erzeugung.

Der bestehende MVP-Referenzfall und die additive Legacy-Kompatibilitaet
bleiben unveraendert.
