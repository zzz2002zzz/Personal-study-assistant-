# Project Selection Methods

## Why Project Selection Matters
Organizations typically have more potential projects than resources to execute them. Project selection methods provide an objective (or semi-objective) basis for choosing which projects to fund, comparing financial return, strategic fit, and risk.

## Net Present Value (NPV)
NPV discounts future cash flows to today's value using a required rate of return (discount rate), then subtracts the initial investment.

**Formula:** NPV = Σ [CFt / (1 + r)^t] − Initial Investment

Where CFt = cash flow in year t, r = discount rate, t = year number.

**Decision rule**: Accept a project if NPV > 0 (it adds value beyond the required rate of return). When comparing mutually exclusive projects, prefer the one with the **higher NPV**.

**Worked example**: Initial investment = $100,000. Expected cash flows: Year 1 = $40,000, Year 2 = $40,000, Year 3 = $40,000. Discount rate = 10%.
NPV = 40,000/1.1 + 40,000/1.1² + 40,000/1.1³ − 100,000
= 36,364 + 33,058 + 30,053 − 100,000 ≈ **−$525** (slightly negative — marginally reject at this discount rate).

## Return on Investment (ROI)
ROI = (Total discounted benefits − Total discounted costs) / Total discounted costs, expressed as a percentage.
Higher ROI is preferred. ROI is useful for comparing projects of different sizes proportionally, though it doesn't show absolute value like NPV does.

## Payback Period
The length of time required to recover the initial investment from net cash inflows.

**Formula (simple, even cash flows)**: Payback Period = Initial Investment / Annual Cash Inflow

**Worked example**: Initial investment = $90,000, even annual cash inflow = $30,000/year → Payback Period = 90,000/30,000 = **3 years**.

For uneven cash flows, subtract each year's cash flow cumulatively from the initial investment until the remaining balance reaches zero.

**Limitation**: Payback period ignores the time value of money and ignores cash flows after the payback point — it's a liquidity/risk measure, not a profitability measure. Organizations often prefer projects with **shorter** payback periods, especially under capital constraints.

## Internal Rate of Return (IRR)
The discount rate at which NPV = 0. A project is acceptable if IRR exceeds the organization's required rate of return (hurdle rate/cost of capital). Higher IRR is generally preferred when comparing projects, though IRR can be misleading with non-conventional cash flows (multiple sign changes).

## Weighted Scoring Model
A technique for comparing projects against multiple criteria (which may include non-financial, strategic factors) using assigned weights.

**Method:**
1. Identify criteria relevant to the decision (e.g. strategic fit, cost, risk, time to market, customer impact).
2. Assign a weight to each criterion (weights sum to 100% or 1.0).
3. Score each project against each criterion (e.g. 1–10 scale).
4. Multiply each score by its weight and sum for a total weighted score per project.
5. Select the project(s) with the highest weighted score.

**Worked example:**
| Criterion | Weight | Project A Score | Project B Score |
|---|---|---|---|
| Strategic Fit | 0.4 | 8 | 6 |
| Cost Efficiency | 0.3 | 5 | 9 |
| Risk Level | 0.3 | 7 | 6 |

Project A weighted score = 0.4(8) + 0.3(5) + 0.3(7) = 3.2 + 1.5 + 2.1 = **6.8**
Project B weighted score = 0.4(6) + 0.3(9) + 0.3(6) = 2.4 + 2.7 + 1.8 = **6.9**
→ Project B is marginally preferred despite a lower strategic-fit score, because it scores much better on cost.

## Choosing a Method
- **NPV**: best overall measure of absolute value creation; accounts for time value of money.
- **IRR**: useful for ranking by rate of return, intuitive for stakeholders, but can be unreliable with unconventional cash flows.
- **Payback Period**: simple, favors liquidity/quick recovery, ignores time value of money and long-term returns.
- **Weighted Scoring Model**: best when strategic/qualitative factors matter alongside or instead of pure financials.

## Common Exam Angles
- Calculate NPV, ROI, or Payback Period from given cash flow data.
- Recommend which project to select given competing NPV/IRR/Payback results, and justify with reasoning (not just the number).
- Build/interpret a weighted scoring model table.
- Explain limitations of Payback Period vs NPV.
