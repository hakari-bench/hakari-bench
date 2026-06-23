# NanoMMTEB-v2 / miracl

## Overview

`NanoMMTEB-v2 / miracl` is a multilingual Wikipedia retrieval task from the
MIRACL hard-negative setting. Queries are short information needs in many
languages, and documents are same-language Wikipedia passages. The Nano split
has 200 queries, 10,000 documents, and 444 positive qrel rows. It is
multi-positive, averaging 2.22 positives per query. Current diagnostics show
dense retrieval as the strongest top-rank profile, `reranking_hybrid` as the
strongest recall@100 profile, and BM25 as useful but clearly weaker in this
multilingual hard-negative setting.

## Details

### What the Original Data Measures

MIRACL was introduced as a multilingual information retrieval benchmark across a
continuum of languages. It uses monolingual retrieval over Wikipedia, with
queries and relevance judgments produced or validated by native speakers. The
MTEB hard-negative version pools challenging candidates from BM25 and
multilingual dense retrievers.

This task measures multilingual same-language passage retrieval. A model must
find answer-bearing Wikipedia passages while handling many scripts, language
families, morphologies, and hard negatives from the same topic space.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 444 positive qrel
rows. The task is multi-positive: average positives per query is 2.22, with a
minimum of 1, median of 2, and maximum of 8. The metadata records 56.5% of
queries as multi-positive. Queries average 37.22 characters, while documents
average 448.21 characters.

Observed examples include Telugu, German, Arabic, Chinese, Finnish, Persian,
English, Bengali, and other languages. Documents are short Wikipedia-style
passages.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset contains 500 candidates per query and
achieves nDCG@10 = 0.5760, hit@10 = 0.8500, and recall@100 = 0.8761. BM25 is
useful because many queries contain named entities or exact topic terms that
also appear in the answer passage.

BM25 is still well below dense retrieval. Cross-script tokenization,
morphology, spelling variants, short queries, and multiple relevant passages
limit exact lexical matching. Hard negatives from related Wikipedia passages
also share many surface terms.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset contains 500 candidates per
query and achieves nDCG@10 = 0.7775, hit@10 = 0.9600, and recall@100 = 0.9369.
Dense retrieval is the strongest observed top-rank profile.

This reflects the importance of multilingual semantic alignment. Dense
retrieval can match questions to answer-bearing passages even when lexical
forms differ or when morphology and script handling make sparse matching
difficult. It also ranks positives more effectively among same-topic hard
negatives.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains 100 candidates per query and
achieves nDCG@10 = 0.6942, hit@10 = 0.9400, and recall@100 = 0.9887. Hybrid
retrieval has the best recall@100 but is below dense retrieval for nDCG@10 and
hit@10.

This makes `reranking_hybrid` an excellent candidate pool for downstream
reranking. It combines sparse and dense evidence to retain nearly all positives,
but the top-rank ordering still favors the dense profile. A reranker should
convert the hybrid pool's coverage into dense-level or better rank quality.

### Metric Interpretation for Model Researchers

This is a multi-positive retrieval task. nDCG@10 rewards ranking several
relevant passages early, while hit@10 only checks whether at least one positive
appears near the top. Recall@100 measures whether positives are available for a
reranker.

Because many queries have multiple relevant passages, models should be judged by
how well they rank the set of answer-bearing passages, not just whether they
find one. The hybrid profile is especially useful for reranking experiments
because it has the highest positive coverage.

### Query and Relevance Type Tendencies

Queries are short native-language information needs about places, people,
definitions, dates, counts, and factual properties. Relevant documents are
Wikipedia passages in the same language setting that explicitly answer the
query.

The task rewards multilingual lexical coverage, semantic retrieval, and robust
script-specific processing. It also rewards handling multiple relevant passages
from the same article or closely related Wikipedia pages.

### Representative Failure Modes

BM25 can fail on morphology, tokenization, script variation, or paraphrased
queries. Dense retrieval can confuse same-topic passages when the correct
answer depends on a precise number, date, definition, or entity relation.
Hybrid retrieval can retain the positive but rank a dense or lexical hard
negative above it.

Rerankers should compare answer support directly, especially for questions that
ask for counts, dates, definitions, or named relations.

### Training Data That May Help

Useful training data includes MIRACL train splits, native-language Wikipedia
retrieval pairs, multilingual QA retrieval data, and same-language hard
negatives. Training should avoid overlapping MIRACL dev or test queries, qrels,
and positive passages from this Nano split.

Synthetic data can generate native-language questions from non-evaluation
Wikipedia passages. Negatives should come from the same article, adjacent
entities, or related topics while failing to answer the query. Questions should
be natural information needs, not translated English-only templates.

### Model Improvement Notes

Dense retrievers should strengthen multilingual alignment, script coverage, and
fine-grained factual discrimination. Sparse systems should use language-aware
tokenization and normalization. Rerankers should handle multiple positives and
same-topic hard negatives.

For hybrid systems, `NanoMMTEB-v2 / miracl` shows the value of hybrid candidate
generation: `reranking_hybrid` has the best recall@100. The next step is
reranking that preserves dense top-rank quality while using hybrid recall.

## Example Data

| Query | Positive document |
| --- | --- |
| కిమ్మూరు గ్రామ విస్తీర్ణం ఎంత? [30 chars] | కిమ్మూరు ఇది మండల కేంద్రమైన అడ్డతీగల నుండి 25 కి. మీ. దూరం లోను, సమీప పట్టణమైన పెద్దాపురం నుండి 33 కి. మీ. దూరంలోనూ ఉంది. 2011 భారత జనగణన గణాంకాల ప్రకారం ఈ గ్రామం 249 ఇళ్లతో, 887 జనాభాతో 283 హెక్టార్లలో విస్తరించి ఉంది. గ్రామంలో మగవారి సంఖ్య 455, ఆడవారి సంఖ్య 432. షెడ్యూల్డ్ కులాల సంఖ్య 138 కాగా షెడ్యూల్డ్ తెగల సంఖ్య 2. గ్రామం యొక్క జనగణన లొకేషన్ కోడ్ 586876.పిన్ కోడ్: 533429. [380 chars] |
| Welche Sekte hat Jim Jones geführt? [35 chars] | William Branham In den Jahren 1956 und 1957 unterstützte William Branham den jungen Prediger des Latter-Rain Movements und späteren Sektenführer Jim Jones und trat beispielsweise als Gastprediger in einer von ihm geleiteten Predigtreihe im "Cadle Tabernacle" in Indianapolis (Indiana) auf. Branham verhieß Jim Jones und seiner Gemeinde den Segen Gottes. Nach dieser Zeit überwarfen sich Branham und Jim Jones, u. a. da letzterer eine Rassentrennung ablehnte, während Branham eine klare Trennung befürwortete und Mischehen sogar verurteilte. [541 chars] |
| متى عقدت الجمعية البرلمانية لمجلس أوروبا دورتها الأولى؟ [55 chars] | الجمعية البرلمانية لمجلس أوروبا عقدت الجمعية دورتها الأولى في ستراسبورغ في 10 أغسطس 1949. [90 chars] |

### Public Sources

- [Making a MIRACL: Multilingual Information Retrieval Across a Continuum of Languages](https://arxiv.org/abs/2210.09984),
  2023.
- [MIRACL project page](https://project-miracl.github.io/).
- [mteb/MIRACLRetrievalHardNegatives](https://huggingface.co/datasets/mteb/MIRACLRetrievalHardNegatives).
- [hakari-bench/NanoMMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoMMTEB-v2),
  Nano benchmark dataset.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Making a MIRACL: Multilingual Information Retrieval Across a Continuum of Languages | 2023 | task paper | [https://arxiv.org/abs/2210.09984](https://arxiv.org/abs/2210.09984) |
| MIRACL project page | 2023 | project page | [https://project-miracl.github.io/](https://project-miracl.github.io/) |
| mteb/MIRACLRetrievalHardNegatives | 2024 | dataset card | [https://huggingface.co/datasets/mteb/MIRACLRetrievalHardNegatives](https://huggingface.co/datasets/mteb/MIRACLRetrievalHardNegatives) |

### Representative Snippets

| Query pattern | Positive document pattern |
| --- | --- |
| A Telugu question asking the area of a village. | A Telugu Wikipedia passage giving village area and population. |
| A German question asking which sect Jim Jones led. | A German passage mentioning Jim Jones in a religious-movement context. |
| An Arabic question asking when a parliamentary assembly first met. | An Arabic passage stating the first session date. |
| A Chinese question asking India's population. | A Chinese passage about India's population. |
| A Finnish question asking what voivode means. | A Finnish passage defining the title. |
