from ma_analyse.analysis.templates import (
    is_time_filtered_template,
    template_requires_single_room,
    template_uses_overlay_options,
)
from ma_ui.tkinter_app.module_views.analyse.selection import resolve_variant_list_state


def test_gui_app_imports_without_starting_window():
    from ma_ui.tkinter_app.module_views.analyse import app

    assert hasattr(app, "run_gui")


def test_gui_mousewheel_resolver_ignores_tk_popdown_widget():
    from ma_ui.tkinter_app.module_views.analyse.app import PipelineGUI

    class FakeRoot:
        def nametowidget(self, widget_name):
            if "popdown" in widget_name:
                raise KeyError("popdown")
            raise AssertionError(f"Unexpected widget lookup: {widget_name}")

    gui = object.__new__(PipelineGUI)
    gui.root = FakeRoot()

    assert gui._resolve_widget(".!combobox.popdown.f.l") is None
    assert gui._should_skip_mousewheel(".!combobox.popdown.f.l") is False


def test_variant_list_state_starts_without_selection():
    state = resolve_variant_list_state(variant_count=3, scope="", current_selection=(0,))

    assert state.selectmode == "multiple"
    assert state.selected_indices == ()
    assert state.enabled is True


def test_variant_list_state_all_variants_selects_and_disables_all():
    state = resolve_variant_list_state(variant_count=3, scope="Alle Varianten")

    assert state.selectmode == "multiple"
    assert state.selected_indices == (0, 1, 2)
    assert state.enabled is False


def test_variant_list_state_keeps_manual_single_selection():
    state = resolve_variant_list_state(variant_count=3, scope="Eine Variante", current_selection=(2,))

    assert state.selectmode == "browse"
    assert state.selected_indices == (2,)
    assert state.enabled is True


def test_variant_list_state_clears_all_variants_when_scope_changes():
    state = resolve_variant_list_state(
        variant_count=3,
        scope="Mehrere Varianten",
        current_selection=(0, 1, 2),
        previous_scope="Alle Varianten",
    )

    assert state.selectmode == "multiple"
    assert state.selected_indices == ()
    assert state.enabled is True


def test_plot_template_gui_visibility_helpers_distinguish_time_and_overlay_templates():
    assert template_uses_overlay_options("heating-year") is False
    assert is_time_filtered_template("heating-year") is False
    assert template_uses_overlay_options("heating-overlay") is True
    assert is_time_filtered_template("heating-overlay") is False
    assert template_uses_overlay_options("heating-month") is False
    assert is_time_filtered_template("heating-month") is True
    assert template_uses_overlay_options("cooling-day") is False
    assert is_time_filtered_template("cooling-day") is True
    assert template_uses_overlay_options("cooling-absolute-year") is False
    assert is_time_filtered_template("cooling-absolute-year") is False
    assert template_uses_overlay_options("cooling-absolute-day") is False
    assert is_time_filtered_template("cooling-absolute-day") is True
    assert template_uses_overlay_options("energy-balance-week") is False
    assert is_time_filtered_template("energy-balance-week") is True
    assert template_uses_overlay_options("internal-loads-month") is False
    assert is_time_filtered_template("internal-loads-month") is True
    assert template_uses_overlay_options("comfort-plot") is False
    assert is_time_filtered_template("comfort-plot") is False
    assert template_uses_overlay_options("thermal-room-climate-day") is False
    assert is_time_filtered_template("thermal-room-climate-day") is True


def test_plot_template_gui_room_requirement_helper_allows_room_comparison():
    assert template_requires_single_room("internal-loads-year") is True
    assert template_requires_single_room("internal-loads-room-comparison") is False
    assert template_requires_single_room("comfort-plot") is True
    assert template_requires_single_room("comfort-plot-overview") is False
    assert template_requires_single_room("heating-bar") is False
    assert template_requires_single_room("cooling-bar") is False


def test_tkinter_plot_template_choices_show_complete_catalog():
    from ma_analyse.analysis.templates import PLOT_TEMPLATE_CHOICES
    from ma_ui.tkinter_app.module_views.analyse.app import PipelineGUI

    class FakeVariable:
        def __init__(self, value):
            self.value = value

        def get(self):
            return self.value

    gui = object.__new__(PipelineGUI)
    gui.plot_template_mode = FakeVariable("single")

    choices = gui._filtered_plot_template_choices()

    assert "heating-year" in choices
    assert "heating-overlay" in choices
    assert choices == list(PLOT_TEMPLATE_CHOICES)


def test_tkinter_plot_template_choices_fall_back_before_group_and_mode_selection():
    from ma_analyse.analysis.templates import PLOT_TEMPLATE_CHOICES
    from ma_ui.tkinter_app.module_views.analyse.app import PipelineGUI

    class FakeVariable:
        def get(self):
            return ""

    gui = object.__new__(PipelineGUI)
    gui.plot_template_mode = FakeVariable()

    assert gui._filtered_plot_template_choices() == list(PLOT_TEMPLATE_CHOICES)
