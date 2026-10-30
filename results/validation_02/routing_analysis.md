# Routing and reranking validation

This post-test diagnostic preserves original labels, rankings and policies. “Regret” means lower nDCG than the best static baseline on the same query under existing qrels. It does not by itself prove an incorrect decision or an unsupported answer. Six questions meet this definition.

| Query suffix / topic | Route and trigger | Observed labeled ranks | Interpretation from evidence inspection |
|---|---|---|---|
| B4M37Q5xCcVGgB4IF5IV_002 / docusate use | A; margin 0.0560, length 13, no exact indicator | P1 3; B3 2 | Dense favors the general drug introduction; the answer-bearing ear-irrigation detail is later. A large top-score margin does not guarantee best evidence rank. The reference starts with a clipped Thai character, another annotation-quality issue. |
| ICQ054THVjycHK3DNNt0_003 / regional fish name | C; margin 0.0180 | Hybrid 1; reranked 2 | Reranking promotes the same article's introductory species description over its later regional-name sentence. Topic relevance differs from answer-bearing relevance. |
| vrMwo56XajptJAiH2Br0_004 / Tolkien death | C; margin 0.0132 | Hybrid 2; reranked 3; dense misses top 5 | Abbreviated entity name is weakly specified. Reranking promotes passages about other deaths; hybrid retrieves the source answer better. Reranking is not always helpful even when dense is weak. |
| x4fSbfJrXClYXpMMSwja_002 / park type | C; margin 0.000594 | Hybrid labeled 1; reranked labeled 2 | **Qrel limitation:** the reranked first passage explicitly says the park is a small community park, matching the reference. It is unjudged because labels derive from one source span. The apparent nDCG loss cannot be treated as confirmed evidence-quality loss. |
| zcQWGlRuU1bLyQEaW2Ea_004 / Diana concert | A; margin 0.0341 | Dense 2; hybrid/reranked 1 | Same-article passages mention two concerts. The query and reference designate one, while dense promotes a similar guest-performance sentence. Thai names are not recognized by the digit/Latin/quote proxy. This is an observed limitation of the proxy, not validation of a new NER rule. |
| oUNCj0S0anI3YTYCKL3X_000 / band nationality | C; margin 0.00428 | Hybrid 1; reranked 4 | The standalone question omits the band's name. Top reranked passage is about Metallica; another retrieved passage describes a Thai band. The source-derived label identifies one intended band, but the query itself is ambiguous. Regret cannot establish an unambiguous semantic error. |

## Why removing reranking raises nDCG

Ten of 60 queries route to C. Removing reranking changes C to B while leaving all other decisions unchanged. Across these ten: four improve nDCG, one worsens and five retain the same nDCG. The remaining 50 queries are unchanged. Improvements are +0.369070 (fish), +0.130930 (Tolkien), +0.369070 (park), +0.569323 (band); the loss is −0.430677 on “Who directed it?”, where reranking retrieves the labeled passage at rank 4 while hybrid misses it. Their sum divided by 60 is +0.016795, exactly the observed change from 0.923085 to 0.939880. Recall decreases by 1/60 because the director evidence is lost. Reranking therefore sometimes rescues recall while harming ranking elsewhere.

The park contribution reflects incomplete judgments and the band/director questions are context-dependent. Consequently, the result supports a measured effect under this evaluation protocol, not a broad claim that reranking harms Thai evidence retrieval. Source snapshots and all passages for the six cases are preserved in `routing_evidence.json`; the ten ablation effects are in `reranking_effects.json`.

## Future work without test tuning

1. On development data, collect pooled relevance judgments for all strategies' top passages, including same-title duplicates. Inspect whether a passage answers the actual question, not only whether it covers one original span.
2. Flag questions that require omitted source context. Assess a separately annotated standalone-answerable subset; do not silently remove difficult questions from the completed test.
3. Calibrate predicted incremental benefit of reranking, rather than interpret raw dense margin as a calibrated probability. Use group-separated development/validation outcomes and explicit cost constraints.
4. Evaluate Thai entity features and query–passage answer-bearing alignment on development data; the present six examples do not justify a tuned threshold or learned policy.
5. Pre-register any new policy and evaluate on an untouched held-out sample, with a frozen generator and independent grounding annotation. Preserve this negative result as the first experiment.
