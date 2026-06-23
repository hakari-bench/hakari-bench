# NanoBRIGHT / NanoBrightBiology

## Overview

NanoBrightBiology is the compact NanoBRIGHT slice for Biology StackExchange-style retrieval. Each query is a detailed biology question or explanatory request, and relevant documents are passages from cited web sources that help answer it. The retrieval goal is to find supporting biological evidence or mechanism passages, not merely pages that repeat the organisms or terms in the question. This makes the task useful for evaluating reasoning-intensive scientific retrieval, source-backed QA, and multi-positive biological explanation matching.

## Details

### What the Original Data Measures

BRIGHT defines its StackExchange tasks as retrieval over knowledge-intensive posts whose answers cite external web documents. Relevance is based on cited documents that support the reasoning needed for a high-quality answer, followed by validation. Positives may therefore be evidence sources rather than direct answer snippets.

In the Biology slice, questions often ask about mechanisms, evolutionary explanations, physiology, genetics, viruses, immunity, plant biology, or perception. A relevant document should help explain the biological question. It can be a cited encyclopedia passage, scientific page, or reference passage that provides the needed concept.

### Observed Data Profile

The task contains 103 queries, 10,000 documents, and 372 relevance judgments. It is strongly multi-positive, with an average of 3.61 positives per query. The minimum is 1, the median is 3.0, the maximum is 19, and 93 queries are multi-positive, or 90.29% of the set.

Queries average 523.03 characters, while documents average 473.93 characters. Queries are often long enough to include context and uncertainty, while documents are shorter cited passages. The model must connect user-level biological questions to technical mechanisms and supporting sources.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.3425, hit@10 of 0.5825, and recall@100 of 0.6801 using the top-500 BM25 candidate subset. Lexical matching helps when questions include distinctive terms such as fluoride, phototropism, phages, tumors, or chlorophyll. It can often retrieve relevant source material when exact terminology appears.

The limitation is mechanism matching. Biology questions often use lay phrasing, while cited passages use technical vocabulary. BM25 may retrieve pages about the same organism or process but miss the passage that supports the specific explanation.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.4945, hit@10 of 0.7670, and recall@100 of 0.8387. Dense retrieval is the strongest direct top-rank profile. It improves substantially over BM25 across all main metrics, showing that embedding similarity helps bridge user questions and biological mechanism passages.

This is a strong signal that the task is semantic and explanatory. Relevant sources may not repeat the question terms, but they contain the concept needed for the answer. Dense retrieval is better at matching the biological relation, mechanism, or evidence need.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.4690, hit@10 of 0.7767, and recall@100 of 0.8495. It uses a top-100 candidate range with an optional rank-101 safeguard; this slice has 3 safeguard rows, candidate counts from 100 to 101, and a mean of 100.03 candidates. Hybrid has the best hit@10 and recall@100, while dense retrieval has the best nDCG@10.

This means hybrid search is a strong candidate pool for reranking. BM25 contributes exact biological terminology, while dense retrieval contributes mechanism-level semantic matching. The combined pool slightly broadens coverage, even though dense retrieval orders the top results better.

### Metric Interpretation for Model Researchers

Because most queries have multiple positives, nDCG@10 measures whether the first page contains useful supporting sources, while hit@10 only checks whether at least one source appears. recall@100 measures candidate completeness for downstream explanation or answer generation.

The comparison shows that BM25 is limited by vocabulary mismatch, dense retrieval is strongest for top-rank support, and reranking_hybrid gives the broadest candidate coverage. This task is useful for testing biology reasoning support retrieval rather than keyword search.

### Query and Relevance Type Tendencies

Queries include questions about the longest-lasting protein in the human body, whether kissing is natural, what light plants cannot photosynthesize with, why immune systems may not detect tumors, and whether viruses can be used as antibiotics. Positive documents discuss elastin half-life, animal kissing analogies, chlorophyll, MHC and immune response, bacteriophage therapy, and related concepts.

The task rewards connecting an explanatory question to a source passage that supports the reasoning. A passage can share the same organism or process and still fail if it does not answer the mechanism.

### Representative Failure Modes

Likely failures include retrieving same-term pages that do not answer the mechanism, missing technical synonyms, over-ranking broad encyclopedia pages, and under-covering multiple cited sources. BM25 may be too literal, while dense retrieval may sometimes retrieve plausible but unsupported biological neighbors.

### Training Data That May Help

Useful training data includes non-overlapping Biology StackExchange posts with cited sources, biology QA with source citations, textbook or Wikipedia retrieval pairs, and hard negatives about the same organism or mechanism but a different explanation. Multi-positive supervision should be preserved.

### Model Improvement Notes

A model targeting this task should improve mechanism-level evidence retrieval. Sparse systems need biological synonym expansion and term normalization. Dense systems are strong and should train on question-to-source citation pairs. Hybrid systems are useful for reranking because they combine exact biological terms with semantic explanation matching.

## Example Data

| Query | Positive document |
| --- | --- |
| What is the longest-lasting protein in a human body? Protein life times are, on average, not particu... [100 / 1,199 chars] | Characteristics[edit] Elastin is a very long-lived protein, with a half-life of over 78 years in humans. [104 chars] |
| Is kissing a natural human activity? The word natural here is meant in contrast to it being a sociol... [100 / 435 chars] | Biology and evolution[edit] Black-tailed prairie dogs "kissing." Prairie dogs use a nuzzle of this variety to greet their relatives. Within the natural world of other animals, there are numerous analo... [200 / 3,310 chars] |
| What types of light can't a plant photosynthesize in? I have a plant on my desk, and it got me to wo... [100 / 509 chars] | Chlorophyll is any of several related green pigments found in cyanobacteria and in the chloroplasts of algae and plants. Its name is derived from the Greek words χλωρός, khloros ("pale green") and φύλ... [200 / 712 chars] |
| If Tumors have lots of mutations in them how is it the immune system can't detect them? If a cancero... [100 / 425 chars] | In transplant rejection[edit] In a transplant procedure, as of an organ or stem cells, MHC molecules themselves act as antigens and can provoke immune response in the recipient, thus causing transplan... [200 / 3,065 chars] |
| Could viruses be used as antibiotics? Could we use viruses that only affect bacteria to act as antib... [100 / 204 chars] | Applications[edit] Collection[edit] Phages for therapeutic use can be collected from environmental sources that likely contain high quantities of bacteria and bacteriophages, such as effluent outlets,... [200 / 7,339 chars] |

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original benchmark paper | [BRIGHT](https://arxiv.org/abs/2407.12883) |
| Project page | [BRIGHT project page](https://brightbenchmark.github.io/) |
| Source dataset | [xlangai/BRIGHT](https://huggingface.co/datasets/xlangai/BRIGHT) |
| NanoBRIGHT dataset | [hakari-bench/NanoBRIGHT](https://huggingface.co/datasets/hakari-bench/NanoBRIGHT) |

Representative query and positive source snippets:

| Query | Positive document snippet |
| --- | --- |
| What is the longest-lasting protein in a human body? | Elastin is a very long-lived protein, with a half-life of over 78 years in humans. |
| Is kissing a natural human activity? | Prairie dogs use a nuzzle-like behavior to greet relatives, and other animals have analogies to kissing. |
| What types of light can't a plant photosynthesize in? | Chlorophyll is a green pigment found in cyanobacteria and chloroplasts of algae and plants. |
| If tumors have many mutations, why can't the immune system detect them? | MHC molecules can act as antigens and provoke immune response in transplant rejection. |
| Could viruses be used as antibiotics? | Phages for therapeutic use can be collected from sources rich in bacteria and bacteriophages. |
