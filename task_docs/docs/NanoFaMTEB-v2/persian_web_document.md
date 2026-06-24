# NanoFaMTEB-v2 / persian_web_document

## Overview

`persian_web_document` is a Persian web document retrieval task in NanoFaMTEB-v2. The queries are very short Persian web-search phrases, and the documents are web page snippets or short web passages.

This task is highly lexical but still useful for retrieval research. Short queries often appear directly in relevant documents, while ambiguity, spelling variation, near-duplicate snippets, and many-positive relevance sets create ranking pressure beyond exact phrase matching.

## Details

### What the Original Data Measures

FaMTEB adds Persian retrieval datasets, including web-collected resources, to broaden Persian embedding evaluation. This task uses `MCINext/persian-web-document-retrieval`, with a source reference available through an IEEE record. MTEB provides the general retrieval evaluation framework.

The task measures web-style document retrieval in Persian. Unlike encyclopedia QA, the query may be a search phrase, song lyric, video title, series episode request, or short informational keyword string. Relevant documents resemble search results, snippets, or compact pages that satisfy the user's web intent.

### Observed Data Profile

This Nano split contains 200 queries, 10,000 documents, and 2,186 positive qrels. Queries have 10.93 positives on average, with a minimum of 1, a median of 9.0, and a maximum of 39. There are 185 multi-positive queries, or 92.5% of the split. Queries average only 16.35 characters, and documents average 228.31 characters.

Observed examples include movie download searches, romantic clip searches, television episode requests, music lyric queries, and Quran-related search phrases. Documents are often short snippets with titles, download text, platform names, or direct answer fragments.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.6990, hit@10 of 0.9500, and recall@100 of 0.9607 with a top-500 candidate pool. This is a strong lexical profile. Many queries are short and phrase-like, so exact term occurrence and title overlap are highly predictive.

The remaining difficulty comes from ambiguity and near duplicates. A short phrase can refer to several videos, songs, pages, or answer snippets. BM25 may also over-rank pages that repeat the query phrase but do not match the user's intended result.

### Dense Evaluation Profile

The dense harrier-oss-270m profile reaches nDCG@10 of 0.7780, hit@10 of 0.9700, and recall@100 of 0.9689. Dense retrieval improves over BM25 across the main metrics, despite the task's lexical character.

This suggests that embedding similarity helps resolve web intent beyond exact phrase overlap. Dense retrieval can connect spelling variation, transliteration, related titles, and query-document paraphrases. It is especially useful when a snippet answers the intent without repeating the full query string.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate subset reaches nDCG@10 of 0.7703, hit@10 of 0.9750, and recall@100 of 0.9895. It uses exactly 100 candidates per query and has no safeguard-positive rows.

Hybrid retrieval provides the strongest candidate coverage and the best hit@10. Dense retrieval is slightly higher on nDCG@10, but the hybrid pool is better for reranking because it combines exact phrase recall with semantic matching and captures nearly all relevant candidates in the top 100.

### Metric Interpretation for Model Researchers

`persian_web_document` is a short-query web retrieval task where all three profiles are strong. BM25 is already competitive because query words frequently appear in titles or snippets. Dense retrieval gives better top-10 ranking, and reranking_hybrid gives the best relevant coverage.

Because most queries have multiple positives, hit@10 is not enough to distinguish models. nDCG@10 and recall@100 better show whether a model ranks the most useful snippets highly and covers many acceptable results.

### Query and Relevance Type Tendencies

Queries are short Persian search phrases. Many are not grammatical questions; they are closer to search-box input. They may contain media titles, informal wording, spelling variants, or partial phrases.

Relevant documents are snippets or short web pages. A positive document may be relevant because it links to the requested media, provides a direct answer, repeats the searched phrase in a useful title, or matches the user's intended page type.

### Representative Failure Modes

BM25 may retrieve spam-like or repeated-query pages that contain the words but do not satisfy the intent. Dense retrieval may merge similar entertainment titles, episodes, songs, or religious terms. Hybrid retrieval reduces candidate misses, but reranking must still handle near-duplicate snippets and noisy web text.

Short queries also create intent ambiguity. The same phrase may refer to a film, download page, clip, lyric, answer site, or episode list.

### Training Data That May Help

Useful training data includes Persian web search logs, query-document click pairs, Persian snippet retrieval, short-query passage ranking, and hard negatives from the same search result pages. Training should include spelling variants, informal Persian, transliterated names, and near-duplicate web snippets.

Training should exclude this split's evaluation queries and qrels.

### Model Improvement Notes

Improving this task requires balancing lexical precision and semantic intent. Models should preserve short exact phrases and media titles while also handling variants and partial matches.

For reranking, useful signals include title quality, snippet intent match, and rejecting pages that only repeat the query. A strong reranker should prefer pages that look like the requested result rather than pages with generic keyword stuffing.

## Example Data

| Query | Positive document |
| --- | --- |
| فیلم سینمایی۳۵۶ روز بدون‌سانسور [31 chars] | دانلود فیلم 365 روز 1 (بدون سانسور) - فیلو دانلود فیلم 365 روز 1 (بدون سانسور) تیزر مووی [89 chars] |
| کلیپ عاشفانه [12 chars] | آپارات \| کافه کلیپ عاشقانه [27 chars] |
| واکینگ دد قسمت ۲۲ فصل ۱۱ [24 chars] | سریال مردگان متحرک :: فصل 11 قسمت 22 :: زیرنویس فارسی دانلود فصل یازدهم مجموعه واکینگ دِد(The Walking Dead - مردگان متحرک) با زیرنویس فارسی و کیفیت فول اچ دی 1080p Full HD \| رده سنی: 15+ سال \| محصول: امریکا \| ژانر:درام، وحشت، ماجراجویی \| IMDb خلاصه: سریال مردگان متحرک (The Walking Dead) یکی از محبوب‌ترین مجموعه‌های تاریخ تلویزیون است. این مجموعه در طول ۱۰ فصل قبلی‌اش با فراز و نشیب‌های بسیاری همراه بوده و هم‌اکنون با فصل یازدهم، می‌خواهد تجربه تازه‌ای را برای مخاطبان رقم بزند آخرین فصل از مجموعه تلویزیونی مردگان متحرک است که شامل ۲۴ قسمت خواهد بود و در طول سالهای ۲۰۲۱ و ۲۰۲۲ پخش خواهد شد. [596 chars] |

### Source Reference Table

| Source | Role |
| --- | --- |
| [FaMTEB: Massive Text Embedding Benchmark in Persian Language](https://arxiv.org/abs/2502.11571) | Persian embedding benchmark paper. |
| [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316) | General embedding benchmark framework. |
| [PersianWebDocumentRetrieval source reference](https://ieeexplore.ieee.org/document/10553090) | IEEE source record linked from the task metadata. |
| [MCINext/persian-web-document-retrieval](https://huggingface.co/datasets/MCINext/persian-web-document-retrieval) | Public source dataset card. |
| [hakari-bench/NanoFaMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoFaMTEB-v2) | Nano benchmark dataset containing this split. |

### Representative Snippets

| Query Pattern | Positive Document Pattern |
| --- | --- |
| A short Persian query for an uncensored movie download. | A snippet whose title advertises a specific movie download page. |
| A brief query for a romantic clip. | A video-platform or clip-page snippet matching the requested clip type. |
| A query for a specific episode of a television series. | A snippet describing the season, episode, subtitles, quality, and genre of the requested show. |
| A lyric-like music query containing a place name and phrase. | A music download page snippet with the song title, remix, or lyrics. |
| A short Quran-related search phrase. | A question-answer or magazine-style snippet giving the requested surah-related answer. |
