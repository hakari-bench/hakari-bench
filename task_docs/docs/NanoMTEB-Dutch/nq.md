# NanoMTEB-Dutch / nq

## Overview

`nq` is the Dutch Natural Questions retrieval task from BEIR-NL. Queries are
Dutch translations of real Google search questions, and documents are
Dutch-translated Wikipedia passages. The Nano split contains 200 queries,
10,000 documents, and 242 positive qrel rows. Most queries have one positive,
but 38 queries have multiple positives, with at most three positives for one
query. It evaluates open-domain question-to-passage retrieval for natural,
short user information needs.

This task is substantially harder than translated FEVER because the query is a
question rather than a claim, and the relevant passage must contain the answer
relation. BM25 is useful but limited. Dense retrieval with `harrier_oss_v1_270m`
is clearly strongest in nDCG@10 and hit@10, while `reranking_hybrid` has the
highest recall@100. The task is therefore a good example of dense retrieval
being better for top-ranked answer-bearing passages, while hybrid retrieval is
better as a broad reranking pool.

## Details

### What the Original Data Measures

[Natural Questions: A Benchmark for Question Answering Research](https://aclanthology.org/Q19-1026/)
introduced NQ as real anonymized Google search questions paired with Wikipedia
pages from search results, with annotator-provided long and short answers when
available. BEIR adapts Natural Questions as an open-domain retrieval task:
given the user question, retrieve Wikipedia passages that contain the answer.

BEIR-NL translates public BEIR datasets into Dutch. This split is therefore a
Dutch translation of an English-origin open-domain QA retrieval benchmark. The
core task remains question-to-evidence retrieval, but independent translation
of questions and passages can introduce additional lexical mismatch.

### Observed Data Profile

The split has 200 queries and 10,000 documents. Queries average 52.69
characters and look like natural web questions, often asking who, when, how
many, what difference, or which institution. Documents average 595.40
characters and are Wikipedia-style passages with page titles and explanatory
text.

Representative queries ask when Chinese New Year occurs and which year it is,
the difference between RON and MON, who owned Puerto Rico before it belonged to
the United States, who decides what is produced in a market economy, and who
was the man who jumped from space. The positive passage must answer the asked
relation, not merely mention the main entity.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 = 0.4505, hit@10 = 0.7050, and recall@100 = 0.8760 over
top-500 candidate lists. Sparse retrieval benefits when the question includes a
distinct entity, title, or phrase that appears in the answer passage. It can
often retrieve the right Wikipedia page or a nearby article.

The weakness is relation matching. Questions such as "who introduced", "when
was it released", or "which university" require the passage to contain the
answer-bearing relation. BM25 can retrieve an entity page while failing to rank
the specific passage that answers the question. Translated wording can also
reduce exact term overlap between query and passage.

### Dense Evaluation Profile

Dense retrieval with `harrier_oss_v1_270m` reaches nDCG@10 = 0.6335, hit@10 =
0.8650, and recall@100 = 0.9008. It is the strongest top-10 candidate source by
a large margin. This indicates that embedding similarity is capturing the
semantic relation between a natural question and an answer-bearing Wikipedia
passage better than term frequency alone.

Dense retrieval is especially useful when the question is colloquial or when
the passage expresses the answer with different syntax. Its remaining failures
are likely entity-near or topic-near passages that are semantically related but
do not contain the requested answer. A strong model must preserve the question
operator and relation, not only the entity.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate column reaches nDCG@10 = 0.5473, hit@10 =
0.7700, and recall@100 = 0.9876, with 100 to 101 candidates per query and two
rank-101 safeguard rows. The hybrid pool has much higher recall@100 than dense
or BM25, but its top-10 ranking is worse than dense retrieval.

This profile is important for reranking. Hybrid search recovers nearly all
positive passages within the candidate pool by combining exact entity matches
from BM25 with semantic matches from dense retrieval. However, the initial
ranking includes many entity-near distractors. A reranker starting from this
pool must identify which candidate actually answers the question.

### Metric Interpretation for Model Researchers

The task has 242 positives for 200 queries, so most queries are single-positive
but multi-positive supervision should still be preserved. nDCG@10 measures
answer-passage ranking quality, hit@10 measures whether at least one relevant
passage is user-visible, and recall@100 measures reranking coverage.

The key contrast is dense top ranking versus hybrid coverage. Dense retrieval
is best if the first-stage result list is the product. Hybrid retrieval is best
if a second-stage reranker can exploit the high candidate recall.

### Query and Relevance Type Tendencies

Queries are natural Dutch search questions. They ask for entities, dates,
counts, definitions, ownership, releases, institutions, and relations. Relevant
documents are Wikipedia passages that explicitly contain the answer.

Relevance is answer bearing. A passage about the same entity is not enough if
it does not answer the relation requested by the question. Entity-near hard
negatives are therefore central to the task.

### Representative Failure Modes

BM25 can fail by ranking the main entity page but missing the answer passage.
Dense retrieval can fail by retrieving a semantically close passage about the
same entity or topic that does not answer the question. Hybrid retrieval can
include both the correct passage and many entity-overlap distractors, making
reranking necessary.

Translation can create additional failures when query wording and passage
wording diverge. Robust models should rely on the answer relation rather than
only exact Dutch terms.

### Training Data That May Help

Useful training data includes official Natural Questions training data with
overlap removed, Dutch Wikipedia question-answer retrieval pairs, multilingual
open-domain QA retrieval datasets, and hard negatives sharing entity pages but
not answer relations. Training should exclude translated NQ test questions,
qrels, and positive Wikipedia passages used by this Nano split.

Synthetic data can be generated from non-evaluation Dutch Wikipedia passages.
Create natural Dutch search questions about entities, dates, counts,
definitions, and relations. Hard negatives should share the entity or topic but
not contain the answer.

### Model Improvement Notes

Improving this task requires question-aware passage retrieval. Dense models
should encode question operators and answer relations, not only entities.
Rerankers should compare the query against the candidate passage and verify
that the passage contains the requested fact.

Hybrid retrieval is best treated as candidate generation here. Its recall is
excellent, but dense retrieval provides a stronger initial top order.

## Example Data

### Public Sources

- [Natural Questions: A Benchmark for Question Answering Research](https://aclanthology.org/Q19-1026/), 2019.
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663), 2021.
- [BEIR-NL: Zero-shot Information Retrieval Benchmark for the Dutch Language](https://aclanthology.org/2025.bucc-1.5/), 2025.
- [clips/beir-nl-nq](https://huggingface.co/datasets/clips/beir-nl-nq), source dataset card.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Natural Questions: A Benchmark for Question Answering Research | 2019 | ACL paper | https://aclanthology.org/Q19-1026/ |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | arXiv paper | https://arxiv.org/abs/2104.08663 |
| BEIR-NL: Zero-shot Information Retrieval Benchmark for the Dutch Language | 2025 | ACL paper | https://aclanthology.org/2025.bucc-1.5/ |
| clips/beir-nl-nq |  | dataset card | https://huggingface.co/datasets/clips/beir-nl-nq |

### Representative Snippets

| Query | Positive passage |
| --- | --- |
| Wanneer is Chinees Nieuwjaar en welk jaar is het? | A translated Wikipedia passage explains Chinese New Year and its relation to the traditional lunisolar calendar. |
| Wat is het verschil tussen RON en MON? | A translated passage about octane rating explains that Motor Octane Number is measured under different engine conditions than RON. |
| Aan wie behoorde Puerto Rico voordat het tot de VS behoorde? | A translated Puerto Rico passage describes the island's indigenous population and its claim by Spain during Columbus's voyage. |
| Wie neemt de beslissingen over wat er geproduceerd wordt in een markteconomie? | A translated passage explains market economy decisions through supply, demand, investment, production, and distribution. |
| Wie is de man die vanuit de ruimte sprong? | A translated passage identifies Felix Baumgartner and describes his high-altitude jump from a helium balloon. |
