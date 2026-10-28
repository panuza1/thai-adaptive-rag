# API verification log

Checked 2026-10-29 against official sources before implementation:

- SentenceTransformer constructor accepts model revision/device; `encode` supports normalized NumPy embeddings: https://sbert.net/docs/package_reference/sentence_transformer/model.html
- CrossEncoder accepts model revision/device/max_length and `predict` accepts query-document pairs: https://sbert.net/docs/package_reference/cross_encoder/model.html
- E5 requires query/passage prefixes, including non-English inputs: https://huggingface.co/intfloat/multilingual-e5-small
- BM25Okapi accepts token lists and exposes `get_scores`: https://github.com/dorianbrown/rank_bm25
- PyThaiNLP `word_tokenize` supports `engine='newmm'`, `keep_whitespace=False`: https://pythainlp.org/docs/5.1/api/tokenize.html
- Local generation uses AutoTokenizer, AutoModelForCausalLM, chat template and `generate`: https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct and https://huggingface.co/docs/transformers/main/en/llm_tutorial

Resolved installed versions are in `results/environment.lock.txt`. Documentation availability does not imply runtime model validation; execution evidence is separate in run logs. Dependencies were installed in `.venv`; remove inherited PYTHONPATH for isolation.
