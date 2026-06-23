# MNanoBEIR / NanoBEIR-no / NanoSCIDOCS

## Overview

NanoBEIR-no NanoSCIDOCS is a Norwegian scientific-document retrieval task
derived from SCIDOCS. Queries are translated scientific titles or short
research descriptions, and documents are translated abstracts or document
descriptions. The task is valuable for evaluating related-paper retrieval
rather than direct answer retrieval: the relevant documents are scientifically
connected through method, topic, citation neighborhood, or research problem.
This makes it a compact multilingual benchmark for models that need to
represent scholarly relatedness across longer technical text.

## Details

### What the Original Data Measures

SCIDOCS was introduced with SPECTER as an evaluation suite for scientific
document representations. In BEIR, SCIDOCS is used as a scientific retrieval
task where systems retrieve papers or abstracts related to a query paper or
scientific description. The MNanoBEIR Norwegian version keeps this scholarly
retrieval objective after translation. It measures whether a model can connect
research documents by scientific content, including method similarity,
disciplinary context, and citation-like relatedness.

### Observed Data Profile

This Nano subset contains 50 queries, 2,210 documents, and 244 positive qrels.
Every query has multiple positives, with an average of 4.88 positives per
query, a minimum of 3, median of 5.00, and maximum of 5. Queries average 75.04
characters, while documents average 934.18 characters. This creates a
multi-positive scholarly retrieval setting where the model must recover several
related documents for each query, not simply one answer passage.

### BM25 Evaluation Profile

BM25 uses the `bm25` top-500 candidate subset. It reaches nDCG@10 0.2153,
hit@10 0.6800, and recall@100 0.3852. Scientific vocabulary provides useful
lexical anchors: method names, domain terms, acronyms, and technical phrases
often repeat across related documents. However, scientific relatedness is not
always lexical. Papers can be related through shared methods, datasets, or
problem framing while using different terminology. BM25 therefore finds some
obvious matches but has limited coverage of the full related-document set.

### Dense Evaluation Profile

Dense retrieval uses the `harrier_oss_v1_270m` top-500 candidate subset. It
scores nDCG@10 0.3412, hit@10 0.8400, and recall@100 0.6721, clearly
outperforming BM25. This is the expected pattern for related-paper retrieval:
embedding similarity can capture conceptual and disciplinary connections that
do not depend on exact word overlap. Dense retrieval is especially helpful for
linking a query title to abstracts that discuss a similar method or research
area using different phrasing. The remaining gap suggests that generic dense
representations still struggle with fine-grained scientific distinctions and
translation artifacts in technical prose.

### Reranking Hybrid Evaluation Profile

The reranking hybrid subset uses `reranking_hybrid` with top-100 candidates and
an optional rank-101 safeguard. Candidate counts range from 100 to 101, with a
mean of 100.02 and 1 safeguard row. It reaches nDCG@10 0.2467, hit@10 0.7200,
and recall@100 0.6270. The hybrid pool improves substantially over BM25 recall
and nearly approaches dense coverage, but its top-10 ranking is weaker than
dense. This means the mixed candidate pool is useful for reranking because it
contains both lexical term matches and semantic related-paper candidates, but
the initial hybrid order needs a stronger scientific relevance model.

### Metric Interpretation for Model Researchers

Because all queries have multiple positives, hit@10 only indicates that at
least one related paper was found. Recall@100 is important for measuring how
much of the related-document set is available to a reranker, while nDCG@10
shows whether the most relevant related documents are ranked early. The dense
profile is strongest across the main metrics, indicating that scientific
document retrieval benefits heavily from semantic representation. The hybrid
profile's relatively high recall but lower nDCG highlights a common reranking
opportunity: use a broad candidate pool, then apply a domain-aware model that
can judge method, dataset, and contribution similarity.

### Query and Relevance Type Tendencies

Queries are scholarly titles or compact scientific descriptions. Relevant
documents are abstracts or descriptions of papers in related research areas.
Examples include power converters, Gaussian Markov fields, texture synthesis,
antenna design, and digital heart monitoring. The relevance relation is broader
than duplicate text and narrower than general topic similarity: related
documents should share scientific purpose, methodology, or problem context.
This favors models that understand technical terminology and the structure of
scientific contributions.

### Representative Failure Modes

BM25 may over-rank abstracts that repeat technical words while addressing a
different method or application. Dense models may retrieve papers from the same
discipline but miss the specific contribution or dataset relation. Hybrid
retrieval may include useful candidates from both groups, but a reranker still
needs to separate true related work from same-field distractors. Translation
can add noise in technical text, including awkward terminology or untranslated
phrases, which can affect both lexical and semantic matching.

### Training Data That May Help

Helpful training data includes non-overlapping citation recommendation,
related-paper retrieval, scientific abstract pairs, title-to-abstract retrieval,
and multilingual scholarly text. Hard negatives should come from the same
field but differ in method, task, dataset, or claim. Training should exclude
SCIDOCS, SPECTER evaluation data, BEIR, NanoBEIR, and overlapping translated
scientific abstracts.

### Model Improvement Notes

NanoSCIDOCS-no is a good diagnostic for scientific retrieval models because it
tests relatedness rather than direct answer containment. Dense retrieval is the
strongest single profile, while reranking hybrid provides a mixed pool with
useful coverage. Improvements should focus on scientific-domain embeddings,
technical term normalization, citation-style contrastive learning, and
rerankers that compare methods and contributions. For research workflows, the
most informative metric is whether a model can retrieve several genuinely
related papers, not only the paper with the closest title wording.

## Example Data

| Query | Positive document |
| --- | --- |
| Ny DC-DC Flernivå Boostkonverter [32 chars] | AbstructMultilevel spenningskilder omformere dukker opp som nye typer kraftomformere for høyeffektsapplikasjoner. Multilevel spenningskilder omformere syntetiserer vanligvis en trappet spenningsbølge... [200 / 962 chars] |
| Hurtig læringsalgoritme for sparsete Gaussiske Markov-felt basert på Cholesky-faktorisering [91 chars] | Sure, please provide the English document text that you need translated into Norwegian. [87 chars] |
| Tekstursyntese ved hjelp av konvolusjonelle neuronnettverk [58 chars] | I denne arbeidet undersøker vi hvordan dybden av et konvolusjonelt nettverk påvirker dets nøyaktighet i store bildegjenkjenningssettinger. Vår hovedbidrag er en grundig vurdering av nettverk med økend... [200 / 792 chars] |
| Planar bredbåndsannulærringantenne med sirkulær polarisering for RFID-system [76 chars] | I denne artikkelen foreslås en horisontalt meanderende strip (HMS) matningsmetode for å oppnå god impedansmatching og symmetriske bredsideutstrålingsmønstre for en enkeltmatet bredbånds sirkulært pola... [200 / 1,263 chars] |
| Utforming av avansert digital hjerteovervåker ved bruk av grunnleggende elektroniske komponenter [96 chars] | I denne artikkelen presenterer vi design og utvikling av en ny integrert enhet for måling av hjertefrekvens ved bruk av fingertupp for å forbedre estimering av hjertefrekvens. Da hjertesykdommer øker... [200 / 1,047 chars] |

### Public Sources

- [SPECTER: Document-level Representation Learning using Citation-informed Transformers](https://arxiv.org/abs/2004.07180).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [NanoBEIR-no dataset](https://huggingface.co/datasets/hakari-bench/NanoBEIR-no).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| SPECTER: Document-level Representation Learning using Citation-informed Transformers | 2020 | task paper | [https://arxiv.org/abs/2004.07180](https://arxiv.org/abs/2004.07180) |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | [https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663) |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | [https://arxiv.org/abs/2502.13595](https://arxiv.org/abs/2502.13595) |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | [https://huggingface.co/collections/zeta-alpha-ai/nanobeir](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
