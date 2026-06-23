# NanoVNMTEB / nq_vn

## Overview

`nq_vn` is the Vietnamese NanoVNMTEB version of Natural Questions retrieval. Natural Questions was built from real Google search questions and Wikipedia evidence, with annotations for answer-bearing passages and short answers. In this retrieval formulation, each translated Vietnamese question must retrieve a Wikipedia-style passage containing the evidence needed to answer it.

The Nano split contains 200 queries, 10,000 candidate documents, and 234 positive qrels. Queries average 39.4 characters, and documents average 557.6004 characters. Most queries have a single relevant passage, while 32 queries have more than one. Dense retrieval is strongest on nDCG@10 and hit@10, while `reranking_hybrid` has the highest recall@100. The task tests whether a model can map short factoid questions to the passage containing the requested attribute, not just to a broadly related entity page.

## Details

### What the Original Data Measures

Natural Questions uses naturally occurring Google search questions paired with Wikipedia pages selected from search results. Annotators mark long answers and short answers, which makes the benchmark an open-domain QA task grounded in real user behavior. Retrieval systems are evaluated on finding the passage that contains answer evidence.

The Vietnamese version translates this setting into Vietnamese. Questions often ask about people, places, industries, books, films, fictional characters, renamed products, rivers, or dates. Relevant documents are translated Wikipedia-style passages. A model must retrieve the passage that provides the requested fact, even when several passages share the same named entity.

### Observed Data Profile

The task has 234 positives across 200 queries. The average is 1.17 positives per query, the median is 1, and the maximum is 3. The multi-positive rate is 16.0%. This makes the task mostly single-evidence retrieval.

Documents are mid-length Wikipedia passages. Queries are short and search-like, so they often provide only a named entity plus an attribute request. The difficulty is identifying the right attribute page or passage rather than retrieving any page that mentions the entity.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.5882327267, hit@10 of 0.7450, and recall@100 of 0.8717948718 with a top-500 candidate set. Exact entity names and rare terms are useful, and lexical retrieval often finds relevant candidate passages.

The lower top-rank metrics show that BM25 struggles with attribute matching. A query may mention a character, place, book, or product, but the positive passage is the one that contains a particular relation such as parent, industry, location, author, inspiration, or renaming date. Same-entity different-attribute negatives are the main issue.

### Dense Evaluation Profile

Dense retrieval with `harrier-oss-270m` reaches nDCG@10 of 0.7981125310, hit@10 of 0.9000, and recall@100 of 0.9658119658. It is the strongest condition for top-rank quality. The large gap over BM25 indicates that semantic matching between the question form and the answer-bearing passage is crucial.

Dense retrieval is helpful when the query asks for an attribute using wording not repeated in the passage. It can connect questions about a main industry, a venue tenant, books by a person, a character's inspiration, or a product rename to the relevant evidence. Its remaining weakness is recall in rare entity cases, where exact lexical matching can still rescue candidates.

### Reranking Hybrid Evaluation Profile

`reranking_hybrid` reaches nDCG@10 of 0.6825894352, hit@10 of 0.8300, and recall@100 of 0.9957264957. The top-100 candidate pool has exactly 100 candidates per query and no safeguard-expanded rows. Hybrid retrieval gives nearly complete recall@100 but falls below dense retrieval on nDCG@10 and hit@10.

This shows a coverage-versus-ordering tradeoff. Sparse evidence helps ensure that almost every positive passage appears in the candidate set, but it can also raise same-entity distractors. Dense retrieval ranks answer-bearing passages better. A strong pipeline would use hybrid candidate generation followed by a relation-aware reranker.

### Metric Interpretation for Model Researchers

Because the median positive count is 1, nDCG@10 is a strict measure of whether the correct answer evidence appears early. Recall@100 is valuable for reranking pipelines, but on its own it does not show whether a user or reader model will see the right passage first.

The metric pattern is clear: dense is best for immediate ranking, hybrid is best for coverage. Researchers should analyze whether errors are caused by missing the entity entirely or by retrieving the right entity but the wrong attribute passage.

### Query and Relevance Type Tendencies

Queries ask concise factoid questions: what industry dominates an area, who plays at a venue, which books a person wrote, who inspired a character, when a product changed names, or which river is associated with a city. Relevant documents are passages that explicitly contain the answer relation.

Relevance is answer-evidence matching. A document about the same person, city, show, or product is not necessarily relevant unless it contains the requested fact. This makes the task more precise than broad Wikipedia entity retrieval.

### Representative Failure Modes

BM25 can retrieve passages with entity overlap but no answer. Dense retrieval can confuse short ambiguous queries when several entities or titles are similar. Hybrid retrieval can place lexical same-entity candidates above the positive passage, reducing nDCG despite excellent recall.

Another failure mode is translation and title mismatch. Some names, works, or locations may retain English forms, be transliterated, or appear in translated titles. Models need robust entity matching and attribute-aware ranking together.

### Training Data That May Help

Useful training data includes official Natural Questions training examples with overlap removed, Vietnamese Wikipedia QA, non-overlapping question-to-passage retrieval pairs, and translated NQ data. Because NQ is widely used for retrieval training, overlap checks are important.

Synthetic data should generate Vietnamese search-style questions from Wikipedia passages and include same-entity hard negatives with different requested attributes. This teaches the model to distinguish answer evidence from topical similarity.

### Model Improvement Notes

The main improvement direction is attribute-aware dense retrieval and reranking. Sparse matching should preserve entity names, while dense matching should represent the requested relation. Rerankers should verify that the passage contains the answer evidence, not only the query entity.

Error analysis should categorize entity recall, attribute mismatch, title translation mismatch, and ambiguous short-query interpretation. For this task, improving top-rank precision is more important than expanding already-high candidate recall.

## Example Data

| Query | Positive document |
| --- | --- |
| ai la cha của Dylan trong Bates Motel [37 chars] | Danh sách nhân vật trong phim Bates Motel Dylan Massett (do Max Thieriot thủ vai) [3] là con trai xa lạ của Norma và là anh cùng cha khác mẹ với Norman. Sau khi lớn lên hầu như tự lực cánh sinh, anh r... [200 / 2,150 chars] |
| mùa 5 của Ruby ra khi nào [25 chars] | Danh sách tập RWBY RWBY là một loạt phim hoạt hình trực tuyến Mỹ được sản xuất bởi Rooster Teeth Productions. Phim ra mắt vào ngày 18 tháng 7 năm 2013 trên trang web Rooster Teeth, và sau đó các tập p... [200 / 486 chars] |
| câu nói blue moon xuất phát từ đâu [34 chars] | Trăng xanh Một giả thuyết đã được đưa ra rằng thuật ngữ "trăng xanh" cho "tháng nhuận" xuất hiện từ dân gian, trong đó "xanh" thay thế cho belewe không còn được hiểu nghĩa là "bất trung". Ý nghĩa gốc... [200 / 476 chars] |
| danh sách sách viết bởi abul kalam azad [39 chars] | Abul Kalam Azad Maulana Azad được cho là một trong những nhà văn tiếng Urdu vĩ đại nhất của thế kỷ 20. Ông đã viết nhiều sách bao gồm cả Ấn Độ giành được tự do, Ghubar-e-Khatir, Tazkirah, Tarjumanul Q... [200 / 211 chars] |
| sông nào liên quan đến thành phố rome [37 chars] | Tiber Sông Tiber (/ ˈtaɪbər /, tiếng Latin Tiberis,[1] tiếng Ý Tevere, phát âm tiếng Ý: [ˈteːvere] ) [2] là con sông dài thứ ba ở Ý, bắt nguồn từ dãy núi Apennine ở Emilia-Romagna và chảy 406 km (252... [200 / 513 chars] |

### Source Reference Table

| Source | Role |
|---|---|
| Natural Questions | Original open-domain QA benchmark |
| Natural Questions official page | Dataset and task context |
| BEIR | Retrieval benchmark framing |
| VN-MTEB | Vietnamese benchmark collection using translated retrieval tasks |
| GreenNode dataset card | Public dataset entry for this Vietnamese NQ split |

### Representative Snippets

- Query: `ai la cha của Dylan trong Bates Motel`
  Relevant documents describe Bates Motel characters and Dylan's family relation.
- Query: `mùa 5 của Ruby ra khi nào`
  Relevant documents contain RWBY release or episode information.
- Query: `câu nói blue moon xuất phát từ đâu`
  Relevant documents explain the origin or meaning of "blue moon".
- Query: `danh sách sách viết bởi abul kalam azad`
  Relevant documents list books written by Abul Kalam Azad.
- Query: `sông nào liên quan đến thành phố rome`
  Relevant documents identify the Tiber as the river associated with Rome.
