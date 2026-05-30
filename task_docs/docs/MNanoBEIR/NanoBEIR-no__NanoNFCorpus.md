# MNanoBEIR / NanoBEIR-no / NanoNFCorpus

## Overview

NanoBEIR-no NanoNFCorpus is a Norwegian biomedical and nutrition retrieval
task derived from NFCorpus. Queries are short translated health search phrases,
and documents are translated biomedical or nutrition-related abstracts. The
task is valuable because it combines extremely short queries with long,
technical documents and a large set of relevant passages per query. It tests
whether retrieval models can connect lay or compact health expressions to
scientific evidence, while also handling biomedical vocabulary, synonymy, and
many-positive relevance judgments.

## Details

### What the Original Data Measures

NFCorpus was created as a learning-to-rank dataset for medical information
retrieval, with a focus on nutrition and health-related information needs. In
BEIR, it functions as a biomedical retrieval task. The MNanoBEIR Norwegian
version keeps the health-query to biomedical-document setup in a compact
translated form. It measures retrieval over medical and nutrition concepts,
including situations where a short phrase points to many relevant abstracts
rather than one exact answer.

### Observed Data Profile

This Nano subset contains 50 queries, 2,953 documents, and 1,651 positive
qrels. It is highly multi-positive: the average is 33.02 positives per query,
with a minimum of 1, median of 23.50, and maximum of 100. There are 47
multi-positive queries, covering 94.0% of the task. Queries average only 24.16
characters, while documents average 1,494.75 characters. This creates a broad
medical recall setting where a tiny query may correspond to many long abstracts
that discuss related evidence, mechanisms, or findings.

### BM25 Evaluation Profile

BM25 uses the `bm25` top-500 candidate subset. It reaches nDCG@10 0.2618,
hit@10 0.6400, and recall@100 0.1187. The top-10 ranking is competitive with
dense retrieval, but recall is very low relative to the large number of
positives. This reflects the task's structure: exact biomedical terms, food
names, symptoms, and organism names can give BM25 strong anchors for a few
documents, yet a short query has many relevant abstracts that do not repeat the
same surface wording. BM25 is useful for high-precision lexical matches but
does not cover the broader evidence set well.

### Dense Evaluation Profile

Dense retrieval uses the `harrier_oss_v1_270m` top-500 candidate subset. It
scores nDCG@10 0.2334, hit@10 0.5800, and recall@100 0.1878. Dense retrieval
has better recall@100 than BM25, showing that semantic similarity can recover
more relevant biomedical documents beyond exact term overlap. However, dense
top-10 ranking and hit@10 are lower. This suggests that dense similarity
spreads retrieval over a wider medical concept neighborhood, which helps
coverage but can rank broad or weakly related abstracts ahead of the most
directly relevant ones. Domain-specific biomedical embedding quality is likely
important here.

### Reranking Hybrid Evaluation Profile

The reranking hybrid subset uses `reranking_hybrid` with top-100 candidates and
an optional rank-101 safeguard. Candidate counts range from 100 to 101, with a
mean of 100.12 and 6 safeguard rows. It reaches nDCG@10 0.2722, hit@10 0.6800,
and recall@100 0.1841. This is the strongest early-ranking profile and nearly
matches dense recall@100. The hybrid behavior fits the biomedical setting:
lexical matching captures exact technical terms, while dense retrieval adds
semantic coverage for related abstracts. A hybrid candidate pool is therefore
particularly useful for reranking, even though the absolute recall remains low
because the number of positives per query is very large.

### Metric Interpretation for Model Researchers

This task must be interpreted as many-positive retrieval. Hit@10 only indicates
that at least one relevant abstract appeared early; it does not show whether
the system covered the relevant evidence set. Recall@100 is difficult because
some queries have dozens of positives, and the top-100 candidate budget cannot
include everything. nDCG@10 is still useful for judging whether the most useful
early results are relevant. The observed pattern shows a clear tradeoff: BM25
is relatively precise for exact terms, dense improves broader recall, and
reranking hybrid gives the best early precision by combining both signals.

### Query and Relevance Type Tendencies

Queries are short health or nutrition phrases, sometimes layperson-like and
sometimes technical. Relevant documents are long abstracts with scientific
background, methods, results, and conclusions. A query may refer to a food,
condition, nutrient, medical concern, or ethical topic, while relevant passages
may use technical biomedical terminology. This favors models that can bridge
consumer health wording and scientific language. It also rewards systems that
can retrieve a diverse set of abstracts rather than only the one with the
closest exact phrase.

### Representative Failure Modes

BM25 may focus on exact phrase overlap and miss abstracts that use synonyms,
abbreviations, or related biomedical concepts. Dense models may retrieve
conceptually related but clinically different documents, especially when a
short query lacks context. Hybrid systems can improve early ranking but may
still fail to cover enough positives because the relevant set is so large.
Translation adds another challenge when medical terms, food names, or
scientific expressions are rendered differently across query and document.

### Training Data That May Help

Helpful training data includes non-overlapping biomedical retrieval,
nutrition-focused QA, consumer health search, clinical abstract retrieval,
scientific synonym pairs, and multilingual medical IR. Hard negatives should
share symptoms, foods, organisms, or medical terms while discussing a different
finding or population. Training should exclude NFCorpus, BEIR, NanoBEIR, and
overlapping biomedical abstracts.

### Model Improvement Notes

NanoNFCorpus-no is a strong test of biomedical retrieval under short-query and
many-positive conditions. Reranking hybrid is the strongest early-rank profile,
while dense retrieval gives better broad coverage than BM25. Improvements
should focus on biomedical domain adaptation, synonym handling, query expansion
behavior, and rerankers that can distinguish direct evidence from loosely
related health content. For research, the most informative analysis is not only
whether a model finds one relevant abstract, but how much of the diverse
evidence set it can surface within a limited candidate budget.

## Example Data

| Query | Positive document |
| --- | --- |
| Sunn sjokolademelk | Mål: Å undersøke forholdet mellom inntak av kirsebær og risikoen for gjentatte giktangrep hos individer med gikt... |
| Medisinsk etikk | BAKGRUNN: En av de største utfordringene ved å kontrollere serumkolesterol gjennom diettintervensjoner... |
| bikubear | De siste 20 årene har økt interesse for L-arginins biokjemi, ernæring og farmakologi ført til omfattende studier... |
| Hva er egentlig i kyllingnuggets? | PURPOSE: Å fastslå innholdet i kyllingnuggets fra to nasjonale matkjeder... |
| mettet fett | Interessen for muligheten av at mors kosthold under graviditet kan påvirke utviklingen av allergiske lidelser hos barn har økt... |

### Public Sources

- [NFCorpus: A Full-Text Learning to Rank Dataset for Medical Information Retrieval](https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [NanoBEIR-no dataset](https://huggingface.co/datasets/hakari-bench/NanoBEIR-no).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| NFCorpus: A Full-Text Learning to Rank Dataset for Medical Information Retrieval | 2016 | task paper | https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | https://arxiv.org/abs/2104.08663 |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | https://arxiv.org/abs/2502.13595 |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | https://huggingface.co/collections/zeta-alpha-ai/nanobeir |
