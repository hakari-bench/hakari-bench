# NanoFaMTEB-v2 / wikipedia_multilingual_fa

## Overview

`wikipedia_multilingual_fa` is a Persian Wikipedia retrieval task in NanoFaMTEB-v2. The queries are synthetic Persian information-seeking questions, and the documents are Persian Wikipedia-derived passages.

This task evaluates clean encyclopedia passage retrieval. The query and target passage usually have strong topical alignment, but the model still has to retrieve the single answer-bearing passage from a 10,000-document pool.

## Details

### What the Original Data Measures

FaMTEB includes Wikipedia retrieval among the Persian retrieval datasets. The source metadata says this task derives from Cohere's `wikipedia-2023-11` data and contains synthetically generated queries. The public task is exposed through `mteb/WikipediaRetrievalMultilingual`, and MTEB provides the retrieval evaluation framework.

The benchmark measures whether a retriever can match a generated natural-language query to the source Wikipedia passage. This is useful for evaluating encyclopedia RAG retrieval in Persian and multilingual settings.

### Observed Data Profile

This Nano split contains 200 queries, 10,000 documents, and 200 positive qrels. Each query has exactly one positive. Queries average 49.17 characters, and documents average 352.93 characters.

Observed examples ask about affective reactions before cognitive processing, architectural features of Taqavi School in Gorgan, low-tillage agriculture in the Midwestern United States, a spelling change from "Rudmehjan" to "Rudmajan", and the first chapters of Genesis. Positive documents are direct encyclopedia passages.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.8934, hit@10 of 0.9600, and recall@100 of 0.9800 with a top-500 candidate pool. This is a very strong lexical profile.

Synthetic queries often reuse entity names, technical terms, or distinctive phrases from the source passage. BM25 therefore finds most positives. Its errors are likely cases where a generated query paraphrases the passage or where several documents share the same entity or topic.

### Dense Evaluation Profile

The dense harrier-oss-270m profile reaches nDCG@10 of 0.9007, hit@10 of 0.9550, and recall@100 of 0.9750. Dense retrieval is slightly strongest on nDCG@10, while BM25 is slightly stronger on hit and recall.

This pattern suggests that semantic matching helps order the best answer passage near the top, but exact lexical matching remains highly reliable. Dense retrieval is useful when the synthetic question is phrased differently from the passage, especially for explanatory or definitional content.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate subset reaches nDCG@10 of 0.8958, hit@10 of 0.9750, and recall@100 of 0.9900. It uses 100 candidates per query, with two rank-101 safeguard positives.

Hybrid retrieval gives the best hit@10 and recall@100, while dense retrieval slightly leads nDCG@10. For reranking, the hybrid pool is the most reliable because it combines lexical entity coverage with semantic passage matching and nearly always includes the labeled positive.

### Metric Interpretation for Model Researchers

`wikipedia_multilingual_fa` is a high-baseline encyclopedia retrieval task. Because each query has exactly one positive, nDCG@10 and hit@10 directly indicate whether the answer passage is found near the top.

The three profiles are close, so small differences should be interpreted carefully. Dense retrieval is best for direct ranking quality, BM25 is highly competitive, and hybrid retrieval is best for candidate coverage. This makes the task useful as a sanity check for Persian Wikipedia retrieval rather than as the hardest benchmark in the set.

### Query and Relevance Type Tendencies

Queries are Persian synthetic questions generated from Wikipedia passages. They often ask about definitions, reasons, historical facts, geographic or architectural details, and procedural descriptions. Documents are concise encyclopedia passages.

The relevance relation is direct source-passage matching. A positive document contains the fact or explanation that motivated the generated query.

### Representative Failure Modes

BM25 may miss paraphrased generated questions that do not repeat the passage's distinctive words. Dense retrieval may retrieve a semantically related passage about the same entity but not the exact source passage. Hybrid retrieval reduces these failures, but single-positive labels make near-duplicate encyclopedia passages difficult.

Another risk is overestimating generalization from synthetic query style. A model may perform well on generated Wikipedia questions while being less robust on real user queries with misspellings or incomplete context.

### Training Data That May Help

Useful training data includes Persian Wikipedia query-passage retrieval, synthetic query generation over encyclopedia passages, multilingual Wikipedia retrieval, and hard negatives sharing the same entity or topic but omitting the requested fact.

Training should exclude this split's generated queries and positive passages.

### Model Improvement Notes

Improving this task requires reliable Persian encyclopedia retrieval. Models should preserve entity names and technical terms while supporting paraphrased questions and explanatory relations.

For reranking, the main goal is selecting the exact answer-bearing passage among related Wikipedia passages. Because candidate coverage is already high, gains mostly come from fine-grained top-rank ordering.

## Example Data

| Query | Positive document |
| --- | --- |
| واکنش‌های عاطفی چگونه بدون فرآیندهای شناختی رخ می‌دهند؟ [55 chars] | «عاطفه» می‌تواند به معنای واکنش غریزی به تحریک باشد که قبل از فرآیندهای شناختی معمولی که برای شکل‌گیری یک احساس پیچیده‌تر ضروری تلقی می‌شوند، رخ می‌دهد. رابرت بی زایونک اظهار می‌دارد که این واکنش به محرک‌ها برای انسان‌ها اولیه است و این واکنش غالب برای موجودات غیرانسانی است. Zajonc پیشنهاد می‌کند که واکنش‌های عاطفی می‌تواند بدون رمزگذاری ادراکی و شناختی گسترده رخ دهد و زودتر و با اطمینان بیشتری نسبت به قضاوت‌های شناختی انجام شود (Zajonc, 1980). [448 chars] |
| مدرسهٔ تقوی در گرگان چه ویژگی‌های معماری خاصی دارد؟ [51 chars] | مدرسهٔ تقوی، یکی دیگر از مدارس تاریخی شهر گرگان، مربوط به دورهٔ قاجار و بخشی از مجموعهٔ تقوی است. عمارت تقوی متعلق به یکی از تجار بزرگ استرآباد به نام تقی‌اُف بوده. مدرسهٔ تقوی نیز از جمله نمونه‌های نفیس معماری شهر گرگان محسوب می‌شود. این مدرسه دارای دو حیاط شمالی و جنوبی بوده که درِ شمالی به محلهٔ سرچشمه و درِ جنوبی به محلهٔ نعلبندان باز می‌شد. بنای مدرسه در ابتدا به عنوان یک منزل مسکونی ساخته شده بود و تا اواخر دورهٔ قاجار نیز کاربری مسکونی داشت. اما در دورهٔ پهلوی که مدرسهٔ علمی نوین ایجاد شد این بنا تغییر کاربری داد و به عنوان مدرسه مورد استفاده قرار گرفت. از ویژگی‌های بارز معماری این بنا می‌توان به بالکن‌های چوبی آن اشاره کرد که با استفاده از چوب خراطی شده ساخته شده‌اند و چشم‌اندازی ویژه و زیبا به بنا بخشیده‌اند. همچنین تناسب و هماهنگی درها در طبقهٔ پایین بنا که تأثیر ویژه‌ای بر ایجاد تعادل دما در بخش داخلی ساختمان داشته نشان‌دهندهٔ هوش و تبحر سازندگان این مدرسه است. [884 chars] |
| تکنیک‌های کشاورزی کم خاکورزی یا بی خاکورزی در نواحی میدوسترن ایالات متحده چگونه انجام می‌شوند؟ [94 chars] | در نواحی میدوسترن ایالات متحده، معمولاً تکنیک‌های کشاورزی کم خاکورزی یا بی خاکورزی استفاده می‌شوند. در کم خاکورزی، مزارع یکبار یا دو بار با یک ابزار شخم زنی قبل از کشت محصول یا بعد از برداشت قبلی خاکورزی می‌شوند. مزارع کشت می‌شوند و کوددهی می‌شوند. علف‌های هرز با استفاده از علف کش‌ها کنترل می‌شوند و در فصل رشد کولتیوار زده نمی‌شود. این تکنیک تبخیر رطوبت از خاک را کاهش می‌دهد و به این ترتیب رطوبت بیشتری برای گیاه فراهم می‌کند. تکنولوژی‌هایی که در پاراگراف قبل اشاره شد، کشاورزی کم خاکورزی یا بی خاکورزی را توانمند می‌کند. علف‌های هرز بر سر مواد غذایی و رطوبت با محصول رقابت می‌کنند و این سبب می‌شود آن‌ها ناخوشایند باشند. [624 chars] |

### Source Reference Table

| Source | Role |
| --- | --- |
| [FaMTEB: Massive Text Embedding Benchmark in Persian Language](https://arxiv.org/abs/2502.11571) | Persian embedding benchmark paper. |
| [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316) | General embedding benchmark framework. |
| [mteb/WikipediaRetrievalMultilingual](https://huggingface.co/datasets/mteb/WikipediaRetrievalMultilingual) | Public source dataset card. |
| [ellamind/wikipedia-2023-11-retrieval-multilingual-queries](https://huggingface.co/datasets/ellamind/wikipedia-2023-11-retrieval-multilingual-queries) | Multilingual synthetic-query source reference. |
| [hakari-bench/NanoFaMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoFaMTEB-v2) | Nano benchmark dataset containing this split. |

### Representative Snippets

| Query Pattern | Positive Document Pattern |
| --- | --- |
| A question asking how affective reactions can occur before cognitive processes. | A passage explaining affect as an instinctive reaction that may precede complex cognition. |
| A question asking about architectural features of Taqavi School in Gorgan. | A passage describing the historical school, its Qajar context, and architectural value. |
| A question asking how low-tillage or no-tillage agriculture is practiced in the Midwestern United States. | A passage explaining tillage frequency and field preparation practices. |
| A question asking why the spelling of a place name changed. | A passage discussing the historical spelling shift and possible origin of the name. |
| A question asking what the first chapters of Genesis discuss. | A passage stating that the chapters concern creation, world order, and early relations between God and people. |
