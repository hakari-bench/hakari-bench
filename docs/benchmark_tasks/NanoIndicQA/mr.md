# NanoIndicQA / mr

## Overview

`NanoIndicQA / mr` is the Marathi split of IndicQA retrieval. Marathi questions
retrieve the Marathi paragraph that supports the answer.

## Details

### What the Original Data Measures

IndicQA is a manually curated cloze-style reading-comprehension component of
IndicXTREME, described in [Towards Leaving No Indic Language Behind](https://arxiv.org/abs/2212.05409).
The retrieval adaptation uses each question as a query and the source context as
the relevant document.

### Observed Data Profile

The Nano split has 200 queries, 250 documents, and 200 positive qrel rows. Each
query has one positive. Queries average 59.85 characters and documents average
1,711.74 characters. Several observed questions ask about the same Chandrayaan
paragraph.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.4612
and hit@10 = 0.5950. It ranks 67 positives at rank 1 and 119 in the top 10. All
positives are within the top 100.

### Training Data That May Help

Marathi QA context retrieval, Marathi Wikipedia retrieval, and multilingual
IndicQA training are useful. Hard negatives should include same-domain science,
history, and biography paragraphs.

### Synthetic Data Guidance

Generate Marathi questions from full paragraphs and include several questions
per paragraph. Keep long evidence paragraphs as positives and include related
paragraphs as hard negatives.

## Example Data

| Query | Positive document |
| --- | --- |
| कोणत्या वर्षी अमर्त्य सेन आपल्या कुटुंबासह पश्चिम बंगालला गेले? (63 chars) | अमर्त्य सेनचा जन्म बंगालमधील , ब्रिटिश भारतातील एका बंगाली हिंदू वैद्य कुटुंबात झाला होता. रवींद्रनाथ टागोर यांनी अमर्त्य सेन यांना त्याचे नाव दिले (बंगाली অমৃতत्य ortमॉर्टो, लिटर. "अमर"). सेन यांचे कुटुंबीय सध्याचे बांगलादेश ... [truncated 225 chars](1263 chars) |
| डेटिंगसाठी चुनखडीची साधने राज्यात उत्खनन केव्हा करण्यात आली? (61 chars) | 20,000 वर्षांपूर्वी डेटिंगसाठी अश्मयुगातील साधने राज्यात excavated गेले आहेत . [ 13 ] प्रदेश Vanga किंगडम , निवडणुक भारत प्राचीन राज्यांचे एक एक भाग होता . [ 14 ] Magadha राज्य होणारी , 7 शतक इ. स. पू. मध्ये स्थापना झाली बिहा ... [truncated 225 chars](2901 chars) |
| भारतीय इतिहासातील सर्वात महत्वाचा ऐतिहासिक वारसा कोणी दिला? (59 chars) | अशोकाने भारतीय इतिहासातील सर्वांत महत्त्वाचा ऐतिहासिक वारसा दिला म्हणजे त्याने त्याच्या राज्यात सर्वत्र लिहिलेले शिलालेख. अशोकाअगोदरच्या व नंतरच्या भारतीय राजांच्या फारश्या नोंदी आढळत नाहीत त्यामुळे तत्कालीन ऐतिहासिक मिळवणे ज ... [truncated 225 chars](1012 chars) |
| दिल्लीवर राज्य करणारा शेवटचा हिंदू सम्राट कोण ठरला? (51 chars) | अकबरने राज्यावर आल्याआल्या ठरवले की शेरशाह सुरीच्या, ज्याने हुमायूॅंला दिल्लीतून हाकलुन देउन दिल्लीचे तख्त काबीज केले होते, वंशाचा नायनाट करायचा. शेरशाहची तीन मुले वेगवेगळ्या ठिकाणी स्वतंत्र राज्ये चालवित होती. अकबरने त्यातील ... [truncated 225 chars](1300 chars) |
| त्याने कोणास सांगितले की दुसऱ्या समाजावर दबाव आणून कोणत्याही समाजाला गुलाम बनण्याचा अधिकार नाही? (96 chars) | इ. स. १९२७-३० मधील सायमन कमिशनने अस्पृश्यांच्या राजकीय हितांना फारसे महत्त्व दिले नाही. ब्रिटिश सरकार भारताला काही राजकीय हक्क राज्यघटनेच्या माध्यमातून देण्याच्या तयारीत होते तेव्हा भारताच्या भावी राज्यघटनेत अस्पृश्यांच्या हि ... [truncated 225 chars](6702 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoIndicQA |
| Backing dataset | NanoIndicQA |
| Task / split | mr |
| Hugging Face dataset | [hakari-bench/NanoIndicQA](https://huggingface.co/datasets/hakari-bench/NanoIndicQA) |
| Language | mr |
| Category | natural_language |
| Queries | 200 |
| Documents | 250 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.4612 |
| BM25 hit@10 | 0.5950 |
| BM25 Recall@100 | 0.8400 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.6720 |
| Dense hit@10 | 0.8150 |
| Dense Recall@100 | 0.9700 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.5916 |
| Reranking hybrid hit@10 | 0.7600 |
| Reranking hybrid Recall@100 | 0.9650 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 7 |
| Query length avg chars | 59.85 |
| Document length avg chars | 1,711.74 |

### Public Sources

- [Towards Leaving No Indic Language Behind](https://arxiv.org/abs/2212.05409), ACL 2023.
- [mteb/IndicQARetrieval](https://huggingface.co/datasets/mteb/IndicQARetrieval).
- [ai4bharat/IndicQA](https://huggingface.co/datasets/ai4bharat/IndicQA).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoIndicQA](https://huggingface.co/datasets/hakari-bench/NanoIndicQA)
- Source task dataset: [mteb/IndicQARetrieval](https://huggingface.co/datasets/mteb/IndicQARetrieval)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Towards Leaving No Indic Language Behind | 2023 | paper | https://arxiv.org/abs/2212.05409 |
| mteb/IndicQARetrieval |  | dataset card | https://huggingface.co/datasets/mteb/IndicQARetrieval |
| ai4bharat/IndicQA |  | dataset card | https://huggingface.co/datasets/ai4bharat/IndicQA |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoIndicQA
  backing_dataset: NanoIndicQA
  dataset_id: hakari-bench/NanoIndicQA
  task_name: mr
  split_name: mr
  language: mr
  category: natural_language
  document_path: docs/benchmark_tasks/NanoIndicQA/mr.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 200
    documents: 250
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 59.85
    document_mean: 1711.74
  bm25:
    ndcg_at_10: 0.46119204075094833
    hit_at_10: 0.595
    source: dataset_candidate_subset
  example_count: 5
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.4611920408
      hit_at_10: 0.595
      recall_at_100: 0.84
      candidate_count_min: 250
      candidate_count_max: 250
      candidate_count_mean: 250.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.84
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.6720272379
      hit_at_10: 0.815
      recall_at_100: 0.97
      candidate_count_min: 250
      candidate_count_max: 250
      candidate_count_mean: 250.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.97
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.5916179506
      hit_at_10: 0.76
      recall_at_100: 0.965
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.035
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.965
      safeguard_positive_rows: 7
      rows_with_101_candidates: 7
```
