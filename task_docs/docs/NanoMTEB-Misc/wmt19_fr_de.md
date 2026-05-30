# NanoMTEB-Misc / wmt19_fr_de

## Overview

`wmt19_fr_de` is the reverse WMT19 German-French CLSD direction. Queries are
German news sentences, and documents are French candidate sentences. The
positive document is the French translation counterpart of the German query.
The Nano split contains 200 queries, 7,365 documents, and 200 positive qrels,
with one positive per query. Queries average 148.98 characters, and documents
average 154.22 characters. The task evaluates sentence-level cross-lingual
semantic equivalence from German into French, with lexical overlap limited
mostly to names, numbers, and international terms.

## Details

### What the Original Data Measures

[Cross-Lingual Semantic Discrimination for Building Better Multilingual Embeddings](https://arxiv.org/abs/2502.08638)
frames CLSD as a benchmark for multilingual embeddings that must recover true
translation equivalents while avoiding close semantic distractors. The
[Andrianos/clsd_wmt19_21](https://huggingface.co/datasets/Andrianos/clsd_wmt19_21)
dataset card provides WMT19 and WMT21 German-French retrieval variants built
from sentence-level news translation data.

In this split, German sentences retrieve French translations. Relevance is exact
cross-lingual semantic correspondence at sentence level.

### Observed Data Profile

The split has 200 German queries, 7,365 French documents, and 200 positive
judgments. Every query has one positive. The sentences are compact news
statements involving EU politics, public affairs, named entities, and quoted or
reported claims.

Examples mirror the opposite WMT19 direction: EU treaty voting rights, Europe
and populism, George Soros funding, a party congress in Bonn, and a Brussels
administrative leadership statement.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.3078, hit@10 of 0.4550, and recall@100 of 0.6700.
This is weak compared with dense retrieval, but slightly stronger than the
opposite WMT19 direction. BM25 succeeds mainly through shared named entities,
numbers, quotations, EU terminology, and cognates.

The result confirms that lexical term frequency is not enough for bilingual
sentence retrieval. Most true translation matches require semantic alignment
across German and French.

### Dense Evaluation Profile

Dense retrieval is dominant, with nDCG@10 of 0.9574, hit@10 of 0.9850, and
recall@100 of 0.9850. It nearly solves the task at top-10, showing strong
German-French sentence alignment. The model can retrieve true French
translations even when the German query shares little surface vocabulary with
the document.

For model researchers, this is a high-signal multilingual embedding benchmark:
top-ranking failures likely involve subtle translation distinctions rather than
gross topical mismatch.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` profile reaches nDCG@10 of 0.6054, hit@10 of 0.7800,
and recall@100 of 0.9950. It has the best recall@100 but is far below dense
retrieval in top-10 ranking. Candidate lists contain 100 to 101 entries, with
one safeguard-positive row.

This pattern shows that lexical signals can help expose the true translation
somewhere in the candidate pool, but they also introduce many top-rank
distractors. Dense retrieval remains the best first-stage ranking method.

### Metric Interpretation for Model Researchers

`wmt19_fr_de` is strongly dense-favorable. BM25 is limited by language mismatch,
and hybrid search is useful mainly for recall. Since every query has one
positive, nDCG@10 is a direct measure of where the true translation ranks.

The dense score is near ceiling, so remaining errors should be inspected for
fine-grained semantic discrimination: polarity, modality, named-entity role,
numeric detail, and sentence scope.

### Query and Relevance Type Tendencies

Queries are German news sentences, and positives are French translations.
Relevant documents must preserve the same meaning, not merely the same topic.
Distractors can share entities or event context while differing in predicate,
time, or stance.

This is strict sentence-pair retrieval, not document search or QA.

### Representative Failure Modes

BM25 fails on ordinary translation pairs with no shared tokens. Dense retrieval
can fail on near-equivalent distractors that differ in a small but important
detail. Hybrid retrieval can over-rank sentences with the same names or
international terms even when they are not translations.

Cross-lingual punctuation, quotation style, and named-entity spelling can also
affect retrieval.

### Training Data That May Help

Useful training data includes German-French bitext retrieval, multilingual
contrastive learning, translation ranking, and CLSD-style hard distractors.
Training should avoid WMT19 evaluation pairs and overlapping distractors.

Synthetic data should create German-French sentence pairs with hard negatives
that keep entities but alter event details, modality, number, actor, or
negation. Sentence-level contrastive objectives are more relevant than
paragraph-level topical retrieval.

### Model Improvement Notes

Models should optimize cross-lingual semantic equivalence with hard translation
distractors. Dense encoders are the primary retrieval component. Hybrid pools
may help reranking coverage, but lexical terms should not dominate early
ranking.

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
| A German sentence about Article 20 of the EU treaty and European Parliament voting rights. | The French translation about EU citizens exercising voting and eligibility rights in their Member State of residence. |
| A German sentence about Europe, climate change, internet-company taxation, and migration. | The French translation describing arguments against leaving Europe. |
| A German sentence about Soros supporting associations and initiatives. | The French translation describing humanitarian, social, scientific, and artistic support. |
| Sie nimmt deshalb auch nicht an dem Parteitag in Bonn teil. | C'est egalement pour cette raison qu'elle ne participe pas au congres du parti a Bonn. |
| A German sentence about a German becoming head of a Brussels authority. | The French translation about a German again becoming head of a Brussels administration. |
