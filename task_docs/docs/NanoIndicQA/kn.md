# NanoIndicQA / kn

## Overview

`NanoIndicQA / kn` is the Kannada split of IndicQA retrieval. The queries are Kannada reading-comprehension questions, and the documents are Kannada evidence paragraphs.

This task evaluates Kannada context retrieval in a small paragraph corpus. The target is the full supporting paragraph, so models must rank the passage that contains the answer evidence rather than generate or match only the answer string.

## Details

### What the Original Data Measures

IndicQA is a manually curated cloze-style reading-comprehension task introduced with IndicXTREME in "Towards Leaving No Indic Language Behind". The retrieval conversion asks models to retrieve the source context paragraph for each question.

In the Kannada split, the benchmark measures whether a retriever can map Kannada questions to Kannada paragraphs covering history, geography, cities, culture, and public institutions.

### Observed Data Profile

This Nano split contains 200 queries, 257 documents, and 200 positive qrels. Each query has exactly one positive. Queries average 53.27 characters, and documents average 882.74 characters.

Observed examples ask about Muslim-majority regions, the meaning of "Chennai", vintage cars in Jaipur, the river region where the British East India Company was established, and the best time to visit Aligarh. Several questions may target related geography or history contexts.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.4730, hit@10 of 0.6000, and recall@100 of 0.8250. The candidate pool contains the full 257-document corpus. BM25 is useful when the Kannada question repeats a distinctive place name, institution, or entity from the context.

The lower hit rate shows that lexical overlap alone is fragile. Short questions may not repeat enough of the context, and multiple history or geography paragraphs can share names and topic words.

### Dense Evaluation Profile

The dense harrier-oss-270m profile reaches nDCG@10 of 0.7037, hit@10 of 0.8500, and recall@100 of 0.9800. Dense retrieval is clearly strongest across the main metrics.

This indicates that semantic question-context matching is important for Kannada IndicQA. Dense retrieval can connect a question to the paragraph even when the exact evidence sentence is phrased differently.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate subset reaches nDCG@10 of 0.6111, hit@10 of 0.7450, and recall@100 of 0.9700. It uses 100 candidates per query, with six rank-101 safeguard positives.

Hybrid retrieval has high recall but does not match dense retrieval's top-10 ranking. It is a useful candidate pool for reranking, while dense retrieval is the best direct first-stage ranker for this split.

### Metric Interpretation for Model Researchers

`NanoIndicQA / kn` is a dense-favored Kannada context retrieval task. The gap between BM25 and dense retrieval is large, so this split is useful for detecting whether a model has robust Kannada semantic representations.

Since each query has one positive, nDCG@10 and hit@10 directly measure correct-context ranking. Recall@100 is useful for diagnosing candidate generation, especially for reranking pipelines.

### Query and Relevance Type Tendencies

Queries are Kannada factual or cloze-style questions. Documents are paragraph-length contexts from encyclopedic or educational sources.

The relevance relation is evidence support: the positive paragraph must contain the information needed to answer the question.

### Representative Failure Modes

BM25 may retrieve a paragraph that repeats a place or institution name but lacks the requested detail. Dense retrieval may still confuse semantically similar city, history, or geography paragraphs. Hybrid retrieval reduces candidate misses but requires reranking for exact evidence selection.

Because the corpus is small, recall can be high while top-10 ordering remains difficult.

### Training Data That May Help

Useful training data includes Kannada QA, Kannada Wikipedia passage retrieval, Indic multilingual retrieval training, and topic-neighbor negatives from related history, geography, city, or cultural paragraphs.

Training should exclude this split's questions and positive context paragraphs.

### Model Improvement Notes

Improving this task requires Kannada semantic coverage and paragraph-level evidence ranking. Models should preserve names, dates, locations, and factual relations while handling question paraphrases.

For reranking, the model should determine whether the paragraph actually contains the answer evidence, not only whether it shares topical vocabulary.

## Example Data

| Query | Positive document |
| --- | --- |
| ಮುಸ್ಲಿಂ-ಬಹುಸಂಖ್ಯಾತ ಪ್ರದೇಶ ಯಾವುದು? [33 chars] | 1947ರಲ್ಲಿ, ಕಾಶ್ಮೀರದ ಜನಸಂಖ್ಯೆಯ "ಶೇಕಡಾ 77ರಷ್ಟು ಭಾಗವು ಮುಸ್ಲಿಮರಿಂದ ಕೂಡಿತ್ತು ಮತ್ತು ತನ್ನೊಂದು ಗಡಿಯನ್ನು ಅದು ಪಾಕಿಸ್ತಾನದೊಂದಿಗೆ ಹಂಚಿಕೊಂಡಿತ್ತು. ಆದ್ದರಿಂದ, ಬ್ರಿಟಿಷ್‌ ಸಾರ್ವಭೌಮತೆಯು ಆಗಸ್ಟ್‌ನ 14-15ರಂದು ಕೊನೆಗೊಂಡಾಗ, ಮಹಾರಾಜನು ಪಾಕಿಸ್ತಾನವನ್ನು ಅಂಗೀಕರಿಸಬಹುದು ಅಥವಾ ಪಾಕಿಸ್ತಾನಕ್ಕೆ ಸೇರಿಕೊಳ್ಳಬಹುದು ಎಂದು ನಿರೀಕ್ಷಿಸಲಾಗಿತ್ತು. ಈ ರೀತಿ ಮಾಡಲು ಆತ ಹಿಂದುಮುಂದು ನೋಡಿದಾಗ, ತನ್ನ ಆಡಳಿತಗಾರನನ್ನು ಬೆದರಿಸಿ ಇದಕ್ಕೆ ಒಪ್ಪಿಸುವ ಅಥವಾ ಶರಣಾಗತನನ್ನಾಗಿಸುವ ಅಸ್ತ್ರವಾಗಿ ಪಾಕಿಸ್ತಾನವು ಗೆರಿಲ್ಲಾ ದಾಳಿಯನ್ನು ಪ್ರಾರಂಭಿಸಿತು. ಇದರ ಬದಲಿಗೆ ಮೌಂಟ್‌ಬ್ಯಾಟನ್‌ರನ್ನು ಭೇಟಿಮಾಡಿದ ಮಹಾರಾಜ ಸಹಾಯಕ್ಕಾಗಿ ಮನವಿ ಸಲ್ಲಿಸಿದ ಮತ್ತು ಆಡಳಿತಗಾರನು ಭಾರತಕ್ಕೆ ಸೇರಿಕೊಳ್ಳಬೇಕು ಎಂಬ ಷರತ್ತಿನ ಮೇಲೆ ಸದರಿ ಗೌರ್ನರ‍್-ಜನರಲ್‌ ಒಪ್ಪಿಗೆ ನೀಡಿದರು. " ಸೇರ್ಪಡೆಯ ದಸ್ತಾವೇಜು ಒಪ್ಪಂದಕ್ಕೆ ಮಹಾರಾಜನು ಸಹಿ ಹಾಕುತ್ತಿದ್ದಂತೆ, "ಭಾರತೀಯ ಯೋಧರು ಕಾಶ್ಮೀರವನ್ನು ಪ್ರವೇಶಿಸಿದ್ದೇ ಅಲ್ಲದೇ, ರಾಜ್ಯದ ಸಾಕಷ್ಟು ಭಾಗಗಳಿಂದ ಪಾಕಿಸ್ತಾನಿ-ಪ್ರಾಯೋಜಿತ ಅನಿಯತ ಸೈನಿಕರು ಅಥವಾ ದಂಗೆಕೋರರನ್ನು ಓಡಿಸಿದರು. ಈ ಜಗಳದ ಮಧ್ಯಸ್ಥಿಕೆಯನ್ನು ವಹಿಸಲು ಆಗ ವಿಶ್ವಸಂಸ್ಥೆಯನ್ನು ಆಹ್ವಾನಿಸಲಾಯಿತು. ಕಾಶ್ಮೀರಿಗಳ ಅಭಿಪ್ರಾಯವನ್ನು ಪರಿಗಣಿಸಬೇಕು ಎಂದು UN ನಿಯೋಗವು ಒತ್ತಾಯಿಸಿದರೆ, ರಾಜ್ಯದ ಎಲ್ಲಾ ಭಾಗಗಳಿಂದ ಅನಿಯತ ಸೈನಿಕರು ಅಥವಾ ದಂಗೆಕೋರರನ್ನು... [1,000 / 1,598 chars] |
| ಚೆನ್ನೈ ಪದದ ಅರ್ಥವೇನು? [20 chars] | 'ಮದ್ರಾಸು' ಎಂಬ ಹೆಸರು 'ಮದ್ರಾಸುಪಟ್ನಂ' ಪದದಿಂದ ಬಂದಿದೆ, ಈ ಜಾಗವನ್ನು ಬ್ರಿಟೀಷ್ ಈಸ್ಟ್ ಇಂಡಿಯಾ ಕಂಪನಿ ಖಾಯಂ ನೆಲೆಗಾಗಿ 1639 ರಲ್ಲಿ ಆಯ್ಕೆ ಮಾಡಿಕೊಂಡಿತು. https://www. mapsofindia. com/on-this-day/22nd-august-1639-madras-now-chennai-is-founded-by-the-east-india-company ಮದ್ರಾಸು ನಗರದ ದಕ್ಷಿಣ ಭಾಗದಲ್ಲಿ 'ಚೆನ್ನಪಟ್ಟಣಂ' ಎಂಬ ಚಿಕ್ಕ ಪೇಟೆಯಿದೆ. ಕಾಲಾಂತರದಲ್ಲಿ ಎರಡೂ ಪಟ್ಟಣಗಳೂ ಸೇರಿ 'ಮದರಾಸು' ಬ್ರಿಟೀಷರ ಕೃಪೆಗೆ ಪಾತ್ರವಾಯಿತು. ಆದರೆ ಅಲ್ಲಿನ ಜನ ಅದನ್ನು 'ಚೆನ್ನಪಟ್ಟಣ' ಅಥವಾ 'ಚೆನ್ನಪುರಿ' ಎಂದೇ ಗುರುತಿಸುತ್ತಿದ್ದರು. 'ಚೆನ್ನು' ಎಂಬ ಪದ ತೆಲುಗು ಮೂಲದ ದಕ್ಷಿಣ ಮಧ್ಯ ದ್ರಾವಿಡ ಭಾಷೆಯ ಪದ ಇದರ ಅರ್ಥ "ಸುಂದರ" ಎಂದು ಹಾಗಾಗಿ 'ಚೆನ್ನಪುರಿ' ಅಥವಾ 'ಚೆನ್ನಪಟ್ಟಣಂ' ಎಂದರೆ "ಸುಂದರ ನಗರ" ಎಂದರ್ಥ. [599 chars] |
| ಕಾರು ಪ್ರಿಯರು ಯಾವ ವಿವಿಧ ಮಾದರಿಯ ಕಾರು ಗಳನ್ನು ನೋಡಬಹುದು ? [53 chars] | ಅರಮನೆಗಳು ಮತ್ತು ಕೋಟೆಗಳ ಹೊರತಾಗಿ ಜೈಪುರದಲ್ಲಿನ ಹಬ್ಬಗಳು ಮತ್ತು ಮೇಳಗಳೂ ತುಂಬಾ ಜನಪ್ರಿಯವಾಗಿದೆ. ಇಲ್ಲಿನ ಮೇಳಗಳಲ್ಲಿ ಒಂದೆಂದರೆ ಜೈಪುರ ವಿಂಟೇಜ್ ಕಾರ್ ರ್ಯಾಲಿ. ಇದನ್ನು ಜನವರಿಯಲ್ಲಿ ನಡೆಸಲಾಗುತ್ತದೆ. ಇತ್ತೀಚೆಗೆ ಈ ಮೇಳವು ತುಂಬಾ ಜನಪ್ರಿಯವಾಗುತ್ತಿದೆ. ಕಾರು ಪ್ರಿಯರು ಮರ್ಸಿಡಿಸ್‌, ಆಸ್ಟಿನ್‌ ಮತ್ತು ಫಿಯೆಟ್‌ನ ವಿವಿಧ ಮಾದರಿಯ ಕಾರುಗಳನ್ನು ನೋಡಬಹುದು. ಇಲ್ಲಿನ ಕೆಲವು ಕಾರುಗಳು 1900ರದ್ದಾಗಿರುವುದು ಗಮನಾರ್ಹ. ಇನ್ನೊಂದು ಜನಪ್ರಿಯ ಮೇಳವೆಂದರೆ ಆನೆ ಉತ್ಸವ. ಹೋಳಿ ಸಂದರ್ಭದಲ್ಲಿ ಈ ಉತ್ಸವವನ್ನು ಆಯೋಜಿಸಲಾಗುತ್ತದೆ. ಈ ಉತ್ಸವದಲ್ಲಿ ರಂಗುರಂಗಿನ ಸಾಂಸ್ಕೃತಿಕ ಕಾರ್ಯಕ್ರಮಗಳ ಜೊತೆಗೆ ಆನೆಯ ವಿವಿಧ ಆಟಗಳನ್ನೂ ನೋಡಬಹುದು. ಇದರ ಜೊತೆಗೆ, ಗಂಗಾರ್ ಹಬ್ಬ ಕೂಡಾ ಸ್ವಲ್ಪ ಮಟ್ಟಿಗೆ ಜನಪ್ರಿಯವಾಗಿದೆ. ಗನ್‌ ಎಂದರೆ ಶೀವ, ಗೌರ್ ಎಂದರೆ ಶಿವನ ಪತ್ನಿ ಪಾರ್ವತಿ. ಈ ಹಬ್ಬವು ಮದುವೆಯ ಬಂಧದ ಬಗ್ಗೆ. ಇನ್ನೂ ಕೆಲವು ಜನಪ್ರಿಯ ಹಬ್ಬಗಳು ಮತ್ತು ಮೇಳಗಳೆಂದರೆ ಭಂಗಾಂಗ ಮೇಳ, ತೀಜ್‌, ಹೋಳಿ ಮತ್ತು ಚಕ್ಸು ಮೇಳ. ಅವಕಾಶಗಳುಸಾಹಸೀ ಪ್ರವೃತ್ತಿಯವರು ಒಂಟೆ ಸವಾರಿ, ಬಿಸಿ ಗಾಳಿ ಬಲೂನಿಂಗ್‌, ಪ್ಯಾರಾಗ್ಲೈಡಿಂಗ್‌ ಮತ್ತು ರಾಕ್‌ ಕ್ಲೈಂಬಿಂಗ್‌ನ್ನು ಮಾಡಬಹುದು. ಕರೌಲಿ ಮತ್ತು ರಣಥಂಬೋರ್ ನ್ಯಾಷನಲ್‌ ಪಾರ್ಕ್‌ಗೆ ಉತ್ಸಾಹಿಗಳು ಪ್ರವಾಸ ಕೈಗೊಳ್ಳಬಹುದು. ಪ್ರವಾಸಿಗರು ಜೈಪುರದಲ್ಲಿ ಶಾಪಿಂಗ್‌ ಮಾಡುವುದನ್ನು ಇಷ್ಟಪಡುತ್ತಾರೆ. [978 chars] |

### Source Reference Table

| Source | Role |
| --- | --- |
| [Towards Leaving No Indic Language Behind](https://arxiv.org/abs/2212.05409) | IndicXTREME and IndicQA benchmark paper. |
| [mteb/IndicQARetrieval](https://huggingface.co/datasets/mteb/IndicQARetrieval) | MTEB retrieval task dataset card. |
| [ai4bharat/IndicQA](https://huggingface.co/datasets/ai4bharat/IndicQA) | Upstream IndicQA dataset card. |
| [hakari-bench/NanoIndicQA](https://huggingface.co/datasets/hakari-bench/NanoIndicQA) | Nano benchmark dataset containing this split. |

### Representative Snippets

| Query Pattern | Positive Document Pattern |
| --- | --- |
| A Kannada question asking which region was Muslim-majority. | A paragraph about Kashmir's population, borders, and accession context around 1947. |
| A question asking the meaning or origin of the word Chennai. | A paragraph about Madras, Madraspatnam, and the British East India Company settlement. |
| A question asking what types of vintage cars enthusiasts can see. | A paragraph about Jaipur festivals, fairs, and the vintage car rally. |
| A question asking in which river region the British East India Company was established. | A paragraph about the Ganga plain and British East India Company influence. |
| A question asking the best time to visit Aligarh. | A climate paragraph about monsoon-influenced weather, summer, and temperature ranges. |
