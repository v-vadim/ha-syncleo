"""Draft ventilation profiles from individual Hommyn JSON layouts."""

from homeassistant.components.fan import FanEntityFeature
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import (
    CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    CONCENTRATION_PARTS_PER_MILLION,
    PERCENTAGE,
    # UnitOfDensity,  # Not available in the minimum supported HA 2026.5.0.
    UnitOfTemperature,
    UnitOfTime,
)

from ..const import (
    FEATURE_AUTO_OFF_BACKLIGHT,
    FEATURE_CHILD_LOCK,
    FEATURE_CURRENT_CO2,
    FEATURE_CURRENT_HUMIDITY,
    FEATURE_CURRENT_PM2,
    FEATURE_CURRENT_TEMPERATURE,
    FEATURE_EXHAUST_FAN_SPEED,
    FEATURE_EXPENDABLES_FILTER,
    FEATURE_EXPENDABLES_PREFILTER,
    FEATURE_IONIZATION,
    FEATURE_OPERATING_MODE,
    FEATURE_ULTRAVIOLET,
    FEATURE_VALVE_POSITION,
    FEATURE_VOLUME,
    PD_ANTI_FROST,
    PD_AUTO_TEMPERATURE,
    PD_AUTO_VALVE_POSITION,
    PD_BYPASS_RANGE,
    PD_BYPASS_TEMPERATURE,
    PD_DEVICE_ID,
    PD_DISPLAY_BRIGHTNESS,
    PD_FILTER_DAYS,
    PD_FILTER_RUNNING_DAYS,
    PD_FILTER_TRACKING,
    PD_HEATER_START_TEMPERATURE,
    PD_HYSTERESIS,
    PD_INTERVAL_VALVE_POSITION,
    PD_LAMP_RUNNING_HOURS,
    PD_LAST_PROGRAM,
    PD_LIGHT_TIME,
    PD_MODBUS,
    PD_OUTDOOR_AIR_TEMPERATURE,
    PD_PREHEATER_START_TEMPERATURE,
    PD_RETURN_AIR_TEMPERATURE,
    PD_TVOC,
    PD_VALVE_CLOSING_TEMPERATURE,
    PD_VALVE_IS_CLOSING,
    PD_VENTILATION_DURATION,
    PD_VENTILATION_INTERVAL,
    PRESET_MANUAL,
    PROFILE_TYPE_VENTILATION,
    VENDOR_RUSCLIMATE,
)
from .profiles import (
    NumberConfig,
    ProgramDataField,
    SelectConfig,
    SensorConfig,
    VentilationControlProfile,
    VentilationProfile,
)

PROFILES = [
    VentilationControlProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=27,
        program_data_fields={
            PD_DISPLAY_BRIGHTNESS: ProgramDataField(
                mode=0, offset=0, size=1, min_value=0, max_value=2, step=1
            ),
            PD_MODBUS: ProgramDataField(
                mode=0, offset=1, size=1, min_value=0, max_value=1, step=1
            ),
            PD_FILTER_RUNNING_DAYS: ProgramDataField(
                mode=1, offset=0, size=1, min_value=0, max_value=255, step=1
            ),
            PD_LAMP_RUNNING_HOURS: ProgramDataField(
                mode=1, offset=1, size=2, min_value=0, max_value=65536, step=1
            ),
        },
        selects={
            FEATURE_OPERATING_MODE: SelectConfig(options_map={"off": 0, "auto": 1}),
            PD_DISPLAY_BRIGHTNESS: SelectConfig(
                options_map={"10%": 0, "50%": 1, "100%": 2}
            ),
        },
        sensors={
            PD_FILTER_RUNNING_DAYS: SensorConfig(unit_of_measurement=UnitOfTime.DAYS),
            PD_LAMP_RUNNING_HOURS: SensorConfig(unit_of_measurement=UnitOfTime.HOURS),
            PD_MODBUS: SensorConfig(),
        },
        switches=[FEATURE_IONIZATION, FEATURE_CHILD_LOCK],
    ),
    VentilationProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=34,
        profile_type=PROFILE_TYPE_VENTILATION,
        supported_features=FanEntityFeature.SET_SPEED
        | FanEntityFeature.PRESET_MODE
        | FanEntityFeature.TURN_OFF
        | FanEntityFeature.TURN_ON,
        speed_count=3,
        preset_modes_map={PRESET_MANUAL: 1, "sync": 2},
        default_preset_mode=PRESET_MANUAL,
        program_data_fields={
            PD_FILTER_DAYS: ProgramDataField(
                mode=0, offset=0, size=1, min_value=0, max_value=3, step=1
            ),
            PD_ANTI_FROST: ProgramDataField(
                mode=0, offset=1, size=1, min_value=0, max_value=1, step=1
            ),
            PD_BYPASS_TEMPERATURE: ProgramDataField(
                mode=1, offset=0, size=1, min_value=5, max_value=30, step=1
            ),
            PD_BYPASS_RANGE: ProgramDataField(
                mode=1, offset=1, size=1, min_value=2, max_value=15, step=1
            ),
            PD_RETURN_AIR_TEMPERATURE: ProgramDataField(
                mode=2, offset=0, size=1, min_value=0, max_value=255, step=1
            ),
            PD_OUTDOOR_AIR_TEMPERATURE: ProgramDataField(
                mode=2, offset=1, size=1, min_value=0, max_value=255, step=1
            ),
            PD_LAST_PROGRAM: ProgramDataField(
                mode=3, offset=0, size=1, min_value=1, max_value=2, step=1
            ),
        },
        numbers=[FEATURE_EXHAUST_FAN_SPEED, PD_BYPASS_TEMPERATURE, PD_BYPASS_RANGE],
        number_configs={
            FEATURE_EXHAUST_FAN_SPEED: NumberConfig(min_value=1, max_value=3),
        },
        selects={
            PD_FILTER_DAYS: SelectConfig(
                options_map={"45_days": 0, "60_days": 1, "90_days": 2, "180_days": 3}
            ),
        },
        sensors={
            FEATURE_CURRENT_HUMIDITY: SensorConfig(
                device_class=SensorDeviceClass.HUMIDITY,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=PERCENTAGE,
            ),
            FEATURE_CURRENT_CO2: SensorConfig(
                device_class=SensorDeviceClass.CO2,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=CONCENTRATION_PARTS_PER_MILLION,
            ),
            FEATURE_CURRENT_PM2: SensorConfig(
                device_class=SensorDeviceClass.PM25,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
                # TODO: migrate before HA 2027.8 removes the legacy constant.
                # unit_of_measurement=UnitOfDensity.MICROGRAMS_PER_CUBIC_METER,
            ),
            FEATURE_EXPENDABLES_FILTER: SensorConfig(
                unit_of_measurement=PERCENTAGE, value_fn=lambda v: v[0] if v else None
            ),
        },
    ),
    VentilationProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=36,
        profile_type=PROFILE_TYPE_VENTILATION,
        supported_features=FanEntityFeature.SET_SPEED
        | FanEntityFeature.PRESET_MODE
        | FanEntityFeature.TURN_OFF
        | FanEntityFeature.TURN_ON,
        speed_count=10,
        preset_modes_map={PRESET_MANUAL: 1, "sync": 2},
        default_preset_mode=PRESET_MANUAL,
        program_data_fields={
            PD_FILTER_DAYS: ProgramDataField(
                mode=0, offset=0, size=1, min_value=0, max_value=3, step=1
            ),
            PD_ANTI_FROST: ProgramDataField(
                mode=0, offset=1, size=1, min_value=0, max_value=1, step=1
            ),
            PD_BYPASS_TEMPERATURE: ProgramDataField(
                mode=1, offset=0, size=1, min_value=5, max_value=30, step=1
            ),
            PD_BYPASS_RANGE: ProgramDataField(
                mode=1, offset=1, size=1, min_value=2, max_value=15, step=1
            ),
            PD_RETURN_AIR_TEMPERATURE: ProgramDataField(
                mode=2, offset=0, size=1, min_value=0, max_value=255, step=1
            ),
            PD_OUTDOOR_AIR_TEMPERATURE: ProgramDataField(
                mode=2, offset=1, size=1, min_value=0, max_value=255, step=1
            ),
            PD_LAST_PROGRAM: ProgramDataField(
                mode=3, offset=0, size=1, min_value=1, max_value=2, step=1
            ),
        },
        numbers=[FEATURE_EXHAUST_FAN_SPEED, PD_BYPASS_TEMPERATURE, PD_BYPASS_RANGE],
        number_configs={
            FEATURE_EXHAUST_FAN_SPEED: NumberConfig(min_value=1, max_value=10),
        },
        selects={
            PD_FILTER_DAYS: SelectConfig(
                options_map={"45_days": 0, "60_days": 1, "90_days": 2, "180_days": 3}
            ),
        },
        sensors={
            FEATURE_CURRENT_HUMIDITY: SensorConfig(
                device_class=SensorDeviceClass.HUMIDITY,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=PERCENTAGE,
            ),
            FEATURE_CURRENT_CO2: SensorConfig(
                device_class=SensorDeviceClass.CO2,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=CONCENTRATION_PARTS_PER_MILLION,
            ),
            FEATURE_CURRENT_PM2: SensorConfig(
                device_class=SensorDeviceClass.PM25,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
                # TODO: migrate before HA 2027.8 removes the legacy constant.
                # unit_of_measurement=UnitOfDensity.MICROGRAMS_PER_CUBIC_METER,
            ),
            FEATURE_EXPENDABLES_FILTER: SensorConfig(
                unit_of_measurement=PERCENTAGE, value_fn=lambda v: v[0] if v else None
            ),
        },
    ),
    VentilationProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=98,
        profile_type=PROFILE_TYPE_VENTILATION,
        supported_features=FanEntityFeature.SET_SPEED
        | FanEntityFeature.PRESET_MODE
        | FanEntityFeature.TURN_OFF
        | FanEntityFeature.TURN_ON,
        speed_count=6,
        preset_modes_map={
            "energy_recovery": 3,
            "mixed_air": 4,
            "purification": 5,
            "supply_air": 6,
        },
        default_preset_mode="energy_recovery",
        program_data_fields={
            PD_TVOC: ProgramDataField(
                mode=0, offset=0, size=2, min_value=0, max_value=10000, step=1
            ),
            PD_LIGHT_TIME: ProgramDataField(
                mode=0, offset=2, size=1, min_value=20, max_value=60, step=1
            ),
            PD_DEVICE_ID: ProgramDataField(
                mode=0, offset=3, size=1, min_value=0, max_value=127, step=1
            ),
            PD_HEATER_START_TEMPERATURE: ProgramDataField(
                mode=1, offset=0, size=1, min_value=0, max_value=20, step=1
            ),
            PD_PREHEATER_START_TEMPERATURE: ProgramDataField(
                mode=1, offset=1, size=1, min_value=0, max_value=40, step=1
            ),
            PD_LAST_PROGRAM: ProgramDataField(
                mode=3, offset=0, size=1, min_value=0, max_value=6, step=1
            ),
        },
        numbers=[PD_LIGHT_TIME, PD_HEATER_START_TEMPERATURE],
        sensors={
            FEATURE_CURRENT_TEMPERATURE: SensorConfig(
                device_class=SensorDeviceClass.TEMPERATURE,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTemperature.CELSIUS,
            ),
            FEATURE_CURRENT_HUMIDITY: SensorConfig(
                device_class=SensorDeviceClass.HUMIDITY,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=PERCENTAGE,
            ),
            FEATURE_CURRENT_CO2: SensorConfig(
                device_class=SensorDeviceClass.CO2,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=CONCENTRATION_PARTS_PER_MILLION,
            ),
            FEATURE_CURRENT_PM2: SensorConfig(
                device_class=SensorDeviceClass.PM25,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
                # TODO: migrate before HA 2027.8 removes the legacy constant.
                # unit_of_measurement=UnitOfDensity.MICROGRAMS_PER_CUBIC_METER,
            ),
            PD_TVOC: SensorConfig(),
            FEATURE_EXPENDABLES_FILTER: SensorConfig(
                unit_of_measurement=PERCENTAGE, value_fn=lambda v: v[0] if v else None
            ),
        },
        switches=[FEATURE_CHILD_LOCK, FEATURE_IONIZATION, FEATURE_ULTRAVIOLET],
    ),
    VentilationProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=100,
        profile_type=PROFILE_TYPE_VENTILATION,
        supported_features=FanEntityFeature.SET_SPEED
        | FanEntityFeature.PRESET_MODE
        | FanEntityFeature.TURN_OFF
        | FanEntityFeature.TURN_ON,
        speed_count=6,
        preset_modes_map={"on": 1},
        default_preset_mode="on",
        program_data_fields={
            PD_TVOC: ProgramDataField(
                mode=0, offset=0, size=2, min_value=0, max_value=10000, step=1
            ),
            PD_LIGHT_TIME: ProgramDataField(
                mode=0, offset=2, size=1, min_value=10, max_value=60, step=1
            ),
            PD_DEVICE_ID: ProgramDataField(
                mode=0, offset=3, size=1, min_value=0, max_value=127, step=1
            ),
            PD_BYPASS_TEMPERATURE: ProgramDataField(
                mode=1, offset=0, size=1, min_value=5, max_value=30, step=1
            ),
            PD_BYPASS_RANGE: ProgramDataField(
                mode=1, offset=1, size=1, min_value=2, max_value=15, step=1
            ),
            PD_RETURN_AIR_TEMPERATURE: ProgramDataField(
                mode=2, offset=0, size=1, min_value=0, max_value=255, step=1
            ),
            PD_OUTDOOR_AIR_TEMPERATURE: ProgramDataField(
                mode=2, offset=1, size=1, min_value=0, max_value=255, step=1
            ),
            PD_LAST_PROGRAM: ProgramDataField(
                mode=3, offset=0, size=1, min_value=0, max_value=6, step=1
            ),
        },
        numbers=[PD_LIGHT_TIME],
        sensors={
            FEATURE_CURRENT_TEMPERATURE: SensorConfig(
                device_class=SensorDeviceClass.TEMPERATURE,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTemperature.CELSIUS,
            ),
            FEATURE_CURRENT_HUMIDITY: SensorConfig(
                device_class=SensorDeviceClass.HUMIDITY,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=PERCENTAGE,
            ),
            FEATURE_CURRENT_CO2: SensorConfig(
                device_class=SensorDeviceClass.CO2,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=CONCENTRATION_PARTS_PER_MILLION,
            ),
            FEATURE_CURRENT_PM2: SensorConfig(
                device_class=SensorDeviceClass.PM25,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
                # TODO: migrate before HA 2027.8 removes the legacy constant.
                # unit_of_measurement=UnitOfDensity.MICROGRAMS_PER_CUBIC_METER,
            ),
            PD_TVOC: SensorConfig(),
            FEATURE_EXPENDABLES_FILTER: SensorConfig(
                unit_of_measurement=PERCENTAGE, value_fn=lambda v: v[0] if v else None
            ),
        },
        switches=[FEATURE_CHILD_LOCK],
    ),
    VentilationControlProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=124,
        program_data_fields={
            PD_LAST_PROGRAM: ProgramDataField(
                mode=0, offset=0, size=1, min_value=0, max_value=4, step=1
            ),
            PD_OUTDOOR_AIR_TEMPERATURE: ProgramDataField(
                mode=1, offset=0, size=1, min_value=0, max_value=255, step=1
            ),
            PD_FILTER_TRACKING: ProgramDataField(
                mode=2, offset=0, size=1, min_value=0, max_value=1, step=1
            ),
            PD_VALVE_CLOSING_TEMPERATURE: ProgramDataField(
                mode=3, offset=0, size=1, min_value=0, max_value=90, step=1
            ),
            PD_AUTO_VALVE_POSITION: ProgramDataField(
                mode=4, offset=0, size=1, min_value=0, max_value=3, step=1
            ),
            PD_AUTO_TEMPERATURE: ProgramDataField(
                mode=4, offset=1, size=1, min_value=18, max_value=28, step=1
            ),
            PD_HYSTERESIS: ProgramDataField(
                mode=4, offset=2, size=1, min_value=1, max_value=5, step=1
            ),
            PD_INTERVAL_VALVE_POSITION: ProgramDataField(
                mode=5, offset=0, size=1, min_value=0, max_value=3, step=1
            ),
            PD_VENTILATION_INTERVAL: ProgramDataField(
                mode=5, offset=1, size=4, min_value=900, max_value=86400, step=60
            ),
            PD_VENTILATION_DURATION: ProgramDataField(
                mode=5, offset=5, size=4, min_value=900, max_value=10800, step=60
            ),
            PD_VALVE_IS_CLOSING: ProgramDataField(
                mode=6, offset=0, size=1, min_value=0, max_value=1, step=1
            ),
        },
        numbers=[
            PD_AUTO_TEMPERATURE,
            PD_HYSTERESIS,
            PD_VENTILATION_INTERVAL,
            PD_VENTILATION_DURATION,
        ],
        selects={
            FEATURE_OPERATING_MODE: SelectConfig(
                options_map={
                    "off": 0,
                    "manual": 1,
                    "auto": 2,
                    "night": 3,
                    "interval_ventilation": 4,
                }
            ),
            FEATURE_VALVE_POSITION: SelectConfig(
                options_map={"auto": 0, "25%": 1, "50%": 2, "75%": 3, "100%": 4}
            ),
            PD_AUTO_VALVE_POSITION: SelectConfig(
                options_map={"25%": 0, "50%": 1, "75%": 2, "100%": 3}
            ),
            PD_INTERVAL_VALVE_POSITION: SelectConfig(
                options_map={"25%": 0, "50%": 1, "75%": 2, "100%": 3}
            ),
        },
        sensors={
            FEATURE_CURRENT_TEMPERATURE: SensorConfig(
                device_class=SensorDeviceClass.TEMPERATURE,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTemperature.CELSIUS,
            ),
            FEATURE_EXPENDABLES_FILTER: SensorConfig(
                required_program_data_field=PD_FILTER_TRACKING,
                unit_of_measurement=PERCENTAGE,
                value_fn=lambda v: v[1] if len(v) > 1 else None,
            ),
            FEATURE_EXPENDABLES_PREFILTER: SensorConfig(
                unit_of_measurement=PERCENTAGE, value_fn=lambda v: v[0] if v else None
            ),
        },
        switches=[FEATURE_VOLUME, FEATURE_AUTO_OFF_BACKLIGHT],
    ),
]
