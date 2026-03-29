# aioopnsense

Async Python client for the OPNsense API, compatible with OPNsense 25.7+.

Uses the snake_case API endpoints introduced in OPNsense 25.7.

## Installation

```bash
pip install aioopnsense
```

## Usage

```python
import aiohttp
from aioopnsense import OPNsenseClient

async with aiohttp.ClientSession() as session:
    client = OPNsenseClient(
        url="https://opnsense.local/api",
        api_key="your_api_key",
        api_secret="your_api_secret",
        session=session,
    )

    # Get ARP table
    arp_table = await client.get_arp()

    # Get network interfaces
    interfaces = await client.get_interfaces()
```

## Supported Endpoints

- `GET /api/diagnostics/interface/get_arp` - ARP table
- `GET /api/diagnostics/networkinsight/get_interfaces` - Network interfaces

## License

Apache-2.0
