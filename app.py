import os
import streamlit as st
from orchestrator import run_pipeline

st.set_page_config(page_title="PM Study Assistant", page_icon="📘", layout="centered")

# Pull secrets (Streamlit Cloud) into env vars so agent modules can read
# them via os.environ, without ever hardcoding a key in source.
for key in ("GROQ_API_KEY", "OPENROUTER_API_KEY"):
    if key in st.secrets:
        os.environ[key] = st.secrets[key]

st.title("📘 Project Management Study Assistant")
st.caption(
    "Grounded in my own module notes: Intro to PM, PM in the IT Context, Risk, HR, "
    "Communication, Agile, Scope, Cost Management (EVM), Procurement, Project Selection, "
    "and Time Management (Network Diagrams / CPM / PERT)."
)

missing = [k for k in ("GROQ_API_KEY", "OPENROUTER_API_KEY") if not os.environ.get(k)]
if missing:
    st.error(
        f"Missing API key(s): {', '.join(missing)}. "
        "Add them under Streamlit Cloud → App settings → Secrets "
        "(see README.md for the exact format), then reload the app."
    )
    st.stop()

with st.sidebar:
    st.subheader("How it works")
    st.markdown(
        "1. **Router agent** (Groq, Llama 3.1 8B) classifies your question.\n"
        "2. Router sends a structured JSON message to the **Answerer agent**.\n"
        "3. Answerer retrieves relevant chunks from your notes (RAG) and drafts "
        "an answer using a stronger OpenRouter model.\n"
        "4. A quick **reflection pass** checks the draft is actually grounded "
        "in the retrieved notes before it's shown to you."
    )
    st.divider()
    st.caption("Example questions to try:")
    st.code("What is scope creep?", language=None)
    st.code("Explain why IT projects fail more often than construction projects.", language=None)
    st.code("Given PV=40000, EV=35000, AC=45000, BAC=100000, calculate CPI and EAC.", language=None)

query = st.text_input(
    "Ask a Project Management question:",
    placeholder="e.g. What is the difference between contingency and management reserve?",
)

if st.button("Ask", type="primary") and query.strip():
    with st.spinner("Routing question and retrieving your notes..."):
        try:
            result = run_pipeline(query.strip())
        except Exception as e:
            st.error(
                "Something went wrong running the agent pipeline. "
                "This usually means an API key is invalid/expired or a provider is temporarily down."
            )
            st.exception(e)
            st.stop()

    category_labels = {
        "concept_explanation": "🧩 Concept Explanation",
        "past_exam_question": "📝 Past Exam Question",
        "definition_lookup": "📖 Definition Lookup",
    }
    conf = result.get("route_message", {}).get("confidence")
    conf_str = f" (confidence: {conf:.2f})" if isinstance(conf, (int, float)) else ""
    st.markdown(f"**Detected category:** {category_labels.get(result['category'], result['category'])}{conf_str}")

    st.markdown("### Answer")
    st.write(result["answer"])

    if result.get("error"):
        st.warning("Part of the pipeline hit an error - the message above is a graceful fallback response.")

    with st.expander("🔍 Retrieved note chunks (RAG context)"):
        if not result.get("sources"):
            st.write("No chunks retrieved.")
        for i, src in enumerate(result.get("sources", []), 1):
            st.markdown(f"**{i}. {src['source']} — {src['heading']}**  (distance: {src['distance']:.3f})")
            preview = src["text"][:400] + ("..." if len(src["text"]) > 400 else "")
            st.text(preview)

    with st.expander("🔁 Reflection / self-critique (Agent 2's second pass)"):
        st.json(result.get("reflection") or {})

    with st.expander("📨 Agent-to-agent message (Router → Answerer)"):
        st.json(result.get("route_message", {}))

st.divider()
st.caption(
    "Router + reflection: Groq (Llama 3.1 8B Instant) · "
    "Answer synthesis: OpenRouter (Llama 3.3 70B Instruct) · "
    "Retrieval: local Chroma + sentence-transformers embeddings."
)
