# Master-Prompt – Quelleninventar und Lernpakete für die Masterarbeit

**Status:** freigegebene Arbeitsfassung

## Rolle und Kontext

Strukturiere Literatur- und Internetquellen für die Masterarbeit
„Analyse der Differenz zwischen TGA-Dimensionierung und simulationsgestützter
Optimierung – Fachliche Simulationen und Prozessinnovation am Beispiel eines
Referenzgebäudes“.

## Ergebnis

Erstelle:

1. eine interne Excel-Quellenmatrix als zentrales Projektregister,
2. eine getrennte, veröffentlichungsfähige Excel-Quellenmatrix,
3. eine interne Markdown-Analyse je Quelle,
4. eine Themen- und Quellenlandkarte sowie
5. eine priorisierte Grundlage für spätere, vertiefte Lernpakete.

## Reihenfolge

1. Recherchiere im Internet aktuelle Themenrahmen, Schlüsselquellen und Lücken
   zu TGA-Dimensionierung, dynamischer Simulation, Heiz-/Kühllast,
   Optimierung, Sensitivität, BIM/IFC, Prozessautomatisierung,
   Softwareentwicklung und agentischer KI.
2. Inventarisiere anschließend navigatorgestützt lokale Quellen, Fundstellen
   und physische Ablagen.
3. Gleiche Internet- und Lokalbestand über Source-ID, DOI, Titel, Autor, Jahr
   und Version ab.
4. Führe zuerst Probeläufe für Buch/Buchkapitel, Whitepaper/Forschungsbericht
   und Webquelle durch. Ergänze weitere vorhandene Quellentypen, wenn sie ein
   abweichendes Datenmuster benötigen.
5. Wende das bestätigte Schema erst danach auf den Gesamtbestand an.

## Quellenstruktur

Jede Quelle erhält eine stabile Source-ID und bleibt unverändert am
Originalfundort. Erstelle pro Quelle eine interne Markdown-Analyse mit:

- bibliografischer Einordnung und Kurzfassung,
- Kernaussagen, Methodik, Ergebnissen und Grenzen,
- Themenzuordnung, möglicher Thesis-Verwendung und Software-/Workflow-Bezug,
- Zitationsfundstellen sowie offenen Prüfhinweisen.

Die interne Excel-Quellenmatrix ist das zentrale Register. Sie verlinkt pro
Quelle auf Originaldatei oder Webquelle sowie die zugehörige Markdown-Analyse
und enthält mindestens bibliografische Angaben, DOI/ISBN/URL, Quellentyp,
Themen, Relevanz, Evidenzqualität, Fundort, Ablagestatus, Zugangsstatus,
Lizenz-/Veröffentlichungsstatus, Aktualitätsstatus,
Dubletten-/Versionsbezug, Prüfstatus und nächste Aktion.

## Interne und öffentliche Trennung

Die interne Fassung enthält alle rechtmäßig verfügbaren Quellen, interne
Fundorte, zulässige semantische Analysen, Volltextverweise und Arbeitsnotizen.
Sie wird nicht veröffentlicht.

Die separate öffentliche Excel-Datei enthält ausschließlich zulässige und
überprüfte bibliografische Angaben, Themenzuordnung, DOI/URL, kurze zulässige
Beschreibung sowie Evidenz- und Prüfstatus. Sie enthält keine internen Pfade,
Lizenznotizen, Originaldateien, Volltexte, umfangreiche Auszüge oder
ungeprüften KI-Aussagen.

## Qualität und Rechte

Erfinde keine Metadaten, Seitenzahlen, DOI oder Quellenbehauptungen. Trenne
Quelleninhalt, KI-Analyse und Projektübertragung strikt. Eine Aussage für den
Masterarbeitstext wird erst nach manuellem Nachlesen der Originalfundstelle als
`citation_ready` markiert. Setze bei Rechte-, Zugriffs-, Qualitäts- oder
Aktualitätsunsicherheit `requires_manual_review`.

Originalquellen werden weder verändert noch weiterveröffentlicht. Für
lizenzierte Quellen dokumentiere den zulässigen Analyseumfang und führe nicht
zulässige KI-Verarbeitung als manuelle Prüfung.

## Pflichtregister der internen Excel-Datei

- Quellenmatrix
- Themenlandkarte
- Quellentypen und Evidenzqualität
- Fundorte und Ablagestatus
- Prüfwarteschlange
- Dubletten und Versionen
- Fehlende Quellen
- Recherche- und Abgleichprotokoll

## Ablage

- Prompts: `docs/prompts/`
- Excel-Register: lokaler Bereich `config/ma_database/literature/`
- Quellenanalysen: lokaler Bereich `config/ma_database/literature/analyses/`
- Originale: unverändert an ihren bisherigen Fundorten

Die Excel-Quellenmatrix referenziert immer die Originalquelle und die
zugehörige Markdown-Analyse über Source-ID und stabilen lokalen Pfad.

## Nicht-Ziele

Der Aufbau eines später möglichen Parallel-Recherche-Skills und eine
maschinenlesbare JSON-Wissensdatenbank gehören nicht zum ersten Durchlauf.
