"""
Custom lightweight agent-to-agent (A2A) message protocol, inspired by
MCP/A2A-style structured message envelopes. Every inter-agent message is a
plain, JSON-serialisable object with a fixed schema, so:

  - Agent 1 (Router) and Agent 2 (Answerer) stay decoupled - neither one
    imports or calls the other's internals directly, they only exchange
    AgentMessage objects via the orchestrator.
  - Every exchange can be logged, inspected, or replayed for debugging
    and for the viva walkthrough (see the "Agent-to-agent message" panel
    in the Streamlit app).

Schema:
    from_agent   : str    - sender ("router" | "answerer")
    to_agent     : str    - recipient
    intent       : str    - message purpose, e.g. "route_response"
    payload      : dict   - the actual content (query, category, etc.)
    confidence   : float  - optional confidence score (router's classification confidence)
    message_id   : str    - short unique id for tracing
    timestamp    : float  - unix timestamp
"""

from dataclasses import dataclass, asdict, field
from typing import Optional
import time
import uuid


@dataclass
class AgentMessage:
    from_agent: str
    to_agent: str
    intent: str
    payload: dict
    confidence: Optional[float] = None
    message_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    timestamp: float = field(default_factory=time.time)

    def to_dict(self):
        return asdict(self)
