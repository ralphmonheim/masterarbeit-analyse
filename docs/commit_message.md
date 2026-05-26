Commit-Message-Richtlinie

Ziel: Einheitliche, leicht lesbare Release- und Commit-Beschreibungen.

Muster (erste Zeile wird als Titel benutzt):

Release x.x.x - Zusammenfassung der Version

- `x.x.x` ist die Release-Nummer (SemVer empfohlen).
- `Zusammenfassung der Version` ist eine kurze, prägnante Zeile (Ein-Zeiler).

Empfohlener Aufbau (mehrere Abschnitte, optional):

Kurzbeschreibung (ein Satz)

Added:
- Kurze Stichpunkte zu neuen Funktionen

Changed:
- Wichtige Änderungen oder Breaking Changes

Fixed:
- Kurzbeschreibung behobener Fehler

Docs:
- Erwähnung aktualisierter Dokumentation

Beispiel-Commit-Workflow (einmalig lokal konfigurieren):

```powershell
# Template-Datei als Commit-Template setzen
git config commit.template .gitmessage
```

Hinweis: Die erste Zeile der Commit-Nachricht entspricht dem kurzen Release-Titel. Bei normalen (nicht-Release) Commits kann das Muster adaptiv verwendet werden, z.B. `Fix: Kurze Beschreibung`.

Empfehlung: Vor jedem Release einen Commit mit der Release-Zeile erstellen, z.B. `Release 0.3.2 - Kurzbeschreibung` und dann taggen.

Optional: Wenn du möchtest, kann ich einen Git-Hook hinzufügen, der beim Commit prüft, ob Release-Commits dem Muster `^Release \d+\.\d+\.\d+ - ` folgen.
