# aioopnsense

[![CI](https://github.com/kisst/aioopnsense/actions/workflows/ci.yml/badge.svg)](https://github.com/kisst/aioopnsense/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/aioopnsense)](https://pypi.org/project/aioopnsense/)
[![Python](https://img.shields.io/pypi/pyversions/aioopnsense)](https://pypi.org/project/aioopnsense/)
[![License](https://img.shields.io/github/license/kisst/aioopnsense)](https://github.com/kisst/aioopnsense/blob/main/LICENSE)

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
