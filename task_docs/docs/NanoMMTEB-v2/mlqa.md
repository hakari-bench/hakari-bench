# NanoMMTEB-v2 / mlqa

## Overview

`NanoMMTEB-v2 / mlqa` is a multilingual QA retrieval task derived from MLQA.
Queries are questions in Arabic, German, Spanish, Hindi, Vietnamese, Chinese,
and English, and documents are Wikipedia-style context passages. The Nano split
has 196 queries, 10,000 documents, and 196 positive qrel rows, with exactly one
positive passage per query. Current diagnostics show dense retrieval as the
strongest profile, `reranking_hybrid` as better than BM25 in recall but weaker
than dense, and BM25 as very weak because many query-passage pairs are
cross-lingual or paraphrastic.

## Details

### What the Original Data Measures

MLQA was introduced as a multi-way aligned extractive question-answering
benchmark in seven languages. It uses Wikipedia contexts and questions designed
for cross-lingual QA evaluation. In the retrieval adaptation, the question is
the query and the answer-bearing context is the positive document.

This task measures multilingual and cross-lingual passage retrieval for
extractive QA. A model must retrieve the passage containing the answer span or
direct answer-bearing sentence, even when the question and context are in
different languages.

### Observed Data Profile

The Nano split contains 196 queries, 10,000 documents, and 196 positive qrel
rows. Every query has exactly one positive document. Queries average 47.39
characters, while documents average 731.34 characters.

Observed examples include Vietnamese, Arabic, German, Hindi, Chinese, Spanish,
and English questions. Positive passages can be in the same language or a
different MLQA language, including examples where Arabic questions retrieve
German passages or Hindi questions retrieve English passages.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset contains 500 candidates per query and
achieves nDCG@10 = 0.0390, hit@10 = 0.0663, and recall@100 = 0.1429. BM25 is
extremely weak for this task.

The reason is structural: exact word overlap is often unavailable when the
query and positive passage use different languages or scripts. Even monolingual
pairs may ask for an answer span with paraphrased wording. Term frequency is
therefore a poor proxy for answerability.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset contains 500 candidates per
query and achieves nDCG@10 = 0.0959, hit@10 = 0.2194, and recall@100 = 0.5561.
Dense retrieval is the strongest observed profile, but absolute top-rank
quality is still low.

This shows that multilingual embeddings recover far more positives than lexical
matching, especially for cross-lingual question-context pairs. At the same
time, the task remains difficult: the model must align answer-seeking questions
with passages in different languages and distinguish answer-bearing contexts
from same-topic Wikipedia passages.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains mostly 100 candidates per
query, with 113 queries using a rank-101 safeguard row. It achieves nDCG@10 =
0.0534, hit@10 = 0.1071, and recall@100 = 0.4235. Hybrid retrieval improves
over BM25 but is clearly below dense retrieval.

The many safeguard rows indicate that the hybrid top-100 pool often needs
positive injection to retain the correct passage. Sparse evidence is weak
enough that combining it with dense retrieval can dilute the stronger dense
signal. This is a dense-first cross-lingual retrieval task.

### Metric Interpretation for Model Researchers

This task is single-positive: each query has one answer-bearing context.
Hit@10 measures whether that context appears near the top. nDCG@10 is sensitive
to the exact rank of the positive, and recall@100 measures whether it is
available for reranking.

The low absolute scores are meaningful. They indicate that cross-lingual
answer-passage retrieval is challenging even for dense multilingual models.
Researchers should not treat BM25 as a competitive baseline here; it mostly
measures same-script lexical overlap when it exists.

### Query and Relevance Type Tendencies

Queries are short multilingual questions targeting explicit answer spans in
Wikipedia-style contexts. Relevant documents are context passages that contain
the answer. Cross-lingual cases require language alignment rather than surface
matching.

The task rewards multilingual semantic alignment, answer-span sensitivity, and
robust retrieval across scripts. It penalizes systems that only retrieve broad
article topics without locating the answer-bearing passage.

### Representative Failure Modes

BM25 fails when query and context are in different languages or when the answer
is paraphrased. Dense retrieval can fail by retrieving a same-topic passage that
lacks the answer span, especially for common entities or broad Wikipedia
topics. Hybrid retrieval can underperform dense retrieval when weak sparse
candidates pull the positive down.

Rerankers should compare the question's requested answer type against the
candidate passage and should be cross-lingual when necessary.

### Training Data That May Help

Useful training data includes SQuAD-style QA retrieval, multilingual Wikipedia
passage retrieval, cross-lingual question-context pairs, and non-overlapping
MLQA-style parallel QA data. Overlapping MLQA validation or test questions,
contexts, and positives from this Nano split should be excluded.

Synthetic data can generate questions from Wikipedia-style contexts in each
MLQA language, including cross-lingual variants where query and context are in
different languages. Positives must contain the answer span or direct
answer-bearing sentence. Hard negatives should share the article topic but not
answer the question.

### Model Improvement Notes

Dense retrievers should improve cross-lingual alignment and answer-aware
passage scoring. Sparse systems need translation, transliteration, or query
expansion to be useful. Rerankers should support cross-lingual evidence
matching and answer-span verification.

For hybrid systems, `NanoMMTEB-v2 / mlqa` is a warning case: sparse evidence can
weaken a dense-first task. The best first-stage profile is dense retrieval, and
hybrid designs need language-aware weighting.

## Example Data

| Query | Positive document |
| --- | --- |
| Phiên dịch được sử dụng cho ngôn ngữ nào? [41 chars] | Nói chung, tất cả mọi người trong nước đều hiểu và nói tiếng Nga, ngoại trừ tại một số vùng xa xôi hẻo lánh. Tiếng Nga là tiếng mẹ đẻ của đa số dân cư Bishkek, và hầu hết các giao dịch thương mại cũng... [200 / 539 chars] |
| ما هي التقنيات الحديثة المستخدمة للوصول إلى الإنترنت عبر الهاتف المحمول؟ [72 chars] | Reichweite und Bandbreite: Mobiler Internetzugriff ist generell langsamer als direkte Kabelverbindungen. Verwendete Technologien sind hier GPRS, oder EDGE, aktuell auch HSDPA und HSUPA, 3G und 4G Netz... [200 / 435 chars] |
| Was wurde in den 1990er Jahren eingeführt? [42 chars] | أما القديس فالنتين الذي كان يعيش في تورني فقد أصبح أسقفًا لمدينة انترامنا (الاسم الحديث لمدينة تورني) تقريبًا في عام 197 بعد الميلاد، ويُقال إنه قد قُتل فترة الاضطهاد التي تعرض له المسيحيون أثناء عهد... [200 / 407 chars] |
| TB-3 là loại phương tiện vận tải gì? [36 chars] | 图波列夫TB-3（俄语：Тяжёлый Бомбардировщик，转写：Tyazholy Bombardirovschik，意为重型轰炸机；民用型则称为ANT-6）是西元1930年代苏联空军列装的重型轰炸机，并被使用于第二次世界大战。它是世界上第一个悬翼四引擎的重型轰炸机。 西元1939年，TB-3因过时而正式退役，但TB-3仍在整个二次世界大战进行轰炸和运输工作。 TB-3也以Zveno计划... [200 / 221 chars] |
| बाह्यत्वचा की कोशिकाएं क्या कर सकती हैं? [40 chars] | The plant epidermis is specialised tissue, composed of parenchyma cells, that covers the external surfaces of leaves, stems and roots. Several cell types may be present in the epidermis. Notable among... [200 / 1,229 chars] |

### Public Sources

- [MLQA: Evaluating Cross-lingual Extractive Question Answering](https://arxiv.org/abs/1910.07475),
  2019.
- [MLQA dataset](https://huggingface.co/datasets/mlqa).
- [mteb/MLQARetrieval](https://huggingface.co/datasets/mteb/MLQARetrieval).
- [hakari-bench/NanoMMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoMMTEB-v2),
  Nano benchmark dataset.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| MLQA: Evaluating Cross-lingual Extractive Question Answering | 2019 | task paper | [https://arxiv.org/abs/1910.07475](https://arxiv.org/abs/1910.07475) |
| MLQA dataset | 2019 | dataset card | [https://huggingface.co/datasets/mlqa](https://huggingface.co/datasets/mlqa) |
| mteb/MLQARetrieval | 2024 | dataset card | [https://huggingface.co/datasets/mteb/MLQARetrieval](https://huggingface.co/datasets/mteb/MLQARetrieval) |

### Representative Snippets

| Query pattern | Positive document pattern |
| --- | --- |
| A Vietnamese question about what language interpretation is used for. | A Vietnamese passage about Russian language use in Bishkek. |
| An Arabic question about mobile internet technologies. | A German passage listing GPRS, EDGE, 3G, 4G, and 5G. |
| A German question about what was introduced in the 1990s. | An Arabic passage containing the answer context. |
| A Vietnamese question asking what kind of vehicle TB-3 was. | A Chinese passage about the Tupolev TB-3 heavy bomber. |
| A Hindi question about what epidermal cells can do. | An English passage about plant epidermis. |
