# NanoRuMTEB

## Overview

NanoRuMTEB is a compact Russian retrieval group based on ruMTEB retrieval
tasks. It contains three Russian-language subtasks: MIRACL-style Wikipedia
passage retrieval, RIA news headline-to-article retrieval, and RuBQ
question-to-Wikipedia paragraph retrieval. The group is small, but it covers
two important Russian retrieval modes: short question answering over Wikipedia
and headline/article matching in news.

The group contains 600 queries, 30,000 task-local documents, and 1,113 positive
qrel rows. All tasks are Russian, and all candidate pools contain 10,000
documents. The group is useful for checking whether a retriever handles Russian
morphology, named entities, inflection, and native-language query phrasing
rather than only English or translated retrieval.

## What This Group Measures

The group measures native Russian lexical and semantic retrieval. `miracl_ru`
uses short Russian questions and Russian Wikipedia passages. `ria_news` maps
Russian news headlines to the corresponding news articles. `ru_bq` retrieves
Wikipedia paragraphs that support answers to Russian open-domain questions.

The main evaluation contrast is between a lexically strong headline-to-article
task and QA-style passage retrieval tasks. News headlines and articles often
share event terms and named entities. Wikipedia QA tasks require matching short
questions to answer-bearing paragraphs, where the answer passage may use
different inflected forms or broader context.

## Task Families

- **Wikipedia passage retrieval:** `miracl_ru` retrieves Russian Wikipedia
  passages for short information needs.
- **News retrieval:** `ria_news` retrieves Russian news articles from headline
  strings.
- **Open-domain QA retrieval:** `ru_bq` retrieves Russian Wikipedia paragraphs
  that support answers to questions.

## Dataset Shape

Each task has 200 queries and 10,000 candidate documents. `ria_news` is
single-positive, while `miracl_ru` and `ru_bq` are multi-positive, averaging
2.90 and 1.67 positives per query. The group therefore combines one exact
headline-to-article retrieval task with two evidence retrieval tasks where
several passages may be relevant.

Queries are short Russian questions or headlines. Documents are longer
Wikipedia passages or news articles. The task-local corpus sizes are equal, so
differences in retrieval behavior mostly reflect source family and relevance
relation rather than corpus size.

## Retrieval Behavior

### BM25 Profile

BM25 is not the best profile for any task, but it is strong on `ria_news`.
The news split reaches 0.9135 nDCG@10, because headlines and articles often
share names, places, dates, and event vocabulary. BM25 is also usable on
`ru_bq`, reaching 0.6979 nDCG@10, where some question terms and entities appear
in the answer passage.

BM25 is weakest on `miracl_ru` at 0.5154 nDCG@10. Short Russian questions do
not always repeat the exact wording of a relevant Wikipedia passage, and
morphology or paraphrase can reduce sparse overlap. BM25 is therefore a strong
Russian lexical baseline, but not the leading retrieval profile for this group.

### Dense Profile

Dense retrieval with `harrier-oss-270m` is the best profile for all three tasks.
It reaches 0.9478 nDCG@10 on `ria_news`, 0.8739 on `ru_bq`, and 0.7938 on
`miracl_ru`. The improvements on the two QA-style tasks show that embedding
similarity helps connect Russian questions to answer-bearing passages beyond
exact token overlap.

Dense also slightly improves the already strong news task, suggesting that
headline-to-article retrieval benefits from both event-term overlap and broader
semantic matching. At group level, dense retrieval is the clearest default
profile for NanoRuMTEB.

### Reranking Hybrid Profile

The reranking hybrid profile is not the best nDCG@10 profile for any task, but
it has the best recall@100 on all three tasks. It reaches 0.9948 recall@100 on
`miracl_ru`, 0.9900 on `ria_news`, and 0.9790 on `ru_bq`. This means hybrid
retrieval is a strong candidate-generation strategy even when dense retrieval
orders the top 10 better.

The top-10 pattern suggests that adding sparse evidence can slightly dilute
dense ranking for Russian QA tasks, while still recovering complementary
candidate passages. For reranking pipelines, hybrid candidates are useful; for
first-stage top-10 scoring in this Nano slice, dense retrieval leads.

## Task Summary

| Task | Family | Language | Queries | Docs | Positives | Positives/query | BM25 nDCG@10 | Dense nDCG@10 | Reranking hybrid nDCG@10 | Best profile |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| [miracl_ru](miracl_ru.md) | Wikipedia passage retrieval | `ru` | 200 | 10,000 | 579 | 2.90 | 0.5154 | 0.7938 | 0.6646 | Dense |
| [ria_news](ria_news.md) | News retrieval | `ru` | 200 | 10,000 | 200 | 1.00 | 0.9135 | 0.9478 | 0.9272 | Dense |
| [ru_bq](ru_bq.md) | Open-domain QA retrieval | `ru` | 200 | 10,000 | 334 | 1.67 | 0.6979 | 0.8739 | 0.7767 | Dense |

## Interpretation Notes for Model Researchers

NanoRuMTEB is a compact but clean Russian diagnostic. Dense retrieval dominates
all three tasks, especially the QA-style Wikipedia tasks. BM25 remains strong on
news retrieval and is still useful for entity-heavy Russian queries, but it does
not capture all paraphrase and answer-evidence relations.

Because there are only three tasks, group averages are easy to inspect. A model
that improves `ria_news` may be improving event and headline matching, while a
model that improves `miracl_ru` or `ru_bq` is more likely improving Russian
question-to-passage retrieval. Hybrid recall should be considered if the system
uses a reranker after first-stage retrieval.

## Training and Leakage Notes

Useful training data includes Russian MIRACL or Wikipedia question-passage
pairs, RuBQ-style QA retrieval data, Russian news headline-to-article pairs, and
hard negatives mined from same-topic Russian passages. Native Russian training
data is preferable to English-only data translated after the fact.

Leakage control should exclude NanoRuMTEB evaluation queries, qrels, and
positive documents. Source dev/test overlap should be audited before using
ruMTEB, MIRACL, RIA news, or RuBQ-derived data for training.

## Public Sources

- [The Russian-focused embedders' exploration: ruMTEB benchmark and Russian embedding model design](https://aclanthology.org/2025.naacl-long.12/), 2025.
- [MIRACL](http://miracl.ai/).
- [mteb/RiaNewsRetrieval_test_top_250_only_w_correct-v2](https://huggingface.co/datasets/mteb/RiaNewsRetrieval_test_top_250_only_w_correct-v2).
- [ai-forever/rubq-retrieval](https://huggingface.co/datasets/ai-forever/rubq-retrieval).
- [mteb/MIRACLRetrievalHardNegatives](https://huggingface.co/datasets/mteb/MIRACLRetrievalHardNegatives).

### Source Reference Table

| Source | Year | Type | URL |
| --- | ---: | --- | --- |
| The Russian-focused embedders' exploration: ruMTEB benchmark and Russian embedding model design | 2025 | benchmark paper | https://aclanthology.org/2025.naacl-long.12/ |
| MIRACL |  | project page | http://miracl.ai/ |
| mteb/RiaNewsRetrieval_test_top_250_only_w_correct-v2 |  | dataset card | https://huggingface.co/datasets/mteb/RiaNewsRetrieval_test_top_250_only_w_correct-v2 |
| ai-forever/rubq-retrieval |  | dataset card | https://huggingface.co/datasets/ai-forever/rubq-retrieval |
| mteb/MIRACLRetrievalHardNegatives |  | dataset card | https://huggingface.co/datasets/mteb/MIRACLRetrievalHardNegatives |
