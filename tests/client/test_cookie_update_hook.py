import typing

import aiohttp
import aiohttp.test_utils
import aiohttp.web

import genshin
from genshin.client.manager import managers


async def test_update_cookies_calls_hook():
    manager = managers.CookieManager({"ltuid": "1", "ltoken": "a"})
    received: typing.List[typing.Mapping[str, str]] = []

    async def hook(cookies: typing.Mapping[str, str]) -> None:
        received.append(cookies)

    manager.on_cookie_update = hook
    await manager.update_cookies({"cookie_token": "b"})

    assert manager.cookies == {"ltuid": "1", "ltoken": "a", "cookie_token": "b"}
    assert received == [{"ltuid": "1", "ltoken": "a", "cookie_token": "b"}]
    # the hook receives a snapshot, not the live mapping
    assert received[0] is not manager.cookies


async def test_sync_hook_supported():
    manager = managers.CookieManager({"ltuid": "1"})
    received: typing.List[typing.Mapping[str, str]] = []
    manager.on_cookie_update = received.append

    await manager.update_cookies({"stuid": "1"})

    assert received == [{"ltuid": "1", "stuid": "1"}]


async def test_response_cookies_call_hook():
    async def handler(request: aiohttp.web.Request) -> aiohttp.web.Response:
        response = aiohttp.web.json_response({"retcode": 0, "data": {"ok": True}})
        response.set_cookie("e_nap_token", "fresh")
        return response

    app = aiohttp.web.Application()
    app.router.add_get("/", handler)

    received: typing.List[typing.Mapping[str, str]] = []
    manager = managers.CookieManager({"ltuid": "1"})
    manager.on_cookie_update = received.append

    async with aiohttp.test_utils.TestServer(app) as server:
        data = await manager.request(server.make_url("/"))
        assert data == {"ok": True}
        # already-known keys do not trigger another update
        await manager.request(server.make_url("/"))

    assert received == [{"ltuid": "1", "e_nap_token": "fresh"}]


async def test_client_hook_survives_set_cookies():
    def hook(cookies: typing.Mapping[str, str]) -> None: ...

    client = genshin.Client({"ltuid": "1", "ltoken": "a"}, on_cookie_update=hook)
    assert client.on_cookie_update is hook
    assert client.cookie_manager.on_cookie_update is hook

    client.set_cookies({"ltuid": "2", "ltoken": "b"})
    assert client.cookie_manager.on_cookie_update is hook

    client.on_cookie_update = None
    assert client.cookie_manager.on_cookie_update is None
