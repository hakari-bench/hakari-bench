# MNanoBEIR / NanoBEIR-ar / NanoQuoraRetrieval

## Overview

NanoBEIR-ar / NanoQuoraRetrieval is the Arabic NanoBEIR version of Quora
duplicate-question retrieval. Unlike MS MARCO or Natural Questions, both the
query and the document are user questions; a positive document is another
question with the same underlying answer intent. The task is based on the Quora
Question Pairs source used by BEIR-style retrieval benchmarks rather than a
standalone retrieval paper. The Nano task contains 50 Arabic translated query
questions, 5,046 candidate questions, and 70 positive qrels. Most queries have
one duplicate, but a minority have multiple duplicates. The task tests Arabic
paraphrase and intent-equivalence retrieval: related questions are not enough
unless they would be answered by the same answer.

## Details

### What the Original Data Measures

Quora duplicate-question retrieval evaluates whether a system can find
questions that are semantically equivalent to a query question. The upstream
Quora Question Pairs data labels question pairs as duplicates or non-duplicates.
In the retrieval formulation, the query is one question and the corpus contains
candidate questions; positives are duplicate questions.

The Arabic NanoBEIR version keeps the same duplicate-question objective in
translated form. This makes the task different from answer-passage retrieval:
the model does not need to find evidence or an answer document. It must decide
whether two user questions express the same intent despite differences in word
order, specificity, grammar, or phrasing.

### Observed Data Profile

The metadata records 50 queries, 5,046 documents, and 70 positive qrels.
Queries have 1.40 positives on average, with 10 multi-positive queries and a
maximum of 6 positives. Query text averages 43.22 characters, and candidate
questions average 58.16 characters. Examples include whether laughing at one's
own jokes is odd, the biggest lie someone invented, Quora answers about Donald
Trump, becoming physically strong, and how a quantum satellite works.

The documents are short questions rather than passages. This makes the task
more symmetric than QA retrieval: both sides can be fragmentary, informal, and
underspecified. Relevance depends on answer equivalence, not on topical
relatedness.

### BM25 Evaluation Profile

The BM25 candidate subset reaches nDCG@10 = 0.7238, hit@10 = 0.9000, and
Recall@100 = 0.9429. BM25 is strong because duplicate questions often preserve
rare content words, names, phrases, or the main predicate. When two Arabic
translations remain close in surface form, sparse overlap places duplicates
near the top.

BM25's limitation is paraphrase variation. It can miss duplicates that use
different wording, omit a word, change specificity, or restructure the
question. It can also over-rank related but non-duplicate questions that share
keywords. This is a key distinction: a related Quora question is not relevant
unless it has the same answer intent.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` reaches nDCG@10 =
0.8170, hit@10 = 0.9000, and Recall@100 = 0.9429. Dense retrieval is the best
top-rank signal for this task. It ties BM25 on hit@10 and Recall@100 but orders
the top candidates better, showing that embedding similarity helps detect
paraphrase and intent equivalence beyond exact word overlap.

Dense retrieval's risk is over-general semantic matching. It can rank a
question about the same topic or entity even if the expected answer differs.
For duplicate retrieval, the model must learn answer-equivalence, not broad
semantic relatedness.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset reaches nDCG@10 = 0.7728, hit@10 =
0.9000, and Recall@100 = 1.0000. Hybrid is not the best top-rank sorter because
dense has higher nDCG@10, but it is the strongest candidate-generation view.
It recovers all judged positives within the top 100 without rank-101 safeguard
rows.

For reranker evaluation, hybrid is the safest pool. It includes lexical
duplicates from BM25 and paraphrastic duplicates from dense retrieval. The
reranker can then focus on whether two questions are answer-equivalent rather
than merely related.

### Metric Interpretation for Model Researchers

This task shows a clear difference between ordering and coverage. Dense
retrieval has the best nDCG@10, so it is strongest at ordering duplicate
questions near the top. BM25 is already strong because many duplicates share
visible words. Hybrid has perfect Recall@100, which makes it useful for
reranker experiments and duplicate-cluster expansion.

Because some queries have multiple positives, models should be evaluated not
only on the first duplicate but also on whether they recover the duplicate
cluster. A model that retrieves semantically related but non-equivalent
questions may look plausible in examples but is wrong for this task.

### Query and Relevance Type Tendencies

Queries are short Arabic user questions. They often ask about advice,
definitions, social behavior, politics, technology, translation, or personal
experience. Relevant documents are other questions with the same intent. Small
surface differences are allowed, but answer intent must be preserved.

Lexical-heavy cases include duplicates that share rare words or names. Dense
cases include paraphrases with different syntax or specificity. Hybrid
retrieval is strongest when some duplicates are near-exact rewrites and others
are looser paraphrases.

### Representative Failure Modes

BM25 can over-rank questions that share keywords but ask something different.
Dense retrieval can over-rank broad topical neighbors, such as another question
about the same person, technology, or social issue, while missing a difference
in intent. Multi-positive clusters can create partial failures where the model
finds one obvious duplicate but misses more distant paraphrases.

Good hard negatives are related questions with different expected answers,
questions that share an entity but ask a different relation, and paraphrases
that change a crucial condition.

### Arabic-Specific Notes

Arabic duplicate-question retrieval depends on paraphrase handling,
word-order variation, morphology, clitics, dialect-like phrasing, and
translated user-question style. Sparse retrieval benefits from preserving rare
content words and names. Dense retrieval needs enough Arabic paraphrase and
intent-equivalence training to avoid treating all related questions as
duplicates. Transliteration and mixed-language terms can matter for names,
products, and technical topics.

### Training and Leakage Notes

Training should exclude Quora, BEIR, or NanoBEIR records likely to overlap with
these evaluation duplicate questions. Useful non-overlapping data includes
Quora-style duplicate-question pairs, Arabic or multilingual paraphrase
datasets, FAQ duplicate pairs, community-question duplicate links, and
supervised intent-equivalence data.

### Model Improvement Hints

The main improvement target is answer-intent equivalence. First-stage
retrievers should combine exact keyword preservation with paraphrase matching.
Rerankers should be trained on related-but-not-duplicate hard negatives, since
those are the most important mistakes for this task. Multi-positive training
can improve duplicate-cluster recovery.

### Training Data That May Help

Useful training data includes non-overlapping duplicate-question pairs, Arabic
FAQ deduplication data, multilingual paraphrase datasets, community QA duplicate
links, and synthetic question clusters with multiple equivalent phrasings per
intent.

### Synthetic Data Guidance

Generate clusters of short Arabic user questions around the same intent. Vary
word order, grammar, specificity, politeness, and phrasing while preserving the
answer. Include hard negatives that share the topic but require a different
answer. Positives should be answer-equivalent duplicate questions, not merely
related questions.

## Example Data

| Query | Positive document |
| --- | --- |
| هل من الجيد أن يضحك الشخص على نكاته الخاصة؟ (43 chars) | هل من الغريب أن أضحك على نكتي الخاصة؟ (37 chars) |
| ما هو أفضل كذبة اخترعتها في حياتك؟ (34 chars) | ما هي أكبر كذبة اخترعتها في حياتك؟ (34 chars) |
| لماذا يقترح موقع كورا باستمرار إجابات تهاجم دونالد ترامب في محتوى صفحتي؟ (72 chars) | لماذا تبدو إجابات موقع كورا حول أسئلة عن دونالد ترامب موضوعية ومتحيزة؟ (70 chars) |
| كيف يمكنني أن أصبح قويًا جسديًا؟ (32 chars) | كيف أصبح قويًا جسديًا؟ (22 chars) |
| كيف يعمل قمر صناعي كمي؟ (23 chars) | كيف يعمل قمر صناعي كمي؟ وما هي بعض الأغراض الرئيسية له؟ (55 chars) |

### Public Sources

- [Quora Question Pairs](https://kaggle.com/competitions/quora-question-pairs), 2017.
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663), 2021.
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595), 2025.
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-ar](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ar)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Quora Question Pairs | 2017 | dataset | https://kaggle.com/competitions/quora-question-pairs |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | https://arxiv.org/abs/2104.08663 |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | https://arxiv.org/abs/2502.13595 |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | https://huggingface.co/collections/zeta-alpha-ai/nanobeir |
