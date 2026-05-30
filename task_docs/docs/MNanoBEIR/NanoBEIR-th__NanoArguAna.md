# MNanoBEIR / NanoBEIR-th / NanoArguAna

## Overview

NanoArguAna in the Thai NanoBEIR slice is an argument-counterargument retrieval task derived from ArguAna. The queries and documents are Thai translated argumentative passages, and each query has one paired relevant response passage. The benchmark measures whether a retriever can identify argumentative relation, stance contrast, and response fit between long texts. It is a compact but demanding diagnostic for multilingual retrieval where topical similarity alone is not sufficient.

## Details

### What the Original Data Measures

ArguAna is used in BEIR as an argument retrieval task where relevance depends on the relation between an argument and a counterargument. The relevant passage may challenge a premise, present a different stance, or respond to the specific reasoning in the query. A same-topic passage is not automatically relevant if it does not answer the argumentative move.

The Thai translated version adds difficulty from long translated passages and Thai word segmentation. Both query and document are substantial argumentative texts, so the model must compare claims, reasons, and stance across a full discourse unit. Lexical overlap helps identify the debate topic, but the relevant response may not be the passage with the most repeated words.

### Observed Data Profile

The task contains 50 queries, 3,635 documents, and 50 relevance judgments. Every query has exactly one positive passage: the average, minimum, median, and maximum positives per query are all 1.0, and there are no multi-positive queries. This makes the benchmark a precise single-target retrieval task.

Queries average 820.62 characters, and documents average 860.05 characters. Both sides are long compared with ordinary web-search tasks. The length means that simple keyword overlap can find same-topic passages, but ranking the exact paired response requires understanding the argumentative relation across many sentences.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.4051, hit@10 of 0.7200, and recall@100 of 0.9400 using the top-500 BM25 candidate subset. This is a strong lexical candidate-generation profile. Long argumentative passages repeat topic words, entities, and policy terms, which gives BM25 useful anchors.

The gap between recall@100 and nDCG@10 is the main signal. BM25 usually gets the correct response into the first 100 ranks, but it often cannot place it in the top 10. That is consistent with ArguAna: many distractors discuss the same topic, while only one passage responds to the query's stance and premise.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.3721, hit@10 of 0.7000, and recall@100 of 0.9000. Dense retrieval is slightly weaker than BM25 on this Thai slice. This suggests that the dense model captures broad argumentative or topical similarity, but exact lexical anchors and long-passage overlap remain especially important for finding the paired response.

The dense weakness does not mean semantics are irrelevant. Rather, it indicates that general embedding similarity may blur stance and response relation in long Thai argumentative text. A dense model can retrieve passages about the same debate while still missing the exact counterargument pair.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.4349, hit@10 of 0.7200, and recall@100 of 0.9200. It uses a top-100 candidate range with an optional rank-101 safeguard; the observed candidate count ranges from 100 to 101, with 4 safeguard rows and a mean of 100.08 candidates. This is the strongest top-10 ranking profile among the three modes.

The hybrid result shows that Thai ArguAna benefits from combining lexical topic anchors with dense semantic signals. BM25 alone has the best recall@100, but hybrid improves nDCG@10 by better ordering the high-confusion same-topic candidate set. For direct top-rank retrieval, the hybrid profile is the most aligned with the task.

### Metric Interpretation for Model Researchers

Because every query has one positive, nDCG@10 and hit@10 directly measure whether the paired response is visible near the top. recall@100 measures whether a later reranker has a chance to recover it. The task is useful for separating candidate recall from stance-aware ordering: BM25 finds candidates, but hybrid ranks the top list better.

The comparison also warns that dense retrieval alone may not be enough for long Thai argument matching. A model may need language-aware tokenization, Thai discourse coverage, and hard negatives that share topic vocabulary but differ in stance or response target.

### Query and Relevance Type Tendencies

Queries are long argumentative passages about issues such as public indifference to reform, Heathrow expansion, choice overload, cyberattacks by non-state actors, and the relation between religion, hate speech, and free expression. Positives are paired response passages, often counterarguments or passages that qualify the original reasoning.

The task rewards models that understand the target of an argument. A relevant document should respond to the claim being made, not just mention the same policy area. This makes stance, premise, and argumentative role central to relevance.

### Representative Failure Modes

Likely failures include retrieving same-topic passages that do not respond to the query, confusing support and counterargument roles, over-ranking long passages with repeated topic words, and missing the paired response when Thai translation changes wording. Dense models may retrieve semantically related but stance-mismatched passages, while BM25 may overvalue surface overlap.

### Training Data That May Help

Useful training data includes Thai debate retrieval, argument-counterargument pairs, stance-aware ranking, multilingual argument mining, and hard negatives from the same topic but different stance or premise. Thai segmentation-aware preprocessing may help sparse systems. For rerankers, same-topic non-response passages are the most important negative examples.

### Model Improvement Notes

A model targeting this task should improve response-relation modeling for long Thai argumentative passages. Sparse systems should preserve strong lexical candidate recall while reducing same-topic distractors. Dense systems need hard-negative training on stance and counterargument relation. Hybrid systems are promising because they combine topic anchoring with semantic response cues.

## Example Data

### Public Sources

The original task is based on ArguAna argument retrieval, with BEIR providing the retrieval benchmark framing and NanoBEIR providing the compact multilingual dataset packaging.

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original dataset | [ArguAna](https://aclanthology.org/P18-1023/) |
| Retrieval benchmark framing | [BEIR](https://arxiv.org/abs/2104.08663) |
| Multilingual benchmark context | [MMTEB](https://arxiv.org/abs/2502.13595) |
| NanoBEIR collection | [NanoBEIR on Hugging Face](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
| NanoBEIR-th dataset | [hakari-bench/NanoBEIR-th](https://huggingface.co/datasets/hakari-bench/NanoBEIR-th) |

Representative query and positive response snippets:

| Query | Positive document snippet |
| --- | --- |
| สาธารณชนไม่สนใจการปฏิรูป ไม่ว่าจะเป็นการปฏิรูปสภาขุนนางควรเป็นลำดับความสำคัญสูงสุด... | แคมเปญ AV ไม่สามารถเปรียบเทียบกับการปฏิรูปสภาขุนนางได้... |
| การขยายสนามบินฮีทโธรว์มีความสำคัญต่อเศรษฐกิจ... | ชุมชนธุรกิจยังห่างไกลจากการเป็นเอกภาพในความสนับสนุนที่กล่าวอ้าง... |
| ผู้คนได้รับทางเลือกมากเกินไป ซึ่งทำให้พวกเขาน้อยใจมากขึ้น... | ผู้คนไม่พอใจเพราะพวกเขาไม่สามารถมีทุกอย่างได้... |
| การโจมตีทางไซเบอร์มักเกิดขึ้นโดยผู้ที่ไม่ใช่รัฐ... | ในกรณีที่มีการโจมตีจากผู้ไม่ใช่รัฐ ผู้เชี่ยวชาญหลายคนในกฎหมายระหว่างประเทศเห็นพ้องกัน... |
| เนื่องจากศาสนาส่งเสริมความแน่นอนของความเชื่อ... | ไม่มีใครถูกบังคับให้กระทำการใช้ความรุนแรงโดยคำพูดของผู้อื่น... |
