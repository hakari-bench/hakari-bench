# NanoFaMTEB-v2 / treccovid_fa

## Overview

`treccovid_fa` is a Persian biomedical retrieval task in NanoFaMTEB-v2 based on TREC-COVID. The queries are COVID-19 information needs, and the documents are Persian biomedical abstracts or article passages.

This task evaluates broad scientific literature retrieval for COVID-19 topics. Each query has many relevant documents, so the task is less about finding a single answer and more about ranking a useful set of biomedical articles for a topic.

## Details

### What the Original Data Measures

FaMTEB includes translated BEIR-style retrieval datasets as Persian evaluation resources. `treccovid_fa` uses `MCINext/trec-covid-fa-v2`, a Persian TREC-COVID retrieval variant evaluated through the MTEB retrieval framework.

TREC-COVID was designed for searching the COVID-19 scientific literature. Its topics include treatments, diagnostics, transmission, risk factors, public datasets, clinical course, and biomedical mechanisms. In this Persian variant, the retrieval problem is represented through translated or Persian-rendered biomedical queries and abstracts.

### Observed Data Profile

This Nano split contains 50 queries, 10,000 documents, and 4,623 positive qrels. Every query is multi-positive. Queries have 92.46 positives on average, with a minimum of 14, a median of 100.0, and a maximum of 100. Queries average 64.58 characters, and documents average 1,210.70 characters.

Observed examples ask about evidence for dexamethasone as a COVID-19 treatment, coronavirus stability on surfaces, social distancing effectiveness, serological tests for coronavirus antibodies, and biomarkers predicting severe COVID-19. Positive documents are biomedical abstracts or review-style passages.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.3519, hit@10 of 0.8800, and recall@100 of 0.2029 with a top-500 candidate pool. The high hit rate shows that biomedical terms such as SARS-CoV-2, COVID-19, dexamethasone, antibodies, and biomarkers provide useful lexical anchors.

The low recall@100 is the key feature of this task. Each query has many positives, and the top 100 can cover only a fraction of them. BM25 may retrieve articles that repeat the topic terms while missing other relevant abstracts that use different terminology or discuss another aspect of the same information need.

### Dense Evaluation Profile

The dense harrier-oss-270m profile reaches nDCG@10 of 0.3594, hit@10 of 0.9000, and recall@100 of 0.2379. Dense retrieval is slightly stronger than BM25 across the main metrics.

This suggests that embedding similarity helps connect COVID-19 information needs to biomedical abstracts beyond exact word overlap. Dense retrieval is useful when a relevant article discusses the same treatment, diagnostic method, or public-health intervention using a different phrasing. The improvement is modest because exact biomedical terminology remains important.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate subset reaches nDCG@10 of 0.4161, hit@10 of 0.9400, and recall@100 of 0.2557. It uses exactly 100 candidates per query and has no safeguard-positive rows.

Hybrid retrieval is the strongest profile for this task. Combining exact biomedical term matching with dense semantic retrieval improves both top-10 ranking and relevant coverage. The absolute recall remains low because the relevance sets are extremely large, but the hybrid pool is the best starting point for reranking.

### Metric Interpretation for Model Researchers

`treccovid_fa` should be read as a many-positive biomedical literature search task. Hit@10 is not enough because most systems can find at least one relevant abstract. nDCG@10 shows how useful the first page is, while recall@100 shows how much of the broad relevance set is covered.

The metric pattern shows a clear hybrid advantage. Dense retrieval is slightly better than BM25, but the best behavior comes from combining term precision with semantic coverage. Researchers should be careful when comparing recall values because each query may have up to 100 positives.

### Query and Relevance Type Tendencies

Queries are Persian biomedical information needs about COVID-19, public health, treatments, diagnostics, transmission, and clinical outcomes. Documents are long scientific abstracts, reviews, or article summaries.

The relevance relation is topical and evidence-oriented. A positive document may answer the query directly, provide supporting evidence, or discuss a relevant clinical or biological aspect of the topic.

### Representative Failure Modes

BM25 may over-rank articles that repeat COVID-19 terms but are not focused on the requested relation. Dense retrieval may retrieve broad pandemic articles that are semantically close but not medically specific enough. Hybrid retrieval improves ranking but still cannot cover all relevant abstracts in the top 100.

Because the relevance sets are large, a model can look strong on hit@10 while failing to retrieve diverse evidence across treatment, mechanism, clinical study, and public-health angles.

### Training Data That May Help

Useful training data includes Persian biomedical retrieval, translated TREC-COVID topics, COVID-19 literature QA, scientific abstract search, and hard negatives sharing COVID-19 terminology but not the requested relation.

Training should exclude this split's topics, qrels, and positive abstracts.

### Model Improvement Notes

Improving this task requires both biomedical vocabulary preservation and semantic topic coverage. Models should handle disease names, drug names, diagnostics, clinical study language, and public-health interventions.

For reranking, the goal is not only to find one relevant abstract but to prioritize diverse, highly relevant evidence. A strong reranker should distinguish treatment evidence, diagnostic evidence, transmission studies, and general COVID-19 background.

## Example Data

| Query | Positive document |
| --- | --- |
| چه شواهدی مبنی بر استفاده از دگزامتازون به عنوان درمان کووید-۱۹ وجود دارد؟ [74 chars] | بررسی نظام‌مند و آماری کارآزمایی‌های درمانی بیماری کووید-۱۹ این مرور سیستماتیک و متاآنالیز، داده‌های فعلی مربوط به کارآزمایی‌های بالینی کنترل‌شده انسانی برای درمان کووید-۱۹ را جمع‌آوری می‌کند. یک جستجوی الکترونیکی در منابع علمی، مطالعات مربوط به کارآزمایی‌های بالینی کنترل‌شده انسانی با کووید-۱۹ را گردآوری کرد. داروهای مورد ارزیابی شامل لوپیناویر/ریتوناویر، آربیدول، هیدروکسی‌کلروکین، توسیلیزوماب، فاوپیراویر، هپارین و دگزامتازون بودند. تجزیه و تحلیل‌های آماری برای نقاط پایانی رایج پاکسازی ویروس در صورت امکان انجام شد. لوپیناویر/ریتوناویر تأثیر معنی‌داری بر پاکسازی ویروس در موارد کووید-۱۹ نشان نداد (OR 0.95 [95% CI 0.50–1.83]). هیدروکسی‌کلروکین نیز تأثیر معنی‌داری بر میزان پاکسازی ویروس کووید-۱۹ نشان نداد (OR 2.16 [95% CI 0.80–5.84]). آربیدول تفاوت معنی‌داری در پاکسازی ویروس در روزهای ۷ (OR 1.63 [95% CI 0.76–3.50]) یا ۱۴ (OR 5.37 [95% CI 0.35–83.30]) در مقایسه با لوپیناویر/ریتوناویر نشان نداد. بررسی منابع علمی نشان داد که با لوپیناویر/ریتوناویر، آربیدول، هیدروکسی‌کلروکین یا رم‌دسیویر، بهب... [1,000 / 1,536 chars] |
| ویروس کرونا چه مدت روی سطوح پایدار می‌ماند؟ [43 chars] | راهنمای کووید-۱۹: یک همه‌گیری جهانی ناشی از ویروس کرونای جدید SARS-CoV-2 ظهور سویه SARS-CoV-2 از کروناویروس انسانی، جهان را به میانه یک همه‌گیری جدید انداخته است. این ویروس در بدن انسان باعث بیماری کووید-۱۹ می‌شود، بیماری که با تنگی نفس، تب و ذات‌الریه مشخص می‌شود و می‌تواند در افراد آسیب‌پذیر کشنده باشد. SARS-CoV-2 دارای ویژگی‌های کروناویروس‌های انسانی گذشته است و شباهت‌های ژنومی نزدیکی با SARS-CoV، ویروسی که باعث بیماری SARS می‌شود، دارد. مانند این کروناویروس‌های مرتبط، SARS-CoV-2 از طریق استنشاق قطرات و تماس با سطوح آلوده منتقل می‌شود. در سراسر جهان، آزمایشگاه‌ها در حال توسعه واکسن‌های کاندید برای این ویروس هستند – با آزمایش‌های واکسن در ایالات متحده و بریتانیا در حال انجام – و داروهای مختلف را برای درمان‌های احتمالی و پیشگیری در نظر می‌گیرند. در اینجا، ما با تجزیه و تحلیل ویروس‌شناسی، اپیدمیولوژی و روش‌های انتقال SARS-CoV-2، مروری بر آن ارائه می‌دهیم و در عین حال پیشرفت‌های فعلی روش‌های آزمایش و درمان‌های احتمالی از طریق داروها و واکسن‌ها را بررسی می‌کنیم. [975 chars] |
| آیا فاصله‌گذاری اجتماعی در کند کردن شیوع کووید-۱۹ تأثیر داشته است؟ [66 chars] | افزایش تشخیص همراه با فاصله‌گذاری اجتماعی و برنامه‌ریزی ظرفیت بهداشتی، بار موارد و مرگ‌ومیر ناشی از کووید-۱۹ را کاهش می‌دهد: یک مطالعه اثبات مفهوم با استفاده از مدل شبیه‌سازی محاسباتی تصادفی. هدف: در غیاب واکسن، همه‌گیری بیماری کرونا 2019 (COVID-19) از طریق تدابیری غیردارویی به نام فاصله‌گذاری اجتماعی (SD) مهار می‌شود. با این حال، اینکه آیا خودِ فاصله‌گذاری اجتماعی برای مسطح کردن منحنی همه‌گیری کافی است یا خیر، قابل بحث است. با استفاده از یک مدل شبیه‌سازی محاسباتی تصادفی، تأثیر افزایش فاصله‌گذاری اجتماعی، تخت‌های بیمارستانی و میزان تشخیص COVID-19 را در پیشگیری از موارد و مرگ‌ومیرهای COVID-19 بررسی کردیم. طراحی و روش تحقیق: مدل شبیه‌سازی تصادفی با استفاده از بسته EpiModel در R ساخته شد. به عنوان یک مطالعه اثبات مفهوم، شبیه‌سازی را بر روی کاسارگود، آسیب‌دیده‌ترین منطقه در کرالا، اجرا کردیم. ما 3 بخش به مدل SEIR اضافه کردیم تا به یک مدل SEIQHRF (آسیب‌پذیر-در معرض-عفونی-قرنطینه شده-بستری شده-بهبود یافته-مرگ) دست یابیم. نتایج: اجرای صرفاً فاصله‌گذاری اجتماعی، فقط زمان ظهور اوج شیوع موارد CO... [1,000 / 1,491 chars] |

### Source Reference Table

| Source | Role |
| --- | --- |
| [FaMTEB: Massive Text Embedding Benchmark in Persian Language](https://arxiv.org/abs/2502.11571) | Persian embedding benchmark paper. |
| [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316) | General embedding benchmark framework. |
| [MCINext/trec-covid-fa-v2](https://huggingface.co/datasets/MCINext/trec-covid-fa-v2) | Public source dataset card. |
| [hakari-bench/NanoFaMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoFaMTEB-v2) | Nano benchmark dataset containing this split. |

### Representative Snippets

| Query Pattern | Positive Document Pattern |
| --- | --- |
| A question asking what evidence exists for dexamethasone as a COVID-19 treatment. | A systematic review or clinical-trial summary discussing treatments for COVID-19. |
| A question asking how long coronavirus remains stable on surfaces. | A biomedical or guidance passage about SARS-CoV-2 properties and disease context. |
| A question asking whether social distancing slowed COVID-19 spread. | A modeling or public-health article about social distancing, testing, capacity planning, and reduced cases or deaths. |
| A question asking whether serological tests detect coronavirus antibodies. | A review passage about serodiagnostics and host antibody detection for SARS-CoV-2. |
| A question asking which biomarkers predict severe COVID-19 clinical course. | A cohort-study abstract about clinical features and predictors in severe SARS-CoV-2 pneumonia. |
