# NanoCMTEB / video

## Overview

NanoCMTEB `video` is a Chinese entertainment-video retrieval task from the Multi-CPR and C-MTEB retrieval families. Queries are very short user video-search strings, and documents are compact video title or metadata records. The task measures whether retrieval systems can identify the intended video, episode, clip, performer, title, or metadata item from short and sometimes mixed-script queries.

## Details

### What the Original Data Measures

Multi-CPR includes an entertainment-video retrieval domain collected from real search systems with human relevance judgments. C-MTEB includes VideoRetrieval in its Chinese retrieval group. The task is industrial search over short titles and metadata rather than long passage QA.

The query may be a title fragment, performer name, episode clue, romanized string, device term, or mixed-script entertainment search. The positive document is the matching video title or metadata record.

### Observed Data Profile

The task contains 200 queries, 10,000 documents, and 200 relevance judgments. It is strictly single-positive in the Nano labels: every query has exactly 1 positive, and there are 0 multi-positive queries.

Queries average 7.07 characters, and documents average 30.52 characters. Text is mainly Chinese but may include Japanese, English, Korean names, romanization, abbreviations, and mixed-script titles.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.6897, hit@10 of 0.8050, and recall@100 of 0.8950 using the top-500 BM25 candidate subset. This is a strong lexical baseline because exact title fragments, names, and episode tokens are highly informative.

BM25's limitation is alias and script variation. Short user queries may omit words, use alternate title forms, include romanization, or refer to a performer rather than the full title. Exact matching can also confuse same-series or same-cast items.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.8629, hit@10 of 0.9500, and recall@100 of 0.9850. Dense retrieval is the strongest top-ranking profile. It improves substantially over BM25 in nDCG@10 and hit@10.

This suggests that embedding similarity is effective for short entertainment metadata retrieval, especially when aliases, title variants, or mixed scripts separate the query from the exact document title.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.8103, hit@10 of 0.9200, and recall@100 of 0.9950. It uses a top-100 candidate range with an optional rank-101 safeguard; this task has 1 safeguard row, candidate counts from 100 to 101, and a mean of 100.01 candidates.

Hybrid retrieval has the best recall@100 but trails dense retrieval for top-10 ordering. The hybrid pool is useful for broad candidate coverage, while dense retrieval is the best observed ranker for the intended video item.

### Metric Interpretation for Model Researchers

This task is dense-favorable with a strong exact-match baseline. BM25 performs well because title terms and names are powerful signals, but dense retrieval better handles aliases and short-query ambiguity. Reranking_hybrid is useful when downstream reranking needs nearly complete top-100 coverage.

Because each query has a single positive, ranking mistakes usually represent selecting the wrong video, episode, cast-related item, or title variant. Precision over near duplicates is critical.

### Query and Relevance Type Tendencies

Queries include dance or exam videos, TV drama titles, performer names, animation episodes, educational or medical clips, device troubleshooting videos, and short mixed-script searches. Positive documents are compact titles or metadata records.

The relevance relation is exact media-item identification. Same-series, same-cast, same-topic, or same-device documents are hard negatives if they are not the intended item.

### Representative Failure Modes

Likely failures include retrieving the wrong episode from the same series, matching a performer but wrong clip, confusing romanized and translated titles, over-ranking same-topic device videos, and missing short aliases.

BM25 is vulnerable to alias and script mismatch. Dense retrieval can over-generalize within series or performer clusters. Hybrid retrieval improves coverage but still needs metadata-aware reranking for exact item selection.

### Training Data That May Help

Useful training data includes video search query-title pairs, entertainment metadata retrieval pairs, multilingual title alias pairs, and hard negatives from the same series, cast, performer, episode number, or device model.

Synthetic data should generate compact Chinese video titles and metadata records, then create short user video-search strings with aliases, abbreviations, romanization, and title variants. Hard negatives should share series names or people but differ in episode, season, device model, or media object.

### Model Improvement Notes

Strong systems should handle short queries, aliases, mixed scripts, and near-duplicate media metadata. Dense retrieval is the best observed first-stage method, while sparse matching remains useful for exact title fragments and names.

The task is useful for evaluating entertainment search systems where the user intent is a specific video record rather than a general topic.

## Example Data

| Query | Positive document |
| --- | --- |
| 游泳和悦悦 [5 chars] | 悦悦游泳20170817 21m [16 chars] |
| 甲状腺的检查 [6 chars] | 科普时间 专业仪器如何检查甲状腺 [16 chars] |
| BAMBINo [7 chars] | bambino2016 恩率 oppa [19 chars] |

### Source Reference Table

| Item | Reference |
| --- | --- |
| Task paper | [Multi-CPR: A Multi Domain Chinese Dataset for Passage Retrieval](https://arxiv.org/abs/2203.03367) |
| Benchmark paper | [C-Pack: Packed Resources For General Chinese Embeddings](https://arxiv.org/abs/2309.07597) |
| Source dataset | [mteb/VideoRetrieval](https://huggingface.co/datasets/mteb/VideoRetrieval) |
| NanoCMTEB dataset | [hakari-bench/NanoCMTEB](https://huggingface.co/datasets/hakari-bench/NanoCMTEB) |

Representative query and positive source snippets:

| Query | Positive document snippet |
| --- | --- |
| 游泳和悦悦 | A compact video title for a Yueyue swimming clip from 2017. |
| 甲状腺的检查 | A science or medical video title about checking the thyroid with professional instruments. |
| BAMBINo | A mixed-script performer or title metadata record containing "bambino". |
| 明天依然爱你泰国电视剧普通话版 | A drama title record for episode 15 of the series. |
| 秃鹰档案国语 | A video title about the Mandarin version of a crime or action clip. |
