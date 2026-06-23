# MNanoBEIR / NanoBEIR-vi / NanoHotpotQA

## Overview

NanoHotpotQA in the Vietnamese NanoBEIR slice is a multi-hop Wikipedia passage retrieval task derived from HotpotQA. The queries are Vietnamese translated questions, and each query normally requires evidence from two supporting passages. The retrieval goal is not only to find a page about the right entity, but to recover the passages that jointly support the answer. This makes the task useful for evaluating Vietnamese multi-hop retrieval, bridge-entity reasoning, and candidate coverage for downstream question answering.

## Details

### What the Original Data Measures

HotpotQA was designed for diverse, explainable multi-hop question answering over Wikipedia. In the retrieval setting, the model must find supporting passages that contain the evidence chain needed to answer the question. Many questions mention one entity and require following a relation to another entity, work, place, event, or person.

The Vietnamese translated version keeps this multi-hop structure while adding multilingual retrieval challenges. Entity names, film titles, organization names, and historical names may remain close to English or their original script, while the surrounding question and passage text is Vietnamese. A strong retriever must combine lexical entity recognition with semantic bridge matching.

### Observed Data Profile

The task contains 50 queries, 5,090 documents, and 100 relevance judgments. Every query has exactly 2 positive passages, so the average, minimum, median, and maximum positives per query are all 2.0, 2, 2.0, and 2. All 50 queries are multi-positive, or 100.0% of the set.

Queries average 90.66 characters, while documents average 374.15 characters. Compared with many BEIR-style QA tasks, the queries are relatively long because they often encode the bridge relation directly. The documents are short enough that passage-level evidence is fairly focused, but retrieving both positives remains the central difficulty.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.6311, hit@10 of 0.8800, and recall@100 of 0.8200 using the top-500 BM25 candidate subset. This is a strong lexical baseline. Multi-hop questions often include distinctive entity names, dates, locations, or titles, and those terms give BM25 enough signal to retrieve many supporting passages.

The weakness is coverage and ordering across the two-positive requirement. BM25 can find one passage about a named entity but miss the second bridge passage, or rank another same-entity passage above the needed support. The recall@100 value shows that lexical matching is useful but does not fully cover the evidence set for reranking.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.7552, hit@10 of 0.9400, and recall@100 of 0.9000. Dense retrieval is the strongest direct top-rank profile on this task. It improves both nDCG@10 and recall@100 over BM25, indicating that embedding similarity helps recover passages connected by the question's relation rather than by term overlap alone.

This behavior is important for HotpotQA-style retrieval. A model must understand that a question about an actor, work, event, or institution may require a passage whose most important evidence is expressed through a relation, not through repeated query terms. Dense retrieval appears better suited to that semantic bridge.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.7089, hit@10 of 0.9400, and recall@100 of 0.9600. It uses 100 candidates per query, with no rank-101 safeguard rows in this slice. The hybrid profile matches dense hit@10 and exceeds both BM25 and dense retrieval on recall@100.

This means the hybrid candidate pool is especially useful for downstream reranking. It combines BM25's exact entity capture with dense retrieval's semantic bridge coverage. Dense retrieval remains better for direct first-stage ordering, but reranking_hybrid is the better source when the priority is to make both supporting passages available to a stronger second-stage model.

### Metric Interpretation for Model Researchers

Because every query has two positives, nDCG@10 is sensitive to whether both supporting passages appear near the top, not only whether the first answer-bearing passage is found. hit@10 can be high even if only one of the two positives is visible, while recall@100 is a better diagnostic for whether a reranker can complete the evidence chain.

The comparison shows a clear pattern: BM25 is already strong because the questions contain useful surface anchors, dense retrieval improves semantic ordering, and reranking_hybrid gives the highest candidate coverage. This task is therefore good for separating direct ranking quality from candidate-pool completeness.

### Query and Relevance Type Tendencies

Queries ask multi-hop questions such as which actor appeared in a television comedy with Penny Rae Bridges, who gave Kaganoi Shigemochi a sword made by the founder of the Muramasa school, which film was written and directed by Joby Harold with music by Samuel Sim, and what date a specific college football game occurred. Relevant documents are short encyclopedia-style passages that supply one side of the evidence chain.

The task rewards bridge-entity tracking, relation matching, and complete evidence retrieval. A passage can mention the main entity yet fail to supply the relation needed for the answer. Models that retrieve only one obvious entity page may score worse than models that retrieve a broader but well-ranked evidence set.

### Representative Failure Modes

Likely failures include retrieving only one of the two supporting passages, over-ranking a page about a mentioned entity that lacks the bridge fact, confusing works with similar titles, and missing evidence when translated wording differs from the source phrase. BM25 may be too dependent on names and surface terms, while dense retrieval can sometimes retrieve semantically related but incomplete background passages.

### Training Data That May Help

Useful training data includes Vietnamese multi-hop QA retrieval, translated Wikipedia evidence chains, bridge-question generation, and hard negatives that share one entity but omit the second supporting relation. Multi-positive supervision is especially important because the task requires recovering two passages per query.

### Model Improvement Notes

A model targeting this task should optimize for both first-page quality and multi-positive recall. Sparse systems need strong entity and title normalization. Dense systems need relation-aware question-passage training. Hybrid systems are promising as reranking inputs because their recall@100 profile gives a second-stage model more complete evidence chains to judge.

## Example Data

| Query | Positive document |
| --- | --- |
| Penny Rae Bridges đã đóng vai trong một bộ phim hài truyền hình cùng với diễn viên nào khác? [92 chars] | Penny Rae Bridges (sinh ngày 29 tháng 7 năm 1990) là một nữ diễn viên người Mỹ. Công việc truyền hình của cô đã bao gồm các vai diễn trong "For Your Love", "Family Law", "Boy Meets World" và "The Parent 'Hood". Cô được biết đến nhiều nhất với vai diễn trong "Half & Half", trong vai Mona trẻ. [292 chars] |
| Ai đã tặng Kaganoi Shigemochi một thanh kiếm được làm bởi người sáng lập trường Muramasa? [89 chars] | Kaganoi Shigemochi (加賀井 重望, 1561 – 27 tháng 8, 1600) là một samurai Nhật Bản của thời kỳ Azuchi-Momoyama, phục vụ cho gia tộc Oda. Ông cai trị lâu đài Kaganoi. Trong trận chiến Komaki và Nagakute, Shigemochi chiến đấu dưới sự chỉ huy của cha mình là Shigemune, người đã tham gia vào lực lượng của Oda Nobukatsu. Ngay sau đó, lâu đài Kaganoi bị bao vây bởi lực lượng của Toyotomi Hideyoshi; Shigemune đã đầu hàng, và Shigemochi được Hideyoshi tuyển dụng làm sứ giả, nhận một khoản trợ cấp 10.000 "koku". Ông cũng sở hữu một thanh kiếm được chế tác bởi Muramasa, mà Hideyoshi đã ban tặng cho ông vào năm 1598. [607 chars] |
| Bộ phim nào được viết và đạo diễn bởi Joby Harold với nhạc được viết bởi Samuel Sim? [84 chars] | Samuel Sim là một nhạc sĩ phim và truyền hình. Ông lần đầu tiên được công nhận với bản nhạc đoạt giải cho loạt phim truyền hình của BBC "Dunkirk". Kể từ đó, ông đã sáng tác nhạc cho nhiều sản phẩm phim và truyền hình khác nhau, gần đây nhất là nhạc cho bộ phim "Awake" của The Weinstein Company và loạt phim truyền hình BBC/HBO "House of Saddam". Bản nhạc được đánh giá cao gần đây nhất của ông là nhạc phim cho Home Fires. Home Fires (Nhạc từ loạt phim truyền hình) được phát hành vào ngày 6 tháng 5 năm 2016 bởi Sony Classical Records. [537 chars] |

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original dataset | [HotpotQA](https://arxiv.org/abs/1809.09600) |
| Retrieval benchmark framing | [BEIR](https://arxiv.org/abs/2104.08663) |
| Multilingual benchmark context | [MMTEB](https://arxiv.org/abs/2502.13595) |
| NanoBEIR collection | [NanoBEIR on Hugging Face](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
| NanoBEIR-vi dataset | [hakari-bench/NanoBEIR-vi](https://huggingface.co/datasets/hakari-bench/NanoBEIR-vi) |

Representative query and positive evidence snippets:

| Query | Positive document snippet |
| --- | --- |
| Penny Rae Bridges da dong vai trong mot bo phim hai truyen hinh cung voi dien vien nao khac? | Penny Rae Bridges la mot nu dien vien nguoi My... |
| Ai da tang Kaganoi Shigemochi mot thanh kiem duoc lam boi nguoi sang lap truong Muramasa? | Kaganoi Shigemochi la mot samurai Nhat Ban cua thoi ky Azuchi-Momoyama... |
| Bo phim nao duoc viet va dao dien boi Joby Harold voi nhac duoc viet boi Samuel Sim? | Samuel Sim la mot nhac si phim va truyen hinh... |
| Ngay dien ra tran dau bong da dai hoc nay tai San van dong Sun Life o Miami Gardens, Florida la gi? | Doi bong da Clemson Tigers nam 2015 dai dien cho Dai hoc Clemson... |
| Devil's Food la mot album tong hop cac bai hat don cua mot ban nhac rock and roll nguoi My, cung duoc biet den voi viec bieu dien cac chuong trinh nhac dong que duoi cai gi? | Devil's Food la mot album tong hop cac bai hat don cua ban nhac rock and roll My Supersuckers... |
