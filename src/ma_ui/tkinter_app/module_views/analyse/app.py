"""Tk-GUI fuer die ma_analyse-Pipeline."""

from __future__ import annotations

import contextlib
import ctypes
import os
import time

from . import constants as _constants
from .dialogs import SettingsDialogMixin
from .initial_state import TkinterAnalysisInitialStateMixin
from .layout_steps import TkinterAnalysisLayoutStepsMixin
from .pipeline_runner import TkinterAnalysisPipelineRunnerMixin
from .plot_template_state import TkinterAnalysisPlotTemplateStateMixin
from .selection_state import TkinterAnalysisSelectionStateMixin
from .singleton import GUI_REPLACE_TIMEOUT_SECONDS, GuiInstanceController, send_refresh_message
from .step_flow import TkinterAnalysisStepFlowMixin
from .theme_window import TkinterAnalysisThemeWindowMixin
from .tk_compat import HAS_TKINTER, tk

DEFAULT_COMMAND = _constants.DEFAULT_COMMAND
WINDOWS_APP_USER_MODEL_ID = _constants.WINDOWS_APP_USER_MODEL_ID


def _set_windows_app_user_model_id():
    """Setzt unter Windows eine stabile App-ID fuer Taskleisten-Gruppierung."""
    if os.name != "nt":
        return
    with contextlib.suppress(Exception):
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(WINDOWS_APP_USER_MODEL_ID)


def run_gui(args):
    """Startet die normale GUI und ersetzt eine bereits laufende Instanz."""
    if not HAS_TKINTER:
        print("X Tkinter ist nicht verfuegbar. Bitte fuehren Sie das Skript in einer GUI-faehigen Umgebung aus.")
        raise SystemExit(1)

    if getattr(args, "gui_refresh_port", None):
        run_gui_refresh(args)
        return

    controller = GuiInstanceController()
    if not controller.acquire():
        response = None
        with contextlib.suppress(Exception):
            response = GuiInstanceController.send_message("REPLACE_WITH_NEW")
        if response not in {"RELEASING", "CLOSING"}:
            print("X Die vorhandene GUI konnte nicht fuer den neuen Aufruf freigegeben werden.")
            return

        deadline = time.time() + GUI_REPLACE_TIMEOUT_SECONDS
        while time.time() < deadline:
            if controller.acquire():
                break
            time.sleep(0.1)
        else:
            print("X Neue GUI konnte die vorhandene Instanz nicht abloesen.")
            return

    _set_windows_app_user_model_id()
    root = tk.Tk()
    PipelineGUI(root, args, singleton_controller=controller)
    root.mainloop()


def run_gui_refresh(args):
    """Startet eine neue GUI-Instanz im kontrollierten Refresh-Ablauf."""
    refresh_port = getattr(args, "gui_refresh_port", None)
    if not refresh_port:
        raise SystemExit(1)

    response = send_refresh_message(refresh_port, "REQUEST_RELEASE", timeout=5)
    if response != "RELEASED":
        print("X GUI-Aktualisierung konnte die alte Instanz nicht freigeben.")
        raise SystemExit(1)

    controller = GuiInstanceController()
    deadline = time.time() + 10
    while time.time() < deadline:
        if controller.acquire():
            break
        time.sleep(0.1)
    else:
        print("X Neue GUI konnte die Singleton-Rolle nicht uebernehmen.")
        raise SystemExit(1)

    _set_windows_app_user_model_id()
    root = tk.Tk()
    gui = PipelineGUI(
        root,
        args,
        singleton_controller=controller,
        refresh_port=refresh_port,
    )
    root.update_idletasks()
    gui._focus_window()
    with contextlib.suppress(Exception):
        send_refresh_message(refresh_port, "NEW_GUI_ACTIVE", timeout=5)
    root.mainloop()


class PipelineGUI(
    TkinterAnalysisInitialStateMixin,
    TkinterAnalysisThemeWindowMixin,
    TkinterAnalysisLayoutStepsMixin,
    TkinterAnalysisStepFlowMixin,
    TkinterAnalysisPipelineRunnerMixin,
    TkinterAnalysisSelectionStateMixin,
    TkinterAnalysisPlotTemplateStateMixin,
    SettingsDialogMixin,
):
    """Grafische Oberflaeche fuer Pipeline-Auswahl und Ausfuehrung.

    Die Klasse verwaltet GUI-Zustand, Validierung und Protokollausgabe. Die
    eigentliche Arbeit wird an die Runner-Funktionen delegiert und in einem
    Hintergrundthread gestartet, damit das Fenster waehrend der Analyse
    bedienbar bleibt.
    """

    def __init__(self, root, args, singleton_controller=None, refresh_port=None):
        self._initialize_pipeline_gui(root, args, singleton_controller, refresh_port)


def run_gui_menu(args):
    """Startet die GUI ohne Singleton-Ersetzung fuer Menue-/Tool-Aufrufe."""
    if not HAS_TKINTER:
        print("X Tkinter ist nicht verfuegbar. Bitte fuehren Sie das Skript in einer GUI-faehigen Umgebung aus.")
        raise SystemExit(1)
    _set_windows_app_user_model_id()
    root = tk.Tk()
    gui = PipelineGUI(root, args)
    gui._focus_window()
    root.mainloop()
