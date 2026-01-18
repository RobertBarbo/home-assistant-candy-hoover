from abc import abstractmethod

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .client.model import TumbleDryerStatus
from .const import *


async def async_setup_entry(
    hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities
):
    """Set up the Candy binary sensors from config entry."""
    config_id = config_entry.entry_id
    coordinator = hass.data[DOMAIN][config_id][DATA_KEY_COORDINATOR]

    if isinstance(coordinator.data, TumbleDryerStatus):
        async_add_entities(
            [
                CandyTumbleRemoteControlBinarySensor(coordinator, config_id),
                CandyTumbleRefreshBinarySensor(coordinator, config_id),
                CandyTumbleNeedCleanFilterBinarySensor(coordinator, config_id),
                CandyTumbleWaterTankFullBinarySensor(coordinator, config_id),
                CandyTumbleDoorClosedBinarySensor(coordinator, config_id),
            ]
        )


class CandyBaseBinarySensor(CoordinatorEntity, BinarySensorEntity):
    def __init__(self, coordinator: DataUpdateCoordinator, config_id: str):
        super().__init__(coordinator)
        self.config_id = config_id

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self.config_id)},
            name=self.device_name(),
            manufacturer=MANUFACTURER,
            suggested_area=self.suggested_area(),
        )

    @abstractmethod
    def device_name(self) -> str:
        pass

    @abstractmethod
    def suggested_area(self) -> str:
        pass


class CandyTumbleRemoteControlBinarySensor(CandyBaseBinarySensor):
    def device_name(self) -> str:
        return DEVICE_NAME_TUMBLE_DRYER

    def suggested_area(self) -> str:
        return SUGGESTED_AREA_BATHROOM

    @property
    def name(self) -> str:
        return "Dryer remote control"

    @property
    def unique_id(self) -> str:
        return UNIQUE_ID_TUMBLE_REMOTE_CONTROL.format(self.config_id)

    @property
    def is_on(self) -> bool:
        status: TumbleDryerStatus = self.coordinator.data
        return bool(status.remote_control)

    @property
    def icon(self) -> str:
        return "mdi:remote"


class CandyTumbleRefreshBinarySensor(CandyBaseBinarySensor):
    def device_name(self) -> str:
        return DEVICE_NAME_TUMBLE_DRYER

    def suggested_area(self) -> str:
        return SUGGESTED_AREA_BATHROOM

    @property
    def name(self) -> str:
        return "Dryer refresh"

    @property
    def unique_id(self) -> str:
        return UNIQUE_ID_TUMBLE_REFRESH.format(self.config_id)

    @property
    def is_on(self) -> bool:
        status: TumbleDryerStatus = self.coordinator.data
        return bool(status.refresh)

    @property
    def icon(self) -> str:
        return "mdi:refresh"


class CandyTumbleNeedCleanFilterBinarySensor(CandyBaseBinarySensor):
    def device_name(self) -> str:
        return DEVICE_NAME_TUMBLE_DRYER

    def suggested_area(self) -> str:
        return SUGGESTED_AREA_BATHROOM

    @property
    def name(self) -> str:
        return "Dryer needs clean filter"

    @property
    def unique_id(self) -> str:
        return UNIQUE_ID_TUMBLE_NEED_CLEAN_FILTER.format(self.config_id)

    @property
    def is_on(self) -> bool:
        status: TumbleDryerStatus = self.coordinator.data
        return bool(status.need_clean_filter)

    @property
    def icon(self) -> str:
        return "mdi:air-filter"


class CandyTumbleWaterTankFullBinarySensor(CandyBaseBinarySensor):
    def device_name(self) -> str:
        return DEVICE_NAME_TUMBLE_DRYER

    def suggested_area(self) -> str:
        return SUGGESTED_AREA_BATHROOM

    @property
    def name(self) -> str:
        return "Dryer water tank full"

    @property
    def unique_id(self) -> str:
        return UNIQUE_ID_TUMBLE_WATER_TANK_FULL.format(self.config_id)

    @property
    def is_on(self) -> bool:
        status: TumbleDryerStatus = self.coordinator.data
        return bool(status.water_tank_full)

    @property
    def icon(self) -> str:
        return "mdi:cup-water"


class CandyTumbleDoorClosedBinarySensor(CandyBaseBinarySensor):
    def device_name(self) -> str:
        return DEVICE_NAME_TUMBLE_DRYER

    def suggested_area(self) -> str:
        return SUGGESTED_AREA_BATHROOM

    @property
    def name(self) -> str:
        return "Dryer door closed"

    @property
    def unique_id(self) -> str:
        return UNIQUE_ID_TUMBLE_DOOR_CLOSED.format(self.config_id)

    @property
    def is_on(self) -> bool:
        status: TumbleDryerStatus = self.coordinator.data
        return bool(status.door_closed)

    @property
    def icon(self) -> str:
        return "mdi:door-closed" if self.is_on else "mdi:door-open"
