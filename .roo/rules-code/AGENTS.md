# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Post-Edit Hook

After modifying any `.py` file, run:
```bash
ruff check --fix <files> && ruff format <files>
```

## Critical Coding Rules

- **`from __future__ import annotations`** must be the first import in every `.py` file.
- **`__all__`** must be declared in every module — `reformat` nox session auto-sorts it (RUF022). Add new exports manually.
- **Field aliases**: Use `Aliased("api_field_name")` from [`genshin.models.model`](genshin/models/model.py), never `pydantic.Field(alias=...)` directly.
- **Datetime fields**: Annotate with `TZDateTime`, `DateTime`, or `UnixDateTime` from [`model.py`](genshin/models/model.py) — these are `Annotated` types with validators baked in, not functions to call.
- **Enum fields**: Wrap unknown API enum values with `prevent_enum_error(value, EnumClass)` to avoid crashes on new API values.
- **Routes**: Define new endpoints as `Route("url")` or `InternationalRoute(overseas="...", chinese="...")` in [`client/routes.py`](genshin/client/routes.py). Never hardcode URLs in component methods.
- **No `X | Y` union syntax** — use `typing.Optional[X]` and `typing.Union[X, Y]` for Python 3.9 compat.
- **No `list[X]` / `dict[K, V]` generics** — use `typing.List`, `typing.Dict`, `typing.Sequence`, etc.
- **Docstrings required** for all exported symbols (numpy convention); `@property` methods are exempt.
- **`pyright` strict mode** — all code must be fully type-annotated and pass pyright without errors.
- `ruff.toml` excludes `tests/` and `test.py` — linting rules don't apply there.
