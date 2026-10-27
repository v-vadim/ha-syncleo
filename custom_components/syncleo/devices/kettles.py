from homeassistant.components.water_heater import STATE_OFF

from ..const import (
    FEATURE_BACKLIGHT,
    FEATURE_CHILD_LOCK,
    FEATURE_ERROR,
    FEATURE_KETTLE_TEMPERATURE_PRESET,
    FEATURE_NIGHT,
    FEATURE_VOLUME,
    KETTLE_MODE_BOILING,
    KETTLE_MODE_BOILING_KEEP,
    KETTLE_MODE_IQ_BOILING,
    KETTLE_MODE_TEA_TIME,
    KETTLE_MODE_WARM_UP,
    KETTLE_MODE_WARM_UP_KEEP,
    KETTLE_PRESET_BABY_BOTTLE,
    KETTLE_PRESET_BLACK_TEA,
    KETTLE_PRESET_FLOWER_TEA,
    KETTLE_PRESET_GREEN_TEA,
    KETTLE_PRESET_HERBAL_TEA,
    KETTLE_PRESET_INSTANT_COFFEE,
    KETTLE_PRESET_NONE,
    KETTLE_PRESET_OOLONG_TEA,
    KETTLE_PRESET_PUER,
    KETTLE_PRESET_RED_TEA,
    KETTLE_PRESET_TEA_BAG,
    KETTLE_PRESET_WHITE_TEA,
    PD_BACKLIGHT_BLUE,
    PD_BACKLIGHT_GREEN,
    PD_BACKLIGHT_RED,
    VENDOR_POLARIS,
)
from .profiles import (
    KettleProfile,
    LightConfig,
    ProgramDataField,
    SelectConfig,
)


def _create_polaris_kettle(
    device_type: int,
    has_tea_time: bool = False,
    has_boiling_keep: bool = False,
    **kwargs,
) -> KettleProfile:
    modes = {
        STATE_OFF: 0,
        KETTLE_MODE_BOILING: 1,
        KETTLE_MODE_WARM_UP: 3,
        KETTLE_MODE_WARM_UP_KEEP: 4,
        KETTLE_MODE_IQ_BOILING: 5,
    }

    if has_boiling_keep:
        modes[KETTLE_MODE_BOILING_KEEP] = 2
    if has_tea_time:
        modes[KETTLE_MODE_TEA_TIME] = 6

    minimum = kwargs.get("min_temp", 30)
    temperature_modes = {
        mode: (100, 100) if value in (1, 5) else (minimum, 95)
        for mode, value in modes.items()
        if value != 0
    }
    params = {
        "vendor": VENDOR_POLARIS,
        "device_type": device_type,
        "default_operation_mode": KETTLE_MODE_BOILING,
        "operation_modes_map": modes,
        "temperature_modes_map": temperature_modes,
        "binary_sensors": [FEATURE_ERROR],
        "switches": [FEATURE_CHILD_LOCK],
        "selects": {
            FEATURE_KETTLE_TEMPERATURE_PRESET: SelectConfig(
                options_map={
                    KETTLE_PRESET_NONE: 0,
                    KETTLE_PRESET_BLACK_TEA: 100,
                    KETTLE_PRESET_BABY_BOTTLE: 40,
                    KETTLE_PRESET_INSTANT_COFFEE: 95,
                    KETTLE_PRESET_GREEN_TEA: 80,
                    KETTLE_PRESET_FLOWER_TEA: 80,
                    KETTLE_PRESET_TEA_BAG: 100,
                    KETTLE_PRESET_RED_TEA: 90,
                    KETTLE_PRESET_PUER: 95,
                    KETTLE_PRESET_OOLONG_TEA: 90,
                    KETTLE_PRESET_WHITE_TEA: 65,
                    KETTLE_PRESET_HERBAL_TEA: 90,
                }
            )
        },
    } | kwargs

    # Recipes must fit this type's selectable temperatures (notably type 245).
    preset = params["selects"][FEATURE_KETTLE_TEMPERATURE_PRESET]
    preset.options_map = {
        name: value
        for name, value in preset.options_map.items()
        if value == 0
        or value == 100
        or (
            minimum <= value <= params["temperature_modes_map"][KETTLE_MODE_WARM_UP][1]
            and (value - minimum) % params.get("target_temp_step", 5) == 0
        )
    }
    return KettleProfile(**params)


PROFILES = [
    _create_polaris_kettle(
        device_type=2,
        has_tea_time=True,
    ),
    _create_polaris_kettle(
        device_type=6,
    ),
    _create_polaris_kettle(
        device_type=8,
        has_tea_time=True,
        min_temp=40,
    ),
    _create_polaris_kettle(
        device_type=29,
    ),
    _create_polaris_kettle(
        device_type=35,
        has_tea_time=True,
        switches=[FEATURE_BACKLIGHT, FEATURE_CHILD_LOCK, FEATURE_VOLUME],
    ),
    _create_polaris_kettle(
        device_type=38,
        switches=[FEATURE_CHILD_LOCK, FEATURE_VOLUME],
    ),
    _create_polaris_kettle(
        device_type=51,
        has_tea_time=True,
        switches=[FEATURE_BACKLIGHT, FEATURE_CHILD_LOCK, FEATURE_VOLUME],
    ),
    _create_polaris_kettle(
        device_type=52,
        switches=[FEATURE_BACKLIGHT, FEATURE_CHILD_LOCK, FEATURE_VOLUME],
    ),
    _create_polaris_kettle(
        device_type=53,
        has_tea_time=True,
        switches=[FEATURE_BACKLIGHT, FEATURE_CHILD_LOCK, FEATURE_VOLUME],
    ),
    _create_polaris_kettle(
        device_type=54,
        switches=[FEATURE_BACKLIGHT, FEATURE_CHILD_LOCK, FEATURE_VOLUME],
    ),
    _create_polaris_kettle(
        device_type=56,
        has_tea_time=True,
        switches=[FEATURE_CHILD_LOCK, FEATURE_VOLUME],
    ),
    _create_polaris_kettle(
        device_type=57,
        switches=[FEATURE_CHILD_LOCK, FEATURE_VOLUME],
    ),
    _create_polaris_kettle(
        device_type=58,
        has_tea_time=True,
        switches=[FEATURE_CHILD_LOCK, FEATURE_VOLUME],
        min_temp=40,
    ),
    _create_polaris_kettle(
        device_type=59,
        switches=[FEATURE_CHILD_LOCK, FEATURE_VOLUME],
    ),
    _create_polaris_kettle(
        device_type=60,
        has_tea_time=True,
        switches=[FEATURE_BACKLIGHT, FEATURE_CHILD_LOCK, FEATURE_VOLUME],
    ),
    _create_polaris_kettle(
        device_type=61,
        switches=[FEATURE_BACKLIGHT, FEATURE_CHILD_LOCK, FEATURE_VOLUME],
    ),
    _create_polaris_kettle(
        device_type=62,
        has_tea_time=True,
        switches=[FEATURE_BACKLIGHT, FEATURE_CHILD_LOCK, FEATURE_VOLUME],
    ),
    _create_polaris_kettle(
        device_type=63,
        switches=[FEATURE_BACKLIGHT, FEATURE_CHILD_LOCK, FEATURE_VOLUME],
    ),
    _create_polaris_kettle(
        device_type=67,
        switches=[FEATURE_BACKLIGHT, FEATURE_CHILD_LOCK, FEATURE_VOLUME],
    ),
    _create_polaris_kettle(
        device_type=82,
        switches=[FEATURE_CHILD_LOCK, FEATURE_VOLUME],
        program_data_fields={
            PD_BACKLIGHT_RED: ProgramDataField(mode=0, max_value=255),
            PD_BACKLIGHT_GREEN: ProgramDataField(mode=0, offset=1, max_value=255),
            PD_BACKLIGHT_BLUE: ProgramDataField(mode=0, offset=2, max_value=255),
        },
        lights={
            FEATURE_BACKLIGHT: LightConfig(
                red_key=PD_BACKLIGHT_RED,
                green_key=PD_BACKLIGHT_GREEN,
                blue_key=PD_BACKLIGHT_BLUE,
                rgb_brightness=True,
            )
        },
    ),
    _create_polaris_kettle(
        device_type=83,
        switches=[FEATURE_CHILD_LOCK, FEATURE_VOLUME],
        program_data_fields={
            PD_BACKLIGHT_RED: ProgramDataField(mode=0, max_value=255),
            PD_BACKLIGHT_GREEN: ProgramDataField(mode=0, offset=1, max_value=255),
            PD_BACKLIGHT_BLUE: ProgramDataField(mode=0, offset=2, max_value=255),
        },
        lights={
            FEATURE_BACKLIGHT: LightConfig(
                red_key=PD_BACKLIGHT_RED,
                green_key=PD_BACKLIGHT_GREEN,
                blue_key=PD_BACKLIGHT_BLUE,
                rgb_brightness=True,
            )
        },
    ),
    _create_polaris_kettle(
        device_type=84,
        switches=[FEATURE_CHILD_LOCK, FEATURE_VOLUME],
        program_data_fields={
            PD_BACKLIGHT_RED: ProgramDataField(mode=0, max_value=255),
            PD_BACKLIGHT_GREEN: ProgramDataField(mode=0, offset=1, max_value=255),
            PD_BACKLIGHT_BLUE: ProgramDataField(mode=0, offset=2, max_value=255),
        },
        lights={
            FEATURE_BACKLIGHT: LightConfig(
                red_key=PD_BACKLIGHT_RED,
                green_key=PD_BACKLIGHT_GREEN,
                blue_key=PD_BACKLIGHT_BLUE,
                rgb_brightness=True,
            )
        },
    ),
    _create_polaris_kettle(
        device_type=86,
        switches=[FEATURE_BACKLIGHT, FEATURE_CHILD_LOCK, FEATURE_VOLUME],
        program_data_fields={
            PD_BACKLIGHT_RED: ProgramDataField(mode=0, max_value=255),
            PD_BACKLIGHT_GREEN: ProgramDataField(mode=0, offset=1, max_value=255),
            PD_BACKLIGHT_BLUE: ProgramDataField(mode=0, offset=2, max_value=255),
        },
        lights={
            FEATURE_NIGHT: LightConfig(
                red_key=PD_BACKLIGHT_RED,
                green_key=PD_BACKLIGHT_GREEN,
                blue_key=PD_BACKLIGHT_BLUE,
                rgb_brightness=True,
            )
        },
    ),
    _create_polaris_kettle(
        device_type=97,
        switches=[FEATURE_BACKLIGHT, FEATURE_CHILD_LOCK, FEATURE_VOLUME],
        program_data_fields={
            PD_BACKLIGHT_RED: ProgramDataField(mode=0, max_value=255),
            PD_BACKLIGHT_GREEN: ProgramDataField(mode=0, offset=1, max_value=255),
            PD_BACKLIGHT_BLUE: ProgramDataField(mode=0, offset=2, max_value=255),
        },
        lights={
            FEATURE_NIGHT: LightConfig(
                red_key=PD_BACKLIGHT_RED,
                green_key=PD_BACKLIGHT_GREEN,
                blue_key=PD_BACKLIGHT_BLUE,
                rgb_brightness=True,
            )
        },
    ),
    _create_polaris_kettle(
        device_type=98,
        has_tea_time=True,
        switches=[FEATURE_BACKLIGHT, FEATURE_CHILD_LOCK, FEATURE_VOLUME],
    ),
    _create_polaris_kettle(
        device_type=105,
        switches=[FEATURE_BACKLIGHT, FEATURE_CHILD_LOCK, FEATURE_VOLUME],
    ),
    _create_polaris_kettle(
        device_type=106,
        has_tea_time=True,
        switches=[FEATURE_BACKLIGHT, FEATURE_CHILD_LOCK, FEATURE_VOLUME],
        program_data_fields={
            PD_BACKLIGHT_RED: ProgramDataField(mode=0, max_value=255),
            PD_BACKLIGHT_GREEN: ProgramDataField(mode=0, offset=1, max_value=255),
            PD_BACKLIGHT_BLUE: ProgramDataField(mode=0, offset=2, max_value=255),
        },
        lights={
            FEATURE_NIGHT: LightConfig(
                red_key=PD_BACKLIGHT_RED,
                green_key=PD_BACKLIGHT_GREEN,
                blue_key=PD_BACKLIGHT_BLUE,
                rgb_brightness=True,
            )
        },
    ),
    _create_polaris_kettle(
        device_type=117,
        switches=[FEATURE_BACKLIGHT, FEATURE_CHILD_LOCK, FEATURE_VOLUME],
        program_data_fields={
            PD_BACKLIGHT_RED: ProgramDataField(mode=0, max_value=255),
            PD_BACKLIGHT_GREEN: ProgramDataField(mode=0, offset=1, max_value=255),
            PD_BACKLIGHT_BLUE: ProgramDataField(mode=0, offset=2, max_value=255),
        },
        lights={
            FEATURE_NIGHT: LightConfig(
                red_key=PD_BACKLIGHT_RED,
                green_key=PD_BACKLIGHT_GREEN,
                blue_key=PD_BACKLIGHT_BLUE,
                rgb_brightness=True,
            )
        },
    ),
    _create_polaris_kettle(
        device_type=121,
        switches=[FEATURE_CHILD_LOCK, FEATURE_VOLUME],
    ),
    _create_polaris_kettle(
        device_type=165,
        has_tea_time=True,
        has_boiling_keep=True,
        switches=[FEATURE_CHILD_LOCK, FEATURE_VOLUME],
    ),
    _create_polaris_kettle(
        device_type=175,
        switches=[FEATURE_BACKLIGHT, FEATURE_CHILD_LOCK, FEATURE_VOLUME],
        program_data_fields={
            PD_BACKLIGHT_RED: ProgramDataField(mode=0, max_value=255),
            PD_BACKLIGHT_GREEN: ProgramDataField(mode=0, offset=1, max_value=255),
            PD_BACKLIGHT_BLUE: ProgramDataField(mode=0, offset=2, max_value=255),
        },
        lights={
            FEATURE_NIGHT: LightConfig(
                red_key=PD_BACKLIGHT_RED,
                green_key=PD_BACKLIGHT_GREEN,
                blue_key=PD_BACKLIGHT_BLUE,
                rgb_brightness=True,
            )
        },
    ),
    _create_polaris_kettle(
        device_type=176,
        switches=[FEATURE_BACKLIGHT, FEATURE_CHILD_LOCK, FEATURE_VOLUME],
        program_data_fields={
            PD_BACKLIGHT_RED: ProgramDataField(mode=0, max_value=255),
            PD_BACKLIGHT_GREEN: ProgramDataField(mode=0, offset=1, max_value=255),
            PD_BACKLIGHT_BLUE: ProgramDataField(mode=0, offset=2, max_value=255),
        },
        lights={
            FEATURE_NIGHT: LightConfig(
                red_key=PD_BACKLIGHT_RED,
                green_key=PD_BACKLIGHT_GREEN,
                blue_key=PD_BACKLIGHT_BLUE,
                rgb_brightness=True,
            )
        },
    ),
    _create_polaris_kettle(
        device_type=177,
        has_tea_time=True,
        has_boiling_keep=True,
        switches=[FEATURE_BACKLIGHT, FEATURE_CHILD_LOCK, FEATURE_VOLUME],
        program_data_fields={
            PD_BACKLIGHT_RED: ProgramDataField(mode=0, max_value=255),
            PD_BACKLIGHT_GREEN: ProgramDataField(mode=0, offset=1, max_value=255),
            PD_BACKLIGHT_BLUE: ProgramDataField(mode=0, offset=2, max_value=255),
        },
        lights={
            FEATURE_NIGHT: LightConfig(
                red_key=PD_BACKLIGHT_RED,
                green_key=PD_BACKLIGHT_GREEN,
                blue_key=PD_BACKLIGHT_BLUE,
                rgb_brightness=True,
            )
        },
    ),
    _create_polaris_kettle(
        device_type=185,
        has_tea_time=True,
        has_boiling_keep=True,
        switches=[FEATURE_CHILD_LOCK, FEATURE_VOLUME],
    ),
    _create_polaris_kettle(
        device_type=188,
        has_tea_time=True,
        switches=[FEATURE_BACKLIGHT, FEATURE_CHILD_LOCK, FEATURE_VOLUME],
    ),
    _create_polaris_kettle(
        device_type=189,
        switches=[FEATURE_BACKLIGHT, FEATURE_CHILD_LOCK, FEATURE_VOLUME],
        program_data_fields={
            PD_BACKLIGHT_RED: ProgramDataField(mode=0, max_value=255),
            PD_BACKLIGHT_GREEN: ProgramDataField(mode=0, offset=1, max_value=255),
            PD_BACKLIGHT_BLUE: ProgramDataField(mode=0, offset=2, max_value=255),
        },
        lights={
            FEATURE_NIGHT: LightConfig(
                red_key=PD_BACKLIGHT_RED,
                green_key=PD_BACKLIGHT_GREEN,
                blue_key=PD_BACKLIGHT_BLUE,
                rgb_brightness=True,
            )
        },
    ),
    _create_polaris_kettle(
        device_type=194,
        switches=[FEATURE_BACKLIGHT, FEATURE_CHILD_LOCK, FEATURE_VOLUME],
        program_data_fields={
            PD_BACKLIGHT_RED: ProgramDataField(mode=0, max_value=255),
            PD_BACKLIGHT_GREEN: ProgramDataField(mode=0, offset=1, max_value=255),
            PD_BACKLIGHT_BLUE: ProgramDataField(mode=0, offset=2, max_value=255),
        },
        lights={
            FEATURE_NIGHT: LightConfig(
                red_key=PD_BACKLIGHT_RED,
                green_key=PD_BACKLIGHT_GREEN,
                blue_key=PD_BACKLIGHT_BLUE,
                rgb_brightness=True,
            )
        },
    ),
    _create_polaris_kettle(
        device_type=196,
        switches=[FEATURE_BACKLIGHT, FEATURE_CHILD_LOCK, FEATURE_VOLUME],
        program_data_fields={
            PD_BACKLIGHT_RED: ProgramDataField(mode=0, max_value=255),
            PD_BACKLIGHT_GREEN: ProgramDataField(mode=0, offset=1, max_value=255),
            PD_BACKLIGHT_BLUE: ProgramDataField(mode=0, offset=2, max_value=255),
        },
        lights={
            FEATURE_NIGHT: LightConfig(
                red_key=PD_BACKLIGHT_RED,
                green_key=PD_BACKLIGHT_GREEN,
                blue_key=PD_BACKLIGHT_BLUE,
                rgb_brightness=True,
            )
        },
    ),
    _create_polaris_kettle(
        device_type=205,
        has_boiling_keep=True,
        operation_modes_map={
            STATE_OFF: 0,
            KETTLE_MODE_BOILING: 1,
            KETTLE_MODE_BOILING_KEEP: 2,
            KETTLE_MODE_WARM_UP: 3,
            KETTLE_MODE_WARM_UP_KEEP: 4,
        },
        switches=[FEATURE_CHILD_LOCK, FEATURE_VOLUME],
        program_data_fields={
            PD_BACKLIGHT_RED: ProgramDataField(mode=0, max_value=255),
            PD_BACKLIGHT_GREEN: ProgramDataField(mode=0, offset=1, max_value=255),
            PD_BACKLIGHT_BLUE: ProgramDataField(mode=0, offset=2, max_value=255),
        },
        lights={
            FEATURE_NIGHT: LightConfig(
                red_key=PD_BACKLIGHT_RED,
                green_key=PD_BACKLIGHT_GREEN,
                blue_key=PD_BACKLIGHT_BLUE,
                rgb_brightness=True,
            )
        },
    ),
    _create_polaris_kettle(
        device_type=208,
        has_tea_time=True,
        has_boiling_keep=True,
        switches=[FEATURE_BACKLIGHT, FEATURE_CHILD_LOCK, FEATURE_VOLUME],
        program_data_fields={
            PD_BACKLIGHT_RED: ProgramDataField(mode=0, max_value=255),
            PD_BACKLIGHT_GREEN: ProgramDataField(mode=0, offset=1, max_value=255),
            PD_BACKLIGHT_BLUE: ProgramDataField(mode=0, offset=2, max_value=255),
        },
        lights={
            FEATURE_NIGHT: LightConfig(
                red_key=PD_BACKLIGHT_RED,
                green_key=PD_BACKLIGHT_GREEN,
                blue_key=PD_BACKLIGHT_BLUE,
                rgb_brightness=True,
            )
        },
    ),
    _create_polaris_kettle(
        device_type=223,
        has_tea_time=True,
        switches=[FEATURE_BACKLIGHT, FEATURE_CHILD_LOCK, FEATURE_VOLUME],
    ),
    _create_polaris_kettle(
        device_type=244,
        has_boiling_keep=True,
        switches=[FEATURE_BACKLIGHT, FEATURE_CHILD_LOCK, FEATURE_VOLUME],
        program_data_fields={
            PD_BACKLIGHT_RED: ProgramDataField(mode=0, max_value=255),
            PD_BACKLIGHT_GREEN: ProgramDataField(mode=0, offset=1, max_value=255),
            PD_BACKLIGHT_BLUE: ProgramDataField(mode=0, offset=2, max_value=255),
        },
        lights={
            FEATURE_NIGHT: LightConfig(
                red_key=PD_BACKLIGHT_RED,
                green_key=PD_BACKLIGHT_GREEN,
                blue_key=PD_BACKLIGHT_BLUE,
                rgb_brightness=True,
            )
        },
        min_temp=40,
    ),
    _create_polaris_kettle(
        device_type=253,
        has_boiling_keep=True,
        switches=[FEATURE_BACKLIGHT, FEATURE_CHILD_LOCK, FEATURE_VOLUME],
        program_data_fields={
            PD_BACKLIGHT_RED: ProgramDataField(mode=0, max_value=255),
            PD_BACKLIGHT_GREEN: ProgramDataField(mode=0, offset=1, max_value=255),
            PD_BACKLIGHT_BLUE: ProgramDataField(mode=0, offset=2, max_value=255),
        },
        lights={
            FEATURE_NIGHT: LightConfig(
                red_key=PD_BACKLIGHT_RED,
                green_key=PD_BACKLIGHT_GREEN,
                blue_key=PD_BACKLIGHT_BLUE,
                rgb_brightness=True,
            )
        },
    ),
    _create_polaris_kettle(
        device_type=254,
        switches=[FEATURE_BACKLIGHT, FEATURE_CHILD_LOCK, FEATURE_VOLUME],
        program_data_fields={
            PD_BACKLIGHT_RED: ProgramDataField(mode=0, max_value=255),
            PD_BACKLIGHT_GREEN: ProgramDataField(mode=0, offset=1, max_value=255),
            PD_BACKLIGHT_BLUE: ProgramDataField(mode=0, offset=2, max_value=255),
        },
        lights={
            FEATURE_NIGHT: LightConfig(
                red_key=PD_BACKLIGHT_RED,
                green_key=PD_BACKLIGHT_GREEN,
                blue_key=PD_BACKLIGHT_BLUE,
                rgb_brightness=True,
            )
        },
        has_boiling_keep=True,
    ),
    _create_polaris_kettle(
        device_type=255,
        switches=[FEATURE_BACKLIGHT, FEATURE_CHILD_LOCK, FEATURE_VOLUME],
        program_data_fields={
            PD_BACKLIGHT_RED: ProgramDataField(mode=0, max_value=255),
            PD_BACKLIGHT_GREEN: ProgramDataField(mode=0, offset=1, max_value=255),
            PD_BACKLIGHT_BLUE: ProgramDataField(mode=0, offset=2, max_value=255),
        },
        lights={
            FEATURE_NIGHT: LightConfig(
                red_key=PD_BACKLIGHT_RED,
                green_key=PD_BACKLIGHT_GREEN,
                blue_key=PD_BACKLIGHT_BLUE,
                rgb_brightness=True,
            )
        },
        has_boiling_keep=True,
    ),
    _create_polaris_kettle(
        device_type=260,
        switches=[FEATURE_BACKLIGHT, FEATURE_CHILD_LOCK, FEATURE_VOLUME],
        program_data_fields={
            PD_BACKLIGHT_RED: ProgramDataField(mode=0, max_value=255),
            PD_BACKLIGHT_GREEN: ProgramDataField(mode=0, offset=1, max_value=255),
            PD_BACKLIGHT_BLUE: ProgramDataField(mode=0, offset=2, max_value=255),
        },
        lights={
            FEATURE_NIGHT: LightConfig(
                red_key=PD_BACKLIGHT_RED,
                green_key=PD_BACKLIGHT_GREEN,
                blue_key=PD_BACKLIGHT_BLUE,
                rgb_brightness=True,
            )
        },
        has_boiling_keep=True,
    ),
    _create_polaris_kettle(
        device_type=262,
        has_tea_time=True,
        switches=[FEATURE_BACKLIGHT, FEATURE_CHILD_LOCK, FEATURE_VOLUME],
    ),
    _create_polaris_kettle(
        device_type=263,
        has_tea_time=True,
        switches=[FEATURE_BACKLIGHT, FEATURE_CHILD_LOCK, FEATURE_VOLUME],
        has_boiling_keep=True,
    ),
    _create_polaris_kettle(
        device_type=271,
        has_boiling_keep=True,
        switches=[FEATURE_BACKLIGHT, FEATURE_CHILD_LOCK, FEATURE_VOLUME],
        program_data_fields={
            PD_BACKLIGHT_RED: ProgramDataField(mode=0, max_value=255),
            PD_BACKLIGHT_GREEN: ProgramDataField(mode=0, offset=1, max_value=255),
            PD_BACKLIGHT_BLUE: ProgramDataField(mode=0, offset=2, max_value=255),
        },
        lights={
            FEATURE_NIGHT: LightConfig(
                red_key=PD_BACKLIGHT_RED,
                green_key=PD_BACKLIGHT_GREEN,
                blue_key=PD_BACKLIGHT_BLUE,
                rgb_brightness=True,
            )
        },
    ),
    _create_polaris_kettle(
        device_type=275,
        has_tea_time=True,
        switches=[FEATURE_BACKLIGHT, FEATURE_CHILD_LOCK, FEATURE_VOLUME],
        has_boiling_keep=True,
    ),
    _create_polaris_kettle(
        device_type=294,
        has_tea_time=True,
        switches=[FEATURE_BACKLIGHT, FEATURE_CHILD_LOCK, FEATURE_VOLUME],
        has_boiling_keep=True,
    ),
    _create_polaris_kettle(
        device_type=308,
        switches=[FEATURE_BACKLIGHT, FEATURE_CHILD_LOCK, FEATURE_VOLUME],
        program_data_fields={
            PD_BACKLIGHT_RED: ProgramDataField(mode=0, max_value=255),
            PD_BACKLIGHT_GREEN: ProgramDataField(mode=0, offset=1, max_value=255),
            PD_BACKLIGHT_BLUE: ProgramDataField(mode=0, offset=2, max_value=255),
        },
        lights={
            FEATURE_NIGHT: LightConfig(
                red_key=PD_BACKLIGHT_RED,
                green_key=PD_BACKLIGHT_GREEN,
                blue_key=PD_BACKLIGHT_BLUE,
                rgb_brightness=True,
            )
        },
        has_boiling_keep=True,
    ),
    _create_polaris_kettle(
        device_type=36,
        switches=[FEATURE_BACKLIGHT, FEATURE_CHILD_LOCK, FEATURE_VOLUME],
        program_data_fields={
            PD_BACKLIGHT_RED: ProgramDataField(mode=0, max_value=255),
            PD_BACKLIGHT_GREEN: ProgramDataField(mode=0, offset=1, max_value=255),
            PD_BACKLIGHT_BLUE: ProgramDataField(mode=0, offset=2, max_value=255),
        },
        lights={
            FEATURE_NIGHT: LightConfig(
                red_key=PD_BACKLIGHT_RED,
                green_key=PD_BACKLIGHT_GREEN,
                blue_key=PD_BACKLIGHT_BLUE,
                rgb_brightness=True,
            )
        },
    ),
    _create_polaris_kettle(
        device_type=37,
        switches=[FEATURE_BACKLIGHT, FEATURE_CHILD_LOCK, FEATURE_VOLUME],
        program_data_fields={
            PD_BACKLIGHT_RED: ProgramDataField(mode=0, max_value=255),
            PD_BACKLIGHT_GREEN: ProgramDataField(mode=0, offset=1, max_value=255),
            PD_BACKLIGHT_BLUE: ProgramDataField(mode=0, offset=2, max_value=255),
        },
        lights={
            FEATURE_NIGHT: LightConfig(
                red_key=PD_BACKLIGHT_RED,
                green_key=PD_BACKLIGHT_GREEN,
                blue_key=PD_BACKLIGHT_BLUE,
                rgb_brightness=True,
            )
        },
    ),
    _create_polaris_kettle(
        device_type=85,
        has_tea_time=True,
        switches=[FEATURE_BACKLIGHT, FEATURE_CHILD_LOCK, FEATURE_VOLUME],
    ),
    _create_polaris_kettle(
        device_type=139,
        has_tea_time=True,
        switches=[FEATURE_BACKLIGHT, FEATURE_CHILD_LOCK, FEATURE_VOLUME],
    ),
    _create_polaris_kettle(
        device_type=164,
        has_tea_time=True,
        switches=[FEATURE_BACKLIGHT, FEATURE_CHILD_LOCK, FEATURE_VOLUME],
        temperature_modes_map={
            KETTLE_MODE_BOILING: (100, 100),
            KETTLE_MODE_WARM_UP: (30, 95),
            KETTLE_MODE_WARM_UP_KEEP: (30, 100),
            KETTLE_MODE_IQ_BOILING: (100, 100),
            KETTLE_MODE_TEA_TIME: (30, 95),
        },
        program_data_fields={
            PD_BACKLIGHT_RED: ProgramDataField(mode=0, max_value=255),
            PD_BACKLIGHT_GREEN: ProgramDataField(mode=0, offset=1, max_value=255),
            PD_BACKLIGHT_BLUE: ProgramDataField(mode=0, offset=2, max_value=255),
        },
        lights={
            FEATURE_NIGHT: LightConfig(
                red_key=PD_BACKLIGHT_RED,
                green_key=PD_BACKLIGHT_GREEN,
                blue_key=PD_BACKLIGHT_BLUE,
                rgb_brightness=True,
            )
        },
    ),
    _create_polaris_kettle(
        device_type=209,
        switches=[FEATURE_BACKLIGHT, FEATURE_CHILD_LOCK, FEATURE_VOLUME],
        program_data_fields={
            PD_BACKLIGHT_RED: ProgramDataField(mode=0, max_value=255),
            PD_BACKLIGHT_GREEN: ProgramDataField(mode=0, offset=1, max_value=255),
            PD_BACKLIGHT_BLUE: ProgramDataField(mode=0, offset=2, max_value=255),
        },
        lights={
            FEATURE_NIGHT: LightConfig(
                red_key=PD_BACKLIGHT_RED,
                green_key=PD_BACKLIGHT_GREEN,
                blue_key=PD_BACKLIGHT_BLUE,
                rgb_brightness=True,
            )
        },
    ),
    _create_polaris_kettle(
        device_type=245,
        switches=[FEATURE_BACKLIGHT, FEATURE_CHILD_LOCK, FEATURE_VOLUME],
        min_temp=40,
        target_temp_step=10.0,
        operation_modes_map={
            STATE_OFF: 0,
            KETTLE_MODE_BOILING: 1,
            KETTLE_MODE_WARM_UP: 3,
        },
        temperature_modes_map={
            KETTLE_MODE_BOILING: (100, 100),
            KETTLE_MODE_WARM_UP: (40, 90),
        },
    ),
    _create_polaris_kettle(
        device_type=332,
        has_boiling_keep=True,
        switches=[FEATURE_BACKLIGHT, FEATURE_CHILD_LOCK, FEATURE_VOLUME],
        program_data_fields={
            PD_BACKLIGHT_RED: ProgramDataField(mode=0, max_value=255),
            PD_BACKLIGHT_GREEN: ProgramDataField(mode=0, offset=1, max_value=255),
            PD_BACKLIGHT_BLUE: ProgramDataField(mode=0, offset=2, max_value=255),
        },
        lights={
            FEATURE_NIGHT: LightConfig(
                red_key=PD_BACKLIGHT_RED,
                green_key=PD_BACKLIGHT_GREEN,
                blue_key=PD_BACKLIGHT_BLUE,
                rgb_brightness=True,
            )
        },
    ),
    _create_polaris_kettle(
        device_type=337,
        has_boiling_keep=True,
        switches=[FEATURE_BACKLIGHT, FEATURE_CHILD_LOCK, FEATURE_VOLUME],
        program_data_fields={
            PD_BACKLIGHT_RED: ProgramDataField(mode=0, max_value=255),
            PD_BACKLIGHT_GREEN: ProgramDataField(mode=0, offset=1, max_value=255),
            PD_BACKLIGHT_BLUE: ProgramDataField(mode=0, offset=2, max_value=255),
        },
        lights={
            FEATURE_NIGHT: LightConfig(
                red_key=PD_BACKLIGHT_RED,
                green_key=PD_BACKLIGHT_GREEN,
                blue_key=PD_BACKLIGHT_BLUE,
                rgb_brightness=True,
            )
        },
    ),
    _create_polaris_kettle(
        device_type=338,
        has_boiling_keep=True,
        switches=[FEATURE_BACKLIGHT, FEATURE_CHILD_LOCK, FEATURE_VOLUME],
        program_data_fields={
            PD_BACKLIGHT_RED: ProgramDataField(mode=0, max_value=255),
            PD_BACKLIGHT_GREEN: ProgramDataField(mode=0, offset=1, max_value=255),
            PD_BACKLIGHT_BLUE: ProgramDataField(mode=0, offset=2, max_value=255),
        },
        lights={
            FEATURE_NIGHT: LightConfig(
                red_key=PD_BACKLIGHT_RED,
                green_key=PD_BACKLIGHT_GREEN,
                blue_key=PD_BACKLIGHT_BLUE,
                rgb_brightness=True,
            )
        },
    ),
    _create_polaris_kettle(
        device_type=339,
        has_boiling_keep=True,
        switches=[FEATURE_BACKLIGHT, FEATURE_CHILD_LOCK, FEATURE_VOLUME],
        program_data_fields={
            PD_BACKLIGHT_RED: ProgramDataField(mode=0, max_value=255),
            PD_BACKLIGHT_GREEN: ProgramDataField(mode=0, offset=1, max_value=255),
            PD_BACKLIGHT_BLUE: ProgramDataField(mode=0, offset=2, max_value=255),
        },
        lights={
            FEATURE_NIGHT: LightConfig(
                red_key=PD_BACKLIGHT_RED,
                green_key=PD_BACKLIGHT_GREEN,
                blue_key=PD_BACKLIGHT_BLUE,
                rgb_brightness=True,
            )
        },
    ),
]
