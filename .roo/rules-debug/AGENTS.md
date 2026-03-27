# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Debugging Notes

- **Tests hit live APIs** — failures may be network/auth issues, not code bugs. Check env vars first: `GENSHIN_COOKIES`, `HSR_COOKIES`, `HONKAI_COOKIES`, `ZZZ_COOKIES`, `CHINESE_GENSHIN_COOKIES`.
- **`prevent_enum_error`** logs a `WARNING` (not an exception) when an unknown enum value is encountered — check logs for `"Unknown <EnumClass>"` messages to detect new API values.
- **`asyncio_mode = "auto"`** in `pyproject.toml` — pytest-asyncio runs all `async def` test functions automatically; no decorator needed.
- **`nox --no-install -s test`** skips dependency reinstall — use when deps haven't changed to speed up iteration.
- **pyright excludes `**/__init__.py` and `tests/**`** — type errors in those files won't surface in `nox -s type-check`.
- **`ruff.toml` excludes `tests/` and `test.py`** — linting errors in test files are intentionally suppressed.
- **`InternationalRoute`** selects URL based on `client.region` (OVERSEAS vs CHINESE) — wrong region causes 404/auth errors, not obvious exceptions.
