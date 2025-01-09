# Reading Documentation

The Reading module provides classes for handling IOmeter readings. 

## OBIS Codes

Important OBIS codes used in the module:

- `01-00:01.08.00*ff`: Total energy consumption on all tariffs
- `01-00:02.08.00*ff`: Total energy production on all tariffs
- `01-00:10.07.00*ff`: Current power consumption

## Classes

### Reading
Top-level class for complete meter reading, currently consist of one meter:
```python
@dataclass
class Reading:
    __typename: str = "iometer.reading.v1"
    meter: Meter = None

    # OBIS code constants
    TOTAL_CONSUMPTION_OBIS = "01-00:01.08.00*ff"
    TOTAL_PRODUCTION_OBIS = "01-00:02.08.00*ff"

    @classmethod
    def from_json(cls, json_str: str) -> 'Reading':
        # Creates Reading instance from JSON string

    def get_total_consumption(self) -> float:
        # Returns total consumption in Wh

    def get_total_production(self) -> float:
        # Returns total production in Wh

    def get_current_power(self) -> float:
        # Returns current power consumption in W
```

### Meter
Represents the meter device and its reading:
```python
@dataclass
class Meter:
    number: str            # Meter serial number
    reading: MeterReading  # Current meter reading
```

### MeterReading
Represents a collection of register readings at a specific time:
```python
@dataclass
class MeterReading:
    time: datetime          # Timestamp of the reading in UTC
    registers: List[Register] # List of register readings

    def get_register_by_obis(self, obis: str) -> Register | None:
        # Returns specific register by OBIS code
```

### Register
Represents a single meter register reading:
```python
@dataclass
class Register:
    obis: str      # OBIS code identifying the reading type
    value: float   # Reading value
    unit: str      # Unit of measurement (e.g., "Wh", "W")
```

### JSON Handling
```python
# Parse from JSON
reading = Reading.from_json(json_data)

# Access data
meter_number = reading.meter.number
timestamp = reading.meter.reading.time
consumption = reading.get_total_consumption()
```