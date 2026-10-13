# hacktoberfest-jev

A small Python playground for building type-safe AI apps with LangChain, Pydantic AI, Gemini and the TypeSafe AI SDK.

## Setup

You need Python 3.11+ and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
source .venv/bin/activate
```

## What's inside

- `langchain` for chains and agents
- `langchain-google-genai` for Gemini models
- `pydantic-ai` for typed agents
- `typesafe-sdk` for the TypeSafe AI API

All versions are pinned in `pyproject.toml`.

## Checks

```bash
uv run ruff check .
uv run mypy .
uv run pytest
```

## License

See [LICENSE](LICENSE).
