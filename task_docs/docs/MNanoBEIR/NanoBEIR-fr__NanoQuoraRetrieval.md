# MNanoBEIR / NanoBEIR-fr / NanoQuoraRetrieval

## Overview

This task is the French NanoBEIR version of Quora Question Pairs, a duplicate-question retrieval benchmark. The original Quora Question Pairs dataset was released for identifying whether two user questions have the same intent, and BEIR frames it as a retrieval task where each query should retrieve semantically duplicate questions. In this NanoBEIR slice, French translated questions are matched against 5,046 French translated candidate questions. The task contains 50 queries and 70 positive relevance judgments, with an average of 1.40 positives per query. It is a compact diagnostic for paraphrase retrieval, question intent matching, and separating true duplicates from same-topic questions with different information needs.

## Details

### What the Original Data Measures

Quora duplicate-question retrieval measures semantic equivalence between short user questions. A relevant document is another question that asks essentially the same thing as the query. This is not evidence retrieval and not broad topic retrieval. The task rewards intent preservation across spelling, word order, synonymy, added context, and compressed phrasing, while penalizing questions that are merely on the same subject.

### Observed Data Profile

The French Nano task has 50 queries, 5,046 documents, and 70 positives. Ten queries have multiple positives, and the maximum positives per query is six. Queries average about 61 characters, and candidate questions average about 72 characters. Examples include laughing at one's own jokes, the biggest lie someone has told, Quora suggestions about Donald Trump, physical fitness, and quantum satellites. Both query and document sides are short questions.

### BM25 Evaluation Profile

BM25 is strong, with nDCG@10 of 0.766, Hit@10 of 0.920, and Recall@100 of 0.986. Duplicate questions often reuse the same words or templates, so sparse matching gives excellent broad coverage. Exact or near-exact duplicates are easy for BM25. Its main limitation is paraphrase: a true duplicate can preserve intent with different wording, and a lexical near-match can still ask a different question.

### Dense Evaluation Profile

The dense harrier-oss-270m baseline is strongest by top ranking, with nDCG@10 of 0.859, Hit@10 of 0.980, and Recall@100 of 0.971. This shows that embedding similarity is particularly effective for duplicate-question retrieval. Dense retrieval can identify intent equivalence beyond token overlap and rank paraphrases above topical neighbors. Its recall is slightly below BM25 and hybrid, but its first-page ordering is best.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid profile reaches nDCG@10 of 0.838, Hit@10 of 0.940, and Recall@100 of 0.986. It matches BM25's excellent Recall@100 while improving ranking substantially over BM25, but it does not beat dense retrieval on nDCG@10 or Hit@10. This pattern suggests that hybrid search is a reliable candidate generator, while dense similarity is the strongest direct duplicate-intent ranker for this French sample.

### Metric Interpretation for Model Researchers

Hit@10 is high for all methods, so nDCG@10 and Recall@100 are more discriminative. nDCG@10 measures whether the true duplicate appears at the top. Recall@100 measures whether all duplicate candidates are available for reranking, especially for multi-positive queries. A good model should rank same-intent questions above questions that merely share the same topic or named entity.

### Query and Relevance Type Tendencies

Queries are short French user questions. Positives are duplicate questions that preserve the same user intent. Some are almost identical, while others vary wording, perspective, or specificity. Hard negatives can ask about the same topic but require a different answer. The task is sensitive to paraphrase, semantic textual similarity, and intent granularity.

### Representative Failure Modes

BM25 can miss paraphrases with little lexical overlap. Dense retrieval can over-rank related but non-duplicate questions. Hybrid retrieval improves coverage but may still inherit lexical near-match errors. Failure analysis should compare the implied answer or action requested by each question, not only shared terms.

### Training and Leakage Considerations

Training should exclude Quora Question Pairs, BEIR, NanoBEIR, and translated duplicate-question records likely to overlap with this evaluation slice. Useful non-overlapping data includes duplicate-question pairs, French and multilingual paraphrase datasets, semantic textual similarity data, and hard-negative question retrieval examples. Multi-positive training is useful because some queries have several duplicates.

### Model Improvement Signals

Strong models should preserve near-duplicate recognition while improving paraphrase robustness. Useful signals include same-topic hard negatives, intent-preserving rewrites, lexical substitutions, and multilingual duplicate-question supervision. Hybrid systems should use sparse retrieval for exact duplicates and dense retrieval for paraphrase ordering.

## Example Data

| Query | Positive Document |
|---|---|
| Est-ce que c'est permis de rire de ses propres blagues ? | Est-ce que c'est bizarre de rire de mes propres blagues ? |
| Quel est le plus gros mensonge que tu aies jamais raconté ? | Quel est le plus beau mensonge que vous ayez jamais raconté ? |
| Pourquoi Quora suggère-t-il fréquemment des réponses dans mon fil d'actualité qui critiquent Donald Trump ? | Pourquoi Quora ne propose-t-il que des réponses partisanes aux questions sur Donald Trump ? |
| Comment renforcer ma condition physique ? | Comment puis-je améliorer ma condition physique ? |
| Comment fonctionne un satellite quantique ? | Comment fonctionne un satellite quantique et quelles seraient ses principales utilisations ? |

## Public Sources

- [Quora Question Pairs](https://kaggle.com/competitions/quora-question-pairs)
- [BEIR benchmark](https://github.com/beir-cellar/beir)
- [MMTEB benchmark](https://arxiv.org/abs/2502.13595)
- [NanoBEIR dataset](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

## Source Reference Table

| Label | URL |
|---|---|
| Quora Question Pairs | https://kaggle.com/competitions/quora-question-pairs |
| BEIR benchmark | https://github.com/beir-cellar/beir |
| MMTEB benchmark | https://arxiv.org/abs/2502.13595 |
| NanoBEIR dataset | https://huggingface.co/collections/zeta-alpha-ai/nanobeir |
