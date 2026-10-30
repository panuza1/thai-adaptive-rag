# Failure analysis

Exploratory analysis after test access. It cannot be used to retune this test run. Retrieval labels are derived, non-exhaustive answer-span relevance.

| Query ID | Question | Route | B1 nDCG | B2 nDCG | B3 nDCG | P1 nDCG |
|---|---|---|---:|---:|---:|---:|
| B4M37Q5xCcVGgB4IF5IV_002 | ด็อกคิวเสตสามารถใช้ทำอะไรได้อีกบ้างนอกจากเป็นยาระบาย | A | 0.500000 | 0.430677 | 0.630930 | 0.500000 |
| ICQ054THVjycHK3DNNt0_003 | ปลาใบไม้ในภาษาอีสานเรียกว่าปลาชนิดนี้ว่าอะไร | C | 0.630930 | 1.000000 | 0.630930 | 0.630930 |
| vrMwo56XajptJAiH2Br0_004 | เจ. อาร์. อาร์. เสียชีวิตเมื่อไร | C | 0.000000 | 0.630930 | 0.500000 | 0.500000 |
| x4fSbfJrXClYXpMMSwja_002 | สวนเบญจสิริเป็นสวนสาธารณะประเภทใด | C | 1.000000 | 1.000000 | 0.630930 | 0.630930 |
| zcQWGlRuU1bLyQEaW2Ea_004 | ส่วนด้านคอนเสิร์ตที่ไดอาน่าไปร่วมแสดงก็คือ ? | A | 0.630930 | 1.000000 | 1.000000 | 0.630930 |
| oUNCj0S0anI3YTYCKL3X_000 | วงดนตรีสัญชาติอะไร | C | 1.000000 | 1.000000 | 0.430677 | 0.430677 |

Four of the six regret cases route to reranking and two remain on dense retrieval. A small margin does not reliably identify reranker benefit. The short question “วงดนตรีสัญชาติอะไร” omits the band identity; its source context supplies information unavailable in the standalone query. This illustrates possible context-dependent QA artifacts in the converted retrieval task.

## Generation case inspection (assistant qualitative review; not independent human labels)

- `jHrp17T8wjCgn4OuzdDZ_000`, B1: asks for the Roman name of Aphrodite. The output says “Aphrodite”; retrieved chunk `b478edabc2d675c78dd63a9db0be2376fb69be6e6f73d0e69dd5321574c7f764:0` explicitly states “ภาคโรมัน คือ วีนัส”. The response conflicts with supplied evidence despite successful retrieval.

- `vrMwo56XajptJAiH2Br0_004`, B2: asks when J. R. R. died. The output gives Buddhist year 2528; retrieved evidence states CE 1973. Thus the supplied evidence does not support the generated year.

- `1rWZnIO61zP1HgpWejEh_001`, P1: the answer contains the reference singer name but earns zero strict exact match because of additional prose and a long, unfinished citation. Its 128-token output reaches the configured cap. This demonstrates that strict exact match is not semantic correctness and that citation formatting can consume the response budget.

These selected cases establish examples, not population hallucination rates. The blinded packet must be independently annotated before aggregate correctness, faithfulness, unsupported-claim or hallucination comparisons. No policy or prompt is changed after these observations.
