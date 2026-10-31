"""Draft Rusclimate air-cleaner profiles based on Hommyn JSON.

Application command handling, firmware behavior and special speed reports still
need verification. Pending controls are listed in the shared research notes.
"""

from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import (
    CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    PERCENTAGE,
    EntityCategory,
    # UnitOfDensity,  # Not available in the minimum supported HA 2026.5.0.
)
from pysyncleo.commands import CmdProgramData

from ..const import (
    FEATURE_BACKLIGHT,
    FEATURE_CHILD_LOCK,
    FEATURE_CURRENT_PM2,
    FEATURE_ERROR,
    FEATURE_EXPENDABLES_FILTER,
    FEATURE_IONIZATION,
    FEATURE_RESET_FILTER,
    FEATURE_ULTRAVIOLET,
    PD_BACKLIGHT_MODE,
    PD_FILTER_RESET,
    PD_LAST_PROGRAM,
    PD_LIGHT_TIME,
    PRESET_AUTO,
    PRESET_MANUAL,
    PRESET_NIGHT,
    VENDOR_RUSCLIMATE,
)
from .profiles import AirCleanerProfile, ButtonConfig, ProgramDataField, SensorConfig

PROFILES = [
    AirCleanerProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=1,
        speed_count=3,
        preset_modes_map={
            PRESET_AUTO: 1,
            PRESET_NIGHT: 2,
            PRESET_MANUAL: 3,
        },
        default_preset_mode=PRESET_AUTO,
        program_data_fields={
            PD_LAST_PROGRAM: ProgramDataField(mode=0, min_value=1, max_value=3),
        },
        binary_sensors=[FEATURE_ERROR],
        sensors={
            FEATURE_CURRENT_PM2: SensorConfig(
                device_class=SensorDeviceClass.PM25,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
                # TODO: migrate before HA 2027.8 removes the legacy constant.
                # unit_of_measurement=UnitOfDensity.MICROGRAMS_PER_CUBIC_METER,
            ),
            FEATURE_EXPENDABLES_FILTER: SensorConfig(
                # JSON specifies 4320; unit and direction need verification.
                state_class=SensorStateClass.MEASUREMENT,
                value_fn=lambda value: (
                    value[0] if isinstance(value, list) and value else None
                ),
            ),
        },
        switches=[
            FEATURE_BACKLIGHT,
            FEATURE_ULTRAVIOLET,
            FEATURE_IONIZATION,
            FEATURE_CHILD_LOCK,
        ],
    ),
    AirCleanerProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=26,
        speed_count=4,
        preset_modes_map={
            PRESET_AUTO: 1,
            PRESET_NIGHT: 2,
            PRESET_MANUAL: 3,
        },
        default_preset_mode=PRESET_AUTO,
        program_data_fields={
            PD_LAST_PROGRAM: ProgramDataField(mode=0, min_value=1, max_value=3),
            PD_BACKLIGHT_MODE: ProgramDataField(mode=0, offset=1, max_value=4),
        },
        binary_sensors=[FEATURE_ERROR],
        sensors={
            FEATURE_CURRENT_PM2: SensorConfig(
                device_class=SensorDeviceClass.PM25,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
                # TODO: migrate before HA 2027.8 removes the legacy constant.
                # unit_of_measurement=UnitOfDensity.MICROGRAMS_PER_CUBIC_METER,
            ),
            FEATURE_EXPENDABLES_FILTER: SensorConfig(
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=PERCENTAGE,
                value_fn=lambda value: (
                    value[0] if isinstance(value, list) and value else None
                ),
            ),
        },
        switches=[
            FEATURE_BACKLIGHT,
            FEATURE_ULTRAVIOLET,
            FEATURE_IONIZATION,
            FEATURE_CHILD_LOCK,
        ],
    ),
    AirCleanerProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=117,
        speed_count=3,
        preset_modes_map={
            PRESET_AUTO: 1,
            PRESET_NIGHT: 2,
            PRESET_MANUAL: 3,
        },
        default_preset_mode=PRESET_AUTO,
        program_data_fields={
            PD_LAST_PROGRAM: ProgramDataField(mode=0, min_value=1, max_value=3),
            PD_FILTER_RESET: ProgramDataField(mode=1),
        },
        buttons={
            FEATURE_RESET_FILTER: ButtonConfig(
                command_factory=lambda: CmdProgramData(mode=1, data=b"\x01"),
                entity_category=EntityCategory.CONFIG,
            ),
        },
        binary_sensors=[FEATURE_ERROR],
        sensors={
            FEATURE_CURRENT_PM2: SensorConfig(
                device_class=SensorDeviceClass.PM25,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
                # TODO: migrate before HA 2027.8 removes the legacy constant.
                # unit_of_measurement=UnitOfDensity.MICROGRAMS_PER_CUBIC_METER,
            ),
            FEATURE_EXPENDABLES_FILTER: SensorConfig(
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=PERCENTAGE,
                value_fn=lambda value: (
                    value[0] if isinstance(value, list) and value else None
                ),
            ),
        },
        # Its child lock uses placeholder_feature_1, not the usual CHILD_LOCK.
        switches=[FEATURE_BACKLIGHT, FEATURE_ULTRAVIOLET],
    ),
    AirCleanerProfile(
        vendor=VENDOR_RUSCLIMATE,
        device_type=122,
        speed_count=5,
        preset_modes_map={
            PRESET_AUTO: 1,
            PRESET_NIGHT: 2,
            PRESET_MANUAL: 3,
        },
        default_preset_mode=PRESET_AUTO,
        program_data_fields={
            PD_LAST_PROGRAM: ProgramDataField(mode=0, min_value=1, max_value=3),
            PD_FILTER_RESET: ProgramDataField(mode=1),
            PD_LIGHT_TIME: ProgramDataField(mode=2, max_value=3),
        },
        buttons={
            FEATURE_RESET_FILTER: ButtonConfig(
                command_factory=lambda: CmdProgramData(mode=1, data=b"\x01"),
                entity_category=EntityCategory.CONFIG,
            ),
        },
        binary_sensors=[FEATURE_ERROR],
        sensors={
            FEATURE_CURRENT_PM2: SensorConfig(
                device_class=SensorDeviceClass.PM25,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
                # TODO: migrate before HA 2027.8 removes the legacy constant.
                # unit_of_measurement=UnitOfDensity.MICROGRAMS_PER_CUBIC_METER,
            ),
            FEATURE_EXPENDABLES_FILTER: SensorConfig(
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=PERCENTAGE,
                value_fn=lambda value: (
                    value[0] if isinstance(value, list) and value else None
                ),
            ),
        },
        switches=[FEATURE_CHILD_LOCK],
    ),
]
