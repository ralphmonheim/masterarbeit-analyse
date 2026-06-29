"""Wizard-Fluss und Schrittnavigation der Tkinter-Analyse."""

from __future__ import annotations

from ma_analyse.analysis.templates import (
    PLOT_TEMPLATE_CHOICES,
    get_plot_template_spec,
    template_uses_overlay_options,
)

from .tk_compat import tk


class TkinterAnalysisStepFlowMixin:
    """Mixin fuer ausgelagerte PipelineGUI-Methoden."""

    def _build_right_column(self):
        self.run_log_text = None
        self.steps_list_container = None
        self._activate_first_available_step()

    def _refresh_step_indicators(self):
        visible_cards = [card for card in self.step_card_order if getattr(card, "step_available", True)]

        for index, card in enumerate(visible_cards, start=1):
            card.step_number_label.configure(text=str(index))

        if self.active_step_card not in visible_cards:
            self._activate_first_available_step()
        else:
            self._update_step_nav_styles()

    def _activate_first_available_step(self):
        for card in getattr(self, "step_card_order", []):
            if getattr(card, "step_available", True):
                self._activate_step(card)
                return

    def _activate_next_available_step_after(self, current_card):
        try:
            current_index = self.step_card_order.index(current_card)
        except ValueError:
            return

        for card in self.step_card_order[current_index + 1 :]:
            if getattr(card, "step_available", True) and card.step_nav.winfo_manager() == "pack":
                self._activate_step(card)
                return

    def _advance_after_completed_single_choice(self, current_card):
        if self._is_single_choice_step_complete(current_card):
            self._activate_next_available_step_after(current_card)

    def _is_single_choice_step_complete(self, card):
        selected_command = self.command.get()

        if card is self.subcommand_card:
            if selected_command == "comfort":
                return bool(self.comfort_type.get())
            if selected_command in {"heating", "cooling"}:
                return self.load_subcommand.get() in {"bar", "timeline"}
            if selected_command == "plot-template":
                return self.plot_template.get() in PLOT_TEMPLATE_CHOICES
            return False

        if card is self.prepare_export_card:
            if selected_command == "prepare":
                return bool(self.prepare_export_format.get())
            if selected_command == "plot-template":
                return self.plot_template_mode.get() in {"single", "compare"}
            if selected_command == "analyze_data":
                return self.heating_series_layout.get() in {"separate", "combined"}
            if selected_command in {"heating", "cooling"}:
                if self.heating_mode.get() not in {"single", "compare"}:
                    return False
                return self.heating_mode.get() != "compare" or self.heating_series_layout.get() in {
                    "separate",
                    "combined",
                }
            return False

        if card is self.step_3_card:
            if selected_command == "plot-template":
                return bool(self.plot_template.get())
            if selected_command == "analyze_data":
                return True
            if selected_command in {"heating", "cooling"}:
                if self.load_subcommand.get() not in {"bar", "timeline"}:
                    return False
                if self.load_subcommand.get() == "timeline" and self.heating_view.get() not in {
                    "year",
                    "month",
                    "week",
                    "day",
                }:
                    return False
                return True
            return False

        return False

    def _activate_step(self, card):
        if not getattr(card, "step_available", True):
            return
        for step_card in getattr(self, "step_card_order", []):
            if step_card.winfo_manager() == "pack":
                step_card.pack_forget()
        card.pack(fill=tk.BOTH, expand=True)
        self.active_step_card = card
        self._update_step_nav_styles()
        self.right_scroll_canvas.yview_moveto(0)

    def _update_step_nav_styles(self):
        for card in getattr(self, "step_card_order", []):
            bg = self.color_panel
            number_bg = self.color_border
            dot_color = self.color_blue if card is self.active_step_card else self.color_panel
            card.step_nav.configure(bg=bg, highlightbackground=self.color_border)
            card.step_header.configure(bg=bg)
            card.step_number_label.configure(bg=number_bg)
            card.step_heading.configure(background=bg)
            card.step_status_dot.configure(bg=bg, fg=dot_color)

    def _build_step_summary_text(self, target_card):
        lines = []
        for card in getattr(self, "step_card_order", []):
            if card is target_card:
                break
            if not getattr(card, "step_available", True) or card.step_nav.winfo_manager() != "pack":
                continue
            summary_line = self._get_step_summary_line(card)
            if summary_line:
                lines.append(summary_line)
        return "\n".join(lines)

    def _format_summary_selection(self, singular_label, plural_label, values):
        if not values:
            return ""
        if len(values) == 1:
            return f"{singular_label}: {values[0]}"
        return f"{plural_label}: {len(values)} ausgewaehlt"

    def _get_step_summary_line(self, card):
        if card is self.step_2_card:
            command = self.command.get()
            return f"Befehl: {command}" if command else ""

        if card is self.subcommand_card:
            if self.command.get() == "comfort" and self.comfort_type.get():
                return f"Unterbefehl: {self.comfort_type.get()}"
            if self.command.get() in {"heating", "cooling"} and self.load_subcommand.get():
                return f"Unterbefehl: {self.load_subcommand.get()}"
            if self.command.get() == "plot-template" and self.plot_template.get():
                return f"Unterbefehl: {self.plot_template.get()}"
            return ""

        if card is self.prepare_export_card:
            if self.command.get() == "prepare" and self.prepare_export_format.get():
                return f"Exportformat: {self.prepare_export_format.get()}"
            if self.command.get() == "plot-template" and self.plot_template_mode.get():
                return f"Ausgabe: {self.plot_template_mode.get()}"
            if self.command.get() == "analyze_data" and self.heating_series_layout.get():
                return f"Excel-Ausgabe: {self.heating_series_layout.get()}"
            if self.command.get() in {"heating", "cooling"} and self.heating_mode.get():
                parts = [self.heating_mode.get()]
                if self.heating_mode.get() == "compare" and self.heating_series_layout.get():
                    parts.append(self.heating_series_layout.get())
                return f"Ausgabe: {', '.join(parts)}"
            return ""

        if card is self.step_3_card:
            selected_command = self.command.get()
            if selected_command == "plot-template":
                template_label = self.plot_template.get()
                spec = get_plot_template_spec(template_label)
                if spec is None or spec.view == "year":
                    return f"Template: {template_label}"
                if spec.view == "month":
                    return f"Template: {template_label}, Monat {self.heating_month.get()}"
                if spec.view == "week":
                    return f"Template: {template_label}, KW {self.heating_week.get()}"
                if spec.view == "day":
                    return f"Template: {template_label}, {self.heating_day.get()}. {self.heating_month.get()}"
                return f"Template: {template_label}"
            if selected_command == "analyze_data" and self.heating_series_layout.get():
                return f"Excel-Ausgabe: {self.heating_series_layout.get()}"
            if selected_command in {"heating", "cooling"}:
                parts = []
                if self.load_subcommand.get() == "timeline" and self.heating_view.get():
                    view_label = self.heating_view.get()
                    if view_label == "month":
                        view_label = f"month {self.heating_month.get()}"
                    elif view_label == "week":
                        view_label = f"week KW {self.heating_week.get()}"
                    elif view_label == "day":
                        view_label = f"day {self.heating_month.get()} {self.heating_day.get()}"
                    parts.append(f"Ansicht {view_label}")
                return f"Optionen: {', '.join(parts)}" if parts else ""
            return ""

        if card is self.overlay_card:
            parts = []
            if self.plot_show_setpoint_band.get():
                parts.append(f"Sollwertband {self.plot_setpoint_min.get()}-{self.plot_setpoint_max.get()} °C")
            if self.plot_show_outdoor_temperature.get():
                parts.append("Außenluft")
            if self.plot_show_operative_temperature.get():
                parts.append("Operative Temperatur")
            if self.free_overlay_lines:
                line_label = "freie Linie" if len(self.free_overlay_lines) == 1 else "freie Linien"
                parts.append(f"{len(self.free_overlay_lines)} {line_label}")
            return f"Überlagerungen: {', '.join(parts)}" if parts else ""

        if hasattr(self, "step_1_card") and card is self.step_1_card and self.analysis_scope.get():
            return f"Analyseumfang: {self.analysis_scope.get()}"

        if card is self.step_4_card:
            if self.analysis_scope.get() == "Alle Varianten" and self.command.get() != "plot-template":
                return f"Varianten: alle ({len(self.variant_names)})"
            return self._format_summary_selection("Variante", "Varianten", self._get_selected_variants())

        if card is self.step_5_card:
            return self._format_summary_selection("Raum", "Raeume", self._get_selected_rooms())

        return ""

    def _update_step_summaries(self):
        for card in getattr(self, "step_card_order", []):
            summary_text = self._build_step_summary_text(card)
            card.step_summary_label.configure(text=summary_text)
            if summary_text and card.step_summary_frame.winfo_manager() != "pack":
                card.step_summary_frame.pack(
                    fill=tk.X,
                    pady=(0, 12),
                    before=card.step_body,
                )
            elif not summary_text and card.step_summary_frame.winfo_manager() == "pack":
                card.step_summary_frame.pack_forget()
        self._update_right_scrollbar_visibility()

    def _update_step_visibility(self):
        selected_command = self.command.get()
        no_command = not selected_command
        is_prepare = selected_command == "prepare"
        is_plot_template = selected_command == "plot-template"
        show_subcommands = selected_command in {"comfort", "heating", "cooling", "plot-template"}
        load_without_subcommand = selected_command in {"heating", "cooling"} and self.load_subcommand.get() not in {
            "bar",
            "timeline",
        }
        hide_options_step = (
            no_command
            or selected_command in {"prepare", "analyze_data", "all"}
            or load_without_subcommand
        )
        show_overlays = (
            is_plot_template
            and self.overlay_enabled.get()
            and template_uses_overlay_options(self.plot_template.get())
        )
        self._set_card_visible(self.subcommand_card, show_subcommands)
        self._set_card_visible(self.step_3_card, not hide_options_step)
        self._set_card_visible(self.step_4_card, not no_command)
        self._set_card_visible(self.step_5_card, not no_command and not is_prepare)
        self._set_card_visible(self.overlay_card, show_overlays)
        self._set_card_visible(
            self.prepare_export_card,
            not no_command,
        )

    def _set_card_visible(self, card, visible):
        card.step_available = visible
        nav_visible = card.step_nav.winfo_manager() == "pack"
        if visible and not nav_visible:
            self._show_step_card_in_order(card)
        elif not visible and nav_visible:
            card.step_nav.pack_forget()
        if not visible and card.winfo_manager() == "pack":
            card.pack_forget()

    def _show_step_card_in_order(self, card):
        card_index = self.step_card_order.index(card)
        for next_card in self.step_card_order[card_index + 1 :]:
            if next_card.step_nav.winfo_manager() == "pack":
                card.step_nav.pack(fill=tk.X, pady=6, before=next_card.step_nav)
                return
        card.step_nav.pack(fill=tk.X, pady=6)
