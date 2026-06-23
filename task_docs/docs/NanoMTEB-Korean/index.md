# NanoMTEB-Korean

## Overview

NanoMTEB-Korean is a compact Korean retrieval group with five tasks spanning
RAG evidence retrieval, implicit-reasoning evidence retrieval, legal article
lookup, MIRACL-style Wikipedia retrieval, and KorQuAD/SQuAD-style context
retrieval. It is a useful group for model researchers because Korean retrieval
quality is shaped by morphology, spacing variation, domain-specific terms, and
the difference between literal evidence matching and semantic answerability.

The group contains 914 queries, 24,493 task-local documents, and 1,400 positive
qrel rows. `autorag`, `lawir_ko`, and `squad_kor_v1` are single-positive in the
Nano splits. `ko_strategy_qa` and `miracl_ko` are multi-positive, so a model can
receive credit for retrieving several acceptable evidence passages. This means
the group combines exact target retrieval with broader evidence-list ranking.

## What This Group Measures

The group measures whether Korean retrieval systems can handle five related but
different relevance relations. `autorag` retrieves public-document chunks needed
for Korean RAG questions. `ko_strategy_qa` retrieves Korean evidence for
StrategyQA-style questions where the supporting fact may be implicit.
`lawir_ko` retrieves statute articles from law and provision queries.
`miracl_ko` retrieves Korean Wikipedia passages for information-seeking
questions. `squad_kor_v1` retrieves answer-bearing Korean Wikipedia contexts.

The benchmark is not just a Korean QA suite. It includes legal lookup and public
document retrieval, and it separates tasks where exact terminology is highly
predictive from tasks where dense semantic matching has a clearer advantage.
This makes it useful for diagnosing whether a model is strong because it
understands Korean semantic relations, because it matches surface terms well, or
because it balances both signals in a hybrid setting.

## Task Families

- **Korean RAG retrieval:** `autorag` retrieves answer-supporting chunks from
  public and domain documents.
- **Implicit-reasoning retrieval:** `ko_strategy_qa` retrieves evidence passages
  for Korean StrategyQA-style questions.
- **Legal retrieval:** `lawir_ko` retrieves Korean statutory article text from
  law/provision queries.
- **Korean Wikipedia retrieval:** `miracl_ko` retrieves MIRACL Korean Wikipedia
  passages.
- **Reading-comprehension retrieval:** `squad_kor_v1` retrieves KorQuAD/SQuAD
  answer contexts.

## Dataset Shape

The group has five Korean-language tasks. The largest document pools are
`miracl_ko` with 10,000 documents and `ko_strategy_qa` with 9,251 documents.
`autorag` is the smallest pool with 720 documents, while `squad_kor_v1` has 960
documents and very direct QA-context matching. The group-level document count is
the sum of task-local candidate pools, not a deduplicated Korean corpus.

Positive density varies by task. Three tasks have exactly one positive per
query. `ko_strategy_qa` averages 1.89 positives per query, and `miracl_ko`
averages 2.54 positives per query. Those two tasks should be read with recall
and listwise ranking behavior in mind, because one question may have multiple
valid evidence passages.

## Retrieval Behavior

### BM25 Profile

BM25 is strongest on tasks with direct lexical anchors. It is the best nDCG@10
profile for `autorag` and `squad_kor_v1`. `autorag` reaches 0.9053 nDCG@10,
suggesting that many RAG queries retain domain terms, numbers, named entities,
or report language that appear in the positive chunk. `squad_kor_v1` reaches
0.9618 nDCG@10, which indicates that the question and target context often share
enough Korean surface evidence for sparse retrieval to rank the answer context
very highly.

BM25 is less dominant on `ko_strategy_qa`, `lawir_ko`, and `miracl_ko`.
StrategyQA-style evidence may not repeat the exact question wording, legal
article lookup can require mapping a provision description to formal statutory
language, and MIRACL-style Wikipedia retrieval often benefits from semantic
matching beyond exact token overlap. At group level BM25 is still strong
(0.6525 query-weighted nDCG@10), but it is not the leading profile overall.

### Dense Profile

Dense retrieval with `harrier-oss-270m` is the best profile for
`ko_strategy_qa` and `lawir_ko`. The gain on `ko_strategy_qa` is large:
0.7084 nDCG@10 for dense against 0.4740 for BM25. This is the expected pattern
for implicit-reasoning evidence retrieval, where the useful passage can express
the supporting fact rather than repeat the question. `lawir_ko` also favors
dense at 0.6534 nDCG@10, showing that semantic matching helps bridge query
phrasing and formal legal article text.

Dense is competitive but not best on `autorag` and `squad_kor_v1`, and it is
slightly behind hybrid on `miracl_ko`. This profile suggests that Korean dense
retrieval is valuable when evidence is paraphrastic or domain phrasing diverges,
but exact surface forms remain important in direct QA and RAG chunk retrieval.

### Reranking Hybrid Profile

The reranking hybrid profile is the strongest query-weighted profile for the
group: 0.7557 nDCG@10, 0.9114 hit@10, and 0.9640 recall@100. It is the best
individual nDCG@10 profile for `miracl_ko`, where dense and sparse signals
complement each other in a multi-positive Wikipedia retrieval setting. It is
also close to the best profile on `squad_kor_v1` and `lawir_ko`.

Hybrid is not uniformly superior. It trails BM25 on `autorag` and
`squad_kor_v1`, and it trails dense on `ko_strategy_qa` and `lawir_ko`.
However, its recall@100 is the best or tied-best on most tasks. This makes
NanoMTEB-Korean a clear example where hybrid retrieval can be a strong candidate
generation strategy even when the top-10 ordering still depends on task family.

## Task Summary

| Task | Family | Language | Queries | Docs | Positives | Positives/query | BM25 nDCG@10 | Dense nDCG@10 | Reranking hybrid nDCG@10 | Best profile |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| [autorag](autorag.md) | RAG evidence retrieval | `ko` | 114 | 720 | 114 | 1.00 | 0.9053 | 0.7745 | 0.8530 | BM25 |
| [ko_strategy_qa](ko_strategy_qa.md) | Implicit-reasoning evidence retrieval | `ko` | 200 | 9,251 | 378 | 1.89 | 0.4740 | 0.7084 | 0.6476 | Dense |
| [lawir_ko](lawir_ko.md) | Legal retrieval | `ko` | 200 | 3,562 | 200 | 1.00 | 0.5232 | 0.6534 | 0.6491 | Dense |
| [miracl_ko](miracl_ko.md) | Wikipedia retrieval | `ko` | 200 | 10,000 | 508 | 2.54 | 0.5069 | 0.6997 | 0.7121 | Reranking hybrid |
| [squad_kor_v1](squad_kor_v1.md) | Reading-comprehension retrieval | `ko` | 200 | 960 | 200 | 1.00 | 0.9618 | 0.9158 | 0.9585 | BM25 |

## Interpretation Notes for Model Researchers

The group separates three patterns. First, `autorag` and `squad_kor_v1` reward
models that preserve Korean lexical evidence and rank direct answer chunks
early. Second, `ko_strategy_qa` and `lawir_ko` reward semantic matching, because
the relevant passage can differ from the query in wording or legal formulation.
Third, `miracl_ko` benefits most from a hybrid candidate set, suggesting that
MIRACL-style Korean Wikipedia retrieval needs both named-entity overlap and
semantic relatedness.

Because best profiles are split across BM25, dense, and hybrid, a single group
average can hide important behavior. A model that improves `ko_strategy_qa` may
be learning semantic evidence retrieval, while a model that improves
`squad_kor_v1` may simply be better at precise context matching. Per-task
inspection is required before drawing conclusions about Korean retrieval
quality.

## Training and Leakage Notes

Useful training data includes non-overlapping Korean RAG question-to-chunk
pairs, Korean Wikipedia QA retrieval pairs, MIRACL Korean training examples,
Ko-StrategyQA evidence data, and Korean law/provision retrieval pairs. For
multi-positive tasks, listwise or multi-positive contrastive objectives match
the evaluation better than forcing each query to a single positive.

Leakage control should exclude Nano evaluation queries, positive passages,
qrels, and overlapping upstream test/dev examples from AutoRAG, Ko-StrategyQA,
LawIRKo, MIRACL Korean, and KorQuAD/SQuADKor sources. Synthetic data should
preserve Korean spacing and morphology, named entities, legal article numbers,
domain terms, dates, and quantities. Strong hard negatives should come from the
same report, same statute, same Wikipedia page family, or related evidence chain.

## Public Sources

- [AutoRAG: Automated Framework for optimization of Retrieval Augmented Generation Pipeline](https://arxiv.org/abs/2410.20878), 2024.
- [Did Aristotle Use a Laptop? A Question Answering Benchmark with Implicit Reasoning Strategies](https://arxiv.org/abs/2101.02235), 2021.
- [KorQuAD1.0: Korean QA Dataset for Machine Reading Comprehension](https://arxiv.org/abs/1909.07005), 2019.
- [MIRACL](http://miracl.ai/).
- [Massive Text Embedding Benchmark (MTEB)](https://github.com/embeddings-benchmark/mteb).
- [yjoonjang/markers_bm](https://huggingface.co/datasets/yjoonjang/markers_bm).
- [taeminlee/Ko-StrategyQA](https://huggingface.co/datasets/taeminlee/Ko-StrategyQA).
- [on-and-on/lawgov_ir-ko](https://huggingface.co/datasets/on-and-on/lawgov_ir-ko).
- [mteb/MIRACLRetrieval](https://huggingface.co/datasets/mteb/MIRACLRetrieval).
- [yjoonjang/squad_kor_v1](https://huggingface.co/datasets/yjoonjang/squad_kor_v1).

### Source Reference Table

| Source | Year | Type | URL |
| --- | ---: | --- | --- |
| AutoRAG: Automated Framework for optimization of Retrieval Augmented Generation Pipeline | 2024 | paper | [https://arxiv.org/abs/2410.20878](https://arxiv.org/abs/2410.20878) |
| Did Aristotle Use a Laptop? A Question Answering Benchmark with Implicit Reasoning Strategies | 2021 | paper | [https://arxiv.org/abs/2101.02235](https://arxiv.org/abs/2101.02235) |
| KorQuAD1.0: Korean QA Dataset for Machine Reading Comprehension | 2019 | paper | [https://arxiv.org/abs/1909.07005](https://arxiv.org/abs/1909.07005) |
| MIRACL |  | benchmark page | [http://miracl.ai/](http://miracl.ai/) |
| Massive Text Embedding Benchmark (MTEB) |  | benchmark repository | [https://github.com/embeddings-benchmark/mteb](https://github.com/embeddings-benchmark/mteb) |
| yjoonjang/markers_bm |  | dataset card | [https://huggingface.co/datasets/yjoonjang/markers_bm](https://huggingface.co/datasets/yjoonjang/markers_bm) |
| taeminlee/Ko-StrategyQA |  | dataset card | [https://huggingface.co/datasets/taeminlee/Ko-StrategyQA](https://huggingface.co/datasets/taeminlee/Ko-StrategyQA) |
| on-and-on/lawgov_ir-ko |  | dataset card | [https://huggingface.co/datasets/on-and-on/lawgov_ir-ko](https://huggingface.co/datasets/on-and-on/lawgov_ir-ko) |
| mteb/MIRACLRetrieval |  | dataset card | [https://huggingface.co/datasets/mteb/MIRACLRetrieval](https://huggingface.co/datasets/mteb/MIRACLRetrieval) |
| yjoonjang/squad_kor_v1 |  | dataset card | [https://huggingface.co/datasets/yjoonjang/squad_kor_v1](https://huggingface.co/datasets/yjoonjang/squad_kor_v1) |
