"""Router pattern.

One Jev call answers every routing question at once.
Plain Python then decides what to do with the answers; an LLM runs only at the
very end, inside the selected agent.

Layout:
    config.toml  thresholds and model names
    settings.py  loads config.toml into a validated ``Settings``
    intents.py   ``Intent`` enum and ``Agent`` signature
    questions.py the routing questions and the one SDK call
    handlers.py  hand-off / clarify outcomes
    router.py    ``Router``
"""

from .intents import Agent, Intent
from .router import Router
from .settings import Settings, settings

__all__ = ["Agent", "Intent", "Router", "Settings", "settings"]
