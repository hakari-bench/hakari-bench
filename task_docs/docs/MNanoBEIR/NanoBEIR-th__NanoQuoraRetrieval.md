# MNanoBEIR / NanoBEIR-th / NanoQuoraRetrieval

## Overview

NanoQuoraRetrieval in the Thai NanoBEIR slice is a duplicate-question retrieval task derived from Quora Question Pairs. The queries are Thai translated questions, and the corpus contains Thai translated questions that may ask the same thing in another way. The retrieval goal is to identify duplicate or near-duplicate questions, not answer passages. This makes the task a compact diagnostic for Thai paraphrase retrieval, short-text semantic matching, and the balance between lexical overlap and embedding similarity.

## Details

### What the Original Data Measures

Quora Question Pairs was created to determine whether two user-written questions are duplicates. In retrieval form, each query question must retrieve other questions with the same intent. A relevant pair may be nearly identical, or it may use a different construction, level of specificity, or phrasing while preserving the same information need.

The Thai translated version tests this behavior with short Thai questions. Because both query and candidate are short, there is little surrounding context. The model must compare intent directly and avoid treating same-topic but non-equivalent questions as duplicates. Thai wording and segmentation can make both exact matching and semantic matching more delicate.

### Observed Data Profile

The task contains 50 queries, 5,046 documents, and 70 relevance judgments. The average number of positives is 1.40 per query, with a minimum of 1, a median of 1.0, and a maximum of 6. Ten queries have multiple positives, or 20.0% of the query set. Most queries therefore have one duplicate target, with a small number of paraphrase clusters.

Queries average 46.94 characters, and documents average 53.67 characters. Query and document lengths are very close. This gives the task a clean sentence-level retrieval shape: relevance depends on the meaning of the full question, not on long passage context.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.7267, hit@10 of 0.8200, and recall@100 of 0.9714 using the top-500 BM25 candidate subset. This is a strong lexical profile. Many duplicate questions share key words, entities, or very similar phrasing, so exact overlap is highly informative.

However, BM25 still trails dense retrieval in top-10 quality. Lexical overlap can be misleading when questions share terms but ask different things, and it can miss duplicates that use different Thai wording. The high recall@100 shows that BM25 is a strong candidate generator, but it is not the best final ranker.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.8859, hit@10 of 0.9800, and recall@100 of 1.0000. Dense retrieval is the strongest profile on this task. It captures paraphrase and intent equivalence extremely well in this Thai duplicate-question slice.

The short symmetric question format is favorable for dense retrieval. Both sides are questions, and the semantic unit is compact. Dense similarity can connect equivalent formulations while avoiding some same-word non-duplicates. The remaining errors are likely to involve subtle scope shifts, subjective framing, or broad versus narrow question variants.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.7928, hit@10 of 0.9400, and recall@100 of 1.0000. It uses exactly 100 candidates per query, with no rank-101 safeguard rows. Its recall@100 matches dense retrieval, but dense retrieval remains stronger on nDCG@10 and hit@10.

This suggests that hybrid search preserves complete candidate coverage but does not improve top-rank duplicate ordering. The lexical component can help with exact duplicates, but it can also elevate same-word distractors. For Thai Quora retrieval, dense similarity is the best direct ranking signal, while reranking_hybrid is still a complete candidate source for downstream reranking.

### Metric Interpretation for Model Researchers

Because most queries have one positive, nDCG@10 and hit@10 are direct measures of whether the duplicate question is visible near the top. recall@100 measures candidate completeness for a later reranker. Dense and reranking_hybrid both reach complete recall, so their difference is primarily ordering quality.

The task clearly shows the value of semantic paraphrase modeling. BM25 is already strong because many duplicates share words, but dense retrieval is much better at ranking intent-equivalent questions. Researchers can use this task to test whether a model distinguishes true duplicates from high-overlap non-duplicates.

### Query and Relevance Type Tendencies

Queries include ordinary user questions such as whether it is okay to laugh at one's own jokes, the best lie someone has made up, why Quora recommends answers criticizing Donald Trump, how to become physically strong, and how a quantum satellite works. Relevant documents are duplicate or near-duplicate questions.

The task rewards fine-grained question intent. Two questions may differ slightly in form but preserve the same meaning, while another pair may share many words but change the target, stance, or requested explanation. The short length makes each word and phrase influential.

### Representative Failure Modes

Likely failures include ranking same-topic non-duplicates too high, missing paraphrases with different Thai wording, confusing broad and narrow question variants, and overvaluing repeated names or political terms. BM25 is most vulnerable to high-overlap distractors, while dense retrieval may overgeneralize when two questions are semantically close but not equivalent.

### Training Data That May Help

Useful training data includes Thai paraphrase pairs, duplicate-question retrieval, multilingual question rewrite data, and hard negatives that share words or entities but ask a different question. For rerankers, near-duplicate non-equivalent pairs are especially important because they represent the main ranking ambiguity.

### Model Improvement Notes

A model targeting this task should prioritize sentence-level intent equivalence. Dense retrieval is the strongest baseline and should be refined with hard negatives for scope, stance, and specificity. Sparse systems remain useful for exact duplicate candidates but need paraphrase expansion. Hybrid systems should keep dense ordering dominant unless lexical evidence clearly indicates duplicate status.

## Example Data

### Public Sources

The original data source is Quora Question Pairs, with BEIR providing the retrieval benchmark framing and NanoBEIR providing the compact multilingual dataset packaging.

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original dataset | [Quora Question Pairs](https://kaggle.com/competitions/quora-question-pairs) |
| Retrieval benchmark framing | [BEIR](https://arxiv.org/abs/2104.08663) |
| Multilingual benchmark context | [MMTEB](https://arxiv.org/abs/2502.13595) |
| NanoBEIR collection | [NanoBEIR on Hugging Face](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
| NanoBEIR-th dataset | [hakari-bench/NanoBEIR-th](https://huggingface.co/datasets/hakari-bench/NanoBEIR-th) |

Representative query and positive question snippets:

| Query | Positive question |
| --- | --- |
| มันโอเคไหมที่จะหัวเราะกับมุกของตัวเอง? | มันแปลกไหมที่หัวเราะกับมุกของตัวเอง? |
| คำโกหกที่ดีที่สุดที่คุณเคยแต่งขึ้นคืออะไร? | คำโกหกที่คุณเคยพูดออกมาดีที่สุดคืออะไร? |
| ทำไม Quora ถึงแนะนำคำตอบที่ดูถูกโดนัลด์ ทรัมป์บ่อยๆ ในฟีดของฉัน? | ทำไม Quora ถึงดูเหมือนว่าจะมีคำตอบที่มีอคติและเป็นอัตวิสัยเกี่ยวกับคำถามเกี่ยวกับโดนัลด์ ทรัมป์เท่านั้น? |
| ฉันจะทำให้ตัวเองแข็งแรงทางกายได้อย่างไร? | ฉันจะทำให้ตัวเองแข็งแรงทางกายได้อย่างไร? |
| ดาวเทียมควอนตัมจะทำงานอย่างไร? | ดาวเทียมควอนตัมทำงานอย่างไรและการใช้งานหลักบางอย่างจะเป็นอะไรบ้าง? |
