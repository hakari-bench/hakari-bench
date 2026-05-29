# NanoBEIR-en / NanoNFCorpus

## Overview

NFCorpus is a medical information retrieval dataset that links layperson health
topics from NutritionFacts.org to technical medical research documents, mostly
PubMed and PMC abstracts. `NanoNFCorpus` is the compact English NanoBEIR version
of this task. Queries are short health, nutrition, disease, drug, or food-topic
phrases, and relevant documents are biomedical abstracts that support or are
linked from the source health topic. The task tests domain transfer across a
large consumer-to-scientific vocabulary gap.

## Details

### What the Original Data Measures

[A Full-Text Learning to Rank Dataset for Medical Information
Retrieval](https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf)
introduces NFCorpus as a learning-to-rank dataset for medical information
retrieval. The paper explains that queries are extracted from NutritionFacts.org
content written in layperson English, while documents are research-article
titles and abstracts, mainly from PubMed and PMC. Relevance links come from
direct citations, indirect NutritionFacts links, and topic/tag relations, giving
the original corpus three relevance levels.

The official NFCorpus project page reports 3,244 natural-language queries,
169,756 automatically extracted relevance judgments, and 9,964 medical
documents. It also states that the data is split by query into train,
development, and test subsets. This source construction matters for retrieval
interpretation: the task is not asking for a clinical answer written in consumer
language. It asks whether a retriever can connect a simple health topic such as
`memory`, `pork`, or `Foods for Glaucoma` to technical biomedical abstracts that
may use epidemiological, nutritional, biochemical, or clinical-trial language.

[BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information
Retrieval Models](https://arxiv.org/abs/2104.08663) includes NFCorpus in its
Bio-Medical Information Retrieval group. BEIR reports NFCorpus as a title-bearing
dataset with three-level relevance, a small query set, many relevant documents
per query, and short keyword-like queries against much longer scientific
documents. The NanoBEIR page below uses the binary positive qrels exposed by the
Nano tables, but the original graded and link-derived nature of the dataset
should still guide interpretation.

### Observed Data Profile

The sampled Nano task has 50 queries, 2,953 documents, and 1,651 positive qrel
rows. Unlike many NanoBEIR tasks, this is strongly multi-positive: the average
query has 33.02 positive documents, the median has 23.5, and 47 of 50 queries
have more than one positive. This makes the task closer to topical biomedical
recall and ranking than to single-answer passage retrieval.

The queries are all `PLAIN-*` NFCorpus query IDs and are usually very short:
single food or drug terms such as `veal`, `pork`, `Mevacor`, `Zoloft`,
`thiamine`, and `memory`, plus NutritionFacts-style article titles such as
`What Do Meat Purge and Cola Have in Common?`, `Infectobesity: Adenovirus 36
and Childhood Obesity`, and `The Actual Benefit of Diet vs. Drugs`. The
documents are scientific abstracts with an average length of about 1,513
characters. They commonly begin with structured abstract markers such as
`BACKGROUND`, `OBJECTIVE`, `METHODS`, or `RESULTS`, and contain domain-specific
phrases, measurements, study designs, and epidemiological terminology.

This data profile creates two different retrieval requirements. For some queries,
the lexical anchor is explicit and useful: `Foods for Glaucoma` retrieves
abstracts about glaucoma and fruit/vegetable or supplement consumption. For many
others, the query is a broad topic label whose positive set comes from
NutritionFacts link structure rather than from direct word overlap. A relevant
document for `fava beans`, for example, can discuss L-arginine and metabolic
effects rather than repeating the food name. Models therefore need both exact
medical term matching and learned associations between consumer nutrition topics
and scientific evidence.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.3620
and hit@10 = 0.6600. This is much lower than on lexical BEIR tasks such as Quora
or some fact-checking splits, despite the many positives per query. Only 150 of
1,651 positive qrel rows appear in the top 10 across all queries, the median
positive rank among the forced top-100 candidate lists is 74, and only 22
positive rows are ranked first.

The BM25 behavior is uneven. It performs well when the query carries rare
scientific or disease vocabulary: `Infectobesity: Adenovirus 36 and Childhood
Obesity` has positives about Ad-36 and obesity at ranks 1, 2, and 3, and `Foods
for Glaucoma` has glaucoma abstracts at ranks 1, 2, and 3. It struggles when the
query is a short consumer label. `Mevacor`, `Zoloft`, `thiamine`, `veal`,
`mesquite`, and `poisonous plants` have positives only near the end of the
top-100 candidate list in the inspected Nano ranking. In those cases BM25 often
finds documents with generic food, disease, or health terms, but misses the
source-link relation that made an abstract relevant to the NutritionFacts topic.

Because the task has many positives per query, nDCG@10 is the primary signal.
Hit@10 can be satisfied by finding just one related abstract, but a good system
should rank many evidence documents for the same health topic. Training and
evaluation should therefore preserve multi-positive supervision rather than
collapsing each query to a single positive.

### Training Data That May Help

The official NFCorpus train split is the first source to inspect for supervised
medical retrieval training, subject to the benchmark rules for any leaderboard
use. Data likely to overlap with the Nano evaluation records, including upstream
development/test queries, qrels, or the same NutritionFacts-derived links, should
preferably be excluded from training.

Other helpful training sources include biomedical abstract retrieval pairs,
consumer-health-question to PubMed evidence pairs, medical evidence retrieval
from PubMed or PMC, BioASQ-style question-to-article supervision, and weakly
supervised citation/link data that maps lay health pages to scientific papers.
General paraphrase data is not enough by itself because the core challenge is
matching informal health topics to technical scientific evidence.

### Synthetic Data Guidance

For document-to-question generation, use non-evaluation PubMed or PMC abstracts
and generate short consumer-health topic queries, NutritionFacts-style titles,
and simple food/drug/disease phrases that are explicitly supported by the
abstract. The generated query should not merely repeat the abstract title; it
should express the layperson information need that a nutrition or health site
would use when linking to the paper.

For joint document-and-question generation, create realistic biomedical
abstracts with study population, intervention or exposure, outcome, and
measurement details, then pair them with broad consumer-facing topics. Synthetic
data should include multiple positives for the same topic and should preserve
medical terminology, dietary exposures, drug names, disease outcomes, and study
design language. Do not seed generation with Nano evaluation queries or positive
documents.

## Example Data

| Query | Positive document |
| --- | --- |
| Healthy Chocolate Milkshakes (28 chars) | Objective To study the relation between cherry intake and the risk of recurrent gout attacks among individuals with gout. Methods We conducted a case-crossover study to examine associations of a set of putative risk factors w ... [truncated 225 chars](1586 chars) |
| medical ethics (14 chars) | BACKGROUND: One of the major issues in controlling serum cholesterol through dietetic intervention appears to be the need to improve patient adherence. AIMS: To explore the many questions regarding barriers to, and motivators ... [truncated 225 chars](1831 chars) |
| fava beans (10 chars) | Over the past 20 years, growing interest in the biochemistry, nutrition, and pharmacology of L-arginine has led to extensive studies to explore its nutritional and therapeutic roles in treating and preventing human metabolic ... [truncated 225 chars](1240 chars) |
| What is Actually in Chicken Nuggets? (36 chars) | PURPOSE: To determine the contents of chicken nuggets from 2 national food chains. BACKGROUND: Chicken nuggets have become a major component of the American diet. We sought to determine the current composition of this highly ... [truncated 225 chars](714 chars) |
| saturated fat (13 chars) | Interest has increased in the possibility that maternal dietary intake during pregnancy might influence the development of allergic disorders in children. The present prospective study examined the association of maternal int ... [truncated 225 chars](2022 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoBEIR-en |
| Backing dataset | NanoBEIR-en |
| Task / split | NanoNFCorpus |
| Hugging Face dataset | [hakari-bench/NanoBEIR-en](https://huggingface.co/datasets/hakari-bench/NanoBEIR-en) |
| Language | en |
| Category | natural_language |
| Queries | 50 |
| Documents | 2,953 |
| Positive qrels | 1,651 |
| Avg positives / query | 33.02 |
| Positives per query (min / median / max) | 1 / 23.50 / 100 |
| Queries with multiple positives | 47 (94.0%) |
| BM25 nDCG@10 | 0.3060 |
| BM25 hit@10 | 0.6800 |
| BM25 Recall@100 | 0.1690 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.3135 |
| Dense hit@10 | 0.7200 |
| Dense Recall@100 | 0.2447 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.3178 |
| Reranking hybrid hit@10 | 0.6800 |
| Reranking hybrid Recall@100 | 0.2332 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 6 |
| Query length avg chars | 21.04 |
| Document length avg chars | 1,512.73 |

### Public Sources

- [A Full-Text Learning to Rank Dataset for Medical Information Retrieval](https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf); 2016; Vera Boteva, Demian Gholipour Ghalandari, Artem Sokolov, Stefan Riezler; DOI: `10.1007/978-3-319-30671-1_58`.
- [NFCorpus project page](https://www.cl.uni-heidelberg.de/statnlpgroup/nfcorpus/); official dataset page.
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663); 2021; Nandan Thakur, Nils Reimers, Andreas Rueckle, Abhishek Srivastava, Iryna Gurevych.
- [ir_datasets BEIR documentation](https://ir-datasets.com/beir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-en](https://huggingface.co/datasets/hakari-bench/NanoBEIR-en)
- Source dataset: [mteb/nfcorpus](https://huggingface.co/datasets/mteb/nfcorpus)
- Source dataset: [BeIR/nfcorpus](https://huggingface.co/datasets/BeIR/nfcorpus)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| A Full-Text Learning to Rank Dataset for Medical Information Retrieval | 2016 | paper | https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf |
| NFCorpus project page |  | dataset page | https://www.cl.uni-heidelberg.de/statnlpgroup/nfcorpus/ |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | https://arxiv.org/abs/2104.08663 |
| mteb/nfcorpus |  | dataset card | https://huggingface.co/datasets/mteb/nfcorpus |
| BeIR/nfcorpus |  | dataset card | https://huggingface.co/datasets/BeIR/nfcorpus |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoBEIR-en
  backing_dataset: NanoBEIR-en
  dataset_id: hakari-bench/NanoBEIR-en
  task_name: NanoNFCorpus
  split_name: NanoNFCorpus
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoBEIR-en/NanoNFCorpus.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 50
    documents: 2953
    positive_qrels: 1651
  positives_per_query:
    average: 33.02
    min: 1
    median: 23.5
    max: 100
    multi_positive_queries: 47
    multi_positive_query_percent: 94.0
  text_stats_chars:
    query_mean: 21.04
    document_mean: 1512.730105
  bm25:
    ndcg_at_10: 0.30601019251665673
    hit_at_10: 0.68
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: unknown
    train_eval_overlap_audit: not_audited
    leakage_note: prefer excluding upstream dev/test data, Nano evaluation records,
      and NutritionFacts/NFCorpus links likely to overlap with this task
    useful_training_data:
    - official non-overlapping NFCorpus train split
    - consumer-health-question to PubMed evidence pairs
    - biomedical abstract retrieval and citation-link supervision
    - BioASQ-style medical question-to-article retrieval data
    synthetic_data:
      document_generation: non-evaluation PubMed or PMC abstracts with biomedical
        study details
      question_generation: layperson health, nutrition, food, drug, or disease topics
        answerable from the abstract
      answerability: positives should be scientific evidence documents linked to the
        same health topic, not generic medical neighbors
    multi_positive_training: multi_positive_objective
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoBEIR-en
    source_urls:
    - label: NFCorpus project page
      url: https://www.cl.uni-heidelberg.de/statnlpgroup/nfcorpus/
    - label: mteb/nfcorpus
      url: https://huggingface.co/datasets/mteb/nfcorpus
    - label: BeIR/nfcorpus
      url: https://huggingface.co/datasets/BeIR/nfcorpus
    - label: Zeta Alpha NanoBEIR collection
      url: https://huggingface.co/collections/zeta-alpha-ai/nanobeir
    source_notes: []
  references:
  - title: A Full-Text Learning to Rank Dataset for Medical Information Retrieval
    url: https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf
    year: 2016
    doi: 10.1007/978-3-319-30671-1_58
    is_paper: true
    source_confidence: definitive_paper_link
  - title: NFCorpus project page
    url: https://www.cl.uni-heidelberg.de/statnlpgroup/nfcorpus/
    year: null
    doi: null
    is_paper: false
    source_confidence: definitive_dataset_page
  - title: 'BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information
      Retrieval Models'
    url: https://arxiv.org/abs/2104.08663
    year: 2021
    doi: 10.48550/arXiv.2104.08663
    is_paper: true
    source_confidence: definitive_paper_link
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.3060101925
      hit_at_10: 0.68
      recall_at_100: 0.1689884918
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.1689884918
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.3135207633
      hit_at_10: 0.72
      recall_at_100: 0.2447001817
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.2447001817
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.3177785244
      hit_at_10: 0.68
      recall_at_100: 0.2331920048
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.12
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.2331920048
      safeguard_positive_rows: 6
      rows_with_101_candidates: 6
```
