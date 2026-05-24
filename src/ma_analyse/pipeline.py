"""Zentraler Einstiegspunkt fuer CLI und GUI der Analysepipeline.

Dieses Modul verbindet die einzelnen Fachskripte zu Befehlen wie ``prepare``,
``comfort``, ``analyze_data``, ``heating``, ``cooling`` und ``all``. Es stellt
sowohl die CLI als auch die Tk-GUI bereit.

Wichtige Aufgaben:
    - CLI-Argumente in Runtime-Optionen der Fachskripte uebersetzen.
    - GUI-Auswahl validieren und in Hintergrundthreads ausfuehren.
    - Eine einzelne aktive GUI-Instanz erzwingen und Aktualisierungen abwickeln.
    - Zusatzdialoge fuer Namensmapping und Ausgabeformate bereitstellen.
"""

import argparse
import contextlib
import ctypes
import os
import queue
import socket
import subprocess
import sys
import threading
import time
import traceback
from pathlib import Path

try:
    import tkinter as tk
    from tkinter import messagebox, ttk

    HAS_TKINTER = True
except ImportError:
    tk = None
    ttk = None
    messagebox = None
    HAS_TKINTER = False

from . import naming as NAMENSMAPPING_MODULE
from .analyze import build_excel_report
from .comfort import (
    OUTPUT_DIR,
    get_run_id,
    process_analysis,
    process_overview,
    process_plots,
)
from .config import DATENBANK_DIR, EXPORT_FORMATS, INPUT_DIR, ROOMS
from .cooling import main as compare_cooling_comparison
from .heating import (
    MAX_CALENDAR_WEEK,
    MONTH_DAY_COUNTS,
    MONTH_NAMES,
)
from .heating import (
    main as compare_heating_comparison,
)
from .naming import LEGACY_MAPPING_DOC as NAMENSMAPPING_DOC
from .output_formats import (
    FORMAT_CATALOG,
    FORMAT_DOC,
    ensure_output_format_doc,
    get_format_names,
    load_output_format_rules,
    write_output_format_rules,
)
from .prepare import process_all_variants

OUTPUT_FORMAT_DOC = FORMAT_DOC

STEP_SEQUENCE = ["prepare", "plots", "overview", "analysis", "analyze", "heating", "cooling"]
DATABASE_STEPS = {"plots", "overview", "analysis", "analyze", "heating", "cooling"}
STEP_TITLES = {
    "prepare": "prepare (Rohdaten aufbereiten)",
    "plots": "plots (Einzelne Raumdiagramme)",
    "overview": "overview (PDF-Uebersicht)",
    "analysis": "analysis (Behaglichkeitsanalyse)",
    "analyze": "analyze_data (Excel-Auswertung)",
    "heating": "heating (Heizvergleich)",
    "cooling": "cooling (Kuehlvergleich)",
}
COMMAND_TO_INTERNAL_STEP = {
    "prepare": "prepare",
    "plots": "plots",
    "overview": "overview",
    "analysis": "analysis",
    "analyze_data": "analyze",
    "analyze-data": "analyze",
    "heating": "heating",
    "cooling": "cooling",
}
DISABLED_GUI_COMMANDS = set()
GUI_SINGLETON_HOST = "127.0.0.1"
GUI_SINGLETON_PORT = 47683
GUI_SINGLETON_TIMEOUT = 0.35
GUI_REFRESH_TIMEOUT_SECONDS = 20
GUI_REPLACE_TIMEOUT_SECONDS = 10

COMFORT_OUTPUT_TYPES = {
    "plot": {
        "steps": ["plots"],
        "plot_single": True,
        "plot_overview": False,
        "analysis_individual": False,
        "analysis_overview": False,
    },
    "plot_overview": {
        "steps": ["overview"],
        "plot_single": False,
        "plot_overview": True,
        "analysis_individual": False,
        "analysis_overview": False,
    },
    "plot_analysis": {
        "steps": ["plots", "analysis"],
        "plot_single": True,
        "plot_overview": False,
        "analysis_individual": True,
        "analysis_overview": False,
    },
    "plot_analysis_overview": {
        "steps": ["plots", "overview", "analysis"],
        "plot_single": True,
        "plot_overview": True,
        "analysis_individual": True,
        "analysis_overview": True,
    },
}


# ============================================================================
# GUI-Instanzsteuerung und Hintergrundkommunikation
# ============================================================================


class GuiInstanceController:
    """Verwaltet die einzelne aktive GUI-Instanz und Fokus-Signale."""

    def __init__(self, host=GUI_SINGLETON_HOST, port=GUI_SINGLETON_PORT):
        self.host = host
        self.port = port
        self.server_socket = None
        self.listener_thread = None
        self.stop_event = threading.Event()
        self.message_handler = None

    def acquire(self):
        if self.server_socket is not None:
            return True

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._set_exclusive_bind(server_socket)
        try:
            server_socket.bind((self.host, self.port))
            server_socket.listen(5)
            server_socket.settimeout(0.5)
        except OSError:
            server_socket.close()
            return False

        self.server_socket = server_socket
        self.stop_event.clear()
        return True

    def _set_exclusive_bind(self, server_socket):
        if os.name == "nt" and hasattr(socket, "SO_EXCLUSIVEADDRUSE"):
            with contextlib.suppress(OSError):
                server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
            return

        with contextlib.suppress(OSError):
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def start_listener(self, message_handler):
        self.message_handler = message_handler
        if self.server_socket is None:
            raise RuntimeError("Listener kann nur nach erfolgreicher Singleton-Akquise gestartet werden.")

        if self.listener_thread is not None and self.listener_thread.is_alive():
            return

        self.listener_thread = threading.Thread(target=self._serve, daemon=True)
        self.listener_thread.start()

    def _serve(self):
        while not self.stop_event.is_set() and self.server_socket is not None:
            try:
                connection, _address = self.server_socket.accept()
            except socket.timeout:
                continue
            except OSError:
                break

            with connection:
                try:
                    payload = connection.recv(1024).decode("utf-8").strip()
                except OSError:
                    payload = ""
                if self.message_handler is not None and payload:
                    try:
                        response = self.message_handler(payload)
                    except Exception:
                        response = "ERROR"
                else:
                    response = "IGNORED"
                try:
                    connection.sendall((response or "OK").encode("utf-8"))
                except OSError:
                    pass

    def stop(self):
        self.stop_event.set()
        if self.server_socket is not None:
            try:
                self.server_socket.close()
            except OSError:
                pass
            self.server_socket = None

    @classmethod
    def send_message(cls, message, host=GUI_SINGLETON_HOST, port=GUI_SINGLETON_PORT, timeout=GUI_SINGLETON_TIMEOUT):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(timeout)
        try:
            client.connect((host, port))
            client.sendall(message.encode("utf-8"))
            response = client.recv(1024).decode("utf-8").strip()
            return response or None
        finally:
            client.close()


class GuiRefreshCoordinator:
    """Koordiniert den sicheren Übergang von alter zu neuer GUI-Instanz."""

    def __init__(self, gui):
        self.gui = gui
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((GUI_SINGLETON_HOST, 0))
        self.server_socket.listen(5)
        self.server_socket.settimeout(0.5)
        self.port = self.server_socket.getsockname()[1]
        self.stop_event = threading.Event()
        self.listener_thread = threading.Thread(target=self._serve, daemon=True)
        self.released_singleton = False
        self.completed = False

    def start(self):
        self.listener_thread.start()
        return self.port

    def _serve(self):
        while not self.stop_event.is_set():
            try:
                connection, _address = self.server_socket.accept()
            except socket.timeout:
                continue
            except OSError:
                break

            with connection:
                try:
                    payload = connection.recv(1024).decode("utf-8").strip()
                except OSError:
                    payload = ""
                response = self._handle_message(payload)
                try:
                    connection.sendall(response.encode("utf-8"))
                except OSError:
                    pass

    def _handle_message(self, payload):
        if payload == "REQUEST_RELEASE":
            released = self.gui.root.after(0, self.gui._release_singleton_for_refresh)
            del released
            deadline = time.time() + 5
            while time.time() < deadline:
                if self.released_singleton:
                    self.gui.root.after(0, self.gui._schedule_refresh_timeout_recovery)
                    return "RELEASED"
                time.sleep(0.05)
            return "FAILED"

        if payload == "NEW_GUI_ACTIVE":
            self.completed = True
            self.gui.root.after(0, self.gui._finalize_refresh_shutdown)
            return "ACK"

        return "IGNORED"

    def mark_released(self):
        self.released_singleton = True

    def close(self):
        self.stop_event.set()
        if self.server_socket is not None:
            try:
                self.server_socket.close()
            except OSError:
                pass
            self.server_socket = None


def send_refresh_message(port, message, timeout=5):
    """Sendet eine Steuerungsnachricht an den temporären GUI-Refresh-Server."""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(timeout)
    try:
        client.connect((GUI_SINGLETON_HOST, port))
        client.sendall(message.encode("utf-8"))
        return client.recv(1024).decode("utf-8").strip()
    finally:
        client.close()


class QueueLogWriter:
    """Leitet stdout/stderr aus dem Worker-Thread in die Tk-Queue."""

    def __init__(self, output_queue):
        self.output_queue = output_queue

    def write(self, text):
        if text:
            self.output_queue.put(("log", text))
        return len(text)

    def flush(self):
        return None


# ============================================================================
# CLI-/Pipeline-Hilfsfunktionen
# ============================================================================


def get_comfort_output_settings(output_type):
    """Uebersetzt Comfort-Unterbefehle in interne Pipeline-Schritte."""
    if output_type not in COMFORT_OUTPUT_TYPES:
        raise ValueError(f"Ungültiger output_type: {output_type}. Erwartet: {', '.join(COMFORT_OUTPUT_TYPES)}")
    return COMFORT_OUTPUT_TYPES[output_type]


def parse_comma_separated_list(value):
    """Wandelt eine kommaseparierte CLI-Eingabe in eine Liste um."""
    if not value:
        return None
    return [item.strip() for item in value.split(",") if item.strip()]


def format_cli_list(values):
    """Wandelt eine Liste zurueck in das CLI-Listenformat."""
    if not values:
        return None
    return ",".join(values)


def has_cli_option(argv, *option_names):
    """Prueft, ob eine Option explizit in der CLI-Eingabe vorkam."""
    for item in argv:
        if item in option_names:
            return True
        if any(item.startswith(f"{option_name}=") for option_name in option_names):
            return True
    return False


def normalize_rooms(selected_rooms):
    """Normalisiert eine optionale Raumauswahl auf die Standardraumliste."""
    if selected_rooms is None:
        return ROOMS.copy()

    normalized = [room for room in ROOMS if room in selected_rooms]
    if normalized:
        return normalized

    print(f"X Ungueltige Raeume: {selected_rooms}")
    print(f"  Verfuegbare Raeume: {ROOMS}")
    raise SystemExit(1)


def list_input_variants(input_root):
    """Listet Rohdatenvarianten fuer den prepare-Befehl."""
    if not os.path.isdir(input_root):
        return []
    return sorted(
        entry
        for entry in os.listdir(input_root)
        if os.path.isdir(os.path.join(input_root, entry))
        and any(os.path.isdir(os.path.join(input_root, entry, room_name)) for room_name in ROOMS)
    )


def list_datenbank_variants(datenbank_dir):
    """Listet Nutzdatenvarianten fuer Analyse- und Plotbefehle."""
    if not os.path.isdir(datenbank_dir):
        return []
    return sorted(
        entry
        for entry in os.listdir(datenbank_dir)
        if os.path.isdir(os.path.join(datenbank_dir, entry)) and entry.endswith("_nutzdaten")
    )


def strip_variant_suffix(variant_name):
    """Entfernt bekannte Varianten-Suffixe fuer GUI-Anzeigen."""
    for suffix in ("_rohdaten", "_nutzdaten"):
        if variant_name.endswith(suffix):
            return variant_name[: -len(suffix)]
    return variant_name


def run_prepare(args):
    """Fuehrt den prepare-Befehl aus und erzeugt Nutzdaten."""
    process_all_variants(
        args.input_dir,
        args.rooms,
        args.datenbank_dir,
        debug=args.debug,
        selected_variants=args.variants,
        export_format=getattr(args, "export_format", "csv"),
    )


def run_plots(args):
    """Fuehrt Comfort-Einzelplots aus."""
    process_plots(
        datenbank_dir=args.datenbank_dir,
        rooms=args.rooms,
        run_id=args.run_id,
        output_root=args.output_root,
        variant_dirs=args.variants,
        debug=args.debug,
        output_subdir=getattr(args, "plot_output_subdir", None),
    )


def run_overview(args):
    """Fuehrt Comfort-PDF-Uebersichten aus."""
    process_overview(
        datenbank_dir=args.datenbank_dir,
        rooms=args.rooms,
        run_id=args.run_id,
        output_root=args.output_root,
        variant_dirs=args.variants,
        debug=args.debug,
    )


def run_analysis(args, run_id=None, output_individual=True, output_overview=True):
    """Fuehrt die Comfort-Zonenanalyse aus und protokolliert die Tabelle."""
    result = process_analysis(
        datenbank_dir=args.datenbank_dir,
        rooms=args.rooms,
        run_id=run_id,
        output_root=args.output_root,
        variant_dirs=args.variants,
        debug=args.debug,
        output_individual=output_individual,
        output_overview=output_overview,
    )
    if result is None:
        print("X Keine Ergebnisse erzeugt")
        raise SystemExit(1)

    print(result.to_string(index=False))


def run_analyze(args):
    """Fuehrt analyze_data aus und mappt GUI-Ausgabearten auf Excel-Modi."""
    layout_mode = getattr(args, "heating_series_layout", None)
    if layout_mode == "separate":
        variant_mode = "single"
    elif layout_mode == "combined":
        variant_mode = "compare"
    else:
        variant_mode = getattr(args, "heating_mode", None)
        if variant_mode is None:
            variant_mode = "compare" if getattr(args, "variant_mode_explicit", False) else "single"

    output_files = build_excel_report(
        args.datenbank_dir,
        output_root=args.output_root,
        debug=args.debug,
        run_id=args.run_id,
        selected_variants=args.variants,
        rooms=args.rooms,
        variant_mode=variant_mode,
    )
    if isinstance(output_files, list):
        for output_file in output_files:
            print(f"Excel-Ausgabe erstellt: {output_file}")
        return
    print(f"Excel-Ausgabe erstellt: {output_files}")


def run_heating(args):
    """Fuehrt den Heating-Vergleich mit den gewaehlten Zeit-/Layoutoptionen aus."""
    compare_heating_comparison(
        args.datenbank_dir,
        debug=args.debug,
        selected_variants=args.variants,
        rooms=args.rooms,
        view=getattr(args, "view", "bar"),
        month=getattr(args, "month", None),
        week=getattr(args, "week", None),
        day=getattr(args, "day", None),
        variant_mode=getattr(args, "heating_mode", None) or "compare",
        series_layout=getattr(args, "heating_series_layout", None) or "separate",
        output_root=getattr(args, "output_root", None),
        run_id=getattr(args, "run_id", None),
    )


def run_cooling(args):
    """Fuehrt den Cooling-Vergleich mit den gewaehlten Zeit-/Layoutoptionen aus."""
    view = getattr(args, "view", "year")
    compare_cooling_comparison(
        args.datenbank_dir,
        debug=args.debug,
        selected_variants=args.variants,
        rooms=args.rooms,
        view=view,
        month=getattr(args, "month", None),
        week=getattr(args, "week", None),
        day=getattr(args, "day", None),
        variant_mode=getattr(args, "heating_mode", None) or "compare",
        series_layout=getattr(args, "heating_series_layout", None) or "separate",
        output_root=getattr(args, "output_root", None),
        run_id=getattr(args, "run_id", None),
    )


def run_comfort(args):
    """Fuehrt den Comfort-Unterbefehl ueber die gemeinsame Pipeline aus."""
    output_type = getattr(args, "output_type", "plot_analysis_overview")
    settings = get_comfort_output_settings(output_type)
    execute_steps(
        args,
        steps=settings["steps"],
        variants=args.variants,
        rooms=args.rooms,
        comfort_options=settings,
    )


def ensure_required_data(args, steps):
    """Bricht Analyse-/Plotbefehle ab, wenn vorherige Nutzdaten fehlen."""
    if not any(step in DATABASE_STEPS for step in steps):
        return

    if os.path.exists(args.datenbank_dir):
        return

    if "prepare" in steps:
        return

    print(f"X Verzeichnis mit aufbereiteten Daten nicht gefunden: {args.datenbank_dir}")
    print("  Fuehren Sie zuerst 'prepare' aus oder waehlen Sie in der GUI auch prepare.")
    raise SystemExit(1)


def build_runtime_args(
    args,
    variants=None,
    rooms=None,
    heating_mode=None,
    prepare_options=None,
    comfort_options=None,
    heating_options=None,
    plot_output_subdir=None,
):
    """Baut ein einheitliches Argumentobjekt fuer interne Pipeline-Schritte."""
    comfort_defaults = {
        "plot_single": True,
        "plot_overview": True,
        "analysis_individual": True,
        "analysis_overview": True,
    }
    if comfort_options:
        comfort_defaults.update(comfort_options)

    heating_defaults = {
        "view": getattr(args, "view", "bar"),
        "month": getattr(args, "month", None),
        "week": getattr(args, "week", None),
        "day": getattr(args, "day", None),
        "series_layout": getattr(args, "heating_series_layout", None) or "separate",
    }
    if heating_options:
        heating_defaults.update(heating_options)

    prepare_defaults = {
        "export_format": getattr(args, "export_format", "csv"),
    }
    if prepare_options:
        prepare_defaults.update(prepare_options)

    return argparse.Namespace(
        input_dir=args.input_dir,
        datenbank_dir=args.datenbank_dir,
        output_root=args.output_root,
        run_id=args.run_id,
        debug=args.debug,
        variants=variants,
        rooms=rooms if rooms is not None else ROOMS.copy(),
        view=heating_defaults["view"],
        month=heating_defaults["month"],
        week=heating_defaults["week"],
        day=heating_defaults["day"],
        heating_series_layout=heating_defaults["series_layout"],
        heating_mode=heating_mode or getattr(args, "heating_mode", None) or "compare",
        plot_single=comfort_defaults["plot_single"],
        plot_overview=comfort_defaults["plot_overview"],
        analysis_individual=comfort_defaults["analysis_individual"],
        analysis_overview=comfort_defaults["analysis_overview"],
        plot_output_subdir=plot_output_subdir,
        export_format=prepare_defaults["export_format"],
    )


def execute_steps(
    args,
    steps,
    variants=None,
    rooms=None,
    heating_mode=None,
    prepare_options=None,
    comfort_options=None,
    heating_options=None,
    plot_output_subdir=None,
):
    """Fuehrt eine geordnete Teilmenge der Pipeline-Schritte aus."""
    selected_steps = [step for step in STEP_SEQUENCE if step in steps]
    ensure_required_data(args, selected_steps)

    runtime_args = build_runtime_args(
        args,
        variants=variants,
        rooms=rooms,
        heating_mode=heating_mode,
        prepare_options=prepare_options,
        comfort_options=comfort_options,
        heating_options=heating_options,
        plot_output_subdir=plot_output_subdir,
    )

    print("\n" + "=" * 70)
    print("PIPELINE GESTARTET")
    print("=" * 70)

    total_steps = len(selected_steps)
    for index, step in enumerate(selected_steps, start=1):
        if step == "plots" and not runtime_args.plot_single:
            continue
        if step == "overview" and not runtime_args.plot_overview:
            continue

        print(f"\nSchritt {index}/{total_steps}: {STEP_TITLES[step]}")
        print("-" * 70)

        if step == "prepare":
            run_prepare(runtime_args)
            continue

        if step == "plots":
            run_plots(runtime_args)
            continue

        if step == "overview":
            run_overview(runtime_args)
            continue

        if step == "analysis":
            run_analysis(
                runtime_args,
                run_id=runtime_args.run_id,
                output_individual=runtime_args.analysis_individual,
                output_overview=runtime_args.analysis_overview,
            )
            continue

        if step == "analyze":
            run_analyze(runtime_args)
            continue

        if step == "heating":
            run_heating(runtime_args)

        if step == "cooling":
            run_cooling(runtime_args)

    print("\n" + "=" * 70)
    print("PIPELINE ABGESCHLOSSEN")
    print("=" * 70)


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


def build_gui_restart_argv(args, refresh_port):
    """Baut den CLI-Aufruf, mit dem sich die GUI selbst neu startet."""
    script_path = Path(__file__).resolve()
    argv = [sys.executable, str(script_path), "gui"]

    option_values = [
        ("--input-dir", getattr(args, "input_dir", None), INPUT_DIR),
        ("--datenbank-dir", getattr(args, "datenbank_dir", None), DATENBANK_DIR),
        ("--output-root", getattr(args, "output_root", None), OUTPUT_DIR),
        ("--run-id", getattr(args, "run_id", None), None),
        ("--variants", format_cli_list(getattr(args, "variants", None)), None),
        ("--rooms", format_cli_list(getattr(args, "rooms", None)), None),
        ("--view", getattr(args, "view", None), "bar"),
        ("--month", getattr(args, "month", None), None),
        ("--week", getattr(args, "week", None), None),
        ("--day", getattr(args, "day", None), None),
        ("--heating-mode", getattr(args, "heating_mode", None), "compare"),
        ("--heating-series-layout", getattr(args, "heating_series_layout", None), "separate"),
        ("--export-format", getattr(args, "export_format", None), "csv"),
    ]

    for option_name, value, default_value in option_values:
        if value is None:
            continue
        if default_value is not None and value == default_value:
            continue
        argv.extend([option_name, str(value)])

    if getattr(args, "debug", True):
        argv.append("--debug")
    else:
        argv.append("--no-debug")

    window_geometry = getattr(args, "gui_window_geometry", None)
    if isinstance(window_geometry, dict):
        for option_name, key in (
            ("--gui-window-x", "x"),
            ("--gui-window-y", "y"),
            ("--gui-window-width", "width"),
            ("--gui-window-height", "height"),
        ):
            value = window_geometry.get(key)
            if value is not None:
                argv.extend([option_name, str(value)])

    argv.extend(
        [
            "--gui-window-maximized",
            "1" if getattr(args, "gui_window_maximized", False) else "0",
        ]
    )
    argv.extend(["--gui-refresh-port", str(refresh_port)])
    return argv


def run_all(args):
    """Fuehrt das feste Ausgabeprofil fuer den Sammelbefehl ``all`` aus."""
    shared_run_id = get_run_id(command_name="all", run_id=args.run_id)
    args.run_id = shared_run_id

    steps = ["overview", "analysis", "heating", "cooling"]
    ensure_required_data(args, steps)

    variants = args.variants
    rooms = args.rooms if args.rooms is not None else ROOMS.copy()
    comfort_options = {
        "plot_single": False,
        "plot_overview": True,
        "analysis_individual": False,
        "analysis_overview": True,
    }
    year_separate_options = {
        "view": "year",
        "month": None,
        "week": None,
        "day": None,
        "series_layout": "separate",
    }
    bar_options = {
        "view": "bar",
        "month": None,
        "week": None,
        "day": None,
        "series_layout": "separate",
    }

    comfort_runtime_args = build_runtime_args(
        args,
        variants=variants,
        rooms=rooms,
        comfort_options=comfort_options,
    )
    load_single_args = build_runtime_args(
        args,
        variants=variants,
        rooms=rooms,
        heating_mode="single",
        heating_options=year_separate_options,
    )
    load_compare_args = build_runtime_args(
        args,
        variants=variants,
        rooms=rooms,
        heating_mode="compare",
        heating_options=year_separate_options,
    )
    load_bar_args = build_runtime_args(
        args,
        variants=variants,
        rooms=rooms,
        heating_mode="compare",
        heating_options=bar_options,
    )

    all_steps = [
        ("Comfort-Uebersicht", lambda: run_overview(comfort_runtime_args)),
        (
            "Analyse-Uebersicht",
            lambda: run_analysis(
                comfort_runtime_args,
                run_id=comfort_runtime_args.run_id,
                output_individual=False,
                output_overview=True,
            ),
        ),
        ("Heating Barplots", lambda: run_heating(load_bar_args)),
        ("Cooling Barplots", lambda: run_cooling(load_bar_args)),
        ("Heating Jahresplots single", lambda: run_heating(load_single_args)),
        ("Heating Jahresplots Raeume kombiniert", lambda: run_heating(load_compare_args)),
        ("Cooling Jahresplots single", lambda: run_cooling(load_single_args)),
        ("Cooling Jahresplots Raeume kombiniert", lambda: run_cooling(load_compare_args)),
    ]

    print("\n" + "=" * 70)
    print("ALL-PROFIL GESTARTET")
    print("=" * 70)
    print(f"Run-ID: {shared_run_id}")

    total_steps = len(all_steps)
    for index, (title, runner) in enumerate(all_steps, start=1):
        print(f"\nSchritt {index}/{total_steps}: {title}")
        print("-" * 70)
        runner()

    print("\n" + "=" * 70)
    print("ALL-PROFIL ABGESCHLOSSEN")
    print("=" * 70)


class PipelineGUI:
    """Grafische Oberflaeche fuer Pipeline-Auswahl und Ausfuehrung.

    Die Klasse verwaltet GUI-Zustand, Validierung und Protokollausgabe. Die
    eigentliche Arbeit wird an die Runner-Funktionen delegiert und in einem
    Hintergrundthread gestartet, damit das Fenster waehrend der Analyse
    bedienbar bleibt.
    """

    def __init__(self, root, args, singleton_controller=None, refresh_port=None):
        self.root = root
        self.args = args
        self.singleton_controller = singleton_controller
        self.refresh_port = refresh_port
        self.refresh_coordinator = None
        self.refresh_recovery_after_id = None
        self.is_refresh_shutdown = False
        self.custom_window_chrome_enabled = False

        self.root.title("ANALYSE TOOLS")
        self.root.minsize(1050, 650)

        self.color_bg = "#0f141a"
        self.color_panel = "#161b22"
        self.color_panel_light = "#1f2630"
        self.color_border = "#30363d"
        self.color_text = "#f0f3f6"
        self.color_muted = "#a9b1ba"
        self.color_blue = "#0078d4"
        self.color_blue_dark = "#005a9e"
        self.window_icon = None

        self._set_window_icon()

        self.command_to_steps = {
            "prepare": ["prepare"],
            "comfort": [],
            "analyze_data": ["analyze"],
            "heating": ["heating"],
            "cooling": ["cooling"],
            "all": ["overview", "analysis", "heating", "cooling"],
        }
        self.commands = list(self.command_to_steps.keys())
        initial_export_format = getattr(args, "export_format", "csv")

        self.analysis_scope = tk.StringVar(value="Alle Varianten")
        self.command = tk.StringVar(value="comfort")
        self.prepare_export_format = tk.StringVar(value=initial_export_format)
        self.comfort_type = tk.StringVar(value="plot")
        self.analysis_level = tk.StringVar(value="Analyse Raum")
        self.load_subcommand = tk.StringVar(value="")
        self.heating_mode = tk.StringVar(value="single")
        self.heating_view = tk.StringVar(value="year")
        self.heating_series_layout = tk.StringVar(value="separate")
        self.heating_month = tk.StringVar(value=MONTH_NAMES[0])
        self.heating_week = tk.StringVar(value="1")
        self.heating_day = tk.StringVar(value="1")

        self.selected_steps = []
        self.selected_variants = []
        self.selected_rooms = ROOMS.copy()
        self.selected_load_subcommand = ""
        self.selected_heating_mode = "single"
        self.selected_heating_view = "year"
        self.selected_heating_series_layout = "separate"
        self.selected_prepare_export_format = initial_export_format
        self.selected_month = MONTH_NAMES[0]
        self.selected_week = 1
        self.selected_day = 1
        self.selected_comfort_type = "plot"
        self.selected_plot_single = True
        self.selected_plot_overview = True
        self.selected_analysis_individual = True
        self.selected_analysis_overview = True

        self.comfort_allowed_by_level = {
            "Analyse Raum": {"plot", "plot_analysis"},
            "Analyse Variante": {"plot_overview", "plot_analysis_overview"},
        }
        self.comfort_default_by_level = {
            "Analyse Raum": "plot",
            "Analyse Variante": "plot_overview",
        }
        self.last_variant_scope = None

        self.variant_names = []
        self.variant_source_kind = None
        self.left_scroll_window = None
        self.right_scroll_window = None
        self.tools_menu = None
        self.mapping_dialog = None
        self.mapping_row_vars = {}
        self.mapping_table_frame = None
        self.mapping_doc_path = NAMENSMAPPING_DOC
        self.format_dialog = None
        self.format_row_vars = {}
        self.format_table_frame = None
        self.format_doc_path = ensure_output_format_doc(OUTPUT_FORMAT_DOC)
        self.log_card = None
        self.log_expand_button = None
        self.log_focus_frame = None
        self.expanded_log_text = None
        self.is_log_expanded = False
        self.bottom_button_frame = None
        self.run_log_text = None
        self.analysis_log_window = None
        self.analysis_log_text = None
        self.analysis_status_var = None
        self.pipeline_queue = None
        self.pipeline_thread = None
        self.pipeline_log_poll_after_id = None
        self.status_var = tk.StringVar(value="Bereit.")
        self.is_running_pipeline = False
        self.maximize_button = None
        self.title_frame = None
        self.title_label = None
        self.is_window_maximized = False
        self.is_minimizing_window = False
        self.normal_window_geometry = None
        self.drag_start_pointer_x = 0
        self.drag_start_pointer_y = 0
        self.drag_start_window_x = 0
        self.drag_start_window_y = 0

        self._setup_style()
        self._build_ui()
        self._populate_variants()
        self._populate_rooms()
        if self.singleton_controller is not None:
            self.singleton_controller.start_listener(self._handle_singleton_message)
        self.root.protocol("WM_DELETE_WINDOW", self._close_window)
        self.root.bind("<Configure>", self._on_window_configure, add="+")
        self.root.bind("<Map>", self._on_window_map, add="+")
        self._apply_initial_window_state()
        self.root.update_idletasks()
        self.normal_window_geometry = self._get_current_window_geometry()
        self._enable_custom_window_chrome()
        self._update_window_state_buttons()
        self._update_dynamic_fields()

    def _setup_style(self):
        self.root.configure(bg=self.color_bg)

        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Title.TLabel",
            background=self.color_bg,
            foreground=self.color_text,
            font=("Segoe UI", 18, "bold"),
        )
        style.configure(
            "Heading.TLabel",
            background=self.color_panel,
            foreground=self.color_text,
            font=("Segoe UI", 13, "bold"),
        )
        style.configure(
            "Dark.TLabel",
            background=self.color_panel,
            foreground=self.color_text,
            font=("Segoe UI", 10),
        )
        style.configure(
            "Muted.TLabel",
            background=self.color_panel,
            foreground=self.color_muted,
            font=("Segoe UI", 9),
        )
        style.configure(
            "TCombobox",
            fieldbackground=self.color_panel_light,
            background=self.color_panel_light,
            foreground=self.color_text,
            arrowcolor=self.color_text,
            bordercolor=self.color_border,
            lightcolor=self.color_border,
            darkcolor=self.color_border,
            font=("Segoe UI", 10),
        )

        style.map(
            "TCombobox",
            fieldbackground=[("readonly", self.color_panel_light)],
            foreground=[("readonly", self.color_text)],
        )
        style.configure(
            "TRadiobutton",
            background=self.color_panel,
            foreground=self.color_text,
            font=("Segoe UI", 10),
        )
        style.map(
            "TRadiobutton",
            background=[("active", self.color_panel)],
            foreground=[
                ("disabled", self.color_muted),
                ("active", self.color_text),
            ],
        )
        style.configure(
            "TCheckbutton",
            background=self.color_panel,
            foreground=self.color_text,
            font=("Segoe UI", 10),
        )
        style.map(
            "TCheckbutton",
            background=[("active", self.color_panel)],
            foreground=[("active", self.color_text)],
        )
        style.configure(
            "Primary.TButton",
            background=self.color_blue,
            foreground="white",
            font=("Segoe UI", 11, "bold"),
            padding=(18, 10),
            borderwidth=0,
        )
        style.map(
            "Primary.TButton",
            background=[("active", self.color_blue_dark)],
        )
        style.configure(
            "Secondary.TButton",
            background=self.color_panel_light,
            foreground=self.color_text,
            font=("Segoe UI", 11),
            padding=(18, 10),
            borderwidth=1,
        )
        style.map(
            "Secondary.TButton",
            background=[("active", self.color_border)],
        )
        style.layout(
            "Tool.Vertical.TScrollbar",
            [
                (
                    "Vertical.Scrollbar.trough",
                    {
                        "sticky": "ns",
                        "children": [
                            (
                                "Vertical.Scrollbar.thumb",
                                {"expand": "1", "sticky": "nswe"},
                            )
                        ],
                    },
                )
            ],
        )
        style.configure(
            "Tool.Vertical.TScrollbar",
            background="#2a313b",
            troughcolor=self.color_bg,
            bordercolor=self.color_bg,
            darkcolor="#2a313b",
            lightcolor="#2a313b",
            arrowcolor=self.color_bg,
            gripcount=0,
            relief="flat",
            borderwidth=0,
            width=8,
        )
        style.map(
            "Tool.Vertical.TScrollbar",
            background=[
                ("active", "#343c47"),
                ("pressed", "#3b4552"),
            ],
            troughcolor=[("active", self.color_bg)],
        )

    def _set_window_icon(self):
        icon_image = self._create_window_icon()
        if icon_image is None:
            return
        self.window_icon = icon_image
        with contextlib.suppress(tk.TclError):
            self.root.iconphoto(True, self.window_icon)

    def _create_window_icon(self):
        if tk is None:
            return None

        size = 32
        image = tk.PhotoImage(width=size, height=size)
        image.put(self.color_bg, to=(0, 0, size, size))

        border_color = self.color_border
        axis_color = self.color_text
        bar_colors = [self.color_blue, "#2a9d8f", "#f77f00", "#d62828"]

        image.put(border_color, to=(3, 3, 29, 5))
        image.put(border_color, to=(3, 27, 29, 29))
        image.put(border_color, to=(3, 3, 5, 29))
        image.put(border_color, to=(27, 3, 29, 29))
        image.put(axis_color, to=(8, 23, 25, 25))
        image.put(axis_color, to=(8, 9, 10, 25))

        bars = [
            (12, 17, 15, 23, bar_colors[0]),
            (16, 13, 19, 23, bar_colors[1]),
            (20, 10, 23, 23, bar_colors[2]),
            (24, 15, 26, 23, bar_colors[3]),
        ]
        for x0, y0, x1, y1, color in bars:
            image.put(color, to=(x0, y0, x1, y1))

        return image

    def _update_left_scroll_region(self, _event=None):
        self.left_scroll_canvas.configure(scrollregion=self.left_scroll_canvas.bbox("all"))

    def _sync_left_scroll_width(self, event):
        self.left_scroll_canvas.itemconfigure(self.left_scroll_window, width=event.width)

    def _update_right_scroll_region(self, _event=None):
        self.right_scroll_canvas.configure(scrollregion=self.right_scroll_canvas.bbox("all"))

    def _sync_right_scroll_width(self, event):
        self.right_scroll_canvas.itemconfigure(self.right_scroll_window, width=event.width)

    def _should_skip_mousewheel(self, widget):
        widget_class = widget.winfo_class()
        return widget_class in {"Listbox", "Text", "Entry", "TCombobox", "Combobox"}

    def _widget_is_in_left_scroll_area(self, widget):
        current = widget
        while current is not None:
            if current == self.left_scroll_host:
                return True
            parent_name = current.winfo_parent()
            if not parent_name:
                break
            current = current.nametowidget(parent_name)
        return False

    def _widget_is_in_right_scroll_area(self, widget):
        current = widget
        while current is not None:
            if current == self.right_column:
                return True
            parent_name = current.winfo_parent()
            if not parent_name:
                break
            current = current.nametowidget(parent_name)
        return False

    def _on_mousewheel(self, event):
        if self._should_skip_mousewheel(event.widget):
            return
        delta = int(-event.delta / 120)
        if delta == 0:
            return
        if self._widget_is_in_right_scroll_area(event.widget):
            self.right_scroll_canvas.yview_scroll(delta, "units")
            return
        if self._widget_is_in_left_scroll_area(event.widget):
            self.left_scroll_canvas.yview_scroll(delta, "units")

    def _on_mousewheel_linux_up(self, event):
        if self._should_skip_mousewheel(event.widget):
            return
        if self._widget_is_in_right_scroll_area(event.widget):
            self.right_scroll_canvas.yview_scroll(-1, "units")
            return
        if self._widget_is_in_left_scroll_area(event.widget):
            self.left_scroll_canvas.yview_scroll(-1, "units")

    def _on_mousewheel_linux_down(self, event):
        if self._should_skip_mousewheel(event.widget):
            return
        if self._widget_is_in_right_scroll_area(event.widget):
            self.right_scroll_canvas.yview_scroll(1, "units")
            return
        if self._widget_is_in_left_scroll_area(event.widget):
            self.left_scroll_canvas.yview_scroll(1, "units")

    def _build_ui(self):
        self._build_title()
        self._build_main_layout()
        self._build_left_column()
        self._build_right_column()
        self._build_bottom_buttons()

    def _build_title(self):
        self.title_frame = tk.Frame(self.root, bg=self.color_bg)
        self.title_frame.pack(fill=tk.X, padx=22, pady=(18, 8))

        title_left_frame = tk.Frame(self.title_frame, bg=self.color_bg)
        title_left_frame.pack(side=tk.LEFT)

        title_icon_label = tk.Label(
            title_left_frame,
            text="📊",
            bg=self.color_bg,
            fg=self.color_text,
            font=("Segoe UI Emoji", 18),
        )
        title_icon_label.pack(side=tk.LEFT, padx=(0, 10))

        self.title_label = ttk.Label(title_left_frame, text="ANALYSE TOOLS", style="Title.TLabel")
        self.title_label.pack(side=tk.LEFT)

        actions_frame = tk.Frame(self.title_frame, bg=self.color_bg)
        actions_frame.pack(side=tk.RIGHT)

        self.more_button = tk.Label(
            actions_frame,
            text="•••",
            bg=self.color_bg,
            fg=self.color_text,
            font=("Segoe UI", 18, "bold"),
            cursor="hand2",
        )
        self.more_button.pack(side=tk.LEFT, padx=(0, 16))
        self.more_button.bind("<Button-1>", self._open_tools_menu)

        minimize_label = tk.Label(
            actions_frame,
            text="-",
            bg=self.color_bg,
            fg=self.color_text,
            font=("Segoe UI", 18, "bold"),
            cursor="hand2",
        )
        minimize_label.pack(side=tk.LEFT, padx=(0, 16))
        minimize_label.bind("<Button-1>", lambda event: self._minimize_window())

        self.maximize_button = tk.Label(
            actions_frame,
            text="□",
            bg=self.color_bg,
            fg=self.color_text,
            font=("Segoe UI", 16, "bold"),
            cursor="hand2",
        )
        self.maximize_button.pack(side=tk.LEFT, padx=(0, 16))
        self.maximize_button.bind("<Button-1>", lambda event: self._toggle_maximize_window())

        close_label = tk.Label(
            actions_frame,
            text="X",
            bg=self.color_bg,
            fg=self.color_text,
            font=("Segoe UI", 18, "bold"),
            cursor="hand2",
        )
        close_label.pack(side=tk.LEFT)
        close_label.bind("<Button-1>", lambda event: self._close_window())

        for widget in (self.title_frame, title_left_frame, title_icon_label, self.title_label):
            widget.bind("<ButtonPress-1>", self._start_window_drag, add="+")
            widget.bind("<B1-Motion>", self._drag_window, add="+")
            widget.bind("<Double-Button-1>", lambda event: self._toggle_maximize_window(), add="+")

    def _open_tools_menu(self, event=None):
        if self.tools_menu is None:
            self.tools_menu = tk.Menu(
                self.root,
                tearoff=0,
                bg=self.color_panel_light,
                fg=self.color_text,
                activebackground=self.color_blue,
                activeforeground="white",
                relief=tk.FLAT,
            )
            self.tools_menu.add_command(label="Format", command=self._open_output_format_dialog)
            self.tools_menu.add_command(label="Namensmapping", command=self._open_name_mapping_dialog)
            self.tools_menu.add_command(label="GUI aktualisieren", command=self._restart_gui)

        x_pos = self.more_button.winfo_rootx()
        y_pos = self.more_button.winfo_rooty() + self.more_button.winfo_height()
        self._safe_popup_menu(self.tools_menu, x_pos, y_pos)

    def _handle_singleton_message(self, payload):
        if payload == "FOCUS":
            self.root.after(0, self._focus_window)
            return "FOCUSED"
        if payload == "REPLACE_WITH_NEW":
            if self.singleton_controller is not None:
                self.singleton_controller.stop()
            self.root.after(0, self._close_for_new_gui_invocation)
            return "RELEASING"
        return "IGNORED"

    def _on_window_configure(self, _event=None):
        if self.root.winfo_exists() and not self.is_window_maximized:
            with contextlib.suppress(tk.TclError):
                if self.root.state() != "iconic":
                    self.normal_window_geometry = self._get_current_window_geometry()
        self._update_window_state_buttons()

    def _on_window_map(self, _event=None):
        if self.root.winfo_exists():
            with contextlib.suppress(tk.TclError):
                if self.root.state() == "iconic":
                    return
            delay_ms = 80 if self.is_minimizing_window else 30
            self.root.after(delay_ms, self._restore_custom_window_chrome_after_show)

    def _update_window_state_buttons(self):
        if self.maximize_button is None or not self.root.winfo_exists():
            return
        self.maximize_button.configure(text="❐" if self.is_window_maximized else "□")

    def _apply_initial_window_state(self):
        restored_geometry = self._extract_refresh_window_geometry()
        if restored_geometry is not None:
            self._apply_window_geometry(restored_geometry)
            self.normal_window_geometry = restored_geometry.copy()
            self.is_window_maximized = bool(getattr(self.args, "gui_window_maximized", False))
            if self.is_window_maximized:
                self._apply_window_geometry(self._get_current_monitor_work_area_geometry())
            return

        self.root.geometry("1250x720")
        self.is_window_maximized = False

    def _extract_refresh_window_geometry(self):
        geometry_keys = ("gui_window_x", "gui_window_y", "gui_window_width", "gui_window_height")
        values = {key: getattr(self.args, key, None) for key in geometry_keys}
        if any(value is None for value in values.values()):
            return None

        return {
            "x": int(values["gui_window_x"]),
            "y": int(values["gui_window_y"]),
            "width": int(values["gui_window_width"]),
            "height": int(values["gui_window_height"]),
        }

    def _get_current_window_geometry(self):
        self.root.update_idletasks()
        return {
            "x": self.root.winfo_x(),
            "y": self.root.winfo_y(),
            "width": self.root.winfo_width(),
            "height": self.root.winfo_height(),
        }

    def _apply_window_geometry(self, geometry):
        self.root.geometry(f"{geometry['width']}x{geometry['height']}+{geometry['x']}+{geometry['y']}")

    def _get_current_monitor_work_area_geometry(self):
        if os.name == "nt" and self.root.winfo_exists():

            class RECT(ctypes.Structure):
                _fields_ = [
                    ("left", ctypes.c_long),
                    ("top", ctypes.c_long),
                    ("right", ctypes.c_long),
                    ("bottom", ctypes.c_long),
                ]

            class MONITORINFO(ctypes.Structure):
                _fields_ = [
                    ("cbSize", ctypes.c_ulong),
                    ("rcMonitor", RECT),
                    ("rcWork", RECT),
                    ("dwFlags", ctypes.c_ulong),
                ]

            monitor_default_to_nearest = 2
            monitor_handle = ctypes.windll.user32.MonitorFromWindow(
                ctypes.c_void_p(self.root.winfo_id()),
                monitor_default_to_nearest,
            )
            if monitor_handle:
                monitor_info = MONITORINFO()
                monitor_info.cbSize = ctypes.sizeof(MONITORINFO)
                if ctypes.windll.user32.GetMonitorInfoW(
                    ctypes.c_void_p(monitor_handle),
                    ctypes.byref(monitor_info),
                ):
                    work_area = monitor_info.rcWork
                    return {
                        "x": work_area.left,
                        "y": work_area.top,
                        "width": work_area.right - work_area.left,
                        "height": work_area.bottom - work_area.top,
                    }

        return self._get_work_area_geometry()

    def _get_work_area_geometry(self):
        if os.name == "nt":

            class RECT(ctypes.Structure):
                _fields_ = [
                    ("left", ctypes.c_long),
                    ("top", ctypes.c_long),
                    ("right", ctypes.c_long),
                    ("bottom", ctypes.c_long),
                ]

            rect = RECT()
            if ctypes.windll.user32.SystemParametersInfoW(48, 0, ctypes.byref(rect), 0):
                return {
                    "x": rect.left,
                    "y": rect.top,
                    "width": rect.right - rect.left,
                    "height": rect.bottom - rect.top,
                }

        return {
            "x": 0,
            "y": 0,
            "width": self.root.winfo_screenwidth(),
            "height": self.root.winfo_screenheight(),
        }

    def _enable_custom_window_chrome(self):
        if not self.root.winfo_exists() or self.custom_window_chrome_enabled:
            return
        with contextlib.suppress(tk.TclError):
            self.root.overrideredirect(True)
            self.custom_window_chrome_enabled = True

    def _disable_custom_window_chrome(self):
        if not self.root.winfo_exists() or not self.custom_window_chrome_enabled:
            return
        with contextlib.suppress(tk.TclError):
            self.root.overrideredirect(False)
            self.custom_window_chrome_enabled = False

    def _restore_custom_window_chrome_after_show(self):
        if not self.root.winfo_exists():
            return
        with contextlib.suppress(tk.TclError):
            if self.root.state() == "iconic":
                return
        self.is_minimizing_window = False
        self._enable_custom_window_chrome()
        if self.is_window_maximized:
            self._apply_window_geometry(self._get_current_monitor_work_area_geometry())
        self._update_window_state_buttons()

    def _start_window_drag(self, event):
        if self.is_window_maximized:
            return
        self.drag_start_pointer_x = event.x_root
        self.drag_start_pointer_y = event.y_root
        self.drag_start_window_x = self.root.winfo_x()
        self.drag_start_window_y = self.root.winfo_y()

    def _drag_window(self, event):
        if self.is_window_maximized:
            return
        offset_x = event.x_root - self.drag_start_pointer_x
        offset_y = event.y_root - self.drag_start_pointer_y
        self.root.geometry(f"+{self.drag_start_window_x + offset_x}+{self.drag_start_window_y + offset_y}")

    def _focus_window(self):
        if not self.root.winfo_exists():
            return
        self._disable_custom_window_chrome()
        self.root.deiconify()
        self.root.lift()
        with contextlib.suppress(tk.TclError):
            self.root.attributes("-topmost", True)
            self.root.after(120, lambda: self.root.attributes("-topmost", False))
        with contextlib.suppress(tk.TclError):
            self.root.focus_force()
        self.root.after(30, self._restore_custom_window_chrome_after_show)

    def _minimize_window(self):
        if not self.root.winfo_exists():
            return

        self.is_minimizing_window = True
        self._disable_custom_window_chrome()
        self.root.update_idletasks()

        def finish_minimize():
            if not self.root.winfo_exists():
                return
            with contextlib.suppress(tk.TclError):
                self.root.iconify()
            self._update_window_state_buttons()
            self.root.after(250, self._finish_minimize_window)

        self.root.after_idle(finish_minimize)

    def _finish_minimize_window(self):
        if not self.root.winfo_exists():
            return
        with contextlib.suppress(tk.TclError):
            if self.root.state() == "iconic":
                return
        self.is_minimizing_window = False
        self._restore_custom_window_chrome_after_show()

    def _toggle_maximize_window(self):
        if not self.root.winfo_exists():
            return
        if self.is_window_maximized:
            self.is_window_maximized = False
            if self.normal_window_geometry is not None:
                self._apply_window_geometry(self.normal_window_geometry)
        else:
            self.normal_window_geometry = self._get_current_window_geometry()
            self.is_window_maximized = True
            self._apply_window_geometry(self._get_current_monitor_work_area_geometry())
        self._update_window_state_buttons()

    def _close_window(self):
        if self.mapping_dialog is not None and self.mapping_dialog.winfo_exists():
            self.mapping_dialog.destroy()
            self.mapping_dialog = None
        if self.refresh_recovery_after_id is not None:
            with contextlib.suppress(Exception):
                self.root.after_cancel(self.refresh_recovery_after_id)
            self.refresh_recovery_after_id = None
        if self.refresh_coordinator is not None:
            self.refresh_coordinator.close()
            self.refresh_coordinator = None
        if self.singleton_controller is not None:
            self.singleton_controller.stop()
        self.root.unbind_all("<MouseWheel>")
        self.root.unbind_all("<Button-4>")
        self.root.unbind_all("<Button-5>")
        if self.root.winfo_exists():
            self.root.quit()
            self.root.destroy()

    def _close_for_new_gui_invocation(self):
        if not self.root.winfo_exists():
            return
        self._set_status("Neuer GUI-Aufruf uebernimmt. Diese Instanz wird geschlossen.")
        if self.run_log_text is not None:
            self._append_log("Neuer GUI-Aufruf priorisiert. Alte Instanz wird geschlossen.")
        self.root.after(80, self._close_window)

    def _restart_gui(self):
        if self.is_running_pipeline:
            messagebox.showwarning(
                "GUI aktualisieren",
                "Bitte warten Sie, bis der laufende Befehl abgeschlossen ist.",
                parent=self.root,
            )
            return

        if self.refresh_coordinator is not None:
            return

        self.refresh_coordinator = GuiRefreshCoordinator(self)
        refresh_port = self.refresh_coordinator.start()
        window_geometry = (
            self.normal_window_geometry.copy()
            if self.is_window_maximized and self.normal_window_geometry is not None
            else self._get_current_window_geometry()
        )
        self.args.gui_window_geometry = window_geometry
        self.args.gui_window_maximized = self.is_window_maximized
        argv = build_gui_restart_argv(self.args, refresh_port)
        try:
            subprocess.Popen(argv, cwd=os.getcwd())
        except Exception as exc:
            self.refresh_coordinator.close()
            self.refresh_coordinator = None
            messagebox.showerror(
                "GUI aktualisieren",
                f"Die neue GUI konnte nicht gestartet werden:\n{exc}",
                parent=self.root,
            )
            return

        self._set_status("GUI-Aktualisierung gestartet. Neue Instanz wird vorbereitet.")
        self._append_log("GUI-Aktualisierung gestartet. Warte auf Uebergabe an neue Instanz.")

    def _release_singleton_for_refresh(self):
        if self.refresh_coordinator is None or self.singleton_controller is None:
            return
        self.singleton_controller.stop()
        self.refresh_coordinator.mark_released()
        self._set_status("GUI-Refresh: Singleton freigegeben, warte auf neue Instanz.")

    def _schedule_refresh_timeout_recovery(self):
        if self.refresh_recovery_after_id is not None:
            with contextlib.suppress(Exception):
                self.root.after_cancel(self.refresh_recovery_after_id)
        self.refresh_recovery_after_id = self.root.after(
            GUI_REFRESH_TIMEOUT_SECONDS * 1000,
            self._recover_from_refresh_timeout,
        )

    def _recover_from_refresh_timeout(self):
        if self.is_refresh_shutdown or self.refresh_coordinator is None or self.refresh_coordinator.completed:
            return
        self._append_log(
            "GUI-Aktualisierung wurde nicht abgeschlossen. Die bestehende GUI uebernimmt wieder die Kontrolle."
        )
        self._set_status("GUI-Aktualisierung fehlgeschlagen. Bestehende GUI bleibt aktiv.")
        if self.singleton_controller is not None and self.singleton_controller.acquire():
            self.singleton_controller.start_listener(self._handle_singleton_message)
        if self.refresh_coordinator is not None:
            self.refresh_coordinator.close()
            self.refresh_coordinator = None
        self.refresh_recovery_after_id = None

    def _finalize_refresh_shutdown(self):
        self.is_refresh_shutdown = True
        if self.refresh_coordinator is not None:
            self.refresh_coordinator.close()
            self.refresh_coordinator = None
        self._close_window()

    def _build_main_layout(self):
        self.main_frame = tk.Frame(self.root, bg=self.color_bg)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=22, pady=10)

        self.left_scroll_host = tk.Frame(self.main_frame, bg=self.color_bg)
        self.left_scroll_host.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 12))

        self.left_scroll_canvas = tk.Canvas(
            self.left_scroll_host,
            bg=self.color_bg,
            highlightthickness=0,
            bd=0,
        )
        self.left_scroll_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.left_scrollbar = ttk.Scrollbar(
            self.left_scroll_host,
            orient=tk.VERTICAL,
            command=self.left_scroll_canvas.yview,
            style="Tool.Vertical.TScrollbar",
        )
        self.left_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.left_scroll_canvas.configure(yscrollcommand=self.left_scrollbar.set)

        self.left_column = tk.Frame(self.left_scroll_canvas, bg=self.color_bg)
        self.left_scroll_window = self.left_scroll_canvas.create_window(
            (0, 0),
            window=self.left_column,
            anchor="nw",
        )

        self.left_column.bind("<Configure>", self._update_left_scroll_region)
        self.left_scroll_canvas.bind("<Configure>", self._sync_left_scroll_width)

        self.right_column = tk.Frame(self.main_frame, bg=self.color_bg, width=430)
        self.right_column.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(12, 0))
        self.right_column.pack_propagate(False)

        self.right_scroll_canvas = tk.Canvas(
            self.right_column,
            bg=self.color_bg,
            highlightthickness=0,
            bd=0,
        )
        self.right_scroll_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.right_scrollbar = ttk.Scrollbar(
            self.right_column,
            orient=tk.VERTICAL,
            command=self.right_scroll_canvas.yview,
            style="Tool.Vertical.TScrollbar",
        )
        self.right_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.right_scroll_canvas.configure(yscrollcommand=self.right_scrollbar.set)

        self.right_content = tk.Frame(self.right_scroll_canvas, bg=self.color_bg)
        self.right_scroll_window = self.right_scroll_canvas.create_window(
            (0, 0),
            window=self.right_content,
            anchor="nw",
        )

        self.right_content.bind("<Configure>", self._update_right_scroll_region)
        self.right_scroll_canvas.bind("<Configure>", self._sync_right_scroll_width)

        self.root.bind_all("<MouseWheel>", self._on_mousewheel, add="+")
        self.root.bind_all("<Button-4>", self._on_mousewheel_linux_up, add="+")
        self.root.bind_all("<Button-5>", self._on_mousewheel_linux_down, add="+")

    def _create_step_card(self, parent, number, title):
        card = tk.Frame(
            parent,
            bg=self.color_panel,
            highlightbackground=self.color_border,
            highlightthickness=1,
        )
        card.pack(fill=tk.X, pady=6)

        header = tk.Frame(card, bg=self.color_panel)
        header.pack(fill=tk.X, padx=18, pady=(14, 8))

        number_label = tk.Label(
            header,
            text=str(number),
            bg=self.color_blue,
            fg="white",
            width=3,
            height=1,
            font=("Segoe UI", 12, "bold"),
        )
        number_label.pack(side=tk.LEFT, padx=(0, 12))

        heading = ttk.Label(header, text=title, style="Heading.TLabel")
        heading.pack(side=tk.LEFT)

        content = tk.Frame(card, bg=self.color_panel)
        content.pack(fill=tk.X, padx=18, pady=(0, 16))
        card.step_header = header
        card.step_number_label = number_label
        card.step_heading = heading
        card.step_title = title
        return card, content

    def _build_left_column(self):
        self._build_step_2()
        self._build_subcommand_step()
        self._build_prepare_export_step()
        self._build_step_3()
        self._build_step_1()
        self._build_step_4()
        self._build_step_5()
        self.step_card_order = [
            self.step_2_card,
            self.subcommand_card,
            self.prepare_export_card,
            self.step_3_card,
            self.step_1_card,
            self.step_4_card,
            self.step_5_card,
        ]
        self.step_card_descriptions = {
            self.step_2_card: "Befehl festlegen",
            self.subcommand_card: "Unterbefehl passend zum Befehl waehlen",
            self.prepare_export_card: "Exportformat fuer prepare waehlen",
            self.step_3_card: "Befehlsabhaengige Optionen pruefen",
            self.step_1_card: "Analyseumfang waehlen",
            self.step_4_card: "Varianten passend zum Befehl auswaehlen",
            self.step_5_card: "Raeume auswaehlen oder automatisch uebernehmen",
        }

    def _build_step_1(self):
        self.step_1_card, content = self._create_step_card(self.left_column, 5, "Analyseumfang")

        button_frame = tk.Frame(content, bg=self.color_panel)
        button_frame.pack(fill=tk.X)

        self.scope_buttons = {}
        for scope in ["Eine Variante", "Mehrere Varianten", "Alle Varianten"]:
            button = tk.Button(
                button_frame,
                text=scope,
                command=lambda value=scope: self._set_analysis_scope(value),
                bg=self.color_panel_light,
                fg=self.color_text,
                activebackground=self.color_blue_dark,
                activeforeground="white",
                relief=tk.FLAT,
                font=("Segoe UI", 10),
                padx=18,
                pady=10,
            )
            button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=1)
            self.scope_buttons[scope] = button

    def _build_step_2(self):
        self.step_2_card, content = self._create_step_card(self.left_column, 1, "Befehl")

        ttk.Label(content, text="Befehl auswaehlen", style="Dark.TLabel").pack(anchor=tk.W, pady=(0, 6))
        self.command_buttons = {}
        button_frame = tk.Frame(content, bg=self.color_panel)
        button_frame.pack(fill=tk.X)

        for command_name in self.commands:
            button = tk.Button(
                button_frame,
                text=command_name,
                command=lambda value=command_name: self._set_command(value),
                bg=self.color_panel_light,
                fg=self.color_text,
                activebackground=self.color_blue_dark,
                activeforeground="white",
                relief=tk.FLAT,
                font=("Segoe UI", 10),
                anchor=tk.W,
                padx=18,
                pady=10,
            )
            button.pack(fill=tk.X, pady=1)
            self.command_buttons[command_name] = button

    def _build_subcommand_step(self):
        self.subcommand_card, content = self._create_step_card(self.left_column, 2, "Unterbefehle")

        self.comfort_section = tk.Frame(content, bg=self.color_panel)
        ttk.Label(self.comfort_section, text="Comfort Unterbefehle", style="Dark.TLabel").pack(anchor=tk.W, pady=(0, 6))
        _, self.comfort_type_widgets = self._create_selection_button_group(
            self.comfort_section,
            [
                ("plot", "plot"),
                ("plot_analysis", "plot_analysis"),
                ("plot_overview", "plot_overview"),
                ("plot_analysis_overview", "plot_analysis_overview"),
            ],
            self._set_comfort_type,
        )

        self.load_subcommand_section = tk.Frame(content, bg=self.color_panel)
        self.load_subcommand_title = ttk.Label(
            self.load_subcommand_section,
            text="Unterbefehl",
            style="Dark.TLabel",
        )
        self.load_subcommand_title.pack(anchor=tk.W, pady=(0, 6))
        _, self.load_subcommand_buttons = self._create_selection_button_group(
            self.load_subcommand_section,
            [
                ("bar", "bar"),
                ("timeline", "timeline"),
            ],
            self._set_load_subcommand,
        )
        self.load_subcommand_note = ttk.Label(
            self.load_subcommand_section,
            text="bar erzeugt Maximalwertdiagramme. timeline aktiviert die Zeitansichten.",
            style="Muted.TLabel",
            wraplength=640,
            justify=tk.LEFT,
        )
        self.load_subcommand_note.pack(anchor=tk.W, pady=(6, 0))

    def _build_prepare_export_step(self):
        self.prepare_export_card, content = self._create_step_card(self.left_column, 3, "Exportformat")

        button_frame = tk.Frame(content, bg=self.color_panel)
        button_frame.pack(fill=tk.X)
        self.prepare_export_buttons = {}
        export_options = [
            ("csv", "csv"),
            ("excel", "excel"),
            ("both", "both"),
        ]
        for value, label in export_options:
            button = tk.Button(
                button_frame,
                text=label,
                command=lambda selected=value: self._set_prepare_export_format(selected),
                bg=self.color_panel_light,
                fg=self.color_text,
                activebackground=self.color_blue_dark,
                activeforeground="white",
                relief=tk.FLAT,
                font=("Segoe UI", 10),
                padx=18,
                pady=10,
            )
            button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=1)
            self.prepare_export_buttons[value] = button

        self.prepare_export_note = ttk.Label(
            content,
            text="CSV ist das operative Standardformat fuer die Folgeskripte.",
            style="Muted.TLabel",
            wraplength=640,
            justify=tk.LEFT,
        )
        self.prepare_export_note.pack(anchor=tk.W, pady=(10, 0))

    def _create_selection_button_group(self, parent, options, command, columns=2, wraplength=240):
        """Erzeugt eine Einzelauswahl als Button-Raster mit festem 2-Spalten-Muster."""
        frame = tk.Frame(parent, bg=self.color_panel)
        frame.pack(fill=tk.X)

        for column in range(columns):
            frame.grid_columnconfigure(column, weight=1)

        buttons = {}
        for index, (value, label) in enumerate(options):
            button = tk.Button(
                frame,
                text=label,
                command=lambda selected=value: command(selected),
                bg=self.color_panel_light,
                fg=self.color_text,
                activebackground=self.color_blue_dark,
                activeforeground="white",
                disabledforeground=self.color_muted,
                relief=tk.FLAT,
                font=("Segoe UI", 10),
                justify=tk.CENTER,
                wraplength=wraplength,
                padx=18,
                pady=10,
            )
            button.grid(
                row=index // columns,
                column=index % columns,
                sticky="ew",
                padx=1,
                pady=1,
            )
            buttons[value] = button

        return frame, buttons

    def _enable_dynamic_button_group_height(self, frame, buttons, columns=2):
        """Laesst ein Button-Raster vertikal mit seinem Container mitwachsen."""
        if not buttons:
            return

        row_count = (len(buttons) + columns - 1) // columns
        for row in range(row_count):
            frame.grid_rowconfigure(row, weight=1, uniform="dynamic_button_rows")

        for button in buttons.values():
            button.grid_configure(sticky="nsew")

    def _build_step_3(self):
        self.step_3_card, content = self._create_step_card(self.left_column, 4, "Analyseebene und Befehlsoptionen")

        self.heating_mode_section = tk.Frame(content, bg=self.color_panel)
        self.load_mode_title = ttk.Label(self.heating_mode_section, text="Heizvergleich Modus", style="Dark.TLabel")
        self.load_mode_title.pack(anchor=tk.W, pady=(0, 6))
        _, self.heating_mode_buttons = self._create_selection_button_group(
            self.heating_mode_section,
            [
                ("single", "single"),
                ("compare", "compare"),
            ],
            self._set_heating_mode,
        )

        self.heating_note = ttk.Label(
            self.heating_mode_section,
            text="single erzeugt getrennte Ausgaben. compare fasst mehrere Datenreihen oder Varianten in einer Ausgabe zusammen.",
            style="Muted.TLabel",
            wraplength=640,
            justify=tk.LEFT,
        )
        self.heating_note.pack(anchor=tk.W, pady=(6, 0))

        self.heating_layout_section = tk.Frame(content, bg=self.color_panel)
        self.heating_layout_title = ttk.Label(self.heating_layout_section, text="Diagrammausgabe", style="Dark.TLabel")
        self.heating_layout_title.pack(anchor=tk.W, pady=(0, 6))
        _, self.heating_layout_buttons = self._create_selection_button_group(
            self.heating_layout_section,
            [
                ("separate", "separate"),
                ("combined", "combined"),
            ],
            self._set_heating_series_layout,
        )
        self.heating_layout_note = ttk.Label(
            self.heating_layout_section,
            text="Waehlt, ob mehrere Linien gemeinsam oder einzeln dargestellt werden sollen.",
            style="Muted.TLabel",
            wraplength=640,
            justify=tk.LEFT,
        )
        self.heating_layout_note.pack(anchor=tk.W, pady=(6, 0))

        self.analysis_section = tk.Frame(content, bg=self.color_panel)
        ttk.Label(self.analysis_section, text="Analyseebene", style="Dark.TLabel").pack(anchor=tk.W, pady=(0, 6))
        _, self.analysis_level_buttons = self._create_selection_button_group(
            self.analysis_section,
            [
                ("Analyse Raum", "Analyse Raum"),
                ("Analyse Variante", "Analyse Variante"),
            ],
            self._set_analysis_level,
        )
        self.analysis_note = ttk.Label(
            self.analysis_section,
            text="Steuert, ob die Auswertung raumbezogen oder variantenbezogen arbeitet.",
            style="Muted.TLabel",
            wraplength=640,
            justify=tk.LEFT,
        )
        self.analysis_note.pack(anchor=tk.W, pady=(6, 0))

        self.heating_view_section = tk.Frame(content, bg=self.color_panel)
        self.load_view_title = ttk.Label(self.heating_view_section, text="Heizvergleich Ansichten", style="Dark.TLabel")
        self.load_view_title.pack(anchor=tk.W, pady=(0, 6))
        self.heating_time_view_section = tk.Frame(self.heating_view_section, bg=self.color_panel)
        self.heating_time_view_section.pack(fill=tk.BOTH, expand=True)
        ttk.Label(self.heating_time_view_section, text="Zeitansichten", style="Dark.TLabel").pack(
            anchor=tk.W, pady=(0, 6)
        )

        self.heating_time_view_layout = tk.Frame(self.heating_time_view_section, bg=self.color_panel)
        self.heating_time_view_layout.pack(fill=tk.BOTH, expand=True)

        self.heating_time_view_buttons_section = tk.Frame(self.heating_time_view_layout, bg=self.color_panel)
        self.heating_time_view_buttons_section.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 20))
        self.heating_view_button_group_frame, self.heating_view_buttons = self._create_selection_button_group(
            self.heating_time_view_buttons_section,
            [
                ("year", "year"),
                ("month", "month"),
                ("week", "week"),
                ("day", "day"),
            ],
            self._set_heating_view,
        )
        self._enable_dynamic_button_group_height(
            self.heating_view_button_group_frame,
            self.heating_view_buttons,
        )
        self.heating_view_button_group_frame.pack(fill=tk.BOTH, expand=True)

        self.heating_view_detail_section = tk.Frame(self.heating_time_view_layout, bg=self.color_panel)
        self.heating_view_detail_section.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.heating_view_detail_title = ttk.Label(
            self.heating_view_detail_section,
            text="Detailauswahl",
            style="Dark.TLabel",
        )
        self.heating_view_detail_title.pack(anchor=tk.W, pady=(0, 6))

        self.heating_view_note = ttk.Label(
            self.heating_view_detail_section,
            text="Keine Zusatzangaben fuer die aktuelle Heizansicht erforderlich.",
            style="Muted.TLabel",
            wraplength=320,
            justify=tk.LEFT,
        )
        self.heating_view_note.pack(anchor=tk.W, pady=(0, 8))

        self.heating_month_container = tk.Frame(self.heating_view_detail_section, bg=self.color_panel)
        self.heating_month_label = ttk.Label(self.heating_month_container, text="Monat", style="Dark.TLabel")
        self.heating_month_label.pack(anchor=tk.W, pady=(0, 4))
        self.heating_month_combo = ttk.Combobox(
            self.heating_month_container,
            textvariable=self.heating_month,
            values=MONTH_NAMES,
            state="readonly",
        )
        self.heating_month_combo.pack(fill=tk.X)
        self.heating_month_combo.bind("<<ComboboxSelected>>", lambda event: self._update_dynamic_fields())

        self.heating_week_container = tk.Frame(self.heating_view_detail_section, bg=self.color_panel)
        self.heating_week_label = ttk.Label(self.heating_week_container, text="Kalenderwoche", style="Dark.TLabel")
        self.heating_week_label.pack(anchor=tk.W, pady=(0, 4))
        self.heating_week_entry = tk.Entry(
            self.heating_week_container,
            textvariable=self.heating_week,
            bg=self.color_panel_light,
            fg=self.color_text,
            insertbackground=self.color_text,
            relief=tk.FLAT,
            highlightbackground=self.color_border,
            highlightcolor=self.color_blue,
            font=("Segoe UI", 10),
        )
        self.heating_week_entry.pack(fill=tk.X)

        self.heating_day_container = tk.Frame(self.heating_view_detail_section, bg=self.color_panel)
        self.heating_day_label = ttk.Label(self.heating_day_container, text="Tag", style="Dark.TLabel")
        self.heating_day_label.pack(anchor=tk.W, pady=(0, 4))
        self.heating_day_combo = ttk.Combobox(
            self.heating_day_container,
            textvariable=self.heating_day,
            state="readonly",
        )
        self.heating_day_combo.pack(fill=tk.X)
        self.heating_day_combo.bind("<<ComboboxSelected>>", lambda event: self._update_dynamic_fields())

    def _build_step_4(self):
        self.step_4_card, content = self._create_step_card(self.left_column, 6, "Varianten")

        left = tk.Frame(content, bg=self.color_panel)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 20))

        right = tk.Frame(content, bg=self.color_panel)
        right.pack(side=tk.RIGHT, fill=tk.X, expand=True)

        self.variants_listbox = tk.Listbox(
            left,
            height=6,
            selectmode=tk.MULTIPLE,
            bg=self.color_panel_light,
            fg=self.color_text,
            selectbackground=self.color_blue,
            selectforeground="white",
            highlightbackground=self.color_border,
            highlightcolor=self.color_blue,
            relief=tk.FLAT,
            exportselection=False,
            font=("Segoe UI", 10),
        )
        self.variants_listbox.pack(fill=tk.BOTH, expand=True)
        self.variants_listbox.bind(
            "<<ListboxSelect>>", lambda event: self._update_variant_note_state(self.analysis_scope.get())
        )

        self.variant_note = ttk.Label(
            right,
            text="Es ist aktuell keine Variante ausgewaehlt. Bitte waehlen Sie mindestens eine Variante.",
            style="Muted.TLabel",
            wraplength=330,
        )
        self.variant_note.pack(anchor=tk.W)

    def _build_step_5(self):
        self.step_5_card, content = self._create_step_card(self.left_column, 7, "Raeume")

        self.step_5_left = tk.Frame(content, bg=self.color_panel)
        self.step_5_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 20))

        self.step_5_right = tk.Frame(content, bg=self.color_panel)
        self.step_5_right.pack(side=tk.RIGHT, fill=tk.X, expand=True)

        self.rooms_listbox = tk.Listbox(
            self.step_5_left,
            height=5,
            selectmode=tk.MULTIPLE,
            bg=self.color_panel_light,
            fg=self.color_text,
            selectbackground=self.color_blue,
            selectforeground="white",
            highlightbackground=self.color_border,
            highlightcolor=self.color_blue,
            relief=tk.FLAT,
            exportselection=False,
            font=("Segoe UI", 10),
        )
        self.rooms_listbox.pack(fill=tk.BOTH, expand=True)
        self.rooms_listbox.bind(
            "<<ListboxSelect>>", lambda event: self._update_room_note_state(self.analysis_level.get())
        )

        self.room_note = ttk.Label(
            self.step_5_right,
            text="Es ist aktuell kein Raum ausgewaehlt. Bitte waehlen Sie mindestens einen Raum.",
            style="Muted.TLabel",
            wraplength=330,
        )
        self.room_note.pack(anchor=tk.W)

    def _build_right_column(self):
        panel = tk.Frame(
            self.right_content,
            bg=self.color_panel,
            highlightbackground=self.color_border,
            highlightthickness=1,
        )
        panel.pack(fill=tk.BOTH, expand=True)

        ttk.Label(panel, text="Anleitung und Hinweise", style="Heading.TLabel").pack(
            anchor=tk.W,
            padx=18,
            pady=(18, 16),
        )

        steps_card = tk.Frame(
            panel,
            bg=self.color_panel_light,
            highlightbackground=self.color_border,
            highlightthickness=1,
        )
        steps_card.pack(fill=tk.X, padx=18, pady=(0, 12))

        ttk.Label(steps_card, text="Schritte", style="Heading.TLabel").pack(anchor=tk.W, padx=16, pady=(14, 10))
        self.steps_list_container = tk.Frame(steps_card, bg=self.color_panel_light)
        self.steps_list_container.pack(fill=tk.X)

        hints_card = tk.Frame(
            panel,
            bg=self.color_panel_light,
            highlightbackground=self.color_border,
            highlightthickness=1,
        )
        hints_card.pack(fill=tk.X, padx=18, pady=(0, 18))

        ttk.Label(hints_card, text="Moegliche Hinweise", style="Heading.TLabel").pack(
            anchor=tk.W,
            padx=16,
            pady=(14, 10),
        )

        hints = [
            "'all' erzeugt Comfort-/Analyseuebersichten plus Heating-/Cooling-Barplots und Jahresplots.",
            f"Die Variantenliste zeigt bei 'prepare' Input-Varianten aus {INPUT_DIR}, sonst Datenbank-Varianten aus {DATENBANK_DIR}.",
            "'prepare' kann CSV, Excel oder beides erzeugen; die Folgeskripte arbeiten operativ mit CSV.",
            "'comfort' zeigt die passenden Unterbefehle in zwei Spalten.",
            "'heating' arbeitet direkt mit der Raumauswahl; die Analyseebene wird dort nicht verwendet.",
            "'heating' bietet Maximalwert, Jahr, Monat, Woche und Tag mit passender Detailauswahl.",
            "'cooling' arbeitet wie heating mit der Raumauswahl, zeigt aber Kuehllasten als negative Zeitverlaeufe.",
            f"Berechnungen und Diagramme arbeiten mit den Daten aus {DATENBANK_DIR}.",
        ]
        for hint in hints:
            label = tk.Label(
                hints_card,
                text="* " + hint,
                bg=self.color_panel_light,
                fg=self.color_text,
                font=("Segoe UI", 10),
                anchor=tk.W,
                justify=tk.LEFT,
                wraplength=360,
            )
            label.pack(anchor=tk.W, padx=16, pady=5)

        self.log_card = tk.Frame(
            panel,
            bg=self.color_panel_light,
            highlightbackground=self.color_border,
            highlightthickness=1,
        )
        self.log_card.pack(fill=tk.BOTH, expand=True, padx=18, pady=(0, 18))

        log_header = tk.Frame(self.log_card, bg=self.color_panel_light)
        log_header.pack(fill=tk.X, padx=16, pady=(14, 10))

        ttk.Label(log_header, text="Status und Protokoll", style="Heading.TLabel").pack(
            side=tk.LEFT,
            anchor=tk.W,
        )

        self.log_expand_button = tk.Button(
            log_header,
            text="⤢",
            command=self._expand_log_panel,
            bg=self.color_panel_light,
            fg=self.color_text,
            activebackground=self.color_blue_dark,
            activeforeground="white",
            relief=tk.FLAT,
            font=("Segoe UI Symbol", 12, "bold"),
            width=3,
            cursor="hand2",
        )
        self.log_expand_button.pack(side=tk.RIGHT)

        status_label = ttk.Label(
            self.log_card,
            textvariable=self.status_var,
            style="Muted.TLabel",
        )
        status_label.pack(anchor=tk.W, padx=16, pady=(0, 8))

        self.run_log_text = tk.Text(
            self.log_card,
            height=14,
            bg=self.color_panel,
            fg=self.color_text,
            insertbackground=self.color_text,
            relief=tk.FLAT,
            highlightbackground=self.color_border,
            highlightcolor=self.color_blue,
            font=("Consolas", 9),
            wrap=tk.WORD,
        )
        self.run_log_text.pack(fill=tk.BOTH, expand=True, padx=16, pady=(0, 16))
        self.run_log_text.configure(state=tk.DISABLED)

    def _refresh_step_indicators(self):
        visible_cards = [card for card in self.step_card_order if card.winfo_manager() == "pack"]

        for index, card in enumerate(visible_cards, start=1):
            card.step_number_label.configure(text=str(index))

        for child in self.steps_list_container.winfo_children():
            child.destroy()

        for index, card in enumerate(visible_cards, start=1):
            text = self.step_card_descriptions[card]
            row = tk.Frame(self.steps_list_container, bg=self.color_panel_light)
            row.pack(fill=tk.X, padx=16, pady=5)

            number = tk.Label(
                row,
                text=str(index),
                bg=self.color_blue,
                fg="white",
                width=2,
                font=("Segoe UI", 10, "bold"),
            )
            number.pack(side=tk.LEFT, padx=(0, 10))

            label = tk.Label(
                row,
                text=text,
                bg=self.color_panel_light,
                fg=self.color_text,
                font=("Segoe UI", 10),
                anchor=tk.W,
                justify=tk.LEFT,
                wraplength=340,
            )
            label.pack(side=tk.LEFT, fill=tk.X, expand=True)

    def _set_status(self, message):
        self.status_var.set(message)
        if self.analysis_status_var is not None:
            self.analysis_status_var.set(message)
        self.root.update_idletasks()

    def _append_log(self, text, clear=False):
        if clear:
            self._clear_log_widgets()
        if self.run_log_text is None:
            return
        if text:
            self._append_log_text(text.rstrip() + "\n")

    def _clear_log_widgets(self):
        for text_widget in (self.run_log_text, self.expanded_log_text, self.analysis_log_text):
            if text_widget is None:
                continue
            with contextlib.suppress(tk.TclError):
                text_widget.configure(state=tk.NORMAL)
                text_widget.delete("1.0", tk.END)
                text_widget.configure(state=tk.DISABLED)

    def _append_log_text(self, text):
        if not text:
            return
        for text_widget in (self.run_log_text, self.expanded_log_text, self.analysis_log_text):
            if text_widget is None:
                continue
            with contextlib.suppress(tk.TclError):
                text_widget.configure(state=tk.NORMAL)
                text_widget.insert(tk.END, text)
                text_widget.see(tk.END)
                text_widget.configure(state=tk.DISABLED)

    def _expand_log_panel(self):
        if self.is_log_expanded:
            return

        self.is_log_expanded = True
        if self.log_expand_button is not None:
            self.log_expand_button.configure(text="⤡")

        if self.main_frame is not None:
            self.main_frame.pack_forget()
        if self.bottom_button_frame is not None:
            self.bottom_button_frame.pack_forget()

        self.log_focus_frame = tk.Frame(self.root, bg=self.color_bg)
        self.log_focus_frame.pack(fill=tk.BOTH, expand=True, padx=22, pady=10)

        focus_card = tk.Frame(
            self.log_focus_frame,
            bg=self.color_panel_light,
            highlightbackground=self.color_border,
            highlightthickness=1,
        )
        focus_card.pack(fill=tk.BOTH, expand=True)

        header = tk.Frame(focus_card, bg=self.color_panel_light)
        header.pack(fill=tk.X, padx=16, pady=(14, 10))
        ttk.Label(header, text="Status und Protokoll", style="Heading.TLabel").pack(side=tk.LEFT, anchor=tk.W)

        collapse_button = tk.Button(
            header,
            text="⤡",
            command=self._collapse_log_panel,
            bg=self.color_panel_light,
            fg=self.color_text,
            activebackground=self.color_blue_dark,
            activeforeground="white",
            relief=tk.FLAT,
            font=("Segoe UI Symbol", 12, "bold"),
            width=3,
            cursor="hand2",
        )
        collapse_button.pack(side=tk.RIGHT)

        ttk.Label(
            focus_card,
            textvariable=self.status_var,
            style="Muted.TLabel",
        ).pack(anchor=tk.W, padx=16, pady=(0, 8))

        body = tk.Frame(focus_card, bg=self.color_panel_light)
        body.pack(fill=tk.BOTH, expand=True, padx=16, pady=(0, 16))

        self.expanded_log_text = tk.Text(
            body,
            bg=self.color_panel,
            fg=self.color_text,
            insertbackground=self.color_text,
            relief=tk.FLAT,
            highlightbackground=self.color_border,
            highlightcolor=self.color_blue,
            font=("Consolas", 9),
            wrap=tk.WORD,
        )
        scrollbar = ttk.Scrollbar(
            body,
            orient=tk.VERTICAL,
            command=self.expanded_log_text.yview,
            style="Tool.Vertical.TScrollbar",
        )
        self.expanded_log_text.configure(yscrollcommand=scrollbar.set)
        self.expanded_log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.expanded_log_text.configure(state=tk.NORMAL)
        if self.run_log_text is not None:
            with contextlib.suppress(tk.TclError):
                existing_log = self.run_log_text.get("1.0", "end-1c")
                if existing_log:
                    self.expanded_log_text.insert(tk.END, existing_log)
        self.expanded_log_text.see(tk.END)
        self.expanded_log_text.configure(state=tk.DISABLED)

    def _collapse_log_panel(self):
        if not self.is_log_expanded:
            return

        self.is_log_expanded = False
        self.expanded_log_text = None
        if self.log_focus_frame is not None:
            with contextlib.suppress(tk.TclError):
                self.log_focus_frame.destroy()
        self.log_focus_frame = None

        if self.log_expand_button is not None:
            self.log_expand_button.configure(text="⤢")

        if self.main_frame is not None:
            self.main_frame.pack(fill=tk.BOTH, expand=True, padx=22, pady=10, after=self.title_frame)
        if self.bottom_button_frame is not None:
            self.bottom_button_frame.pack(fill=tk.X, padx=22, pady=(0, 18), after=self.main_frame)

    def _create_analysis_log_window(self, command_name):
        if self.analysis_log_window is not None and self.analysis_log_window.winfo_exists():
            self.analysis_log_window.destroy()

        dialog = tk.Toplevel(self.root)
        dialog.title(f"Analyse laeuft: {command_name}")
        dialog.geometry("980x560")
        dialog.minsize(760, 420)
        dialog.configure(bg=self.color_bg)
        dialog.transient(self.root)
        dialog.protocol("WM_DELETE_WINDOW", self._handle_analysis_log_window_close)

        header = tk.Frame(dialog, bg=self.color_bg)
        header.pack(fill=tk.X, padx=18, pady=(16, 8))
        ttk.Label(header, text="Status und Protokoll", style="Heading.TLabel").pack(anchor=tk.W)

        self.analysis_status_var = tk.StringVar(value=self.status_var.get())
        ttk.Label(
            header,
            textvariable=self.analysis_status_var,
            style="Muted.TLabel",
        ).pack(anchor=tk.W, pady=(6, 0))

        body = tk.Frame(dialog, bg=self.color_bg)
        body.pack(fill=tk.BOTH, expand=True, padx=18, pady=(0, 18))

        text_widget = tk.Text(
            body,
            bg=self.color_panel,
            fg=self.color_text,
            insertbackground=self.color_text,
            relief=tk.FLAT,
            highlightbackground=self.color_border,
            highlightcolor=self.color_blue,
            font=("Consolas", 9),
            wrap=tk.WORD,
        )
        scrollbar = ttk.Scrollbar(
            body,
            orient=tk.VERTICAL,
            command=text_widget.yview,
            style="Tool.Vertical.TScrollbar",
        )
        text_widget.configure(yscrollcommand=scrollbar.set)
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.configure(state=tk.DISABLED)

        self.analysis_log_window = dialog
        self.analysis_log_text = text_widget
        dialog.lift()

    def _handle_analysis_log_window_close(self):
        if self.is_running_pipeline:
            messagebox.showinfo(
                "Analyse laeuft",
                "Das Protokollfenster bleibt waehrend der laufenden Analyse geoeffnet.",
                parent=self.analysis_log_window if self.analysis_log_window is not None else self.root,
            )
            return
        self._destroy_analysis_log_window()

    def _destroy_analysis_log_window(self):
        if self.analysis_log_window is not None:
            with contextlib.suppress(tk.TclError):
                self.analysis_log_window.destroy()
        self.analysis_log_window = None
        self.analysis_log_text = None
        self.analysis_status_var = None

    def _schedule_pipeline_log_polling(self):
        if self.pipeline_log_poll_after_id is None:
            self.pipeline_log_poll_after_id = self.root.after(80, self._poll_pipeline_log_queue)

    def _poll_pipeline_log_queue(self):
        self.pipeline_log_poll_after_id = None
        if self.pipeline_queue is None:
            return

        completed_result = None
        while True:
            try:
                message_type, payload = self.pipeline_queue.get_nowait()
            except queue.Empty:
                break

            if message_type == "log":
                self._append_log_text(payload)
            elif message_type == "done":
                completed_result = payload

        if completed_result is not None:
            self._finish_pipeline_run(*completed_result)
            return

        if self.is_running_pipeline:
            self._schedule_pipeline_log_polling()

    def _run_pipeline_worker(
        self,
        selected_command,
        steps,
        variants,
        rooms,
        heating_mode,
        prepare_options,
        comfort_options,
        heating_options,
    ):
        success = True
        writer = QueueLogWriter(self.pipeline_queue)
        try:
            with contextlib.redirect_stdout(writer), contextlib.redirect_stderr(writer):
                if selected_command == "all":
                    all_args = build_runtime_args(
                        self.args,
                        variants=variants,
                        rooms=rooms,
                    )
                    run_all(all_args)
                    return

                execute_steps(
                    self.args,
                    steps=steps,
                    variants=variants,
                    rooms=rooms,
                    heating_mode=heating_mode,
                    prepare_options=prepare_options,
                    comfort_options=comfort_options,
                    heating_options=heating_options,
                )
        except SystemExit as exc:
            success = exc.code in (0, None)
            if not success:
                self.pipeline_queue.put(("log", f"X Prozess beendet mit Exit-Code {exc.code}\n"))
        except Exception:
            success = False
            self.pipeline_queue.put(("log", traceback.format_exc()))
        finally:
            self.pipeline_queue.put(("done", (selected_command, success)))

    def _finish_pipeline_run(self, selected_command, success):
        self.is_running_pipeline = False
        self.pipeline_thread = None
        self.pipeline_queue = None
        self.start_button.configure(state=tk.NORMAL)
        self.reset_button.configure(state=tk.NORMAL)

        if success:
            self._set_status(f"Pipeline abgeschlossen: {selected_command}")
            self._destroy_analysis_log_window()
            messagebox.showinfo("Analyse", "Der Befehl wurde erfolgreich ausgefuehrt.", parent=self.root)
        else:
            self._set_status(f"Pipeline fehlgeschlagen: {selected_command}")
            if self.analysis_log_window is not None and self.analysis_log_window.winfo_exists():
                self.analysis_log_window.lift()
            messagebox.showerror(
                "Analyse",
                "Bei der Ausfuehrung ist ein Fehler aufgetreten. Details stehen im Protokoll.",
                parent=self.root,
            )

    def _safe_popup_menu(self, menu, x_pos, y_pos):
        try:
            menu.tk_popup(x_pos, y_pos)
        finally:
            menu.grab_release()

    def _open_output_format_dialog(self):
        if self.format_dialog is not None and self.format_dialog.winfo_exists():
            self.format_dialog.focus_set()
            self.format_dialog.lift()
            return

        dialog = tk.Toplevel(self.root)
        dialog.title("Format")
        dialog.geometry("1180x760")
        dialog.minsize(980, 620)
        dialog.configure(bg=self.color_bg)
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.protocol("WM_DELETE_WINDOW", self._close_output_format_dialog)
        self.format_dialog = dialog

        header = tk.Frame(dialog, bg=self.color_bg)
        header.pack(fill=tk.X, padx=18, pady=(18, 10))

        ttk.Label(header, text="Ausgabeformate", style="Title.TLabel").pack(anchor=tk.W)
        ttk.Label(
            header,
            text=f"Quelle: {self.format_doc_path}",
            style="Muted.TLabel",
        ).pack(anchor=tk.W, pady=(4, 0))

        body = tk.Frame(dialog, bg=self.color_bg)
        body.pack(fill=tk.BOTH, expand=True, padx=18, pady=(0, 12))

        left = tk.Frame(body, bg=self.color_bg)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 14))

        right = tk.Frame(body, bg=self.color_panel, highlightbackground=self.color_border, highlightthickness=1)
        right.pack(side=tk.RIGHT, fill=tk.Y)

        ttk.Label(left, text="Ausgabe-Regeln", style="Heading.TLabel").pack(anchor=tk.W, pady=(0, 8))

        canvas = tk.Canvas(left, bg=self.color_bg, highlightthickness=0, bd=0)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(left, orient=tk.VERTICAL, command=canvas.yview, style="Tool.Vertical.TScrollbar")
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.configure(yscrollcommand=scrollbar.set)

        table_frame = tk.Frame(canvas, bg=self.color_panel_light)
        self.format_table_frame = table_frame
        window_id = canvas.create_window((0, 0), window=table_frame, anchor="nw")

        def _sync_table_width(event):
            canvas.itemconfigure(window_id, width=event.width)

        canvas.bind("<Configure>", _sync_table_width)
        table_frame.bind(
            "<Configure>",
            lambda _event: canvas.configure(scrollregion=canvas.bbox("all")),
        )
        self._build_output_format_table_header(table_frame)
        self._reload_output_format_rows(table_frame)

        self._build_format_catalog_column(right)

        button_bar = tk.Frame(dialog, bg=self.color_bg)
        button_bar.pack(fill=tk.X, padx=18, pady=(0, 18))

        ttk.Button(
            button_bar,
            text="Speichern",
            style="Primary.TButton",
            command=self._save_output_formats,
        ).pack(side=tk.RIGHT)
        ttk.Button(
            button_bar,
            text="Abbrechen",
            style="Secondary.TButton",
            command=self._close_output_format_dialog,
        ).pack(side=tk.RIGHT, padx=(0, 12))

    def _build_output_format_table_header(self, table_frame):
        headers = ["Befehl", "Unterbefehl", "Ausgabe", "Format"]
        widths = [14, 16, 34, 18]
        for column, (label_text, width) in enumerate(zip(headers, widths, strict=True)):
            label = tk.Label(
                table_frame,
                text=label_text,
                bg=self.color_panel,
                fg=self.color_text,
                font=("Segoe UI", 10, "bold"),
                anchor=tk.W,
                padx=8,
                pady=8,
            )
            label.grid(row=0, column=column, sticky="ew", padx=1, pady=1)
            table_frame.grid_columnconfigure(column, weight=1, minsize=width * 10)

    def _reload_output_format_rows(self, table_frame):
        if table_frame is None:
            return
        for child in table_frame.grid_slaves():
            if int(child.grid_info()["row"]) > 0:
                child.destroy()

        self.format_row_vars = {}
        rules = load_output_format_rules(self.format_doc_path)
        format_names = get_format_names()
        for row_index, rule in enumerate(rules, start=1):
            row_bg = self.color_panel_light if row_index % 2 else self.color_panel
            for column, value in enumerate([rule["command"], rule["subcommand"], rule["output"]]):
                label = tk.Label(
                    table_frame,
                    text=value,
                    bg=row_bg,
                    fg=self.color_text,
                    anchor=tk.W,
                    padx=8,
                    pady=8,
                    wraplength=300 if column == 2 else 160,
                    justify=tk.LEFT,
                )
                label.grid(row=row_index, column=column, sticky="ew", padx=1, pady=1)

            var = tk.StringVar(value=rule["format"] if rule["format"] in FORMAT_CATALOG else format_names[0])
            combo = ttk.Combobox(
                table_frame,
                textvariable=var,
                values=format_names,
                state="readonly",
            )
            combo.grid(row=row_index, column=3, sticky="ew", padx=1, pady=1, ipady=4)
            self.format_row_vars[rule["id"]] = {"var": var, "rule": rule}

    def _build_format_catalog_column(self, parent):
        ttk.Label(parent, text="Formate", style="Heading.TLabel").pack(anchor=tk.W, padx=14, pady=(14, 8))
        ttk.Label(
            parent,
            text="Verfuegbare feste Groessen",
            style="Muted.TLabel",
            wraplength=260,
            justify=tk.LEFT,
        ).pack(anchor=tk.W, padx=14, pady=(0, 8))

        for format_name, values in FORMAT_CATALOG.items():
            item = tk.Frame(
                parent, bg=self.color_panel_light, highlightbackground=self.color_border, highlightthickness=1
            )
            item.pack(fill=tk.X, padx=14, pady=5)
            ttk.Label(item, text=format_name, style="Dark.TLabel").pack(anchor=tk.W, padx=10, pady=(8, 2))
            if values["width_cm"] is None:
                size_text = "ohne feste Groesse"
            else:
                size_text = f"{values['width_cm']:g} cm x {values['height_cm']:g} cm"
            ttk.Label(item, text=size_text, style="Muted.TLabel").pack(anchor=tk.W, padx=10)
            ttk.Label(
                item,
                text=values["description"],
                style="Muted.TLabel",
                wraplength=240,
                justify=tk.LEFT,
            ).pack(anchor=tk.W, padx=10, pady=(2, 8))

    def _save_output_formats(self):
        if self.format_dialog is None or not self.format_dialog.winfo_exists():
            return
        rules = []
        for row_data in self.format_row_vars.values():
            rule = row_data["rule"].copy()
            selected_format = row_data["var"].get()
            if selected_format in FORMAT_CATALOG:
                rule["format"] = selected_format
            rules.append(rule)
        write_output_format_rules(rules, self.format_doc_path)
        self._set_status("Ausgabeformate gespeichert.")
        self._append_log(f"Ausgabeformate gespeichert: {self.format_doc_path}")
        messagebox.showinfo("Format", "Die Ausgabeformate wurden gespeichert.", parent=self.format_dialog)

    def _close_output_format_dialog(self):
        if self.format_dialog is not None and self.format_dialog.winfo_exists():
            self.format_dialog.destroy()
        self.format_dialog = None
        self.format_table_frame = None
        self.format_row_vars = {}

    def _open_name_mapping_dialog(self):
        if self.mapping_dialog is not None and self.mapping_dialog.winfo_exists():
            self.mapping_dialog.focus_set()
            self.mapping_dialog.lift()
            return

        dialog = tk.Toplevel(self.root)
        dialog.title("Namensmapping")
        dialog.geometry("1100x760")
        dialog.minsize(920, 600)
        dialog.configure(bg=self.color_bg)
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.protocol("WM_DELETE_WINDOW", self._close_name_mapping_dialog)
        self.mapping_dialog = dialog

        header = tk.Frame(dialog, bg=self.color_bg)
        header.pack(fill=tk.X, padx=18, pady=(18, 10))

        ttk.Label(header, text="Namensmapping", style="Title.TLabel").pack(anchor=tk.W)
        ttk.Label(
            header,
            text=f"Quelle: {self.mapping_doc_path}",
            style="Muted.TLabel",
        ).pack(anchor=tk.W, pady=(4, 0))

        body = tk.Frame(dialog, bg=self.color_bg)
        body.pack(fill=tk.BOTH, expand=True, padx=18, pady=(0, 12))

        canvas = tk.Canvas(body, bg=self.color_bg, highlightthickness=0, bd=0)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(body, orient=tk.VERTICAL, command=canvas.yview, style="Tool.Vertical.TScrollbar")
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.configure(yscrollcommand=scrollbar.set)

        table_frame = tk.Frame(canvas, bg=self.color_panel_light)
        self.mapping_table_frame = table_frame
        window_id = canvas.create_window((0, 0), window=table_frame, anchor="nw")

        def _sync_table_width(event):
            canvas.itemconfigure(window_id, width=event.width)

        canvas.bind("<Configure>", _sync_table_width)
        table_frame.bind(
            "<Configure>",
            lambda _event: canvas.configure(scrollregion=canvas.bbox("all")),
        )

        headers = ["Kategorie", "Aktueller Name", "Neuer Name", "Verwendung"]
        widths = [18, 24, 24, 34]
        for column, (label_text, width) in enumerate(zip(headers, widths, strict=True)):
            label = tk.Label(
                table_frame,
                text=label_text,
                bg=self.color_panel,
                fg=self.color_text,
                font=("Segoe UI", 10, "bold"),
                anchor=tk.W,
                padx=8,
                pady=8,
            )
            label.grid(row=0, column=column, sticky="ew", padx=1, pady=1)
            table_frame.grid_columnconfigure(column, weight=1, minsize=width * 10)

        self.mapping_row_vars = {}
        self._reload_mapping_rows(table_frame)

        button_bar = tk.Frame(dialog, bg=self.color_bg)
        button_bar.pack(fill=tk.X, padx=18, pady=(0, 18))

        ttk.Button(button_bar, text="Speichern", style="Secondary.TButton", command=self._save_name_mapping).pack(
            side=tk.LEFT
        )
        ttk.Button(
            button_bar,
            text="Dry-Run pruefen",
            style="Secondary.TButton",
            command=self._dry_run_name_mapping,
        ).pack(side=tk.LEFT, padx=(12, 0))
        ttk.Button(
            button_bar,
            text="Anwenden und bestaetigen",
            style="Primary.TButton",
            command=self._apply_name_mapping,
        ).pack(side=tk.RIGHT)
        ttk.Button(
            button_bar,
            text="Abbrechen",
            style="Secondary.TButton",
            command=self._close_name_mapping_dialog,
        ).pack(side=tk.RIGHT, padx=(0, 12))

    def _reload_mapping_rows(self, table_frame):
        for child in table_frame.grid_slaves():
            if int(child.grid_info()["row"]) > 0:
                child.destroy()

        resolved_doc, entries = NAMENSMAPPING_MODULE.load_mapping_entries(self.mapping_doc_path)
        self.mapping_doc_path = resolved_doc
        self.mapping_row_vars = {}

        for row_index, entry in enumerate(entries, start=1):
            row_bg = self.color_panel_light if row_index % 2 else self.color_panel
            cells = [entry.category, entry.current_name, None, entry.usage]
            for column, cell_value in enumerate(cells):
                if column == 2:
                    var = tk.StringVar(value=entry.new_name)
                    self.mapping_row_vars[entry.entry_id] = {"var": var, "entry": entry}
                    entry_widget = tk.Entry(
                        table_frame,
                        textvariable=var,
                        bg=self.color_panel,
                        fg=self.color_text,
                        insertbackground=self.color_text,
                        relief=tk.FLAT,
                        highlightbackground=self.color_border,
                        highlightcolor=self.color_blue,
                        font=("Segoe UI", 10),
                    )
                    entry_widget.grid(row=row_index, column=column, sticky="ew", padx=1, pady=1, ipady=6)
                    continue

                label = tk.Label(
                    table_frame,
                    text=cell_value,
                    bg=row_bg,
                    fg=self.color_text,
                    font=("Segoe UI", 9),
                    anchor=tk.W,
                    justify=tk.LEFT,
                    wraplength=280 if column == 3 else 220,
                    padx=8,
                    pady=8,
                )
                label.grid(row=row_index, column=column, sticky="nsew", padx=1, pady=1)

    def _collect_mapping_entries_from_dialog(self):
        entries = []
        for mapping_data in self.mapping_row_vars.values():
            entry = mapping_data["entry"]
            entries.append(
                NAMENSMAPPING_MODULE.replace(
                    entry,
                    new_name=mapping_data["var"].get().strip(),
                )
            )
        entries.sort(key=lambda item: item.line_number)
        return entries

    def _save_name_mapping(self):
        if self.mapping_dialog is None or not self.mapping_dialog.winfo_exists():
            return
        entries = self._collect_mapping_entries_from_dialog()
        NAMENSMAPPING_MODULE.write_mapping_entries(self.mapping_doc_path, entries)
        self._set_status("Namensmapping gespeichert.")
        self._append_log(f"Namensmapping gespeichert: {self.mapping_doc_path}")
        messagebox.showinfo("Namensmapping", "Das Mapping wurde gespeichert.", parent=self.mapping_dialog)
        if self.mapping_table_frame is not None:
            self._reload_mapping_rows(self.mapping_table_frame)

    def _dry_run_name_mapping(self):
        entries = self._collect_mapping_entries_from_dialog()
        summary = NAMENSMAPPING_MODULE.run_mapping(
            mapping_doc=self.mapping_doc_path,
            dry_run=True,
            entries=entries,
        )
        summary_text = NAMENSMAPPING_MODULE.format_run_summary(summary)
        self._set_status("Namensmapping Dry-Run abgeschlossen.")
        self._append_log(summary_text)
        messagebox.showinfo("Namensmapping Dry-Run", summary_text, parent=self.mapping_dialog)

    def _apply_name_mapping(self):
        if not messagebox.askyesno(
            "Namensmapping anwenden",
            "Sollen die aktuellen Mapping-Aenderungen gespeichert und direkt angewendet werden?",
            parent=self.mapping_dialog,
        ):
            return

        entries = self._collect_mapping_entries_from_dialog()
        summary = NAMENSMAPPING_MODULE.run_mapping(
            mapping_doc=self.mapping_doc_path,
            dry_run=False,
            entries=entries,
        )
        summary_text = NAMENSMAPPING_MODULE.format_run_summary(summary)
        self._set_status("Namensmapping angewendet.")
        self._append_log(summary_text)
        messagebox.showinfo(
            "Namensmapping",
            summary_text + "\n\nGUI-bezogene Aenderungen werden nach 'GUI aktualisieren' sichtbar.",
            parent=self.mapping_dialog,
        )

    def _close_name_mapping_dialog(self):
        if self.mapping_dialog is not None and self.mapping_dialog.winfo_exists():
            self.mapping_dialog.destroy()
        self.mapping_dialog = None
        self.mapping_table_frame = None

    def _build_bottom_buttons(self):
        self.bottom_button_frame = tk.Frame(self.root, bg=self.color_bg)
        self.bottom_button_frame.pack(fill=tk.X, padx=22, pady=(0, 18))

        self.start_button = ttk.Button(
            self.bottom_button_frame,
            text="Analyse starten",
            style="Primary.TButton",
            command=self._start_pipeline,
        )
        self.start_button.pack(side=tk.RIGHT)

        self.reset_button = ttk.Button(
            self.bottom_button_frame,
            text="Zuruecksetzen",
            style="Secondary.TButton",
            command=self._reset_fields,
        )
        self.reset_button.pack(side=tk.RIGHT, padx=(0, 12))

    def _populate_variants(self):
        selected_names = []
        if self.variants_listbox.size() > 0 and self.variants_listbox.get(0) != "[Keine Varianten gefunden]":
            selected_names = [self.variants_listbox.get(index) for index in self.variants_listbox.curselection()]

        selected_command = self.command.get()
        if selected_command == "prepare":
            variant_source_kind = "input"
            available_variants = list_input_variants(self.args.input_dir)
            source_dir = INPUT_DIR
        else:
            variant_source_kind = "datenbank"
            available_variants = list_datenbank_variants(self.args.datenbank_dir)
            source_dir = DATENBANK_DIR

        variant_names = sorted({strip_variant_suffix(variant) for variant in available_variants})
        if variant_source_kind == self.variant_source_kind and variant_names == self.variant_names:
            return

        self.variants_listbox.delete(0, tk.END)
        self.variant_source_kind = variant_source_kind
        self.variant_names = variant_names

        if not self.variant_names:
            self.variants_listbox.insert(tk.END, "[Keine Varianten gefunden]")
            self.variants_listbox.configure(state=tk.DISABLED)
            self.variant_note.configure(text=f"Keine Varianten in {source_dir} gefunden.")
            return

        for variant_name in self.variant_names:
            self.variants_listbox.insert(tk.END, variant_name)

        for variant_name in selected_names:
            if variant_name not in self.variant_names:
                continue
            selected_index = self.variant_names.index(variant_name)
            self.variants_listbox.selection_set(selected_index)

    def _populate_rooms(self):
        self.rooms_listbox.delete(0, tk.END)
        for room in ROOMS:
            self.rooms_listbox.insert(tk.END, room)

    def _set_analysis_scope(self, value):
        self.analysis_scope.set(value)
        self._update_dynamic_fields()

    def _set_command(self, value):
        if value in DISABLED_GUI_COMMANDS:
            return
        self.command.set(value)
        self.load_subcommand.set("")
        if value == "comfort":
            self.comfort_type.set(self.comfort_default_by_level[self.analysis_level.get()])
        if value in {"heating", "cooling"}:
            self.load_subcommand.set("bar")
            self.heating_view.set("bar")
        if value == "analyze_data":
            self.heating_series_layout.set("separate")
        self._update_dynamic_fields()

    def _set_prepare_export_format(self, value):
        self.prepare_export_format.set(value)
        self._update_dynamic_fields()

    def _set_analysis_level(self, value):
        self.analysis_level.set(value)
        self._update_dynamic_fields()

    def _set_heating_mode(self, value):
        self.heating_mode.set(value)
        self._update_dynamic_fields()

    def _set_heating_series_layout(self, value):
        self.heating_series_layout.set(value)
        self._update_dynamic_fields()

    def _set_load_subcommand(self, value):
        self.load_subcommand.set(value)
        if value == "bar":
            self.heating_view.set("bar")
        elif value == "timeline" and self.heating_view.get() not in {"year", "month", "week", "day"}:
            self.heating_view.set("year")
        self._update_dynamic_fields()

    def _set_comfort_type(self, value):
        self.comfort_type.set(value)
        self._update_dynamic_fields()

    def _set_heating_view(self, value):
        self.heating_view.set(value)
        self._update_dynamic_fields()

    def _update_dynamic_fields(self):
        self._populate_variants()
        self._update_scope_buttons()
        self._update_command_buttons()
        self._update_prepare_export_buttons()
        self._update_analysis_level_buttons()
        self._update_heating_mode_buttons()
        self._update_heating_layout_buttons()
        self._update_load_subcommand_buttons()
        self._update_heating_view_buttons()
        self._update_step_visibility()
        self._update_subcommand_dependent_fields()
        self._update_command_dependent_fields()
        self._update_prepare_export_note()
        self._update_comfort_options_for_analysis_level()
        self._update_heating_detail_fields()
        self._update_variant_field()
        self._update_room_field()
        self._refresh_step_indicators()

    def _update_step_visibility(self):
        selected_command = self.command.get()
        is_prepare = selected_command == "prepare"
        show_subcommands = selected_command in {"comfort", "heating", "cooling"}
        load_without_subcommand = selected_command in {"heating", "cooling"} and self.load_subcommand.get() not in {
            "bar",
            "timeline",
        }
        hide_options_step = selected_command in {"prepare", "all"} or load_without_subcommand
        self._set_card_visible(self.subcommand_card, show_subcommands)
        self._set_card_visible(self.prepare_export_card, is_prepare)
        self._set_card_visible(self.step_3_card, not hide_options_step)
        self._set_card_visible(self.step_4_card, True)
        self._set_card_visible(self.step_5_card, not is_prepare)

    def _set_card_visible(self, card, visible):
        is_visible = card.winfo_manager() == "pack"
        if visible and not is_visible:
            self._show_step_card_in_order(card)
        elif not visible and is_visible:
            card.pack_forget()

    def _show_step_card_in_order(self, card):
        card_index = self.step_card_order.index(card)
        for next_card in self.step_card_order[card_index + 1 :]:
            if next_card.winfo_manager() == "pack":
                card.pack(fill=tk.X, pady=6, before=next_card)
                return
        card.pack(fill=tk.X, pady=6)

    def _update_scope_buttons(self):
        for scope, button in self.scope_buttons.items():
            if self.analysis_scope.get() == scope:
                button.configure(bg=self.color_blue, fg="white")
            else:
                button.configure(bg=self.color_panel_light, fg=self.color_text)

    def _update_command_buttons(self):
        for command_name, button in self.command_buttons.items():
            if command_name in DISABLED_GUI_COMMANDS:
                button.configure(
                    state=tk.DISABLED,
                    bg=self.color_panel,
                    fg=self.color_muted,
                    disabledforeground=self.color_muted,
                )
            elif self.command.get() == command_name:
                button.configure(bg=self.color_blue, fg="white")
            else:
                button.configure(
                    state=tk.NORMAL,
                    bg=self.color_panel_light,
                    fg=self.color_text,
                )

    def _update_prepare_export_buttons(self):
        for export_format, button in self.prepare_export_buttons.items():
            if self.prepare_export_format.get() == export_format:
                button.configure(bg=self.color_blue, fg="white")
            else:
                button.configure(bg=self.color_panel_light, fg=self.color_text)

    def _update_selection_button_group(self, buttons, selected_value, disabled_values=None):
        disabled_values = disabled_values or set()
        for value, button in buttons.items():
            if value in disabled_values:
                button.configure(
                    state=tk.DISABLED,
                    bg=self.color_panel,
                    fg=self.color_muted,
                    disabledforeground=self.color_muted,
                )
            elif value == selected_value:
                button.configure(state=tk.NORMAL, bg=self.color_blue, fg="white")
            else:
                button.configure(state=tk.NORMAL, bg=self.color_panel_light, fg=self.color_text)

    def _update_analysis_level_buttons(self):
        self._update_selection_button_group(
            self.analysis_level_buttons,
            self.analysis_level.get(),
        )

    def _update_heating_mode_buttons(self):
        self._update_selection_button_group(
            self.heating_mode_buttons,
            self.heating_mode.get(),
        )

    def _update_heating_layout_buttons(self):
        self._update_selection_button_group(
            self.heating_layout_buttons,
            self.heating_series_layout.get(),
        )

    def _update_load_subcommand_buttons(self):
        self._update_selection_button_group(
            self.load_subcommand_buttons,
            self.load_subcommand.get(),
        )

    def _update_heating_view_buttons(self):
        self._update_selection_button_group(
            self.heating_view_buttons,
            self.heating_view.get(),
        )

    def _update_prepare_export_note(self):
        selected_format = self.prepare_export_format.get()
        if selected_format == "csv":
            self.prepare_export_note.configure(text="CSV ist das operative Standardformat fuer die Folgeskripte.")
            return
        if selected_format == "excel":
            self.prepare_export_note.configure(
                text="Excel dient aktuell nur der uebersichtlicheren Darstellung. Die Folgeskripte verwenden weiterhin CSV-Dateien."
            )
            return
        self.prepare_export_note.configure(
            text="CSV + Excel erzeugt operative CSV-Dateien fuer die Pipeline und zusaetzlich XLSX-Dateien zur Ansicht."
        )

    def _update_subcommand_dependent_fields(self):
        selected_command = self.command.get()
        for section in [
            self.comfort_section,
            self.load_subcommand_section,
        ]:
            section.pack_forget()

        if selected_command == "comfort":
            self.comfort_section.pack(fill=tk.X)
            return

        if selected_command in {"heating", "cooling"}:
            self.load_subcommand_title.configure(
                text="Kuehlvergleich Unterbefehle" if selected_command == "cooling" else "Heizvergleich Unterbefehle"
            )
            self.load_subcommand_note.configure(
                text="bar erzeugt Maximalwertdiagramme. timeline aktiviert die Zeitansichten."
            )
            self.load_subcommand_section.pack(fill=tk.X)

    def _update_command_dependent_fields(self):
        selected_command = self.command.get()
        steps = self.command_to_steps.get(selected_command, [])

        prepare_active = selected_command == "prepare"
        analyze_active = selected_command == "analyze_data"
        all_active = selected_command == "all"
        heating_active = "heating" in steps
        cooling_active = "cooling" in steps
        load_active = heating_active or cooling_active
        comfort_active = selected_command == "comfort"

        for section in [
            self.heating_mode_section,
            self.heating_layout_section,
            self.analysis_section,
            self.heating_view_section,
        ]:
            section.pack_forget()

        if all_active:
            return

        if load_active:
            self.load_mode_title.configure(text="Kuehlvergleich Modus" if cooling_active else "Heizvergleich Modus")
            self.load_view_title.configure(
                text="Kuehlvergleich Ansichten" if cooling_active else "Heizvergleich Ansichten"
            )
            self.heating_layout_title.configure(text="Diagrammausgabe")
            if self.load_subcommand.get() not in {"bar", "timeline"}:
                return
            self.heating_mode_section.pack(fill=tk.X, pady=(0, 12))
            if self.heating_mode.get() == "compare":
                self.heating_layout_section.pack(fill=tk.X, pady=(0, 12))
                self.heating_layout_note.configure(
                    text="Waehlt, ob mehrere Linien einzeln oder gemeinsam dargestellt werden sollen."
                )
            if self.load_subcommand.get() == "timeline":
                self.heating_view_section.pack(fill=tk.X)
            self.heating_note.configure(
                text="single erzeugt getrennte Ausgaben. compare fasst mehrere Datenreihen oder Varianten in einer Ausgabe zusammen."
            )
            return

        if comfort_active:
            self.analysis_section.pack(fill=tk.X)
            return

        if analyze_active:
            self.heating_layout_title.configure(text="Excel-Ausgabe")
            self.heating_layout_section.pack(fill=tk.X, pady=(0, 12))
            self.heating_layout_note.configure(
                text="separate erzeugt eine Excel pro Variante. combined erzeugt eine gemeinsame Excel fuer alle ausgewaehlten Varianten und Raeume."
            )
            return

        if prepare_active:
            return

        self.analysis_section.pack(fill=tk.X)

    def _update_comfort_options_for_analysis_level(self):
        allowed_values = self.comfort_allowed_by_level.get(
            self.analysis_level.get(),
            self.comfort_allowed_by_level["Analyse Raum"],
        )

        if self.command.get() == "comfort" and self.comfort_type.get() not in allowed_values:
            self.comfort_type.set(self.comfort_default_by_level[self.analysis_level.get()])

        disabled_values = {value for value in self.comfort_type_widgets if value not in allowed_values}
        self._update_selection_button_group(
            self.comfort_type_widgets,
            self.comfort_type.get(),
            disabled_values=disabled_values,
        )

    def _update_heating_detail_fields(self):
        selected_view = self.heating_view.get()
        load_label = "Kuehlansicht" if self.command.get() == "cooling" else "Heizansicht"
        self.heating_month_container.pack_forget()
        self.heating_week_container.pack_forget()
        self.heating_day_container.pack_forget()

        month_index = MONTH_NAMES.index(self.heating_month.get())
        valid_days = [str(day) for day in range(1, MONTH_DAY_COUNTS[month_index] + 1)]
        self.heating_day_combo.configure(values=valid_days)
        if self.heating_day.get() not in valid_days:
            self.heating_day.set(valid_days[0])

        if selected_view == "month":
            self.heating_view_note.configure(
                text=f"Waehlt einen Monat fuer die stuendliche {load_label} mit Tages- und Stundenachse."
            )
            self.heating_month_container.pack(fill=tk.X)
            return

        if selected_view == "week":
            self.heating_view_note.configure(
                text=f"Geben Sie eine Kalenderwoche im Bereich 1 bis {MAX_CALENDAR_WEEK} ein. Die Achse zeigt die echten Tageszahlen dieser Woche."
            )
            self.heating_week_container.pack(fill=tk.X)
            return

        if selected_view == "day":
            self.heating_view_note.configure(text="Waehlt Monat und Tag fuer eine 24-Stunden-Ansicht.")
            self.heating_month_container.pack(fill=tk.X, pady=(0, 8))
            self.heating_day_container.pack(fill=tk.X)
            return

        if selected_view == "year":
            self.heating_view_note.configure(
                text="Die Jahresansicht zeigt Monatslabels zwischen den Grenzen und zusaetzlich eine Stunden-Skalierung."
            )
            return

        self.heating_view_note.configure(text="Die Maximalwert-Ansicht benoetigt keine zusaetzliche Auswahl.")

    def _update_variant_field(self):
        if not self.variant_names:
            return

        scope = self.analysis_scope.get()
        previous_scope = self.last_variant_scope
        self.variants_listbox.configure(state=tk.NORMAL)

        if previous_scope == "Alle Varianten" and scope != "Alle Varianten":
            self.variants_listbox.selection_clear(0, tk.END)

        if scope == "Eine Variante":
            self.variants_listbox.configure(selectmode=tk.BROWSE)
            self._update_variant_note_state(scope)
            self.last_variant_scope = scope
            return

        self.variants_listbox.configure(selectmode=tk.MULTIPLE)
        if scope == "Mehrere Varianten":
            self._update_variant_note_state(scope)
            self.last_variant_scope = scope
            return

        self.variants_listbox.selection_set(0, tk.END)
        self.variants_listbox.configure(state=tk.DISABLED)
        self._update_variant_note_state(scope)
        self.last_variant_scope = scope

    def _update_variant_note_state(self, scope):
        if not self.variant_names:
            return

        if self.command.get() == "prepare":
            if scope == "Alle Varianten":
                self.variant_note.configure(
                    text=f"Alle Input-Varianten aus {INPUT_DIR} sind aktiv und werden vorbereitet."
                )
                return

            if not self.variants_listbox.curselection():
                if scope == "Eine Variante":
                    self.variant_note.configure(
                        text="Es ist aktuell keine Input-Variante ausgewaehlt. Bitte waehlen Sie eine Variante."
                    )
                    return

                self.variant_note.configure(
                    text="Es ist aktuell keine Input-Variante ausgewaehlt. Bitte waehlen Sie mindestens eine Variante."
                )
                return

            if scope == "Eine Variante":
                self.variant_note.configure(
                    text="Eine Input-Variante ist aktiv. Es wird genau diese Variante vorbereitet."
                )
                return

            self.variant_note.configure(
                text="Mehrere Input-Varianten sind aktiv. Es werden nur die ausgewaehlten Varianten vorbereitet."
            )
            return

        if scope == "Alle Varianten":
            self.variant_note.configure(
                text=f"Alle Datenbank-Varianten sind aktiv. Die Variantenauswahl wird automatisch aus {DATENBANK_DIR} uebernommen."
            )
            return

        if not self.variants_listbox.curselection():
            if scope == "Eine Variante":
                self.variant_note.configure(
                    text="Es ist aktuell keine Variante ausgewaehlt. Bitte waehlen Sie eine Variante."
                )
                return

            self.variant_note.configure(
                text="Es ist aktuell keine Variante ausgewaehlt. Bitte waehlen Sie mindestens eine Variante."
            )
            return

        if scope == "Eine Variante":
            self.variant_note.configure(
                text="Eine Datenbank-Variante ist aktiv. Es kann genau eine Variante ausgewaehlt werden."
            )
            return

        self.variant_note.configure(
            text="Mehrere Datenbank-Varianten sind aktiv. Es koennen mehrere Varianten ausgewaehlt werden."
        )

    def _update_room_field(self):
        if self.command.get() in {"heating", "cooling", "analyze_data", "all"}:
            self.rooms_listbox.configure(state=tk.NORMAL, selectmode=tk.MULTIPLE)
            self._set_step_5_enabled(True)
            if self.command.get() == "all":
                self._update_room_note_state("All")
                return
            self._update_room_note_state(
                "AnalyzeData"
                if self.command.get() == "analyze_data"
                else "Cooling"
                if self.command.get() == "cooling"
                else "Heating"
            )
            return

        level = self.analysis_level.get()
        if level == "Analyse Variante":
            self.rooms_listbox.selection_clear(0, tk.END)
            self.rooms_listbox.configure(state=tk.DISABLED, selectmode=tk.MULTIPLE)
            self._set_step_5_enabled(False)
            self._update_room_note_state(level)
            return

        self.rooms_listbox.configure(state=tk.NORMAL, selectmode=tk.MULTIPLE)
        self._set_step_5_enabled(True)
        self._update_room_note_state(level)

    def _set_step_5_enabled(self, enabled):
        card_bg = self.color_panel if enabled else self.color_panel_light
        header_bg = self.color_panel if enabled else self.color_panel_light
        number_bg = self.color_blue if enabled else self.color_border
        listbox_bg = self.color_panel_light if enabled else self.color_panel
        listbox_fg = self.color_text if enabled else self.color_muted
        highlight_color = self.color_blue if enabled else self.color_border
        note_color = self.color_muted if enabled else "#8a929c"

        self.step_5_card.configure(bg=card_bg)
        self.step_5_card.step_header.configure(bg=header_bg)
        self.step_5_left.configure(bg=card_bg)
        self.step_5_right.configure(bg=card_bg)
        self.step_5_card.step_number_label.configure(bg=number_bg)
        self.step_5_card.step_heading.configure(background=header_bg, foreground=self.color_text)
        self.rooms_listbox.configure(
            bg=listbox_bg,
            fg=listbox_fg,
            disabledforeground=listbox_fg,
            highlightbackground=self.color_border,
            highlightcolor=highlight_color,
            selectbackground=self.color_blue,
            selectforeground="white",
        )
        self.room_note.configure(foreground=note_color)

    def _update_room_note_state(self, level):
        if level == "AnalyzeData":
            if not self.rooms_listbox.curselection():
                self.room_note.configure(
                    text="Fuer analyze_data ist aktuell kein Raum ausgewaehlt. Bitte waehlen Sie mindestens einen Raum."
                )
                return

            self.room_note.configure(
                text="analyze_data ist aktiv. Die ausgewaehlten Raeume werden direkt fuer die Auswertung verwendet."
            )
            return

        if level == "Heating":
            if not self.rooms_listbox.curselection():
                self.room_note.configure(
                    text="Fuer heating ist aktuell kein Raum ausgewaehlt. Bitte waehlen Sie mindestens einen Raum."
                )
                return

            self.room_note.configure(
                text="Heating ist aktiv. Die ausgewaehlten Raeume werden direkt fuer den Lauf verwendet."
            )
            return

        if level == "Cooling":
            if not self.rooms_listbox.curselection():
                self.room_note.configure(
                    text="Fuer cooling ist aktuell kein Raum ausgewaehlt. Bitte waehlen Sie mindestens einen Raum."
                )
                return

            self.room_note.configure(
                text="Cooling ist aktiv. Die ausgewaehlten Raeume werden direkt fuer den Lauf verwendet."
            )
            return

        if level == "All":
            if not self.rooms_listbox.curselection():
                self.room_note.configure(
                    text="Fuer all ist aktuell kein Raum ausgewaehlt. Bitte waehlen Sie mindestens einen Raum."
                )
                return

            self.room_note.configure(
                text="All ist aktiv. Die ausgewaehlten Raeume werden fuer Comfort-/Analyseuebersichten sowie Heating-/Cooling-Barplots und Jahresplots verwendet."
            )
            return

        if level == "Analyse Variante":
            self.room_note.configure(
                text="Analyse Variante ist aktiv. Die Raumauswahl ist deaktiviert; es werden automatisch alle Raeume verwendet."
            )
            return

        if not self.rooms_listbox.curselection():
            self.room_note.configure(
                text="Es ist aktuell kein Raum ausgewaehlt. Bitte waehlen Sie mindestens einen Raum."
            )
            return

        if level == "Analyse Raum":
            self.room_note.configure(
                text="Analyse Raum ist aktiv. Es koennen einzelne oder mehrere Raeume ausgewaehlt werden."
            )
            return

        self.room_note.configure(
            text="Analyse Variante ist aktiv. Waehlen Sie die Raeume bewusst aus; es wird nichts automatisch uebernommen."
        )

    def _reset_fields(self):
        self.analysis_scope.set("Alle Varianten")
        self.command.set("comfort")
        self.prepare_export_format.set("csv")
        self.comfort_type.set("plot")
        self.analysis_level.set("Analyse Raum")
        self.load_subcommand.set("")
        self.heating_mode.set("single")
        self.heating_view.set("year")
        self.heating_series_layout.set("separate")
        self.heating_month.set(MONTH_NAMES[0])
        self.heating_week.set("1")
        self.heating_day.set("1")

        self.selected_comfort_type = "plot"
        self.selected_prepare_export_format = "csv"
        self.selected_load_subcommand = ""
        self.selected_heating_mode = "single"
        self.selected_heating_view = "year"
        self.selected_heating_series_layout = "separate"
        self.selected_month = MONTH_NAMES[0]
        self.selected_week = 1
        self.selected_day = 1

        self._update_dynamic_fields()

    def _parse_heating_week(self):
        raw_value = self.heating_week.get().strip()
        if not raw_value:
            messagebox.showwarning("Warnung", "Bitte geben Sie eine Kalenderwoche ein.")
            return None
        if not raw_value.isdigit():
            messagebox.showwarning("Warnung", "Die Kalenderwoche muss eine ganze Zahl sein.")
            return None

        week_value = int(raw_value)
        if week_value < 1 or week_value > MAX_CALENDAR_WEEK:
            messagebox.showwarning(
                "Warnung",
                f"Bitte geben Sie eine Kalenderwoche zwischen 1 und {MAX_CALENDAR_WEEK} ein.",
            )
            return None
        return week_value

    def _parse_heating_day(self):
        raw_value = self.heating_day.get().strip()
        if not raw_value:
            messagebox.showwarning("Warnung", "Bitte waehlen Sie einen Tag.")
            return None
        if not raw_value.isdigit():
            messagebox.showwarning("Warnung", "Der Tag muss eine ganze Zahl sein.")
            return None

        day_value = int(raw_value)
        month_index = MONTH_NAMES.index(self.heating_month.get())
        max_days = MONTH_DAY_COUNTS[month_index]
        if day_value < 1 or day_value > max_days:
            messagebox.showwarning(
                "Warnung",
                f"Bitte waehlen Sie fuer {self.heating_month.get()} einen Tag zwischen 1 und {max_days}.",
            )
            return None
        return day_value

    def _get_selected_variants(self):
        if not self.variant_names:
            return []
        if self.analysis_scope.get() == "Alle Varianten":
            return self.variant_names.copy()
        selected_indices = self.variants_listbox.curselection()
        return [self.variant_names[index] for index in selected_indices]

    def _get_selected_rooms(self):
        if self.command.get() == "prepare":
            return ROOMS.copy()
        if self.command.get() in {"heating", "cooling", "analyze_data", "all"}:
            selected_indices = self.rooms_listbox.curselection()
            return [self.rooms_listbox.get(index) for index in selected_indices]
        if self.analysis_level.get() == "Analyse Variante":
            return ROOMS.copy()
        selected_indices = self.rooms_listbox.curselection()
        return [self.rooms_listbox.get(index) for index in selected_indices]

    def _validate_variant_sources(self, steps, variants):
        if not variants:
            messagebox.showwarning("Warnung", "Bitte waehlen Sie mindestens eine Variante.")
            return False

        return True

    def _start_pipeline(self):
        if self.is_running_pipeline:
            return

        selected_command = self.command.get()
        if selected_command == "comfort":
            comfort_settings = get_comfort_output_settings(self.comfort_type.get())
            steps = comfort_settings["steps"]
        else:
            steps = self.command_to_steps.get(selected_command, [])

        variants = self._get_selected_variants()
        rooms = self._get_selected_rooms()

        if not steps:
            messagebox.showwarning("Warnung", "Bitte waehlen Sie einen gueltigen Befehl.")
            return
        if not self._validate_variant_sources(steps, variants):
            return
        if not rooms:
            messagebox.showwarning("Warnung", "Bitte waehlen Sie mindestens einen Raum.")
            return
        selected_week = None
        selected_day = None
        if selected_command in {"heating", "cooling"} and self.load_subcommand.get() not in {"bar", "timeline"}:
            messagebox.showwarning("Warnung", "Bitte waehlen Sie den Unterbefehl bar oder timeline.")
            return

        uses_load_detail_options = (
            selected_command in {"heating", "cooling"} and self.load_subcommand.get() == "timeline"
        )
        if uses_load_detail_options:
            if self.heating_view.get() in {"month", "day"} and self.heating_month.get() not in MONTH_NAMES:
                messagebox.showwarning("Warnung", "Bitte waehlen Sie einen gueltigen Monat.")
                return
            if self.heating_view.get() == "week":
                selected_week = self._parse_heating_week()
                if selected_week is None:
                    return
            elif self.heating_view.get() == "day":
                selected_day = self._parse_heating_day()
                if selected_day is None:
                    return
            elif self.heating_view.get() == "month":
                selected_week = None

        self.selected_steps = steps
        self.selected_variants = variants
        self.selected_rooms = rooms
        self.selected_prepare_export_format = self.prepare_export_format.get()
        self.selected_load_subcommand = self.load_subcommand.get()
        self.selected_heating_mode = "single" if selected_command == "all" else self.heating_mode.get()
        if selected_command == "all":
            self.selected_heating_view = "year"
        elif selected_command in {"heating", "cooling"} and self.selected_load_subcommand == "bar":
            self.selected_heating_view = "bar"
        else:
            self.selected_heating_view = self.heating_view.get()
        self.selected_heating_series_layout = (
            "separate" if selected_command == "all" else self.heating_series_layout.get()
        )
        self.selected_month = self.heating_month.get()
        self.selected_week = selected_week if selected_week is not None else 1
        self.selected_day = selected_day if selected_day is not None else int(self.heating_day.get())
        self.selected_comfort_type = self.comfort_type.get()
        comfort_options = {}
        if selected_command == "comfort":
            comfort_options = get_comfort_output_settings(self.selected_comfort_type)

        prepare_options = {
            "export_format": self.selected_prepare_export_format,
        }
        heating_options = {
            "view": self.selected_heating_view,
            "month": self.selected_month,
            "week": self.selected_week if self.selected_heating_view == "week" else None,
            "day": self.selected_day if self.selected_heating_view == "day" else None,
            "series_layout": self.selected_heating_series_layout,
        }

        self.is_running_pipeline = True
        self.start_button.configure(state=tk.DISABLED)
        self.reset_button.configure(state=tk.DISABLED)
        self._create_analysis_log_window(selected_command)
        self._set_status(f"Pipeline läuft: {selected_command}")
        self._append_log(f"Starte Pipeline fuer Befehl: {selected_command}", clear=False)
        self.root.update_idletasks()

        self.pipeline_queue = queue.Queue()
        self.pipeline_thread = threading.Thread(
            target=self._run_pipeline_worker,
            args=(
                selected_command,
                steps,
                variants,
                rooms,
                self.selected_heating_mode,
                prepare_options,
                comfort_options,
                heating_options,
            ),
            daemon=True,
        )
        self.pipeline_thread.start()
        self._schedule_pipeline_log_polling()


def run_gui_menu(args):
    """Legacy-Dialogfluss: GUI oeffnen und danach die Auswahl zurueckgeben."""
    root = tk.Tk()
    gui = PipelineGUI(root, args)
    root.mainloop()

    comfort_options = {}
    if gui.command.get() == "comfort":
        comfort_options = get_comfort_output_settings(gui.selected_comfort_type)

    prepare_options = {
        "export_format": gui.selected_prepare_export_format,
    }

    heating_options = {
        "view": gui.selected_heating_view,
        "month": gui.selected_month,
        "week": gui.selected_week if gui.selected_heating_view == "week" else None,
        "day": gui.selected_day if gui.selected_heating_view == "day" else None,
        "series_layout": gui.selected_heating_series_layout,
    }

    return (
        gui.selected_steps,
        gui.selected_variants,
        gui.selected_rooms,
        gui.selected_heating_mode,
        prepare_options,
        comfort_options,
        heating_options,
    )


def build_parser():
    """Definiert die zentrale CLI mit allen Befehlen und gemeinsamen Optionen."""
    parser = argparse.ArgumentParser(
        description="Zentraler Einstiegspunkt fuer Datenaufbereitung, Auswertung und GUI der Pipeline."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument(
        "--input-dir",
        default=INPUT_DIR,
        help="Wurzelverzeichnis mit Variantenordnern, optional mit Suffix *_rohdaten",
    )
    common.add_argument(
        "--datenbank-dir",
        default=DATENBANK_DIR,
        help="Verzeichnis mit aufbereiteten Daten vom Typ *_nutzdaten",
    )
    common.add_argument(
        "--output-root",
        default=OUTPUT_DIR,
        help="Wurzelverzeichnis fuer erzeugte Ausgaben",
    )
    common.add_argument(
        "--run-id",
        default=None,
        help="Optionale Lauf-ID fuer Plot- und Analyseausgaben",
    )
    common.add_argument(
        "--variants",
        type=parse_comma_separated_list,
        default=None,
        help="Komma-getrennte Variantenliste ohne Suffix",
    )
    common.add_argument(
        "--rooms",
        type=parse_comma_separated_list,
        default=None,
        help="Komma-getrennte Raumliste",
    )
    common.add_argument(
        "--view",
        choices=["bar", "year", "month", "week", "day"],
        default="bar",
        help="Darstellungsmodus fuer heating/cooling: bar, year, month, week oder day",
    )
    common.add_argument(
        "--month",
        choices=MONTH_NAMES,
        default=None,
        help="Monatsfilter fuer heating/cooling bei view=month",
    )
    common.add_argument(
        "--week",
        type=int,
        default=None,
        help="Kalenderwoche fuer heating/cooling bei view=week",
    )
    common.add_argument(
        "--day",
        type=int,
        default=None,
        help="Tag im gewaelten Monat fuer heating/cooling bei view=day",
    )
    common.add_argument(
        "--heating-mode",
        "--variant-mode",
        choices=["single", "compare"],
        default=None,
        dest="heating_mode",
        help="Ausgabe fuer heating/cooling/analyze_data: single erzeugt getrennte Ausgaben, compare fasst Ausgaben zusammen",
    )
    common.add_argument(
        "--heating-series-layout",
        "--series-layout",
        choices=["separate", "combined"],
        default=None,
        dest="heating_series_layout",
        help="Ausgabe fuer heating/cooling/analyze_data: separate oder combined; Standard ist separate",
    )
    common.add_argument(
        "--gui-refresh-port",
        type=int,
        default=None,
        help=argparse.SUPPRESS,
    )
    common.add_argument(
        "--gui-window-x",
        type=int,
        default=None,
        help=argparse.SUPPRESS,
    )
    common.add_argument(
        "--gui-window-y",
        type=int,
        default=None,
        help=argparse.SUPPRESS,
    )
    common.add_argument(
        "--gui-window-width",
        type=int,
        default=None,
        help=argparse.SUPPRESS,
    )
    common.add_argument(
        "--gui-window-height",
        type=int,
        default=None,
        help=argparse.SUPPRESS,
    )
    common.add_argument(
        "--gui-window-maximized",
        type=int,
        choices=[0, 1],
        default=0,
        help=argparse.SUPPRESS,
    )
    common.add_argument("--debug", dest="debug", action="store_true", help="Aktiviert Debug-Ausgaben")
    common.add_argument("--no-debug", dest="debug", action="store_false", help="Deaktiviert Debug-Ausgaben")

    prepare_parser = subparsers.add_parser(
        "prepare",
        parents=[common],
        help="Bereitet Rohdaten zu Raum-CSV-, Raum-XLSX- oder kombinierten Ausgaben auf",
    )
    prepare_parser.add_argument(
        "--export-format",
        choices=EXPORT_FORMATS,
        default="csv",
        help="Exportformat fuer prepare: csv, excel oder both",
    )
    prepare_parser.set_defaults(debug=True)

    comfort_parser = subparsers.add_parser(
        "comfort",
        parents=[common],
        help="Erstellt Komfortausgaben: plot, overview, analysis oder Kombinationen",
    )
    comfort_parser.add_argument(
        "--output-type",
        choices=["plot", "plot_overview", "plot_analysis", "plot_analysis_overview"],
        default="plot_analysis_overview",
        help="Wählt das Komfort-Ausgabeprofil aus",
    )
    comfort_parser.set_defaults(debug=True)

    analyze_parser = subparsers.add_parser(
        "analyze-data",
        aliases=["analyze_data"],
        parents=[common],
        help="Erstellt die Excel-Auswertung",
    )
    analyze_parser.set_defaults(debug=True)

    heating_parser = subparsers.add_parser(
        "heating",
        parents=[common],
        help="Erstellt Heizleistungsvergleichsdiagramme",
    )
    heating_parser.set_defaults(debug=True)

    cooling_parser = subparsers.add_parser(
        "cooling",
        parents=[common],
        help="Erstellt Kuehlleistungsvergleichsdiagramme",
    )
    cooling_parser.set_defaults(debug=True)

    gui_parser = subparsers.add_parser(
        "gui",
        parents=[common],
        help="Startet die grafische Pipeline-Oberflaeche",
    )
    gui_parser.add_argument(
        "--export-format",
        choices=EXPORT_FORMATS,
        default="csv",
        help="Startwert fuer das Prepare-Exportformat in der GUI",
    )
    gui_parser.set_defaults(debug=True)

    all_parser = subparsers.add_parser(
        "all",
        parents=[common],
        help="Erzeugt Comfort-/Analyseuebersichten sowie Heating-/Cooling-Barplots und Jahresplots",
    )
    all_parser.set_defaults(debug=True)

    return parser


def main():
    """Parst CLI-Argumente und verzweigt zum gewaehlten Befehl."""
    parser = build_parser()
    args = parser.parse_args()
    raw_argv = sys.argv[1:]
    args.variant_mode_explicit = has_cli_option(raw_argv, "--heating-mode", "--variant-mode")
    args.series_layout_explicit = has_cli_option(raw_argv, "--heating-series-layout", "--series-layout")

    args.rooms = normalize_rooms(args.rooms)

    if args.command == "prepare":
        ensure_required_data(args, ["prepare"])
        run_prepare(args)
        return

    if args.command == "comfort":
        comfort_steps = get_comfort_output_settings(args.output_type)["steps"]
        ensure_required_data(args, comfort_steps)
        run_comfort(args)
        return

    if args.command in {"analyze-data", "analyze_data"}:
        ensure_required_data(args, ["analyze"])
        run_analyze(args)
        return

    if args.command == "heating":
        ensure_required_data(args, ["heating"])
        run_heating(args)
        return

    if args.command == "cooling":
        ensure_required_data(args, ["cooling"])
        run_cooling(args)
        return

    if args.command == "gui":
        run_gui(args)
        return

    if args.command == "all":
        run_all(args)


if __name__ == "__main__":
    main()
