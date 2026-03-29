"""Async client for the OPNsense API."""

from __future__ import annotations

from typing import Any

import aiohttp

from .exceptions import OPNsenseApiError, OPNsenseAuthError, OPNsenseConnectionError

DEFAULT_TIMEOUT = aiohttp.ClientTimeout(total=20)


class OPNsenseClient:
    """Async client for the OPNsense API.

    Uses the snake_case API endpoints introduced in OPNsense 25.7.
    """

    def __init__(
        self,
        url: str,
        api_key: str,
        api_secret: str,
        session: aiohttp.ClientSession,
        verify_ssl: bool = False,
        timeout: aiohttp.ClientTimeout | None = None,
    ) -> None:
        """Initialize the OPNsense client.

        Args:
            url: Base URL of the OPNsense API (e.g. https://opnsense.local/api).
            api_key: API key for authentication.
            api_secret: API secret for authentication.
            session: aiohttp client session to use for requests.
            verify_ssl: Whether to verify SSL certificates.
            timeout: Request timeout. Defaults to 20 seconds.

        """
        self._url = url.rstrip("/")
        self._auth = aiohttp.BasicAuth(api_key, api_secret)
        self._session = session
        self._verify_ssl = verify_ssl
        self._timeout = timeout or DEFAULT_TIMEOUT

    async def get_arp(self) -> list[dict[str, Any]]:
        """Get the ARP table from OPNsense.

        Returns a list of ARP entries, each containing keys like:
        mac, ip, hostname, intf, intf_description, manufacturer.
        """
        result: list[dict[str, Any]] = await self._get("diagnostics/interface/get_arp")
        return result

    async def get_interfaces(self) -> dict[str, str]:
        """Get available network interfaces from OPNsense.

        Returns a dict mapping interface identifiers to descriptions,
        e.g. {"igb0": "WAN", "igb1": "LAN"}.
        """
        result: dict[str, str] = await self._get(
            "diagnostics/networkinsight/get_interfaces"
        )
        return result

    async def _get(self, endpoint: str) -> Any:
        """Make a GET request to the OPNsense API.

        Args:
            endpoint: API endpoint path (without leading slash).

        Returns:
            Parsed JSON response.

        Raises:
            OPNsenseAuthError: If authentication fails (401/403).
            OPNsenseConnectionError: If the connection fails.
            OPNsenseApiError: For other API errors.

        """
        url = f"{self._url}/{endpoint}"
        try:
            async with self._session.get(
                url,
                auth=self._auth,
                ssl=self._verify_ssl,
                timeout=self._timeout,
            ) as resp:
                if resp.status in (401, 403):
                    raise OPNsenseAuthError(f"Authentication failed: {resp.status}")
                if resp.status != 200:
                    raise OPNsenseApiError(f"API request failed: {resp.status}")
                return await resp.json()
        except OPNsenseApiError:
            raise
        except aiohttp.ClientError as err:
            raise OPNsenseConnectionError(
                f"Failed to connect to OPNsense at {url}"
            ) from err
        except TimeoutError as err:
            raise OPNsenseConnectionError(
                f"Timeout connecting to OPNsense at {url}"
            ) from err
