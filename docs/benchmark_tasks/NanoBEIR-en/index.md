# NanoBEIR-en

## Overview

NanoBEIR-en is the English compact BEIR group. It keeps BEIR's central design
idea, a deliberately heterogeneous retrieval benchmark, but packages each task
as a small query-corpus-qrels split for fast evaluation. The group spans
argument retrieval, climate and general fact verification, entity search,
financial QA, multi-hop Wikipedia QA, web passage ranking, medical and
scientific evidence retrieval, duplicate-question matching, scientific
document-relatedness, and controversial-question argument retrieval.

This group should not be read as one homogeneous English search task. Its
subtasks reward different retrieval behavior: exact entity matching helps
DBpedia, paraphrase and intent matching matter for Quora and MS MARCO, evidence
grounding matters for FEVER, Climate-FEVER, SciFact, and TREC-like scientific
tasks, and long argumentative text dominates ArguAna and Touché.

## Details

### What the Original Group Measures

[BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663)
introduced BEIR to evaluate zero-shot retrieval across many datasets, domains,
query styles, and relevance definitions rather than optimizing for a single web
search collection. [NanoBEIR: Smaller BEIR dataset subsets](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)
then provides compact BEIR-style subsets. NanoBEIR-en is the English component:
it preserves BEIR's task diversity while making the evaluation small enough for
quick iteration.

The group includes both classic ad-hoc retrieval tasks and tasks that started
as QA, fact verification, duplicate detection, entity search, or argument
mining. That matters because relevance is not uniform. A relevant DBpedia
document names the intended entity; a relevant Quora document is a semantically
equivalent question; a relevant SciFact or Climate-FEVER document is evidence
for a claim; a relevant ArguAna document is a counterargument; and a relevant
Touché document may be a high-quality argumentative passage rather than a short
answer.

### Subtask Coverage

- **Argument and debate retrieval:** `NanoArguAna` retrieves counterarguments
  for long debate arguments, while `NanoTouche2020` retrieves argumentative
  passages for controversial questions.
- **Fact and evidence retrieval:** `NanoFEVER`, `NanoClimateFEVER`, and
  `NanoSciFact` retrieve evidence for general, climate, and scientific claims.
- **Open-domain and web QA retrieval:** `NanoHotpotQA`, `NanoNQ`, and
  `NanoMSMARCO` use Wikipedia or web-style questions and passages, with HotpotQA
  adding multi-hop evidence needs.
- **Specialized domains:** `NanoFiQA2018` covers finance questions,
  `NanoNFCorpus` covers medical and nutrition topics, and `NanoSCIDOCS` covers
  scientific document relatedness.
- **Entity and duplicate matching:** `NanoDBPedia` emphasizes entity
  disambiguation, while `NanoQuoraRetrieval` emphasizes paraphrase and duplicate
  question intent.

All 13 subtasks are English natural-language retrieval tasks. They differ
strongly in positives per query: single-positive tasks such as `NanoArguAna`,
`NanoMSMARCO`, and most QA-style splits coexist with multi-positive tasks such
as `NanoDBPedia`, `NanoNFCorpus`, and `NanoTouche2020`.

### Observed Group Profile

The current NanoBEIR-en task pages report 649 queries, 4,696 positive qrels, and
56,723 split-local candidate documents. The document count is a sum across
subtasks, not a deduplicated shared corpus size. Queries average 147.53
characters when weighted by query count. That average is pulled upward by
`NanoArguAna`, whose queries are full arguments averaging 1,201.78 characters;
many other tasks use short questions or claims under 100 characters.

The documents average 903.41 characters when weighted by split-local document
count. Short duplicate-question documents in `NanoQuoraRetrieval` average only
54.81 characters, while argumentative and evidence-heavy corpora such as
`NanoTouche2020`, `NanoClimateFEVER`, `NanoNFCorpus`, and `NanoSciFact` use much
longer passages or abstracts. The group contains 343 multi-positive queries,
which means listwise or multi-positive-aware training is relevant for several
subtasks even though the compact group also includes many one-positive splits.

### BM25 Difficulty

Using the dataset-provided BM25 candidate columns, NanoBEIR-en has
query-weighted BM25 nDCG@10 = 0.5533 and hit@10 = 0.8182. The strongest BM25
subtasks are `NanoHotpotQA` (nDCG@10 = 0.8176, hit@10 = 1.0000),
`NanoFEVER` (0.8141, 0.9400), and `NanoQuoraRetrieval` (0.7864, 0.9400), where
named entities, Wikipedia terms, or repeated question wording often provide
strong lexical anchors.

The weakest BM25 subtask is `NanoClimateFEVER` (nDCG@10 = 0.3289,
hit@10 = 0.7400), followed by `NanoSCIDOCS`, `NanoFiQA2018`, and
`NanoNFCorpus`. These tasks often require domain wording, evidence
interpretation, or a mapping from short user language to longer technical
documents. `NanoArguAna` is also a useful warning case: the texts are long and
lexical overlap is common, but the target relation is counterargument matching,
not topical similarity alone.

### Training Data That May Help

Useful training data should match the subtask relation, not just the English
language. BEIR-style training can include non-overlapping MS MARCO passage
pairs, Natural Questions or HotpotQA train evidence pairs, FEVER and SciFact
claim-evidence retrieval data, finance QA pairs, medical or nutrition evidence
retrieval pairs, entity search logs, duplicate-question pairs, and
argument-counterargument datasets. Multi-positive tasks benefit from objectives
that preserve multiple relevant documents rather than collapsing each query to a
single positive.

Training should exclude NanoBEIR-en evaluation queries, qrels, and positive
documents. For source datasets that have public train/dev/test splits, upstream
dev or test data likely to overlap with BEIR or NanoBEIR evaluation rows should
be avoided unless an explicit overlap audit has been performed.

### Synthetic Data Guidance

Synthetic data should be generated by task family. For evidence retrieval,
create realistic claims or questions grounded in non-evaluation Wikipedia,
scientific, climate, medical, or finance passages. For duplicate-question
retrieval, generate paraphrase clusters that preserve intent while changing
surface wording. For argument retrieval, generate claims and counterarguments
with stance and rebuttal structure, not merely topical passages. For entity
search, generate short keyword or natural-language entity queries with
disambiguating descriptions.

Do not seed synthetic generation with NanoBEIR-en evaluation queries or positive
documents. Generated positives should be explicitly relevant under the source
task's definition: evidence should support the claim, duplicate questions should
share intent, counterarguments should oppose or rebut the query argument, and
entity documents should identify the intended entity.

## Task Summary

| Task | Retrieval focus | Queries | Docs | Positive qrels | BM25 nDCG@10 | BM25 hit@10 | Query avg chars | Doc avg chars |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| [NanoArguAna](NanoArguAna.md) | argument to counterargument | 50 | 3,635 | 50 | 0.4462 | 0.7400 | 1,201.78 | 1,011.77 |
| [NanoClimateFEVER](NanoClimateFEVER.md) | climate claim to evidence | 50 | 3,408 | 148 | 0.3289 | 0.7400 | 128.40 | 1,619.53 |
| [NanoDBPedia](NanoDBPedia.md) | entity query to DBpedia entity document | 50 | 6,045 | 1,158 | 0.5619 | 0.9200 | 33.12 | 336.28 |
| [NanoFEVER](NanoFEVER.md) | factual claim to Wikipedia evidence | 50 | 4,996 | 57 | 0.8141 | 0.9400 | 45.44 | 1,228.73 |
| [NanoFiQA2018](NanoFiQA2018.md) | finance question to answer passage | 50 | 4,598 | 123 | 0.3583 | 0.6400 | 58.48 | 899.64 |
| [NanoHotpotQA](NanoHotpotQA.md) | multi-hop question to Wikipedia evidence | 50 | 5,090 | 100 | 0.8176 | 1.0000 | 88.34 | 349.65 |
| [NanoMSMARCO](NanoMSMARCO.md) | web search question to passage | 50 | 5,043 | 50 | 0.4890 | 0.7400 | 32.16 | 330.23 |
| [NanoNFCorpus](NanoNFCorpus.md) | health topic to medical evidence | 50 | 2,953 | 1,651 | 0.3620 | 0.6600 | 21.00 | 1,512.68 |
| [NanoNQ](NanoNQ.md) | natural question to Wikipedia evidence | 50 | 5,035 | 57 | 0.4708 | 0.6800 | 46.96 | 525.62 |
| [NanoQuoraRetrieval](NanoQuoraRetrieval.md) | question to duplicate question | 50 | 5,046 | 70 | 0.7864 | 0.9400 | 47.96 | 54.81 |
| [NanoSCIDOCS](NanoSCIDOCS.md) | paper title to related scientific document | 50 | 2,210 | 244 | 0.3360 | 0.7800 | 72.84 | 1,093.82 |
| [NanoSciFact](NanoSciFact.md) | scientific claim to evidence abstract | 50 | 2,919 | 56 | 0.7174 | 0.8600 | 95.82 | 1,431.24 |
| [NanoTouche2020](NanoTouche2020.md) | controversial question to argument passage | 49 | 5,745 | 932 | 0.7072 | 1.0000 | 43.43 | 2,142.56 |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoBEIR-en |
| Backing dataset | NanoBEIR-en |
| Hugging Face dataset | [hakari-bench/NanoBEIR-en](https://huggingface.co/datasets/hakari-bench/NanoBEIR-en) |
| Language | en |
| Category | natural language |
| Subtasks | 13 |
| Total queries | 649 |
| Split-local documents | 56,723 |
| Positive qrels | 4,696 |
| Average positives / query | 7.24 |
| Queries with multiple positives | 343 |
| Query-weighted BM25 nDCG@10 | 0.5533 |
| Query-weighted BM25 hit@10 | 0.8182 |
| Mean query length | 147.53 chars, weighted by query count |
| Mean document length | 903.41 chars, weighted by split-local document count |

### Public Sources

- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663); 2021; DOI: `10.48550/arXiv.2104.08663`.
- [NanoBEIR: Smaller BEIR dataset subsets](https://huggingface.co/collections/zeta-alpha-ai/nanobeir); 2024.
- [Retrieval of the Best Counterargument without Prior Topic Knowledge](https://aclanthology.org/P18-1023/); 2018; DOI: `10.18653/v1/P18-1023`.
- [CLIMATE-FEVER: A Dataset for Verification of Real-World Climate Claims](https://arxiv.org/abs/2012.00614); 2020; DOI: `10.48550/arXiv.2012.00614`.
- [DBpedia-Entity v2: A Test Collection for Entity Search](https://doi.org/10.1145/3077136.3080751); 2017; DOI: `10.1145/3077136.3080751`.
- [FEVER: a Large-scale Dataset for Fact Extraction and VERification](https://arxiv.org/abs/1803.05355); 2018; DOI: `10.18653/v1/N18-1074`.
- [HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering](https://arxiv.org/abs/1809.09600); 2018; DOI: `10.18653/v1/D18-1259`.
- [MS MARCO: A Human Generated MAchine Reading COmprehension Dataset](https://arxiv.org/abs/1611.09268); 2016.
- [Natural Questions: A Benchmark for Question Answering Research](https://aclanthology.org/Q19-1026/); 2019; DOI: `10.1162/tacl_a_00276`.
- [SPECTER: Document-level Representation Learning using Citation-informed Transformers](https://arxiv.org/abs/2004.07180); 2020.
- [Fact or Fiction: Verifying Scientific Claims](https://arxiv.org/abs/2004.14974); 2020.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-en](https://huggingface.co/datasets/hakari-bench/NanoBEIR-en)
- NanoBEIR collection: [zeta-alpha-ai/nanobeir](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | https://arxiv.org/abs/2104.08663 |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | https://huggingface.co/collections/zeta-alpha-ai/nanobeir |
| Retrieval of the Best Counterargument without Prior Topic Knowledge | 2018 | source task paper | https://aclanthology.org/P18-1023/ |
| CLIMATE-FEVER: A Dataset for Verification of Real-World Climate Claims | 2020 | source task paper | https://arxiv.org/abs/2012.00614 |
| DBpedia-Entity v2: A Test Collection for Entity Search | 2017 | source task paper | https://doi.org/10.1145/3077136.3080751 |
| FEVER: a Large-scale Dataset for Fact Extraction and VERification | 2018 | source task paper | https://arxiv.org/abs/1803.05355 |
| HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering | 2018 | source task paper | https://arxiv.org/abs/1809.09600 |
| MS MARCO: A Human Generated MAchine Reading COmprehension Dataset | 2016 | source task paper | https://arxiv.org/abs/1611.09268 |
| Natural Questions: A Benchmark for Question Answering Research | 2019 | source task paper | https://aclanthology.org/Q19-1026/ |
| SPECTER: Document-level Representation Learning using Citation-informed Transformers | 2020 | source task paper | https://arxiv.org/abs/2004.07180 |
| Fact or Fiction: Verifying Scientific Claims | 2020 | source task paper | https://arxiv.org/abs/2004.14974 |

## Machine-Readable Metadata

<!-- benchmark-task-group-metadata:v1 -->

```yaml
benchmark_task_group_metadata:
  schema_version: 1
  document_status: reviewed_manual
  nano_set: NanoBEIR-en
  backing_dataset: NanoBEIR-en
  dataset_id: hakari-bench/NanoBEIR-en
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoBEIR-en/index.md
  source_research:
    primary_source_type: benchmark_paper_and_dataset_collection
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    tasks: 13
    queries: 649
    split_local_documents: 56723
    positive_qrels: 4696
  positives_per_query:
    average: 7.2357473035439135
    min: 1
    median: 1.0
    max: 100
    multi_positive_tasks: 8
    multi_positive_queries: 343
  text_stats_chars:
    query_mean_weighted_by_queries: 147.5315870246533
    document_mean_weighted_by_documents: 903.4117960579307
  bm25:
    ndcg_at_10_query_weighted: 0.5532781202953775
    hit_at_10_query_weighted: 0.8181818181818182
    source: dataset_bm25_column
    strongest_task_by_ndcg_at_10: NanoHotpotQA
    weakest_task_by_ndcg_at_10: NanoClimateFEVER
  tasks:
    - name: NanoArguAna
      path: docs/benchmark_tasks/NanoBEIR-en/NanoArguAna.md
      retrieval_focus: argument_to_counterargument
      queries: 50
      documents: 3635
      positive_qrels: 50
      bm25_ndcg_at_10: 0.4462
      bm25_hit_at_10: 0.74
    - name: NanoClimateFEVER
      path: docs/benchmark_tasks/NanoBEIR-en/NanoClimateFEVER.md
      retrieval_focus: climate_claim_to_evidence
      queries: 50
      documents: 3408
      positive_qrels: 148
      bm25_ndcg_at_10: 0.3288755905
      bm25_hit_at_10: 0.74
    - name: NanoDBPedia
      path: docs/benchmark_tasks/NanoBEIR-en/NanoDBPedia.md
      retrieval_focus: entity_query_to_dbpedia_document
      queries: 50
      documents: 6045
      positive_qrels: 1158
      bm25_ndcg_at_10: 0.5619
      bm25_hit_at_10: 0.92
    - name: NanoFEVER
      path: docs/benchmark_tasks/NanoBEIR-en/NanoFEVER.md
      retrieval_focus: factual_claim_to_wikipedia_evidence
      queries: 50
      documents: 4996
      positive_qrels: 57
      bm25_ndcg_at_10: 0.8141
      bm25_hit_at_10: 0.94
    - name: NanoFiQA2018
      path: docs/benchmark_tasks/NanoBEIR-en/NanoFiQA2018.md
      retrieval_focus: finance_question_to_answer_passage
      queries: 50
      documents: 4598
      positive_qrels: 123
      bm25_ndcg_at_10: 0.3583
      bm25_hit_at_10: 0.64
    - name: NanoHotpotQA
      path: docs/benchmark_tasks/NanoBEIR-en/NanoHotpotQA.md
      retrieval_focus: multihop_question_to_wikipedia_evidence
      queries: 50
      documents: 5090
      positive_qrels: 100
      bm25_ndcg_at_10: 0.8175905937
      bm25_hit_at_10: 1.0
    - name: NanoMSMARCO
      path: docs/benchmark_tasks/NanoBEIR-en/NanoMSMARCO.md
      retrieval_focus: web_question_to_passage
      queries: 50
      documents: 5043
      positive_qrels: 50
      bm25_ndcg_at_10: 0.489
      bm25_hit_at_10: 0.74
    - name: NanoNFCorpus
      path: docs/benchmark_tasks/NanoBEIR-en/NanoNFCorpus.md
      retrieval_focus: health_topic_to_medical_evidence
      queries: 50
      documents: 2953
      positive_qrels: 1651
      bm25_ndcg_at_10: 0.362
      bm25_hit_at_10: 0.66
    - name: NanoNQ
      path: docs/benchmark_tasks/NanoBEIR-en/NanoNQ.md
      retrieval_focus: natural_question_to_wikipedia_evidence
      queries: 50
      documents: 5035
      positive_qrels: 57
      bm25_ndcg_at_10: 0.4708
      bm25_hit_at_10: 0.68
    - name: NanoQuoraRetrieval
      path: docs/benchmark_tasks/NanoBEIR-en/NanoQuoraRetrieval.md
      retrieval_focus: question_to_duplicate_question
      queries: 50
      documents: 5046
      positive_qrels: 70
      bm25_ndcg_at_10: 0.7864
      bm25_hit_at_10: 0.94
    - name: NanoSCIDOCS
      path: docs/benchmark_tasks/NanoBEIR-en/NanoSCIDOCS.md
      retrieval_focus: paper_title_to_related_scientific_document
      queries: 50
      documents: 2210
      positive_qrels: 244
      bm25_ndcg_at_10: 0.336
      bm25_hit_at_10: 0.78
    - name: NanoSciFact
      path: docs/benchmark_tasks/NanoBEIR-en/NanoSciFact.md
      retrieval_focus: scientific_claim_to_evidence_abstract
      queries: 50
      documents: 2919
      positive_qrels: 56
      bm25_ndcg_at_10: 0.7174
      bm25_hit_at_10: 0.86
    - name: NanoTouche2020
      path: docs/benchmark_tasks/NanoBEIR-en/NanoTouche2020.md
      retrieval_focus: controversial_question_to_argument_passage
      queries: 49
      documents: 5745
      positive_qrels: 932
      bm25_ndcg_at_10: 0.7072
      bm25_hit_at_10: 1.0
  learning:
    leakage_note: exclude NanoBEIR-en evaluation queries, qrels, and positive documents; audit BEIR and source-task split overlap before training on public source data
    useful_training_data:
      - non-overlapping BEIR-style retrieval training pairs
      - MS MARCO and Natural Questions passage retrieval train data
      - FEVER, Climate-FEVER, and SciFact claim-evidence pairs
      - finance, medical, and scientific document retrieval data
      - duplicate-question and paraphrase retrieval pairs
      - argument-counterargument retrieval pairs
      - entity search and disambiguation examples
    synthetic_data:
      document_generation: source-style English passages, entity descriptions, evidence abstracts, finance or medical documents, and argument passages
      question_generation: task-specific English claims, questions, duplicate-question paraphrases, entity queries, and counterargument prompts
      answerability: positives must satisfy the source task's relevance relation, not only topical overlap
    multi_positive_training: multi_positive_objective
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoBEIR-en
    source_urls:
      - label: BEIR arXiv
        url: https://arxiv.org/abs/2104.08663
      - label: NanoBEIR Hugging Face collection
        url: https://huggingface.co/collections/zeta-alpha-ai/nanobeir
  references:
    - title: "BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models"
      url: https://arxiv.org/abs/2104.08663
      year: 2021
      doi: 10.48550/arXiv.2104.08663
      is_paper: true
      source_confidence: definitive_paper_link
    - title: "NanoBEIR: Smaller BEIR dataset subsets"
      url: https://huggingface.co/collections/zeta-alpha-ai/nanobeir
      year: 2024
      is_paper: false
      source_confidence: probably_correct
```
