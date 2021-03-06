from typing import Callable

import pytest

import hypercorn.utils
from _pytest.monkeypatch import MonkeyPatch
from hypercorn.typing import ASGIFramework


@pytest.mark.parametrize(
    "method, status, expected", [("HEAD", 200, True), ("GET", 200, False), ("GET", 101, True)]
)
def test_suppress_body(method: str, status: int, expected: bool) -> None:
    assert hypercorn.utils.suppress_body(method, status) is expected


def test_response_headers(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr(hypercorn.utils, "time", lambda: 1_512_229_395)
    assert hypercorn.utils.response_headers("test") == [
        (b"date", b"Sat, 02 Dec 2017 15:43:15 GMT"),
        (b"server", b"hypercorn-test"),
    ]


@pytest.mark.asyncio
async def test_invoke_asgi_3() -> None:
    result: dict = {}

    async def asgi3_callable(scope: dict, receive: Callable, send: Callable) -> None:
        nonlocal result
        result = scope

    await hypercorn.utils.invoke_asgi(asgi3_callable, {"asgi": {}}, None, None)
    assert result["asgi"]["version"] == "3.0"


@pytest.mark.asyncio
async def test_invoke_asgi_2() -> None:
    result: dict = {}

    def asgi2_callable(scope: dict) -> Callable:
        nonlocal result
        result = scope

        async def inner(receive: Callable, send: Callable) -> None:
            pass

        return inner

    await hypercorn.utils.invoke_asgi(asgi2_callable, {"asgi": {}}, None, None)  # type: ignore
    assert result["asgi"]["version"] == "2.0"


class ASGI2Class:
    def __init__(self, scope: dict) -> None:
        pass

    async def __call__(self, receive: Callable, send: Callable) -> None:
        pass


class ASGI3ClassInstance:
    def __init__(self) -> None:
        pass

    async def __call__(self, scope: dict, receive: Callable, send: Callable) -> None:
        pass


def asgi2_callable(scope: dict) -> Callable:
    async def inner(receive: Callable, send: Callable) -> None:
        pass

    return inner


async def asgi3_callable(scope: dict, receive: Callable, send: Callable) -> None:
    pass


@pytest.mark.parametrize(
    "app, is_asgi_2",
    [
        (ASGI2Class, True),
        (ASGI3ClassInstance(), False),
        (asgi2_callable, True),
        (asgi3_callable, False),
    ],
)
def test__is_asgi_2(app: ASGIFramework, is_asgi_2: bool) -> None:
    assert hypercorn.utils._is_asgi_2(app) == is_asgi_2
