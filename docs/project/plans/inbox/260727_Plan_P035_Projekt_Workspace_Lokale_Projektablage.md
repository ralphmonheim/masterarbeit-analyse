# P035 Projekt-Workspace und lokale Projektablage

Stand: 2026-07-28
Status: P035-S1 bis S5 als V1-Produktslices mit externer Projektablage umgesetzt; generisches Sammelspeichern bleibt Folgearbeit
Prioritaet: Hoch
Abhaengigkeiten: P011, P027, P032, UD-104, UD-106, UD-107

## Ziel

P035 fuehrt den lokalen Projekt-Workspace als eigenen technischen Baustein.
Der Plan trennt Dateisystem-, Registry- und Persistenzaufgaben von der
fachlichen Projektidentitaet in `ma_project`.

`ma_project` bleibt Eigentuemer von Projektstammdaten, Standort,
Simulationsprogramm und Naming-Profil. P035 stellt dafuer lokale
Projektordner, Projektdateien, bekannte Projektpfade und sichere
Oeffnen-/Speichern-Ablaufe bereit.

Aktive Projektordner sind Arbeitsdaten und liegen nicht im Repository. Der
V1-Standardpfad ist:

`../260524_Masterarbeit_Arbeitsablage/04_Teil2_Prozessinnovation/Projekt_Workspaces/`

Im Repository verbleiben nur unveraenderliche Seed-Vorlagen unter
`config/ma_project/examples/`.

## Verbindlicher V1-Ablauf

```text
Anwendung starten
    -> Projektwahl anzeigen
    -> bekanntes Projekt waehlen
       oder Projekt importieren
       oder Projekt erstellen
    -> Projektordner validieren
    -> project.yaml laden oder anlegen
    -> Projekt als aktiven Workspace bereitstellen
```

Das zuletzt verwendete Projekt wird nur vorgeschlagen. Es wird nicht
stillschweigend geoeffnet.

## Projekt erstellen

1. Projektname abfragen.
2. Simulationsprogramm verpflichtend waehlen.
3. Land und Stadt verpflichtend sowie Adresse optional erfassen.
4. Ueber einen nativen Windows-Ordnerdialog einen uebergeordneten Zielordner
   waehlen.
5. Darunter einen Unterordner mit dem Projektnamen anlegen.
6. Bei bereits vorhandenem Zielordner abbrechen und einen anderen Namen
   verlangen. Automatische Suffixe wie `-2` sind unzulaessig.
7. Eine stabile, nicht bearbeitbare Projekt-ID erzeugen.
8. Zunaechst nur `project.yaml` und die minimalen Workspace-Metadaten
   speichern.

Gebaeude-, Wetter-, Zonen-, Technik-, Parameter- und Variantenstaende
entstehen erst bei ihrer Auswahl oder Bearbeitung im jeweiligen Fachmodul.

## Projekt auswaehlen und importieren

- Bekannte lokale Projekte werden direkt angeboten.
- Fuer V1 sind mindestens `Masterarbeit-Analyse` und `Demo-Project1` als
  bekannte Projekte vorgesehen.
- `Projekt importieren` oeffnet einen nativen Windows-Ordnerdialog.
- Ein importiertes Projekt wird am vorhandenen Ort geoeffnet und nicht
  kopiert.
- Nur Ordner mit einer gueltigen Projektdatei duerfen aktiviert werden.
- Importierte Projekte werden anschliessend in die lokale Registry
  aufgenommen.

## Lokale Projekt-Registry

Die Registry speichert ausschliesslich:

- Projekt-ID,
- sichtbaren Projektnamen,
- lokalen Projektordner.

Sie dupliziert keine fachlichen Projektinhalte. Nicht mehr vorhandene oder
ungueltige Projektordner bleiben als `nicht verfuegbar` sichtbar und koennen
nach ausdruecklicher Bestaetigung aus der Registry entfernt werden.

## Projektstruktur

Die minimale Zielstruktur lautet:

```text
260524_Masterarbeit_Arbeitsablage/
  04_Teil2_Prozessinnovation/
    Projekt_Workspaces/
      workspace_registry.yaml
      <projektordner>/
        project.yaml
        assets/
          gallery/
        config/
        output/
```

Fachmodule duerfen ihre projektbezogenen Dateien erst anlegen, wenn der
Nutzer im jeweiligen Modul eine Vorlage, einen Katalogeintrag oder einen
Entwurf uebernimmt. Zentrale Vorlagen und Kataloge bleiben unveraendert.

Ein Projekt darf mehrere Gebaeude enthalten. Das SmallOffice ist ein
Gebaeude im Projekt `Masterarbeit-Analyse` und besitzt mit 5Z und 29Z zwei
alternative thermische Modelle.

## Projektgalerie

- Erlaubte Formate: PNG, JPG/JPEG und WEBP.
- Hochgeladene Bilder werden nach `assets/gallery/` kopiert.
- Links erscheint die Dateiliste mit Upload-Aktion.
- Rechts wird genau das aktuell ausgewaehlte Bild gross angezeigt.
- Entfernen ist nur nach ausdruecklicher Bestaetigung zulaessig.

## Sitzungsentwuerfe und Projektwechsel

- Streamlit-Neulaeufe erhalten aktive Seite, Reiter, Unterreiter,
  Auswahlen und nicht gespeicherte Sitzungsentwuerfe.
- Ein Projektwechsel mit offenen Entwuerfen erzeugt eine Warnung.
- `Aenderungen speichern und wechseln` uebernimmt alle gueltigen Entwuerfe
  des aktuellen Moduls.
- Ungueltige Entwuerfe blockieren den Wechsel mit einer konkreten Meldung.
- Entwuerfe werden ohne Uebernahmebutton nicht in Projektdateien geschrieben.

## Technische Grenzen

- V1 arbeitet ausschliesslich lokal unter Windows.
- Ein spaeterer Browser- oder Cloudbetrieb benoetigt einen anderen
  Ordnerauswahl- und Speicheradapter.
- P035 fuehrt keine Cloudspeicherung, Synchronisation oder
  Mehrbenutzerverwaltung ein.
- Zielpfade werden vor jeder Anlage oder Aenderung auf Existenz,
  Schreibbarkeit und erwartete Projektstruktur geprueft.
- Projektordner werden niemals rekursiv geloescht.
- Synthetische `tmp_path`-Testordner sind kurzlebige technische
  Zwischenartefakte. Sie werden nach jedem Test entfernt und weder als
  Projektworkspaces noch als wissenschaftliche Ergebnisdaten archiviert.

## Umsetzungsslices

### P035-S1 Verträge und Pfadvalidierung

- `ProjectWorkspace`-, Registry- und Projektdateivertraege definieren.
- Validierung fuer Projektname, Projekt-ID, Zielpfad und `project.yaml`
  umsetzen.
- Tests mit temporaeren lokalen Verzeichnissen ergaenzen.

### P035-S2 Registry und bekannte Projekte

- Lokale Registry laden, validieren und sicher aktualisieren.
- `Masterarbeit-Analyse` und `Demo-Project1` als bekannte V1-Projekte
  vorbereiten.
- Fehlende Projekte sichtbar und entfernbar machen.

### P035-S3 Windows-Ordnerdialog

- Lokalen nativen Ordnerdialog hinter einer kleinen Adaptergrenze anbinden.
- Abbruch, ungueltigen Zielordner, Namenskollision und fehlende
  Schreibberechtigung behandeln.
- Keine neue externe Python-Abhaengigkeit einfuehren, sofern die lokale
  Standardbibliothek ausreicht.

### P035-S4 Streamlit-Projektstart

- Projektwahl als ersten sichtbaren Einstieg umsetzen.
- Erstellen, Auswaehlen und Importieren an den Workspace-Service anbinden.
- Letztes Projekt nur vorschlagen.
- Nach erfolgreicher Aktivierung die `ma_project`-Bearbeitungsansicht
  oeffnen.

### P035-S5 Galerie und Entwurfswarnung

- Lokale Galerieablage und Vorschau umsetzen.
- Bestaetigtes Entfernen einzelner Bilder ergaenzen.
- Moduluebergreifende Warnung bei offenen Sitzungsentwuerfen vorbereiten.

## Tests und Abnahme

- Projektname und Projekt-ID werden deterministisch validiert.
- Existierende Zielordner werden nicht ueberschrieben.
- Dialogabbruch erzeugt keine Projektdatei.
- Registry-Eintraege duplizieren keine Projekte mit gleicher Projekt-ID.
- Ungueltige und fehlende Projektordner bleiben beherrschbar.
- Projektwechsel verliert keine gueltigen Entwuerfe ohne Warnung.
- Galerie akzeptiert nur die freigegebenen Bildformate.
- Ein lokaler manueller Streamlit-Smoke-Test bildet Erstellen, Schliessen,
  erneutes Auswaehlen und Importieren ab.

## Abgrenzung zu P011

P011 bleibt die fachliche Wahrheit fuer Projektidentitaet,
Untersuchungsrahmen, Standort, Simulationsprogramm und Naming-Profil.
P035 ist ausschliesslich fuer lokale Projektordner, Registry, Projektdatei,
Galerie und den technischen Speicherablauf verantwortlich. P011 referenziert
P035, uebernimmt dessen Dateisystemlogik aber nicht.

## Umsetzungsstand 2026-07-28

- `ma_workspace` besitzt Workspace-, Registry-, Projektdatei-, Galerie- und
  Fachconfig-Persistenz; `ma_project` besitzt weiterhin die fachlichen
  Projektmodelle.
- Projektanlage und -import verwenden einen lokalen, injizierbaren
  Tkinter-Ordnerdialog ohne neue Abhaengigkeit.
- `Masterarbeit-Analyse` und `Demo-Project1` liegen als getrennte bekannte
  Projekte in der separaten Arbeitsablage vor. Das SmallOffice bleibt ein
  Gebaeude mit 5Z und 29Z im ersten Projekt. Die Repository-Kopien wurden in
  unveraenderliche Seed-Vorlagen ueberfuehrt.
- Das fruehere lokale Testarchiv wurde bis auf 19 durch Windows-ACLs
  gesperrte UUID-Verzeichnisse entfernt. Diese Reste sind ignorierte,
  synthetische Zwischenartefakte und muessen einmalig mit lokalen
  Administratorrechten geloescht werden; sie werden nicht versioniert oder
  als Nachweis weiterverwendet.
- Projektname und Projekt-ID werden nicht still geaendert; vorhandene
  Zielordner, doppelte Registry-IDs und abweichende Projektordnernamen
  blockieren.
- Die Galerie speichert nur PNG, JPG/JPEG und WEBP, zeigt links die Liste und
  rechts genau das gewaehlte Bild; Entfernen verlangt Bestaetigung.
- Streamlit-Bereichsauswahlen sind sitzungsgespeichert. Offene
  Fachmodulentwuerfe blockieren einen Projektwechsel mit einer konkreten
  Meldung, bis sie im jeweiligen Modul gespeichert oder zurueckgesetzt
  wurden. Damit gehen in V1 keine Entwuerfe still verloren.
- Ein spaeteres fachmoduluebergreifendes Sammelspeichern benoetigt
  normalisierte Draft-Vertraege je Modul und bleibt bewusst eine
  Folgearbeit; der V1-Guard behauptet keine generische Validierung.

## Uebertragene Folgearbeit 2026-08-11: Galeriepfad und lokale Snapshots

UD-119 legt fuer die lokalen, ignorierten Snapshot-Ordner unter
`data/project_output/` die sichtbare Trennung `gallery/` fuer Projektbilder
und `diagrams/` fuer Auswertungsabbildungen fest. Diese Snapshots sind keine
aktiven P035-Workspaces. Der aktuelle P035-Workspace-Vertrag und seine
Implementierung verwenden bis zu einer gesondert freigegebenen Migration
weiterhin `assets/gallery/`; es gibt weder einen stillen Umzug noch einen
Fallback auf beide Pfade. Eine Vereinheitlichung ist ein eigener P035-Slice
mit Pfadvertrag, Migration vorhandener lokaler Projektbilder,
Kompatibilitaetspruefung und manueller UI-Abnahme.
