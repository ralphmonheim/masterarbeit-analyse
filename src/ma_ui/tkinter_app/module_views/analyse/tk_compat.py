"""Gemeinsamer Tkinter-Import fuer die Analyseansicht."""

from __future__ import annotations

try:
    import tkinter as tk
    from tkinter import messagebox, ttk

    HAS_TKINTER = True
except ImportError:
    tk = None
    ttk = None
    messagebox = None
    HAS_TKINTER = False

__all__ = ["HAS_TKINTER", "messagebox", "tk", "ttk"]
