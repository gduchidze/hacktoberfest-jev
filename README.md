# Jev patterns

Small, practical patterns for building with Jev.

One Jev call answers many questions at once. Plain Python decides what to do next.
An LLM runs only when it has to.

## Install

You need Python 3.11+ and [uv](https://docs.astral.sh/uv/).

```bash
uv venv venv --python 3.12
source venv/bin/activate
uv sync --active
```

Add your key to a `.env` file:

```bash
TYPESAFE_API_KEY=your-key
```

## Patterns

### Router

Reads a message and picks the path:

- Wants a person? Hand off.
- Not sure what they mean? Ask back.
- Otherwise? Send to the right agent, on a small or big model.

```bash
python -m src.router
```

Tweak thresholds in `src/router/config.toml`.

## License

See [LICENSE](LICENSE).
