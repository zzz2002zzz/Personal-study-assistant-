# Project Cost Management (Earned Value Management)

## Key Processes
1. **Plan Cost Management** — how costs will be estimated, budgeted, and controlled.
2. **Estimate Costs** — approximating the cost of resources (analogous estimating, parametric estimating, bottom-up estimating, three-point estimating).
3. **Determine Budget** — aggregating estimated costs into an authorized **cost baseline** (a time-phased budget, often shown as an S-curve).
4. **Control Costs** — monitoring cost performance, managing changes to the cost baseline. This is where **Earned Value Management (EVM)** is applied.

## Core EVM Terms
- **PV (Planned Value)**: the authorized budget assigned to scheduled work as of a point in time — "what should have been spent by now."
- **EV (Earned Value)**: the value of work actually completed, expressed in terms of the approved budget — "what the completed work is worth."
- **AC (Actual Cost)**: the actual cost incurred for the work completed — "what was really spent."
- **BAC (Budget at Completion)**: the total planned budget for the entire project.

## EVM Formulas
| Metric | Formula | Interpretation |
|---|---|---|
| Cost Variance (CV) | EV − AC | Positive = under budget; Negative = over budget |
| Schedule Variance (SV) | EV − PV | Positive = ahead of schedule; Negative = behind schedule |
| Cost Performance Index (CPI) | EV / AC | >1 = efficient cost performance; <1 = cost overrun |
| Schedule Performance Index (SPI) | EV / PV | >1 = ahead of schedule; <1 = behind schedule |
| Estimate at Completion (EAC) | BAC / CPI | Forecasted total cost if current cost performance continues |
| Estimate to Complete (ETC) | EAC − AC | Expected cost of remaining work |
| Variance at Completion (VAC) | BAC − EAC | Projected budget surplus/deficit at project end |
| To-Complete Performance Index (TCPI) | (BAC − EV) / (BAC − AC) | Efficiency required for remaining work to meet BAC |

## Worked Example
A project has BAC = $100,000. At the review date: PV = $40,000, EV = $35,000, AC = $45,000.
- CV = 35,000 − 45,000 = **−$10,000** (over budget)
- SV = 35,000 − 40,000 = **−$5,000** (behind schedule)
- CPI = 35,000 / 45,000 = **0.78** (getting only $0.78 of value per $1 spent)
- SPI = 35,000 / 40,000 = **0.875** (behind schedule)
- EAC = 100,000 / 0.78 ≈ **$128,205** (forecast final cost, higher than BAC — bad news)

## Estimating Techniques
- **Analogous Estimating**: uses historical data from similar past projects; fast but less accurate.
- **Parametric Estimating**: uses a statistical relationship between historical data and variables (e.g. cost per square meter, cost per line of code).
- **Bottom-Up Estimating**: estimates individual work packages/activities and aggregates them; most accurate but time-consuming.
- **Three-Point Estimating (PERT-based cost)**: (Optimistic + 4×Most Likely + Pessimistic) / 6 — accounts for uncertainty.

## Cost Baseline vs Budget vs Funding Requirements
- **Cost Baseline**: the approved, time-phased budget used to measure performance (excludes management reserve).
- **Project Budget**: cost baseline + management reserve.
- **Funding Requirements**: often released periodically/incrementally rather than as one lump sum, sometimes exceeding the baseline briefly to allow for expenditure spikes (funding "steps" above the S-curve).

## Common Exam Angles
- Calculate CV, SV, CPI, SPI, EAC given PV/EV/AC/BAC — this is a very common numeric question type.
- Interpret whether a project is ahead/behind schedule and under/over budget from index values.
- Explain the difference between cost baseline and project budget.
- Choose the appropriate estimating technique for a scenario (early rough estimate vs detailed estimate needed).
