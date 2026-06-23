# MNanoBEIR / NanoBEIR-ar / NanoNQ

## Overview

NanoBEIR-ar / NanoNQ is the Arabic NanoBEIR version of Natural Questions, the
open-domain question answering benchmark introduced in
[Natural Questions: A Benchmark for Question Answering
Research](https://aclanthology.org/Q19-1026/). Each query is an Arabic
translated natural search question, and the retrieval target is an Arabic
translated Wikipedia passage containing the answer evidence. The Nano task
contains 50 queries, 5,035 passages, and 57 positive qrels. Most queries have a
single positive, with a small multi-positive tail. The task tests whether a
retriever can find relation-specific answer evidence for everyday factual
questions. Dense retrieval gives the best nDCG@10, while `reranking_hybrid`
gives the best hit@10 and Recall@100.

## Details

### What the Original Data Measures

Natural Questions was built from real Google search questions and Wikipedia
evidence. Annotators selected long answers, often paragraphs or table regions,
and short answers when available. This distinguishes the task from synthetic
paragraph-based QA: the query is a naturally occurring information need, and
the evidence passage may not be written in the same wording as the question.

The Arabic NanoBEIR version turns that setup into translated passage retrieval.
The system does not output the answer string directly. It ranks passages, and a
positive passage is one that contains the answer-bearing evidence needed by a
downstream reader or QA model.

### Observed Data Profile

The metadata records 50 queries, 5,035 documents, and 57 positive qrels. The
average is 1.14 positives per query; 7 queries have multiple positives. Query
text averages 40.16 characters, and passages average 447.30 characters.
Examples ask where the Final Four is held, whether a film was originally a
Disney production, why the Angel of the North statue is located where it is,
where the Three-Fifths Compromise first appears in the U.S. Constitution, and
who sings a song with Michael Jackson.

The task is mostly single-hop factual evidence retrieval. It is less
multi-hop than HotpotQA and less noisy than MS MARCO, but it still requires
matching a question relation to a passage containing the answer. Entity overlap
is helpful but not sufficient.

### BM25 Evaluation Profile

The BM25 candidate subset reaches nDCG@10 = 0.3555, hit@10 = 0.5800, and
Recall@100 = 0.8772. BM25 can recover passages when questions contain names,
titles, places, constitutional phrases, songs, films, or other exact lexical
anchors. It is also stronger than dense on Recall@100 in this task, which shows
that exact Arabic query terms and translated proper names still preserve
important candidate coverage.

BM25's weakness is top-rank relation matching. A passage can share the entity
or title but fail to answer the requested relation: location, date, authorship,
reason, definition, or participant. This explains why BM25 coverage is useful
but top-10 ranking is weaker than dense.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` reaches nDCG@10 =
0.4600, hit@10 = 0.6600, and Recall@100 = 0.8421. Dense retrieval is the best
top-rank sorter among the single retrievers. It likely helps map Arabic
questions to answer-bearing passages even when the wording differs between the
question and the passage.

Dense retrieval's weakness is candidate coverage. It ranks strong positives
high when it finds them, but its Recall@100 is lower than BM25 and hybrid. This
suggests that some exact names, titles, or Arabic translated surface forms are
lost in the embedding neighborhood.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset reaches nDCG@10 = 0.4247, hit@10 =
0.7200, and Recall@100 = 0.9123. Hybrid is not the best nDCG@10 signal because
dense ranks the strongest positives slightly better, but it is the safest
candidate source. It has the best hit@10 and Recall@100, and the metadata
records 3 rows with the optional rank-101 safeguard.

For reranker experiments, hybrid is the preferred pool. It combines BM25's
proper-name and title coverage with dense retrieval's relation matching. A
reranker can then focus on choosing the passage that actually answers the
question.

### Metric Interpretation for Model Researchers

NanoNQ-ar separates final ranking quality from candidate coverage. Dense
retrieval has the best nDCG@10, so it is strong at placing answer-bearing
passages near the top. BM25 has better Recall@100 than dense, so lexical
anchors remain important for the first-stage pool. Hybrid has the best hit@10
and Recall@100, meaning it is strongest for candidate generation and reranking.

A model that only improves dense-like top ranking but loses rare names or
titles may be brittle. A model that only improves BM25-style coverage may still
need reranking to select the answer-bearing relation. The ideal retriever
combines exact entity preservation with semantic question-to-evidence matching.

### Query and Relevance Type Tendencies

Queries are Arabic natural questions about people, places, films, songs,
institutions, historical clauses, definitions, dates, and reasons. Relevant
documents are Wikipedia-style passages containing the answer evidence. The
question often names an entity but asks for a relation, such as who, where,
when, why, or what distinction.

Lexical-heavy cases include exact titles and names. Dense-heavy cases include
questions where the passage answers in explanatory form or uses different
wording. Hybrid retrieval is strongest when the entity anchor and the relation
must both be preserved.

### Representative Failure Modes

BM25 can retrieve a passage about the named entity but miss the relation that
answers the question. Dense retrieval can retrieve a semantically plausible
page while losing an exact title, song name, constitutional phrase, or proper
noun. Both methods can confuse nearby works, people, or events. Hard negatives
should therefore include same-entity wrong-relation passages and same-title
neighboring pages.

### Arabic-Specific Notes

Arabic NQ retrieval must handle translated Wikipedia style, proper nouns,
transliterated titles, named works, constitutional terms, and question words.
Sparse retrieval benefits from analyzers that preserve names and titles. Dense
retrieval needs Arabic factual QA coverage so it can connect question phrasing
to answer-bearing evidence. Small differences in names, articles, and
transliterations can determine whether the correct passage appears in the
candidate pool.

### Training and Leakage Notes

Training should exclude NQ, BEIR, or NanoBEIR records likely to overlap with
these evaluation questions or evidence passages. Useful non-overlapping data
includes Natural Questions training examples, Arabic or multilingual
open-domain QA retrieval pairs, Wikipedia question-to-passage supervision, and
KILT-style question-to-Wikipedia evidence pairs.

### Model Improvement Hints

The main improvement target is relation-specific evidence selection. First-stage
retrievers should preserve entity and title anchors while using dense
similarity to match the requested relation. Rerankers should be trained on
same-entity wrong-answer passages, because those are the candidates most likely
to fool a topical retriever.

### Training Data That May Help

Useful training data includes non-overlapping NQ examples, Arabic Wikipedia QA,
multilingual open-domain QA retrieval, KILT-style evidence retrieval, and
synthetic fact questions over Wikipedia-style passages with hard negatives from
the same entity neighborhood.

### Synthetic Data Guidance

Generate Arabic natural search-style factual questions from non-evaluation
Wikipedia passages. Cover who, where, when, why, what, how long, definition,
release-date, location, author, participant, and relation questions. Positives
should contain the requested answer evidence, not just the same entity.

## Example Data

| Query | Positive document |
| --- | --- |
| أين تقام أربع النهائي هذا العام؟ [32 chars] | بطولة كرة السلة للرجال في القسم الأول من الاتحاد الوطني للرياضات الجامعية لعام 2018 كانت بطولة إقصاء فردي تضم 68 فريقًا لتحديد بطل كرة السلة الجامعية للرجال في القسم الأول للاتحاد الوطني للرياضات الجامعية للعام الدراسي 2017–18. بدأت النسخة الثمانين من البطولة في 13 مارس 2018 وانتهت بمباراة النهائي في 2 أبريل في ملعب ألامودوم في سان أنطونيو، تكساس. [349 chars] |
| هل كان فيلم "ليلة مرعبة قبل عيد الميلاد" من إنتاج ديزني في البداية؟ [67 chars] | بدأ فكرة فيلم ليلة مرعبة في عيد الميلاد بقصيدة كتبها تيم بورتون في عام 1982، وهو يعمل كرسام متحرك في استوديوهات والت ديزني للرسوم المتحركة. بعد نجاح فيلم فينسنت في نفس العام، بدأت استوديوهات والت ديزني في التفكير في تطوير فيلم ليلة مرعبة في عيد الميلاد إما كفيلم قصير أو برنامج تلفزيوني خاص لمدة 30 دقيقة. عبر السنوات، استمر بورتون في العودة إلى الفكرة، وفي عام 1990، أبرم صفقة تطوير مع ديزني. بدأت الإنتاج في يوليو 1991 في سان فرانسيسكو؛ أصدرت ديزني الفيلم تحت لواء شركة تاتشستون بيكتشرز لأن الاستوديو اعتقد أن الفيلم سيكون "مظلمة ومخيفة جدًا للأطفال".[4] [556 chars] |
| لماذا يوجد تمثال الملاك الشمالي هناك؟ [37 chars] | وفقًا لـ غورملي، كان لمعنى التمثال الملاك ثلاثة جوانب: أولاً، لإظهار أن تحت موقع بنائه عمل عمال المناجم على مدى قرنين؛ ثانيًا، لاستيعاب الانتقال من عصر صناعي إلى عصر المعلومات؛ وثالثًا، لأن يكون مركزًا لأملنا وخوفنا المتطور. [224 chars] |

### Public Sources

- [Natural Questions: A Benchmark for Question Answering Research](https://aclanthology.org/Q19-1026/), 2019.
- [Google Research Natural Questions publication page](https://research.google/pubs/natural-questions-a-benchmark-for-question-answering-research/).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663), 2021.
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595), 2025.
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-ar](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ar)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Natural Questions: A Benchmark for Question Answering Research | 2019 | task paper | [https://aclanthology.org/Q19-1026/](https://aclanthology.org/Q19-1026/) |
| Google Research Natural Questions publication page |  | project page | [https://research.google/pubs/natural-questions-a-benchmark-for-question-answering-research/](https://research.google/pubs/natural-questions-a-benchmark-for-question-answering-research/) |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | [https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663) |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | [https://arxiv.org/abs/2502.13595](https://arxiv.org/abs/2502.13595) |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | [https://huggingface.co/collections/zeta-alpha-ai/nanobeir](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
