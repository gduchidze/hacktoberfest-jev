"""The router: plain Python decides, an LLM runs only inside the chosen agent."""

import logging
from typing import Self

from pydantic import BaseModel, ConfigDict, model_validator
from typesafe_sdk import TypeSafeClient

from .handlers import clarify, handoff
from .intents import Agent, Intent
from .questions import ask
from .settings import Settings, settings

logger = logging.getLogger(__name__)


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
        cfg = self.settings
        logger.info("1. ask   | one system_one call, 3 questions | msg=%r", msg)
        response = ask(client, msg)

        wants_human = response.nouls["wants_human"].noul
        logger.info(
            "2. human | P(wants_human)=%.2f vs threshold %.2f -> %s",
            wants_human,
            cfg.human_threshold,
            "HAND OFF" if wants_human > cfg.human_threshold else "continue",
        )
        if wants_human > cfg.human_threshold:
            return handoff(msg)

        intent = response.choices["intent"]
        logger.info(
            "3. intent| %s (confidence=%.2f) vs abstain_below %.2f -> %s",
            intent.choice,
            intent.confidence,
            cfg.abstain_below,
            "CLARIFY" if intent.confidence < cfg.abstain_below else "continue",
        )
        if intent.confidence < cfg.abstain_below:
            return clarify(msg)

        complexity = response.scores["complexity"].score
        use_frontier = complexity >= cfg.frontier_from
        model = cfg.frontier_model if use_frontier else cfg.small_model
        logger.info(
            "4. model | complexity=%.2f vs frontier_from %.2f -> %s",
            complexity,
            cfg.frontier_from,
            model,
        )

        logger.info("5. agent | %s agent runs with model=%s (LLM only here)", intent.choice, model)
        return self.agents[Intent(intent.choice)](msg, model)
