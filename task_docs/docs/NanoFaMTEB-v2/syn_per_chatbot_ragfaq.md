# NanoFaMTEB-v2 / syn_per_chatbot_ragfaq

## Overview

`syn_per_chatbot_ragfaq` is a synthetic Persian chatbot RAG FAQ retrieval task in NanoFaMTEB-v2. The query is a Persian user-chatbot conversation or latest user message, and the target document is the FAQ-style question-answer entry that should be retrieved.

This task evaluates conversation-to-knowledge-base retrieval. The query is much longer than the target document, and it may contain greetings, previous turns, distractor details, or partial reformulations. A model must infer the active user need and map it to a concise FAQ entry.

## Details

### What the Original Data Measures

FaMTEB explicitly introduces chatbot and RAG datasets into the Persian benchmark, including synthetic Persian chatbot and chatbot-RAG data. `syn_per_chatbot_ragfaq` uses `MCINext/synthetic-persian-chatbot-rag-faq-retrieval` and is evaluated through the MTEB retrieval framework.

The task measures retrieval for a Persian RAG assistant. The system receives a dialogue-like query and must retrieve a short FAQ item that can answer or ground the assistant response. This is different from ordinary passage retrieval because the relevant intent may be embedded inside a long conversational context.

### Observed Data Profile

This Nano split contains 200 queries, 8,696 documents, and 200 positive qrels. Each query has exactly one positive. Queries average 597.44 characters, while documents average 145.69 characters.

Observed examples include conversations about electricity bill delivery, delayed orders, social theory, toy buying advice, and health recommendations for young people. Positive documents are compact FAQ items with a question and answer.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.2882, hit@10 of 0.4150, and recall@100 of 0.7250 with a top-500 candidate pool. Lexical retrieval is weak because the long dialogue contains many words that are not part of the final retrieval intent.

BM25 can work when the user's final need repeats FAQ keywords exactly, such as "order status" or "invoice by email". It struggles when the conversation includes topic drift, paraphrase, or many support-like terms that also occur in unrelated FAQ entries.

### Dense Evaluation Profile

The dense harrier-oss-270m profile reaches nDCG@10 of 0.4304, hit@10 of 0.6200, and recall@100 of 0.8900. Dense retrieval is the strongest direct ranking profile for this task.

This is expected for dialogue-to-FAQ matching. Embedding similarity can compress the conversation into a broader intent and match it to a short FAQ even when the surface wording differs. Dense retrieval also handles cases where the current user message is a paraphrase of the FAQ question.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate subset reaches nDCG@10 of 0.3826, hit@10 of 0.5600, and recall@100 of 0.8900. It uses 100 candidates per query, with 22 rank-101 safeguard positives.

Hybrid retrieval matches dense retrieval on recall@100 but falls below dense on top-10 ranking. The hybrid pool is still useful for reranking because it preserves high candidate coverage while including lexical FAQ matches. The safeguard count indicates that many positives sit near the boundary of the top-100 candidate set.

### Metric Interpretation for Model Researchers

`syn_per_chatbot_ragfaq` is a strong test of query understanding. Dense retrieval outperforming BM25 shows that the main difficulty is not term matching; it is extracting the user's active intent from a long dialogue and aligning it with a compact FAQ.

Since each query has one positive, hit@10 and nDCG@10 are highly consequential. Recall@100 indicates whether reranking has a chance to recover the correct FAQ. The dense and hybrid recall values show that a reranker can work with these pools, but first-stage ranking remains difficult.

### Query and Relevance Type Tendencies

Queries are Persian chatbot transcripts, sometimes with multiple turns and sometimes with a single latest message. They include support requests, shopping advice, education topics, billing, order tracking, and health-style informational needs.

Relevant documents are short FAQ entries. A positive document is the FAQ item that can answer the active user need, not necessarily the document sharing the most words with the full conversation.

### Representative Failure Modes

BM25 may retrieve an FAQ matching a distractor phrase from earlier in the conversation. Dense retrieval may choose a broadly related FAQ but miss a specific operational detail, such as delivery method, tracking status, or age group. Hybrid retrieval improves coverage but still needs reranking to identify the current intent.

Long conversations can also contain assistant turns that are not part of the user's need. Models that encode the whole transcript without intent selection may be distracted.

### Training Data That May Help

Useful training data includes Persian RAG FAQ retrieval, conversation-to-knowledge-base matching, synthetic chatbot logs, dialogue query rewriting, customer-support FAQ pairs, and hard negatives that share the same topic but answer a different support question.

Training should exclude the evaluation conversations and FAQ entries from this split.

### Model Improvement Notes

Improving this task requires intent extraction before or during retrieval. Models should learn to downweight greetings, assistant boilerplate, and earlier turns when the final user need is clear.

For reranking, the key behavior is answerability: the selected FAQ should directly ground the next assistant response. Query rewriting into a concise Persian search query may also be beneficial before first-stage retrieval.

## Example Data

| Query | Positive document |
| --- | --- |
| کاربر : با سلام، می‌خواستم اطلاعات بیشتری در مورد نحوه پرداخت قبوض برق دریافت کنم. چت بات : سلام! برای پرداخت قبوض برق، می‌تونی از چندین روش استفاده کنی. مثل پرداخت آنلاین، از طریق تلفن، یا مراجعه به دفاتر پرداخت. کاربر : آیا می‌توانید مراحل پرداخت آنلاین را دقیق‌تر توضیح دهید؟ چت بات : البته! اول به سایت اداره برق می‌ری، بعد روی گزینه‌ی پرداخت قبوض کلیک می‌کنی، اطلاعات حساب کاربری و جزئیات قبض رو وارد می‌کنی و در نهایت پرداخت رو انجام می‌دی. کاربر : آیا امکان پرداخت قبوض از طریق اپلیکیشن موبایل... [500 / 889 chars] | سوال : چگونه می‌توانم صورتحساب خود را از طریق ایمیل دریافت کنم؟ پاسخ : برای دریافت صورتحساب از طریق ایمیل، کافیست اطلاعات خود را به خدمات مشتریان بدهید. [152 chars] |
| کاربر : چرا هنوز سفارش من ارسال نشده؟ چت بات : ما هیچ تأخیری نداریم! سفارش شما همین حالا در حال پردازش است. کاربر : به من گفتید که سه روزه می‌رسد، حالا یک هفته گذشته! چت بات : این مسئله به شرایط حمل و نقل بستگی دارد! ما در این مورد نمی‌توانیم کاری کنیم. کاربر : دیگر به این بهانه‌ها گوش نمی‌دهم! باید به من بگویید چه زمانی خواهد رسید! چت بات : ما تمام اطلاعات مروج را در اختیار شما گذاشته‌ایم! حوصله‌تان را سر نبرم. کاربر : این چه نوع خدماتی است؟ من به شدت ناراحتم. چت بات : ما تمام تلاش‌مان را می‌کن... [500 / 632 chars] | سوال : چگونه می‌توانم وضعیت سفارش خود را بررسی کنم؟ پاسخ : شما می‌توانید با وارد کردن شماره سفارش در بخش پیگیری سفارش، وضعیت آن را بررسی کنید. [142 chars] |
| کاربر : با سلام، می‌خواستم در مورد نظریه‌های کلان اجتماعی توضیح دهید. چت بات : سلام! حتماً، نظریه‌های کلان اجتماعی به بررسی ساختارهای بزرگ اجتماعی مثل جامعه، فرهنگ و تاریخ می‌پردازند. کاربر : آیا می‌توانید به صورت مختصر به برخی از این نظریه‌ها اشاره کنید؟ چت بات : البته! مثل نظریهٔ مارکسیسم که به تضادهای طبقاتی می‌پردازد یا نظریهٔ ساختارگرایی که به چگونگی سازماندهی جامعه توجه دارد. کاربر : این نظریه‌ها چگونه بر رفتار فردی تأثیر می‌گذارند؟ چت بات : خوب، این نظریه‌ها به ما کمک می‌کنند تا بفهمیم چط... [500 / 824 chars] | سوال : نقش نظریه‌های اجتماعی در سیاست چیست؟ پاسخ : نظریه‌های اجتماعی به ما کمک می‌کنند تا درک بهتری از رفتارهای سیاسی و فرایندهای اجتماعی داشته باشیم. [150 chars] |

### Source Reference Table

| Source | Role |
| --- | --- |
| [FaMTEB: Massive Text Embedding Benchmark in Persian Language](https://arxiv.org/abs/2502.11571) | Persian embedding benchmark paper. |
| [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316) | General embedding benchmark framework. |
| [MCINext/synthetic-persian-chatbot-rag-faq-retrieval](https://huggingface.co/datasets/MCINext/synthetic-persian-chatbot-rag-faq-retrieval) | Public source dataset card. |
| [hakari-bench/NanoFaMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoFaMTEB-v2) | Nano benchmark dataset containing this split. |

### Representative Snippets

| Query Pattern | Positive Document Pattern |
| --- | --- |
| A multi-turn support conversation about receiving an electricity bill by email. | An FAQ explaining how to receive a bill or statement through email. |
| A conversation about a delayed order and checking what happened. | An FAQ explaining how to check order status with an order number. |
| A conversation asking about macro social theories and their implications. | An FAQ about the role of social theories in politics or social processes. |
| A shopping conversation about choosing a toy. | An FAQ about finding age-appropriate toys using preferences or recommendations. |
| A latest user message asking for health recommendations for young people. | An FAQ giving health advice for teenagers, including diet, exercise, sleep, and avoidance of harmful substances. |
