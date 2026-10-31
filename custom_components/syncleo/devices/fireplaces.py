"""Draft fireplace profiles based on individual Hommyn JSON layouts."""

from homeassistant.components.climate.const import ClimateEntityFeature, HVACMode
from homeassistant.components.sensor import SensorStateClass
from homeassistant.const import PERCENTAGE
from pysyncleo.commands import CmdPlaceholder1, CmdPlaceholder2, CmdPlaceholder6

from ..const import (
    FEATURE_BOTTOM_ILLUMINATION,
    FEATURE_DEVICE_POWER,
    FEATURE_FIREWOOD_BRIGHTNESS,
    FEATURE_FLAME,
    FEATURE_FLAME_BRIGHTNESS,
    FEATURE_FLAME_COLOR,
    FEATURE_ILLUMINATION_BRIGHTNESS,
    FEATURE_POWER_LEVEL,
    FEATURE_STEAM_LEVEL,
    FEATURE_TIMER,
    FEATURE_TOP_ILLUMINATION,
    FEATURE_VOLUME,
    FEATURE_WATER_LEVEL,
    PD_BUTTON_SOUND,
    PD_DISPLAY_TEMPERATURE_UNIT,
    PROFILE_TYPE_FIREPLACE,
    VENDOR_RUSCLIMATE,
)
from .profiles import (
    ButtonConfig,
    ClimateProfile,
    FireplaceProfile,
    NumberConfig,
    ProgramDataField,
    SelectConfig,
    SensorConfig,
)

PROFILES = [
    FireplaceProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=50,
        program_data_fields={
            PD_BUTTON_SOUND: ProgramDataField(mode=0),
        },
        numbers=[FEATURE_POWER_LEVEL, FEATURE_STEAM_LEVEL, FEATURE_VOLUME],
        number_configs={
            FEATURE_POWER_LEVEL: NumberConfig(min_value=0, max_value=2),
            FEATURE_STEAM_LEVEL: NumberConfig(min_value=1, max_value=3),
            FEATURE_VOLUME: NumberConfig(min_value=0, max_value=2),
        },
        selects={
            FEATURE_FIREWOOD_BRIGHTNESS: SelectConfig(options_map={"min": 0, "max": 1}),
        },
        sensors={
            FEATURE_WATER_LEVEL: SensorConfig(
                unit_of_measurement=PERCENTAGE,
                state_class=SensorStateClass.MEASUREMENT,
                value_fn=lambda value: {0: 0, 1: 15, 2: 30, 3: 50, 4: 70, 5: 100}.get(
                    value
                ),
            ),
        },
        switches=[FEATURE_DEVICE_POWER],
    ),
    ClimateProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=112,
        profile_type=PROFILE_TYPE_FIREPLACE,
        min_temp=14,
        max_temp=30,
        target_temp_step=2,
        supported_features=ClimateEntityFeature.TARGET_TEMPERATURE
        | ClimateEntityFeature.TURN_ON
        | ClimateEntityFeature.TURN_OFF,
        hvac_modes_map={HVACMode.OFF: 0, HVACMode.HEAT: 1},
        default_hvac_mode=HVACMode.HEAT,
        program_data_fields={
            PD_DISPLAY_TEMPERATURE_UNIT: ProgramDataField(mode=0),
        },
        numbers=[
            FEATURE_POWER_LEVEL,
            FEATURE_VOLUME,
            FEATURE_FLAME_BRIGHTNESS,
            FEATURE_TIMER,
        ],
        number_configs={
            FEATURE_POWER_LEVEL: NumberConfig(min_value=0, max_value=2),
            FEATURE_VOLUME: NumberConfig(min_value=0, max_value=5),
            FEATURE_FLAME_BRIGHTNESS: NumberConfig(min_value=0, max_value=5),
            FEATURE_TIMER: NumberConfig(min_value=0, max_value=28800, step=3600),
        },
        selects={
            PD_DISPLAY_TEMPERATURE_UNIT: SelectConfig(
                options_map={"celsius": 0, "fahrenheit": 1}
            ),
            FEATURE_BOTTOM_ILLUMINATION: SelectConfig(
                options_map={
                    "orange": 0,
                    "red": 1,
                    "yellow": 2,
                    "blue": 3,
                    "green": 4,
                    "purple": 5,
                    "pink": 6,
                    "auto_1": 7,
                    "auto_2": 8,
                    "auto_red": 9,
                    "auto_green": 10,
                    "auto_blue": 11,
                    "off": 12,
                }
            ),
            FEATURE_TOP_ILLUMINATION: SelectConfig(
                options_map={
                    "orange": 0,
                    "red": 1,
                    "yellow": 2,
                    "blue": 3,
                    "green": 4,
                    "purple": 5,
                    "pink": 6,
                    "auto_1": 7,
                    "auto_2": 8,
                    "auto_red": 9,
                    "auto_green": 10,
                    "auto_blue": 11,
                    "off": 12,
                }
            ),
        },
        buttons={
            FEATURE_FLAME: ButtonConfig(command_factory=lambda: CmdPlaceholder1(1)),
            FEATURE_FLAME_COLOR: ButtonConfig(
                command_factory=lambda: CmdPlaceholder2(1)
            ),
            FEATURE_ILLUMINATION_BRIGHTNESS: ButtonConfig(
                command_factory=lambda: CmdPlaceholder6(1)
            ),
        },
    ),
]
