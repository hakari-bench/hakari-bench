# NanoVNMTEB / quora_vn

## Overview

`quora_vn` is the Vietnamese NanoVNMTEB version of the Quora duplicate-question retrieval task. The source data comes from the Quora Question Pairs release as used in BEIR, where relevance means that two questions ask the same underlying thing. VN-MTEB translates and filters the task into Vietnamese, producing a translated duplicate-question retrieval benchmark rather than native Vietnamese Quora data.

The Nano split contains 200 queries, 10,000 candidate documents, and 452 positive qrels. Queries average 76.51 characters, while documents average 129.2151 characters. The task is short-text paraphrase retrieval: both sides are questions, and the model must find duplicate formulations, including noisy translated variants. `reranking_hybrid` is strongest overall, BM25 is close, and dense retrieval is slightly weaker. This indicates that exact word and entity overlap are highly useful, but hybrid retrieval adds coverage and ranking stability.

## Details

### What the Original Data Measures

The Quora Question Pairs dataset was released to support duplicate-question detection. BEIR turns it into a retrieval task by treating one question as a query and candidate questions as documents, with duplicates as positives. Unlike answer retrieval, the target document is not an answer passage; it is another question with equivalent intent.

The Vietnamese version translates the questions. Some examples retain translation-helper wording or extra fragments, so the model must identify the underlying question inside noisy text. Relevance depends on semantic duplication, not broad topic similarity. A question about whether Trump could win an election is relevant to a paraphrase of that same question, but not to every question about Trump.

### Observed Data Profile

The task has 452 positives across 200 queries. The average is 2.26 positives per query, the median is 1, and 67 queries have multiple positives. The maximum positive cluster has 57 documents, so most queries are narrow duplicate searches, while some have large paraphrase clusters.

Documents are short compared with passage tasks. This makes exact wording and small semantic differences important. Many duplicates share key entities or phrases, but some are paraphrased or wrapped in translation artifacts. A good retriever must handle both clean paraphrase and noisy duplicated intent.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.8345337070, hit@10 of 0.9600, and recall@100 of 0.9402654867 with a top-500 candidate set. These high scores show that lexical overlap is very strong for this task. Short duplicate questions often repeat entities, dates, product names, and core predicates.

BM25 can still fail when the duplicate is a true paraphrase with different wording or when the question is embedded inside extra translation text. It can also over-rank same-keyword non-duplicates: questions can share a named entity while asking different relations or opinions. The high baseline means improvements must be judged by ranking quality and recall, not just first-hit success.

### Dense Evaluation Profile

Dense retrieval with `harrier-oss-270m` reaches nDCG@10 of 0.8259395743, hit@10 of 0.9350, and recall@100 of 0.9048672566. It is close to BM25 but slightly weaker across the reported metrics. This suggests that for translated Quora duplicates, exact tokens and entity overlap are unusually valuable.

Dense retrieval remains useful for paraphrases, but it can over-generalize across questions with similar topics and different intent. Short questions leave little context, so embedding similarity may group related political, technology, or advice questions that are not duplicates. The task needs semantic matching, but not at the cost of exact intent distinctions.

### Reranking Hybrid Evaluation Profile

`reranking_hybrid` is strongest: nDCG@10 is 0.8510204725, hit@10 is 0.9600, and recall@100 is 0.9623893805. The top-100 candidate pool has exactly 100 candidates per query and no safeguard-expanded rows. Hybrid retrieval keeps BM25's first-hit strength while improving recall and nDCG.

The improvement reflects complementary evidence. Sparse retrieval preserves shared words and entities, while dense retrieval can rescue paraphrased duplicates or noisy translated variants. Because documents are short, a small amount of wrong semantic smoothing can hurt; hybrid retrieval works best when exact overlap and semantic equivalence agree.

### Metric Interpretation for Model Researchers

This task is already high-performing, so the key differences are subtle. BM25's strength shows that duplicate questions often share surface forms. Dense underperforming BM25 suggests that generic semantic similarity is not enough; it must preserve question intent and entity constraints.

The multi-positive rate of 33.5% means recall@100 matters for duplicate clusters, but the median positive count of 1 keeps nDCG@10 important. Researchers should evaluate whether models retrieve several paraphrases when they exist while avoiding same-topic non-duplicates.

### Query and Relevance Type Tendencies

Queries include everyday advice, politics, product-release timing, films, social media problems, weight loss, nightmares, and factual or opinion questions. Relevant documents are alternate phrasings of the same question. Some positives include noisy translated prompts such as requests to translate a sentence, with the actual duplicate embedded inside.

Relevance is intent equivalence. Same entity is not enough, and same broad topic is not enough. The question must ask the same thing from the user's perspective.

### Representative Failure Modes

BM25 can miss paraphrases that share few words. Dense retrieval can retrieve semantically related but non-duplicate questions. Hybrid retrieval can still fail when translation noise changes the apparent intent or when a question contains extra irrelevant text before the true duplicate.

Another failure mode is entity drift. Two questions mentioning Donald Trump, Xiaomi Redmi, or Facebook may ask different relations, judgments, or troubleshooting needs. Models must preserve the full predicate, not only the entity.

### Training Data That May Help

Useful training data includes non-overlapping Quora duplicate-question pairs, Vietnamese duplicate-question and paraphrase data, translated duplicate pairs with overlap removed, and same-entity hard negatives with different intent. Multi-positive training is useful because some queries have many duplicates.

Synthetic data can generate Vietnamese paraphrases and noisy translated variants. Hard negatives should share keywords or named entities while changing the question relation, opinion, or requested action.

### Model Improvement Notes

The main improvement direction is intent-preserving duplicate retrieval. Sparse matching should preserve entities and core words; dense matching should capture paraphrase. Reranking should compare full question meaning and reject same-topic but different-intent candidates.

Error analysis should group false positives by same-entity drift, same-topic drift, translation-wrapper noise, and paraphrase failure. Because BM25 is strong, dense improvements need carefully mined hard negatives rather than broad paraphrase training alone.

## Example Data

| Query | Positive document |
| --- | --- |
| Xiaomi Redmi note 4 ra mắt ở Ấn Độ vào ngày nào? [48 chars] | Hãy chuyển câu này sang tiếng Việt: Khi nào Xiaomi Redmi note 4 sẽ ra mắt ở Ấn Độ? [83 chars] |
| Có khả năng Trump sẽ thắng cuộc bầu cử không? [45 chars] | Nếu bạn muốn dịch câu này sang tiếng Việt, hãy viết câu đó ở dưới này. Trump có cơ hội thắng cử không? [103 chars] |
| Có nên thực hiện một phim truyền hình dựa trên bộ phim Shiva Trilogy? [69 chars] | Chào các bạn, Nếu bộ ba Shiva được chuyển thể thành một series phim truyền hình thì nó sẽ như thế nào? [103 chars] |

### Source Reference Table

| Source | Role |
|---|---|
| Quora Question Pairs release | Original duplicate-question data release |
| BEIR | Retrieval benchmark framing for Quora |
| VN-MTEB | Vietnamese benchmark collection using translated retrieval tasks |
| GreenNode dataset card | Public dataset entry for this Vietnamese split |

### Representative Snippets

- Query: `Xiaomi Redmi note 4 ra mắt ở Ấn Độ vào ngày nào?`
  Relevant documents ask the same product-release timing question in another wording.
- Query: `Có khả năng Trump sẽ thắng cuộc bầu cử không?`
  Relevant documents ask whether Trump has a chance to win the election.
- Query: `Có nên thực hiện một phim truyền hình dựa trên bộ phim Shiva Trilogy?`
  Relevant documents ask about adapting the Shiva Trilogy into a TV series.
- Query: `Donald Trump bị một số phương tiện truyền thông gọi là "điên"...`
  Relevant documents ask about Trump's mental stability or related judgment.
- Query: `Trang Facebook của bạn trai tôi đã bị hack...`
  Relevant documents contain duplicate troubleshooting questions about account recovery.
