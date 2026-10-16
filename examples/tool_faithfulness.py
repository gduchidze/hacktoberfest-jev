from deepeval.metrics.jev_eval import Choice, Noul, Score
from deepeval.test_case import LLMTestCase, SingleTurnParams, ToolCall
from deepeval.metrics import JevEval
from deepeval import evaluate

tool_faithfulness = JevEval(
    name="Tool Faithfulness",
    evaluation_params=[
        SingleTurnParams.INPUT,
        SingleTurnParams.ACTUAL_OUTPUT,
        SingleTurnParams.TOOLS_CALLED,
    ],
    questions=[
        Noul(
            "Every fact and figure in actual_output appears in the output "
            "of a tool in tools_called.",
            weight=2,
        ),
        Noul(
            "actual_output reports every value returned in tools_called accurately."
        ),
        Score(
            "How much of actual_output is grounded in tools_called?",
            levels=[
                "Fabricated",
                "Mostly fabricated",
                "Mostly grounded",
                "Fully grounded",
            ],
        ),
        Choice(
            "What did actual_output do with information the tools did not return?",
            options={
                "left_it_out": 1.0,
                "flagged_it_as_unknown": 1.0,
                "hedged_it": 0.5,
                "stated_it_as_fact": 0.0,
                "nothing_missing": None,
            },
        ),
    ],
    include_reason=False,
)

test_case = LLMTestCase(
    input="What's the weather in Paris right now?",
    actual_output=(
        "It's 18°C and sunny in Paris, with a light breeze "
        "and around 40% humidity."
    ),
    tools_called=[
        ToolCall(
            name="get_weather",
            input_parameters={"city": "Paris"},
            output={"temp_c": 18, "condition": "sunny"},
        )
    ],
)

evaluate(test_cases=[test_case], metrics=[tool_faithfulness])
