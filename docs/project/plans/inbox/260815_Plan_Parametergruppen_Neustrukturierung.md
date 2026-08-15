# Projektplan – Neustrukturierung der Eingabeparameter und Parametergruppen

## 1. Ziel des Arbeitspakets

Das bestehende Eingabesystem soll zu einem konsistenten, fachlich vollständigen Parameterkatalog für die Gebäudesimulation weiterentwickelt werden.

Die bisherige Anzahl von ungefähr 84 Parametern ist dabei **nicht als feste Zielgröße** zu verstehen. Stattdessen soll das Programm alle fachlich relevanten Parameter der vier Eingabemodule

1. `BUILDING`
2. `ZONES`
3. `TECHNOLOGY`
4. `WEATHER`

abbilden können.

Die Parameter sollen nicht als flache Liste organisiert werden, sondern hierarchisch:

```text
Eingabemodul
└── Parametergruppe
    └── Parameter
        ├── Wert
        ├── Einheit
        ├── Datentyp
        ├── LOD
        ├── Quelle
        ├── Status
        ├── Editierbarkeit
        └── Variantenfähigkeit
```

Zentrale Anforderung ist, dass zwischen

- einem fachlichen Objekt bzw. einer **Parametergruppe**,
- einem konkreten **Einzelparameter**,
- einem aus anderen Größen **abgeleiteten Wert**,
- einer aus IFC übernommenen **festen Größe**
- und einem tatsächlich **variierbaren Parameter**

unterschieden wird.

---

# 2. Grundregeln des Parameterkonzepts

## 2.1 Parametergruppe

Eine Parametergruppe repräsentiert ein fachlich zusammengehöriges Objekt.

Beispiele:

```text
Außenwandkonstruktion AW01
Fenstertyp FE01
Türtyp TA01
Zone Z01
Wärmeerzeuger HG01
Kälteerzeuger CG01
Lüftungsgerät AHU01
Pumpe PU01
PV-Anlage PV01
```

Eine Parametergruppe selbst ist kein einzelner Parameter.

Beispiel:

```text
Fenstertyp FE01
├── Uw
├── g_value
├── frame_fraction
├── glazing_type
├── air_permeability
└── ...
```

---

## 2.2 Einzelparameter

Ein Einzelparameter ist eine adressierbare fachliche Größe.

Beispiele:

```text
building.windows.FE01.u_value
building.windows.FE01.g_value

building.constructions.AW01.layer_01.thickness
building.constructions.AW01.layer_01.lambda

zones.Z01.heating_setpoint

technology.heating.HG01.nominal_power

weather.weather_dataset
```

---

# 3. Status eines Parameters

Jeder Parameter muss mindestens einen der folgenden Status besitzen.

## FIXED

Wert ist vorhanden, wird angezeigt, ist aber im aktuellen Modell nicht veränderbar.

Beispiel:

```text
Gebäudelänge aus IFC
```

## EDITABLE

Parameter darf durch den Benutzer geändert werden.

## VARIANT

Parameter darf zusätzlich im Variantengenerator verwendet werden.

`VARIANT` setzt grundsätzlich `EDITABLE` voraus.

## DERIVED

Parameter wird aus anderen Eingaben oder der IFC-Geometrie berechnet.

Beispiele:

```text
Fensterfläche
WWR
U-Wert aus Schichtaufbau
A/V-Verhältnis
```

## OPTIONAL

Parameter ist nur vorhanden bzw. relevant, wenn ein bestimmtes Produkt oder System verwendet wird.

---

# 4. LOD-Grundprinzip

## LOD 1

LOD 1 beschreibt ein parametrisches, vereinfachtes Gebäude.

Hier können insbesondere Gebäudegeometrien frei verändert werden.

Beispiele:

```text
Gebäudelänge
Gebäudebreite
Gebäudehöhe
Geschossanzahl
Geschosshöhe
Gebäudeorientierung
Fensterflächenanteil
```

## LOD 2

LOD 2 verwendet ein konkretes Referenzgebäude auf Grundlage einer IFC.

Beim aktuellen Small Office gilt daher:

```text
Gebäudegrundgeometrie = IFC = FIXED
```

Die Parameter bleiben im Datenmodell sichtbar, sind aber gesperrt.

Variierbar bleiben insbesondere:

- Baukonstruktionen
- Materialeigenschaften
- Fenstereigenschaften
- Türeigenschaften
- Nutzung
- interne Lasten
- Sollwerte
- technische Systeme
- technische Produktparameter
- Anlagenleistungen
- Wirkungsgrade
- Regelstrategien
- Wetterdatensatz

## LOD 3

LOD 3 kann später eine noch detailliertere Produkt- und Komponentenauflösung abbilden.

Beispiele:

- einzelne Glasscheiben
- Gaszwischenräume
- Herstellerprodukte
- detaillierte Pumpenkennlinien
- Teillastkennfelder
- detaillierte Regelalgorithmen
- produktspezifische HVAC-Kennlinien

---

# 5. Eingabemodul BUILDING

---

# 5.1 Parametergruppe `BUILDING_GEOMETRY`

Diese Parameter gehören zum allgemeinen Datenmodell.

Im aktuellen Small Office sind sie aufgrund der IFC jedoch `FIXED`.

## Parameter

```text
building.geometry.length
building.geometry.width
building.geometry.height

building.geometry.orientation

building.geometry.storey_count
building.geometry.storey_height[]

building.geometry.gross_floor_area
building.geometry.net_floor_area

building.geometry.gross_volume
building.geometry.conditioned_volume

building.geometry.facade_area_north
building.geometry.facade_area_east
building.geometry.facade_area_south
building.geometry.facade_area_west

building.geometry.roof_area
building.geometry.ground_contact_area

building.geometry.external_wall_area
building.geometry.window_area
building.geometry.door_area

building.geometry.envelope_area

building.geometry.area_volume_ratio
building.geometry.window_wall_ratio
```

## Einheiten

```text
length / width / height           m
orientation                       °
area                              m²
volume                            m³
A/V                               1/m
WWR                               -
```

## Verhalten LOD 2

Folgende Parameter werden aus IFC übernommen:

```text
length
width
height
orientation
storey_count
storey_height
floor_area
volume
facade_area
roof_area
ground_contact_area
window_area
door_area
```

Status:

```text
source = IFC
editable = false
variant_capable = false
```

Folgende Größen werden berechnet:

```text
envelope_area
area_volume_ratio
window_wall_ratio
```

Status:

```text
source = DERIVED
editable = false
variant_capable = false
```

---

# 5.2 Parametergruppe `OPAQUE_CONSTRUCTION`

Für jede tatsächlich vorkommende opake Konstruktion ist eine eigene Parametergruppe anzulegen.

Beispiele:

```text
AW01
AW02

IW01
IW02

DA01

BP01

GD01
```

Kategorien:

```text
EXTERIOR_WALL
INTERIOR_WALL
ROOF
GROUND_SLAB
FLOOR
CEILING
GROUND_WALL
WALL_TO_UNCONDITIONED_SPACE
```

---

# 5.3 Konstruktionsebene

Je Konstruktion:

```text
construction.category
construction.total_thickness

construction.u_value

construction.surface_resistance_inside
construction.surface_resistance_outside

construction.solar_absorptance_external
construction.thermal_emissivity_external
construction.thermal_emissivity_internal

construction.areal_mass
construction.areal_heat_capacity
```

## Status

`total_thickness`

→ DERIVED aus Schichten.

`u_value`

→ nach Möglichkeit DERIVED.

Direkte Eingabe von `u_value` nur bei einem vereinfachten LOD oder einem vereinfachten Konstruktionsmodell.

---

# 5.4 Materialschichten

Eine Konstruktion besitzt `n` Materialschichten.

Beispiel:

```text
AW01
├── layer_01
├── layer_02
├── layer_03
└── layer_04
```

Je Schicht:

```text
material
thickness
thermal_conductivity
density
specific_heat_capacity
vapour_diffusion_resistance
solar_absorptance
thermal_absorptance
visible_absorptance
```

Optional:

```text
porosity
moisture_capacity
temperature_dependent_conductivity
```

## Einheiten

```text
thickness                    m
thermal_conductivity         W/(mK)
density                      kg/m³
specific_heat_capacity       J/(kgK)
vapour_diffusion_resistance  -
```

## Variantenfähigkeit

Typischerweise variierbar:

```text
material
thickness
thermal_conductivity
density
specific_heat_capacity
```

Nicht unabhängig variieren, wenn Material aus einem Produktkatalog gewählt wird.

Dann gilt:

```text
material = Auswahlparameter

lambda
rho
cp
mu
```

werden aus dem Materialdatensatz übernommen.

---

# 5.5 Parametergruppe `THERMAL_BRIDGE`

Unterstützte Methoden:

```text
SIMPLIFIED
DETAILED
```

## Vereinfachte Methode

```text
thermal_bridges.delta_u
```

Einheit:

```text
W/(m²K)
```

## Detaillierte Methode

Je Wärmebrückentyp:

```text
thermal_bridge.psi_value
thermal_bridge.length
```

Zusätzlich optional:

```text
thermal_bridge.chi_value
thermal_bridge.point_count
```

Nur eine Berechnungsmethode darf gleichzeitig führend sein.

---

# 5.6 Parametergruppe `WINDOW_TYPE`

Für jeden tatsächlich verwendeten Fenstertyp wird eine eigene Gruppe angelegt.

Beispiel:

```text
FE01
FE02
FE03
```

Eine beliebige Anzahl konkreter Fensterinstanzen kann auf denselben Typ referenzieren.

---

# 5.7 Fenstertyp – thermische Eigenschaften

Je Fenstertyp:

```text
window.u_value
window.glazing_u_value
window.frame_u_value

window.g_value

window.visible_transmittance

window.frame_fraction
window.glazing_fraction

window.edge_psi_value

window.air_permeability
```

Einheiten:

```text
Uw / Ug / Uf       W/(m²K)
psi                W/(mK)
g_value            -
transmittance      -
frame_fraction     -
```

---

# 5.8 Fenstertyp – detaillierte Verglasung

Optional bei höherem Detaillierungsgrad:

```text
window.glazing.layer_count
```

Je Glasscheibe:

```text
glass.thickness
glass.thermal_conductivity

glass.solar_transmittance
glass.solar_reflectance_front
glass.solar_reflectance_back

glass.visible_transmittance
glass.visible_reflectance_front
glass.visible_reflectance_back

glass.infrared_transmittance
glass.emissivity_front
glass.emissivity_back
```

Je Gaszwischenraum:

```text
gas_gap.thickness
gas_gap.gas_type
gas_gap.gas_fraction
```

Mögliche Gasarten:

```text
AIR
ARGON
KRYPTON
XENON
MIXTURE
```

---

# 5.9 Fenstergeometrie

Im allgemeinen Parameterkatalog:

```text
window.width
window.height
window.sill_height

window.offset_horizontal
window.offset_vertical

window.installation_depth
window.offset_inside
window.offset_outside
```

Beim aktuellen Small Office:

```text
source = IFC
editable = false
variant_capable = false
```

Damit wird die Referenzgeometrie nicht verändert.

Diese Parameter können bei einem zukünftigen parametrischen LOD-1-Modell wieder freigegeben werden.

---

# 5.10 Fensteröffnungsparameter

Optional:

```text
window.operable

window.max_opening_fraction
window.opening_area
window.opening_angle

window.opening_control
```

---

# 5.11 Parametergruppe `DOOR_TYPE`

Je Türtyp:

```text
TA01
TA02
TI01
```

## Parameter

```text
door.u_value

door.width
door.height

door.air_permeability

door.glazing_fraction
door.glazing_g_value
door.glazing_u_value

door.frame_fraction
door.frame_u_value

door.installation_depth
door.offset_inside
door.offset_outside
```

Geometrische Parameter im aktuellen IFC-Modell grundsätzlich `FIXED`.

Thermische Eigenschaften können `EDITABLE` beziehungsweise `VARIANT` sein.

---

# 5.12 Parametergruppe `SHADING_SYSTEM`

Je Sonnenschutzsystem:

```text
SH01
SH02
```

Parameter:

```text
shading.type
shading.position

shading.solar_transmittance
shading.solar_reflectance
shading.solar_absorptance

shading.visible_transmittance

shading.reduction_factor

shading.slat_width
shading.slat_spacing
shading.slat_angle

shading.minimum_position
shading.maximum_position

shading.control_type

shading.solar_threshold
shading.indoor_temperature_threshold
shading.outdoor_temperature_threshold

shading.schedule
```

Mögliche Typen:

```text
EXTERNAL_BLIND
INTERNAL_BLIND
EXTERNAL_SCREEN
INTERNAL_SCREEN
SHUTTER
BETWEEN_GLASS
FIXED_SHADING
```

---

# 5.13 Parametergruppe `AIR_TIGHTNESS`

Es muss eine führende Eingabemethode gewählt werden.

Mögliche Parameter:

```text
building.air_tightness.n50
building.air_tightness.q50

building.air_tightness.reference_pressure
building.air_tightness.effective_leakage_area

building.air_tightness.infiltration_model

building.air_tightness.wind_coefficient
building.air_tightness.temperature_coefficient
building.air_tightness.shelter_factor
```

Nicht gleichzeitig mehrere voneinander abhängige Luftdichtheitsparameter als unabhängig variierbare Parameter anbieten.

---

# 6. Eingabemodul ZONES

Jede thermische Zone ist eine eigene Parametergruppe.

Aktuelles Referenzmodell:

```text
Z01
Z02
Z03
Z04
Z05
```

Die genaue Raumzuordnung und Geometrie stammt aus dem bestehenden Referenzmodell und bleibt fest.

---

# 6.1 Parametergruppe `ZONE_GEOMETRY`

Je Zone:

```text
zone.floor_area
zone.volume
zone.mean_height

zone.external_wall_area
zone.internal_wall_area

zone.window_area
zone.door_area

zone.roof_area
zone.ground_area

zone.window_wall_ratio
```

Beim Small Office:

```text
source = IFC / DERIVED
editable = false
variant_capable = false
```

---

# 6.2 Parametergruppe `ZONE_THERMAL_CONTROL`

Je Zone:

```text
zone.heating_setpoint
zone.cooling_setpoint

zone.heating_setback_temperature
zone.cooling_shutdown_temperature

zone.minimum_operating_temperature
zone.maximum_operating_temperature

zone.minimum_relative_humidity
zone.maximum_relative_humidity

zone.co2_setpoint

zone.temperature_deadband
```

Einheiten:

```text
temperature     °C
humidity        %
CO2             ppm
deadband        K
```

Typischerweise besonders relevant für Varianten:

```text
heating_setpoint
cooling_setpoint
```

---

# 6.3 Parametergruppe `OCCUPANCY`

Je Zone:

```text
occupancy.person_count
occupancy.person_density
occupancy.area_per_person

occupancy.occupancy_factor

occupancy.activity_level

occupancy.total_heat_per_person
occupancy.sensible_heat_per_person
occupancy.latent_heat_per_person

occupancy.co2_generation
occupancy.moisture_generation

occupancy.clothing_level

occupancy.schedule
```

Es muss eine führende Belegungsdefinition geben.

Beispielsweise:

```text
person_count
```

oder

```text
person_density
```

oder

```text
area_per_person
```

Die anderen Größen werden daraus abgeleitet.

---

# 6.4 Parametergruppe `LIGHTING`

Je Zone:

```text
lighting.installed_power
lighting.power_density

lighting.load_factor

lighting.schedule

lighting.convective_fraction
lighting.radiative_fraction
lighting.return_air_fraction

lighting.illuminance_setpoint

lighting.daylight_control
lighting.occupancy_control

lighting.minimum_dimming_level

lighting.standby_power
```

Typische Variantenparameter:

```text
power_density
load_factor
illuminance_setpoint
```

---

# 6.5 Parametergruppe `EQUIPMENT`

Je Zone:

```text
equipment.installed_power
equipment.power_density

equipment.load_factor

equipment.schedule

equipment.convective_fraction
equipment.radiative_fraction
equipment.latent_fraction
equipment.lost_fraction

equipment.standby_power
```

---

# 6.6 Parametergruppe `PROCESS_LOADS`

Optional für andere Gebäudenutzungen:

```text
process.sensible_heat
process.latent_heat
process.moisture_load
process.power_density
process.schedule
```

Beim Small Office zunächst deaktiviert.

---

# 6.7 Parametergruppe `ZONE_OUTDOOR_AIR`

Je Zone:

```text
outdoor_air.total_flow
outdoor_air.flow_per_person
outdoor_air.flow_per_area
outdoor_air.air_changes_per_hour

outdoor_air.factor

outdoor_air.minimum_flow

outdoor_air.schedule
```

Auch hier ist eine führende Definition notwendig.

Beispielsweise:

```text
flow_per_person + flow_per_area
```

Nicht gleichzeitig alle möglichen Formulierungen als unabhängige Variablen behandeln.

---

# 6.8 Parametergruppe `NATURAL_VENTILATION`

Je Zone:

```text
natural_ventilation.enabled

natural_ventilation.max_air_change_rate
natural_ventilation.max_flow

natural_ventilation.window_opening_fraction

natural_ventilation.min_indoor_temperature
natural_ventilation.max_indoor_temperature

natural_ventilation.min_outdoor_temperature
natural_ventilation.max_outdoor_temperature

natural_ventilation.min_temperature_difference

natural_ventilation.max_wind_speed

natural_ventilation.co2_threshold

natural_ventilation.night_ventilation

natural_ventilation.schedule
```

---

# 6.9 Parametergruppe `ZONE_HVAC_ASSIGNMENT`

Je Zone:

```text
zone.heating_terminal_type
zone.cooling_terminal_type
zone.ventilation_system

zone.heating_available
zone.cooling_available
zone.mechanical_ventilation_available

zone.max_heating_power
zone.max_cooling_power
```

Hier können später auch unterschiedliche technische Systeme je Zone untersucht werden.

---

# 7. Eingabemodul TECHNOLOGY

Das Technikmodul ist objektorientiert aufzubauen.

Nicht:

```text
heating = einige Werte
```

sondern beispielsweise:

```text
Heating System
├── Generator
├── Hydraulic Loop
├── Pump
├── Distribution
├── Storage
└── Terminal Units
```

Dasselbe gilt für Kühlung und Lüftung.

---

# 7.1 Parametergruppe `HEATING_GENERATOR`

Jeder Wärmeerzeuger ist eine eigene Instanz:

```text
HG01
HG02
...
```

## Allgemeine Parameter

```text
heating_generator.type
heating_generator.energy_carrier

heating_generator.nominal_power
heating_generator.minimum_power
heating_generator.maximum_power

heating_generator.minimum_modulation
heating_generator.maximum_modulation

heating_generator.supply_temperature
heating_generator.return_temperature

heating_generator.minimum_supply_temperature
heating_generator.maximum_supply_temperature

heating_generator.auxiliary_power

heating_generator.standby_loss

heating_generator.control_strategy

heating_generator.operation_schedule
```

---

# 7.2 Heizkessel

Zusätzliche Parameter:

```text
boiler.nominal_efficiency
boiler.part_load_efficiency

boiler.condensing_operation

boiler.minimum_return_temperature

boiler.flue_gas_loss
boiler.radiation_loss
```

---

# 7.3 Wärmepumpe

Zusätzliche Parameter:

```text
heat_pump.source_type

heat_pump.nominal_cop
heat_pump.scop

heat_pump.nominal_heating_capacity

heat_pump.source_temperature

heat_pump.minimum_source_temperature
heat_pump.maximum_source_temperature

heat_pump.minimum_sink_temperature
heat_pump.maximum_sink_temperature

heat_pump.bivalence_temperature

heat_pump.capacity_curve
heat_pump.cop_curve

heat_pump.defrost_control

heat_pump.backup_heater_enabled
heat_pump.backup_heater_power
```

---

# 7.4 Parametergruppe `COOLING_GENERATOR`

Je Kälteerzeuger:

```text
CG01
CG02
```

Parameter:

```text
cooling_generator.type

cooling_generator.nominal_cooling_power
cooling_generator.minimum_cooling_power
cooling_generator.maximum_cooling_power

cooling_generator.eer
cooling_generator.seer
cooling_generator.cop

cooling_generator.part_load_curve

cooling_generator.chilled_water_supply_temperature
cooling_generator.chilled_water_return_temperature

cooling_generator.minimum_outdoor_temperature
cooling_generator.maximum_outdoor_temperature

cooling_generator.auxiliary_power

cooling_generator.control_strategy
```

---

# 7.5 Parametergruppe `HYDRAULIC_LOOP`

Je Heiz- oder Kühlkreis:

```text
hydraulic_loop.medium
hydraulic_loop.glycol_fraction

hydraulic_loop.supply_temperature
hydraulic_loop.return_temperature
hydraulic_loop.temperature_difference

hydraulic_loop.design_flow
hydraulic_loop.minimum_flow
hydraulic_loop.maximum_flow

hydraulic_loop.design_pressure
hydraulic_loop.pressure_drop

hydraulic_loop.temperature_control
hydraulic_loop.flow_control

hydraulic_loop.heating_curve
hydraulic_loop.cooling_curve

hydraulic_loop.outdoor_temperature_compensation

hydraulic_loop.operation_schedule
```

---

# 7.6 Parametergruppe `PUMP`

Je Pumpe:

```text
pump.type

pump.nominal_flow
pump.nominal_head

pump.electrical_power

pump.hydraulic_efficiency
pump.motor_efficiency
pump.total_efficiency

pump.variable_speed

pump.minimum_speed
pump.maximum_speed

pump.minimum_flow
pump.maximum_flow

pump.control_type

pump.pressure_setpoint

pump.performance_curve
pump.part_load_curve

pump.standby_power
```

---

# 7.7 Parametergruppe `PIPE_DISTRIBUTION`

Je Rohrnetz:

```text
pipe.total_length
pipe.supply_length
pipe.return_length

pipe.internal_diameter

pipe.material

pipe.insulation_material
pipe.insulation_thickness
pipe.insulation_conductivity

pipe.heat_loss_coefficient

pipe.design_flow

pipe.pressure_drop

pipe.environment_temperature

pipe.fraction_inside_conditioned_space
pipe.fraction_outside_conditioned_space
```

---

# 7.8 Parametergruppe `HEATING_TERMINAL`

Je Heizübergabesystem beziehungsweise je Zone:

```text
heating_terminal.type

heating_terminal.nominal_power
heating_terminal.maximum_power
heating_terminal.minimum_power

heating_terminal.design_supply_temperature
heating_terminal.design_return_temperature
heating_terminal.design_room_temperature

heating_terminal.water_flow

heating_terminal.convective_fraction
heating_terminal.radiative_fraction

heating_terminal.control_type
heating_terminal.setpoint

heating_terminal.time_constant
```

---

# 7.9 Heizkörper – zusätzliche Parameter

```text
radiator.exponent
radiator.water_content
radiator.thermal_mass
radiator.valve_type
radiator.valve_authority
```

---

# 7.10 Flächenheizung

```text
surface_heating.type

surface_heating.active_area

surface_heating.specific_power

surface_heating.pipe_spacing
surface_heating.pipe_diameter

surface_heating.installation_depth

surface_heating.supply_temperature
surface_heating.return_temperature

surface_heating.flow

surface_heating.floor_covering_resistance

surface_heating.maximum_surface_temperature

surface_heating.control_strategy
```

---

# 7.11 Parametergruppe `COOLING_TERMINAL`

Je Kühlübergabesystem:

```text
cooling_terminal.type

cooling_terminal.nominal_power
cooling_terminal.maximum_power
cooling_terminal.minimum_power

cooling_terminal.design_supply_temperature
cooling_terminal.design_return_temperature

cooling_terminal.water_flow

cooling_terminal.convective_fraction
cooling_terminal.radiative_fraction

cooling_terminal.control_type

cooling_terminal.setpoint

cooling_terminal.condensation_control
```

---

# 7.12 Fan Coil

```text
fan_coil.configuration

fan_coil.heating_power
fan_coil.total_cooling_power
fan_coil.sensible_cooling_power

fan_coil.air_flow

fan_coil.heating_water_flow
fan_coil.cooling_water_flow

fan_coil.heating_supply_temperature
fan_coil.heating_return_temperature

fan_coil.cooling_supply_temperature
fan_coil.cooling_return_temperature

fan_coil.fan_power

fan_coil.fan_speed_levels

fan_coil.control_type
```

---

# 7.13 Kühldecke / Kühlsegel

```text
radiant_cooling.active_area

radiant_cooling.nominal_power
radiant_cooling.specific_power

radiant_cooling.supply_temperature
radiant_cooling.return_temperature

radiant_cooling.water_flow

radiant_cooling.radiative_fraction
radiant_cooling.convective_fraction

radiant_cooling.minimum_supply_temperature

radiant_cooling.dew_point_control
```

---

# 7.14 Direkte Verdampfung / Splitgerät

```text
dx_unit.nominal_cooling_power
dx_unit.nominal_heating_power

dx_unit.eer
dx_unit.seer
dx_unit.cop
dx_unit.scop

dx_unit.air_flow

dx_unit.minimum_capacity
dx_unit.maximum_capacity

dx_unit.minimum_outdoor_temperature
dx_unit.maximum_outdoor_temperature

dx_unit.fan_power

dx_unit.control_strategy
```

---

# 7.15 Parametergruppe `AIR_HANDLING_UNIT`

Je Lüftungsgerät:

```text
AHU01
AHU02
```

Parameter:

```text
ahu.system_type

ahu.supply_air_flow
ahu.exhaust_air_flow

ahu.minimum_air_flow
ahu.maximum_air_flow

ahu.outdoor_air_fraction
ahu.recirculation_fraction

ahu.supply_air_temperature

ahu.minimum_supply_air_temperature
ahu.maximum_supply_air_temperature

ahu.operation_schedule

ahu.night_operation

ahu.free_cooling_enabled

ahu.demand_controlled_ventilation

ahu.co2_control

ahu.humidity_control

ahu.pressure_control

ahu.flow_control
```

---

# 7.16 Parametergruppe `HEAT_RECOVERY`

Je WRG:

```text
heat_recovery.type

heat_recovery.sensible_efficiency
heat_recovery.latent_efficiency

heat_recovery.temperature_efficiency
heat_recovery.moisture_efficiency

heat_recovery.supply_pressure_drop
heat_recovery.exhaust_pressure_drop

heat_recovery.frost_protection_temperature

heat_recovery.bypass_available
heat_recovery.bypass_control

heat_recovery.leakage_fraction

heat_recovery.auxiliary_power
```

---

# 7.17 Parametergruppe `FAN`

Je Ventilator:

```text
fan.type

fan.nominal_air_flow

fan.pressure_rise

fan.electrical_power

fan.total_efficiency
fan.motor_efficiency

fan.specific_fan_power

fan.variable_speed

fan.minimum_speed
fan.maximum_speed

fan.minimum_flow
fan.maximum_flow

fan.control_type

fan.performance_curve
fan.part_load_curve
```

---

# 7.18 Parametergruppe `AIR_FILTER`

Je Filter:

```text
filter.class

filter.initial_pressure_drop
filter.final_pressure_drop
filter.design_pressure_drop

filter.efficiency
```

---

# 7.19 Parametergruppe `HEATING_COIL`

```text
heating_coil.medium

heating_coil.nominal_power

heating_coil.air_flow
heating_coil.water_flow

heating_coil.air_inlet_temperature
heating_coil.air_outlet_temperature

heating_coil.water_supply_temperature
heating_coil.water_return_temperature

heating_coil.air_pressure_drop
heating_coil.water_pressure_drop

heating_coil.control_type
```

---

# 7.20 Parametergruppe `COOLING_COIL`

```text
cooling_coil.total_power
cooling_coil.sensible_power

cooling_coil.air_flow
cooling_coil.water_flow

cooling_coil.chilled_water_supply_temperature
cooling_coil.chilled_water_return_temperature

cooling_coil.air_inlet_temperature
cooling_coil.air_outlet_temperature

cooling_coil.air_inlet_humidity
cooling_coil.air_outlet_humidity

cooling_coil.air_pressure_drop
cooling_coil.water_pressure_drop

cooling_coil.control_type
```

---

# 7.21 Parametergruppe `HUMIDIFIER`

Optional:

```text
humidifier.type
humidifier.maximum_capacity
humidifier.electrical_power
humidifier.efficiency
humidifier.humidity_setpoint
humidifier.control_type
```

---

# 7.22 Parametergruppe `DEHUMIDIFIER`

Optional:

```text
dehumidifier.type
dehumidifier.maximum_capacity
dehumidifier.electrical_power
dehumidifier.humidity_setpoint
dehumidifier.control_type
```

---

# 7.23 Parametergruppe `AIR_DISTRIBUTION`

Je Kanalnetz:

```text
duct.total_length

duct.cross_section_area
duct.hydraulic_diameter

duct.air_velocity

duct.pressure_drop

duct.leakage_class

duct.insulation_material
duct.insulation_thickness
duct.insulation_conductivity

duct.environment_temperature

duct.silencer_pressure_drop
duct.damper_pressure_drop
```

---

# 7.24 Parametergruppe `AIR_TERMINAL`

Je Luftdurchlass bzw. je Zone:

```text
air_terminal.type

air_terminal.design_flow
air_terminal.minimum_flow
air_terminal.maximum_flow

air_terminal.discharge_temperature
air_terminal.discharge_velocity

air_terminal.discharge_direction

air_terminal.control_type

air_terminal.minimum_damper_position
```

---

# 7.25 Parametergruppe `THERMAL_STORAGE`

Je Heiz- oder Kältespeicher:

```text
storage.type

storage.volume
storage.usable_volume

storage.height
storage.diameter

storage.insulation_material
storage.insulation_thickness

storage.heat_loss_coefficient

storage.setpoint_temperature
storage.minimum_temperature
storage.maximum_temperature

storage.maximum_charge_power
storage.maximum_discharge_power

storage.maximum_charge_flow
storage.maximum_discharge_flow

storage.stratified

storage.number_of_layers

storage.standby_loss

storage.control_strategy
```

---

# 7.26 Parametergruppe `DOMESTIC_HOT_WATER`

Für zukünftige Systemgrenzen:

```text
dhw.enabled

dhw.demand
dhw.draw_profile

dhw.hot_water_temperature
dhw.cold_water_temperature

dhw.generator_type

dhw.storage_volume

dhw.storage_loss

dhw.circulation_enabled
dhw.circulation_flow
dhw.circulation_temperature

dhw.pipe_length
dhw.pipe_insulation_thickness

dhw.distribution_loss

dhw.generator_efficiency

dhw.operation_schedule
```

Für den aktuellen Small-Office-Test kann diese Parametergruppe deaktiviert bleiben.

---

# 7.27 Parametergruppe `PV_SYSTEM`

Je PV-Anlage:

```text
pv.module_area

pv.module_count

pv.nominal_module_power
pv.installed_power

pv.module_efficiency

pv.module_type

pv.orientation
pv.tilt

pv.temperature_coefficient

pv.nominal_operating_cell_temperature

pv.inverter_power
pv.inverter_efficiency

pv.mpp_efficiency

pv.cable_loss
pv.shading_loss
pv.soiling_loss

pv.system_loss
```

Beim Small Office:

```text
pv.orientation
pv.tilt
```

sollen möglichst aus der festen Dachgeometrie übernommen werden.

---

# 7.28 Parametergruppe `BATTERY_STORAGE`

```text
battery.nominal_capacity
battery.usable_capacity

battery.initial_soc
battery.minimum_soc
battery.maximum_soc

battery.maximum_charge_power
battery.maximum_discharge_power

battery.charge_efficiency
battery.discharge_efficiency

battery.round_trip_efficiency

battery.self_discharge

battery.standby_power

battery.control_strategy

battery.pv_surplus_charging
battery.grid_charging_allowed
battery.peak_shaving_enabled
```

---

# 7.29 Parametergruppe `ELECTRICAL_SYSTEM`

Optional:

```text
electrical.grid_connection_power

electrical.base_load

electrical.load_profile

electrical.grid_import_limit
electrical.grid_export_limit

electrical.self_consumption_control
electrical.load_management_strategy
```

---

# 7.30 Parametergruppe `CONTROL`

Regelparameter sollen technisch grundsätzlich dem jeweiligen Objekt zugeordnet werden.

Das System soll aber folgende allgemeine Regelparameter unterstützen:

```text
control.type

control.setpoint
control.setpoint_schedule

control.deadband
control.hysteresis

control.p_gain
control.i_gain
control.d_gain

control.minimum_runtime
control.minimum_offtime

control.enable_threshold
control.disable_threshold

control.outdoor_temperature_enable

control.load_enable

control.priority

control.sequence
```

Diese Parameter werden nur angezeigt, wenn sie für den jeweiligen Reglertyp relevant sind.

---

# 8. Eingabemodul WEATHER

Das Wettermodul wird bewusst **nicht als Parametergruppe mit einzelnen meteorologischen Variablen** behandelt.

Es besitzt im Input genau einen fachlichen Parameter:

```text
weather.weather_dataset
```

## Datentyp

```text
enum / dataset reference
```

## Beispielwerte

```text
Frankfurt_2015
Frankfurt_2016
Frankfurt_2017
...
```

Die im Datensatz enthaltenen Zeitreihen wie

```text
air_temperature
relative_humidity
direct_solar_radiation
diffuse_solar_radiation
wind_speed
wind_direction
air_pressure
```

sind **keine Eingabeparameter**.

Sie sind Inhalte des ausgewählten Wetterdatensatzes.

Das Programm darf diese Werte lesen und verwenden, aber sie dürfen nicht im Variantengenerator als einzelne Parameter erscheinen.

---

# 9. Anforderungen an das zentrale Parameter-Datenmodell

Codex soll ein gemeinsames Parameterschema implementieren.

Mindestens:

```text
ParameterDefinition
```

mit:

```text
id
module
category
group
name

display_name
description

datatype
unit

lod_min
lod_max

source

value

default_value

allowed_values
min_value
max_value
step

editable
variant_capable
derived

required
optional

depends_on

calculation_rule

validation_rule
```

---

# 10. Parametergruppen-Datenmodell

Zusätzlich:

```text
ParameterGroup
```

mit:

```text
id
module
category
group_type

display_name

instance_type

repeatable

parameters[]

children[]
```

Beispiel:

```text
ParameterGroup:
    id: FE01
    module: BUILDING
    category: WINDOWS
    group_type: WINDOW_TYPE
```

---

# 11. Objektinstanzen und Typen trennen

Besonders wichtig für:

```text
Fenster
Türen
Konstruktionen
Heizkörper
Luftdurchlässe
Pumpen
```

Beispiel Fenster:

```text
WindowInstance:
    id: WINDOW_001
    type_ref: FE01
    host_surface_ref: WALL_017
    zone_ref: Z03
```

Die konkreten physikalischen Eigenschaften liegen auf:

```text
WindowType FE01
```

Dadurch müssen gleiche Produkte nicht mehrfach parametriert werden.

---

# 12. Verhalten der IFC-Geometrie im Small Office

Codex soll die IFC nicht als editierbare Variantenquelle behandeln.

Alle geometrischen Parameter werden importiert.

Beispiel:

```text
building.geometry.length
```

Resultat:

```text
value = <IFC value>
source = IFC
editable = false
variant_capable = false
```

Dasselbe gilt für:

```text
Gebäudebreite
Gebäudehöhe
Geschosshöhen
Raumgeometrien
Zonengeometrien
Fensterpositionen
Fenstergrößen
Türpositionen
Türgrößen
Wandflächen
Dachflächen
Bodenflächen
```

Die Werte müssen dennoch in UI und Datenmodell sichtbar sein.

---

# 13. Variantenlogik

Der Variantengenerator darf ausschließlich Parameter anbieten, bei denen

```text
editable == true
AND
variant_capable == true
```

gilt.

Beispiel:

```text
building.windows.FE01.u_value

editable = true
variant_capable = true
```

→ im Variantengenerator sichtbar.

Dagegen:

```text
building.geometry.length

editable = false
variant_capable = false
```

→ nur anzeigen.

---

# 14. Abhängigkeiten

Codex muss Parameterabhängigkeiten unterstützen.

Beispiel U-Wert:

```text
AW01.u_value
```

wird berechnet aus:

```text
AW01.layer_01
AW01.layer_02
...
```

Wenn Schichten vollständig vorhanden sind:

```text
u_value.editable = false
u_value.derived = true
```

---

# 15. Abhängigkeiten bei Produktwahl

Beispiel:

```text
FE01.product
```

Auswahl:

```text
Window_Product_X
```

kann automatisch setzen:

```text
Uw
Ug
Uf
g
visible_transmittance
frame_fraction
```

Der Benutzer darf entweder:

1. ein Produkt auswählen,

oder

2. ein benutzerdefiniertes Fenster definieren.

Nicht beide Methoden gleichzeitig als widersprüchliche Datenquellen verwenden.

---

# 16. Abhängigkeiten bei Zonenbelegung

Es darf beispielsweise nicht gleichzeitig unabhängig eingegeben werden:

```text
person_count
person_density
area_per_person
```

Es muss eine führende Methode geben.

Beispiel:

```text
occupancy_input_method = PERSON_DENSITY
```

Dann:

```text
person_density = INPUT
person_count = DERIVED
area_per_person = DERIVED
```

---

# 17. Abhängigkeiten bei Außenluft

Entsprechend:

```text
outdoor_air_input_method
```

Möglichkeiten:

```text
TOTAL_FLOW
FLOW_PER_PERSON
FLOW_PER_AREA
ACH
COMBINED
```

Nur für die gewählte Methode relevante Eingaben werden aktiviert.

---

# 18. Abhängigkeiten bei Luftdichtheit

```text
air_tightness_input_method
```

beispielsweise:

```text
N50
Q50
EFFECTIVE_LEAKAGE_AREA
```

Andere Größen werden entsprechend berechnet oder deaktiviert.

---

# 19. UI-Anforderungen

Die Benutzeroberfläche soll zunächst nach Eingabemodulen aufgebaut werden:

```text
Gebäude
Zonen
Technik
Wetter
```

Innerhalb eines Moduls nach Parametergruppen.

Beispiel Gebäude:

```text
Gebäude
├── Geometrie
├── Konstruktionen
│   ├── AW01
│   ├── IW01
│   ├── DA01
│   └── BP01
├── Fenster
│   ├── FE01
│   └── FE02
├── Türen
├── Sonnenschutz
└── Luftdichtheit
```

Technik:

```text
Technik
├── Heizung
│   ├── Wärmeerzeuger
│   ├── Heizkreis
│   ├── Pumpen
│   ├── Verteilung
│   ├── Speicher
│   └── Übergabe
│
├── Kühlung
│   ├── Kälteerzeuger
│   ├── Kältekreis
│   ├── Pumpen
│   └── Übergabe
│
├── Lüftung
│   ├── AHU
│   ├── WRG
│   ├── Ventilatoren
│   ├── Filter
│   ├── Register
│   ├── Kanalnetz
│   └── Luftdurchlässe
│
├── PV
├── Batterie
└── Trinkwarmwasser
```

Zonen:

```text
Zonen
├── Z01
│   ├── Raumklima
│   ├── Personen
│   ├── Beleuchtung
│   ├── Geräte
│   ├── Lüftung
│   └── HVAC
├── Z02
├── Z03
├── Z04
└── Z05
```

Wetter:

```text
Wetter
└── Wetterdatensatz
```

---

# 20. Darstellung gesperrter Parameter

IFC-Parameter dürfen nicht ausgeblendet werden.

Beispiel UI:

```text
Gebäudelänge

24.80 m

Quelle: IFC
LOD: 2
Status: Gesperrt
```

Dadurch ist nachvollziehbar, welche Eingaben tatsächlich in das Simulationsmodell eingehen.

---

# 21. Darstellung abgeleiteter Parameter

Beispiel:

```text
Fensterflächenanteil

0.31

Quelle: Berechnet
Status: Abgeleitet
```

Optional sollte die Berechnungsgrundlage angezeigt werden können.

Beispiel:

```text
window_area / facade_area
```

---

# 22. Darstellung von Variantenparametern

Beispiel:

```text
Fenster FE01
→ Uw

Basiswert:
1.30 W/(m²K)

Varianten:
1.10
0.90
0.70
```

---

# 23. Keine künstliche Begrenzung der Parameterzahl

Der Code darf keine Logik enthalten wie:

```text
MAX_PARAMETERS = 84
```

Die Parameteranzahl ergibt sich dynamisch aus:

```text
Anzahl Konstruktionen
+
Anzahl Schichten
+
Anzahl Fenstertypen
+
Anzahl Türtypen
+
Anzahl Zonen
+
Anzahl technischer Komponenten
+
deren jeweiligen Parametern
```

Ein reales Referenzmodell kann daher problemlos mehrere hundert adressierbare Parameter enthalten.

---

# 24. Small-Office-Referenzmodell

Für das aktuelle Referenzgebäude soll Codex zunächst die tatsächlich vorhandenen Parametergruppen aus dem bestehenden Projekt extrahieren.

Mindestens untersuchen:

```text
BUILDING

Außenwandtypen
Innenwandtypen
Dachtypen
Bodenplatten
Deckentypen

Fenstertypen
Türtypen

Sonnenschutz

Luftdichtheit
```

Danach:

```text
ZONES

Z01
Z02
Z03
Z04
Z05
```

Danach:

```text
TECHNOLOGY

Heating Generator
Heating Distribution
Heating Terminal

Cooling Generator
Cooling Distribution
Cooling Terminal

AHU
Heat Recovery
Fans
Pumps
Storage

PV
```

Danach:

```text
WEATHER

weather_dataset
```

---

# 25. Wichtig: Projektbestand zuerst inventarisieren

Codex soll **nicht sofort neue Werte erfinden**.

Erste Aufgabe:

> Suche im bestehenden Projekt nach allen aktuell definierten Inputparametern, Konfigurationsdateien, Schemas, Katalogen und Standardwerten.

Insbesondere suchen nach Begriffen wie:

```text
parameter
input
config
building
zone
technical
technology
weather
window
door
construction
material
wall
roof
floor
heating
cooling
ventilation
ahu
pump
pv
battery
storage
```

Danach alle vorhandenen Parameter dem neuen Schema zuordnen.

---

# 26. Migration der bisherigen Parameter

Für jeden vorhandenen Parameter feststellen:

```text
1. Welches Eingabemodul?
2. Welche Parametergruppe?
3. Welches konkrete Objekt?
4. Ist es ein echter fachlicher Parameter?
5. Ist es Metadatum?
6. Ist es abgeleitet?
7. Welche Einheit?
8. Welcher Datentyp?
9. Welcher LOD?
10. Ist es editierbar?
11. Ist es variierbar?
12. Was ist seine Quelle?
13. Welche Abhängigkeiten existieren?
```

Metadaten wie:

```text
schema_version
revision
file_path
hash
export_timestamp
workflow_state
variation_locked
```

dürfen nicht als fachliche Parameter gezählt werden.

Sie können weiterhin Bestandteil technischer Konfigurationsobjekte sein.

---

# 27. Ziel-Datenstruktur

Beispiel:

```json
{
  "module": "BUILDING",
  "category": "WINDOWS",
  "group": "FE01",
  "parameter": "u_value",
  "display_name": "Fenster-U-Wert",
  "datatype": "float",
  "unit": "W/(m²K)",
  "lod_min": 1,
  "source": "USER",
  "value": 1.1,
  "editable": true,
  "variant_capable": true,
  "derived": false
}
```

IFC-Beispiel:

```json
{
  "module": "BUILDING",
  "category": "GEOMETRY",
  "group": "BUILDING_GEOMETRY",
  "parameter": "length",
  "display_name": "Gebäudelänge",
  "datatype": "float",
  "unit": "m",
  "lod_min": 1,
  "source": "IFC",
  "value": 24.8,
  "editable": false,
  "variant_capable": false,
  "derived": false
}
```

Abgeleitet:

```json
{
  "module": "BUILDING",
  "category": "GEOMETRY",
  "group": "BUILDING_GEOMETRY",
  "parameter": "window_wall_ratio",
  "datatype": "float",
  "unit": "-",
  "source": "DERIVED",
  "editable": false,
  "variant_capable": false,
  "derived": true
}
```

---

# 28. Validierung

Codex soll Validierungsregeln implementieren.

Beispiele:

```text
0 < g_value <= 1

u_value > 0

thermal_conductivity > 0

density > 0

specific_heat_capacity > 0

0 <= efficiency <= 1
```

Ausnahmen:

```text
COP
EER
SCOP
SEER
```

dürfen größer als 1 sein.

Weiter:

```text
cooling_setpoint > heating_setpoint

minimum_soc < maximum_soc

minimum_power <= nominal_power <= maximum_power

return_temperature < supply_temperature
```

für Heizsysteme.

Für Kaltwasser:

```text
supply_temperature < return_temperature
```

---

# 29. Einheiten

Intern möglichst SI-Einheiten verwenden.

Bevorzugte Grundeinheiten:

```text
Länge                 m
Fläche                m²
Volumen               m³

Leistung              W
spezifische Leistung  W/m²

Energie               Wh oder kWh

Temperatur            °C
Temperaturdifferenz   K

Volumenstrom          m³/s intern
Anzeige ggf.          m³/h

Massenstrom           kg/s

Druck                 Pa

Wärmeleitfähigkeit    W/(mK)

U-Wert                W/(m²K)

Wärmekapazität        J/(kgK)

Dichte                kg/m³
```

Umrechnungen sollen zentral erfolgen.

---

# 30. Variantengenerator

Der Variantengenerator soll nicht länger von einer statischen Parameterliste abhängen.

Vorgehensweise:

```text
all_parameters
    ↓
filter editable
    ↓
filter variant_capable
    ↓
filter dependencies
    ↓
filter active systems
    ↓
show to user
```

Beispiel:

Wenn keine Batterie aktiv ist:

```text
battery.*
```

nicht zur Variantenwahl anbieten.

Wenn eine Batterie aktiviert wird:

```text
battery.nominal_capacity
battery.max_charge_power
battery.max_discharge_power
...
```

aktivieren.

---

# 31. Variantengruppen

Zusätzlich zu Einzelparametern soll das Programm später ganze Parametergruppen variieren können.

Beispiel:

```text
Window Type FE01
```

Variante A:

```text
Uw = 1.3
g = 0.60
```

Variante B:

```text
Uw = 0.9
g = 0.50
```

Variante C:

```text
Uw = 0.7
g = 0.40
```

Damit können Produktalternativen als konsistente Parameterpakete verwendet werden.

Dasselbe für:

```text
Wandaufbau
Wärmepumpe
Kältemaschine
AHU
Pumpe
PV-Modul
```

---

# 32. Produktkatalog

Produktparameter sollen langfristig mit Produktdatensätzen verbunden werden können.

Beispiel:

```text
FE01.product = Window_A
```

Produkt enthält:

```text
Uw
Ug
Uf
g
tau_v
frame_fraction
```

Alternativ:

```text
FE01.product = CUSTOM
```

Dann werden Einzelparameter freigegeben.

Dasselbe Prinzip soll für folgende Kategorien vorbereitet werden:

```text
Fenster
Türen
Materialien

Wärmeerzeuger
Wärmepumpen
Kältemaschinen

Pumpen
Ventilatoren
AHUs

PV-Module
Wechselrichter
Batterien
```

---

# 33. Reihenfolge der Implementierung

## Phase 1 – Bestandsanalyse

- bestehende Parameter suchen
- bestehende Schemas analysieren
- vorhandene Produktkataloge analysieren
- vorhandene UI-Eingaben erfassen
- vorhandene Variantenparameter erfassen
- bestehende Abhängigkeiten dokumentieren

## Phase 2 – neues Kernschema

Implementieren:

```text
ParameterDefinition
ParameterGroup
ParameterInstance
ParameterSource
ParameterStatus
LODDefinition
```

## Phase 3 – Building

Implementieren:

```text
Geometry
Opaque Constructions
Materials
Windows
Doors
Shading
Thermal Bridges
Air Tightness
```

## Phase 4 – Zones

Implementieren:

```text
Geometry
Thermal Control
Occupancy
Lighting
Equipment
Outdoor Air
Natural Ventilation
HVAC Assignment
```

## Phase 5 – Technology

Implementieren:

```text
Heating
Cooling
Hydraulics
Distribution
Terminals
Ventilation
AHU
WRG
Fans
Coils
Air Distribution
Storage
PV
Battery
```

## Phase 6 – Weather

Implementieren ausschließlich:

```text
weather_dataset
```

## Phase 7 – UI

Hierarchische Darstellung nach:

```text
Input Module
→ Parameter Group
→ Parameter
```

## Phase 8 – Variantengenerator

Nur zulässige Parameter dynamisch übernehmen.

## Phase 9 – Small-Office-Migration

Bestehende Small-Office-Werte in neues Schema überführen.

## Phase 10 – Tests

Unit Tests und Integrationstests.

---

# 34. Erforderliche Tests

## Parameter-Schema

Test:

```text
Jeder Parameter besitzt eindeutige ID.
```

Test:

```text
Jeder numerische Parameter besitzt eine Einheit.
```

Test:

```text
Derived Parameter ist nicht editierbar.
```

Test:

```text
IFC-geführte LOD-2-Geometrie ist nicht variierbar.
```

Test:

```text
Variant Parameter muss editierbar sein.
```

---

# 35. Fenster-Test

Anlegen:

```text
FE01
FE02
```

Prüfen:

- unterschiedliche Uw-Werte
- unterschiedliche g-Werte
- unterschiedliche Rahmenanteile
- mehrere Fensterinstanzen referenzieren denselben Fenstertyp
- Änderung FE01 wirkt auf alle FE01-Instanzen
- FE02 bleibt unverändert

---

# 36. Konstruktionstest

Anlegen:

```text
AW01
```

mit mehreren Schichten.

Ändern:

```text
Dämmstoffdicke
```

Prüfen:

```text
U-Wert wird neu berechnet.
```

Anschließend Material ändern.

Prüfen:

```text
lambda
rho
cp
```

werden korrekt übernommen beziehungsweise aktualisiert.

---

# 37. Zonentest

Z01–Z05 anlegen.

Unterschiedliche:

```text
heating_setpoint
cooling_setpoint
occupancy
lighting
equipment
outdoor_air
```

setzen.

Prüfen, dass die Parameter zonenspezifisch bleiben.

---

# 38. Heizsystemtest

Anlegen:

```text
HG01
```

mit:

```text
type
nominal_power
efficiency
supply_temperature
return_temperature
```

Varianten erzeugen.

Prüfen, dass technische Varianten korrekt in den Simulation Input gelangen.

---

# 39. Wettertest

Mehrere Wetterdatensätze anbieten.

Beispiel:

```text
Frankfurt_A
Frankfurt_B
Frankfurt_C
```

Prüfen:

```text
weather_dataset
```

ist genau **ein Variantenparameter**.

Keine meteorologische Einzelgröße darf im Variantengenerator auftauchen.

---

# 40. Akzeptanzkriterien

Die Umstellung ist erfolgreich, wenn:

1. keine feste 84-Parameter-Struktur mehr existiert;

2. Parameter dynamisch aus Parametergruppen erzeugt werden;

3. Building, Zones, Technology und Weather ein gemeinsames Parameterschema verwenden;

4. IFC-Geometrie im LOD-2-Small-Office sichtbar, aber gesperrt ist;

5. Konstruktionen auf Schichtebene verändert werden können;

6. mehrere Fenster- und Türtypen mit eigenen Parametern unterstützt werden;

7. Zonen vollständig getrennte Nutzungs- und Sollwertparameter besitzen;

8. Heizungs-, Kühlungs- und Lüftungssysteme in fachlich sinnvolle technische Komponenten zerlegt sind;

9. unterschiedliche Produkte desselben Systemtyps unterstützt werden;

10. nur zulässige Parameter im Variantengenerator erscheinen;

11. Wetter als genau ein Parameter `weather_dataset` behandelt wird;

12. abgeleitete Größen nicht unabhängig variiert werden können;

13. Parameterabhängigkeiten sauber aufgelöst werden;

14. das bestehende Small Office vollständig auf die neue Struktur migriert werden kann;

15. zukünftige LOD-1-Modelle dieselben Parameterdefinitionen nutzen können, wobei die Gebäudegeometrie dort editierbar wird.

---

# 41. Arbeitsauftrag an Codex

## Schritt 1

Analysiere zuerst das bestehende Repository vollständig.

Suche insbesondere nach:

```text
Input-Modulen
Parameterdefinitionen
Schemas
JSON/YAML-Konfigurationen
Pydantic-/Dataclass-Modellen
Enums
Produktkatalogen
IFC-Import
Zonenlogik
Technikdefinitionen
Wetterauswahl
Variantengenerator
GUI-Komponenten
Tests
```

## Schritt 2

Erstelle eine Bestandsmatrix:

```text
bestehender Parameter
→ neues Modul
→ neue Parametergruppe
→ neuer Parametername
→ Einheit
→ Quelle
→ LOD
→ editable
→ variant_capable
```

## Schritt 3

Vergleiche die vorhandenen Parameter mit diesem Masterkatalog.

Markiere:

```text
EXISTS
MISSING
PARTIAL
REDUNDANT
METADATA
DERIVED
```

## Schritt 4

Entwirf das neue Schema so, dass bestehende Projektteile möglichst migriert und nicht unnötig dupliziert werden.

## Schritt 5

Implementiere zunächst das Schema und die Migration.

Noch keine unnötige Änderung der Simulationslogik vornehmen.

## Schritt 6

Implementiere anschließend Modul für Modul:

```text
BUILDING
→ ZONES
→ TECHNOLOGY
→ WEATHER
```

## Schritt 7

Passe danach GUI und Variantengenerator an.

## Schritt 8

Erweitere Tests.

---

# 42. Wichtigste fachliche Leitlinie

Die wichtigste Regel des gesamten Refactorings lautet:

> Das feste Referenzgebäude definiert die geometrische Realität. Die Parameterstudie verändert die Eigenschaften der Bauteile, Konstruktionen, Nutzungen und technischen Systeme innerhalb dieser Realität.

Daraus folgt für das aktuelle LOD-2-Small-Office:

```text
Primäre Gebäudegeometrie
= sichtbar
= Parameter
= IFC
= FIXED
= NICHT VARIIERBAR
```

aber:

```text
Materialaufbauten
Fenstereigenschaften
Türeigenschaften
Nutzungsparameter
Solltemperaturen
interne Lasten
Außenluft
Heizung
Kühlung
Lüftung
Speicher
PV
Wetterdatensatz
```

sind abhängig vom konkreten Parameter grundsätzlich:

```text
EDITABLE
und/oder
VARIANT_CAPABLE
```

Damit entsteht aus der bisherigen flachen Parameterliste ein langfristig belastbares, LOD-fähiges und produktorientiertes Inputmodell.