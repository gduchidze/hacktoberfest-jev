"""Routing questions, answered together in one ``system_one`` call."""

from typesafe_sdk import Choice, Noul, Questions, Score, SystemOneResponse, TypeSafeClient

from .intents import Intent

ROUTER: Questions = {
    "intent": Choice(
        instructions="What does the customer want right now?",
        criteria={
            Intent.SALES: "Buying, pricing, test drive, trade-in",
            Intent.SERVICE: "Repair, maintenance, booking a service slot",
            Intent.FINANCE: "Loans, leasing, monthly payments",
            Intent.OTHER: "None of the above",
        },
    ),
    "complexity": Score(
        instructions="How much reasoning does answering this require?",
        criteria=[
            "Lookup or single fact",
            "A few steps, one domain",
            "Multi-step, needs planning across domains",
        ],
    ),
    "wants_human": Noul(instructions="Is the customer asking for a human?"),
}


def ask(client: TypeSafeClient, msg: str) -> SystemOneResponse:
    return client.system_one(state=msg, questions=ROUTER)  # pyright: ignore[reportUnknownMemberType]
