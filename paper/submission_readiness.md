# AUCC 2027 submission readiness

Status reviewed: 2026-10-30. The maintained paper sources are `paper/draft.md` and `paper/aucc2027_manuscript.docx`. The author canceled the LaTeX migration; existing migration artifacts are retained as inactive work and must not be treated as the submission master. Manual LaTeX transfer is the author's responsibility.

## Verified evidence

- The existing Word manuscript remains byte-identical to the version before migration. Its eight rendered pages are archived in `paper/qa/manuscript_delivery/`.
- The Markdown content and retained official Word template also remain byte-identical to the pre-migration versions.
- Direct benchmark: 240 unique query–method pairs; 60 matched test queries per method; finite, valid timings; configuration and schedule checks pass. Original held-out outputs remain unchanged.
- Retrieval: 1,620 records, including the completed ablations. No new experiments or routing changes are required for the current manuscript.
- All 240 direct rankings and answers match the original outputs. Existing final test evidence records 15 passing tests. No implementation changed during the canceled migration, so no additional test run was needed for this status review.
- Statistical analysis was reproduced with byte-identical JSON. Three manuscript tables were checked against outputs; two grayscale figures and all eight Word-rendered pages were visually inspected during final validation.

## Scientific claims approved by the current evidence

P1 reduces retrieval latency relative to B3 by 80.85%, including router overhead, but does not reduce observed mean complete-request latency. P1 averages 42.489 seconds versus B3's 42.141; the paired difference is +0.3477 seconds, with a 95% article-cluster interval of [−1.2076, 1.8974]. This is exploratory uncertainty, not a formal significance or equivalence test. Higher recall relative to B1/B2 does not establish better overall answer quality. Source-derived relevance is incomplete; the six regret cases are not all confirmed semantic routing errors.

## Items required before a final submission decision

| Item | Status | Required action |
|---|---|---|
| Independent semantic correctness and claim grounding | Pending; 0/240 human labels | Obtain two independent Thai-proficient raters using `experiments/annotation_protocol.md` and `results/validation_02/annotation/blinded_packet.jsonl`; keep method mapping and post-test failure analysis hidden until ratings finish. Retain disagreement records and adjudicate before analysis. |
| Author affiliation | Pending | Supply department, faculty, institution and country; do not infer them from logos or workspace context. |
| Advisor and coauthors | Pending | Confirm names, affiliations and author order; retain the supplied corresponding author details already in the Word manuscript. |
| Advisor certification | Pending | Obtain the required signed form; an unsigned placeholder is not sufficient. |
| Similarity report | Pending | Obtain the institution's required report; no score has been measured or claimed. |
| Submission deadline | Conflicting official pages | Confirm the operative deadline before relying on an extension. Previously verified pages list 16 November and 4 December 2026; use the earlier date for planning. |
| Final upload package | Pending author/advisor decision | Freeze the final Word version and matching PDF only after the missing author details and any genuine evaluation results have been incorporated and visually checked. |

The verified source links and formatting discrepancies are documented in `paper/aucc_requirements.md`. The official submission information is at https://aucc-conf.org/submission.php and the portal at https://aucc-conf.org/submission/ . The eight-page working draft satisfies the overlapping page-count ranges, but page count alone does not establish submission readiness. Do not contact organizers, upload the paper, or claim advisor approval without authorization.

## Next analysis when human labels arrive

Preserve both original rater files, align claim boundaries, calculate pre-adjudication agreement, and retain adjudicated labels separately from automated exact match. Report annotation coverage and denominators. Use the same available query pairs and article-cluster bootstrap for method comparisons. Do not convert missing or uncertain labels to successful outcomes. The answerable-only corpus does not support balanced abstention accuracy. Update the existing Markdown and Word paper only from actual new evidence; do not retune routing on these held-out results.

Current assessment: the experimental and formatted working draft is ready for advisor review, while independent answer validation and administrative submission materials remain pending. No hallucination reduction or general superiority claim is supported.
