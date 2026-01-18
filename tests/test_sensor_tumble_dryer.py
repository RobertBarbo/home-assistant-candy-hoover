"""Tests for various sensors"""
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry, entity_registry
from pytest_homeassistant_custom_component.common import load_fixture
from pytest_homeassistant_custom_component.test_util.aiohttp import \
    AiohttpClientMocker

from .common import init_integration


async def test_main_sensor_idle(hass: HomeAssistant, aioclient_mock: AiohttpClientMocker):
    await init_integration(hass, aioclient_mock, load_fixture("tumble_dryer/idle.json"))

    state = hass.states.get("sensor.tumble_dryer")

    assert state
    assert state.state == "Idle"
    assert state.attributes == {
        'program': 1,
        'remaining_minutes': 150,
        'remote_control': True,
        'dry_level': 2,
        'dry_level_now': 1,
        'refresh': False,
        'need_clean_filter': False,
        'water_tank_full': False,
        'door_closed': True,
        'friendly_name': 'Tumble dryer',
        'icon': 'mdi:tumble-dryer'
    }


async def test_main_sensor_running(hass: HomeAssistant, aioclient_mock: AiohttpClientMocker):
    await init_integration(hass, aioclient_mock, load_fixture("tumble_dryer/running.json"))

    state = hass.states.get("sensor.tumble_dryer")

    assert state
    assert state.state == "Running"
    assert state.attributes == {
        'program': 1,
        'remaining_minutes': 150,
        'remote_control': True,
        'dry_level': 2,
        'dry_level_now': 1,
        'refresh': False,
        'need_clean_filter': False,
        'water_tank_full': False,
        'door_closed': True,
        'friendly_name': 'Tumble dryer',
        'icon': 'mdi:tumble-dryer'
    }


async def test_cycle_sensor_idle(hass: HomeAssistant, aioclient_mock: AiohttpClientMocker):
    await init_integration(hass, aioclient_mock, load_fixture("tumble_dryer/idle.json"))

    state = hass.states.get("sensor.dryer_cycle_status")

    assert state
    assert state.state == "Hang Dry"
    assert state.attributes == {
        "friendly_name": "Dryer cycle status",
        "icon": "mdi:tumble-dryer"
    }


async def test_cycle_sensor_running(hass: HomeAssistant, aioclient_mock: AiohttpClientMocker):
    await init_integration(hass, aioclient_mock, load_fixture("tumble_dryer/running.json"))

    state = hass.states.get("sensor.dryer_cycle_status")

    assert state
    assert state.state == "Running"
    assert state.attributes == {
        "friendly_name": "Dryer cycle status",
        "icon": "mdi:tumble-dryer"
    }


async def test_remaining_time_sensor_idle(hass: HomeAssistant, aioclient_mock: AiohttpClientMocker):
    await init_integration(hass, aioclient_mock, load_fixture("tumble_dryer/idle.json"))

    state = hass.states.get("sensor.dryer_cycle_remaining_time")

    assert state
    assert state.state == "0"
    assert state.attributes == {
        "friendly_name": "Dryer cycle remaining time",
        "icon": "mdi:progress-clock",
        "unit_of_measurement": "min",
    }


async def test_remaining_time_sensor_running(hass: HomeAssistant, aioclient_mock: AiohttpClientMocker):
    await init_integration(hass, aioclient_mock, load_fixture("tumble_dryer/running.json"))

    state = hass.states.get("sensor.dryer_cycle_remaining_time")

    assert state
    assert state.state == "150"
    assert state.attributes == {
        "friendly_name": "Dryer cycle remaining time",
        "icon": "mdi:progress-clock",
        "unit_of_measurement": "min",
    }


async def test_additional_entities_idle(hass: HomeAssistant, aioclient_mock: AiohttpClientMocker):
    await init_integration(hass, aioclient_mock, load_fixture("tumble_dryer/idle.json"))

    program = hass.states.get("sensor.dryer_program")
    remaining = hass.states.get("sensor.dryer_remaining_minutes")
    dry_level = hass.states.get("sensor.dryer_dry_level")
    dry_level_now = hass.states.get("sensor.dryer_dry_level_now")

    remote_control = hass.states.get("binary_sensor.dryer_remote_control")
    refresh = hass.states.get("binary_sensor.dryer_refresh")
    need_clean_filter = hass.states.get("binary_sensor.dryer_needs_clean_filter")
    water_tank_full = hass.states.get("binary_sensor.dryer_water_tank_full")
    door_closed = hass.states.get("binary_sensor.dryer_door_closed")

    assert program
    assert program.state == "1"

    assert remaining
    assert remaining.state == "150"
    assert remaining.attributes["unit_of_measurement"] == "min"

    assert dry_level
    assert dry_level.state == "2"

    assert dry_level_now
    assert dry_level_now.state == "1"

    assert remote_control
    assert remote_control.state == "on"

    assert refresh
    assert refresh.state == "off"

    assert need_clean_filter
    assert need_clean_filter.state == "off"

    assert water_tank_full
    assert water_tank_full.state == "off"

    assert door_closed
    assert door_closed.state == "on"


async def test_main_sensor_device_info(hass: HomeAssistant, aioclient_mock: AiohttpClientMocker):
    await init_integration(hass, aioclient_mock, load_fixture("tumble_dryer/idle.json"))

    entity_reg = entity_registry.async_get(hass)
    device_reg = device_registry.async_get(hass)
    entry = entity_reg.async_get("sensor.tumble_dryer")
    device = device_reg.async_get(entry.device_id)

    assert device
    assert device.manufacturer == "Hoover+Candy"
    assert device.name == "Tumble dryer"
    assert device.suggested_area == "Bathroom"


async def test_sensors_device_info(hass: HomeAssistant, aioclient_mock: AiohttpClientMocker):
    await init_integration(hass, aioclient_mock, load_fixture("tumble_dryer/idle.json"))

    entity_reg = entity_registry.async_get(hass)
    device_reg = device_registry.async_get(hass)

    main_sensor = entity_reg.async_get("sensor.tumble_dryer")
    cycle_sensor = entity_reg.async_get("sensor.dryer_cycle_status")
    time_sensor = entity_reg.async_get("sensor.dryer_cycle_remaining_time")
    program_sensor = entity_reg.async_get("sensor.dryer_program")
    door_closed_binary = entity_reg.async_get("binary_sensor.dryer_door_closed")

    main_device = device_reg.async_get(main_sensor.device_id)
    cycle_device = device_reg.async_get(cycle_sensor.device_id)
    time_device = device_reg.async_get(time_sensor.device_id)
    program_device = device_reg.async_get(program_sensor.device_id)
    door_device = device_reg.async_get(door_closed_binary.device_id)

    assert main_device
    assert cycle_device
    assert time_device
    assert program_device
    assert door_device
    assert main_device == cycle_device == time_device == program_device == door_device
