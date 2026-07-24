"""
Agent 1 - Router

Pattern implemented: Router pattern.
This agent's only job is to classify the incoming question into one of
three intents, then hand off to Agent 2 via a structured AgentMessage.
It deliberately does NOT retrieve or answer anything itself.

Model: Llama 3.1 8B Instant on Groq.
Why: a 3-way intent classification task is simple pattern-matching, not
deep reasoning - an 8B model at Groq's very low latency is more than
sufficient, and far cheaper/faster than routing through a large model
just to pick one of three labels. See README model-comparison table.
"""

import os
import json
from groq import Groq
from agents.protocol import AgentMessage

GROQ_MODEL = "llama-3.1-8b-instant"

CATEGORIES = ["concept_explanation", "past_exam_question", "definition_lookup"]

SYSTEM_PROMPT = f"""You are a routing classifier for a Project Management study assistant.
Classify the user's question into exactly one category from this list:
{CATEGORIES}

- "concept_explanation": the user wants a broader explanation of how/why something works
  (e.g. "explain how EVM works", "why is agile suited to IT projects").
- "past_exam_question": the user is asking a numeric/calculation/scenario-style question
  typical of an exam (e.g. "calculate CPI given...", "which contract type suits this scenario").
- "definition_lookup": the user wants a short, precise definition of a term
  (e.g. "what is scope creep", "define RACI").

Respond ONLY with a JSON object: {{"category": "<one of the categories>", "confidence": <0-1 float>}}
No preamble, no markdown fences, JSON only.
"""


def route(query: str) -> AgentMessage:
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    category, confidence = "concept_explanation", 0.0

    try:
        completion = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": query},
            ],
            temperature=0,
            max_tokens=100,
        )
        raw = completion.choices[0].message.content.strip()
        if raw.startswith("```"):
            raw = raw.strip("`").replace("json", "", 1).strip()
        parsed = json.loads(raw)
        candidate = parsed.get("category", "concept_explanation")
        confidence = float(parsed.get("confidence", 0.5))
        category = candidate if candidate in CATEGORIES else "concept_explanation"
    except Exception:
        # Graceful fallback if Groq call/parsing fails - default category,
        # zero confidence signals to the UI that routing was uncertain.
        category, confidence = "concept_explanation", 0.0

    return AgentMessage(
        from_agent="router",
        to_agent="answerer",
        intent="route_response",
        payload={"query": query, "category": category},
        confidence=confidence,
    )
