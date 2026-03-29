"""Exceptions for the OPNsense API client."""


class OPNsenseApiError(Exception):
    """Base exception for OPNsense API errors."""


class OPNsenseConnectionError(OPNsenseApiError):
    """Raised when a connection to OPNsense fails."""


class OPNsenseAuthError(OPNsenseApiError):
    """Raised when authentication to OPNsense fails."""
