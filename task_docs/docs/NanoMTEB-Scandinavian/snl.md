# NanoMTEB-Scandinavian / snl

## Overview

`snl` is the Norwegian NanoMTEB-Scandinavian retrieval adaptation of Store norske leksikon article data. The task pairs very short title-like queries, aliases, or headwords with long Norwegian encyclopedia entries. No standalone SNL retrieval paper was confirmed; the task is best understood through the Scandinavian Embedding Benchmarks paper and the source dataset cards that expose headline, category, ingress, and article fields.

The Nano split contains 200 queries, 1,300 documents, and exactly 200 positive relevance judgments. Each query has one positive article. Queries are extremely short, averaging about 14 characters, while documents average about 1,987 characters. Many queries are names or terms such as `Kasimir Edschmid`, `Hermann Bondi`, `bønn (kristendom)`, `Centrum-Demokraterne`, or `Joey Baron`. The task therefore evaluates headword-to-article retrieval with long-document ranking.

## Details

### What the Original Data Measures

The Scandinavian benchmark formalizes SNL data as retrieval from Norwegian lexicon content. The query is a headline or title-like string, and the relevant document is the corresponding encyclopedia entry or ingress. This is not a question-answering task and not duplicate retrieval. It is closer to entity, headword, and article lookup.

The source format matters. Articles include category information, ingress text, and body content, which can be much longer than the query. A model must preserve exact title signals while also representing the article's encyclopedic content well enough to disambiguate aliases or short terms.

### Observed Data Profile

The query side is extremely compact. Many queries are proper names, concept names, organizations, or short expressions. Documents are long entries that may include biography, history, definitions, works, and contextual sections. This length imbalance means the retrieval problem depends heavily on whether the model can connect a short headword to the correct long document.

Each query has a single positive, so there is no benefit from retrieving several related articles. If the model retrieves a category neighbor or same-surname article instead of the exact entry, the result is wrong.

### BM25 Evaluation Profile

BM25 is strong, with nDCG@10 of 0.8781, hit@10 of 0.9000, and recall@100 of 0.9200. This is expected because many queries are exact titles or distinctive headwords. If the title appears in the article, lexical matching works well.

BM25's weakness appears for ambiguous, short, or alias-like queries. It may retrieve articles that repeat the same surname, category term, or concept family. Long documents can contain many incidental mentions, so exact word overlap is not always enough to identify the corresponding entry.

### Dense Evaluation Profile

The dense `harrier-oss-270m` run is strongest, with nDCG@10 of 0.9599, hit@10 of 0.9800, and recall@100 of 0.9950. Dense retrieval improves over an already strong BM25 baseline by representing the headword and article content as a coherent semantic match. It appears especially useful when title strings are short or when the article's body provides additional disambiguating context.

This task is a good example where dense retrieval does not replace lexical matching because terms are absent, but rather improves title-article alignment beyond simple token overlap. The combination of short queries and long documents benefits from semantic article representation.

### Reranking Hybrid Evaluation Profile

`reranking_hybrid` reports nDCG@10 of 0.9024, hit@10 of 0.9150, and recall@100 of 0.9950. Candidate lists contain 100 to 101 items, and only 1 row uses the positive safeguard. Hybrid retrieval matches dense recall but has lower top-10 quality.

This suggests that lexical candidates help preserve positives, but they also introduce title-neighbor distractors that can weaken final ordering. For candidate generation, hybrid is robust. For direct ranking, dense retrieval is clearly stronger on this split.

### Metric Interpretation for Model Researchers

This split is dense-favorable, despite strong BM25 performance. BM25 sets a high lexical baseline, but dense retrieval substantially improves the chance that the exact article is ranked at the top. Hybrid retrieval is useful for recall but not the best final ranking.

Because every query has one positive, nDCG@10 is easy to interpret. It measures whether the corresponding article is placed near the top, not whether the system finds a cluster of related documents. This makes `snl` a clean diagnostic for title-to-article retrieval.

### Query and Relevance Type Tendencies

Representative queries are short headwords or names: literary figures, scientists, religious concepts, political parties, and musicians. The relevant documents are full encyclopedia entries with descriptions, biographies, definitions, or historical summaries.

The task rewards exact entity grounding. A query for a person should retrieve that person's article, not an article that merely mentions them. A query for a concept should retrieve the entry defining that concept, not a broader category page.

### Representative Failure Modes

BM25 may over-rank documents that mention the query string incidentally. Dense retrieval may retrieve a semantically related article from the same category but not the exact entry. Hybrid retrieval can include both kinds of distractors. These errors are especially likely for short names, common terms, or entries with overlapping categories.

Another failure mode is long-document dilution. The correct article may contain the query in a small part of a long body, while another article repeats the term more frequently. Models should distinguish article identity from mention frequency.

### Training Data That May Help

Useful training data includes non-overlapping SNL headline/article pairs, Norwegian encyclopedia title-to-article retrieval pairs, category-neighbor hard negatives, and alias or headword matching data. Training should exclude Nano titles, qrels, and matching article or ingress texts from this split.

Hard negatives should include articles with the same surname, same category, related concept family, or incidental mentions of the headword. These help a model learn exact entry retrieval rather than topical retrieval.

### Model Improvement Notes

Dense models can improve by representing very short Norwegian queries and long encyclopedia entries in the same space. Sparse systems can improve with title-field weighting and alias normalization. Hybrid systems can help preserve candidates, but final ranking should avoid over-rewarding incidental mentions in long documents.

For reranking, this task rewards models that can decide whether a long article is the canonical entry for a short query. Field-aware representations of headline, ingress, category, and article body may be especially useful.

## Example Data

### Public Sources

- Scandinavian Embedding Benchmarks paper: https://arxiv.org/abs/2406.02396
- Source dataset card: https://huggingface.co/datasets/adrlau/navjordj-SNL_summarization_copy
- MTEB task dataset card: https://huggingface.co/datasets/mteb/SNLRetrieval

### Source Reference Table

| Source | What it contributes |
| --- | --- |
| Scandinavian Embedding Benchmarks | Retrieval formalization for Scandinavian benchmark tasks. |
| SNL source dataset card | Headline, category, ingress, and article fields. |
| MTEB task card | Retrieval packaging of the SNL task. |

### Representative Snippets

- A query for `Kasimir Edschmid` retrieves a biography entry describing his literary work and contacts.
- A query for `Hermann Bondi` retrieves a biography entry about his move to Cambridge and wartime internment.
- A query for `bønn (kristendom)` retrieves an article about Christian prayer and the Lord's Prayer.
- A query for `Centrum-Demokraterne` retrieves an article about the party's government participation and electoral history.
- A query for `Joey Baron` retrieves an article about the musician's association with modernists such as Bill Frisell and John Zorn.
