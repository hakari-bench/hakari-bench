# MNanoBEIR / NanoBEIR-ar / NanoNFCorpus

## Overview

NanoBEIR-ar / NanoNFCorpus is the Arabic NanoBEIR version of NFCorpus, a
medical information retrieval dataset linking consumer health topics to
scientific biomedical evidence. The original NFCorpus paper,
[A Full-Text Learning to Rank Dataset for Medical Information
Retrieval](https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf),
describes a retrieval setting where lay health and nutrition queries are linked
to PubMed/PMC-style documents. This Arabic Nano task contains 50 short health
queries, 2,953 biomedical documents, and 1,651 positive qrels. It is extremely
multi-positive: queries average 33.02 positives and one query has 100
positives. The task is therefore about broad biomedical evidence discovery,
not single-answer lookup. BM25 keeps visible health terms, dense retrieval adds
semantic biomedical neighbors, and `reranking_hybrid` gives the best top-100
coverage.

## Details

### What the Original Data Measures

NFCorpus bridges consumer-facing health topics and scientific medical
documents. Queries come from health and nutrition topics written for lay
readers, while documents are medical abstracts and article-derived evidence.
Relevance is based on whether a document is linked to the same health topic and
can serve as evidence, not whether it contains a short answer sentence.

The Arabic NanoBEIR version keeps this retrieval problem in translated form.
The retriever must map very short Arabic health phrases to long Arabic
biomedical abstracts. This requires both terminology matching and domain
semantic matching, because the query may use consumer language while the
document uses scientific phrasing.

### Observed Data Profile

The metadata records 50 queries, 2,953 documents, and 1,651 positive qrels.
There are 47 multi-positive queries, or 94.0% of the set. Positives average
33.02 per query, the median is 23.5, and the maximum is 100. Queries are very
short, averaging 22.30 characters, while documents are long biomedical
abstract-style texts averaging 1,408.18 characters. Examples include healthy
chocolate milkshakes, medical ethics, fava beans, chicken nugget composition,
and saturated fat.

This profile changes the meaning of retrieval metrics. A top-100 list can
contain many relevant abstracts but still cover only a small fraction of all
judged positives. The goal is not to retrieve one exact article; it is to cover
a broad biomedical relevance set while keeping the best evidence near the top.

### BM25 Evaluation Profile

The BM25 candidate subset reaches nDCG@10 = 0.2350, hit@10 = 0.5600, and
Recall@100 = 0.1569. BM25 is useful when a query contains a visible food,
nutrient, disease, intervention, drug, or health phrase that appears directly
in biomedical abstracts. For short Arabic queries, exact term preservation can
be the only clear anchor.

BM25's limitation is the consumer-health to biomedical-language gap. A lay
topic may correspond to abstracts using technical terms, study population
descriptions, biomarkers, outcomes, or intervention terminology. Sparse
matching can also over-rank generic medical neighbors that mention a food or
disease but do not belong to the judged evidence set. Because the task has many
positives, BM25's low Recall@100 should be read as limited evidence coverage,
not simply failure to find any relevant document.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` reaches nDCG@10 =
0.1966, hit@10 = 0.4800, and Recall@100 = 0.1605. Dense retrieval slightly
improves Recall@100 over BM25 but is weaker at top-10 ordering. This suggests
that embedding similarity expands the evidence pool modestly but does not
consistently rank the best biomedical abstracts at the top for this Arabic
translated sample.

Dense retrieval is useful for linking consumer health phrases to technical
abstract language, but it can drift toward broad biomedical similarity. A
query about saturated fat, food components, or toxins may retrieve abstracts in
the same health neighborhood without matching the specific judged topic.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset reaches nDCG@10 = 0.2343, hit@10 =
0.6000, and Recall@100 = 0.1841. Hybrid has the best hit@10 and Recall@100,
while nearly matching BM25's nDCG@10. The metadata records 9 rows with the
optional rank-101 safeguard, which is unsurprising in a task where positives
are numerous and preserving evidence coverage is difficult.

For reranker evaluation, hybrid is the most useful candidate source. It keeps
BM25's literal biomedical anchors and adds dense semantic candidates. The
reranker can then focus on ordering a diverse set of relevant and near-relevant
biomedical abstracts.

### Metric Interpretation for Model Researchers

This task should be interpreted as multi-positive biomedical evidence
retrieval. Absolute Recall@100 values are low because the denominator is large:
the average query has more than 33 positives. BM25 is strongest for top-rank
nDCG, dense adds some broader coverage, and hybrid gives the best hit@10 and
Recall@100. The results imply that exact terminology and semantic expansion are
both needed, but neither solves the evidence-coverage problem alone.

Researchers should avoid reading this task like single-positive fact retrieval.
A useful model should retrieve many relevant abstracts, rank strong evidence
near the top, and avoid generic biomedical neighbors that share vocabulary but
do not belong to the topic's evidence set.

### Query and Relevance Type Tendencies

Queries are short Arabic consumer-health or nutrition topics. They include
foods, nutrients, toxins, diseases, medical ethics, interventions, and
body-health relationships. Relevant documents are long biomedical abstracts or
technical summaries with study goals, populations, methods, measurements,
outcomes, and caveats.

Lexical-heavy cases involve exact food, disease, drug, or nutrient terms.
Dense-heavy cases involve lay-to-technical mapping where the answer passage
uses scientific wording. Hybrid retrieval is strongest when a visible health
term must be preserved while the candidate pool also needs semantically related
abstracts.

### Representative Failure Modes

BM25 can over-rank abstracts that mention a query term but investigate a
different outcome, population, intervention, or exposure. Dense retrieval can
retrieve a medically related abstract that is not part of the judged evidence
set. Both methods can under-cover broad topics with dozens of positives. The
most useful hard negatives are biomedical abstracts from the same disease,
food, intervention, or biomarker neighborhood that do not support the same
health topic.

### Arabic-Specific Notes

Arabic NFCorpus retrieval mixes translated consumer health topics, formal
biomedical abstract style, transliterated terms, English-derived names,
chemical expressions, disease names, and numeric study details. Sparse
retrieval needs tokenization that preserves biomedical terms and short food or
disease names. Dense retrieval needs Arabic medical domain coverage to connect
lay terms to scientific phrasing without smoothing away rare terminology.

### Training and Leakage Notes

Training should exclude NFCorpus, NutritionFacts, BEIR, or NanoBEIR records
likely to overlap with these evaluation health topics or documents. Useful
non-overlapping data includes NFCorpus train material, Arabic or multilingual
consumer-health to biomedical evidence pairs, BioASQ-style medical
question-to-article data, and biomedical abstract retrieval or citation-link
supervision. Multi-positive training is important because the task has many
positives per query.

### Model Improvement Hints

The main improvement target is biomedical lexical-semantic fusion with
multi-positive coverage. First-stage retrievers should preserve exact health
terms while expanding to technical abstracts that express the same evidence
topic. Rerankers should be trained on near-topic biomedical negatives and
should rank diverse relevant abstracts, not only the first positive.

### Training Data That May Help

Useful training data includes non-overlapping medical IR, consumer health QA,
Arabic biomedical retrieval, multilingual clinical abstract retrieval,
NutritionFacts-like topic-to-evidence data, and citation-linked biomedical
abstract pairs.

### Synthetic Data Guidance

Generate Arabic biomedical abstract-style passages with study population,
exposure or intervention, outcome, and measurements. Then generate short
consumer-health, nutrition, food, drug, or disease topics supported by those
documents. Include multiple positives for broad topics and hard negatives from
nearby medical areas that are not evidence for the same topic.

## Example Data

| Query | Positive document |
| --- | --- |
| ميلشيكات الشوكولاتة الصحية [26 chars] | الهدف: دراسة العلاقة بين استهلاك الكيريز وتكرار هجمات النقرس لدى الأفراد المصابين بالنقرس. الطرق: أجرينا دراسة تقاطع الحالات لدراسة العلاقات بين مجموعة من العوامل المخاطرة المحتملة مع تكرار هجمات النق... [200 / 1,438 chars] |
| الأخلاق الطبية [14 chars] | الخلفية: يبدو أن أحد المشاكل الرئيسية في التحكم في الكوليسترول في الدم من خلال التدخل الغذائي هو الحاجة إلى تحسين الالتزام بالمريض. الأهداف: استكشاف العديد من الأسئلة المتعلقة بالحواجز والمحفزات للالت... [200 / 1,557 chars] |
| فول [3 chars] | في السنوات العشرين الماضية، زادت الاهتمامات بالبيوكيمياء، التغذية، والعلاج الكيميائي للأرجينين، مما أدى إلى إجراء دراسات شاملة لاستكشاف أدواره الغذائية والعلاجية في علاج ووقاية الاضطرابات الأيضية لدى... [200 / 1,064 chars] |
| ما يحتوي على النيوجتات الدجاجية؟ [32 chars] | غرض: تحديد مكونات قطع الدجاج من 2 سلاسل غذائية وطنية. الخلفية: أصبحت قطع الدجاج مكونًا رئيسيًا في النظام الغذائي الأمريكي. حاولنا تحديد التركيبة الحالية لهذه الأطعمة المعالجة بشكل كبير. الطرق: تم اختي... [200 / 625 chars] |
| الدسم المشبع [12 chars] | الاهتمام باحتمالية أن تناول الأمهات للأغذية أثناء الحمل قد يؤثر على تطور اضطرابات الحساسية لدى الأطفال قد زادت. درس هذا الدراسة المستقبلية الارتباط بين تناول الأمهات لبعض الأغذية الغنية بالحموض الدهني... [200 / 1,884 chars] |

### Public Sources

- [A Full-Text Learning to Rank Dataset for Medical Information Retrieval](https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf), 2016.
- [NFCorpus project page](https://www.cl.uni-heidelberg.de/statnlpgroup/nfcorpus/).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663), 2021.
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595), 2025.
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-ar](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ar)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| A Full-Text Learning to Rank Dataset for Medical Information Retrieval | 2016 | task paper | [https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf](https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf) |
| NFCorpus project page |  | dataset page | [https://www.cl.uni-heidelberg.de/statnlpgroup/nfcorpus/](https://www.cl.uni-heidelberg.de/statnlpgroup/nfcorpus/) |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | [https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663) |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | [https://arxiv.org/abs/2502.13595](https://arxiv.org/abs/2502.13595) |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | [https://huggingface.co/collections/zeta-alpha-ai/nanobeir](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
