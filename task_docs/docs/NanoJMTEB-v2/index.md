# NanoJMTEB-v2

## Overview

NanoJMTEB-v2 is a compact Japanese retrieval group derived from JMTEB, MTEB,
and related Japanese datasets. It covers Japanese casual web search, government
FAQ matching, quiz-to-entity retrieval, answer-label retrieval, MIRACL and
Mr. TyDi passage retrieval, long-document retrieval, and four Japanese NLP
Journal paper-component matching tasks.

The group is useful because it is not simply Japanese passage retrieval. Some
tasks retrieve short answer labels, some retrieve noisy web snippets or FAQ
answers, some retrieve Wikipedia-like passages or full entity pages, and some
match titles or abstracts to academic paper sections. BM25 exposes Japanese
term and entity anchoring, dense retrieval tests semantic passage and label
matching, and `reranking_hybrid` indicates whether sparse and dense retrieval
recover complementary candidates.

## What This Group Measures

JMTEB and MTEB define Japanese retrieval tasks for embedding evaluation. This
Nano group collects several Japanese retrieval sources: JaCWIR, JaGovFaqs,
JAQKET, Mintaka Japanese, MIRACL, Mr. TyDi, MultiLongDocRetrieval, and Japanese
NLP Journal paper-component matching tasks.

The group measures Japanese retrieval robustness across target types. A
relevant document may be a title/description snippet, an official FAQ answer, a
Wikipedia entity page, a short answer label, an answer-bearing passage, a full
long article, or an academic paper section. A model that works well on one of
these surfaces may not work on the others.

## Task Families

- **Web and FAQ retrieval:** `ja_cwir` and `ja_gov_faqs` retrieve web snippets
  or government FAQ answers.
- **Entity and answer-label retrieval:** `jaqket` retrieves entity pages from
  quiz clues, while `mintaka_ja` retrieves short answer labels.
- **Japanese passage retrieval:** `miracl_ja` and `mr_tidy_japanese` retrieve
  answer-bearing Japanese passages with some multi-positive qrels.
- **Long-document retrieval:** `multi_long_doc_ja` retrieves long documents
  from generated questions.
- **Academic component matching:** the four `nlpjournal_*` tasks link titles,
  abstracts, introductions, and full articles from Japanese NLP papers.

## Dataset Shape

NanoJMTEB-v2 contains 11 task pages, 2,200 queries, 64,140 split-local
documents, and 2,432 positive qrel rows. Each split has 200 queries. Most tasks
are single-positive; `miracl_ja` and `mr_tidy_japanese` contain multi-positive
queries.

Text length varies widely. `mintaka_ja` documents are short answer labels,
while `multi_long_doc_ja` and `nlpjournal_abs_article` contain very long
documents. The NLP Journal abstract queries are much longer than web, FAQ,
entity, or passage queries. This makes the group a mix of short Japanese search,
entity inference, evidence passage retrieval, and long academic-document
matching.

## Retrieval Behavior

### BM25 Profile

BM25 is very strong on the Japanese NLP Journal component tasks and on
`ja_cwir`, where exact technical terms, titles, web keywords, and shared paper
vocabulary are highly informative. It is also strong on `jaqket`,
`ja_gov_faqs`, and long-document retrieval. These tasks often preserve Japanese
surface anchors that sparse retrieval can exploit.

BM25 is weaker on `mintaka_ja`, where the target is a short answer label, and
on MIRACL/Mr. TyDi passage retrieval, where short factual questions may not
repeat the evidence passage wording. It remains useful, but semantic inference
and answerability become more important.

### Dense Profile

Dense retrieval is strongest on many passage and answer-oriented tasks:
`ja_gov_faqs`, `mintaka_ja`, `miracl_ja`, and `mr_tidy_japanese` all benefit
from embedding similarity. It connects short Japanese questions to passages or
labels that express the requested answer without exact overlap.

Dense retrieval is not always best. For the NLP Journal tasks and
`multi_long_doc_ja`, BM25 can outperform dense because titles, abstracts, and
long articles share distinctive technical terms. That makes this group useful
for testing whether dense models preserve exact Japanese terminology.

### Reranking Hybrid Profile

`reranking_hybrid` is best on `ja_gov_faqs` and `jaqket`, and is competitive
across many other tasks. These are cases where exact Japanese terms and semantic
matching both matter: an FAQ answer or entity page may contain the right
keywords, but ranking still needs intent or entity disambiguation.

For reranker experiments, the hybrid profile is most useful on tasks where BM25
and dense disagree. It provides a safer candidate pool for FAQ, entity, and
passage retrieval than either signal alone.

## Task Summary

| Task | Retrieval shape | Queries | Docs | Positives | BM25 nDCG@10 | Dense nDCG@10 | Reranking hybrid nDCG@10 | Best profile |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| [ja_cwir](ja_cwir.md) | generated web question to page snippet | 200 | 10,000 | 200 | 0.9181 | 0.8367 | 0.8810 | BM25 |
| [ja_gov_faqs](ja_gov_faqs.md) | government FAQ question to answer | 200 | 10,000 | 200 | 0.7196 | 0.7487 | 0.7614 | Reranking hybrid |
| [jaqket](jaqket.md) | quiz clue to entity page | 200 | 10,000 | 200 | 0.7837 | 0.7830 | 0.7876 | Reranking hybrid |
| [mintaka_ja](mintaka_ja.md) | complex question to answer label | 200 | 1,592 | 200 | 0.2561 | 0.3687 | 0.3354 | Dense |
| [miracl_ja](miracl_ja.md) | Japanese question to Wikipedia passage | 200 | 10,000 | 373 | 0.5361 | 0.6923 | 0.6252 | Dense |
| [mr_tidy_japanese](mr_tidy_japanese.md) | Japanese question to Mr. TyDi passage | 200 | 10,000 | 259 | 0.5518 | 0.7399 | 0.6633 | Dense |
| [multi_long_doc_ja](multi_long_doc_ja.md) | generated question to long article | 200 | 10,000 | 200 | 0.5929 | 0.3956 | 0.5008 | BM25 |
| [nlpjournal_abs_article](nlpjournal_abs_article.md) | abstract to full article | 200 | 637 | 200 | 0.9982 | 0.9763 | 0.9863 | BM25 |
| [nlpjournal_abs_intro](nlpjournal_abs_intro.md) | abstract to introduction | 200 | 637 | 200 | 0.9896 | 0.9553 | 0.9545 | BM25 |
| [nlpjournal_title_abs](nlpjournal_title_abs.md) | title to abstract | 200 | 637 | 200 | 0.9526 | 0.9290 | 0.9428 | BM25 |
| [nlpjournal_title_intro](nlpjournal_title_intro.md) | title to introduction | 200 | 637 | 200 | 0.9132 | 0.8632 | 0.8704 | BM25 |

## Interpretation Notes for Model Researchers

NanoJMTEB-v2 is best read by target format. Academic component matching is
lexically strong because titles, abstracts, and papers share technical terms.
FAQ, entity, Mintaka, MIRACL, and Mr. TyDi tasks require more semantic matching
or entity inference. A single Japanese average will hide those differences.

The BM25-heavy tasks are not trivial; they show that exact Japanese terminology
and paper vocabulary matter. Dense-led tasks show where answerability,
short-label matching, or passage semantics matter more. Hybrid-led tasks show
where exact entity anchors and semantic disambiguation both contribute.

## Training and Leakage Notes

Useful training data includes Japanese search logs, government FAQ pairs,
Wikipedia passage retrieval, JAQKET-style quiz/entity data, Mintaka-style
complex QA, long-document question generation, and Japanese academic paper
component matching. Hard negatives should come from same entities, same
government programs, same article families, or same research subfields.

Exclude NanoJMTEB-v2 evaluation queries, positives, qrels, paper sections,
answer labels, and direct synthetic variants. Upstream JMTEB, MTEB, JAQKET,
Mintaka, MIRACL, Mr. TyDi, MLDR, and NLP Journal evaluation examples should be
audited before use in training.

## Public Sources

- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316), 2022.
- [MIRACL: A Multilingual Retrieval Dataset Covering 18 Diverse Languages](https://aclanthology.org/2023.tacl-1.63/), 2023.
- [Mr. TyDi: A Multi-lingual Benchmark for Dense Retrieval](https://arxiv.org/abs/2108.08787), 2021.
- [Mintaka: A Complex, Natural, and Multilingual Dataset for End-to-End Question Answering](https://aclanthology.org/2022.coling-1.138/), 2022.

### Source Reference Table

| Source | Year | Type | URL |
| --- | ---: | --- | --- |
| MTEB: Massive Text Embedding Benchmark | 2022 | paper | [https://arxiv.org/abs/2210.07316](https://arxiv.org/abs/2210.07316) |
| MIRACL: A Multilingual Retrieval Dataset Covering 18 Diverse Languages | 2023 | paper | [https://aclanthology.org/2023.tacl-1.63/](https://aclanthology.org/2023.tacl-1.63/) |
| Mr. TyDi: A Multi-lingual Benchmark for Dense Retrieval | 2021 | paper | [https://arxiv.org/abs/2108.08787](https://arxiv.org/abs/2108.08787) |
| Mintaka: A Complex, Natural, and Multilingual Dataset for End-to-End Question Answering | 2022 | paper | [https://aclanthology.org/2022.coling-1.138/](https://aclanthology.org/2022.coling-1.138/) |
