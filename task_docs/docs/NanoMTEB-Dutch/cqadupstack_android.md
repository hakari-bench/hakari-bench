# NanoMTEB-Dutch / cqadupstack_android

## Overview

`cqadupstack_android` is the Dutch-translated Android subforum split of
CQADupStack in NanoMTEB-Dutch. Queries are Android Stack Exchange questions,
and relevant documents are earlier questions marked as duplicates. The Nano
split contains 200 queries, 10,000 documents, and 200 positive qrel rows, with
one positive duplicate per query. It measures duplicate-question retrieval for
mobile troubleshooting, Android ROMs, Google Play, device-specific behavior,
screen streaming, app compatibility, and peripheral controls.

This task is much harder than a small same-language reading-comprehension split.
The corpus is larger, forum posts are longer and noisier, and duplicate
questions can differ substantially in wording. BM25 benefits from technical
terms and product names, but its top-10 score is modest. Dense retrieval with
`harrier_oss_v1_270m` is stronger, and `reranking_hybrid` gives nearly the same
top-10 quality with slightly higher top-100 coverage. The task is therefore a
useful diagnostic for whether a retrieval model can combine technical lexical
anchors with semantic duplicate intent in translated Dutch support data.

## Details

### What the Original Data Measures

[CQADupStack: A Benchmark Data Set for Community Question-Answering Research](https://doi.org/10.1145/2838931.2838934)
introduced CQADupStack as a benchmark built from Stack Exchange duplicate
question links. Its retrieval setting models the practical task of finding a
previously asked question that duplicates the user's new question. The Android
subset focuses on mobile operating-system and device-support questions, where
duplicates often share an underlying troubleshooting intent but may use
different titles, body details, or device names.

The Dutch version used here comes from BEIR-NL, which translated BEIR retrieval
datasets into Dutch for zero-shot information retrieval evaluation. As a
result, this split is not originally native Dutch forum text. It preserves the
CQADupStack duplicate-question structure while changing the language surface
through translation. The benchmark is therefore both a duplicate retrieval task
and a test of how translated technical support text affects lexical and dense
retrieval behavior.

### Observed Data Profile

The Nano split has 200 short queries and 10,000 candidate documents. Queries
average 59.10 characters, while documents average 638.08 characters. Documents
often include a title, a duplicate marker, quoted prior-question text, and body
details about a device, app, Android version, or error message. This makes the
positive document much longer and noisier than the query.

Example questions ask why Android ROMs are device-specific, how to save a file
instead of opening it, how to stream an Android phone screen to a laptop, how to
fix a Google Play Services shared-user-ID installation error, and how to control
both volume and track skipping with headphones. Some duplicates are close title
matches, but many require recognizing that two differently worded support
questions describe the same practical problem.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 = 0.2944, hit@10 = 0.4250, and recall@100 = 0.6300 over
top-500 candidate lists. This score reflects a mixed lexical environment. BM25
can exploit exact technical tokens such as Android, ROM, Google Play, ICS,
Gallery, SGS-III, or quoted error messages. These terms often identify the
right product area and can retrieve a duplicate when the title wording is
similar.

The weak side of BM25 is duplicate intent. A user may describe the same problem
with different verbs, omit the exact app name, mention a different device, or
write a short title while the positive document contains a longer body. The
translation process can also vary terminology across otherwise related posts.
For researchers, the BM25 profile shows that lexical matching is valuable but
insufficient: term occurrence finds many technical neighbors, while duplicate
recognition still requires semantic matching.

### Dense Evaluation Profile

Dense retrieval with `harrier_oss_v1_270m` reaches nDCG@10 = 0.3862, hit@10 =
0.5450, and recall@100 = 0.7750. This is a clear improvement over BM25 on all
reported candidate metrics. The dense model is better at connecting paraphrased
support questions, such as "stream my screen" and "project my phone for a
presentation", or a short user symptom and a longer duplicate post that
contains the same troubleshooting goal.

Dense retrieval is not solved, however. The top-10 hit rate remains just over
half, which suggests that Android support posts contain many semantically close
but non-duplicate candidates. A model may retrieve a question about the same
device, app, error message, or OS version while missing the exact duplicate
intent. This makes the split useful for evaluating technical-domain semantic
specificity rather than only broad topic matching.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate column reaches nDCG@10 = 0.3836, hit@10 =
0.5400, and recall@100 = 0.7800, with 100 to 101 candidates per query and 44
rank-101 safeguard rows. Its top-10 quality is nearly identical to dense
retrieval, while its recall@100 is slightly higher. This indicates that the
hybrid pool successfully combines dense semantic duplicates with a small number
of BM25-only positives recovered through exact technical tokens.

The hybrid profile is useful for reranking experiments. It emulates a practical
hybrid search setting in which dense similarity provides the main duplicate
intent signal and sparse retrieval keeps rare technical identifiers from being
lost. Because its initial top-10 order is not much better than dense retrieval,
a reranker must still separate true duplicate intent from same-topic Android
neighbors.

### Metric Interpretation for Model Researchers

Each query has one positive duplicate, so nDCG@10 is a direct measure of how
highly that duplicate is ranked. Hit@10 measures whether a user would see the
duplicate quickly, while recall@100 measures whether a downstream reranker gets
a chance to recover it. The gap between BM25 recall@100 and dense or hybrid
recall@100 is large enough to matter for candidate-generation design.

Dense retrieval is the best single signal for top-10 quality, but the hybrid
candidate set has the best top-100 coverage. This is the kind of task where a
two-stage system can be justified: dense retrieval supplies semantic duplicate
matching, BM25 supplies rare technical anchors, and a reranker must decide
which candidate actually answers the duplicate-question relation.

### Query and Relevance Type Tendencies

The queries are short Dutch Android support questions. They often mention a
device family, Android feature, app-store component, connectivity mode, file
type, or error message. The positive document is another translated question
that was marked as a duplicate in the original Stack Exchange data.

Relevance is based on duplicate intent, not answer similarity alone. Two posts
can mention Google Play or headphones but ask different questions. Conversely,
two duplicates may share few words if one asks about the symptom and the other
uses a more technical description of the same issue.

### Representative Failure Modes

BM25 can fail when the duplicate uses different phrasing or when a long post
contains many unrelated terms that dilute the matching signal. It can also
over-rank documents that share a rare device name or error phrase but describe a
different problem. Dense retrieval can fail by retrieving semantically adjacent
support posts that are not true duplicates, especially when many Android issues
share the same product, version, or hardware context.

Hybrid failures occur when both signals agree on the broad technical area but
not on duplicate identity. A candidate may be about Google Play Services,
screen streaming, or headphone controls without being the same question. These
cases are valuable hard negatives for reranker training.

### Training Data That May Help

Useful training data includes non-overlapping CQADupStack Android duplicate
question pairs, Dutch or translated mobile-support duplicate questions, and
multilingual technical support duplicate retrieval data. Training should
exclude the translated CQADupStack Android test queries and positive duplicate
questions used by this Nano split.

Synthetic data can be generated from Android support posts outside the
evaluation set. A good synthetic pair should create two Dutch questions with
the same troubleshooting intent but different wording, device detail, or
symptom framing. Same-topic hard negatives should mention the same app,
hardware, or Android feature while solving a different problem.

### Model Improvement Notes

Improving this task requires both technical lexical memory and semantic
duplicate understanding. Dense encoders should be trained with hard negatives
from the same Android category so that they do not collapse all related support
questions together. Sparse or hybrid features remain useful for rare exact
tokens such as device names, app components, and quoted error strings.

For rerankers, the important behavior is duplicate-intent verification. The
reranker should compare the user's problem description against the candidate
question and body, giving less weight to incidental shared Android vocabulary
when the underlying issue is different.

## Example Data

### Public Sources

- [CQADupStack: A Benchmark Data Set for Community Question-Answering Research](https://doi.org/10.1145/2838931.2838934), 2015.
- [Author-hosted CQADupStack PDF](https://eltimster.github.io/www/pubs/adcs2015.pdf), 2015.
- [BEIR-NL: Zero-shot Information Retrieval Benchmark for the Dutch Language](https://aclanthology.org/2025.bucc-1.5/), 2025.
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663), 2021.
- [clips/beir-nl-cqadupstack](https://huggingface.co/datasets/clips/beir-nl-cqadupstack), source dataset card.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| CQADupStack: A Benchmark Data Set for Community Question-Answering Research | 2015 | proceedings paper | https://doi.org/10.1145/2838931.2838934 |
| BEIR-NL: Zero-shot Information Retrieval Benchmark for the Dutch Language | 2025 | proceedings paper | https://aclanthology.org/2025.bucc-1.5/ |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | arXiv paper | https://arxiv.org/abs/2104.08663 |
| clips/beir-nl-cqadupstack |  | dataset card | https://huggingface.co/datasets/clips/beir-nl-cqadupstack |

### Representative Snippets

| Query | Positive passage |
| --- | --- |
| Waarom is een Android ROM apparaatspecifiek? | A translated duplicate asks why Android cannot be installed like a regular operating system and discusses device-specific Android builds. |
| Hoe kan ik een bestand opslaan in plaats van het te openen? | A translated Android question asks how to download an audio file from a website so it can be used later offline. |
| Hoe kan ik een video stream van het scherm van mijn Android telefoon vastleggen en deze op mijn laptop weergeven? | A translated duplicate asks how to stream or project an Android phone screen, including for presentation or game playback. |
| Niet compatibel met andere applicaties die dezelfde gedeelde gebruikers-ID gebruiken bij het installeren van Google Play-services? | A translated post reports that Google Play Services cannot be installed because another application uses the same shared user ID. |
| Hoe kan ik zowel het volume als het overslaan van nummers bedienen met mijn hoofdtelefoon? | A translated duplicate discusses headphone controls on an Android phone, including track switching and volume behavior. |
