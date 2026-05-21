# NanoRTEB / NanoChatDoctor

## Overview

`NanoRTEB / NanoChatDoctor` retrieves healthcare response passages for patient
medical questions from the ChatDoctor HealthCareMagic dataset.

## Details

### What the Original Data Measures

[ChatDoctor: A Medical Chat Model Fine-Tuned on a Large Language Model
Meta-AI (LLaMA) Using Medical Domain Knowledge](https://arxiv.org/abs/2303.14070)
describes fine-tuning a medical dialogue model on 100,000 patient-doctor
dialogues sourced from an online consultation platform and cleaned/anonymized
for privacy. RTEB uses this dialogue resource as retrieval: patient descriptions
are queries and medical responses are documents.

The [ChatDoctor HealthCareMagic dataset card](https://huggingface.co/datasets/lavita/ChatDoctor-HealthCareMagic-100k)
shows the underlying format as instruction, patient input, and doctor-style
output. This Nano split tests patient-question-to-response retrieval, not
medical diagnosis accuracy.

### Observed Data Profile

The split has 200 queries, 5,545 documents, and 200 positive qrel rows. Each
query has one positive. Queries average 441.09 characters and documents average
605.12 characters. The examples contain noisy patient language, misspellings,
symptoms, history, and concise medical responses.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.2420 and hit@10 = 0.3350. It ranks 33 positives at rank 1 and 67 in the top
10.

BM25 is weak because many patient questions share common symptom words, while
the matching response may use clinical terminology or a different wording. The
task rewards robust symptom-intent matching under noisy consumer health text.

### Training Data That May Help

Useful training data includes medical QA retrieval, patient-forum question to
doctor-answer ranking, clinical synonym expansion, and hard negatives from
similar symptoms with different diagnoses or advice.

### Synthetic Data Guidance

Generate patient-style questions from non-evaluation medical answers and keep
language noisy and varied. Use hard negatives with overlapping symptoms,
medications, or demographics. Avoid making training examples appear as medical
advice generation without retrieval evidence.

## Example Data

| Query | Positive document |
| --- | --- |
| My wife that is 31yrs old had a major operation 6mos ago. She had thymic cancer with 3 large malignant thymomas pressed against her right lung her heart and her liver ..they removed her right lung and removed then reconstruct ... [truncated 225 chars](1183 chars) | Thanks for the query from the history it is quite evident your wife had shad a very tough time but from the diagnosis of malignant Thomas I have to tell you that it means the liver has got metastasis from the Thomas that is w ... [truncated 225 chars](418 chars) |
| Okay so the past two months I have missed my first birth control pill, I finally got back on track this month and I am 10 days into the packet. I had intercourse last tuesday and have been feeling more than off. Nausea, fatig ... [truncated 225 chars](534 chars) | Hello, Thanks for writing to us. Irregular intake of birth control pill & unprotected sex close to your fertile period or ovulation day (occurs 14 days prior to due date) are quite risky for being pregnant. In this case, I su ... [truncated 225 chars](396 chars) |
| Hi iI have been diagnoed with thymic cancer, I do not like to take the drugs for pain that are prescribed,as they have side effects that are harsh.So instead i have been taking ibuprophen .for abot 4 months ,as dosage recomme ... [truncated 225 chars](728 chars) | Thy mic cancer causes respiratory distress. After a thy mic tumor is found and tests have been done to get a sense of its Factors important in choosing a treatment include the type and stage of the cancer, whether it is respe ... [truncated 225 chars](676 chars) |
| I have some darkened tissue around the left side of the tubercle of the epiglottis, accompanied by ear pain and recently otitis media, which was treated by oral administration of doxycycline. I ve also had increased appetite ... [truncated 225 chars](728 chars) | Hi, how did you see your epiglottis?endoscopy pictures?symptoms for ca. epiglottis are voice change(most common)pain in throathemoptysisdysphagia and loss of weight(not weight gain)increased appetite and weight gain can be du ... [truncated 225 chars](834 chars) |
| hi doctor my wife had recent laparoscopic surgery,i tested my sperm countvolume 2ml,viscocite (93 chars) | Hello, Thanks for the query to Chat Doctor. Forum. I analyze your report as, Volume 2ml (normal 2-5 ml) at borderline level normal. Viscocity normal pH 7.1 (normal 6-8)SPERM COUNT (query) normally it is 60-120 millions total. ... [truncated 225 chars](946 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoRTEB |
| Backing dataset | NanoRTEB |
| Task / split | NanoChatDoctor |
| Hugging Face dataset | [hakari-bench/NanoRTEB](https://huggingface.co/datasets/hakari-bench/NanoRTEB) |
| Source dataset | [lavita/ChatDoctor-HealthCareMagic-100k](https://huggingface.co/datasets/lavita/ChatDoctor-HealthCareMagic-100k) |
| Language | en |
| Category | natural_language |
| Queries | 200 |
| Documents | 5,545 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.2420 |
| BM25 hit@10 | 0.3350 |
| Query length avg chars | 441.09 |
| Document length avg chars | 605.12 |

### Public Sources

- [ChatDoctor: A Medical Chat Model Fine-Tuned on a Large Language Model Meta-AI (LLaMA) Using Medical Domain Knowledge](https://arxiv.org/abs/2303.14070), task paper.
- [lavita/ChatDoctor-HealthCareMagic-100k](https://huggingface.co/datasets/lavita/ChatDoctor-HealthCareMagic-100k), source dataset card.
- [Introducing RTEB: A New Standard for Retrieval Evaluation](https://huggingface.co/blog/rteb), RTEB benchmark announcement.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoRTEB](https://huggingface.co/datasets/hakari-bench/NanoRTEB)
- Source task dataset: [lavita/ChatDoctor-HealthCareMagic-100k](https://huggingface.co/datasets/lavita/ChatDoctor-HealthCareMagic-100k)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| ChatDoctor: A Medical Chat Model Fine-Tuned on a Large Language Model Meta-AI (LLaMA) Using Medical Domain Knowledge | 2023 | task paper | https://arxiv.org/abs/2303.14070 |
| lavita/ChatDoctor-HealthCareMagic-100k | 2023 | dataset card | https://huggingface.co/datasets/lavita/ChatDoctor-HealthCareMagic-100k |
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
  task_name: NanoChatDoctor
  split_name: NanoChatDoctor
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoRTEB/NanoChatDoctor.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 200
    documents: 5545
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 441.09
    document_mean: 605.12
  bm25:
    ndcg_at_10: 0.242
    hit_at_10: 0.335
    source: dataset_bm25_column
  example_count: 5
```
