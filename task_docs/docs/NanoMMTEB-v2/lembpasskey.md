# NanoMMTEB-v2 / lembpasskey

## Overview

`NanoMMTEB-v2 / lembpasskey` is a long-context passkey retrieval task from
LongEmbed. Queries ask for the passkey associated with a named person, and each
document is a long filler passage containing the target passkey statement. The
Nano split has 100 queries, 100 documents, and 100 positive qrel rows, with
exactly one positive document per query. Current diagnostics show BM25 as
nearly perfect, while dense and `reranking_hybrid` have full recall but weaker
top-rank ordering. The task isolates whether retrieval systems can preserve a
small entity-bound fact inside very long documents.

## Details

### What the Original Data Measures

LongEmbed introduced long-context retrieval tasks, including passkey and
needle-in-haystack retrieval, to test whether embedding models can process long
inputs. Documents have controlled lengths and contain a small target fact
inserted among large amounts of filler text.

In this task, the model must retrieve the document containing the named
person's passkey. The core challenge is not broad topic matching; it is binding
the requested name to a small fact buried in a long repeated document.

### Observed Data Profile

The Nano split contains 100 queries, 100 documents, and 100 positive qrel rows.
Every query has exactly one positive document. Queries average 37.80
characters, while documents average 28,060.87 characters.

Queries are short English prompts asking for a passkey associated with a named
person. Documents are long haystacks built from repeated filler sentences, with
one or more explicit passkey statements inserted at controlled positions.
Evaluation origins include multiple length buckets from 256 through 32,768.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset contains all 100 documents per query
and achieves nDCG@10 = 0.9963, hit@10 = 1.0000, and recall@100 = 1.0000. BM25
is effectively perfect for top-rank retrieval.

This reflects the explicit lexical cue. The query contains the person's name
and the term passkey, and the positive document repeats the same entity-passkey
association. Term-frequency matching can therefore identify the correct
document despite the long filler.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset contains all 100 documents per
query and achieves nDCG@10 = 0.8463, hit@10 = 0.8500, and recall@100 = 1.0000.
Dense retrieval sees every positive in the full candidate set but ranks some
positives outside the top 10.

This is the central long-context weakness exposed by the task. A dense vector
for a very long document may be dominated by repeated filler and may not retain
the specific name-passkey binding. The model can know that all documents look
similar, but it must identify the one containing the requested entity.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains all 100 documents per query and
achieves nDCG@10 = 0.8525, hit@10 = 0.8700, and recall@100 = 1.0000. Hybrid
retrieval is slightly stronger than dense retrieval but far below BM25 for
top-rank quality.

Because the full corpus is only 100 documents, recall@100 is saturated for all
profiles. The meaningful comparison is nDCG@10 and hit@10. Hybrid evidence does
not recover BM25's exact entity-match advantage, though it modestly improves
over dense retrieval.

### Metric Interpretation for Model Researchers

This task is single-positive and small-corpus. Hit@10 measures whether the one
correct document appears near the top. nDCG@10 is sensitive to its rank, and
recall@100 is not discriminative because every profile covers the full corpus.

The task should be interpreted as a long-context fact-retention test for
embedding retrieval. A model can score well only if it preserves the named
entity and passkey association inside a very long input.

### Query and Relevance Type Tendencies

Queries are short English requests such as asking for the passkey for a named
person. Relevant documents are long filler passages containing a sentence that
states that person's passkey.

The lexical signal is clear, but the target fact is sparse relative to document
length. The task rewards exact entity binding, long-context encoding, and
resistance to filler dilution.

### Representative Failure Modes

Dense retrieval can rank another filler document above the positive because all
documents share nearly identical background text. It may also preserve the word
passkey without preserving which named person it belongs to. Hybrid retrieval
can improve slightly but still under-rank the exact document if the dense signal
dominates.

BM25 failures are rare in this setup because exact name matching is enough for
most queries. If failures occur, they are likely from similar names or repeated
passkey wording across documents.

### Training Data That May Help

Useful training data includes long-context retrieval examples,
needle-in-haystack retrieval, synthetic passkey retrieval with non-overlapping
names, and QA over long documents with varied answer positions. The Nano split's
generated names, passkeys, qrels, and positive documents should be excluded from
training.

Synthetic data can generate long filler documents with entity-bound passkey
facts at controlled positions. Questions should ask for a named entity's fact.
Hard negatives should include nearby names or different passkeys so the model
must bind the requested entity to the correct fact.

### Model Improvement Notes

Dense retrievers should use long-context encoders, chunked or late-interaction
retrieval, entity-aware pooling, or multi-vector representations. Sparse
systems already perform near ceiling because the lexical clue is explicit.
Rerankers should inspect the exact name-passkey sentence rather than global
document similarity.

For hybrid systems, `NanoMMTEB-v2 / lembpasskey` shows that hybrid search does
not automatically fix long-context dilution. The sparse signal is the reliable
anchor, while dense retrieval needs better local fact preservation.

## Example Data

| Query | Positive document |
| --- | --- |
| what is the passkey for Douglas Alfaro? [39 chars] | The grass is green. Douglas Alfaro's pass key is 6699. Remember it. 6699 is the pass key for Douglas Alfaro. The sky is blue. The sun is yellow. Here we go. There and back again. The grass is green. The sky is blue. The sun is yellow. Here we go. There and back again. The grass is green. The sky is blue. The sun is yellow. Here we go. There and back again. The grass is green. The sky is blue. The sun is yellow. Here we go. There and back again. The grass is green. The sky is blue. The sun is yellow. Here we go. There and back again. The grass is green. The sky is blue. The sun is yellow. Here we go. There and back again. The grass is green. The sky is blue. The sun is yellow. Here we go. There and back again. The grass is green. The sky is blue. The sun is yellow. Here we go. There and back again. The grass is green. The sky is blue. The sun is yellow. Here we go. There and back again. The grass is green. The sky is blue. The sun is yellow. Here we go. There and back again. The grass i... [1,000 / 1,786 chars] |
| what is the passkey for Declan Horton? [38 chars] | The grass is green. The sky is blue. The sun is yellow. Here we go. There and back again. The grass is green. The sky is blue. The sun is yellow. Here we go. There and back again. The grass is green. The sky is blue. The sun is yellow. Here we go. There and back again. The grass is green. The sky is blue. The sun is yellow. Here we go. There and back again. The grass is green. The sky is blue. The sun is yellow. Here we go. There and back again. The grass is green. The sky is blue. The sun is yellow. Here we go. There and back again. The grass is green. The sky is blue. The sun is yellow. Here we go. There and back again. The grass is green. The sky is blue. The sun is yellow. Here we go. There and back again. The grass is green. The sky is blue. The sun is yellow. Here we go. There and back again. The grass is green. The sky is blue. The sun is yellow. Here we go. There and back again. The grass is green. The sky is blue. The sun is yellow. Here we go. There and back again. The grass... [1,000 / 58,175 chars] |
| what is the passkey for Denisse Wilcox? [39 chars] | The grass is green. The sky is blue. The sun is yellow. Here we go. There and back again. The grass is green. The sky is blue. The sun is yellow. Here we go. There and back again. The grass is green. The sky is blue. The sun is yellow. Here we go. There and back again. The grass is green. The sky is blue. The sun is yellow. Here we go. There and back again. The grass is green. The sky is blue. The sun is yellow. Here we go. There and back again. The grass is green. The sky is blue. The sun is yellow. Here we go. There and back again. The grass is green. The sky is blue. The sun is yellow. Here we go. Denisse Wilcox's pass key is 18025. Remember it. 18025 is the pass key for Denisse Wilcox. There and back again. The grass is green. The sky is blue. The sun is yellow. Here we go. There and back again. The grass is green. The sky is blue. The sun is yellow. Here we go. There and back again. The grass is green. The sky is blue. The sun is yellow. Here we go. There and back again. The grass... [1,000 / 3,610 chars] |

### Public Sources

- [LongEmbed: Extending Embedding Models for Long Context Retrieval](https://arxiv.org/abs/2404.12096),
  2024.
- [dwzhu/LongEmbed](https://huggingface.co/datasets/dwzhu/LongEmbed).
- [mteb/LEMBPasskeyRetrieval](https://huggingface.co/datasets/mteb/LEMBPasskeyRetrieval).
- [hakari-bench/NanoMMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoMMTEB-v2),
  Nano benchmark dataset.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| LongEmbed: Extending Embedding Models for Long Context Retrieval | 2024 | task paper | [https://arxiv.org/abs/2404.12096](https://arxiv.org/abs/2404.12096) |
| dwzhu/LongEmbed | 2024 | dataset card | [https://huggingface.co/datasets/dwzhu/LongEmbed](https://huggingface.co/datasets/dwzhu/LongEmbed) |
| mteb/LEMBPasskeyRetrieval | 2024 | dataset card | [https://huggingface.co/datasets/mteb/LEMBPasskeyRetrieval](https://huggingface.co/datasets/mteb/LEMBPasskeyRetrieval) |

### Representative Snippets

| Query pattern | Positive document pattern |
| --- | --- |
| A short question asking for Douglas Alfaro's passkey. | A filler document containing Douglas Alfaro's passkey statement. |
| A question asking for Declan Horton's passkey. | A very long repeated filler document containing Declan Horton's passkey. |
| A question asking for Denisse Wilcox's passkey. | A filler document with the matching Denisse Wilcox passkey fact. |
| A question asking for Cheyenne Jarvis's passkey. | A long haystack document containing the Cheyenne Jarvis association. |
| A question asking for Zyaire Sweeney's passkey. | A repeated filler passage with the requested entity-passkey statement. |
