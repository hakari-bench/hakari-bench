# MNanoBEIR / NanoBEIR-vi / NanoQuoraRetrieval

## Overview

NanoQuoraRetrieval in the Vietnamese NanoBEIR slice is a duplicate-question retrieval task derived from Quora Question Pairs. The queries are Vietnamese translated questions, and the corpus contains Vietnamese translated candidate questions. The retrieval goal is to find questions that ask the same thing, even when the wording changes. This makes the task useful for evaluating Vietnamese paraphrase retrieval, duplicate intent matching, and short-text semantic similarity.

## Details

### What the Original Data Measures

Quora Question Pairs was released as a dataset competition for identifying whether two questions are duplicates. BEIR adapts this style as retrieval: given one question, the system ranks candidate questions and should place duplicate questions near the top. No standalone task paper is used here; the public dataset competition and BEIR benchmark paper are the main references.

The Vietnamese translated version keeps the duplicate-question structure while adding multilingual paraphrase variation. The candidate documents are also questions, so both query and document are short. A strong model must distinguish true paraphrases from near-topic questions that share names, phrases, or broad subject matter.

### Observed Data Profile

The task contains 50 queries, 5,046 documents, and 70 relevance judgments. The average number of positives is 1.40 per query, with a minimum of 1, a median of 1.0, and a maximum of 6. There are 10 multi-positive queries, or 20.0% of the set.

Queries average 57.26 characters, and documents average 62.69 characters. This is a short-text matching task rather than passage retrieval. Because both sides are questions, relevance depends on intent equivalence, not document topicality or answer containment.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.7238, hit@10 of 0.9000, and recall@100 of 0.9857 using the top-500 BM25 candidate subset. This is a strong lexical profile. Many duplicate questions retain shared key terms, named entities, or distinctive phrases after translation, so term overlap often retrieves a duplicate near the top.

The remaining gap shows where lexical matching is insufficient. Duplicate questions may ask the same intent with different syntax or vocabulary, while non-duplicates can share many visible terms. BM25 is therefore useful as a candidate generator, but it does not fully solve paraphrase ranking.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.8646, hit@10 of 0.9600, and recall@100 of 0.9857. Dense retrieval is the strongest direct ranking profile on this task. It keeps BM25-level recall@100 while substantially improving top-10 ordering.

This is the expected pattern for duplicate-question retrieval. Embedding similarity is well suited to matching question intent when word order, synonym choice, or phrasing changes. Dense retrieval also helps reject same-topic questions that use the same terms but ask for different information.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.7903, hit@10 of 0.9400, and recall@100 of 1.0000. It uses exactly 100 candidates per query, with no safeguard rows. The hybrid profile has perfect recall@100, while dense retrieval has the best top-rank ordering.

This shows that hybrid search is a very strong candidate pool for duplicate-question reranking. BM25 contributes exact phrase and entity coverage, while dense retrieval contributes paraphrase matching. A reranker trained for duplicate intent should benefit from the full candidate coverage, even though dense retrieval is the better first-stage ranker by nDCG@10.

### Metric Interpretation for Model Researchers

Because most queries have one or a few duplicate positives, hit@10 measures whether at least one duplicate is visible, and nDCG@10 measures how well duplicates are placed near the top. recall@100 is mainly a reranking-readiness metric. The dense run leading nDCG@10 indicates that this task rewards semantic equivalence more than pure term overlap.

The comparison separates three useful behaviors: BM25 handles lexically close duplicates, dense retrieval handles paraphrastic intent matching, and reranking_hybrid gives complete candidate coverage. This task is a compact diagnostic for Vietnamese duplicate-question retrieval.

### Query and Relevance Type Tendencies

Queries include questions such as whether it is okay to laugh at one's own jokes, the best lie someone has created, why Quora suggests anti-Donald Trump answers, how to make one's body strong, and how a quantum satellite works. Relevant documents ask the same underlying question with different wording.

The task rewards preserving question intent. A model must understand whether two questions expect the same answer, not only whether they share words. This makes near-duplicate hard negatives especially important: same topic, different requested information.

### Representative Failure Modes

Likely failures include over-ranking questions that share entities but ask a different relation, missing paraphrases that use different vocabulary, confusing broad topical similarity with duplicate intent, and mishandling translated informal phrasing. BM25 may overvalue repeated words, while dense retrieval may overgeneralize semantically adjacent questions.

### Training Data That May Help

Useful training data includes Vietnamese paraphrase retrieval, multilingual duplicate-question data, short-question semantic similarity, and hard negatives that share entities or phrases but ask a different question. Cluster-level duplicate supervision is valuable because some queries have multiple positives.

### Model Improvement Notes

A model targeting this task should optimize for intent equivalence between short questions. Sparse systems need paraphrase expansion and careful phrase handling. Dense systems are the strongest direct baseline and can improve with duplicate-specific hard negatives. Hybrid systems are valuable for reranking because they combine exact phrase coverage with semantic paraphrase recall.

## Example Data

### Public Sources

The original data source is Quora Question Pairs, with BEIR providing the retrieval benchmark framing and NanoBEIR providing the compact multilingual dataset packaging.

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original dataset | [Quora Question Pairs](https://kaggle.com/competitions/quora-question-pairs) |
| Retrieval benchmark framing | [BEIR](https://arxiv.org/abs/2104.08663) |
| Multilingual benchmark context | [MMTEB](https://arxiv.org/abs/2502.13595) |
| NanoBEIR collection | [NanoBEIR on Hugging Face](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
| NanoBEIR-vi dataset | [hakari-bench/NanoBEIR-vi](https://huggingface.co/datasets/hakari-bench/NanoBEIR-vi) |

Representative query and duplicate-question snippets:

| Query | Positive question snippet |
| --- | --- |
| Co duoc cuoi vao nhung cau chuyen cuoi cua chinh minh khong? | Co ky la khong khi cuoi voi nhung cau dua cua chinh minh? |
| Dieu doi tra tot nhat ma ban tung tao ra la gi? | Loi noi doi duoc che tac tot nhat ma ban tung noi la gi? |
| Tai sao Quora thuong goi y nhung cau tra loi trong nguon cap du lieu cua toi che bai Donald Trump? | Tai sao Quora duong nhu chi co nhung cau tra loi chu quan ve Donald Trump? |
| Lam the nao toi co the lam cho co the minh manh me? | Lam the nao de toi tro nen manh me ve the chat? |
| Mot ve tinh luong tu se hoat dong nhu the nao? | Mot ve tinh luong tu hoat dong nhu the nao va mot so ung dung chinh cua no la gi? |
