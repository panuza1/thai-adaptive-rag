# Thai evidence-grounding annotation protocol (draft)

Annotate outputs only after retrieval and generation configuration is frozen. Export opaque response IDs; hide strategy names and timing from annotators. Preserve a private response-ID mapping. Supply the question, reference answers, retrieved chunk IDs/text, and answer. Do not tell annotators whether a response is adaptive.

Two Thai-proficient annotators independently segment each response into atomic factual claims. For each claim record its text and one of: supported by supplied evidence; contradicted by supplied evidence; neither supported nor contradicted. Record supporting/contradicting chunk IDs and a brief rationale. An answer can be factually correct but unfaithful to the supplied evidence; score these separately. A citation is not proof of entailment. Outside knowledge must not substitute for retrieved evidence when judging faithfulness.

For semantic correctness assign 1 only if the response answers the question correctly without a material contradictory statement; otherwise 0. Record uncertainty for adjudication, never convert uncertainty automatically to 0. Exact-match score is computed independently. For abstention, mark whether the output declines to answer, then assess appropriateness against a separately established answerability label. iApp answerable-only examples cannot establish balanced abstention accuracy.

Adjudication retains both original annotations, disagreement explanations, and a third/adjudicated label. Export adjudicated counts as `supported_claims` and `unsupported_claims`; the latter combines contradicted and insufficient-evidence claims, while original files preserve the distinction. Zero-claim responses get zero counts and undefined claim faithfulness. Report denominator and annotation coverage for every aggregate. Report raw agreement and Cohen's kappa for categorical correctness/support where units are aligned; resolve claim segmentation before computing claim-level agreement.

Do not use generated model judgments as if they were independent human annotations. Public data may include personal names; retain only task-relevant text and avoid releasing contributor/payment metadata. Final annotation guidelines, consent/ethics requirements at the university, and answerability design need advisor review before collecting human judgments.

## Operational rubric for the frozen 60-query study

Status: the author confirmed that independent annotators are not yet available. No human correctness or faithfulness labels have been collected. The research assistant's selected case inspections are qualitative automated assistance, not a blinded independent human experiment.

Use `results/heldout_01/annotation_packet.jsonl` as the immutable source. The packet has 240 opaque response IDs in a fixed shuffled order and omits system, route, scores and timings. A study coordinator keeps `annotation_mapping_private.json` separate and does not rate responses. Each annotator works independently from a separate blank label file. Do not disclose comparative results or failure-case selections before ratings. Similar or identical answers may reveal equivalence; blinding reduces method expectations but cannot guarantee that experienced raters never infer a strategy.

### Correctness

- `correct`: directly answers the question with the required entity/value/relation, allowing a faithful paraphrase, transliteration variant or equivalent unit/date conversion, and contains no material contradictory assertion.
- `incorrect`: wrong entity/value/relation, an essential omission, misleading extra factual content, or refusal despite sufficient evidence for an unambiguous question.
- `uncertain`: ambiguous standalone question, malformed reference, multiple defensible answers, or insufficient information to resolve a discrepancy. Require a rationale; do not force a binary label.
- Reference answers are aids, not infallible gold. Inspect the evidence when the reference is clipped or overly specific. Record a `reference_issue` flag and keep it separate from model correctness.

### Claim support

Segment each answer into independently checkable factual propositions. Do not treat citation identifiers, discourse markers or a bare refusal as factual claims. Split coordinated claims when one could be true and the other false. Keep the original Thai claim text and record the supporting or contradicting passage IDs.

- `supported`: the supplied passages jointly entail the claim, allowing straightforward paraphrase or explicit arithmetic conversion.
- `contradicted`: a supplied passage gives incompatible information about the same entity, attribute and context.
- `not_supported`: supplied passages neither entail nor directly contradict the claim; outside knowledge cannot rescue it.
- `uncertain`: claim segmentation or evidence interpretation cannot be resolved. Require adjudication; never silently count it as supported.

Correctness and support are independent axes. A correct answer may be unsupported by the supplied passages, while a supported passage may discuss the wrong entity for the intended question. A valid-looking citation alone is not entailment. Distinguish citation validity from claim grounding.

### Synthetic training examples and boundary cases

Use only synthetic or development examples during rater training; do not distribute post-test failure analyses before ratings.

- Synthetic question: “Which city is the capital of Country X?” Evidence: “The capital is City Y.” Answer: “City Z.” Label the capital claim incorrect and contradicted.
- Synthetic question asks for a person; the answer provides the reference person with explanatory prose. Do not reject it merely because exact match is zero; evaluate every factual addition.
- A truncated citation does not alone make its preceding factual statement unsupported. Judge the claim against supplied evidence and flag citation formatting separately.
- A synthetic question says only “When did he leave?” without identifying a person: flag standalone ambiguity and adjudicate instead of silently reconstructing missing context from a reference.

These are fabricated teaching examples explicitly labeled synthetic, not research measurements or dataset annotations.

### Aggregation and missing data

Adjudicate correctness only after both independent ratings are complete. Preserve both original files, timestamps, pseudonymous annotator IDs and disagreement notes. Use a third reviewer or a documented consensus meeting for unresolved judgments. A consensus label is not a third independent rating. Align claim boundaries before measuring support agreement; report segmentation disagreements separately.

Report correctness as correct / adjudicated binary responses, with coverage / 240. Report supported claims / all adjudicated factual claims and unsupported claims / all adjudicated factual claims; unsupported combines contradicted and not_supported, retaining both subcategories in raw annotations. Report response-level hallucination operationally as at least one unsupported factual claim among responses with adjudicated factual claims, with denominator explicit. Zero-claim responses have undefined faithfulness and must not inflate it. Report all-refusal counts separately.

Paired comparisons must use the same available query pairs for both systems and disclose complete-case counts. If annotation is incomplete or uncertain nonrandomly, report sensitivity bounds and do not compare unrelated denominators. Bootstrap source article groups, preserving query and system pairing. Report raw agreement and Cohen's kappa for binary correctness before adjudication; kappa is undefined if its expected-agreement denominator vanishes. Neither agreement nor a confidence interval proves judge validity.

Do not report balanced abstention accuracy from this answerable-only corpus. A separate answerability-labeled set is needed. Do not claim hallucination reduction until actual independent labels support a paired comparison.
