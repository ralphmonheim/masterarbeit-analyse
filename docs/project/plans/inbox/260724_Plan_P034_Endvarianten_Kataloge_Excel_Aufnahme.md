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

## Umsetzungsstand 2026-07-27: begrenzter SmallOffice-V1-Slice

Aus dem lokalen Archiv
`demo_masterarbeit_endvarianten_optionen_v2.zip` ist ausschliesslich
`endvariante_02_5_zonen_innenwaende_entfernt_v2.xlsx` als V1-Ausgangsstand
minimal normalisiert. Das versionierte Fachmodell fuehrt 29 Raeume, fuenf
Zonen, 516,842 m2 und 1677,64455 m3 sowie den Hash des unveraenderten lokalen
Archivs. Die Lobbyhoehe 8,0 m ist fachlich als zweigeschossig bestaetigt.

Dieser Slice ist kein allgemeiner Excel-Importer und schliesst P034-E1 bis E5
nicht ab. Vollstaendige Zellprovenienz, Formelinventar, alle drei
Endvarianten und die Katalogarbeitsmappen bleiben getrennte Folgearbeit.

## Konsolidierter Katalog- und Zielablagebezug 2026-07-27

UD-106 bestaetigt Excel als Inhaltsquelle fuer Materialien, Produkte,
Bauteile und Elemente. Die drei Katalogarbeitsmappen im lokalen Archiv sind
die vorgesehenen Quellen fuer `ma_building`; Configs speichern nur Vorlagen,
Regeln, Referenzen und Projektanpassungen. Ein vollstaendiges
Techniksystem-Paket soll ebenfalls aus einem spaeter bereitzustellenden
Excel-Katalog stammen.

Fuer eine getrennt freizugebende Projektinput-Aufnahme sind folgende lokale
Zielrollen vorgesehen:

- Endvarianten-XLSX: `data/ma_building/input/endvariants/`;
- Bauteilkatalog: `data/catalogs/components/`;
- Materialkatalog: `data/catalogs/materials/`;
- Produktkatalog: `data/catalogs/products/`.

Die Ablageentscheidung ist keine Freigabe zum Entpacken oder Verschieben.
Originale bleiben unveraendert, und bestehende Projekte werden bei einer
spaeteren Katalogaenderung nur als pruefbeduerftig markiert.

## Ausgefuehrte lokale Ablage 2026-07-27

Mit der Produktslice-Freigabe wurden die Quellen an die oben festgelegten
Rollen verschoben:

- Quellarchiv:
  `data/catalogs/sources/demo_masterarbeit_endvarianten_optionen_v2.zip`
- Bauteilkatalog:
  `data/catalogs/components/demo_masterarbeit_bauteilkatalog.xlsx`
- Materialkatalog:
  `data/catalogs/materials/demo_masterarbeit_materialkatalog.xlsx`
- Produktkatalog:
  `data/catalogs/products/demo_masterarbeit_produktkatalog.xlsx`
- Endvarianten-Arbeitsmappen und Quellenhinweis:
  `data/ma_building/input/endvariants/`

Die lokalen Arbeitsmappen bleiben ignorierte Fachquellen. Der V1-Leser
verwendet nur das Blatt `Uebersicht`, bindet Pfad und SHA-256 in die
Projektkopie und veraendert die zentrale Excel-Datei nicht.

## Umsetzungsstand 2026-07-29: Katalog-V1 und eigene Entwuerfe

Der additive Katalog-V1-Schnitt ergaenzt `ma_building` um eine gemeinsame,
lesende Registry fuer Bauteile, Materialien und Produkte. Sie fuehrt
Datensatz-ID, Quelle, optionalen Quellenlink, Hash und Herkunftsstatus
zusammen und blockiert ID-Kollisionen statt still zu ueberschreiben.

Die Streamlit-Gebaeudeansicht speichert eigene Eingaben ausschliesslich als
projektlokale `user_unverified`-Entwuerfe mit stabiler ID, Zeitstempel und
Herkunftsangabe. Sie aendern keine Excel- oder Herstellerwerte. Eine fehlende
Quellen-URL ist eine Warnung; fehlt jede Herkunft, bleibt der Entwurf ohne
fachliche Freigabe und darf nicht fuer Simulation, Oekonomie oder Oekobilanz
genutzt werden.

Dieser Schnitt ersetzt P034-E1 bis E5 nicht. Die neuen Inbox-Pakete bleiben
bis zu ihrem objektbezogenen Quelleninventar, Feldmapping und der fachlichen
Pruefung unveraendert am Eingang. Wetterdaten sind bewusst nicht Teil dieses
ersten Katalogschnitts.
