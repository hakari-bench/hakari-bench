# MNanoBEIR / NanoBEIR-ar / NanoMSMARCO

## Overview

NanoBEIR-ar / NanoMSMARCO is the Arabic NanoBEIR version of MS MARCO passage
ranking, the web question answering benchmark introduced in
[MS MARCO: A Human Generated MAchine Reading COmprehension
Dataset](https://arxiv.org/abs/1611.09268). Each query is an Arabic translated
real-search-style question, and the retrieval target is the Arabic translated
passage that answers it. The Nano task contains 50 queries, 5,043 passages, and
50 positive qrels, with exactly one positive per query. The task is broad and
informal: questions may be definitions, consumer information needs, short
fragments, entertainment queries, or practical "how long" questions. Dense
retrieval is the best top-rank signal here, while `reranking_hybrid` gives the
best top-100 coverage.

## Details

### What the Original Data Measures

MS MARCO was built from anonymized Bing search questions and web passages. This
origin matters because the queries are not clean benchmark questions written
from a known paragraph. They can be short, underspecified, noisy, ambiguous, or
phrased as natural search fragments. In the passage-ranking formulation, the
retriever must find a passage that directly answers the user's information
need.

The Arabic NanoBEIR version keeps that web search retrieval shape in translated
form. It is not a domain-specific QA task and not an entity-only lookup. It
tests whether a model can connect short Arabic questions to compact answer
passages across everyday topics.

### Observed Data Profile

The metadata records 50 queries, 5,043 documents, and 50 positive qrels. Every
query has exactly one positive. Query text is short, averaging 31.02
characters, and documents average 275.62 characters. The examples include
questions about a medical syndrome, who sang a song, a television actor's role,
where major deserts are located, and the meaning of "copper" in a policing
context.

The short-query shape makes this task sensitive to intent understanding. A
query may expose only a few words, while the answer passage may use explanatory
phrasing. The model must decide whether a passage actually resolves the
information need, not merely whether it shares a visible keyword.

### BM25 Evaluation Profile

The BM25 candidate subset reaches nDCG@10 = 0.2732, hit@10 = 0.4400, and
Recall@100 = 0.8200. BM25 is useful when the query contains a distinctive name,
song title, medical term, location, or quoted word that appears in the answer
passage. It provides an exact lexical anchor for noisy web queries.

The sparse baseline is limited because many MS MARCO questions are short and
answer-oriented. The answer passage may explain the concept without repeating
the same wording, or the query may be ambiguous until the passage resolves it.
BM25 can also retrieve passages that share a keyword but do not answer the
specific user question. This makes it a reasonable candidate generator but a
weak final ranker for this Arabic translated sample.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` reaches nDCG@10 =
0.3625, hit@10 = 0.5200, and Recall@100 = 0.8800. Dense retrieval is the best
top-rank signal in this task. The improvement over BM25 indicates that
embedding similarity helps match short Arabic search questions to passages that
answer them with different wording.

Dense retrieval is especially useful for definitions, practical advice,
consumer questions, and queries where the answer passage is explanatory rather
than lexically parallel. Its weakness is broad semantic drift: a model can
retrieve a passage about a related topic without answering the exact question,
especially when the query is very short or ambiguous.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset reaches nDCG@10 = 0.3212, hit@10 =
0.4600, and Recall@100 = 0.9000. Hybrid is weaker than dense in top-rank
ordering but has the best Recall@100. The metadata records 5 rows with the
optional rank-101 safeguard, indicating that a few positives needed explicit
preservation near the top-100 boundary.

For reranking experiments, the hybrid pool is useful because it combines exact
query-term candidates from BM25 with semantically matched answer passages from
dense retrieval. The reranker can then decide which candidate actually answers
the user need.

### Metric Interpretation for Model Researchers

This task shows a split between top-rank quality and candidate coverage. Dense
retrieval has the strongest nDCG@10 and hit@10, so it is the best direct
retriever among the provided candidate views. Hybrid has the strongest
Recall@100, so it is safer as a reranker candidate source. BM25 lags both,
which is expected for noisy, short, answer-oriented web queries where lexical
overlap is often incomplete.

Because every query has one positive, misses and misorderings have a large
effect. Researchers should inspect whether failures are caused by ambiguity,
translation variation, entity/title mismatch, or retrieving a topically related
passage that does not answer the question.

### Query and Relevance Type Tendencies

Queries are short Arabic web questions. They include definitions, entity
questions, entertainment questions, medical and everyday information needs,
location questions, and meaning/usage questions. Relevant documents are compact
answer passages, often explanatory or snippet-like. A positive passage should
directly answer the question, not merely mention a keyword from it.

Lexical-heavy cases include exact names, quoted words, titles, and technical
terms. Dense-heavy cases include paraphrased answers, broad definitions, and
questions whose intent is clearer than their keywords. Hybrid retrieval helps
when both a visible anchor and semantic answer matching are needed.

### Representative Failure Modes

BM25 can retrieve passages that repeat a query term but do not answer the
question. It can also fail when the answer uses a synonym, explanation, or
translation variant rather than the query wording. Dense retrieval can retrieve
semantically related answers that resolve a neighboring question but not the
actual one. Very short queries are especially prone to ambiguity, such as a
single name, title, or word with multiple meanings.

Good hard negatives include passages sharing the main keyword but answering a
different question, passages about the same entity but the wrong attribute, and
definition snippets for a related term.

### Arabic-Specific Notes

Arabic MS MARCO retrieval involves translated web language, proper nouns,
foreign titles, abbreviations, medical terms, and everyday phrasing. Sparse
retrieval needs tokenization that preserves names and quoted terms while
handling Arabic morphology. Dense retrieval needs broad Arabic web coverage so
it can match search-like questions to answer-like passages. Transliteration
variation matters for songs, media titles, people, and products.

### Training and Leakage Notes

Training should exclude MS MARCO, BEIR, or NanoBEIR records likely to overlap
with these evaluation queries or passages. MS MARCO is a common retriever
training source, so leakage disclosure is important. Useful non-overlapping
data includes MS MARCO-style passage-ranking pairs, Arabic or multilingual web
QA retrieval, search-query to answer-passage pairs, and noisy real-user
question datasets.

### Model Improvement Hints

The main improvement target is answerability-sensitive short-query retrieval.
First-stage models should preserve exact names and technical terms while using
dense matching to find passages that answer the question in different words.
Rerankers should be trained on keyword-sharing negatives that do not answer the
query, because those are common first-stage distractors.

### Training Data That May Help

Useful training data includes non-overlapping web QA passage-ranking pairs,
Arabic search logs with answer passages, multilingual MS MARCO-style data,
definition QA, consumer-information QA, and hard negatives from the same query
term neighborhood.

### Synthetic Data Guidance

Generate concise Arabic web-style answer passages across everyday domains, then
write short realistic search questions for them. Include definitions,
abbreviations, entertainment questions, consumer advice, how-long questions,
and underspecified fragments. Positives should directly answer the information
need; hard negatives should share keywords but answer a different question.

## Example Data

| Query | Positive document |
| --- | --- |
| ما هي متلازمة الترميم [21 chars] | متلازمة التمعن. متلازمة التمعن، المعروفة أيضًا باسم مريسيزم، هي نوع من اضطرابات الأكل غير المحددة بشكل خاص، والتي تسبب إرجاع الطعام. على الرغم من أنها لا تُعرف كاضطراب أكل محدد في الدليل التشخيصي والإ... [200 / 265 chars] |
| من غنى أغنية "هنا أذهب مرة أخرى"؟ [33 chars] | للمستعمالات الأخرى، انظر هنا أذهب مرة أخرى (توضيح). "هنا أذهب مرة أخرى" هي أغنية لفريق الروك البريطاني وايتسنيك. تم إصدار الأغنية لأول مرة في ألبومهم لعام 1982، "قديسين ومذنبين"، ثم تم تسجيلها مرة أخر... [200 / 323 chars] |
| من هو دور كاميرون بويس في مسلسل ليف ومادي؟ [42 chars] | استعدوا لجلسة من الضحك الجيد، أيها الأصدقاء. في مشاهدة مسبقة حصرية لجزء من الحلقة التي ستعرض في التاسع عشر من أبريل من مسلسل 'Liv & Maddie' بعنوان 'Prom-A-Rooney'. بالطبع. في الفيديو المضحك، نرى نجم م... [200 / 313 chars] |
| أين توجد أغلبية الصحارى الكبيرة على الأرض؟ [42 chars] | بقية صحارى الأرض تقع خارج المناطق القطبية. أكبر صحراء هي صحراء الصحراء الكبرى، وهي صحراء استوائية في شمال أفريقيا. [114 chars] |
| ما معنى كلمة "copper" في سياق شرطي؟ [35 chars] | وفقًا للنتائج الحالية، يبدو أن مصطلح "كوبر" (أي ضابط شرطة، بمعنى حرفي "من يقبض") سبق مصطلح "كوب" (يُستخدم إما كفعل بمعنى القبض أو كاسم بمعنى ضابط شرطة). قد يكون لشرائط الكوبر التي كان يحملها أول رتب ش... [200 / 302 chars] |

### Public Sources

- [MS MARCO: A Human Generated MAchine Reading COmprehension Dataset](https://arxiv.org/abs/1611.09268), 2016.
- [MS MARCO dataset site](https://microsoft.github.io/msmarco/Datasets.html).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663), 2021.
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595), 2025.
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-ar](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ar)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| MS MARCO: A Human Generated MAchine Reading COmprehension Dataset | 2016 | task paper | [https://arxiv.org/abs/1611.09268](https://arxiv.org/abs/1611.09268) |
| MS MARCO dataset site |  | dataset page | [https://microsoft.github.io/msmarco/Datasets.html](https://microsoft.github.io/msmarco/Datasets.html) |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | [https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663) |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | [https://arxiv.org/abs/2502.13595](https://arxiv.org/abs/2502.13595) |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | [https://huggingface.co/collections/zeta-alpha-ai/nanobeir](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
