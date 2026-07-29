# Chat-Handover: StudyDirection als Steuerung des Pre-Process

Datum: 2026-07-29
Status: Prompt-Intake und erste Read-only-Orientierung; kein Umsetzungsplan und keine Produktivänderung erstellt.

## Anlass und Arbeitsauftrag

Ein neuer fachlicher Arbeitsauftrag beschreibt `StudyDirection` als explizite
Steuerung vor der bestehenden Variantenkette. Er unterscheidet mindestens
`dimensioning`, `optimization`, `standards_verification` und `sensitivity`.
Unterhalb einer Untersuchungsrichtung soll ein konkreter `StudyCase` die
Parameterverwendung, Elternreferenz, Erzeugungsstrategie,
Ergebnisanforderungen und spätere Vergleichsgrundlage definieren.

Der Nutzer möchte zunächst weitere Handover-Dokumente liefern. Erst danach
sollen alle Eingaben gemeinsam gegen Bestand, Entscheidungen und Verträge
analysiert und daraus Umsetzungspläne abgeleitet werden.

## Führende Quellen und erster Abgleich

Führend bleiben `PLAN_INDEX.md`, `PLAN_STATUS.md`, die aktiven Pläne P015 bis
P018 sowie die Entscheidungsdateien. Dieses Dokument ist nur ein historischer
Gesprächssnapshot und ersetzt keine dieser Quellen.

- P015 sieht bereits eine `ParameterVariationSpecification` je `StudyCase`
  vor; sie ist die freigegebene Übergabe an `ma_variants`.
- P016 positioniert die Referenzdimensionierung vor der Variantenbildung und
  reserviert spätere variantenspezifische Dimensionierungsanfragen.
- P017 verwendet bereits die Kette `VSP -> VVER -> VCAT -> VSEL -> VGEN`
  und StudyCases; der allgemeine Vertrag ist nur teilweise umgesetzt.
- P018 materialisiert ausschließlich bestätigte, aktuelle Projektvarianten in
  neutrale Draft-Run-Pakete.
- UD-105 legt für SmallOffice-V1 die 5Z-Endvariante 02, den Referenzfall
  `21/24 Grad C` mit Leistungsfaktor `1,0`, den eingeschränkten
  Optimierungsraum und vorbereitete Sensitivitätsfälle fest.
- UD-106 bestätigt die Reihenfolge: Projekt, Wetter, Gebäude, Zonen, Technik,
  Parameter-Referenzstand, Referenzdimensionierung,
  Parameter-Variationsspezifikation, Varianten, Simulation-Setup.

## Vorläufige Einordnung

Die neue Idee ist voraussichtlich keine zweite Variantenpipeline. Sie präzisiert
und vervollständigt bestehende Konzepte aus P015 und P017. Die größte offene
Architekturfrage ist, ob `dimensioning` nur ein sichtbarer fachlicher Rahmen
oder zusätzlich ein regulärer `StudyDirection`-Typ sein soll. Die fachliche
Referenzdimensionierung bleibt in jedem Fall dem freien Variantenraum
vorgelagert.

Norminhalte und konkrete Normwerte sind nicht Teil dieses Arbeitsstands.
Mögliche Norm-Nachweisprofile dürfen zunächst nur neutral, versioniert und
rekonstruierbar geplant werden.

## Gesammelter Fragenkatalog für die Gesamtanalyse

### Führung, Lebenszyklus und UI

1. Wo liegt die kanonische Persistenz von StudyDirections und StudyCases?
2. Sind StudyDirections projektweite Katalogeinträge oder projektbezogene
   Instanzen?
3. Kann ein StudyCase mehrere Vorgängerfälle referenzieren oder genau einen?
4. Welche Statusfolge gilt für Entwurf, fachliche Prüfung, Freigabe,
   Ausführung, Archivierung und Veraltung?
5. Wird der aktive StudyCase im Projekt, im Workflow oder nur in der
   UI-Sitzung gespeichert?
6. Darf ein StudyCase nach der Erzeugung bestätigter Varianten noch bearbeitet
   werden, oder entsteht stets eine Revision?
7. Wie werden StudyCase-Wechsel in der UI sichtbar, ohne offene
   Modul-Entwürfe zu verlieren?

### Dimensionierung und Referenzen

8. Ist `dimensioning` ein sichtbarer StudyDirection-Typ mit
   `baseline_only`, oder ausschließlich ein vorgelagerter Pflichtschritt?
9. Welche Referenztypen sind im MVP zulässig: Baseline,
   ReferenceDimensioningResult, bestätigte Variante und Vorzugsvariante?
10. Wann darf eine Variation eine neue Dimensionierungsanfrage auslösen?
11. Wie wird eine nicht erforderliche Neudimensionierung fachlich und
   technisch gekennzeichnet?
12. Welche Version des Dimensionierungsergebnisses bindet ein StudyCase?

### Parameter und Variationsvertrag

13. Reicht die bestehende ParameterVariationSpecification für feste,
   variable, gekoppelte und OFAT-Parameter aus?
14. Wie werden absolute Werte, Faktoren und relative Abweichungen eindeutig
   typisiert und mit Einheiten versehen?
15. Welche Regel gewinnt bei Projekt-, StudyDirection- und StudyCase-Scope?
16. Wie werden feste Werte mit einer nachweisbaren Quelle versehen?
17. Wo werden Kopplungsregeln modelliert und geprüft?
18. Wie wird explizit festgelegt, welche Parameter unverändert bleiben?
19. Welche Parameter erfordern vor der Variantenbildung eine fachliche
   Freigabe?

### Variantenbildung, Fingerprints und Aktualität

20. Welche StudyCase- und StudyDirection-Referenzen gehören konkret in VSP,
   VVER, VCAT, VSEL, VGEN und die vollständige Variante?
21. Welche Erzeugungsstrategien sind verbindlich im MVP:
   `baseline_only`, `combinatorial`, `deterministic_profile` und `ofat`?
22. Wie wird sichergestellt, dass OFAT immer nur eine Einflussgröße gegenüber
   dem Elternfall ändert?
23. Welche Selection-Modi sind pro Strategie erlaubt oder verboten?
24. Welche Komponenten gehen in jeden Quellenfingerprint ein?
25. Wann werden Kandidaten, Kataloge, Selections, Varianten und Draft-Run-
   Pakete als veraltet markiert?
26. Werden alte Artefakte nur als veraltet erhalten oder in einen expliziten
   historischen Zustand überführt?
27. Wie bleiben bestehende IDs, Variantenlimits und reproduzierbare Seeds
   unverändert kompatibel?

### Simulation-Setup und Post-Process

28. Gibt es bereits einen gleichwertigen Vertrag zu einem
   OutputRequirementProfile?
29. Welche Ergebnisgrößen, zeitlichen Auflösungen und Aggregationen sind je
   StudyDirection bereits MVP-relevant?
30. Welche Informationen muss das RunManifest zusätzlich tragen, ohne ein
   zweites Handover-Paket einzuführen?
31. Welche Bewertungslogik bleibt bewusst im Post-Process und darf nicht in
   den Pre-Process wandern?
32. Wie werden Norm-Nachweisfälle ohne zusätzliche Simulation gegen Fälle mit
   deterministischem Randbedingungsprofil abgegrenzt?

### Migration, Sicherheit und Nachvollziehbarkeit

33. Welche SmallOffice-V1-Objekte müssen unverändert lesbar bleiben?
34. Welche Teile dürfen nur additiv migriert werden, um P017/P018 nicht zu
   brechen?
35. Welche Tests belegen Rückwärtskompatibilität, Reproduzierbarkeit,
   Strategiegrenzen und Veraltungslogik?
36. Welche Annahmen müssen in der Masterarbeit sichtbar dokumentiert werden?
37. Welche Profilinhalte bleiben bis zum Rechte- und Quellenentscheid rein
   strukturell beziehungsweise neutral?

## Nächster Schritt

Das angekündigte weitere Handover entgegennehmen. Anschließend den
Prompt-Intake abschließen, den aktuellen Code und die zugeordneten Verträge
gezielt analysieren und erst danach einen abgestimmten Umsetzungsplan
vorlegen. Produktive Codeänderungen sind nicht Teil dieses Handover.

## Lokaler Git-Kontext beim Snapshot

- Letzter Commit: `ff1d902` vom 2026-07-28 (`Release 0.35.1 - Externe
  Projektablage und Testbereinigung`).
- Der Arbeitsbaum enthielt bereits umfangreiche fremde, nicht committete
  Änderungen sowie mehrere unversionierte Chat-Handover. Sie wurden weder
  verändert noch bewertet.
