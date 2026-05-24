"""Komfortzonen und Punktklassifizierung fuer Comfort-Auswertungen."""

from __future__ import annotations

from matplotlib.path import Path as MplPath

# Eckpunkte: [operative Temperatur °C, relative Luftfeuchte %]
COMFORT_HIGH = [[17.8, 72.0], [22.0, 66.5], [23.8, 33.5], [18.4, 40.0]]

COMFORT_NORMAL = [
    [17.0, 85.5],
    [20.3, 80.0],
    [24.7, 60.0],
    [26.8, 29.0],
    [25.9, 20.0],
    [19.9, 20.0],
    [17.0, 34.5],
    [16.0, 74.0],
]


def count_points_in_zone(room_data, polygon_points):
    """Zaehlt Messpunkte, die innerhalb eines Polygons liegen."""
    polygon = MplPath(polygon_points)
    measurement_points = room_data[["top", "relhum"]].to_numpy()
    return int(polygon.contains_points(measurement_points).sum())


def build_zone_masks(room_data):
    """Erzeugt Masken fuer Behaglich, noch Behaglich und ausserhalb beider Zonen."""
    measurement_points = room_data[["top", "relhum"]].to_numpy()
    comfort_high_mask = MplPath(COMFORT_HIGH).contains_points(measurement_points)
    comfort_normal_mask = MplPath(COMFORT_NORMAL).contains_points(measurement_points)
    comfort_normal_only_mask = comfort_normal_mask & ~comfort_high_mask
    outside_mask = ~(comfort_high_mask | comfort_normal_mask)
    return comfort_high_mask, comfort_normal_only_mask, outside_mask
