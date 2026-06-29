"""Initialisierung des Tkinter-Analysezustands."""

from __future__ import annotations

from ma_analyse.analysis.components.time_windows import MONTH_NAMES
from ma_analyse.analysis.templates import (
    DEFAULT_OUTDOOR_COLUMN,
    DEFAULT_SETPOINT_MAX,
    DEFAULT_SETPOINT_MIN,
    DEFAULT_TEMPERATURE_YMAX,
    DEFAULT_TEMPERATURE_YMIN,
    HEATING_YEAR_TEMPLATE,
)
from ma_analyse.settings.formats import ensure_output_format_doc
from ma_analyse.settings.naming import LEGACY_MAPPING_DOC as NAMENSMAPPING_DOC
from ma_analyse.settings.plot_templates import get_plot_template_defaults

from .constants import DEFAULT_COMMAND
from .dialogs import OUTPUT_FORMAT_DOC
from .tk_compat import tk


class TkinterAnalysisInitialStateMixin:
    """Kapselt den langen Startzustand der Pipeline-GUI."""

    def _initialize_pipeline_gui(self, root, args, singleton_controller=None, refresh_port=None):
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
            "plot-template": ["plot_template"],
            "all": ["overview", "analysis", "heating", "cooling"],
        }
        self.commands = list(self.command_to_steps.keys())
        self.plot_template_config_path = getattr(args, "plot_template_config", None)
        self.plot_template = tk.StringVar(value=getattr(args, "template", HEATING_YEAR_TEMPLATE))
        self.plot_template_defaults = get_plot_template_defaults(
            self.plot_template.get(),
            self.plot_template_config_path,
        )
        self.fixed_plot_overlays = self.plot_template_defaults.get("default_overlays", [])

        self.analysis_scope = tk.StringVar(value="")
        self.room_scope = tk.StringVar(value="")
        self.command = tk.StringVar(value=getattr(args, "command", DEFAULT_COMMAND) or DEFAULT_COMMAND)
        self.prepare_export_format = tk.StringVar(value="")
        self.comfort_type = tk.StringVar(value="")
        self.analysis_level = tk.StringVar(value="")
        self.load_subcommand = tk.StringVar(value="")
        self.plot_template_mode = tk.StringVar(value="")
        self.overlay_enabled = tk.BooleanVar(value=False)
        self.primary_axis_mode = tk.StringVar(value="automatic")
        self.secondary_axis_mode = tk.StringVar(value="automatic")
        self.primary_ymin = tk.StringVar(value="0")
        self.primary_ymax = tk.StringVar(value="1000")
        self.heating_mode = tk.StringVar(value="")
        self.heating_view = tk.StringVar(value="")
        self.heating_series_layout = tk.StringVar(value="")
        self.heating_month = tk.StringVar(value=MONTH_NAMES[0])
        self.heating_week = tk.StringVar(value="1")
        self.heating_day = tk.StringVar(value="1")
        self.plot_setpoint_min = tk.StringVar(
            value=str(
                getattr(args, "setpoint_min", self.plot_template_defaults.get("setpoint_min", DEFAULT_SETPOINT_MIN))
            )
        )
        self.plot_setpoint_max = tk.StringVar(
            value=str(
                getattr(args, "setpoint_max", self.plot_template_defaults.get("setpoint_max", DEFAULT_SETPOINT_MAX))
            )
        )
        self.plot_temperature_ymin = tk.StringVar(
            value=str(
                getattr(
                    args,
                    "temperature_ymin",
                    self.plot_template_defaults.get("temperature_ymin", DEFAULT_TEMPERATURE_YMIN),
                )
            )
        )
        self.plot_temperature_ymax = tk.StringVar(
            value=str(
                getattr(
                    args,
                    "temperature_ymax",
                    self.plot_template_defaults.get("temperature_ymax", DEFAULT_TEMPERATURE_YMAX),
                )
            )
        )
        self.plot_outdoor_column = tk.StringVar(
            value=getattr(
                args, "outdoor_column", self.plot_template_defaults.get("outdoor_column", DEFAULT_OUTDOOR_COLUMN)
            )
        )
        self.plot_show_setpoint_band = tk.BooleanVar(value=False)
        self.plot_show_outdoor_temperature = tk.BooleanVar(value=False)
        self.plot_show_operative_temperature = tk.BooleanVar(value=False)
        self.overlay_source = tk.StringVar(value="")
        self.overlay_column = tk.StringVar(value="")
        self.overlay_label = tk.StringVar(value="")
        self.overlay_axis = tk.StringVar(value="")

        self.selected_steps = []
        self.selected_variants = []
        self.selected_rooms = []
        self.selected_load_subcommand = ""
        self.selected_heating_mode = ""
        self.selected_heating_view = ""
        self.selected_heating_series_layout = ""
        self.selected_prepare_export_format = ""
        self.selected_month = MONTH_NAMES[0]
        self.selected_week = 1
        self.selected_day = 1
        self.selected_comfort_type = ""
        self.selected_plot_template_options = {}
        self.selected_plot_single = True
        self.selected_plot_overview = True
        self.selected_analysis_individual = True
        self.selected_analysis_overview = True
        self.free_overlay_lines = []
        self.overlay_catalog = {"csv": [], "aux": []}

        self.comfort_allowed_by_level = {
            "Analyse Raum": {"plot", "plot_analysis", "plot_overview", "plot_analysis_overview"},
            "Analyse Variante": {"plot", "plot_analysis", "plot_overview", "plot_analysis_overview"},
        }
        self.comfort_default_by_level = {
            "Analyse Raum": "plot",
            "Analyse Variante": "plot_overview",
        }
        self.last_variant_scope = None

        self.variant_names = []
        self.variant_source_kind = None
        self.active_step_card = None
        self.left_scroll_window = None
        self.right_scroll_window = None
        self.right_scrollbar_visible = False
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
