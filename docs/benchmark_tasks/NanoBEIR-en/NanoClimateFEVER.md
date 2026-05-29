# NanoBEIR-en / NanoClimateFEVER

## Overview

Climate-FEVER is a climate-change fact-checking dataset where real-world climate
claims are matched to Wikipedia evidence that supports, refutes, or is
insufficient for the claim. `NanoClimateFEVER` is the compact English NanoBEIR
retrieval task: each query is a climate-related claim, and the system must
retrieve evidence-bearing Wikipedia passages. The task tests climate-domain
claim/evidence matching, entity grounding, numeric and temporal reasoning, and
retrieval under misinformation-style wording.

## Details

### What the Original Data Measures

[CLIMATE-FEVER: A Dataset for Verification of Real-World Climate
Claims](https://arxiv.org/abs/2012.00614) introduces Climate-FEVER as a dataset
for verification of climate-change-related claims. The paper adapts the FEVER
methodology from artificially written claims to real-world climate claims
collected from the Internet. It reports 1,535 verifiable climate claims and
7,675 annotated claim-evidence pairs, with evidence candidates retrieved from
English Wikipedia and annotated as `SUPPORTS`, `REFUTES`, or
`NOT_ENOUGH_INFO`.

The original paper is important because this is not generic topical climate
retrieval. The dataset was built to help retrieve reliable evidence for humans
checking potentially misleading climate claims. Claims were collected from both
scientifically informed sources and climate-change skeptic or denialist sources,
then filtered by climate scientists for verifiability. Evidence retrieval used a
pipeline over Wikipedia: document-level retrieval, sentence-level retrieval, and
sentence re-ranking. The paper emphasizes that real climate claims are more
subtle than FEVER's synthetic claims; evidence may address only part of a claim,
may contain conflicting support and refutation, or may require careful handling
of quantities, time spans, and climate terminology.

[BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information
Retrieval Models](https://arxiv.org/abs/2104.08663) includes Climate-FEVER in
the fact-checking group. In BEIR, the original dataset claims become queries,
and systems retrieve evidence from the FEVER Wikipedia corpus, with a small
number of Wikipedia articles added because they were present in the original
relevance judgments but missing from the shared corpus. This matters for the
Nano task because the retrieval unit is an evidence document or passage, not the
final entailment label. The retriever is evaluated on whether it can surface
evidence that a later verifier or reader could use.

### Observed Data Profile

The sampled Nano task has 50 queries, 3,408 documents, and 148 positive qrel
rows. The average query length is 128.40 characters, and the average document
length is 1,619.53 characters. This is a multi-positive task: queries have an
average of 2.96 positives, 44 of 50 queries have more than one positive, and the
maximum number of positives for one query is 5. Ranking several relevant
evidence passages matters; a model that finds one useful passage but misses the
rest can still lose nDCG.

The sampled queries read like real climate claims rather than clean search
queries. They include assertions about Arctic and Antarctic sea ice, global
temperature records, solar activity, sea-level rise, drought, hurricane
attribution, natural variability, carbon dioxide levels, and the history of
global cooling or warming claims. Many are long declarative sentences, sometimes
with hedging, quotation marks, named institutions such as NASA and NOAA, or
numeric anchors such as `800,000 years`, `1970 until 1998`, or `2080`. They are
not asking "what is climate change?"; they are making claims whose evidence must
be retrieved.

The documents are Wikipedia passages, often substantially longer than the
queries. Positives may be broad climate pages such as global warming, greenhouse
gas, Arctic sea ice decline, sea-level rise, instrumental temperature record, or
climate change denial. Some positives are surprisingly indirect: a claim about
Antarctic sea ice gain can be paired with an Arctic article, and a claim about
newspaper stories on warmest years can require temperature-record or regional
context rather than a passage that repeats the claim's exact wording. This makes
the data a mixture of topical climate retrieval and evidence selection for
claim verification.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.3289
and hit@10 = 0.7400. BM25 ranks only 16 positives first, although 37 of 50
queries have at least one positive in the top 10. The median first-positive rank
is 3, but the worst observed first-positive rank is 99. This is a much harder
sparse baseline than duplicate-question retrieval because claims often contain
many generic climate terms and the evidence can use different wording.

The inspected BM25 ranking shows several useful failure modes. For the claim
about NASA and NOAA declaring the past five years the warmest on record, BM25
retrieves pages about satellites, extinction events, and journalism before the
temperature-record evidence. For the claim that temperature errors in the Great
Lakes region are not used in global temperature records, BM25 is distracted by
raw data, temperature reconstruction, and the Great Lakes as a region, while
the positives include climate and precipitation context. For "In fact, the
trend, while not statistically significant, is downward", BM25 pulls generic
trend and Arctic sea-ice pages, while the relevant evidence requires knowing
what trend the claim is about.

These examples show that lexical overlap is not enough. The retriever must
recognize the claim's climate subtopic, map it to the right evidence pages, and
avoid passages that share words such as `temperature`, `solar`, `sea level`, or
`drought` but do not address the claim's evidential target. Dense or reranking
models can improve by representing claim semantics, quantities, temporal scope,
and whether a passage is actually evidence-bearing.

### Training Data That May Help

Useful training data includes non-overlapping claim-to-evidence retrieval pairs,
especially climate or science fact-checking data where the positive passage
supports or refutes a claim. FEVER-style evidence retrieval data can help, but
Climate-FEVER differs because its claims are real-world climate claims and often
contain subtler framing, numbers, and partial evidence. Public Climate-FEVER or
BEIR dev/test examples likely to overlap with this Nano split should preferably
be excluded from training.

Helpful auxiliary data includes scientific claim verification, climate FAQ
evidence retrieval, Wikipedia claim-evidence pairs, and supervised retrieval
where the query is a declarative claim rather than a question. Models should
learn to retrieve evidence for both mainstream scientific claims and skeptical or
misleading claims without treating the query wording itself as authoritative.

### Synthetic Data Guidance

For document-to-question generation, start from non-evaluation climate,
environmental science, or Wikipedia passages and generate declarative claims
whose truth can be checked from the selected passage. The generated claims
should include entities, time periods, quantities, comparisons, causal wording,
and common misinformation framings such as "natural variability explains X" or
"models predicted Y". The positive document should contain evidence that clearly
supports, refutes, or qualifies the claim.

For joint document-and-question generation, create Wikipedia-style evidence
passages about climate indicators, greenhouse gases, sea level, ice sheets,
weather extremes, attribution, climate models, and historical temperature
records, then create realistic claims that require those passages. Do not use
evaluation split queries or positive passages as seeds. Synthetic data is most
useful when it teaches claim-to-evidence retrieval, not generic climate topic
classification.

## Example Data

| Query | Positive document |
| --- | --- |
| From 1970 until 1998 there was a warming period that raised temperatures by about 0.7 F that helped spawn the global warming alarmist movement. (143 chars) | The Paleocene ( -LSB- pronˈpæliəˌsiːn , _ ˈpæ - , _ - lioʊ - -RSB- ) or Palaeocene , the `` old recent '' , is a geologic epoch that lasted from about . It is the first epoch of the Paleogene Period in the modern Cenozoic Era ... [truncated 225 chars](1126 chars) |
| In fact, the trend, while not statistically significant, is downward.” (70 chars) | The solar cycle or solar magnetic activity cycle is the nearly periodic 11-year change in the Sun 's activity ( including changes in the levels of solar radiation and ejection of solar material ) and appearance ( changes in t ... [truncated 225 chars](610 chars) |
| Local and regional sea levels continue to exhibit typical natural variability—in some places rising and in others falling. (122 chars) | Mean sea level ( MSL ) ( abbreviated simply sea level ) is an average level of the surface of one or more of Earth 's oceans from which heights such as elevations may be measured . MSL is a type of vertical datuma standardise ... [truncated 225 chars](1011 chars) |
| [climate scientists] say that aspects of the case of Hurricane Harvey suggest global warming is making a bad situation worse. (125 chars) | The effects of global warming are the environmental and social changes caused ( directly or indirectly ) by human emissions of greenhouse gases . There is a scientific consensus that climate change is occurring , and that hum ... [truncated 225 chars](1285 chars) |
| The CERN CLOUD experiment only tested one-third of one out of four requirements necessary to blame global warming on cosmic rays, and two of the other requirements have already failed. (184 chars) | Attribution of recent climate change is the effort to scientifically ascertain mechanisms responsible for recent climate changes on Earth , commonly known as ` global warming ' . The effort has focused on changes observed dur ... [truncated 225 chars](2016 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoBEIR-en |
| Backing dataset | NanoBEIR-en |
| Task / split | NanoClimateFEVER |
| Hugging Face dataset | [hakari-bench/NanoBEIR-en](https://huggingface.co/datasets/hakari-bench/NanoBEIR-en) |
| Language | en |
| Category | natural_language |
| Queries | 50 |
| Documents | 3,408 |
| Positive qrels | 148 |
| Avg positives / query | 2.96 |
| Positives per query (min / median / max) | 1 / 3.00 / 5 |
| Queries with multiple positives | 44 (88.0%) |
| BM25 nDCG@10 | 0.3266 |
| BM25 hit@10 | 0.7200 |
| BM25 Recall@100 | 0.5743 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.2811 |
| Dense hit@10 | 0.6800 |
| Dense Recall@100 | 0.6757 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.3419 |
| Reranking hybrid hit@10 | 0.7600 |
| Reranking hybrid Recall@100 | 0.7027 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 1 |
| Query length avg chars | 128.40 |
| Document length avg chars | 1619.53 |

### Public Sources

- [CLIMATE-FEVER: A Dataset for Verification of Real-World Climate Claims](https://arxiv.org/abs/2012.00614); 2020; Thomas Diggelmann, Jordan Boyd-Graber, Jannis Bulian, Massimiliano Ciaramita, Markus Leippold; DOI: `10.48550/arXiv.2012.00614`.
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663); 2021; Nandan Thakur, Nils Reimers, Andreas Rueckle, Abhishek Srivastava, Iryna Gurevych; DOI: `10.48550/arXiv.2104.08663`.
- [Climate-FEVER project site](http://climatefever.ai).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-en](https://huggingface.co/datasets/hakari-bench/NanoBEIR-en)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| CLIMATE-FEVER: A Dataset for Verification of Real-World Climate Claims | 2020 | paper | https://arxiv.org/abs/2012.00614 |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | https://arxiv.org/abs/2104.08663 |
| Climate-FEVER project site |  | project page | http://climatefever.ai |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoBEIR-en
  backing_dataset: NanoBEIR-en
  dataset_id: hakari-bench/NanoBEIR-en
  task_name: NanoClimateFEVER
  split_name: NanoClimateFEVER
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoBEIR-en/NanoClimateFEVER.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 50
    documents: 3408
    positive_qrels: 148
  positives_per_query:
    average: 2.96
    min: 1
    median: 3.0
    max: 5
    multi_positive_queries: 44
    multi_positive_query_percent: 88.0
  text_stats_chars:
    query_mean: 128.4
    document_mean: 1619.53169
  bm25:
    ndcg_at_10: 0.3265612239542905
    hit_at_10: 0.72
    source: dataset_candidate_subset
  learning:
    original_train_split: unknown
    evaluation_split_origin: unknown
    train_eval_overlap_audit: not_audited
    leakage_note: prefer excluding upstream dev/test data or other Climate-FEVER/BEIR-derived
      data likely to overlap with the NanoBEIR evaluation claims and evidence
    useful_training_data:
    - non-overlapping climate claim-evidence retrieval pairs
    - FEVER-style fact verification evidence retrieval data
    - scientific and climate-domain claim verification datasets
    synthetic_data:
      document_generation: climate or environmental science evidence passages with
        entities, dates, quantities, and causal statements
      question_generation: declarative climate claims that can be supported, refuted,
        or qualified by one selected passage
      answerability: positives should contain evidence addressing the claim, not merely
        the same climate topic
    multi_positive_training: multi_positive_objective
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoBEIR-en
    source_urls:
    - label: Climate-FEVER project site
      url: http://climatefever.ai
    - label: Zeta Alpha NanoBEIR collection
      url: https://huggingface.co/collections/zeta-alpha-ai/nanobeir
    source_notes: []
  references:
  - title: 'CLIMATE-FEVER: A Dataset for Verification of Real-World Climate Claims'
    url: https://arxiv.org/abs/2012.00614
    year: 2020
    doi: 10.48550/arXiv.2012.00614
    is_paper: true
    source_confidence: definitive_paper_link
  - title: 'BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information
      Retrieval Models'
    url: https://arxiv.org/abs/2104.08663
    year: 2021
    doi: 10.48550/arXiv.2104.08663
    is_paper: true
    source_confidence: benchmark_context_paper
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.326561224
      hit_at_10: 0.72
      recall_at_100: 0.5743243243
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.5743243243
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.2810517681
      hit_at_10: 0.68
      recall_at_100: 0.6756756757
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.6756756757
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.3418726246
      hit_at_10: 0.76
      recall_at_100: 0.7027027027
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.02
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.7027027027
      safeguard_positive_rows: 1
      rows_with_101_candidates: 1
```
