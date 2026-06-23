# NanoMTEB-Polish

## Overview

NanoMTEB-Polish is a Polish retrieval group dominated by translated
community-question duplicate retrieval. Ten of its fourteen tasks are Polish
CQADupStack domains, covering Android, English usage, GIS, Mathematica,
Physics, Programmers, Statistics, TeX, Webmasters, and WordPress. The remaining
tasks cover Polish financial QA retrieval, Natural Questions-style fact
retrieval, PUGG Polish Wikipedia QA retrieval, and Quora duplicate-question
retrieval.

The group contains 2,800 queries, 140,000 task-local documents, and 8,151
positive qrel rows. Every task has 200 queries and a 10,000-document candidate
pool, so per-task differences are easy to compare. The group is useful because
it asks whether a model can retrieve Polish paraphrases and duplicates across
technical domains while also handling finance, Wikipedia QA, and short
duplicate-question retrieval.

## What This Group Measures

Most tasks measure duplicate intent rather than simple topical relatedness. In
the CQADupStack and Quora tasks, the model must retrieve another question that
asks the same thing, often with different wording, examples, software versions,
or technical details. This is harder than matching the same domain: two LaTeX,
WordPress, or Mathematica posts can share many tokens while solving different
problems.

The non-duplicate tasks broaden the group. `fiqa` retrieves finance answers,
`nq` retrieves answer-bearing passages for Polish fact questions, and `pugg`
retrieves Polish Wikipedia-style passages. These tasks make the group a
diagnostic for Polish semantic retrieval, not only translated Stack Exchange
duplicate detection.

## Task Families

- **Technical duplicate retrieval:** the ten `cqadupstack_*` tasks retrieve
  duplicate Polish community questions across technical and expert domains.
- **Financial QA retrieval:** `fiqa` retrieves finance answer passages.
- **Open-domain fact retrieval:** `nq` retrieves Polish Natural
  Questions-style answer passages.
- **Native Polish QA retrieval:** `pugg` retrieves Polish Wikipedia passages
  for factoid questions.
- **Short duplicate-question retrieval:** `quora` retrieves paraphrastic Polish
  duplicate questions.

## Dataset Shape

All fourteen tasks are Polish (`pl`) and use equal-sized Nano splits: 200
queries and 10,000 candidate documents per task. Positive density varies much
more than corpus size. `pugg` has exactly one positive per query, while
`cqadupstack_english` averages 6.78 positives per query and several CQADupStack
domains contain large duplicate clusters. Across the group, the average is 2.91
positives per query.

The text style is heterogeneous. CQADupStack documents often contain translated
technical posts, product names, code-like tokens, formulas, and Stack Exchange
formatting. Quora documents are short questions. FiQA answers are explanatory
finance passages. PUGG and NQ are closer to factoid QA retrieval. This makes the
group sensitive to both Polish language modeling and preservation of technical
surface forms.

## Retrieval Behavior

### BM25 Profile

BM25 is the best nDCG@10 profile for none of the fourteen tasks in the current
Nano data, but it remains an important baseline. It is strongest on `quora`
(0.7704 nDCG@10) and `pugg` (0.6390), where short questions or factoid prompts
often contain distinctive entities and overlapping terms. BM25 is also
competitive in some CQADupStack domains when duplicates share product names,
commands, packages, or terminology.

Its weakness is duplicate-intent matching. Many CQADupStack positives express
the same underlying problem with different Polish wording or different examples.
The hardest BM25 tasks are `cqadupstack_mathematica`, `fiqa`,
`cqadupstack_gis`, and `cqadupstack_webmasters`, all below 0.25 nDCG@10. These
results show that exact word frequency alone is not enough for Polish technical
duplicate retrieval.

### Dense Profile

Dense retrieval with `harrier-oss-270m` is the best profile for eight tasks:
`cqadupstack_android`, `cqadupstack_english`, `cqadupstack_physics`,
`cqadupstack_stats`, `fiqa`, `nq`, `pugg`, and `quora`. The largest gains appear
on tasks where relevance depends on paraphrase or answerability. `nq` rises
from 0.3026 BM25 nDCG@10 to 0.6154 dense nDCG@10, and `fiqa` rises from 0.2353
to 0.3890. Quora also benefits from dense paraphrase matching, reaching 0.9073.

Dense is not uniformly best across the technical duplicate tasks. Some domains
with specialized terminology, code-like names, or narrow technical phrasing are
better handled by the reranking hybrid profile. Still, the query-weighted dense
nDCG@10 of 0.4271 is the highest group-level nDCG@10 profile, which makes
NanoMTEB-Polish a strong test of Polish embedding similarity.

### Reranking Hybrid Profile

The reranking hybrid profile is best for six tasks:
`cqadupstack_gis`, `cqadupstack_mathematica`, `cqadupstack_programmers`,
`cqadupstack_tex`, `cqadupstack_webmasters`, and `cqadupstack_wordpress`. These
are mostly technical CQADupStack domains where exact technical strings and
semantic duplicate intent both matter. Hybrid retrieval can recover candidates
that dense misses because they share command names, package names, programming
terms, or product-specific vocabulary.

At group level, hybrid has lower nDCG@10 than dense (0.4088 versus 0.4271), but
it has the best recall@100 at 0.6087. This suggests that hybrid search is useful
for candidate generation in Polish technical duplicate retrieval, even when a
dense model gives a better final top-10 ordering for the broader group.

## Task Summary

| Task | Family | Language | Queries | Docs | Positives | Positives/query | BM25 nDCG@10 | Dense nDCG@10 | Reranking hybrid nDCG@10 | Best profile |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| [cqadupstack_android](cqadupstack_android.md) | Technical duplicate retrieval | `pl` | 200 | 10,000 | 809 | 4.04 | 0.3379 | 0.4139 | 0.4121 | Dense |
| [cqadupstack_english](cqadupstack_english.md) | Technical duplicate retrieval | `pl` | 200 | 10,000 | 1,356 | 6.78 | 0.3188 | 0.3926 | 0.3725 | Dense |
| [cqadupstack_gis](cqadupstack_gis.md) | Technical duplicate retrieval | `pl` | 200 | 10,000 | 313 | 1.56 | 0.2423 | 0.2861 | 0.3143 | Reranking hybrid |
| [cqadupstack_mathematica](cqadupstack_mathematica.md) | Technical duplicate retrieval | `pl` | 200 | 10,000 | 506 | 2.53 | 0.2129 | 0.2171 | 0.2411 | Reranking hybrid |
| [cqadupstack_physics](cqadupstack_physics.md) | Technical duplicate retrieval | `pl` | 200 | 10,000 | 621 | 3.10 | 0.3359 | 0.4306 | 0.4024 | Dense |
| [cqadupstack_programmers](cqadupstack_programmers.md) | Technical duplicate retrieval | `pl` | 200 | 10,000 | 634 | 3.17 | 0.3191 | 0.3275 | 0.3607 | Reranking hybrid |
| [cqadupstack_stats](cqadupstack_stats.md) | Technical duplicate retrieval | `pl` | 200 | 10,000 | 373 | 1.86 | 0.2662 | 0.3375 | 0.3314 | Dense |
| [cqadupstack_tex](cqadupstack_tex.md) | Technical duplicate retrieval | `pl` | 200 | 10,000 | 843 | 4.21 | 0.2555 | 0.2805 | 0.3147 | Reranking hybrid |
| [cqadupstack_webmasters](cqadupstack_webmasters.md) | Technical duplicate retrieval | `pl` | 200 | 10,000 | 882 | 4.41 | 0.2440 | 0.3045 | 0.3162 | Reranking hybrid |
| [cqadupstack_wordpress](cqadupstack_wordpress.md) | Technical duplicate retrieval | `pl` | 200 | 10,000 | 344 | 1.72 | 0.3139 | 0.2951 | 0.3289 | Reranking hybrid |
| [fiqa](fiqa.md) | Financial QA retrieval | `pl` | 200 | 10,000 | 534 | 2.67 | 0.2353 | 0.3890 | 0.3574 | Dense |
| [nq](nq.md) | Open-domain fact retrieval | `pl` | 200 | 10,000 | 251 | 1.25 | 0.3026 | 0.6154 | 0.4363 | Dense |
| [pugg](pugg.md) | Native Polish QA retrieval | `pl` | 200 | 10,000 | 200 | 1.00 | 0.6390 | 0.7817 | 0.7146 | Dense |
| [quora](quora.md) | Short duplicate-question retrieval | `pl` | 200 | 10,000 | 485 | 2.42 | 0.7704 | 0.9073 | 0.8207 | Dense |

## Interpretation Notes for Model Researchers

NanoMTEB-Polish is best interpreted by separating technical duplicate retrieval
from QA retrieval. Dense retrieval leads the group overall and is especially
important for Quora, NQ, PUGG, and FiQA. Hybrid retrieval is more valuable in
technical CQADupStack domains where exact software or mathematical terms should
not be lost. BM25 is a useful sanity baseline, but it does not win any task in
this slice.

The group is also sensitive to Polish translation quality and domain terms.
Strong scores may reflect the ability to preserve technical tokens and code-like
strings, not only general Polish semantic understanding. For model comparison,
inspect the CQADupStack block separately from NQ/PUGG/FiQA/Quora before making
claims about Polish retrieval quality.

## Training and Leakage Notes

Useful training data includes non-overlapping Polish duplicate-question pairs,
translated Stack Exchange duplicates, native Polish paraphrase data, Polish
technical QA, Polish Wikipedia QA retrieval, FiQA-style finance QA, and PUGG
training records. For CQADupStack, hard negatives should come from the same
technical site and share product names, function names, formulas, packages, or
domain terminology while asking a different question.

Leakage control is important because duplicate-question datasets are highly
clustered. Training should exclude Nano evaluation queries, qrels, positive
documents, and overlapping upstream test records from CQADupStack-PL, Quora-PL,
FiQA-PL, NQ-PL, and PUGG. Synthetic examples should preserve Polish wording,
technical tokens, code snippets, mathematical notation, financial terms, and
named entities.

## Public Sources

- [CQADupStack: A Benchmark Data Set for Community Question-Answering Research](https://ir.webis.de/anthology/2015.adcs_conference-2015.3/), 2015.
- [BEIR-PL: Zero Shot Information Retrieval Benchmark for the Polish Language](https://aclanthology.org/2024.lrec-main.194/), 2024.
- [Developing PUGG for Polish: A Modern Approach to KBQA, MRC, and IR Dataset Construction](https://aclanthology.org/2024.findings-acl.652/), 2024.
- [FiQA challenge site](https://sites.google.com/view/fiqa/).
- [Natural Questions](https://ai.google.com/research/NaturalQuestions/).
- [First Quora Dataset Release: Question Pairs](https://quoradata.quora.com/First-Quora-Dataset-Release-Question-Pairs).
- [Massive Text Embedding Benchmark (MTEB)](https://github.com/embeddings-benchmark/mteb).
- [mteb/FiQA-PL](https://huggingface.co/datasets/mteb/FiQA-PL).
- [mteb/NQ-PLHardNegatives](https://huggingface.co/datasets/mteb/NQ-PLHardNegatives).

### Source Reference Table

| Source | Year | Type | URL |
| --- | ---: | --- | --- |
| CQADupStack: A Benchmark Data Set for Community Question-Answering Research | 2015 | paper | [https://ir.webis.de/anthology/2015.adcs_conference-2015.3/](https://ir.webis.de/anthology/2015.adcs_conference-2015.3/) |
| BEIR-PL: Zero Shot Information Retrieval Benchmark for the Polish Language | 2024 | paper | [https://aclanthology.org/2024.lrec-main.194/](https://aclanthology.org/2024.lrec-main.194/) |
| Developing PUGG for Polish: A Modern Approach to KBQA, MRC, and IR Dataset Construction | 2024 | paper | [https://aclanthology.org/2024.findings-acl.652/](https://aclanthology.org/2024.findings-acl.652/) |
| FiQA challenge site |  | project page | [https://sites.google.com/view/fiqa/](https://sites.google.com/view/fiqa/) |
| Natural Questions |  | project page | [https://ai.google.com/research/NaturalQuestions/](https://ai.google.com/research/NaturalQuestions/) |
| First Quora Dataset Release: Question Pairs |  | dataset page | [https://quoradata.quora.com/First-Quora-Dataset-Release-Question-Pairs](https://quoradata.quora.com/First-Quora-Dataset-Release-Question-Pairs) |
| Massive Text Embedding Benchmark (MTEB) |  | benchmark repository | [https://github.com/embeddings-benchmark/mteb](https://github.com/embeddings-benchmark/mteb) |
| mteb/FiQA-PL |  | dataset card | [https://huggingface.co/datasets/mteb/FiQA-PL](https://huggingface.co/datasets/mteb/FiQA-PL) |
| mteb/NQ-PLHardNegatives |  | dataset card | [https://huggingface.co/datasets/mteb/NQ-PLHardNegatives](https://huggingface.co/datasets/mteb/NQ-PLHardNegatives) |
