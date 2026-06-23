# P028 Projekt-, Parameter- und Naming-Demo in Streamlit

Stand: 2026-06-23
Status: Geplant
Prioritaet: Hoch
Abhaengigkeiten: P010, P011, P015, P017, P027

## Ziel

Die vorhandenen Demo-Parameter, Optionswerte und Naming-Regeln entsprechend
der Zielarchitektur in die zentrale Streamlit-Oberflaeche einbinden.

- `ma_project` verwaltet Simulationsprogramme und neutrale
  Varianten-Benennungsprofile.
- `ma_parameters` verwaltet Parameterdefinitionen, Optionsgruppen und
  ausgewaehlte Werte.
- `ma_variants` erzeugt Varianten aus dem freigegebenen Parameterstand und
  wendet das von `ma_project` referenzierte Benennungsprofil an.
- `ma_core` stellt nur technische Datei-, Vorlagen- und Schutzregeln bereit.

## Streamlit-Ansichten und Datenfluss

- `ma_project` erhaelt eine erste Fachansicht fuer:
  - frei verwaltbare Simulationsprogrammliste;
  - Auswahl des aktiven Programms;
  - neutrales Varianten-Benennungsprofil;
  - Vorschau und Validierung der Benennungsregeln.
- `ma_parameters` zeigt die vorhandenen Demo-Parameter schreibgeschuetzt und
  erlaubt die Auswahl aktiver Optionswerte.
- Mindestens ein aktiver Optionswert je variantenrelevantem Parameter ist
  erforderlich.
- `ma_variants` verwendet den gemeinsamen Sitzungsstand, erzeugt den
  Variantenraum und zeigt Namen sowie Eindeutigkeitspruefung an.
- Modulansichten erhalten gezielte Verweise auf die jeweils verantwortliche
  Konfigurationsseite. Der Ruecksprung zur Ausgangsseite bleibt erhalten.
- Ein direkter Einstieg in `ma_variants` initialisiert fehlende Sitzungsdaten
  aus den vorhandenen Vorlagen.

## Neutrale Benennung

Der erste Slice unterstuetzt neutrale Variantennamen wie:

```text
V001_CL24_VCO2_H100
```

Das Profil enthaelt:

- Variantenpraefix;
- Index ein-/ausschalten;
- Indexbreite;
- Trennzeichen;
- Reihenfolge der Parameterbestandteile;
- Token je Optionswert.

Nicht enthalten sind:

- Projektkennung im Variantennamen; dies bleibt eine Zukunftsidee;
- Produkt-, Material-, Raum- oder Systembezeichnungen;
- programmspezifische Objekt- und Exportcodes.

Produkt- und Materialbezeichnungen bleiben neutrale Katalogdaten.
Programmspezifische Mappings gehoeren spaeter in die jeweiligen
Simulationsadapter.

## Speicherung und Vorlagenschutz

Versionierte `example_*.yaml`-Vorlagen duerfen niemals veraendert werden.
Eigene Arbeitsstaende liegen lokal unter:

```text
data/ma_project/config/simulation_programs/
data/ma_project/config/naming/
data/ma_parameters/config/options/
```

Regeln:

- Aenderungen werden nicht automatisch gespeichert.
- Bei einer Vorlage ist nur `Als neue Datei speichern` zulaessig.
- Bei einer eigenen Datei kann nach ausdruecklicher Bestaetigung
  ueberschrieben oder als neue Datei gespeichert werden.
- Existiert der gewaehlte neue Dateiname bereits, wird kein automatischer
  Ersatzname erzeugt und die Datei nicht ueberschrieben. Der Nutzer muss einen
  anderen neuen Namen auswaehlen.
- Pfade ausserhalb der vorgesehenen lokalen Konfigurationsordner werden
  abgelehnt.
- YAML ist das erste Speicherformat dieses Slices. Fachmodelle und Services
  bleiben formatneutral, damit spaeter weitere Formate ergaenzt oder YAML
  ersetzt werden kann.
- Lokale Konfigurationen werden nicht versioniert.

## Akzeptanzkriterien

- Parameter-, Projekt- und Variantenansicht verwenden denselben
  Streamlit-Sitzungsstand.
- Die vorhandene Demo erzeugt weiterhin acht Varianten und beispielsweise
  `V001_CL24_VCO2_H100`.
- Fehlende Tokens, unbekannte Parameter, leere Optionsgruppen und doppelte
  Variantennamen blockieren Anwendung und Speicherung.
- Vorlagen koennen technisch nicht ueberschrieben werden.
- Namenskollisionen bei neuen Dateien erfordern eine neue Nutzereingabe.
- Die Programmliste speichert mindestens Programmschluessel, Anzeigename,
  Version und optionale Notiz.
- Infokarten bleiben auf den neuen Fachansichten erreichbar.
- Bestehende Parameter-, Options- und Naming-Importer bleiben kompatibel.

## Nicht enthalten

- produktiver `ParameterSnapshot`;
- Projektkennung als Bestandteil des Variantennamens;
- programmspezifische Export- oder Objektcodes;
- Produkt- und Materialbenennung in `ma_project`;
- Festlegung von YAML als dauerhaft einziges Speicherformat.
