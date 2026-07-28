# Experimental audit of rerank-suitable tasks

Date: 2026-07-28

## Purpose

This document audits all 551 evaluated HAKARI-Bench tasks and asks which
tasks are suitable for a conventional pairwise reranker. The audit is
experimental: it describes the current findings and does not define product
metadata or an implementation plan.

The starting proposal was to select tasks whose mean query length is at most
100 characters and whose mean document length is at most 2,000 characters.
That rule is not a semantic definition. It admits duplicate-question, entity,
citation, and short-choice tasks, while rejecting valid multilingual, code,
medical, legal, and long-document retrieval tasks.

## Evidence and decision method

The audit uses the canonical DuckDB `dataset_metadata` rows for task identity,
language, and mean character lengths. It also uses the deterministic head-3
query/positive-document examples stored under `task_docs/metadata/`. Those
examples are sampled from each source dataset's queries, corpus, and positive
qrels by `scripts/extract_benchmark_task_examples.py`.

A task is marked **Core** when a candidate document can normally be judged
from the pair text as directly useful or relevant to a question, search
request, claim, topic, legal/medical case, or programming request, and the
task family has sufficiently clear semantics for the proposed default set.
Long documents are allowed; length affects computational cost, not semantic
suitability.

**Extended** contains plausible direct relevance tasks that should receive
another family-level sample audit before joining the default set. This avoids
turning a broad task-name or benchmark-family inference into an automatic
acceptance. **Specialized** means pairwise ranking is meaningful but the
objective is not ordinary topical relevance—for example counterargument
retrieval, reasoning-similarity retrieval, legal case similarity, code-to-code
matching, or synthetic long-context lookup. **No** covers symmetric duplicate
or similarity tasks, entity matching, citation relations, and reasoning-choice
conversions.

For MNanoBEIR, decisions are made by task family and applied to every language.
A family is never accepted in one language and rejected in another merely
because translation changes the average character length.

## Results

- Core: **257**
- Extended: **96**
- Specialized: **62**
- No: **136**
- Total: **551**

The recommended default rerank-oriented set is **Core: 257 tasks**.
Extended tasks are candidates for later promotion after additional sample
review. Specialized tasks may still be valuable when their objective is
stated explicitly. Head-3 inspection identifies task shape but does not prove
that every qrel in a dataset is clean.

## Task-by-task audit

Mean lengths are Unicode character counts from the current canonical DuckDB,
not tokenizer lengths or maxima.

| Nano set | Task | Language | Query avg chars | Document avg chars | Verdict | Finding |
|---|---|---:|---:|---:|---|---|
| MNanoBEIR | arguana (NanoBEIR-ar) | ar | 898.6 | 857.0 | Specialized | Argument-to-counterargument retrieval; requires a non-topical relevance objective. |
| MNanoBEIR | arguana (NanoBEIR-de) | de | 1243.1 | 1142.3 | Specialized | Argument-to-counterargument retrieval; requires a non-topical relevance objective. |
| MNanoBEIR | arguana (NanoBEIR-en) | en | 1201.8 | 1011.8 | Specialized | Argument-to-counterargument retrieval; requires a non-topical relevance objective. |
| MNanoBEIR | arguana (NanoBEIR-es) | es | 1220.0 | 1110.8 | Specialized | Argument-to-counterargument retrieval; requires a non-topical relevance objective. |
| MNanoBEIR | arguana (NanoBEIR-fr) | fr | 1271.2 | 1157.0 | Specialized | Argument-to-counterargument retrieval; requires a non-topical relevance objective. |
| MNanoBEIR | arguana (NanoBEIR-it) | it | 1187.4 | 1102.3 | Specialized | Argument-to-counterargument retrieval; requires a non-topical relevance objective. |
| MNanoBEIR | arguana (NanoBEIR-ja) | ja | 553.9 | 458.8 | Specialized | Argument-to-counterargument retrieval; requires a non-topical relevance objective. |
| MNanoBEIR | arguana (NanoBEIR-ko) | ko | 619.4 | 519.6 | Specialized | Argument-to-counterargument retrieval; requires a non-topical relevance objective. |
| MNanoBEIR | arguana (NanoBEIR-no) | multilingual | 1090.4 | 987.0 | Specialized | Argument-to-counterargument retrieval; requires a non-topical relevance objective. |
| MNanoBEIR | arguana (NanoBEIR-pt) | pt | 1158.5 | 1064.3 | Specialized | Argument-to-counterargument retrieval; requires a non-topical relevance objective. |
| MNanoBEIR | arguana (NanoBEIR-sr) | multilingual | 1182.9 | 989.8 | Specialized | Argument-to-counterargument retrieval; requires a non-topical relevance objective. |
| MNanoBEIR | arguana (NanoBEIR-sv) | sv | 1096.2 | 1006.2 | Specialized | Argument-to-counterargument retrieval; requires a non-topical relevance objective. |
| MNanoBEIR | arguana (NanoBEIR-th) | th | 820.6 | 860.1 | Specialized | Argument-to-counterargument retrieval; requires a non-topical relevance objective. |
| MNanoBEIR | arguana (NanoBEIR-vi) | vi | 979.3 | 998.4 | Specialized | Argument-to-counterargument retrieval; requires a non-topical relevance objective. |
| MNanoBEIR | climatefever (NanoBEIR-ar) | ar | 116.8 | 1343.0 | Core | Claim-to-evidence retrieval. |
| MNanoBEIR | climatefever (NanoBEIR-de) | de | 149.1 | 1767.3 | Core | Claim-to-evidence retrieval. |
| MNanoBEIR | climatefever (NanoBEIR-en) | en | 128.4 | 1619.5 | Core | Claim-to-evidence retrieval. |
| MNanoBEIR | climatefever (NanoBEIR-es) | es | 154.6 | 1772.1 | Core | Claim-to-evidence retrieval. |
| MNanoBEIR | climatefever (NanoBEIR-fr) | fr | 158.8 | 1826.9 | Core | Claim-to-evidence retrieval. |
| MNanoBEIR | climatefever (NanoBEIR-it) | it | 152.4 | 1743.1 | Core | Claim-to-evidence retrieval. |
| MNanoBEIR | climatefever (NanoBEIR-ja) | ja | 57.5 | 666.0 | Core | Claim-to-evidence retrieval. |
| MNanoBEIR | climatefever (NanoBEIR-ko) | ko | 66.0 | 779.7 | Core | Claim-to-evidence retrieval. |
| MNanoBEIR | climatefever (NanoBEIR-no) | multilingual | 124.7 | 1524.2 | Core | Claim-to-evidence retrieval. |
| MNanoBEIR | climatefever (NanoBEIR-pt) | pt | 147.8 | 1680.2 | Core | Claim-to-evidence retrieval. |
| MNanoBEIR | climatefever (NanoBEIR-sr) | multilingual | 135.2 | 1552.3 | Core | Claim-to-evidence retrieval. |
| MNanoBEIR | climatefever (NanoBEIR-sv) | sv | 132.2 | 1538.7 | Core | Claim-to-evidence retrieval. |
| MNanoBEIR | climatefever (NanoBEIR-th) | th | 118.6 | 1395.4 | Core | Claim-to-evidence retrieval. |
| MNanoBEIR | climatefever (NanoBEIR-vi) | vi | 133.8 | 1589.8 | Core | Claim-to-evidence retrieval. |
| MNanoBEIR | dbpedia (NanoBEIR-ar) | ar | 31.2 | 315.5 | No | Entity retrieval rather than ordinary query-document relevance. |
| MNanoBEIR | dbpedia (NanoBEIR-de) | multilingual | 38.0 | 369.5 | No | Entity retrieval rather than ordinary query-document relevance. |
| MNanoBEIR | dbpedia (NanoBEIR-en) | en | 33.1 | 336.3 | No | Entity retrieval rather than ordinary query-document relevance. |
| MNanoBEIR | dbpedia (NanoBEIR-es) | multilingual | 38.0 | 367.8 | No | Entity retrieval rather than ordinary query-document relevance. |
| MNanoBEIR | dbpedia (NanoBEIR-fr) | fr | 41.2 | 373.6 | No | Entity retrieval rather than ordinary query-document relevance. |
| MNanoBEIR | dbpedia (NanoBEIR-it) | multilingual | 38.3 | 361.7 | No | Entity retrieval rather than ordinary query-document relevance. |
| MNanoBEIR | dbpedia (NanoBEIR-ja) | ja | 28.2 | 174.6 | No | Entity retrieval rather than ordinary query-document relevance. |
| MNanoBEIR | dbpedia (NanoBEIR-ko) | ko | 16.8 | 187.6 | No | Entity retrieval rather than ordinary query-document relevance. |
| MNanoBEIR | dbpedia (NanoBEIR-no) | multilingual | 36.9 | 331.0 | No | Entity retrieval rather than ordinary query-document relevance. |
| MNanoBEIR | dbpedia (NanoBEIR-pt) | multilingual | 36.6 | 354.4 | No | Entity retrieval rather than ordinary query-document relevance. |
| MNanoBEIR | dbpedia (NanoBEIR-sr) | multilingual | 41.2 | 338.9 | No | Entity retrieval rather than ordinary query-document relevance. |
| MNanoBEIR | dbpedia (NanoBEIR-sv) | multilingual | 35.7 | 327.0 | No | Entity retrieval rather than ordinary query-document relevance. |
| MNanoBEIR | dbpedia (NanoBEIR-th) | th | 30.9 | 316.4 | No | Entity retrieval rather than ordinary query-document relevance. |
| MNanoBEIR | dbpedia (NanoBEIR-vi) | multilingual | 35.0 | 358.0 | No | Entity retrieval rather than ordinary query-document relevance. |
| MNanoBEIR | fever (NanoBEIR-ar) | ar | 40.1 | 1039.0 | Core | Claim-to-evidence retrieval. |
| MNanoBEIR | fever (NanoBEIR-de) | de | 52.6 | 1308.2 | Core | Claim-to-evidence retrieval. |
| MNanoBEIR | fever (NanoBEIR-en) | en | 45.4 | 1228.7 | Core | Claim-to-evidence retrieval. |
| MNanoBEIR | fever (NanoBEIR-es) | es | 49.6 | 1301.1 | Core | Claim-to-evidence retrieval. |
| MNanoBEIR | fever (NanoBEIR-fr) | fr | 51.2 | 1325.2 | Core | Claim-to-evidence retrieval. |
| MNanoBEIR | fever (NanoBEIR-it) | it | 50.1 | 1290.4 | Core | Claim-to-evidence retrieval. |
| MNanoBEIR | fever (NanoBEIR-ja) | ja | 27.7 | 581.9 | Core | Claim-to-evidence retrieval. |
| MNanoBEIR | fever (NanoBEIR-ko) | ko | 26.4 | 648.1 | Core | Claim-to-evidence retrieval. |
| MNanoBEIR | fever (NanoBEIR-no) | multilingual | 46.0 | 1166.5 | Core | Claim-to-evidence retrieval. |
| MNanoBEIR | fever (NanoBEIR-pt) | pt | 49.0 | 1245.7 | Core | Claim-to-evidence retrieval. |
| MNanoBEIR | fever (NanoBEIR-sr) | multilingual | 46.1 | 1184.6 | Core | Claim-to-evidence retrieval. |
| MNanoBEIR | fever (NanoBEIR-sv) | sv | 44.6 | 1166.7 | Core | Claim-to-evidence retrieval. |
| MNanoBEIR | fever (NanoBEIR-th) | th | 46.9 | 1084.7 | Core | Claim-to-evidence retrieval. |
| MNanoBEIR | fever (NanoBEIR-vi) | vi | 53.1 | 1248.5 | Core | Claim-to-evidence retrieval. |
| MNanoBEIR | fiqa2018 (NanoBEIR-ar) | ar | 53.6 | 796.4 | Core | Information need to relevant financial answer. |
| MNanoBEIR | fiqa2018 (NanoBEIR-de) | de | 74.6 | 1052.2 | Core | Information need to relevant financial answer. |
| MNanoBEIR | fiqa2018 (NanoBEIR-en) | en | 58.5 | 904.9 | Core | Information need to relevant financial answer. |
| MNanoBEIR | fiqa2018 (NanoBEIR-es) | es | 70.3 | 993.6 | Core | Information need to relevant financial answer. |
| MNanoBEIR | fiqa2018 (NanoBEIR-fr) | fr | 82.2 | 1072.0 | Core | Information need to relevant financial answer. |
| MNanoBEIR | fiqa2018 (NanoBEIR-it) | it | 74.6 | 1005.1 | Core | Information need to relevant financial answer. |
| MNanoBEIR | fiqa2018 (NanoBEIR-ja) | ja | 28.5 | 428.0 | Core | Information need to relevant financial answer. |
| MNanoBEIR | fiqa2018 (NanoBEIR-ko) | ko | 29.6 | 493.1 | Core | Information need to relevant financial answer. |
| MNanoBEIR | fiqa2018 (NanoBEIR-no) | multilingual | 64.7 | 910.8 | Core | Information need to relevant financial answer. |
| MNanoBEIR | fiqa2018 (NanoBEIR-pt) | pt | 71.9 | 972.5 | Core | Information need to relevant financial answer. |
| MNanoBEIR | fiqa2018 (NanoBEIR-sr) | multilingual | 63.8 | 914.4 | Core | Information need to relevant financial answer. |
| MNanoBEIR | fiqa2018 (NanoBEIR-sv) | sv | 62.2 | 925.7 | Core | Information need to relevant financial answer. |
| MNanoBEIR | fiqa2018 (NanoBEIR-th) | th | 55.2 | 779.2 | Core | Information need to relevant financial answer. |
| MNanoBEIR | fiqa2018 (NanoBEIR-vi) | vi | 66.5 | 936.1 | Core | Information need to relevant financial answer. |
| MNanoBEIR | hotpotqa (NanoBEIR-ar) | ar | 72.8 | 410.0 | Core | Question to supporting passage. |
| MNanoBEIR | hotpotqa (NanoBEIR-de) | de | 99.8 | 386.2 | Core | Question to supporting passage. |
| MNanoBEIR | hotpotqa (NanoBEIR-en) | en | 88.3 | 349.6 | Core | Question to supporting passage. |
| MNanoBEIR | hotpotqa (NanoBEIR-es) | es | 93.2 | 391.0 | Core | Question to supporting passage. |
| MNanoBEIR | hotpotqa (NanoBEIR-fr) | fr | 98.6 | 389.2 | Core | Question to supporting passage. |
| MNanoBEIR | hotpotqa (NanoBEIR-it) | it | 93.4 | 378.3 | Core | Question to supporting passage. |
| MNanoBEIR | hotpotqa (NanoBEIR-ja) | ja | 46.6 | 184.7 | Core | Question to supporting passage. |
| MNanoBEIR | hotpotqa (NanoBEIR-ko) | ko | 49.5 | 197.1 | Core | Question to supporting passage. |
| MNanoBEIR | hotpotqa (NanoBEIR-no) | multilingual | 87.3 | 341.7 | Core | Question to supporting passage. |
| MNanoBEIR | hotpotqa (NanoBEIR-pt) | pt | 91.1 | 377.5 | Core | Question to supporting passage. |
| MNanoBEIR | hotpotqa (NanoBEIR-sr) | multilingual | 86.5 | 353.6 | Core | Question to supporting passage. |
| MNanoBEIR | hotpotqa (NanoBEIR-sv) | sv | 86.3 | 349.5 | Core | Question to supporting passage. |
| MNanoBEIR | hotpotqa (NanoBEIR-th) | th | 79.7 | 330.7 | Core | Question to supporting passage. |
| MNanoBEIR | hotpotqa (NanoBEIR-vi) | vi | 90.7 | 374.2 | Core | Question to supporting passage. |
| MNanoBEIR | msmarco (NanoBEIR-ar) | ar | 31.0 | 275.6 | Core | Web query to relevant passage. |
| MNanoBEIR | msmarco (NanoBEIR-de) | de | 41.0 | 363.7 | Core | Web query to relevant passage. |
| MNanoBEIR | msmarco (NanoBEIR-en) | en | 32.2 | 330.2 | Core | Web query to relevant passage. |
| MNanoBEIR | msmarco (NanoBEIR-es) | es | 42.1 | 359.9 | Core | Web query to relevant passage. |
| MNanoBEIR | msmarco (NanoBEIR-fr) | fr | 44.6 | 373.7 | Core | Web query to relevant passage. |
| MNanoBEIR | msmarco (NanoBEIR-it) | it | 42.0 | 356.6 | Core | Web query to relevant passage. |
| MNanoBEIR | msmarco (NanoBEIR-ja) | ja | 26.7 | 150.4 | Core | Web query to relevant passage. |
| MNanoBEIR | msmarco (NanoBEIR-ko) | ko | 19.1 | 169.2 | Core | Web query to relevant passage. |
| MNanoBEIR | msmarco (NanoBEIR-no) | multilingual | 35.0 | 331.3 | Core | Web query to relevant passage. |
| MNanoBEIR | msmarco (NanoBEIR-pt) | pt | 40.2 | 344.7 | Core | Web query to relevant passage. |
| MNanoBEIR | msmarco (NanoBEIR-sr) | multilingual | 35.6 | 331.1 | Core | Web query to relevant passage. |
| MNanoBEIR | msmarco (NanoBEIR-sv) | sv | 33.6 | 321.2 | Core | Web query to relevant passage. |
| MNanoBEIR | msmarco (NanoBEIR-th) | th | 32.1 | 293.9 | Core | Web query to relevant passage. |
| MNanoBEIR | msmarco (NanoBEIR-vi) | vi | 34.9 | 335.0 | Core | Web query to relevant passage. |
| MNanoBEIR | nfcorpus (NanoBEIR-ar) | ar | 22.3 | 1408.2 | Core | Information need to relevant biomedical document. |
| MNanoBEIR | nfcorpus (NanoBEIR-de) | multilingual | 29.1 | 1731.9 | Core | Information need to relevant biomedical document. |
| MNanoBEIR | nfcorpus (NanoBEIR-en) | en | 21.0 | 1512.7 | Core | Information need to relevant biomedical document. |
| MNanoBEIR | nfcorpus (NanoBEIR-es) | es | 27.1 | 1732.4 | Core | Information need to relevant biomedical document. |
| MNanoBEIR | nfcorpus (NanoBEIR-fr) | multilingual | 29.1 | 1810.7 | Core | Information need to relevant biomedical document. |
| MNanoBEIR | nfcorpus (NanoBEIR-it) | multilingual | 28.5 | 1725.5 | Core | Information need to relevant biomedical document. |
| MNanoBEIR | nfcorpus (NanoBEIR-ja) | multilingual | 11.2 | 655.8 | Core | Information need to relevant biomedical document. |
| MNanoBEIR | nfcorpus (NanoBEIR-ko) | ko | 10.8 | 752.7 | Core | Information need to relevant biomedical document. |
| MNanoBEIR | nfcorpus (NanoBEIR-no) | multilingual | 24.2 | 1494.7 | Core | Information need to relevant biomedical document. |
| MNanoBEIR | nfcorpus (NanoBEIR-pt) | multilingual | 26.9 | 1650.1 | Core | Information need to relevant biomedical document. |
| MNanoBEIR | nfcorpus (NanoBEIR-sr) | multilingual | 23.1 | 1522.7 | Core | Information need to relevant biomedical document. |
| MNanoBEIR | nfcorpus (NanoBEIR-sv) | multilingual | 23.2 | 1494.0 | Core | Information need to relevant biomedical document. |
| MNanoBEIR | nfcorpus (NanoBEIR-th) | th | 22.6 | 1387.4 | Core | Information need to relevant biomedical document. |
| MNanoBEIR | nfcorpus (NanoBEIR-vi) | multilingual | 25.3 | 1565.9 | Core | Information need to relevant biomedical document. |
| MNanoBEIR | nq (NanoBEIR-ar) | ar | 40.2 | 447.3 | Core | Question to supporting passage. |
| MNanoBEIR | nq (NanoBEIR-de) | de | 55.4 | 588.5 | Core | Question to supporting passage. |
| MNanoBEIR | nq (NanoBEIR-en) | en | 47.0 | 525.6 | Core | Question to supporting passage. |
| MNanoBEIR | nq (NanoBEIR-es) | es | 53.4 | 574.3 | Core | Question to supporting passage. |
| MNanoBEIR | nq (NanoBEIR-fr) | fr | 58.7 | 588.8 | Core | Question to supporting passage. |
| MNanoBEIR | nq (NanoBEIR-it) | it | 54.3 | 575.9 | Core | Question to supporting passage. |
| MNanoBEIR | nq (NanoBEIR-ja) | ja | 42.6 | 244.0 | Core | Question to supporting passage. |
| MNanoBEIR | nq (NanoBEIR-ko) | ko | 29.3 | 274.2 | Core | Question to supporting passage. |
| MNanoBEIR | nq (NanoBEIR-no) | multilingual | 48.0 | 522.0 | Core | Question to supporting passage. |
| MNanoBEIR | nq (NanoBEIR-pt) | pt | 51.6 | 549.8 | Core | Question to supporting passage. |
| MNanoBEIR | nq (NanoBEIR-sr) | multilingual | 45.6 | 514.5 | Core | Question to supporting passage. |
| MNanoBEIR | nq (NanoBEIR-sv) | sv | 46.0 | 526.1 | Core | Question to supporting passage. |
| MNanoBEIR | nq (NanoBEIR-th) | th | 40.8 | 473.6 | Core | Question to supporting passage. |
| MNanoBEIR | nq (NanoBEIR-vi) | vi | 47.9 | 541.0 | Core | Question to supporting passage. |
| MNanoBEIR | quoraretrieval (NanoBEIR-ar) | ar | 43.2 | 58.2 | No | Symmetric duplicate-question retrieval. |
| MNanoBEIR | quoraretrieval (NanoBEIR-de) | de | 55.7 | 65.1 | No | Symmetric duplicate-question retrieval. |
| MNanoBEIR | quoraretrieval (NanoBEIR-en) | en | 48.0 | 54.8 | No | Symmetric duplicate-question retrieval. |
| MNanoBEIR | quoraretrieval (NanoBEIR-es) | es | 55.2 | 64.3 | No | Symmetric duplicate-question retrieval. |
| MNanoBEIR | quoraretrieval (NanoBEIR-fr) | fr | 61.2 | 71.5 | No | Symmetric duplicate-question retrieval. |
| MNanoBEIR | quoraretrieval (NanoBEIR-it) | it | 52.8 | 64.4 | No | Symmetric duplicate-question retrieval. |
| MNanoBEIR | quoraretrieval (NanoBEIR-ja) | ja | 27.2 | 32.2 | No | Symmetric duplicate-question retrieval. |
| MNanoBEIR | quoraretrieval (NanoBEIR-ko) | ko | 28.7 | 32.8 | No | Symmetric duplicate-question retrieval. |
| MNanoBEIR | quoraretrieval (NanoBEIR-no) | multilingual | 50.6 | 57.9 | No | Symmetric duplicate-question retrieval. |
| MNanoBEIR | quoraretrieval (NanoBEIR-pt) | pt | 54.2 | 62.5 | No | Symmetric duplicate-question retrieval. |
| MNanoBEIR | quoraretrieval (NanoBEIR-sr) | multilingual | 49.3 | 58.1 | No | Symmetric duplicate-question retrieval. |
| MNanoBEIR | quoraretrieval (NanoBEIR-sv) | sv | 48.5 | 57.2 | No | Symmetric duplicate-question retrieval. |
| MNanoBEIR | quoraretrieval (NanoBEIR-th) | th | 46.9 | 53.7 | No | Symmetric duplicate-question retrieval. |
| MNanoBEIR | quoraretrieval (NanoBEIR-vi) | vi | 57.3 | 62.7 | No | Symmetric duplicate-question retrieval. |
| MNanoBEIR | scidocs (NanoBEIR-ar) | multilingual | 65.0 | 823.4 | No | Citation or related-document retrieval. |
| MNanoBEIR | scidocs (NanoBEIR-de) | multilingual | 82.4 | 1071.1 | No | Citation or related-document retrieval. |
| MNanoBEIR | scidocs (NanoBEIR-en) | en | 72.8 | 1093.8 | No | Citation or related-document retrieval. |
| MNanoBEIR | scidocs (NanoBEIR-es) | multilingual | 87.5 | 1078.0 | No | Citation or related-document retrieval. |
| MNanoBEIR | scidocs (NanoBEIR-fr) | multilingual | 93.3 | 1115.3 | No | Citation or related-document retrieval. |
| MNanoBEIR | scidocs (NanoBEIR-it) | multilingual | 89.5 | 1062.0 | No | Citation or related-document retrieval. |
| MNanoBEIR | scidocs (NanoBEIR-ja) | ja | 30.5 | 399.6 | No | Citation or related-document retrieval. |
| MNanoBEIR | scidocs (NanoBEIR-ko) | ko | 32.1 | 535.7 | No | Citation or related-document retrieval. |
| MNanoBEIR | scidocs (NanoBEIR-no) | multilingual | 75.0 | 934.2 | No | Citation or related-document retrieval. |
| MNanoBEIR | scidocs (NanoBEIR-pt) | multilingual | 83.0 | 1028.8 | No | Citation or related-document retrieval. |
| MNanoBEIR | scidocs (NanoBEIR-sr) | multilingual | 77.1 | 944.5 | No | Citation or related-document retrieval. |
| MNanoBEIR | scidocs (NanoBEIR-sv) | multilingual | 74.7 | 941.3 | No | Citation or related-document retrieval. |
| MNanoBEIR | scidocs (NanoBEIR-th) | multilingual | 69.1 | 820.4 | No | Citation or related-document retrieval. |
| MNanoBEIR | scidocs (NanoBEIR-vi) | vi | 76.1 | 952.5 | No | Citation or related-document retrieval. |
| MNanoBEIR | scifact (NanoBEIR-ar) | ar | 89.0 | 1316.8 | Core | Scientific claim to evidence. |
| MNanoBEIR | scifact (NanoBEIR-de) | de | 110.6 | 1647.9 | Core | Scientific claim to evidence. |
| MNanoBEIR | scifact (NanoBEIR-en) | en | 95.8 | 1431.2 | Core | Scientific claim to evidence. |
| MNanoBEIR | scifact (NanoBEIR-es) | es | 113.6 | 1644.2 | Core | Scientific claim to evidence. |
| MNanoBEIR | scifact (NanoBEIR-fr) | fr | 119.1 | 1711.1 | Core | Scientific claim to evidence. |
| MNanoBEIR | scifact (NanoBEIR-it) | it | 113.7 | 1631.5 | Core | Scientific claim to evidence. |
| MNanoBEIR | scifact (NanoBEIR-ja) | ja | 40.6 | 633.1 | Core | Scientific claim to evidence. |
| MNanoBEIR | scifact (NanoBEIR-ko) | ko | 46.3 | 723.6 | Core | Scientific claim to evidence. |
| MNanoBEIR | scifact (NanoBEIR-no) | multilingual | 96.2 | 1424.5 | Core | Scientific claim to evidence. |
| MNanoBEIR | scifact (NanoBEIR-pt) | pt | 105.9 | 1562.7 | Core | Scientific claim to evidence. |
| MNanoBEIR | scifact (NanoBEIR-sr) | multilingual | 96.4 | 1433.9 | Core | Scientific claim to evidence. |
| MNanoBEIR | scifact (NanoBEIR-sv) | sv | 95.1 | 1429.1 | Core | Scientific claim to evidence. |
| MNanoBEIR | scifact (NanoBEIR-th) | th | 92.7 | 1328.8 | Core | Scientific claim to evidence. |
| MNanoBEIR | scifact (NanoBEIR-vi) | vi | 100.1 | 1489.6 | Core | Scientific claim to evidence. |
| MNanoBEIR | touche2020 (NanoBEIR-ar) | ar | 40.7 | 1803.6 | Core | Topic to relevant argument document. |
| MNanoBEIR | touche2020 (NanoBEIR-de) | de | 51.0 | 2456.6 | Core | Topic to relevant argument document. |
| MNanoBEIR | touche2020 (NanoBEIR-en) | en | 43.4 | 2142.6 | Core | Topic to relevant argument document. |
| MNanoBEIR | touche2020 (NanoBEIR-es) | es | 53.9 | 2360.8 | Core | Topic to relevant argument document. |
| MNanoBEIR | touche2020 (NanoBEIR-fr) | fr | 59.6 | 2488.2 | Core | Topic to relevant argument document. |
| MNanoBEIR | touche2020 (NanoBEIR-it) | it | 56.3 | 2352.8 | Core | Topic to relevant argument document. |
| MNanoBEIR | touche2020 (NanoBEIR-ja) | ja | 21.7 | 928.5 | Core | Topic to relevant argument document. |
| MNanoBEIR | touche2020 (NanoBEIR-ko) | ko | 21.7 | 1032.8 | Core | Topic to relevant argument document. |
| MNanoBEIR | touche2020 (NanoBEIR-no) | multilingual | 39.8 | 2114.4 | Core | Topic to relevant argument document. |
| MNanoBEIR | touche2020 (NanoBEIR-pt) | pt | 49.1 | 2264.9 | Core | Topic to relevant argument document. |
| MNanoBEIR | touche2020 (NanoBEIR-sr) | multilingual | 55.1 | 2095.8 | Core | Topic to relevant argument document. |
| MNanoBEIR | touche2020 (NanoBEIR-sv) | sv | 41.0 | 2158.8 | Core | Topic to relevant argument document. |
| MNanoBEIR | touche2020 (NanoBEIR-th) | th | 46.3 | 1438.1 | Core | Topic to relevant argument document. |
| MNanoBEIR | touche2020 (NanoBEIR-vi) | vi | 52.9 | 1712.7 | Core | Topic to relevant argument document. |
| NanoBIRCO | NanoBIRCOArguAna | en | 1124.0 | 1140.1 | Specialized | Complex-objective retrieval; valid for instructed reranking but not plain topical relevance. |
| NanoBIRCO | NanoBIRCOClinicalTrial | en | 497.0 | 1174.3 | Specialized | Complex-objective retrieval; valid for instructed reranking but not plain topical relevance. |
| NanoBIRCO | NanoBIRCODorisMae | en | 995.5 | 1220.3 | Specialized | Complex-objective retrieval; valid for instructed reranking but not plain topical relevance. |
| NanoBIRCO | NanoBIRCORelic | en | 1016.3 | 477.3 | Specialized | Complex-objective retrieval; valid for instructed reranking but not plain topical relevance. |
| NanoBIRCO | NanoBIRCOWTB | en | 811.3 | 1091.2 | Specialized | Complex-objective retrieval; valid for instructed reranking but not plain topical relevance. |
| NanoBRIGHT | NanoBrightAops | en | 319.6 | 549.1 | Specialized | Reasoning-similarity retrieval; positives need not answer the query directly. |
| NanoBRIGHT | NanoBrightBiology | en | 523.0 | 473.9 | Specialized | Reasoning-similarity retrieval; positives need not answer the query directly. |
| NanoBRIGHT | NanoBrightBiologyLong | en | 523.0 | 36923.7 | Specialized | Reasoning-similarity retrieval; positives need not answer the query directly. |
| NanoBRIGHT | NanoBrightEarthScience | en | 476.7 | 716.2 | Specialized | Reasoning-similarity retrieval; positives need not answer the query directly. |
| NanoBRIGHT | NanoBrightEarthScienceLong | en | 476.7 | 70649.6 | Specialized | Reasoning-similarity retrieval; positives need not answer the query directly. |
| NanoBRIGHT | NanoBrightEconomics | en | 739.6 | 532.6 | Specialized | Reasoning-similarity retrieval; positives need not answer the query directly. |
| NanoBRIGHT | NanoBrightEconomicsLong | en | 739.6 | 38616.0 | Specialized | Reasoning-similarity retrieval; positives need not answer the query directly. |
| NanoBRIGHT | NanoBrightLeetcode | en | 1459.3 | 1079.6 | Specialized | Reasoning-similarity retrieval; positives need not answer the query directly. |
| NanoBRIGHT | NanoBrightPony | en | 389.0 | 306.5 | Specialized | Reasoning-similarity retrieval; positives need not answer the query directly. |
| NanoBRIGHT | NanoBrightPonyLong | en | 389.0 | 3553.1 | Specialized | Reasoning-similarity retrieval; positives need not answer the query directly. |
| NanoBRIGHT | NanoBrightPsychology | en | 693.2 | 504.5 | Specialized | Reasoning-similarity retrieval; positives need not answer the query directly. |
| NanoBRIGHT | NanoBrightPsychologyLong | en | 693.2 | 40097.5 | Specialized | Reasoning-similarity retrieval; positives need not answer the query directly. |
| NanoBRIGHT | NanoBrightRobotics | en | 2179.4 | 382.4 | Specialized | Reasoning-similarity retrieval; positives need not answer the query directly. |
| NanoBRIGHT | NanoBrightRoboticsLong | en | 2179.4 | 35895.2 | Specialized | Reasoning-similarity retrieval; positives need not answer the query directly. |
| NanoBRIGHT | NanoBrightStackoverflow | en | 1293.0 | 1120.6 | Specialized | Reasoning-similarity retrieval; positives need not answer the query directly. |
| NanoBRIGHT | NanoBrightStackoverflowLong | en | 1293.0 | 77578.4 | Specialized | Reasoning-similarity retrieval; positives need not answer the query directly. |
| NanoBRIGHT | NanoBrightSustainableLiving | en | 682.8 | 733.6 | Specialized | Reasoning-similarity retrieval; positives need not answer the query directly. |
| NanoBRIGHT | NanoBrightSustainableLivingLong | en | 682.8 | 38204.3 | Specialized | Reasoning-similarity retrieval; positives need not answer the query directly. |
| NanoBRIGHT | NanoBrightTheoremQAQuestions | en | 425.6 | 543.4 | Specialized | Reasoning-similarity retrieval; positives need not answer the query directly. |
| NanoBRIGHT | NanoBrightTheoremQATheorems | en | 415.6 | 401.1 | Specialized | Reasoning-similarity retrieval; positives need not answer the query directly. |
| NanoBuiltBench | NanoBuiltBench | en | 102.1 | 341.7 | No | Built-environment entity matching rather than general document relevance. |
| NanoBuiltBench | NanoBuiltBenchReranking | en | 138.3 | 309.0 | No | Built-environment entity matching rather than general document relevance. |
| NanoCMTEB | cmedqa | zh | 52.0 | 157.6 | Extended | Question or search query to relevant answer/document. |
| NanoCMTEB | covid | zh | 25.7 | 409.3 | Extended | Question or search query to relevant answer/document. |
| NanoCMTEB | du | zh | 9.1 | 397.4 | Extended | Question or search query to relevant answer/document. |
| NanoCMTEB | ecom | multilingual | 6.9 | 33.1 | No | Product or media matching. |
| NanoCMTEB | medical | zh | 18.1 | 119.7 | Extended | Question or search query to relevant answer/document. |
| NanoCMTEB | mmarco | zh | 10.4 | 113.9 | Extended | Question or search query to relevant answer/document. |
| NanoCMTEB | t2 | zh | 10.7 | 913.5 | Extended | Question or search query to relevant answer/document. |
| NanoCMTEB | video | zh | 7.1 | 30.5 | No | Product or media matching. |
| NanoChemTEB | NanoChemHotpotQA | en | 104.2 | 402.4 | Core | Chemistry question to supporting passage or scientific document. |
| NanoChemTEB | NanoChemNQ | en | 54.0 | 481.2 | Core | Chemistry question to supporting passage or scientific document. |
| NanoChemTEB | NanoChemRxiv | en | 111.7 | 1079.1 | Core | Chemistry question to supporting passage or scientific document. |
| NanoCoIR | NanoApps | en | 1675.4 | 573.1 | Core | Natural search/programming query to relevant code or answer. |
| NanoCoIR | NanoCodeFeedbackMT | en | 4468.6 | 1468.2 | Specialized | Prompt and draft response to code-feedback response. |
| NanoCoIR | NanoCodeFeedbackST | en | 730.5 | 1538.7 | Specialized | Prompt and draft response to code-feedback response. |
| NanoCoIR | NanoCodeSearchNet | en | 636.3 | 86.1 | Specialized | Code-to-docstring or code-fragment matching. |
| NanoCoIR | NanoCodeSearchNetCCR | en | 372.8 | 158.4 | Specialized | Code-to-docstring or code-fragment matching. |
| NanoCoIR | NanoCodeTransOceanContest | en | 1009.6 | 1528.7 | Specialized | Code-to-code translation or implementation matching. |
| NanoCoIR | NanoCodeTransOceanDL | en | 2153.8 | 1645.0 | Specialized | Code-to-code translation or implementation matching. |
| NanoCoIR | NanoCosQA | en | 36.1 | 307.6 | Core | Natural search/programming query to relevant code or answer. |
| NanoCoIR | NanoStackOverflowQA | en | 1361.8 | 1218.1 | Core | Natural search/programming query to relevant code or answer. |
| NanoCoIR | NanoSyntheticText2SQL | en | 102.9 | 130.6 | Core | Natural search/programming query to relevant code or answer. |
| NanoCodeRAG | NanoCodeRAGLibraryDocumentationSolutions | en | 397.4 | 2045.7 | Core | Programming query to relevant code, tutorial, documentation, or answer. |
| NanoCodeRAG | NanoCodeRAGOnlineTutorials | en | 51.9 | 5722.5 | Core | Programming query to relevant code, tutorial, documentation, or answer. |
| NanoCodeRAG | NanoCodeRAGProgrammingSolutions | en | 78.3 | 189.1 | Core | Programming query to relevant code, tutorial, documentation, or answer. |
| NanoCodeRAG | NanoCodeRAGStackoverflowPosts | en | 209.8 | 4735.0 | Core | Programming query to relevant code, tutorial, documentation, or answer. |
| NanoDAPFAM | NanoDAPFAMAllTitlAbsClmToTitlAbs | en | 8339.5 | 777.9 | No | Patent title/abstract/claim relation and citation-style matching. |
| NanoDAPFAM | NanoDAPFAMAllTitlAbsClmToTitlAbsClm | en | 8339.5 | 7229.1 | No | Patent title/abstract/claim relation and citation-style matching. |
| NanoDAPFAM | NanoDAPFAMAllTitlAbsToTitlAbs | en | 776.0 | 778.0 | No | Patent title/abstract/claim relation and citation-style matching. |
| NanoDAPFAM | NanoDAPFAMAllTitlAbsToTitlAbsClm | en | 776.0 | 7230.6 | No | Patent title/abstract/claim relation and citation-style matching. |
| NanoDAPFAM | NanoDAPFAMInTitlAbsClmToTitlAbs | en | 8405.5 | 777.9 | No | Patent title/abstract/claim relation and citation-style matching. |
| NanoDAPFAM | NanoDAPFAMInTitlAbsClmToTitlAbsClm | en | 8405.5 | 7225.2 | No | Patent title/abstract/claim relation and citation-style matching. |
| NanoDAPFAM | NanoDAPFAMInTitlAbsToTitlAbs | en | 771.3 | 777.7 | No | Patent title/abstract/claim relation and citation-style matching. |
| NanoDAPFAM | NanoDAPFAMInTitlAbsToTitlAbsClm | en | 771.3 | 7226.4 | No | Patent title/abstract/claim relation and citation-style matching. |
| NanoDAPFAM | NanoDAPFAMOutTitlAbsClmToTitlAbs | en | 9315.7 | 777.9 | No | Patent title/abstract/claim relation and citation-style matching. |
| NanoDAPFAM | NanoDAPFAMOutTitlAbsClmToTitlAbsClm | en | 9315.7 | 7257.2 | No | Patent title/abstract/claim relation and citation-style matching. |
| NanoDAPFAM | NanoDAPFAMOutTitlAbsToTitlAbs | en | 786.6 | 777.9 | No | Patent title/abstract/claim relation and citation-style matching. |
| NanoDAPFAM | NanoDAPFAMOutTitlAbsToTitlAbsClm | en | 786.6 | 7257.2 | No | Patent title/abstract/claim relation and citation-style matching. |
| NanoFaMTEB-v2 | argu_ana_fa | fa | 1101.0 | 973.1 | Specialized | Argument-to-counterargument retrieval. |
| NanoFaMTEB-v2 | fever_fa | fa | 47.1 | 523.3 | Core | Question, claim, or search query to relevant answer/document. |
| NanoFaMTEB-v2 | fi_qa2018_fa | fa | 65.8 | 763.5 | Core | Question, claim, or search query to relevant answer/document. |
| NanoFaMTEB-v2 | hotpot_qa_fa | fa | 87.9 | 394.9 | Core | Question, claim, or search query to relevant answer/document. |
| NanoFaMTEB-v2 | miracl_fa | fa | 40.0 | 413.5 | Core | Question, claim, or search query to relevant answer/document. |
| NanoFaMTEB-v2 | msmarco_fa | fa | 31.5 | 326.2 | Core | Question, claim, or search query to relevant answer/document. |
| NanoFaMTEB-v2 | neu_clir2023_fas | fa | 65.8 | 3121.9 | Core | Question, claim, or search query to relevant answer/document. |
| NanoFaMTEB-v2 | nq_fa | fa | 46.7 | 556.8 | Core | Question, claim, or search query to relevant answer/document. |
| NanoFaMTEB-v2 | persian_web_document | fa | 16.4 | 228.3 | Core | Question, claim, or search query to relevant answer/document. |
| NanoFaMTEB-v2 | quora_fa | fa | 48.7 | 60.8 | No | Symmetric duplicate-question retrieval. |
| NanoFaMTEB-v2 | sci_fact_fa | fa | 84.5 | 1361.3 | Core | Question, claim, or search query to relevant answer/document. |
| NanoFaMTEB-v2 | scidocs_fa | fa | 61.6 | 1092.0 | No | Citation or related-document retrieval. |
| NanoFaMTEB-v2 | syn_per_chatbot_ragfaq | fa | 597.4 | 145.7 | Core | Question, claim, or search query to relevant answer/document. |
| NanoFaMTEB-v2 | syn_per_qa | fa | 59.8 | 306.2 | Core | Question, claim, or search query to relevant answer/document. |
| NanoFaMTEB-v2 | treccovid_fa | fa | 64.6 | 1210.7 | Core | Question, claim, or search query to relevant answer/document. |
| NanoFaMTEB-v2 | web_faq_fas | fa | 48.0 | 209.6 | Core | Question, claim, or search query to relevant answer/document. |
| NanoFaMTEB-v2 | wikipedia_multilingual_fa | fa | 49.2 | 352.9 | Core | Question, claim, or search query to relevant answer/document. |
| NanoIFIR | NanoIFIRAila | en | 2890.1 | 19998.1 | Specialized | Legal case-to-case relevance. |
| NanoIFIR | NanoIFIRCds | en | 225.2 | 1630.2 | Core | Question, claim, or information need to relevant domain document. |
| NanoIFIR | NanoIFIRFiQA | en | 65.8 | 791.9 | Core | Question, claim, or information need to relevant domain document. |
| NanoIFIR | NanoIFIRFire | en | 3283.8 | 27167.7 | Specialized | Legal case-to-case relevance. |
| NanoIFIR | NanoIFIRNFCorpus | en | 37.8 | 1589.5 | Core | Question, claim, or information need to relevant domain document. |
| NanoIFIR | NanoIFIRPm | en | 145.7 | 2244.9 | Core | Question, claim, or information need to relevant domain document. |
| NanoIFIR | NanoIFIRScifact | en | 73.6 | 1452.6 | Core | Question, claim, or information need to relevant domain document. |
| NanoIndicQA | as | as | 55.3 | 1401.3 | Core | Question to supporting passage. |
| NanoIndicQA | bn | bn | 52.1 | 2196.0 | Core | Question to supporting passage. |
| NanoIndicQA | gu | gu | 61.0 | 960.5 | Core | Question to supporting passage. |
| NanoIndicQA | hi | hi | 56.9 | 2550.8 | Core | Question to supporting passage. |
| NanoIndicQA | kn | kn | 53.3 | 882.7 | Core | Question to supporting passage. |
| NanoIndicQA | ml | ml | 81.5 | 2522.6 | Core | Question to supporting passage. |
| NanoIndicQA | mr | mr | 59.9 | 1711.7 | Core | Question to supporting passage. |
| NanoIndicQA | or | or | 57.2 | 801.9 | Core | Question to supporting passage. |
| NanoIndicQA | pa | pa | 63.5 | 1423.5 | Core | Question to supporting passage. |
| NanoIndicQA | ta | ta | 56.3 | 2288.3 | Core | Question to supporting passage. |
| NanoIndicQA | te | te | 65.0 | 2936.2 | Core | Question to supporting passage. |
| NanoJMTEB-v2 | ja_cwir | ja | 33.8 | 187.0 | Extended | Japanese question or search query to relevant passage/document. |
| NanoJMTEB-v2 | ja_gov_faqs | ja | 60.0 | 193.4 | Extended | Japanese question or search query to relevant passage/document. |
| NanoJMTEB-v2 | jaqket | ja | 53.0 | 4382.4 | Extended | Japanese question or search query to relevant passage/document. |
| NanoJMTEB-v2 | mintaka_ja | ja | 35.2 | 9.2 | No | Short-answer/entity selection rather than document relevance. |
| NanoJMTEB-v2 | miracl_ja | ja | 17.5 | 180.5 | Extended | Japanese question or search query to relevant passage/document. |
| NanoJMTEB-v2 | mr_tidy_japanese | ja | 18.4 | 291.0 | Extended | Japanese question or search query to relevant passage/document. |
| NanoJMTEB-v2 | multi_long_doc_ja | ja | 61.6 | 14479.4 | Extended | Japanese question or search query to relevant passage/document. |
| NanoJMTEB-v2 | nlpjournal_abs_article | ja | 494.5 | 28330.4 | No | Citation or title/abstract related-document matching. |
| NanoJMTEB-v2 | nlpjournal_abs_intro | ja | 494.5 | 2148.0 | No | Citation or title/abstract related-document matching. |
| NanoJMTEB-v2 | nlpjournal_title_abs | ja | 27.0 | 461.5 | No | Citation or title/abstract related-document matching. |
| NanoJMTEB-v2 | nlpjournal_title_intro | ja | 27.0 | 2148.0 | No | Citation or title/abstract related-document matching. |
| NanoLaw | NanoAILACasedocs | en | 3038.4 | 26947.3 | Specialized | Legal case-to-case relevance. |
| NanoLaw | NanoAILAStatutes | en | 3038.4 | 1972.6 | Core | Legal question, case, or statement to relevant statute, policy, or passage. |
| NanoLaw | NanoGerDaLIRSmall | de | 889.9 | 19706.8 | Specialized | Legal case-to-case relevance. |
| NanoLaw | NanoLeCaRDv2 | zh | 4259.4 | 7231.8 | Specialized | Legal case-to-case relevance. |
| NanoLaw | NanoLegalBenchConsumerContractsQA | en | 97.2 | 2743.3 | Core | Legal question, case, or statement to relevant statute, policy, or passage. |
| NanoLaw | NanoLegalBenchCorporateLobbying | en | 179.7 | 1157.2 | Core | Legal question, case, or statement to relevant statute, policy, or passage. |
| NanoLaw | NanoLegalQuAD | de | 71.9 | 19481.0 | Core | Legal question, case, or statement to relevant statute, policy, or passage. |
| NanoLaw | NanoLegalSummarization | en | 103.1 | 606.2 | Core | Legal question, case, or statement to relevant statute, policy, or passage. |
| NanoLongEmbed | Nano2WikiMultihopQA | en | 67.5 | 37445.6 | Core | Question to relevant long document. |
| NanoLongEmbed | NanoNarrativeQA | en | 49.3 | 326753.0 | Core | Question to relevant long document. |
| NanoLongEmbed | NanoNeedle | en | 59.0 | 35246.1 | Specialized | Synthetic needle/passkey lookup in a long context. |
| NanoLongEmbed | NanoPasskey | en | 37.8 | 28956.7 | Specialized | Synthetic needle/passkey lookup in a long context. |
| NanoLongEmbed | NanoQMSum | en | 446.3 | 53335.8 | Specialized | Summary or description to source transcript/document. |
| NanoLongEmbed | NanoSummScreenFD | en | 600.7 | 30854.3 | Specialized | Summary or description to source transcript/document. |
| NanoMIRACL | ar | ar | 30.1 | 680.5 | Core | Question or search query to relevant passage. |
| NanoMIRACL | bn | bn | 47.2 | 717.9 | Core | Question or search query to relevant passage. |
| NanoMIRACL | de | de | 45.6 | 629.7 | Core | Question or search query to relevant passage. |
| NanoMIRACL | en | en | 40.1 | 760.2 | Core | Question or search query to relevant passage. |
| NanoMIRACL | es | es | 48.2 | 612.5 | Core | Question or search query to relevant passage. |
| NanoMIRACL | fa | fa | 40.0 | 489.7 | Core | Question or search query to relevant passage. |
| NanoMIRACL | fi | fi | 37.3 | 653.4 | Core | Question or search query to relevant passage. |
| NanoMIRACL | fr | fr | 43.3 | 556.7 | Core | Question or search query to relevant passage. |
| NanoMIRACL | hi | hi | 54.8 | 580.4 | Core | Question or search query to relevant passage. |
| NanoMIRACL | id | id | 38.5 | 676.2 | Core | Question or search query to relevant passage. |
| NanoMIRACL | ja | ja | 17.5 | 297.9 | Core | Question or search query to relevant passage. |
| NanoMIRACL | ko | ko | 21.7 | 287.3 | Core | Question or search query to relevant passage. |
| NanoMIRACL | ru | ru | 45.5 | 783.4 | Core | Question or search query to relevant passage. |
| NanoMIRACL | sw | multilingual | 38.3 | 532.8 | Core | Question or search query to relevant passage. |
| NanoMIRACL | te | te | 38.5 | 787.5 | Core | Question or search query to relevant passage. |
| NanoMIRACL | th | th | 43.6 | 595.2 | Core | Question or search query to relevant passage. |
| NanoMIRACL | yo | multilingual | 37.7 | 397.2 | Core | Question or search query to relevant passage. |
| NanoMIRACL | zh | zh | 10.9 | 179.7 | Core | Question or search query to relevant passage. |
| NanoMLDR | ar | ar | 71.1 | 12006.8 | Core | Question to relevant long document; some corpus samples are noisy. |
| NanoMLDR | de | de | 81.5 | 12343.2 | Core | Question to relevant long document; some corpus samples are noisy. |
| NanoMLDR | en | en | 64.1 | 27991.9 | Core | Question to relevant long document; some corpus samples are noisy. |
| NanoMLDR | es | es | 120.3 | 12539.9 | Core | Question to relevant long document; some corpus samples are noisy. |
| NanoMLDR | fr | fr | 119.9 | 11534.1 | Core | Question to relevant long document; some corpus samples are noisy. |
| NanoMLDR | hi | hi | 79.2 | 11900.8 | Core | Question to relevant long document; some corpus samples are noisy. |
| NanoMLDR | it | it | 98.2 | 14374.4 | Core | Question to relevant long document; some corpus samples are noisy. |
| NanoMLDR | ja | ja | 51.7 | 5384.6 | Core | Question to relevant long document; some corpus samples are noisy. |
| NanoMLDR | ko | ko | 55.3 | 5915.2 | Core | Question to relevant long document; some corpus samples are noisy. |
| NanoMLDR | pt | pt | 111.0 | 14744.7 | Core | Question to relevant long document; some corpus samples are noisy. |
| NanoMLDR | ru | ru | 92.9 | 14163.5 | Core | Question to relevant long document; some corpus samples are noisy. |
| NanoMLDR | th | th | 85.3 | 4994.8 | Core | Question to relevant long document; some corpus samples are noisy. |
| NanoMLDR | zh | zh | 20.7 | 12307.3 | Core | Question to relevant long document; some corpus samples are noisy. |
| NanoMMTEB-v2 | ailastatutes | en | 3038.4 | 1972.6 | Extended | Question or search query to relevant passage/document. |
| NanoMMTEB-v2 | argu_ana | en | 1199.8 | 1029.6 | Specialized | Argument-to-counterargument retrieval. |
| NanoMMTEB-v2 | belebele | multilingual | 82.6 | 471.4 | Extended | Question or search query to relevant passage/document. |
| NanoMMTEB-v2 | covid | zh | 25.7 | 409.3 | Extended | Question or search query to relevant passage/document. |
| NanoMMTEB-v2 | hagrid | en | 38.4 | 229.6 | Extended | Question or search query to relevant passage/document. |
| NanoMMTEB-v2 | legal_bench_corporate_lobbying | en | 179.7 | 1157.2 | Extended | Bill text to directly relevant summary. |
| NanoMMTEB-v2 | lembpasskey | en | 37.8 | 28060.9 | Specialized | Synthetic passkey lookup in long context. |
| NanoMMTEB-v2 | miracl | ar | 37.2 | 448.2 | Extended | Question or search query to relevant passage/document. |
| NanoMMTEB-v2 | mlqa | multilingual | 43.7 | 727.9 | Extended | Question or search query to relevant passage/document. |
| NanoMMTEB-v2 | scidocs | en | 69.8 | 1202.7 | No | Citation or related-document retrieval. |
| NanoMMTEB-v2 | spart_qa | en | 654.9 | 49.8 | No | Reasoning or choice conversion rather than document retrieval. |
| NanoMMTEB-v2 | stack_overflow_qa | en | 1361.8 | 1218.1 | Extended | Question or search query to relevant passage/document. |
| NanoMMTEB-v2 | statcan_dialogue_dataset | multilingual | 794.8 | 7237.7 | Extended | Question or search query to relevant passage/document. |
| NanoMMTEB-v2 | temp_reason_l1 | multilingual | 49.9 | 9.0 | No | Reasoning or choice conversion rather than document retrieval. |
| NanoMMTEB-v2 | treccovid | en | 69.2 | 1321.6 | Extended | Question or search query to relevant passage/document. |
| NanoMMTEB-v2 | twitter_hjerne | da | 165.8 | 128.8 | Extended | Question/request to relevant response. |
| NanoMMTEB-v2 | wikipedia_multilingual | bg | 59.2 | 383.3 | Extended | Question or search query to relevant passage/document. |
| NanoMMTEB-v2 | wino_grande | en | 112.0 | 7.7 | No | Reasoning or choice conversion rather than document retrieval. |
| NanoMTEB-Dutch | argu_ana_nl | nl | 1316.9 | 1141.1 | Specialized | Argument-to-counterargument retrieval. |
| NanoMTEB-Dutch | b_bsardnl | nl | 93.8 | 863.2 | Extended | Question or search query to relevant answer/document. |
| NanoMTEB-Dutch | belebele_eng_latn_nld_latn | multilingual | 69.4 | 475.5 | Extended | Question or search query to relevant answer/document. |
| NanoMTEB-Dutch | belebele_nld_latn_eng_latn | multilingual | 81.3 | 529.1 | Extended | Question or search query to relevant answer/document. |
| NanoMTEB-Dutch | belebele_nld_latn_nld_latn | nl | 69.4 | 529.1 | Extended | Question or search query to relevant answer/document. |
| NanoMTEB-Dutch | cqadupstack_android | nl | 59.1 | 638.1 | No | Symmetric duplicate-question retrieval. |
| NanoMTEB-Dutch | cqadupstack_english | nl | 49.6 | 521.7 | No | Symmetric duplicate-question retrieval. |
| NanoMTEB-Dutch | cqadupstack_gis | nl | 62.7 | 1036.1 | No | Symmetric duplicate-question retrieval. |
| NanoMTEB-Dutch | cqadupstack_mathematica | nl | 55.3 | 1166.7 | No | Symmetric duplicate-question retrieval. |
| NanoMTEB-Dutch | cqadupstack_physics | nl | 62.1 | 870.4 | No | Symmetric duplicate-question retrieval. |
| NanoMTEB-Dutch | cqadupstack_programmers | nl | 61.2 | 1142.3 | No | Symmetric duplicate-question retrieval. |
| NanoMTEB-Dutch | cqadupstack_stats | nl | 64.3 | 1097.6 | No | Symmetric duplicate-question retrieval. |
| NanoMTEB-Dutch | cqadupstack_tex | nl | 53.5 | 1211.8 | No | Symmetric duplicate-question retrieval. |
| NanoMTEB-Dutch | cqadupstack_webmasters | nl | 58.8 | 761.2 | No | Symmetric duplicate-question retrieval. |
| NanoMTEB-Dutch | cqadupstack_wordpress | nl | 56.5 | 1183.4 | No | Symmetric duplicate-question retrieval. |
| NanoMTEB-Dutch | dutch_news_articles | nl | 49.0 | 1146.7 | Extended | Question or search query to relevant answer/document. |
| NanoMTEB-Dutch | fever | nl | 54.9 | 445.7 | Extended | Question or search query to relevant answer/document. |
| NanoMTEB-Dutch | legal_qanl | nl | 104.3 | 665.0 | Extended | Question or search query to relevant answer/document. |
| NanoMTEB-Dutch | nfcorpus_nl | multilingual | 18.5 | 1743.7 | Extended | Question or search query to relevant answer/document. |
| NanoMTEB-Dutch | nq | nl | 52.7 | 595.4 | Extended | Question or search query to relevant answer/document. |
| NanoMTEB-Dutch | open_tender | nl | 62.2 | 442.0 | Extended | Question or search query to relevant answer/document. |
| NanoMTEB-Dutch | quora | nl | 51.8 | 66.6 | No | Symmetric duplicate-question retrieval. |
| NanoMTEB-Dutch | sci_fact_nl | nl | 100.1 | 1640.3 | Extended | Question or search query to relevant answer/document. |
| NanoMTEB-Dutch | scidocs_nl | nl | 77.7 | 1331.6 | No | Citation or related-document retrieval. |
| NanoMTEB-Dutch | vabb | nl | 74.5 | 837.9 | Extended | Question or search query to relevant answer/document. |
| NanoMTEB-Dutch | web_faq_nld | nl | 50.4 | 322.2 | Extended | Question or search query to relevant answer/document. |
| NanoMTEB-Dutch | wikipedia_multilingual_nl | nl | 63.5 | 381.0 | Extended | Question or search query to relevant answer/document. |
| NanoMTEB-French | alloprof | fr | 179.3 | 3504.5 | Extended | Question to relevant passage, answer, or product information. |
| NanoMTEB-French | bsard | fr | 145.0 | 793.0 | Extended | Question to relevant passage, answer, or product information. |
| NanoMTEB-French | fquad | fr | 56.2 | 898.3 | Extended | Question to relevant passage, answer, or product information. |
| NanoMTEB-French | mintaka_fr | multilingual | 71.6 | 14.4 | No | Short-answer/entity selection rather than document relevance. |
| NanoMTEB-French | syntec | fr | 72.8 | 1226.3 | Extended | Question to relevant passage, answer, or product information. |
| NanoMTEB-French | xpqa_eng_fra | multilingual | 54.6 | 137.3 | Extended | Question to relevant passage, answer, or product information. |
| NanoMTEB-French | xpqa_fra_eng | multilingual | 52.1 | 77.0 | Extended | Question to relevant passage, answer, or product information. |
| NanoMTEB-French | xpqa_fra_fra | fr | 54.6 | 77.0 | Extended | Question to relevant passage, answer, or product information. |
| NanoMTEB-German | ger_da_lir | de | 879.5 | 18071.5 | Extended | Question or legal/search query to relevant document. |
| NanoMTEB-German | german_dpr | de | 63.7 | 1290.3 | Extended | Question or legal/search query to relevant document. |
| NanoMTEB-German | german_qu_ad | de | 54.9 | 1941.0 | Extended | Question or legal/search query to relevant document. |
| NanoMTEB-German | gov_service | de | 63.9 | 1248.5 | Extended | Question or legal/search query to relevant document. |
| NanoMTEB-German | xmarket_de | multilingual | 14.6 | 457.0 | No | Cross-market product matching. |
| NanoMTEB-Korean | autorag | ko | 69.6 | 823.6 | Extended | Question or search query to relevant answer/document. |
| NanoMTEB-Korean | ko_strategy_qa | ko | 22.4 | 321.3 | Extended | Question or search query to relevant answer/document. |
| NanoMTEB-Korean | lawir_ko | ko | 50.6 | 387.8 | Extended | Question or search query to relevant answer/document. |
| NanoMTEB-Korean | miracl_ko | ko | 21.7 | 193.2 | Extended | Question or search query to relevant answer/document. |
| NanoMTEB-Korean | squad_kor_v1 | ko | 35.8 | 546.2 | Extended | Question or search query to relevant answer/document. |
| NanoMTEB-Misc | 2022_fa | fa | 83.1 | 2818.8 | Extended | Cross-lingual question or search query to relevant document. |
| NanoMTEB-Misc | 2022_ru | ru | 85.6 | 2448.9 | Extended | Cross-lingual question or search query to relevant document. |
| NanoMTEB-Misc | 2022_zh | zh | 24.0 | 1107.6 | Extended | Cross-lingual question or search query to relevant document. |
| NanoMTEB-Misc | cite_ru | ru | 1399.1 | 926.9 | No | Citation or title/abstract related-document matching. |
| NanoMTEB-Misc | cocite_ru | ru | 961.8 | 908.9 | No | Citation or title/abstract related-document matching. |
| NanoMTEB-Misc | en | en | 140.4 | 550.1 | Extended | Cross-lingual question or search query to relevant document. |
| NanoMTEB-Misc | fi | fi | 146.5 | 594.5 | Extended | Cross-lingual question or search query to relevant document. |
| NanoMTEB-Misc | pt | pt | 149.8 | 583.8 | Extended | Cross-lingual question or search query to relevant document. |
| NanoMTEB-Misc | wmt19_de_fr | multilingual | 159.1 | 147.5 | No | Translation semantic-similarity discrimination. |
| NanoMTEB-Misc | wmt19_fr_de | multilingual | 149.0 | 154.2 | No | Translation semantic-similarity discrimination. |
| NanoMTEB-Misc | wmt21_de_fr | multilingual | 170.1 | 177.3 | No | Translation semantic-similarity discrimination. |
| NanoMTEB-Misc | wmt21_fr_de | multilingual | 175.0 | 174.5 | No | Translation semantic-similarity discrimination. |
| NanoMTEB-Polish | cqadupstack_android | pl | 59.3 | 626.7 | No | Symmetric duplicate-question retrieval. |
| NanoMTEB-Polish | cqadupstack_english | pl | 46.5 | 488.1 | No | Symmetric duplicate-question retrieval. |
| NanoMTEB-Polish | cqadupstack_gis | pl | 60.6 | 966.0 | No | Symmetric duplicate-question retrieval. |
| NanoMTEB-Polish | cqadupstack_mathematica | pl | 50.4 | 1088.5 | No | Symmetric duplicate-question retrieval. |
| NanoMTEB-Polish | cqadupstack_physics | pl | 58.8 | 814.7 | No | Symmetric duplicate-question retrieval. |
| NanoMTEB-Polish | cqadupstack_programmers | pl | 59.1 | 1075.3 | No | Symmetric duplicate-question retrieval. |
| NanoMTEB-Polish | cqadupstack_stats | pl | 61.0 | 1016.6 | No | Symmetric duplicate-question retrieval. |
| NanoMTEB-Polish | cqadupstack_tex | pl | 50.3 | 1106.1 | No | Symmetric duplicate-question retrieval. |
| NanoMTEB-Polish | cqadupstack_webmasters | pl | 59.8 | 739.2 | No | Symmetric duplicate-question retrieval. |
| NanoMTEB-Polish | cqadupstack_wordpress | pl | 55.8 | 1040.6 | No | Symmetric duplicate-question retrieval. |
| NanoMTEB-Polish | fiqa | pl | 68.5 | 808.8 | Core | Question or information need to relevant answer/document. |
| NanoMTEB-Polish | nq | pl | 48.6 | 616.8 | Core | Question or information need to relevant answer/document. |
| NanoMTEB-Polish | pugg | pl | 36.2 | 850.3 | Extended | Natural-language question to a directly relevant explanatory passage. |
| NanoMTEB-Polish | quora | pl | 52.5 | 64.6 | No | Symmetric duplicate-question retrieval. |
| NanoMTEB-Scandinavian | dan_fever | multilingual | 59.5 | 312.2 | Extended | Question, claim, or search request to relevant response/document. |
| NanoMTEB-Scandinavian | nor_quad | multilingual | 48.6 | 214.4 | Extended | Question, claim, or search request to relevant response/document. |
| NanoMTEB-Scandinavian | snl | multilingual | 14.0 | 1986.9 | Extended | Question, claim, or search request to relevant response/document. |
| NanoMTEB-Scandinavian | swe_faq | sv | 73.3 | 319.8 | Extended | Question, claim, or search request to relevant response/document. |
| NanoMTEB-Scandinavian | swedn | sv | 45.3 | 2896.0 | Extended | Question, claim, or search request to relevant response/document. |
| NanoMTEB-Scandinavian | tv2_nordretrieval | da | 128.0 | 1440.7 | Extended | Question, claim, or search request to relevant response/document. |
| NanoMTEB-Scandinavian | twitter_hjerne | da | 165.8 | 128.8 | Extended | Question, claim, or search request to relevant response/document. |
| NanoMTEB-Spanish | mintaka_es | multilingual | 66.9 | 14.3 | No | Short-answer/entity selection rather than document relevance. |
| NanoMTEB-Spanish | miracl_es | es | 47.6 | 555.0 | Extended | Question or search statement to relevant passage/product information. |
| NanoMTEB-Spanish | spanish_passage_s2_p | es | 67.6 | 2710.8 | Extended | Question or search statement to relevant passage/product information. |
| NanoMTEB-Spanish | spanish_passage_s2_s | es | 67.6 | 442.4 | No | Symmetric sentence-to-sentence matching. |
| NanoMTEB-Spanish | xpqa_eng_spa | multilingual | 45.2 | 123.4 | Extended | Question or search statement to relevant passage/product information. |
| NanoMTEB-Spanish | xpqa_spa_eng | multilingual | 47.4 | 68.3 | Extended | Question or search statement to relevant passage/product information. |
| NanoMTEB-Spanish | xpqa_spa_spa | es | 45.2 | 68.3 | Extended | Question or search statement to relevant passage/product information. |
| NanoMTEB-Thai | belebele_eng_latn_tha_thai | multilingual | 57.7 | 475.5 | Extended | Question or search query to relevant answer/document. |
| NanoMTEB-Thai | belebele_tha_thai_eng_latn | multilingual | 81.3 | 456.2 | Extended | Question or search query to relevant answer/document. |
| NanoMTEB-Thai | belebele_tha_thai_tha_thai | th | 57.7 | 456.2 | Extended | Question or search query to relevant answer/document. |
| NanoMTEB-Thai | miracl_th | th | 43.6 | 471.8 | Extended | Question or search query to relevant answer/document. |
| NanoMTEB-Thai | mkqa_th | multilingual | 40.2 | 13.4 | No | Short-answer/entity selection rather than document relevance. |
| NanoMTEB-Thai | mr_tidy_thai | th | 41.6 | 416.3 | Extended | Question or search query to relevant answer/document. |
| NanoMTEB-Thai | multi_long_doc_th | th | 107.8 | 25993.3 | Extended | Question or search query to relevant answer/document. |
| NanoMTEB-Thai | web_faq_tha | th | 43.9 | 224.3 | Extended | Question or search query to relevant answer/document. |
| NanoMTEB-Thai | xqu_ad_th | th | 54.2 | 736.8 | Extended | Question or search query to relevant answer/document. |
| NanoMTEB-v2 | argu_ana | en | 1199.8 | 1029.6 | Specialized | Argument-to-counterargument retrieval. |
| NanoMTEB-v2 | climate_fever | en | 115.0 | 1115.9 | Core | Question, claim, or topic to relevant passage/document. |
| NanoMTEB-v2 | cqadupstack_gaming | en | 47.6 | 481.1 | No | Symmetric duplicate-question retrieval. |
| NanoMTEB-v2 | cqadupstack_unix | en | 49.2 | 969.1 | No | Symmetric duplicate-question retrieval. |
| NanoMTEB-v2 | fever | en | 50.6 | 566.0 | Core | Question, claim, or topic to relevant passage/document. |
| NanoMTEB-v2 | fi_qa2018 | en | 61.7 | 780.4 | Core | Question, claim, or topic to relevant passage/document. |
| NanoMTEB-v2 | hotpot_qa | en | 95.8 | 421.2 | Core | Question, claim, or topic to relevant passage/document. |
| NanoMTEB-v2 | scidocs | en | 69.8 | 1202.7 | No | Citation or related-document retrieval. |
| NanoMTEB-v2 | touche2020_v3 | en | 43.4 | 2386.2 | Core | Question, claim, or topic to relevant passage/document. |
| NanoMTEB-v2 | treccovid | en | 69.2 | 1326.6 | Core | Question, claim, or topic to relevant passage/document. |
| NanoMedical | NanoCMedQAv2reranking | zh | 50.1 | 100.9 | Core | Medical question, claim, or information need to relevant answer/evidence. |
| NanoMedical | NanoCUREv1 | en | 75.9 | 604.2 | Core | Medical question, claim, or information need to relevant answer/evidence. |
| NanoMedical | NanoCmedqa | zh | 52.0 | 157.6 | Core | Medical question, claim, or information need to relevant answer/evidence. |
| NanoMedical | NanoMedicalQA | en | 54.2 | 1102.4 | Core | Medical question, claim, or information need to relevant answer/evidence. |
| NanoMedical | NanoNFCorpus | en | 17.1 | 1589.5 | Core | Medical question, claim, or information need to relevant answer/evidence. |
| NanoMedical | NanoPublicHealthQA | ar | 79.8 | 828.2 | Core | Medical question, claim, or information need to relevant answer/evidence. |
| NanoMedical | NanoSciFact | en | 90.1 | 1499.4 | Core | Medical question, claim, or information need to relevant answer/evidence. |
| NanoMedical | NanoSciFactPL | pl | 95.5 | 1554.5 | Core | Medical question, claim, or information need to relevant answer/evidence. |
| NanoMedical | NanoTRECCOVID | en | 69.2 | 1208.8 | Core | Medical question, claim, or information need to relevant answer/evidence. |
| NanoMedical | NanoTRECCOVIDPL | pl | 69.4 | 1251.9 | Core | Medical question, claim, or information need to relevant answer/evidence. |
| NanoMuPLeR | el | el | 141.3 | 744.8 | Core | Natural question to supporting EU passage. |
| NanoMuPLeR | en | en | 134.9 | 650.6 | Core | Natural question to supporting EU passage. |
| NanoMuPLeR | es | es | 134.7 | 734.6 | Core | Natural question to supporting EU passage. |
| NanoMuPLeR | fi | fi | 160.2 | 683.6 | Core | Natural question to supporting EU passage. |
| NanoMuPLeR | fr | fr | 141.2 | 746.4 | Core | Natural question to supporting EU passage. |
| NanoMuPLeR | it | it | 140.8 | 726.1 | Core | Natural question to supporting EU passage. |
| NanoMuPLeR | lt | lt | 143.0 | 621.8 | Core | Natural question to supporting EU passage. |
| NanoMuPLeR | lv | lv | 140.5 | 608.9 | Core | Natural question to supporting EU passage. |
| NanoMuPLeR | nl | nl | 147.9 | 716.3 | Core | Natural question to supporting EU passage. |
| NanoMuPLeR | pl | pl | 144.0 | 686.1 | Core | Natural question to supporting EU passage. |
| NanoMuPLeR | pt | pt | 135.5 | 702.9 | Core | Natural question to supporting EU passage. |
| NanoMuPLeR | sk | sk | 136.2 | 628.2 | Core | Natural question to supporting EU passage. |
| NanoMuPLeR | sl | sl | 136.3 | 607.8 | Core | Natural question to supporting EU passage. |
| NanoMuPLeR | sv | sv | 143.7 | 656.8 | Core | Natural question to supporting EU passage. |
| NanoR2MED | NanoR2MEDBioinformatics | en | 890.3 | 666.8 | Core | Detailed medical question or case to relevant answer/evidence. |
| NanoR2MED | NanoR2MEDBiology | en | 523.0 | 474.1 | Core | Detailed medical question or case to relevant answer/evidence. |
| NanoR2MED | NanoR2MEDIIYiClinical | en | 2584.1 | 5042.3 | Specialized | Clinical case-to-similar-case retrieval. |
| NanoR2MED | NanoR2MEDMedQADiag | en | 706.7 | 791.4 | Core | Detailed medical question or case to relevant answer/evidence. |
| NanoR2MED | NanoR2MEDMedXpertQAExam | en | 928.4 | 723.9 | Core | Detailed medical question or case to relevant answer/evidence. |
| NanoR2MED | NanoR2MEDMedicalSciences | en | 477.6 | 678.6 | Core | Detailed medical question or case to relevant answer/evidence. |
| NanoR2MED | NanoR2MEDPMCClinical | en | 827.7 | 2103.5 | Specialized | Clinical case-to-similar-case retrieval; relevance may depend on a shared diagnosis. |
| NanoR2MED | NanoR2MEDPMCTreatment | en | 1755.8 | 726.6 | Core | Detailed medical question or case to relevant answer/evidence. |
| NanoRARb | NanoARCChallenge | en | 126.7 | 30.9 | No | Reasoning or multiple-choice conversion rather than document retrieval. |
| NanoRARb | NanoAlphaNLI | en | 103.8 | 43.8 | No | Reasoning or multiple-choice conversion rather than document retrieval. |
| NanoRARb | NanoHellaSwag | en | 114.7 | 62.2 | No | Reasoning or multiple-choice conversion rather than document retrieval. |
| NanoRARb | NanoPIQA | en | 37.9 | 98.0 | No | Reasoning or multiple-choice conversion rather than document retrieval. |
| NanoRARb | NanoQuail | en | 1813.8 | 25.0 | No | Reasoning or multiple-choice conversion rather than document retrieval. |
| NanoRARb | NanoRARbCode | en | 470.1 | 256.0 | No | Reasoning or multiple-choice conversion rather than document retrieval. |
| NanoRARb | NanoRARbMath | en | 201.3 | 481.3 | No | Reasoning or multiple-choice conversion rather than document retrieval. |
| NanoRARb | NanoSIQA | en | 126.9 | 21.5 | No | Reasoning or multiple-choice conversion rather than document retrieval. |
| NanoRARb | NanoSpartQA | en | 654.9 | 49.8 | No | Reasoning or multiple-choice conversion rather than document retrieval. |
| NanoRARb | NanoTempReasonL1 | multilingual | 49.9 | 9.0 | No | Reasoning or multiple-choice conversion rather than document retrieval. |
| NanoRARb | NanoTempReasonL2Context | en | 28755.2 | 19.9 | No | Reasoning or multiple-choice conversion rather than document retrieval. |
| NanoRARb | NanoTempReasonL2Fact | en | 1744.4 | 19.9 | No | Reasoning or multiple-choice conversion rather than document retrieval. |
| NanoRARb | NanoTempReasonL2Pure | en | 53.0 | 19.9 | No | Reasoning or multiple-choice conversion rather than document retrieval. |
| NanoRARb | NanoTempReasonL3Context | en | 31804.1 | 19.9 | No | Reasoning or multiple-choice conversion rather than document retrieval. |
| NanoRARb | NanoTempReasonL3Fact | en | 1981.1 | 19.9 | No | Reasoning or multiple-choice conversion rather than document retrieval. |
| NanoRARb | NanoTempReasonL3Pure | en | 65.1 | 19.9 | No | Reasoning or multiple-choice conversion rather than document retrieval. |
| NanoRARb | NanoWinoGrande | en | 112.0 | 7.7 | No | Reasoning or multiple-choice conversion rather than document retrieval. |
| NanoRTEB | NanoAILACasedocs | en | 3038.4 | 26947.3 | Core | Natural-language or programming query to a relevant answer, document, or implementation. |
| NanoRTEB | NanoAILAStatutes | en | 3038.4 | 1972.6 | Core | Natural-language or programming query to a relevant answer, document, or implementation. |
| NanoRTEB | NanoApps | en | 1675.4 | 573.1 | Core | Natural-language or programming query to a relevant answer, document, or implementation. |
| NanoRTEB | NanoCUREv1 | en | 77.2 | 604.0 | Core | Natural-language or programming query to a relevant answer, document, or implementation. |
| NanoRTEB | NanoChatDoctor | en | 441.1 | 605.1 | Core | Natural-language or programming query to a relevant answer, document, or implementation. |
| NanoRTEB | NanoDS1000 | en | 1154.2 | 687.8 | Core | Natural-language or programming query to a relevant answer, document, or implementation. |
| NanoRTEB | NanoFinQA | en | 101.5 | 3918.5 | Core | Natural-language or programming query to a relevant answer, document, or implementation. |
| NanoRTEB | NanoFinanceBench | en | 161.1 | 1677.0 | Core | Natural-language or programming query to a relevant answer, document, or implementation. |
| NanoRTEB | NanoFreshStack | en | 1660.2 | 4983.0 | Core | Natural-language or programming query to a relevant answer, document, or implementation. |
| NanoRTEB | NanoHC3Finance | en | 61.4 | 991.3 | Core | Natural-language or programming query to a relevant answer, document, or implementation. |
| NanoRTEB | NanoHumanEval | en | 291.2 | 177.0 | Core | Natural-language or programming query to a relevant answer, document, or implementation. |
| NanoRTEB | NanoLegalSummarization | en | 103.1 | 606.2 | Core | Natural-language or programming query to a relevant answer, document, or implementation. |
| NanoRTEB | NanoMBPP | en | 78.4 | 180.8 | Core | Natural-language or programming query to a relevant answer, document, or implementation. |
| NanoRTEB | NanoWikiSQL | en | 1551.5 | 62.3 | Core | Natural-language or programming query to a relevant answer, document, or implementation. |
| NanoRuMTEB | miracl_ru | ru | 45.4 | 517.3 | Extended | Question or search query to relevant passage/news document. |
| NanoRuMTEB | ria_news | ru | 62.0 | 1145.3 | Extended | Question or search query to relevant passage/news document. |
| NanoRuMTEB | ru_bq | ru | 52.2 | 484.5 | Extended | Question or search query to relevant passage/news document. |
| NanoVNMTEB | argu_ana_vn | vi | 1183.9 | 1080.3 | Specialized | Argument-to-counterargument retrieval. |
| NanoVNMTEB | climate_fever_vn | vi | 130.0 | 407.1 | Extended | Question, claim, or search query to relevant passage/document. |
| NanoVNMTEB | cqadupstack_android_vn | vi | 55.6 | 604.8 | No | Symmetric duplicate-question retrieval. |
| NanoVNMTEB | cqadupstack_gis_vn | vi | 59.2 | 929.2 | No | Symmetric duplicate-question retrieval. |
| NanoVNMTEB | cqadupstack_mathematica_vn | vi | 49.3 | 1045.8 | No | Symmetric duplicate-question retrieval. |
| NanoVNMTEB | cqadupstack_physics_vn | vi | 58.6 | 801.0 | No | Symmetric duplicate-question retrieval. |
| NanoVNMTEB | cqadupstack_programmers_vn | vi | 58.7 | 1070.6 | No | Symmetric duplicate-question retrieval. |
| NanoVNMTEB | cqadupstack_stats_vn | vi | 52.8 | 998.9 | No | Symmetric duplicate-question retrieval. |
| NanoVNMTEB | cqadupstack_tex_vn | vi | 47.8 | 1090.6 | No | Symmetric duplicate-question retrieval. |
| NanoVNMTEB | cqadupstack_unix_vn | vi | 52.8 | 875.8 | No | Symmetric duplicate-question retrieval. |
| NanoVNMTEB | cqadupstack_webmasters_vn | vi | 58.0 | 731.4 | No | Symmetric duplicate-question retrieval. |
| NanoVNMTEB | cqadupstack_wordpress_vn | vi | 52.4 | 1028.8 | No | Symmetric duplicate-question retrieval. |
| NanoVNMTEB | dbpedia_vn | vi | 42.1 | 340.4 | No | Entity retrieval. |
| NanoVNMTEB | fever_vn | vi | 56.0 | 392.4 | Extended | Question, claim, or search query to relevant passage/document. |
| NanoVNMTEB | fi_qa2018_vn | vi | 69.4 | 811.0 | Extended | Question, claim, or search query to relevant passage/document. |
| NanoVNMTEB | hotpot_qa_vn | vi | 99.5 | 445.3 | Extended | Question, claim, or search query to relevant passage/document. |
| NanoVNMTEB | msmarco_vn | vi | 33.4 | 306.7 | Extended | Question, claim, or search query to relevant passage/document. |
| NanoVNMTEB | nano_fever | vi | 56.0 | 462.3 | Extended | Question, claim, or search query to relevant passage/document. |
| NanoVNMTEB | nano_nq | vi | 39.4 | 565.3 | Extended | Question, claim, or search query to relevant passage/document. |
| NanoVNMTEB | nfcorpus_vn | multilingual | 24.7 | 1584.3 | Extended | Question, claim, or search query to relevant passage/document. |
| NanoVNMTEB | nq_vn | vi | 39.4 | 557.6 | Extended | Question, claim, or search query to relevant passage/document. |
| NanoVNMTEB | quora_vn | vi | 76.5 | 129.2 | No | Symmetric duplicate-question retrieval. |
| NanoVNMTEB | sci_fact_vn | vi | 90.6 | 1518.8 | Extended | Question, claim, or search query to relevant passage/document. |
| NanoVNMTEB | scidocs_vn | vi | 73.4 | 1226.7 | No | Citation or related-document retrieval. |
| NanoVNMTEB | touche2020_vn | vi | 52.2 | 1939.6 | Extended | Question, claim, or search query to relevant passage/document. |
| NanoVNMTEB | treccovid_vn | vi | 70.5 | 1315.6 | Extended | Question, claim, or search query to relevant passage/document. |
