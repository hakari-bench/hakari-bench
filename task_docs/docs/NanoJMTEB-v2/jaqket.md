# NanoJMTEB-v2 / jaqket

## Overview

`NanoJMTEB-v2 / jaqket` is the Nano split of JAQKET, a Japanese quiz-question
to Wikipedia entity retrieval task. A query is a Japanese quiz clue, and the
correct document is the Wikipedia-style entity page that answers the clue. This
is different from ordinary web search or FAQ retrieval: the model must infer an
entity from attributes, aliases, definitions, dates, roles, or descriptions,
then retrieve a long entity document. The Nano split has 200 queries, 10,000
documents, and exactly one positive qrel per query. The current retrieval
profile is balanced: BM25 and dense retrieval are nearly tied at nDCG@10 and
hit@10, while the `reranking_hybrid` candidate set gives the strongest observed
top-10 and top-100 coverage.

## Details

### What the Original Data Measures

JAQKET, "Japanese Questions on Knowledge of Entities", was introduced as a
Japanese question answering dataset built around quiz questions. In the
retrieval formulation used by MTEB and JMTEB, a quiz-style Japanese question is
used as the query, and the relevant document is the Wikipedia passage or entity
page corresponding to the answer.

The original task therefore measures entity retrieval from clue text. The query
may not name the answer directly. Instead, it can describe an origin, a
geographical nickname, a work, a sports object, a historical period, an alias,
or a property. A strong retrieval model must map those clues to the answer
entity and remain robust to long document text that contains far more
information than the query mentions.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 200 positive qrel
rows. Every query has one positive document, with no multi-positive queries.
Queries average 52.98 characters. Documents are much longer than in most Nano
retrieval tasks, averaging 5,363.14 characters, because positives are
Wikipedia-like entity pages rather than short passages.

Representative questions ask for entities such as Golden Week, Budapest, the
mudskipper known in Japanese as "mutsugoro", the Age of Discovery, and the
barbell. These queries often include enough lexical evidence for exact matching,
but the main task is answer-entity identification. The correct document may be
found through a distinctive phrase in the clue, through semantic inference, or
through recognizing an alias or defining property.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset contains 500 candidates per query and
achieves nDCG@10 = 0.7837, hit@10 = 0.8650, and recall@100 = 0.9450. BM25 is
strong on this task because quiz clues often include rare and informative terms:
place nicknames, historical periods, named people, technical object parts,
geographic references, or distinctive descriptions. When those words also occur
in the entity page, lexical matching can rank the positive highly.

The limitation is that BM25 cannot fully solve entity inference. If the query
describes the answer without naming it, or if the decisive clue is expressed
through an alias or indirect property, surface overlap may point to related
entities instead. The long documents also increase distractor risk: many entity
pages contain broad contextual words, and a related but wrong page can share
several clue terms.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset also has 500 candidates per
query. It reaches nDCG@10 = 0.7830, hit@10 = 0.8650, and recall@100 = 0.9300.
Top-10 dense retrieval is nearly identical to BM25 by these metrics, indicating
that semantic entity matching is helpful but does not dominate the lexical
signals in this Nano split.

Dense retrieval is useful when the query describes a concept rather than
repeating the title or answer name. It can connect "the Hungarian capital called
the Pearl of the Danube" to the Budapest page, or a definition of a sports
object to the correct entity. Its lower recall@100 suggests that some positives
are still best preserved by exact words, aliases, or Japanese surface forms
that dense embeddings may blur among related entities.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains 100 or 101 candidates per
query, with 7 safeguard positive rows and a mean of 100.035 candidates. It
achieves nDCG@10 = 0.7876, hit@10 = 0.8750, and recall@100 = 0.9650. The gains
over BM25 and dense retrieval are modest but consistent across the reported
metrics.

This is a classic hybrid entity-retrieval pattern. BM25 contributes rare clue
terms and exact Japanese aliases. Dense retrieval contributes semantic mapping
from clue descriptions to entity pages. The hybrid set is not a dramatic
top-10 breakthrough, but it provides the best candidate coverage and slightly
better rank quality. For reranking experiments, this means the task rewards a
model that can combine clue-word precision with entity-level semantic
recognition.

### Metric Interpretation for Model Researchers

Because every query has one positive document, hit@10 measures whether the
answer entity page appears in the first ten results, and nDCG@10 measures how
high it is ranked within those results. Recall@100 matters for reranking
pipelines because it tells whether the positive entity survives candidate
generation.

The key interpretation is that `jaqket` is not strongly dominated by one
retrieval family. BM25 and dense retrieval are essentially tied in top-10
quality, while hybrid retrieval provides the most complete candidate pool. This
makes the task a useful diagnostic for Japanese models that must handle both
exact clue terms and conceptual entity inference.

### Query and Relevance Type Tendencies

Queries are quiz-style Japanese questions. They often end with a phrase such as
"what is it?" or "where is it?", and they may mention enough properties to
identify an entity without giving the answer name. The relevant document is a
long entity page, so the match is between a compact clue and a broad
encyclopedic document.

This setup rewards models that can identify answer entities, handle aliases and
descriptive names, and compare a short clue to long document context. It also
tests whether long-document embeddings or rerankers can focus on the relevant
parts of an entity page instead of being diluted by unrelated sections.

### Representative Failure Modes

BM25 can fail when a clue's distinctive words also appear in related entity
pages, or when the answer is implied by properties rather than named. Dense
retrieval can fail by retrieving a semantically related entity in the same
category, such as another city, period, object, animal, or person. Hybrid
retrieval reduces these errors but still requires reranking that can resolve the
exact answer from the clue.

Long documents introduce another failure mode: the positive page may contain the
right evidence, but it is surrounded by thousands of characters of unrelated
context. Models that average document meaning too coarsely may miss the decisive
snippet, while models that overfocus on sparse terms may confuse related pages.

### Training Data That May Help

Helpful training data includes Japanese quiz QA, entity linking, question-to-
Wikipedia-page retrieval, alias-aware entity matching, and hard negatives from
neighboring entity categories. Training pairs should include questions that
describe entities indirectly rather than always naming them. Long positive
documents are useful because the benchmark itself uses long entity pages.

Comparable benchmark reporting should avoid training on the same JAQKET
validation or test questions, Nano examples, or exact positive entity passages.
Synthetic data can be useful if it is generated from non-evaluation Wikipedia
pages and includes clue styles similar to real quiz questions.

### Model Improvement Notes

Dense retrievers can improve by learning Japanese entity aliases, definitions,
and property-to-entity mappings while preserving rare clue terms. Sparse systems
benefit from good tokenization of Japanese names, katakana terms, compounds, and
foreign-language aliases. Rerankers should be trained to compare the clue
against the most relevant portions of a long entity page, not just to score the
global topical similarity of the page.

For hybrid search systems, `jaqket` suggests that lexical and dense evidence are
both necessary. The best candidate set is the one that keeps exact clue matches
while also admitting semantically inferred answer entities.

## Example Data

Representative questions ask for the common name of Japan's late-April to early-
May holiday period, the Hungarian capital known as the Pearl of the Danube, the
mudskipper species associated with Ariake and Yatsushiro Seas, the historical
period of European overseas expansion from the 15th to 17th centuries, and the
weightlifting equipment made from a shaft and plates. The positives are long
Wikipedia-style entity pages for Golden Week, Budapest, mutsugoro, the Age of
Discovery, and barbell.

### Public Sources

- [JAQKET: クイズを題材にした日本語 QA データセットの構築](https://www.anlp.jp/proceedings/annual_meeting/2020/pdf_dir/P2-24.pdf),
  2020.
- [mteb/jaqket](https://huggingface.co/datasets/mteb/jaqket), MTEB dataset
  card.
- [sbintuitions/JMTEB](https://huggingface.co/datasets/sbintuitions/JMTEB),
  Japanese embedding benchmark card.
- [hakari-bench/NanoJMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoJMTEB-v2),
  Nano benchmark dataset.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| JAQKET: クイズを題材にした日本語 QA データセットの構築 | 2020 | paper | https://www.anlp.jp/proceedings/annual_meeting/2020/pdf_dir/P2-24.pdf |
| mteb/jaqket |  | dataset card | https://huggingface.co/datasets/mteb/jaqket |
| sbintuitions/JMTEB | 2024 | dataset card | https://huggingface.co/datasets/sbintuitions/JMTEB |

### Representative Snippets

| Query pattern | Positive document pattern |
| --- | --- |
| A quiz clue about a Japanese holiday period whose name originated as a 1950s film-industry promotion term. | The Wikipedia-style page for Golden Week, including alternate names and the late-April to early-May holiday period. |
| A clue asking for the Hungarian capital called the Pearl of the Danube. | The Budapest entity page, including its Hungarian name and history as a city on both sides of the Danube. |
| A clue about a goby-family fish living in the Ariake and Yatsushiro Seas and linked to a writer's nickname. | The mutsugoro entity page describing the mudskipper species, distribution, and Japanese names. |
| A clue about the 15th to 17th century when Europeans expanded by ship into Asia and the Americas. | The Age of Discovery entity page describing European voyages and the historical period. |
| A clue about weightlifting equipment made from a shaft and plate weights. | The barbell entity page describing the shaft, plates, and weight-training use. |
