# Project Time Management (Network Diagrams, Critical Path, PERT, Dependencies)

## Key Processes
1. **Plan Schedule Management**
2. **Define Activities** — identifying specific actions to produce project deliverables.
3. **Sequence Activities** — identifying and documenting relationships (dependencies) among activities.
4. **Estimate Activity Durations**
5. **Develop Schedule** — analyzing sequences, durations, resources, and constraints to create the project schedule.
6. **Control Schedule** — monitoring status, managing changes to the schedule baseline.

## Types of Dependencies
- **Mandatory (hard logic)**: inherent in the nature of the work (e.g. you must lay foundations before building walls).
- **Discretionary (soft logic/preferred logic)**: defined by the team based on best practice or preference, not physical necessity.
- **External**: relationship between project activities and non-project activities (e.g. waiting for a government permit).
- **Internal**: relationship purely between project activities, generally within the team's control.

## Precedence Relationships
- **Finish-to-Start (FS)**: predecessor must finish before successor starts (most common).
- **Start-to-Start (SS)**: predecessor must start before successor can start.
- **Finish-to-Finish (FF)**: predecessor must finish before successor can finish.
- **Start-to-Finish (SF)**: predecessor must start before successor can finish (rare).

**Lead and Lag:**
- **Lead**: allows the successor activity to start before the predecessor finishes (accelerates the schedule; represented as negative lag, e.g. FS − 2 days).
- **Lag**: forces a delay in the successor after the predecessor (e.g. FS + 3 days, such as waiting for concrete to cure).

## Network Diagrams (Precedence Diagramming Method - PDM)
A visual representation of activities and their logical dependencies, using boxes (nodes) for activities and arrows for dependencies (Activity-on-Node is the standard modern approach).

## Critical Path Method (CPM)
The **critical path** is the longest path through the network diagram, determining the shortest possible project duration. Any delay on a critical path activity delays the entire project.

**Forward Pass** (calculates Early Start/Early Finish):
- ES of first activity = 0 (or project start)
- EF = ES + Duration
- ES of successor = EF of predecessor (for FS relationships)

**Backward Pass** (calculates Late Start/Late Finish), starting from the project end date and working backward:
- LF of last activity = project end (or EF of last activity on critical path)
- LS = LF − Duration
- LF of predecessor = LS of successor (for FS relationships)

**Float (Slack):**
- **Total Float** = LS − ES (or LF − EF): amount an activity can be delayed without delaying the overall project finish date.
- **Free Float**: amount an activity can be delayed without delaying the early start of any successor activity.
- Activities on the **critical path have zero total float** (any delay directly delays the project).

**Worked mini-example**: Activities A (4 days) → B (3 days) → D (2 days), and A → C (5 days) → D.
- Path A-B-D = 4+3+2 = 9 days
- Path A-C-D = 4+5+2 = 11 days
- Critical path = A-C-D (longest, = 11 days = minimum project duration)
- Activity B has float: it belongs to the shorter path, so it can slip by (11−9) = 2 days without delaying the project.

## PERT (Program Evaluation and Review Technique)
Used when activity durations are uncertain. Instead of a single duration estimate, PERT uses three estimates:
- **Optimistic (O)**: best-case duration
- **Most Likely (M)**: most probable duration
- **Pessimistic (P)**: worst-case duration

**PERT Expected Duration (weighted average, Beta distribution assumption):**
Te = (O + 4M + P) / 6

**Standard Deviation** (a measure of uncertainty for that activity): SD = (P − O) / 6

**Worked example**: O = 4 days, M = 6 days, P = 14 days.
Te = (4 + 4×6 + 14) / 6 = (4 + 24 + 14)/6 = 42/6 = **7 days**
SD = (14 − 4)/6 = 10/6 ≈ **1.67 days**

This expected duration is then used in place of a single-point estimate when building the network diagram/critical path, giving a more risk-aware schedule.

## Schedule Compression Techniques
- **Crashing**: adding resources to critical path activities to shorten duration, usually at increased cost (e.g. overtime, extra staff).
- **Fast-Tracking**: performing activities that would normally be done in sequence in parallel instead, which increases risk of rework.

## Common Exam Angles
- Draw/interpret a network diagram and identify the critical path given activity durations and dependencies.
- Perform forward pass/backward pass calculations to find ES, EF, LS, LF, and float for each activity.
- Calculate PERT expected duration and standard deviation given O/M/P estimates.
- Explain the difference between crashing and fast-tracking, and the trade-offs of each.
