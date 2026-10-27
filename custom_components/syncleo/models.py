import asyncio
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from homeassistant.config_entries import ConfigEntry
from pysyncleo.transport import SyncleoConnection, TransportManager

from .broadcaster import SyncleoVirtualZeroconfBroadcaster

if TYPE_CHECKING:
    from .kettle import KettleState


@dataclass
class SyncleoDomainData:
    manager: TransportManager
    transport: asyncio.DatagramTransport
    ha_uuid: str
    kettle_states: dict[str, KettleState] = field(default_factory=dict)


type SyncleoGenericConfigEntry = ConfigEntry[
    SyncleoConnection | SyncleoVirtualZeroconfBroadcaster
]
type SyncleoConfigEntry = ConfigEntry[SyncleoConnection]
