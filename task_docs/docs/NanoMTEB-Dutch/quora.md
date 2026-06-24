# NanoMTEB-Dutch / quora

## Overview

`quora` is the Dutch Quora duplicate-question retrieval task from BEIR-NL.
Queries and documents are Dutch translations of Quora questions, and relevance
means that another question has the same user intent. The Nano split contains
200 queries, 10,000 documents, and 573 positive qrel rows. It is multi-positive:
80 queries have more than one duplicate, the average is 2.87 positives per
query, and one query has 50 positives.

This task measures paraphrase retrieval, not answer-passage retrieval. BM25 is
already strong because many duplicates share key nouns, entities, or short
phrases. Dense retrieval with `harrier_oss_v1_270m` is clearly strongest in
nDCG@10, while `reranking_hybrid` has the highest hit@10 and recall@100. The
task is useful for evaluating whether a model can distinguish true duplicate
intent from same-topic non-duplicates, especially when several alternative
question phrasings are valid positives.

## Details

### What the Original Data Measures

BEIR uses the Quora Question Pairs data as a duplicate-question retrieval task.
The original release contains hundreds of thousands of question pairs labeled
for whether two Quora questions are semantically duplicate. BEIR constructs a
retrieval setting from duplicate clusters, where a query question should
retrieve other questions with the same intent.

BEIR-NL translates the public BEIR data into Dutch. This split should therefore
be read as Dutch-translated duplicate-question retrieval. The documents are not
answers or passages; they are other short questions. Relevance is semantic
equivalence of the question, not topical similarity.

### Observed Data Profile

Queries average 51.80 characters and documents average 66.56 characters, so
both sides are short. The corpus has 10,000 question documents, and the qrels
contain 573 positives. The positive-count distribution is uneven: many queries
have one duplicate, but some belong to larger paraphrase clusters.

Representative examples ask about the best drama TV series, whether
mathematics is art or science, the best classical music piece, GMAT institutes
in Delhi/NCR, and the strengths of the Indian army. These examples show that
minor word changes can preserve intent, while same-topic questions can still be
non-duplicates.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 = 0.8391, hit@10 = 0.9550, and recall@100 = 0.9023 over
top-500 candidate lists. This is a strong sparse baseline. Short duplicate
questions often reuse the most important words, such as place names, exam
names, public figures, or topic nouns. When the duplicate is a near-paraphrase,
BM25 performs well.

BM25's remaining weakness is semantic equivalence under different wording. It
can miss a duplicate that changes verbs, asks from a different angle, or uses a
synonym. It can also over-rank a same-topic question that shares many words but
asks for different information. That distinction is central to Quora-style
retrieval.

### Dense Evaluation Profile

Dense retrieval with `harrier_oss_v1_270m` reaches nDCG@10 = 0.9289, hit@10 =
0.9600, and recall@100 = 0.9494. This is the strongest top-ranked profile. The
large nDCG@10 gain over BM25 indicates that embedding similarity captures
duplicate intent and paraphrase structure beyond exact word overlap.

Dense retrieval is especially effective when two questions ask the same thing
with different word order or phrasing. Its likely failures are same-topic
questions with subtly different intent: for example, "best way to learn X" may
not duplicate "is X worth learning", even if both are close in embedding space.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate column reaches nDCG@10 = 0.8772, hit@10 =
0.9700, and recall@100 = 0.9791, with exactly 100 candidates per query and no
safeguard rows. Hybrid retrieval has the best recall and hit rate, but its
top-10 ranking is lower than dense retrieval. This means the hybrid pool is
excellent for candidate generation, while dense retrieval gives a better
initial order.

The hybrid pool combines lexical near-duplicates from BM25 with semantic
paraphrases from dense retrieval. A reranker can benefit from this high-recall
pool if it is trained to demote same-topic non-duplicates.

### Metric Interpretation for Model Researchers

This task has many multi-positive queries, so recall@100 and nDCG@10 should be
interpreted over duplicate clusters rather than a single target. Hit@10 is high
for all three candidate sources, so nDCG@10 is more useful for top-order
comparison. Dense retrieval is best for ranking, while hybrid retrieval is best
for exposing more duplicate positives to a reranker.

Cluster-aware or multi-positive training is important. Treating each query as
having only one positive would throw away much of the supervision.

### Query and Relevance Type Tendencies

Queries are short natural-language questions about advice, education,
technology, entertainment, public figures, travel, and general knowledge.
Relevant documents are alternate questions with the same intent. They may share
wording closely or express the same request with a different formulation.

Relevance is duplicate intent. A question can mention the same topic and still
be non-relevant if it asks for a different decision, fact, or opinion.

### Representative Failure Modes

BM25 can fail on paraphrases with different surface words. Dense retrieval can
fail on same-topic but non-equivalent questions. Hybrid retrieval can include
both true duplicates and high-overlap distractors, requiring careful reranking.

Hard negatives should share entities or topics while changing intent. These
are more useful than random questions because the benchmark already has strong
lexical and semantic signals.

### Training Data That May Help

Useful training data includes official Quora duplicate-question training data
with split overlap removed, Dutch paraphrase and duplicate-question pairs,
multilingual community-QA duplicate datasets, and same-topic non-duplicate hard
negatives. Training should exclude translated Quora test questions, duplicate
clusters, qrels, and positives from this Nano split.

Synthetic data can be built as clusters of Dutch paraphrased questions. Each
cluster should contain several equivalent phrasings and nearby non-equivalent
questions that change the user's intent.

### Model Improvement Notes

Improving this task requires paraphrase-sensitive representations and
duplicate-intent reranking. Dense models should learn invariance to word order,
synonyms, and minor framing changes while preserving intent boundaries.

For rerankers, the key behavior is deciding whether two questions could share
the same answer thread. Hybrid retrieval gives strong candidate coverage, but
dense retrieval gives the sharper first-stage order.

## Example Data

| Query | Positive document |
| --- | --- |
| Wat zijn de beste drama tv-series? [34 chars] | Wat zijn de beste drama-tv-series? [34 chars] |
| Beschouw je wiskunde als kunst of als wetenschap? [49 chars] | Is wiskunde een kunst of een wetenschap? [40 chars] |
| Wat is volgens jou het beste klassieke muziekstuk aller tijden? [63 chars] | Wat is het beste klassieke muziekstuk aller tijden? [51 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | arXiv paper | [https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663) |
| BEIR-NL: Zero-shot Information Retrieval Benchmark for the Dutch Language | 2025 | ACL paper | [https://aclanthology.org/2025.bucc-1.5/](https://aclanthology.org/2025.bucc-1.5/) |
| Quora Question Pairs | 2017 | dataset competition | [https://kaggle.com/competitions/quora-question-pairs](https://kaggle.com/competitions/quora-question-pairs) |
| clips/beir-nl-quora |  | dataset card | [https://huggingface.co/datasets/clips/beir-nl-quora](https://huggingface.co/datasets/clips/beir-nl-quora) |

### Representative Snippets

| Query | Positive passage |
| --- | --- |
| Wat zijn de beste drama tv-series? | A duplicate asks the same question with only minor punctuation and compounding changes. |
| Beschouw je wiskunde als kunst of als wetenschap? | A duplicate asks whether mathematics is an art or a science. |
| Wat is volgens jou het beste klassieke muziekstuk aller tijden? | A duplicate asks for the best classical music piece of all time. |
| Wat zijn enkele van de beste GMAT-instituten in Delhi/NCR? | A duplicate asks for the best GMAT coaching institute in the Delhi NCR region. |
| Wat zijn de grootste sterktes van het Indiase leger? | A duplicate asks for the greatest strong points of the Indian army. |
