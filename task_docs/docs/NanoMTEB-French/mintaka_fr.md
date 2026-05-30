# NanoMTEB-French / mintaka_fr

## Overview

`mintaka_fr` is the French retrieval split of Mintaka, a multilingual complex
question-answering benchmark. Each query is a French question, and each positive
document is a short answer string, entity name, title, or value. The Nano split
contains 200 queries, 1,714 documents, and 200 positive qrels, with one positive
per query. Unlike passage-retrieval tasks, the documents here average only 14.41
characters, so the model must connect a full natural-language question to a
compact answer label. This makes the task a useful stress test for multilingual
entity linking, semantic normalization, and complex-question understanding,
especially when the answer string does not share many words with the question.

## Details

### What the Original Data Measures

[Mintaka: A Complex, Natural, and Multilingual Dataset for End-to-End Question Answering](https://arxiv.org/abs/2210.01613)
introduced a dataset of complex, naturally elicited questions annotated with
Wikidata entities and translated into multiple languages, including French. It
targets question types such as comparison, counting, superlatives,
intersections, and multi-hop entity relations. The retrieval packaging used here
turns the QA benchmark into an answer-retrieval task: the model ranks answer
strings rather than long evidence passages.

This framing changes the difficulty. The retriever is not matching a query to a
paragraph that explains the answer; it is matching a question to the final
entity or value. The required signal is often implicit in world knowledge or
entity semantics, not in shared surface words.

### Observed Data Profile

The Nano split has 200 queries, 1,714 documents, and 200 positive judgments.
Queries average 71.61 characters, while documents average only 14.41 characters.
Sample positives include film titles, actor names, musicians, and other
canonical entities. The language field is multilingual because French questions
may map to answer strings that are in French, English, or mixed title forms.

The single-positive structure makes ranking unforgiving. A semantically related
answer is not acceptable if it is not the exact target entity. The short
documents also reduce the amount of text available for BM25, dense pooling, or
reranker attention. This is closer to multilingual answer selection than
traditional document retrieval.

### BM25 Evaluation Profile

BM25 is weak on this task: the dataset-provided BM25 candidates reach nDCG@10
of 0.2995, hit@10 of 0.3900, and recall@100 of 0.4750. This is expected because
many answer strings do not appear verbatim in the question. When a query asks
"Which actor played Han Solo and Indiana Jones?", the answer "Harrison Ford"
may have no lexical overlap with the descriptive clues. BM25 can only succeed
reliably when the answer name or distinctive title terms appear in the query.

The low recall@100 is especially important. More than half of the positives are
not reachable in the BM25 top-100 candidate pool, so a reranker that depends
only on lexical candidates would be bounded by candidate recall rather than by
its own scoring quality.

### Dense Evaluation Profile

The dense harrier-oss-270m candidates outperform BM25, with nDCG@10 of 0.3676,
hit@10 of 0.5300, and recall@100 of 0.7650. This is the strongest of the three
candidate profiles for this task. Dense retrieval can represent the semantic
relationship between a French complex question and its answer entity, even when
there is little or no direct word overlap.

The result also shows that the task remains difficult for dense models. The
answer documents are extremely short, and many possible answers are the same
type: films, people, places, or organizations. Dense models must separate
closely related entities using implicit relation clues, not just topical
similarity. Improvements on this split are likely to reflect better
entity-centric multilingual representations and stronger handling of complex
question composition.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` profile reaches nDCG@10 of 0.3400, hit@10 of 0.4500,
and recall@100 of 0.6550. It improves substantially over BM25 recall, but it
does not beat the dense candidate column. The candidate lists contain 100 to
101 entries per query, with 69 safeguard-positive rows. Those safeguards show
that many positives would otherwise sit outside the first 100 hybrid positions.

For this task, hybrid search is best understood as a compromise: it recovers
some semantic matches that BM25 misses while still retaining lexical evidence
when answer names appear in the query. However, because dense retrieval is the
dominant signal, mixing lexical candidates can dilute top-rank quality compared
with a strong dense-only candidate set.

### Metric Interpretation for Model Researchers

`mintaka_fr` is a dense-favorable retrieval task. BM25 struggles because the
documents are short answer labels, dense retrieval leads because it can encode
question-answer semantics, and `reranking_hybrid` sits between them. The
contrast is useful for diagnosing whether a model is doing entity-aware semantic
matching rather than passage-level lexical retrieval.

Because each query has exactly one positive, hit@10 and nDCG@10 are direct
signals of whether the target answer appears early. Recall@100 is the critical
candidate-generation metric: if the positive answer is absent from the top-100
pool, no reranker can recover it. On this split, dense recall@100 is much more
promising for downstream reranking than BM25 recall@100.

### Query and Relevance Type Tendencies

Queries are French complex QA questions over films, music, geography, sports,
history, and Wikidata-style relations. They often identify an entity indirectly
through roles, attributes, comparisons, or constraints. Positive documents are
canonical answer strings, not explanatory passages.

Relevance is exact-answer relevance. A document can be topically related but
wrong if it names another film, actor, or entity. This makes the task sensitive
to fine-grained entity identity and relation composition. It also means that
training with generic semantic similarity pairs is not enough; the model needs
answer-selection supervision.

### Representative Failure Modes

BM25 fails when the answer name is absent from the question or appears in a
different language or title variant. Dense retrieval can fail by selecting an
entity with the right broad type but the wrong relation, such as a different
film in the same franchise or another actor connected to the same clues. Hybrid
retrieval can inherit both issues: lexical matches may pull obvious but wrong
titles upward, while semantic matches may be too coarse to resolve the exact
answer.

The short-document format also limits reranker evidence. A cross-encoder cannot
read an explanatory passage, only the question and a short answer candidate, so
success depends on learned world knowledge and entity normalization.

### Training Data That May Help

Useful training data includes non-overlapping Mintaka train examples, French
Wikidata QA pairs, multilingual entity-linking supervision, and complex-question
paraphrases. Training should exclude Mintaka test examples, Nano queries, qrels,
and answer strings likely to overlap with the evaluation.

Synthetic data should generate French complex questions paired with short
canonical answers. Useful examples include film-role questions, music and sports
relations, geography constraints, and historical comparisons. Negatives should
be entity-type matched so the model learns to distinguish the correct answer
from plausible alternatives.

### Model Improvement Notes

Strong models for `mintaka_fr` need multilingual entity representations,
question decomposition, and answer normalization. They should map French clues
to answer labels that may not share surface terms with the query. Dense models
can improve through contrastive training on hard entity negatives, while
rerankers may benefit from auxiliary entity descriptions during training even
if evaluation documents remain short answer strings.

## Example Data

### Public Sources

- [Mintaka: A Complex, Natural, and Multilingual Dataset for End-to-End Question Answering](https://arxiv.org/abs/2210.01613)
- [mteb/MintakaRetrieval](https://huggingface.co/datasets/mteb/MintakaRetrieval)
- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316)
- [hakari-bench/NanoMTEB-French](https://huggingface.co/datasets/hakari-bench/NanoMTEB-French)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Mintaka: A Complex, Natural, and Multilingual Dataset for End-to-End Question Answering | 2022 | Paper | https://arxiv.org/abs/2210.01613 |
| MTEB: Massive Text Embedding Benchmark | 2023 | Paper | https://arxiv.org/abs/2210.07316 |
| mteb/MintakaRetrieval | 2025 | Dataset card | https://huggingface.co/datasets/mteb/MintakaRetrieval |

### Representative Snippets

| Query | Positive document |
| --- | --- |
| Quel film du debut des annees 1970 est-il celui pour lequel Bruce Lee est le plus connu ? | Operation Dragon |
| Quel acteur a joue Hans Solo et Indiana Jones ? | Harrison Ford |
| Quel est le nom du tout premier film du realisateur Kevin Smith ? | Clerks : Les Employes modeles |
| Quel film de Star Trek a le moins rapporte ? | Star Trek : Nemesis |
| Dans quel film de Major League ne figurait pas Charlie Sheen ? | Les Indians 3 |
