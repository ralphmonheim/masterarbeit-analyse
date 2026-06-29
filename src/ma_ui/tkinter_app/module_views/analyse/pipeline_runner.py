"""Pipeline-Start, Worker und Loganzeige der Tkinter-Analyse."""

from __future__ import annotations

import contextlib
import queue
import threading
import traceback
from pathlib import Path

from ma_analyse.analysis.components.time_windows import MONTH_NAMES
from ma_analyse.analysis.templates import PLOT_TEMPLATE_CHOICES
from ma_analyse.app.commands import get_comfort_output_settings
from ma_analyse.core.logging import command_log, should_log_command
from ma_analyse.models import AnalysisResult
from ma_workflow import run_analysis_action

from .pipeline_config import build_tkinter_analysis_config
from .tk_compat import messagebox, tk, ttk
from .worker import QueueLogWriter


class TkinterAnalysisPipelineRunnerMixin:
    """Mixin fuer ausgelagerte PipelineGUI-Methoden."""

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

    def _write_analysis_result_to_log(self, result: AnalysisResult):
        if result.log_text.strip():
            print(result.log_text.rstrip())
        if result.warnings:
            print("Warnungen:")
            for warning in result.warnings:
                print(f"- {warning}")
        if result.errors:
            print("Fehler:")
            for error in result.errors:
                print(f"- {error}")
        if result.created_files:
            print("Erzeugte Dateien:")
            for path in result.created_files:
                display_path = Path(path)
                print(f"- {display_path}")

    def _run_pipeline_worker(self, selected_command, config):
        success = True
        writer = QueueLogWriter(self.pipeline_queue)

        try:
            with contextlib.redirect_stdout(writer), contextlib.redirect_stderr(writer):
                if should_log_command(selected_command):
                    with command_log(selected_command) as log_file:
                        print(f"Logdatei: {log_file}")
                        result = run_analysis_action(config)
                        self._write_analysis_result_to_log(result)
                    print(f"Log gespeichert: {log_file}")
                    success = result.success
                    return

                result = run_analysis_action(config)
                self._write_analysis_result_to_log(result)
                success = result.success
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
        self.preview_button.configure(state=tk.NORMAL)
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

    def _open_log_view(self):
        if self.analysis_log_window is not None and self.analysis_log_window.winfo_exists():
            self.analysis_log_window.lift()
            with contextlib.suppress(tk.TclError):
                self.analysis_log_window.focus_force()
            return
        self._expand_log_panel()

    def _start_preview(self):
        self._set_status("Vorschau wird mit aktuellen Einstellungen erzeugt.")
        self._start_pipeline()

    def _start_pipeline(self):
        if self.is_running_pipeline:
            return

        selected_command = self.command.get()
        if not selected_command:
            messagebox.showwarning("Warnung", "Bitte waehlen Sie einen gueltigen Befehl.")
            return

        if selected_command == "prepare" and not self.prepare_export_format.get():
            messagebox.showwarning("Warnung", "Bitte waehlen Sie ein Exportformat.")
            return

        if selected_command == "comfort":
            if not self.comfort_type.get():
                messagebox.showwarning("Warnung", "Bitte waehlen Sie einen Comfort-Unterbefehl.")
                return

        if selected_command == "analyze_data" and not self.heating_series_layout.get():
            messagebox.showwarning("Warnung", "Bitte waehlen Sie eine Excel-Ausgabe.")
            return

        if selected_command == "plot-template":
            if self.plot_template.get() not in PLOT_TEMPLATE_CHOICES:
                messagebox.showwarning("Warnung", "Bitte waehlen Sie ein Plot-Template.")
                return
            if self.plot_template_mode.get() not in {"single", "compare"}:
                messagebox.showwarning("Warnung", "Bitte waehlen Sie unter Export / Ausgabe single oder compare.")
                return

        if not self.analysis_scope.get():
            messagebox.showwarning("Warnung", "Bitte waehlen Sie den Analyseumfang.")
            return

        if selected_command != "prepare" and not self.room_scope.get():
            messagebox.showwarning("Warnung", "Bitte waehlen Sie den Raumumfang.")
            return

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
        plot_template_options = {}
        if selected_command == "plot-template":
            plot_template_options = self._get_plot_template_options(variants, rooms)
            if plot_template_options is None:
                return
        if selected_command in {"heating", "cooling"} and self.load_subcommand.get() not in {"bar", "timeline"}:
            messagebox.showwarning("Warnung", "Bitte waehlen Sie den Unterbefehl bar oder timeline.")
            return
        if selected_command in {"heating", "cooling"} and not self.heating_mode.get():
            messagebox.showwarning("Warnung", "Bitte waehlen Sie den Vergleichsmodus.")
            return
        if (
            selected_command in {"heating", "cooling"}
            and self.heating_mode.get() == "compare"
            and not self.heating_series_layout.get()
        ):
            messagebox.showwarning("Warnung", "Bitte waehlen Sie die Diagrammausgabe.")
            return

        uses_load_detail_options = (
            selected_command in {"heating", "cooling"} and self.load_subcommand.get() == "timeline"
        )
        if uses_load_detail_options:
            if self.heating_view.get() not in {"year", "month", "week", "day"}:
                messagebox.showwarning("Warnung", "Bitte waehlen Sie eine Zeitansicht.")
                return
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
        self.selected_plot_template_options = plot_template_options
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
        analysis_config = build_tkinter_analysis_config(
            args=self.args,
            selected_command=selected_command,
            variants=variants,
            rooms=rooms,
            heating_mode=self.selected_heating_mode,
            prepare_options=prepare_options,
            comfort_output_type=self.selected_comfort_type if selected_command == "comfort" else None,
            heating_options=heating_options,
            plot_template_options=plot_template_options,
        )

        self.is_running_pipeline = True
        self.start_button.configure(state=tk.DISABLED)
        self.preview_button.configure(state=tk.DISABLED)
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
                analysis_config,
            ),
            daemon=True,
        )
        self.pipeline_thread.start()
        self._schedule_pipeline_log_polling()
