# NanoDAPFAM

## Overview

NanoDAPFAM is the compact Nano set for DAPFAM, a domain-aware patent-family
retrieval benchmark. It evaluates citation-linked prior-art retrieval at the
patent-family level. The group contains eighteen variants formed by three
domain conditions (`All`, `In`, and `Out`), two query representations
(title-abstract or title-abstract-claims), and three target representations
(title-abstract, title-abstract-claims, or full text).

The group is useful because it separates ordinary lexical patent similarity
from cross-domain prior-art retrieval. Same-domain and all-domain variants give
retrievers many technical anchors: components, materials, methods, and claim
phrases. OUT-domain variants remove shared IPC3 technical classes, so the
model must retrieve cited families related by transferable mechanisms or
problem-solution patterns rather than by the same surface vocabulary. BM25,
dense retrieval, and `reranking_hybrid` all reveal different parts of that
domain gap.

## What This Group Measures

[DAPFAM: A Domain-Aware Family-level Dataset to benchmark cross domain patent retrieval](https://arxiv.org/abs/2506.22141)
introduces a patent-family retrieval benchmark with citation-based relevance
judgments and explicit domain partitions. The source benchmark aggregates
patents at family level to reduce international duplicate publications and
uses IPC3 overlap to distinguish same-domain from cross-domain retrieval.

NanoDAPFAM preserves the DAPFAM design in compact 200-query splits. Each split
uses the same high-level prior-art retrieval task but changes the domain
condition and patent text fields. This makes the group a controlled probe of
three factors: whether positives are same-domain or cross-domain, whether the
query includes claims, and whether the target is a compact summary or a very
long patent text.

## Task Families

- **All-domain prior-art retrieval:** `All` variants include both same-IPC3 and
  cross-IPC3 positives, measuring overall citation-linked patent-family
  retrieval.
- **In-domain prior-art retrieval:** `In` variants keep same-domain positives,
  where shared technical vocabulary is often available.
- **Out-domain prior-art retrieval:** `Out` variants keep cross-domain
  positives, where relevance depends more on transferred mechanisms, materials,
  or problem-solution analogies.
- **Representation comparisons:** each domain condition is evaluated with
  title-abstract and title-abstract-claims queries against title-abstract,
  title-abstract-claims, and full-text targets.

## Dataset Shape

NanoDAPFAM contains 18 task pages, 3,600 queries, 180,000 split-local documents,
and 49,879 positive qrel rows. Each split has 200 queries and 10,000 candidate
documents. All variants are multi-positive, but density changes by domain:
All-domain variants average about 20 positives per query, In-domain variants
about 15, and Out-domain variants about 6.

Text length is a core variable. Title-abstract queries average under 800
characters, while title-abstract-claims queries range from about 8,300 to 9,300
characters. Target documents range from short title-abstract records around 778
characters to full-text patent-family documents around 69,000 to 72,000
characters. The group should therefore be read as a matrix of domain difficulty
and representation length, not as eighteen independent tasks.

## Retrieval Behavior

### BM25 Profile

BM25 is much stronger on `All` and `In` variants than on `Out` variants. In the
same-domain setting, shared IPC3 areas provide repeated technical terms,
components, material names, and claim language. In OUT-domain retrieval, those
anchors are weaker or absent, so BM25 must rely on partial mechanism overlap.

Representation also changes sparse behavior. Claim-bearing targets often expose
more components and operations than title-abstract targets. Full text gives
even more vocabulary but adds large amounts of boilerplate and unrelated legal
or descriptive context. A higher BM25 score on long targets does not always
mean better semantic retrieval; it may mean more lexical chances.

### Dense Profile

Dense retrieval is the best profile for nearly every NanoDAPFAM variant in the
current metadata. It improves most clearly in OUT-domain tasks, where the
positive may share an abstract mechanism with the query even when patent-field
vocabulary differs. Dense retrieval also benefits title-abstract targets, where
there is less text for exact matching.

Dense performance should still be interpreted carefully. Patent retrieval
depends on exact technical distinctions, claim scope, and family-level
invention identity. A semantically related patent can be wrong if it solves a
different problem or lacks the cited technical relation.

### Reranking Hybrid Profile

`reranking_hybrid` often falls between BM25 and dense in nDCG@10, but it is
useful for candidate generation. Patent retrieval needs both exact technical
anchors and broader mechanism matching. In several title-abstract and full-text
variants, the hybrid pool can preserve candidates found by either signal.

For reranker experiments, OUT-domain variants are the most important stress
test. If the first-stage candidate pool misses cross-domain positives, reranking
cannot recover the analogy or mechanism relation.

## Task Summary

| Task | Domain | Query fields | Target fields | Positives/query | BM25 nDCG@10 | Dense nDCG@10 | Reranking hybrid nDCG@10 | Best profile |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| [NanoDAPFAMAllTitlAbsClmToFullText](NanoDAPFAMAllTitlAbsClmToFullText.md) | All | title+abstract+claims | full text | 19.95 | 0.3365 | 0.4352 | 0.4215 | Dense |
| [NanoDAPFAMAllTitlAbsClmToTitlAbs](NanoDAPFAMAllTitlAbsClmToTitlAbs.md) | All | title+abstract+claims | title+abstract | 19.91 | 0.2864 | 0.3997 | 0.3767 | Dense |
| [NanoDAPFAMAllTitlAbsClmToTitlAbsClm](NanoDAPFAMAllTitlAbsClmToTitlAbsClm.md) | All | title+abstract+claims | title+abstract+claims | 19.95 | 0.3360 | 0.4156 | 0.3989 | Dense |
| [NanoDAPFAMAllTitlAbsToFullText](NanoDAPFAMAllTitlAbsToFullText.md) | All | title+abstract | full text | 19.95 | 0.3489 | 0.4149 | 0.4175 | Reranking hybrid |
| [NanoDAPFAMAllTitlAbsToTitlAbs](NanoDAPFAMAllTitlAbsToTitlAbs.md) | All | title+abstract | title+abstract | 19.91 | 0.3281 | 0.3786 | 0.3790 | Reranking hybrid |
| [NanoDAPFAMAllTitlAbsToTitlAbsClm](NanoDAPFAMAllTitlAbsToTitlAbsClm.md) | All | title+abstract | title+abstract+claims | 19.95 | 0.3510 | 0.4056 | 0.4088 | Reranking hybrid |
| [NanoDAPFAMInTitlAbsClmToFullText](NanoDAPFAMInTitlAbsClmToFullText.md) | In | title+abstract+claims | full text | 15.35 | 0.3505 | 0.4484 | 0.4375 | Dense |
| [NanoDAPFAMInTitlAbsClmToTitlAbs](NanoDAPFAMInTitlAbsClmToTitlAbs.md) | In | title+abstract+claims | title+abstract | 15.31 | 0.2970 | 0.4135 | 0.3805 | Dense |
| [NanoDAPFAMInTitlAbsClmToTitlAbsClm](NanoDAPFAMInTitlAbsClmToTitlAbsClm.md) | In | title+abstract+claims | title+abstract+claims | 15.35 | 0.3473 | 0.4325 | 0.4157 | Dense |
| [NanoDAPFAMInTitlAbsToFullText](NanoDAPFAMInTitlAbsToFullText.md) | In | title+abstract | full text | 15.36 | 0.3490 | 0.4255 | 0.4228 | Dense |
| [NanoDAPFAMInTitlAbsToTitlAbs](NanoDAPFAMInTitlAbsToTitlAbs.md) | In | title+abstract | title+abstract | 15.33 | 0.3386 | 0.3923 | 0.3942 | Reranking hybrid |
| [NanoDAPFAMInTitlAbsToTitlAbsClm](NanoDAPFAMInTitlAbsToTitlAbsClm.md) | In | title+abstract | title+abstract+claims | 15.36 | 0.3593 | 0.4125 | 0.4220 | Reranking hybrid |
| [NanoDAPFAMOutTitlAbsClmToFullText](NanoDAPFAMOutTitlAbsClmToFullText.md) | Out | title+abstract+claims | full text | 6.29 | 0.0461 | 0.1010 | 0.0869 | Dense |
| [NanoDAPFAMOutTitlAbsClmToTitlAbs](NanoDAPFAMOutTitlAbsClmToTitlAbs.md) | Out | title+abstract+claims | title+abstract | 6.29 | 0.0439 | 0.0872 | 0.0714 | Dense |
| [NanoDAPFAMOutTitlAbsClmToTitlAbsClm](NanoDAPFAMOutTitlAbsClmToTitlAbsClm.md) | Out | title+abstract+claims | title+abstract+claims | 6.29 | 0.0640 | 0.0952 | 0.0811 | Dense |
| [NanoDAPFAMOutTitlAbsToFullText](NanoDAPFAMOutTitlAbsToFullText.md) | Out | title+abstract | full text | 6.29 | 0.0638 | 0.0952 | 0.0858 | Dense |
| [NanoDAPFAMOutTitlAbsToTitlAbs](NanoDAPFAMOutTitlAbsToTitlAbs.md) | Out | title+abstract | title+abstract | 6.29 | 0.0583 | 0.0872 | 0.0762 | Dense |
| [NanoDAPFAMOutTitlAbsToTitlAbsClm](NanoDAPFAMOutTitlAbsToTitlAbsClm.md) | Out | title+abstract | title+abstract+claims | 6.29 | 0.0699 | 0.0909 | 0.0901 | Dense |

## Interpretation Notes for Model Researchers

NanoDAPFAM is best interpreted by domain condition first. All and In variants
measure patent-family retrieval when the target is usually in or near the same
technical area. Out variants measure harder cross-domain prior-art retrieval,
where models need analogy and mechanism transfer. A strong model should reduce
the Out-domain gap without merely memorizing patent families.

Representation effects should be interpreted second. Claims add legal and
component detail; full text adds enormous context. Better performance on full
text may reflect useful mechanism evidence, but it may also reflect more
opportunities for lexical overlap. Comparing title-abstract targets with
claim-bearing and full-text targets helps separate concise semantic matching
from long-document term coverage.

## Training and Leakage Notes

Useful training data includes patent-family citation retrieval, prior-art
search pairs, patent semantic similarity, cross-IPC citation prediction,
patent analogy retrieval, and field-aware training over titles, abstracts,
claims, and full descriptions. Hard negatives should include same-IPC patents
that share terminology but are not cited, plus cross-domain patents that share
surface terms without the relevant mechanism.

Exclude NanoDAPFAM evaluation family IDs, qrels, positive target families,
same-family duplicate publications, and near-duplicate patent publications from
other jurisdictions. Family-level aggregation is important: using another
member of the same patent family can leak the invention.

## Public Sources

- [DAPFAM: A Domain-Aware Family-level Dataset to benchmark cross domain patent retrieval](https://arxiv.org/abs/2506.22141), 2025.

### Source Reference Table

| Source | Year | Type | URL |
| --- | ---: | --- | --- |
| DAPFAM: A Domain-Aware Family-level Dataset to benchmark cross domain patent retrieval | 2025 | paper | https://arxiv.org/abs/2506.22141 |
