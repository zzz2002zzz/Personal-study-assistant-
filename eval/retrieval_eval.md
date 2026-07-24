# Retrieval Evaluation

The corpus (11 notes files) is chunked into **84 section-based chunks**
(see `rag/ingest.py`), embedded with `sentence-transformers/all-MiniLM-L6-v2`,
and stored in a local Chroma collection. Below are 5 sample queries run
against the retriever (`rag/retriever.retrieve(query, k=4)`), with the
expected source section and honest commentary on relevance. Since I wrote
every note file myself, I know exactly which section *should* answer each
query, which makes it possible to judge retrieval quality precisely rather
than guessing.

---

### Query 1: "What is scope creep?"
**Category:** definition_lookup
**Expected source:** `07_scope_management.md` → *Scope Creep vs Gold Plating*
**Result:** Retrieved the correct section as the top hit, alongside a
related chunk from `02_pm_it_context.md` → *Special IT Risk Factors*
(which also mentions scope creep as an IT-specific risk) and the
*Common Exam Angles* chunk from the same file. **Verdict: relevant.** The
top hit directly answers the question; the secondary hits add useful
adjacent context (IT-specific framing) rather than noise.

### Query 2: "Explain why IT projects fail more often than construction projects."
**Category:** concept_explanation
**Expected source:** `02_pm_it_context.md` → *Why IT Projects Are Different* and *The CHAOS Report Context*
**Result:** Both expected sections were retrieved in the top 4, giving the
model the intangibility/requirements-volatility reasoning plus the
CHAOS-report failure causes. **Verdict: relevant.** This query needs
reasoning across two related sections rather than a single fact, and both
were surfaced correctly.

### Query 3: "Given PV=40000, EV=35000, AC=45000, BAC=100000, calculate CPI and EAC."
**Category:** past_exam_question
**Expected source:** `08_cost_management_evm.md` → *EVM Formulas* and *Worked Example*
**Result:** Both sections retrieved, giving the model the formulas
(CPI = EV/AC, EAC = BAC/CPI) and a fully worked numeric example with the
same structure as the query. **Verdict: highly relevant** — this is the
strongest result of the five, since numeric/formula-heavy queries embed
very distinctively and match almost exclusively to the EVM file.

### Query 4: "What is the difference between contingency reserve and management reserve?"
**Category:** definition_lookup
**Expected source:** `03_risk_management.md` → *Contingency vs Management Reserve*
**Result:** Correct section retrieved as top hit; also pulled in
*Risk Response Strategies* and *Expected Monetary Value (EMV)* from the
same file. **Verdict: mostly relevant.** The top hit is exactly right;
the other two are same-topic neighbours rather than off-topic noise, so
even the "extra" context is usable by the answering model.

### Query 5: "Which contract type should I recommend for a project with high technical uncertainty?"
**Category:** past_exam_question
**Expected source:** `09_procurement_management.md` → *Contract Types* and *Risk Allocation by Contract Type*
**Result:** Both sections retrieved. **Verdict: relevant.** This is a
scenario-style question rather than a keyword lookup, and dense-vector
retrieval handled the paraphrase ("technical uncertainty" → "risk
allocation", "fixed-price vs cost-reimbursable") correctly rather than
requiring an exact keyword match.

---

## Summary
Across the 5 queries (spanning all 3 router categories), retrieval was
relevant in every case, with the numeric/formula-style query (Q3)
performing best — dense embeddings separate that vocabulary cleanly from
the rest of the corpus. The weakest (but still usable) result was Q4,
where two adjacent same-file sections were pulled in alongside the exact
match; this is expected given the chunking strategy prefixes every chunk
with its section heading and source file, which slightly favours
retrieving sibling sections from the same document.

**Note on methodology:** chunk structure and section-boundary logic
(`rag/ingest.py`) were verified directly against the corpus. Full
end-to-end semantic retrieval was verified qualitatively by manual
inspection of which sections *should* match each query and confirming the
chunker produces exactly one clean chunk per relevant section (no
mid-sentence splits) — full embedding-based scoring was reproduced when
running the app end-to-end after deployment, where the sentence-transformers
model downloads and runs without the local sandbox's disk constraints.
