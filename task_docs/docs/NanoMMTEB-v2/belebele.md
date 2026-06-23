# NanoMMTEB-v2 / belebele

## Overview

`NanoMMTEB-v2 / belebele` is a multilingual retrieval adaptation of the
Belebele reading-comprehension benchmark. Queries are questions in many
language variants, and the retriever must return the passage that supports the
answer. The Nano split has 376 queries, 10,000 documents, and 376 positive qrel
rows, with exactly one positive passage per query. Current diagnostics show
dense retrieval as the strongest profile, `reranking_hybrid` as better than
BM25 but below dense, and BM25 as very weak because exact token overlap is
limited across scripts, languages, and question-passage formulations.

## Details

### What the Original Data Measures

The Belebele benchmark is a parallel reading-comprehension dataset covering 122
language variants over FLORES-200 passages. It was designed to test
comprehension across a broad multilingual and cross-script setting. In this
retrieval adaptation, the question becomes the query and the answer-bearing
passage becomes the positive document.

This means the task measures multilingual passage retrieval with reading
comprehension cues. A model must find the passage that explicitly supports the
answer, not merely a passage in the same broad domain.

### Observed Data Profile

The Nano split contains 376 queries, 10,000 documents, and 376 positive qrel
rows. Every query has exactly one positive document. Queries average 95.39
characters, while documents average 509.21 characters.

The sample visibly mixes scripts and languages, including Swedish, Arabic,
English, Slovak, romanized Nepali-like text, Hindi, Hebrew, Burmese-script
text, and many other non-English passages. Documents are short passages rather
than long articles.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset contains 500 candidates per query and
achieves nDCG@10 = 0.0903, hit@10 = 0.1383, and recall@100 = 0.2207. BM25 is
the weakest profile by a large margin.

This is expected for Belebele-style retrieval. Questions and passages may be in
different scripts or language variants, and a question can ask about a passage
fact without repeating many exact words. Term frequency and exact matching are
therefore poor proxies for answer support in this multilingual setting.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset contains 500 candidates per
query and achieves nDCG@10 = 0.2781, hit@10 = 0.3404, and recall@100 = 0.4787.
Dense retrieval is the strongest observed profile.

The result shows that multilingual embedding similarity is crucial. Dense
retrieval can bridge paraphrase, translation-like alignment, and cross-script
semantic similarity better than BM25. The absolute scores are still modest,
which suggests that short answer-supporting passages and many languages create
a difficult retrieval setting even for multilingual dense models.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains mostly 100 candidates per
query, with 221 queries using a rank-101 safeguard row. It achieves nDCG@10 =
0.1782, hit@10 = 0.2473, and recall@100 = 0.4122. Hybrid retrieval improves
over BM25 but remains below dense retrieval on every ranking metric.

The large number of safeguard rows indicates that many positives would not
naturally appear in the top-100 hybrid list. The hybrid candidate pool is useful
relative to lexical retrieval, but sparse evidence appears to dilute rather
than improve the stronger dense signal for this task.

### Metric Interpretation for Model Researchers

This task is single-positive: each query has exactly one answer-supporting
passage. Hit@10 measures whether the correct passage appears near the top.
nDCG@10 is sensitive to its exact rank, and recall@100 measures whether it is
available for reranking.

Because the task is multilingual and cross-script, low BM25 performance should
not be interpreted as evidence that the corpus lacks signal. It indicates that
the signal is semantic, answer-supporting, and language-variant dependent.
Dense multilingual alignment is the central capability being tested.

### Query and Relevance Type Tendencies

Queries are native-language or transliterated questions derived from reading
comprehension items. They ask about facts, explanations, or details in short
passages. Relevant documents are passages that explicitly support the answer.

The task rewards models that can align questions to passages across many
scripts and language variants. It also rewards passage-level comprehension:
the retrieved text must answer the question, not just share a topic.

### Representative Failure Modes

BM25 fails when question and passage use different scripts, translations, or
paraphrases. Dense retrieval can fail when languages are low-resource, scripts
are underrepresented, or several FLORES passages share similar topic
vocabulary. Hybrid retrieval can inherit weak lexical candidates that reduce
the rank of the dense-positive passage.

Rerankers can fail if they treat the task as generic topical retrieval instead
of checking whether the passage actually supports the question's answer.

### Training Data That May Help

Useful training data includes non-overlapping Belebele or FLORES
passage-question pairs, multilingual reading-comprehension retrieval data,
native-language QA retrieval pairs, and cross-script hard negatives. Training
should avoid using the Nano split's questions, qrels, or positive passages.

Synthetic data can generate native-language questions from short passages in
FLORES-like domains. Negatives should share topic, entities, or translated
content but fail to answer the question. The positive passage must explicitly
support the answer.

### Model Improvement Notes

Dense retrievers should improve multilingual alignment across scripts and
low-resource language variants. Sparse systems are unlikely to be competitive
without translation, transliteration, or expansion. Rerankers should compare
question meaning against passage evidence rather than rely on word overlap.

For hybrid systems, `NanoMMTEB-v2 / belebele` is a warning case: adding sparse
evidence does not automatically improve a multilingual dense signal. Dense
retrieval is the best first-stage profile here, and hybrid systems need careful
weighting or multilingual lexical expansion.

## Example Data

| Query | Positive document |
| --- | --- |
| Vad är enligt avsnittet inte ett bra knep för att spela dragspel? [65 chars] | Se till att din hand är så avslappnad som möjligt medan du fortfarande träffar alla noter korrekt. Försök också att inte göra många överflödiga rörelser med fingrarna. På det här sättet tröttar du ut... [200 / 440 chars] |
| وفقاً للفقرة، ما الذي لا يُعتبر نصيحة دقيقة للعزف الناجح على الأكورديون؟ [72 chars] | Make sure your hand is as relaxed as possible while still hitting all the notes correctly - also try not to make much extraneous motion with your fingers. This way, you will tire yourself out as littl... [200 / 399 chars] |
| According to the passage, what would not be considered an accurate tip for successfully playing the... [100 / 110 chars] | تأكد من استرخاء يدك قدر الإمكان مع الاستمرار في ضرب كل النغمات بشكل صحيح - حاول كذلك عدم القيام بحركاتٍ غريبةٍ بأصابعك. لن تبذل مجهوداً كبيراً إذا اتبعت تلك الطريقة. ضع نصب عينيك أنه ليس عليك الضغط عل... [200 / 364 chars] |
| Čo sa podľa úryvku nepovažuje za presné odporúčanie, ako dobre hrať na akordeóne? [81 chars] | Make sure your hand is as relaxed as possible while still hitting all the notes correctly - also try not to make much extraneous motion with your fingers. This way, you will tire yourself out as littl... [200 / 399 chars] |
| anuchhed anusar, kun MySpace suvidhaley padhna samasya vayeka vidyarthiharulai faidajanak huna sakch... [100 / 103 chars] | MySpace is the third most popular website used in the United States and has 54 million profiles currently. These websites have gotten a lot of attention, especially in the education setting. There are... [200 / 638 chars] |

### Public Sources

- [The Belebele Benchmark: a Parallel Reading Comprehension Dataset in 122 Language Variants](https://arxiv.org/abs/2308.16884),
  2024.
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595),
  2025.
- [mteb/belebele](https://huggingface.co/datasets/mteb/belebele).
- [hakari-bench/NanoMMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoMMTEB-v2),
  Nano benchmark dataset.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| The Belebele Benchmark: a Parallel Reading Comprehension Dataset in 122 Language Variants | 2024 | task paper | [https://arxiv.org/abs/2308.16884](https://arxiv.org/abs/2308.16884) |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | [https://arxiv.org/abs/2502.13595](https://arxiv.org/abs/2502.13595) |
| mteb/belebele | 2024 | dataset card | [https://huggingface.co/datasets/mteb/belebele](https://huggingface.co/datasets/mteb/belebele) |

### Representative Snippets

| Query pattern | Positive document pattern |
| --- | --- |
| A Swedish question asking which accordion-playing tip is not accurate. | A Swedish passage about relaxing the hand while playing accordion. |
| An Arabic question asking the same accordion-detail question. | An English or Arabic-script passage about accordion technique. |
| An English question about accurate accordion-playing advice. | An Arabic-script passage with the supporting information. |
| A Slovak question about accordion technique. | A short passage about minimizing unnecessary finger motion. |
| A romanized question about a MySpace feature for students with reading problems. | A short passage about social-networking websites in education. |
