# NanoIndicQA / as

## Overview

`NanoIndicQA / as` is the Assamese split of IndicQA retrieval. The queries are Assamese cloze-style reading-comprehension questions, and the documents are Assamese context paragraphs that contain the evidence needed to answer them.

This task evaluates context paragraph retrieval, not answer-string prediction. The model must select the paragraph that supports the question from a small corpus, often where several questions may point to the same long context passage.

## Details

### What the Original Data Measures

IndicQA was introduced as part of IndicXTREME in "Towards Leaving No Indic Language Behind", a benchmark suite for Indic languages. IndicQA is a manually curated cloze-style reading-comprehension task.

The MTEB retrieval version repurposes the QA task by using the question as the query and the relevant context paragraph as the document. In this Assamese split, the task measures whether retrieval models can connect Assamese questions to the supporting Assamese passage.

### Observed Data Profile

This Nano split contains 200 queries, 250 documents, and 200 positive qrels. Each query has exactly one positive. Queries average 55.30 characters, and documents average 1,401.28 characters.

Observed examples ask about Kaziranga and Manas National Park, verses recited by Ugrasrava Sauti, how a japi is made, languages spoken by Mon-Khmer groups, and the maximum width of the Arabian Sea. Documents are long cultural, historical, geographic, or encyclopedic paragraphs in Assamese.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.6111, hit@10 of 0.7500, and recall@100 of 0.9100. The candidate pool contains the full 250-document corpus. BM25 is useful when the question repeats distinctive Assamese named entities, places, objects, or numeric facts from the paragraph.

The failure cases come from short questions, broad wording, and contexts that share cultural or historical vocabulary. With long paragraphs, lexical overlap may select a related passage even when it does not contain the exact evidence.

### Dense Evaluation Profile

The dense harrier-oss-270m profile reaches nDCG@10 of 0.7416, hit@10 of 0.8850, and recall@100 of 0.9800. Dense retrieval is the strongest direct ranking profile.

This suggests that embedding similarity helps connect Assamese questions to their supporting contexts beyond exact word overlap. Dense retrieval is especially useful when the question paraphrases the evidence or when the paragraph contains broader explanatory context.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate subset reaches nDCG@10 of 0.7283, hit@10 of 0.8600, and recall@100 of 0.9800. It uses 100 candidates per query, with four rank-101 safeguard positives.

Hybrid retrieval matches dense retrieval on recall@100 but is slightly weaker on nDCG@10 and hit@10. This makes dense retrieval the best direct first-stage signal, while hybrid retrieval remains a useful reranking pool because it preserves both lexical anchors and semantic matches.

### Metric Interpretation for Model Researchers

`NanoIndicQA / as` is a small-corpus Assamese context retrieval task. Since each query has one positive, nDCG@10 and hit@10 directly measure whether the correct context is ranked early.

The metric pattern is dense-favored: BM25 is a solid baseline, but dense retrieval substantially improves top-10 accuracy. Recall@100 is high for dense and hybrid, so reranking experiments can focus mostly on top-order precision.

### Query and Relevance Type Tendencies

Queries are Assamese cloze-style questions that ask for a fact or phrase grounded in a paragraph. Documents are long context paragraphs, often encyclopedic and culturally specific.

The relevance relation is evidence sufficiency: the positive paragraph should contain enough information to answer the question.

### Representative Failure Modes

BM25 may retrieve a paragraph with overlapping named entities but not the requested fact. Dense retrieval may confuse topically related Assamese passages when they describe similar cultural, geographic, or historical material. Hybrid retrieval reduces candidate misses but still has to rank the exact supporting context above related paragraphs.

Multiple questions pointing to the same paragraph can also make the dataset look easier for memorizing paragraph topics, while still requiring exact evidence matching for individual questions.

### Training Data That May Help

Useful training data includes non-overlapping Assamese QA context retrieval, IndicQA-style cloze pairs, Assamese Wikipedia passage retrieval, and hard negatives from paragraphs about related Indian cultural, geographic, or historical topics.

Training should avoid using this split's queries and positive context paragraphs.

### Model Improvement Notes

Improving this task requires Assamese language coverage and context-level retrieval. Models should preserve named entities and numeric facts while representing the broader question-context relation.

For reranking, the model should check whether the paragraph actually supports the question, not only whether it is about the same entity or topic.

## Example Data

| Query | Positive document |
| --- | --- |
| কেতিয়া কেইবাটাও হাতী আৰু দুটা গঁড় মানাহ ৰাষ্ট্ৰীয় উদ্যানলৈ প্ৰেৰণ কৰা হৈছিল? [78 chars] | [উদ্ধৃতিৰ প্ৰয়োজন] ১৯৬৮ চনত চৰকাৰে প্ৰণয়ন কৰে 'অসম ৰাষ্ট্ৰীয় উদ্যান আইন, ১৯৬৮ চন' (The Assam National Park Act of 1968) আৰু এই আইনৰ জৰিয়তে কাজিৰঙাক ৰাষ্ট্ৰীয় উদ্যানৰ ময্যদা দিয়া হয়। [উদ্ধৃতিৰ প্ৰয়োজন] ১৯৭৪ চনৰ ১১ ফেব্ৰুৱাৰী তাৰিখে কেন্দ্ৰীয় চৰকাৰে ৪৩০ বৰ্গ কি.মি. মাটি-কালিৰে আগুৰা কাজিৰঙাক আনুষ্ঠানিক ভাৱে ৰাষ্ট্ৰীয় উদ্যানৰ স্বীকৃতি দিয়ে। ১৯৮৫ চনত কাজিৰঙাক ইউনেস্কোৰ (UNESCO) 'বিশ্ব ঐতিহ্যক্ষেত্ৰ' (World Heritage Site) হিচাপে অন্তৰ্ভুক্ত কৰা হয়। কাজিৰঙাই বিগত কেইটামান দশকত বহুতো প্ৰাকৃতিক আৰু মানৱ-সৃষ্ট দুৰ্যোগৰ মাজেৰে পাৰ হ'বলগীয়া হৈছে। ব্ৰহ্মপুত্ৰৰ বানপানী যথেষ্ট সংখ্যক পশুৰ মৃত্যুৰ কাৰণ হৈ পৰে। কাজিৰঙাৰ আশ-পাশে চলি থকা বেদখলে উদ্যানখনৰ সীমা চেপি আনি পশুৰ বাবে স্থান সীমিত কৰিছে। [উদ্ধৃতিৰ প্ৰয়োজন] আলফা আৰু অন্যান্য উগ্ৰপন্থী গোটৰ চলিত কাৰ্যকলাপে অঞ্চলটোৰ অৰ্থনৈতিক ক্ষেত্ৰত হানিৰ সৃষ্টি কৰিছে। অৱশ্যে আলফাৰ দ্বাৰা প্ৰত্যক্ষ ভাৱে কাজিৰঙাৰ কোনো হানি হোৱা নাই–বৰং–কিছুমান ক্ষেত্ৰত আলফা সদস্যই উদ্যানৰ পশু হত্যা বন্ধ কৰিবলৈ চেষ্টা কৰা দেখা যায়। ১৯৮০ চনৰপৰাই আলফা সদস্যৰ দ্বাৰা চো... [1,000 / 1,207 chars] |
| উগ্ৰস সৌতীয়ে কিমানটা শ্লোক আবৃত্তি কৰিছিল? [43 chars] | আগতেই কৈ অহা হৈছে যে পৰম্পৰাগতভাৱে ব্যাসক মহাভাৰতৰ লেখক বুলি কোৱা হয়। মহাভাৰতৰ প্ৰথম অনুচ্ছেদৰ মতে ব্যাসে গণেশক তেওঁৰ শ্ৰুতলিপি অনুসৰি শ্লোকসমূহ লিখিবলৈ অনুৰোধ কৰে। তেতিয়া গণেশে চৰ্ত্ত দিয়ে যে ব্যাসে আবৃত্তিৰ মাজত অকণো ৰ’ব নোৱাৰিব। আনহাতে ব্যাসো এই চৰ্ত্ততহে মান্তি হয় যে গণেশে লিখাৰ পূৰ্বে শ্লোকটো বুজি ল’ব লাগিব। এই কাব্যখনত কাহিনীৰ ভিতৰত কাহিনীৰ ৰূপ দেখিবলৈ পোৱা যায়। ইয়াক ব্যাসৰ শিষ্য বৈশম্পায়নে অৰ্জুনৰ পৰিনাতি ৰজা জন্মেজয়ক আবৃত্তি কৰি শুনায়। এই আবৃত্তিকে পুনৰ উগ্ৰস্ৰৱা সৌতী নামৰ এজন পেছাদাৰী সাধুকওঁতাই নৈমিশ বনত সন্ন্যাসীৰ এটা দলক শুনায়। মহাভাৰতৰ মূল কাহিনী "জয়"ক কুৰু নৃপতি ধৃতৰাষ্ট্ৰ আৰু তেওঁৰ উপদেষ্টা তথা সাৰথি সঞ্জয়ৰ কথোপকথন হিছাপে দেখুওৱা হৈছে। সঞ্জয়ে ওঠৰ দিনৰ কুৰুক্ষেত্ৰ যুদ্ধৰ প্ৰতিটো ঘটনা বৰ্ণনা কৰি যায়। ধৃতৰাষ্ট্ৰই মাজে মাজে প্ৰশ্ন কৰে আৰু এই যুদ্ধৰ ধ্বংসলীলাৰ কথা গম পাই দুখ আৰু অনুতাপ কৰে। প্ৰথমে সঞ্জয়ে আন গ্ৰহসমূহৰ আৰু পৃথিৱীৰ বিভিন্ন মহাদেশৰ ব্যাখ্যা কৰে আৰু তাৰপিছত ভাৰতবৰ্ষৰ শ শ ৰাজ্য, জাতি, নগৰ, চহৰ, নদী, পৰ্বত, বন আদি সকলোৰে কথা কয়। তেওঁ লগতে যুদ্ধৰ দুই... [1,000 / 2,113 chars] |
| জাপি কিহেৰে নিৰ্মাণ কৰা হয়? [27 chars] | অসমীয়া সমাজ জীৱনত বিভিন্ন বিশ্বাস, অনুভৱ আৰু আদৰ বা সন্মানৰ ক্ষেত্ৰত তামোল-পান, গামোছা আৰু শৰাইৰ বিশেষ ভূমিকা আছে। যিকোনো সামাজিক কামত তামোল-পাণ ব্যৱহাৰ কৰা হয়। কাৰোবাৰ ঘৰলৈ অহা অতিথিক আন নহ'লেও তামোল-পাণ খাবলৈ দিয়া হয়। সামাজিক কাৰণত হোৱা যিকোনো দণ্ড মিমাংসাৰ বাবেও তামোল-পাণ ব্যৱহাৰ কৰা হয়। আনহাতে গামোছা অসমীয়া সমাজত বিহুৱানৰ ৰূপত ব্যৱহাৰ কৰা হয়। ইয়াৰ লগতে গা ধোৱাৰ পিছত ব্যৱহাৰ কৰা তিয়নী গামোচা, পানী গামোচা আদিও উল্লেখযোগ্য। সৰুৱে ডাঙৰক মান ধৰা আদিৰ ক্ষেত্ৰত গামোচা ব্যৱহাৰ কৰা হয়। শৰাই ধাতুৰে নিৰ্মিত এবিধ খুৰা থকা পাত্ৰ। সাধাৰণতে তামোল-পাণ আৰু গামোচাৰে কাৰোবাক মান ধৰাৰ ক্ষেত্ৰত ইয়াক ব্যৱহাৰ কৰা হয়। অসমৰ যিকোনো সাংস্কৃতিক কাৰ্যকলাপৰ লগত এই তিনিবিধ বস্তুৰ ব্যৱহাৰ অপৰিহাৰ্য। আনাহাতে জাপি অসমীয়া সংস্কৃতিৰ আন এবিধ আদৰৰ প্ৰতিক। কাৰোবাক সন্মান জনোৱাৰ লগতে উপহাৰ দিয়াৰ ক্ষেত্ৰত ইয়াক ব্যৱহাৰ কৰা হয়। ই কেইবাপ্ৰকাৰৰ যেনে-ডাং-জাপি, বৰজাপি, পানী বা হালোৱা-জাপি আৰু সৰুদৈয়া জাপি। অসমত আটাইতকৈ প্ৰচলিত জাপি হ'ল সৰুদৈয়া জাপি। [938 chars] |

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
| An Assamese question asking when elephants and rhinoceroses were sent to Manas National Park. | A paragraph about Kaziranga, national park status, and conservation history. |
| A question asking how many verses Ugrasrava Sauti recited. | A Mahabharata-related paragraph discussing Vyasa, Ganesha, and recitation tradition. |
| A question asking what a japi is made from. | A cultural paragraph about Assamese social objects such as tamol-pan, gamocha, and japi. |
| A question asking which languages the Mon-Khmer spoke. | A paragraph about Andamanese or regional peoples, archaeology, and language context. |
| A question asking the maximum width of the Arabian Sea. | A geography paragraph giving Arabian Sea area, width, depth, and branches. |
