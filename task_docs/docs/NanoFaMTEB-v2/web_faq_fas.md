# NanoFaMTEB-v2 / web_faq_fas

## Overview

`web_faq_fas` is a Persian WebFAQ retrieval task in NanoFaMTEB-v2. The queries are Persian FAQ-style questions, and the documents are short answer passages from FAQ pages.

This task evaluates practical question-answer retrieval from web FAQ content. It is a high-baseline task: questions and answer passages often share domain terms, but the correct answer still has to be distinguished from nearby FAQ items about the same topic.

## Details

### What the Original Data Measures

FaMTEB includes web and RAG-style retrieval datasets for Persian embedding evaluation. The source metadata describes `mteb/WebFAQRetrieval` as broad-coverage natural question-answer pairs gathered from FAQ pages in many languages. MTEB provides the common retrieval evaluation framework.

The task measures whether a retriever can map a user-facing FAQ question to its answer passage. This setting resembles customer-support and public information RAG systems, where a short user question should retrieve the correct knowledge-base answer.

### Observed Data Profile

This Nano split contains 200 queries, 10,000 documents, and 200 positive qrels. Each query has exactly one positive. Queries average 48.01 characters, and documents average 209.60 characters.

Observed examples ask about lipomatic surgery pain and bleeding, newborn vision distance, whether all people have talent, laboratory animal blood collection services, and Windows startup settings. Positive documents are direct FAQ answers.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.8680, hit@10 of 0.9350, and recall@100 of 0.9900 with a top-500 candidate pool. This is a very strong lexical profile.

FAQ question-answer pairs often repeat key terms from the user's question. Domain words such as procedure names, operating-system terms, service names, or health concepts give BM25 reliable anchors. Its remaining failures are likely cases where answers paraphrase the question or where many FAQ entries share the same topic terms.

### Dense Evaluation Profile

The dense harrier-oss-270m profile reaches nDCG@10 of 0.8756, hit@10 of 0.9250, and recall@100 of 0.9600. Dense retrieval slightly improves nDCG@10 over BM25 but has lower hit and recall.

This indicates that semantic matching helps order answer passages when wording differs, but exact lexical coverage remains valuable. Dense retrieval can prefer an answer that satisfies the intent, yet it may miss some exact FAQ items that BM25 captures through distinctive terms.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate subset reaches nDCG@10 of 0.9029, hit@10 of 0.9700, and recall@100 of 1.0000. It uses exactly 100 candidates per query and has no safeguard-positive rows.

Hybrid retrieval is strongest across all key metrics. It combines BM25's exact FAQ-term recall with dense intent matching, and every positive appears in the top-100 hybrid candidate pool. This makes `web_faq_fas` a clean reranking benchmark where candidate misses should not dominate.

### Metric Interpretation for Model Researchers

`web_faq_fas` is a practical FAQ retrieval task with high candidate coverage. Because each query has one positive, nDCG@10 and hit@10 directly measure whether the correct FAQ answer is near the top.

The metric pattern shows that hybrid search is the best first-stage or reranking pool. BM25 and dense retrieval are both strong, but neither alone matches the combined profile. Researchers should use this task to test exact FAQ matching, paraphrase handling, and answer sufficiency.

### Query and Relevance Type Tendencies

Queries are short Persian FAQ-style questions, often about health, services, technology, consumer issues, or definitions. Documents are answer snippets that usually explain the procedure, fact, or practical instruction.

The relevance relation is direct answerability. A passage about the same subject is not enough if it does not answer the exact question.

### Representative Failure Modes

BM25 may retrieve an FAQ answer that repeats the same domain terms but addresses a different aspect of the topic. Dense retrieval may retrieve a semantically related answer but miss a precise operational detail. Hybrid retrieval reduces these issues, but reranking still needs to select the answer that directly resolves the question.

Single-positive labels also make near-duplicate FAQ items risky: a model may retrieve a plausible answer that is not the labeled positive.

### Training Data That May Help

Useful training data includes Persian FAQ retrieval, web question-answer pairs, customer-support knowledge-base retrieval, public service FAQs, and hard negatives from the same product, topic, or definition family.

Training should exclude the evaluation rows from this split.

### Model Improvement Notes

Improving this task requires a balance between exact keyword matching and answer-intent matching. Models should preserve domain terms while recognizing when an answer paraphrases the question.

For reranking, answer sufficiency is the core signal. The selected passage should be the one a RAG assistant could use to answer the user without needing additional context.

## Example Data

| Query | Positive document |
| --- | --- |
| آیا عمل لیپوماتیک با درد و خونریزی همراه است؟ [45 chars] | در عمل لیپوماتیک سوراخ های کوچکی ایجاد می‌شود. سپس لوله مخصوصی به زیر پوست برده می‌شود تا چربی‌ها را بیرون بکشد. این برش‌ها، به طول ۲ تا ۵ میلی‌متر خواهند بود و درد و خونریزی بسیار کمی در پی دارند و خ... [200 / 231 chars] |
| نوزاد تا چه فاصله ای را می بیند؟ [32 chars] | بدیهی است نوزادی که تازه به دنیا آمده شما را با حس بینایی تشخیص نمی‌دهد، زیرا این اولین نگاه او به چهره شما است. نوزادان تازه متولد شده فقط می‌توانند تا فاصله حدود ۳۰ سانتی‌متری را ببینند. این بهترین... [200 / 267 chars] |
| آیا همه افراد جامعه با استعداد هستند؟ [37 chars] | پاسخ به این سوال که آیا همه افراد جامعه با استعداد هستند کاملا مثبت بوده و با کشف موضوعات مورد علاقه افراد خواهید دید که چه پیشرفت هایی را در زمینه های مختلف کسب خواهند کرد. هر کدام از ما انسان ها در... [200 / 507 chars] |
| مرکز خدمات حیوانات آزمایشگاهی جهت خونگیری را معرفی کنید [55 chars] | شما میتوانید انجام امور خدمات مرتبط با آزمایشگاه حیوانات آزمایشگاهی را به شرکت بافت و ژن پاسارگاد (هیستوژن ) برون سپاری کنید [124 chars] |
| آیا تنظیمات استارتاپ ویندوز هشت و ده متفاوت است؟ [48 chars] | تنظیمات Advanced Startup Options ویندوز هشت و ویندوز ده تقریبا مشابه است و تفاوت زیادی با همدیگر ندارند ، مگر برخی امکانات ریکاوری کل ویندوز و بحث Reset و Refresh کردن که شاید کمی متفاوت عمل کنند اما... [200 / 217 chars] |

### Source Reference Table

| Source | Role |
| --- | --- |
| [FaMTEB: Massive Text Embedding Benchmark in Persian Language](https://arxiv.org/abs/2502.11571) | Persian embedding benchmark paper. |
| [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316) | General embedding benchmark framework. |
| [mteb/WebFAQRetrieval](https://huggingface.co/datasets/mteb/WebFAQRetrieval) | Public source dataset card. |
| [PaDaS Lab Hugging Face organization](https://huggingface.co/PaDaS-Lab) | Related source organization referenced by the task documentation. |
| [hakari-bench/NanoFaMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoFaMTEB-v2) | Nano benchmark dataset containing this split. |

### Representative Snippets

| Query Pattern | Positive Document Pattern |
| --- | --- |
| A question asking whether lipomatic surgery involves pain or bleeding. | An FAQ answer explaining small incisions, fat removal tubes, and low pain or bleeding risk. |
| A question asking how far a newborn can see. | An answer explaining that newborns see best at roughly face-to-face distance. |
| A question asking whether everyone in society has talent. | An answer discussing discovering interests and developing abilities. |
| A question asking for a laboratory animal blood collection service center. | A short answer naming a company that can handle laboratory animal services. |
| A question asking whether Windows 8 and Windows 10 startup settings differ. | An answer explaining that advanced startup options are mostly similar, with some recovery differences. |
