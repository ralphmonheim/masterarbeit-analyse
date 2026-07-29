# Chat-Handover – PreProcess V1 und Projekt-Workspace

Datum: 2026-07-28
Status: aktueller Arbeitsstand
Arbeitsbereich: P008, P011 bis P018, P021, P027, P034 und P035

## Zweck

Dieser historische Snapshot bereitet einen verlustarmen Chatwechsel vor. Er
ersetzt weder `PLAN_STATUS.md` noch die aktiven Modulplaene oder die
Nutzerentscheidungen. Bei Widerspruechen sind diese kanonischen Quellen
fuehrend.

## Kopierfertige Uebergabe fuer den naechsten Chat

```text
Arbeite im Repository 260524_Masterarbeit_Analyse nach AGENTS.md und den
projektlokalen Skills. Lies zuerst PLAN_INDEX.md, PLAN_STATUS.md, UD-104 bis
UD-107 sowie die fuer den naechsten Arbeitsschritt betroffenen Plaene.

Aktueller Release-Stand:
- Branch main, Release v0.35.1
- Commit ff1d902
- letzter vollstaendiger Testlauf: 658 Tests bestanden
- keine bekannten versionierten Release-Aenderungen nach v0.35.1 ausser den
  Dokumentationsergaenzungen dieses Handovers

Verbindlicher V1-PreProcess:
Projekt -> Wetter -> Gebaeude -> Zonen -> Technik ->
Parameter-Referenzstand -> Referenzdimensionierung ->
Parameter-Variationsspezifikation -> Varianten -> Simulation-Setup.
Der V1-PreProcess endet nach Simulation-Setup; Simulation, Ergebnisimport und
PostProcess sind nicht Teil dieses Laufs.

SmallOffice V1:
- Projekt Masterarbeit-Analyse, Endvariante 02, fuenf Zonen
- 5Z ist Referenz-, Dimensionierungs- und Optimierungsstand
- 29Z ist auswaehlbar und validierbar, startet aber keinen zweiten V1-Lauf
- Optimierung: 5 Temperaturbaender x 6 gekoppelte Leistungsfaktoren = 30 Faelle
- Sensitivitaet: vier Frankfurt-Jahreswetterfaelle und vier Zeitprofile,
  getrennt vom Optimierungsraum
- Referenzfall: 21/24 Grad C, Faktor 1,0

Aktive Projektworkspaces liegen ausserhalb des Repositorys unter
../260524_Masterarbeit_Arbeitsablage/04_Teil2_Prozessinnovation/Projekt_Workspaces/.
Im Repository liegen nur unveraenderliche Seed-Vorlagen.

Naechster fachlicher Schritt:
Den manuellen V1-PreProcess bis Simulation-Setup durchfuehren und je Modul
Dauer, Eingaben, Ausgaben, Weitergaben, Warnungen und Fehler dokumentieren.
Kritische Fehler stoppen den abhaengigen Ablauf; Warnungen werden
protokolliert.

Vor dem Durchlauf fehlen beziehungsweise sind manuell zu klaeren:
- reale zonale IDA-Heiz- und Kuehllasten in W,
- der konkrete Techniksystem-Excel-Katalog,
- der Rechte- und Quellennachweis fuer vollstaendige DIN-Nutzungsprofilwerte,
- der manuelle Smoke-Test des externen Projektstarts.

Offene Zukunftsideen, nicht fuer V1 freigegeben:
- Umnutzungs-Sensitivitaet mit alternativem Nutzungs-/Belegungsprofil bei
  zunaechst unveraendertem thermischem Modell; neuer Zonenzuschnitt separat,
- Untersuchung, ob manuell bestaetigte oder korrigierte Profilzuordnungen
  spaeter eine methodisch belastbare Lernbasis fuer Machine- oder
  Reinforcement-Learning-Vorschlaege bilden koennen.

Freigaberegel:
Read-only Analyse und Planung sind erlaubt. Aenderungen an Code,
Konfiguration, Daten oder Dokumentation erst nach der exakten Formulierung
„Freigabe zur Umsetzung“. Commit, Tag und Push bleiben den dokumentierten
Direktbefehlen vorbehalten.
```

## Umgesetzter und dokumentierter Stand

- UD-104 trennt Planung und Umsetzung und definiert die Git-Ausnahme fuer
  dokumentierte Direktbefehle.
- UD-105 definiert SmallOffice-Geometrie, Optimierungsraum,
  Sensitivitaetsfaelle und manuellen V1-Abnahmelauf.
- UD-106 fuehrt die modulweise UI-, Projekt- und PreProcess-Neuordnung.
- UD-107 legt aktive Projektworkspaces in die separate Arbeitsablage und
  behaelt im Repository nur Seed-Vorlagen.
- P035-S1 bis P035-S5 sind umgesetzt; der Projektwechsel-Guard verhindert
  stillen Verlust offener Entwuerfe.
- Der Runtime-Zyklus `ma_parameters`/`ma_zones` und der
  Komponenten-Katalog-Guardrail wurden vor v0.35.1 korrigiert.

## Offene Arbeits- und Forschungsfragen

- Manueller PreProcess-Durchlauf und reale V1-Eingaben.
- Techniksystem-Excel-Quelle.
- Rechte- und Quellenfreigabe fuer vollstaendige DIN-Profilwerte.
- Spaeteres generisches Sammelspeichern beliebiger Modul-Drafts.
- Spaetere 5Z/29Z-Struktursensitivitaet.
- Spaetere Umnutzungs-Sensitivitaet gemaess P021.
- Methodische Pruefung einer Lernbasis aus manuellen Profilentscheidungen
  gemaess P013.
- Einmalige lokale Administratorloeschung der 19 verbliebenen
  ACL-gesperrten synthetischen Testverzeichnisse.

## Fuehrende Referenzen

- `../../plans/PLAN_INDEX.md`
- `../../plans/PLAN_STATUS.md`
- `../../decisions/USER_DECISIONS_MASTERTHESIS_CODE.md` (UD-104 bis UD-107)
- `../../plans/inbox/260623_Plan_P008_ma_weather_Gesamtplan.md`
- `../../plans/inbox/260622_Plan_P011_ma_project_Projektinitialisierung.md`
- `../../plans/inbox/260622_Plan_P012_ma_building_Gebaeudeinput.md`
- `../../plans/inbox/260622_Plan_P013_ma_zones_Zonen_Nutzungen.md`
- `../../plans/inbox/260622_Plan_P014_ma_technical_Technische_Systeme.md`
- `../../plans/inbox/260622_Plan_P015_ma_parameters_Zentrale_Parameter.md`
- `../../plans/inbox/260622_Plan_P016_Stage1_Dimensionierung.md`
- `../../plans/inbox/260622_Plan_P017_ma_variants_Naming_Anbindung.md`
- `../../plans/inbox/260622_Plan_P018_ma_simulation_setup_Run_Manifest.md`
- `../../plans/inbox/260622_Plan_P021_Stage4_Sensitivitaet.md`
- `../../plans/inbox/260622_Plan_P027_Querschnitt_UI_Workflow_Validation_Feedback.md`
- `../../plans/inbox/260724_Plan_P034_Endvarianten_Kataloge_Excel_Aufnahme.md`
- `../../plans/inbox/260727_Plan_P035_Projekt_Workspace_Lokale_Projektablage.md`
- `../../../../CHANGELOG.md`
- `../../UPDATE_ROUTINES.md`

## Git- und Nachweisstand

- Ausgangs-HEAD: `ff1d902` (`v0.35.1`, synchron mit `origin/main`)
- Letzter vollstaendiger Testlauf: `658 passed`
- Dieser Handover und seine zugehoerigen Dokumentationsergaenzungen sind bei
  Erstellung noch nicht committed oder gepusht.
- Keine externe Verarbeitung und keine automatische Git-Aktion wurden durch
  `chat-handover` ausgeloest.
