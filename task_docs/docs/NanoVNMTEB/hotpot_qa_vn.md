# NanoVNMTEB / hotpot_qa_vn

## Overview

`hotpot_qa_vn` is the Vietnamese NanoVNMTEB version of HotpotQA retrieval. HotpotQA was designed for diverse, explainable multi-hop question answering over Wikipedia, with supporting facts that connect bridge entities or compare entities. In this retrieval formulation, each question must retrieve the supporting passages needed for the reasoning chain.

The Nano split contains 200 queries, 10,000 candidate documents, and exactly 400 positive qrels. Every query has exactly two positives. Queries average 99.525 characters, and documents average 445.2743 characters. Dense retrieval is strongest on nDCG@10, while `reranking_hybrid` has the best hit@10 and recall@100. The task is not satisfied by finding one obvious entity page: a successful retriever must recover both supporting documents for a two-hop question.

## Details

### What the Original Data Measures

HotpotQA contains Wikipedia-based questions that require reasoning across multiple documents. The original dataset distinguishes bridge questions, where one entity leads to another, from comparison questions, where two entities must be compared. It also provides supporting facts to make the reasoning path explainable.

The Vietnamese version translates questions and supporting passages while preserving named entities and multi-hop structure. Questions may connect albums, film composers, sports drafts, island kingdoms, dog breeds, or historical states. The retrieval target is the pair of passages needed to answer the question, not merely the page with the highest lexical overlap.

### Observed Data Profile

The task has exactly two positives for every query: average 2.0, median 2.0, minimum 2, maximum 2, and a 100.0% multi-positive rate. This is structurally different from tasks where positives vary by query. Every evaluation instance expects a two-document support set.

The queries are relatively long because they often encode a composed relation. Documents are compact Wikipedia-style passages. A model may find the first hop through exact entity names, but it must also retrieve the second hop, which may share fewer query terms. This makes recall and ranking across both positives central.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.8001155515, hit@10 of 0.9500, and recall@100 of 0.9425 with a top-500 candidate set. These are high scores because named entities and rare titles are strong lexical anchors. The first supporting document is often easy to retrieve when it shares an entity with the question.

BM25's weakness is the second hop. A bridge passage may not repeat many query terms, and a comparison-support passage may be relevant because of a relation rather than lexical overlap. Hit@10 can look strong even when the model retrieves only one of the two required supports, so nDCG and recall are more informative.

### Dense Evaluation Profile

Dense retrieval with `harrier-oss-270m` reaches nDCG@10 of 0.8772754905, hit@10 of 0.9800, and recall@100 of 0.9600. It is strongest on nDCG@10. This suggests that embedding similarity improves ordering of the support passages, especially when one passage is connected through semantic or relational context rather than exact words.

Dense retrieval is well suited to questions where the clue describes a relation instead of naming both answers directly. It can connect a question about a film scored by a composer to the film page and the composer page, or a draft-year relation to both the athlete and the draft context. The remaining risk is retrieving one-hop neighbors that are semantically close but do not complete the reasoning chain.

### Reranking Hybrid Evaluation Profile

`reranking_hybrid` reaches nDCG@10 of 0.8649405263, hit@10 of 0.9950, and recall@100 of 0.9925. The top-100 candidate pool has exactly 100 candidates per query and no safeguard-expanded rows. Hybrid retrieval gives the strongest coverage: it almost always places at least one positive in the top ten and retrieves nearly all positives within the top 100.

The tradeoff is ordering. Dense retrieval has better nDCG@10, while hybrid retrieval has better recall. Sparse evidence helps recover exact named entities and rare titles, but it can also rank the obvious first-hop page above a less lexical second-hop passage. A strong reranker should optimize for both support documents, not only the easiest entity match.

### Metric Interpretation for Model Researchers

This task should be evaluated as paired-support retrieval. Hit@10 is useful but incomplete because a model can hit one support without retrieving the second. Recall@100 directly reflects whether both positives are available for downstream multi-hop QA. nDCG@10 reflects whether support passages are ranked early enough to be usable.

The metric pattern shows that dense retrieval provides better top-order reasoning alignment, while hybrid retrieval provides better coverage. Model researchers should inspect whether errors are first-hop misses, second-hop misses, or ordering failures where the second support is present but too low.

### Query and Relevance Type Tendencies

Queries often ask composed questions: one entity is described through another entity, a person's relative connects to a draft year, a film is identified through a screenwriter and cast, or a historical entity is located through a predecessor state. Relevant documents are the two Wikipedia-style passages that together support the answer.

Relevance is not broad topical similarity. A document about one named entity may be relevant only if it is part of the reasoning chain. Same-topic pages that do not connect the chain are hard negatives.

### Representative Failure Modes

BM25 can find the most lexical entity page and miss the bridge passage. Dense retrieval can retrieve semantically related one-hop neighbors that do not complete the relation. Hybrid retrieval can maximize candidate coverage but still rank first-hop or same-entity distractors above the less obvious second support.

Another failure mode is treating the two positives independently. For downstream QA, both supports matter together. A retriever that consistently finds only one support will have high hit rates but poor multi-hop utility.

### Training Data That May Help

Useful training data includes official HotpotQA training examples with overlap removed, Vietnamese multi-hop QA data, Wikipedia question-to-supporting-page retrieval pairs, and translated multi-hop retrieval data. Training should preserve paired positives and use multi-positive or listwise objectives.

Synthetic data should create linked Vietnamese Wikipedia-style passages and questions that require both passages. Hard negatives should share one entity but fail to provide the second hop, so the model learns to complete the reasoning chain rather than stop at the first match.

### Model Improvement Notes

The main improvement direction is multi-hop-aware retrieval and reranking. Candidate generation should preserve exact named entities for first-hop recall and use dense similarity for bridge relations. Reranking should prefer sets of passages that together satisfy the question.

Error analysis should track whether each query retrieves zero, one, or two positives in the top ranks. Models that score well on ordinary hit metrics may still fail the intended two-hop retrieval behavior if they rarely retrieve both supports.

## Example Data

| Query | Positive document |
| --- | --- |
| Đội bóng rổ nam đại học VCU Rams 2011-12, dẫn dắt bởi huấn luyện viên trưởng năm thứ ba Shaka Smart,... [100 / 178 chars] | Đội bóng rổ nam VCU Rams mùa 2011–12 Đội bóng rổ nam đại học VCU Rams 2011-12 đại diện cho trường Đại học Virginia Commonwealth trong giải bóng rổ NCAA Division I mùa giải 2011-12. Đây là mùa thứ 44 đ... [200 / 856 chars] |
| Con chó mà tổ tiên gồm cả Gordon và Irish Setters là giống chó gì: Manchester Terrier hay Scotch Col... [100 / 104 chars] | Chó Manchester Terrier Chó Manchester Terrier là một giống chó thuộc họ chó săn có lông trơn. [94 chars] |
| Bộ phim nào được viết kịch bản và đạo diễn bởi Joby Harold với nhạc nền của Samuel Sim? [87 chars] | Samuel Sim Samuel Sim là một nhạc sĩ phim và truyền hình. Anh nhận được sự công nhận đầu tiên với điểm số đoạt giải cho bộ phim truyền hình "Dunkirk" của BBC. Từ đó, anh đã viết âm nhạc cho nhiều bộ p... [200 / 554 chars] |
| Năm nào thì anh trai của cầu thủ được đội Washington Redskins chọn ở lượt thứ nhất trong giải tuyển... [100 / 124 chars] | Ba-lê Rodney "Boss" Bailey (sinh ngày 14 tháng 10 năm 1979) là một cựu cầu thủ bóng đá Mỹ từng thi đấu ở vị trí hậu vệ trong giải bóng đá quốc gia NFL. Anh được tuyển chọn bởi đội Detroit Lions trong... [200 / 389 chars] |
| Kịch bản gia có tác phẩm "Evolution" đã cùng viết một bộ phim mà Nicolas Cage và Téa Leoni đóng vai... [100 / 112 chars] | David Weissman David Weissman là một biên kịch và đạo diễn. Các bộ phim của ông bao gồm "The Family Man" (năm 2000), "Evolution" (năm 2001) và ""When in Rome"" (năm 2010). [172 chars] |

### Source Reference Table

| Source | Role |
|---|---|
| HotpotQA | Original explainable multi-hop QA benchmark |
| HotpotQA project page | Official dataset and task context |
| BEIR | Retrieval benchmark framing |
| VN-MTEB | Vietnamese benchmark collection using translated retrieval tasks |
| GreenNode dataset card | Public dataset entry for this Vietnamese split |

### Representative Snippets

- Query: `Đội bóng rổ nam đại học VCU Rams 2011-12... được thành lập vào năm nào?`
  Relevant documents include the season/team passage and the institution or entity needed for the date.
- Query: `Con chó mà tổ tiên gồm cả Gordon và Irish Setters là giống chó gì: Manchester Terrier hay Scotch Collie?`
  Relevant documents support comparison between the named dog breeds and ancestry clue.
- Query: `Bộ phim nào được viết kịch bản và đạo diễn bởi Joby Harold với nhạc nền của Samuel Sim?`
  Relevant documents connect the film creator clue with the composer clue.
- Query: `Năm nào thì anh trai của cầu thủ được đội Washington Redskins chọn ở lượt thứ nhất... mới được tuyển?`
  Relevant documents connect the player, sibling, and draft-year relation.
- Query: `Kịch bản gia có tác phẩm "Evolution" đã cùng viết một bộ phim mà Nicolas Cage và Téa Leoni đóng vai chính là ai?`
  Relevant documents connect the screenwriter clue with the film starring Nicolas Cage and Téa Leoni.
