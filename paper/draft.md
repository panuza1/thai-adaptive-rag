# Adaptive Retrieval Strategy for Cost-Efficient and Reliable Thai RAG Systems

**Working content draft — not submission-ready. Authors and affiliations pending.**

## Abstract

Retrieval-augmented generation can improve access to external knowledge, but applying an expensive retrieval pipeline uniformly may waste computation. This study investigates interpretable query-adaptive selection among dense retrieval, hybrid lexical-dense retrieval, and hybrid retrieval with neural reranking for Thai question answering. The proposed router uses query length, exact-token indicators, and an initial dense-retrieval score margin. We specify a controlled evaluation with shared models, evidence budgets, prompts, and article-disjoint query partitions. Retrieval quality, answer correctness, evidence-grounded reliability, and computational efficiency are evaluated separately. Paired article-level uncertainty estimates and component ablations are designed to characterize tradeoffs rather than assume improvement. Implementation and data preparation are available; final held-out and human-annotated results remain pending. Consequently, this draft does not establish superiority, non-inferiority, hallucination reduction, or methodological novelty.

**Keywords:** Thai question answering; retrieval-augmented generation; adaptive retrieval; hybrid retrieval; computational efficiency.

## 1. Introduction

Retrieval-augmented generation combines parametric language models with external evidence [1]. Retrieval can fail through lexical mismatch, semantic ambiguity, or poorly ranked evidence. Dense passage retrieval provides a learned semantic representation [2], while lexical retrieval preserves exact-term signals [3]. Combining these approaches and adding a cross encoder can improve evidence ranking but introduces additional computation.

A fixed expensive pipeline may be unnecessary for some questions, but an adaptive pipeline also incurs decision overhead. The relevant research question is therefore whether query-adaptive selection can reduce measured costs while preserving answer quality and evidence-grounded reliability in Thai. This study focuses on an experimentally testable tradeoff. We do not introduce adaptive retrieval as a new concept.

## 2. Related Work

RRF combines rankings without requiring score calibration [4], although subsequent analysis shows that fusion behavior depends on parameters and tuned score combinations can be stronger [5]. Cross-encoder reranking jointly processes query and passage [6]. These methods motivate the fixed retrieval baselines.

Adaptive-RAG learns to choose retrieval effort from question complexity [7]. Self-RAG integrates retrieval and reflection decisions into generation [8]. MBA-RAG makes cost-sensitive retrieval choices through a bandit formulation [9]. External-feature adaptive retrieval also predates this study [10]. Thus, the candidate contribution is a controlled Thai evaluation of transparent A/B/C routing and its overhead, rather than an unrestricted novelty claim. MIRACL provides a complementary multilingual retrieval benchmark [11]. Ragas motivates separate evaluation of retrieval relevance and grounded generation [12], but automatic judgments require Thai-specific validation.

Thai-specific work further constrains novelty. Similarity-based Thai QA has measured quality and runtime [13]. Thai legal RAG has combined sparse/dense retrieval and neural reranking [14]. A recent Thai Royal Gazette study compares retrieval units and methods with span-level evidence judgments [15]. TSWAP includes query-dependent forced retrieval for Thai entity lookups [16]. These precedents mean that neither Thai hybrid retrieval nor Thai query-dependent retrieval can be claimed as new. Our proposed contribution remains a narrowly controlled evaluation of discrete strategy selection and its measured costs.

## 3. Proposed Method

Given query q, compute a normalized dense embedding and cosine scores against a fixed chunk index. Reuse this search if further processing is selected. Extract Thai-token count, an exact-token proxy indicating digits/Latin strings/quotation marks, and the score margin between the first two dense candidates.

A provisional deterministic policy selects reranking when the query is long or the margin is small; otherwise it selects hybrid retrieval for exact-token queries and dense retrieval for remaining queries. Thresholds are development settings pending calibration. Neither token length nor margin is a validated measure of reasoning complexity or correctness. The selected pipeline returns the same number of evidence chunks as every baseline.

Hybrid retrieval uses RRF over truncated BM25 and dense rankings. Reranking applies a shared multilingual cross encoder to the fused candidate list. The no-hybrid ablation uses dense candidates for reranking. Feature ablations suppress one decision input at a time. All query-side work is included in online retrieval timing.

## 4. Experimental Setup

The initial corpus derives from the training partition of the public iApp Thai Wikipedia QA repository [17]. We validate answer offsets, deduplicate exact normalized questions, and partition connected components of identical normalized titles or contexts by a deterministic hash. The fixed retrieval corpus includes all source contexts, while evaluation labels remain partitioned. Identical contexts cannot cross partitions. Near-duplicate and model-pretraining contamination audits remain necessary before final evaluation.

B1, B2, B3 and P1 share multilingual E5 small embeddings, the corpus, chunking and retrieval budget. B3/P1 share a multilingual mMiniLM cross encoder. Local generation is implemented using a fixed instruction model, common Thai prompt and deterministic decoding. Model identities and resolved revisions are recorded by the runner. The initial generator is resource-driven and requires Thai suitability validation.

Recall@5, MRR@5 and binary nDCG@5 quantify derived span relevance. Strict normalized exact match and human semantic correctness evaluate answers. Independent Thai annotators will label atomic claims for support and contradiction; abstention evaluation requires validated unanswerable examples. Wall latency, process CPU time, reranked pairs and generator token counts quantify efficiency. Bootstrap intervals resample source-context groups while retaining paired system outputs. The primary correctness non-inferiority margin is provisionally 0.03 absolute, to be approved and frozen before test access.

Hardware detected: Intel Core i5-12450H, approximately 32 GiB system RAM, NVIDIA RTX 3050 laptop-class GPU with 4 GiB VRAM. The initial retrieval configuration uses CPU inference with four torch threads. This hardware statement is environment evidence, not a performance measurement.

## 5. Results

Held-out B1/B2/B3/P1 retrieval comparisons: **pending**. Held-out answer correctness, faithfulness, unsupported-claim rate, hallucination rate and abstention accuracy: **pending**. End-to-end token/cost comparisons: **pending**. No statistical significance or non-inferiority conclusion is available.

Data preparation produced 3,223 chunks and 5,667 retained questions: 3,360 development, 1,133 validation and 1,174 test questions. The manifest lists 94 excluded input records due to invalid/uncovered spans or duplicate questions. These are observed processing counts, not model evaluation results. See `data/processed_v2/manifest.json` and `results/` for machine-readable execution evidence. Development-only pilot outputs, when present, must remain separate from final test tables.

## 6. Discussion

The router may save reranking work but lose evidence quality. A small dense score margin can reflect several relevant overlapping passages rather than uncertainty, leading to unnecessary reranking. Exact-token indicators may overroute numerical factoid questions. Neural reranking may itself perform poorly under Thai language transfer. These mechanisms are hypotheses for error analysis; they are not observed findings until supported by per-query outputs.

Learned routing is justified only if development outcomes show predictable differences among strategies and sufficient headroom over static baselines. Otherwise, retaining the simplest fixed pipeline is an appropriate outcome. A negative adaptive result would delimit the value of routing under the evaluated model and hardware configuration.

## 7. Limitations

The current evidence labels are derived from answer spans and are not exhaustive relevance judgments. Overlapping chunks can inflate the number of relevant items. Character windows may split Thai words. Wikipedia factoid QA does not represent all Thai information needs. Model pretraining may include benchmark content. Heuristic features require calibration and may not transfer. Human grounding evaluation, near-duplicate checks, final timing repetitions and full literature detail verification remain incomplete. The small initial generator may be inadequate for Thai. Official conference pages disagree on the submission deadline and page limits; final formatting requires reconciliation.

## 8. Conclusion

This project specifies and implements an interpretable Thai retrieval-routing investigation with explicit leakage controls and separate quality, reliability and efficiency measurements. Whether adaptive routing provides a useful tradeoff remains an empirical question. A final conclusion will follow frozen held-out experiments and independent evidence-grounding annotation.

## References

[1] P. Lewis et al., “Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks,” 2020. https://arxiv.org/abs/2005.11401

[2] V. Karpukhin et al., “Dense Passage Retrieval for Open-Domain Question Answering,” 2020. https://arxiv.org/abs/2004.04906

[3] S. Robertson and H. Zaragoza, “The Probabilistic Relevance Framework: BM25 and Beyond,” 2009. https://doi.org/10.1561/1500000019

[4] G. V. Cormack, C. L. A. Clarke, and S. Büttcher, “Reciprocal Rank Fusion outperforms Condorcet and individual Rank Learning Methods,” 2009. https://doi.org/10.1145/1571941.1572114

[5] S. Bruch, S. Gai, and A. Ingber, “An Analysis of Fusion Functions for Hybrid Retrieval,” 2023. https://doi.org/10.1145/3596512

[6] R. Nogueira and K. Cho, “Passage Re-ranking with BERT,” 2019. https://arxiv.org/abs/1901.04085

[7] S. Jeong et al., “Adaptive-RAG: Learning to Adapt Retrieval-Augmented Large Language Models through Question Complexity,” 2024. https://aclanthology.org/2024.naacl-long.389/

[8] A. Asai et al., “Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection,” 2023. https://arxiv.org/abs/2310.11511

[9] X. Tang et al., “MBA-RAG: a Bandit Approach for Adaptive Retrieval-Augmented Generation through Question Complexity,” 2025. https://arxiv.org/abs/2412.01572

[10] M. Marina et al., “LLM-Independent Adaptive RAG: Let the Question Speak for Itself,” 2025. https://arxiv.org/abs/2505.04253

[11] X. Zhang et al., “Making a MIRACL: Multilingual Information Retrieval Across a Continuum of Languages,” 2022. https://arxiv.org/abs/2210.09984

[12] S. Es et al., “Ragas: Automated Evaluation of Retrieval Augmented Generation,” 2023. https://arxiv.org/abs/2309.15217

[13] K. Jearanaitanakij et al., “Thai Question-Answering System Using Similarity Search and LLM,” 2024. https://doi.org/10.37936/ecti-cit.2024183.256043

[14] P. Promwang and P. Boonma, “Development of a Retrieval-Augmented Generation System for Legal Data in Thai Language,” DSE Record, vol. 6, no. 1, publication year verification pending. https://datascience.cmu.ac.th/storage/articles/73.pdf

[15] P. Suyasri, P. Akarajaradwong, and C. Chaksangchaichot, “An Empirical Study of Evidence Retrieval for Retrieval Augmented Generation over the Thai Royal Gazette,” NLLP, 2026. https://aclanthology.org/2026.nllp-1.19/

[16] P. Ukosaramig and K. Viriyayudhakorn, “TSWAP: A Multilingual Retrieval-Augmented Thai Wellness Advisor,” 2026. https://arxiv.org/abs/2608.22917

[17] iApp Technology, “iapp-wiki-qa-dataset,” repository, accessed October 29, 2026. https://github.com/iapp-technology/iapp-wiki-qa-dataset
