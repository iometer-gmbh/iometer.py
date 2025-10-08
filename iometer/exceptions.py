"""Asynchronous Python client for IOmeter."""


class IOmeterError(Exception):
    """Generic exception."""


class IOmeterConnectionError(IOmeterError):
    """IOmeter connection exception."""


class IOmeterTimeoutError(IOmeterError):
    """IOmeter client and bridge timeout exception."""


class IOmeterNoReadingsError(IOmeterError):
    """No readings available exception."""


class IOmeterNoStatusError(IOmeterError):
    """No status available exception."""
