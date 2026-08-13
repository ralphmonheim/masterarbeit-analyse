import pytest

from ma_analyse.analysis.time_weighted_metrics import (
    TimeWeightedSeries,
    coincident_peak,
    degree_hours,
    hours_outside_limit,
    integrate_power_kwh,
    maximum_continuous_violation_hours,
    ppd_weighted_person_hours,
    time_weighted_mean,
    weighted_person_hours,
)


def test_variable_intervals_are_time_weighted():
    series = TimeWeightedSeries((0.0, 0.5, 2.0), (1000.0, 2000.0, 0.0), 3.0)

    assert series.durations_hours == (0.5, 1.5, 1.0)
    assert time_weighted_mean(series) == pytest.approx(3500.0 / 3.0)
    assert integrate_power_kwh(series) == pytest.approx(3.5)


def test_temperature_hours_and_degree_hours_use_interval_duration():
    series = TimeWeightedSeries((0.0, 0.5, 2.0), (19.0, 20.5, 22.0), 3.0)

    assert hours_outside_limit(series, lower_limit=21.0) == pytest.approx(2.0)
    assert degree_hours(series, lower_limit=21.0) == pytest.approx(1.75)
    assert maximum_continuous_violation_hours(series, lower_limit=21.0) == pytest.approx(2.0)


def test_coincident_peak_is_not_sum_of_individual_peaks():
    first = TimeWeightedSeries((0.0, 1.0), (10.0, 2.0), 2.0)
    second = TimeWeightedSeries((0.0, 1.0), (1.0, 8.0), 2.0)

    assert coincident_peak((first, second)) == 11.0
    assert max(first.values) + max(second.values) == 18.0


def test_person_and_ppd_weighted_hours_are_separate_metrics():
    occupancy = TimeWeightedSeries((0.0, 1.0), (2.0, 1.0), 2.0)
    ppd = TimeWeightedSeries((0.0, 1.0), (10.0, 20.0), 2.0)

    assert weighted_person_hours(occupancy) == 3.0
    assert ppd_weighted_person_hours(ppd, occupancy) == pytest.approx(0.4)


def test_invalid_or_duplicate_time_axis_is_rejected():
    with pytest.raises(ValueError, match="streng monoton"):
        TimeWeightedSeries((0.0, 0.0), (1.0, 2.0), 1.0)


def test_energy_requires_confirmed_power_unit():
    series = TimeWeightedSeries((0.0,), (1.0,), 1.0)
    with pytest.raises(ValueError, match="source_unit"):
        integrate_power_kwh(series, source_unit="unverified")
