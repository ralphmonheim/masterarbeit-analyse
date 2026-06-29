"""Fenster-, Style- und Refresh-Logik der Tkinter-Analyse."""

from __future__ import annotations

import contextlib
import ctypes
import os
import subprocess

from .restart import build_gui_restart_argv
from .singleton import GUI_REFRESH_TIMEOUT_SECONDS, GuiRefreshCoordinator
from .tk_compat import messagebox, tk, ttk


class TkinterAnalysisThemeWindowMixin:
    """Mixin fuer ausgelagerte PipelineGUI-Methoden."""

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
        self._update_right_scrollbar_visibility()

    def _sync_right_scroll_width(self, event):
        self.right_scroll_canvas.itemconfigure(self.right_scroll_window, width=event.width)
        self._update_right_scrollbar_visibility()

    def _update_right_scrollbar_visibility(self):
        if not hasattr(self, "right_scrollbar") or self.right_scrollbar is None:
            return
        if getattr(self, "_is_updating_right_scrollbar", False):
            return
        self._is_updating_right_scrollbar = True
        try:
            self.root.update_idletasks()
            content_height = self.right_content.winfo_reqheight()
            viewport_height = self.right_scroll_canvas.winfo_height()
            needs_scrollbar = content_height > viewport_height + 1
            if needs_scrollbar == self.right_scrollbar_visible:
                return
            self.right_scrollbar_visible = needs_scrollbar
            if needs_scrollbar:
                self.right_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                return
            self.right_scrollbar.pack_forget()
            self.right_scroll_canvas.yview_moveto(0)
        finally:
            self._is_updating_right_scrollbar = False

    def _resolve_widget(self, widget):
        if isinstance(widget, str):
            try:
                return self.root.nametowidget(widget)
            except (KeyError, tk.TclError, AttributeError):
                return None
        return widget

    def _should_skip_mousewheel(self, widget):
        widget = self._resolve_widget(widget)
        if widget is None:
            return False
        widget_class = widget.winfo_class()
        return widget_class in {"Listbox", "Text", "Entry", "TCombobox", "Combobox"}

    def _widget_is_in_left_scroll_area(self, widget):
        widget = self._resolve_widget(widget)
        if widget is None:
            return False
        current = widget
        while current is not None:
            if current == self.left_scroll_host:
                return True
            parent_name = current.winfo_parent()
            if not parent_name:
                break
            try:
                current = current.nametowidget(parent_name)
            except (KeyError, tk.TclError, AttributeError):
                return False
        return False

    def _widget_is_in_right_scroll_area(self, widget):
        widget = self._resolve_widget(widget)
        if widget is None:
            return False
        current = widget
        while current is not None:
            if current == self.right_column:
                return True
            parent_name = current.winfo_parent()
            if not parent_name:
                break
            try:
                current = current.nametowidget(parent_name)
            except (KeyError, tk.TclError, AttributeError):
                return False
        return False

    def _on_mousewheel(self, event):
        if self._should_skip_mousewheel(event.widget):
            return
        delta = int(-event.delta / 120)
        if delta == 0:
            return
        if self._widget_is_in_right_scroll_area(event.widget):
            if self.right_scrollbar_visible:
                self.right_scroll_canvas.yview_scroll(delta, "units")
            return
        if self._widget_is_in_left_scroll_area(event.widget):
            self.left_scroll_canvas.yview_scroll(delta, "units")

    def _on_mousewheel_linux_up(self, event):
        if self._should_skip_mousewheel(event.widget):
            return
        if self._widget_is_in_right_scroll_area(event.widget):
            if self.right_scrollbar_visible:
                self.right_scroll_canvas.yview_scroll(-1, "units")
            return
        if self._widget_is_in_left_scroll_area(event.widget):
            self.left_scroll_canvas.yview_scroll(-1, "units")

    def _on_mousewheel_linux_down(self, event):
        if self._should_skip_mousewheel(event.widget):
            return
        if self._widget_is_in_right_scroll_area(event.widget):
            if self.right_scrollbar_visible:
                self.right_scroll_canvas.yview_scroll(1, "units")
            return
        if self._widget_is_in_left_scroll_area(event.widget):
            self.left_scroll_canvas.yview_scroll(1, "units")

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
        self._ensure_windows_taskbar_button()
        with contextlib.suppress(tk.TclError):
            self.root.after(60, self._ensure_windows_taskbar_button)

    def _ensure_windows_taskbar_button(self):
        """Haelt das rahmenlose Tk-Fenster in der Windows-Taskleiste sichtbar."""
        if os.name != "nt" or not self.root.winfo_exists():
            return

        with contextlib.suppress(Exception):
            user32 = ctypes.windll.user32
            window_handle = self.root.winfo_id()
            taskbar_handle = user32.GetParent(window_handle) or window_handle

            gwl_exstyle = -20
            ws_ex_appwindow = 0x00040000
            ws_ex_toolwindow = 0x00000080
            swp_nosize = 0x0001
            swp_nomove = 0x0002
            swp_nozorder = 0x0004
            swp_framechanged = 0x0020

            get_window_long = getattr(user32, "GetWindowLongPtrW", user32.GetWindowLongW)
            set_window_long = getattr(user32, "SetWindowLongPtrW", user32.SetWindowLongW)

            style = get_window_long(taskbar_handle, gwl_exstyle)
            style = (style | ws_ex_appwindow) & ~ws_ex_toolwindow
            set_window_long(taskbar_handle, gwl_exstyle, style)
            user32.SetWindowPos(
                taskbar_handle,
                0,
                0,
                0,
                0,
                0,
                swp_nomove | swp_nosize | swp_nozorder | swp_framechanged,
            )

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
