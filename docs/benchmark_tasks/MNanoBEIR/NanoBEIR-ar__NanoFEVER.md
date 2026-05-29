# MNanoBEIR / NanoBEIR-ar / NanoFEVER

## Overview

FEVER is a fact verification benchmark where claims are checked against
Wikipedia evidence. `NanoBEIR-ar__NanoFEVER` is the Arabic MNanoBEIR version:
each query is an Arabic claim, and the system must retrieve Arabic translated
Wikipedia passages that contain the evidence needed to support or refute it.
The task tests claim-to-evidence retrieval for short factual statements.

## Details

### What the Original Data Measures

[FEVER: a large-scale dataset for Fact Extraction and
VERification](https://arxiv.org/abs/1803.05355) introduces a dataset of
185,445 claims generated from Wikipedia and verified as supported, refuted, or
not enough information. For supported and refuted claims, annotators recorded
the evidence sentences needed for the judgment. The paper highlights evidence
retrieval as a central challenge: claims may require multiple evidence
sentences or more than one Wikipedia page.

[BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information
Retrieval Models](https://arxiv.org/abs/2104.08663) adapts FEVER into an
information retrieval task: the claim is the query, and the retriever must
surface evidence from a pre-processed Wikipedia corpus. [MMTEB: Massive
Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595)
provides the multilingual benchmark context for this Arabic Nano split. The
Arabic task keeps the FEVER evidence-retrieval objective while changing the
language surface form through translation.

### Observed Data Profile

The sampled Arabic Nano task has 50 queries, 4,996 documents, and 57 positive
qrel rows. Most queries have one positive, but 6 of 50 have multiple positives;
the average is 1.14 positives per query, with a maximum of 3. The average query
length is 40.14 characters, and the average document length is 1,039.03
characters.

The inspected queries are short factual claims: a rank being land-only, a
person's death date, whether Joseph Merrick was the subject of a historical
play, whether Betsy Hodges was ever a candidate, and Jeb Bush's mother. Positive
documents are translated Wikipedia passages, usually entity biographies or
entity descriptions. The task is often close to entity verification: retrieve
the page that contains the decisive fact.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.6670 and hit@10 = 0.8200. BM25 ranks a positive first for 28 of 50 queries,
and the median first-positive rank is 1. Every query has a positive within the
top 100.

BM25 performs well because many claims include the entity name and the positive
document is the corresponding entity page. The remaining difficulty is factual
specificity. A rank claim must retrieve the page about the rank, not a generic
military page; a date claim must retrieve the biography where the date appears;
and a negated claim may still have evidence on a page that contradicts the
query wording. Arabic translation and transliterated names can also reduce exact
token overlap.

### Training Data That May Help

Useful training data includes non-overlapping FEVER claim-evidence pairs,
Wikipedia claim verification data, entity-centric factual retrieval data, and
Arabic or multilingual fact-checking retrieval pairs. Because the Nano task is
mostly single-positive, standard claim-to-document contrastive training is
appropriate, with some multi-positive examples retained for claims requiring
several evidence pages.

Training should exclude FEVER dev/test examples, BEIR-derived evaluation
records, and translated NanoBEIR examples that may overlap with these claims or
evidence passages.

### Synthetic Data Guidance

For document-to-query generation, start from non-evaluation Wikipedia passages
and generate Arabic factual claims whose support or refutation is contained in
the passage. Include claims about dates, occupations, family relations, titles,
rank definitions, offices, and works.

For joint generation, create Arabic Wikipedia-style entity passages and claims
that are either supported or contradicted by a passage. Avoid creating only
keyword-equivalent pairs; the claim should require checking a factual relation.

## Example Data

| Query | Positive document |
| --- | --- |
| كان كيث غودشو يعرف فرقة غريتفول ديد (35 chars) | الغراتفول ديد كانت فرقة روك أمريكية تشكلت في عام 1965 في بالو ألتو، كاليفورنيا. كانت الفرقة تتكون من خمسة إلى سبعة أعضاء، وكانت معروفة بأسلوبها الفريد والمتنوع الذي جمع بين عناصر الروك، والروحي، والموسيقى التجريبية، والجاز ال ... [truncated 225 chars](2591 chars) |
| تارك ميثا كا أولتا تشما هو مسلسل كوميدي (39 chars) | تارك ميثا كا أولتا تشاشما (بالإنجليزية: تارك ميثا 'س مختلف المنظور) هو أطول مسلسل كوميدي في الهند، وهو من إنتاج شركة نيلا تيلي فيلمز برايفيت ليميتد. بدأ بثه في 28 يوليو 2008. يعرض من الأحد إلى الجمعة في الساعة 8:30 مساءً، مع ... [truncated 225 chars](532 chars) |
| تم تصنيع طائرات سرية ومتقدمة تكنولوجياً في بيربانك، كاليفورنيا. (63 chars) | بوربانك هي مدينة تقع في مقاطعة لوس أنجلوس في جنوب كاليفورنيا، الولايات المتحدة الأمريكية، على بعد 12 ميلاً شمال غرب وسط مدينة لوس أنجلوس. بلغ عدد سكانها في تعداد عام 2010 حوالي 103,340 نسمة. المعروفة باسم عاصمة الإعلام العالم ... [truncated 225 chars](1221 chars) |
| نيرو هو شخص (11 chars) | يُطلق على مصطلح سلالة جوليو كلوديوس على أول خمسة إمبراطور رومانيين: أوغسطس، تيبيريوس، كاليجولا، كلوديوس، ونيرو، أو العائلة التي ينتمون إليها. حكموا الإمبراطورية الرومانية منذ تأسيسها تحت حكم أوغسطس في النصف الثاني من القرن ال ... [truncated 225 chars](1524 chars) |
| فيلم "سكرام 2" هو حصريًا فيلم ألماني (36 chars) | فيلم "صرخة 2" هو فيلم رعب أمريكي صدر عام 1997، إخراج ويس كرافن وكتابة كيفن ويليامسون. بطولة ديفيد أركيت، نيف كامبل، كورتني كوكس، سارة ميشيل غيلار، جيمي كينيدي، لورى ميتكالف، جيري أوكونيل، جادا بينكيت، وليف شريبير. صدر الفيلم ... [truncated 225 chars](2047 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-ar |
| Task / split | NanoFEVER |
| Hugging Face dataset | [hakari-bench/NanoBEIR-ar](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ar) |
| Language | ar |
| Category | natural_language |
| Queries | 50 |
| Documents | 4,996 |
| Positive qrels | 57 |
| Avg positives / query | 1.14 |
| Positives per query (min / median / max) | 1 / 1.00 / 3 |
| Queries with multiple positives | 6 (12.0%) |
| BM25 nDCG@10 | 0.6665 |
| BM25 hit@10 | 0.8000 |
| BM25 Recall@100 | 0.9298 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.8243 |
| Dense hit@10 | 0.9600 |
| Dense Recall@100 | 0.9825 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.7767 |
| Reranking hybrid hit@10 | 0.9200 |
| Reranking hybrid Recall@100 | 0.9825 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 1 |
| Query length avg chars | 40.14 |
| Document length avg chars | 1,039.03 |

### Public Sources

- [FEVER: a large-scale dataset for Fact Extraction and VERification](https://arxiv.org/abs/1803.05355); 2018; James Thorne, Andreas Vlachos, Christos Christodoulopoulos, Arpit Mittal; DOI: `10.18653/v1/N18-1074`.
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663); 2021; Nandan Thakur, Nils Reimers, Andreas Rueckle, Abhishek Srivastava, Iryna Gurevych; DOI: `10.48550/arXiv.2104.08663`.
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595); 2025; Kenneth Enevoldsen, Isaac Chung, Imene Kerboua, Marton Kardos, Ashwin Mathur, and others; DOI: `10.48550/arXiv.2502.13595`.
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-ar](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ar)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| FEVER: a large-scale dataset for Fact Extraction and VERification | 2018 | task paper | https://arxiv.org/abs/1803.05355 |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | https://arxiv.org/abs/2104.08663 |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | https://arxiv.org/abs/2502.13595 |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | https://huggingface.co/collections/zeta-alpha-ai/nanobeir |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: MNanoBEIR
  backing_dataset: NanoBEIR-ar
  dataset_id: hakari-bench/NanoBEIR-ar
  task_name: NanoFEVER
  split_name: NanoFEVER
  language: ar
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-ar__NanoFEVER.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 50
    documents: 4996
    positive_qrels: 57
  positives_per_query:
    average: 1.14
    min: 1
    median: 1.0
    max: 3
    multi_positive_queries: 6
    multi_positive_query_percent: 12.0
  text_stats_chars:
    query_mean: 40.14
    document_mean: 1039.031825
  bm25:
    ndcg_at_10: 0.6665110333080634
    hit_at_10: 0.8
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: MNanoBEIR Arabic NanoBEIR task split from hakari-bench/NanoBEIR-ar
    train_eval_overlap_audit: not_audited
    leakage_note: prefer excluding FEVER, BEIR, or NanoBEIR records likely to overlap
      with these evaluation claims or evidence passages
    useful_training_data:
    - non-overlapping FEVER claim-evidence pairs
    - Wikipedia claim verification retrieval data
    - Arabic or multilingual fact-checking datasets
    - entity-centric factual retrieval pairs
    synthetic_data:
      document_generation: Arabic Wikipedia-style entity and event passages containing
        factual relations
      question_generation: Arabic factual claims about dates, offices, ranks, biographies,
        works, and family relations
      answerability: positives should contain evidence for verifying the claim, not
        just the same entity name
    multi_positive_training: optional_multi_positive_objective
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoBEIR-ar
    source_urls:
    - label: FEVER paper
      url: https://arxiv.org/abs/1803.05355
    - label: BEIR paper
      url: https://arxiv.org/abs/2104.08663
    - label: MMTEB paper
      url: https://arxiv.org/abs/2502.13595
    - label: Zeta Alpha NanoBEIR collection
      url: https://huggingface.co/collections/zeta-alpha-ai/nanobeir
    source_notes:
    - Arabic task is a multilingual NanoBEIR adaptation of the original English BEIR
      task
  references:
  - title: 'FEVER: a large-scale dataset for Fact Extraction and VERification'
    url: https://arxiv.org/abs/1803.05355
    year: 2018
    doi: 10.18653/v1/N18-1074
    is_paper: true
    source_confidence: definitive_paper_link
  - title: 'BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information
      Retrieval Models'
    url: https://arxiv.org/abs/2104.08663
    year: 2021
    doi: 10.48550/arXiv.2104.08663
    is_paper: true
    source_confidence: benchmark_context_paper
  - title: 'MMTEB: Massive Multilingual Text Embedding Benchmark'
    url: https://arxiv.org/abs/2502.13595
    year: 2025
    doi: 10.48550/arXiv.2502.13595
    is_paper: true
    source_confidence: benchmark_context_paper
  - title: 'NanoBEIR: Smaller BEIR dataset subsets'
    url: https://huggingface.co/collections/zeta-alpha-ai/nanobeir
    year: 2024
    doi: null
    is_paper: false
    source_confidence: dataset_collection
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.6665110333
      hit_at_10: 0.8
      recall_at_100: 0.9298245614
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9298245614
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.8243489048
      hit_at_10: 0.96
      recall_at_100: 0.9824561404
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9824561404
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.7766510421
      hit_at_10: 0.92
      recall_at_100: 0.9824561404
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.02
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9824561404
      safeguard_positive_rows: 1
      rows_with_101_candidates: 1
```
