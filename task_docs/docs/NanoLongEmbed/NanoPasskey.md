# NanoLongEmbed / NanoPasskey

## Overview

`NanoLongEmbed / NanoPasskey` is LongEmbed's synthetic personalized passkey
retrieval task. Queries ask for the passkey associated with a named person, and
documents are long filler contexts containing a single explicit name-key
statement. The model must retrieve the document that contains the requested
association. The Nano split has 100 queries, 800 documents, and one positive
document per query. Documents average 28,956.68 characters and are dominated by
repetitive filler text. Current diagnostics show all profiles reaching perfect
hit@10 and recall@100, while BM25 ranks positives highest by nDCG@10, followed
by `reranking_hybrid`, then dense retrieval.

## Details

### What the Original Data Measures

LongEmbed describes Personalized Passkey Retrieval as a synthetic diagnostic for
long-context embedding models. A short query names a person or entity, and the
positive document contains a sentence linking that name to a passkey. The rest
of the document is long repetitive filler. The task tests whether the model can
retain a small key-value fact inside a long context.

There is no separate standalone task paper confirmed for `NanoPasskey`; the
source benchmark is LongEmbed and its dataset card. The task should be
interpreted as a controlled long-context retention test, not as a naturally
occurring retrieval dataset.

### Observed Data Profile

The Nano split contains 100 queries, 800 documents, and 100 positive qrel rows.
Every query has one positive, with no multi-positive queries. Queries average
37.80 characters, while documents average 28,956.68 characters.

Observed documents repeat simple filler sentences such as "The grass is green",
"The sky is blue", and "The sun is yellow" around a single sentence such as a
person's passkey statement. Queries are short and formulaic, for example asking
for the passkey of Ronan Day, Flora Wu, Summer Walton, Cassidy Wolf, or Archer
Peralta.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset contains 500 candidates per query
and achieves nDCG@10 = 0.7717, hit@10 = 1.0000, and recall@100 = 1.0000. BM25
finds every positive in the top ten and the top 100. It is the strongest
observed profile by nDCG@10 because the person name is a rare exact lexical
anchor.

The task still has nontrivial ordering. Perfect hit@10 does not mean every
positive is rank 1. Repetitive filler and similar passkey sentence templates
make many documents look structurally identical except for the name and key.
BM25 succeeds by keying on the exact requested name.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset contains 500 candidates per
query and also achieves hit@10 = 1.0000 and recall@100 = 1.0000, but its
nDCG@10 is lower at 0.6473. Dense retrieval always keeps the positive near the
top, but it ranks it less sharply than BM25.

This is expected for a synthetic key-value task. Semantic similarity between
filler-heavy documents is nearly identical, and the decisive evidence is an
exact name-key association. If a dense representation does not preserve the
specific name strongly enough, it can rank another filler document above the
positive even though it still retrieves the positive within the first ten.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains exactly 100 candidates per
query, with no safeguard rows. It achieves nDCG@10 = 0.7294, hit@10 = 1.0000,
and recall@100 = 1.0000. Hybrid retrieval ranks positives better than dense but
below BM25.

The hybrid profile shows that lexical evidence is the main driver, while dense
evidence is not harmful for coverage. Since all profiles already retrieve the
positive in the top ten, the relevant distinction is how high the exact
name-key document is placed. A reranker should focus on verifying the requested
name association.

### Metric Interpretation for Model Researchers

This is a single-positive synthetic task. Hit@10 and recall@100 are saturated
for all three profiles, so nDCG@10 carries most of the diagnostic value. It
measures whether the positive document is ranked close to the top rather than
merely included somewhere in the first ten.

The result shows that this passkey retrieval setting is more about exact
association retention than semantic matching. BM25 is strongest because the
person name is the decisive signal. Dense retrieval's lower nDCG indicates that
long-context embeddings can find the right area but may blur exact identity.

### Query and Relevance Type Tendencies

Queries are short questions of the form "what is the passkey for [person]?"
Relevant documents contain the matching sentence linking that person to a
numeric passkey. The rest of the document is repetitive distractor text.

The task rewards exact entity matching, key-value retention, and position
robustness. It does not test broad topical retrieval or complex reasoning.

### Representative Failure Modes

BM25 can rank imperfectly when repeated filler and similar templates dominate
document scoring, but it generally benefits from the rare name. Dense retrieval
can fail to rank the positive first when the long filler context overwhelms the
specific name-key association. Hybrid retrieval can inherit dense ambiguity
while still benefiting from lexical exactness.

A model that truncates or underweights the section containing the passkey may
also fail if the association is placed far from the beginning.

### Training Data That May Help

Useful training data includes synthetic key-value retrieval over long contexts,
named-entity attribute lookup pairs, long-context QA over inserted facts, and
position-robust retrieval examples. Data should vary names, identifier formats,
filler text, context length, and insertion position.

Comparable evaluation should exclude Nano evaluation names, passkeys, qrels,
and positive documents.

### Model Improvement Notes

Dense retrievers can improve with architectures or training objectives that
preserve exact entity-token identity and local key-value facts across long
contexts. Sparse retrieval already performs strongly because exact names matter.
Rerankers should explicitly check whether the candidate contains the requested
person and associated passkey.

For hybrid systems, `NanoPasskey` is mostly a calibration and ranking test:
coverage is easy, but exact top-rank ordering depends on retaining the precise
name-key pair.

## Example Data

| Query | Positive document |
| --- | --- |
| what is the passkey for Ronan Day? [34 chars] | The grass is green. The sky is blue. The sun is yellow. Here we go. There and back again. The grass is green. The sky is blue. The sun is yellow. Here we go. There and back again. The grass is green.... [200 / 1,778 chars] |
| what is the passkey for Flora Wu? [33 chars] | The grass is green. The sky is blue. The sun is yellow. Here we go. There and back again. The grass is green. The sky is blue. The sun is yellow. Here we go. There and back again. The grass is green.... [200 / 3,598 chars] |
| what is the passkey for Summer Walton? [38 chars] | The grass is green. The sky is blue. The sun is yellow. Here we go. There and back again. The grass is green. The sky is blue. The sun is yellow. Here we go. There and back again. The grass is green.... [200 / 3,608 chars] |
| what is the passkey for Cassidy Wolf? [37 chars] | The grass is green. The sky is blue. The sun is yellow. Here we go. There and back again. The grass is green. The sky is blue. The sun is yellow. Here we go. There and back again. The grass is green.... [200 / 1,784 chars] |
| what is the passkey for Archer Peralta? [39 chars] | The grass is green. The sky is blue. The sun is yellow. Here we go. There and back again. The grass is green. The sky is blue. The sun is yellow. Here we go. There and back again. The grass is green.... [200 / 878 chars] |

### Public Sources

- [LongEmbed: Extending Embedding Models for Long Context Retrieval](https://arxiv.org/abs/2404.12096),
  2024.
- [dwzhu/LongEmbed](https://huggingface.co/datasets/dwzhu/LongEmbed), source
  dataset card.
- [hakari-bench/NanoLongEmbed](https://huggingface.co/datasets/hakari-bench/NanoLongEmbed),
  Nano benchmark dataset.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| LongEmbed: Extending Embedding Models for Long Context Retrieval | 2024 | arXiv paper | [https://arxiv.org/abs/2404.12096](https://arxiv.org/abs/2404.12096) |
| dwzhu/LongEmbed | 2024 | dataset card | [https://huggingface.co/datasets/dwzhu/LongEmbed](https://huggingface.co/datasets/dwzhu/LongEmbed) |

### Representative Snippets

| Query pattern | Positive document pattern |
| --- | --- |
| A short question asking for Ronan Day's passkey. | A long repeated filler document containing the sentence with Ronan Day's passkey. |
| A question asking for Flora Wu's passkey. | A filler-heavy document with one explicit Flora Wu name-key statement. |
| A question asking for Summer Walton's passkey. | A long context where the only decisive evidence is Summer Walton's key sentence. |
| A question asking for Cassidy Wolf's passkey. | A repeated sentence context containing Cassidy Wolf's passkey association. |
| A question asking for Archer Peralta's passkey. | A long synthetic document containing the requested passkey statement. |
