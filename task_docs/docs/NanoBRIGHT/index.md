# NanoBRIGHT

## Overview

NanoBRIGHT is the compact Nano set for BRIGHT, a reasoning-intensive retrieval
benchmark. It contains English retrieval tasks from math problem solving,
theorem use, programming, StackExchange-style evidence retrieval, and
long-document web evidence retrieval. The positive document is often useful
because it supports a reasoning step, not because it paraphrases the query.

This group is useful for evaluating whether retrievers can connect a query to a
mechanism, theorem, algorithm, cited source, API behavior, or supporting
evidence. Many queries contain enough domain vocabulary for BM25 to find topical
neighbors, but topical neighbors are often wrong. Dense retrieval tests whether
embedding similarity captures the hidden reasoning relation, and
`reranking_hybrid` is valuable when exact technical terms and semantic problem
structure recover different positives.

## What This Group Measures

[BRIGHT: A Realistic and Challenging Benchmark for Reasoning-Intensive Retrieval](https://arxiv.org/abs/2407.12883)
introduces retrieval tasks where standard lexical or semantic matching is not
enough. NanoBRIGHT keeps that premise in smaller form. AoPS and TheoremQA tasks
retrieve problems or theorem statements connected by solution skill. LeetCode
and Pony tasks retrieve algorithmic or language-reference evidence. Biology,
Earth Science, Economics, Psychology, Robotics, Stack Overflow, and Sustainable
Living tasks retrieve cited support for complex user questions, with long
variants retrieving full source pages.

The group measures reasoning-aware first-stage retrieval. A strong model should
retrieve evidence that helps solve or justify the query, even when the evidence
does not repeat the query wording.

## Task Families

- **Mathematical and theorem retrieval:** `NanoBrightAops`,
  `NanoBrightTheoremQAQuestions`, and `NanoBrightTheoremQATheorems` connect
  problems to shared theorems, proof ideas, or problem-solving skills.
- **Programming retrieval:** `NanoBrightLeetcode`, `NanoBrightPony`, and
  `NanoBrightPonyLong` require algorithmic, API, or language-reference matching.
- **StackExchange evidence retrieval:** Biology, Earth Science, Economics,
  Psychology, Robotics, Stack Overflow, and Sustainable Living retrieve
  supporting cited passages for complex questions.
- **Long-document retrieval:** the `Long` variants retrieve complete cited pages
  with very long documents, testing whether candidate generation survives large
  amounts of unrelated context.

## Dataset Shape

NanoBRIGHT contains 20 task pages, 2,245 queries, 121,771 split-local documents,
and 9,287 positive qrel rows. All tasks are English, but their formats differ
substantially. LeetCode, Robotics, and Stack Overflow queries can be long and
technical; theorem queries can be compact but require abstract matching; long
variants have small document pools with very large documents.

The group is multi-positive overall. Passage-style StackExchange tasks,
`NanoBrightPony`, and several domain splits have many positives per query, while
long-document variants and theorem retrieval are closer to single-positive.
This makes Recall@100 important: a retriever may find a plausible supporting
document but still miss much of the relevant set.

## Retrieval Behavior

### BM25 Profile

BM25 performs best when the query contains exact technical phrases that appear
in the support document. Stack Overflow long documents, Earth Science, Biology,
and Sustainable Living have visible sparse signal. The theorem-statement task
is the hardest BM25 case because applied problem text rarely looks like a formal
theorem statement. Pony is also hard because many programming tasks share
surface vocabulary without sharing the relevant language behavior.

The key lesson is that technical vocabulary does not make retrieval easy. It can
retrieve domain neighbors, but the benchmark rewards documents that support the
reasoning path.

### Dense Profile

Dense retrieval is helpful on many reasoning tasks, especially Biology,
EarthScience, Psychology, SustainableLiving, and theorem-question retrieval. It
can connect a problem to supporting evidence even when wording differs. Dense
retrieval is also valuable on long-document variants where exact terms may be
buried among unrelated page text.

Dense retrieval still struggles when the relevance relation is highly formal or
algorithmic. Theorem statements, Pony tasks, and some programming cases require
precise matching of method, API behavior, or proof concept, not just topical
semantic similarity.

### Reranking Hybrid Profile

`reranking_hybrid` is particularly informative in NanoBRIGHT. It is the best
profile for tasks such as EarthScience, LeetCode, Pony, Stack Overflow,
Robotics, and several long-document variants. These are cases where sparse
anchors and dense problem structure recover complementary candidates.

For reranker experiments, NanoBRIGHT is a strong stress test because candidate
loss is easy: if the initial pool misses the theorem, algorithm, or cited page,
the reranker has no chance to recover the correct reasoning evidence.

## Task Summary

| Task | Retrieval shape | Queries | Docs | Positives | BM25 nDCG@10 | Dense nDCG@10 | Reranking hybrid nDCG@10 | Best profile |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| [NanoBrightAops](NanoBrightAops.md) | math problem to same-skill problem | 111 | 10,000 | 524 | 0.1433 | 0.2623 | 0.2167 | Dense |
| [NanoBrightBiology](NanoBrightBiology.md) | biology question to cited passage | 103 | 10,000 | 372 | 0.3425 | 0.4945 | 0.4690 | Dense |
| [NanoBrightBiologyLong](NanoBrightBiologyLong.md) | biology question to full source page | 103 | 498 | 134 | 0.3708 | 0.5779 | 0.4897 | Dense |
| [NanoBrightEarthScience](NanoBrightEarthScience.md) | earth science question to cited passage | 116 | 10,000 | 579 | 0.4611 | 0.5406 | 0.5518 | Reranking hybrid |
| [NanoBrightEarthScienceLong](NanoBrightEarthScienceLong.md) | earth science question to full source page | 116 | 587 | 186 | 0.3526 | 0.5786 | 0.4971 | Dense |
| [NanoBrightEconomics](NanoBrightEconomics.md) | economics question to cited passage | 103 | 10,000 | 800 | 0.3029 | 0.4095 | 0.3875 | Dense |
| [NanoBrightEconomicsLong](NanoBrightEconomicsLong.md) | economics question to full source page | 103 | 515 | 109 | 0.2658 | 0.4266 | 0.3764 | Dense |
| [NanoBrightLeetcode](NanoBrightLeetcode.md) | programming problem to algorithmic neighbor | 142 | 10,000 | 262 | 0.2655 | 0.3024 | 0.3048 | Reranking hybrid |
| [NanoBrightPony](NanoBrightPony.md) | Pony task to support passage | 112 | 6,183 | 2,219 | 0.0496 | 0.0219 | 0.0780 | Reranking hybrid |
| [NanoBrightPonyLong](NanoBrightPonyLong.md) | Pony task to long reference page | 112 | 577 | 769 | 0.2244 | 0.0767 | 0.2871 | Reranking hybrid |
| [NanoBrightPsychology](NanoBrightPsychology.md) | psychology question to cited passage | 101 | 10,000 | 692 | 0.2474 | 0.4591 | 0.4124 | Dense |
| [NanoBrightPsychologyLong](NanoBrightPsychologyLong.md) | psychology question to full source page | 101 | 509 | 116 | 0.3010 | 0.5069 | 0.4149 | Dense |
| [NanoBrightRobotics](NanoBrightRobotics.md) | robotics question to cited passage | 101 | 10,000 | 518 | 0.2607 | 0.2589 | 0.2976 | Reranking hybrid |
| [NanoBrightRoboticsLong](NanoBrightRoboticsLong.md) | robotics question to full source page | 101 | 505 | 106 | 0.2490 | 0.2851 | 0.2866 | Reranking hybrid |
| [NanoBrightStackoverflow](NanoBrightStackoverflow.md) | developer question to support passage | 117 | 10,000 | 478 | 0.3685 | 0.4033 | 0.4686 | Reranking hybrid |
| [NanoBrightStackoverflowLong](NanoBrightStackoverflowLong.md) | developer question to full source page | 117 | 1,846 | 129 | 0.4440 | 0.3894 | 0.4744 | Reranking hybrid |
| [NanoBrightSustainableLiving](NanoBrightSustainableLiving.md) | sustainability question to cited passage | 108 | 10,000 | 575 | 0.4189 | 0.5338 | 0.5198 | Dense |
| [NanoBrightSustainableLivingLong](NanoBrightSustainableLivingLong.md) | sustainability question to full page | 108 | 551 | 129 | 0.3277 | 0.5501 | 0.4436 | Dense |
| [NanoBrightTheoremQAQuestions](NanoBrightTheoremQAQuestions.md) | STEM question to solved theorem-use question | 194 | 10,000 | 439 | 0.1646 | 0.2798 | 0.2316 | Dense |
| [NanoBrightTheoremQATheorems](NanoBrightTheoremQATheorems.md) | STEM question to theorem statement | 76 | 10,000 | 151 | 0.0198 | 0.1653 | 0.0895 | Dense |

## Interpretation Notes for Model Researchers

NanoBRIGHT is best read as a first-stage reasoning retrieval probe. High scores
suggest the model can connect queries to useful evidence, not just similar text.
The long variants should be interpreted separately from passage variants:
document pools are smaller, but documents contain much more irrelevant context.

Profile differences are especially important. BM25-led behavior points to exact
technical anchors. Dense-led behavior points to semantic problem-structure
matching. Hybrid-led behavior points to candidate complementarity, often in code
and long-document tasks where exact identifiers and broader semantic cues both
matter.

## Training and Leakage Notes

Useful training data includes theorem-labeled solved problems, contest math
problem families, algorithm-problem similarity data, programming documentation
retrieval, question-to-cited-source pairs, scientific and technical QA with
references, and long-document evidence retrieval. Hard negatives should share
the same domain vocabulary while requiring a different theorem, algorithm,
mechanism, API behavior, or cited source.

Exclude NanoBRIGHT evaluation queries, positives, qrels, and source pages.
Long-document variants are especially leakage-sensitive because one full page
can contain passages related to many questions.

## Public Sources

- [BRIGHT: A Realistic and Challenging Benchmark for Reasoning-Intensive Retrieval](https://arxiv.org/abs/2407.12883), 2024.

### Source Reference Table

| Source | Year | Type | URL |
| --- | ---: | --- | --- |
| BRIGHT: A Realistic and Challenging Benchmark for Reasoning-Intensive Retrieval | 2024 | paper | https://arxiv.org/abs/2407.12883 |
