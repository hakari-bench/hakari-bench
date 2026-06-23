# NanoFaMTEB-v2 / msmarco_fa

## Overview

`msmarco_fa` is a Persian MS MARCO-style passage retrieval task in NanoFaMTEB-v2. The queries are short web-search questions, and the documents are answer-like Persian passages from a hard-negative retrieval corpus.

This task is unusual inside the Nano set because it has a small number of queries but many positives per query. It is therefore useful for studying broad answer coverage: a model must find many acceptable passages for a short query, not just one exact answer page.

## Details

### What the Original Data Measures

FaMTEB includes translated and Persian-adapted retrieval datasets to evaluate Persian text embedding models. `msmarco_fa` uses `MCINext/MSMARCO_FA_test_top_250_only_w_correct-v2`, a Persian MS MARCO-style test split prepared for passage retrieval evaluation.

The original MS MARCO retrieval setting measures whether a system can retrieve answer passages for real web-search queries. In this Persian version, the same style appears as short translated or Persian queries paired with many answer-bearing passages. The MTEB framework supplies the common retrieval evaluation protocol.

### Observed Data Profile

This Nano split contains 43 queries, 8,766 documents, and 2,826 positive qrels. Every query has multiple positives. Queries have 65.72 positives on average, with a minimum of 4, a median of 75.0, and a maximum of 100. Queries average 31.49 characters, and documents average 326.20 characters.

Observed examples include Persian web-search questions about suicide causes among military personnel, physical descriptions of pine trees, interior concrete flooring cost, declaratory judgments, and hydrogen liquefaction temperature. Documents are short answer passages, often translated from web-style informational sources.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.4737, hit@10 of 0.9070, and recall@100 of 0.4296 with a top-500 candidate pool. The high hit rate shows that lexical matching often finds at least one relevant passage. Short queries with concrete terms such as "hydrogen", "temperature", "concrete flooring", or "declaratory judgment" give BM25 useful anchors.

The lower nDCG and recall are more informative than hit@10 here. Because each query may have dozens of positives, retrieving one relevant passage is not enough to cover the relevance set. BM25 tends to favor passages that repeat the most obvious query terms, while missing paraphrased or semantically equivalent answers.

### Dense Evaluation Profile

The dense harrier-oss-270m profile reaches nDCG@10 of 0.6139, hit@10 of 0.9302, and recall@100 of 0.4922. Dense retrieval is strongest on nDCG@10 and recall@100 among the initial top-500 profiles.

This pattern matches the MS MARCO-style task design. Many positive passages answer the same intent using different wording, so embedding similarity can connect short queries to answer passages that do not share all surface words. Dense retrieval is especially helpful for translated or web-like phrases where exact token overlap is not the only relevance signal.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate subset reaches nDCG@10 of 0.6119, hit@10 of 0.9767, and recall@100 of 0.4812. It uses exactly 100 candidates per query and has no safeguard-positive rows.

Hybrid retrieval improves the chance that at least one positive appears near the top, as shown by the strongest hit@10. Its nDCG@10 is almost identical to dense retrieval, while its recall@100 is slightly lower than the dense top-500 profile because the hybrid subset is constrained to 100 candidates. For reranking work, this makes the task a compact but high-signal candidate pool.

### Metric Interpretation for Model Researchers

`msmarco_fa` should not be interpreted only through hit@10. Hit@10 is high for all three profiles because every query has many positives. nDCG@10 and recall@100 better show whether a model can rank several answer-bearing passages highly and cover the broader relevance set.

Dense retrieval is the clearest first-stage winner for ranking quality, while reranking_hybrid is best for ensuring a positive in the top 10. The gap between many positives and moderate recall@100 indicates that this task remains useful for measuring semantic coverage, not just exact answer retrieval.

### Query and Relevance Type Tendencies

Queries are short Persian web-search phrases or questions. They often name a concept, cost, definition, condition, or physical property. Relevant documents are answer passages, and many of them can satisfy the same information need.

The relevance relation is broad compared with encyclopedia QA tasks. A passage may be relevant because it gives a useful explanation, definition, cost factor, or practical answer, even if it is not a single canonical source.

### Representative Failure Modes

BM25 may retrieve passages with strong term overlap but the wrong intent. For example, a document may mention the same legal or medical phrase while answering a different question. Dense retrieval may cluster semantically nearby answers but still miss rare terms, units, or technical constraints.

Because there are many positives, another failure mode is shallow coverage. A model may retrieve a few obvious positives and still miss many alternate answer passages, which lowers recall even when hit@10 looks strong.

### Training Data That May Help

Useful training data includes Persian web-search logs, mMARCO-style translated query-passage pairs, Persian passage ranking data, and hard negatives with high lexical overlap. Query-passage pairs should include multiple valid answers per query so the model learns broad relevance coverage.

Training should exclude the 43 evaluation queries and their positive passages from this Nano split.

### Model Improvement Notes

Improving this task requires representing short Persian queries as information needs rather than as bags of keywords. Models should learn to match answer intent, units, definitions, and practical explanations across paraphrases.

For reranking, the best gains will come from distinguishing truly answer-bearing passages from topically related passages. Since many positives are acceptable, rerankers should avoid over-specializing to a single canonical wording.

## Example Data

| Query | Positive document |
| --- | --- |
| علل خودکشی در میان نظامیان [26 chars] | علائم اختلال استرس پس از سانحه می‌توانند خیلی زود پس از تجربه یک رویداد آسیب‌زا ظاهر شوند. مشکلات دیگری نیز معمولاً همراه با اختلال استرس پس از سانحه رخ می‌دهند، از جمله افسردگی، سایر اختلالات اضطرابی... [200 / 580 chars] |
| توصیف فیزیکی درخت کاج چیست؟ [27 chars] | توضیحات محصول. صنوبر چشم آبی نوزاد، یک گونه مخروطی و پرشاخه از صنوبر کلرادو با رشد یکنواخت و سوزن‌های آبی رنگ فشرده است. به طور متوسط، سالانه حدود 20 سانتی‌متر رشد عمودی دارد، در حالی که برخی از صنوبر... [200 / 371 chars] |
| هزینه کفپوش بتنی داخلی [22 chars] | برخی از عواملی که ممکن است به این هزینه اضافه کنند عبارتند از: آماده‌سازی محل و زیرسازی، دسترسی به محل، کف‌های کوچک زیر ۴۶ متر مربع، و بتن ضخیم‌تر. هزینه کف بتنی رنگی یکپارچه: ۳.۷۵ دلار به ازای هر متر... [200 / 260 chars] |
| تعریف حکم اعلامی [16 chars] | در بیشتر ایالت‌های آمریکا و کانادا، شرکت بیمه به طور کلی در این مرحله چهار گزینه اصلی دارد: ۱. دفاع بی‌قید و شرط از بیمه‌شده؛ ۲. دفاع از بیمه‌شده با قید حفظ حقوق؛ ۳. درخواست حکم قضایی مبنی بر عدم تعهد... [200 / 260 chars] |
| هیدروژن در چه دمایی به حالت مایع تبدیل می‌شود؟ [46 chars] | گاز. برای اینکه هیدروژن به مایع تبدیل شود، باید آن را تا 20.28 کلوین، که معادل -252.87 درجه سانتی‌گراد یا -434.45 درجه فارنهایت است، سرد کنید. ۶ نفر این مطلب را مفید دانسته‌اند. [177 chars] |

### Source Reference Table

| Source | Role |
| --- | --- |
| [FaMTEB: Massive Text Embedding Benchmark in Persian Language](https://arxiv.org/abs/2502.11571) | Persian embedding benchmark paper. |
| [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316) | General embedding benchmark framework. |
| [MCINext/MSMARCO_FA_test_top_250_only_w_correct-v2](https://huggingface.co/datasets/MCINext/MSMARCO_FA_test_top_250_only_w_correct-v2) | Public source dataset card. |
| [hakari-bench/NanoFaMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoFaMTEB-v2) | Nano benchmark dataset containing this split. |

### Representative Snippets

| Query Pattern | Positive Document Pattern |
| --- | --- |
| A Persian web query about causes of suicide among military personnel. | An answer passage discussing trauma, PTSD, depression, anxiety, and substance abuse risks. |
| A question asking for the physical description of a pine or conifer tree. | A descriptive passage about growth, needles, branches, and related tree characteristics. |
| A query about the cost of interior concrete flooring. | A passage listing factors that affect floor cost, such as preparation, access, area, and concrete thickness. |
| A query asking for the definition of a declaratory judgment. | A legal passage explaining options or obligations around a court declaration. |
| A question asking the temperature at which hydrogen becomes liquid. | A passage giving the liquefaction temperature in kelvin, Celsius, and Fahrenheit. |
