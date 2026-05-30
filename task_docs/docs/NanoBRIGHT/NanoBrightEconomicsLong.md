# NanoBRIGHT / NanoBrightEconomicsLong

## Overview

NanoBrightEconomicsLong is the long-document NanoBRIGHT slice for Economics StackExchange retrieval. It uses the same style of long economics queries as the compact passage task, but candidate documents are full cited source pages or long documents. The task measures whether a retriever can find the source document that contains the relevant economic model, empirical evidence, institutional explanation, or policy argument when the answer-bearing material may be buried inside a much larger page.

## Details

### What the Original Data Measures

BRIGHT's long-document variants test source-level retrieval rather than passage-level retrieval. For Economics, a query may ask about GDP accounting, taxes, central-bank financing, asset-market mechanics, welfare tradeoffs, or a derivation in a macroeconomic model. The relevant document can be a long report, paper, reference page, encyclopedia article, or finance education page.

The task therefore measures two abilities at once: matching the economic concept behind a detailed question and tolerating long-document noise. A relevant page may contain the needed section, but it can also include navigation material, definitions, tables, citations, examples, or adjacent economic topics that are not directly useful.

### Observed Data Profile

The task contains 103 queries, 515 documents, and 109 relevance judgments. Unlike the compact Economics slice, the long-document version is mostly single-positive: it has 1.06 positives per query on average, a minimum of 1, a median of 1.0, a maximum of 3, and only 5 multi-positive queries, or 4.85% of the set.

Queries average 739.57 characters, while documents average 38,615.97 characters. The corpus is much smaller than the passage version, but each candidate is far longer. This changes the retrieval problem from selecting among many short supporting passages to identifying which long source contains the right piece of economic evidence.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.2658, hit@10 of 0.4369, and recall@100 of 0.7248 using the top-500 BM25 candidate subset. The recall is reasonably high because long economic documents contain many terms that can overlap with detailed queries, including formulas, policy vocabulary, institutional names, and market terminology.

The top-rank performance is much weaker. Long pages can mention the right words in unrelated sections, or repeat broad terms such as market, tax, GDP, capital, or policy without answering the query. BM25 can place the positive somewhere in the candidate pool but often fails to rank it high enough for direct use.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.4266, hit@10 of 0.6602, and recall@100 of 0.9083. Dense retrieval is the strongest profile for all three headline metrics in this long-document task. It substantially improves over BM25 and slightly exceeds reranking_hybrid in recall@100.

This suggests that the long Economics task is dominated by semantic support matching. The model must connect a detailed economic puzzle to a source page whose overall content and central concepts align with the requested explanation. Embedding similarity is better than term frequency at recognizing the relevant economics source despite long-document noise.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.3764, hit@10 of 0.5728, and recall@100 of 0.8991. It uses a top-100 candidate range with an optional rank-101 safeguard; this task has 10 safeguard rows, candidate counts from 100 to 101, and a mean of 100.10 candidates.

Hybrid retrieval remains strong as a compact candidate pool, but dense retrieval is better in the reported metrics. The useful interpretation is that sparse signals add coverage for some formulaic or named-concept queries, while the fused ordering can dilute dense's strongest semantic matches. For reranking experiments, reranking_hybrid is still valuable because it keeps recall high in only about 100 candidates.

### Metric Interpretation for Model Researchers

This task is a clear example where dense retrieval is stronger than BM25 and stronger than the hybrid fused order at the top of the ranking. BM25's high recall@100 compared with its low nDCG@10 indicates that exact terms can locate relevant pages, but not rank them reliably. Dense retrieval provides the best top-rank signal.

For model researchers, the important difficulty is not corpus size but document granularity. With only 515 documents, the challenge might look small, yet each document is long enough to contain many distracting economic terms. A system that represents only global topic may retrieve plausible pages; a system that preserves the relevant economic mechanism will rank better.

### Query and Relevance Type Tendencies

Queries include long-form questions about national accounting, RBC model transformations, deficit financing, equity versus efficiency, order-book matching, and requests for credible economic sources. Positive documents include full reference pages, long policy or research documents, encyclopedia-like pages, and finance explanations.

Relevance is usually tied to a specific section or argument inside the document. A long source may be relevant because one paragraph defines a model, one table supports an empirical point, or one section explains an institutional process. The rest of the document may be only loosely related.

### Representative Failure Modes

Common failures include ranking a long page because it repeats the query's economic vocabulary while omitting the needed explanation, confusing a related policy topic with the specific claim, missing a full paper whose abstract uses different language from the query, and losing evidence because the positive signal is a small part of a long page.

BM25 is especially exposed to repeated terms and boilerplate. Dense retrieval can still over-rank documents that share the broad topic but not the exact mechanism. Hybrid retrieval improves candidate robustness, but final quality depends on a reranker or document model that can inspect the relevant section.

### Training Data That May Help

Useful training data includes long economics reports aligned to questions, document-level paper recommendation data, cited-source retrieval from economics forums, and passage-to-full-document distillation where a model learns to map a short evidence span back to its source page.

Synthetic data should generate long economics documents with abstracts, definitions, examples, tables, and policy context, then create detailed questions answerable by one section. Hard negatives should be long documents from the same economic topic with the wrong model, country, time period, or empirical claim.

### Model Improvement Notes

For this task, dense retrieval is the strongest observed first-stage method, but practical systems should still preserve sparse signals for named models, formulas, and institutional phrases. Long-document models may benefit from hierarchical pooling, passage aggregation, late interaction, or source-page reranking over extracted sections.

Because most queries have only one positive, small rank changes matter. Training should emphasize exact source support rather than broad topical relevance. Reranking_hybrid is a useful high-recall diagnostic pool, but the top ranking should be judged against dense's strong baseline.

## Example Data

### Public Sources

The original task is based on BRIGHT's reasoning-intensive retrieval benchmark, with NanoBRIGHT providing the compact dataset packaging and long-document split.

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original benchmark paper | [BRIGHT](https://arxiv.org/abs/2407.12883) |
| Project page | [BRIGHT project page](https://brightbenchmark.github.io/) |
| Source dataset | [xlangai/BRIGHT](https://huggingface.co/datasets/xlangai/BRIGHT) |
| NanoBRIGHT dataset | [hakari-bench/NanoBRIGHT](https://huggingface.co/datasets/hakari-bench/NanoBRIGHT) |

Representative query and positive source snippets:

| Query | Positive document snippet |
| --- | --- |
| Would a GDP measure be improved by excluding foreign interest paid? | A long OECD-style page provides country-level well-being and economic context. |
| Why does a derivative expression appear in an RBC capital equation? | A long reference page includes production-function and substitution-elasticity material. |
| What is the purpose of taxes if central banks can fund deficit spending? | A long economics paper discusses money growth, inflation, and policy relationships. |
| Is there always a tradeoff between efficiency and equity? | A long economics association page or article discusses welfare-related distortions. |
| How are stock prices determined when orders match? | A finance education page explains matching orders and how exchanges pair buy and sell requests. |
