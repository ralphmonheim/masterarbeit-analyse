# Chat-Handover: Technisch final validierter PostProcess-Tabellenvertrag

Datum: 2026-08-12

Status: P029-S12 und seine aktuelle Integration sind technisch umgesetzt,
Council-geprueft und mit 826 Projekttests validiert. Normnachweise selbst sind
ausdruecklich nicht fachlich validiert. Release 0.39.0 liegt auf `main`; dieser
Handover fuehrt keinen Commit, Tag oder Push aus.

## Kontext und Begriffe

Dieser Snapshot ersetzt den
[Snapshot vom 11.08.](260811_chat-handover_postprocess-tabellenvertrag-stage3-readiness.md)
nicht, sondern dokumentiert den spaeteren, final technisch validierten Stand.

`ma_analyse` ist der PostProcess-Owner fuer die technische Auswertung bereits
aufbereiteter Simulationsergebnisse. Stage 2 bezeichnet die vorhandenen
Analyse- und Vergleichsfunktionen; Stage 3 bereitet spaetere fachliche
Normnachweise vor. Die vier Bezeichnungen Dimensionierung, Optimierung,
Nachweis und Sensitivitaet sind in Streamlit derzeit eigene Demo-Tabs und kein
verbindlicher Benutzerworkflow.

`AnalysisTableBundle` ist der gemeinsame UI-, Service- und Excel-Vertrag fuer
Kennwerte, Dateninventar, Berechnungsgrenzen und Nachweisbereitschaft.
`metrics` ist das abwaertskompatible Excel-Blatt ohne neue fachliche Aussagen;
`metrics_v2` ist der neue nachvollziehbare Tabellenvertrag. `W` und `W/m2`
werden nur bei angegebener Quelleneinheit und, falls eine Umrechnung notwendig
ist, positiver Netto-Raumflaeche abgeleitet. Einheitenoffene
Aggregationskennwerte sind bereits berechnete Extrema oder Mittelwerte aus
Quellreihen und keine unverarbeiteten Einzelwerte.

Die prepared-`time`-Achse ist die bei der Datenvorbereitung erzeugte
Stundenachse. Eine Building-Version ist der im aktiven Projekt ausgewaehlte
Stand des Gebaeudemodells. Das Council bezeichnet die getrennten Qualitaets-,
Methodik- und Compliance-Reviews. Ein Gate ist ein noch zu erbringender
Rechte-, Methoden- oder Testnachweis. `NOT_EVALUABLE` bedeutet hier: Mit den
aktuell freigegebenen Daten und implementierten Regeln kann noch kein
fachlicher Normnachweis erstellt werden.

## Fuehrende Referenzen

- [Planstatus](../../plans/PLAN_STATUS.md) und
  [Planindex](../../plans/PLAN_INDEX.md) fuer den aktuellen Gesamtstand.
- [P019 - Analyse Stufe 2 Optimierung](../../plans/inbox/260622_Plan_P019_Stage2_Optimierung.md),
  [P020 - Analyse Stufe 3 Standards Verification](../../plans/inbox/260622_Plan_P020_Stage3_Standards_Verification.md)
  und [P029 - ma_analyse Service- und Runner-Bereinigung](../../plans/inbox/260627_Plan_P029_ma_analyse_Service_Runner_Bereinigung.md)
  fuer den PostProcess-Umfang.
- [UD-121 - Leistungsdarstellung und vorbereitete Nachweisvalidierung](../../decisions/USER_DECISIONS_MASTERTHESIS_CODE.md)
  fuer die getroffene Nutzerentscheidung.
- [OP-008, OP-017 und OP-018](../../decisions/USER_DECISIONS_OPEN_POINTS.md)
  fuer die verbleibenden Nutzerentscheidungen.
- [Changelog](../../../../CHANGELOG.md) fuer Release 0.39.0.

## Erledigter Stand

- Streamlit zeigt den Auswahl- und Laufbereich sowie die vier Demo-Tabs
  Dimensionierung, Optimierung, Nachweis und Sensitivitaet. `all` und
  `analyze_data` verwenden denselben sichtbaren Einheiten- und
  Flaechenvertrag.
- Ohne bestaetigte Quelleneinheit bleiben `W` und `W/m2` leer;
  einheitenoffene Aggregationskennwerte bleiben sichtbar. Die manuelle
  Einheitenwahl ist an Projekt, Datenbankpfad und Variantenauswahl gebunden
  und wird bei Kontextwechsel zurueckgesetzt.
- Flaechenzuordnungen sind an Projekt und Building-Version gebunden;
  mehrdeutige Raumnamen werden nicht automatisch zugeordnet.
- Kuehlung trennt algebraisches Minimum, algebraisches Maximum und maximalen
  Betrag.
- Excel schreibt `metrics` als Legacy-Adapter, `metrics_v2` als neuen Vertrag
  sowie Dateninventar, Berechnungsgrenzen und Nachweisbereitschaft.
- Auswertungsstunden werden nur aus einer lueckenlosen prepared-`time`-Achse
  bestimmt. Eine Zeilenanzahl wird nicht als Nutzungszeit ausgegeben.
- Stage 3 trennt Metadatenbasis, Rechtestatus und gesperrten Inhaltszugriff.
  DIN/TS 18599-10 bleibt ein vorbereitetes Schema ohne Profilwerte;
  DIN 4108-2 bleibt ein Kandidat fuer ein spaeteres Ergebnisfeld. Beide sind
  `NOT_EVALUABLE`; keine Normformel, kein Grenzwert und kein PASS-/FAIL-Urteil
  wurde aktiviert.

## Nachweise und Grenzen

- Die vollstaendige Projekttestsuite bestand mit 826 Tests.
- Ruff und `git diff --check` bestanden.
- Der finale Qualitaetsreview meldete keine Blocker, wichtigen oder optionalen
  Befunde; sein eigener Tabellenfokus bestand mit 29 Tests.
- Der Methodikreview bestaetigte die Korrekturen zu Quelleneinheit und
  Kuehlmaximum und meldete keinen verbleibenden Blocker.
- Der Compliance-Review war im lokal geprueften Umfang ohne Befund. Es wurden
  keine Normvolltexte verarbeitet. Norminhaltsanalyse, externe Verarbeitung
  und Veroeffentlichung bleiben separat gesperrt beziehungsweise
  freigabepflichtig.
- Die schreibfreie Navigator-Pruefung mit `--validate-only` war erfolgreich.

Offene Aufgaben und Entscheidungen werden ausschliesslich in P019, P020,
P029 sowie OP-008, OP-017 und OP-018 gefuehrt; dieser Snapshot enthaelt keine
eigene Aufgabenliste.

## Git- und Archivstatus

Ausgangslage vor dem Anlegen dieses Handovers: Branch `main`, HEAD `1169fc0`
(`Release 0.39.0 - PostProcess, Gebaeude und Navigation`), versionierter
Arbeitsbaum sauber. Beim Anlegen werden nur diese Handover-Datei und ihr
Indexeintrag geaendert. Der Snapshot vom 11.08. bleibt unveraendert. Commit,
Tag und Push erfolgen nicht.
