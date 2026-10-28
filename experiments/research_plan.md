# Execution plan and decision gates

Planning date: 29 October 2026. Treat 16 November as the working submission deadline until official conflict resolution. Dates below are a proposed schedule, not completed actions.

| Window | Deliverable | Gate |
|---|---|---|
| Oct 29–31 | Reproduce all fixed retrieval baselines; inspect routing and duplicate audits | No result claims until every arm runs on identical queries and corpus |
| Nov 1–3 | Complete closest-prior-work comparison and full-development calibration; validate generator Thai behavior | Drop unsupported novelty claims; change model only before final evaluation |
| Nov 4–5 | Freeze protocol/config; estimate annotation sample requirements using development variability; validate thresholds | Prespecify primary endpoint, non-inferiority margin, exclusions and denominators |
| Nov 6–8 | Held-out retrieval/generation run, timing repeats and ablations | No threshold or model changes using test labels |
| Nov 7–11 | Independent Thai annotations and adjudication | Missing labels stay missing; assess agreement and uncertainty |
| Nov 12–14 | Final paired analysis, negative-result interpretation, manuscript tables/figures | Every number traceable to run artifacts |
| Nov 15–16 | Advisor review, template proof, similarity check, certification and submission preparation | Confirm actual deadline and submission requirements; do not submit automatically |

If the schedule cannot support credible annotation and frozen evaluation, narrow the claim to retrieval-quality/cost analysis and explicitly remove unsupported generation-reliability claims. Do not replace annotation with invented or uncalibrated scores. Discuss conference suitability with the advisor; an engineering smoke run alone is not a completed research paper.

Learned-router gate: first quantify route diversity and per-query best-strategy headroom. If static B1/B2/B3 already dominates, a learned router adds unnecessary complexity. If headroom exists, use development-only labels and a shallow interpretable learner, with validation selection and no test refitting.
