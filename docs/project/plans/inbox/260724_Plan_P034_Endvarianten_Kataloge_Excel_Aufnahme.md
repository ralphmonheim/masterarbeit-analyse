# P034 Endvarianten und Kataloge aus Excel aufnehmen

Stand: 2026-07-24

## Ziel

Die drei Endvarianten und die zugehoerigen Bauteil-, Material- und
Produktkataloge werden kontrolliert analysiert und in kanonische
Projektvertraege ueberfuehrt. Die Original-XLSX bleiben unveraendert und
werden nicht zur konkurrierenden Katalogwahrheit.

## Eingang

- `endvariante_01_29_thermische_zonen_v2.xlsx`
- `endvariante_02_5_zonen_innenwaende_entfernt_v2.xlsx`
- `endvariante_03_5_zonen_innenwaende_als_masse_v2.xlsx`
- `kataloge/demo_masterarbeit_bauteilkatalog.xlsx`
- `kataloge/demo_masterarbeit_materialkatalog.xlsx`
- `kataloge/demo_masterarbeit_produktkatalog.xlsx`

## Abgrenzung

- keine automatische Fachfreigabe von Excel-Werten
- keine Ueberschreibung bestehender lokaler oder versionierter Kataloge
- keine direkte Variantenwirkung behaupten, wenn Gebaeude, Wetter, Profile,
  Simulationsstand oder Auswertungszeitraum abweichen
- keine ungepruefte Nutzung von Formelergebnissen, externen Links oder Makros

## Umsetzungsslices

### P034-E1 Archiv- und Arbeitsmappeninventar

1. ZIP und XLSX unveraendert mit Hash, Groesse, Version, Datum, Herkunft und
   Rechtebeleg registrieren.
2. Blattnamen, sichtbare/ausgeblendete Blaetter, Tabellen, Formeln, Festwerte,
   externe Links, Makros und Formel-Caches inventarisieren.
3. Jede Endvariante als eigenstaendige Eingabequelle fuehren.

Akzeptanz: Jede gelesene Zelle ist auf Datei, Blatt und Adresse
zurueckfuehrbar.

### P034-E2 Datenwoerterbuch und kanonisches Mapping

1. Je Spalte Bedeutung, Datentyp, Einheit, Bezugsflaeche, Zeitraum und
   Missing-Code dokumentieren.
2. Stabile IDs fuer Varianten, Zonen, Bauteile, Materialien und Produkte
   definieren oder vorhandene IDs validieren.
3. Mapping zu `ma_building`, `ma_zones`, `ma_parameters`, `ma_variants` und
   den bestehenden Katalogeigentuemern erstellen.
4. Einheitenumrechnungen und Konflikte explizit protokollieren.

Akzeptanz: Kein Excel-Feld wird ohne dokumentierte Semantik in ein Fachmodell
uebernommen.

### P034-E3 Fachliche und referenzielle Validierung

1. Pflichtfelder, ID-Eindeutigkeit, Fremdschluessel und Duplikate pruefen.
2. Flaechen, Volumen, Laufzeiten, Wirkungsgrade, Vorzeichen und
   Aggregationsebenen plausibilisieren.
3. Doppelzaehlungen zwischen Innenwaenden, thermischer Masse, Zonen und
   Katalogzuordnungen pruefen.
4. Die drei Varianten nur auf identischen Randbedingungen vergleichen.

Akzeptanz: Blockierende Inkonsistenzen verhindern die Uebergabe an
Variantenbildung oder Simulation.

### P034-E4 Importadapter und Tests

1. Kleinen read-only Excel-Adapter mit klarer Parser-/Mapping-/Validierungs-
   Trennung planen.
2. Eine synthetische Minimal-Arbeitsmappe als versionierte Test-Fixture
   verwenden; reale Arbeitsmappen bleiben lokal.
3. Importbericht mit Zellprovenienz und Konfliktliste erzeugen.
4. Bestehende Varianten- und Katalogtests regressiv ausfuehren.

Akzeptanz: Der Adapter kann die drei Schemata diagnostizieren, ohne bestehende
Fachmodelle oder Kataloge zu veraendern.

### P034-E5 Vergleich und Bericht

1. Eingaben, berechnete Ergebnisse und Interpretation getrennt darstellen.
2. Einheitliche Wetter-, Profil-, Simulations- und Auswertungsreferenzen
   erzwingen.
3. Abweichende Randbedingungen als Stoergroessen kennzeichnen.
4. Unsicherheiten und spaetere Sensitivitaeten dokumentieren.

Akzeptanz: Ein Variantenvergleich ist reproduzierbar und verwechselt keine
Randbedingung mit einer Variantenwirkung.

## Tests

- Parser- und Mappingtests mit synthetischer XLSX-Fixture
- Pflichtfeld-, Einheiten-, ID-, Fremdschluessel- und Duplikatfehler
- Erkennung externer Links und nicht aktualisierter Formel-Caches
- Regression bestehender `ma_variants`-, Katalog- und Zonenvertraege

## Offene Nachweise und Entscheidungen

- Herkunft und Repo-/Veroeffentlichungsrecht jeder Arbeitsmappe
- fachliche Bedeutung und Bezugsflaeche aller Spalten
- Eigentuemermodul fuer Bauteil-, Material- und Produktkatalog
- verbindliche Randbedingungen fuer den Endvariantenvergleich
- Umgang mit Formeln, externen Links und Makros

## Abhaengigkeiten

P012, P013, P015, P017, P018, P027 und die vorhandenen
Katalog-/Quellenvertraege.
