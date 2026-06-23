# NanoVNMTEB / cqadupstack_physics_vn

## Overview

`cqadupstack_physics_vn` is the Vietnamese NanoVNMTEB version of the CQADupStack Physics duplicate-question retrieval task. CQADupStack was created from StackExchange duplicate links and later became a common BEIR-style retrieval benchmark; this Vietnamese version follows the same title-to-thread retrieval structure for VN-MTEB. Each query is a short translated Physics StackExchange-style title, and the corpus contains longer discussion threads that may include conceptual explanations, equations, thought experiments, and references to physical principles.

The Nano split contains 200 queries, 10,000 candidate documents, and 592 positive relevance judgments. Queries average 58.56 characters, while documents average 800.961 characters. Compared with the Mathematica subset, this task is less code-like and more concept-driven: a relevant document may use different wording while preserving the same physical setup, equation, or explanatory question. The observed evaluation profile reflects that difference. Dense retrieval with `harrier-oss-270m` is strongest at the top ranks and recall, while `reranking_hybrid` remains substantially better than BM25 but does not surpass dense retrieval on nDCG@10 or hit@10.

## Details

### What the Original Data Measures

CQADupStack measures whether a system can retrieve duplicate or semantically equivalent forum questions from a large candidate pool. In the Physics subset, duplicate links often connect questions that ask about the same principle using different examples. A query may mention the propagation speed of force, whether human activity affects Earth rotation, the interpretation of Archimedes' principle, quantum-computing capability, the Higgs boson, negative temperature, or a gravity thought experiment.

The Vietnamese version preserves this duplicate-search problem while introducing translated scientific terminology. Good retrieval requires matching the physical relation, not only the exact words. A thread about a rigid rod and faster-than-light signaling may be relevant to a query phrased as force propagation through matter. A thread about floating cups and displaced water may be relevant to a query about Archimedes' principle. This makes the task a useful benchmark for semantic retrieval over scientific Q&A.

### Observed Data Profile

The task has 592 positive qrels for 200 queries, or 2.96 positives per query on average. The median remains 1, but 82 queries have multiple positives, and the multi-positive query rate is 41.0%. The largest positive cluster has 72 relevant documents. This means the task contains many single-duplicate cases as well as several recurring physics topics that have been asked in many forms.

Documents are much longer than queries and often include explanatory reasoning, equations, comments, and answer context. Query titles are compact and may omit the physical assumptions that determine relevance. In practice, a retriever has to bridge from a short question title to a longer thread where the decisive content may be a scenario description or a principle stated in the body. Because Physics Q&A is concept-heavy, semantic similarity is a stronger signal here than in more code-anchored CQADupStack subsets.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.4126511755, hit@10 of 0.6050, and recall@100 of 0.5000 with a top-500 candidate set. These are solid lexical scores for a translated duplicate-retrieval task. Physics questions often reuse distinctive terms such as force, gravity, Higgs, quantum computer, temperature, or Archimedes, and BM25 can use these terms effectively when they appear in both the query and relevant documents.

However, BM25 is limited by paraphrase and scenario variation. Duplicate questions frequently share a physical principle without repeating the same title words. A query about force propagation may retrieve many documents containing force-related terms, but the actual duplicate might describe information transfer in a rigid object. A query about the Earth's rotation may have relevant posts that talk about angular momentum, mass redistribution, buildings, or human activity. BM25 therefore provides important lexical coverage but misses many cases where the connection is conceptual rather than word-for-word.

### Dense Evaluation Profile

Dense retrieval with `harrier-oss-270m` reaches nDCG@10 of 0.4990659053, hit@10 of 0.7550, and recall@100 of 0.6368243243. It is the strongest reported condition for this task. The gain over BM25 is large at both top rank and recall, which indicates that embedding similarity captures many duplicate relations that are not obvious from exact term overlap alone.

This behavior matches the nature of physics Q&A. The same question can be expressed as a concrete thought experiment, an equation-level formulation, or a conceptual request. Dense retrieval can connect these forms when the underlying physical principle is similar. It is especially helpful for queries where a translated title uses one wording and the relevant document frames the issue through a different example. The remaining errors likely come from physically adjacent but non-duplicate discussions: documents may share terms like gravity, force, quantum, or temperature while addressing different assumptions or scales.

### Reranking Hybrid Evaluation Profile

`reranking_hybrid` reaches nDCG@10 of 0.4696468010, hit@10 of 0.6900, and recall@100 of 0.6351351351. The top-100 reranking candidate pool has mean candidate count 100.085, with 17 rows expanded to 101 candidates by qrels safeguards. The hybrid condition clearly outperforms BM25 and nearly matches dense recall@100, but it is below dense retrieval on nDCG@10 and hit@10.

This pattern is important. Hybrid search is not automatically strongest when dense embeddings already capture the primary relevance structure. In this task, lexical evidence still helps identify exact topics and named concepts, but dense semantic matching appears better at ordering the most useful duplicates near the top. The hybrid candidate pool recovers many relevant documents, yet the final top-10 ranking does not improve over dense. Researchers should treat this as a case where hybrid recall is valuable, but the reranking or fusion strategy must be tuned carefully to avoid pulling lexical near-matches above more semantically faithful duplicates.

### Metric Interpretation for Model Researchers

The relation among metrics shows a concept-oriented retrieval task. Dense retrieval beats BM25 by about 0.0864 nDCG@10 and 0.15 hit@10, with a large recall@100 advantage. `reranking_hybrid` closes most of the recall gap but remains between BM25 and dense at the top ranks. A model that improves this task should preserve dense semantic strength while using sparse evidence only when it disambiguates the physical setup.

The multi-positive rate of 41.0% means that recall@100 is meaningful. Many queries have several valid duplicates, and models should retrieve more than one phrasing of the same recurring question. At the same time, the median positive count is 1, so nDCG@10 still punishes models that rank a merely related physics topic above the actual duplicate. Good evaluation should inspect both whether the relevant cluster is present in the candidate pool and whether the most precise duplicate appears early.

### Query and Relevance Type Tendencies

Queries often ask about a principle through a concrete scenario: gravity in a tunnel through Earth, the speed at which force propagates, cloud thickness, pushing versus pulling, negative temperature, or whether a newly observed particle completes a theory. Relevant documents may phrase the same issue as a different thought experiment or a more formal physical question.

Relevance is stricter than topical similarity. Two quantum-computing posts are not necessarily duplicates; they must ask about the same kind of capability or claim. Two gravity posts may be unrelated if one is about orbital mechanics and another about local acceleration. This makes the task useful for evaluating whether models distinguish physical principle, boundary conditions, and question intent.

### Representative Failure Modes

BM25 can over-rank documents that share a named concept but answer a different question. For example, many documents may mention Higgs bosons, quantum computers, or Archimedes' principle while focusing on different scientific claims. Dense retrieval can make the opposite mistake: it may group documents by broad conceptual neighborhood and miss a decisive condition, such as whether the question is about force propagation, material deformation, or information transfer.

Another failure mode is scenario substitution. A model may retrieve a document with a superficially similar thought experiment but a different physical mechanism. Strong systems need to track the object, interaction, scale, and principle together rather than treating the topic label as sufficient.

### Training Data That May Help

Useful training data includes multilingual science Q&A duplicates, paraphrase pairs for physics questions, and hard negatives drawn from the same subfield. Contrastive examples should include questions that share terms but differ in mechanism, such as related force questions with different propagation assumptions or related quantum-computing questions with different claims.

Data with equations and explanatory prose is also valuable. The relevant relation is often established in the body rather than the title, so title-to-long-document training can help. Vietnamese scientific paraphrase data would improve matching across translated terminology, while English-origin Physics StackExchange duplicates can help preserve the domain structure if aligned carefully.

### Model Improvement Notes

For this task, improving dense semantic retrieval is likely more important than adding more lexical weighting. The dense baseline already has the best nDCG@10 and hit@10, so additional sparse evidence should be used for disambiguation rather than broad score boosting. A reranker that compares physical assumptions explicitly could turn the hybrid candidate pool into better top-rank performance.

Researchers should audit false positives by subfield. If a model confuses broad quantum topics, gravity thought experiments, or thermodynamics questions, the fix may require domain-specific hard negatives. If it misses duplicates with different Vietnamese wording, multilingual paraphrase training is the better target. The task is a compact but useful diagnostic for scientific semantic retrieval in Vietnamese.

## Example Data

| Query | Positive document |
| --- | --- |
| Thương mại có ảnh hưởng đến sự quay của Trái Đất không? [55 chars] | Nhân loại và các hoạt động/cấu trúc do con người tạo ra có ảnh hưởng đến chuyển động quay của Trái Đất? Chúng ta đi bộ hay lái phương tiện đến đích hàng ngày. Hành động của chúng ta có ảnh hưởng đến s... [200 / 410 chars] |
| Nguyên lý của Archimedes: thuật ngữ không chính xác? [52 chars] | Tại sao một cốc có 100 g nước nổi khi đặt trên một cốc khác có 50 g nước? Hãy tưởng tượng chúng ta có cốc A với 50 g nước và cốc B (nhỏ hơn so với cốc A) với 100 g nước. Bây giờ cho cốc B vào trong cố... [200 / 716 chars] |
| Máy tính lượng tử D-Wave có thể làm gì? [39 chars] | Máy tính lượng tử do D-Wave Systems, Inc. sản xuất có hoạt động không? D-wave tuyên bố đã chế tạo được 128 máy tính lượng tử qbit thương mại? Điều tôi không hiểu là họ có thực sự làm được điều này hay... [200 / 1,857 chars] |
| Có phải hạt Higgs là hạt cuối cùng được dự đoán bởi Mô hình chuẩn? [66 chars] | Boson Higgs trong LHC Gần đây, các hạt higgs bosons đã được phát hiện ra ở LHC. Câu hỏi của tôi là làm sao họ biết rằng những hạt được tạo ra thực sự là higgs boson? Họ xác nhận chúng là higgs boson d... [200 / 229 chars] |
| Lực lan truyền trong vật chất nhanh như thế nào? [48 chars] | Có thể truyền tải thông tin nhanh hơn tốc độ ánh sáng bằng cách sử dụng một cây gậy cứng không? Có thể truyền tải thông tin (như 1 và 0) nhanh hơn tốc độ ánh sáng không? Ví dụ, hãy lấy một cây cột cứn... [200 / 468 chars] |

### Source Reference Table

| Source | Role |
|---|---|
| CQADupStack | Original duplicate-question retrieval benchmark |
| BEIR | Common retrieval-evaluation framing for CQADupStack |
| VN-MTEB | Vietnamese benchmark collection using translated retrieval tasks |
| GreenNode dataset card | Public dataset entry for this Vietnamese Physics subset |

### Representative Snippets

- Query: `Thương mại có ảnh hưởng đến sự quay của Trái Đất không?`
  Relevant documents discuss whether human activity, structures, or mass redistribution can affect Earth's rotation.
- Query: `Nguyên lý của Archimedes: thuật ngữ không chính xác?`
  Relevant documents concern buoyancy reasoning, such as why one cup of water can float in another under particular conditions.
- Query: `Máy tính lượng tử D-Wave có thể làm gì?`
  Relevant documents ask about the practical capability or interpretation of D-Wave quantum computers.
- Query: `Có phải hạt Higgs là hạt cuối cùng được dự đoán bởi Mô hình chuẩn?`
  Relevant documents discuss the Higgs boson in relation to the Standard Model and particle-discovery claims.
- Query: `Lực lan truyền trong vật chất nhanh như thế nào?`
  Relevant documents ask how quickly force or information propagates through matter, including rigid-object thought experiments.
