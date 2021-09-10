"""Enums for here."""

from enum import Enum


class WeatherProductType(Enum):
    """Identifies the type of report to obtain."""

    observation = "observation"
    forecast_7days = "forecast_7days"
    forecast_7days_simple = "forecast_7days_simple"
    forecast_hourly = "forecast_hourly"
    forecast_astronomy = "forecast_astronomy"
    alerts = "alerts"
    nws_alerts = "nws_alerts"

    def __str__(self):
        return "%s" % self._value_
