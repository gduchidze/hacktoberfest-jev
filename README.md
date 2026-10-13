# hacktoberfest-jev

A small Python playground for building type-safe AI apps with LangChain, Pydantic AI, Gemini and the TypeSafe AI SDK.

## Setup

You need Python 3.11+ and [uv](https://docs.astral.sh/uv/).

```bash
uv venv venv --python 3.12
source venv/bin/activate
uv sync --active
```

Use `--active` so uv installs into `venv/` instead of creating `.venv`.

## What's inside

- `langchain` for chains and agents
- `langchain-google-genai` for Gemini models
- `pydantic-ai` for typed agents
- `typesafe-sdk` for the TypeSafe AI API

All versions are pinned in `pyproject.toml`.

## Checks

```bash
ruff check .
mypy .
pytest
```

## License

See [LICENSE](LICENSE).
