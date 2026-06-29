"""Layout- und Schrittaufbau der Tkinter-Analyse."""

from __future__ import annotations

from ma_analyse.analysis.components.time_windows import MONTH_NAMES
from ma_analyse.analysis.templates import DEFAULT_OUTDOOR_COLUMN, PLOT_TEMPLATE_CHOICES
from ma_analyse.settings.plot_templates import OPERATIVE_OVERLAY_ID, OUTDOOR_OVERLAY_ID

from .tk_compat import tk, ttk


class TkinterAnalysisLayoutStepsMixin:
    """Mixin fuer ausgelagerte PipelineGUI-Methoden."""

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

        source_widget = event.widget if event is not None else getattr(self, "settings_bottom_button", self.root)
        x_pos = source_widget.winfo_rootx()
        y_pos = source_widget.winfo_rooty() + source_widget.winfo_height()
        self._safe_popup_menu(self.tools_menu, x_pos, y_pos)

    def _build_main_layout(self):
        self.main_frame = tk.Frame(self.root, bg=self.color_bg)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=22, pady=10)

        self.left_scroll_host = tk.Frame(self.main_frame, bg=self.color_bg)
        self.left_scroll_host.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 12))
        self.left_scroll_host.configure(width=270)
        self.left_scroll_host.pack_propagate(False)

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

        self.right_column = tk.Frame(self.main_frame, bg=self.color_bg)
        self.right_column.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

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
        self.right_scrollbar_visible = True
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
        nav_item = tk.Frame(
            parent,
            bg=self.color_panel,
            highlightbackground=self.color_border,
            highlightthickness=1,
            cursor="hand2",
        )
        nav_item.pack(fill=tk.X, pady=6)

        header = tk.Frame(nav_item, bg=self.color_panel, cursor="hand2")
        header.pack(fill=tk.X, padx=14, pady=12)

        number_label = tk.Label(
            header,
            text=str(number),
            bg=self.color_border,
            fg="white",
            width=3,
            height=1,
            font=("Segoe UI", 12, "bold"),
            cursor="hand2",
        )
        number_label.pack(side=tk.LEFT, padx=(0, 12))

        heading = ttk.Label(header, text=title, style="Heading.TLabel")
        heading.pack(side=tk.LEFT)

        status_dot = tk.Label(
            header,
            text="●",
            bg=self.color_panel,
            fg=self.color_panel,
            font=("Segoe UI", 12, "bold"),
            cursor="hand2",
        )
        status_dot.pack(side=tk.RIGHT, padx=(10, 0))

        card = tk.Frame(
            self.right_content,
            bg=self.color_bg,
        )
        summary_frame = tk.Frame(
            card,
            bg=self.color_panel,
            highlightbackground=self.color_border,
            highlightthickness=1,
        )
        ttk.Label(
            summary_frame,
            text="summary",
            style="Dark.TLabel",
        ).pack(anchor=tk.W, padx=18, pady=(18, 6))
        summary_label = ttk.Label(
            summary_frame,
            text="",
            style="Muted.TLabel",
            justify=tk.LEFT,
            wraplength=650,
        )
        summary_label.pack(fill=tk.X, padx=18, pady=(0, 18))

        step_body = tk.Frame(
            card,
            bg=self.color_panel,
            highlightbackground=self.color_border,
            highlightthickness=1,
        )
        step_body.pack(fill=tk.BOTH, expand=True)

        card_header = tk.Frame(step_body, bg=self.color_panel)
        card_header.pack(fill=tk.X, padx=18, pady=(18, 10))
        ttk.Label(card_header, text=title, style="Heading.TLabel").pack(anchor=tk.W)

        content = tk.Frame(step_body, bg=self.color_panel)
        content.pack(fill=tk.BOTH, expand=True, padx=18, pady=(0, 18))
        card.step_nav = nav_item
        card.step_header = nav_item
        card.step_number_label = number_label
        card.step_heading = heading
        card.step_status_dot = status_dot
        card.step_summary_frame = summary_frame
        card.step_summary_label = summary_label
        card.step_body = step_body
        card.step_card_header = card_header
        card.step_content = content
        card.step_title = title
        card.step_available = True

        for widget in (nav_item, header, number_label, heading, status_dot):
            widget.bind("<Button-1>", lambda _event, selected_card=card: self._activate_step(selected_card))
        return card, content

    def _build_left_column(self):
        self._build_step_2()
        self._build_subcommand_step()
        self._build_step_3()
        self._build_overlay_step()
        self._build_step_4()
        self._build_step_5()
        self._build_prepare_export_step()
        self.step_card_order = [
            self.step_2_card,
            self.subcommand_card,
            self.step_3_card,
            self.overlay_card,
            self.step_4_card,
            self.step_5_card,
            self.prepare_export_card,
        ]
        self.step_card_descriptions = {
            self.step_2_card: "Befehl festlegen",
            self.subcommand_card: "Unterbefehl passend zum Befehl waehlen",
            self.step_3_card: "Template / Diagramm auswaehlen",
            self.overlay_card: "Datenlinien fuer Plot-Templates auswaehlen",
            self.step_4_card: "Varianten passend zum Befehl auswaehlen",
            self.step_5_card: "Raeume auswaehlen oder automatisch uebernehmen",
            self.prepare_export_card: "Export oder Ausgabe waehlen",
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

        self.plot_template_list_section = tk.Frame(content, bg=self.color_panel)
        ttk.Label(
            self.plot_template_list_section,
            text="Plot-Template",
            style="Dark.TLabel",
        ).pack(anchor=tk.W, pady=(0, 6))
        template_list_frame = tk.Frame(self.plot_template_list_section, bg=self.color_panel)
        template_list_frame.pack(fill=tk.BOTH, expand=True)
        self.plot_template_listbox = tk.Listbox(
            template_list_frame,
            height=12,
            selectmode=tk.BROWSE,
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
        template_scrollbar = ttk.Scrollbar(
            template_list_frame,
            orient=tk.VERTICAL,
            command=self.plot_template_listbox.yview,
        )
        self.plot_template_listbox.configure(yscrollcommand=template_scrollbar.set)
        self.plot_template_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        template_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        for template_name in PLOT_TEMPLATE_CHOICES:
            self.plot_template_listbox.insert(tk.END, template_name)
        self.plot_template_listbox.bind(
            "<<ListboxSelect>>",
            lambda _event: self._select_plot_template_from_list(),
        )
        self.plot_template_list_note = ttk.Label(
            self.plot_template_list_section,
            text="Alle experimentellen Diagramme werden direkt angezeigt. Die Gruppierung erfolgt erst bei der Übernahme in einen Hauptbefehl.",
            style="Muted.TLabel",
            wraplength=640,
            justify=tk.LEFT,
        )
        self.plot_template_list_note.pack(anchor=tk.W, pady=(6, 0))

    def _build_prepare_export_step(self):
        self.prepare_export_card, content = self._create_step_card(self.left_column, 7, "Export / Ausgabe")

        self.prepare_export_section = tk.Frame(content, bg=self.color_panel)
        ttk.Label(self.prepare_export_section, text="Exportformat", style="Dark.TLabel").pack(anchor=tk.W, pady=(0, 6))
        button_frame = tk.Frame(self.prepare_export_section, bg=self.color_panel)
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
            self.prepare_export_section,
            text="CSV ist das operative Standardformat fuer die Folgeskripte.",
            style="Muted.TLabel",
            wraplength=640,
            justify=tk.LEFT,
        )
        self.prepare_export_note.pack(anchor=tk.W, pady=(10, 0))

        self.plot_template_export_section = tk.Frame(content, bg=self.color_panel)
        ttk.Label(self.plot_template_export_section, text="Ausgabemodus", style="Dark.TLabel").pack(
            anchor=tk.W,
            pady=(0, 6),
        )
        _, self.plot_template_mode_buttons = self._create_selection_button_group(
            self.plot_template_export_section,
            [
                ("single", "single"),
                ("compare", "compare"),
            ],
            self._set_plot_template_mode,
        )
        self.plot_template_mode_note = ttk.Label(
            self.plot_template_export_section,
            text="single ist fuer Einzelraum-Templates gedacht, compare fuer Vergleichsansichten.",
            style="Muted.TLabel",
            wraplength=640,
            justify=tk.LEFT,
        )
        self.plot_template_mode_note.pack(anchor=tk.W, pady=(6, 0))

        self.load_export_section = tk.Frame(content, bg=self.color_panel)
        self.load_export_title = ttk.Label(
            self.load_export_section,
            text="Ausgabemodus",
            style="Dark.TLabel",
        )
        self.load_export_title.pack(anchor=tk.W, pady=(0, 6))
        _, self.heating_mode_buttons = self._create_selection_button_group(
            self.load_export_section,
            [("single", "single"), ("compare", "compare")],
            self._set_heating_mode,
        )
        self.load_export_note = ttk.Label(
            self.load_export_section,
            text="single erzeugt getrennte Ausgaben, compare fasst Datenreihen zusammen.",
            style="Muted.TLabel",
            wraplength=640,
            justify=tk.LEFT,
        )
        self.load_export_note.pack(anchor=tk.W, pady=(6, 10))
        self.load_layout_title = ttk.Label(
            self.load_export_section,
            text="Diagrammausgabe",
            style="Dark.TLabel",
        )
        _, self.heating_layout_buttons = self._create_selection_button_group(
            self.load_export_section,
            [("separate", "separate"), ("combined", "combined")],
            self._set_heating_series_layout,
        )
        self.load_layout_note = ttk.Label(
            self.load_export_section,
            text="Diese Zusatzwahl wird bei compare verwendet.",
            style="Muted.TLabel",
            wraplength=640,
            justify=tk.LEFT,
        )

        self.analysis_export_section = tk.Frame(content, bg=self.color_panel)
        ttk.Label(self.analysis_export_section, text="Excel-Ausgabe", style="Dark.TLabel").pack(
            anchor=tk.W,
            pady=(0, 6),
        )
        _, self.analysis_export_buttons = self._create_selection_button_group(
            self.analysis_export_section,
            [("separate", "separate"), ("combined", "combined")],
            self._set_heating_series_layout,
        )
        ttk.Label(
            self.analysis_export_section,
            text="separate erzeugt eine Excel pro Variante, combined eine gemeinsame Excel.",
            style="Muted.TLabel",
            wraplength=640,
            justify=tk.LEFT,
        ).pack(anchor=tk.W, pady=(6, 0))

        self.generic_export_section = tk.Frame(content, bg=self.color_panel)
        ttk.Label(
            self.generic_export_section,
            text="Für diesen Befehl ist keine zusätzliche Ausgabeart erforderlich.",
            style="Muted.TLabel",
            wraplength=640,
            justify=tk.LEFT,
        ).pack(anchor=tk.W)

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
        self.step_3_card, content = self._create_step_card(self.left_column, 3, "Template / Diagramm")

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

        self.plot_template_section = tk.Frame(content, bg=self.color_panel)
        ttk.Label(self.plot_template_section, text="Ausgewähltes Template", style="Dark.TLabel").pack(
            anchor=tk.W,
            pady=(0, 6),
        )
        self.plot_template_selected_label = ttk.Label(
            self.plot_template_section,
            textvariable=self.plot_template,
            style="Heading.TLabel",
        )
        self.plot_template_selected_label.pack(anchor=tk.W, pady=(0, 8))
        self.plot_template_note = ttk.Label(
            self.plot_template_section,
            text="single erzeugt je Variante-Raum-Kombination eine eigene Ausgabe. compare führt die Auswahl in einer gemeinsamen Ausgabe zusammen.",
            style="Muted.TLabel",
            wraplength=640,
            justify=tk.LEFT,
        )
        self.plot_template_note.pack(anchor=tk.W, pady=(8, 0))

        self.overlay_toggle = ttk.Checkbutton(
            self.plot_template_section,
            text="Overlay aktivieren",
            variable=self.overlay_enabled,
            command=self._update_dynamic_fields,
            style="TCheckbutton",
        )
        self.overlay_toggle.pack(anchor=tk.W, pady=(14, 0))

        self.diagram_adjustment_button = tk.Label(
            self.plot_template_section,
            text="> Diagrammanpassung",
            bg=self.color_panel,
            fg=self.color_text,
            cursor="hand2",
            font=("Segoe UI", 10, "underline"),
        )
        self.diagram_adjustment_button.bind("<Button-1>", lambda _event: self._toggle_diagram_adjustment())
        self.diagram_adjustment_button.pack(anchor=tk.W, pady=(14, 8))
        self.diagram_adjustment_frame = tk.Frame(
            self.plot_template_section,
            bg=self.color_panel_light,
            highlightbackground=self.color_border,
            highlightthickness=1,
        )
        self.diagram_adjustment_expanded = False
        adjustment_content = tk.Frame(self.diagram_adjustment_frame, bg=self.color_panel_light)
        adjustment_content.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)
        ttk.Label(adjustment_content, text="Primäre Y-Achse", style="Dark.TLabel").pack(anchor=tk.W)
        _, self.primary_axis_mode_buttons = self._create_selection_button_group(
            adjustment_content,
            [("automatic", "Automatisch"), ("manual", "Manuell")],
            self._set_primary_axis_mode,
        )
        primary_grid = tk.Frame(adjustment_content, bg=self.color_panel_light)
        primary_grid.pack(fill=tk.X, pady=(6, 10))
        primary_grid.grid_columnconfigure(0, weight=1)
        primary_grid.grid_columnconfigure(1, weight=1)
        self.primary_ymin_entry = self._create_labeled_entry(
            primary_grid,
            "Primär Minimum",
            self.primary_ymin,
            row=0,
            column=0,
        )
        self.primary_ymax_entry = self._create_labeled_entry(
            primary_grid,
            "Primär Maximum",
            self.primary_ymax,
            row=0,
            column=1,
        )
        ttk.Label(adjustment_content, text="Sekundäre Y-Achse", style="Dark.TLabel").pack(anchor=tk.W)
        _, self.secondary_axis_mode_buttons = self._create_selection_button_group(
            adjustment_content,
            [("automatic", "Automatisch"), ("manual", "Manuell")],
            self._set_secondary_axis_mode,
        )
        secondary_grid = tk.Frame(adjustment_content, bg=self.color_panel_light)
        secondary_grid.pack(fill=tk.X, pady=(6, 10))
        secondary_grid.grid_columnconfigure(0, weight=1)
        secondary_grid.grid_columnconfigure(1, weight=1)
        self.plot_temperature_ymin_entry = self._create_labeled_entry(
            secondary_grid,
            "Sekundär Minimum",
            self.plot_temperature_ymin,
            row=0,
            column=0,
        )
        self.plot_temperature_ymax_entry = self._create_labeled_entry(
            secondary_grid,
            "Sekundär Maximum",
            self.plot_temperature_ymax,
            row=0,
            column=1,
        )
        for entry in (
            self.primary_ymin_entry,
            self.primary_ymax_entry,
            self.plot_temperature_ymin_entry,
            self.plot_temperature_ymax_entry,
        ):
            entry.bind("<KeyRelease>", lambda _event: self._redraw_axis_mockup())
        self.axis_mockup = tk.Canvas(
            adjustment_content,
            height=210,
            bg="white",
            highlightbackground=self.color_border,
            highlightthickness=1,
        )
        self.axis_mockup.pack(fill=tk.X, pady=(12, 0))

    def _get_fixed_plot_overlay(self, overlay_id, fallback=None):
        for overlay in self.fixed_plot_overlays:
            if isinstance(overlay, dict) and overlay.get("id") == overlay_id:
                return overlay
        return fallback or {}

    def _format_fixed_overlay_source(self, overlay):
        source = overlay.get("source", "")
        column = overlay.get("column", "")
        if source == "aux":
            return f"REPORT-AUX.prn:{column}"
        if source == "csv":
            fallback_columns = overlay.get("fallback_columns", [])
            if fallback_columns:
                return f"{column}, Fallback {', '.join(fallback_columns)}"
            return column
        return column

    def _build_overlay_step(self):
        self.overlay_card, content = self._create_step_card(self.left_column, 4, "Überlagerungen")
        self.overlay_reference_label = ttk.Label(
            content,
            text="Der Overlay-Katalog wird nach Varianten- und Raumauswahl geladen.",
            style="Muted.TLabel",
            wraplength=640,
            justify=tk.LEFT,
        )
        self.overlay_reference_label.pack(anchor=tk.W, pady=(0, 12))

        fixed_section = tk.Frame(content, bg=self.color_panel)
        fixed_section.pack(fill=tk.X, pady=(0, 14))
        ttk.Label(fixed_section, text="Feste Linien", style="Dark.TLabel").pack(anchor=tk.W, pady=(0, 8))

        heat_row = tk.Frame(
            fixed_section, bg=self.color_panel_light, highlightbackground=self.color_border, highlightthickness=1
        )
        heat_row.pack(fill=tk.X, pady=3)
        ttk.Label(heat_row, text="Heizleistung [W]", style="Dark.TLabel").pack(anchor=tk.W, padx=10, pady=(8, 2))
        ttk.Label(heat_row, text="Pflichtlinie auf der linken Achse", style="Muted.TLabel").pack(
            anchor=tk.W,
            padx=10,
            pady=(0, 8),
        )

        self.setpoint_row = tk.Frame(
            fixed_section, bg=self.color_panel_light, highlightbackground=self.color_border, highlightthickness=1
        )
        self.setpoint_row.pack(fill=tk.X, pady=3)
        ttk.Checkbutton(
            self.setpoint_row,
            text="Sollwertband",
            variable=self.plot_show_setpoint_band,
            command=self._update_dynamic_fields,
            style="TCheckbutton",
        ).pack(anchor=tk.W, padx=10, pady=(8, 4))
        setpoint_grid = tk.Frame(self.setpoint_row, bg=self.color_panel_light)
        setpoint_grid.pack(fill=tk.X, padx=10, pady=(0, 8))
        setpoint_grid.grid_columnconfigure(0, weight=1)
        setpoint_grid.grid_columnconfigure(1, weight=1)
        self.plot_setpoint_min_entry = self._create_labeled_entry(
            setpoint_grid,
            "Min [°C]",
            self.plot_setpoint_min,
            row=0,
            column=0,
        )
        self.plot_setpoint_max_entry = self._create_labeled_entry(
            setpoint_grid,
            "Max [°C]",
            self.plot_setpoint_max,
            row=0,
            column=1,
        )

        outdoor_overlay = self._get_fixed_plot_overlay(
            OUTDOOR_OVERLAY_ID,
            {"label": "Außenlufttemperatur", "source": "aux", "column": DEFAULT_OUTDOOR_COLUMN},
        )
        operative_overlay = self._get_fixed_plot_overlay(
            OPERATIVE_OVERLAY_ID,
            {
                "label": "Operative Temperatur",
                "source": "csv",
                "column": "temperatures_top",
                "fallback_columns": ["local_de_comf_diag_t_top"],
            },
        )
        fixed_overlay_rows = [
            (
                outdoor_overlay.get("label", "Außenlufttemperatur"),
                self.plot_show_outdoor_temperature,
                f"{self._format_fixed_overlay_source(outdoor_overlay)}, rechte Achse",
            ),
            (
                operative_overlay.get("label", "Operative Temperatur"),
                self.plot_show_operative_temperature,
                f"{self._format_fixed_overlay_source(operative_overlay)}, rechte Achse",
            ),
        ]
        for label_text, variable, detail in fixed_overlay_rows:
            row = tk.Frame(
                fixed_section,
                bg=self.color_panel_light,
                highlightbackground=self.color_border,
                highlightthickness=1,
            )
            row.pack(fill=tk.X, pady=3)
            ttk.Checkbutton(
                row,
                text=label_text,
                variable=variable,
                command=self._update_dynamic_fields,
                style="TCheckbutton",
            ).pack(anchor=tk.W, padx=10, pady=(8, 2))
            ttk.Label(row, text=detail, style="Muted.TLabel").pack(anchor=tk.W, padx=10, pady=(0, 8))

        free_section = tk.Frame(content, bg=self.color_panel)
        free_section.pack(fill=tk.BOTH, expand=True)
        ttk.Label(free_section, text="Freie Datenlinien", style="Dark.TLabel").pack(anchor=tk.W, pady=(0, 8))

        editor = tk.Frame(free_section, bg=self.color_panel)
        editor.pack(fill=tk.X)
        for column in range(4):
            editor.grid_columnconfigure(column, weight=1)

        self.overlay_source_combo = self._create_labeled_entry(
            editor,
            "Quelle",
            self.overlay_source,
            row=0,
            column=0,
            values=["csv", "aux"],
        )
        self.overlay_source_combo.bind("<<ComboboxSelected>>", lambda _event: self._refresh_overlay_column_options())
        self.overlay_column_combo = self._create_labeled_entry(
            editor,
            "Spalte",
            self.overlay_column,
            row=0,
            column=1,
            values=[],
        )
        self.overlay_column_combo.configure(state=tk.NORMAL)
        self.overlay_column_combo.bind("<<ComboboxSelected>>", lambda _event: self._prefill_overlay_label())
        self.overlay_label_entry = self._create_labeled_entry(
            editor,
            "Anzeigename",
            self.overlay_label,
            row=0,
            column=2,
        )
        self.overlay_axis_combo = self._create_labeled_entry(
            editor,
            "Achse",
            self.overlay_axis,
            row=0,
            column=3,
            values=["temperature", "heat"],
        )

        button_row = tk.Frame(free_section, bg=self.color_panel)
        button_row.pack(fill=tk.X, pady=(8, 8))
        ttk.Button(
            button_row, text="Linie hinzufügen", style="Primary.TButton", command=self._add_free_overlay_line
        ).pack(side=tk.LEFT)
        ttk.Button(
            button_row,
            text="Linie entfernen",
            style="Secondary.TButton",
            command=self._remove_selected_free_overlay_line,
        ).pack(side=tk.LEFT, padx=(10, 0))

        self.overlay_lines_listbox = tk.Listbox(
            free_section,
            height=6,
            selectmode=tk.BROWSE,
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
        self.overlay_lines_listbox.pack(fill=tk.BOTH, expand=True)

    def _create_labeled_entry(self, parent, label_text, textvariable, row, column, values=None):
        """Erzeugt ein beschriftetes Eingabefeld im Optionsraster."""
        container = tk.Frame(parent, bg=self.color_panel)
        container.grid(row=row, column=column, sticky="ew", padx=2, pady=4)
        ttk.Label(container, text=label_text, style="Dark.TLabel").pack(anchor=tk.W, pady=(0, 4))
        if values is not None:
            widget = ttk.Combobox(container, textvariable=textvariable, values=values, state="readonly")
        else:
            widget = tk.Entry(
                container,
                textvariable=textvariable,
                bg=self.color_panel_light,
                fg=self.color_text,
                insertbackground=self.color_text,
                relief=tk.FLAT,
                highlightbackground=self.color_border,
                highlightcolor=self.color_blue,
                font=("Segoe UI", 10),
            )
        widget.pack(fill=tk.X)
        return widget

    def _build_step_4(self):
        self.step_4_card, content = self._create_step_card(self.left_column, 5, "Varianten")

        ttk.Label(content, text="Variantenauswahl", style="Dark.TLabel").pack(anchor=tk.W, pady=(0, 6))
        _, self.scope_buttons = self._create_selection_button_group(
            content,
            [
                ("Eine Variante", "Eine Variante"),
                ("Mehrere Varianten", "Mehrere Varianten"),
                ("Alle Varianten", "Alle Varianten"),
            ],
            self._set_analysis_scope,
            columns=3,
            wraplength=180,
        )

        left = tk.Frame(content, bg=self.color_panel)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 20), pady=(12, 0))

        right = tk.Frame(content, bg=self.color_panel)
        right.pack(side=tk.RIGHT, fill=tk.X, expand=True, pady=(12, 0))

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
        self.variants_listbox.bind("<<ListboxSelect>>", lambda _event: self._handle_variant_selection_changed())

        self.variant_note = ttk.Label(
            right,
            text="Es ist aktuell keine Variante ausgewaehlt. Bitte waehlen Sie mindestens eine Variante.",
            style="Muted.TLabel",
            wraplength=330,
        )
        self.variant_note.pack(anchor=tk.W)

    def _build_step_5(self):
        self.step_5_card, content = self._create_step_card(self.left_column, 6, "Raeume")

        ttk.Label(content, text="Raumauswahl", style="Dark.TLabel").pack(anchor=tk.W, pady=(0, 6))
        _, self.room_scope_buttons = self._create_selection_button_group(
            content,
            [
                ("Ein Raum", "Ein Raum"),
                ("Mehrere Räume", "Mehrere Räume"),
                ("Alle Räume", "Alle Räume"),
            ],
            self._set_room_scope,
            columns=3,
            wraplength=180,
        )

        self.step_5_left = tk.Frame(content, bg=self.color_panel)
        self.step_5_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 20), pady=(12, 0))

        self.step_5_right = tk.Frame(content, bg=self.color_panel)
        self.step_5_right.pack(side=tk.RIGHT, fill=tk.X, expand=True, pady=(12, 0))

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
        self.rooms_listbox.bind("<<ListboxSelect>>", lambda _event: self._handle_room_selection_changed())

        self.room_note = ttk.Label(
            self.step_5_right,
            text="Es ist aktuell kein Raum ausgewaehlt. Bitte waehlen Sie mindestens einen Raum.",
            style="Muted.TLabel",
            wraplength=330,
        )
        self.room_note.pack(anchor=tk.W)

    def _build_bottom_buttons(self):
        self.bottom_button_frame = tk.Frame(self.root, bg=self.color_bg)
        self.bottom_button_frame.pack(fill=tk.X, padx=22, pady=(0, 18))

        self.settings_bottom_button = ttk.Button(
            self.bottom_button_frame,
            text="settings",
            style="Secondary.TButton",
            command=self._open_tools_menu,
        )
        self.settings_bottom_button.pack(side=tk.LEFT)

        self.log_bottom_button = ttk.Button(
            self.bottom_button_frame,
            text="log",
            style="Secondary.TButton",
            command=self._open_log_view,
        )
        self.log_bottom_button.pack(side=tk.LEFT, padx=(8, 0))

        self.bottom_status_label = ttk.Label(
            self.bottom_button_frame,
            textvariable=self.status_var,
            style="Muted.TLabel",
        )
        self.bottom_status_label.pack(side=tk.LEFT, padx=(14, 0))

        self.start_button = ttk.Button(
            self.bottom_button_frame,
            text="Start",
            style="Primary.TButton",
            command=self._start_pipeline,
        )
        self.start_button.pack(side=tk.RIGHT)

        self.preview_button = ttk.Button(
            self.bottom_button_frame,
            text="Vorschau aktualisieren",
            style="Secondary.TButton",
            command=self._start_preview,
        )
        self.preview_button.pack(side=tk.RIGHT, padx=(0, 12))

        self.reset_button = ttk.Button(
            self.bottom_button_frame,
            text="Zuruecksetzen",
            style="Secondary.TButton",
            command=self._reset_fields,
        )
        self.reset_button.pack(side=tk.RIGHT, padx=(0, 12))
