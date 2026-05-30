# MNanoBEIR / NanoBEIR-pt / NanoNFCorpus

## Overview

NanoBEIR-pt NanoNFCorpus is a Portuguese biomedical and nutrition information
retrieval task derived from NFCorpus. Queries are very short translated health
or biomedical information needs, and documents are translated scientific or
medical passages. The task is notable for its many-positive structure: a short
query can have dozens of relevant documents. It is useful for evaluating
whether retrieval models can bridge consumer-health phrasing, biomedical
terminology, and long scientific abstracts in Portuguese.

## Details

### What the Original Data Measures

NFCorpus was built from nutrition and health information needs with expert
relevance judgments over medical text. In BEIR, it is used as a domain-specific
biomedical retrieval benchmark. The MNanoBEIR Portuguese version keeps this
health-query to scientific-document structure after translation. It measures
whether a model can retrieve medically relevant documents for short queries,
including cases where the relevant abstract uses technical terminology rather
than the query's surface words.

### Observed Data Profile

This Nano subset contains 50 queries, 2,953 documents, and 1,651 positive
qrels. It is highly multi-positive: the average is 33.02 positives per query,
with a minimum of 1, median of 23.50, and maximum of 100. There are 47
multi-positive queries, covering 94.0% of the task. Queries are extremely short
at 26.92 characters on average, while documents average 1,650.10 characters.
This produces a broad evidence retrieval setting where full coverage is much
harder than finding a single relevant abstract.

### BM25 Evaluation Profile

BM25 uses the `bm25` top-500 candidate subset. It reaches nDCG@10 0.2982,
hit@10 0.6600, and recall@100 0.1581. Exact biomedical, food, symptom, or
condition terms can give BM25 useful anchors, which explains its reasonable
top-10 behavior. However, recall is low because many relevant abstracts do not
repeat the same short query terms, and the positive set can be very large.
BM25 is therefore good at retrieving a few direct lexical matches but weak at
covering the full range of relevant biomedical evidence.

### Dense Evaluation Profile

Dense retrieval uses the `harrier_oss_v1_270m` top-500 candidate subset. It
scores nDCG@10 0.2966, hit@10 0.6600, and recall@100 0.1908. Dense retrieval
matches BM25 in hit@10 and nearly matches nDCG@10 while improving recall@100.
This suggests that embedding similarity expands coverage beyond exact term
matching, but the dense model also retrieves broad biomedical neighbors that
are not always the most directly relevant early results. The task likely
requires stronger biomedical domain adaptation to improve both precise ranking
and broad recall.

### Reranking Hybrid Evaluation Profile

The reranking hybrid subset uses `reranking_hybrid` with top-100 candidates and
an optional rank-101 safeguard. Candidate counts range from 100 to 101, with a
mean of 100.10 and 5 safeguard rows. It reaches nDCG@10 0.3146, hit@10 0.6200,
and recall@100 0.1987. Hybrid retrieval has the best nDCG@10 and recall@100,
although its hit@10 is slightly lower than BM25 and dense. This indicates that
the hybrid pool improves evidence diversity and early relevance quality, but
some queries still lack any relevant item in the first page. For reranking, it
offers the best coverage among the three candidate profiles.

### Metric Interpretation for Model Researchers

Because most queries have many positives, hit@10 is only a weak success
measure. A model may find one relevant abstract while missing most of the
evidence set. Recall@100 is especially important, but the task remains hard
because some queries have up to 100 positives and only 100 candidates are
evaluated in the hybrid profile. nDCG@10 shows early ranking quality. The
observed scores show that BM25 and dense are close in top ranking, while
hybrid retrieval gives the best overall balance for this Portuguese subset.

### Query and Relevance Type Tendencies

Queries are short health phrases or consumer biomedical questions, such as
healthy chocolate shakes, medical ethics, fava beans, chicken nuggets, and
saturated fat. Relevant documents are long scientific passages or abstracts
with methods, findings, and background information. The task favors models that
can connect everyday phrasing to technical biomedical language and retrieve
multiple relevant documents across a health topic.

### Representative Failure Modes

BM25 may focus on exact query terms and miss synonyms, broader clinical
concepts, or related abstracts. Dense models may retrieve medically related
but clinically different passages, especially when the query is only a short
phrase. Hybrid retrieval improves coverage but still struggles with the scale
of the positive set. Translation can also vary medical terminology and food
names, which affects both lexical matching and embedding similarity.

### Training Data That May Help

Helpful training data includes non-overlapping biomedical retrieval,
Portuguese medical question answering, consumer health search, nutrition QA,
scientific abstract retrieval, and multi-positive relevance training. Hard
negatives should share symptoms, foods, interventions, or organisms while
addressing a different finding or population. Training should exclude
NFCorpus, BEIR, NanoBEIR, and overlapping translated abstracts.

### Model Improvement Notes

NanoNFCorpus-pt is a demanding biomedical retrieval benchmark because queries
are very short and positives are numerous. Reranking hybrid is the strongest
overall profile, but all candidate sets have low recall relative to the size of
the relevance set. Improvements should focus on biomedical domain embeddings,
synonym handling, query expansion, and reranking that distinguishes direct
health evidence from loose topical similarity. Researchers should inspect both
early precision and breadth of evidence coverage.

## Example Data

| Query | Positive document |
| --- | --- |
| Batidas de chocolate saudáveis | Objetivo: Estudar a relação entre o consumo de cerejas e o risco de ataques recorrentes de gota em indivíduos com gota... |
| ética médica | Fundamentação: Um dos principais problemas no controle do colesterol sérico através de intervenção dietética parece ser a necessidade de melhorar a adesão... |
| favas | Nos últimos 20 anos, o crescente interesse pela bioquímica, nutrição e farmacologia da L-arginina levou a estudos extensivos... |
| Do que são feitos os nuggets de frango? | Objetivo: Determinar os componentes dos nuggets de frango de 2 redes de fast food nacionais... |
| gordura saturada | O interesse pelo possível impacto da ingestão alimentar materna durante a gravidez no desenvolvimento de doenças alérgicas em crianças tem aumentado... |

### Public Sources

- [NFCorpus: A Full-Text Learning to Rank Dataset for Medical Information Retrieval](https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [NanoBEIR-pt dataset](https://huggingface.co/datasets/hakari-bench/NanoBEIR-pt).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| NFCorpus: A Full-Text Learning to Rank Dataset for Medical Information Retrieval | 2016 | task paper | https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | https://arxiv.org/abs/2104.08663 |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | https://arxiv.org/abs/2502.13595 |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | https://huggingface.co/collections/zeta-alpha-ai/nanobeir |
