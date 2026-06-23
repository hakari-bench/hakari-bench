# NanoMTEB-French / fquad

## Overview

`fquad` is a French passage-retrieval task derived from FQuAD, a French
question-answering benchmark built from French Wikipedia. Each query is a
French reading-comprehension question, and the positive document is the
Wikipedia passage that contains the evidence needed to answer it. The Nano
split contains 200 queries, 269 candidate documents, and 200 positive qrels,
with exactly one positive passage per query. Because the document pool is small
and the passages are article-like paragraphs with explicit entities, dates, and
definitions, this task is a compact test of whether a retrieval model can map a
French question to the answer-bearing encyclopedic passage. It is especially
useful for studying the boundary between lexical matching and semantic QA
retrieval in a native French setting.

## Details

### What the Original Data Measures

[FQuAD: French Question Answering Dataset](https://arxiv.org/abs/2002.06071)
introduced a SQuAD-style reading-comprehension benchmark for French, using
native French questions and answer spans over French Wikipedia passages. The
larger FQuAD line later added unanswerable examples in FQuAD2.0, but this Nano
retrieval task focuses on answer-bearing passages: the model is not asked to
extract the answer span, only to retrieve the passage that contains the evidence.

The resulting retrieval problem is narrower than open-domain web search but
closer to how QA retrieval is used in a reader-reranker pipeline. Queries are
short natural questions, while documents preserve enough surrounding context to
make the answer identifiable. A good model needs to recognize French question
forms, named entities, paraphrased predicates, and local topical context.

### Observed Data Profile

The Nano split has 200 French queries, 269 documents, and 200 positive
judgments. Query text averages 56.21 characters, while documents average 898.31
characters. The documents are much longer than the questions and usually contain
article-title prefixes followed by compact encyclopedic prose. Examples cover
biographical, historical, film, religious, political, and scientific topics.

The single-positive setup makes each query a direct evidence-location task. A
retriever cannot benefit from many interchangeable positives, but the small
candidate pool means the target passage is often lexically close to the query.
The corpus size is also below the nominal top-500 candidate depth, so BM25 and
dense candidate lists effectively cover all 269 documents for every query.

### BM25 Evaluation Profile

BM25 is very strong on this task: the dataset-provided BM25 candidates reach
nDCG@10 of 0.8899, hit@10 of 0.9700, and recall@100 of 1.0000. The result shows
that exact or near-exact term overlap is highly informative for FQuAD-style
French retrieval. Many questions reuse salient nouns, named entities, or
answer-bearing phrases from the positive passage, so BM25 can often rank the
right paragraph near the top without modeling deep semantics.

This does not mean the task is trivial. Errors are more likely when a question
asks for a relation that is expressed with different wording in the passage, or
when several paragraphs share the same article title and entities. Still, the
dominant retrieval signal is lexical specificity: rare names, film titles,
institution names, and dates tend to anchor the correct document.

### Dense Evaluation Profile

The dense harrier-oss-270m candidate column is weaker than BM25 here, with
nDCG@10 of 0.8102, hit@10 of 0.9250, and recall@100 of 0.9600. Dense retrieval
still performs well, indicating that the semantic relationship between French
questions and answer-bearing passages is learnable. However, the drop against
BM25 suggests that embedding similarity sometimes smooths over the exact
lexical cues that distinguish one Wikipedia paragraph from another.

For model researchers, this is a useful diagnostic: a dense model that improves
substantially on this task likely handles French entity grounding, question
intent, and long-passage pooling well. A model that underperforms BM25 may still
be semantically fluent, but may not preserve enough fine-grained entity and
phrase identity for compact QA retrieval.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate set reaches nDCG@10 of 0.8666, hit@10 of
0.9500, and recall@100 of 1.0000. It recovers the complete top-100 relevant
coverage of BM25 while ranking slightly below BM25 at the top of the list. This
is the expected shape for a hybrid search emulation when lexical matching is
already very strong: the hybrid list protects recall and combines semantic and
lexical evidence, but it does not automatically beat the best lexical ordering
for the first ten positions.

There are no safeguard rank-101 rows for this task, because the positive
documents are already covered in the top-100 hybrid candidates. The hybrid
profile is therefore best read as a high-recall candidate pool for later
reranking rather than as proof that dense semantics dominate the task.

### Metric Interpretation for Model Researchers

`fquad` is a BM25-favorable French QA retrieval task. The most important metric
comparison is not only absolute nDCG@10, but the gap between BM25, dense, and
hybrid behavior. BM25 leads at top-10 ranking, dense loses some recall by 100,
and `reranking_hybrid` restores recall while staying close to BM25. A reranker
evaluated on this candidate pool should be expected to exploit both exact
entity overlap and question-passage entailment.

Because each query has one positive, nDCG@10 and hit@10 are easy to interpret:
they largely measure whether the correct passage appears early. Recall@100
measures whether a downstream reranker has any chance to recover the correct
answer. On this split, failures below recall@100 are more concerning for dense
retrievers than for lexical or hybrid candidate generation.

### Query and Relevance Type Tendencies

Queries are extractive French questions asking who, when, where, why, or what
relationship holds. The relevant document normally states the answer directly
inside a Wikipedia-style paragraph. Some questions are entity-heavy, while
others depend on recognizing a paraphrased event or role.

Relevance is evidence-based rather than topical-only. A paragraph about the same
person or film is not enough if it does not contain the required fact. This
makes same-article hard negatives useful: they share many surface terms but lack
the precise answer evidence.

### Representative Failure Modes

BM25 can fail when the query uses a paraphrase and the positive passage uses a
different formulation, or when several candidate passages share the same entity
name and broad topic. Dense retrieval can fail in the opposite direction by
retrieving a semantically related paragraph that lacks the exact answer-bearing
fact. Both approaches can confuse adjacent passages from the same article when
the title prefix dominates the representation.

Hybrid retrieval is less likely to miss the target entirely, but its top ranks
can still be pulled toward passages that are lexically similar or semantically
near but not answer-bearing. This makes the task a good candidate for testing
cross-encoder rerankers and late-interaction models over a compact top-100 pool.

### Training Data That May Help

Useful training data includes non-overlapping FQuAD train examples, French
Wikipedia QA retrieval pairs, same-article hard negatives, and French extractive
QA paraphrases. Training should exclude FQuAD test examples, Nano queries,
qrels, and positive French Wikipedia passages likely to overlap with the
evaluation split.

Synthetic data can be useful if it keeps the evidence structure explicit:
generate French Wikipedia-style paragraphs with entities, dates, definitions,
and roles, then generate answerable French questions whose answer is stated in
the paragraph. The most valuable negatives are not random documents, but nearby
paragraphs from the same topic that do not answer the question.

### Model Improvement Notes

Models should preserve exact French entity names while also handling question
paraphrase. Strong passage pooling matters because the answer evidence may be a
small span inside a much longer paragraph. For dense models, contrastive
training with same-article negatives can reduce over-reliance on topical
similarity. For rerankers, explicit attention to answer-bearing spans should
improve top-10 ordering beyond candidate recall.

## Example Data

| Query | Positive document |
| --- | --- |
| Quand est-ce que Pierre Lambert est proche des Jésuites ? [57 chars] | pierre-lambert-de-la-motte_2_36 La spiritualité de Pierre Lambert de La Motte évolue tout au long de sa vie. Il est marqué par son époque et principalement par le centralisme issue de l'Église post tr... [200 / 786 chars] |
| Comment se nomme le frère de Carnot ? [37 chars] | sadi-carnot-(physicien)_12_8 Parmi ses écrits posthumes, un manuscrit intitulé Recherche d’une formule propre à représenter la puissance motrice de la vapeur d’eau, rédigé entre novembre 1819 et mars... [200 / 1,382 chars] |
| Pour quoi sont réputés les deux frères engagés par Wallis ? [59 chars] | casablanca-(film)_7_9 Ce sont Julius J. et Philip G. Epstein qui sont engagés par Wallis pour adapter la pièce au grand écran. Réputés pour leur esprit ironique, les deux frères introduisent plusieurs... [200 / 732 chars] |
| Qui tire sur Strasser ? [23 chars] | casablanca-(film)_7_7 Lorsque Renault tente d'arrêter Laszlo, Rick double le policier en l'obligeant, sous la menace d'une arme, à laisser partir le couple. Il convainc également Ilsa de prendre l'avi... [200 / 640 chars] |
| De quelle société Hal B. Wallis fait-il parti ? [47 chars] | casablanca-(film)_7_18 Dans les années 1940, Casablanca était une ville paisible sur l'Atlantique jusqu'au jour où Hal B. Wallis, producteur de la Warner Bros., tombe sur la pièce Everybody Comes to R... [200 / 857 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| FQuAD: French Question Answering Dataset | 2020 | Paper | [https://arxiv.org/abs/2002.06071](https://arxiv.org/abs/2002.06071) |
| FQuAD2.0: French Question Answering and knowing that you know nothing | 2021 | Paper | [https://arxiv.org/abs/2109.13209](https://arxiv.org/abs/2109.13209) |
| manu/fquad2_test | 2024 | Dataset card | [https://huggingface.co/datasets/manu/fquad2_test](https://huggingface.co/datasets/manu/fquad2_test) |

### Representative Snippets

| Query | Positive document excerpt |
| --- | --- |
| Quand est-ce que Pierre Lambert est proche des Jesuites ? | A passage about Pierre Lambert de La Motte's spirituality and the religious context that shaped him. |
| Comment se nomme le frere de Carnot ? | A Sadi Carnot passage describing posthumous writings and family context. |
| Pour quoi sont reputes les deux freres engages par Wallis ? | A Casablanca passage identifying Julius J. and Philip G. Epstein and their ironic style. |
| Qui tire sur Strasser ? | A Casablanca plot passage where Rick stops Renault and lets Laszlo and Ilsa leave. |
| De quelle societe Hal B. Wallis fait-il parti ? | A Casablanca production passage linking Hal B. Wallis to Warner Bros. |
