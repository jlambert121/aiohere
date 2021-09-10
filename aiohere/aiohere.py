"""A module to query the here web api."""
from __future__ import annotations

import asyncio
import socket
from typing import Any, Mapping, Optional

import aiohttp
import async_timeout
from yarl import URL

from aiohere.enum import WeatherProductType

from .exceptions import (
    HereError,
    HereInvalidRequestError,
    HereTimeOutError,
    HereUnauthorizedError,
)

SCHEME = "https"
API_HOST = "weather.cc.api.here.com"
API_PATH = "/weather/1.0/report.json"
API_URL = str(URL.build(scheme=SCHEME, host=API_HOST, path=API_PATH))


class AioHere:
    """Main class for handling connections with here."""

    def __init__(
        self,
        api_key: str,
        request_timeout: int = 10,
        session: aiohttp.client.ClientSession | None = None,
    ) -> None:
        """Initialize connection with here.
        Class constructor for setting up an AioHere object to
        communicate with the here API.
        Args:
            api_key: HERE API key.
            request_timeout: Max timeout to wait for a response from the API.
            session: Optional, shared, aiohttp client session.
        """
        self._session = session
        self._close_session = False

        self.api_key = api_key
        self.request_timeout = request_timeout

    async def request(
        self,
        method: str = "GET",
        data: Any | None = None,
        json_data: dict | None = None,
        params: Mapping[str, str] | None = None,
    ) -> Any:
        """Handle a request to the weenect API.
        Make a request against the weenect API and handles the response.
        Args:
            uri: The request URI on the weenect API to call.
            method: HTTP method to use for the request; e.g., GET, POST.
            data: RAW HTTP request data to send with the request.
            json_data: Dictionary of data to send as JSON with the request.
            params: Mapping of request parameters to send with the request.
        Returns:
            The response from the API. In case the response is a JSON response,
            the method will return a decoded JSON response as a Python
            dictionary.
        Raises:
            WeenectConnectionError: An error occurred while communicating
                with the weenect API (connection issues).
            WeenectHomeError: An error occurred while processing the
                response from the weenect API (invalid data).
        """

        headers = {
            "Accept": "application/json",
            "DNT": "1",
        }

        if self._session is None:
            self._session = aiohttp.ClientSession()
            self._close_session = True

        try:
            with async_timeout.timeout(self.request_timeout):
                response = await self._session.request(
                    method,
                    API_URL,
                    data=data,
                    json=json_data,
                    params=params,
                    headers=headers,
                )
        except asyncio.TimeoutError as exception:
            raise HereTimeOutError(
                "Timeout occurred while connecting to the here API."
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            raise HereError(
                "Error occurred while communicating with the here API."
            ) from exception

        content_type = response.headers.get("Content-Type", "")
        if response.status // 100 in [4, 5]:
            contents = await response.read()
            response.close()

            if content_type == "application/json":
                raise get_error_from_response(await response.json())
            raise HereError(response.status, {"message": contents.decode("utf8")})

        if response.status == 204:  # NO CONTENT
            response.close()
            return None

        if "application/json" in content_type:
            return await response.json()

    async def weather_for_coordinates(
        self,
        latitude: float,
        longitude: float,
        product: WeatherProductType,
        one_observation: bool = True,
        metric: bool = True,
    ) -> Optional[Any]:
        """Request the product for given location name.
        Args:
          latitude (float):
            Latitude.
          longitude (float):
            Longitude.
          product (WeatherProductType):
            A WeatherProductType identifying the type of report to obtain.
          one_observation (bool):
            Limit the result to the best mapped weather station.
          metric (bool):
            Use the metric system.
        Returns:
          DestinationWeatherResponse
        Raises:
          HereError
        """

        params: Mapping[str, str] = {
            "apiKey": self.api_key,
            "product": str(product),
            "oneobservation": "true" if one_observation is True else "false",
            "metric": "true" if metric is True else "false",
            "latitude": str(latitude),
            "longitude": str(longitude),
        }
        json_data = await self.request(params=params)

        if json_data.get(product_node(product)) is not None:
            return json_data

        error = get_error_from_response(json_data)
        raise error

    async def close(self) -> None:
        """Close open client session."""
        if self._session and self._close_session:
            await self._session.close()

    async def __aenter__(self) -> AioHere:
        """Async enter.
        Returns:
            The AioHere object.
        """
        return self

    async def __aexit__(self, *_exc_info) -> None:
        """Async exit.
        Args:
            _exc_info: Exec type.
        """
        await self.close()


def get_error_from_response(json_data: Mapping[str, Any]) -> HereError:
    """Return the correct error type."""
    if "error" in json_data:
        if json_data["error"] == "Unauthorized":
            return HereUnauthorizedError(json_data["error_description"])
    error_type = json_data.get("Type")
    error_message = json_data.get("Message")
    if error_type == "Invalid Request":
        return HereInvalidRequestError(error_message)
    return HereError(error_message)


def product_node(product: WeatherProductType) -> str:
    """Return the correct node name for the provided product type."""
    if product == WeatherProductType.OBSERVATION:
        return "observations"
    if product == WeatherProductType.FORECAST_7DAYS:
        return "forecasts"
    if product == WeatherProductType.FORECAST_7DAYS_SIMPLE:
        return "dailyForecasts"
    if product == WeatherProductType.FORECAST_HOURLY:
        return "hourlyForecasts"
    if product == WeatherProductType.FORECAST_ASTRONOMY:
        return "astronomy"
    if product == WeatherProductType.ALERTS:
        return "alerts"
    return "nwsAlerts"
