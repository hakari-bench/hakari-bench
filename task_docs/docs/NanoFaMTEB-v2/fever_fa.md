# NanoFaMTEB-v2 / fever_fa

## Overview

`fever_fa` is a Persian fact-verification evidence retrieval task in NanoFaMTEB-v2. The query is a short factual claim, and the target documents are Persian evidence passages that can support or refute the claim. The task is adapted from FEVER-style retrieval through FaMTEB.

This task evaluates whether a Persian retriever can connect concise claims to encyclopedia-style evidence. Entity names and factual phrases are often strong lexical anchors, but the model still needs to rank the passage that contains the relevant evidence rather than merely a passage about the same entity.

## Details

### What the Original Data Measures

FaMTEB is a Persian text embedding benchmark that includes retrieval tasks adapted from BEIR-style and MTEB-style sources. `fever_fa` uses `MCINext/FEVER_FA_test_top_250_only_w_correct-v2`, a Persian FEVER-style hard-negative dataset.

The original FEVER setting measures evidence retrieval for factual claims. A retrieval system must find passages that provide factual evidence for verification. In this Persian variant, the same evidence-retrieval problem is evaluated over Persian claims and passages.

### Observed Data Profile

This Nano split contains 200 queries, 10,000 documents, and 229 positive qrels. Most queries have one positive, while 25 queries are multi-positive. Positives per query average 1.15, with a minimum of 1, median of 1.0, and maximum of 4. Queries average 47.09 characters, and documents average 523.29 characters.

Observed examples include claims about films, geographic valleys, companies, actors, and city statistics. Documents are mostly Persian encyclopedia-style passages with entity titles and factual descriptions.

### BM25 Evaluation Profile

BM25 is very strong, with nDCG@10 of 0.8025, hit@10 of 0.9000, and recall@100 of 0.9432 using a top-500 candidate pool. This reflects the strong entity signal in FEVER-style retrieval. Claims often mention the entity whose page or passage contains the evidence.

BM25 can still fail when multiple passages share the same entity name or when the evidence requires matching a specific factual property rather than only the entity title. Lexical retrieval narrows the search space well, but final ranking still needs fact-level precision.

### Dense Evaluation Profile

The dense harrier-oss-270m profile is strongest by top-rank metrics, with nDCG@10 of 0.8972, hit@10 of 0.9450, and recall@100 of 0.9170. Dense retrieval improves top ranking by matching claim meaning to evidence content.

The lower recall@100 relative to BM25 and hybrid indicates that dense retrieval can rank known evidence very well but may miss some positive evidence passages deeper in the candidate set. This is plausible when exact entity names are decisive.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate subset reaches nDCG@10 of 0.8396, hit@10 of 0.9250, and recall@100 of 0.9825. It uses top-100 candidates with optional rank-101 safeguards; one row contains 101 candidates and one safeguard-positive row is recorded. Hybrid retrieval has the strongest top-100 coverage.

This suggests that BM25 and dense signals are complementary: BM25 preserves entity-name coverage, while dense retrieval improves fact-level ranking. A reranker using hybrid candidates can start from a very complete evidence pool.

### Metric Interpretation for Model Researchers

`fever_fa` is an entity-heavy Persian evidence retrieval task. BM25 is already strong, dense retrieval is best at top ranking, and hybrid retrieval is best at candidate recall. The main research target is fact-sensitive ranking among entity-related passages.

Because some queries have multiple positives, recall@100 matters for evidence coverage. Top-rank metrics measure whether the retriever places the most useful evidence early.

### Query and Relevance Type Tendencies

Queries are short Persian factual claims. Documents are encyclopedia-like passages that often begin with an entity title and factual description. Relevance depends on whether the passage contains evidence for the claim.

### Representative Failure Modes

BM25 may retrieve the right entity page but the wrong evidence passage. Dense retrieval may retrieve semantically related passages while missing exact entity evidence. Hybrid retrieval can recover many positives but still needs fact-sensitive reranking.

### Training Data That May Help

Useful training data includes Persian fact-checking retrieval, translated FEVER claim-evidence pairs, and entity-centric Wikipedia evidence retrieval. Hard negatives should share named entities but not support the claim.

Training should exclude evaluation queries, positives, and translated duplicates from this split.

### Model Improvement Notes

Improving this task requires combining entity recall with factual matching. Models should preserve names, dates, titles, and locations, while also matching predicates and claim polarity.

For reranking, evidence sufficiency and claim-passage entailment signals may help.

## Example Data

| Query | Positive document |
| --- | --- |
| یک پرنده بر فراز آشیانه نسترن تنها یک جایزه اسکار را برنده شد. [62 chars] | بر فراز آشیانه فاخته (فیلم) پرواز بر فراز آشیانه فاخته فیلمی آمریکایی محصول سال ۱۹۷۵ به کارگردانی میلوش فورمن، بر اساس رمانی به همین نام از کن کسی است. جک نیکلسون در این فیلم بازی کرده و لوئیز فletche... [200 / 925 chars] |
| دره رود سالت در کنار رودخانه می‌سی‌سی‌پی قرار دارد. [51 chars] | دره رودخانه سالت دره رودخانه نمک در مرکز آریزونا یک دره وسیع در امتداد رودخانه نمک است که منطقه کلان‌شهری فینیکس را در خود جای داده است. اگرچه این اصطلاح جغرافیایی هنوز هم برای شناسایی این منطقه استفا... [200 / 527 chars] |
| اسکای یوکی یک شرکت مخابراتی بریتانیایی است. [43 chars] | بریتانیا پادشاهی متحد بریتانیای کبیر و ایرلند شمالی، که معمولاً به عنوان پادشاهی متحد (بریتانیا) شناخته می‌شود، کشوری مستقل در اروپای غربی است. این کشور در سواحل شمال غربی سرزمین اصلی اروپا واقع شده و... [200 / 4,136 chars] |
| کایا اسکودلاریو یک کارگردان است. [32 chars] | کایا اسکودلاریو کایا اسکودلاریو-دیویس (زاده کایا رز هامفری؛ ۱۳ مارس ۱۹۹۲) بازیگر انگلیسی است. او با نقش آفرینی در نقش افی استونم در سریال درام نوجوان شبکه E4 به نام Skins (۲۰۰۷-۲۰۱۰) وارد دنیای بازیگر... [200 / 1,535 chars] |
| در سال ۲۰۱۲، شهر سیمی ولی در کالیفرنیا گزارش داد که درآمد متوسط خانوار در این شهر برای اولین بار در... [100 / 149 chars] | سیمی ولی، کالیفرنیا شهر سیمی ولی (از واژه چوماش، شیمیی) در دره‌ای به همین نام، در گوشه جنوب شرقی شهرستان ونتورا، کالیفرنیا، ایالات متحده واقع شده است. سیمی ولی در فاصله ۳۰ مایلی مرکز شهر لس‌آنجلس قرار... [200 / 1,485 chars] |

### Source Reference Table

| Source | Role |
| --- | --- |
| [FaMTEB: Massive Text Embedding Benchmark in Persian Language](https://arxiv.org/abs/2502.11571) | Persian embedding benchmark paper. |
| [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316) | General benchmark framework. |
| [MCINext/FEVER_FA_test_top_250_only_w_correct-v2](https://huggingface.co/datasets/MCINext/FEVER_FA_test_top_250_only_w_correct-v2) | Public source dataset card. |
| [hakari-bench/NanoFaMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoFaMTEB-v2) | Nano benchmark dataset containing this split. |

### Representative Snippets

| Query Pattern | Positive Document Pattern |
| --- | --- |
| A Persian claim about a film and an Academy Award. | A passage about the film, its production, cast, and awards context. |
| A claim about the Salt River Valley and a major river. | A geographic passage describing the Salt River Valley. |
| A claim about a company being British. | An evidence passage about the relevant country or entity. |
| A claim about Kaya Scodelario's occupation. | A biographical passage describing the actor's career. |
| A claim about Simi Valley household income. | A city passage containing geographic and demographic context. |
