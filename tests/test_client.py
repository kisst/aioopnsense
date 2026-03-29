"""Tests for the OPNsense API client."""

from unittest.mock import AsyncMock, MagicMock

import aiohttp
import pytest

from aioopnsense import (
    OPNsenseApiError,
    OPNsenseAuthError,
    OPNsenseClient,
    OPNsenseConnectionError,
)

ARP_RESPONSE = [
    {
        "hostname": "Desktop",
        "intf": "igb1",
        "intf_description": "LAN",
        "ip": "192.168.0.167",
        "mac": "ff:ff:ff:ff:ff:fe",
        "manufacturer": "OEM",
    },
]

INTERFACES_RESPONSE = {"igb0": "WAN", "igb1": "LAN"}


def _mock_session(json_data: object, status: int = 200) -> MagicMock:
    """Create a mock aiohttp session."""
    mock_resp = MagicMock()
    mock_resp.status = status
    mock_resp.json = AsyncMock(return_value=json_data)

    mock_ctx = AsyncMock()
    mock_ctx.__aenter__ = AsyncMock(return_value=mock_resp)
    mock_ctx.__aexit__ = AsyncMock(return_value=False)

    session = MagicMock(spec=aiohttp.ClientSession)
    session.get = MagicMock(return_value=mock_ctx)
    return session


async def test_get_arp() -> None:
    """Test fetching ARP table."""
    session = _mock_session(ARP_RESPONSE)
    client = OPNsenseClient(
        "https://opnsense.local/api", "key", "secret", session
    )

    result = await client.get_arp()

    assert result == ARP_RESPONSE
    session.get.assert_called_once()
    call_url = session.get.call_args[0][0]
    assert call_url == "https://opnsense.local/api/diagnostics/interface/get_arp"


async def test_get_interfaces() -> None:
    """Test fetching network interfaces."""
    session = _mock_session(INTERFACES_RESPONSE)
    client = OPNsenseClient(
        "https://opnsense.local/api", "key", "secret", session
    )

    result = await client.get_interfaces()

    assert result == INTERFACES_RESPONSE
    call_url = session.get.call_args[0][0]
    assert call_url == (
        "https://opnsense.local/api/diagnostics/networkinsight/get_interfaces"
    )


async def test_auth_error() -> None:
    """Test that 403 raises OPNsenseAuthError."""
    session = _mock_session({}, status=403)
    client = OPNsenseClient(
        "https://opnsense.local/api", "key", "secret", session
    )

    with pytest.raises(OPNsenseAuthError):
        await client.get_arp()


async def test_api_error() -> None:
    """Test that 500 raises OPNsenseApiError."""
    session = _mock_session({}, status=500)
    client = OPNsenseClient(
        "https://opnsense.local/api", "key", "secret", session
    )

    with pytest.raises(OPNsenseApiError):
        await client.get_arp()


async def test_connection_error() -> None:
    """Test that connection failure raises OPNsenseConnectionError."""
    session = MagicMock(spec=aiohttp.ClientSession)
    session.get = MagicMock(side_effect=aiohttp.ClientError())
    client = OPNsenseClient(
        "https://opnsense.local/api", "key", "secret", session
    )

    with pytest.raises(OPNsenseConnectionError):
        await client.get_arp()


async def test_timeout_error() -> None:
    """Test that timeout raises OPNsenseConnectionError."""
    session = MagicMock(spec=aiohttp.ClientSession)
    session.get = MagicMock(side_effect=TimeoutError())
    client = OPNsenseClient(
        "https://opnsense.local/api", "key", "secret", session
    )

    with pytest.raises(OPNsenseConnectionError):
        await client.get_arp()


async def test_url_trailing_slash_stripped() -> None:
    """Test that trailing slash on URL is handled."""
    session = _mock_session([])
    client = OPNsenseClient(
        "https://opnsense.local/api/", "key", "secret", session
    )

    await client.get_arp()

    call_url = session.get.call_args[0][0]
    assert call_url == "https://opnsense.local/api/diagnostics/interface/get_arp"


async def test_ssl_and_auth_passed() -> None:
    """Test that SSL and auth parameters are passed to session."""
    session = _mock_session([])
    client = OPNsenseClient(
        "https://opnsense.local/api", "mykey", "mysecret", session,
        verify_ssl=True,
    )

    await client.get_arp()

    call_kwargs = session.get.call_args[1]
    assert call_kwargs["ssl"] is True
    assert isinstance(call_kwargs["auth"], aiohttp.BasicAuth)
