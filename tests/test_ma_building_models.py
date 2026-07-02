from ma_building import BuildingMaturityLevel, building_specification_from_dict


def test_building_specification_from_dict_normalizes_tuples_and_levels():
    spec = building_specification_from_dict(
        {
            "schema_version": "1.0",
            "project": {"project_id": "P1", "name": "Projekt"},
            "building": {
                "building_id": "B1",
                "name": "Gebaeude",
                "unit": "m",
                "north_angle_deg": 0,
                "length_m": 10,
                "width_m": 5,
                "height_m": 3,
            },
            "model_version": {
                "version_id": "V1",
                "source_input_level": "BIL-4",
                "detected_input_level": "BIL-4",
                "confirmed_input_level": "BIL-4",
                "current_maturity_level": "BIL-4",
                "target_maturity_level": "BIL-4",
            },
            "storeys": [{"storey_id": "S1", "name": "EG", "elevation_m": 0, "height_m": 3}],
            "spaces": [{"space_id": "R1", "name": "Raum", "storey_id": "S1", "floor_area_m2": 12, "volume_m3": 36}],
            "elements": [
                {
                    "element_id": "W1",
                    "element_type": "external_wall",
                    "construction_code": "AW",
                    "storey_id": "S1",
                    "area_m2": 15,
                    "orientation_deg": 90,
                    "adjacent_space_ids": ["R1"],
                }
            ],
        }
    )

    assert spec.model_version.current_maturity_level is BuildingMaturityLevel.BIL_4
    assert spec.storey_ids == {"S1"}
    assert spec.space_ids == {"R1"}
    assert spec.element_ids == {"W1"}
    assert spec.object_id_locations()[0] == ("B1", "building.building_id")
