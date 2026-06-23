# NanoVNMTEB / nano_nq

## Overview

`nano_nq` is the Vietnamese NanoVNMTEB version of the Nano Natural Questions retrieval task. Natural Questions was built from real Google search questions and Wikipedia evidence, with answer annotations over long and short answer spans. In this retrieval setting, short translated questions retrieve Vietnamese-translated Wikipedia-style passages that contain the answer evidence.

The Nano split contains 200 queries, 10,000 candidate documents, and 234 positive qrels. Queries average 39.4 characters, and documents average 565.2831 characters. Most queries have one positive, though 32 queries have multiple positives. Dense retrieval is strongest on nDCG@10 and hit@10, while `reranking_hybrid` has the best recall@100. The task is a concise open-domain QA retrieval benchmark where a model must match the asked attribute, not merely the named entity.

## Details

### What the Original Data Measures

Natural Questions uses naturally occurring Google search queries and Wikipedia pages from search results. Annotators mark answer-containing spans, which makes the task closer to real open-domain QA than synthetic question writing. In retrieval form, the system must retrieve the passage that contains the answer evidence.

The Vietnamese NanoNQ variant translates the queries and evidence passages. Questions often ask for people, locations, dates, works, definitions, meanings, or relationships. Relevant passages are Wikipedia-style documents headed by an entity or topic title. The retrieval challenge is to rank the passage that answers the specific question.

### Observed Data Profile

The task has 234 positives across 200 queries. The average positive count is 1.17, the median is 1, and the maximum is 3. The multi-positive rate is 16.0%. This means the benchmark is mostly single-answer evidence retrieval, with a small number of alternate evidence passages.

Queries are short and search-like. Documents are moderately long Wikipedia-style passages, often containing more context than the answer itself. A query such as a TV-character relation, a song phrase origin, or a geographic fact may share entity words with multiple passages, but only one passage contains the needed attribute.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.6095441594, hit@10 of 0.7650, and recall@100 of 0.8717948718 with a top-500 candidate set. Entity names and direct keywords help lexical retrieval, and many questions include recognizable titles or places.

The gap between BM25 and dense retrieval is large. BM25 often retrieves entity-related passages but struggles to identify the answer-bearing passage when wording changes or when the query asks for an attribute rather than an entity page. Same-entity different-attribute negatives are a major challenge.

### Dense Evaluation Profile

Dense retrieval with `harrier-oss-270m` reaches nDCG@10 of 0.8495036532, hit@10 of 0.9200, and recall@100 of 0.9572649573. It is clearly strongest on top-rank quality. This suggests that embeddings capture the semantic relation between a short question and the answer-bearing passage more effectively than lexical overlap.

Dense retrieval is especially valuable for queries where the target attribute is implicit: who a character's father is, when a season was released, where a phrase came from, what books someone wrote, or which river is associated with a city. The model must map the question form to evidence content, not simply match terms.

### Reranking Hybrid Evaluation Profile

`reranking_hybrid` reaches nDCG@10 of 0.7234286722, hit@10 of 0.8650, and recall@100 of 0.9914529915. The top-100 candidate pool has mean candidate count 100.005, with one safeguard-positive row and one row containing 101 candidates. Hybrid retrieval gives the best recall@100 but is below dense retrieval on top-rank metrics.

This pattern is typical for open-domain QA retrieval. Sparse signals help ensure that the positive passage is in the candidate pool, especially when entity names are exact. However, hybrid ranking can also promote same-entity distractors. Dense retrieval better orders the passage that answers the asked attribute.

### Metric Interpretation for Model Researchers

Because most queries have one positive, nDCG@10 and hit@10 are central. Recall@100 is useful for candidate generation, but a downstream QA model benefits most when the answer-bearing passage is near the top. Dense retrieval is the best top-rank signal in this split.

The hybrid recall result is still important: if a reranker can recover dense-like ordering over the high-recall candidate pool, it should improve the full pipeline. Evaluation should distinguish candidate coverage from final answer-passage ranking.

### Query and Relevance Type Tendencies

Queries ask about entertainment, geography, language usage, TV characters, books, rivers, release dates, and named entities. They are often short and ungrammatical in search-query style. Relevant documents are passages containing the specific answer evidence.

Relevance is attribute-specific. A passage about Bates Motel is not enough unless it identifies Dylan's father. A passage about Rome is not enough unless it contains the river relation. This makes the task stricter than broad entity retrieval.

### Representative Failure Modes

BM25 can retrieve the wrong page for a shared entity or title. Dense retrieval can fail when the query is too short or when entities are ambiguous after translation. Hybrid retrieval can maximize recall while ranking a lexical distractor above the actual answer passage.

Another failure mode is answer-slot mismatch. The model may retrieve a passage about a work's cast when the query asks for release date, or a geography page when the query asks for a related river. Hard negatives should target these same-entity different-attribute cases.

### Training Data That May Help

Useful training data includes official Natural Questions training examples with overlap removed, Vietnamese factoid QA over Wikipedia, non-overlapping Wikipedia question-passage retrieval pairs, and translated NQ data. Training should preserve the distinction between passage retrieval and answer extraction.

Synthetic data can generate short Vietnamese search-style questions from Wikipedia passages. It should include hard negatives that mention the same entity but answer a different attribute, because that is the main distinction retrieval must learn.

### Model Improvement Notes

The main improvement direction is attribute-aware dense retrieval with high-recall hybrid candidates. Sparse retrieval should preserve entity names and titles. Dense retrieval and reranking should focus on whether the passage answers the question's requested slot.

Error analysis should classify misses by entity ambiguity, attribute mismatch, translation issue, and long-passage distraction. Top-rank precision matters more than broad topical recall for this split.

## Example Data

| Query | Positive document |
| --- | --- |
| ai la cha của Dylan trong Bates Motel [37 chars] | Danh sách nhân vật trong phim Bates Motel Dylan Massett (do Max Thieriot thủ vai) [3] là con trai xa lạ của Norma và là anh cùng cha khác mẹ với Norman. Sau khi lớn lên hầu như tự lực cánh sinh, anh rất khôn ngoan, mạnh mẽ và độc lập. Anh thực sự quan tâm đến Norman, nhưng có mối quan hệ khó khăn với Norma. Anh tin rằng Norma tìm kiếm xung đột và kịch tính, và cách đối xử của cô ấy với Norman sẽ làm tổn thương anh ta. Khi đến White Pine Bay, sau khi bị sa thải gần đây, Dylan kết nối với Norman và khuyến khích anh ta sống cuộc sống ngoài Norma. Anh tham gia vào kinh doanh cần sa bất hợp pháp của thị trấn, và nhanh chóng thăng tiến trong hàng ngũ khi được những cấp trên yêu mến. Thế giới của anh sụp đổ, tuy nhiên, khi anh biết từ Norma rằng mình là kết quả của một vụ hiếp dâm loạn luân - cha thật sự của anh là anh trai của Norma, Caleb - và giữ khoảng cách với gia đình, chuyển ra khỏi nhà Bates. Cuối cùng anh kết nối lại với mẹ và em trai trong tập cuối mùa giải thứ hai. Trong mùa giải t... [1,000 / 2,150 chars] |
| mùa 5 của Ruby ra khi nào [25 chars] | Danh sách tập RWBY RWBY là một loạt phim hoạt hình trực tuyến Mỹ được sản xuất bởi Rooster Teeth Productions. Phim ra mắt vào ngày 18 tháng 7 năm 2013 trên trang web Rooster Teeth, và sau đó các tập phim được tải lên YouTube và các trang web phát trực tuyến như Crunchyroll. Bốn mùa, được gọi là "Tập", đã được phát hành, với mùa thứ năm hiện đang phát sóng kể từ khi ra mắt vào ngày 14 tháng 10 năm 2017.[1] Tính đến tháng 10 năm 2017, 54 tập, được gọi là "Chương", đã được phát hành. [486 chars] |
| câu nói blue moon xuất phát từ đâu [34 chars] | Trăng xanh Một giả thuyết đã được đưa ra rằng thuật ngữ "trăng xanh" cho "tháng nhuận" xuất hiện từ dân gian, trong đó "xanh" thay thế cho belewe không còn được hiểu nghĩa là "bất trung". Ý nghĩa gốc của nó sẽ là "Trăng phản bội", ám chỉ một trăng tròn mà nếu theo lịch thông thường (năm không có tháng nhuận), nó sẽ là trăng tròn mùa xuân, nhưng trong năm nhuận thì nó lại "phản bội" vì người ta sẽ phải kiêng ăn thêm một tháng nữa để tuân thủ theo thời gian Mùa Chay.[8][9] [476 chars] |

### Source Reference Table

| Source | Role |
|---|---|
| Natural Questions | Original open-domain QA benchmark |
| Natural Questions official page | Dataset and task context |
| BEIR | Retrieval benchmark framing |
| VN-MTEB | Vietnamese benchmark collection using translated retrieval tasks |
| GreenNode dataset card | Public dataset entry for this Vietnamese NanoNQ split |

### Representative Snippets

- Query: `ai la cha của Dylan trong Bates Motel`
  Relevant documents describe Bates Motel characters and Dylan's family relation.
- Query: `mùa 5 của Ruby ra khi nào`
  Relevant documents discuss RWBY episode or season release information.
- Query: `câu nói blue moon xuất phát từ đâu`
  Relevant documents explain the origin or meaning of the phrase "blue moon".
- Query: `danh sách sách viết bởi abul kalam azad`
  Relevant documents list works by Abul Kalam Azad.
- Query: `sông nào liên quan đến thành phố rome`
  Relevant documents identify the Tiber in relation to Rome.
