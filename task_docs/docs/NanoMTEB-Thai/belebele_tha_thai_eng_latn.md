# NanoMTEB-Thai / belebele_tha_thai_eng_latn

## Overview

`belebele_tha_thai_eng_latn` is the reverse cross-lingual Belebele retrieval split in the Thai NanoMTEB set. English reading-comprehension questions are used as queries, and Thai passages are the candidate documents. The retriever must bridge English questions to the corresponding Thai translated passage. This makes the task a strong test of English-to-Thai multilingual retrieval.

The Nano split contains 200 queries, 488 documents, and exactly 200 positive relevance judgments. Each query has one positive passage. Queries average about 81 characters, while Thai documents average about 456 characters. The sampled questions ask about French Revolution effects, agriculture societies, subsistence agriculture, violent eras in China, and King Tutankhamun. The relevant documents are Thai passages containing the supporting information.

## Details

### What the Original Data Measures

Belebele is a parallel reading-comprehension benchmark. Its passages and questions are available across many language variants. The retrieval conversion treats each question as a query and the corresponding passage as the relevant document. In this split, the query is English and the document is Thai, so the task measures cross-language passage retrieval rather than same-language reading comprehension.

The positive document is the passage behind the question. It is not necessarily a short answer. The model must identify the full Thai passage that contains the evidence.

### Observed Data Profile

The document side is Thai prose, while the query side is English. Documents are moderate-length passages with general educational content. Queries are full English questions and often contain "according to the passage" wording. There is almost no normal lexical overlap between query and document.

Each query has one positive, so incorrect same-topic passages count as failures. This makes the task a precise test of cross-lingual alignment between English question meaning and Thai passage content.

### BM25 Evaluation Profile

BM25 is weak, with nDCG@10 of 0.0944, hit@10 of 0.1050, and recall@100 of 0.2850. The result reflects the script and language gap. Sparse matching can only use digits, names, or accidental shared strings. English words generally do not appear in Thai passages.

This baseline shows that lexical overlap is not a useful retrieval strategy in this direction. If a model performs close to BM25, it is not solving the cross-lingual task.

### Dense Evaluation Profile

The dense `harrier-oss-270m` run is very strong, with nDCG@10 of 0.8046, hit@10 of 0.8650, and recall@100 of 0.9850. Dense retrieval successfully aligns English questions to Thai passages in a shared embedding space. It captures the semantic relation between the query's requested information and the Thai passage content.

The dense score is slightly lower than the Thai-query to English-passage direction, but still far above BM25. This suggests that the model has strong English-Thai alignment but still faces some difficulty ranking Thai passages for English questions.

### Reranking Hybrid Evaluation Profile

`reranking_hybrid` reports nDCG@10 of 0.2741, hit@10 of 0.3150, and recall@100 of 0.9850. Candidate lists contain 100 to 101 items, and 3 rows use the positive safeguard. Hybrid recall equals dense recall, but top-10 ranking is much lower.

This indicates that hybrid retrieval can preserve the right Thai passage for reranking, but lexical components weaken the final ranking. Dense retrieval should be treated as the main direct-rank baseline.

### Metric Interpretation for Model Researchers

This split is strongly dense-favorable. BM25 is essentially a language-independent token baseline, while dense retrieval performs the real cross-lingual alignment. Hybrid retrieval is useful for top-100 candidate preservation but not for final ranking.

Because each query has one positive, nDCG@10 directly measures how high the correct Thai passage is placed. Recall@100 is relevant for reranking pipelines, but dense top-10 quality is the key direct-search metric.

### Query and Relevance Type Tendencies

Representative questions ask which French Revolution changes affected working-class citizens, who may have started an agricultural society, which statement describes subsistence agriculture, which period was one of China's most violent eras, and when King Tutankhamun gained notoriety. Relevant Thai passages are translations or parallel versions of the supporting passages.

The queries often require understanding a relation within the passage, not just matching a topic. For example, the correct passage must contain the specific historical, agricultural, or biographical context needed for the question.

### Representative Failure Modes

BM25 fails because it cannot bridge English and Thai. Dense retrieval may confuse passages with similar topics, especially among educational history or geography passages. Hybrid retrieval may include the correct passage at top 100 but rank unrelated lexical artifacts higher.

Another failure mode is relying on named entities alone. If several passages mention a known person or place, the model must still identify the exact passage that supports the question.

### Training Data That May Help

Useful training data includes English-to-Thai parallel retrieval pairs, translated QA pairs, multilingual dual-encoder training data, and Thai passages with English questions. Training should avoid the same Belebele evaluation items.

Hard negatives should be Thai passages from the same broad topic or from other Belebele passages that share entity type or theme. These are necessary to learn exact source-passage matching.

### Model Improvement Notes

Dense models can improve through better English-Thai representation alignment and Thai passage encoding. Sparse systems provide little value except for shared proper names and numbers. Hybrid retrieval can be used for candidate preservation, but final ranking should rely on semantic or cross-encoder reranking.

For model research, this split is useful because it isolates cross-script retrieval. Strong performance requires aligning English questions with Thai evidence passages without relying on surface overlap.

## Example Data

### Public Sources

- Belebele paper: https://arxiv.org/abs/2308.16884
- Belebele repository: https://github.com/facebookresearch/belebele
- MTEB task dataset card: https://huggingface.co/datasets/mteb/belebele

### Source Reference Table

| Source | What it contributes |
| --- | --- |
| Belebele paper | Original parallel reading-comprehension benchmark. |
| Belebele repository | Source data and benchmark resources. |
| MTEB task card | Retrieval packaging of Belebele. |

### Representative Snippets

- An English query asks which French Revolution changes affected working-class citizens; the Thai passage describes social and political effects.
- A query asks who may have started an agricultural society; the Thai passage discusses New Zealand settlement theories.
- A query asks which statement describes subsistence agriculture; the Thai passage defines agriculture carried out to meet family needs.
- A query asks which era was one of China's most violent; the Thai passage describes the Warring States period.
- A query asks when King Tutankhamun gained notoriety; the Thai passage discusses his fame in modern times.
