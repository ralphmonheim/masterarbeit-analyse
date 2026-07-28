"""Lokale native Dialogadapter der Desktop-Ausfuehrung."""

from __future__ import annotations

from pathlib import Path


class TkinterFolderDialogAdapter:
    """Windows-Ordnerdialog ohne zusaetzliche Abhaengigkeit."""

    def choose_folder(self, *, initial_directory: Path | None = None) -> Path | None:
        import tkinter as tk
        from tkinter import filedialog

        root = tk.Tk()
        root.withdraw()
        try:
            selected = filedialog.askdirectory(
                initialdir=str(initial_directory) if initial_directory else None
            )
        finally:
            root.destroy()
        return Path(selected) if selected else None
