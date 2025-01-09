# IOmeter Python Library

A Python client for polling IOmeter devices over HTTP. This client provides an async interface for reading energy consumption/production data and monitoring device status.

## Features

- 🔌 Asynchronous communication with IOmeter device over HTTP
- 📊 Read energy consumption and production data
- 🔋 Monitor device status including battery levels and signal strength etc.

Refer to the [HTTP API](api.md) documentation for further information on how to interact with your IOmeter bridge in your local network.

## Quick Start

### Installation

```bash
pip install iometer
```

### Basic Usage

```python
import asyncio
from iometer import IOmeterClient

async def main():
    async with IOmeterClient("192.168.1.100") as client:
        # Get current reading
        reading = await client.get_current_reading()
        print(f"Total consumption: {reading.get_total_consumption()} Wh")
        print(f"Total production: {reading.get_total_production()} Wh")

        # Get device status
        status = await client.get_current_status()
        print(f"Signal strength: {status.device.bridge.rssi} dBm")
        
        if status.device.core.power_status == "battery":
            print(f"Battery level: {status.device.core.battery_level}%")

if __name__ == "__main__":
    asyncio.run(main())
```

## Requirements

- Python 3.12 or higher, not tested on lower versions
- aiohttp
- yarl

## Next Steps

- Check out the [Examples](examples.md) for more usage scenarios
- Learn about the [Status](status.md) for device status monitoring
- Explore the [Reading](reading.md) for energy data collection