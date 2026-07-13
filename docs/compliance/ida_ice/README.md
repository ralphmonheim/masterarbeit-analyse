# IDA ICE Compliance-Vorpruefung

Stand: 2026-07-13
Status: technische und vertragliche Vorpruefung, keine Rechtsberatung

## Executive Summary

Das Projekt darf eigene, bereinigte Eingabedaten und nach einem manuell
gestarteten IDA-ICE-Lauf exportierte Ergebnisse auswerten. Vollstaendige oder
gemischte IDA-ICE-Dateien, mitgelieferte Bibliotheken sowie Cloud-Verarbeitung
bleiben bis zu einer dokumentierten Einzelfallpruefung gesperrt. Insbesondere
verbietet die als primaere Quelle erfasste EQUA-EULA automatisierte Starts und
Ausfuehrungen von Simulationen ohne ausdrueckliche EQUA-Genehmigung.

Die verbindliche Architekturgrenze lautet deshalb:

```text
ma_variants -> neutrale Variantendaten -> ma_simulation_setup
  -> manuelle Uebergabe an IDA ICE -> manueller Simulationsstart
  -> Ergebnisexport -> automatisierte Ergebnisanalyse
```

Die eigene Software ersetzt IDA ICE nicht, startet keine Simulation und
rekonstruiert weder Dateiformat noch Algorithmen oder Bibliotheken.

## Quellen und Aussagegrenzen

- Der gemeinsame Projekt-Preflight unter `../shared/` gilt vor den
  IDA-spezifischen Regeln.
- `sources.json` ist das Quellenregister; Volltexte werden nicht versioniert.
- `terms_register.yaml` trennt verifizierte Vertragsregeln von Ableitungen.
- Die Online-EULA EULA 2023/12 wurde am 2026-07-13 gegen den offiziellen
  Abruf geprueft. Der konkrete Hochschul-Lizenzuntertyp bleibt `unknown`, bis
  der Lizenznachweis ohne Kennungen ausgewertet oder EQUA ihn bestaetigt.
- OpenAI-Quellen beschreiben Datenverarbeitung, ersetzen aber keine Rechte an
  EQUA-, Kunden- oder Drittinhalten. Vor jeder externen Verarbeitung muessen
  diese Rechte gesondert vorliegen.
- Der erneute Primarquellenabgleich hat fruehere lokale Abschnittsverweise
  korrigiert: Automatisierung steht in EULA `3(e)`, die konkurrierende
  Hauptfunktion in `3(i)`.

## Risikobewertung

| Klasse | Beispiele | Projektregel |
|---|---|---|
| Gruen | eigene bereinigte Exporte, Ergebnisse, Diagramme | zulaessig, soweit keine Dritt- oder vertraulichen Daten enthalten sind |
| Gelb | vollstaendige `.idm`, begrenzte Vorlagenanalyse, API/Makro ohne Simulationsstart | Preflight, Warnung und minimaler Umfang erforderlich |
| Rot | Bibliotheksspiegelung, Format-Reverse-Engineering, Generator/Editor, automatischer Simulationsstart | nicht durchfuehren ohne schriftliche EQUA-Freigabe |

Die maschinenlesbaren Listen stehen in `processing_limits.yaml`,
`automation_limits.yaml` und `risk_matrix.yaml`.

## Masterarbeitsworkflow

1. Nur eigene oder klar freigegebene Daten verwenden.
2. Vollstaendige oder unbekannte IDA-Dateien zuerst mit
   `../shared/preflight_schema.yaml` und danach mit `preflight_schema.yaml`
   bewerten; `unknown` fuehrt zur Entscheidung `stop`.
3. Lizenzkennungen, Kunden-, Personen-, Standort- und Bibliotheksdaten vor
   jeder externen Verarbeitung nach `data_sanitization.yaml` entfernen oder
   den Vorgang stoppen.
4. Bei Gelb nur lokal und im kleinsten notwendigen Umfang arbeiten, bis die
   Einzelfallfreigabe dokumentiert ist.
5. IDA ICE manuell bedienen und starten; Ergebnisse danach automatisch
   zu `RUN-ID + VAR-ID` zuordnen und auswerten.

## Offene Punkte und erforderliche Freigaben

- Exakter Typ der Hochschullizenz und ihr Berechtigtenkreis.
- Lokales, projektspezifisches Parsen einer selbst erstellten `.idm`.
- Cloud-Analyse einer bereinigten `.idm`.
- Zulassiger Umfang einer wissenschaftlichen Beschreibung von Objektstrukturen.
- Zulaessigkeit begrenzter Vorlagen- oder Bibliotheksauszuege.
- API-/Makro-Nutzung fuer Import oder Projektdatei-Aenderungen.

Der nicht versendete Entwurf `equa_permission_request.md` buendelt diese
Fragen. Bis zu einer Antwort gelten die restriktiven Grenzen dieser Ablage.

## Dokumentationsstand

Quellenabgleich: 2026-07-13. Die Dokumentation wird bei einer neuen EULA,
einer EQUA-Antwort oder einer vorgesehenen IDA-bezogenen Implementierung
erneut geprueft.
