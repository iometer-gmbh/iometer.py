"""Device status for IOmeter bridge and core"""

import json
from dataclasses import dataclass


@dataclass
class Bridge:
    """Represents the bridge device status"""

    rssi: int
    version: str


@dataclass
class Core:
    """Represents the core device status"""

    connection_status: str
    rssi: int | None
    version: str | None
    power_status: str | None
    attachment_status: str | None
    pin_status: str | None
    battery_level: int | None


@dataclass
class Device:
    """Represents the complete device information"""

    bridge: Bridge
    id: str
    core: Core


@dataclass
class Meter:
    """Represents the meter device."""

    number: str


@dataclass
class Status:
    """Top level class representing the complete device status"""

    meter: Meter
    device: Device
    typename: str = "iometer.status.v1"

    @classmethod
    def from_json(cls, json_str: str) -> "Status":
        """Create a Status instance from JSON string"""
        data = json.loads(json_str)

        # Create bridge
        bridge = Bridge(
            rssi=data["device"]["bridge"]["rssi"],
            version=data["device"]["bridge"]["version"],
        )

        # Create Core
        core_data = data["device"]["core"]

        core = Core(
            connection_status=core_data["connectionStatus"],
            rssi=core_data.get("rssi", None),
            version=core_data.get("version", None),
            power_status=core_data.get("powerStatus", None),
            battery_level=core_data.get("batteryLevel", None),
            attachment_status=core_data.get("attachmentStatus", None),
            pin_status=core_data.get("pinStatus", None),
        )

        # Create device
        device = Device(bridge=bridge, id=data["device"]["id"], core=core)

        meter = Meter(number=data["meter"]["number"])

        # Create full status
        return cls(meter=meter, device=device)

    def to_json(self) -> str:
        """Convert the status to JSON string"""
        return json.dumps(
            {
                "__typename": self.typename,
                "meter": {"number": self.meter.number},
                "device": {
                    "bridge": {
                        "rssi": self.device.bridge.rssi,
                        "version": self.device.bridge.version,
                    },
                    "id": self.device.id,
                    "core": {
                        "connectionStatus": self.device.core.connection_status,
                        "rssi": self.device.core.rssi,
                        "version": self.device.core.version,
                        "powerStatus": self.device.core.power_status,
                        "batteryLevel": self.device.core.battery_level,
                        "attachmentStatus": self.device.core.attachment_status,
                        "pinStatus": self.device.core.pin_status,
                    },
                },
            }
        )

    def __str__(self) -> str:
        return self.to_json()
