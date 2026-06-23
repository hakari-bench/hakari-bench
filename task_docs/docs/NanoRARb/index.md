# NanoRARb

## Overview

NanoRARb is the Nano task group for RAR-b, the Reasoning as Retrieval Benchmark.
It converts reasoning problems into retrieval tasks: the query is a question,
story context, code prompt, math problem, spatial scene, or temporal reasoning
prompt, and the relevant document is the correct answer, continuation, entity,
solution, or implementation from a large answer pool. The group tests whether a
retriever can rank logically correct answers, not just topically related text.

The group contains 3,400 queries, 156,037 task-local documents, and 3,584
positive qrel rows. Most tasks are single-positive; `NanoSpartQA` is the main
multi-positive exception. Documents are often short answer strings, while some
queries are very long, especially the TempReason context tasks. This makes the
group a compact stress test for reasoning-level semantic retrieval.

## What This Group Measures

RAR-b asks whether retrievers can solve reasoning problems after they are recast
as information retrieval. Instead of retrieving ordinary topical documents, the
model must retrieve the correct answer from a pool of plausible candidates. The
Nano group includes science QA, abductive story reasoning, event continuation,
physical and social commonsense, reading comprehension, spatial reasoning,
temporal reasoning, code generation, math problem solving, and Winograd-style
referent resolution.

This benchmark is intentionally hard for lexical retrieval. The positive answer
may be a short phrase, a date, an entity, a referent, a code snippet, or a
worked solution. The query may imply the answer through causal, temporal,
mathematical, spatial, or program-behavior constraints rather than through
shared vocabulary.

## Task Families

- **Commonsense and answer selection:** ARC-Challenge, AlphaNLI, HellaSwag,
  PIQA, SIQA, and WinoGrande-style tasks.
- **Reading and spatial reasoning:** `NanoQuail` and `NanoSpartQA` retrieve
  answers from narrative or spatial contexts.
- **Code reasoning:** `NanoRARbCode` retrieves implementations for code prompts.
- **Math reasoning:** `NanoRARbMath` retrieves worked mathematical solutions.
- **Temporal reasoning:** the TempReason L1/L2/L3 tasks retrieve dates or
  entities under temporal constraints.

## Dataset Shape

All task metadata is English. Each split has 200 queries. Candidate pools are
usually 10,000 documents, except `NanoARCChallenge`, `NanoSpartQA`, and
`NanoWinoGrande`, which use smaller pools. Most tasks have one positive per
query. `NanoSpartQA` averages 1.92 positives per query and has 384 qrel rows.

The query/document length contrast is important. TempReason context queries can
contain tens of thousands of characters of facts, while the target answer is a
short entity string. Math and code documents are longer because they contain
solutions or implementations. Many other tasks retrieve very short answers, so
retrieval success depends on reasoning, not document length.

## Retrieval Behavior

### BM25 Profile

BM25 is weak overall, with query-weighted nDCG@10 of 0.1536. This is expected:
the answer is often logically entailed by the query rather than lexically
similar to it. BM25 is strongest on `NanoRARbMath`, `NanoWinoGrande`, and
`NanoAlphaNLI`, where equations, quantities, story entities, or candidate
referents can overlap with the query. `NanoRARbMath` reaches 0.6147 nDCG@10,
and `NanoWinoGrande` reaches 0.5067.

BM25 nearly fails on pure temporal and social reasoning tasks. `NanoTempReasonL2Pure`
has 0.0000 nDCG@10, and `NanoSIQA` has 0.0239. These tasks require choosing an
answer that follows from world, social, or temporal structure rather than from
repeated words. BM25 is therefore a useful lower bound for the group, but not a
reasonable proxy for reasoning retrieval.

### Dense Profile

Dense retrieval with `harrier-oss-270m` is the strongest group-level profile,
with 0.2469 nDCG@10 and 0.6563 recall@100. It is best for many reasoning
families: ARC, AlphaNLI, PIQA, QuAIL, Math, SIQA, and most TempReason tasks.
The gains are particularly large for temporal tasks, where dense retrieval can
rank entities or dates better than sparse overlap even when absolute nDCG@10
remains low.

Dense is not uniformly best. `NanoHellaSwag`, `NanoRARbCode`, `NanoSpartQA`,
and `NanoWinoGrande` favor the reranking hybrid profile. Some of those tasks
still benefit from exact entities, identifiers, object labels, or code tokens.
This means dense reasoning retrieval helps substantially, but surface anchors
remain useful in several answer-pool settings.

### Reranking Hybrid Profile

The reranking hybrid profile is best for `NanoHellaSwag`, `NanoRARbCode`,
`NanoSpartQA`, and `NanoWinoGrande`. These tasks combine semantic plausibility
with surface cues: story continuations share entities and activities, code
answers share identifiers or API names, spatial answers share object labels,
and WinoGrande answers are often explicit referents in the sentence.

Hybrid trails dense on group-level nDCG@10 but remains close, and it improves
some recall-heavy or candidate-sensitive tasks. The practical interpretation is
that hybrid search can help when reasoning answers still contain lexical
anchors, while dense retrieval is the stronger default for pure temporal,
social, reading, and abductive reasoning.

## Task Summary

| Task | Family | Language | Queries | Docs | Positives | Positives/query | BM25 nDCG@10 | Dense nDCG@10 | Reranking hybrid nDCG@10 | Best profile |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| [NanoARCChallenge](NanoARCChallenge.md) | Science QA retrieval | `en` | 200 | 9,350 | 200 | 1.00 | 0.0386 | 0.1113 | 0.0642 | Dense |
| [NanoAlphaNLI](NanoAlphaNLI.md) | Abductive reasoning | `en` | 200 | 10,000 | 200 | 1.00 | 0.3288 | 0.5898 | 0.4777 | Dense |
| [NanoHellaSwag](NanoHellaSwag.md) | Event continuation | `en` | 200 | 10,000 | 200 | 1.00 | 0.1393 | 0.1253 | 0.1551 | Reranking hybrid |
| [NanoPIQA](NanoPIQA.md) | Physical commonsense | `en` | 200 | 10,000 | 200 | 1.00 | 0.2443 | 0.4017 | 0.3741 | Dense |
| [NanoQuail](NanoQuail.md) | Reading comprehension | `en` | 200 | 10,000 | 200 | 1.00 | 0.0522 | 0.1174 | 0.0982 | Dense |
| [NanoRARbCode](NanoRARbCode.md) | Code reasoning | `en` | 200 | 10,000 | 200 | 1.00 | 0.1318 | 0.1173 | 0.1773 | Reranking hybrid |
| [NanoRARbMath](NanoRARbMath.md) | Math reasoning | `en` | 200 | 10,000 | 200 | 1.00 | 0.6147 | 0.7818 | 0.7350 | Dense |
| [NanoSIQA](NanoSIQA.md) | Social commonsense | `en` | 200 | 10,000 | 200 | 1.00 | 0.0239 | 0.0618 | 0.0405 | Dense |
| [NanoSpartQA](NanoSpartQA.md) | Spatial reasoning | `en` | 200 | 1,592 | 384 | 1.92 | 0.1888 | 0.2634 | 0.3419 | Reranking hybrid |
| [NanoTempReasonL1](NanoTempReasonL1.md) | Temporal date reasoning | `en` | 200 | 10,000 | 200 | 1.00 | 0.0125 | 0.0488 | 0.0129 | Dense |
| [NanoTempReasonL2Context](NanoTempReasonL2Context.md) | Temporal entity reasoning | `en` | 200 | 10,000 | 200 | 1.00 | 0.1114 | 0.2171 | 0.2049 | Dense |
| [NanoTempReasonL2Fact](NanoTempReasonL2Fact.md) | Temporal entity reasoning | `en` | 200 | 10,000 | 200 | 1.00 | 0.0615 | 0.3005 | 0.2513 | Dense |
| [NanoTempReasonL2Pure](NanoTempReasonL2Pure.md) | Temporal entity reasoning | `en` | 200 | 10,000 | 200 | 1.00 | 0.0000 | 0.0483 | 0.0033 | Dense |
| [NanoTempReasonL3Context](NanoTempReasonL3Context.md) | Temporal relation reasoning | `en` | 200 | 10,000 | 200 | 1.00 | 0.0945 | 0.1926 | 0.1668 | Dense |
| [NanoTempReasonL3Fact](NanoTempReasonL3Fact.md) | Temporal relation reasoning | `en` | 200 | 10,000 | 200 | 1.00 | 0.0547 | 0.2549 | 0.1981 | Dense |
| [NanoTempReasonL3Pure](NanoTempReasonL3Pure.md) | Temporal relation reasoning | `en` | 200 | 10,000 | 200 | 1.00 | 0.0074 | 0.0707 | 0.0238 | Dense |
| [NanoWinoGrande](NanoWinoGrande.md) | Coreference reasoning | `en` | 200 | 5,095 | 200 | 1.00 | 0.5067 | 0.4946 | 0.6020 | Reranking hybrid |

## Interpretation Notes for Model Researchers

NanoRARb should be read as a reasoning-as-retrieval diagnostic. A strong score
on ordinary semantic retrieval does not guarantee strong performance here,
because the candidate document can be a short answer whose relevance is only
visible after reasoning. Dense retrieval improves many tasks, but the absolute
scores show that this remains difficult for embedding-only retrieval.

Task-family analysis is essential. Math and WinoGrande are much easier than
social, temporal, and reading-comprehension answer retrieval. Hybrid wins where
surface anchors remain important, while dense retrieval is better for most pure
reasoning tasks. The aggregate group score hides these differences.

## Training and Leakage Notes

Useful training data includes abductive story reasoning, event continuation,
physical and social commonsense QA, Winograd/coreference examples, ARC-style
science QA, passage QA answer retrieval, textual spatial reasoning, temporal
interval QA, docstring-to-code retrieval, and math problem-solution pairs.

Leakage control should exclude NanoRARb evaluation queries, qrels, candidate
answers, worked solutions, code snippets, and upstream reasoning benchmark test
examples. Synthetic data should preserve the reasoning relation and include
hard negatives that share vocabulary but fail the causal, temporal, spatial,
mathematical, social, or program-behavior constraint.

## Public Sources

- [RAR-b: Reasoning as Retrieval Benchmark](https://arxiv.org/abs/2404.06347), 2024.
- [ARC, the AI2 Reasoning Challenge](https://arxiv.org/abs/1803.05457), 2018.
- [Abductive Commonsense Reasoning](https://arxiv.org/abs/1908.05739), 2019.
- [HellaSwag](https://arxiv.org/abs/1905.07830), 2019.
- [PIQA](https://arxiv.org/abs/1911.11641), 2020.
- [QuAIL](https://ojs.aaai.org/index.php/AAAI/article/view/6398), 2020.

### Source Reference Table

| Source | Year | Type | URL |
| --- | ---: | --- | --- |
| RAR-b: Reasoning as Retrieval Benchmark | 2024 | benchmark paper | [https://arxiv.org/abs/2404.06347](https://arxiv.org/abs/2404.06347) |
| ARC, the AI2 Reasoning Challenge | 2018 | source task paper | [https://arxiv.org/abs/1803.05457](https://arxiv.org/abs/1803.05457) |
| Abductive Commonsense Reasoning | 2019 | source task paper | [https://arxiv.org/abs/1908.05739](https://arxiv.org/abs/1908.05739) |
| HellaSwag | 2019 | source task paper | [https://arxiv.org/abs/1905.07830](https://arxiv.org/abs/1905.07830) |
| PIQA | 2020 | source task paper | [https://arxiv.org/abs/1911.11641](https://arxiv.org/abs/1911.11641) |
| QuAIL | 2020 | source task paper | [https://ojs.aaai.org/index.php/AAAI/article/view/6398](https://ojs.aaai.org/index.php/AAAI/article/view/6398) |
