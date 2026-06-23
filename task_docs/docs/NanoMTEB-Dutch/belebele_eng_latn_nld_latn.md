# NanoMTEB-Dutch / belebele_eng_latn_nld_latn

## Overview

`NanoMTEB-Dutch / belebele_eng_latn_nld_latn` is the English-to-Dutch Belebele
retrieval split: Dutch questions retrieve English passages. The Nano split has
200 queries, 488 documents, and 200 positive qrel rows, with exactly one
positive passage per query. Current diagnostics show dense retrieval as by far
the strongest top-rank profile, `reranking_hybrid` as strongest recall@100, and
BM25 as much weaker but not useless because named entities and numbers often
survive across Dutch and English.

## Details

### What the Original Data Measures

Belebele is a parallel reading-comprehension benchmark covering 122 language
variants over FLORES-200 passages. The retrieval adaptation uses a question as
the query and the corresponding answer-bearing passage as the positive
document. MTEB-NL includes Belebele retrieval to evaluate Dutch monolingual and
cross-lingual retrieval.

This split specifically tests cross-lingual alignment from Dutch questions to
English passages. A model must bridge language while preserving the
reading-comprehension relation between question and evidence.

### Observed Data Profile

The Nano split contains 200 queries, 488 documents, and 200 positive qrel rows.
Every query has exactly one positive document. Queries average 69.39
characters, while documents average 475.51 characters.

Queries are Dutch comprehension questions. Documents are English passages.
Observed examples ask about a shooting event, arrestee detention rules, the
Chandrayaan-1 lunar probe, the Clean Air Act, and the NBA season suspension.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset contains all 488 documents per query
and achieves nDCG@10 = 0.4738, hit@10 = 0.5850, and recall@100 = 0.6150. BM25
has a moderate score for a cross-lingual task because names, dates, acronyms,
and cognates can overlap between Dutch questions and English passages.

Still, BM25 is far below dense retrieval. Ordinary Dutch wording such as
question forms, negation, causal language, and descriptions has no direct
lexical match in the English evidence passage.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset contains all 488 documents per
query and achieves nDCG@10 = 0.8918, hit@10 = 0.9650, and recall@100 = 0.9850.
Dense retrieval is the strongest top-rank profile.

This is a clear cross-lingual embedding success case. Dense retrieval can align
Dutch question meaning with English passage evidence, including questions about
exclusions, reasons, chronology, and entity roles that are not recoverable from
surface token overlap alone.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains mostly 100 candidates per
query, with two queries using a rank-101 safeguard row. It achieves nDCG@10 =
0.6283, hit@10 = 0.7000, and recall@100 = 0.9900. Hybrid retrieval has the best
recall@100 but is much weaker than dense retrieval for top-rank quality.

The profile suggests that sparse evidence helps retain positives through named
entities and numbers, but it also introduces many lexical false positives. A
reranker must rely primarily on cross-lingual semantic evidence.

### Metric Interpretation for Model Researchers

This task is single-positive: each Dutch question has one English
answer-bearing passage. Hit@10 measures whether that passage appears near the
top. nDCG@10 is sensitive to rank, and recall@100 measures whether the passage
is available for reranking.

The main signal is cross-lingual reading-comprehension retrieval. BM25 is an
entity-anchor baseline; dense retrieval is the meaningful first-stage standard.

### Query and Relevance Type Tendencies

Queries are Dutch questions asking about facts, events, reasons, exclusions, or
decisions in an English passage. Relevant documents are short English passages
from FLORES-style sources.

The task rewards Dutch-English semantic alignment and evidence matching. It
penalizes models that only match names without checking whether the passage
answers the question.

### Representative Failure Modes

BM25 can retrieve English passages sharing a name or date but not answering the
Dutch question. Dense retrieval can confuse related passages when several
English documents contain similar entities or events. Hybrid retrieval can
under-rank the dense-positive passage when lexical anchors point to a wrong
entity-neighbor.

Rerankers should compare the Dutch question's requested relation against the
English passage, including negation and exclusion questions.

### Training Data That May Help

Useful training data includes Dutch-to-English parallel QA retrieval pairs,
translated reading-comprehension retrieval examples, multilingual
question-passage pairs with Dutch queries and English documents, and
sentence-aligned Dutch-English corpora converted to retrieval with overlap
removed. Belebele test questions and passages used by this Nano split should be
excluded from training.

Synthetic data can use non-evaluation English news or encyclopedic passages and
generate Dutch comprehension questions. Hard negatives should share entities or
topic words but not answer the question.

### Model Improvement Notes

Dense retrievers should preserve Dutch-English alignment for question intent,
not only entity names. Sparse systems need translation or expansion to be
competitive. Rerankers should perform cross-lingual evidence checking.

For hybrid systems, `NanoMTEB-Dutch / belebele_eng_latn_nld_latn` is a
dense-first task: hybrid retrieval gives excellent recall, but top-rank quality
comes from cross-lingual dense similarity.

## Example Data

| Query | Positive document |
| --- | --- |
| Welke uitspraak over het evenement waar de schietpartij plaatsvond, is juist? [77 chars] | At least 100 people had attended the party, in order to celebrate the first anniversary of a couple whose wedding was held last year. A formal anniversary event was scheduled for a later date, officia... [200 / 435 chars] |
| Wat moeten arrestanten volgens het tijdelijke contactverbod dat in de tekst wordt genoemd, krijgen o... [100 / 149 chars] | In the last 3 months, over 80 arrestees were released from the Central Booking facility without being formally charged. In April this year, a temporary restaining order was issued by Judge Glynn again... [200 / 608 chars] |
| Welke uitspraak over de maansonde van de Chandrayaan-1 is niet waar? [68 chars] | The unmanned lunar orbiter Chandrayaan-1 ejected its Moon Impact Probe (MIP), which hurtled across the surface of the Moon at 1.5 kilometres per second (3000 miles per hour), and successfully crash la... [200 / 379 chars] |
| Wie stelde voor om de 'Clean Air Act' te herschrijven? [54 chars] | "Prime Minister Stephen Harper has agreed to send the government's 'Clean Air Act' to an all-party committee for review, before its second reading, after Tuesday's 25 minute meeting with NDP leader Ja... [200 / 864 chars] |
| Welke van de volgende heeft de NBA besloten op te schorten? [59 chars] | On Wednesday, the United States' National Basketball Association (NBA) suspended its professional basketball season due to concerns regarding COVID-19. The NBA's decision followed a Utah Jazz player t... [200 / 239 chars] |

### Public Sources

- [The Belebele Benchmark: a Parallel Reading Comprehension Dataset in 122 Language Variants](https://arxiv.org/abs/2308.16884),
  2023.
- [facebookresearch/belebele](https://github.com/facebookresearch/belebele).
- [mteb/belebele](https://huggingface.co/datasets/mteb/belebele).
- [MTEB-NL and E5-NL: Embedding Benchmark and Models for Dutch](https://arxiv.org/abs/2509.12340),
  2025.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| The Belebele Benchmark: a Parallel Reading Comprehension Dataset in 122 Language Variants | 2023 | arXiv paper | [https://arxiv.org/abs/2308.16884](https://arxiv.org/abs/2308.16884) |
| facebookresearch/belebele | 2023 | repository | [https://github.com/facebookresearch/belebele](https://github.com/facebookresearch/belebele) |
| mteb/belebele |  | dataset card | [https://huggingface.co/datasets/mteb/belebele](https://huggingface.co/datasets/mteb/belebele) |
| MTEB-NL and E5-NL: Embedding Benchmark and Models for Dutch | 2025 | arXiv paper | [https://arxiv.org/abs/2509.12340](https://arxiv.org/abs/2509.12340) |

### Representative Snippets

| Query pattern | Positive document pattern |
| --- | --- |
| A Dutch question asking which statement about a shooting event is correct. | An English passage about an anniversary party and shooting. |
| A Dutch question about detention longer than 24 hours. | An English passage about arrestees and a temporary restraining order. |
| A Dutch question asking which Chandrayaan-1 statement is not true. | An English passage about the lunar impact probe. |
| A Dutch question asking who proposed reviewing the Clean Air Act. | An English passage about Stephen Harper, Jack Layton, and committee review. |
| A Dutch question asking what the NBA suspended. | An English passage about suspending the professional basketball season. |
