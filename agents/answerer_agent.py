"""
Agent 2 - Answerer

Patterns implemented in this file:
  - RAG (retrieval-augmented generation): retrieve() is called as an
    explicit tool before any generation happens - the model never answers
    from parametric memory alone.
  - Tool-use / ReAct-style step: retrieval is treated as a discrete tool
    call whose output is fed into the reasoning step, rather than being
    baked into a single end-to-end prompt.
  - Reflection / self-critique: after drafting an answer, a second pass
    (_reflect) checks whether the draft is actually grounded in the
    retrieved chunks and appends a caveat if not, instead of silently
    returning an ungrounded answer.

Models:
  - Draft answer -> OpenRouter, meta-llama/llama-3.3-70b-instruct
    (stronger reasoning/synthesis model - justified in README table).
  - Reflection check -> Groq llama-3.1-8b-instant (same cheap model used
    for routing - a grounded/ungrounded judgement is a simple
    classification task and doesn't need frontier reasoning).
"""

import os
import json
import requests
from groq import Groq
from rag.retriever import retrieve
from agents.protocol import AgentMessage

OPENROUTER_MODEL = "meta-llama/llama-3.3-70b-instruct"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
GROQ_REFLECT_MODEL = "llama-3.1-8b-instant"

CATEGORY_INSTRUCTIONS = {
    "concept_explanation": "Give a clear, structured explanation with the reasoning behind it, in 3-6 sentences or short bullet points.",
    "past_exam_question": "Show any relevant formula and a worked calculation/step-by-step reasoning, exam-answer style.",
    "definition_lookup": "Give a short, precise definition (1-3 sentences), no filler.",
}


def _call_openrouter(system_prompt: str, user_prompt: str) -> str:
    api_key = os.environ.get("OPENROUTER_API_KEY")
    resp = requests.post(
        OPENROUTER_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENROUTER_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.2,
            "max_tokens": 500,
        },
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    return data["choices"][0]["message"]["content"].strip()


def _reflect(query: str, context: str, draft_answer: str) -> dict:
    """Cheap Groq pass: is the draft answer actually grounded in context?"""
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    system = (
        "You check whether an answer is supported by the given context. "
        'Respond ONLY with JSON: {"grounded": true or false, "note": "<short reason>"}'
    )
    user = f"CONTEXT:\n{context}\n\nQUESTION:\n{query}\n\nDRAFT ANSWER:\n{draft_answer}"
    try:
        completion = client.chat.completions.create(
            model=GROQ_REFLECT_MODEL,
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
            temperature=0,
            max_tokens=100,
        )
        raw = completion.choices[0].message.content.strip().strip("`")
        if raw.lower().startswith("json"):
            raw = raw[4:].strip()
        return json.loads(raw)
    except Exception:
        return {"grounded": True, "note": "reflection check unavailable, defaulting to accept"}


def answer(message: AgentMessage) -> dict:
    query = message.payload["query"]
    category = message.payload["category"]

    try:
        retrieved = retrieve(query, k=4)
    except Exception as e:
        return {
            "answer": "Sorry, I couldn't reach the notes database right now. Please try again shortly.",
            "category": category,
            "sources": [],
            "reflection": None,
            "error": str(e),
        }

    context = "\n\n".join(f"({r['source']} - {r['heading']}): {r['text']}" for r in retrieved)
    instruction = CATEGORY_INSTRUCTIONS.get(category, CATEGORY_INSTRUCTIONS["concept_explanation"])

    system_prompt = (
        "You are a Project Management study assistant. Answer strictly using the "
        "provided context from the student's own module notes. If the context "
        "does not contain the answer, say so honestly rather than guessing. "
        f"{instruction}"
    )
    user_prompt = f"CONTEXT FROM NOTES:\n{context}\n\nQUESTION: {query}"

    try:
        draft = _call_openrouter(system_prompt, user_prompt)
    except Exception as e:
        return {
            "answer": "Sorry, the answering model is currently unavailable. Please try again shortly.",
            "category": category,
            "sources": retrieved,
            "reflection": None,
            "error": str(e),
        }

    reflection = _reflect(query, context, draft)
    final_answer = draft
    if not reflection.get("grounded", True):
        final_answer += (
            "\n\n_Note: parts of this answer may go beyond what's directly in your notes "
            f"({reflection.get('note', '')}). Please verify against the source material._"
        )

    return {
        "answer": final_answer,
        "category": category,
        "sources": retrieved,
        "reflection": reflection,
    }
