# NanoMTEB-Spanish

## Overview

NanoMTEB-Spanish is a compact Spanish and Spanish-English retrieval group. It
covers complex entity-answer QA, Spanish Wikipedia passage retrieval, Spanish
consumer-health passage and document retrieval, and product question answering
in Spanish-English, English-Spanish, and Spanish-Spanish directions. The group
is useful because the target is not always a Spanish paragraph with obvious word
overlap: some positives are short entity answers, health passages, or compact
product snippets.

The group contains 1,334 queries, 25,262 task-local documents, and 4,806
positive qrel rows. It is multi-positive overall, with MIRACL, Spanish Passage
Retrieval, and xPQA contributing multiple relevant documents or snippets per
query. This makes the group a good diagnostic for Spanish retrieval systems that
need to combine semantic answerability, domain evidence, and cross-lingual
product matching.

## What This Group Measures

The group measures several Spanish retrieval relations. `mintaka_es` maps
Spanish complex questions to short answer strings or entity names. `miracl_es`
retrieves Spanish Wikipedia passages for information needs. `spanish_passage_s2_p`
retrieves full Spanish health web pages, while `spanish_passage_s2_s` retrieves
shorter answer passages for the same consumer-health setting. The three xPQA
tasks retrieve product answer snippets across Spanish-English and monolingual
Spanish directions.

This mixture separates lexical Spanish passage retrieval from semantic and
cross-lingual retrieval. A model can do well on MIRACL or health pages because
query terms overlap with passages, but still fail on product QA where snippets
are short and may be in another language. Conversely, a cross-lingual dense
model can be strong on xPQA while still needing exact medical terms and entities
for health retrieval.

## Task Families

- **Complex entity-answer retrieval:** `mintaka_es` retrieves short canonical
  answers for Spanish complex questions.
- **Wikipedia retrieval:** `miracl_es` retrieves Spanish Wikipedia passages.
- **Consumer-health retrieval:** `spanish_passage_s2_p` retrieves full pages,
  and `spanish_passage_s2_s` retrieves answer passages.
- **Product QA retrieval:** `xpqa_eng_spa`, `xpqa_spa_eng`, and `xpqa_spa_spa`
  retrieve compact product answer snippets across Spanish and English.

## Dataset Shape

The group has seven task pages. `mintaka_es` is single-positive, while the
other six tasks have multiple positives per query on average. The Spanish
Passage Retrieval tasks have the densest relevance sets, with about 5.96 and
7.35 positives per query. `miracl_es` averages 4.67 positives per query, and
the xPQA tasks average about 2.3 to 2.5 positives per query.

Document length varies sharply. Mintaka positives are very short answer strings.
xPQA snippets are compact product answers. MIRACL uses mid-length Wikipedia
passages. The health `s2_p` split uses long full web pages, while `s2_s` uses
shorter answer passages. The group therefore tests how retrieval systems behave
when the target unit changes from entity string to snippet to passage to full
page.

## Retrieval Behavior

### BM25 Profile

BM25 is best only for `mintaka_es`, where the relevant answer strings often
contain names, titles, or entities that can be matched directly when present in
the query. BM25 is also reasonably strong on Spanish health retrieval and
MIRACL because Spanish queries often share medical terms, entities, or topical
words with the relevant pages and passages. `spanish_passage_s2_p` is a case
where BM25 beats dense, reaching 0.5129 nDCG@10.

BM25 struggles on cross-lingual product QA. `xpqa_eng_spa` and `xpqa_spa_eng`
score 0.0986 and 0.1227 nDCG@10, because the question and answer snippets may
be in different languages and are too short for sparse overlap to recover many
relevant items. At group level, BM25 reaches 0.3599 query-weighted nDCG@10,
which is useful but clearly below dense retrieval.

### Dense Profile

Dense retrieval with `harrier-oss-270m` is the strongest query-weighted profile
for the group at 0.5100 nDCG@10. It is best for `mintaka_es`, `miracl_es`,
`spanish_passage_s2_s`, `xpqa_eng_spa`, `xpqa_spa_eng`, and `xpqa_spa_spa`.
The cross-lingual product QA gains are especially large: `xpqa_spa_eng` rises
from 0.1227 BM25 nDCG@10 to 0.4872 dense nDCG@10, and `xpqa_eng_spa` rises from
0.0986 to 0.3104.

Dense retrieval is also strong for answer passage retrieval and MIRACL, where
it can connect Spanish questions to semantically relevant passages even when
surface wording differs. Its one clear weakness is `spanish_passage_s2_p`,
where full health pages and medical lexical anchors favor hybrid or BM25 more
than dense alone.

### Reranking Hybrid Profile

The reranking hybrid profile is best for `spanish_passage_s2_p`, reaching
0.6220 nDCG@10 and the highest recall@100 for that task. This is the expected
pattern for full-page health retrieval: sparse evidence finds medical terms and
entities, while dense evidence helps with question intent and related concepts.
Hybrid is also close to dense on `spanish_passage_s2_s`, `miracl_es`, and
`xpqa_spa_spa`.

Hybrid does not dominate the cross-lingual xPQA tasks. It trails dense sharply
on `xpqa_eng_spa` and `xpqa_spa_eng`, where sparse evidence contributes little
because the query and answer may be in different languages. The group therefore
shows a clean division: hybrid is useful for long Spanish health pages, while
dense retrieval is more important for short cross-lingual product snippets and
semantic answer matching.

## Task Summary

| Task | Family | Language | Queries | Docs | Positives | Positives/query | BM25 nDCG@10 | Dense nDCG@10 | Reranking hybrid nDCG@10 | Best profile |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| [mintaka_es](mintaka_es.md) | Entity-answer retrieval | `multilingual` | 200 | 1,693 | 200 | 1.00 | 0.2502 | 0.3614 | 0.2721 | Dense |
| [miracl_es](miracl_es.md) | Wikipedia retrieval | `es` | 200 | 10,000 | 934 | 4.67 | 0.5620 | 0.7481 | 0.7042 | Dense |
| [spanish_passage_s2_p](spanish_passage_s2_p.md) | Health page retrieval | `es` | 167 | 7,501 | 996 | 5.96 | 0.5129 | 0.4719 | 0.6220 | Reranking hybrid |
| [spanish_passage_s2_s](spanish_passage_s2_s.md) | Health passage retrieval | `es` | 167 | 250 | 1,228 | 7.35 | 0.5458 | 0.6398 | 0.6333 | Dense |
| [xpqa_eng_spa](xpqa_eng_spa.md) | Product QA retrieval | `multilingual` | 200 | 1,936 | 491 | 2.46 | 0.0986 | 0.3104 | 0.1428 | Dense |
| [xpqa_spa_eng](xpqa_spa_eng.md) | Product QA retrieval | `multilingual` | 200 | 1,941 | 469 | 2.34 | 0.1227 | 0.4872 | 0.1444 | Dense |
| [xpqa_spa_spa](xpqa_spa_spa.md) | Product QA retrieval | `es` | 200 | 1,941 | 488 | 2.44 | 0.4829 | 0.5667 | 0.5582 | Dense |

## Interpretation Notes for Model Researchers

NanoMTEB-Spanish is a useful diagnostic for whether a model's Spanish retrieval
strength comes from lexical overlap, semantic matching, or cross-lingual
alignment. Dense retrieval dominates the group because it handles short answers,
MIRACL passages, and xPQA snippets better than sparse retrieval. Hybrid is most
valuable on full-page health retrieval, where exact medical terminology and
semantic question intent both matter.

The cross-lingual xPQA tasks should be inspected separately from the Spanish
monolingual tasks. A model can improve Spanish passage retrieval without
improving Spanish-English product QA. Similarly, strong product QA does not
guarantee good retrieval over long health pages. Per-task analysis is necessary
before interpreting the aggregate score.

## Training and Leakage Notes

Useful training data includes non-overlapping Mintaka examples, Spanish
Wikidata-style entity QA, MIRACL Spanish training data, Spanish Wikipedia
question-passage pairs, Spanish consumer-health QA, medical FAQ retrieval,
document-level health web retrieval, and product QA ranking data in Spanish and
English. Multi-positive behavior should be preserved for MIRACL, Spanish
Passage Retrieval, and xPQA.

Leakage control should exclude Nano evaluation queries, qrels, answer strings,
positive passages, health pages, and product snippets. Synthetic examples
should preserve entity names, medical terms, product model numbers, quantities,
dimensions, compatibility terms, yes/no polarity, and customer-reported facts.
Hard negatives should come from the same entity type, medical topic, product
category, or answer family.

## Public Sources

- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316), 2023.
- [Mintaka: A Complex, Natural, and Multilingual Dataset for End-to-End Question Answering](https://arxiv.org/abs/2210.01613), 2022.
- [Making a MIRACL](https://arxiv.org/abs/2210.09984), 2023.
- [A Test Collection for Passage Retrieval Evaluation of Spanish Health-Related Resources](https://doi.org/10.1007/978-3-030-15719-7_19), 2019.
- [Spanish Passage Retrieval dataset page](https://mklab.iti.gr/results/spanish-passage-retrieval-dataset/).
- [xPQA: Cross-Lingual Product Question Answering across 12 Languages](https://arxiv.org/abs/2305.09249), 2023.
- [mteb/MintakaRetrieval](https://huggingface.co/datasets/mteb/MintakaRetrieval).
- [mteb/MIRACLRetrievalHardNegatives](https://huggingface.co/datasets/mteb/MIRACLRetrievalHardNegatives).
- [mteb/SpanishPassageRetrievalS2P](https://huggingface.co/datasets/mteb/SpanishPassageRetrievalS2P).
- [mteb/XPQARetrieval](https://huggingface.co/datasets/mteb/XPQARetrieval).

### Source Reference Table

| Source | Year | Type | URL |
| --- | ---: | --- | --- |
| MTEB: Massive Text Embedding Benchmark | 2023 | benchmark paper | https://arxiv.org/abs/2210.07316 |
| Mintaka: A Complex, Natural, and Multilingual Dataset for End-to-End Question Answering | 2022 | source task paper | https://arxiv.org/abs/2210.01613 |
| Making a MIRACL: Multilingual Information Retrieval Across a Continuum of Languages | 2023 | source task paper | https://arxiv.org/abs/2210.09984 |
| A Test Collection for Passage Retrieval Evaluation of Spanish Health-Related Resources | 2019 | source task paper | https://doi.org/10.1007/978-3-030-15719-7_19 |
| Spanish Passage Retrieval dataset page |  | project page | https://mklab.iti.gr/results/spanish-passage-retrieval-dataset/ |
| xPQA: Cross-Lingual Product Question Answering across 12 Languages | 2023 | source task paper | https://arxiv.org/abs/2305.09249 |
| mteb/MintakaRetrieval |  | dataset card | https://huggingface.co/datasets/mteb/MintakaRetrieval |
| mteb/MIRACLRetrievalHardNegatives |  | dataset card | https://huggingface.co/datasets/mteb/MIRACLRetrievalHardNegatives |
| mteb/SpanishPassageRetrievalS2P |  | dataset card | https://huggingface.co/datasets/mteb/SpanishPassageRetrievalS2P |
| mteb/XPQARetrieval |  | dataset card | https://huggingface.co/datasets/mteb/XPQARetrieval |
