# NanoIndicQA / bn

## Overview

`NanoIndicQA / bn` is the Bengali split of IndicQA retrieval. The queries are Bengali reading-comprehension questions, and the documents are Bengali context paragraphs that support the answer.

This task evaluates Bengali context retrieval in a small-corpus setting. The model must retrieve the paragraph that contains the evidence for the question, not merely return a short answer string.

## Details

### What the Original Data Measures

IndicQA is part of IndicXTREME, introduced in "Towards Leaving No Indic Language Behind". It is a manually curated cloze-style reading-comprehension benchmark for Indic languages.

The retrieval formulation uses questions as queries and context paragraphs as documents. In the Bengali split, the task measures whether a retriever can identify the Bengali paragraph that contains the necessary evidence.

### Observed Data Profile

This Nano split contains 200 queries, 250 documents, and 201 positive qrels. Queries have 1.005 positives on average, with a minimum of 1, a median of 1.0, and a maximum of 2. Only one query is multi-positive. Queries average 52.08 characters, and documents average 2,196.01 characters.

Observed examples ask about Jallianwala Bagh and public anger, the Ghurid dynasty, the national sport of Bangladesh, construction details of the Taj Mahal, and why Ashoka was called Chanda Ashoka. Documents are long Bengali paragraphs about history, culture, geography, politics, and religion.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.6971, hit@10 of 0.8150, and recall@100 of 0.8955. The candidate pool contains the full 250-document corpus. BM25 is strong when Bengali names, events, dates, or historical terms repeat between the question and context.

Its main weakness is contextual matching. A question may rely on information in a long paragraph where the evidence is expressed indirectly, or several paragraphs may share the same names and cultural vocabulary.

### Dense Evaluation Profile

The dense harrier-oss-270m profile reaches nDCG@10 of 0.7773, hit@10 of 0.8700, and recall@100 of 0.9900. Dense retrieval is the strongest direct profile.

This suggests that embedding similarity helps with Bengali paragraph selection, especially when the question and paragraph do not share all surface words. Dense retrieval also improves recall substantially, making it a better candidate generator than BM25.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate subset reaches nDCG@10 of 0.7460, hit@10 of 0.8350, and recall@100 of 0.9701. It uses 100 candidates per query, with six rank-101 safeguard positives.

Hybrid retrieval is strong but below dense retrieval across the main metrics. It still provides a useful reranking pool by combining exact Bengali term overlap with semantic context matching.

### Metric Interpretation for Model Researchers

`NanoIndicQA / bn` is a Bengali single-context retrieval task with mostly one positive per query. nDCG@10 and hit@10 are the main indicators of whether the correct paragraph is surfaced early.

The profile is dense-favored. BM25 works well for repeated names and explicit terms, but dense retrieval is better for ranking and coverage. Hybrid retrieval is useful, but not the top direct ranker for this split.

### Query and Relevance Type Tendencies

Queries are Bengali factual or cloze-style questions. Documents are long context paragraphs, often from encyclopedic or educational material.

The relevance relation is paragraph-level evidence support. The positive paragraph should contain the information needed to answer the question.

### Representative Failure Modes

BM25 may retrieve a paragraph sharing a historical figure, place, or event but missing the requested fact. Dense retrieval may confuse related history or culture paragraphs when several cover similar topics. Hybrid retrieval can still rank a topically related paragraph above the exact evidence context.

Long context paragraphs can also contain many unrelated terms, making both lexical and dense matching noisy.

### Training Data That May Help

Useful training data includes Bengali QA context retrieval, Bengali Wikipedia passage retrieval, IndicQA-style multilingual training, and hard negatives from same-topic Bengali paragraphs.

Training should exclude this split's questions and positive context paragraphs.

### Model Improvement Notes

Improving this task requires Bengali language coverage and evidence-sensitive paragraph ranking. Models should preserve named entities, dates, and factual relations while handling paraphrased question wording.

For reranking, the key check is whether the paragraph actually contains the answer evidence, not only whether it discusses the same broad topic.

## Example Data

| Query | Positive document |
| --- | --- |
| কার দ্বারা পাঞ্জাবের জালিয়ানওয়ালাবাগে বেসামরিক লোকদের গণহত্যা জনরোষ সৃষ্টি করে এবং সহিংসতা বৃদ্ধি করে ? [105 chars] | অন্যায়ের বিরুদ্ধে গান্ধীর অস্ত্র ছিল অসহযোগ এবং শান্তিপূর্ণ প্রতিরোধ। পাঞ্জাবের জালিয়ানওয়ালাবাগে সাধারণ মানুষের উপরে ব্রিটিশ সরকার কর্তৃক সংগঠিত হত্যাকাণ্ডের ফলে জনসাধারণ ক্ষুব্ধ হয়ে যায় এবং সহিংসতার মাত্রা বৃদ্ধি পায়। গান্ধী ব্রিটিশ সরকারের কৃতকর্ম এরং ভারতীয়দের প্রতিশোধপরায়ণ আচরণ উভয়েরই নিন্দা করেন। তিনি একটি লিখিত বিবৃতিতে ক্ষতিগ্রস্ত ব্রিটিশ নাগরিকদের সমবেদনা জ্ঞাপন করেন এবং বিশৃঙ্খলার সমালোচনা করেন। তার এই পদক্ষেপ প্রাথমিক পর্যায়ে দলের ভিতরে অসন্তোষের জন্ম দিলেও গান্ধীর একটি আবেগীয় বক্তৃতার পর তা গৃহীত হয়। বক্তৃতায় তিনি মূলনীতিগুলোর বর্ণনা দিয়ে বলেন সবরকম বিশৃঙ্খলাই অমঙ্গলজনক এবং সমর্থনযোগ্য নয়। এই হত্যাকাণ্ড এবং গণবিক্ষোভের পর গান্ধী পূর্ণাঙ্গ স্বায়ত্তশাসন এবং সকল সরকারি প্রতিষ্ঠানের নিয়ন্ত্রণ লাভের দিকে মনোনিবেশ করেন, যা শেষ পর্যন্ত স্বরাজ বা সম্পূর্ণ ব্যক্তিগত, আদর্শগত, রাজনৈতিক স্বাধীনতার আন্দোলনে রূপ নেয়। ১৯২১ সালের ডিসেম্বরে মহাত্মা গান্ধী ভারতীয় জাতীয় কংগ্রেসের নির্বাহী হন। তার নেতৃত্বে কংগ্রেস স্বরাজের লক্ষ্যকে সামনে রেখে নতুন সংবিধান গ্রহণ করেন। সদস্য... [1,000 / 1,277 chars] |
| ঘুরি রাজবংশের অন্যতম শাসক কে ছিলেন ? [36 chars] | আফগানিস্থানে সম্প্রতি মেন্‌রোজ প্রদেশের ‘শাহ্ পোশ্’-এ খননকালে একটি মিনারের ধ্বংসাবশেষ আবিষ্কৃত হয়েছে। একটি মস্‌জিদের অনতিদূরে সেই মিনারটি নির্মিত হয়েছিল নবম অথবা দশম-শতাব্দীর প্রথম পাদে। সামানিদ্-ইটের তৈরি এই মিনারের শুধু পাদদেশটুকুই আবিষ্কৃত হয়েছে—কিন্তু তার প্ল্যান কুৎব মিনারের ছন্দে গড়া। একটি করে কোণ এবং একটি করে গোলাকৃতি (বাঁশী) পর-পর সাজানো, ঠিক যেমনটি দেখা যায় কুৎব-এ। বিশেষজ্ঞ শ্রী আর. সেনগুপ্তের মতে এই মিনারটি প্ল্যানিং-এ পূর্বযুগে নির্মিত সামানিদ্-বংশের বুখারার শাসক ইস্‌মাইল (৮৯২–৯০৭) নির্মিত একটি মিনারের ছাপ পড়েছে। সেটিও প্রথম নয়—তারও পূর্বে নির্মিত হয়েছিল আফগানিস্থানের প্রাচীনতম মস্‌জিদ একটি মিনার—স্থানীয় লোকেরা যার পরিচয় দিতে বলে বল্‌ক্-এর ‘নাও গাম্বাদ’ (Naw Gumbad—‘নয়া গম্বুজ’)। কুৎব মিনারের সঙ্গে শাহ্-পোশ্ মিনারের কিছুটা সাদৃশ্য থাকলেও তার পরিকল্পনা যেন বেশি করে ছাপ ফেলেছে ‘জাম’-এ নির্মিত গীয়াৎউদ্‌দীন ঘোরীর (১১৫৭–১২০২) অপর একটি মিনার। বাস্তবিকপক্ষে, ঘোরীরা অনেকগুলি বিজয় মিনার নির্মাণ করেছিলেন আফগানিস্তানের বিভিন্ন অঞ্চলে। [961 chars] |
| বাংলাদেশের জাতীয় খেলার নাম কি ? [31 chars] | ঈদুল ফিতরের আগের দিনটি বাংলাদেশে ‘চাঁদ রাত’ নামে পরিচিত। ছোট ছোট বাচ্চারা এ দিনটি অনেক সময়ই আতশবাজির মাধ্যমে পটকা ফাটিয়ে উদ্‌যাপন করে। ঈদুল আজহার সময় শহরাঞ্চলে প্রচুর কোরবানির পশুর আগমন হয় এবং এটি নিয়ে শিশুদের মাঝে একটি উৎসবমুখর উচ্ছাস থাকে। এই দুই ঈদেই বাংলাদেশের রাজধানী শহর ঢাকা ছেড়ে বিপুলসংখ্যক মানুষ তাদের জন্মস্থল গ্রামে পাড়ি জমায়। এছাড়া বাংলাদেশের সর্বজনীন উৎসবের মধ্যে পহেলা বৈশাখ প্রধান। গ্রামাঞ্চলে নবান্ন, পৌষ পার্বণ ইত্যাদি লোকজ উৎসবের প্রচলন রয়েছে। এছাড়া স্বাধীনতা দিবস, বিজয় দিবস এবং ভাষা আন্দোলনের শহীদদের স্মরণে ২১শে ফেব্রুয়ারি তারিখে শহীদ দিবস ঘটা করে পালিত হয়। বাংলাদেশের জাতীয় খেলা হা-ডু-ডু বা কাবাডি। এই খেলার মতোই বাংলাদেশের অধিকাংশ নিজস্ব খেলাই উপকরণহীন কিংবা উপকরণের বাহুল্যবর্জিত। উপকরণবহুল খুব কম খেলাই বাংলাদেশের নিজস্ব খেলা। উপকরণহীন খেলার মধ্যে এক্কাদোক্কা, দাড়িয়াবান্দা, গোল্লাছুট, কানামাছি, বরফ-পানি, বউচি, ছোঁয়াছুঁয়ি ইত্যাদি খেলা উল্লেখযোগ্য। উপকরণের বাহুল্যবর্জিত বা সীমিত সহজলভ্য উপকরণের খেলার মধ্যে ডাঙ্গুলি, সাতচাড়া, রাম-সাম-যদু-মধু বা চোর-ডাকাত... [1,000 / 2,396 chars] |

### Source Reference Table

| Source | Role |
| --- | --- |
| [Towards Leaving No Indic Language Behind](https://arxiv.org/abs/2212.05409) | IndicXTREME and IndicQA benchmark paper. |
| [mteb/IndicQARetrieval](https://huggingface.co/datasets/mteb/IndicQARetrieval) | MTEB retrieval task dataset card. |
| [ai4bharat/IndicQA](https://huggingface.co/datasets/ai4bharat/IndicQA) | Upstream IndicQA dataset card. |
| [hakari-bench/NanoIndicQA](https://huggingface.co/datasets/hakari-bench/NanoIndicQA) | Nano benchmark dataset containing this split. |

### Representative Snippets

| Query Pattern | Positive Document Pattern |
| --- | --- |
| A Bengali question asking who caused the Jallianwala Bagh massacre that created public anger. | A paragraph about Gandhi's non-cooperation, peaceful resistance, and public reaction to the massacre. |
| A question asking who was one of the rulers of the Ghurid dynasty. | A historical paragraph about Afghanistan, minaret remains, and medieval dynastic context. |
| A question asking the name of Bangladesh's national sport. | A cultural paragraph about Bangladeshi festivals and children's activities. |
| A question asking who made gold work on the Taj Mahal's large dome finial. | A paragraph describing Taj Mahal water systems, garden infrastructure, and architectural details. |
| A question asking why Emperor Ashoka was called Chanda Ashoka. | A paragraph discussing Ashoka's cruel nature and later Buddhist transformation. |
