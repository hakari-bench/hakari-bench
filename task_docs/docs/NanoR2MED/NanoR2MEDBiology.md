# NanoR2MED / NanoR2MEDBiology

## Overview

`NanoR2MEDBiology` is an English reasoning-driven biology retrieval task from R2MED. Queries are Biology StackExchange questions, and documents are explanatory biology passages drawn from web or Wikipedia-derived sources. Each query can have multiple relevant passages, so the task measures retrieval of answer-supporting evidence rather than one exact passage. Dense retrieval is much stronger than BM25, while the hybrid pool improves hit@10 and recall@100 but trails dense retrieval on nDCG@10. The split is useful for evaluating concept selection in biology questions with everyday phrasing.

## Details

### What the Original Data Measures

R2MED frames retrieval as finding documents that support a latent reasoning answer. The benchmark paper includes Q&A reference retrieval, clinical evidence retrieval, and clinical case retrieval. Biology is part of the Q&A reference retrieval group and is adopted from BRIGHT-style reasoning-intensive retrieval data.

In this task, StackExchange questions serve as queries and external answer-supporting pages serve as positives. Relevance often depends on identifying the biological mechanism, molecule, organism, or evolutionary concept behind the question rather than matching a short keyword string.

### Observed Data Profile

The Nano split contains 103 queries, 10,000 documents, and 374 positive qrel rows. Queries average 523.03 characters, and documents average 474.07 characters.

The task is strongly multi-positive: each query has 3.63 positives on average, with a median of 3 and a maximum of 19. Ninety-three of 103 queries, or 90.29%, have multiple positives. Examples ask about long-lived proteins in the human body, whether kissing is natural human behavior, which monitor light plants can use for photosynthesis, immune recognition of tumor mutations, and bacteriophage therapy.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.3455, hit@10 of 0.5922, and recall@100 of 0.6818. BM25 benefits from clear entity or concept words such as chlorophyll, phage, tumor, protein, and photosynthesis.

The remaining difficulty is conceptual. Many questions are phrased as everyday puzzles or broad biological curiosity, while the relevant documents use scientific terminology. BM25 can retrieve the same broad biological topic but miss the mechanism that actually supports the answer.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.4953, hit@10 of 0.7573, and recall@100 of 0.8369. Dense retrieval clearly outperforms BM25 across all reported metrics. This shows that embedding similarity is better at mapping informal biology questions to explanatory scientific passages.

Dense retrieval is especially useful when the query describes a phenomenon in plain language and the document names the underlying mechanism. It is the strongest standalone ranking profile for this split.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates, with three rows receiving the optional rank-101 safeguard. It reaches nDCG@10 of 0.4722, hit@10 of 0.7864, and recall@100 of 0.8503. Hybrid retrieval improves hit@10 and recall@100 over dense retrieval but has lower nDCG@10.

This means hybrid candidate construction is valuable for coverage, but dense retrieval still orders the most relevant evidence more effectively at the very top. A reranker should use the hybrid pool to recover additional positives while restoring dense-like top-rank precision.

### Metric Interpretation for Model Researchers

Because most queries have multiple positives, nDCG@10 captures graded quality of the ranked evidence set, not just whether one document is found. Hit@10 measures whether the system finds any supporting evidence early. Recall@100 measures how much of the available positive set is exposed to a reranker.

For Biology, dense retrieval is the top-rank baseline, while hybrid retrieval is the stronger coverage-oriented pool. A model improvement should be judged by whether it retrieves the right mechanism, not merely the same broad biological topic.

### Query and Relevance Type Tendencies

Queries are natural-language biology questions, often with a misconception, analogy, or explanatory goal. Relevant passages are encyclopedia-like or educational descriptions of proteins, behavior, plant pigments, antigen presentation, phage therapy, and related mechanisms.

The relevance relation is answer support. A passage may be relevant if it explains the mechanism needed to answer the question, even if it does not repeat the user's exact phrasing.

### Representative Failure Modes

Common failures include retrieving a page about the same organism or broad topic but the wrong mechanism, matching everyday words such as light or smell without the needed biological concept, and ranking disease or immune-system passages that do not support the requested causal explanation. BM25 misses latent concepts; dense retrieval can overgeneralize among related mechanisms.

### Training Data That May Help

Useful training data includes non-overlapping Biology StackExchange answer-link retrieval, BRIGHT reasoning-intensive biology retrieval without overlap, biological concept QA, Wikipedia section retrieval, and hard negatives from adjacent mechanisms or taxa. Evaluation queries, qrels, and positive passages should be excluded, and overlap with BRIGHT should be audited before training.

### Model Improvement Notes

Models should learn to map informal biology questions to scientific mechanisms and evidence passages. Multi-positive objectives are appropriate because most queries have several supporting documents. Hard negatives should share the same broad biology field while changing the mechanism, molecule, organism, or evolutionary explanation.

## Example Data

| Query | Positive document |
| --- | --- |
| What is the longest-lasting protein in a human body? Protein life times are, on average, not particularly long, on a human life timescale. I was wondering, how old is the oldest protein in a human body? Just to clarify, I mean in terms of seconds/minutes/days passed from the moment that given protein was translated. I am not sure is the same thing as asking which human protein has the longest half-life, as I think there might be "tricks" the cell uses to elongate a given protein's half-life unde... [500 / 1,199 chars] | Characteristics[edit] Elastin is a very long-lived protein, with a half-life of over 78 years in humans. [104 chars] |
| Is kissing a natural human activity? The word natural here is meant in contrast to it being a sociological construct. Is kissing in all its forms something natural for humans? Is it instinctively erotic? Or is it just a conventional form to show trust and intimicy, i.e. the association besically just comes via a social means? Because the only other advantage of this mouth to mouth contact I could see is maybe for the immune system. [435 chars] | Biology and evolution[edit] Black-tailed prairie dogs "kissing." Prairie dogs use a nuzzle of this variety to greet their relatives. Within the natural world of other animals, there are numerous analogies to kissing, notes Crawley, such as "the billing of birds, the cataglottism of pigeons and the antennal play of some insects." Even among mammals such as the dog, cat and bear, similar behavior is noted. Anthropologists have not reached a conclusion as to whether kissing is learned or a behavior from instinct. It may be related to grooming behavior also seen between other animals, or arising as a result of mothers premasticating food for their children. Non-human primates also exhibit kissing behavior. Dogs, cats, birds and other animals display licking, nuzzling, and grooming behavior among themselves, and also towards humans or other species. This is sometimes interpreted by observers as a type of kissing. Kissing in humans is postulated to have evolved from the direct mouth-to-mouth... [1,000 / 3,310 chars] |
| What types of light can't a plant photosynthesize in? I have a plant on my desk, and it got me to wondering: Can my plant use the light from my monitors to photosynthesize? If so, what light (apart from green light, to a degree) can't plants use to perform photosynthesis? I know that plants have the photosynthetic pigments to absorb many different wavelengths of light (primarily red and blue) but would there be certain types of light it can't use? (The specific plant by the way is Schlumbergera... [500 / 509 chars] | Chlorophyll is any of several related green pigments found in cyanobacteria and in the chloroplasts of algae and plants. Its name is derived from the Greek words χλωρός, khloros ("pale green") and φύλλον, phyllon ("leaf"). Chlorophyll allows plants to absorb energy from light. Chlorophylls absorb light most strongly in the blue portion of the electromagnetic spectrum as well as the red portion. Conversely, it is a poor absorber of green and near-green portions of the spectrum. Hence chlorophyll-containing tissues appear green because green light, diffusively reflected by structures like cell walls, is less absorbed. Two types of chlorophyll exist in the photosystems of green plants: chlorophyll a and b. [712 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| R2MED: A Benchmark for Reasoning-Driven Medical Retrieval | 2025 | arXiv paper | [https://arxiv.org/abs/2505.14558](https://arxiv.org/abs/2505.14558) |
| R2MED project page | 2025 | project page | [https://r2med.github.io/](https://r2med.github.io/) |
| R2MED GitHub repository | 2025 | source repository | [https://github.com/R2MED/R2MED](https://github.com/R2MED/R2MED) |
| R2MED/Biology | 2025 | dataset card | [https://huggingface.co/datasets/R2MED/Biology](https://huggingface.co/datasets/R2MED/Biology) |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| What is the longest-lasting protein in the human body? | A passage identifying elastin as a very long-lived protein with a human half-life of more than 78 years. |
| Is kissing a natural human activity rather than only a sociological construct? | A passage discussing animal analogies to kissing and biological or evolutionary interpretations of the behavior. |
| What kinds of light can or cannot support plant photosynthesis from a monitor? | A passage explaining chlorophyll pigments in cyanobacteria, algae, and plants. |
| If tumors contain many mutations, why can the immune system fail to detect them? | A passage about antigen processing and presentation through the MHC class I pathway. |
| Could viruses that affect bacteria be used as antibiotics? | A passage about therapeutic applications of bacteriophages and collection of phages from bacteria-rich environments. |
