"""Datenvorbereitung fuer importierte Simulationsergebnisse.

Die bestehenden Befehle ``prepare`` und ``analyze-data`` bleiben fachlich in
ihren aktuellen Modulen. Dieser Bereich beschreibt den Workflow-Schritt, in dem
sie gemeinsam vor Analyse Stufe 2 eingeordnet werden.
"""

PREPARATION_COMMANDS: tuple[str, ...] = ("prepare", "analyze-data")
