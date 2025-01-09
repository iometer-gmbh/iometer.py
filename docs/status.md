# Status Documentation

The Status module provides classes for handling IOmeter device status information. It includes enums for various device states.

## Classes

### Status
Top-level class for complete device status:
```python
@dataclass
class Status:
    meter: Meter
    device: Device
    typename: str = "iometer.status.v1"

    @classmethod
    def from_json(cls, json_str: str) -> 'Status':
        # Creates Status instance from JSON string

    def to_json(self) -> str:
        # Converts Status to JSON string
```

### Meter
Represents the meter device:
```python
@dataclass
class Meter:
    number: str
```

### Device
Combines bridge, device id and core information:
```python
@dataclass
class Device:
    bridge: Bridge
    id: str
    core: Core
```

### Core
Represents the core device status:
```python
@dataclass
class Core:
    connection_status: ConnectionStatus
    rssi: int                              # Signal strength in dBm
    version: str                           # Core firmware version
    power_status: PowerStatus
    attachment_status: AttachmentStatus
    battery_level: Optional[int] = None    # Battery percentage if applicable
    pin_status: Optional[PinStatus] = None # PIN status if applicable

    def to_dict(self) -> dict:
        # Converts core data to ordered dictionary
```

### Bridge
Represents the bridge device status:
```python
@dataclass
class Bridge:
    rssi: int           # Signal strength in dBm
    version: str        # Bridge firmware version

    def __str__(self) -> str:
        # Returns formatted string with signal strength and version
```

## Enums

### ConnectionStatus
Represents the device connection state:
```python
class ConnectionStatus(Enum):
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
```

### PowerStatus
Represents the device power source:
```python
class PowerStatus(Enum):
    BATTERY = "battery"
    WIRED = "wired"
```

### AttachmentStatus
Represents physical attachment state:
```python
class AttachmentStatus(Enum):
    ATTACHED = "attached"
    DETACHED = "detached"
```

### PinStatus
Represents PIN entry state:
```python
class PinStatus(Enum):
    ENTERED = "entered"
    PENDING = "pending"
    MISSING = "missing"
```







### JSON Handling
```python
# Parse from JSON
status = Status.from_json(json_string)

# Convert to JSON
json_string = status.to_json()
```