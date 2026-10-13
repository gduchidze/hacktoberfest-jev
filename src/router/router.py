"""The router: plain Python decides, an LLM runs only inside the chosen agent."""

from typing import Self

from pydantic import BaseModel, ConfigDict, model_validator
from typesafe_sdk import TypeSafeClient

from .handlers import clarify, handoff
from .intents import Agent, Intent
from .questions import ask
from .settings import Settings, settings


class Router(BaseModel):
    model_config = ConfigDict(frozen=True)

    agents: dict[Intent, Agent]
    settings: Settings = settings

    @model_validator(mode="after")
    def _every_intent_has_an_agent(self) -> Self:
        missing = set(Intent) - self.agents.keys()
        if missing:
            names = ", ".join(sorted(intent.value for intent in missing))
            raise ValueError(f"no agent for intents: {names}")
        return self

    def route(self, client: TypeSafeClient, msg: str) -> str:
        """Route ``msg`` to a human, a clarifying question, or an intent agent."""
        response = ask(client, msg)

        if response.nouls["wants_human"].noul > self.settings.human_threshold:
            return handoff(msg)

        intent = response.choices["intent"]
        if intent.confidence < self.settings.abstain_below:
            return clarify(msg)

        complexity = response.scores["complexity"].score
        use_frontier = complexity >= self.settings.frontier_from
        model = self.settings.frontier_model if use_frontier else self.settings.small_model
        return self.agents[Intent(intent.choice)](msg, model)  # LLM only here
