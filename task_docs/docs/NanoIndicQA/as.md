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
| কেতিয়া কেইবাটাও হাতী আৰু দুটা গঁড় মানাহ ৰাষ্ট্ৰীয় উদ্যানলৈ প্ৰেৰণ কৰা হৈছিল? [78 chars] | [উদ্ধৃতিৰ প্ৰয়োজন] ১৯৬৮ চনত চৰকাৰে প্ৰণয়ন কৰে 'অসম ৰাষ্ট্ৰীয় উদ্যান আইন, ১৯৬৮ চন' (The Assam National Park Act of 1968) আৰু এই আইনৰ জৰিয়তে কাজিৰঙাক ৰাষ্ট্ৰীয় উদ্যানৰ ময্যদা দিয়া হয়। [উদ্ধৃতিৰ প... [200 / 1,207 chars] |
| উগ্ৰস সৌতীয়ে কিমানটা শ্লোক আবৃত্তি কৰিছিল? [43 chars] | আগতেই কৈ অহা হৈছে যে পৰম্পৰাগতভাৱে ব্যাসক মহাভাৰতৰ লেখক বুলি কোৱা হয়। মহাভাৰতৰ প্ৰথম অনুচ্ছেদৰ মতে ব্যাসে গণেশক তেওঁৰ শ্ৰুতলিপি অনুসৰি শ্লোকসমূহ লিখিবলৈ অনুৰোধ কৰে। তেতিয়া গণেশে চৰ্ত্ত দিয়ে যে ব্যা... [200 / 2,113 chars] |
| জাপি কিহেৰে নিৰ্মাণ কৰা হয়? [27 chars] | অসমীয়া সমাজ জীৱনত বিভিন্ন বিশ্বাস, অনুভৱ আৰু আদৰ বা সন্মানৰ ক্ষেত্ৰত তামোল-পান, গামোছা আৰু শৰাইৰ বিশেষ ভূমিকা আছে। যিকোনো সামাজিক কামত তামোল-পাণ ব্যৱহাৰ কৰা হয়। কাৰোবাৰ ঘৰলৈ অহা অতিথিক আন নহ'লেও তাম... [200 / 938 chars] |
| মন খেমাৰে কি কি ভাষা কৈছিল? [27 chars] | অতি কমেও কেইবা শতিকাৰ পৰা এই দ্বীপ মালাত মানুহে বসবাস কৰি আহিছে। পুৰাতত্ববিদ সকলৰ মতে প্ৰায় ২,২০০ বছৰ মানৰ পৰা ইয়াত মানুহ থকাৰ প্ৰমাণ আছে, আনহাতেদি জিনীয় আৰু সাংস্কৃতিক অধ্যয়ণৰ পৰা দেখা গৈছে খিলঞ্... [200 / 1,224 chars] |
| আৰৱ সাগৰৰ সৰ্বাধিক প্ৰস্থ কিমান? [32 chars] | আৰৱ সাগৰৰ আয়তন ৩৮,৬২,০০০ বৰ্গ কিলোমিটাৰ। ইয়াৰ সৰ্বোচ্চ প্ৰস্থ প্ৰায় ২,৪০০ কিলোমিটাৰ আৰু ইয়াৰ সৰ্বনিম্ন গভীৰতা ৪,৬০০ মিটাৰ। সিন্ধু নদ আৰৱ সাগৰলৈ প্ৰবাহিত সৰ্ববৃহৎ নদী। আৰৱ সাগৰৰ দুটা গুৰুত্বপূৰ্ণ শ... [200 / 1,063 chars] |

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
