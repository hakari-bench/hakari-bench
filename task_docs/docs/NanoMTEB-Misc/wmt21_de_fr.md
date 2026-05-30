# NanoMTEB-Misc / wmt21_de_fr

## Overview

`wmt21_de_fr` is the WMT21 German-French CLSD retrieval direction. Queries are
French news sentences, and documents are German candidate sentences. The
positive document is the German translation counterpart of the French query.
The Nano split contains 200 queries, 4,465 documents, and 200 positive qrels,
with one positive per query. Queries average 170.07 characters, and documents
average 177.26 characters. This task evaluates German-French sentence-level
semantic equivalence on WMT21-style news text, where translation meaning matters
more than lexical overlap.

## Details

### What the Original Data Measures

[Cross-Lingual Semantic Discrimination for Building Better Multilingual Embeddings](https://arxiv.org/abs/2502.08638)
introduces CLSD as a benchmark for distinguishing true cross-lingual semantic
equivalents from plausible distractors. The
[Andrianos/clsd_wmt19_21](https://huggingface.co/datasets/Andrianos/clsd_wmt19_21)
dataset provides WMT19 and WMT21 German-French retrieval variants built from
parallel news sentence data.

In this split, French sentences retrieve German translations. The benchmark
tests whether multilingual embeddings can represent sentence meaning across
languages while rejecting same-topic but non-equivalent sentences.

### Observed Data Profile

The split has 200 French queries, 4,465 German documents, and 200 positive
judgments. Every query has one positive. Sentences are Reuters-style financial
and political news, with names, dates, percentages, institutions, COVID-era
economic context, and quoted statements.

Examples include Justin Trudeau testifying before a committee, Sebastian
Pinera's pension-fund reform, capital requirements for investors, Apple and
Amazon earnings, and Trudeau's admission of a conflict-related mistake.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.3127, hit@10 of 0.4400, and recall@100 of 0.6950.
It is weak because the query and document are in different languages. It
succeeds mainly when sentences share proper names, dates, percentages, company
names, or international terms.

The score is a reminder that lexical retrieval is not a reliable solution for
cross-lingual translation retrieval. The key signal is semantic equivalence.

### Dense Evaluation Profile

Dense retrieval is dominant, with nDCG@10 of 0.9249, hit@10 of 0.9700, and
recall@100 of 0.9700. The dense model aligns French and German sentence meaning
well, even when the wording differs substantially. This is the expected shape
for a sentence-level translation retrieval task.

For researchers, failures should be inspected for subtle distinctions: changed
numbers, actors, dates, modality, or attribution. Broad topical similarity is
not enough.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` profile reaches nDCG@10 of 0.5988, hit@10 of 0.7300,
and recall@100 of 0.9950. It has the best recall@100 but much weaker top-10
ranking than dense retrieval. Candidate lists contain 100 to 101 entries, with
one safeguard-positive row.

Hybrid search is useful for candidate recoverability, but lexical matching
injects many distractors into early ranks. A reranker can benefit from the
hybrid pool, while dense retrieval remains the better first-stage ranker.

### Metric Interpretation for Model Researchers

`wmt21_de_fr` is dense-favorable for top ranking and hybrid-favorable for
recall. Since each query has one positive, nDCG@10 and hit@10 directly measure
where the true translation appears. Recall@100 matters for reranking pipelines,
especially because `reranking_hybrid` exposes nearly all positives.

The task is a clean cross-lingual semantic discrimination benchmark rather than
a general news search task.

### Query and Relevance Type Tendencies

Queries are French news sentences, and positives are German translations.
Sentences often contain named entities, market figures, government actions, and
quoted claims. Distractors can preserve entities or numbers while altering the
event detail.

Relevance is strict translation equivalence. Same-topic sentences are hard
negatives unless they express the same meaning.

### Representative Failure Modes

BM25 fails when there are few shared names or numbers. Dense retrieval can fail
on near-translation distractors with changed modality, time, actor, or
quantity. Hybrid retrieval can over-rank sentences with matching entities even
when the statement differs.

Finance-news examples are especially sensitive to numbers and dates: matching
the companies is not enough if the event or estimate differs.

### Training Data That May Help

Useful training data includes German-French parallel news data,
sentence-transformer contrastive training, translation-pair mining, and hard
negatives with the same entities and altered facts. Training should avoid WMT21
evaluation pairs and overlapping distractors.

Synthetic data should use non-evaluation French-German sentence pairs and
create distractors that preserve market numbers, names, or organizations while
changing the meaning.

### Model Improvement Notes

Models should prioritize sentence-level cross-lingual equivalence. Dense
encoders need hard negative training over translation-like distractors. Rerankers
should compare the full proposition across languages, including numbers,
negation, attribution, and temporal details.

## Example Data

### Public Sources

- [Cross-Lingual Semantic Discrimination for Building Better Multilingual Embeddings](https://arxiv.org/abs/2502.08638)
- [Andrianos/clsd_wmt19_21](https://huggingface.co/datasets/Andrianos/clsd_wmt19_21)
- [hakari-bench/NanoMTEB-Misc](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Misc)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Cross-Lingual Semantic Discrimination for Building Better Multilingual Embeddings | 2025 | Task paper | https://arxiv.org/abs/2502.08638 |
| Andrianos/clsd_wmt19_21 | 2025 | Dataset card | https://huggingface.co/datasets/Andrianos/clsd_wmt19_21 |

### Representative Snippets

| Query | Positive document |
| --- | --- |
| A French sentence about Justin Trudeau testifying before a committee. | The German translation announcing Trudeau would testify before the committee at a date to be determined. |
| A French sentence about Sebastian Pinera's pension-fund reform. | The German translation describing the July 24 reform allowing early withdrawal of 10 percent of pension funds. |
| A French sentence about minor adjustments freeing capital for investors. | The German translation about making it easier for companies to obtain financing. |
| A French sentence about Apple, Alphabet, Amazon, and second-quarter GDP. | The German translation about company results and the Commerce Department GDP estimate. |
| A French sentence about Trudeau admitting a mistake in UNIS negotiations. | The German translation saying he admitted he should have stayed out of the discussions. |
