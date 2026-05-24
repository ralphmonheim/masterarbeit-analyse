from ma_analyse.analysis.components.time_windows import get_day_hour_range, get_month_hour_range, get_week_hour_range


def test_time_window_helpers():
    assert get_month_hour_range("Jan") == (0, 31 * 24)
    assert get_week_hour_range(1) == (0, 7 * 24)
    assert get_day_hour_range("Feb", 1) == (31 * 24, 32 * 24)
