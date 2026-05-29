# NanoIndicQA / ml

## Overview

`NanoIndicQA / ml` is the Malayalam split of IndicQA retrieval. Malayalam
questions retrieve Malayalam context paragraphs.

## Details

### What the Original Data Measures

IndicQA is part of the IndicXTREME benchmark described in
[Towards Leaving No Indic Language Behind](https://arxiv.org/abs/2212.05409).
The MTEB retrieval version asks models to retrieve the paragraph that supports a
question.

### Observed Data Profile

The Nano split has 200 queries, 247 documents, and 200 positive qrel rows. Each
query has one positive. Queries average 81.55 characters, the longest query
average in this set, and documents average 2,522.64 characters.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.6528
and hit@10 = 0.7950. It ranks 101 positives at rank 1 and 159 in the top 10.
All positives are within the top 100.

### Training Data That May Help

Malayalam QA, Malayalam Wikipedia retrieval, and Indic multilingual context
retrieval are useful. Include long paragraph positives and same-topic hard
negatives.

### Synthetic Data Guidance

Generate Malayalam questions from paragraphs and include several per paragraph.
Use historical, cultural, geographic, and biographical contexts with long
paragraph positives.

## Example Data

| Query | Positive document |
| --- | --- |
| ഈസ്റ്റ് ഇന്ത്യാ കമ്പനി കലാപം അടിച്ചമർത്തപ്പെട്ടതിനെ തുടർന്ന്,രാജ്യം വിട്ട് തന്റെ പുത്രന്മാരെ വെടിവെച്ചു കൊല്ലേണ്ടിവന്ന മുഗൾ ഭരണാധികാരി ആരായിരുന്നു ? (148 chars) | 1803-ലെ ദില്ലി യുദ്ധത്തിൽ മറാഠരെ പരാജയപ്പെടുത്തി ബ്രിട്ടീഷുകാർ ഉത്തരേന്ത്യയുടെ നിയന്ത്രണം കൈയടക്കി. മുഗളരുടെ സംരക്ഷകരായി ദില്ലിയിലെത്തിയ ബ്രിട്ടീഷുകാർ തുടക്കത്തിൽ ചക്രവർത്തിയോട് ബഹുമാനപൂർവ്വമായിരുന്നു പെരുമാറിയിരുന്നത്. അവർ ന ... [truncated 225 chars](1588 chars) |
| വർഷങ്ങളുടെ പോരാട്ടത്തിന് ശേഷം, ബ്രിട്ടീഷുകാരിൽ നിന്ന് ഇന്ത്യയ്ക്ക് സ്വാതന്ത്ര്യം ലഭിച്ചതെന്ന്? (94 chars) | 1857-ൽ ഇംഗ്ലീഷ്‌ ഈസ്റ്റിന്ത്യാ കമ്പനിക്കു നേരെയുണ്ടായ കലാപമാണ്‌ യൂറോപ്യൻ അധിനിവേശത്തിനു നേരെ ഇന്ത്യക്കാർ നടത്തിയ പ്രധാന ചെറുത്തുനിൽപ്പ്‌ ശ്രമം. ഒന്നാം ഇന്ത്യൻ സ്വാതന്ത്ര്യ സമരം എന്നറിയപ്പെടുന്ന ഈ കലാപം പക്ഷേ ബ്രിട്ടീഷ്‌ സൈന്യ ... [truncated 225 chars](2424 chars) |
| ആർ കെ നാരായണന്റെ ആദ്യ കൃതി ഏത് ? (32 chars) | ആർ. കെ. നാരായണൻ ബ്രിട്ടീഷ് ഇന്ത്യയിലെ മദ്രാസിൽ (ഇപ്പോൾ ചെന്നൈ, തമിഴ്‌നാട്) ഒരു അയ്യർ വടാമ തമിഴ് ബ്രാഹ്മണ കുടുംബത്തിൽ 1906 ഒക്ടോബർ 10-ന് ജനിച്ചു. ആറ് ആൺമക്കളും രണ്ട് പെൺമക്കളുമുള്ള ഒരു കുടുംബത്തിലെ എട്ട് മക്കളിൽ ഒരാളായിരുന്നു ... [truncated 225 chars](4050 chars) |
| അലാവുദ്ദീൻ ഖൽജി നിർമ്മിച്ച ഒരു വലിയ കവാടം ഏതായിരുന്നു? (54 chars) | 1199-ൽ ദില്ലി സുൽത്താനായിരുന്ന ഖുത്ബ്ദീൻ ഐബക് ആയിരുന്നു ഈ മിനാറിന്റെ ആദ്യ നില പണികഴിപ്പിച്ചത്. സുൽത്താൻ ഇൽത്തുമിഷ്, 1229-ഓടെ മറ്റു നാലുനിലകളുടെ പണി പൂർത്തീകരിച്ചു. ഗോറി സാമ്രാജ്യത്തിന്റെ കാലത്ത് അഫ്ഗാനിസ്താനിൽ പലയിടത്തും ഇത്ത ... [truncated 225 chars](1608 chars) |
| നികെ അപ്പാച്ചേ എന്ന ഉപഗ്രഹം വിക്ഷേപിച്ചത് ഏത് വർഷം? (51 chars) | 1960-ൽ ബിരുദം നേടിയ ശേഷം കലാം, ഡയറക്ടറേറ്റ് ഓഫ് ടെക്നിക്കൽ ഡെവലപ്പ്മെന്റ് ആന്റ് പ്രൊഡക്ഷൻ (എയർ) എന്ന സ്ഥാപനത്തിൽ ശാസ്ത്രജ്ഞനായി ജോലിക്കു ചേർന്നു. ഇന്ത്യയുടെ പ്രതിരോധ മന്ത്രാലയത്തിന്റെ കീഴിലുള്ളതായിരുന്നു ഈ സ്ഥാപനം. പ്രതിരോധ മ ... [truncated 225 chars](2366 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoIndicQA |
| Backing dataset | NanoIndicQA |
| Task / split | ml |
| Hugging Face dataset | [hakari-bench/NanoIndicQA](https://huggingface.co/datasets/hakari-bench/NanoIndicQA) |
| Language | ml |
| Category | natural_language |
| Queries | 200 |
| Documents | 247 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.6528 |
| BM25 hit@10 | 0.7950 |
| BM25 Recall@100 | 0.9400 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.8214 |
| Dense hit@10 | 0.9550 |
| Dense Recall@100 | 0.9900 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.7807 |
| Reranking hybrid hit@10 | 0.9150 |
| Reranking hybrid Recall@100 | 0.9900 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 2 |
| Query length avg chars | 81.55 |
| Document length avg chars | 2,522.64 |

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
  task_name: ml
  split_name: ml
  language: ml
  category: natural_language
  document_path: docs/benchmark_tasks/NanoIndicQA/ml.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 200
    documents: 247
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 81.55
    document_mean: 2522.643725
  bm25:
    ndcg_at_10: 0.6527870422537473
    hit_at_10: 0.795
    source: dataset_candidate_subset
  example_count: 5
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.6527870423
      hit_at_10: 0.795
      recall_at_100: 0.94
      candidate_count_min: 247
      candidate_count_max: 247
      candidate_count_mean: 247.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.94
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.8213801681
      hit_at_10: 0.955
      recall_at_100: 0.99
      candidate_count_min: 247
      candidate_count_max: 247
      candidate_count_mean: 247.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.99
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.7807142837
      hit_at_10: 0.915
      recall_at_100: 0.99
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.01
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.99
      safeguard_positive_rows: 2
      rows_with_101_candidates: 2
```
