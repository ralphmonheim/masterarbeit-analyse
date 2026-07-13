# Projektweites Compliance-System

Stand: 2026-07-13
Status: technische und vertragliche Vorpruefung, keine Rechtsberatung

## Zweck

Diese Ablage beschreibt die verbindlichen Schutzgrenzen fuer geschuetzte,
lizenzierte, vertrauliche oder personenbezogene Inhalte. Sie ist vor jeder
relevanten Dateioperation oder Implementierung anzuwenden.

```yaml
default_policy: stop_and_warn
```

Unklare Herkunft, unbekannte Lizenz oder ein nicht geklaertes
Verarbeitungsrecht fuehren nicht zu einer stillschweigenden Freigabe.

## Bereiche

- `shared/`: gemeinsamer Preflight, Risikostufen, Datenbereinigung,
  Repository- und Cloud-Grenzen sowie OpenAI-Verarbeitungsprofil.
- `ida_ice/`: IDA ICE, EQUA-EULA, Bibliotheken, `.idm`, NMF und
  Automatisierungsgrenzen.
- `din_nautos/`: DIN Media, Nautos, Normeninhalte, KI-Lizenz und
  wissenschaftliches Text and Data Mining.
- `dwd/`: frei zugaengliche DWD-OpenData-Geodaten sowie registrierte oder
  bestellte DWD-/TRY-Leistungen.

Volltexte, Norm-PDFs, EQUA-Bibliotheken, Lizenzkennungen, Zugangsdaten und
reale Projekt- oder Wetterdateien werden hier nicht versioniert.

## Verbindlicher Ablauf

1. Gemeinsamen Preflight ausfuellen.
2. Betroffenen Fachbereich bestimmen.
3. Individuellen Vertrag und produktspezifische Bedingungen vor allgemeinen
   Quellen pruefen.
4. `compliance_decision` mit erlaubtem und ausgeschlossenem Umfang
   dokumentieren.
5. Bei `green` nur den dokumentierten Umfang ausfuehren.
6. Bei `yellow` warnen und die erforderliche Einzelfallfreigabe dokumentieren.
7. Bei `red` stoppen.
8. `unknown` als fehlenden-Nachweis-Status gesperrt halten und nicht als
   bestaetigtes Verbot oder Freigabe behandeln.

Die technische Durchsetzung liegt in `src/ma_core/compliance/`. Der
`ComplianceService` bewertet eine `OperationRequest` nach einem reinen
Metadaten-Preflight. `green` ist unmittelbar zulaessig, `yellow` bleibt bis
zur dokumentierten Bestaetigung und allen geforderten Rechtebelegen gesperrt,
`red` stoppt und `unknown` bleibt bis zur Klaerung gesperrt. Sichere Wrapper
verhindern Datei-, Parser-,
Upload-, Index- und Simulationsoperationen ohne freigegebene
`ComplianceDecision`. Das append-only Audit unter `logs/compliance/` speichert
nur Metadaten, Hashes und Entscheidungen, niemals geschuetzten Volltext.

Vor Implementierungen mit `.idm`, NMF, EQUA-Libraries, EQUA-API,
IDA-Simulationsstart, DIN-/Nautos-Inhalten, Norm-OCR, Embeddings, RAG oder
Vektordatenbanken ist eine ausdrueckliche `compliance_decision` erforderlich.

## Codex-Durchsetzung

Der projektlokale `compliance_auditor` wendet diese Regeln als read-only
Council-Mitglied an. Er wird bei erkennbaren Compliance-Risiken automatisch
hinzugezogen und ist ein fester Preflight fuer `plan aufnehmen` und
`projektinput aufnehmen` sowie fuer Routinen, die neue Plaene oder
Projektinputs einordnen.

Ein belegter Compliance-Blocker stoppt den betroffenen Vorgang. Bei Plaenen
werden Dokument- und Umsetzungsrisiko getrennt: Unbekannte Plandokumente
werden zuerst nur anhand bereinigter Metadaten geprueft und erst nach belegter
Inhalts- und KI-Verarbeitung gelesen. Ein reiner Umsetzungsblocker bleibt mit
dem Plan sichtbar. Bei lokalen Inbox-Dateien werden Inhaltszugriff,
Extraktion, Verschieben und Einarbeitung gestoppt; das Original bleibt
unveraendert am aktuellen Eingangspfad. `needs_review/` enthaelt nur
Metadatenhinweise oder ausdruecklich freigegebene Arbeitskopien.
Unabhaengige, unkritische Objekte derselben Routine duerfen weiterbearbeitet
werden.

Der Agent erteilt keine Rechts-, Vertrags- oder Fachfreigabe. Eine blosse
Risikoakzeptanz hebt keinen fehlenden Rechte- oder Genehmigungsnachweis auf.
Der Hauptagent prueft die Empfehlung und dokumentiert die anzuwendende
`compliance_decision` mit Belegreferenz im passenden Fachregister oder im
Metadaten-Audit unter `logs/compliance/decisions.jsonl`. Materielle oder gelbe
Entscheidungen benoetigen eine dokumentierte menschliche Bestaetigung und alle
geforderten Rechtebelege.

Vor jeder Veroeffentlichung oder Weitergabe wird geprueft, ob eine gueltige
Entscheidung den konkreten Stand, externe oder geschuetzte Inhalte,
personenbezogene oder vertrauliche Daten sowie neue Abhaengigkeiten abdeckt.
Fehlende, veraltete oder nicht passende Entscheidungen loesen einen neuen
Preflight aus.

## Aktuelle technische Anbindung

| Bereich | Aktueller Projektzustand | Durchsetzung |
|---|---|---|
| DWD TRY 2011 aus IDA-Paket | Konverter vorhanden | vor `.idm` und jeder `.PRN` gegatet |
| IDA-Simulationsstart | nicht implementiert, manuell | Service-Regel `red` |
| EQUA-Bibliotheksimport | nicht implementiert | Service-Regel `red` |
| DIN-/Nautos-OCR, RAG, Extraktion | nicht implementiert | Service-Regel `red` |
| Externe KI-/Cloud-Uebergabe geschuetzter Inhalte | nicht implementiert | Wrapper und Policy blockieren ohne Rechtebeleg |
| Allgemeiner TRY-Import | neutrale Formatgrenze | Datensatzfreigabe bleibt zusaetzlich in `ma_weather`/`ma_validation` |

Damit sind alle derzeit vorhandenen spezialisierten geschuetzten Operationen
entweder technisch gegatet oder gar nicht implementiert. Neue Adapter duerfen
nicht direkt auf die darunterliegenden neutralen Parser zugreifen, sondern
muessen zuerst eine `ComplianceDecision` an ihrer oeffentlichen Modulgrenze
erzwingen.

## Vorlaeufige Hauptgrenzen

- IDA ICE: neutrale Daten vorbereiten, manuell uebergeben und Simulation
  manuell starten; exportierte Ergebnisse danach automatisiert auswerten.
- DIN/Nautos: Normen manuell lesen und eigene fachliche Ableitungen bilden;
  keine maschinelle oder KI-gestuetzte Normverarbeitung ohne nachgewiesene
  passende Rechte.
- DWD: frei zugaengliche OpenData-Geodaten sind mit Quellenvermerk
  weiterverwendbar. Registrierungspflichtige oder bestellte TRY-Leistungen
  richten sich dagegen nach Angebot und AGB und sind nicht automatisch offen.
- OpenAI: Produkt- und Aufbewahrungseinstellungen aendern keine Rechte an
  hochgeladenen Drittinhalten.

## Quellenstand

Die offiziellen Quellen wurden am 2026-07-13 abgeglichen. Wesentliche
Aussagen stehen in den jeweiligen Quellen- und Vertragsregistern. Eigene
Ableitungen werden als solche gekennzeichnet.
