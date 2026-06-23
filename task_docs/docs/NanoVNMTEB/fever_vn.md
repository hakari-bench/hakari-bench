# NanoVNMTEB / fever_vn

## Overview

`fever_vn` is the Vietnamese NanoVNMTEB version of FEVER evidence retrieval. FEVER was introduced as a large-scale fact extraction and verification dataset in which claims are verified against Wikipedia evidence. In the BEIR-style retrieval formulation used here, the claim is the query and Wikipedia-style evidence passages are the documents. VN-MTEB translates the retrieval task into Vietnamese.

The Nano split contains 200 queries, 10,000 candidate documents, and 232 positive qrels. Queries average 56.03 characters, and documents average 392.3979 characters. Most queries have one relevant evidence passage, with an average of 1.16 positives per query. Dense retrieval is strongest on nDCG@10, while `reranking_hybrid` has the highest hit@10 and recall@100. The task is a high-performing entity-and-relation retrieval benchmark: many claims contain strong entity anchors, but top-rank quality depends on finding the evidence passage that actually supports or refutes the relation.

## Details

### What the Original Data Measures

FEVER asks systems to verify textual claims using evidence from Wikipedia. The original task includes supported, refuted, and not-enough-information labels, and supported or refuted claims require evidence sentences. In retrieval-only form, the label decision is not the main task; the retriever must find passages that contain enough information for verification.

The Vietnamese version translates factual claims and evidence passages. Claims may mention people, films, historical events, occupations, sports teams, music releases, or fictional works. Relevant documents usually contain the named entity plus enough relational context to verify the claim. The model must preserve entities, dates, roles, and relations across translation.

### Observed Data Profile

The task has 232 positives across 200 queries. The average is 1.16 positives per query, the median is 1, and only 29 queries have multiple positives. The maximum positive count is 3. This is mostly a single-evidence retrieval task, unlike DBpedia-style list retrieval.

Documents are compact Wikipedia-style passages. The query is a factual claim, often short and declarative. A strong retriever must identify which entity page contains the evidence and rank it early. Because positives are sparse, nDCG@10 is a strict measure of whether the correct evidence appears at the very top.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.8013465591, hit@10 of 0.8950, and recall@100 of 0.9612068966 with a top-500 candidate set. These are high scores because many FEVER claims contain exact entity names, titles, dates, or occupations that also appear in the evidence passage.

BM25's recall@100 is slightly higher than dense retrieval, showing that exact entity matching is a powerful candidate-generation signal. Its lower nDCG@10 and hit@10 show that lexical overlap alone does not always rank the best evidence first. Same-entity distractors can mention the claim subject without proving the target relation.

### Dense Evaluation Profile

Dense retrieval with `harrier-oss-270m` reaches nDCG@10 of 0.9519864530, hit@10 of 0.9650, and recall@100 of 0.9568965517. It is strongest on nDCG@10, indicating excellent top-rank ordering for this translated FEVER split. Dense retrieval appears to capture both entity identity and relation-level semantic similarity.

This is valuable because evidence retrieval is not just entity lookup. A claim about a film's setting, a person's occupation, an actor's sitcom roles, or a song's release context may require matching a specific relation. Dense retrieval can rank the passage that states the relation above other same-entity or same-topic pages. Its slight recall@100 deficit relative to BM25 suggests that exact entity preservation remains useful for candidate coverage.

### Reranking Hybrid Evaluation Profile

`reranking_hybrid` reaches nDCG@10 of 0.8903686066, hit@10 of 0.9750, and recall@100 of 0.9956896552. The top-100 candidate pool has exactly 100 candidates per query and no safeguard-expanded rows. Hybrid retrieval gives the best hit@10 and nearly complete recall@100, but it does not match dense retrieval's nDCG@10.

The result shows a common evidence-retrieval tradeoff. Combining sparse and dense signals finds almost every positive somewhere in the candidate pool and increases the chance that at least one positive appears in the top ten. However, the final ordering can be less precise than dense retrieval alone, likely because lexical same-entity candidates compete with the relation-bearing passage.

### Metric Interpretation for Model Researchers

This task has high absolute scores, so small differences are meaningful. Dense retrieval's nDCG@10 advantage shows superior evidence ordering. Hybrid retrieval's recall@100 advantage shows superior candidate coverage. BM25 remains strong because entity names and titles are highly informative.

Because most queries have a single positive, nDCG@10 is especially important. A model cannot rely on retrieving one of many acceptable documents; it must rank the evidence passage near the top. Researchers should inspect whether errors are entity misses, relation misses, or cases where the model retrieves a related page that lacks the verifying evidence.

### Query and Relevance Type Tendencies

Queries are factual claims such as a film being set in an alternate history, a public figure being a model, an actor appearing in sitcoms, a historical person being the subject of some claim, or a basketball player being associated with a professional team. Relevant documents are Wikipedia-style passages that contain enough context to support or refute the claim.

The relevance relation is evidence sufficiency. A passage about the same entity is not necessarily relevant unless it contains the needed fact. This separates FEVER retrieval from ordinary entity search and makes relation matching central.

### Representative Failure Modes

BM25 can retrieve same-entity passages that do not contain the target relation. Dense retrieval can retrieve semantically similar claims or neighboring entities when names or dates are ambiguous. Hybrid retrieval can maximize recall but still rank relation-insufficient pages above the precise evidence.

Another failure mode is translation-sensitive entity handling. Names, titles, and occupations may appear in slightly different forms. A retriever needs robust entity matching without losing relation-level precision.

### Training Data That May Help

Useful training data includes official FEVER training claims and evidence with overlap removed, Vietnamese claim-evidence retrieval pairs, Wikipedia entity evidence pairs, and translated FEVER-style data. Training should keep retrieval separate from final label prediction: the model must learn to find evidence, not memorize verdicts.

Synthetic data can generate Vietnamese factual claims from non-evaluation Wikipedia-style passages. Strong examples should include same-entity hard negatives that omit or contradict the target relation, as well as date, role, and title variations.

### Model Improvement Notes

The main improvement direction is relation-aware evidence ranking. Sparse retrieval should preserve exact names and titles for coverage, while dense retrieval should rank passages that express the claim relation. A reranker should compare whether the document actually contains the evidence needed for support or refutation.

Error analysis should separate entity retrieval failures from evidence sufficiency failures. If positives are absent from candidates, improve sparse entity recall and alias handling. If positives are present but ranked lower, improve relation-aware reranking with same-entity hard negatives.

## Example Data

| Query | Positive document |
| --- | --- |
| Watchmen là một bộ phim được đặt trong bối cảnh lịch sử thay thế vào năm 1985. [78 chars] | Watchmen (phim) Watchmen là một bộ phim siêu anh hùng Mỹ năm 2009 do Zack Snyder đạo diễn, dựa trên loạt truyện tranh cùng tên của DC Comics ra mắt năm 1986-87 của Alan Moore và Dave Gibbons. Phim có sự tham gia của dàn diễn viên Malin Åkerman, Billy Crudup, Matthew Goode, Carla Gugino, Jackie Earle Haley, Jeffrey Dean Morgan và Patrick Wilson. Đây là một tác phẩm châm biếm đen tối về thể loại phim siêu anh hùng với bối cảnh lịch sử thay thế trong thời Chiến tranh Lạnh vào năm 1985 giữa Hoa Kỳ và Liên Xô khi nhóm siêu anh hùng đã giải nghệ điều tra vụ giết người đồng đội trước khi phát hiện âm mưu phức tạp chết chóc; đồng thời những hạn chế về đạo đức bị thách thức bởi tính chất phức tạp của hoàn cảnh. Từ tháng 10/1987 đến tháng 10/2005 dự án chuyển thể phim hành động sống từ loạt truyện Watchmen bị vướng mắc trong địa ngục phát triển; nhà sản xuất Lawrence Gordon khởi đầu dự án tại hãng phim 20th Century Fox và Warner Bros., công ty mẹ của nhà xuất bản truyện tranh DC - nơi ra đời Wat... [1,000 / 2,181 chars] |
| Jenny McCarthy là một người mẫu. [32 chars] | Jenny McCarthy Jennifer Ann McCarthy ( sinh ngày 1 tháng 11 năm 1972), được biết đến với tên Jenny McCarthy và Jenny Wahlberg, là một nữ diễn viên, người mẫu, người dẫn chương trình truyền hình, tác giả kịch bản điện ảnh và nhà vận động chống tiêm chủng. Cô bắt đầu sự nghiệp của mình vào năm 1993 khi làm người mẫu khỏa thân cho tạp chí Playboy và sau đó trở thành Playmate của năm theo bình chọn của tạp chí này. Sau đó cô sử dụng danh tiếng từ những bức hình trên Playboy để phát triển sự nghiệp diễn xuất trong lĩnh vực truyền hình cũng như điện ảnh bằng việc tham gia đồng dẫn chương trình Singled Out của đài MTV trước khi tham gia các bộ phim hài tự đề cử cùng tên với cô như BASEketball, Diamonds hay Scream 3 cùng với Santa Baby. Cô từng là đồng MC cho chương trình The View thuộc đài ABC. McCarthy đã viết sách về cách nuôi dạy con cái và trở thành một nhà vận động thúc đẩy nghiên cứu về các vấn đề môi trường cũng như điều trị y học thay thế cho bệnh tự kỷ. Cô tuyên bố rằng vắc-xin gây r... [1,000 / 1,368 chars] |
| James Brolin đã từng đóng vai trong những vở kịch hài tình huống. [65 chars] | James Brolin James Brolin ( - LSB- broʊlᵻn - RSB- sinh ngày 18 tháng Bảy năm 1940 ) là một diễn viên , nhà sản xuất và đạo diễn người Mỹ, được biết đến với những vai diễn phim và truyền hình , bao gồm sitcom cũng như opera xà phòng . Anh là cha của nam diễn viên Josh Brolin và chồng của ca sĩ/diễn viên Barbra Streisand. Trong số các giải thưởng khác, ông đã giành hai Quả cầu vàng cùng với một giải Emmy. Ông nhận được ngôi sao trên Đại lộ Danh vọng Hollywood vào ngày 27 tháng Tám năm 1998. [494 chars] |

### Source Reference Table

| Source | Role |
|---|---|
| FEVER | Original fact extraction and verification dataset |
| FEVER project page | Official dataset and task context |
| BEIR | Retrieval benchmark framing |
| VN-MTEB | Vietnamese benchmark collection using translated retrieval tasks |
| GreenNode dataset card | Public dataset entry for this Vietnamese split |

### Representative Snippets

- Query: `Watchmen là một bộ phim được đặt trong bối cảnh lịch sử thay thế vào năm 1985.`
  Relevant documents describe the film and its alternate-history setting.
- Query: `Jenny McCarthy là một người mẫu.`
  Relevant documents contain the person's biography and occupation.
- Query: `James Brolin đã từng đóng vai trong những vở kịch hài tình huống.`
  Relevant documents describe the actor's television roles.
- Query: `Joseph Merrick đã là chủ đề của hàng ngàn những dòng tweet hận thù.`
  Relevant documents concern Joseph Merrick and provide evidence context for the claim.
- Query: `Chris Mullin chơi bóng rổ cho một đội bóng chuyên nghiệp.`
  Relevant documents include professional basketball team or career evidence.
