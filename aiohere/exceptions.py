"""Exceptions for aiohere."""


class HereError(Exception):
    """Generic aiohere exception."""


class HereTimeOutError(HereError):
    """Timeout while calling the API."""


class HereUnauthorizedError(HereError):
    """Invalid or missing api key."""


class HereInvalidRequestError(HereError):
    """Invalid request."""
