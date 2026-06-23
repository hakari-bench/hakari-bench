# NanoVNMTEB / nano_fever

## Overview

`nano_fever` is the Vietnamese NanoVNMTEB version of the NanoFEVER evidence-retrieval split. It uses the FEVER fact-verification task family, where factual claims must be checked against Wikipedia evidence. In this retrieval setting, the query is a translated claim and the documents are translated Wikipedia-style evidence passages; the model is evaluated on retrieving evidence before any verification label is predicted.

The Nano split contains 200 queries, 10,000 candidate documents, and 232 positive qrels. Queries average 56.03 characters, and documents average 462.2504 characters. Most queries have a single positive, with an average of 1.16 positives per query. Dense retrieval is strongest on nDCG@10 and hit@10, while `reranking_hybrid` is strongest on recall@100. The task is a high-accuracy entity-and-relation retrieval benchmark where exact entity names help, but top-rank quality depends on evidence sufficiency.

## Details

### What the Original Data Measures

FEVER was introduced as a large-scale dataset for fact extraction and verification. Claims are generated from Wikipedia and labeled as supported, refuted, or not enough information. For supported and refuted claims, systems must retrieve evidence sentences from Wikipedia. BEIR casts the task as retrieval, with claims as queries and evidence passages as documents.

The Vietnamese NanoFEVER variant translates claims and evidence passages. The examples include people, films, medical conditions, software, nationalities, dates, roles, and works. A relevant passage must contain the information needed to verify the claim, not just mention the same entity.

### Observed Data Profile

The task has 232 positives across 200 queries. The average is 1.16 positives per query, the median is 1, and 29 queries have multiple positives. The maximum positive count is 3. This means most queries depend on one primary evidence passage.

Documents are Wikipedia-style entity passages and are slightly longer on average than the separate `fever_vn` split. Many passages begin with an entity title and then provide biographical, historical, or descriptive facts. The retrieval challenge is to select the passage that contains the specific evidence relation.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.7966815672, hit@10 of 0.9050, and recall@100 of 0.9439655172 with a top-500 candidate set. Entity names and titles make sparse retrieval strong. Claims about named people, works, or organizations often share exact words with the evidence page.

BM25's weakness is ranking the relation-bearing evidence above same-entity distractors. A claim may require a profession, date, work, location, or descriptive relation. A passage that only mentions the entity is not enough. BM25 provides good candidate coverage but does not match dense retrieval's top-order precision.

### Dense Evaluation Profile

Dense retrieval with `harrier-oss-270m` reaches nDCG@10 of 0.9409427247, hit@10 of 0.9650, and recall@100 of 0.9568965517. It is the strongest condition for top-rank quality. Dense retrieval appears to capture both the entity and the relation expressed by the claim, allowing it to place the evidence passage near the top.

This is especially useful when the positive passage answers through a descriptive sentence rather than repeated claim wording. Claims about occupations, works, software history, medical or educational facts, and person attributes all require relation-sensitive matching. Dense retrieval's recall remains slightly below hybrid, so exact entity matching is still useful for full candidate coverage.

### Reranking Hybrid Evaluation Profile

`reranking_hybrid` reaches nDCG@10 of 0.8680422986, hit@10 of 0.9450, and recall@100 of 0.9956896552. The top-100 candidate pool has exactly 100 candidates per query and no safeguard-expanded rows. Hybrid retrieval nearly saturates recall@100, meaning it is highly effective at ensuring the evidence is in the candidate pool.

The downside is top-rank ordering. Hybrid retrieval is below dense retrieval on both nDCG@10 and hit@10. This suggests that sparse same-entity evidence can introduce candidates that look relevant lexically but lack the specific verifying fact. For this task, hybrid candidate generation is valuable, but final ranking needs relation-aware reranking.

### Metric Interpretation for Model Researchers

This split should be interpreted as mostly single-evidence retrieval. Because the median positive count is 1, nDCG@10 is a strong indicator of whether the verifier would see the right passage early. Recall@100 is still important for downstream reranking, but a high recall result can hide poor evidence ordering.

The metric pattern is clear: dense retrieval is best for top-order precision, and hybrid retrieval is best for candidate coverage. A practical pipeline should combine them, but the reranker must learn evidence sufficiency rather than entity overlap alone.

### Query and Relevance Type Tendencies

Queries are factual claims about entities and relations. Examples include claims about a person having a condition named after them, an actor or public figure, a film or work, browser software, and medical-school programs. Relevant documents are Wikipedia-style passages containing dates, roles, works, descriptions, or institutional facts.

Relevance depends on whether the passage can support or refute the claim. A same-entity passage without the target relation is not enough. This makes the task closer to evidence retrieval than ordinary entity search.

### Representative Failure Modes

BM25 can retrieve pages that mention the entity but omit the target fact. Dense retrieval can confuse nearby entities or similar relations when the claim is short. Hybrid retrieval can place entity-heavy distractors above the evidence passage if sparse overlap is over-weighted.

Translation can also introduce difficulty. Names may stay in English, be transliterated, or appear inside translated titles. The retriever must be robust to these forms while still preserving relation-level precision.

### Training Data That May Help

Useful training data includes official FEVER train claims and evidence with overlap removed, Vietnamese claim-evidence retrieval pairs, Wikipedia entity evidence data, and translated FEVER-style data. Training should emphasize evidence retrieval rather than final label classification.

Synthetic data should generate Vietnamese claims from non-evaluation Wikipedia-style passages. Strong hard negatives should mention the same entity but omit or contradict the target relation, forcing the model to distinguish entity match from evidence sufficiency.

### Model Improvement Notes

The main improvement direction is relation-aware reranking over high-recall candidates. Sparse retrieval should preserve names and titles; dense retrieval should model the relation expressed by the claim. Rerankers should ask whether the passage contains the fact needed for support or refutation.

Error analysis should separate entity recall failures from relation-ordering failures. If positives are missing from candidates, improve alias and lexical recall. If positives are present but low ranked, add same-entity hard negatives and train evidence-sufficiency scoring.

## Example Data

| Query | Positive document |
| --- | --- |
| Watchmen là một bộ phim được đặt trong bối cảnh lịch sử thay thế vào năm 1985. [78 chars] | Watchmen (phim) Watchmen là một bộ phim siêu anh hùng Mỹ năm 2009 do Zack Snyder đạo diễn, dựa trên loạt truyện tranh cùng tên của DC Comics ra mắt năm 1986-87 của Alan Moore và Dave Gibbons. Phim có... [200 / 2,181 chars] |
| Jenny McCarthy là một người mẫu. [32 chars] | Jenny McCarthy Jennifer Ann McCarthy ( sinh ngày 1 tháng 11 năm 1972), được biết đến với tên Jenny McCarthy và Jenny Wahlberg, là một nữ diễn viên, người mẫu, người dẫn chương trình truyền hình, tác g... [200 / 1,368 chars] |
| James Brolin đã từng đóng vai trong những vở kịch hài tình huống. [65 chars] | James Brolin James Brolin ( - LSB- broʊlᵻn - RSB- sinh ngày 18 tháng Bảy năm 1940 ) là một diễn viên , nhà sản xuất và đạo diễn người Mỹ, được biết đến với những vai diễn phim và truyền hình , bao gồm... [200 / 494 chars] |
| Joseph Merrick đã là chủ đề của hàng ngàn những dòng tweet hận thù. [67 chars] | Joseph Merrick Joseph Carey Merrick (5 tháng 8 năm 1862 - ngày 11 tháng 4 năm 1890, thường bị nhầm tên là John Merrick) là một người đàn ông Anh với những dị tật rất nặng nề đã từng được trưng bày tại... [200 / 1,396 chars] |
| Chris Mullin chơi bóng rổ cho một đội bóng chuyên nghiệp. [57 chars] | Indiana Pacers Indiana Pacers là một đội bóng rổ chuyên nghiệp của Mỹ có trụ sở tại Indianapolis. Indiana Pacers thi đấu tại giải Nhà nghề Hoa Kỳ (NBA) trong hội nghị miền Đông, giải Trung Bộ. Đội đượ... [200 / 871 chars] |

### Source Reference Table

| Source | Role |
|---|---|
| FEVER | Original fact extraction and verification dataset |
| FEVER project page | Official dataset and task context |
| BEIR | Retrieval benchmark framing |
| VN-MTEB | Vietnamese benchmark collection using translated retrieval tasks |
| GreenNode dataset card | Public dataset entry for this Vietnamese NanoFEVER split |

### Representative Snippets

- Query: `Watchmen là một bộ phim được đặt trong bối cảnh lịch sử thay thế vào năm 1985.`
  Relevant documents describe the film and the alternate-history setting.
- Query: `Jenny McCarthy là một người mẫu.`
  Relevant documents contain the biography and occupation evidence.
- Query: `James Brolin đã từng đóng vai trong những vở kịch hài tình huống.`
  Relevant documents describe the actor's television roles.
- Query: `Joseph Merrick đã là chủ đề của hàng ngàn những dòng tweet hận thù.`
  Relevant documents contain entity evidence needed to evaluate the claim.
- Query: `Chris Mullin chơi bóng rổ cho một đội bóng chuyên nghiệp.`
  Relevant documents include professional basketball career or team evidence.
