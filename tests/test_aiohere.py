"""Tests for `aioweenect.aioweenect`."""
from aiohere.enum import WeatherProductType
from aiohere.aiohere import API_HOST, API_PATH
import json
import os

import aiohttp
import pytest

from aiohere import AioHere


@pytest.mark.asyncio
async def test_get_weather(aresponses):
    """Test getting weather information."""
    aresponses.add(
        API_HOST,
        API_PATH,
        "GET",
        response=load_json_fixture("daily_simple_forecasts.json"),
    )
    async with aiohttp.ClientSession() as session:
        aiohere = AioHere(api_key="password", session=session)
        response = await aiohere.weather_for_coordinates(
            latitude=0.0,
            longitude=0.0,
            product=WeatherProductType.FORECAST_7DAYS_SIMPLE,
        )

        assert (
            response["dailyForecasts"]["forecastLocation"]["forecast"][0][
                "highTemperature"
            ]
            == "4.00"
        )


def load_json_fixture(filename):
    """Load a fixture."""
    path = os.path.join(os.path.dirname(__file__), "fixtures", filename)
    with open(path, encoding="utf-8") as fptr:
        content = fptr.read()
        json_content = json.loads(content)
        return json_content
