"""Enums for here."""

from enum import Enum


class WeatherProductType(Enum):
    """Identifies the type of report to obtain."""

    OBSERVATION = "observation"
    FORECAST_7DAYS = "forecast_7days"
    FORECAST_7DAYS_SIMPLE = "forecast_7days_simple"
    FORECAST_HOURLY = "forecast_hourly"
    FORECAST_ASTRONOMY = "forecast_astronomy"
    ALERTS = "alerts"
    NWS_ALERTS = "nws_alerts"

    def __str__(self):
        return "%s" % self.value
