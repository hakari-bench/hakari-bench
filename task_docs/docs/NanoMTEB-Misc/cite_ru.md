# NanoMTEB-Misc / cite_ru

## Overview

`cite_ru` is the Russian direct-citation retrieval task from RuSciBench. Queries
are Russian scientific paper titles and abstracts, and documents are abstracts
of candidate papers. Each query paper has exactly five positive documents,
representing papers directly cited by the query paper. The Nano split contains
200 queries, 10,000 documents, and 1,000 positive qrels. Queries are long,
averaging 1,399.06 characters, while documents average 926.86 characters. This
task evaluates scientific-document representation for citation retrieval, where
relevance is stricter than topical similarity.

## Details

### What the Original Data Measures

[RuSciBench: Open Benchmark for Russian and English Scientific Document Representations](https://doi.org/10.1134/S1064562424602191)
introduces a benchmark for Russian and English scientific texts from eLibrary.ru
and the Russian Science Citation Index. Its retrieval tasks include direct
citation prediction: given a scientific paper representation, retrieve papers
that it directly cites.

This setup is not ordinary semantic search. A relevant document must be a cited
paper, not merely another paper in the same field. Citation links often reflect
methodological, background, or prior-result relationships that may or may not be
obvious from abstract vocabulary alone.

### Observed Data Profile

The split has 200 Russian queries, 10,000 documents, and 1,000 positive
judgments. Every query has exactly five positives, so the task is uniformly
multi-positive. Queries contain title plus abstract text and are longer than the
documents. Documents are scientific abstracts across many disciplines.

Examples include geography education, fertilizer systems for winter rye,
finite-difference modeling of rock pressure, Russian perceptions of Japan, and
oil-filled composites. Positive documents are cited papers with related
methods, background, or empirical context.

### BM25 Evaluation Profile

BM25 is strong but not best, reaching nDCG@10 of 0.5566, hit@10 of 0.8950, and
recall@100 of 0.7840. It benefits from shared scientific terminology, method
names, material names, and domain-specific phrases. Direct citations often use
similar vocabulary because cited papers are in the same subfield.

BM25 is limited because citation relevance is not identical to lexical overlap.
Topically close papers may share many terms but not be citation targets, while
cited papers can use different wording for related methods or background
concepts.

### Dense Evaluation Profile

Dense retrieval is the best top-10 profile, with nDCG@10 of 0.6182, hit@10 of
0.9350, and recall@100 of 0.8260. Dense embeddings better capture scientific
semantic relationships across abstracts, including method similarity and
conceptual relatedness. They improve both early ranking and top-100 coverage
relative to BM25.

This makes `cite_ru` a useful diagnostic for Russian scientific embeddings. A
model must represent long abstracts, discipline terminology, and citation-like
relationships rather than only title-level topic.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` profile reaches nDCG@10 of 0.6134, hit@10 of 0.9200,
and recall@100 of 0.8400. It is slightly below dense retrieval in nDCG@10 and
hit@10, but it has the best recall@100. Candidate lists contain 100 to 101
entries, with three safeguard-positive rows.

This is a balanced dense/hybrid task. Dense retrieval provides the best early
ordering, while hybrid search exposes the most cited papers by rank 100. For a
downstream citation reranker, the hybrid pool may be valuable even when dense
ranking is cleaner at the top.

### Metric Interpretation for Model Researchers

`cite_ru` is dense-favorable for early ranking and hybrid-favorable for
candidate coverage. BM25 remains a strong baseline because scientific abstracts
reuse technical terms. Since every query has five positives, recall@100 is
important: a model should recover several cited papers, not only one.

nDCG@10 measures whether cited papers are ranked early among many topically
similar but non-cited abstracts. Hit@10 is easier to satisfy, because retrieving
any one of five positives counts as a hit.

### Query and Relevance Type Tendencies

Queries and documents are Russian scientific titles and abstracts. Positive
documents are directly cited papers. Relevance can reflect shared methods,
background literature, empirical domain, or theoretical framing.

The task is citation-specific. A same-topic abstract is a hard negative if the
query paper did not cite it. This makes citation graph supervision more useful
than generic semantic similarity labels.

### Representative Failure Modes

BM25 can over-rank same-field abstracts with shared terminology but no citation
link. Dense retrieval can over-rank conceptually similar papers that are not
actually cited. Hybrid retrieval can improve recall while still mixing true
cited papers with near-topic literature.

Long abstracts also create mixed signals: a query paper may mention several
subtopics, but only some correspond to citation targets.

### Training Data That May Help

Useful training data includes non-overlapping Russian citation graphs,
scientific title and abstract pairs, SPECTER-style citation training, and
Russian/English scientific bilingual embeddings. Hard negatives should be
topically close papers from the same discipline that are not citation-linked.

Synthetic data should start from real scientific abstracts and construct
citation-like positives only when a plausible bibliographic relation is known
or carefully simulated from cited-paper metadata. Generic topic pairs are too
weak for this task.

### Model Improvement Notes

Models should encode scientific terminology and citation intent. Dense encoders
need long-abstract representations and hard negatives from the same field.
Rerankers should distinguish actual bibliographic relationships from broad
disciplinary similarity.

## Example Data

### Public Sources

- [RuSciBench: Open Benchmark for Russian and English Scientific Document Representations](https://doi.org/10.1134/S1064562424602191)
- [mlsa-iai-msu-lab/ru_sci_bench_cite_retrieval](https://huggingface.co/datasets/mlsa-iai-msu-lab/ru_sci_bench_cite_retrieval)
- [ru_sci_bench_mteb repository](https://github.com/mlsa-iai-msu-lab/ru_sci_bench_mteb)
- [hakari-bench/NanoMTEB-Misc](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Misc)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| RuSciBench: Open Benchmark for Russian and English Scientific Document Representations | 2024 | Benchmark paper | https://doi.org/10.1134/S1064562424602191 |
| mlsa-iai-msu-lab/ru_sci_bench_cite_retrieval | 2025 | Dataset card | https://huggingface.co/datasets/mlsa-iai-msu-lab/ru_sci_bench_cite_retrieval |
| ru_sci_bench_mteb | 2025 | Code repository | https://github.com/mlsa-iai-msu-lab/ru_sci_bench_mteb |

### Representative Snippets

| Query | Positive document excerpt |
| --- | --- |
| A Russian abstract about developing geoinformation competencies in teacher education. | A cited abstract about integrating ICT tools in geography education training. |
| A Russian abstract evaluating fertilizer systems for winter rye under radioactive contamination. | A cited abstract on long-term organic and mineral fertilizer use for winter rye. |
| A Russian abstract on nonlinear rock-pressure modeling by finite differences. | A cited abstract on nonlinear-plastic stress distribution around a circular excavation. |
| A Russian abstract about Japan in Russian public consciousness. | A cited abstract on Japan and Japanese people in Russian phraseology. |
| A Russian abstract on mechanical characteristics of oil-filled composites. | A cited abstract analyzing oil filling effects on a metal counterbody surface. |
