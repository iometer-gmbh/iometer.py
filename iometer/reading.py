"""IOmeter reading."""

import json
from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class Register:
    """Represents a meter register reading."""

    obis: str
    value: float
    unit: str


@dataclass
class MeterReading:
    """Represents a point-in-time reading."""

    time: datetime
    registers: List[Register]

    def get_register_by_obis(self, obis: str) -> Register | None:
        """Get register by OBIS code."""
        return next((reg for reg in self.registers if reg.obis == obis), None)


@dataclass
class Meter:
    """Represents the meter device."""

    number: str
    reading: MeterReading


@dataclass
class Reading:
    """Top level class representing a complete meter reading."""

    meter: Meter
    typename: str = "iometer.reading.v1"

    # OBIS code constants
    TOTAL_CONSUMPTION_OBIS = "01-00:01.08.00*ff"
    TOTAL_PRODUCTION_OBIS = "01-00:02.08.00*ff"
    CURRENT_POWER_OBIS = "01-00:10.07.00*ff"

    @classmethod
    def from_json(cls, json_str: str) -> "Reading":
        """Create Reading instance from JSON string."""
        data = json.loads(json_str)

        # Create registers
        registers = [
            Register(obis=reg["obis"], value=reg["value"], unit=reg["unit"])
            for reg in data["meter"]["reading"]["registers"]
        ]

        # Create meter reading
        meter_reading = MeterReading(
            time=datetime.fromisoformat(
                data["meter"]["reading"]["time"].replace("Z", "+00:00")
            ),
            registers=registers,
        )

        # Create meter
        meter = Meter(number=data["meter"]["number"], reading=meter_reading)

        # Create reading
        return cls(meter=meter)

    def to_json(self) -> str:
        """Convert the status to JSON string"""
        return json.dumps(
            {
                "__typename": self.typename,
                "meter": {
                    "number": self.meter.number,
                    "reading": {
                        "time": self.meter.reading.time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                        "registers": [
                            {
                                "obis": register.obis,
                                "value": register.value,
                                "unit": register.unit,
                            }
                            for register in self.meter.reading.registers
                        ],
                    },
                },
            }
        )

    def get_total_consumption(self) -> float:
        """Get total consumption in Wh."""
        register = self.meter.reading.get_register_by_obis(self.TOTAL_CONSUMPTION_OBIS)
        return register.value if register else 0

    def get_total_production(self) -> float:
        """Get total production in Wh."""
        register = self.meter.reading.get_register_by_obis(self.TOTAL_PRODUCTION_OBIS)
        return register.value if register else 0

    def get_current_power(self) -> float:
        """Get current power consumption in W."""
        register = self.meter.reading.get_register_by_obis(self.CURRENT_POWER_OBIS)
        return register.value if register else 0

    def __str__(self) -> str:
        return self.to_json()
