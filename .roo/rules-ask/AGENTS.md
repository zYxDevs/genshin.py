# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Documentation Context

- **`Client`** in [`genshin/client/clients.py`](genshin/client/clients.py) is assembled via multiple inheritance of component classes — each component in [`client/components/`](genshin/client/components/) handles a distinct API surface area.
- **`genshin/models/model.py`](genshin/models/model.py)** is the single source of truth for `APIModel`, `Aliased`, `Unique`, `TZDateTime`, `DateTime`, `UnixDateTime`, `LevelField`, and `prevent_enum_error` — all model utilities live here.
- **`InternationalRoute`** (in [`client/routes.py`](genshin/client/routes.py)) is not exported in `__all__` but is used throughout components — it selects between OVERSEAS and CHINESE API base URLs at call time.
- **`tests/`** are integration tests only — there are no unit tests. All tests require live API cookies.
- **`genshin/utility/`** contains helpers: `ds.py` (dynamic secret generation for API auth), `uid.py` (UID→server mapping), `concurrency.py`, `deprecation.py`, `logfile.py`, `fs.py`, `extdb.py`.
- **`nox -s reformat`** does three things in sequence: black format → ruff RUF022+I fix (sort `__all__` + imports) → ruff fix (all fixable lint). Running just `ruff format` is not equivalent.
