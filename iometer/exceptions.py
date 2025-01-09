"""Asynchronous Python client for IOmeter."""


class IOmeterError(Exception):
    """Generic exception."""


class IOmeterConnectionError(IOmeterError):
    """IOmeter connection exception."""


class IOmeterTimeoutError(IOmeterError):
    """IOmeter client and bridge timeout exception"""


class IOmeterParseError(IOmeterError):
    """IOmeter parse exception."""
