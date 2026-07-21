# DIN-/Nautos-/VDE-/VDI-Compliance-Vorpruefung

Stand: 2026-07-14
Status: technische und vertragliche Vorpruefung, keine Rechtsberatung

## Ergebnis

Der institutionelle Nautos-Zugang der Frankfurt UAS ist durch den
DBIS-Eintrag 105040 belegt. Autorisierte Hochschulangehoerige koennen am
Campus und per VPN manuell recherchieren und die lokal lizenzierten Volltexte
lesen. Walk-in-Zugang gilt nur vor Ort. Der DBIS-Nachweis bestaetigt
Netzwerkzugang, aber nicht den konkreten DIN-Media-Vertragstyp
`Netzwerklizenz`, ein Vervielfaeltigungsrecht oder eine KI-Lizenz.

Die institutionsspezifische DBIS-Angabe ist fuer den Projektumfang enger als
der allgemeine Beschreibungstext: DIN-, VDI- und DWA-Volltexte sind
zugaenglich, DIN-VDE liegt in der separaten VDE-NormenBibliothek. ISO und
sonstige Normen stehen fuer Frankfurt UAS nicht als Nautos-Onlinevolltext zur
Verfuegung.

Der DBIS-Eintrag 103475 bestaetigt auch den lokalen Frankfurter Zugang zur
VDE-NormenBibliothek: DIN-VDE-Volltexte duerfen angesehen, aber nicht
heruntergeladen oder gedruckt werden. Erlaubt ist nur das Kopieren einzelner
Textpassagen, deren konkrete Weiterverwendung weiterhin geprueft werden muss.
IEC-Normen und Fachbuecher sind nicht Teil dieser lokalen Lizenz.

Fuer DIN-Inhalte erfordert die maschinelle Verarbeitung nach den aktuellen
DIN-Media-AGB grundsaetzlich eine gesonderte KI-Lizenz. Das derzeit
oeffentlich beschriebene DIN-KI-Angebot umfasst VDE nicht; fuer VDE und VDI
ist kein vergleichbares Standardangebot identifiziert.

Fuer beim VDE VERLAG erworbene Produkte untersagen die aktuellen AGB die
KI-Verarbeitung ausdruecklich. Der oeffentliche Standard-Nutzungsvertrag 2026
der VDE-NormenBibliothek behaelt Text und Data Mining vor und untersagt die
KI-Verarbeitung auch von erlaubten Auszuegen. Ob der konkrete Hochschulvertrag
abweicht, ist nicht belegt. VDI weist ausserdem Vervielfaeltigung,
Softwareverwertung und Netzwerknutzung als gesondert zu lizenzierende
Nutzungen aus.

Bis zu einem passenden schriftlichen Rechtebeleg gelten Norm-PDFs,
Seitenbilder, OCR, automatisierte Tabellen-/Formelextraktion, Embeddings, RAG,
systematische Normdatenbanken sowie das Einfuegen geschuetzter VDE- oder
VDI-Texte in KI-Systeme als gesperrt. Das gilt auch fuer ChatGPT, Codex und die
OpenAI API.

`vde_vdi_profile.yaml` bildet die quellenabhaengigen Schutzgrenzen ab. Der
Bezugsweg und die anwendbaren Bedingungen werden immer vor der
Verarbeitung bestimmt; bei gemeinsamen VDI/VDE-Regelwerken gilt bis zur
Klaerung die strengste einschlaegige Grenze.

## Zulassiger Zwischenweg

- oeffentliche bibliografische Metadaten manuell und offizielle
  Quellenverweise speichern,
- lizenzierte Normen als autorisierte Person manuell lesen,
- begrenzte eigene Notizen und eigenstaendige Formulierungen ohne
  Rekonstruktion erstellen,
- fachliche Parameter, Regeln und Rechenlogik unabhaengig entwickeln,
- jede produktive Regel mit Norm, Ausgabe, Abschnitt, Einheit und manueller
  Fachpruefung belegen,
- keine Ersatzfassung der Norm erzeugen.

Eine aus einer konkreten VDE- oder VDI-Regel abgeleitete Softwarelogik ist
nicht automatisch eine gruen freigegebene eigene Entwicklung. Sie bleibt bis
zur Pruefung der Rechte-, Quellen- und Veroeffentlichungsbedingungen `yellow`.
Dasselbe gilt fuer manuell uebernommene Grenzwerte, Formeln,
Tabellenfragmente, Abbildungen und kurze Zitate.

Die lokalen Arbeitsdaten unter `data/common/normen/` und
`data/ma_parameters/config/din18599_10_nutzungsprofile/` bleiben lokale
Pruefbestaende. Sie sind keine freigegebene produktive Normlogik und duerfen
nicht ungeprueft versioniert, mit KI verarbeitet oder implementiert werden.

## Schlanker Arbeitsmodus fuer die Entwicklung

Die Compliance-Pruefung wird nicht fuer jeden normalen Entwicklungsschritt
wiederholt. Frei bleiben eigener Quellcode, neutrale Datenvertraege,
synthetische Tests, bibliografische Metadaten sowie eigene begrenzte
Paraphrasen und fachliche Interpretationen.

Eine einzelne, paket- oder quellenbezogene Pruefung ist nur erforderlich,
bevor ein geschuetztes Dokument maschinell geoeffnet oder verarbeitet wird,
eine Tabelle oder Formel automatisch extrahiert beziehungsweise konvertiert
wird, Inhalte an externe Dienste oder KI uebergeben werden, reale oder
abgeleitete geschuetzte Daten in das Repository gelangen oder Inhalte
veroeffentlicht beziehungsweise weitergegeben werden.

Eine autorisierte Person darf die Quelle lokal manuell lesen und erforderliche
Werte gezielt in einen als `local_only` markierten Reviewbestand eintragen.
Dieser Arbeitsmodus erlaubt weder eine automatische Uebernahme noch eine
vollstaendige Rekonstruktion der Norm und ersetzt keine Pruefung vor einer
produktiven oder veroeffentlichten Nutzung.

## Gesetzliche Ausnahmen

Die Paragraphen 44b und 60d UrhG enthalten Regelungen zu Text und Data Mining.
Ob sie die konkrete Masterarbeit, die vorhandenen Hochschulzugriffe, externe
KI-Dienste, Kopien und Aufbewahrung abdecken, wird hier nicht abschliessend
entschieden. Hierfuer ist eine Bestaetigung der Hochschule oder ihrer
Lizenz-/Rechtsstelle erforderlich.

## Offene Freigabe

`university_permission_request.md` ist ein noch nicht versendeter Entwurf zur
Bestaetigung der konkreten Hochschulvertraege. Separate, ebenfalls nicht
versendete Rechteinhaberanfragen stehen in
`rights_holder_permission_requests.md`. Eine Hochschulbestaetigung belegt nur
den Umfang des Hochschulvertrags und ersetzt keine darueber hinaus benoetigte
Rechteinhabergenehmigung.

Bis zu passenden Antworten gelten `ai_license_confirmed: false` und
`default_policy: stop_and_warn`.
