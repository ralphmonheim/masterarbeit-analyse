"""Plot-Template-, Achsen- und Overlay-State der Tkinter-Analyse."""

from __future__ import annotations

from ma_analyse.analysis.components.time_windows import MONTH_NAMES
from ma_analyse.analysis.templates import (
    DEFAULT_OUTDOOR_COLUMN,
    DEFAULT_SETPOINT_MAX,
    DEFAULT_SETPOINT_MIN,
    DEFAULT_SHOW_OPERATIVE_TEMPERATURE,
    DEFAULT_SHOW_OUTDOOR_TEMPERATURE,
    DEFAULT_SHOW_SETPOINT_BAND,
    DEFAULT_TEMPERATURE_YMAX,
    DEFAULT_TEMPERATURE_YMIN,
    PLOT_TEMPLATE_CHOICES,
    get_plot_template_spec,
    list_heating_year_overlay_sources,
    template_uses_overlay_options,
    validate_template_request,
)
from ma_analyse.settings.plot_templates import get_plot_template_defaults

from .tk_compat import messagebox, tk


class TkinterAnalysisPlotTemplateStateMixin:
    """Mixin fuer ausgelagerte PipelineGUI-Methoden."""

    def _set_plot_template_mode(self, value):
        self.plot_template_mode.set(value)
        self._update_dynamic_fields()
        self._advance_after_completed_single_choice(self.prepare_export_card)

    def _select_plot_template_from_list(self):
        if not hasattr(self, "plot_template_listbox"):
            return
        selection = self.plot_template_listbox.curselection()
        if not selection:
            return
        self.plot_template.set(self.plot_template_listbox.get(selection[0]))
        self.overlay_enabled.set(False)
        self.free_overlay_lines = []
        self._update_dynamic_fields()
        self._advance_after_completed_single_choice(self.subcommand_card)

    def _set_primary_axis_mode(self, value):
        self.primary_axis_mode.set(value)
        self._update_dynamic_fields()

    def _set_secondary_axis_mode(self, value):
        self.secondary_axis_mode.set(value)
        self._update_dynamic_fields()

    def _toggle_diagram_adjustment(self):
        self.diagram_adjustment_expanded = not self.diagram_adjustment_expanded
        if self.diagram_adjustment_expanded:
            self.diagram_adjustment_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 8))
            self.diagram_adjustment_button.configure(text="v Diagrammanpassung")
        else:
            self.diagram_adjustment_frame.pack_forget()
            self.diagram_adjustment_button.configure(text="> Diagrammanpassung")
        self._redraw_axis_mockup()

    def _redraw_axis_mockup(self):
        if not hasattr(self, "axis_mockup"):
            return
        canvas = self.axis_mockup
        canvas.delete("all")
        width = max(canvas.winfo_width(), 560)
        height = max(canvas.winfo_height(), 210)
        left, right, top, bottom = 55, width - 55, 20, height - 35
        canvas.create_rectangle(left, top, right, bottom, outline="#777777")
        canvas.create_text(left, 8, text="Primäre Achse", anchor=tk.W, fill="#d62828")
        canvas.create_text(right, 8, text="Sekundäre Achse", anchor=tk.E, fill="#2563eb")
        primary_points = []
        secondary_points = []
        for index in range(13):
            x_value = left + ((right - left) * index / 12)
            primary_y = bottom - ((bottom - top) * ((index % 5) + 1) / 6)
            secondary_y = bottom - ((bottom - top) * ((index % 7) + 1) / 8)
            primary_points.extend((x_value, primary_y))
            secondary_points.extend((x_value, secondary_y))
        canvas.create_line(*primary_points, fill="#d62828", width=2, smooth=True)
        canvas.create_line(*secondary_points, fill="#2563eb", width=2, smooth=True)
        primary_text = "automatisch"
        if self.primary_axis_mode.get() == "manual":
            primary_text = f"{self.primary_ymin.get()} bis {self.primary_ymax.get()}"
        secondary_text = "automatisch"
        if self.secondary_axis_mode.get() == "manual":
            secondary_text = f"{self.plot_temperature_ymin.get()} bis {self.plot_temperature_ymax.get()}"
        canvas.create_text(left, height - 12, text=f"Primär: {primary_text}", anchor=tk.W, fill="#444444")
        canvas.create_text(right, height - 12, text=f"Sekundär: {secondary_text}", anchor=tk.E, fill="#444444")

    def _update_plot_template_mode_buttons(self):
        self._update_selection_button_group(
            self.plot_template_mode_buttons,
            self.plot_template_mode.get(),
        )

    def _sync_plot_template_list_selection(self):
        if not hasattr(self, "plot_template_listbox"):
            return
        try:
            index = PLOT_TEMPLATE_CHOICES.index(self.plot_template.get())
        except ValueError:
            return
        self.plot_template_listbox.selection_clear(0, tk.END)
        self.plot_template_listbox.selection_set(index)
        self.plot_template_listbox.see(index)

    def _update_axis_adjustment_fields(self):
        if not hasattr(self, "primary_axis_mode_buttons"):
            return
        self._update_selection_button_group(
            self.primary_axis_mode_buttons,
            self.primary_axis_mode.get(),
        )
        self._update_selection_button_group(
            self.secondary_axis_mode_buttons,
            self.secondary_axis_mode.get(),
        )
        spec = get_plot_template_spec(self.plot_template.get())
        has_secondary_axis = bool(
            spec
            and (
                spec.supports_overlays
                or spec.metric in {"energy_balance", "thermal_room_climate"}
            )
        )
        if not has_secondary_axis:
            self.secondary_axis_mode.set("automatic")
            for button in self.secondary_axis_mode_buttons.values():
                button.configure(state=tk.DISABLED)
        primary_state = tk.NORMAL if self.primary_axis_mode.get() == "manual" else tk.DISABLED
        secondary_state = (
            tk.NORMAL
            if has_secondary_axis and self.secondary_axis_mode.get() == "manual"
            else tk.DISABLED
        )
        self.primary_ymin_entry.configure(state=primary_state)
        self.primary_ymax_entry.configure(state=primary_state)
        self.plot_temperature_ymin_entry.configure(state=secondary_state)
        self.plot_temperature_ymax_entry.configure(state=secondary_state)

    def _refresh_overlay_catalog(self):
        if (
            self.command.get() != "plot-template"
            or not template_uses_overlay_options(self.plot_template.get())
            or not hasattr(self, "overlay_column_combo")
        ):
            return

        variant_name = None
        if self.variant_names:
            selected_indices = self.variants_listbox.curselection()
            if selected_indices:
                variant_name = self.variant_names[selected_indices[0]]

        room_name = None
        if self.rooms_listbox.size() > 0:
            selected_room_indices = self.rooms_listbox.curselection()
            if selected_room_indices:
                room_name = self.rooms_listbox.get(selected_room_indices[0])

        if not variant_name or not room_name:
            self.overlay_catalog = {"csv": [], "aux": []}
            if hasattr(self, "overlay_reference_label"):
                self.overlay_reference_label.configure(
                    text="Wähle mindestens eine Variante und einen Raum, um den Overlay-Katalog zu laden."
                )
            self._refresh_overlay_column_options()
            return

        if hasattr(self, "overlay_reference_label"):
            self.overlay_reference_label.configure(
                text=(
                    f"Referenz für den Overlay-Katalog: {variant_name} / {room_name}. "
                    "Weitere ausgewählte Kombinationen werden beim Start validiert."
                )
            )

        try:
            self.overlay_catalog = list_heating_year_overlay_sources(
                self.args.datenbank_dir,
                self.args.input_dir,
                variant_name,
                room_name,
                outdoor_column=self.plot_outdoor_column.get() or DEFAULT_OUTDOOR_COLUMN,
                fixed_overlays=self.fixed_plot_overlays,
            )
        except Exception:
            self.overlay_catalog = {"csv": [], "aux": []}
        self._refresh_overlay_column_options()

    def _refresh_overlay_column_options(self):
        if not hasattr(self, "overlay_column_combo"):
            return
        source = self.overlay_source.get()
        columns = self.overlay_catalog.get(source, [])
        self.overlay_column_combo.configure(values=columns)
        if columns and self.overlay_column.get() not in columns:
            self.overlay_column.set(columns[0])
            self._prefill_overlay_label()

    def _plot_template_specs_by_name(self):
        return {template: get_plot_template_spec(template) for template in PLOT_TEMPLATE_CHOICES}

    def _filtered_plot_template_choices(self):
        return list(PLOT_TEMPLATE_CHOICES)

    def _update_plot_template_choices(self):
        if not hasattr(self, "plot_template_combo"):
            return
        choices = self._filtered_plot_template_choices()
        self.plot_template_combo.configure(values=choices)
        if choices and self.plot_template.get() not in choices:
            self.plot_template.set(choices[0])
            self._active_plot_template = None

    def _load_plot_template_defaults(self, template: str | None = None):
        template = template or self.plot_template.get()
        return get_plot_template_defaults(template, self.plot_template_config_path)

    def _sync_plot_template_fields(self):
        if not hasattr(self, "plot_setpoint_min"):
            return
        self.plot_setpoint_min.set(
            str(self.plot_template_defaults.get("setpoint_min", DEFAULT_SETPOINT_MIN))
        )
        self.plot_setpoint_max.set(
            str(self.plot_template_defaults.get("setpoint_max", DEFAULT_SETPOINT_MAX))
        )
        self.plot_temperature_ymin.set(
            str(self.plot_template_defaults.get("temperature_ymin", DEFAULT_TEMPERATURE_YMIN))
        )
        self.plot_temperature_ymax.set(
            str(self.plot_template_defaults.get("temperature_ymax", DEFAULT_TEMPERATURE_YMAX))
        )
        self.plot_outdoor_column.set(
            self.plot_template_defaults.get("outdoor_column", DEFAULT_OUTDOOR_COLUMN)
        )
        self.plot_show_setpoint_band.set(
            bool(self.plot_template_defaults.get("show_setpoint_band", DEFAULT_SHOW_SETPOINT_BAND))
        )
        self.plot_show_outdoor_temperature.set(
            bool(self.plot_template_defaults.get("show_outdoor_temperature", DEFAULT_SHOW_OUTDOOR_TEMPERATURE))
        )
        self.plot_show_operative_temperature.set(
            bool(self.plot_template_defaults.get("show_operative_temperature", DEFAULT_SHOW_OPERATIVE_TEMPERATURE))
        )
        self.fixed_plot_overlays = self.plot_template_defaults.get("default_overlays", [])

    def _refresh_plot_template_defaults(self):
        template = self.plot_template.get()
        if getattr(self, "_active_plot_template", None) == template:
            return
        self.plot_template_defaults = self._load_plot_template_defaults(template)
        self.fixed_plot_overlays = self.plot_template_defaults.get("default_overlays", [])
        self._active_plot_template = template
        self._sync_plot_template_fields()

    def _prefill_overlay_label(self):
        if not self.overlay_label.get().strip():
            self.overlay_label.set(self.overlay_column.get())

    def _add_free_overlay_line(self):
        source = self.overlay_source.get()
        column = self.overlay_column.get().strip()
        axis = self.overlay_axis.get()
        label = self.overlay_label.get().strip() or column
        if source not in {"csv", "aux"} or axis not in {"heat", "temperature"} or not column:
            messagebox.showwarning("Warnung", "Bitte waehlen Sie Quelle, Spalte und Achse fuer die Datenlinie.")
            return
        if column not in self.overlay_catalog.get(source, []):
            messagebox.showwarning("Warnung", "Die gewaehlte Spalte ist fuer Variante/Raum aktuell nicht verfuegbar.")
            return
        if any(
            line["source"] == source and line["column"] == column and line["axis"] == axis
            for line in self.free_overlay_lines
        ):
            messagebox.showwarning("Warnung", "Diese Datenlinie ist bereits hinzugefuegt.")
            return

        self.free_overlay_lines.append(
            {
                "source": source,
                "column": column,
                "label": label,
                "axis": axis,
                "enabled": True,
            }
        )
        self.overlay_label.set("")
        self._sync_free_overlay_listbox()
        self._update_step_summaries()

    def _remove_selected_free_overlay_line(self):
        if not hasattr(self, "overlay_lines_listbox"):
            return
        selection = self.overlay_lines_listbox.curselection()
        if not selection:
            return
        del self.free_overlay_lines[selection[0]]
        self._sync_free_overlay_listbox()
        self._update_step_summaries()

    def _sync_free_overlay_listbox(self):
        if not hasattr(self, "overlay_lines_listbox"):
            return
        self.overlay_lines_listbox.delete(0, tk.END)
        for line in self.free_overlay_lines:
            axis_label = "Temperatur [°C]" if line["axis"] == "temperature" else "Leistung [W]"
            self.overlay_lines_listbox.insert(
                tk.END,
                f"{line['label']}  |  {line['source']}:{line['column']}  |  {axis_label}",
            )

    def _parse_float_option(self, raw_value, label):
        raw_value = raw_value.strip()
        if not raw_value:
            messagebox.showwarning("Warnung", f"Bitte geben Sie einen Wert fuer {label} ein.")
            return None
        try:
            return float(raw_value.replace(",", "."))
        except ValueError:
            messagebox.showwarning("Warnung", f"{label} muss eine Zahl sein.")
            return None

    def _get_plot_template_options(self, variants, rooms):
        template = self.plot_template.get()
        spec = get_plot_template_spec(template)
        uses_overlay_options = template_uses_overlay_options(template) and self.overlay_enabled.get()
        month = None
        week = None
        day = None

        if spec is not None and spec.view in {"month", "day"}:
            if self.heating_month.get() not in MONTH_NAMES:
                messagebox.showwarning("Warnung", "Bitte waehlen Sie einen gueltigen Monat.")
                return None
            month = self.heating_month.get()
        if spec is not None and spec.view == "week":
            week = self._parse_heating_week()
            if week is None:
                return None
        if spec is not None and spec.view == "day":
            day = self._parse_heating_day()
            if day is None:
                return None

        if uses_overlay_options and self.plot_show_setpoint_band.get():
            setpoint_min = self._parse_float_option(self.plot_setpoint_min.get(), "Sollwert min")
            if setpoint_min is None:
                return None
            setpoint_max = self._parse_float_option(self.plot_setpoint_max.get(), "Sollwert max")
            if setpoint_max is None:
                return None
        else:
            setpoint_min = self.plot_template_defaults.get("setpoint_min", DEFAULT_SETPOINT_MIN)
            setpoint_max = self.plot_template_defaults.get("setpoint_max", DEFAULT_SETPOINT_MAX)
        if self.secondary_axis_mode.get() == "manual":
            temperature_ymin = self._parse_float_option(self.plot_temperature_ymin.get(), "Temp.-Achse min")
            if temperature_ymin is None:
                return None
            temperature_ymax = self._parse_float_option(self.plot_temperature_ymax.get(), "Temp.-Achse max")
            if temperature_ymax is None:
                return None
        else:
            temperature_ymin = self.plot_template_defaults.get("temperature_ymin", DEFAULT_TEMPERATURE_YMIN)
            temperature_ymax = self.plot_template_defaults.get("temperature_ymax", DEFAULT_TEMPERATURE_YMAX)
        primary_ymin = None
        primary_ymax = None
        if self.primary_axis_mode.get() == "manual":
            primary_ymin = self._parse_float_option(self.primary_ymin.get(), "Primärachse min")
            if primary_ymin is None:
                return None
            primary_ymax = self._parse_float_option(self.primary_ymax.get(), "Primärachse max")
            if primary_ymax is None:
                return None
            if primary_ymin >= primary_ymax:
                messagebox.showwarning("Warnung", "Primärachse min muss kleiner als max sein.")
                return None
        if self.secondary_axis_mode.get() == "manual" and temperature_ymin >= temperature_ymax:
            messagebox.showwarning("Warnung", "Sekundärachse min muss kleiner als max sein.")
            return None

        options = {
            "template": template,
            "output_mode": self.plot_template_mode.get(),
            "setpoint_min": setpoint_min,
            "setpoint_max": setpoint_max,
            "temperature_ymin": temperature_ymin,
            "temperature_ymax": temperature_ymax,
            "outdoor_column": self.plot_outdoor_column.get().strip() or DEFAULT_OUTDOOR_COLUMN,
            "show_setpoint_band": self.plot_show_setpoint_band.get() if uses_overlay_options else False,
            "show_outdoor_temperature": self.plot_show_outdoor_temperature.get() if uses_overlay_options else False,
            "show_operative_temperature": self.plot_show_operative_temperature.get() if uses_overlay_options else False,
            "overlay_lines": [line.copy() for line in self.free_overlay_lines] if uses_overlay_options else [],
            "fixed_overlays": self.fixed_plot_overlays if uses_overlay_options else [],
            "month": month,
            "week": week,
            "day": day,
            "primary_axis_mode": self.primary_axis_mode.get(),
            "primary_ymin": primary_ymin,
            "primary_ymax": primary_ymax,
            "secondary_axis_mode": self.secondary_axis_mode.get(),
            "secondary_ymin": temperature_ymin if self.secondary_axis_mode.get() == "manual" else None,
            "secondary_ymax": temperature_ymax if self.secondary_axis_mode.get() == "manual" else None,
        }
        errors = validate_template_request(
            options["template"],
            variants,
            rooms[:1],
            options["setpoint_min"],
            options["setpoint_max"],
            options["temperature_ymin"],
            options["temperature_ymax"],
            validate_setpoint_band=options["show_setpoint_band"],
            month=month,
            week=week,
            day=day,
        )
        if errors:
            messagebox.showwarning("Warnung", "\n".join(errors))
            return None
        return options
