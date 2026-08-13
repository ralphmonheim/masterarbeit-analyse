# P037-S0 Dokumentinventar und Ist-Analyse

Stand: 2026-08-13  
Status: abgeschlossen; reine Bestandsaufnahme, keine Archivierung oder Bereinigung

## Methode und Umfang

Die Erfassung verwendet ausschließlich `git ls-files '*.md'`. Zum Analysezeitpunkt sind das **196 versionierte Markdown-Dokumente**. Die vollständige, reproduzierbare Pfadmenge wird nicht manuell dupliziert, sondern über diesen Versionsstand erzeugt; die nachstehende Matrix klassifiziert jeden erfassten Pfad über seine eindeutige Pfadklasse. Für die konkrete Einzeldokumentliste bleibt `git ls-files '*.md'` der maßgebliche technische Nachweis.

Die lokale Arbeitsablage wurde nicht inhaltlich geöffnet. Der Navigator war in dieser Sitzung wegen eines lokalen Zugriffsfehlers auf die Arbeitsablage nicht lesbar. Dies ist ein Umgebungsbefund, keine Änderung seiner Rolle als reiner Navigationsadapter.

## Rollenmatrix für den vollständigen Bestand

| Pfadklasse (deckt jeden erfassten Pfad ab) | Aktueller Zweck und Themen | Zielgruppe | Führungsrolle / Aktualität | Überschneidungen | Empfohlene Zukunftsrolle |
|---|---|---|---|---|---|
| `docs/project/archive/**` | Archivierte Pläne, Leitfäden, Workflowstände und Chat-Handover | Projektsteuerung | Historischer Nachweis; nicht aktiv führend | Frühere aktive Quellen | Unverändert archivisch; nur über Archivindex und aktuelle Quelle navigieren |
| `docs/project/plans/inbox/**` | Aktive Gesamt-, Modul- und Umsetzungspläne | Projektsteuerung, Entwicklung | Führend für geplanten Scope | Planstatus, Entscheidungen, Architektur | Je Plan Scope/Ziele/Grenzen führen; Status nur verlinken |
| `docs/project/decisions/**` | Nutzer- und technische Entscheidungen, offene Punkte, Chat-Auswertung | Projektsteuerung, Entwicklung | Führend für Entscheidungen je Scope | Pläne, Architektur | Entscheidung als Ursprung, keine parallele Umsetzungsbeschreibung |
| `docs/project/architecture/**` | Zielarchitektur, Schnittstellen, Inventare, zeitgebundene Reviews | Entwicklung | Führend für Architektur; Reviews sind zeitgebunden | Pläne, Moduldocs, Entscheidungen | Zielquellen und Reviewnachweise in S1 klar trennen |
| `docs/project/MASTERARBEIT_LEITFADEN.md` | Wissenschaftliche Richtung, Methodenrahmen, Systemgrenzen | Autor, Betreuer | Führend | Pläne, Entscheidungen | Unverändert führend gemäß UD-128 |
| `docs/project/plans/PLAN_STATUS.md` | Aktueller Arbeits- und Modulstand | Projektsteuerung | Führend für Arbeitsstand | Einzelpläne, Changelog | Nur Ist-Status und nächste Schritte |
| `CHANGELOG.md` | Änderungshistorie | Projektsteuerung | Führend für Historie | Planstatus | Keine Statuswahrheit |
| `docs/project/UPDATE_ROUTINES.md` und `PROJECT_INPUT_WORKFLOW.md` | Verbindliche Routinen und Input-Prozess | Codex, Projektsteuerung | Führend für ihre Routine | commands_common, Skills | Als operative Ablaufquellen erhalten |
| übrige `docs/project/**` | Register, Projektorganisation, Wochenreviews, Ausgabeninventar | Projektsteuerung | Steuernde oder nachweisende Nebenquelle | Status, Pläne, Entscheidungen | In S1 je Informationsart einordnen |
| `docs/ma_*/**`, `docs/ida_ice/**` | Modulbedienung, Datenmodelle, Befehle, Architektur, technische Beispiele | Nutzer, Entwicklung | Gemischt und dezentral | Künftige Workflowsteckbriefe, technische Karten, Pläne | Fachlichen Langtext von technischer Modulinfo trennen oder stabil verweisen |
| `docs/prompts/**` | Wiederverwendbare Arbeitsaufträge | Autor, Codex | Führend für ihren Auftrag | Quellen-/Projektworkflow | Als Ausführungsartefakt erhalten |
| `docs/common/**`, `docs/examples/**`, `docs/README.md` | Gemeinsame Bedienung, Beispiele, Einstieg | Nutzer, Entwicklung | Lokale Orientierung | Fach- und Projektdokumentation | Kurze Adapter mit eindeutigem Verweisziel |
| `README.md`, `config/**/README.md`, `data/**/README.md`, `migrations/README.md`, `src/**.md` | Lokale Paket-, Daten- und Konfigurationsgrenze | Nutzer, Entwicklung | Lokale Orientierung | Modul- und Fachdocs | Kurz halten, auf führende Dokumentation verweisen |
| `.agents/**/*.md`, `.github/agents/*.md`, `AGENTS.md` | Agenten- und Arbeitsanweisungen | Codex, Entwicklung | Führend für konkrete Arbeitsregel | Routinen, Skills | Spezialanweisungen beibehalten |

## Konfliktliste und Priorisierung

| Priorität | Befund | Auswirkung | Weiterbehandlung |
|---|---|---|---|
| Hoch | Der fachliche Gesamtworkflow mit vollständigen Modulsteckbriefen fehlt. | Workflowwissen und technische Entwicklung sind noch nicht eindeutig getrennt. | S1-Sollstruktur prüfen; anschließend S2 als einzige fachliche Workflowquelle aufbauen. |
| Hoch | `PLAN_STATUS.md`, aktive Pläne, Entscheidungen und Architekturtexte enthalten teils überlappende Status- oder Zielaussagen. | Risiko paralleler Arbeitswahrheiten. | S1 definiert die Pflegematrix je Informationsart; S3 erst nach Bestätigung der konkreten Verweise. |
| Mittel | Modul-READMEs sind unterschiedlich tief und vermischen teils Fach- und Entwicklungsinformation. | UI-Karten könnten Langtexte doppelt pflegen. | S1 Rollen festlegen; S2/S4 Markdown-Steckbriefe und technischen Katalog trennen. |
| Mittel | Architektur-Reviews vom 2026-07-15 liegen neben aktuellen Architekturquellen. | Historische Empfehlung kann als aktuelle Vorgabe missverstanden werden. | S1 als Reviewnachweis einordnen, ohne Verschiebung. |
| Niedrig | Root-, Daten-, Konfigurations- und Skill-READMEs sind parallele Einstiegshilfen. | Geringes Risiko; oft notwendige Schnittstellensicht. | In S1 Zweck und Verweisziel festlegen, nicht zusammenziehen. |

## Ergebnis und Übergabe

Die Ist-Analyse bestätigt die Zielhierarchie aus UD-128: Leitfaden; fachlicher Gesamtworkflow (noch aufzubauen); Architektur, Entscheidungen und aktive Pläne; Arbeitsstand; Archiv; Navigator als Auffindbarkeitsadapter. Es wurden keine Dateien archiviert, verschoben oder gelöscht und keine Produkt- oder UI-Änderungen vorgenommen.

P037-S1 legt als nächsten Schritt für jedes nichtarchivische Dokument die verbindliche Hauptaufgabe sowie je Informationsart die führende Quelle fest. Vor S2 wird die daraus abgeleitete Sollstruktur gegen die P037-Abnahmekriterien geprüft.
