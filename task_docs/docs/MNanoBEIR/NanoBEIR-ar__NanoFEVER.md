# MNanoBEIR / NanoBEIR-ar / NanoFEVER

## Overview

NanoBEIR-ar / NanoFEVER is the Arabic NanoBEIR version of FEVER, the
Wikipedia-based fact extraction and verification benchmark introduced in
[FEVER: a large-scale dataset for Fact Extraction and
VERification](https://arxiv.org/abs/1803.05355). Each query is an Arabic
translated factual claim, and the retrieval target is an Arabic translated
Wikipedia passage containing evidence needed to support or refute that claim.
The Nano task contains 50 claims, 4,996 evidence candidates, and 57 positive
qrels. Most claims have a single positive, so the benchmark is close to
single-positive fact retrieval, but a small number of claims require multiple
evidence pages. The dominant challenge is factual specificity: the model must
retrieve the entity or event page that contains the decisive relation, not just
a page that mentions the same name.

## Details

### What the Original Data Measures

FEVER was designed to evaluate fact verification against Wikipedia. The
original dataset contains claims labeled as supported, refuted, or not enough
information, with evidence sentences annotated for supported and refuted
claims. In BEIR-style retrieval, the claim becomes the query and the retriever
must surface evidence documents before a verifier can make the label decision.

The Arabic NanoBEIR version keeps the evidence-retrieval objective while
changing the language surface through translation. The task does not ask a
retriever to decide whether a claim is true. It asks whether the retriever can
find the Arabic evidence passage that would allow a downstream fact checker to
make that decision.

### Observed Data Profile

The metadata records 50 queries, 4,996 documents, and 57 positive qrels. The
average is 1.14 positives per query, the median is 1, and only 6 queries are
multi-positive. Query text averages 40.14 characters, while documents average
1,039.03 characters. The examples include claims about a band member's
relationship to the Grateful Dead, an Indian sitcom, aircraft built in
Burbank, Nero, and the nationality of a film.

The task is strongly entity-centered. Many claims contain one or two visible
entity names, and the positive document is often a biography, work page, place
page, or organizational description. However, exact entity retrieval is not
enough: the page must contain the specific fact needed for verification, such
as a date, family relation, office, nationality, role, or classification.

### BM25 Evaluation Profile

The BM25 candidate subset reaches nDCG@10 = 0.6665, hit@10 = 0.8000, and
Recall@100 = 0.9298. BM25 performs well because short FEVER claims often expose
the entity name or key phrase that appears in the evidence passage. Arabic
translated Wikipedia pages preserve many names, titles, and named entities, so
sparse retrieval can usually find the right evidence neighborhood.

BM25's limitation is factual relation selection. It can retrieve a page with
the same entity but fail to rank the passage containing the decisive evidence
high enough. It can also be weakened by translation variation, transliterated
names, or claims whose key fact is expressed with different wording in the
document. BM25 is therefore a strong but incomplete first-stage retrieval
signal.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` reaches nDCG@10 =
0.8243, hit@10 = 0.9600, and Recall@100 = 0.9825. Dense retrieval is clearly
the strongest candidate view for this task. It improves top-rank ordering and
nearly eliminates top-100 candidate loss. This suggests that embedding
similarity is connecting short Arabic claims to evidence pages even when the
claim and document differ in wording.

The dense advantage is plausible because FEVER claims are declarative
sentences, not keyword lists. They express factual relations, and dense
representations can match that relation to an entity page or event page. The
remaining risk is semantic overreach: a dense model can retrieve a related page
about the same entity family while missing the exact evidence needed to verify
the claim.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset reaches nDCG@10 = 0.7767, hit@10 =
0.9200, and Recall@100 = 0.9825. Hybrid ties dense on Recall@100 but is weaker
on nDCG@10 and hit@10. This means the hybrid pool is useful for reranking
coverage, but dense alone is the best top-rank sorter among the provided
candidate views.

The metadata records one row with the optional rank-101 safeguard, so candidate
coverage is nearly complete but not entirely automatic. For reranker
experiments, the hybrid pool is still valuable because it contains both lexical
entity matches and dense semantic matches. A reranker can then focus on
evidence selection among plausible Wikipedia pages.

### Metric Interpretation for Model Researchers

NanoFEVER-ar shows a dense-favored retrieval pattern. BM25 is strong because
entity names are visible, but dense retrieval substantially improves nDCG@10,
hit@10, and Recall@100. Hybrid does not improve top-rank quality over dense,
which suggests that the dense candidate order is already well aligned with the
claim-to-evidence relation. For first-stage retrieval, a dense model should be
the main baseline; for reranking, the hybrid candidate pool can still be useful
because it preserves lexical alternatives.

Because the task is mostly single-positive, a missed or misordered positive has
a large effect on nDCG@10. Researchers should inspect failures at the entity
relation level: same entity but wrong fact, same title family but wrong page,
or related event but missing the claim's assertion.

### Query and Relevance Type Tendencies

Queries are short Arabic factual claims. They often name people, works, places,
organizations, media properties, offices, or historical entities. Relevant
documents are Wikipedia-style pages that contain evidence for verification. A
document is relevant if it contains the fact needed to support or refute the
claim; broad topical relatedness is insufficient.

Lexical-heavy cases contain exact names or titles. Dense-heavy cases require
mapping a claim relation to a passage that phrases the fact differently. Hybrid
retrieval matters when exact names must be preserved but semantic relation
matching is needed to select the right evidence page.

### Representative Failure Modes

BM25 can retrieve the right entity family but rank a non-evidence page above
the positive. It may also over-rank a document that repeats the entity name but
does not contain the relation stated in the claim. Dense retrieval can retrieve
a semantically related biography, work, or event page while missing the
specific subject of the claim. Translation can add another layer of difficulty
when names and titles are rendered inconsistently.

Good hard negatives include pages about the same person or work that do not
contain the target fact, pages that mention the same title but refer to a
different work, and documents that are semantically related but cannot verify
the claim.

### Arabic-Specific Notes

Arabic FEVER retrieval depends on translated named entities, transliteration
variation, definite articles, and morphology around names and titles. Sparse
retrieval needs tokenization that preserves proper nouns and work titles. Dense
retrieval needs enough Arabic factual and encyclopedic coverage to connect
short claims to longer evidence passages. Strong systems should preserve exact
entities while representing factual relations such as family membership,
occupation, nationality, authorship, dates, and offices.

### Training and Leakage Notes

Training should exclude FEVER, BEIR, and NanoBEIR records likely to overlap
with these evaluation claims or evidence passages. Useful non-overlapping data
includes FEVER-style claim/evidence pairs, Wikipedia claim verification
retrieval, Arabic or multilingual fact-checking datasets, and entity-centric
factual retrieval pairs. Reports should disclose whether FEVER or translated
FEVER-derived material was used in training.

### Model Improvement Hints

The main improvement target is relation-aware entity evidence retrieval.
First-stage retrievers should keep exact entity names while using dense
representations to match factual claims to evidence pages. Rerankers should be
trained on same-entity and same-title hard negatives so they learn to identify
the passage that actually verifies the claim.

### Training Data That May Help

Useful training data includes non-overlapping FEVER claim-evidence pairs,
Arabic Wikipedia fact-checking data, multilingual claim verification retrieval,
entity-centric QA evidence retrieval, and hard negatives from the same
Wikipedia entity neighborhood.

### Synthetic Data Guidance

Generate Arabic factual claims from non-evaluation Wikipedia passages. Cover
dates, offices, ranks, biographies, works, family relations, nationalities,
occupations, and membership relations. Positives should contain explicit
evidence for verifying the claim. Hard negatives should mention the same entity
but omit or contradict the target relation.

## Example Data

| Query | Positive document |
| --- | --- |
| كان كيث غودشو يعرف فرقة غريتفول ديد [35 chars] | الغراتفول ديد كانت فرقة روك أمريكية تشكلت في عام 1965 في بالو ألتو، كاليفورنيا. كانت الفرقة تتكون من خمسة إلى سبعة أعضاء، وكانت معروفة بأسلوبها الفريد والمتنوع الذي جمع بين عناصر الروك، والروحي، والموسيقى التجريبية، والجاز المودالي، والكونتري، والفولك، والبلوغراس، والبلوز، والريغي، وروك الفضاء، بالإضافة إلى عروضها الحية التي كانت تتميز بأداء موسيقي طويل، ولجمهورها المخلص المعروف باسم "Deadheads". كما كتب ليني كاي: "موسيقىهم تلمس أرضًا لا يعرف عنها معظم الفرق الأخرى وجودها". هذه التأثيرات المتنوعة تم دمجها في وحدة متنوعة ومذهلة جعلت الغراتفول ديد "أباء رواد عالم الفرق الموسيقية الجاز". تم تصنيف الفرقة في المرتبة 57 من قبل مجلة رولينج ستون في قائمة أعظم الفنانين على الإطلاق. تم إدخال الفرقة إلى قاعة مشاهير الروك أند رول في عام 1994، وتم إضافة تسجيل لأداء الفرقة في 8 مايو 1977 في قاعة بارتون بجامعة كورنيل إلى سجل التسجيلات الوطنية في مكتبة الكونغرس في عام 2012. باعت الغراتفول ديد أكثر من 35 مليون ألبوم في جميع أنحاء العالم. تأسست الغراتفول ديد في منطقة خليج سان فرانسيسكو في ظل ارتفاع ثقاف... [1,000 / 2,591 chars] |
| تارك ميثا كا أولتا تشما هو مسلسل كوميدي [39 chars] | تارك ميثا كا أولتا تشاشما (بالإنجليزية: تارك ميثا 'س مختلف المنظور) هو أطول مسلسل كوميدي في الهند، وهو من إنتاج شركة نيلا تيلي فيلمز برايفيت ليميتد. بدأ بثه في 28 يوليو 2008. يعرض من الأحد إلى الجمعة في الساعة 8:30 مساءً، مع إعادة البث في الساعة 11:00 مساءً وفي اليوم التالي في الساعة 3:00 مساءً على قناة ساب تي في. بدأ عرضه مرة أخرى على قناة سوني بال في 2 نوفمبر 2015 في الساعة 4:30 مساءً و8:00 مساءً كل يوم. المسلسل مستند إلى عمود "دنيا نيه أوندها تشاشما" الذي كتبه الكاتب الصحفي تارك ميثا لمجلة "تشيترليخا" الأسبوعية الغوجاراتية. [532 chars] |
| تم تصنيع طائرات سرية ومتقدمة تكنولوجياً في بيربانك، كاليفورنيا. [63 chars] | بوربانك هي مدينة تقع في مقاطعة لوس أنجلوس في جنوب كاليفورنيا، الولايات المتحدة الأمريكية، على بعد 12 ميلاً شمال غرب وسط مدينة لوس أنجلوس. بلغ عدد سكانها في تعداد عام 2010 حوالي 103,340 نسمة. المعروفة باسم عاصمة الإعلام العالمية، وهي على بعد عدة أميال شمال شرق هوليوود، تستضيف المدينة العديد من شركات الإعلام والترفيه التي لها مقرها أو مرافق إنتاج كبيرة في بوربانك، بما في ذلك شركة والت ديزني، وارنر برذرز إنترتينمنت، استوديوهات نيكيلوديون للرسوم المتحركة، إن بي سي، استوديوهات كارتون نتورك مع الفرع الغربي من كارتون نتورك، وإينسومنياك جيمز. تستضيف المدينة أيضًا مطار بوب هوب. كانت موقعًا لمشروع لوكهيد السري المعروف باسم "سكانك ووركس"، الذي أنتج بعض الطائرات الأكثر سرية وتقدمًا تكنولوجيًا، بما في ذلك طائرات التجسس يو-2 التي كشفت عن مكونات صواريخ الاتحاد السوفيتي في كوبا في أكتوبر 1962. تتكون المدينة من منطقتين مميزتين: منطقة وسط المدينة/الأراضي المرتفعة في سفوح جبال فيردوجو، ومنطقة السهول. بوربانك هي المدينة الشرقية في وادي سان فرناندو. جيران بوربانك، جلينديل، هي المدينة الغربية في وادي سان غا... [1,000 / 1,221 chars] |

### Public Sources

- [FEVER: a large-scale dataset for Fact Extraction and VERification](https://arxiv.org/abs/1803.05355), 2018.
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663), 2021.
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595), 2025.
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-ar](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ar)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| FEVER: a large-scale dataset for Fact Extraction and VERification | 2018 | task paper | [https://arxiv.org/abs/1803.05355](https://arxiv.org/abs/1803.05355) |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | [https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663) |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | [https://arxiv.org/abs/2502.13595](https://arxiv.org/abs/2502.13595) |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | [https://huggingface.co/collections/zeta-alpha-ai/nanobeir](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
