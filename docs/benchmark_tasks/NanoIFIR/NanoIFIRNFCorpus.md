# NanoIFIR / NanoIFIRNFCorpus

## Overview

`NanoIFIRNFCorpus` is an instruction-following medical and nutrition literature
retrieval task. Queries are layperson-style health and nutrition topics, and
documents are medical research article titles and abstracts. The retriever must
find scientific literature relevant to the health question.

## Details

### What the Original Data Measures

[IFIR](https://arxiv.org/abs/2503.04644) uses NFCorpus in the scientific
literature/health-related expert retrieval setting, where the goal is to retrieve
relevant scientific literature tailored to a research or information need.

[NFCorpus: A Full-Text Learning to Rank Dataset for Medical Information Retrieval](https://www.cl.uni-heidelberg.de/~sokolov/pubs/boteva16full.pdf)
builds a medical learning-to-rank dataset from NutritionFacts.org pages written
in lay English and links them to PubMed/PMC research articles. The paper
emphasizes the lexical gap between lay health queries and medical literature,
and extracts graded relevance links from direct and indirect links between
NutritionFacts content and scientific articles.

### Observed Data Profile

The Nano split has 86 queries, 3,593 documents, and 242 positive qrels. Queries
average 37.84 characters, and documents average 1,589.51 characters. Queries
are short consumer-health titles such as `Eggs and Arterial Function` or
`Diabetes as a Disease of Fat Toxicity`. Documents are PubMed-like article
titles and abstracts.

Most queries have multiple positives: 64 of 86 queries have more than one
positive, with a maximum of 8.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.2833 and hit@10 = 0.5698. BM25 ranks a positive first for 21 queries. The task
is moderately hard because lay topic wording often differs from the biomedical
terms used in abstracts.

### Training Data That May Help

Useful training data includes non-overlapping NFCorpus training pairs, PubMed
abstract retrieval, consumer-health-to-biomedical query rewriting, and hard
negatives from the same MeSH/topic area. Training should preserve graded or
multi-positive relevance where available.

### Synthetic Data Guidance

Generate lay health questions or article-like titles, then pair them with
biomedical abstracts that use scientific terminology. Include lexical-gap cases
where positives use terms such as biomarkers, trial endpoints, exposure, or
mechanism rather than the consumer phrase.

## Example Data

| Query | Positive document |
| --- | --- |
| Who Should be Careful About Curcumin? (37 chars) | Curcumin as "Curecumin": from kitchen to clinic. Although turmeric (Curcuma longa; an Indian spice) has been described in Ayurveda, as a treatment for inflammatory diseases and is referred by different names in different cult ... [truncated 225 chars](1773 chars) |
| Preventing Ulcerative Colitis with Diet (39 chars) | A diet high in fat and meat but low in dietary fibre increases the genotoxic potential of 'faecal water'. To determine the effects of different diets on the genotoxicity of human faecal water, a diet rich in fat, meat and sug ... [truncated 225 chars](1604 chars) |
| Exploiting Autophagy to Live Longer (35 chars) | mTOR: from growth signal integration to cancer, diabetes and ageing Preface In all eukaryotes, the target of rapamycin (TOR) signaling pathway couples energy and nutrient abundance to the execution of cell growth and division ... [truncated 225 chars](694 chars) |
| Treating Multiple Sclerosis With the Swank MS Diet (50 chars) | Effect of low saturated fat diet in early and late cases of multiple sclerosis. 144 multiple sclerosis patients took a low-fat diet for 34 years. For each of three categories of neurological disability (minimum, moderate, sev ... [truncated 225 chars](683 chars) |
| Boosting the Bioavailability of Curcumin (40 chars) | Bioavailability of curcumin: problems and promises. Curcumin, a polyphenolic compound derived from dietary spice turmeric, possesses diverse pharmacologic effects including anti-inflammatory, antioxidant, antiproliferative an ... [truncated 225 chars](1418 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoIFIR |
| Backing dataset | NanoIFIR |
| Task / split | NanoIFIRNFCorpus |
| Hugging Face dataset | [hakari-bench/NanoIFIR](https://huggingface.co/datasets/hakari-bench/NanoIFIR) |
| Language | en |
| Category | natural_language |
| Queries | 86 |
| Documents | 3,593 |
| Positive qrels | 242 |
| Positives per query | avg 2.81 / min 1 / median 3.0 / max 8 |
| Multi-positive queries | 64 (74.42%) |
| BM25 nDCG@10 | 0.3338 |
| BM25 hit@10 | 0.6628 |
| BM25 Recall@100 | 0.6488 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.4580 |
| Dense hit@10 | 0.7326 |
| Dense Recall@100 | 0.8306 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.4108 |
| Reranking hybrid hit@10 | 0.7209 |
| Reranking hybrid Recall@100 | 0.7975 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 9 |
| Query length avg chars | 37.84 |
| Document length avg chars | 1,589.51 |

### Public Sources

- [IFIR: A Comprehensive Benchmark for Evaluating Instruction-Following in Expert-Domain Information Retrieval](https://arxiv.org/abs/2503.04644); 2025; Tingyu Song et al.
- [NFCorpus: A Full-Text Learning to Rank Dataset for Medical Information Retrieval](https://www.cl.uni-heidelberg.de/~sokolov/pubs/boteva16full.pdf); 2016; Vera Boteva et al.
- [NFCorpus project page](https://www.cl.uni-heidelberg.de/statnlpgroup/nfcorpus/).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoIFIR](https://huggingface.co/datasets/hakari-bench/NanoIFIR)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| IFIR: A Comprehensive Benchmark for Evaluating Instruction-Following in Expert-Domain Information Retrieval | 2025 | arXiv paper | https://arxiv.org/abs/2503.04644 |
| NFCorpus: A Full-Text Learning to Rank Dataset for Medical Information Retrieval | 2016 | ECIR paper | https://www.cl.uni-heidelberg.de/~sokolov/pubs/boteva16full.pdf |
| NFCorpus project page | 2016 | project page | https://www.cl.uni-heidelberg.de/statnlpgroup/nfcorpus/ |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoIFIR
  backing_dataset: NanoIFIR
  dataset_id: hakari-bench/NanoIFIR
  task_name: NanoIFIRNFCorpus
  split_name: NanoIFIRNFCorpus
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoIFIR/NanoIFIRNFCorpus.md
  source_research:
    primary_source_type: benchmark_paper_and_task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 86
    documents: 3593
    positive_qrels: 242
  positives_per_query:
    average: 2.813953488372093
    min: 1
    median: 3.0
    max: 8
    multi_positive_queries: 64
    multi_positive_query_percent: 74.4186046511628
  text_stats_chars:
    query_mean: 37.83720930232558
    document_mean: 1589.5082104091289
  bm25:
    ndcg_at_10: 0.3337680194125584
    hit_at_10: 0.6627906976744186
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: ifir_adapted
    train_eval_overlap_audit: not_audited
    leakage_note: exclude NanoIFIRNFCorpus queries, qrels, and positive PubMed/PMC
      abstracts
    useful_training_data:
    - non-overlapping NFCorpus train pairs
    - PubMed abstract retrieval pairs
    - consumer-health to biomedical query rewriting
    - same-topic biomedical hard negatives
    synthetic_data:
      document_generation: PubMed-style titles and abstracts about nutrition, disease
        risk, mechanisms, and trials
      question_generation: layperson health and nutrition titles with instruction
        context
      answerability: positives should scientifically address the lay health topic
    multi_positive_training: preserve_multiple_relevant_medical_abstracts
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoIFIR
    source_urls:
    - label: IFIR arXiv
      url: https://arxiv.org/abs/2503.04644
    - label: NFCorpus paper PDF
      url: https://www.cl.uni-heidelberg.de/~sokolov/pubs/boteva16full.pdf
    - label: NFCorpus project page
      url: https://www.cl.uni-heidelberg.de/statnlpgroup/nfcorpus/
    source_notes: []
  references:
  - title: 'NFCorpus: A Full-Text Learning to Rank Dataset for Medical Information
      Retrieval'
    url: https://www.cl.uni-heidelberg.de/~sokolov/pubs/boteva16full.pdf
    year: 2016
    doi: 10.1007/978-3-319-30671-1_58
    is_paper: true
    source_confidence: definitive_paper_link
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.3337680194
      hit_at_10: 0.6627906977
      recall_at_100: 0.6487603306
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 86
      query_coverage: 1.0
      relevant_coverage_at_100: 0.6487603306
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.4580487514
      hit_at_10: 0.7325581395
      recall_at_100: 0.8305785124
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 86
      query_coverage: 1.0
      relevant_coverage_at_100: 0.8305785124
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.4107738671
      hit_at_10: 0.7209302326
      recall_at_100: 0.7975206612
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.104651
      query_count: 86
      query_coverage: 1.0
      relevant_coverage_at_100: 0.7975206612
      safeguard_positive_rows: 9
      rows_with_101_candidates: 9
```
