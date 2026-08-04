# ma_zones

- **Zweck:** Zonen, Nutzungen, Profile, Konditionierung, interne Lasten,
  Zeitprofile und zonenbezogene Uebergabesysteme verwalten.
- **Eingaben:** freigegebene Raumreferenzen aus `ma_building`, zentrale
  technische Systemreferenzen aus `ma_technical` und Nutzungsanforderungen.
- **Ausgaben:** validierte Zonendaten fuer `ma_parameters` sowie
  zonenbezogene Betriebs-, Konditionierungs- und Uebergabezuordnungen.
- **Abgrenzung:** keine Gebaeudegeometrie, keine zentralen Erzeugungsanlagen
  und keine automatische Zonenbildung im MVP.
- **Abhaengigkeiten:** `ma_building`, `ma_technical`; Phase 2.
- **Status:** teilweise umgesetzt. P013-S1 stellt eine LoD-1-Demo fuer das
  BusinessIntegration-Testgebaeude bereit:
  `config/ma_zones/examples/business_integration_lod1_zone_spec.yaml`.
- **SmallOffice V1:** Endvariante 02 besitzt fuenf feste thermische Zonen und
  eine vollstaendige Zuordnung aller 29 Raeume. Optimierung und Sensitivitaet
  veraendern in V1 weder den Zonenzuschnitt noch zonenweise Sollwertmuster;
  innerhalb jedes Falls gelten dieselben Sollwerte fuer alle fuenf Zonen.
- **Planstand:** P013-S2 ist fachlich konsolidiert. Der Zielworkflow lautet
  `ma_weather -> ma_building -> ma_technical -> ma_zones -> ma_validation ->
  ma_parameters`.
- **LoD-1-Inhalt:** eine Gesamtgebaeudezone, ein einfaches Buero-Nutzungsprofil,
  Sollwerte, interne Lasten, Betriebszeiten und Mindestluftwechsel.
- **Validierung:** Pflichtfelder, eindeutige IDs, Profilreferenzen,
  Flaeche/Volumen, Sollwerte, Betriebszeiten und Gebaeudebezug werden geprueft.
  Fehler blockieren; Warnungen benoetigen eine bewusste Freigabeentscheidung.
  Die additive zonenseitige Integritaetspruefung validiert technische
  Zonenreferenzen bei unveraenderter Legacy-Diagnostik.
- **Released-Zonencheckpoint:** P013-S3c erzeugt aus einem validierten
  Building-, Zonen-, ThermalBuilding- und P014-Stand einen immutable,
  payloadfreien `ReleasedZoneHandover`. Sein kanonischer Fingerprint bindet
  Zonenstand, Raum-Zonen-Zuordnung, Building-ID/-Revision und das technische
  Modell-/Revisions-/Hash-Triple. Optionale, explizit manuell bestaetigte
  `ZoneTechnicalServiceAssignment`-Eintraege werden gegen den vollstaendigen
  P014-Handover geprueft und nur bei Nutzung zusaetzlich in den Fingerprint
  aufgenommen; der DTO gibt keine Fachnutzlast weiter.
- **Streamlit:** Die Modulansicht trennt Übersicht, tabellarische
  Nutzungsprofilzuweisung als Sitzungsentwurf, Konditionierung sowie Zeit und
  Belegung. Im Bereich `Konditionierung & Übergabe` kann ein Nutzer Zonen
  manuell den Serviceinterfaces des aktiven, buildinggebundenen P014-
  Handovers zuordnen. Pruefung und Speicherung sind getrennte Aktionen;
  geaenderte oder veraltete Handover-Bezuege werden nicht vorausgewaehlt.
  Trinkwarmwasser-Erzeugung, Speicher und Verteilung bleiben in
  `ma_technical`.
- **Freigabebereitschaft:** `Zusammenfassung & Prüfung` verbindet den
  uebernommenen Building-Stand, die versionierte Zonenquelle, den
  gespeicherten P013-Projektentwurf und den aktiven P014-Handover. Die
  vorhandenen Fach-Builder erzeugen daraus nur im Speicher ein
  `ThermalBuildingModel` und einen deterministischen Handover-Kandidaten.
  `RELEASED` bedeutet hier ausschliesslich bestandene Fachvalidierung; die
  Vorschau speichert und aktiviert keine Revision und ist kein P018-Eingang.
- **Projektentwurf:** Die Zuordnungen werden additiv in `ma_zones.yaml`
  gespeichert und an Technikmodell, Revision, Content-, Interface-,
  Freigabenachweis- und Handover-Hash gebunden. Dieser Schritt erzeugt noch
  keinen `ReleasedZoneHandover`, berechnet keine Last und nimmt keine
  Dimensionierung vor. Ein eigener Zoneninhalt-Hash bindet den Entwurf auch
  an die konkrete Zonenspezifikation und Raumzuordnung. Fremde Projekt-IDs
  werden nicht ueberschrieben. Leere Zuordnungen bleiben als bewusst
  gepruefter Entwurf moeglich und behaupten keine Vollversorgung; die
  Pruefung bestaetigt nur Beziehungsintegritaet, keine Eignung oder Deckung.
- **Naechster Schritt:** Die schreibfreie Vorschau im manuellen SmallOffice-
  Durchstich pruefen. Vor einer vollstaendigen Zonenfreigabe und P018-
  Anbindung ist ein append-only P013-Release-Envelope samt Owner,
  Persistenzpfad, ID-/Revisionsschema und Reload-Pruefung zu entscheiden.
  Die separate Workflowansicht folgt erst am Ende der Gesamtmigration.
