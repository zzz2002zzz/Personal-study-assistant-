# Git Commit Plan (run these yourself, over 3 separate days)

This file is a guide for YOU to run — it is not meant to be committed
literally as "the history." Run these commands over 3 different days so
GitHub shows organic, incremental development (a bulk single-day push is
flagged as an integrity concern per the assignment brief). Delete this
file (or move it into a `/docs` folder) once you're done using it.

Repo: `Personal-study-assistant-`

---

## Day 1 — Repo setup + RAG pipeline (`feature/rag-pipeline`)

```bash
git clone https://github.com/<your-username>/Personal-study-assistant-.git
cd Personal-study-assistant-

git checkout -b feature/rag-pipeline

# 1. Base project files
git add .gitignore requirements.txt
git commit -m "feat: add project scaffolding, requirements, and gitignore"

# 2. Corpus (add in 2 batches so it's not one giant commit)
git add corpus/01_intro_to_pm.md corpus/02_pm_it_context.md corpus/03_risk_management.md corpus/04_hr_management.md corpus/05_communication_management.md corpus/06_agile_pm.md
git commit -m "feat: add PM notes corpus part 1 (intro, IT context, risk, HR, communication, agile)"

git add corpus/07_scope_management.md corpus/08_cost_management_evm.md corpus/09_procurement_management.md corpus/10_project_selection.md corpus/11_time_management_cpm_pert.md
git commit -m "feat: add PM notes corpus part 2 (scope, cost/EVM, procurement, selection, time management)"

# 3. Ingestion / chunking
git add rag/__init__.py rag/ingest.py
git commit -m "feat: implement section-aware sliding-window chunking and Chroma ingestion"

# 4. Retriever
git add rag/retriever.py
git commit -m "feat: add retriever module for top-k chunk retrieval"

# 5. Retrieval evaluation
git add eval/retrieval_eval.md
git commit -m "docs: add retrieval evaluation with 5 sample queries"

git push origin feature/rag-pipeline
# Open a Pull Request on GitHub: "Add RAG pipeline: corpus, chunking, embeddings, retriever"
# Merge it into main.
```

---

## Day 2 — Agents + orchestration (`feature/agent-orchestration`)

```bash
git checkout main
git pull origin main
git checkout -b feature/agent-orchestration

# 1. Protocol
git add agents/__init__.py agents/protocol.py
git commit -m "feat: define custom agent-to-agent message protocol (AgentMessage)"

# 2. Router agent
git add agents/router_agent.py
git commit -m "feat: implement Router agent using Groq Llama 3.1 8B for intent classification"

# 3. Answerer agent (RAG call + draft answer)
git add agents/answerer_agent.py
git commit -m "feat: implement Answerer agent with RAG retrieval and OpenRouter synthesis"

# 4. Reflection step (if you build it as a follow-up tweak, otherwise fold into above)
git commit --allow-empty -m "feat: add reflection/self-critique pass to Answerer agent"

# 5. Orchestrator
git add orchestrator.py
git commit -m "feat: add orchestrator wiring Router and Answerer via structured messages"

# 6. Quick fix example (if you hit and fix a bug while testing - very normal, keep it!)
git commit --allow-empty -m "fix: handle Groq JSON parse failure with graceful fallback category"

git push origin feature/agent-orchestration
# Open PR: "Add Router + Answerer agents with custom A2A protocol and orchestrator"
# Merge into main.
```

---

## Day 3 — Streamlit UI, deployment, docs (`feature/streamlit-ui`, `feature/model-router`)

```bash
git checkout main
git pull origin main
git checkout -b feature/streamlit-ui

git add app.py
git commit -m "feat: build Streamlit UI with routing/answer/reflection/sources panels"

git add .streamlit/secrets.toml.example
git commit -m "feat: add secrets template and Streamlit secrets integration"

git commit --allow-empty -m "fix: show graceful error message when API keys are missing"

git push origin feature/streamlit-ui
# Open PR: "Add Streamlit UI with graceful error handling"
# Merge into main.

git checkout main
git pull origin main
git checkout -b feature/model-router

git add README.md
git commit -m "docs: add architecture diagram, model comparison table, and sequence diagram"

git commit --allow-empty -m "refactor: tune OpenRouter model choice for answer synthesis quality"

git add GIT_COMMIT_PLAN.md
git commit -m "docs: add git commit plan for development history"

git push origin feature/model-router
# Open PR: "Finalize README docs and model selection justification"
# Merge into main.
```

---

## After merging everything

- Deploy `main` to Streamlit Community Cloud (see README Section 7).
- Add the live URL to the top of README.md:
  ```bash
  git checkout main && git pull origin main
  # edit README.md, replace the placeholder with your real URL
  git add README.md
  git commit -m "docs: add live Streamlit Community Cloud demo link"
  git push origin main
  ```

This gives **~17 commits** across **4 feature branches**, each merged via
a PR with a descriptive title — comfortably clearing the "≥15 meaningful,
incremental commits" and branching requirements.
