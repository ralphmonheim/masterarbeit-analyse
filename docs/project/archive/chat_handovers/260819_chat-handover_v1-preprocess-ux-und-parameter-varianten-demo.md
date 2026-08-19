# Chat-Handover: V1-PreProcess-UX und Parameter-/Varianten-Demolauf

Datum: 2026-08-19
Status: historischer Arbeitsstand; keine neue Produktumsetzung in diesem Chat

## Anlass und eingeordneter Stand

Nutzer-Rueckmeldungen zur direkten Bearbeitungsansicht sowie ein neuer, noch
unvollstaendiger Themenstart zum V1-Parameter-/Varianten-Demolauf wurden
dokumentiert. Es wurde keine Produktfunktion umgesetzt. Der Demolauf bleibt
im Prompt-Intake: Nutzer und Codex klaeren den Arbeitsauftrag; vor `Prompt
abschliessen` wird weder ein Plan noch eine Implementierung erzeugt.

## In fuehrende Plaene uebertragene Folgeoptionen

- **P012 – ma_building Gebaeudeinput**
  (`docs/project/plans/inbox/260622_Plan_P012_ma_building_Gebaeudeinput.md`):
  Die Auswahl des aktiven Gebaeudedokuments soll aus dem Importbereich in
  einen eigenen vierten sichtbaren Fachreiter verschoben werden. Import,
  Diagnose und Aktivierung eines Projektstands bleiben getrennt.
- **P013 – ma_zones Zonen und Nutzungen**
  (`docs/project/plans/inbox/260622_Plan_P013_ma_zones_Zonen_Nutzungen.md`):
  Die Seite `ma_zones` soll erkannte Raeume in einer bearbeitbaren
  Raum-zu-Zone-Tabelle zeigen. Erst nach dieser Zuordnung folgt die
  Profilzuweisung. Fuer den UI-Referenzfall werden eine nicht normative
  MA-Buero-Vorlage und fuer die Lobby ausschliesslich die Metadaten
  `DIN/TS 18599-10, Profil A.5 Schalterhalle` gezeigt; geschuetzte Normwerte
  bleiben ausgeschlossen.
- **P015 – ma_parameters Zentrale Parameter**
  (`docs/project/plans/inbox/260622_Plan_P015_ma_parameters_Zentrale_Parameter.md`):
  P015-S5A ist der bestehende Definitionskern mit `ParameterGroup`,
  `ParameterDefinition` und `ParameterInstance`; die vorhandene
  84-Zeilen-Matrix ist nur ein Inventar des bisherigen
  SmallOffice-/LoD-1-Umfangs. Die neue Folgeoption verlangt einen
  vollstaendigen SmallOffice-LoD-2-Parameterkatalog. LoD beschreibt den
  verfuegbaren Detaillierungsgrad; nicht verfuegbare Werte bleiben gesperrt
  sichtbar, bewusst erfasste Annahmen werden als `provisional_assumption`
  markiert. Baseline-Werte und Variationsregeln liegen in getrennten,
  fingerprintbaren Konfigurationen.
- **P017 – ma_variants und Naming-Anbindung**
  (`docs/project/plans/inbox/260622_Plan_P017_ma_variants_Naming_Anbindung.md`):
  Die UI soll eine Generatormethode, einen Zufalls-Seed und eine Zielanzahl
  aufnehmen. Der gewuenschte technische Demolauf erzeugt 50 eindeutige
  Varianten, prueft sie, bestaetigt eine Demoauswahl und gibt IDs, Werte und
  Fingerprint aus. Dieser Demolauf ist getrennt vom wissenschaftlichen
  V1-Studienraum mit 30 Optimierungsfaellen und separaten
  Wetter-/Belegungs-OFAT-Faellen. OFAT bedeutet, dass jeweils nur ein
  Einflussfaktor variiert wird. Der Demolauf loest weder IDA noch eine
  automatische fachliche Variantenbewertung aus.
- **P027 – Querschnitt UI, Workflow, Validation und Feedback**
  (`docs/project/plans/inbox/260622_Plan_P027_Querschnitt_UI_Workflow_Validation_Feedback.md`):
  Fachseiten sollen wieder explizit zu der Bearbeitungsuebersicht und zur
  Gesamtworkflowansicht navigieren. Nach der Projektauswahl im Gesamtworkflow
  soll die Arbeitsseite des Moduls `ma_project` (Projektinitialisierung)
  oeffnen. `Weiter` prueft den Mindeststand, speichert bei Erfolg den
  Projektentwurf und markiert abhaengige Staende als `update_required`
  (aktualisierungsbeduerftig); dies ersetzt keine Fachfreigabe. Zudem sind der
  Analyse-Output-Session-State-Fehler und die faelschliche Anzeige von
  Wirtschaftlichkeitsinhalten in `ma_assessment` (Gesamtbewertung) zu
  korrigieren.

Diese Eintraege sind ausdruecklich nicht zur Umsetzung freigegeben. Sie
erweitern insbesondere nicht automatisch den unabhaengigen V1-5Z-Plan.

## Bestehender Ausfuehrungsplan

Der unabhaengige Plan
`docs/project/plans/independent/260814_V1_5Z_Gebaeudemapping_Workflow_UI_PostProcess_Test.md`
bleibt fuer seine am 2026-08-14 freigegebenen Pakete massgeblich. Die hier
erfassten Folgeoptionen benoetigen vor einer Umsetzung einen neuen,
abgegrenzten Plan und eine neue menschliche `Freigabe zur Umsetzung`.

## Weiterer Themenstand

Der noch nicht abgeschlossene Prompt-Intake und seine offenen Daten- und
Variationsfestlegungen stehen im Abschnitt `Nicht freigegebene
V1-Parameter- und Varianten-Demofolgeoption 2026-08-19` von P015. P015
fuehrt diese Punkte, weil Baseline, Variationsraum, Werteherkunft und
Persistenz dort fachlich verantwortet werden. Der korrespondierende Abschnitt
`Nicht freigegebene V1-Demogenerierung 2026-08-19` von P017 begrenzt nur die
nachgelagerte Erzeugung, Pruefung, Auswahl und Ausgabe der Varianten. Der
Snapshot fuehrt keine eigene offene Aufgabenliste. Nach `Prompt abschliessen`
kann der Nutzer ausdruecklich `umsetzungsplan erstellen` anfordern. Die
UI-Korrekturpunkte werden weder parallel noch automatisch geplant; sie
benoetigen einen spaeteren, eigenen Nutzerauftrag.

## Nachweise und Arbeitsbaum

Der Navigator-Validator konnte den externen Navigationsindex nicht
vollstaendig lesen, weil `local_repository_catalog.md` im Schwesterordner
nicht zugreifbar war. Der Handover beruht daher auf den frisch gelesenen
kanonischen Plaenen.

Beim Handover war der Arbeitsbaum bereits veraendert: `CHANGELOG.md`,
`docs/project/architecture/workflow/README.md`, die geloeschte
`docs/ma_core/README.md`, zwei neue HTML-Dateien unter
`docs/project/architecture/workflow/` und ein neuer Unterordner
`docs/ma_data_export/ma_core/`. Herkunft und beabsichtigter Umgang sind nicht
geklaert. Diese Dateien gehoeren nicht zu diesem Handover; sie wurden weder
gelesen, bewertet, wiederhergestellt noch geaendert. Der naechste Bearbeiter
prueft vor jeder Ueberschneidung gezielt `git status` und den Dateidiff.

## Naechster Einstieg

Der naechste Chat liest zuerst den genannten P015-Abschnitt fuer die offenen
Baseline-, Variations-, Kandidaten- und Seed-Festlegungen und danach den
P017-Abschnitt fuer die Generierungsgrenze. Er setzt ausschliesslich diesen
Prompt-Intake fort. Erst nach dessen Abschluss entscheidet der Nutzer, ob ein
unabhaengiger Plan fuer den Demolauf erstellt wird. Die uebertragene
UI-Restarbeit bleibt bis zu einem separaten Nutzerauftrag unveraendert.
