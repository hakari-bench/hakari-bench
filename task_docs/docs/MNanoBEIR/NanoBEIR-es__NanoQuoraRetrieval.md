# MNanoBEIR / NanoBEIR-es / NanoQuoraRetrieval

## Overview

This task is the Spanish NanoBEIR version of Quora Question Pairs, a duplicate-question retrieval benchmark. The original Quora Question Pairs dataset was released for identifying whether two user questions have the same intent, and BEIR frames it as a retrieval task where each query must retrieve semantically duplicate questions. In this NanoBEIR slice, Spanish translated questions are matched against 5,046 Spanish translated candidate questions. The task contains 50 queries and 70 positive relevance judgments, with an average of 1.40 positives per query. It is a compact diagnostic for paraphrase retrieval, intent matching, and the distinction between true duplicate questions and merely topically related questions.

## Details

### What the Original Data Measures

Quora duplicate-question retrieval measures semantic equivalence between short user questions. Relevance is not based on answer evidence or topic alone; the retrieved question should ask essentially the same thing as the query. Some duplicates share many tokens, while others preserve intent through different wording, word order, or specificity. Hard negatives often mention the same topic but ask a different question.

### Observed Data Profile

The Spanish Nano task has 50 queries, 5,046 documents, and 70 positives. Ten queries have multiple positives, and the maximum positives per query is six. Queries average about 55 characters and candidate questions average about 64 characters. Examples include laughing at one's own jokes, the best lie someone has told, Quora suggestions about Donald Trump, physical strengthening, and how a quantum satellite works. The query and document sides are both short questions.

### BM25 Evaluation Profile

BM25 is very strong, with nDCG@10 of 0.791, Hit@10 of 0.960, and Recall@100 of 0.971. Duplicate questions frequently reuse the same words, named entities, or question templates, so sparse matching gives excellent coverage. It works especially well for near-identical duplicates and small lexical variations. The remaining challenge is semantic paraphrase: questions can have the same intent despite different vocabulary.

### Dense Evaluation Profile

The dense harrier-oss-270m baseline gives the best nDCG@10, reaching 0.866 with Hit@10 of 0.940 and Recall@100 of 0.957. Dense retrieval is well suited to duplicate intent because it can recognize paraphrase beyond token overlap. It slightly trails BM25 on recall but ranks positives more effectively near the top. This makes dense retrieval the strongest direct ranker for this Spanish Quora slice.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid profile reaches nDCG@10 of 0.842, Hit@10 of 0.960, and Recall@100 of 1.000. It gives complete top-100 coverage and matches BM25 Hit@10, while dense retrieval still has the highest nDCG@10. This pattern is useful: hybrid search is the best candidate generator, and dense similarity is the clearest top-rank duplicate-intent signal. For reranking pipelines, the hybrid pool is attractive because it preserves all positives in this sample.

### Metric Interpretation for Model Researchers

Hit@10 is high across all methods, so nDCG@10 and Recall@100 are more useful. nDCG@10 measures whether the duplicate appears at the top, while Recall@100 measures whether alternate duplicates are available for reranking. Because positives are few, ranking mistakes are easy to inspect manually. A strong model should rank true duplicates above same-topic non-duplicates.

### Query and Relevance Type Tendencies

Queries are short Spanish user questions. Positives are duplicate questions that preserve the same intent. Differences may include synonyms, word order, spelling, added context, or compression. Same-topic hard negatives are common in this task family, so models must distinguish "same subject" from "same question".

### Representative Failure Modes

BM25 can miss paraphrases with little lexical overlap. Dense retrieval can over-rank a question that is semantically close but asks for a different answer. Hybrid retrieval improves coverage but may still rank a lexical near-match above the true duplicate if intent differs. Failure analysis should compare the implied answer or action requested by each question.

### Training and Leakage Considerations

Training should exclude Quora Question Pairs, BEIR, NanoBEIR, and translated duplicate-question records likely to overlap with this evaluation slice. Useful non-overlapping data includes duplicate-question pairs, Spanish and multilingual paraphrase datasets, semantic textual similarity data, and hard-negative question retrieval examples. Multi-positive training is useful because some queries have several valid duplicates.

### Model Improvement Signals

Strong models should preserve exact duplicate detection while improving paraphrase robustness. Useful signals include same-topic hard negatives, lexical substitution pairs, compressed variants, and intent-preserving rewrites. Hybrid systems should use sparse retrieval for near-duplicates and dense retrieval for broader paraphrase matching.

## Example Data

| Query | Positive document |
| --- | --- |
| ¿Está bien reírse de tus propios chistes? [41 chars] | ¿Es raro reírse de mis propios chistes? [39 chars] |
| ¿Cuál es la mejor mentira que has contado? [42 chars] | ¿Cuál es la mentira más ingeniosa que hayas contado? [52 chars] |
| ¿Por qué Quora me sugiere con frecuencia respuestas en mi timeline que critican a Donald Trump? [95 chars] | ¿Por qué parece que en Quora solo hay respuestas subjetivas y parciales sobre Donald Trump? [91 chars] |

## Public Sources

- [Quora Question Pairs](https://kaggle.com/competitions/quora-question-pairs)
- [BEIR benchmark](https://github.com/beir-cellar/beir)
- [MMTEB benchmark](https://arxiv.org/abs/2502.13595)
- [NanoBEIR dataset](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

## Source Reference Table

| Label | URL |
|---|---|
| Quora Question Pairs (https://kaggle.com/competitions/quora-question-pairs) |
| BEIR benchmark (https://github.com/beir-cellar/beir) |
| MMTEB benchmark (https://arxiv.org/abs/2502.13595) |
| NanoBEIR dataset (https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
