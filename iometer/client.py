"""Asynchronous Python client for IOmeter."""

import asyncio
from dataclasses import dataclass
from typing import Optional, Self

from aiohttp import ClientResponseError, ClientSession
from yarl import URL

from .exceptions import IOmeterConnectionError, IOmeterTimeoutError
from .reading import Reading
from .status import Status


@dataclass
class IOmeterClient:
    """Main IOmeter client class for handling HTTP connections with the IOmeter bridge.

    Attributes:
        host: The hostname or IP address of the IOmeter bridge
        request_timeout: Number of seconds to wait for bridge response
        session: Optional aiohttp ClientSession for making requests

    Example:
        async with IOmeterClient("192.168.1.100") as client:
            reading = await client.get_current_reading()
            status = await client.get_current_status()
    """

    host: str
    request_timeout: int = 5
    session: Optional[ClientSession] = None

    async def _request(self, uri: str) -> str:
        """Make a request to the IOmeter bridge.

        Args:
            uri: The URI endpoint to request
        Returns:
            The response text from the bridge

        Raises:
            IOmeterConnectionError: If any communication error occurs
        """
        if not self.session:
            raise RuntimeError("Client session not initialized")

        url = URL.build(scheme="http", host=self.host).joinpath(uri)
        headers = {
            "User-Agent": "PythonIOmeter/0.1",
            "Accept": "application/json",
        }

        try:
            async with asyncio.timeout(self.request_timeout):
                response = await self.session.get(url, headers=headers)
                response.raise_for_status()
                return await response.text()

        except asyncio.TimeoutError as error:
            raise IOmeterTimeoutError(
                "Timeout while communicating with IOmeter bridge"
            ) from error

        except ClientResponseError as error:
            raise IOmeterConnectionError(
                f"Bridge returned error {error.status}: {error.message}"
            ) from error

        except Exception as error:
            raise IOmeterConnectionError(
                f"Error communicating with IOmeter bridge: {str(error)}"
            ) from error

    async def get_current_reading(self) -> Reading:
        """Get current reading from IOmeter bridge.

        Returns:
            Reading object containing the current meter values

        Raises:
            IOmeterConnectionError: If communication with bridge fails
        """
        response = await self._request("v1/reading")
        return Reading.from_json(response)

    async def get_current_status(self) -> Status:
        """Get device status from IOmeter bridge.

        Returns:
            Status object containing the current bridge status

        Raises:
            IOmeterConnectionError: If communication with bridge fails
        """
        response = await self._request("v1/status")
        return Status.from_json(response)

    async def close(self) -> None:
        """Close the client session."""
        if self.session:
            await self.session.close()
            self.session = None

    async def __aenter__(self) -> Self:
        """Set up the client session.

        Returns:
            The configured client instance
        """
        self.session = self.session or ClientSession()
        return self

    async def __aexit__(self, *_exc_info: object) -> None:
        """Clean up the client session."""
        await self.close()
