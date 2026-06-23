# MNanoBEIR / NanoBEIR-ar / NanoArguAna

## Overview

NanoBEIR-ar / NanoArguAna is the Arabic NanoBEIR version of ArguAna, an
argument retrieval task where the query is a long argument and the relevant
document is its best counterargument. The original ArguAna dataset was
introduced in the paper
[Retrieval of the Best Counterargument without Prior Topic
Knowledge](https://aclanthology.org/P18-1023/), and BEIR later used it as one
of its zero-shot retrieval tasks. This Nano version keeps the same retrieval
shape in Arabic translated form: 50 long Arabic debate arguments retrieve from
3,635 Arabic counterargument candidates, with exactly one positive qrel per
query. The task is difficult because topic similarity alone is insufficient. A
good retriever must identify the same controversial issue, preserve the
argument's main aspects, and prefer an opposing stance rather than a same-side
supporting argument.

## Details

### What the Original Data Measures

ArguAna frames retrieval as finding a counterargument for an input argument on
an arbitrary topic. The original paper emphasizes that a strong counterargument
usually discusses the same aspects as the query while taking the opposite
position. This makes the task different from duplicate-question retrieval,
ordinary topical search, or passage retrieval for answer evidence. A document
can be topically similar and still be wrong if it supports the query's stance,
addresses only a loosely related issue, or attacks a different premise.

The Arabic NanoBEIR task inherits that design through the multilingual NanoBEIR
adaptation. The retrieved item is a translated Arabic debate-style passage, not
a short answer span. The benchmark therefore tests whether retrieval models can
represent long argumentative structure: claim, premise, evidence, consequence,
value judgment, feasibility, and stance opposition.

### Observed Data Profile

The metadata records 50 queries, 3,635 documents, and 50 positive qrels. Every
query has exactly one positive document, so this is a single-positive retrieval
task. Queries average 898.62 characters and documents average 857.03
characters, making both sides much longer than typical factoid passage
retrieval. The examples include debates about House of Lords reform, airport
expansion, advertising and choice, cyber attacks, religious speech, alternative
medicine, gender and labor, compulsory voting, and school nutrition.

This shape makes the ranking highly sensitive to top-10 ordering. Because there
is only one judged positive per query, a candidate set can have high top-100
coverage while still scoring poorly if it ranks same-topic distractors above
the actual counterargument. The useful retrieval signal is not merely "same
topic"; it is "same topic, opposite argumentative move."

### BM25 Evaluation Profile

The BM25 candidate subset reaches nDCG@10 = 0.3619, hit@10 = 0.6600, and
Recall@100 = 0.9000. BM25 is helpful because long Arabic arguments share many
topic words, named entities, policy terms, and phrase fragments with their
counterarguments. If the query discusses Heathrow, cyber attacks, advertising,
or religious speech, sparse matching can often keep the relevant debate
neighborhood inside the candidate pool.

BM25's limitation is that lexical overlap does not distinguish stance. Same-side
arguments, neutral background passages, and adjacent debate points can share the
same vocabulary as the true counterargument. In ArguAna, high term overlap can
even be misleading because both supporting and opposing arguments often repeat
the same issue framing. BM25 is therefore a useful first-stage topic anchor, but
not a reliable final ranker for counterargument selection.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` reaches nDCG@10 =
0.4295, hit@10 = 0.7600, and Recall@100 = 0.9000. Dense retrieval is stronger
than BM25 at the top of the ranking. This suggests that embedding similarity is
capturing more than shared terms: it can identify argumentative relatedness,
premise-level correspondence, and paraphrased statements across long translated
Arabic passages.

Dense retrieval still has a coverage ceiling here, matching BM25 at Recall@100.
Its likely failure mode is semantic neighbor confusion. A dense model may rank a
passage that is broadly about the same policy or social issue but does not
actually counter the query's claim. It can also blur stance direction if the
embedding space treats two arguments as similar because they discuss the same
aspects, even when one supports and the other attacks the claim.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset reaches nDCG@10 = 0.4188, hit@10 =
0.7400, and Recall@100 = 0.9200. Hybrid is not the strongest top-rank sorter
because dense has higher nDCG@10 and hit@10, but it has the best top-100
coverage. The metadata also records 4 rows with the optional rank-101 safeguard,
showing that a small number of positives needed explicit preservation at the
candidate boundary.

For reranker research, this hybrid pool is useful because it brings together
lexical topic anchors from BM25 and semantic counterargument candidates from
dense retrieval. A reranker evaluated on this pool is asked to decide which
candidate is the actual opposing argument, not merely whether a candidate talks
about the same debate.

### Metric Interpretation for Model Researchers

This task separates stance-sensitive ranking from candidate coverage. Dense
leading nDCG@10 and hit@10 means that semantic representations are more useful
than sparse overlap for ordering the best counterargument near the top. BM25
and dense tying at Recall@100 means both retrieval families miss some positives
by the top-100 cutoff. Hybrid improving Recall@100 to 0.9200 means the two
signals recover partly complementary candidates, even though hybrid's top-10
ordering is slightly weaker than dense alone.

For first-stage retrievers, the main target is to keep the correct debate
neighborhood while improving stance-aware semantic ranking. For rerankers, the
main target is to distinguish same-topic same-stance passages from true
counterarguments. A model that performs well on ordinary semantic similarity
may still fail this task if it cannot represent attack, rebuttal, concession,
or contradiction relations.

### Query and Relevance Type Tendencies

Queries are long Arabic debate arguments with claims and supporting reasoning.
Relevant documents are long Arabic passages that oppose the query by attacking
a premise, presenting a contrary consequence, questioning feasibility, shifting
the value tradeoff, or denying the claimed harm or benefit. The examples show
that many positives reuse the same issue vocabulary while reversing the
argumentative direction.

Lexical-heavy cases are those with distinctive topic anchors such as airport
names, institutions, legal terms, or technical policy vocabulary. Semantic-heavy
cases are those where the counterargument uses different wording but addresses
the same underlying premise. The strongest systems should treat relevance as a
counterargument relation, not as broad topical similarity.

### Representative Failure Modes

BM25 can over-rank passages that repeat the query's policy vocabulary but do not
oppose the claim. It may retrieve a supporting argument, a background passage,
or a different objection within the same debate. Dense retrieval can over-rank
semantically close arguments that discuss the same issue while missing stance
direction. In Arabic translation, additional errors can come from long sentence
structure, repeated discourse markers, and translated debate phrasing that
makes multiple candidates look similarly related.

Good hard negatives for this task include same-topic same-stance arguments,
arguments that attack a different premise, and counterarguments that are
opposed but not the best match for the query's specific reasoning.

### Arabic-Specific Notes

Arabic retrieval depends on tokenization, normalization, clitic handling,
orthographic variation, and translated discourse style. Sparse retrieval needs
to preserve topic terms while handling inflection and attached function words.
Dense retrieval needs enough Arabic and multilingual argument data to recognize
stance opposition in long passages. Because both query and document are long,
models also need robust pooling or late-interaction behavior; a single salient
topic phrase should not dominate the representation if the actual relevance is
in the argumentative relation.

### Training and Leakage Notes

Training should exclude ArguAna, BEIR, NanoBEIR, and translated idebate-derived
records likely to overlap with these evaluation arguments or counterarguments.
Useful non-overlapping data includes argument-counterargument pairs, Arabic or
multilingual pro/con debate responses, stance-classified argument datasets, and
argument attack/support relation data. Generic sentence-similarity or
paraphrase-only data is not enough and may be harmful if it teaches the model to
prefer same-stance similarity.

### Model Improvement Hints

The main improvement target is stance-aware lexical-semantic retrieval. A good
first-stage model should keep the topic anchors that BM25 preserves, while
dense representations should identify which candidate attacks the query's
specific claim. Rerankers should be trained on same-topic hard negatives with
different stance and attack relations. Pairwise losses may be especially useful
when comparing a true counterargument against a topically similar same-stance
candidate.

### Training Data That May Help

Useful training data includes non-overlapping argument-counterargument pairs,
Arabic or multilingual pro/con debate responses, stance-classified argument
datasets, argument attack/support relation data, and synthetic debate pairs
with same-topic hard negatives. Training examples should include both long
queries and long candidate passages so the model learns document-level argument
matching rather than sentence-level paraphrase.

### Synthetic Data Guidance

For document-to-query generation, start from non-evaluation debate arguments
and generate Arabic opposing arguments that attack a premise, consequence,
value judgment, or feasibility claim. For joint generation, create debate
topics with multiple long arguments on both sides, label the best
counterargument for each query, and include same-topic same-stance negatives.
The positive should be a counterargument, not a supporting paraphrase or merely
related policy discussion.

## Example Data

| Query | Positive document |
| --- | --- |
| الجمهور غير مهتم بالتغيير. ما إذا كان يجب أن يكون إصلاح مجلس اللوردات أولوية قصوى في الظروف الاقتصاد... [100 / 434 chars] | الحملة الانتخابية لا يمكن مقارنتها بإصلاح النظام السياسي. بالإضافة إلى ذلك، لا يجب الخلط بين الجمهور غير المعلومات بسبب التأثير السياسي واللامبالاة. غالبًا ما يعبر الناخبون عن شعورهم باليأس لأنهم يشعر... [200 / 366 chars] |
| توسيع مطار هيثرو ضروري للاقتصاد، حيث سيضمن الحفاظ على العديد من الوظائف الحالية وسيخلق وظائف جديدة.... [100 / 933 chars] | المجتمع التجاري بعيد عن الوحدة في دعمه المزعوم لممر جوي ثالث. تشير الاستطلاعات إلى أن العديد من الأعمال المؤثرة لا تدعم التوسعة. وقع رسالة تعبر عن القلق جاستن كينغ، الرئيس التنفيذي لشركة ج ساينزبوري،... [200 / 877 chars] |
| الناس يُعطون خيارات كثيرة جداً، مما يجعلهم أقل سعادة. الإعلانات تؤدي إلى إرهاق العديد من الناس بسبب... [100 / 767 chars] | الناس غير سعداء لأنهم لا يمكنهم الحصول على كل شيء، وليس لأنهم يشعرون بالتوتر من كثرة الخيارات. في الواقع، تلعب الإعلانات دورًا حاسمًا في توجيه الناس إلى إنفاق ما يملكونه من مال على المنتج الأكثر ملاءم... [200 / 759 chars] |
| الهجمات الإلكترونية غالبًا ما تُنفذها كيانات غير حكومية مثل الإرهابيين السيبرانيين أو الهاكتيفيست (ا... [100 / 860 chars] | في حالة هجمات الفاعلين غير الدوليين، يتفق العديد من الخبراء في القانون الدولي على أن الدولة يمكنها الرد دفاعًا عن النفس إذا كانت دولة أخرى 'غير مستعدة أو غير قادرة على اتخاذ إجراءات فعالة' لمواجهة اله... [200 / 479 chars] |
| لأن الدين يعزز يقين الاعتقاد، فإن الكراهية الإلهية الملهمة سهلة الاستخدام لتبرير وتعزيز الأفعال العن... [100 / 1,158 chars] | لا أحد يُجبر على ارتكاب أعمال العنف بسبب كلام شخص آخر؛ إنه اختيارهم القيام بذلك. بالمثل، هناك العديد من الأشخاص الذين قد يؤيدون آراء يمكن اعتبارها معادية للمثليين ولكنهم سيشعرون بالصدمة من أعمال العنف... [200 / 495 chars] |

### Public Sources

- [Retrieval of the Best Counterargument without Prior Topic Knowledge](https://aclanthology.org/P18-1023/), 2018.
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663), 2021.
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595), 2025.
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-ar](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ar)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Retrieval of the Best Counterargument without Prior Topic Knowledge | 2018 | task paper | [https://aclanthology.org/P18-1023/](https://aclanthology.org/P18-1023/) |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | [https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663) |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | [https://arxiv.org/abs/2502.13595](https://arxiv.org/abs/2502.13595) |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | [https://huggingface.co/collections/zeta-alpha-ai/nanobeir](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
