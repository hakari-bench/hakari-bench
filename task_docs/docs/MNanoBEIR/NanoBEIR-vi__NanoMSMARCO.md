# MNanoBEIR / NanoBEIR-vi / NanoMSMARCO

## Overview

NanoMSMARCO in the Vietnamese NanoBEIR slice is a web passage retrieval task derived from MS MARCO. The queries are Vietnamese translated web-search questions, and the corpus contains Vietnamese translated answer-bearing passages. The retrieval goal is to find a passage that directly answers a short user question. This compact task is useful for evaluating Vietnamese open-domain QA retrieval, short-query interpretation, and answer-oriented passage ranking.

## Details

### What the Original Data Measures

MS MARCO was built from real user questions submitted to a search engine and passages that can answer them. In retrieval form, the model must match a short, natural question to an answer passage. The relevant passage may define a term, identify a person, explain a location, resolve a consumer question, or provide a concise factual answer.

The Vietnamese translated version preserves the web-question style. Queries are short and often informal, while passages may contain fuller explanatory text. Some named entities, song titles, organizations, and quoted terms remain in English. A strong retriever must bridge between the question wording and the answer expression used in the passage.

### Observed Data Profile

The task contains 50 queries, 5,043 documents, and 50 relevance judgments. Each query has one positive passage, so the positives-per-query average is 1.0, the minimum is 1, the median is 1.0, the maximum is 1, and there are no multi-positive queries.

Queries average 34.92 characters, while documents average 335.01 characters. This is a short-query retrieval task: the query often provides only a small number of words, and the model must infer the answer type and rank the correct passage above many topically similar distractors.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.3423, hit@10 of 0.5600, and recall@100 of 0.9200 using the top-500 BM25 candidate subset. The high recall@100 shows that lexical matching often finds the answer passage somewhere in the candidate set. Short web questions include visible anchors such as names, quoted terms, or key nouns.

The much lower top-10 metrics show that BM25 struggles with final ordering. Many web passages share the same surface terms but do not answer the exact question. Term frequency helps candidate generation, but it can overvalue passages that mention the query words without providing the answer.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.4934, hit@10 of 0.6800, and recall@100 of 1.0000. Dense retrieval is the strongest direct profile across these metrics. It improves first-page ranking and covers every positive passage within the top 100 candidates.

This indicates that embedding similarity is especially useful for Vietnamese MS MARCO-style questions. The model can connect question intent to answer passages even when the answer wording differs from the query. The gain over BM25 is consistent with a task where semantic answer matching matters more than repeated term overlap.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.4454, hit@10 of 0.6800, and recall@100 of 0.9800. It uses a top-100 candidate range with an optional rank-101 safeguard; this slice has 1 safeguard row, candidate counts from 100 to 101, and a mean of 100.02 candidates.

The hybrid profile matches dense hit@10 and keeps very high recall, but dense retrieval remains stronger on nDCG@10 and recall@100. This suggests that lexical signals help preserve some exact-match cases, while dense retrieval already captures most of the answer intent. For reranking, reranking_hybrid is still a strong candidate pool because it combines exact anchors with semantic coverage.

### Metric Interpretation for Model Researchers

Because each query has one positive, hit@10 is a direct visibility metric: the answer passage is either present in the top results or not. nDCG@10 adds sensitivity to rank position, which is important for search and RAG systems that only inspect a few passages. recall@100 indicates whether a reranker has access to the answer.

The comparison shows that BM25 is effective as a broad candidate generator, dense retrieval is best as a direct ranker, and reranking_hybrid is a high-recall candidate pool with dense-like hit@10. This task is useful for testing whether improvements come from understanding short question intent rather than from lexical memorization.

### Query and Relevance Type Tendencies

Queries ask short web questions such as what rumination syndrome is, who sang "Here I Go Again", who Cameron Boyce played in Liv and Maddie, where Earth's major deserts occur, and what "copper" means as police slang. Relevant passages typically give a direct factual or definitional answer.

The task rewards answer-type recognition. The model must distinguish passages that merely mention the entity from passages that answer the question. Short queries leave little context, so errors often depend on whether the retriever can infer the missing relation.

### Representative Failure Modes

Likely failures include retrieving passages that contain the same name but answer another question, confusing song or media titles, missing definitions when the query uses informal wording, and ranking broad background passages above concise answers. BM25 may be too literal, while dense retrieval may retrieve semantically related passages that do not contain the final answer.

### Training Data That May Help

Useful training data includes Vietnamese web QA retrieval, translated MS MARCO-style question-passage pairs, short-query answer ranking, and hard negatives that share the main entity but do not answer the asked relation. Query rewriting or synthetic short-question generation can also help models learn the implicit answer type.

### Model Improvement Notes

A model targeting this task should focus on short-query semantic matching and answer-bearing passage ranking. Sparse systems need better expansion for paraphrases and informal phrasing. Dense systems are already strong but can improve with answer-aware hard negatives. Hybrid systems should be evaluated as reranking inputs because they retain strong exact-match coverage while approaching dense top-10 behavior.

## Example Data

| Query | Positive document |
| --- | --- |
| hội chứng suy nghĩ lặp lại là gì [32 chars] | Hội chứng nhai lại. Hội chứng nhai lại, còn được gọi là Merycism, là một loại rối loạn ăn uống không được xác định cụ thể nào khác, gây ra việc trào ngược thức ăn. Mặc dù nó không được xác định là một rối loạn ăn uống cụ thể trong DSM-IV, một số tiêu chí đã được nêu ra để chẩn đoán rối loạn này. [296 chars] |
| ai đã hát bài here i go again [29 chars] | Đối với các mục đích khác, xem Here I Go Again (phân định). Here I Go Again là một bài hát của ban nhạc rock người Anh Whitesnake. Ban đầu được phát hành trong album năm 1982 của họ, Saints & Sinners, bài hát đã được thu âm lại cho album tựa đề của họ năm 1987, Whitesnake. Bài hát đã được thu âm lại một lần nữa trong năm đó với phiên bản trộn radio mới. [355 chars] |
| ai là người mà cameron boyce đóng trong liv và maddie [53 chars] | Chuẩn bị cho những tiếng cười nghiêng ngả, các bạn ơi. Trong một đoạn clip độc quyền của tập phim ngày 19 tháng 4 của Liv & Maddie có tên “Prom-A-Rooney.” Rõ ràng rồi. Trong đoạn clip hài hước này, chúng ta thấy ngôi sao Jessie Cameron Boyce nhảy sang một chương trình Disney khác để gặp Maddie (Shelby Wulfert). Nhân vật của anh ấy thì, ừm, lập dị! [349 chars] |

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original dataset | [MS MARCO](https://arxiv.org/abs/1611.09268) |
| Retrieval benchmark framing | [BEIR](https://arxiv.org/abs/2104.08663) |
| Multilingual benchmark context | [MMTEB](https://arxiv.org/abs/2502.13595) |
| NanoBEIR collection | [NanoBEIR on Hugging Face](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
| NanoBEIR-vi dataset | [hakari-bench/NanoBEIR-vi](https://huggingface.co/datasets/hakari-bench/NanoBEIR-vi) |

Representative query and positive answer snippets:

| Query | Positive document snippet |
| --- | --- |
| hoi chung suy nghi lap lai la gi | Hoi chung nhai lai, con duoc goi la Merycism, la mot loai roi loan an uong... |
| ai da hat bai here i go again | Here I Go Again la mot bai hat cua ban nhac rock nguoi Anh Whitesnake... |
| ai la nguoi ma cameron boyce dong trong liv va maddie | Trong mot doan clip doc quyen cua tap phim Liv & Maddie co ten Prom-A-Rooney... |
| cac sa mac lon cua trai dat chu yeu xay ra o dau | Phan con lai cua cac sa mac tren Trai Dat nam ngoai cac khu vuc cuc... |
| nghia cua tu "copper" trong tieng long chi canh sat | Tu "copper" co the co truoc tu "cop" va duoc dung de chi canh sat... |
