# NanoMMTEB-v2 / wino_grande

## Overview

`NanoMMTEB-v2 / wino_grande` is an English commonsense-reasoning retrieval task
adapted from WinoGrande. Queries are Winograd-style sentences with a blank, and
documents are short candidate referent strings. The Nano split has 200 queries,
5,095 documents, and 200 positive qrel rows, with exactly one positive document
per query. Current diagnostics show `reranking_hybrid` as the strongest
profile, BM25 as second, and dense retrieval as slightly weaker. The task tests
whether retrieval can combine surface referent matching with commonsense
resolution.

## Details

### What the Original Data Measures

WinoGrande is an adversarially filtered Winograd Schema Challenge at scale. It
tests commonsense pronoun and referent resolution by presenting sentences where
two candidates are plausible unless the model uses the sentence's causal,
social, physical, or intentional constraints. The retrieval version treats the
masked sentence as the query and the correct referent string as the positive
document.

The task measures retrieval over very short candidate answers. A model must
select the entity or noun that correctly fills the blank, not just the one that
appears nearby.

### Observed Data Profile

The Nano split contains 200 queries, 5,095 documents, and 200 positive qrel
rows. Every query has exactly one positive document. Queries average 111.98
characters, while documents average 7.68 characters.

Documents are usually names or short nouns, such as "water", "apple",
"Carrie", or a candidate entity from the sentence. Queries are single
Winograd-style sentences with one blank and commonsense cues.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset contains 500 candidates per query and
achieves nDCG@10 = 0.5084, hit@10 = 0.8750, and recall@100 = 1.0000. BM25 is
strong because candidate referents often appear verbatim in the query sentence.

However, lexical evidence alone does not solve the task. Both candidate
referents may appear in the sentence, and the correct one is determined by
commonsense constraints. BM25 can find candidates but cannot reliably decide
which referent fits the blank.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset contains 500 candidates per
query and achieves nDCG@10 = 0.4940, hit@10 = 0.7750, and recall@100 = 0.9800.
Dense retrieval is close to BM25 by nDCG@10 but weaker by hit@10 and recall.

The difficulty is that candidate documents are extremely short. A dense vector
for a single noun or name provides little context, so the model must rely almost
entirely on how the query sentence maps to candidate meaning.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains 100 candidates per query and
achieves nDCG@10 = 0.6139, hit@10 = 0.9050, and recall@100 = 1.0000. Hybrid
retrieval is the best observed profile across the reported metrics.

This is a useful hybrid case. BM25 preserves exact candidate strings from the
sentence, while dense evidence adds some commonsense compatibility. The hybrid
ranking better balances candidate presence and semantic fit than either source
alone.

### Metric Interpretation for Model Researchers

This task is single-positive: each sentence has one correct referent. Hit@10
measures whether that referent appears near the top. nDCG@10 is sensitive to
rank, and recall@100 measures whether the candidate remains available to
rerankers.

Because candidate documents are tiny, retrieval scores partly reflect candidate
generation and partly reflect reasoning. A reranker or cross-encoder can add
value by reading the full sentence and candidate together.

### Query and Relevance Type Tendencies

Queries are English masked commonsense sentences. They involve physical
properties, intentions, preferences, social roles, causal relations, possession,
or event order. Relevant documents are short candidate referent strings.

The task rewards coreference reasoning, commonsense constraints, and careful
binding of candidate nouns to sentence roles.

### Representative Failure Modes

BM25 can rank the wrong candidate high because both referents appear in the
sentence. Dense retrieval can struggle with short answer strings and may prefer
a generally common or semantically related noun. Hybrid retrieval can still fail
when the correct answer requires a subtle physical or social inference.

Rerankers should evaluate the sentence with each candidate inserted into the
blank and choose the referent that makes the sentence coherent.

### Training Data That May Help

Useful training data includes Winograd-style pronoun resolution, coreference
question answering, commonsense cloze tasks, and candidate-referent retrieval
pairs. The Nano split's WinoGrande sentences, qrels, and answer candidates
should be excluded from training.

Synthetic data can generate masked commonsense sentences with two plausible
referents. Positives should require a commonsense relation such as cause,
possession, physical property, intention, or social role. Hard negatives should
include the competing referent from the same sentence.

### Model Improvement Notes

Sparse systems should preserve candidate string matches but need reasoning
reranking. Dense retrievers should improve short-candidate representation and
commonsense compatibility scoring. Cross-encoders can directly compare the
masked sentence with each candidate.

For hybrid systems, `NanoMMTEB-v2 / wino_grande` is a positive example:
`reranking_hybrid` outperforms both BM25 and dense retrieval. The remaining
challenge is commonsense reranking among exact candidate strings.

## Example Data

| Query | Positive document |
| --- | --- |
| Sentence: Mary wanted to get another piercing in her ear, but the _ was much too tiny.. [87 chars] | ear [3 chars] |
| Sentence: She counted her calories for her diet and found she needed more so she ate a brownie instead of an apple since the _ has fewer.. [138 chars] | apple [5 chars] |
| Sentence: The game of chess was easy to play for Angela but not Rebecca because _ had a analytical mind.. [105 chars] | Angela [6 chars] |

### Public Sources

- [WinoGrande: An Adversarial Winograd Schema Challenge at Scale](https://arxiv.org/abs/1907.10641),
  2019.
- [WinoGrande project page](https://winogrande.allenai.org/).
- [mteb/WinoGrande](https://huggingface.co/datasets/mteb/WinoGrande).
- [hakari-bench/NanoMMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoMMTEB-v2),
  Nano benchmark dataset.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| WinoGrande: An Adversarial Winograd Schema Challenge at Scale | 2019 | task paper | [https://arxiv.org/abs/1907.10641](https://arxiv.org/abs/1907.10641) |
| WinoGrande project page | 2019 | project page | [https://winogrande.allenai.org/](https://winogrande.allenai.org/) |
| mteb/WinoGrande | 2024 | dataset card | [https://huggingface.co/datasets/mteb/WinoGrande](https://huggingface.co/datasets/mteb/WinoGrande) |

### Representative Snippets

| Query pattern | Positive document pattern |
| --- | --- |
| A sentence about wanting another piercing but the blank was too tiny. | The answer string "ear." |
| A calorie-counting sentence comparing a brownie and an apple. | The answer string "apple." |
| A chess sentence contrasting Angela and Rebecca. | The answer string "Angela." |
| A sentence about going to a bakery before the bank because of limited supply. | The answer string "bakery." |
| A sentence about preferring to be outside and arguing for a pool. | The answer string "William." |
