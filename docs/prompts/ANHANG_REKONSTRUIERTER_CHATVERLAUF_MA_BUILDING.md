# Anhang X: Rekonstruierter Chatverlauf zur agentischen Softwareentwicklung am Beispiel `ma_building`

## Einordnung

Dieser Anhang ist eine gekürzte, konsolidierte Rekonstruktion eines
Planungs- und Übergabeprozesses. Er ist weder ein wortgetreues
Originaltranskript noch eine vollständige oder automatisch erzeugte
Protokollierung einzelner Chat-Interaktionen. Er verdeutlicht den
methodischen Ablauf von fachlichen Einzelideen über eine ChatGPT-gestützte
Modulplanung und einen konsolidierten Teilplan bis zum Repository-Abgleich
und zur Umsetzungsplanung durch Codex.

Die Aussagen zum aktuellen Projektstand wurden mit dem Plan P012 sowie den
versionierten `ma_building`-Moduldateien abgeglichen. Nicht durch diesen
Projektstand belegte historische Details sind ausdrücklich gekennzeichnet.

## Teil 1: ChatGPT-gestützte Modulplanung

**Ralph:**

Ich möchte für `ma_building` ein Modul für physische und geometrische
Gebäudedaten planen. Es soll KI-gestützte Erfassung, Dateiimport und eine
manuelle beziehungsweise textbasierte Eingabe ermöglichen.

**ChatGPT:**

Die drei Wege sollten nicht zu getrennten Datenmodellen führen. Sie sollen
eine gemeinsame, programmunabhängige `BuildingModelSpecification` erzeugen.
Diese enthält mindestens Gebäude, Geschosse, Räume, Bauteile, Öffnungen,
Sonnenschutz, Herkunft, Annahmen und Validierungsstatus.

**Ralph:**

Für die Dateiübernahme möchte ich mit Rhino arbeiten. Zusätzlich soll eine
textliche Eingabe möglich sein.

**ChatGPT:**

`.3dm` kann als Rhino-Quell- und Diagnoseformat vorgesehen werden. YAML ist
ein geeigneter erster verbindlicher textlicher Weg; JSON kann als kompatibles
Folgeformat vorbereitet werden. Die verbindliche Eingabe bleibt die
`BuildingModelSpecification`, nicht die CAD-Datei allein.

**Ralph:**

Wie unterscheiden wir Bauteiltypen von einzelnen Bauteilen?

**ChatGPT:**

Bauteilcodes beschreiben wiederverwendbare Typen, etwa `AW` für Außenwand,
`BP` für Bodenplatte, `DA` für Dach, `FA` für Außenfenster und `TA` für
Außentür. Jedes konkrete Objekt braucht zusätzlich eine eindeutige ID, etwa
`WALL-0001` oder `OPENING-0001`. Damit bleiben Typ und physisches Objekt
getrennt.

**Ralph:**

Fenster und Türen müssen einer Wand zugeordnet werden. Reichen Layernamen?

**ChatGPT:**

Layer können die Bearbeitung unterstützen, sind aber keine fachlich
verbindliche Beziehung. Eine konkrete Öffnung benötigt eine eigene ID und
eine `host_element_id`, die auf das konkrete Host-Bauteil verweist.

**Ralph:**

In einer frühen Phase kenne ich oft nur den Fensterflächenanteil. Einzelne
Fenster, ihre Einbaulage und Sonnenschutzelemente sind dann noch nicht
vollständig beschrieben.

**ChatGPT:**

Das Modell muss deshalb reifegradabhängig sein. Für eine einfache
LoD-1-Eingabe können Hüllkennwerte und Fensterflächenanteile genügen. Räume,
Einzelöffnungen und Host-Beziehungen werden erst bei höherem Eingabeumfang
verbindlich. Bei konkreten oder generierten Fenstern können Einbaulage und
Einbautiefe als zusätzliche Angaben erfasst werden. Sonnenschutz kann von
einem einfachen Kennwert bis zu einer detaillierten Geometrie reichen.

**Ralph:**

Welche Daten gehören nicht in `ma_building`?

**ChatGPT:**

`ma_building` verwaltet die bauliche Struktur, ein bauliches Raumregister,
Geometrie und bauliche Randbedingungen. Thermische Zonierung,
Nutzungsprofile und Betriebszeiten gehören zu `ma_zones`; technische Anlagen
und Regelungslogik zu `ma_technical`; zentrale Datenhaltung zu `ma_database`;
Variantensteuerung zu `ma_parameters`; die IDA-ICE-Übergabe zu
`ma_export_simulation`. Importierte Zonierungshinweise dürfen lediglich als
unverbindliche Hinweise erhalten bleiben.

**Ralph:**

Die Validierung soll davon abhängen, welche Analyse vorbereitet wird.

**ChatGPT:**

Die Validierung sollte den Eingabeumfang und den Analysezweck berücksichtigen.
Grundsätzlich sind eindeutige IDs, zulässige Bauteilcodes, Einheiten,
Nordrichtung und – bei konkreten Öffnungen – Host-Beziehungen zu prüfen. Für
LoD-1 sind insbesondere die Hüllparameter und der Fensterflächenanteil
relevant. Weitergehende analyseabhängige Pflichtdaten sind **zu prüfen**.

**Ralph:**

Fasse die Punkte als Übergabe für Codex zusammen. Codex soll zunächst nur
den vorhandenen Projektstand prüfen und daraus einen Umsetzungsplan ableiten.

**ChatGPT:**

Der konsolidierte Teilplan beschreibt die Rolle von `ma_building`, die drei
Eingabewege, die gemeinsame `BuildingModelSpecification`, Kennungen,
Reifegrade, Validierung und Modulgrenzen. Codex erhält ihn als fachliche
Arbeitsgrundlage und gleicht ihn vor jeder Umsetzung mit Repository, Plänen,
Tests und vorhandenen Schnittstellen ab.

## Teil 2: Übergabeprompt an Codex

**Ralph:**

Ich übergebe dir den konsolidierten Teilplan für `ma_building`. Prüfe zuerst
den Repository-Stand. Starte noch keine Implementierung.

`ma_building` soll physische und geometrische Gebäudedaten über KI-gestützte
Erfassung, Dateiimport sowie manuelle oder textbasierte Eingabe in eine
gemeinsame `BuildingModelSpecification` überführen. YAML ist der erste
verbindliche textliche Weg; JSON ist vorbereitet. `.3dm` ist als Rhino-Quell-
und Diagnoseformat vorgesehen, aber ein produktiver Rhino-Import ist nicht
vorausgesetzt.

Prüfe insbesondere vorhandene Fachmodelle, YAML-Beispiele, Importdiagnosen,
Validierung, Tests und UI. Berücksichtige Bauteilcodes und eindeutige
Objekt-IDs, `host_element_id` für konkrete Öffnungen, Öffnungs- und
Sonnenschutzreifegrade, Fensterflächenanteile, ein bauliches Raumregister
sowie die Abgrenzung zu `ma_zones`, `ma_database`, `ma_parameters` und
`ma_export_simulation`.

Ordne jede Anforderung als vorhanden, zu erweitern, neu anzulegen,
zurückzustellen, als Übergabe an ein anderes Modul oder als unklar ein.
Lege danach einen priorisierten Umsetzungsplan einschließlich Prüfschritten
vor. Überschreibe keine vorhandenen Strukturen.

## Teil 3: Rekonstruierter Codex-Anschluss

**Codex:**

Ich gleiche den Teilplan zunächst mit den vorhandenen Plänen, dem
`ma_building`-Paket, Konfigurationsbeispielen, Tests und der UI ab. Ich führe
noch keine Implementierung aus.

**Codex:**

Der Repository-Abgleich belegt eine `BuildingModelSpecification`,
YAML-Beispiele, LoD-1-Hüllparameter, Objekt-IDs, Bauteilcodes, Validierung
von `host_element_id`, einfache Sonnenschutzobjekte, lokale IFC-/3DM-
Quelldiagnose, Tests und eine Streamlit-Prüfansicht. Der aktuelle Umfang
enthält keinen produktiven IFC- oder Rhino-Import.

**Codex:**

Ich behandle die `BuildingModelSpecification` und die LoD-1-Eingabe als
vorhanden. Einen produktiven Rhino- oder IFC-Import, LoD-2/LoD-3-
Raum-/Bauteilumfang, detaillierte Fenstereinbaulagen und weitergehende
analyseabhängige Validierung markiere ich als zurückgestellt oder **zu
prüfen**. Die Übergaben an andere Module bleiben Schnittstellen- und
Handover-Punkte; sie werden nicht in `ma_building` implementiert.

**Codex:**

Als nächsten Schritt erstelle ich eine priorisierte Iterationsplanung mit
betroffenen Dateien und Tests. Eine Umsetzung beginnt erst nach einer
gesonderten Freigabe.

> Der Wortlaut dieses Codex-Anschlusses ist ein Methodikbeispiel. Ein
> vollständiger historischer Codex-Verlauf für genau diese Übergabe ist **aus
> Codex-Verlauf zu ergänzen**.

## Hinweis zur Prozessgrafik

Die zugehörige Prozessgrafik verdichtet die dargestellte Arbeitsfolge:

```text
fachliche Einzelideen und Rückfragen
→ ChatGPT-gestützte Modulplanung
→ konsolidierter Teilplan
→ Übergabe an Codex
→ Repository-Abgleich
→ Umsetzungsplanung
→ Implementierung
```

Sie ist eine methodische Übersicht und bildet weder einzelne Originalchats
noch eine zeitlich vollständige Projektchronologie ab.

## Hinweis zur KI-generierten Abbildung

Die Abbildung dient der visuellen Verdichtung des beschriebenen Prozesses.
Sie ist als KI-generierte Darstellung zu kennzeichnen; sie ist keine
automatisch aus Chat-, Git- oder Laufzeitdaten erzeugte Prozessaufzeichnung.
Verwendetes Werkzeug, Prompt, Erstellungsdatum und gegebenenfalls
nachträgliche Bearbeitungen sind **aus Codex-Verlauf zu ergänzen**, soweit
diese Nachweise für den Anhang erforderlich sind.

## Offene Prüfpunktliste

- Der genaue historische Ursprung, Zeitpunkt und Wortlaut der rekonstruierten
  ChatGPT- und Codex-Beiträge sind **nicht belegt**.
- Ob ein zusammenhängender historischer Codex-Handover zu diesem konkreten
  Teilplan vorliegt, ist **aus Codex-Verlauf zu ergänzen**.
- Die Herkunft, Prompt-Version und Bearbeitungsschritte der Prozessgrafik
  sowie der KI-generierten Abbildung sind **zu prüfen**.
- Der produktive Import von Rhino-`.3dm` oder IFC ist im geprüften Stand
  **nicht belegt**; vorhanden sind nur lokale Quelldiagnosen.
- JSON als produktiver Eingabeweg, detaillierte Fenstereinbaulagen,
  umfassende Öffnungs- und Sonnenschutzreifegrade sowie analyseabhängige
  Validierungsregeln über LoD-1 hinaus sind **zu prüfen**.
- Ein tatsächlicher Implementierungsabschluss unmittelbar nach dem hier
  dargestellten Codex-Anschluss ist **nicht belegt**; spätere Releases zeigen
  jedoch die schrittweise Umsetzung von `ma_building`.

## Repositorybezug der Rekonstruktion

Der Abgleich stützt sich insbesondere auf P012 (`ma_building
Gebäudeinput`), `docs/ma_building/README.md`, die Fachmodelle und Validierung
unter `src/ma_building/`, die YAML-Beispiele unter
`config/ma_building/examples/`, die Streamlit-Ansicht
`src/ma_ui/streamlit_app/module_views/building_view.py` sowie die zugehörigen
Tests. Die Git-Historie enthält dazu unter anderem Releases für
`ma_building`-Planung (1. Juli 2026), `ma_building` v1 (2. Juli 2026) und
LoD-1/Referenzrollen (5. Juli 2026). Diese Spuren belegen Projektentwicklung,
nicht jedoch den hier rekonstruierten Wortlaut einzelner Dialoge.
