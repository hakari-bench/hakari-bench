# NanoFaMTEB-v2 / scidocs_fa

## Overview

`scidocs_fa` is a Persian scientific document retrieval task in NanoFaMTEB-v2. The queries are scientific paper titles or short scientific text snippets, and the documents are related scientific abstracts or paper summaries.

This task evaluates related-paper retrieval rather than direct fact lookup. A relevant document may use different terminology from the query but be connected by method, application, citation context, or research topic. That makes it harder than entity-based retrieval and gives all first-stage profiles relatively low scores.

## Details

### What the Original Data Measures

FaMTEB includes translated scientific retrieval datasets as part of Persian embedding evaluation. `scidocs_fa` uses `MCINext/scidocs-fa-v2`, a Persian SCIDOCS variant evaluated through the MTEB retrieval framework.

SCIDOCS-style tasks are designed to measure scientific document similarity and relatedness. In retrieval form, the query is a paper-like text, and positives are related papers. The relationship can be broader than exact evidence support, which makes semantic scientific similarity central to the task.

### Observed Data Profile

This Nano split contains 200 queries, 10,000 documents, and 986 positive qrels. Every query is multi-positive. Queries have 4.93 positives on average, with a minimum of 3, a median of 5.0, and a maximum of 5. Queries average 61.56 characters, and documents average 1,092.04 characters.

Observed examples include paper titles about data extraction from system logs, search-result visualization, content delivery algorithms, neurophysiological views of architectural experience, and PD control for robots with elastic joints. Positive documents are related abstracts from scientific or technical fields.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.1745, hit@10 of 0.5650, and recall@100 of 0.3925 with a top-500 candidate pool. Lexical retrieval is relatively weak here because related scientific papers may not repeat the exact title terms.

BM25 can still help when query and document share distinctive technical terms, such as method names, system types, or application domains. Its limitations appear when the relevant relation is conceptual: a paper may be related through citation context, task framing, or methodology even with limited surface overlap.

### Dense Evaluation Profile

The dense harrier-oss-270m profile reaches nDCG@10 of 0.1937, hit@10 of 0.5800, and recall@100 of 0.4209. Dense retrieval is modestly stronger than BM25 across the main metrics.

This pattern fits a related-paper task. Embedding similarity can capture broader scientific concepts and topical associations beyond exact terms. The gains are not large, which suggests that general-purpose dense embeddings still struggle with specialized scientific relatedness in Persian translation.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate subset reaches nDCG@10 of 0.2143, hit@10 of 0.6400, and recall@100 of 0.4371. It uses 100 candidates per query, with 25 rank-101 safeguard positives.

Hybrid retrieval is the strongest of the three profiles, but the absolute scores remain low. Combining lexical and dense signals helps capture both technical-term overlap and broader topical relatedness. The safeguard count also shows that relevant documents are often near the edge of the candidate pool rather than naturally concentrated at the top.

### Metric Interpretation for Model Researchers

`scidocs_fa` is a difficult scientific relatedness benchmark. The low nDCG@10 values indicate that ranking related papers near the top is hard for all initial profiles. Since every query has multiple positives, recall@100 is important for understanding candidate coverage.

The metric pattern suggests that hybrid search is the best starting point for reranking, while dense retrieval is better than BM25 as a direct semantic signal. Researchers should not expect exact term matching to be sufficient.

### Query and Relevance Type Tendencies

Queries are Persian scientific titles or short paper-like descriptions. Documents are longer abstracts or summaries. Topics span computer science, information retrieval, robotics, human-computer interaction, architecture, psychology, and other scientific fields.

The relevance relation is related-paper similarity. A positive document may share a method, task, research problem, or citation neighborhood with the query, even when it does not answer a specific question.

### Representative Failure Modes

BM25 may miss related papers that use different terminology. Dense retrieval may retrieve papers in the same broad field but with a different method or application. Hybrid retrieval improves coverage but can still rank general topical neighbors above more specifically related papers.

Scientific title translation can also introduce mismatched terminology, making exact word overlap less reliable and semantic matching more fragile.

### Training Data That May Help

Useful training data includes citation recommendation, scientific title-to-abstract retrieval, Persian academic search data, translated SCIDOCS pairs, and hard negatives from the same field but different subtopic or method.

Training should exclude evaluation paper IDs and qrels from this Nano split.

### Model Improvement Notes

Improving this task requires scientific-domain embeddings that capture methods, tasks, and research context. Models should represent relatedness at a paper level rather than only matching named terms or isolated keywords.

For reranking, useful signals include methodological compatibility, shared research problem, and whether the document would be a plausible citation or related-work item for the query.

## Example Data

| Query | Positive document |
| --- | --- |
| چارچوبی یکپارچه برای استخراج داده از فایل‌های گزارش سیستم‌های محاسباتی جهت مدیریت سیستم [87 chars] | یادگیری ماشین در دسته‌بندی خودکار متن دسته‌بندی خودکار (یا طبقه‌بندی) متون به دسته‌های از پیش تعریف‌شده، در ۱۰ سال گذشته با افزایش علاقه مواجه شده است، به دلیل افزایش در دسترس بودن اسناد به صورت دیجیتال و نیاز ناشی از آن برای سازماندهی آن‌ها. در جامعه تحقیقاتی، رویکرد غالب به این مسئله بر اساس تکنیک‌های یادگیری ماشین است: یک فرآیند استقرایی کلی به طور خودکار یک طبقه‌بندی‌کننده را با یادگیری ویژگی‌های دسته‌ها از مجموعه‌ای از اسناد از پیش طبقه‌بندی‌شده ایجاد می‌کند. مزایای این رویکرد نسبت به رویکرد مهندسی دانش (که شامل تعریف دستی یک طبقه‌بندی‌کننده توسط متخصصان حوزه است) عبارتند از کارایی بسیار خوب، صرفه‌جویی قابل توجه در نیروی کار متخصصان و قابلیت انتقال آسان به حوزه‌های مختلف. این بررسی به بررسی رویکردهای اصلی به دسته‌بندی متون می‌پردازد که در چارچوب پارادایم یادگیری ماشین قرار می‌گیرند. ما به تفصیل به مسائلی مربوط به سه مشکل مختلف، یعنی نمایش اسناد، ساخت طبقه‌بندی‌کننده و ارزیابی طبقه‌بندی‌کننده خواهیم پرداخت. [925 chars] |
| نقشهٔ ارتباط موضوعی: تجسم برای بهبود درک نتایج جستجو [52 chars] | طراحی برای جستجوی اکتشافی بر روی دستگاه‌های لمسی جستجوی اکتشافی کاربران را با چالش‌هایی در بیان مقاصد جستجو مواجه می‌کند، زیرا رابط‌های جستجوی فعلی نیازمند بررسی فهرست نتایج برای شناسایی مسیرهای جستجو، تایپ تکراری و بازنویسی پرسش‌ها هستند. ما در اینجا طراحی «دیوار اکتشاف» را ارائه می‌دهیم، یک رابط کاربری جستجوی مبتنی بر لمس که امکان اکتشاف تدریجی و درک عمیق‌تر فضاهای اطلاعاتی بزرگ را با ترکیب جستجوی مبتنی بر موجودیت، استفاده‌ی انعطاف‌پذیر از موجودیت‌های نتیجه به عنوان پارامترهای پرسش و پیکربندی فضایی جریان‌های جستجو که برای تعامل تجسم می‌شوند، فراهم می‌کند. می‌توان از موجودیت‌ها به طور انعطاف‌پذیر برای اصلاح و ایجاد جریان‌های جستجوی جدید استفاده کرد و آن‌ها را دستکاری کرد تا روابطشان با سایر موجودیت‌ها بررسی شود. داده‌های حاصل از آزمایش‌های مبتنی بر وظیفه که «دیوار اکتشاف» را با رابط کاربری جستجوی مرسوم مقایسه می‌کنند، نشان می‌دهند که «دیوار اکتشاف» به طور قابل توجهی فراخوانی را برای وظایف جستجوی اکتشافی بهبود می‌بخشد در حالی که دقت را حفظ می‌کند. بازخورد ذهنی از انتخاب‌های طراحی ما پش... [1,000 / 1,191 chars] |
| ریزه‌کاری‌های الگوریتمی در تحویل محتوا [38 chars] | هشینگ سازگار و درخت‌های تصادفی: پروتکل‌های ذخیره‌سازی توزیع‌شده برای کاهش نقاط داغ در وب جهان‌گستر ما مجموعه‌ای از پروتکل‌های حافظه پنهان برای شبکه‌های توزیع‌شده را توصیف می‌کنیم که می‌توانند برای کاهش یا حذف نقاط داغ در شبکه مورد استفاده قرار گیرند. پروتکل‌های ما به‌ویژه برای استفاده در شبکه‌های بسیار بزرگ مانند اینترنت طراحی شده‌اند، جایی که تأخیرهای ناشی از نقاط داغ می‌تواند شدید باشد و جایی که برای هر سرور امکان داشتن اطلاعات کامل در مورد وضعیت فعلی کل شبکه وجود ندارد. این پروتکل‌ها با استفاده از پروتکل‌های شبکه موجود مانند TCP/IP به آسانی قابل پیاده‌سازی هستند و سربار بسیار کمی دارند. این پروتکل‌ها با کنترل محلی کار می‌کنند، از منابع موجود به طور موثر استفاده می‌کنند و با رشد شبکه به طور مناسب مقیاس‌پذیر هستند. پروتکل‌های حافظه پنهان ما بر اساس نوع خاصی از هشینگ است که ما آن را هشینگ سازگار می‌نامیم. به طور خلاصه، یک تابع هشینگ سازگار، تابعی است که با تغییر دامنه تابع، تغییرات آن به حداقل می‌رسد. با توسعه توابع هشینگ سازگار خوب، ما قادر به توسعه پروتکل‌های حافظه پنهان هستیم که نیا... [1,000 / 1,200 chars] |

### Source Reference Table

| Source | Role |
| --- | --- |
| [FaMTEB: Massive Text Embedding Benchmark in Persian Language](https://arxiv.org/abs/2502.11571) | Persian embedding benchmark paper. |
| [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316) | General embedding benchmark framework. |
| [MCINext/scidocs-fa-v2](https://huggingface.co/datasets/MCINext/scidocs-fa-v2) | Public source dataset card. |
| [hakari-bench/NanoFaMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoFaMTEB-v2) | Nano benchmark dataset containing this split. |

### Representative Snippets

| Query Pattern | Positive Document Pattern |
| --- | --- |
| A paper title about extracting data from computational system log files for system management. | A related abstract about automated text categorization or information processing methods. |
| A title about topic relationship maps for improving search-result understanding. | A related abstract about exploratory search interfaces and result visualization. |
| A title about algorithmic details in content delivery. | An abstract about distributed caching, consistent hashing, and reducing web hot spots. |
| A title about architectural experience from a neurophysiological perspective. | A related abstract about affective outcomes in virtual reality exposure or embodied experience. |
| A title about PD control with online gravity compensation for robots with elastic joints. | A robotics abstract about impedance control, torque feedback, and gravity compensation. |
