# NanoMTEB-Thai

## Overview

NanoMTEB-Thai is a compact Thai and Thai-English retrieval group aligned with
MTEB-style task families. It includes Belebele reading-comprehension retrieval
in cross-lingual and monolingual directions, Thai MIRACL and Mr. TyDi Wikipedia
retrieval, Thai MKQA answer-label retrieval, Thai long-document retrieval,
WebFAQ question-answer retrieval, and Thai XQuAD context retrieval. The group
tests Thai retrieval across script handling, word segmentation, answer
granularity, cross-lingual alignment, and document length.

The group contains 1,800 queries, 48,356 task-local documents, and 2,077
positive qrel rows. Most tasks are single-positive or near single-positive, but
MIRACL, MKQA, and Mr. TyDi include multiple positives for some queries. It is a
useful diagnostic because Thai retrieval quality changes sharply depending on
whether the target is a passage, a short answer label, a long document, or a
document in another language.

## What This Group Measures

The group measures several Thai retrieval relations. Belebele tests whether
reading-comprehension relevance survives Thai-English direction changes.
`miracl_th` and `mr_tidy_thai` retrieve Thai Wikipedia-style evidence passages.
`mkqa_th` retrieves short accepted answers such as names, dates, numbers, or
locations. `multi_long_doc_th` retrieves full long Thai documents from generated
questions. `web_faq_tha` retrieves FAQ answers, and `xqu_ad_th` retrieves the
Thai context paragraph that answers a translated QA question.

This mix separates language segmentation from retrieval semantics. BM25 can be
excellent when Thai query and passage wording overlaps, but it collapses on
cross-lingual Belebele directions and MKQA answer labels. Dense retrieval
handles cross-lingual and semantic matching much better, while hybrid retrieval
helps with recall and with tasks where exact Thai terms and semantic relatedness
both matter.

## Task Families

- **Belebele reading-comprehension retrieval:** three tasks cover Thai-to-English,
  English-to-Thai, and Thai-to-Thai retrieval.
- **Thai Wikipedia retrieval:** `miracl_th` and `mr_tidy_thai` retrieve
  evidence passages for Thai information needs.
- **Short answer-label retrieval:** `mkqa_th` retrieves canonical answer labels
  for Thai questions.
- **Long-document retrieval:** `multi_long_doc_th` retrieves full long Thai
  documents.
- **FAQ retrieval:** `web_faq_tha` retrieves Thai web FAQ answer snippets.
- **Translated QA context retrieval:** `xqu_ad_th` retrieves answer-bearing Thai
  XQuAD contexts.

## Dataset Shape

The group has nine task pages with 200 queries each. Candidate pools range from
240 documents for `xqu_ad_th` to 10,000 documents for MIRACL, Mr. TyDi, WebFAQ,
and the long-document task. `mkqa_th` has short answer labels with an average of
1.5 positives per query. `miracl_th` and `mr_tidy_thai` are also
multi-positive, while the Belebele, WebFAQ, XQuAD, and long-document tasks are
single-positive in the Nano splits.

Document length is uneven. `mkqa_th` documents are short labels. Belebele,
MIRACL, Mr. TyDi, WebFAQ, and XQuAD use passage-style documents. `multi_long_doc_th`
is the outlier, with very long Thai documents. This makes the group sensitive to
tokenization, truncation, and whether a model can rank long noisy pages without
losing the relevant evidence.

## Retrieval Behavior

### BM25 Profile

BM25 is best for `multi_long_doc_th` and `xqu_ad_th`, and it is nearly tied on
Thai-to-Thai Belebele. It performs very well when the query and document share
Thai lexical evidence: `xqu_ad_th` reaches 0.9835 nDCG@10, `mr_tidy_thai`
reaches 0.8502, `web_faq_tha` reaches 0.7607, and Thai-to-Thai Belebele reaches
0.9297. These scores show that sparse retrieval can be strong when segmentation
and exact terms line up.

The failures are equally clear. BM25 scores 0.0891 and 0.0944 on the two
cross-lingual Belebele directions, and only 0.0182 on `mkqa_th`. Thai-English
matching has little direct lexical overlap, and short answer labels often do not
repeat the question wording. BM25 is therefore a strong monolingual passage
baseline, but not a robust solution for the whole Thai group.

### Dense Profile

Dense retrieval with `harrier-oss-270m` is the strongest query-weighted profile
at 0.6978 nDCG@10. It is best for both cross-lingual Belebele directions,
`miracl_th`, `mkqa_th`, and `mr_tidy_thai`. The cross-lingual gain is dramatic:
Thai-to-English Belebele rises from 0.0891 BM25 nDCG@10 to 0.8483 dense
nDCG@10, and English-to-Thai rises from 0.0944 to 0.8046. This is the main
semantic alignment signal in the group.

Dense is also the best profile for `mkqa_th`, although the absolute score is
low at 0.0359. That indicates that answer-label retrieval remains difficult
even with embeddings. Dense is weaker than BM25 on `multi_long_doc_th` and
`xqu_ad_th`, where exact Thai terms and small context pools favor sparse
matching.

### Reranking Hybrid Profile

The reranking hybrid profile is best for Thai-to-Thai Belebele and
`web_faq_tha`, and it has the best query-weighted recall@100 at 0.8556. It
works well when exact Thai terms and semantic similarity are both useful:
Thai-to-Thai Belebele reaches 0.9615 nDCG@10 and WebFAQ reaches 0.7866. Hybrid
also improves recall for MIRACL, Mr. TyDi, XQuAD, and the long-document task.

Hybrid is much weaker than dense on the cross-lingual Belebele tasks. Sparse
evidence adds little when query and document are in different languages, so the
hybrid profile falls far below dense in top-10 ranking. This group therefore
supports a task-aware interpretation: hybrid is useful for Thai monolingual
candidate coverage, but dense retrieval is essential for Thai-English semantic
alignment.

## Task Summary

| Task | Family | Language | Queries | Docs | Positives | Positives/query | BM25 nDCG@10 | Dense nDCG@10 | Reranking hybrid nDCG@10 | Best profile |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| [belebele_eng_latn_tha_thai](belebele_eng_latn_tha_thai.md) | Cross-lingual reading retrieval | `multilingual` | 200 | 488 | 200 | 1.00 | 0.0891 | 0.8483 | 0.2919 | Dense |
| [belebele_tha_thai_eng_latn](belebele_tha_thai_eng_latn.md) | Cross-lingual reading retrieval | `multilingual` | 200 | 488 | 200 | 1.00 | 0.0944 | 0.8046 | 0.2741 | Dense |
| [belebele_tha_thai_tha_thai](belebele_tha_thai_tha_thai.md) | Monolingual reading retrieval | `th` | 200 | 488 | 200 | 1.00 | 0.9297 | 0.9287 | 0.9615 | Reranking hybrid |
| [miracl_th](miracl_th.md) | Wikipedia retrieval | `th` | 200 | 10,000 | 343 | 1.72 | 0.5999 | 0.8076 | 0.7250 | Dense |
| [mkqa_th](mkqa_th.md) | Answer-label retrieval | `multilingual` | 200 | 6,652 | 300 | 1.50 | 0.0182 | 0.0359 | 0.0272 | Dense |
| [mr_tidy_thai](mr_tidy_thai.md) | Wikipedia retrieval | `th` | 200 | 10,000 | 234 | 1.17 | 0.8502 | 0.9147 | 0.8914 | Dense |
| [multi_long_doc_th](multi_long_doc_th.md) | Long-document retrieval | `th` | 200 | 10,000 | 200 | 1.00 | 0.3684 | 0.2125 | 0.3672 | BM25 |
| [web_faq_tha](web_faq_tha.md) | FAQ retrieval | `th` | 200 | 10,000 | 200 | 1.00 | 0.7607 | 0.7822 | 0.7866 | Reranking hybrid |
| [xqu_ad_th](xqu_ad_th.md) | QA context retrieval | `th` | 200 | 240 | 200 | 1.00 | 0.9835 | 0.9459 | 0.9674 | BM25 |

## Interpretation Notes for Model Researchers

NanoMTEB-Thai has one of the clearest divisions between retrieval profiles.
Dense retrieval is crucial for Thai-English tasks and semantic passage
retrieval. BM25 remains very strong for monolingual Thai contexts with lexical
overlap. Hybrid helps with monolingual passage and FAQ coverage but does not
solve cross-lingual retrieval when sparse evidence is absent.

`mkqa_th` should be read separately from the passage tasks. All profiles score
low because the target is a short answer label, not an explanatory passage. A
model can improve MIRACL or Belebele substantially while still failing to rank
short Thai answer labels. Long-document retrieval is also separate: success
there depends on handling long noisy documents and exact evidence anchors.

## Training and Leakage Notes

Useful training data includes Thai Wikipedia QA, MIRACL Thai, Mr. TyDi Thai,
XQuAD-style question-context pairs, Thai-English parallel reading-comprehension
data, MKQA-like answer-label supervision, Thai long-document question-to-article
pairs, and Thai FAQ question-answer pairs. Cross-lingual directions should be
kept explicit rather than mixed into one undifferentiated retrieval objective.

Leakage control should exclude Nano evaluation queries, qrels, positive
documents, answer labels, generated long-document questions, and upstream
evaluation rows. Synthetic examples should preserve Thai script, segmentation,
named entities, dates, numbers, answer types, FAQ wording, and long-document
evidence locations. Hard negatives should be drawn from related entities,
adjacent FAQ entries, same-topic Wikipedia pages, or nearby sections of long
documents.

## Public Sources

- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316).
- [The Belebele Benchmark](https://arxiv.org/abs/2308.16884), 2023.
- [Making a MIRACL](https://arxiv.org/abs/2210.09984), 2022.
- [MKQA](https://arxiv.org/abs/2007.15207), 2020.
- [Mr. TyDi](https://arxiv.org/abs/2108.08787), 2021.
- [M3-Embedding / MLDR](https://arxiv.org/abs/2402.03216), 2024.
- [WebFAQ](https://arxiv.org/abs/2502.20936), 2025.
- [On the Cross-lingual Transferability of Monolingual Representations](https://arxiv.org/abs/1910.11856), 2019.
- [mteb/belebele](https://huggingface.co/datasets/mteb/belebele).
- [mteb/MIRACLRetrievalHardNegatives](https://huggingface.co/datasets/mteb/MIRACLRetrievalHardNegatives).
- [mteb/MKQARetrieval](https://huggingface.co/datasets/mteb/MKQARetrieval).
- [mteb/mrtidy](https://huggingface.co/datasets/mteb/mrtidy).
- [mteb/MultiLongDocRetrieval](https://huggingface.co/datasets/mteb/MultiLongDocRetrieval).

### Source Reference Table

| Source | Year | Type | URL |
| --- | ---: | --- | --- |
| MTEB: Massive Text Embedding Benchmark | 2023 | benchmark paper | [https://arxiv.org/abs/2210.07316](https://arxiv.org/abs/2210.07316) |
| The Belebele Benchmark | 2023 | source task paper | [https://arxiv.org/abs/2308.16884](https://arxiv.org/abs/2308.16884) |
| Making a MIRACL | 2022 | source task paper | [https://arxiv.org/abs/2210.09984](https://arxiv.org/abs/2210.09984) |
| MKQA | 2020 | source task paper | [https://arxiv.org/abs/2007.15207](https://arxiv.org/abs/2007.15207) |
| Mr. TyDi | 2021 | source task paper | [https://arxiv.org/abs/2108.08787](https://arxiv.org/abs/2108.08787) |
| M3-Embedding / MLDR | 2024 | source task paper | [https://arxiv.org/abs/2402.03216](https://arxiv.org/abs/2402.03216) |
| WebFAQ | 2025 | source task paper | [https://arxiv.org/abs/2502.20936](https://arxiv.org/abs/2502.20936) |
| On the Cross-lingual Transferability of Monolingual Representations | 2019 | source task paper | [https://arxiv.org/abs/1910.11856](https://arxiv.org/abs/1910.11856) |
| mteb/belebele |  | dataset card | [https://huggingface.co/datasets/mteb/belebele](https://huggingface.co/datasets/mteb/belebele) |
| mteb/MIRACLRetrievalHardNegatives |  | dataset card | [https://huggingface.co/datasets/mteb/MIRACLRetrievalHardNegatives](https://huggingface.co/datasets/mteb/MIRACLRetrievalHardNegatives) |
| mteb/MKQARetrieval |  | dataset card | [https://huggingface.co/datasets/mteb/MKQARetrieval](https://huggingface.co/datasets/mteb/MKQARetrieval) |
| mteb/mrtidy |  | dataset card | [https://huggingface.co/datasets/mteb/mrtidy](https://huggingface.co/datasets/mteb/mrtidy) |
| mteb/MultiLongDocRetrieval |  | dataset card | [https://huggingface.co/datasets/mteb/MultiLongDocRetrieval](https://huggingface.co/datasets/mteb/MultiLongDocRetrieval) |
