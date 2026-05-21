# NanoMTEB-Dutch

## Overview

NanoMTEB-Dutch is a compact Dutch retrieval group covering translated BEIR-NL
tasks, MTEB-NL native Dutch tasks, cross-lingual Belebele retrieval, legal and
medical retrieval, scientific evidence retrieval, news and tender retrieval,
web FAQ retrieval, and Dutch Wikipedia retrieval. Ten of the twenty-seven
subtasks are Dutch-translated CQADupStack duplicate-question splits, but the
group is broader than duplicate QA: it also measures statutory article
retrieval, scientific-paper relatedness, public procurement, fact verification,
and cross-lingual passage matching.

## Details

### What the Original Group Measures

NanoMTEB-Dutch follows the Dutch retrieval coverage assembled for MTEB-NL and
BEIR-NL. Several tasks are Dutch translations of established BEIR datasets such
as ArguAna, CQADupStack, FEVER, NFCorpus, Natural Questions, Quora, SciFact, and
SCIDOCS. Other tasks are Dutch-specific or Low Countries-specific resources:
bBSARD and LegalQA-NL for legal retrieval, Dutch News Articles for NOS news,
OpenTender for public procurement, VABB for Flemish academic bibliography
records, and WebFAQ or WikipediaRetrievalMultilingual for broad question-answer
retrieval.

The group therefore tests both Dutch language retrieval and translation
robustness. Some tasks have clean same-language Dutch question-passage pairs,
while others are translated from English-origin benchmarks or intentionally
cross-lingual, such as Belebele English-to-Dutch and Dutch-to-English
directions.

### Subtask Coverage

The twenty-seven subtasks cover eight retrieval families:

- **Argument and duplicate-question retrieval:** `argu_ana_nl`, the ten
  `cqadupstack_*` splits, and `quora` test counterargument or duplicate-intent
  matching rather than answer passage lookup.
- **Cross-lingual and monolingual reading-comprehension retrieval:** the three
  Belebele splits test Dutch-English, English-Dutch, and Dutch-Dutch passage
  retrieval.
- **Legal retrieval:** `b_bsardnl` and `legal_qanl` retrieve Belgian or Dutch
  statutory articles for citizen or legal questions.
- **Open-domain and encyclopedic retrieval:** `nq`, `wikipedia_multilingual_nl`,
  and `fever` retrieve Wikipedia-style evidence or answer passages.
- **Scientific and medical retrieval:** `nfcorpus_nl`, `sci_fact_nl`, and
  `scidocs_nl` cover medical article retrieval, scientific claim evidence, and
  citation-style paper relatedness.
- **News, tender, and bibliography retrieval:** `dutch_news_articles`,
  `open_tender`, and `vabb` retrieve event articles, procurement notices, or
  Flemish academic publication records.
- **FAQ retrieval:** `web_faq_nld` retrieves Dutch web FAQ answers.
- **Translated technical support retrieval:** the CQADupStack splits include
  Android, GIS, Mathematica, Physics, Programmers, Statistics, TeX, Webmasters,
  WordPress, and English-language usage forums.

Most tasks are Dutch, but several are marked multilingual because the retrieval
direction or content mixes Dutch and English. The three Belebele directions are
the clearest example; product names, code snippets, scientific names, and
technical terms also remain mixed in translated forum and scientific tasks.

### Observed Group Profile

Across the twenty-seven splits, NanoMTEB-Dutch contains 5,299 queries, 13,018
positive qrels, and 227,987 split-local candidate documents. The document count
is a sum across subtasks, not a deduplicated group-wide corpus size. The group
average is 2.46 positives per query, and 708 queries have more than one
positive.

Query lengths vary sharply. `argu_ana_nl` has very long argument queries
averaging 1,316.90 characters, while `nfcorpus_nl` has very short lay health
topics averaging 18.51 characters. Documents are also heterogeneous: Belebele
and Wikipedia passages are short, CQADupStack documents are longer forum posts,
NFCorpus and SciFact use abstract-like biomedical text, and legal/procurement
tasks contain formal article or tender language. The query-weighted mean query
length is 110.04 characters; the document-weighted mean document length is
841.65 characters.

### BM25 Difficulty

The query-weighted BM25 baseline reaches nDCG@10 = 0.4560 and hit@10 = 0.5820.
The easiest split by nDCG@10 is `fever` at 0.9221, followed by Dutch news,
Wikipedia, Quora, LegalQA-NL, and same-language Belebele. These tasks often
contain distinctive names, article titles, or direct answer/evidence wording.

The hardest split is `belebele_nld_latn_eng_latn` at nDCG@10 = 0.1226, where
English questions must retrieve Dutch passages and BM25 has little lexical
bridge beyond names and numbers. Other hard splits include `b_bsardnl`,
`scidocs_nl`, and the Mathematica/TeX/Webmasters CQADupStack splits. These
tasks require legal terminology mapping, citation-style scientific relatedness,
or duplicate technical intent rather than simple word overlap.

### Training Data That May Help

Useful training data should be chosen by retrieval family. For translated BEIR
tasks, non-overlapping BEIR-NL or MTEB-NL training data, multilingual retrieval
pairs, and Dutch paraphrase data are useful, but upstream evaluation rows should
be excluded. For legal retrieval, use non-overlapping Dutch and Belgian
statutory question-article pairs, legal QA attribution data, and hard negatives
from adjacent articles. For scientific and medical tasks, use Dutch or
translated scientific claim-evidence pairs, biomedical article retrieval, and
citation graph supervision.

For CQADupStack and Quora, duplicate-question leakage is especially risky:
training should exclude evaluation duplicate clusters, positives, and near
duplicates. For cross-lingual Belebele, multilingual QA retrieval pairs and
parallel passage data can help, but the model should learn retrieval alignment
rather than memorize the benchmark passages.

### Synthetic Data Guidance

Synthetic data should preserve the retrieval relation of each task. For
duplicate-question tasks, generate multiple Dutch phrasings of the same
technical or forum problem and include hard negatives from the same domain but
different intent. For legal tasks, generate citizen or legal questions grounded
in specific statute articles with near-negative adjacent provisions. For
scientific tasks, generate claims, titles, and abstracts where relevance depends
on evidence, citation, or related-work relations. For cross-lingual tasks,
generate paired questions and passages in different languages while keeping the
answer-bearing relation explicit.

Evaluation queries, positive documents, and duplicate clusters from
NanoMTEB-Dutch should not be used as seeds.

## Task Summary

| Task | Retrieval shape | Lang | Queries | Docs | Positive qrels | BM25 nDCG@10 | BM25 hit@10 | Query avg chars | Doc avg chars | Source status |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| [argu_ana_nl](argu_ana_nl.md) | Dutch argument to counterargument | nl | 199 | 8,624 | 199 | 0.2970 | 0.6482 | 1,316.90 | 1,141.13 | BEIR-NL / ArguAna |
| [b_bsardnl](b_bsardnl.md) | Dutch legal question to Belgian statute articles | nl | 200 | 10,000 | 923 | 0.1249 | 0.2950 | 93.84 | 863.16 | bBSARD paper |
| [belebele_eng_latn_nld_latn](belebele_eng_latn_nld_latn.md) | Dutch question to English passage | multilingual | 200 | 488 | 200 | 0.4738 | 0.5850 | 69.39 | 475.51 | Belebele paper |
| [belebele_nld_latn_eng_latn](belebele_nld_latn_eng_latn.md) | English question to Dutch passage | multilingual | 200 | 488 | 200 | 0.1226 | 0.1950 | 81.31 | 529.14 | Belebele paper |
| [belebele_nld_latn_nld_latn](belebele_nld_latn_nld_latn.md) | Dutch question to Dutch passage | nl | 200 | 488 | 200 | 0.8364 | 0.9150 | 69.39 | 529.14 | Belebele paper |
| [cqadupstack_android](cqadupstack_android.md) | Dutch Android duplicate question retrieval | nl | 200 | 10,000 | 200 | 0.2944 | 0.4250 | 59.10 | 638.08 | CQADupStack + BEIR-NL |
| [cqadupstack_english](cqadupstack_english.md) | Dutch English-usage duplicate retrieval | nl | 200 | 10,000 | 200 | 0.2769 | 0.3550 | 49.65 | 521.67 | CQADupStack + BEIR-NL |
| [cqadupstack_gis](cqadupstack_gis.md) | Dutch GIS duplicate question retrieval | nl | 200 | 10,000 | 200 | 0.2790 | 0.3700 | 62.70 | 1,036.05 | CQADupStack + BEIR-NL |
| [cqadupstack_mathematica](cqadupstack_mathematica.md) | Dutch Mathematica duplicate retrieval | nl | 200 | 10,000 | 200 | 0.1826 | 0.2750 | 55.30 | 1,166.66 | CQADupStack + BEIR-NL |
| [cqadupstack_physics](cqadupstack_physics.md) | Dutch physics duplicate retrieval | nl | 200 | 10,000 | 200 | 0.3269 | 0.4250 | 62.09 | 870.44 | CQADupStack + BEIR-NL |
| [cqadupstack_programmers](cqadupstack_programmers.md) | Dutch software-engineering duplicate retrieval | nl | 200 | 10,000 | 200 | 0.2991 | 0.4150 | 61.25 | 1,142.35 | CQADupStack + BEIR-NL |
| [cqadupstack_stats](cqadupstack_stats.md) | Dutch statistics duplicate retrieval | nl | 200 | 10,000 | 200 | 0.2827 | 0.3850 | 64.27 | 1,097.65 | CQADupStack + BEIR-NL |
| [cqadupstack_tex](cqadupstack_tex.md) | Dutch TeX duplicate retrieval | nl | 200 | 10,000 | 200 | 0.2106 | 0.2850 | 53.53 | 1,211.75 | CQADupStack + BEIR-NL |
| [cqadupstack_webmasters](cqadupstack_webmasters.md) | Dutch webmaster duplicate retrieval | nl | 200 | 10,000 | 200 | 0.2307 | 0.2850 | 58.83 | 761.20 | CQADupStack + BEIR-NL |
| [cqadupstack_wordpress](cqadupstack_wordpress.md) | Dutch WordPress duplicate retrieval | nl | 200 | 10,000 | 200 | 0.2608 | 0.3700 | 56.55 | 1,183.40 | CQADupStack + BEIR-NL |
| [dutch_news_articles](dutch_news_articles.md) | Dutch headline to news article | nl | 200 | 10,000 | 200 | 0.8868 | 0.9350 | 48.96 | 1,146.66 | MTEB-NL / NOS articles |
| [fever](fever.md) | Dutch claim to Wikipedia evidence | nl | 200 | 10,000 | 233 | 0.9221 | 0.9800 | 54.87 | 445.71 | FEVER + BEIR-NL |
| [legal_qanl](legal_qanl.md) | Dutch legal question to law article | nl | 102 | 10,000 | 157 | 0.8143 | 0.9804 | 104.29 | 665.01 | LegalQA-NL paper |
| [nfcorpus_nl](nfcorpus_nl.md) | Dutch health topic to biomedical article | multilingual | 199 | 3,593 | 5,880 | 0.3486 | 0.6432 | 18.51 | 1,743.72 | NFCorpus + BEIR-NL |
| [nq](nq.md) | Dutch web question to Wikipedia passage | nl | 200 | 10,000 | 242 | 0.4505 | 0.7050 | 52.69 | 595.40 | Natural Questions + BEIR-NL |
| [open_tender](open_tender.md) | Dutch tender title to procurement notice | nl | 199 | 10,000 | 199 | 0.6712 | 0.7136 | 62.19 | 442.03 | MTEB-NL / OpenTender |
| [quora](quora.md) | Dutch duplicate short-question retrieval | nl | 200 | 10,000 | 573 | 0.8376 | 0.9550 | 51.80 | 66.56 | Quora + BEIR-NL |
| [sci_fact_nl](sci_fact_nl.md) | Dutch scientific claim to evidence abstract | nl | 200 | 5,183 | 226 | 0.6160 | 0.7900 | 100.13 | 1,640.32 | SciFact + BEIR-NL |
| [scidocs_nl](scidocs_nl.md) | Dutch scientific title to related papers | nl | 200 | 10,000 | 986 | 0.1335 | 0.4250 | 77.72 | 1,331.57 | SCIDOCS + BEIR-NL |
| [vabb](vabb.md) | Dutch academic title to bibliography record | nl | 200 | 9,123 | 200 | 0.6952 | 0.7850 | 74.47 | 837.89 | VABB / MTEB-NL |
| [web_faq_nld](web_faq_nld.md) | Dutch FAQ question to answer snippet | nl | 200 | 10,000 | 200 | 0.7698 | 0.8450 | 50.45 | 322.18 | WebFAQ |
| [wikipedia_multilingual_nl](wikipedia_multilingual_nl.md) | Dutch synthetic question to Wikipedia passage | nl | 200 | 10,000 | 200 | 0.8444 | 0.9250 | 63.54 | 381.01 | WikipediaRetrievalMultilingual |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-Dutch |
| Backing dataset | NanoMTEB-Dutch |
| Hugging Face dataset | [hakari-bench/NanoMTEB-Dutch](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Dutch) |
| Languages | nl, multilingual |
| Category | natural_language |
| Subtasks | 27 |
| Total queries | 5,299 |
| Split-local documents | 227,987 |
| Positive qrels | 13,018 |
| Positives per query | 2.46 average |
| Multi-positive queries | 708 |
| Query-weighted BM25 nDCG@10 | 0.4560 |
| Query-weighted BM25 hit@10 | 0.5820 |
| Mean query length | 110.04 chars, weighted by query count |
| Mean document length | 841.65 chars, weighted by split-local document count |

### Public Sources

- [MTEB-NL and E5-NL](https://arxiv.org/abs/2509.12340); Dutch benchmark source.
- [BEIR-NL: Zero-shot Information Retrieval Benchmark for the Dutch Language](https://aclanthology.org/2025.bucc-1.5/); Dutch translation benchmark.
- [The Belebele Benchmark](https://arxiv.org/abs/2308.16884); multilingual reading-comprehension source.
- [CQADupStack](https://doi.org/10.1145/2838931.2838934); community QA duplicate retrieval source.
- [Bilingual BSARD](https://arxiv.org/abs/2412.07462); Dutch/French Belgian statutory article retrieval.
- [Retrieval-Augmented Generation for Long-form Question Answering in Dutch](https://aclanthology.org/2024.nllp-1.12/); LegalQA-NL source.
- [FEVER](https://aclanthology.org/N18-1074/), [NFCorpus](https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf), [Natural Questions](https://aclanthology.org/Q19-1026/), [SciFact](https://arxiv.org/abs/2004.14974), and [SPECTER/SciDocs](https://arxiv.org/abs/2004.07180).
- [WebFAQ](https://arxiv.org/abs/2502.20936), [VABB-SHW Zenodo record](https://zenodo.org/records/14214806), and [WikipediaRetrievalMultilingual source dataset](https://huggingface.co/datasets/ellamind/wikipedia-2023-11-retrieval-multilingual-queries).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMTEB-Dutch](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Dutch)
- Source examples:
  [clips/beir-nl-arguana](https://huggingface.co/datasets/clips/beir-nl-arguana),
  [clips/mteb-nl-bbsard](https://huggingface.co/datasets/clips/mteb-nl-bbsard),
  [mteb/belebele](https://huggingface.co/datasets/mteb/belebele),
  [clips/beir-nl-cqadupstack](https://huggingface.co/datasets/clips/beir-nl-cqadupstack),
  [clips/mteb-nl-legalqa-pr](https://huggingface.co/datasets/clips/mteb-nl-legalqa-pr),
  [mteb/WebFAQRetrieval](https://huggingface.co/datasets/mteb/WebFAQRetrieval),
  [mteb/WikipediaRetrievalMultilingual](https://huggingface.co/datasets/mteb/WikipediaRetrievalMultilingual).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| MTEB-NL and E5-NL | 2025 | benchmark paper | https://arxiv.org/abs/2509.12340 |
| BEIR-NL: Zero-shot Information Retrieval Benchmark for the Dutch Language | 2025 | benchmark paper | https://aclanthology.org/2025.bucc-1.5/ |
| The Belebele Benchmark | 2023 | source task paper | https://arxiv.org/abs/2308.16884 |
| CQADupStack: A Benchmark Data Set for Community Question-Answering Research | 2015 | source task paper | https://doi.org/10.1145/2838931.2838934 |
| Bilingual BSARD: Extending Statutory Article Retrieval to Dutch | 2024 | source task paper | https://arxiv.org/abs/2412.07462 |
| Retrieval-Augmented Generation for Long-form Question Answering in Dutch | 2024 | source task paper | https://aclanthology.org/2024.nllp-1.12/ |
| FEVER: a Large-scale Dataset for Fact Extraction and Verification | 2018 | source task paper | https://aclanthology.org/N18-1074/ |
| NFCorpus: A Full-Text Learning to Rank Dataset for Medical Information Retrieval | 2016 | source task paper | https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf |
| Natural Questions: A Benchmark for Question Answering Research | 2019 | source task paper | https://aclanthology.org/Q19-1026/ |
| Fact or Fiction: Verifying Scientific Claims | 2020 | source task paper | https://arxiv.org/abs/2004.14974 |
| SPECTER: Document-level Representation Learning using Citation-informed Transformers | 2020 | source task paper | https://arxiv.org/abs/2004.07180 |
| WebFAQ: A Multilingual Collection of Natural Q&A Datasets for Dense Retrieval | 2025 | source task paper | https://arxiv.org/abs/2502.20936 |

## Machine-Readable Metadata

<!-- benchmark-task-group-metadata:v1 -->

```yaml
benchmark_task_group_metadata:
  schema_version: 1
  document_status: reviewed_manual
  nano_set: NanoMTEB-Dutch
  backing_dataset: NanoMTEB-Dutch
  dataset_id: hakari-bench/NanoMTEB-Dutch
  language: nl
  languages:
    - nl
    - multilingual
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-Dutch/index.md
  source_research:
    primary_source_type: multiple_dataset_cards_and_source_references
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    tasks: 27
    queries: 5299
    split_local_documents: 227987
    positive_qrels: 13018
  positives_per_query:
    average: 2.456689941498396
    min: 1
    median_task_median: 1.0
    max: 100
    multi_positive_tasks: 8
    multi_positive_queries: 708
  text_stats_chars:
    query_mean_weighted_by_queries: 110.04415928983921
    document_mean_weighted_by_documents: 841.6543881824689
  bm25:
    ndcg_at_10_query_weighted: 0.45604667070484994
    hit_at_10_query_weighted: 0.5819966031117192
    ndcg_at_10_unweighted_task_mean: 0.46253901523703705
    hit_at_10_unweighted_task_mean: 0.5892747141481481
    source: dataset_bm25_column
    easiest_task_by_ndcg_at_10: fever
    hardest_task_by_ndcg_at_10: belebele_nld_latn_eng_latn
  tasks:
    - name: argu_ana_nl
      path: docs/benchmark_tasks/NanoMTEB-Dutch/argu_ana_nl.md
      retrieval_shape: dutch_argument_to_counterargument
      language: nl
      queries: 199
      documents: 8624
      positive_qrels: 199
      bm25_ndcg_at_10: 0.296979197
      bm25_hit_at_10: 0.648241206
    - name: b_bsardnl
      path: docs/benchmark_tasks/NanoMTEB-Dutch/b_bsardnl.md
      retrieval_shape: dutch_legal_question_to_belgian_statute_articles
      language: nl
      queries: 200
      documents: 10000
      positive_qrels: 923
      bm25_ndcg_at_10: 0.1249128833
      bm25_hit_at_10: 0.295
    - name: belebele_eng_latn_nld_latn
      path: docs/benchmark_tasks/NanoMTEB-Dutch/belebele_eng_latn_nld_latn.md
      retrieval_shape: dutch_question_to_english_passage
      language: multilingual
      queries: 200
      documents: 488
      positive_qrels: 200
      bm25_ndcg_at_10: 0.4737822933
      bm25_hit_at_10: 0.585
    - name: belebele_nld_latn_eng_latn
      path: docs/benchmark_tasks/NanoMTEB-Dutch/belebele_nld_latn_eng_latn.md
      retrieval_shape: english_question_to_dutch_passage
      language: multilingual
      queries: 200
      documents: 488
      positive_qrels: 200
      bm25_ndcg_at_10: 0.1226419985
      bm25_hit_at_10: 0.195
    - name: belebele_nld_latn_nld_latn
      path: docs/benchmark_tasks/NanoMTEB-Dutch/belebele_nld_latn_nld_latn.md
      retrieval_shape: dutch_question_to_dutch_passage
      language: nl
      queries: 200
      documents: 488
      positive_qrels: 200
      bm25_ndcg_at_10: 0.8364107302
      bm25_hit_at_10: 0.915
    - name: cqadupstack_android
      path: docs/benchmark_tasks/NanoMTEB-Dutch/cqadupstack_android.md
      retrieval_shape: dutch_android_duplicate_question_retrieval
      language: nl
      queries: 200
      documents: 10000
      positive_qrels: 200
      bm25_ndcg_at_10: 0.2943883243
      bm25_hit_at_10: 0.425
    - name: cqadupstack_english
      path: docs/benchmark_tasks/NanoMTEB-Dutch/cqadupstack_english.md
      retrieval_shape: dutch_english_usage_duplicate_retrieval
      language: nl
      queries: 200
      documents: 10000
      positive_qrels: 200
      bm25_ndcg_at_10: 0.2768966576
      bm25_hit_at_10: 0.355
    - name: cqadupstack_gis
      path: docs/benchmark_tasks/NanoMTEB-Dutch/cqadupstack_gis.md
      retrieval_shape: dutch_gis_duplicate_question_retrieval
      language: nl
      queries: 200
      documents: 10000
      positive_qrels: 200
      bm25_ndcg_at_10: 0.2790339168
      bm25_hit_at_10: 0.37
    - name: cqadupstack_mathematica
      path: docs/benchmark_tasks/NanoMTEB-Dutch/cqadupstack_mathematica.md
      retrieval_shape: dutch_mathematica_duplicate_retrieval
      language: nl
      queries: 200
      documents: 10000
      positive_qrels: 200
      bm25_ndcg_at_10: 0.1826120876
      bm25_hit_at_10: 0.275
    - name: cqadupstack_physics
      path: docs/benchmark_tasks/NanoMTEB-Dutch/cqadupstack_physics.md
      retrieval_shape: dutch_physics_duplicate_retrieval
      language: nl
      queries: 200
      documents: 10000
      positive_qrels: 200
      bm25_ndcg_at_10: 0.32693259
      bm25_hit_at_10: 0.425
    - name: cqadupstack_programmers
      path: docs/benchmark_tasks/NanoMTEB-Dutch/cqadupstack_programmers.md
      retrieval_shape: dutch_software_engineering_duplicate_retrieval
      language: nl
      queries: 200
      documents: 10000
      positive_qrels: 200
      bm25_ndcg_at_10: 0.2990881643
      bm25_hit_at_10: 0.415
    - name: cqadupstack_stats
      path: docs/benchmark_tasks/NanoMTEB-Dutch/cqadupstack_stats.md
      retrieval_shape: dutch_statistics_duplicate_retrieval
      language: nl
      queries: 200
      documents: 10000
      positive_qrels: 200
      bm25_ndcg_at_10: 0.2826641003
      bm25_hit_at_10: 0.385
    - name: cqadupstack_tex
      path: docs/benchmark_tasks/NanoMTEB-Dutch/cqadupstack_tex.md
      retrieval_shape: dutch_tex_duplicate_retrieval
      language: nl
      queries: 200
      documents: 10000
      positive_qrels: 200
      bm25_ndcg_at_10: 0.2105825851
      bm25_hit_at_10: 0.285
    - name: cqadupstack_webmasters
      path: docs/benchmark_tasks/NanoMTEB-Dutch/cqadupstack_webmasters.md
      retrieval_shape: dutch_webmaster_duplicate_retrieval
      language: nl
      queries: 200
      documents: 10000
      positive_qrels: 200
      bm25_ndcg_at_10: 0.2306924388
      bm25_hit_at_10: 0.285
    - name: cqadupstack_wordpress
      path: docs/benchmark_tasks/NanoMTEB-Dutch/cqadupstack_wordpress.md
      retrieval_shape: dutch_wordpress_duplicate_retrieval
      language: nl
      queries: 200
      documents: 10000
      positive_qrels: 200
      bm25_ndcg_at_10: 0.2607990583
      bm25_hit_at_10: 0.37
    - name: dutch_news_articles
      path: docs/benchmark_tasks/NanoMTEB-Dutch/dutch_news_articles.md
      retrieval_shape: dutch_headline_to_news_article
      language: nl
      queries: 200
      documents: 10000
      positive_qrels: 200
      bm25_ndcg_at_10: 0.886775466
      bm25_hit_at_10: 0.935
    - name: fever
      path: docs/benchmark_tasks/NanoMTEB-Dutch/fever.md
      retrieval_shape: dutch_claim_to_wikipedia_evidence
      language: nl
      queries: 200
      documents: 10000
      positive_qrels: 233
      bm25_ndcg_at_10: 0.92210826
      bm25_hit_at_10: 0.98
    - name: legal_qanl
      path: docs/benchmark_tasks/NanoMTEB-Dutch/legal_qanl.md
      retrieval_shape: dutch_legal_question_to_law_article
      language: nl
      queries: 102
      documents: 10000
      positive_qrels: 157
      bm25_ndcg_at_10: 0.814312257
      bm25_hit_at_10: 0.980392157
    - name: nfcorpus_nl
      path: docs/benchmark_tasks/NanoMTEB-Dutch/nfcorpus_nl.md
      retrieval_shape: dutch_health_topic_to_biomedical_article
      language: multilingual
      queries: 199
      documents: 3593
      positive_qrels: 5880
      bm25_ndcg_at_10: 0.348620615
      bm25_hit_at_10: 0.64321608
    - name: nq
      path: docs/benchmark_tasks/NanoMTEB-Dutch/nq.md
      retrieval_shape: dutch_web_question_to_wikipedia_passage
      language: nl
      queries: 200
      documents: 10000
      positive_qrels: 242
      bm25_ndcg_at_10: 0.45050919
      bm25_hit_at_10: 0.705
    - name: open_tender
      path: docs/benchmark_tasks/NanoMTEB-Dutch/open_tender.md
      retrieval_shape: dutch_tender_title_to_procurement_notice
      language: nl
      queries: 199
      documents: 10000
      positive_qrels: 199
      bm25_ndcg_at_10: 0.671173217
      bm25_hit_at_10: 0.713567839
    - name: quora
      path: docs/benchmark_tasks/NanoMTEB-Dutch/quora.md
      retrieval_shape: dutch_duplicate_short_question_retrieval
      language: nl
      queries: 200
      documents: 10000
      positive_qrels: 573
      bm25_ndcg_at_10: 0.837639743
      bm25_hit_at_10: 0.955
    - name: sci_fact_nl
      path: docs/benchmark_tasks/NanoMTEB-Dutch/sci_fact_nl.md
      retrieval_shape: dutch_scientific_claim_to_evidence_abstract
      language: nl
      queries: 200
      documents: 5183
      positive_qrels: 226
      bm25_ndcg_at_10: 0.616037929
      bm25_hit_at_10: 0.79
    - name: scidocs_nl
      path: docs/benchmark_tasks/NanoMTEB-Dutch/scidocs_nl.md
      retrieval_shape: dutch_scientific_title_to_related_papers
      language: nl
      queries: 200
      documents: 10000
      positive_qrels: 986
      bm25_ndcg_at_10: 0.133520298
      bm25_hit_at_10: 0.425
    - name: vabb
      path: docs/benchmark_tasks/NanoMTEB-Dutch/vabb.md
      retrieval_shape: dutch_academic_title_to_bibliography_record
      language: nl
      queries: 200
      documents: 9123
      positive_qrels: 200
      bm25_ndcg_at_10: 0.695249921
      bm25_hit_at_10: 0.785
    - name: web_faq_nld
      path: docs/benchmark_tasks/NanoMTEB-Dutch/web_faq_nld.md
      retrieval_shape: dutch_faq_question_to_answer_snippet
      language: nl
      queries: 200
      documents: 10000
      positive_qrels: 200
      bm25_ndcg_at_10: 0.769755238
      bm25_hit_at_10: 0.845
    - name: wikipedia_multilingual_nl
      path: docs/benchmark_tasks/NanoMTEB-Dutch/wikipedia_multilingual_nl.md
      retrieval_shape: dutch_synthetic_question_to_wikipedia_passage
      language: nl
      queries: 200
      documents: 10000
      positive_qrels: 200
      bm25_ndcg_at_10: 0.844434252
      bm25_hit_at_10: 0.925
  learning:
    leakage_note: exclude NanoMTEB-Dutch evaluation queries, qrels, positive documents, translated duplicate clusters, and upstream test rows from training
    useful_training_data:
      - Dutch and multilingual duplicate-question retrieval pairs
      - BEIR-NL and MTEB-NL training data with evaluation rows removed
      - Dutch legal question-to-statute and legal attribution pairs
      - Dutch biomedical and scientific evidence retrieval pairs
      - Dutch news, procurement, bibliography, FAQ, and Wikipedia retrieval pairs
      - cross-lingual Dutch-English reading-comprehension retrieval pairs
      - hard negatives from the same forum, statute family, paper area, tender domain, or Wikipedia entity
    synthetic_data:
      document_generation: Dutch forum posts, legal articles, news articles, tender notices, scientific abstracts, FAQ answers, and Wikipedia passages in source-like style
      question_generation: Dutch duplicate questions, legal questions, claims, headlines, tender titles, FAQ questions, and cross-lingual reading-comprehension questions grounded in generated or selected documents
      answerability: positives must preserve counterargument, duplicate intent, answer evidence, statutory support, citation relevance, or passage grounding rather than only broad topic overlap
    multi_positive_training: preserve_nfcorpus_bbsard_scidocs_quora_and_other_multi_positive_qrels
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMTEB-Dutch
    source_urls:
      - label: MTEB-NL arXiv
        url: https://arxiv.org/abs/2509.12340
      - label: BEIR-NL ACL Anthology
        url: https://aclanthology.org/2025.bucc-1.5/
      - label: Belebele arXiv
        url: https://arxiv.org/abs/2308.16884
      - label: CQADupStack DOI
        url: https://doi.org/10.1145/2838931.2838934
      - label: bBSARD arXiv
        url: https://arxiv.org/abs/2412.07462
      - label: LegalQA-NL paper
        url: https://aclanthology.org/2024.nllp-1.12/
      - label: WebFAQ arXiv
        url: https://arxiv.org/abs/2502.20936
      - label: VABB-SHW Zenodo
        url: https://zenodo.org/records/14214806
    source_notes: []
  references:
    - title: MTEB-NL and E5-NL
      url: https://arxiv.org/abs/2509.12340
      year: 2025
      is_paper: true
      source_confidence: definitive_paper_link
    - title: "BEIR-NL: Zero-shot Information Retrieval Benchmark for the Dutch Language"
      url: https://aclanthology.org/2025.bucc-1.5/
      year: 2025
      is_paper: true
      source_confidence: definitive_paper_link
    - title: The Belebele Benchmark
      url: https://arxiv.org/abs/2308.16884
      year: 2023
      is_paper: true
      source_confidence: definitive_paper_link
    - title: "CQADupStack: A Benchmark Data Set for Community Question-Answering Research"
      url: https://doi.org/10.1145/2838931.2838934
      year: 2015
      is_paper: true
      source_confidence: definitive_paper_link
    - title: "Bilingual BSARD: Extending Statutory Article Retrieval to Dutch"
      url: https://arxiv.org/abs/2412.07462
      year: 2024
      is_paper: true
      source_confidence: definitive_paper_link
    - title: Retrieval-Augmented Generation for Long-form Question Answering in Dutch
      url: https://aclanthology.org/2024.nllp-1.12/
      year: 2024
      is_paper: true
      source_confidence: definitive_paper_link
```
