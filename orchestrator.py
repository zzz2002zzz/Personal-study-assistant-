"""
Orchestrator-worker pattern.

This module is the thin orchestrator that wires Agent 1 (router) and
Agent 2 (answerer) together. It is the ONLY place that calls both agents;
neither agent ever imports or calls the other directly. All communication
between them is a structured AgentMessage (see agents/protocol.py), which
keeps the two agents independently testable and replaceable, and gives us
a clean object to display in the UI for the "Agent-to-agent message" panel.

Sequence (see README.md for the rendered diagram):
    User -> Streamlit UI -> orchestrator.run_pipeline(query)
          -> Agent 1 (router.route)      [Groq, cheap model]
          -> AgentMessage(router -> answerer)
          -> Agent 2 (answerer.answer)   [RAG + OpenRouter model + reflection]
          -> result dict -> Streamlit UI -> User
"""

from agents.router_agent import route
from agents.answerer_agent import answer


def run_pipeline(query: str) -> dict:
    route_message = route(query)
    result = answer(route_message)
    result["route_message"] = route_message.to_dict()
    return result
