"""Ratelimit handlers."""

import functools
import logging
import typing

import aiohttp
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception,
    retry_if_exception_type,
    stop_after_attempt,
    wait_random_exponential,
)

from genshin import errors

LOGGER_ = logging.getLogger(__name__)
TIMEOUT_ERRORS = (TimeoutError, aiohttp.ClientError, ConnectionResetError)
CallableT = typing.TypeVar("CallableT", bound=typing.Callable[..., typing.Awaitable[typing.Any]])


def handle_ratelimits(
    tries: int = 7,
    exception: type[errors.GenshinException] = errors.VisitsTooFrequently,
    delay: float = 0.5,
) -> typing.Callable[[CallableT], CallableT]:
    """Handle ratelimits for requests."""
    return retry(
        stop=stop_after_attempt(tries),
        wait=wait_random_exponential(multiplier=delay, min=delay),
        retry=retry_if_exception_type(exception),
        reraise=True,
        before_sleep=before_sleep_log(LOGGER_, logging.DEBUG),
    )


def handle_request_timeouts(
    tries: int = 5,
    delay: float = 0.5,
) -> typing.Callable[[CallableT], CallableT]:
    """Handle timeout errors for requests."""
    try:
        from aiohttp_socks import ProxyError
    except ImportError:
        return retry(
            stop=stop_after_attempt(tries),
            wait=wait_random_exponential(multiplier=delay, min=delay),
            retry=retry_if_exception_type(TIMEOUT_ERRORS),
            reraise=True,
            before_sleep=before_sleep_log(LOGGER_, logging.DEBUG),
        )
    else:
        # Exclude ProxyError (subclass of aiohttp.ClientError) so it is handled
        # separately by handle_proxy_errors instead of being retried with the proxy.
        return retry(
            stop=stop_after_attempt(tries),
            wait=wait_random_exponential(multiplier=delay, min=delay),
            retry=retry_if_exception(lambda e: isinstance(e, TIMEOUT_ERRORS) and not isinstance(e, ProxyError)),
            reraise=True,
            before_sleep=before_sleep_log(LOGGER_, logging.DEBUG),
        )


def handle_proxy_errors(func: CallableT) -> CallableT:
    """If a proxy error occurs, retry the request once without the proxy."""
    try:
        from aiohttp_socks import ProxyError
    except ImportError:
        return func

    @functools.wraps(func)  # type: ignore[arg-type]
    async def wrapper(self: typing.Any, *args: typing.Any, **kwargs: typing.Any) -> typing.Any:
        try:
            return await func(self, *args, **kwargs)
        except ProxyError:
            LOGGER_.warning("Proxy error encountered, retrying without proxy.")
            original_proxy = self._proxy
            original_socks_proxy = self._socks_proxy
            self._proxy = None
            self._socks_proxy = None
            try:
                return await func(self, *args, **kwargs)
            finally:
                self._proxy = original_proxy
                self._socks_proxy = original_socks_proxy

    return typing.cast(CallableT, wrapper)
