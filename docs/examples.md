# IOmeter Examples

This document provides practical examples for using the IOmeter library in different scenarios.

## Basic Usage

### Getting Current Reading

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

### Check Device Status

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
        
        if core.power_status == "battery":
            print(f"Battery Level: {core.battery_level}%")
```

## Continuous Monitoring

### Reading Monitor

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

### Health Monitor

```python
import asyncio
from iometer import IOmeterClient

async def monitor_health(interval: int = 60):
    """Monitor device health every minute."""
    async with IOmeterClient("192.168.1.100") as client:
        while True:
            try:
                status = await client.get_current_status()
                core = status.device.core
                
                health_info = {
                    "connection": core.connection_status,
                    "signal": core.rssi,
                    "power": core.power_status
                }
                
                if core.power_status == "battery":
                    health_info["battery"] = core.battery_level
                    
                print(health_info)
                await asyncio.sleep(interval)
            except Exception as e:
                print(f"Error: {e}")
                await asyncio.sleep(60)
```