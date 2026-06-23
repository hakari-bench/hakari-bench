# MNanoBEIR / NanoBEIR-vi / NanoDBPedia

## Overview

NanoDBPedia in the Vietnamese NanoBEIR slice is an entity-oriented retrieval task derived from DBpedia Entity Retrieval. The queries are Vietnamese translated entity information needs, and the corpus contains Vietnamese translated DBpedia-style entity descriptions. The task asks a model to rank entities that satisfy short needs involving names, categories, places, works, organizations, or entity classes. It is a compact diagnostic for Vietnamese entity search, alias handling, and type-aware retrieval.

## Details

### What the Original Data Measures

DBpedia Entity Retrieval evaluates entity ranking for information needs over a structured encyclopedic collection. In BEIR-style retrieval, entity descriptions are treated as documents. Relevance can depend on names, aliases, types, places, categories, and relationships. A relevant entity must satisfy the intent of the query, not simply share a visible token.

The Vietnamese translated version tests short-query entity matching with translated descriptions and mixed entity names. Some names remain English, while surrounding descriptions are Vietnamese. A strong retriever must combine exact name matching with semantic type and category understanding.

### Observed Data Profile

The task contains 50 queries, 6,045 documents, and 1,158 relevance judgments. It is strongly multi-positive, with an average of 23.16 positives per query. The minimum is 1, the median is 18.0, the maximum is 81, and 48 queries are multi-positive, or 96.0% of the query set. This makes the task a broad entity ranking benchmark.

Queries average 35.04 characters, while documents average 358.04 characters. Queries are short and often keyword-like, while the documents are concise entity summaries. Ranking must cover many acceptable entities for broad needs, not just the most obvious exact match.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.4949, hit@10 of 0.9000, and recall@100 of 0.6010 using the top-500 BM25 candidate subset. This is a strong lexical baseline. Entity queries often include names, locations, or category words that appear directly in the relevant descriptions.

The recall@100 value shows that exact overlap still misses a significant part of the relevant set. Entity needs can involve aliases, translated category labels, or broad classes of entities. BM25 can find obvious name matches, but it is less reliable for type-aware coverage across many positives.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.5676, hit@10 of 0.9600, and recall@100 of 0.7098. Dense retrieval is strongest across the main metrics. This indicates that embedding similarity captures type, category, and semantic entity constraints beyond surface words.

Dense retrieval is especially helpful for short entity needs that are underspecified or category-like. It can connect a query such as films shot in a city, former republics, or architecture in a location to entity descriptions that satisfy the type constraint without sharing all terms exactly. Remaining errors likely involve ambiguous entity classes or broad queries with many relevant results.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.5628, hit@10 of 0.9400, and recall@100 of 0.7029. It uses exactly 100 candidates per query, with no rank-101 safeguard rows. The hybrid profile is close to dense retrieval but slightly weaker on all three metrics.

This suggests that lexical evidence is useful, but dense ordering is already well aligned with the Vietnamese entity retrieval task. Hybrid search remains a strong candidate source, especially for exact names, but it does not improve over dense retrieval in this slice. The final ranking should keep semantic type matching central.

### Metric Interpretation for Model Researchers

Because almost every query has many positives, hit@10 alone is not enough. A model can find one entity early while missing many other relevant entities. nDCG@10 measures first-page ranking quality, while recall@100 measures relevant-set coverage for downstream reranking or browsing.

The method comparison shows that BM25 is strong for exact entity anchors, dense retrieval is best for broad entity ranking, and reranking_hybrid is competitive but not superior. NanoDBPedia-vi is useful for testing whether models can combine entity names with type and category constraints.

### Query and Relevance Type Tendencies

Queries include entity needs such as a Fitzgerald Auto Mall in Chambersburg, a 1994 Alice Munro short-story collection, Gallo-Roman architecture in Paris, former Yugoslav republics, and films shot in Venice. Relevant documents are DBpedia-style descriptions of entities satisfying those needs.

The task rewards constraint tracking. A query may specify a work type, location, author, historical group, or class of films. A same-name or same-location entity can be wrong if it violates the intended type.

### Representative Failure Modes

Likely failures include retrieving the wrong entity type, over-ranking famous entities that share a name fragment, missing aliases or translated category labels, and failing to cover broad entity classes. BM25 may be too literal, while dense retrieval may blur related entity types. Hybrid systems can inherit both errors if lexical anchors overpower type semantics.

### Training Data That May Help

Useful training data includes Vietnamese entity search, Wikipedia or DBpedia retrieval, alias matching, multilingual entity linking, type-aware ranking, and hard negatives sharing a location, name, category, or entity type while violating a key constraint.

### Model Improvement Notes

A model targeting this task should combine exact name precision with semantic type awareness. Sparse systems need alias and morphology handling. Dense systems should improve constraint tracking for short queries. Hybrid systems should preserve exact entity anchors without weakening the dense model's ability to rank broad relevant sets.

## Example Data

| Query | Positive document |
| --- | --- |
| fitzgerald auto mall chambersburg pa [36 chars] | Fitzgerald Auto Malls là một đại lý ô tô thuộc sở hữu và điều hành bởi gia đình, được thành lập vào năm 1966, với địa điểm đầu tiên mở cửa tại Bethesda, Maryland. Tính đến năm 2014, Fitzgerald Auto Ma... [200 / 457 chars] |
| Tập truyện ngắn năm 1994 của Alice Munro là Mở [46 chars] | Alice Ann Munro (/ˈælɨs ˌæn mʌnˈroʊ/, tên thật là Laidlaw /ˈleɪdlɔː/; sinh ngày 10 tháng 7 năm 1931) là một tác giả người Canada. Tác phẩm của Munro được mô tả là đã cách mạng hóa cấu trúc của truyện... [200 / 553 chars] |
| kiến trúc Gallo-Roman ở Paris [29 chars] | Nghệ thuật ở Paris là một bài viết về văn hóa và lịch sử nghệ thuật ở Paris, thủ đô của Pháp. Trong nhiều thế kỷ, Paris đã thu hút các nghệ sĩ từ khắp nơi trên thế giới, đến thành phố để học hỏi và tì... [200 / 344 chars] |
| các nước cộng hòa của Nam Tư cũ [31 chars] | Hiến pháp Nam Tư năm 1974 là hiến pháp thứ tư và cuối cùng của Cộng hòa Liên bang Xã hội chủ nghĩa Nam Tư. Nó có hiệu lực vào ngày 21 tháng 2. Với 406 điều khoản gốc, hiến pháp năm 1974 là một trong n... [200 / 420 chars] |
| phim quay ở Venice [18 chars] | A Little Romance là một bộ phim hài lãng mạn Technicolor và Panavision của Mỹ ra mắt năm 1979, được đạo diễn bởi George Roy Hill và có sự tham gia của Laurence Olivier, Thelonious Bernard, và Diane La... [200 / 403 chars] |

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original dataset | [DBpedia Entity Retrieval](https://doi.org/10.1145/3077136.3080751) |
| Retrieval benchmark framing | [BEIR](https://arxiv.org/abs/2104.08663) |
| Multilingual benchmark context | [MMTEB](https://arxiv.org/abs/2502.13595) |
| NanoBEIR collection | [NanoBEIR on Hugging Face](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
| NanoBEIR-vi dataset | [hakari-bench/NanoBEIR-vi](https://huggingface.co/datasets/hakari-bench/NanoBEIR-vi) |

Representative query and positive entity snippets:

| Query | Positive document snippet |
| --- | --- |
| fitzgerald auto mall chambersburg pa | Fitzgerald Auto Malls là một đại lý ô tô thuộc sở hữu và điều hành bởi gia đình... |
| Tập truyện ngắn năm 1994 của Alice Munro là Mở | Alice Ann Munro là một tác giả người Canada. Tác phẩm của Munro được mô tả là đã cách mạng hóa... |
| kiến trúc Gallo-Roman ở Paris | Nghệ thuật ở Paris là một bài viết về văn hóa và lịch sử nghệ thuật ở Paris... |
| các nước cộng hòa của Nam Tư cũ | Hiến pháp Nam Tư năm 1974 là hiến pháp thứ tư và cuối cùng của Cộng hòa Liên bang Xã hội chủ nghĩa Nam Tư... |
| phim quay ở Venice | A Little Romance là một bộ phim hài lãng mạn Technicolor và Panavision của Mỹ ra mắt năm 1979... |
