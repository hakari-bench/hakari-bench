# MNanoBEIR / NanoBEIR-vi / NanoFEVER

## Overview

NanoFEVER in the Vietnamese NanoBEIR slice is a factual claim evidence retrieval task derived from FEVER. The queries are Vietnamese translated claims, and the corpus contains Vietnamese translated Wikipedia-style evidence passages. The retrieval goal is to find passages that can verify the claim, not merely passages that mention the same entity or topic. This compact task is useful for evaluating Vietnamese claim-to-evidence retrieval, entity grounding, and factual relation ranking.

## Details

### What the Original Data Measures

FEVER was created for fact extraction and verification over Wikipedia. In retrieval form, a model receives a factual claim and must retrieve the passage that contains enough evidence to assess it. The relevant passage often discusses a named entity, work, place, event, or category, but the exact factual relation is what determines relevance.

The Vietnamese translated version tests whether a model can handle claims with translated wording and mixed entity forms. Some names and media titles remain close to English, while surrounding context is Vietnamese. A strong retriever must use entity cues without mistaking every same-entity passage for evidence.

### Observed Data Profile

The task contains 50 queries, 4,996 documents, and 57 relevance judgments. Most queries have one positive passage, with an average of 1.14 positives per query. The minimum is 1, the median is 1.0, the maximum is 3, and 6 queries are multi-positive, or 12.0% of the query set. This is mostly a single-evidence retrieval task.

Queries average 53.12 characters, while documents average 1,248.48 characters. The claims are short, while the evidence passages are longer encyclopedia-style text. This makes the benchmark sensitive to whether a retriever can rank the evidence-bearing passage above broader background text.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.6109, hit@10 of 0.7200, and recall@100 of 0.8947 using the top-500 BM25 candidate subset. Entity names and claim wording provide strong lexical anchors, so BM25 often finds the correct evidence by rank 100. However, the top-10 hit rate is much lower than dense retrieval.

The gap indicates that BM25 can locate the right topical area but often ranks same-entity distractors too high. Claims about people, films, or places can share many words with non-evidence passages. Lexical matching is therefore useful for candidate generation but less reliable for final evidence ordering.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.8304, hit@10 of 0.9600, and recall@100 of 0.9474. Dense retrieval is the strongest direct ranking profile on this task. It improves both first-page quality and candidate coverage over BM25, showing that embedding similarity captures claim-evidence semantics beyond surface entity overlap.

This is especially important for FEVER-style claims where the passage must resolve category membership, exclusivity, identity, or factual relation. Dense retrieval is better at distinguishing the passage that verifies the claim from other passages about the same topic. Remaining errors are likely to involve rare entities, mixed-language titles, or fine factual distinctions.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.6964, hit@10 of 0.8600, and recall@100 of 0.9825. It uses a top-100 candidate range with an optional rank-101 safeguard; the observed candidate count ranges from 100 to 101, with 1 safeguard row and a mean of 100.02 candidates. The hybrid profile has the best recall@100, while dense retrieval has the strongest top-rank ordering.

This means hybrid search is a very good evidence candidate pool, but not the best direct first-stage ranker. The lexical component adds coverage for some entity-heavy claims, yet can also elevate same-entity distractors. A downstream reranker should benefit from the high-recall hybrid pool if it can judge the exact claim-passage relation.

### Metric Interpretation for Model Researchers

Because most queries have one positive, nDCG@10 and hit@10 directly measure whether the evidence passage is visible where a verifier or RAG system can use it. recall@100 measures whether a second-stage reranker has access to the answer. In this slice, dense retrieval is best for direct ranking, while reranking_hybrid is best for candidate completeness.

The comparison separates three behaviors: BM25 provides strong entity-based retrieval, dense retrieval provides evidence-sensitive ordering, and hybrid search broadens recall. This task is useful for checking whether improvements come from factual ranking rather than simply retrieving same-topic passages.

### Query and Relevance Type Tendencies

Queries include claims such as Keith Godchaux knowing Grateful Dead, whether Taarak Mehta Ka Ooltah Chashmah is a comedy, whether advanced aircraft were produced in Burbank, whether Nero was a person, and whether Scream 2 is exclusively German. Relevant documents are Wikipedia-style passages that resolve those claims.

The task rewards precise entity grounding and factual relation matching. Category, identity, location, and exclusivity claims are common sources of subtle retrieval errors. A passage can mention the right entity but still fail to verify the claim.

### Representative Failure Modes

Likely failures include retrieving a correct entity but wrong fact, confusing similar titles or people, over-ranking broad background pages, and missing evidence because translated wording differs from the claim. BM25 may overvalue repeated names, while dense retrieval may still struggle with rare mixed-script entities.

### Training Data That May Help

Useful training data includes Vietnamese claim-evidence retrieval, Wikipedia evidence mining, multilingual fact-checking, and hard negatives that share entities but do not verify the claim. For rerankers, same-entity non-evidence passages are especially valuable because they match the task's main ambiguity.

### Model Improvement Notes

A model targeting this task should preserve entity recall while improving evidence-relation ranking. Sparse systems need exact entity and title handling. Dense systems are the strongest direct baseline and can be improved with claim-specific hard negatives. Hybrid systems should exploit their high recall with an evidence-aware reranker.

## Example Data

| Query | Positive document |
| --- | --- |
| Keith Godchaux biết đến Grateful Dead. [38 chars] | Grateful Dead là một ban nhạc rock của Mỹ được thành lập vào năm 1965 tại Palo Alto, California. Với đội hình từ quintet đến septet, ban nhạc nổi tiếng với phong cách độc đáo và đa dạng, kết hợp các yếu tố của rock, psychedelia, nhạc experimental, jazz modal, country, folk, bluegrass, blues, reggae và space rock, cho các buổi biểu diễn trực tiếp với những đoạn nhạc dài, và với lượng fan hâm mộ trung thành, được biết đến với tên gọi "Deadheads". "Âm nhạc của họ," viết Lenny Kaye, "chạm đến những vùng đất mà hầu hết các nhóm khác thậm chí không biết tồn tại." Những ảnh hưởng đa dạng này đã được chưng cất thành một tổng thể đa dạng và psychedelic khiến Grateful Dead trở thành "những người sáng lập tiên phong của thế giới jam band". Ban nhạc được xếp hạng 57 bởi tạp chí Rolling Stone trong số The Greatest Artists of All Time. Ban nhạc đã được đưa vào Rock and Roll Hall of Fame vào năm 1994 và một bản ghi âm buổi biểu diễn của họ vào ngày 8 tháng 5 năm 1977 tại Barton Hall của Đại học Corne... [1,000 / 3,093 chars] |
| Taarak Mehta Ka Ooltah Chashmah phim hài? [41 chars] | Taarak Mehta Ka Ooltah Chashmah (tiếng Anh: Góc Nhìn Khác Của Taarak Mehta) là bộ phim hài dài nhất Ấn Độ do Neela Tele Films Private Limited sản xuất. Chương trình bắt đầu phát sóng vào ngày 28 tháng 7 năm 2008. Nó được phát sóng từ thứ Hai đến thứ Sáu lúc 8:30 tối, với buổi phát lại vào lúc 11:00 tối và ngày hôm sau lúc 3:00 chiều trên kênh SAB TV. Chương trình bắt đầu phát lại trên Sony Pal từ ngày 2 tháng 11 năm 2015 vào lúc 4:30 chiều và 8:00 tối hàng ngày. Chương trình dựa trên chuyên mục Duniya Ne Oondha Chashma do nhà báo và nhà văn Taarak Mehta viết cho tạp chí hàng tuần Gujarati Chitralekha. [608 chars] |
| Có phải những chiếc máy bay bí mật và công nghệ tiên tiến đã được sản xuất ở Burbank, California không? [103 chars] | Burbank là một thành phố thuộc quận Los Angeles ở miền Nam California, Hoa Kỳ, cách trung tâm Los Angeles 12 dặm về phía tây bắc. Dân số theo điều tra năm 2010 là 103,340. Được mệnh danh là "Thủ đô truyền thông của thế giới" và chỉ cách Hollywood vài dặm về phía đông bắc, nhiều công ty truyền thông và giải trí có trụ sở hoặc có cơ sở sản xuất quan trọng tại Burbank, bao gồm The Walt Disney Company, Warner Bros. Entertainment, Nickelodeon Animation Studios, NBC, Cartoon Network Studios với chi nhánh Bờ Tây của Cartoon Network, và Insomniac Games. Thành phố cũng là nơi có Sân bay Bob Hope. Đây là địa điểm của Lockheed 's Skunk Works, nơi sản xuất một số máy bay bí mật và tiên tiến về công nghệ nhất, bao gồm cả máy bay do thám U-2 đã phát hiện các thành phần tên lửa của Liên Xô ở Cuba vào tháng 10 năm 1962. Burbank bao gồm hai khu vực khác biệt: một khu vực trung tâm/thung lũng, nằm ở chân đồi của dãy núi Verdugo, và khu vực đồng bằng. Burbank là thành phố nằm ở phía đông nhất trong thung... [1,000 / 1,401 chars] |

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original dataset | [FEVER](https://arxiv.org/abs/1803.05355) |
| Retrieval benchmark framing | [BEIR](https://arxiv.org/abs/2104.08663) |
| Multilingual benchmark context | [MMTEB](https://arxiv.org/abs/2502.13595) |
| NanoBEIR collection | [NanoBEIR on Hugging Face](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
| NanoBEIR-vi dataset | [hakari-bench/NanoBEIR-vi](https://huggingface.co/datasets/hakari-bench/NanoBEIR-vi) |

Representative query and positive evidence snippets:

| Query | Positive document snippet |
| --- | --- |
| Keith Godchaux biết đến Grateful Dead. | Grateful Dead là một ban nhạc rock của Mỹ được thành lập vào năm 1965 tại Palo Alto... |
| Taarak Mehta Ka Ooltah Chashmah phim hài? | Taarak Mehta Ka Ooltah Chashmah là bộ phim hài dài nhất Ấn Độ... |
| Có phải những chiếc máy bay bí mật và công nghệ tiên tiến đã được sản xuất ở Burbank, California không? | Burbank là một thành phố thuộc quận Los Angeles ở miền Nam California... |
| Nero có phải là một người không? | Thuật ngữ triều đại Julio-Claudian đề cập đến năm hoàng đế La Mã đầu tiên... |
| Scream 2 là một bộ phim độc quyền của Đức. | Scream 2 là một bộ phim kinh dị slasher của Mỹ ra mắt năm 1997... |
