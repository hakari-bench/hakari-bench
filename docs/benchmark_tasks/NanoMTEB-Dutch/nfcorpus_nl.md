# NanoMTEB-Dutch / nfcorpus_nl

## Overview

`nfcorpus_nl` is the Dutch NFCorpus retrieval task from BEIR-NL and MTEB-NL.
Queries are short consumer-health or nutrition topics, and documents are long
medical or biomedical article passages translated into Dutch. The task measures
whether a retriever can bridge lay health wording and technical medical
evidence.

## Details

### What the Original Data Measures

[NFCorpus: A Full-Text Learning to Rank Dataset for Medical Information Retrieval](https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf)
describes a medical learning-to-rank dataset built from NutritionFacts.org
topics linked to PubMed and PubMed Central research articles. The paper
emphasizes the gap between layperson health information needs and biomedical
terminology, with graded relevance signals from direct and indirect source
links.

[BEIR-NL](https://aclanthology.org/2025.bucc-1.5/) translates BEIR datasets into
Dutch and notes that translated query and passage text can introduce lexical
mismatch because translations are produced independently. This Dutch task should
therefore be read as translated medical retrieval, with occasional remaining
English or multilingual artifacts.

### Observed Data Profile

The Nano split has 199 queries, 3,593 documents, and 5,880 positive qrel rows.
It is strongly multi-positive: the average is 29.55 positives per query, the
median is 15, and the maximum is 100. Queries average only 18.51 characters,
often a short topic such as `rapamycine`, `bloemkool`, or `kookmethoden`.
Documents are long, averaging 1,743.72 characters, and often resemble translated
abstracts with technical biomedical terms.

The sample includes carcinogens in cooked meat, shellfish, rapamycin,
cauliflower, and cooking methods. Several query terms are very short or broad,
so relevance depends on a set of medically related documents rather than one
exact answer passage.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.3486
and hit@10 = 0.6432. This is a difficult lexical baseline despite the large
number of positives. Short lay queries often do not share many terms with
technical abstracts, and translated biomedical terminology can vary.

The multi-positive qrels mean hit@10 alone understates ranking quality: a model
must rank many useful medical documents near the top, not merely find one
related article. Dense models should benefit from medical synonymy and concept
matching.

### Training Data That May Help

Useful training data includes official NFCorpus training data if allowed,
non-overlapping health topic-to-article pairs, Dutch biomedical QA and evidence
retrieval data, and multilingual medical retrieval datasets with overlap
removed. Avoid training on the exact translated test queries, qrels, and corpus
passages used in this Nano split.

Training should preserve the multi-positive nature of the task. Pairwise
single-positive sampling can work, but listwise or multi-positive objectives are
better aligned with the benchmark.

### Synthetic Data Guidance

For document-to-query generation, use non-evaluation Dutch medical abstracts or
patient-facing health articles and generate short lay health topics or natural
queries. Generated queries should sometimes use everyday wording while the
documents retain technical terms.

For joint generation, create Dutch biomedical abstracts with measurements,
conditions, interventions, or nutrition exposures, then generate consumer-health
queries and multiple relevant documents. Include hard negatives from adjacent
conditions or similar compounds.

## Example Data

| Query | Positive document |
| --- | --- |
| bagels (6 chars) | Papaverzaadproducten en opiaten drugstesten – waar staan we nu? Zaden van de opiumpapaverplant worden legaal verkocht en veel geconsumeerd als voedsel. Door contaminatie tijdens de oogst kunnen de zaden morfine en andere opia ... [truncated 225 chars](1902 chars) |
| druiven (7 chars) | Een beslist prikkelend idee: de potentiële rol van plantaardige polyfenolen bij de behandeling van leeftijdsgebonden cognitieve stoornissen. Tegenwoordig lijden tientallen miljoenen ouderen wereldwijd aan dementie. Hoewel de ... [truncated 225 chars](1953 chars) |
| Dr. Walter Willett (18 chars) | Cocountolie voorspelt een gunstig lipidenprofiel bij premenopauzale vrouwen in de Filipijnen Cocountolie is een veelgebruikte eetbare olie in veel landen, en er is gemengd bewijs voor de effecten ervan op lipidenprofielen en ... [truncated 225 chars](1491 chars) |
| Chronische hoofdpijn en varkens parasieten (42 chars) | Klinische manifestaties, diagnose en behandeling van neurocysticercose. Neurocysticercose (NCC) is de meest voorkomende parasitaire ziekte van de hersenen. Moderne beeldvormende technieken, CT en MRI, hebben de diagnose en ka ... [truncated 225 chars](996 chars) |
| Inheemse Amerikanen (19 chars) | Westerse ziekten en hun ontstaan in relatie tot voeding. Veel van de meest voorkomende ziekten in economisch ontwikkelde gemeenschappen zijn kenmerkend voor de moderne Westerse cultuur. Er wordt bewijs gepresenteerd dat sugge ... [truncated 225 chars](504 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-Dutch |
| Backing dataset | NanoMTEB-Dutch |
| Task / split | nfcorpus_nl |
| Hugging Face dataset | [hakari-bench/NanoMTEB-Dutch](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Dutch) |
| Source dataset | [clips/beir-nl-nfcorpus](https://huggingface.co/datasets/clips/beir-nl-nfcorpus) |
| Language | multilingual |
| Category | natural_language |
| Queries | 199 |
| Documents | 3,593 |
| Positive qrels | 5,880 |
| Avg positives / query | 29.55 |
| Positives per query (min / median / max) | 1 / 15 / 100 |
| Queries with multiple positives | 181 (90.95%) |
| BM25 nDCG@10 | 0.2683 |
| BM25 hit@10 | 0.6181 |
| BM25 Recall@100 | 0.1371 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.2590 |
| Dense hit@10 | 0.6181 |
| Dense Recall@100 | 0.1757 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.2656 |
| Reranking hybrid hit@10 | 0.6231 |
| Reranking hybrid Recall@100 | 0.1815 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 37 |
| Query length avg chars | 18.51 |
| Document length avg chars | 1,743.72 |

### Public Sources

- [NFCorpus: A Full-Text Learning to Rank Dataset for Medical Information Retrieval](https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf), 2016.
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663), 2021.
- [BEIR-NL: Zero-shot Information Retrieval Benchmark for the Dutch Language](https://aclanthology.org/2025.bucc-1.5/), 2025.
- [clips/beir-nl-nfcorpus](https://huggingface.co/datasets/clips/beir-nl-nfcorpus), source dataset card.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMTEB-Dutch](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Dutch)
- Source dataset: [clips/beir-nl-nfcorpus](https://huggingface.co/datasets/clips/beir-nl-nfcorpus)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| NFCorpus: A Full-Text Learning to Rank Dataset for Medical Information Retrieval | 2016 | paper PDF | https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | arXiv paper | https://arxiv.org/abs/2104.08663 |
| BEIR-NL: Zero-shot Information Retrieval Benchmark for the Dutch Language | 2025 | ACL paper | https://aclanthology.org/2025.bucc-1.5/ |
| clips/beir-nl-nfcorpus |  | dataset card | https://huggingface.co/datasets/clips/beir-nl-nfcorpus |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMTEB-Dutch
  backing_dataset: NanoMTEB-Dutch
  dataset_id: hakari-bench/NanoMTEB-Dutch
  task_name: nfcorpus_nl
  split_name: nfcorpus_nl
  language: multilingual
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-Dutch/nfcorpus_nl.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    paper_url: https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf
    additional_source_urls:
    - https://arxiv.org/abs/2104.08663
    - https://aclanthology.org/2025.bucc-1.5/
    - https://huggingface.co/datasets/clips/beir-nl-nfcorpus
    no_paper_note: null
  counts:
    queries: 199
    documents: 3593
    positive_qrels: 5880
  positives_per_query:
    average: 29.547738693
    min: 1
    median: 15
    max: 100
    multi_positive_queries: 181
    multi_positive_query_percent: 90.954773869
  text_stats_chars:
    query_mean: 18.507537688
    document_mean: 1743.724464236
  bm25:
    ndcg_at_10: 0.26834309064618656
    hit_at_10: 0.6180904522613065
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: translated BEIR-NL NFCorpus test split from clips/beir-nl-nfcorpus
    train_eval_overlap_audit: not_audited
    leakage_note: Exclude translated NFCorpus test queries, qrels, and medical documents
      used by this Nano split.
    useful_training_data:
    - official NFCorpus training data with overlap removed
    - Dutch biomedical QA and evidence retrieval pairs
    - non-overlapping health topic to medical article pairs
    - multilingual medical retrieval data adapted to Dutch
    synthetic_data:
      document_generation: Dutch biomedical abstracts or patient-facing health passages
        with precise terminology.
      question_generation: Short lay health topics and questions answerable by technical
        medical passages.
      answerability: Queries should map to multiple medically relevant documents and
        include concept-level hard negatives.
    multi_positive_training: multi_positive_objective
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMTEB-Dutch
    source_urls:
    - label: NFCorpus paper PDF
      url: https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf
    - label: BEIR arXiv
      url: https://arxiv.org/abs/2104.08663
    - label: BEIR-NL ACL Anthology
      url: https://aclanthology.org/2025.bucc-1.5/
    - label: clips/beir-nl-nfcorpus
      url: https://huggingface.co/datasets/clips/beir-nl-nfcorpus
    source_notes: []
  references:
  - title: 'NFCorpus: A Full-Text Learning to Rank Dataset for Medical Information
      Retrieval'
    url: https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf
    year: 2016
    doi: null
    is_paper: true
    source_confidence: definitive_paper_link
  - title: 'BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information
      Retrieval Models'
    url: https://arxiv.org/abs/2104.08663
    year: 2021
    doi: 10.48550/arXiv.2104.08663
    is_paper: true
    source_confidence: definitive_paper_link
  - title: 'BEIR-NL: Zero-shot Information Retrieval Benchmark for the Dutch Language'
    url: https://aclanthology.org/2025.bucc-1.5/
    year: 2025
    doi: null
    is_paper: true
    source_confidence: definitive_paper_link
  - title: clips/beir-nl-nfcorpus
    url: https://huggingface.co/datasets/clips/beir-nl-nfcorpus
    year: null
    doi: null
    is_paper: false
    source_confidence: probably_correct
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.2683430906
      hit_at_10: 0.6180904523
      recall_at_100: 0.1370748299
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 199
      query_coverage: 1.0
      relevant_coverage_at_100: 0.1370748299
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.2590347446
      hit_at_10: 0.6180904523
      recall_at_100: 0.1756802721
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 199
      query_coverage: 1.0
      relevant_coverage_at_100: 0.1756802721
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.2656254982
      hit_at_10: 0.6231155779
      recall_at_100: 0.181462585
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.18593
      query_count: 199
      query_coverage: 1.0
      relevant_coverage_at_100: 0.181462585
      safeguard_positive_rows: 37
      rows_with_101_candidates: 37
```
