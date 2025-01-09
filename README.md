# IOmeter Python Client

A Python client for interacting with [IOmeter](https://iometer.de/) devices over HTTP. This client provides an async interface for reading energy consumption/production data and monitoring device status.

## Features

- 🔌 Asynchronous communication with IOmeter bridge over HTTP
- 📊 Read energy consumption and energy production data
- 🔋 Monitor device status including battery level and signal strength

## Quick Start

### Installation

```bash
pip install iometer
```

### Basic Usage

```python
from iometer import IOmeterClient

async def check_meter_reading():
    async with IOmeterClient("192.168.1.100") as client:
        # Get current reading
        reading = await client.get_current_reading()
        
        # Access basic metrics
        consumption = reading.get_total_consumption()
        production = reading.get_total_production()
        power = reading.get_current_power()
        
        print(f"Meter: {reading.meter.number}")
        print(f"Time: {reading.meter.reading.time}")
        print(f"Consumption: {consumption} Wh")
        print(f"Production: {production} Wh")
        print(f"Current Power: {power} W")
```

### Continuous Monitoring

```python
import asyncio
from iometer import IOmeterClient

async def monitor_readings(interval: int = 300):
    """Monitor readings every 5 minutes."""
    async with IOmeterClient("192.168.1.100") as client:
        while True:
            try:
                reading = await client.get_current_reading()
                print(f"Time: {reading.meter.reading.time}")
                print(f"Consumption: {reading.get_total_consumption()} Wh")
                await asyncio.sleep(interval)
            except Exception as e:
                print(f"Error: {e}")
                await asyncio.sleep(60)  # Wait before retry
```
### Device Status Information

```python
from iometer import IOmeterClient

async def check_device_status():
    async with IOmeterClient("192.168.1.100") as client:
        # Get current status
        status = await client.get_current_status()
        
        # Bridge information
        print(f"Bridge Version: {status.device.bridge.version}")
        print(f"Bridge Signal: {status.device.bridge.rssi} dBm")
        
        # Core information
        core = status.device.core
        print(f"Connection: {core.connection_status}")
        print(f"Power Mode: {core.power_status}")
        
        if core.power_status.value == "battery":
            print(f"Battery Level: {core.battery_level}%")
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Setting up a dev environment
We use [Poetry](https://python-poetry.org/) for dependency management and testing. Install everything with:
```bash
poetry install
```

To run the Python tests use:
```bash
poetry run pytest tests/test.py
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
