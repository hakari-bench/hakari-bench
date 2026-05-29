# NanoIndicQA / ta

## Overview

`NanoIndicQA / ta` is the Tamil split of IndicQA retrieval. Tamil questions
retrieve Tamil context paragraphs.

## Details

### What the Original Data Measures

[Towards Leaving No Indic Language Behind](https://arxiv.org/abs/2212.05409)
introduces IndicQA as a manually curated cloze-style reading-comprehension task
inside IndicXTREME. The MTEB retrieval adaptation evaluates retrieval of the
context paragraph for each question.

### Observed Data Profile

The Nano split has 200 queries, 253 documents, and 201 positive qrel rows. One
query has two positives. Queries average 56.34 characters and documents average
2,288.26 characters. The first observed questions target a Rishikesh paragraph.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.2932
and hit@10 = 0.4600. It ranks only 32 positives at rank 1 and 92 in the top 10.
All positives are within the top 100.

This is the weakest BM25 profile in NanoIndicQA. Tamil questions can be short or
transliterated, and long paragraphs share many broad religious, geographic, or
historical terms. Dense retrievers should improve over sparse matching by
capturing the question-context relation.

### Training Data That May Help

Tamil QA context retrieval, Tamil Wikipedia passage retrieval, and Indic
multilingual retrieval data are useful. Training should include transliterated
terms, named entities, and same-topic hard negatives.

### Synthetic Data Guidance

Generate Tamil questions from paragraphs and keep the paragraph as the positive.
Include Sanskrit/English transliterations, place names, bridges, religious
terms, and hard negatives from related geography or religious contexts.

## Example Data

| Query | Positive document |
| --- | --- |
| டிஃபின் டாப்பின் மற்ற பெயர் என்ன? (33 chars) | 1880 ஆம் ஆண்டு நிலச்சரிவில் அழிந்துபோன நைனா தேவி கோயில் பின்னாளில் மீண்டும் கட்டப்பட்டது. இது நைனி ஏரியின் வடக்குப்புறக் கரையில் காணப்படுகிறது. இந்தக் கோயிலில் இருக்கும் கடவுளான மா நைனா தேவி நேத்ராக்கள் அல்லது கண்களைக் குறிக் ... [truncated 225 chars](2917 chars) |
| தொழில்நுட்ப சிறப்பு மற்றும் துல்லியமான கணித அறிவைக் கொண்ட தனித்துவமான அமைப்பின் பெயர் என்ன? (91 chars) | 1600 ஆண்டுகாலப் பழமை வாய்ந்த சிகிரியா ஓவியங்கள் பண்டைய இலங்கையின் கலைச் சிறப்பை வெளிக்காட்டுகின்றன. இது உலகின் பண்டைக்கால நகரத் திட்டமிடலின் ஒரு உதாரணமாகக் காணப்படுகிறது. இது இலங்கையில் உள்ள ஏழு உலக மரபுரிமைக் களங்களில் ஒன்றா ... [truncated 225 chars](4916 chars) |
| இலங்கையில் எத்தனை ஆண்டுகள் உள்நாட்டுப் போர் நடந்தது? (52 chars) | 1959ல் கடும்போக்கு பௌத்த பிக்கு ஒருவனால் பண்டாரநாயக்க படுகொலை செய்யப்பட்டார். 1960ல் S. W. R. D. பண்டாரநாயக்கவின் மனைவியான சிறிமாவோ பண்டாரநாயக்க பிரதமராகப் பதவியேற்றார். 1962இல் ஏற்பட்ட கலகத்தையும் வெற்றிகரமாக எதிர்கொண்டார். ... [truncated 225 chars](3363 chars) |
| பஞ்சாபில் ஒரு பன்முக கலாச்சார அரசை நிறுவ விரும்பியது யார்? (58 chars) | 1713 ஆம் ஆண்டில், பன்டா சிங் பகதூர் பஞ்சாபில் ஒரு பன்முக கலாச்சார அரசை நிறுவ விரும்பினார். இதற்காக முகலாயர்களுடன் இவர் தளர்ச்சியின்றி போராடினார். அவரது அரசு தனது வீழ்ச்சிக்கு முன்னதாக ஒரு வருடத்திற்கும் கீழ் தான் இருந்தது. பல ... [truncated 225 chars](1988 chars) |
| எந்த மொழியிலிருந்து ஹிந்து உருவானது? (36 chars) | 'இந்து' என்ற சொல் 'சிந்து' (Sindhu) என்ற சமஸ்கிருதச் சொல்லிலிருந்து ஈரானிய மொழியான பாரசீக மொழி மூலமாக உருவான ஒரு சொல் ஆகும். இந்து என்ற சொல் முதன்முதலில் பாரசீகத்தினரால் ஒரு புவியியல் சொல்லாக, அதாவது 'சிந்து நதிக்குக் கிழக்கு ... [truncated 225 chars](1524 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoIndicQA |
| Backing dataset | NanoIndicQA |
| Task / split | ta |
| Hugging Face dataset | [hakari-bench/NanoIndicQA](https://huggingface.co/datasets/hakari-bench/NanoIndicQA) |
| Language | ta |
| Category | natural_language |
| Queries | 200 |
| Documents | 253 |
| Positive qrels | 201 |
| BM25 nDCG@10 | 0.2932 |
| BM25 hit@10 | 0.4600 |
| BM25 Recall@100 | 0.7413 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.6415 |
| Dense hit@10 | 0.7900 |
| Dense Recall@100 | 0.9403 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.4551 |
| Reranking hybrid hit@10 | 0.6100 |
| Reranking hybrid Recall@100 | 0.9502 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 10 |
| Query length avg chars | 56.34 |
| Document length avg chars | 2,288.26 |

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
  task_name: ta
  split_name: ta
  language: ta
  category: natural_language
  document_path: docs/benchmark_tasks/NanoIndicQA/ta.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 200
    documents: 253
    positive_qrels: 201
  positives_per_query:
    average: 1.005
    min: 1
    median: 1.0
    max: 2
    multi_positive_queries: 1
    multi_positive_query_percent: 0.5
  text_stats_chars:
    query_mean: 56.335
    document_mean: 2288.26087
  bm25:
    ndcg_at_10: 0.29321092529354836
    hit_at_10: 0.46
    source: dataset_candidate_subset
  example_count: 5
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.2932109253
      hit_at_10: 0.46
      recall_at_100: 0.7412935323
      candidate_count_min: 253
      candidate_count_max: 253
      candidate_count_mean: 253.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.7412935323
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.6415030707
      hit_at_10: 0.79
      recall_at_100: 0.9402985075
      candidate_count_min: 253
      candidate_count_max: 253
      candidate_count_mean: 253.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9402985075
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.4550558328
      hit_at_10: 0.61
      recall_at_100: 0.9502487562
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.05
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9502487562
      safeguard_positive_rows: 10
      rows_with_101_candidates: 10
```
