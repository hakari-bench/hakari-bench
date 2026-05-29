# NanoRTEB / NanoCUREv1

## Overview

`NanoRTEB / NanoCUREv1` retrieves English clinical and biomedical passages for
clinician-oriented medical questions from CUREv1.

## Details

### What the Original Data Measures

[CURE: A Dataset for Clinical Understanding & Retrieval
Evaluation](https://arxiv.org/abs/2412.06954) describes a clinical retrieval
benchmark with expert-written queries spanning 10 medical domains, including a
monolingual English condition and cross-lingual French/Spanish-to-English
conditions. The goal is point-of-care passage retrieval for healthcare
providers.

The [CUREv1 dataset card](https://huggingface.co/datasets/clinia/CUREv1)
publishes the dataset used by MTEB/RTEB. This Nano split uses the English
subset: short clinical questions retrieve relevant biomedical passage snippets.

### Observed Data Profile

The split has 182 queries, 10,000 documents, and 5,163 positive qrel rows.
Queries average 77.16 characters and documents average 603.96 characters. It is
strongly multi-positive: the average is 28.37 positives per query, and 171
queries have more than one positive.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.4709 and hit@10 = 0.9451. It ranks 104 queries at rank 1 and finds a positive
in the top 10 for 172 queries.

BM25 has high hit@10 because many clinical questions contain specialized terms
that also appear in relevant passages. nDCG@10 is lower because many positives
exist per query and ranking the best biomedical evidence first remains hard.

### Training Data That May Help

Useful training data includes clinical passage retrieval, PubMed-style evidence
retrieval, medical QA with gold evidence, and hard negatives from the same
specialty or condition.

### Synthetic Data Guidance

Generate clinician-style questions from non-evaluation biomedical passages.
Keep multiple relevant passages per query when evidence is distributed across
studies. Hard negatives should share diagnoses, procedures, or anatomical terms
but answer a different clinical relation.

## Example Data

| Query | Positive document |
| --- | --- |
| What are self/cutting or self-drilling screws? (46 chars) | The Use of MMF Screws: Surgical Technique, Indications, Contraindications, and Common Problems in Review of the Literature Self-cutting or self-drilling screws have a drill-shaped point to penetrate through the bone with more ... [truncated 225 chars](231 chars) |
| Where is the bad split in sagittal split osteotomies of the mandible usually located during orthognathic surgery? (113 chars) | Dal Pont vs Hunsuck: Which Technique Can Lead to a Lower Incidence of Bad Split during Bilateral Sagittal Split Osteotomy? A Triple-blind Randomized Clinical Trial Older age is definitely correlated to a higher risk of bad sp ... [truncated 225 chars](1064 chars) |
| Which are the advantages of endoscopic approach to treat massive arterial epistaxis? (84 chars) | Success Rate of Endoscopic Sphenopalatine Artery Ligation for the Management of Refractory Posterior Epistaxis Patients in a Tertiary Care Hospital: A Descriptive Cross-sectional Study The findings of the study conclude that ... [truncated 225 chars](613 chars) |
| How do fixed orthodontic appliances contribute to the development of white spot lesions? (88 chars) | In-vivo durability of a fluoride-releasing sealant (OpalSeal) for protection against white-spot lesion formation in orthodontic patients The results of this study provide some evidence on the abatement characteristics of the ... [truncated 225 chars](1370 chars) |
| What is the most frequent type of dental injury when anterior and buccal teeth are associated with facial fractures? (116 chars) | Traumatic Dental Injury—An Enigma for Adolescents: A Series of Case Reports Coronal fractures of permanent dentition are the most frequent type of dental injury. Fractured anterior teeth are usually treated with conventional ... [truncated 225 chars](733 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoRTEB |
| Backing dataset | NanoRTEB |
| Task / split | NanoCUREv1 |
| Hugging Face dataset | [hakari-bench/NanoRTEB](https://huggingface.co/datasets/hakari-bench/NanoRTEB) |
| Source dataset | [clinia/CUREv1](https://huggingface.co/datasets/clinia/CUREv1) |
| Language | en |
| Category | natural_language |
| Queries | 182 |
| Documents | 10,000 |
| Positive qrels | 5,163 |
| Positives per query | avg 28.37 / min 1 / median 20 / max 100 |
| Multi-positive queries | 171 |
| BM25 nDCG@10 | 0.5102 |
| BM25 hit@10 | 0.9835 |
| BM25 Recall@100 | 0.5326 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.5479 |
| Dense hit@10 | 0.9615 |
| Dense Recall@100 | 0.5838 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.5688 |
| Reranking hybrid hit@10 | 0.9890 |
| Reranking hybrid Recall@100 | 0.6122 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 1 |
| Query length avg chars | 77.16 |
| Document length avg chars | 603.96 |

### Public Sources

- [CURE: A Dataset for Clinical Understanding & Retrieval Evaluation](https://arxiv.org/abs/2412.06954), task paper.
- [CURE ACM proceedings record](https://doi.org/10.1145/3711896.3737435), proceedings DOI.
- [clinia/CUREv1](https://huggingface.co/datasets/clinia/CUREv1), source dataset card.
- [Introducing RTEB: A New Standard for Retrieval Evaluation](https://huggingface.co/blog/rteb), RTEB benchmark announcement.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoRTEB](https://huggingface.co/datasets/hakari-bench/NanoRTEB)
- Source task dataset: [clinia/CUREv1](https://huggingface.co/datasets/clinia/CUREv1)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| CURE: A Dataset for Clinical Understanding & Retrieval Evaluation | 2024 | task paper | https://arxiv.org/abs/2412.06954 |
| CURE ACM proceedings record | 2025 | proceedings record | https://doi.org/10.1145/3711896.3737435 |
| clinia/CUREv1 | 2025 | dataset card | https://huggingface.co/datasets/clinia/CUREv1 |
| Introducing RTEB: A New Standard for Retrieval Evaluation | 2025 | benchmark article | https://huggingface.co/blog/rteb |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoRTEB
  backing_dataset: NanoRTEB
  dataset_id: hakari-bench/NanoRTEB
  task_name: NanoCUREv1
  split_name: NanoCUREv1
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoRTEB/NanoCUREv1.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 182
    documents: 10000
    positive_qrels: 5163
  positives_per_query:
    average: 28.3681318681
    min: 1
    median: 20.0
    max: 100
    multi_positive_queries: 171
    multi_positive_query_percent: 93.956043956
  text_stats_chars:
    query_mean: 77.16
    document_mean: 603.96
  bm25:
    ndcg_at_10: 0.5101559862560149
    hit_at_10: 0.9835164835164835
    source: dataset_candidate_subset
  example_count: 5
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.5101559863
      hit_at_10: 0.9835164835
      recall_at_100: 0.5326360643
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 182
      query_coverage: 1.0
      relevant_coverage_at_100: 0.5326360643
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.5479419128
      hit_at_10: 0.9615384615
      recall_at_100: 0.5837691265
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 182
      query_coverage: 1.0
      relevant_coverage_at_100: 0.5837691265
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.5688129717
      hit_at_10: 0.989010989
      recall_at_100: 0.6122409452
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.005495
      query_count: 182
      query_coverage: 1.0
      relevant_coverage_at_100: 0.6122409452
      safeguard_positive_rows: 1
      rows_with_101_candidates: 1
```
