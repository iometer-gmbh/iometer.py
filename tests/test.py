"""Tests for the IOmeter package."""

import pytest
from aiohttp import ClientResponseError, ClientSession
from aioresponses import aioresponses

from iometer.client import IOmeterClient
from iometer.exceptions import (
    IOmeterConnectionError,
    IOmeterNoReadingsError,
    IOmeterNoStatusError,
    IOmeterTimeoutError,
)
from iometer.reading import Reading
from iometer.status import NullMeter, Status

HOST = "192.168.1.100"


@pytest.fixture(name="reading_json")
def reading_json_fixture():
    """Fixture reading response."""
    return {
        "__typename": "iometer.reading.v1",
        "meter": {
            "number": "1ISK0000000000",
            "reading": {
                "time": "2024-11-11T11:11:11Z",
                "registers": [
                    {"obis": "01-00:01.08.00*ff", "value": 1234.5, "unit": "Wh"},
                    {"obis": "01-00:02.08.00*ff", "value": 5432.1, "unit": "Wh"},
                    {"obis": "01-00:10.07.00*ff", "value": 100, "unit": "W"},
                ],
            },
        },
    }


@pytest.fixture(name="reading_alt_obis_json")
def reading_alt_obis_json_fixture():
    """Fixture reading response with alternate current power OBIS only."""
    return {
        "__typename": "iometer.reading.v1",
        "meter": {
            "number": "1ISK0000000000",
            "reading": {
                "time": "2024-11-11T11:11:11Z",
                "registers": [
                    {"obis": "01-00:01.08.00*ff", "value": 1234.5, "unit": "Wh"},
                    {"obis": "01-00:02.08.00*ff", "value": 5432.1, "unit": "Wh"},
                    {"obis": "01-00:24.07.00*ff", "value": 100, "unit": "W"},
                ],
            },
        },
    }


@pytest.fixture(name="reading_no_power_obis_json")
def reading_no_power_obis_json_fixture():
    """Fixture reading response without any current power OBIS registers."""
    return {
        "__typename": "iometer.reading.v1",
        "meter": {
            "number": "1ISK0000000000",
            "reading": {
                "time": "2024-11-11T11:11:11Z",
                "registers": [
                    {"obis": "01-00:01.08.00*ff", "value": 1234.5, "unit": "Wh"},
                    {"obis": "01-00:02.08.00*ff", "value": 5432.1, "unit": "Wh"},
                ],
            },
        },
    }


@pytest.fixture(name="reading_no_power_no_production_obis_json")
def reading_no_power_no_production_obis_json_fixture():
    """Fixture reading response without any current power OBIS
    and production OBIS register.
    """
    return {
        "__typename": "iometer.reading.v1",
        "meter": {
            "number": "1ISK0000000000",
            "reading": {
                "time": "2024-11-11T11:11:11Z",
                "registers": [
                    {"obis": "01-00:01.08.00*ff", "value": 1234.5, "unit": "Wh"}
                ],
            },
        },
    }


@pytest.fixture(name="status_json")
def status_json_fixture():
    """ "Fixture status response"""
    return {
        "__typename": "iometer.status.v1",
        "meter": {
            "number": "1ISK0000000000",
        },
        "device": {
            "bridge": {"rssi": -30, "version": "build-65"},
            "id": "658c2b34-2017-45f2-a12b-731235f8bb97",
            "core": {
                "connectionStatus": "connected",
                "rssi": -30,
                "version": "build-58",
                "powerStatus": "battery",
                "batteryLevel": 100,
                "attachmentStatus": "attached",
                "pinStatus": "entered",
            },
        },
    }


@pytest.fixture(name="status_wired_json")
def status_wired_json_fixture():
    """ "Fixture status response with wired power"""
    return {
        "__typename": "iometer.status.v1",
        "meter": {
            "number": "1ISK0000000000",
        },
        "device": {
            "bridge": {"rssi": -30, "version": "build-65"},
            "id": "658c2b34-2017-45f2-a12b-731235f8bb97",
            "core": {
                "connectionStatus": "connected",
                "rssi": -30,
                "version": "build-58",
                "powerStatus": "wired",
                "attachmentStatus": "attached",
                "pinStatus": "entered",
            },
        },
    }


@pytest.fixture(name="status_detached_json")
def status_detached_json_fixture():
    """ "Fixture status response with detached core"""
    return {
        "__typename": "iometer.status.v1",
        "meter": {
            "number": "1ISK0000000000",
        },
        "device": {
            "bridge": {"rssi": -30, "version": "build-65"},
            "id": "658c2b34-2017-45f2-a12b-731235f8bb97",
            "core": {
                "connectionStatus": "connected",
                "rssi": -30,
                "version": "build-58",
                "powerStatus": "wired",
                "attachmentStatus": "detached",
            },
        },
    }


@pytest.fixture(name="status_disconnected_json")
def status_disconnected_json_fixture():
    """ "Fixture status response with disconnected core"""
    return {
        "__typename": "iometer.status.v1",
        "meter": {
            "number": "1ISK0000000000",
        },
        "device": {
            "bridge": {"rssi": -30, "version": "build-65"},
            "id": "658c2b34-2017-45f2-a12b-731235f8bb97",
            "core": {"connectionStatus": "disconnected"},
        },
    }


@pytest.fixture(name="status_no_meter_json")
def status_no_meter_json_fixture():
    """ "Fixture status response"""
    return {
        "__typename": "iometer.status.v1",
        "device": {
            "bridge": {"rssi": -30, "version": "build-65"},
            "id": "658c2b34-2017-45f2-a12b-731235f8bb97",
            "core": {
                "connectionStatus": "connected",
                "rssi": -30,
                "version": "build-58",
                "powerStatus": "battery",
                "batteryLevel": 100,
                "attachmentStatus": "attached",
            },
        },
    }


@pytest.fixture(name="mock_aioresponse")
def mock_aioresponse_fixture():
    """ "Fixture mock session"""
    with aioresponses() as m:
        yield m


@pytest.fixture(name="client_iometer")
async def client_iometer_fixture():
    """Fixture IOmeter client"""
    async with IOmeterClient(HOST) as client:
        yield client


@pytest.mark.asyncio
async def test_client_initialization():
    """Test client initialization."""
    client = IOmeterClient("test-host")
    assert client.host == "test-host"
    assert client.request_timeout == 5
    assert client.session is None


@pytest.mark.asyncio
async def test_client_context_manager():
    """Test client as context manager."""
    async with IOmeterClient("test-host") as client:
        assert isinstance(client.session, ClientSession)
        assert not client.session.closed  # Session should not be closed

    # After the context
    assert client.session is None  # Verify session is closed


@pytest.mark.asyncio
async def test_get_current_reading(client_iometer, mock_aioresponse, reading_json):
    """Test getting current reading."""
    mock_endpoint = f"http://{HOST}/v1/reading"
    mock_aioresponse.get(mock_endpoint, status=200, payload=reading_json)

    reading = await client_iometer.get_current_reading()
    assert isinstance(reading, Reading)
    assert reading.meter.number == "1ISK0000000000"
    assert reading.get_total_consumption() == 1234.5
    assert reading.get_total_production() == 5432.1
    assert reading.get_current_power() == 100


@pytest.mark.asyncio
async def test_get_current_reading_alt_obis(
    client_iometer, mock_aioresponse, reading_alt_obis_json
):
    """Test current power using alternate OBIS when primary is missing."""
    mock_endpoint = f"http://{HOST}/v1/reading"
    mock_aioresponse.get(mock_endpoint, status=200, payload=reading_alt_obis_json)

    reading = await client_iometer.get_current_reading()
    assert isinstance(reading, Reading)
    assert reading.get_current_power() == 100


@pytest.mark.asyncio
async def test_get_current_reading_no_power_obis(
    client_iometer, mock_aioresponse, reading_no_power_obis_json
):
    """Test current power returns None when no power OBIS registers are present."""
    mock_endpoint = f"http://{HOST}/v1/reading"
    mock_aioresponse.get(mock_endpoint, status=200, payload=reading_no_power_obis_json)

    reading = await client_iometer.get_current_reading()
    assert isinstance(reading, Reading)
    assert reading.get_current_power() is None
    assert reading.get_total_production() == 5432.1
    assert reading.get_total_consumption() == 1234.5


@pytest.mark.asyncio
async def test_get_current_reading_no_power_no_production_obis(
    client_iometer, mock_aioresponse, reading_no_power_no_production_obis_json
):
    """Test current power returns None when no power OBIS registers are present."""
    mock_endpoint = f"http://{HOST}/v1/reading"
    mock_aioresponse.get(
        mock_endpoint, status=200, payload=reading_no_power_no_production_obis_json
    )

    reading = await client_iometer.get_current_reading()
    assert isinstance(reading, Reading)
    assert reading.get_current_power() is None
    assert reading.get_total_production() is None
    assert reading.get_total_consumption() == 1234.5


@pytest.mark.asyncio
async def test_get_current_status(client_iometer, mock_aioresponse, status_json):
    """Test getting device status."""

    mock_endpoint = f"http://{HOST}/v1/status"
    mock_aioresponse.get(mock_endpoint, status=200, payload=status_json)

    status = await client_iometer.get_current_status()

    assert isinstance(status, Status)
    assert status.meter.number == "1ISK0000000000"
    assert status.device.bridge.rssi == -30
    assert status.device.bridge.version == "build-65"
    assert status.device.id == "658c2b34-2017-45f2-a12b-731235f8bb97"
    assert status.device.core.connection_status == "connected"
    assert status.device.core.rssi == -30
    assert status.device.core.version == "build-58"
    assert status.device.core.power_status == "battery"
    assert status.device.core.battery_level == 100
    assert status.device.core.attachment_status == "attached"
    assert status.device.core.pin_status == "entered"


@pytest.mark.asyncio
async def test_get_current_status_wired(
    client_iometer, mock_aioresponse, status_wired_json
):
    """Test getting device status."""

    mock_endpoint = f"http://{HOST}/v1/status"
    mock_aioresponse.get(mock_endpoint, status=200, payload=status_wired_json)

    status = await client_iometer.get_current_status()

    assert isinstance(status, Status)
    assert status.meter.number == "1ISK0000000000"
    assert status.device.bridge.rssi == -30
    assert status.device.bridge.version == "build-65"
    assert status.device.id == "658c2b34-2017-45f2-a12b-731235f8bb97"
    assert status.device.core.connection_status == "connected"
    assert status.device.core.rssi == -30
    assert status.device.core.version == "build-58"
    assert status.device.core.power_status == "wired"
    assert status.device.core.battery_level is None
    assert status.device.core.attachment_status == "attached"
    assert status.device.core.pin_status == "entered"


@pytest.mark.asyncio
async def test_get_current_status_detached(
    client_iometer, mock_aioresponse, status_detached_json
):
    """Test getting device status."""

    mock_endpoint = f"http://{HOST}/v1/status"
    mock_aioresponse.get(mock_endpoint, status=200, payload=status_detached_json)

    status = await client_iometer.get_current_status()

    assert isinstance(status, Status)
    assert status.meter.number == "1ISK0000000000"
    assert status.device.bridge.rssi == -30
    assert status.device.bridge.version == "build-65"
    assert status.device.id == "658c2b34-2017-45f2-a12b-731235f8bb97"
    assert status.device.core.connection_status == "connected"
    assert status.device.core.rssi == -30
    assert status.device.core.version == "build-58"
    assert status.device.core.power_status == "wired"
    assert status.device.core.battery_level is None
    assert status.device.core.attachment_status == "detached"
    assert status.device.core.pin_status is None


@pytest.mark.asyncio
async def test_get_current_status_disconnected(
    client_iometer, mock_aioresponse, status_disconnected_json
):
    """Test getting device status."""

    mock_endpoint = f"http://{HOST}/v1/status"
    mock_aioresponse.get(mock_endpoint, status=200, payload=status_disconnected_json)

    status = await client_iometer.get_current_status()

    assert isinstance(status, Status)
    assert status.meter.number == "1ISK0000000000"
    assert status.device.bridge.rssi == -30
    assert status.device.bridge.version == "build-65"
    assert status.device.id == "658c2b34-2017-45f2-a12b-731235f8bb97"
    assert status.device.core.connection_status == "disconnected"
    assert status.device.core.rssi is None
    assert status.device.core.version is None
    assert status.device.core.power_status is None
    assert status.device.core.battery_level is None
    assert status.device.core.attachment_status is None
    assert status.device.core.pin_status is None


@pytest.mark.asyncio
async def test_get_current_status_no_meter(
    client_iometer, mock_aioresponse, status_no_meter_json
):
    """Test getting device status."""

    mock_endpoint = f"http://{HOST}/v1/status"
    mock_aioresponse.get(mock_endpoint, status=200, payload=status_no_meter_json)

    status = await client_iometer.get_current_status()

    assert isinstance(status, Status)
    assert isinstance(status.meter, NullMeter)
    assert status.meter.number is None
    assert status.device.bridge.rssi == -30
    assert status.device.bridge.version == "build-65"
    assert status.device.id == "658c2b34-2017-45f2-a12b-731235f8bb97"
    assert status.device.core.connection_status == "connected"
    assert status.device.core.rssi == -30
    assert status.device.core.version == "build-58"
    assert status.device.core.power_status == "battery"
    assert status.device.core.battery_level == 100
    assert status.device.core.attachment_status == "attached"
    assert status.device.core.pin_status is None


@pytest.mark.asyncio
async def test_timeout_error(client_iometer, mock_aioresponse):
    """Test handling of timeout errors."""

    mock_endpoint = f"http://{HOST}/v1/reading"
    mock_aioresponse.get(mock_endpoint, timeout=True)

    with pytest.raises(IOmeterTimeoutError, match="Timeout while communicating"):
        await client_iometer.get_current_reading()


@pytest.mark.asyncio
async def test_client_error(client_iometer, mock_aioresponse):
    """Test handling of client errors."""

    mock_endpoint = f"http://{HOST}/v1/reading"
    mock_aioresponse.get(mock_endpoint, exception=ClientResponseError)
    with pytest.raises(IOmeterConnectionError, match="Error communicating"):
        await client_iometer.get_current_reading()


@pytest.mark.asyncio
async def test_reading_not_found(client_iometer, mock_aioresponse):
    """Test that a 404 on the reading endpoint raises IOmeterNoReadingsError."""

    mock_endpoint = f"http://{HOST}/v1/reading"
    mock_aioresponse.get(mock_endpoint, status=404)

    with pytest.raises(IOmeterNoReadingsError, match="No readings available"):
        await client_iometer.get_current_reading()


@pytest.mark.asyncio
async def test_status_not_found(client_iometer, mock_aioresponse):
    """Test that a 404 on the status endpoint raises IOmeterNoStatusError."""

    mock_endpoint = f"http://{HOST}/v1/status"
    mock_aioresponse.get(mock_endpoint, status=404)

    with pytest.raises(IOmeterNoStatusError, match="No status available"):
        await client_iometer.get_current_status()
