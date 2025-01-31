# IOmeter Bridge API Documentation

This document describes the HTTP API endpoints exposed by the IOmeter bridge.

## Base URL

The current base URL is:
```
http://{bridge-ip}/v1
```

## Endpoints

### Reading endpoint

Get the last/current meter reading including consumption and production values. Learn more on how the module handles the readings [here](reading.md).

#### Request
```http
GET /reading
```

#### Response
```json
{
  "__typename": "iometer.reading.v1",
  "meter": {
    "number": "1HLY0000000000",
    "reading": {
      "time": "2024-11-11T11:11:00Z",
      "registers": [
        {
          "obis": "01-00:01.08.00*ff",
          "value": 1234.5,
          "unit": "Wh"
        },
        {
          "obis": "01-00:02.08.00*ff",
          "value": 5432.1,
          "unit": "Wh"
        },
        {
          "obis": "01-00:10.07.00*ff",
          "value": 10,
          "unit": "W"
        }
      ]
    }
  }
}
```

#### Fields
| Field | Type | Description |
|-------|------|-------------|
| __typename | string | Type identifier for the response |
| meter.number | string | Meter number |
| meter.reading.time | string | ISO 8601 timestamp |
| meter.reading.registers | array | List of register readings |

#### Register OBIS Codes
| OBIS Code | Description | Unit |
|-----------|-------------|------|
| 01-00:01.08.00*ff | Total energy consumption | Wh |
| 01-00:02.08.00*ff | Total energy production | Wh |
| 01-00:10.07.00*ff | Current power consumption | W |

### Status endpoint

Get the current status of the bridge and core. Learn more on how the module handles the status [here](status.md).

#### Request
```http
GET /status
```

#### Response with Battery Power
```json
  {
    "__typename": "iometer.status.v1",
    "meter": {
      "number": "1ISK0000000000",
    },
    "device": {
      "bridge": {
        "rssi": -30,
        "version": "build-60"
      },
      "id": "658c2b34-2017-45f2-a12b-731235f8bb97",
      "core": {
        "connectionStatus": "connected",
        "rssi": -30,
        "version": "build-58",
        "powerStatus": "battery",
        "batteryLevel": 100,
        "attachmentStatus": "attached",
        "pinStatus": "entered"
      }
    }
  }
```

#### Response with Wired Power
```json
{
  "__typename": "iometer.status.v1",
  "meter": {
    "number": "1ISK0000000000",
  },
  "device": {
    "bridge": {
      "rssi": -15,
      "version": "build-60"
    },
    "id": "eaf4f756-1d8b-41fa-9d4f-06eff5b33dea",
    "core": {
      "connectionStatus": "connected",
      "rssi": -30,
      "version": "build-58",
      "powerStatus": "wired",
      "attachmentStatus": "attached",
      "pinStatus": "entered"
    }
  }
}
```

#### Response when Core is disconnected
```json
{
  "__typename": "iometer.status.v1",
  "meter": {
    "number": "1ISK0000000000",
  },
  "device": {
    "bridge": {
      "rssi": -15,
      "version": "build-60"
    },
    "id": "eaf4f756-1d8b-41fa-9d4f-06eff5b33dea",
    "core": {
      "connectionStatus": "disconnected"
    }
  }
}
```

#### Fields
| Field | Type | Description |
|-------|------|-------------|
| __typename | string | Type identifier for the response |
| meter.number | string | Meter number |
| device.bridge.rssi | integer? | WiFi signal strength in dBm (optional) |
| device.bridge.version | string? | Bridge firmware version (optional) |
| device.id | string | Unique device identifier |
| device.core.connectionStatus | string | Connection status ("connected", "disconnected") |
| device.core.rssi | integer? | Core/Bridge signal strength in dBm (optional) |
| device.core.version | string? | Core firmware version (optional) |
| device.core.powerStatus | string? | Power source ("battery", "wired") (optional) |
| device.core.batteryLevel | integer? | Battery percentage, only present with battery power (optional) |
| device.core.attachmentStatus | string? | Physical attachment status ("attached", "detached") (optional) |
| device.core.pinStatus | string? | PIN status ("entered", "pending", "missing") (optional) |

## Example Requests

Using curl:
```bash
# Get current reading
curl --url "http://192.168.1.100/v1/reading" \
  --header "User-Agent: curl/8.10.1" \
  --header "Accept: application/json"

# Get device status
curl --url "http://192.168.1.100/v1/status" \
  --header "User-Agent: curl/8.10.1" \
  --header "Accept: application/json"
```

## Discovery
The IOmeter bridge can be found on networks that support [mDNS](https://en.wikipedia.org/wiki/Multicast_DNS). The fully qualified service type name is `_iometer._tcp.local.`. Prominient Python modules to discover devices are for instance [python-zeroconf](https://python-zeroconf.readthedocs.io). 