"""Kettle control using separate mode and temperature protocol commands."""

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from homeassistant.components.select import SelectEntity
from homeassistant.components.water_heater import WaterHeaterEntity
from homeassistant.const import ATTR_TEMPERATURE, STATE_OFF, UnitOfTemperature
from homeassistant.core import callback
from homeassistant.exceptions import ServiceValidationError
from pysyncleo.commands import CmdMode, CmdTargetTemperature, UdpCommandType

from .const import (
    DOMAIN,
    FEATURE_KETTLE_TEMPERATURE_PRESET,
    KETTLE_MODE_BOILING,
    KETTLE_MODE_WARM_UP,
    KETTLE_PRESET_NONE,
)
from .devices import KettleProfile, SelectConfig
from .entity import SyncleoBaseEntity
from .models import SyncleoConfigEntry


@dataclass
class KettleState:
    """Intent shared by the heater and preset entities of one config entry."""

    mode: int | None = None
    selected_mode: str | None = None
    target: float | None = None
    device_target: float | None = None
    temperature: float | None = None
    staged: bool = False
    preset: str = KETTLE_PRESET_NONE
    listeners: set[Callable[[], None]] = field(default_factory=set)

    @callback
    def notify(self) -> None:
        for listener in self.listeners.copy():
            listener()


class SyncleoKettleEntity(SyncleoBaseEntity):
    def __init__(
        self,
        connection,
        profile: KettleProfile,
        entry: SyncleoConfigEntry,
        state: KettleState,
    ) -> None:
        super().__init__(connection, profile, entry)
        self._profile: KettleProfile = profile
        self._state = state

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        self._state.listeners.add(self.async_write_ha_state)

    async def async_will_remove_from_hass(self) -> None:
        self._state.listeners.discard(self.async_write_ha_state)
        await super().async_will_remove_from_hass()

    @callback
    def _handle_device_update(self, cmd) -> None:
        super()._handle_device_update(cmd)
        state = self._state
        if cmd.command_type == UdpCommandType.MODE:
            state.mode = int(cmd.value)
            if state.mode in range(1, 7):
                state.staged = False
                if state.device_target is not None:
                    state.target = state.device_target
                state.selected_mode = next(
                    (
                        name
                        for name, value in self._profile.operation_modes_map.items()
                        if value == state.mode
                    ),
                    None,
                )
        elif cmd.command_type == UdpCommandType.TARGET_TEMPERATURE:
            state.device_target = float(cmd.value)
            if not state.staged:
                state.target = state.device_target
        elif cmd.command_type == UdpCommandType.TEMPERATURE:
            state.temperature = float(cmd.value)
        else:
            return
        config = self._profile.selects.get(FEATURE_KETTLE_TEMPERATURE_PRESET)
        if (
            not state.staged
            and config
            and config.options_map.get(state.preset) != state.target
        ):
            state.preset = KETTLE_PRESET_NONE
        state.notify()

    async def _async_set_temperature(
        self, temperature: float, preset: str = KETTLE_PRESET_NONE
    ) -> None:
        profile = self._profile
        state = self._state
        target = max(profile.min_temp, min(profile.max_temp, temperature))
        if target != int(target):
            raise ServiceValidationError("Kettles accept whole degrees Celsius")
        mode = state.selected_mode
        limits = profile.temperature_modes_map.get(mode) if mode else None
        if limits is None or not limits[0] <= target <= limits[1]:
            mode = KETTLE_MODE_BOILING if target == 100 else KETTLE_MODE_WARM_UP
        limits = profile.temperature_modes_map[mode]
        target = max(limits[0], min(limits[1], target))
        state.selected_mode = mode
        state.target = target
        state.preset = preset
        state.staged = True
        if state.mode in profile.operation_modes_map.values() and state.mode != 0:
            await self._async_start()
        state.notify()

    async def _async_start(self) -> None:
        state = self._state
        mode = state.selected_mode or self._profile.default_operation_mode
        limits = self._profile.temperature_modes_map[mode]
        target = (
            state.target
            if state.target is not None
            else self._profile.default_target_temp
        )
        target = max(limits[0], min(limits[1], target))
        # The firmware handles 0x02 and 0x01 independently. Prepare the target first.
        await self.async_send_command(CmdTargetTemperature(target))
        # Keep the optimistic target when a mode report arrives before its echo.
        state.device_target = target
        await self.async_send_command(CmdMode(self._profile.operation_modes_map[mode]))
        state.target = target
        state.selected_mode = mode
        state.mode = self._profile.operation_modes_map[mode]
        state.staged = False
        config = self._profile.selects.get(FEATURE_KETTLE_TEMPERATURE_PRESET)
        if config and config.options_map.get(state.preset) != target:
            state.preset = KETTLE_PRESET_NONE
        state.notify()


class SyncleoKettle(SyncleoKettleEntity, WaterHeaterEntity):
    """HA has no kettle domain; expose kettle controls through water_heater."""

    _attr_name = None
    _attr_temperature_unit = UnitOfTemperature.CELSIUS

    def __init__(
        self,
        connection,
        profile: KettleProfile,
        entry: SyncleoConfigEntry,
        state: KettleState,
    ) -> None:
        super().__init__(connection, profile, entry, state)
        self._attr_unique_id = f"{self._device_unique_id}_{profile.profile_type}"
        self._attr_translation_key = f"{DOMAIN}_{profile.profile_type}"
        self._attr_min_temp = profile.min_temp
        self._attr_max_temp = profile.max_temp
        self._attr_target_temperature_step = profile.target_temp_step
        self._attr_supported_features = profile.supported_features
        self._attr_operation_list = list(profile.operation_modes_map)

    @property
    def current_operation(self) -> str | None:
        return next(
            (
                name
                for name, value in self._profile.operation_modes_map.items()
                if value == self._state.mode
            ),
            None,
        )

    @property
    def current_temperature(self) -> float | None:
        return self._state.temperature

    @property
    def target_temperature(self) -> float | None:
        return self._state.target

    async def async_turn_on(self, **kwargs: Any) -> None:
        await self._async_start()

    async def async_turn_off(self, **kwargs: Any) -> None:
        await self.async_send_command(CmdMode(0))
        self._state.mode = 0
        self._state.notify()

    async def async_set_temperature(self, **kwargs: Any) -> None:
        if ATTR_TEMPERATURE in kwargs:
            await self._async_set_temperature(float(kwargs[ATTR_TEMPERATURE]))

    async def async_set_operation_mode(self, operation_mode: str) -> None:
        if operation_mode not in self._profile.operation_modes_map:
            raise ServiceValidationError(f"Unsupported kettle mode: {operation_mode}")
        if operation_mode == STATE_OFF:
            await self.async_turn_off()
            return
        self._state.selected_mode = operation_mode
        await self._async_start()


class SyncleoKettlePreset(SyncleoKettleEntity, SelectEntity):
    def __init__(
        self,
        connection,
        profile: KettleProfile,
        entry: SyncleoConfigEntry,
        state: KettleState,
        config: SelectConfig,
    ) -> None:
        super().__init__(connection, profile, entry, state)
        self._config = config
        self._attr_unique_id = (
            f"{self._device_unique_id}_{FEATURE_KETTLE_TEMPERATURE_PRESET}"
        )
        self._attr_translation_key = FEATURE_KETTLE_TEMPERATURE_PRESET
        self._attr_options = config.options

    @property
    def current_option(self) -> str:
        return self._state.preset

    async def async_select_option(self, option: str) -> None:
        if option not in self._config.options_map:
            raise ServiceValidationError(f"Unsupported kettle preset: {option}")
        if option == KETTLE_PRESET_NONE:
            self._state.preset = option
            self._state.notify()
            return
        await self._async_set_temperature(self._config.options_map[option], option)
