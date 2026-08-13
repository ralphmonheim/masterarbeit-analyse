from ma_analyse.analysis.tables.master_thesis import (
    ZONE_COLUMNS,
    ZoneMetricRecord,
    build_zone_metrics_table,
    zone_metric_keys,
)


def test_zone_table_keeps_requested_metrics_and_separates_person_hours():
    table = build_zone_metrics_table(
        [
            ZoneMetricRecord(
                zone="EG Ost",
                group="5Z",
                values={
                    "area_m2": 67.96,
                    "person_hours_h": 200.0,
                    "ppd_weighted_person_hours_h": 12.0,
                },
            )
        ]
    )

    assert list(table.columns) == [column.output_name for column in ZONE_COLUMNS]
    assert table.loc[0, "Personenstunden [Pers·h]"] == 200.0
    assert table.loc[0, "PPD-gewichtete Personenstunden [Pers·h]"] == 12.0


def test_missing_metrics_remain_empty_instead_of_being_invented():
    table = build_zone_metrics_table([ZoneMetricRecord(zone="Lobby", group="5Z")])

    assert table.loc[0, "Zone"] == "Lobby"
    assert table.loc[0, "Gruppe"] == "5Z"
    assert table.loc[0, "Raumheizung [kWh]"] is None
    assert "overtemperature_degree_hours_kh" in zone_metric_keys()
