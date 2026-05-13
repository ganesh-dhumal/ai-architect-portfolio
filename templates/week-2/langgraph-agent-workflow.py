"""LangGraph multi-step agent workflow starter."""

from __future__ import annotations

from typing import TypedDict

from langgraph.graph import END, StateGraph


class AgentState(TypedDict):
    query: str
    retrieved_context: str
    generated_response: str


async def retrieve_context(state: AgentState) -> AgentState:
    """Retrieve contextual information."""

    state["retrieved_context"] = (
        "Retrieved semantic context for: "
        f"{state['query']}"
    )

    return state


async def generate_response(state: AgentState) -> AgentState:
    """Generate AI response."""

    state["generated_response"] = (
        f"AI Response using context: {state['retrieved_context']}"
    )

    return state


def build_workflow():
    """Construct LangGraph workflow."""

    workflow = StateGraph(AgentState)

    workflow.add_node("retrieve_context", retrieve_context)
    workflow.add_node("generate_response", generate_response)

    workflow.set_entry_point("retrieve_context")

    workflow.add_edge("retrieve_context", "generate_response")
    workflow.add_edge("generate_response", END)

    return workflow.compile()


if __name__ == "__main__":
    graph = build_workflow()

    result = graph.invoke(
        {
            "query": "Explain agentic RAG",
            "retrieved_context": "",
            "generated_response": "",
        }
    )

    print(result)
