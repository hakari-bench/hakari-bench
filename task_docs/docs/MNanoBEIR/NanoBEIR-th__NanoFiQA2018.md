# MNanoBEIR / NanoBEIR-th / NanoFiQA2018

## Overview

NanoFiQA2018 in the Thai NanoBEIR slice is a financial question-answer retrieval task derived from FiQA. The queries are Thai translated finance questions, and the corpus contains Thai translated answer passages. The retrieval goal is to find passages that answer practical finance questions about investment returns, taxes, trading volume, credit card rewards, and contractor filing. This makes the task a compact diagnostic for domain-specific answer retrieval, where terminology, intent, and practical context all matter.

## Details

### What the Original Data Measures

FiQA was introduced for financial opinion mining and question answering. In retrieval form, it tests whether a model can connect a finance question to answer passages that resolve the user's need. The answers may explain a concept, describe a tax rule, compare financial measurements, or give practical advice. Relevance is therefore answer-specific rather than merely topical.

The Thai translated version adds multilingual pressure around finance vocabulary, tax terminology, investment concepts, and long explanatory answer passages. Some financial names and abbreviations remain in English, while the rest of the text is Thai. A strong retriever must bridge Thai question wording to answer passages that may use technical terms or examples rather than repeating the question.

### Observed Data Profile

The task contains 50 queries, 4,598 documents, and 123 relevance judgments. The average number of positives is 2.46 per query, with a minimum of 1, a median of 2.0, and a maximum of 15. There are 28 multi-positive queries, or 56.0% of the query set. The task therefore mixes single-answer retrieval with broader answer-set ranking.

Queries average 55.18 characters, while documents average 779.20 characters. The queries are short finance questions, and the answer passages are often several sentences long. The model must identify whether the passage actually answers the financial decision problem, not just whether it shares a finance topic.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.2726, hit@10 of 0.5200, and recall@100 of 0.6098 using the top-500 BM25 candidate subset. This is a moderate lexical profile. Financial terms provide useful anchors, but many question-answer pairs do not share enough exact wording for BM25 to dominate the task.

BM25 is likely to succeed when the question includes distinctive terms such as Vanguard, tax, volume, or credit-card points. It is weaker when the answer uses a technical synonym or explains the answer indirectly. The recall@100 value shows that lexical retrieval often finds some relevant candidates, but it misses a substantial part of the answer set.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.4085, hit@10 of 0.6800, and recall@100 of 0.6504. Dense retrieval improves top-rank quality and hit rate substantially over BM25. This indicates that embedding similarity is better aligned with financial answer intent than exact term overlap alone.

The dense advantage is important because finance answers often paraphrase the question. A question about return type can be answered with a discussion of CAGR; a tax question can be answered with a passage about income rules or filing status. Dense retrieval still leaves room for improvement because financial answers can depend on jurisdiction, assumptions, and detailed context that general semantic similarity may not fully capture.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.3911, hit@10 of 0.5800, and recall@100 of 0.6829. It uses a top-100 candidate range with an optional rank-101 safeguard; the observed candidate count ranges from 100 to 101, with 6 safeguard rows and a mean of 100.12 candidates. The hybrid profile has the best recall@100, while dense retrieval has the strongest nDCG@10 and hit@10.

This suggests that hybrid search is useful for candidate coverage but not optimal as a direct first-stage ranker. BM25 contributes extra candidates through exact finance terms, but it can also pull term-overlap passages above better semantic answers. For Thai FiQA, dense retrieval is the better first-page signal, while reranking_hybrid is a broader pool for a later answer-aware reranker.

### Metric Interpretation for Model Researchers

nDCG@10 is the most practical metric for this task because a finance QA system needs the answer passage near the top. hit@10 measures whether at least one answer is visible, and recall@100 measures whether downstream reranking can access the answer set. Since more than half the queries have multiple positives, recall also reflects answer diversity.

The profile shows a clear answer-intent challenge. BM25 is not enough because finance questions and answers often use different wording. Dense retrieval provides the best top-rank behavior. reranking_hybrid expands candidate recall but needs stronger final ordering. Researchers can use this task to test finance-domain hard negatives and Thai question-answer alignment.

### Query and Relevance Type Tendencies

Queries ask practical finance questions such as what type of return Vanguard reports, the tax consequences of freelance work in the United States, what counts as high or low volume, whether credit-card points can pay tax-deductible business expenses, and how a contractor should file taxes. Relevant passages are explanatory answers with assumptions, examples, and caveats.

The task rewards models that understand financial concepts and answer type. A passage can mention tax or investments and still be irrelevant if it answers a different decision problem. The short Thai questions make intent recognition especially important.

### Representative Failure Modes

Likely failures include retrieving passages with the same financial term but a different answer target, missing answers expressed with technical language, over-ranking generic investment or tax advice, and confusing personal and business contexts. BM25 may be too literal, while dense retrieval may retrieve semantically related but practically unhelpful answers.

### Training Data That May Help

Useful training data includes Thai financial QA, multilingual finance retrieval, personal-finance forums, tax and investment answer ranking, and hard negatives that share financial terminology but answer a different need. For rerankers, near-topic wrong answers are particularly valuable because they reflect the main ambiguity in the task.

### Model Improvement Notes

A model targeting this task should improve domain-specific answer matching. Dense retrieval is the strongest direct baseline, but it should be refined with finance-specific positives and hard negatives. Sparse systems need query expansion and Thai-aware tokenization for finance terms. Hybrid systems should use the high-recall pool with a reranker that judges whether the passage actually answers the question.

## Example Data

### Public Sources

The original task is based on FiQA, with BEIR providing the retrieval benchmark framing and NanoBEIR providing the compact multilingual dataset packaging.

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original dataset | [FiQA](https://doi.org/10.1145/3184558.3192301) |
| Retrieval benchmark framing | [BEIR](https://arxiv.org/abs/2104.08663) |
| Multilingual benchmark context | [MMTEB](https://arxiv.org/abs/2502.13595) |
| NanoBEIR collection | [NanoBEIR on Hugging Face](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
| NanoBEIR-th dataset | [hakari-bench/NanoBEIR-th](https://huggingface.co/datasets/hakari-bench/NanoBEIR-th) |

Representative query and positive answer snippets:

| Query | Positive document snippet |
| --- | --- |
| Vanguard กำลังอ้างถึงผลตอบแทนประเภทใด? | จากหน้า Vanguard - นี่ดูเหมือนจะเป็นเรื่องที่ง่ายที่สุดเพราะข้อมูล S&P หาง่าย... |
| ผลกระทบด้านภาษีของการทำงานฟรีแลนซ์ในสหรัฐอเมริกา | หากคุณมีรายได้ในสหรัฐอเมริกา คุณจะต้องเสียภาษีรายได้สหรัฐจากรายได้ดังกล่าว... |
| ปริมาณอะไรถือว่าสูงหรือต่ำเมื่อพูดถึงปริมาณ? | ปริมาณการซื้อขายรายวันมักจะถูกเปรียบเทียบกับปริมาณการซื้อขายเฉลี่ยรายวัน... |
| การใช้คะแนนบัตรเครดิตเพื่อชำระค่าใช้จ่ายทางธุรกิจที่หักลดหย่อนภาษีได้ | เพื่อความเรียบง่าย มาลองพิจารณาแค่เงินคืนกันก่อน... |
| ฉันควรยื่นภาษีอย่างไรในฐานะผู้รับเหมา? | เพื่อวัตถุประสงค์ด้านภาษี คุณจะต้องยื่นแบบฟอร์มในฐานะพนักงาน... |
