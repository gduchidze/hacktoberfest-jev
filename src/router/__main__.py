"""Run: ``python -m src.router`` ."""

import logging

from dotenv import load_dotenv
from typesafe_sdk import TypeSafeClient

from .intents import Intent
from .router import Router
from .settings import settings


def echo_agent(msg: str, model: str) -> str:
    return f"[{model}] {msg}"


def main() -> None:
    load_dotenv()
    logging.basicConfig(level=settings.log_level)
    router = Router(agents=dict.fromkeys(Intent, echo_agent))
    with TypeSafeClient() as typesafe:
        reply = router.route(typesafe, "What's the monthly payment on a leased SUV?")
        logging.info("6. reply | %s", reply)


if __name__ == "__main__":
    main()
