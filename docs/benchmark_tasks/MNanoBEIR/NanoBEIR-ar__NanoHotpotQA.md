# MNanoBEIR / NanoBEIR-ar / NanoHotpotQA

## Overview

HotpotQA is a multi-hop question answering benchmark built from Wikipedia.
`NanoBEIR-ar__NanoHotpotQA` is the Arabic MNanoBEIR version: each query is an
Arabic multi-hop question, and the system must retrieve Arabic translated
Wikipedia passages that form the supporting evidence. The task tests whether a
retriever can find all required evidence pages, not just a single obvious
entity page.

## Details

### What the Original Data Measures

[HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question
Answering](https://arxiv.org/abs/1809.09600) introduces a Wikipedia QA dataset
designed to require reasoning over multiple supporting documents. The paper
reports 113K question-answer pairs, includes sentence-level supporting facts,
and builds bridge questions from the Wikipedia hyperlink graph as well as
comparison questions over similar entities.

[BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information
Retrieval Models](https://arxiv.org/abs/2104.08663) includes HotpotQA as a
question-answering retrieval task in which the retriever must surface the
supporting Wikipedia evidence. [MMTEB: Massive Multilingual Text Embedding
Benchmark](https://arxiv.org/abs/2502.13595) provides the multilingual
benchmark context for this Arabic Nano split. The Arabic task preserves the
multi-hop evidence objective while presenting translated queries and passages.

### Observed Data Profile

The sampled Arabic Nano task has 50 queries, 5,090 documents, and 100 positive
qrel rows. Every query has exactly two positives, so complete retrieval means
finding a pair of supporting passages. The average query length is 72.76
characters, and the average document length is 410.03 characters.

The inspected queries include comparison questions and bridge questions:
which magazine is published in more countries, a question that starts from an
actress in "Friday Night Lights" and asks for a film director, a crime-family
question involving a brother-in-law and a witness, and questions involving
translation or film credits. Positive documents are short Wikipedia-style
entity descriptions. Often one positive identifies the intermediate entity,
while another supplies the requested attribute.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.6505 and hit@10 = 0.9200. BM25 ranks a positive first for 34 of 50 queries,
and the median first-positive rank is 1. Every query has a positive within the
top 100.

The main difficulty is completeness rather than finding any relevant page.
Because each query has two positives, a retriever that finds only the most
lexically obvious entity can still miss the evidence set. Arabic translation
adds another layer: names, titles, and relations can appear partly translated
and partly transliterated. Strong models should identify both entities or the
bridge relation and rank both supporting pages high.

### Training Data That May Help

Useful training data includes non-overlapping HotpotQA training examples with
supporting facts, multi-hop QA retrieval datasets, Wikipedia hyperlink graph
retrieval pairs, and Arabic or multilingual question-to-multiple-document
supervision. Single-hop QA helps with entity matching but does not fully teach
complete evidence-set retrieval.

Training should exclude HotpotQA dev/test, BEIR, NanoBEIR, or translated
records likely to overlap with the evaluation questions or supporting pages.
Multi-positive training is especially important because every query has two
positives.

### Synthetic Data Guidance

For document-to-query generation, start from pairs of non-evaluation
Wikipedia-style passages connected by a hyperlink, shared type, or comparison
attribute, then generate Arabic questions requiring both passages. Include
bridge-entity and comparison forms.

For joint generation, create paired Arabic entity descriptions with dates,
occupations, locations, creators, membership relations, or aliases, then write
questions whose positives are both documents. Synthetic questions answerable
from only one passage are less useful for this task.

## Example Data

| Query | Positive document |
| --- | --- |
| شاركت بيني راي بريدجز في مسلسل كوميدي تلفزيوني مع أي ممثل آخر؟ (62 chars) | بيني راي بريدجز (ولدت في 29 يوليو 1990) ممثلة أمريكية. شاركت في العديد من الأعمال التلفزيونية مثل "لأجل حبك"، "القانون العائلي"، "ولد يلتقي العالم"، و"بيت الآباء". تشتهر بدورها في مسلسل "نصف ونصف" كشابة مونا. (208 chars) |
| من منح كاغانوي شيجيموتشي سيفًا صنعه مؤسس مدرسة موراماسا؟ (56 chars) | كاغانوي شيجيموتشي (加賀井 重望، 1561 – 27 أغسطس 1600) كان ساموراي يابانيًا في فترة أزوتشي-موموياما، خدم عشيرة أودا. كان حاكمًا على قلعة كاغانوي. خلال معركة كوماكي وناغاكوت، قاتل شيجيموتشي تحت قيادة والده شيجيموني، الذي كان مرتبطًا ... [truncated 225 chars](457 chars) |
| أي فيلم كتب وأخرجه جوبي هارولد مع موسيقى كتبها صموئيل سيم؟ (58 chars) | سامويل سيم هو ملحن أفلام وتلفزيون. استطاع أن يحصل على الشهرة لأول مرة بموسيقى حازت على جوائز لسلسلة الدراما البريطانية "دونكيرك". منذ ذلك الحين، كتب الموسيقى لأعمال متنوعة من الأفلام والتلفزيون، وأحدث أعماله هي موسيقى فيلم "أ ... [truncated 225 chars](452 chars) |
| ما هو تاريخ مباراة كرة القدم الجامعية التي لعبت في ملعب صن لايف في ميامي جاردنز، فلوريدا، حيث هزم كليمسون فريق أوكلاهوما سونرز رقم 4 بنتيجة 37-17؟ (146 chars) | فريق كرة القدم كليمسون تايجرز لعام 2015 كان يمثل جامعة كليمسون في موسم كرة القدم NCAA Division I FBS لعام 2015. كان الفريق بقيادة المدرب الرئيسي دابو سويني في عامه السابع الكامل والثامن بشكل عام منذ توليه القيادة منتصف موسم 2 ... [truncated 225 chars](1006 chars) |
| Devil's Food هي مجموعة من الأغاني الفردية من فرقة روك أند رول أمريكية كانت معروفة أيضًا بأداء عروض كاونتري باسم أي فرقة؟ (120 chars) | Devil's Food هي مجموعة من الأغاني الفردية المفضلة من فرقة الروك الأمريكية Supersuckers، صدرت في أبريل 2005 عن طريق شركة Mid-Fi Records. (135 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-ar |
| Task / split | NanoHotpotQA |
| Hugging Face dataset | [hakari-bench/NanoBEIR-ar](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ar) |
| Language | ar |
| Category | natural_language |
| Queries | 50 |
| Documents | 5,090 |
| Positive qrels | 100 |
| Avg positives / query | 2.00 |
| Positives per query (min / median / max) | 2 / 2.00 / 2 |
| Queries with multiple positives | 50 (100.0%) |
| BM25 nDCG@10 | 0.6837 |
| BM25 hit@10 | 0.9400 |
| BM25 Recall@100 | 0.8900 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.7365 |
| Dense hit@10 | 0.9800 |
| Dense Recall@100 | 0.9400 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.7798 |
| Reranking hybrid hit@10 | 0.9800 |
| Reranking hybrid Recall@100 | 0.9400 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100 |
| Reranking hybrid safeguard rows | 0 |
| Query length avg chars | 72.76 |
| Document length avg chars | 410.03 |

### Public Sources

- [HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering](https://arxiv.org/abs/1809.09600); 2018; Zhilin Yang, Peng Qi, Saizheng Zhang, Yoshua Bengio, William W. Cohen, Ruslan Salakhutdinov, Christopher D. Manning; DOI: `10.18653/v1/D18-1259`.
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663); 2021; Nandan Thakur, Nils Reimers, Andreas Rueckle, Abhishek Srivastava, Iryna Gurevych; DOI: `10.48550/arXiv.2104.08663`.
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595); 2025; Kenneth Enevoldsen, Isaac Chung, Imene Kerboua, Marton Kardos, Ashwin Mathur, and others; DOI: `10.48550/arXiv.2502.13595`.
- [HotpotQA official site](https://hotpotqa.github.io/).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-ar](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ar)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering | 2018 | task paper | https://arxiv.org/abs/1809.09600 |
| HotpotQA official site |  | project page | https://hotpotqa.github.io/ |
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
  task_name: NanoHotpotQA
  split_name: NanoHotpotQA
  language: ar
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-ar__NanoHotpotQA.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 50
    documents: 5090
    positive_qrels: 100
  positives_per_query:
    average: 2.0
    min: 2
    median: 2.0
    max: 2
    multi_positive_queries: 50
    multi_positive_query_percent: 100.0
  text_stats_chars:
    query_mean: 72.76
    document_mean: 410.025147
  bm25:
    ndcg_at_10: 0.6836749082085007
    hit_at_10: 0.94
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: MNanoBEIR Arabic NanoBEIR task split from hakari-bench/NanoBEIR-ar
    train_eval_overlap_audit: not_audited
    leakage_note: prefer excluding HotpotQA, BEIR, or NanoBEIR records likely to overlap
      with these evaluation questions or supporting pages
    useful_training_data:
    - non-overlapping HotpotQA examples with supporting facts
    - Arabic or multilingual multi-hop QA retrieval datasets
    - Wikipedia hyperlink graph retrieval pairs
    - question-to-multiple-document supervision
    synthetic_data:
      document_generation: paired Arabic Wikipedia-style entity passages connected
        by hyperlinks, shared types, dates, locations, occupations, creators, or memberships
      question_generation: Arabic bridge and comparison questions that require both
        generated passages
      answerability: positives should be both documents needed for the reasoning path,
        not a single answer-bearing passage
    multi_positive_training: required
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoBEIR-ar
    source_urls:
    - label: HotpotQA paper
      url: https://arxiv.org/abs/1809.09600
    - label: HotpotQA official site
      url: https://hotpotqa.github.io/
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
  - title: 'HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering'
    url: https://arxiv.org/abs/1809.09600
    year: 2018
    doi: 10.18653/v1/D18-1259
    is_paper: true
    source_confidence: definitive_paper_link
  - title: HotpotQA official site
    url: https://hotpotqa.github.io/
    year: null
    doi: null
    is_paper: false
    source_confidence: definitive_project_page
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
      ndcg_at_10: 0.6836749082
      hit_at_10: 0.94
      recall_at_100: 0.89
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.89
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.7365317285
      hit_at_10: 0.98
      recall_at_100: 0.94
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.94
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.7798242459
      hit_at_10: 0.98
      recall_at_100: 0.94
      candidate_count_min: 100
      candidate_count_max: 100
      candidate_count_mean: 100.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.94
      safeguard_positive_rows: 0
      rows_with_101_candidates: 0
```
