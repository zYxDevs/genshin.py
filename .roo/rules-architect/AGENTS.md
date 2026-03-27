# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Architectural Constraints

- **`Client` is assembled via multiple inheritance** — [`genshin/client/clients.py`](genshin/client/clients.py) composes all component classes. New feature areas must be implemented as a separate component class in [`client/components/`](genshin/client/components/) and mixed in there.
- **`BaseClient`** in [`client/components/base.py`](genshin/client/components/base.py) owns all HTTP, cookie, region, and language state. Components must not duplicate this state.
- **Region split is structural** — `InternationalRoute(overseas="...", chinese="...")` in [`client/routes.py`](genshin/client/routes.py) is the only sanctioned way to handle OVERSEAS vs CHINESE API differences. Adding `if region == CHINESE` branches in component methods is an anti-pattern.
- **`APIModel` is pydantic v2** — `model_config` uses `ConfigDict`. Validators use `@pydantic.field_validator` with `mode="before"` or `mode="after"`. Do not use pydantic v1 patterns (`@validator`, `class Config`).
- **`Aliased()` wraps `pydantic.Field(alias=...)`** — it exists to enforce a single import point and consistent alias declaration. Never bypass it.
- **`prevent_enum_error`** is the crash-safety layer for API enum fields — omitting it means new API values will raise `ValueError` in production.
- **`genshin/utility/ds.py`** generates dynamic secrets required for certain API endpoints — this is not optional middleware; endpoints that need it will silently fail or return auth errors without it.
- **`__all__` in every module** is enforced by `RUF022` lint rule and auto-sorted by `nox -s reformat`. New public symbols must be added manually before reformat runs.
- **pyright strict mode** is enforced project-wide (excluding `__init__.py` and `tests/`). Architectural changes must maintain full type coverage.
