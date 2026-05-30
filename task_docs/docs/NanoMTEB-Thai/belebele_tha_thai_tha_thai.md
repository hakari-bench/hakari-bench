# NanoMTEB-Thai / belebele_tha_thai_tha_thai

## Overview

`belebele_tha_thai_tha_thai` is the same-language Thai Belebele retrieval split. Thai reading-comprehension questions are used as queries, and Thai passages are the candidate documents. This isolates Thai passage retrieval from the cross-lingual alignment difficulty seen in the other Belebele Thai directions. The task asks whether a retriever can find the source passage that supports a Thai question.

The Nano split contains 200 queries, 488 documents, and exactly 200 positive relevance judgments. Each query has one positive passage. Queries average about 58 characters, while documents average about 456 characters. The examples cover historical, agricultural, and biographical passages, including the French Revolution, New Zealand settlement, subsistence agriculture, violent eras in China, and King Tutankhamun. Because query and document are both Thai, lexical and semantic signals can both work well.

## Details

### What the Original Data Measures

Belebele is a parallel multiple-choice reading-comprehension benchmark based on short FLORES-200 passages. The retrieval version treats a question as the query and the corresponding passage as the relevant document. In this split, both sides are Thai, so the task measures same-language Thai question-to-passage retrieval.

The positive document is the full passage behind the question. The model is not selecting a multiple-choice option; it is retrieving the passage that contains the evidence needed to answer the question.

### Observed Data Profile

The corpus is small and contains short educational passages. The query wording often overlaps with the relevant passage because both are in Thai and both derive from the same reading-comprehension item. At the same time, some questions refer to the passage indirectly or ask about an implication, so exact overlap is not the whole task.

Every query has one positive. This makes ranking simple to interpret: the correct source passage should appear near the top, and same-topic passages are not substitutes.

### BM25 Evaluation Profile

BM25 is very strong, with nDCG@10 of 0.9297, hit@10 of 0.9850, and recall@100 of 0.9950. Same-language Thai lexical overlap is highly effective. The question and passage often share content words or phrases, and the corpus has only 488 documents.

The strong BM25 result contrasts sharply with the cross-lingual Belebele Thai splits. It shows that when the script and language match, term occurrence is a powerful signal for this dataset. Remaining errors likely involve paraphrased questions, generic terms, or passages with overlapping topical vocabulary.

### Dense Evaluation Profile

The dense `harrier-oss-270m` run is also very strong, with nDCG@10 of 0.9287, hit@10 of 0.9650, and recall@100 of 0.9800. Dense retrieval is nearly tied with BM25 in nDCG, though slightly lower in hit and recall. It captures passage-level semantic similarity but does not outperform the strong lexical baseline by itself.

This profile indicates that the same-language task is easy for both lexical and dense retrieval. The main distinction is not whether the model understands Thai at all, but whether it can preserve exact passage identity in a small corpus.

### Reranking Hybrid Evaluation Profile

`reranking_hybrid` is strongest in nDCG@10, with 0.9615, hit@10 of 0.9800, and recall@100 of 0.9950. Candidate lists contain 100 to 101 items, and 1 row uses the positive safeguard. Hybrid retrieval combines the exact-word strength of BM25 with dense semantic alignment, producing the best top-rank ordering.

This is a clear case where hybrid search improves a same-language task. Unlike the cross-lingual directions, lexical candidates are valuable rather than noisy. Dense matching helps refine the top order when surface overlap is not enough.

### Metric Interpretation for Model Researchers

This split is hybrid-favorable, with BM25 and dense both near ceiling. It is useful as a control condition for the Belebele Thai group: same-language Thai retrieval is easy compared with Thai-English or English-Thai retrieval. If a model struggles here, the issue is likely Thai tokenization, passage encoding, or basic retrieval quality rather than cross-lingual alignment.

Because each query has one positive, nDCG@10 measures how high the correct passage is placed. The high recall values mean there is limited headroom, so small top-rank ordering differences matter most.

### Query and Relevance Type Tendencies

Representative queries ask which French Revolution changes affected working-class citizens, who may have started an agricultural society, which statement describes subsistence agriculture, which period was one of China's most violent eras, and when King Tutankhamun gained notoriety. The relevant Thai passages contain the supporting text.

Questions may ask for passage-level inference or detail. A retriever must find the source passage, not merely a passage from the same broad educational topic.

### Representative Failure Modes

BM25 can fail when the question paraphrases the passage or uses generic words shared by many passages. Dense retrieval can retrieve semantically similar passages from the same broad topic but not the exact source passage. Hybrid retrieval reduces these risks but may still confuse passages with overlapping educational themes.

Another failure mode is over-reliance on repeated phrases such as "according to the passage." These phrases do not identify the relevant passage; content-bearing words and semantic topic must drive retrieval.

### Training Data That May Help

Useful training data includes Thai question-to-passage retrieval pairs, Thai reading-comprehension data converted to retrieval, same-language Belebele-style pairs, and Thai hard negatives from nearby short passages. Training should avoid using the same evaluation items.

Hard negatives should be Thai passages with similar broad topics but different evidence. This helps distinguish exact source-passage matching from topical matching.

### Model Improvement Notes

Sparse systems can perform very well if Thai tokenization and term matching are handled well. Dense models should focus on preserving passage identity and handling paraphrases. Hybrid systems are especially suitable here because both lexical and semantic signals are reliable in the same-language setting.

For evaluation, this split provides a same-language benchmark to compare against the cross-lingual Belebele Thai directions. The contrast helps identify whether a model's failures come from Thai retrieval itself or from multilingual alignment.

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

- A Thai query asks which French Revolution change affected working-class citizens; the Thai passage discusses social and political effects.
- A query asks who may have started an agricultural society; the passage discusses New Zealand settlement and Maori theories.
- A query asks which statement describes subsistence agriculture; the passage defines agriculture for family food needs.
- A query asks which era was one of China's most violent; the passage describes unstable periods between dynasties.
- A query asks when King Tutankhamun gained notoriety; the passage discusses his modern fame and ancient importance.
