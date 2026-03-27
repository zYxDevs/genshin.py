# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Project

Async API wrapper for HoYoLAB/Miyoushe APIs (Genshin Impact, Honkai Impact, Star Rail, ZZZ). Python 3.9+, asyncio, pydantic v2, aiohttp. Uses `uv` for package management and `nox` for task automation.

## Commands

```bash
nox -s test                                          # run all tests
nox -s test -- tests/client/components/test_X.py    # run single test file
nox -s test -- -k "keyword"                          # filter tests by keyword
nox -s lint                                          # ruff check
nox -s reformat                                      # black + ruff fix + sort __all__
nox -s type-check                                    # pyright (strict) + mypy
nox --no-install -s test                             # skip reinstalling deps
uv sync --all-groups --all-extras                    # install all dev deps
```

Direct ruff (per `.roo/rules-code/AGENTS.md` hook):

```bash
ruff check --fix <files> && ruff format <files>
```

## Critical Patterns

- **Models**: Always inherit from [`APIModel`](genshin/models/model.py) (pydantic v2 `BaseModel` subclass). Use [`Unique`](genshin/models/model.py) mixin for hashable models with `id`.
- **Field aliases**: Use `Aliased("api_field_name")` from [`genshin.models.model`](genshin/models/model.py) — NOT `pydantic.Field(alias=...)` directly.
- **Datetime types**: Use `TZDateTime`, `DateTime`, `UnixDateTime` from [`model.py`](genshin/models/model.py) as type annotations — they apply validators automatically.
- **Enum safety**: Use `prevent_enum_error(value, EnumClass)` when parsing unknown API enum values to avoid crashes.
- **Routes**: Use `Route` or `InternationalRoute` from [`client/routes.py`](genshin/client/routes.py) — never hardcode URLs. `InternationalRoute` handles OVERSEAS vs CHINESE region split.
- **`__all__`**: Every module must declare `__all__`. The `reformat` nox session auto-sorts it via `RUF022`.
- **`from __future__ import annotations`**: Required in all files (enables forward references, Python 3.9 compat).

## Import Style

- Import modules, not symbols: `from genshin.models.model import Aliased, APIModel` is the exception (these two are always imported directly).
- Use `typing.Optional`, `typing.Union`, `typing.Sequence` — NOT `X | Y` or `list[X]` syntax (Python 3.9 compat).
- Import `typing` as a module; use `typing.` prefix for generics.

## Code Style

- Line length: 120 (black + ruff enforced); docstring convention: numpy; pyright strict mode.
- Docstrings required for all exported symbols; `@property` methods exempt.
- `ruff.toml` excludes `tests/` and `test.py` from linting.
- `pyright` excludes `**/__init__.py` and `tests/**` from type checking.

## Testing

- Tests require real cookies via env vars: `GENSHIN_COOKIES`, `HSR_COOKIES`, `HONKAI_COOKIES`, `ZZZ_COOKIES`, `CHINESE_GENSHIN_COOKIES`.
- `asyncio_mode = "auto"` — all test functions are `async def` without explicit `@pytest.mark.asyncio`.
- Test files use a `client: genshin.Client` fixture (defined in `tests/conftest.py`); no manual client setup needed.
- Tests are integration tests hitting live APIs — they will fail without valid cookies.
