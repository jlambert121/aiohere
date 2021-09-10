# aiohere

Asynchronous Python client for the HERE API

Based on [herepy](https://github.com/abdullahselek/HerePy)

[![GitHub Actions](https://github.com/eifinger/aiohere/workflows/CI/badge.svg)](https://github.com/eifinger/aiohere/actions?workflow=CI)
[![PyPi](https://img.shields.io/pypi/v/aiohere.svg)](https://pypi.python.org/pypi/aiohere)
[![PyPi](https://img.shields.io/pypi/l/aiohere.svg)](https://github.com/eifinger/aiohere/blob/master/LICENSE)
[![codecov](https://codecov.io/gh/eifinger/aiohere/branch/master/graph/badge.svg)](https://codecov.io/gh/eifinger/aiohere)
[![Downloads](https://pepy.tech/badge/aiohere)](https://pepy.tech/project/aiohere)

## Installation

```bash
$ pip install aiohere
```

## Usage

```python
from aiohere import AioHere, WeatherProductType

import asyncio

API_KEY = ""

async def main():
    """Show example how to get weather forecast for your location."""
    async with AioHere(api_key=API_KEY) as aiohere:
        response = await aiohere.weather_for_coordinates(
            latitude=49.9836187,
            longitude=8.2329145,
            product=WeatherProductType.forecast_7days_simple,
        )
        lowTemperature = response["dailyForecasts"]["forecastLocation"]["forecast"][0]["lowTemperature"]
        highTemperature = response["dailyForecasts"]["forecastLocation"]["forecast"][0]["highTemperature"]
        weekday = response["dailyForecasts"]["forecastLocation"]["forecast"][0]["weekday"]

        print(f"Temperature on {weekday} will be between {lowTemperature}°C and {highTemperature}°C")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
```

<a href="https://www.buymeacoffee.com/eifinger" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/black_img.png" alt="Buy Me A Coffee" style="height: auto !important;width: auto !important;" ></a><br>