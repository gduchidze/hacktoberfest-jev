"""Intents the router can pick, and the agent signature they map to."""

from collections.abc import Callable
from enum import StrEnum


class Intent(StrEnum):
    SALES = "sales"
    SERVICE = "service"
    FINANCE = "finance"
    OTHER = "other"


# An agent takes ``(message, model_name)`` and returns the reply.
Agent = Callable[[str, str], str]
