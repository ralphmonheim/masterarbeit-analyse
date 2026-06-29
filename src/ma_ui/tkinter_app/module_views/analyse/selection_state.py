"""Auswahl- und Button-State der Tkinter-Analyse."""

from __future__ import annotations

from ma_analyse.analysis.components.time_windows import MAX_CALENDAR_WEEK, MONTH_DAY_COUNTS, MONTH_NAMES
from ma_analyse.analysis.templates import (
    DEFAULT_OUTDOOR_COLUMN,
    DEFAULT_SETPOINT_MAX,
    DEFAULT_SETPOINT_MIN,
    DEFAULT_TEMPERATURE_YMAX,
    DEFAULT_TEMPERATURE_YMIN,
    HEATING_YEAR_TEMPLATE,
    get_plot_template_spec,
    is_time_filtered_template,
    template_uses_overlay_options,
)
from ma_analyse.core.config import DATENBANK_DIR, INPUT_DIR, ROOMS

from .constants import DISABLED_GUI_COMMANDS
from .selection import (
    list_datenbank_variants,
    list_input_variants,
    resolve_variant_list_state,
    strip_variant_suffix,
)
from .tk_compat import messagebox, tk


class TkinterAnalysisSelectionStateMixin:
    """Mixin fuer ausgelagerte PipelineGUI-Methoden."""

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

    def _select_all_rooms(self):
        self.rooms_listbox.configure(state=tk.NORMAL)
        self.rooms_listbox.selection_set(0, tk.END)

    def _set_analysis_scope(self, value):
        self.analysis_scope.set(value)
        self._update_dynamic_fields()

    def _set_room_scope(self, value):
        self.room_scope.set(value)
        self._update_dynamic_fields()
        self._activate_step(self.step_5_card)

    def _set_command(self, value):
        if value in DISABLED_GUI_COMMANDS:
            return
        self.command.set(value)
        self.load_subcommand.set("")
        self.plot_template_mode.set("")
        self.overlay_enabled.set(False)
        self.primary_axis_mode.set("automatic")
        self.secondary_axis_mode.set("automatic")
        self.primary_ymin.set("0")
        self.primary_ymax.set("1000")
        self._update_dynamic_fields()
        self._activate_next_available_step_after(self.step_2_card)

    def _set_prepare_export_format(self, value):
        self.prepare_export_format.set(value)
        self._update_dynamic_fields()
        self._advance_after_completed_single_choice(self.prepare_export_card)

    def _set_analysis_level(self, value):
        self.analysis_level.set(value)
        self._update_dynamic_fields()
        self._advance_after_completed_single_choice(self.step_3_card)

    def _set_heating_mode(self, value):
        self.heating_mode.set(value)
        self._update_dynamic_fields()
        self._advance_after_completed_single_choice(self.prepare_export_card)

    def _set_heating_series_layout(self, value):
        self.heating_series_layout.set(value)
        self._update_dynamic_fields()
        self._advance_after_completed_single_choice(self.prepare_export_card)

    def _set_load_subcommand(self, value):
        self.load_subcommand.set(value)
        if value == "bar":
            self.heating_view.set("bar")
        elif value == "timeline" and self.heating_view.get() == "bar":
            self.heating_view.set("")
        self._update_dynamic_fields()
        self._advance_after_completed_single_choice(self.subcommand_card)

    def _set_comfort_type(self, value):
        self.comfort_type.set(value)
        self._update_dynamic_fields()
        self._advance_after_completed_single_choice(self.subcommand_card)

    def _set_heating_view(self, value):
        self.heating_view.set(value)
        self._update_dynamic_fields()
        self._advance_after_completed_single_choice(self.step_3_card)

    def _update_dynamic_fields(self):
        self._update_plot_template_choices()
        self._refresh_plot_template_defaults()
        self._populate_variants()
        self._update_scope_buttons()
        self._update_room_scope_buttons()
        self._update_command_buttons()
        self._update_prepare_export_buttons()
        self._update_analysis_level_buttons()
        self._update_heating_mode_buttons()
        self._update_heating_layout_buttons()
        self._update_load_subcommand_buttons()
        self._sync_plot_template_list_selection()
        self._update_plot_template_mode_buttons()
        self._update_heating_view_buttons()
        self._update_axis_adjustment_fields()
        self._update_step_visibility()
        self._update_subcommand_dependent_fields()
        self._update_command_dependent_fields()
        self._update_prepare_export_note()
        self._update_comfort_options_for_analysis_level()
        self._update_heating_detail_fields()
        self._update_variant_field()
        self._update_room_field()
        self._refresh_overlay_catalog()
        self._refresh_step_indicators()
        self._update_step_summaries()
        self._redraw_axis_mockup()

    def _update_scope_buttons(self):
        for scope, button in self.scope_buttons.items():
            if self.analysis_scope.get() == scope:
                button.configure(bg=self.color_blue, fg="white")
            else:
                button.configure(bg=self.color_panel_light, fg=self.color_text)

    def _update_room_scope_buttons(self):
        for scope, button in self.room_scope_buttons.items():
            if self.room_scope.get() == scope:
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
        if hasattr(self, "analysis_export_buttons"):
            self._update_selection_button_group(
                self.analysis_export_buttons,
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
        if hasattr(self, "prepare_export_section"):
            self.prepare_export_section.pack_forget()
        if hasattr(self, "plot_template_export_section"):
            self.plot_template_export_section.pack_forget()
        if hasattr(self, "load_export_section"):
            self.load_export_section.pack_forget()
        if hasattr(self, "analysis_export_section"):
            self.analysis_export_section.pack_forget()
        if hasattr(self, "generic_export_section"):
            self.generic_export_section.pack_forget()

        if self.command.get() == "plot-template":
            self.plot_template_export_section.pack(fill=tk.X)
            return

        if self.command.get() in {"heating", "cooling"}:
            self.load_export_title.configure(
                text="Kühlvergleich Ausgabemodus"
                if self.command.get() == "cooling"
                else "Heizvergleich Ausgabemodus"
            )
            self.load_export_section.pack(fill=tk.X)
            if self.heating_mode.get() == "compare":
                self.load_layout_title.pack(anchor=tk.W, pady=(8, 6))
                for button in self.heating_layout_buttons.values():
                    button.master.pack(fill=tk.X)
                    break
                self.load_layout_note.pack(anchor=tk.W, pady=(6, 0))
            else:
                self.load_layout_title.pack_forget()
                if self.heating_layout_buttons:
                    next(iter(self.heating_layout_buttons.values())).master.pack_forget()
                self.load_layout_note.pack_forget()
            return

        if self.command.get() == "analyze_data":
            self.analysis_export_section.pack(fill=tk.X)
            return

        if self.command.get() != "prepare":
            self.generic_export_section.pack(fill=tk.X)
            return

        self.prepare_export_section.pack(fill=tk.X)
        selected_format = self.prepare_export_format.get()
        if selected_format == "csv":
            self.prepare_export_note.configure(text="CSV ist das operative Standardformat fuer die Folgeskripte.")
            return
        if selected_format == "excel":
            self.prepare_export_note.configure(
                text="Excel dient aktuell nur der uebersichtlicheren Darstellung. Die Folgeskripte verwenden weiterhin CSV-Dateien."
            )
            return
        if selected_format == "both":
            self.prepare_export_note.configure(
                text="CSV + Excel erzeugt operative CSV-Dateien fuer die Pipeline und zusaetzlich XLSX-Dateien zur Ansicht."
            )
            return
        self.prepare_export_note.configure(text="Bitte waehlen Sie ein Exportformat.")

    def _update_subcommand_dependent_fields(self):
        selected_command = self.command.get()
        for section in [
            self.comfort_section,
            self.load_subcommand_section,
            self.plot_template_list_section,
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
            return

        if selected_command == "plot-template":
            self.plot_template_list_section.pack(fill=tk.X)

    def _update_command_dependent_fields(self):
        selected_command = self.command.get()
        steps = self.command_to_steps.get(selected_command, [])

        prepare_active = selected_command == "prepare"
        analyze_active = selected_command == "analyze_data"
        all_active = selected_command == "all"
        heating_active = "heating" in steps
        cooling_active = "cooling" in steps
        load_active = heating_active or cooling_active

        for section in [
            self.heating_mode_section,
            self.heating_layout_section,
            self.analysis_section,
            self.heating_view_section,
            self.plot_template_section,
        ]:
            section.pack_forget()

        if not selected_command:
            return

        if all_active:
            return

        if load_active:
            self._set_time_view_buttons_visible(True)
            self.load_mode_title.configure(text="Kuehlvergleich Modus" if cooling_active else "Heizvergleich Modus")
            self.load_view_title.configure(
                text="Kuehlvergleich Ansichten" if cooling_active else "Heizvergleich Ansichten"
            )
            self.heating_layout_title.configure(text="Diagrammausgabe")
            if self.load_subcommand.get() not in {"bar", "timeline"}:
                return
            if self.load_subcommand.get() == "timeline":
                self.heating_view_section.pack(fill=tk.X)
            return

        if selected_command == "plot-template":
            self._update_plot_template_choices()
            self.plot_template_section.pack(fill=tk.X)
            spec = get_plot_template_spec(self.plot_template.get())
            if template_uses_overlay_options(self.plot_template.get()):
                self.overlay_toggle.pack(anchor=tk.W, pady=(14, 0))
            else:
                self.overlay_enabled.set(False)
                self.overlay_toggle.pack_forget()
            if spec is not None and is_time_filtered_template(self.plot_template.get()):
                if self.heating_view.get() != spec.view:
                    self.heating_view.set(spec.view)
                self.load_view_title.configure(text="Template-Zeitwahl")
                self._set_time_view_buttons_visible(False)
                self.heating_view_section.pack(fill=tk.X, pady=(12, 0))
            return

        if analyze_active:
            return

        if prepare_active:
            return

        self.analysis_section.pack(fill=tk.X)

    def _set_time_view_buttons_visible(self, visible):
        buttons_visible = bool(self.heating_time_view_buttons_section.winfo_manager())
        if visible and not buttons_visible:
            self.heating_time_view_buttons_section.pack(
                side=tk.LEFT,
                fill=tk.BOTH,
                expand=True,
                padx=(0, 20),
                before=self.heating_view_detail_section,
            )
            return
        if not visible and buttons_visible:
            self.heating_time_view_buttons_section.pack_forget()

    def _update_comfort_options_for_analysis_level(self):
        self._update_selection_button_group(
            self.comfort_type_widgets,
            self.comfort_type.get(),
        )

    def _update_heating_detail_fields(self):
        selected_view = self.heating_view.get()
        if self.command.get() == "plot-template":
            spec = get_plot_template_spec(self.plot_template.get())
            if spec is not None:
                selected_view = spec.view
            load_label = "Template-Zeitansicht"
        else:
            load_label = "Kuehlansicht" if self.command.get() == "cooling" else "Heizansicht"
        self.heating_month_container.pack_forget()
        self.heating_week_container.pack_forget()
        self.heating_day_container.pack_forget()

        month_index = MONTH_NAMES.index(self.heating_month.get())
        valid_days = [str(day) for day in range(1, MONTH_DAY_COUNTS[month_index] + 1)]
        self.heating_day_combo.configure(values=valid_days)
        if self.heating_day.get() not in valid_days:
            self.heating_day.set(valid_days[0])

        if not selected_view:
            self.heating_view_note.configure(text="Bitte waehlen Sie eine Zeitansicht.")
            return

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
        state = resolve_variant_list_state(
            len(self.variant_names),
            scope,
            current_selection=self.variants_listbox.curselection(),
            previous_scope=previous_scope,
        )
        selectmode = tk.BROWSE if state.selectmode == "browse" else tk.MULTIPLE
        widget_state = tk.NORMAL if state.enabled else tk.DISABLED
        self.variants_listbox.configure(state=tk.NORMAL, selectmode=selectmode)
        self.variants_listbox.selection_clear(0, tk.END)
        for index in state.selected_indices:
            self.variants_listbox.selection_set(index)
        self.variants_listbox.configure(state=widget_state)
        self._update_variant_note_state(scope)
        self.last_variant_scope = scope

    def _update_variant_note_state(self, scope):
        if not self.variant_names:
            return

        if not scope:
            self.variant_note.configure(text="Bitte waehlen Sie zuerst den Analyseumfang.")
            return

        if self.command.get() == "prepare":
            if scope == "Alle Varianten":
                self.variant_note.configure(
                    text=f"Alle IDA-Import-Varianten aus {INPUT_DIR} sind aktiv und werden vorbereitet."
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
                text="Mehrere IDA-Import-Varianten sind aktiv. Es werden nur die ausgewaehlten Varianten vorbereitet."
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
        if self.command.get() == "prepare":
            return

        scope = self.room_scope.get()
        self._set_step_5_enabled(True)
        if not scope:
            self.rooms_listbox.configure(state=tk.DISABLED, selectmode=tk.MULTIPLE)
            self.room_note.configure(text="Bitte waehlen Sie zuerst den Raumumfang.")
            return

        if scope == "Alle Räume":
            self.rooms_listbox.configure(state=tk.NORMAL, selectmode=tk.MULTIPLE)
            self.rooms_listbox.selection_set(0, tk.END)
            self.rooms_listbox.configure(state=tk.DISABLED, selectmode=tk.MULTIPLE)
            self.room_note.configure(
                text="Alle bekannten Räume werden verwendet: bei single getrennt, bei compare gemeinsam."
            )
            return

        selectmode = tk.BROWSE if scope == "Ein Raum" else tk.MULTIPLE
        self.rooms_listbox.configure(state=tk.NORMAL, selectmode=selectmode)
        self._update_room_note_state(scope)

    def _set_step_5_enabled(self, enabled):
        card_bg = self.color_panel if enabled else self.color_panel_light
        header_bg = self.color_panel if enabled else self.color_panel_light
        number_bg = self.color_border
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
        if level == "Ein Raum":
            if not self.rooms_listbox.curselection():
                self.room_note.configure(text="Es ist aktuell kein Raum ausgewaehlt. Bitte waehlen Sie einen Raum.")
                return
            self.room_note.configure(text="Ein Raum ist aktiv. Es wird genau dieser Raum verwendet.")
            return

        if level == "Mehrere Räume":
            if not self.rooms_listbox.curselection():
                self.room_note.configure(
                    text="Es ist aktuell kein Raum ausgewaehlt. Bitte waehlen Sie mindestens einen Raum."
                )
                return
            self.room_note.configure(text="Mehrere Raeume sind aktiv. Es werden die ausgewaehlten Raeume verwendet.")
            return

        if level == "Alle Räume":
            self.room_note.configure(text="Alle bekannten Raeume werden verwendet.")
            return

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

    def _handle_variant_selection_changed(self):
        if self.command.get() == "plot-template":
            self._update_variant_note_state(self.analysis_scope.get())
        else:
            self._update_variant_note_state(self.analysis_scope.get())
        self._refresh_overlay_catalog()
        self._update_step_summaries()

    def _handle_room_selection_changed(self):
        if self.command.get() == "plot-template":
            self.room_note.configure(
                text="Alle ausgewählten Räume werden verarbeitet: bei single getrennt, bei compare gemeinsam."
            )
        else:
            self._update_room_note_state(self.room_scope.get())
        self._refresh_overlay_catalog()
        self._update_step_summaries()

    def _reset_fields(self):
        self.analysis_scope.set("")
        self.room_scope.set("")
        self.command.set("")
        self.prepare_export_format.set("")
        self.comfort_type.set("")
        self.analysis_level.set("")
        self.load_subcommand.set("")
        self.plot_template_mode.set("")
        self.overlay_enabled.set(False)
        self.primary_axis_mode.set("automatic")
        self.secondary_axis_mode.set("automatic")
        self.primary_ymin.set("0")
        self.primary_ymax.set("1000")
        self.heating_mode.set("")
        self.heating_view.set("")
        self.heating_series_layout.set("")
        self.heating_month.set(MONTH_NAMES[0])
        self.heating_week.set("1")
        self.heating_day.set("1")
        self.plot_template.set(HEATING_YEAR_TEMPLATE)
        self.plot_setpoint_min.set(str(self.plot_template_defaults.get("setpoint_min", DEFAULT_SETPOINT_MIN)))
        self.plot_setpoint_max.set(str(self.plot_template_defaults.get("setpoint_max", DEFAULT_SETPOINT_MAX)))
        self.plot_temperature_ymin.set(
            str(self.plot_template_defaults.get("temperature_ymin", DEFAULT_TEMPERATURE_YMIN))
        )
        self.plot_temperature_ymax.set(
            str(self.plot_template_defaults.get("temperature_ymax", DEFAULT_TEMPERATURE_YMAX))
        )
        self.plot_outdoor_column.set(self.plot_template_defaults.get("outdoor_column", DEFAULT_OUTDOOR_COLUMN))
        self.plot_show_setpoint_band.set(False)
        self.plot_show_outdoor_temperature.set(False)
        self.plot_show_operative_temperature.set(False)
        self.overlay_source.set("")
        self.overlay_column.set("")
        self.overlay_label.set("")
        self.overlay_axis.set("")
        self.free_overlay_lines = []

        self.variants_listbox.selection_clear(0, tk.END)
        self.rooms_listbox.selection_clear(0, tk.END)

        self.selected_comfort_type = ""
        self.selected_prepare_export_format = ""
        self.selected_load_subcommand = ""
        self.selected_heating_mode = ""
        self.selected_heating_view = ""
        self.selected_heating_series_layout = ""
        self.selected_month = MONTH_NAMES[0]
        self.selected_week = 1
        self.selected_day = 1
        self.selected_plot_template_options = {}
        self._sync_free_overlay_listbox()

        self._update_dynamic_fields()
        self._activate_first_available_step()

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
        if self.command.get() == "plot-template":
            selected_indices = self.variants_listbox.curselection()
            return [self.variant_names[index] for index in selected_indices]
        selected_indices = self.variants_listbox.curselection()
        return [self.variant_names[index] for index in selected_indices]

    def _get_selected_rooms(self):
        if self.command.get() == "prepare":
            return ROOMS.copy()
        if self.room_scope.get() == "Alle Räume":
            return ROOMS.copy()
        selected_indices = self.rooms_listbox.curselection()
        rooms = [self.rooms_listbox.get(index) for index in selected_indices]
        return rooms

    def _validate_variant_sources(self, steps, variants):
        if not variants:
            messagebox.showwarning("Warnung", "Bitte waehlen Sie mindestens eine Variante.")
            return False

        return True
