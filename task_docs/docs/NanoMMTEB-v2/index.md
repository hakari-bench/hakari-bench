# NanoMMTEB-v2

## Overview

NanoMMTEB-v2 is a compact retrieval group drawn from multilingual MTEB/MMTEB
retrieval tasks. It is intentionally heterogeneous: legal statute retrieval,
counterargument retrieval, multilingual reading comprehension, Chinese COVID
policy search, FAQ-style retrieval, legal bill retrieval, long-context passkey
retrieval, MIRACL, MLQA, scientific related-paper retrieval, spatial and
temporal reasoning, StackOverflow QA, StatCan dialogue-to-table retrieval,
TREC-COVID, Danish Twitter advice retrieval, multilingual Wikipedia QA, and
WinoGrande-style referent retrieval all appear in one group.

The group is useful as a mixed-domain multilingual stress test. It does not
isolate one source benchmark, one language, or one relevance relation. BM25
identifies tasks where answer text, legal terms, or web vocabulary repeat;
dense retrieval identifies semantic, multilingual, and reasoning-style gains;
`reranking_hybrid` highlights tasks where exact anchors and semantic candidates
recover different positives.

## What This Group Measures

[MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595)
expands the MTEB framework to a wide multilingual task inventory.
[MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316)
provides the retrieval interface used by many source tasks. NanoMMTEB-v2 is a
Nano-style retrieval subset that samples a diverse set of those tasks.

The group measures robustness under task heterogeneity. Some tasks are normal
passage retrieval; others convert legal, reasoning, dialogue, FAQ, or
long-context problems into retrieval. The common format is query, corpus,
qrels, and candidate rankings, but the relevance relation changes sharply by
task.

## Task Families

- **Legal and government retrieval:** `ailastatutes`,
  `legal_bench_corporate_lobbying`, and `statcan_dialogue_dataset`.
- **Multilingual QA and evidence retrieval:** `belebele`, `miracl`, `mlqa`,
  `wikipedia_multilingual`, `hagrid`, and `covid`.
- **Scientific and biomedical retrieval:** `scidocs` and `treccovid`.
- **Argument, social, and code support retrieval:** `argu_ana`,
  `twitter_hjerne`, and `stack_overflow_qa`.
- **Reasoning retrieval:** `spart_qa`, `temp_reason_l1`, and `wino_grande`.
- **Long-context key lookup:** `lembpasskey`.

## Dataset Shape

NanoMMTEB-v2 contains 18 task pages, 3,248 queries, 116,569 split-local
documents, and 9,408 positive qrel rows. The group mixes single-positive tasks
with strongly multi-positive ones. TREC-COVID has many positives per query,
while MIRACL, SCIDOCS, StatCan, Twitter Hjerne, and AILAStatutes also require
multi-positive interpretation.

Text shape varies from one-word or short answer candidates to long legal
queries and long passkey documents. `statcan_dialogue_dataset` uses dialogue
logs and table metadata; `lembpasskey` uses long synthetic documents; legal
statute retrieval uses long fact scenarios; reasoning tasks can have very short
answer documents. This diversity is the point of the group.

## Retrieval Behavior

### BM25 Profile

BM25 is strongest on tasks with direct answer or term repetition:
`lembpasskey`, `hagrid`, `wikipedia_multilingual`, corporate lobbying,
StackOverflow QA, Chinese COVID retrieval, and MIRACL. These tasks often expose
names, answer terms, exact legal or policy words, or distinctive support text.

BM25 is weak on tasks where the answer must be inferred or represented through a
different format: `statcan_dialogue_dataset`, `temp_reason_l1`, `mlqa`,
`belebele`, and `scidocs`. In these cases, exact term overlap is not enough or
the target text is too short to carry many lexical anchors.

### Dense Profile

Dense retrieval is strongest on many low-BM25 tasks. It improves Belebele,
MLQA, StatCan, Twitter Hjerne, SCIDOCS, MIRACL, StackOverflow QA, and several
legal or scientific tasks by matching semantic intent or multilingual evidence
where exact overlap is weak. This group is therefore useful for identifying
whether dense models handle heterogeneous retrieval relations, not just one
passage-search format.

Dense retrieval can still lose exact anchors. Passkey, legal bill retrieval,
COVID policy retrieval, and short-answer reasoning tasks can depend on exact
tokens, dates, names, or answer strings.

### Reranking Hybrid Profile

`reranking_hybrid` is best for tasks such as `spart_qa`, `treccovid`, and
`wino_grande`, and remains competitive on many others. These are cases where
sparse and dense candidate sets provide complementary evidence. In WinoGrande
and spatial reasoning, a short answer may require both context matching and
exact candidate discrimination.

For reranker experiments, this group is valuable because candidate-generation
failure modes differ by task. The same reranker pool will face long documents,
short answer strings, multilingual passages, code answers, legal text, and
scientific abstracts.

## Task Summary

| Task | Language | Retrieval focus | Queries | Docs | BM25 nDCG@10 | Dense nDCG@10 | Reranking hybrid nDCG@10 | Best profile |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [ailastatutes](ailastatutes.md) | `en` | legal scenario to statute | 50 | 82 | 0.2070 | 0.2725 | 0.2557 | Dense |
| [argu_ana](argu_ana.md) | `en` | argument to counterargument | 199 | 8,626 | 0.3464 | 0.3998 | 0.3716 | Dense |
| [belebele](belebele.md) | `multilingual` | reading comprehension to answer | 376 | 10,000 | 0.0903 | 0.2781 | 0.1782 | Dense |
| [covid](covid.md) | `zh` | COVID query to policy/news passage | 200 | 10,000 | 0.7888 | 0.7592 | 0.7873 | BM25 |
| [hagrid](hagrid.md) | `en` | FAQ-style query to answer | 200 | 493 | 0.9814 | 0.9570 | 0.9639 | BM25 |
| [legal_bench_corporate_lobbying](legal_bench_corporate_lobbying.md) | `en` | policy description to bill summary | 200 | 319 | 0.8955 | 0.9110 | 0.9080 | Dense |
| [lembpasskey](lembpasskey.md) | `en` | passkey query to long context | 100 | 100 | 0.9963 | 0.8463 | 0.8525 | BM25 |
| [miracl](miracl.md) | `multilingual` | question to Wikipedia passage | 200 | 10,000 | 0.5760 | 0.7775 | 0.6942 | Dense |
| [mlqa](mlqa.md) | `multilingual` | multilingual QA to evidence | 196 | 10,000 | 0.0390 | 0.0959 | 0.0534 | Dense |
| [scidocs](scidocs.md) | `en` | paper title to related document | 200 | 10,000 | 0.2067 | 0.2773 | 0.2590 | Dense |
| [spart_qa](spart_qa.md) | `en` | spatial reasoning query to answer | 200 | 1,592 | 0.1848 | 0.2591 | 0.3382 | Reranking hybrid |
| [stack_overflow_qa](stack_overflow_qa.md) | `en` | developer question to answer | 200 | 10,000 | 0.7970 | 0.8886 | 0.8457 | Dense |
| [statcan_dialogue_dataset](statcan_dialogue_dataset.md) | `multilingual` | dialogue to statistical table | 200 | 10,000 | 0.0112 | 0.2731 | 0.1564 | Dense |
| [temp_reason_l1](temp_reason_l1.md) | `multilingual` | temporal reasoning to date answer | 200 | 10,000 | 0.0161 | 0.0488 | 0.0134 | Dense |
| [treccovid](treccovid.md) | `en` | COVID topic to biomedical abstracts | 50 | 10,000 | 0.3627 | 0.4266 | 0.4505 | Reranking hybrid |
| [twitter_hjerne](twitter_hjerne.md) | `da` | Danish tweet to advice response | 77 | 262 | 0.2395 | 0.6243 | 0.4402 | Dense |
| [wikipedia_multilingual](wikipedia_multilingual.md) | `multilingual` | question to Wikipedia answer passage | 200 | 10,000 | 0.9425 | 0.9624 | 0.9452 | Dense |
| [wino_grande](wino_grande.md) | `en` | pronoun reasoning context to referent | 200 | 5,095 | 0.5084 | 0.4940 | 0.6139 | Reranking hybrid |

## Interpretation Notes for Model Researchers

NanoMMTEB-v2 should be read as a stress test for breadth. It does not tell a
single story about one language or one retrieval relation. Instead, it exposes
whether a model is robust across legal, QA, reasoning, scientific, code, social,
and long-context formats.

The most useful analysis is task-family based. BM25-heavy tasks test exact
anchors and short answer matching. Dense-heavy tasks test semantic and
multilingual transfer. Hybrid-led tasks test complementarity and candidate
coverage. Because several tasks are multi-positive, Recall@100 should be read
alongside nDCG@10.

## Training and Leakage Notes

Useful training data must be task-matched: statute retrieval for legal tasks,
multilingual QA evidence for Belebele/MIRACL/MLQA, scientific and biomedical
retrieval for SCIDOCS/TREC-COVID, code QA for StackOverflow, and reasoning data
for spatial, temporal, and WinoGrande-style tasks. Pooling everything into one
generic similarity objective can erase the distinctions this group tests.

Exclude NanoMMTEB-v2 evaluation queries, positives, qrels, answer candidates,
long contexts, and source rows. Because the group mixes public benchmark tasks,
upstream evaluation splits should be audited carefully before use in training.

## Public Sources

- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595), 2025.
- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316), 2022.

### Source Reference Table

| Source | Year | Type | URL |
| --- | ---: | --- | --- |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | paper | https://arxiv.org/abs/2502.13595 |
| MTEB: Massive Text Embedding Benchmark | 2022 | paper | https://arxiv.org/abs/2210.07316 |
