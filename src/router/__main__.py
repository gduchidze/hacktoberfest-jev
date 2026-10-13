"""Demo: ``python -m src.router`` (needs ``TYPESAFE_API_KEY`` in the environment)."""

import logging

from typesafe_sdk import TypeSafeClient

from .intents import Intent
from .router import Router
from .settings import settings


def echo_agent(msg: str, model: str) -> str:
    return f"[{model}] {msg}"


def main() -> None:
    logging.basicConfig(level=settings.log_level)
    router = Router(agents=dict.fromkeys(Intent, echo_agent))
    with TypeSafeClient() as typesafe:
        logging.info(router.route(typesafe, "What's the monthly payment on a leased SUV?"))


if __name__ == "__main__":
    main()
