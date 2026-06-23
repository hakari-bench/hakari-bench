# NanoVNMTEB / msmarco_vn

## Overview

`msmarco_vn` is the Vietnamese NanoVNMTEB version of MS MARCO passage retrieval. MS MARCO was introduced from real Bing search queries, human-generated answers, and web passages; BEIR later made the passage-ranking task a central dense-retrieval benchmark. In this VN-MTEB split, translated web-search queries retrieve translated short passages that answer everyday information needs.

The Nano split contains 200 queries, 10,000 candidate documents, and 214 positive qrels. Queries are very short, averaging 33.395 characters, while documents average 306.6902 characters. Most queries have a single positive, so the task behaves like concise question-to-passage retrieval rather than list retrieval. Dense retrieval is by far strongest on nDCG@10 and hit@10, while `reranking_hybrid` has the best recall@100. This makes the task useful for measuring whether a Vietnamese embedding model can map short web-search intent to answer-bearing passages without relying only on exact query words.

## Details

### What the Original Data Measures

MS MARCO measures retrieval for real user information needs. The passage-ranking setup uses a natural-language query and a set of candidate web passages, with positives that answer the query. The information needs are broad: health, weather, education, entertainment, products, locations, definitions, people, and factual attributes.

The Vietnamese version translates these short search queries and answer passages. Some queries are almost keyword-like, while others are short questions. Relevant passages often contain the answer directly but may not repeat the query surface form exactly. Retrieval therefore depends on matching answerability, not only topic.

### Observed Data Profile

There are 214 positive judgments for 200 queries. The average positive count is 1.07, the median is 1, and only 12 queries have multiple positives, giving a multi-positive rate of 6.0%. The maximum positive count is 3. This is a mostly single-positive benchmark where ranking the one answer-bearing passage early is central.

Documents are short web snippets or answer passages. Queries are the shortest in this group, which increases ambiguity. A phrase such as weather, a product count, a movie cast, a medical term, or a location may need a specific attribute rather than broad topical retrieval. The best systems must infer the intended answer slot.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.7578794816, hit@10 of 0.8250, and recall@100 of 0.9065420561 with a top-500 candidate set. This is a strong lexical baseline because many queries contain entity names, product names, medical terms, locations, or direct attribute words that also appear in the positive passage.

However, BM25 is well below dense retrieval at top ranks. Short translated queries often use compact wording, while passages answer with explanatory text. BM25 can retrieve same-entity passages that do not answer the requested attribute, or miss passages that express the answer using different wording. Lexical overlap is useful for candidate coverage, but not sufficient for answerability ranking.

### Dense Evaluation Profile

Dense retrieval with `harrier-oss-270m` reaches nDCG@10 of 0.9258599329, hit@10 of 0.9650, and recall@100 of 0.9719626168. It is the strongest condition for top-rank quality by a large margin. This result reflects the MS MARCO style: matching a user query to an answer passage often requires semantic compatibility rather than exact token overlap.

Dense retrieval is particularly helpful for short queries such as effects of Pedialyte, long-term effects of air pollution, energy-requiring cellular processes, Coca-Cola product lines, or weather in a location. It can connect the query intent to the answer sentence even when the passage uses expanded explanatory language. Its remaining weakness is candidate coverage for rare entity or exact attribute cases where sparse matching may rescue a missed positive.

### Reranking Hybrid Evaluation Profile

`reranking_hybrid` reaches nDCG@10 of 0.8285481029, hit@10 of 0.9000, and recall@100 of 0.9906542056. The top-100 candidate pool has mean candidate count 100.01, with 2 safeguard-positive rows and 2 rows containing 101 candidates. Hybrid retrieval is best on recall@100 but substantially below dense retrieval on nDCG@10 and hit@10.

This pattern shows a common tradeoff for web-search passage retrieval. Sparse evidence expands coverage and catches nearly all positives within the top 100, but the final ranking is less precise than dense retrieval alone. Same-entity or same-keyword passages can enter the candidate pool and compete with the answer-bearing passage. A stronger reranker would need to prioritize answerability over simple lexical match.

### Metric Interpretation for Model Researchers

Because most queries have exactly one positive, nDCG@10 and hit@10 are especially important. A model that retrieves the relevant passage at rank 50 has good recall but poor user-facing ranking. Dense retrieval's strong nDCG indicates better answer-bearing passage ordering.

At the same time, `reranking_hybrid` has the best recall@100, so hybrid candidate generation is valuable for downstream rerankers. The key research question is whether reranking can retain hybrid coverage while recovering dense-like top-order precision. Same-entity hard negatives are essential for evaluating that.

### Query and Relevance Type Tendencies

Queries include medical or health effects, weather, cell biology, product counts, entertainment, schools, location attributes, and definitions. Relevant documents are short passages that directly answer the query. Many queries are not full grammatical questions; they resemble search-box inputs.

The relevance relation is answerability. A passage mentioning Coca-Cola is not relevant unless it answers the product-line question. A passage about air pollution is not relevant unless it addresses long-term effects on humans. This makes the task different from broad topical retrieval.

### Representative Failure Modes

BM25 can retrieve passages that share the main entity but answer the wrong attribute. Dense retrieval can misread very short queries when the intended slot is underspecified. Hybrid retrieval can improve recall while ranking keyword-heavy distractors above the actual answer.

Another failure mode is translation ambiguity. Short Vietnamese search phrases may omit context, and passages may contain transliterated or imperfectly encoded names. Models need robust matching for both entity names and answer intent.

### Training Data That May Help

Useful training data includes official MS MARCO passage-ranking data with overlap removed, Vietnamese web-search query-passage pairs, multilingual click or answer-passage data, and translated MS MARCO data after careful leakage filtering. Because MS MARCO is widely used in retriever pretraining, overlap auditing is especially important.

Synthetic data should generate short Vietnamese search queries from short web passages. Hard negatives should share entities or locations but answer a different attribute. This teaches the model to rank answerability rather than topic overlap.

### Model Improvement Notes

The main improvement direction is answer-aware dense retrieval with hybrid coverage. Dense retrieval already ranks positives well, so sparse retrieval should be used to improve candidate recall without overpowering the semantic answer signal. Rerankers should compare the query's requested attribute against the passage's answer content.

Error analysis should classify failures as entity misses, attribute misses, ambiguity, or translation noise. For this task, improving top-rank precision is more important than simply increasing candidate volume, because most queries have only one relevant passage.

## Example Data

| Query | Positive document |
| --- | --- |
| Tác dụng của việc sử dụng pedialyte [35 chars] | Ngoài ra, nếu bạn đang hướng đến việc giảm cân thì lượng calo trong Pedialyte và nước tăng lực sẽ có thể làm mất tác dụng của những bài tập vừa phải. Tuy nhiên, bù nước bằng một loại thức uống như Pedialyte cho phép cơ thể tái tạo và giữ chất lỏng cũng như các khoáng chất thiết yếu lâu hơn so với nước lọc. Điểm cuối cùng: hãy cố gắng để chọn nước là lựa chọn số 1 của bạn về vấn đề cung cấp nước. Nhưng Pedialyte có thể mang lại lợi ích nếu bạn cảm thấy đặc biệt mất nước sau khi chạy đường dài hoặc thời tiết nóng nực. Nếu bạn nghĩ rằng mình sẽ được hưởng lợi từ việc bổ sung khoáng chất, DeRaad nói rằng nó có khả năng tự pha chế tại nhà theo hướng dẫn của Tổ chức Y tế Thế giới (World Health Organization). [711 chars] |
| hiệu ứng lâu dài của ô nhiễm không khí tác động lên con người là gì? [68 chars] | Khó thở, ho, đau ngực và khó thở. ï§ Ho ra nhiều hơn hoặc nặng hơn. ï§ Tăng nguy cơ bị bệnh tim mạch. Ngoài ra, tiếp xúc lâu dài với ô nhiễm không khí có thể gây ung thư và làm tổn thương hệ miễn dịch, thần kinh, sinh sản và hô hấp. [234 chars] |
| Quá trình tế bào nào đòi hỏi năng lượng [39 chars] | Có nhiều hơn nữa, những cái này chỉ là một vài ví dụ! [ATP (adenosine triphosphate) được dùng cho việc chuyển năng lượng trong tế bào nhưng nó không phải là hợp chất duy nhất được sử dụng. NTP, ADP, GTP & UTP để nêu ra một vài cái tên.] Các quá trình tế bào cần năng lượng. Ồm... bất cứ quá trình nào của tế bào sử dụng ATP (hoặc NTP/NTP khác) sẽ trả lời câu hỏi này. Ví dụ như sao chép DNA, phiên mã gen, tổng hợp protein, sinh tổng hợp axit béo--để nêu ra một vài cái tên. [474 chars] |

### Source Reference Table

| Source | Role |
|---|---|
| MS MARCO | Original machine reading and passage-ranking dataset |
| MS MARCO official page | Dataset and task context |
| BEIR | Retrieval benchmark framing |
| VN-MTEB | Vietnamese benchmark collection using translated retrieval tasks |
| GreenNode dataset card | Public dataset entry for this Vietnamese split |

### Representative Snippets

- Query: `Tác dụng của việc sử dụng pedialyte`
  Relevant documents discuss rehydration, calories, and effects of using Pedialyte.
- Query: `hiệu ứng lâu dài của ô nhiễm không khí tác động lên con người là gì?`
  Relevant documents describe long-term health effects of air pollution.
- Query: `Quá trình tế bào nào đòi hỏi năng lượng`
  Relevant documents discuss cellular processes and energy carriers such as ATP.
- Query: `Coca Cola có bao nhiêu dòng sản phẩm?`
  Relevant documents answer with counts or portfolios of Coca-Cola product lines.
- Query: `Thời tiết ở sao miguel`
  Relevant documents provide weather conditions or forecasts for Sao Miguel.
