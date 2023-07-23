import json
import logging
from contextlib import suppress
from datetime import timedelta
from pathlib import Path
from typing import Optional, Any

import pkg_resources  # type: ignore[import, unused-ignore]
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.typing import HomeAssistantType
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from pyhon.appliance import HonAppliance

from .const import DOMAIN, UPDATE_INTERVAL
from .typedefs import HonEntityDescription, HonOptionEntityDescription, T

_LOGGER = logging.getLogger(__name__)


class HonInfo:
    def __init__(self) -> None:
        self._manifest: dict[str, Any] = self._get_manifest()
        self._hon_version: str = self._manifest.get("version", "")
        self._pyhon_version: str = pkg_resources.get_distribution("pyhon").version

    @staticmethod
    def _get_manifest() -> dict[str, Any]:
        manifest = Path(__file__).parent / "manifest.json"
        with open(manifest, "r", encoding="utf-8") as file:
            result: dict[str, Any] = json.loads(file.read())
        return result

    @property
    def manifest(self) -> dict[str, Any]:
        return self._manifest

    @property
    def hon_version(self) -> str:
        return self._hon_version

    @property
    def pyhon_version(self) -> str:
        return self._pyhon_version


class HonCoordinator(DataUpdateCoordinator[None]):
    def __init__(self, hass: HomeAssistantType, device: HonAppliance):
        """Initialize my coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=device.unique_id,
            update_interval=timedelta(seconds=UPDATE_INTERVAL),
        )
        self._device = device
        self._info = HonInfo()

    async def _async_update_data(self) -> None:
        return await self._device.update()

    @property
    def info(self) -> HonInfo:
        return self._info


class HonEntity(CoordinatorEntity[HonCoordinator]):
    _attr_has_entity_name = True

    def __init__(
        self,
        hass: HomeAssistantType,
        entry: ConfigEntry,
        device: HonAppliance,
        description: Optional[HonEntityDescription] = None,
    ) -> None:
        coordinator = get_coordinator(hass, device)
        super().__init__(coordinator)

        self._hon = hass.data[DOMAIN][entry.unique_id]
        self._hass = hass
        self._coordinator = coordinator
        self._device: HonAppliance = device

        if description is not None:
            self.entity_description = description
            self._attr_unique_id = f"{self._device.unique_id}{description.key}"
        else:
            self._attr_unique_id = self._device.unique_id
        self._handle_coordinator_update(update=False)

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self._device.unique_id)},
            manufacturer=self._device.get("brand", ""),
            name=self._device.nick_name,
            model=self._device.model_name,
            sw_version=self._device.get("fwVersion", ""),
        )

    @callback
    def _handle_coordinator_update(self, update: bool = True) -> None:
        if update:
            self.async_write_ha_state()


def unique_entities(
    base_entities: tuple[T, ...],
    new_entities: tuple[T, ...],
) -> tuple[T, ...]:
    result = list(base_entities)
    existing_entities = [entity.key for entity in base_entities]
    entity: HonEntityDescription
    for entity in new_entities:
        if entity.key not in existing_entities:
            result.append(entity)
    return tuple(result)


def get_coordinator(hass: HomeAssistantType, appliance: HonAppliance) -> HonCoordinator:
    coordinators = hass.data[DOMAIN]["coordinators"]
    if appliance.unique_id in coordinators:
        coordinator: HonCoordinator = hass.data[DOMAIN]["coordinators"][
            appliance.unique_id
        ]
    else:
        coordinator = HonCoordinator(hass, appliance)
        hass.data[DOMAIN]["coordinators"][appliance.unique_id] = coordinator
    return coordinator


def get_readable(
    description: HonOptionEntityDescription, value: float | str
) -> float | str:
    if description.option_list is not None:
        with suppress(ValueError):
            return description.option_list.get(int(value), value)
    return value
