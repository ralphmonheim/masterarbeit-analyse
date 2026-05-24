"""Gemeinsame Kalender-, Zeitfenster- und Zeitachsenlogik fuer Jahresdaten."""

from __future__ import annotations

MONTH_DAY_COUNTS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
MONTH_NAMES = ["Jan", "Feb", "Mär", "Apr", "Mai", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Dez"]
MONTH_HOURS = [days * 24 for days in MONTH_DAY_COUNTS]
MONTH_BOUNDARIES = [sum(MONTH_HOURS[: index + 1]) for index in range(len(MONTH_HOURS))]
MONTH_START_HOURS = [0] + MONTH_BOUNDARIES[:-1]
HOURS_PER_WEEK = 7 * 24
HOURS_PER_DAY = 24
MAX_CALENDAR_WEEK = ((MONTH_BOUNDARIES[-1] - 1) // HOURS_PER_WEEK) + 1


def hour_to_month_label(hour) -> str:
    """Gibt fuer eine Jahresstunde den passenden Monatsnamen zurueck."""
    try:
        hour = int(hour)
    except Exception:
        return "Unbekannt"
    for index, boundary in enumerate(MONTH_BOUNDARIES):
        if hour < boundary:
            return MONTH_NAMES[index]
    return MONTH_NAMES[-1]


def get_month_hour_range(month_name: str) -> tuple[int, int]:
    """Liefert Start- und Endstunde eines Monats im 8760h-Jahr."""
    if month_name not in MONTH_NAMES:
        raise ValueError(f"Ungueltiger Monat: {month_name}")
    month_index = MONTH_NAMES.index(month_name)
    return MONTH_START_HOURS[month_index], MONTH_BOUNDARIES[month_index]


def get_week_hour_range(week_number: int) -> tuple[int, int]:
    """Liefert Start- und Endstunde einer Kalenderwoche im 8760h-Jahr."""
    if week_number < 1 or week_number > MAX_CALENDAR_WEEK:
        raise ValueError(f"Ungueltige Kalenderwoche: {week_number}")
    start_hour = (week_number - 1) * HOURS_PER_WEEK
    end_hour = start_hour + HOURS_PER_WEEK
    return start_hour, end_hour


def get_day_hour_range(month_name: str, day_number: int) -> tuple[int, int]:
    """Liefert Start- und Endstunde eines Kalendertags im 8760h-Jahr."""
    if month_name not in MONTH_NAMES:
        raise ValueError(f"Ungueltiger Monat: {month_name}")
    month_index = MONTH_NAMES.index(month_name)
    max_days = MONTH_DAY_COUNTS[month_index]
    if day_number < 1 or day_number > max_days:
        raise ValueError(f"Ungueltiger Tag {day_number} fuer {month_name}")
    start_hour = MONTH_START_HOURS[month_index] + ((day_number - 1) * HOURS_PER_DAY)
    end_hour = start_hour + HOURS_PER_DAY
    return start_hour, end_hour


def get_month_day_from_day_of_year(day_of_year: int) -> tuple[int, int]:
    """Wandelt einen Tagesindex im Jahr in Monat und Tag um."""
    remaining_days = day_of_year
    for month_index, day_count in enumerate(MONTH_DAY_COUNTS):
        if remaining_days < day_count:
            return month_index, remaining_days + 1
        remaining_days -= day_count
    return len(MONTH_DAY_COUNTS) - 1, MONTH_DAY_COUNTS[-1]


def get_time_window(view: str, month: str | None = None, week: int | None = None, day: int | None = None) -> dict:
    """Baut ein einheitliches Zeitfenster fuer month/week/day-Ansichten."""
    if view == "month":
        month_index = MONTH_NAMES.index(month)
        start_hour, end_hour = get_month_hour_range(month)
        return {
            "start_hour": start_hour,
            "end_hour": end_hour,
            "file_stub": f"month_{month_index + 1:02d}",
            "title_text": f"Monat {month}",
            "x_label": f"Stunde in {month}",
            "month_name": month,
        }

    if view == "week":
        start_hour, end_hour = get_week_hour_range(week)
        return {
            "start_hour": start_hour,
            "end_hour": end_hour,
            "file_stub": f"week_kw{week:02d}",
            "title_text": f"KW {week:02d}",
            "x_label": f"Stunde in KW {week:02d}",
        }

    if view == "day":
        start_hour, end_hour = get_day_hour_range(month, day)
        month_index = MONTH_NAMES.index(month)
        return {
            "start_hour": start_hour,
            "end_hour": end_hour,
            "file_stub": f"day_{month_index + 1:02d}_{day:02d}",
            "title_text": f"{day:02d}. {month}",
            "x_label": f"Stunde am {day:02d}. {month}",
            "month_name": month,
            "day_number": day,
        }

    raise ValueError(f"Nicht unterstuetzte Zeitansicht: {view}")


def filter_time_window(df, time_window: dict):
    """Filtert eine Zeitreihe auf ein Zeitfenster und setzt die lokale x-Achse."""
    filtered = df[(df["time"] >= time_window["start_hour"]) & (df["time"] < time_window["end_hour"])].copy()
    if filtered.empty:
        return filtered

    filtered["time_window"] = filtered["time"] - time_window["start_hour"]
    return filtered


def validate_time_selection(
    view: str, month: str | None = None, week: int | None = None, day: int | None = None, label: str = "Auswertung"
) -> bool:
    """Prueft CLI-/GUI-Zeitangaben, bevor Plots erzeugt werden."""
    if view == "month":
        if month is None:
            print("X Fuer view=month muss ein Monat gewaehlt werden.")
            return False
        if month not in MONTH_NAMES:
            print(f"X Ungueltiger Monat fuer {label}: {month}")
            return False
        return True

    if view == "week":
        if week is None:
            print("X Fuer view=week muss eine Kalenderwoche gewaehlt werden.")
            return False
        if week < 1 or week > MAX_CALENDAR_WEEK:
            print(f"X Die Kalenderwoche muss zwischen 1 und {MAX_CALENDAR_WEEK} liegen.")
            return False
        return True

    if view == "day":
        if month is None:
            print("X Fuer view=day muss ein Monat gewaehlt werden.")
            return False
        if month not in MONTH_NAMES:
            print(f"X Ungueltiger Monat fuer {label}: {month}")
            return False
        if day is None:
            print("X Fuer view=day muss ein Tag gewaehlt werden.")
            return False
        month_index = MONTH_NAMES.index(month)
        if day < 1 or day > MONTH_DAY_COUNTS[month_index]:
            print(f"X Der Tag muss fuer {month} zwischen 1 und {MONTH_DAY_COUNTS[month_index]} liegen.")
            return False
        return True

    return True


def build_energy_plot_subtitle(
    view: str,
    month_name: str | None = None,
    week_number: int | None = None,
    day_number: int | None = None,
    year_text: str = "Zeitraum: Jan bis Dez",
) -> str:
    """Kurzer Zeitraumtext fuer die rechte obere Diagrammecke."""
    if view == "year":
        return year_text
    if view == "month":
        return f"Zeitraum: Monat {month_name}"
    if view == "week":
        return f"Zeitraum: KW {week_number:02d}"
    if view == "day":
        return f"Zeitraum: {day_number:02d}. {month_name}"
    return ""


def build_energy_time_axis_config(view: str, time_window: dict | None = None, year_tick_mode: str = "1000h") -> dict:
    """Definiert Grid, Zeitstrahl und Zusatzlabels fuer die gewaehlte Ansicht."""
    if view == "year":
        if year_tick_mode == "14-day":
            hour_ticks = list(range(0, MONTH_BOUNDARIES[-1] + 1, 14 * HOURS_PER_DAY))
            if hour_ticks[-1] != MONTH_BOUNDARIES[-1] and (MONTH_BOUNDARIES[-1] - hour_ticks[-1]) > (3 * HOURS_PER_DAY):
                hour_ticks.append(MONTH_BOUNDARIES[-1])
        else:
            hour_ticks = list(range(0, 9000, 1000))
        month_boundary_ticks = [0] + MONTH_START_HOURS[1:] + [MONTH_BOUNDARIES[-1]]
        month_centers = [MONTH_START_HOURS[index] + (MONTH_HOURS[index] / 2) for index in range(len(MONTH_NAMES))]
        return {
            "ticks": hour_ticks,
            "labels": [str(int(tick)) for tick in hour_ticks],
            "grid_ticks": month_boundary_ticks,
            "x_label": "Stunde im Jahr",
            "x_lim": (0, MONTH_BOUNDARIES[-1]),
            "rotation": 0,
            "boundary_ticks": MONTH_START_HOURS[1:],
            "annotation_ticks": month_centers,
            "annotation_labels": MONTH_NAMES,
        }

    if time_window is None:
        raise ValueError("Fuer month/week/day wird ein time_window benoetigt.")

    total_hours = time_window["end_hour"] - time_window["start_hour"]

    if view == "month":
        total_days = max(1, total_hours // HOURS_PER_DAY)
        hour_step = 48 if total_hours > (10 * HOURS_PER_DAY) else 24
        ticks = list(range(0, total_hours + 1, hour_step))
        if ticks[-1] != total_hours:
            ticks.append(total_hours)
        span_ticks = [((day_index * HOURS_PER_DAY) + (HOURS_PER_DAY / 2)) for day_index in range(total_days)]
        span_labels = [str(day_index + 1) for day_index in range(total_days)]
        return {
            "ticks": ticks,
            "labels": [str(int(tick)) for tick in ticks],
            "grid_ticks": list(range(0, total_hours + 1, HOURS_PER_DAY)),
            "x_label": f"Stunde in {time_window['title_text']}",
            "x_lim": (0, total_hours),
            "rotation": 0,
            "boundary_ticks": list(range(HOURS_PER_DAY, total_hours, HOURS_PER_DAY)),
            "annotation_ticks": span_ticks,
            "annotation_labels": span_labels,
        }

    if view == "week":
        ticks = list(range(0, total_hours + 1, HOURS_PER_DAY))
        if ticks[-1] != total_hours:
            ticks.append(total_hours)
        first_day_of_year = time_window["start_hour"] // HOURS_PER_DAY
        span_ticks = []
        span_labels = []
        previous_month_index = None
        for offset in range(total_hours // HOURS_PER_DAY):
            span_ticks.append((offset * HOURS_PER_DAY) + (HOURS_PER_DAY / 2))
            month_index, month_day = get_month_day_from_day_of_year(first_day_of_year + offset)
            if previous_month_index is None or previous_month_index != month_index:
                span_labels.append(f"{month_day} {MONTH_NAMES[month_index]}")
            else:
                span_labels.append(str(month_day))
            previous_month_index = month_index
        return {
            "ticks": ticks,
            "labels": [str(int(tick)) for tick in ticks],
            "grid_ticks": ticks,
            "x_label": time_window["x_label"],
            "x_lim": (0, total_hours),
            "rotation": 0,
            "boundary_ticks": list(range(HOURS_PER_DAY, total_hours, HOURS_PER_DAY)),
            "annotation_ticks": span_ticks,
            "annotation_labels": span_labels,
        }

    if view == "day":
        ticks = list(range(0, total_hours + 1, 3))
        if ticks[-1] != total_hours:
            ticks.append(total_hours)
        return {
            "ticks": ticks,
            "labels": [str(int(tick)) for tick in ticks],
            "grid_ticks": ticks,
            "x_label": time_window["x_label"],
            "x_lim": (0, total_hours),
            "rotation": 0,
        }

    raise ValueError(f"Nicht unterstuetzte Achsenansicht: {view}")
