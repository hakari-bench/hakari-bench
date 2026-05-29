# NanoBRIGHT / NanoBrightPsychology

## Overview

`NanoBrightPsychology` is the Psychology StackExchange slice of BRIGHT. Queries
are user posts about psychology, perception, cognition, behavior, and research
methods; relevant documents are cited web passages that help answer those posts.

## Details

### What the Original Data Measures

[BRIGHT: A Realistic and Challenging Benchmark for Reasoning-Intensive Retrieval](https://arxiv.org/abs/2407.12883)
describes its StackExchange tasks as reasoning-intensive retrieval: annotators
combine a post title and body into a query, collect web pages cited by accepted
or high-vote answers, split them into passages, and retain positives only after
expert validation. For Psychology, this makes the task less like direct QA and
more like retrieving the scientific or conceptual support needed to reason
about a user's question.

### Observed Data Profile

The split has 101 queries, 10,000 documents, and 692 positive qrels. Queries
average 693.16 characters and often contain a lay description plus a request for
a formal construct, experiment, or psychological mechanism. Documents average
504.47 characters and include excerpts from research articles, Wikipedia-style
pages, and technical explanations. Positives average 6.85 per query, but the
median is 3 and the maximum is 54.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.1475 and hit@10 = 0.3168. It ranks 12 queries with a positive first, and the
median best positive rank is 66. Psychology questions often use everyday
phrasing while the cited source uses terms such as predictive coding,
photoreceptors, translational regulation, or attentional cueing.

### Training Data That May Help

Useful data includes non-overlapping Psychology StackExchange posts with cited
sources, psychology QA with references, paper-to-question retrieval data, and
hard negatives about the same construct but a different mechanism or
measurement.

### Synthetic Data Guidance

Generate psychology questions from realistic user descriptions, then pair them
with source passages that name the relevant construct, experiment, or measure.
Hard negatives should share broad terms such as attention, perception, or
addiction while failing to support the specific explanation.

## Example Data

| Query | Positive document |
| --- | --- |
| Asking for illogical things to make extreme views normal? A couple of months back I was reading an article about how politicians were asking to make decisions that are way beyond possible (name it unreasonable, unacceptable, ... [truncated 225 chars](363 chars) | **Share** All sharing options for: How Trump makes extreme things look normal * [ Reddit ](https://reddit.com/submit?title=How+Trump+makes+extreme+things+look+normal&url=https%3A%2F%2Fwww.vox.com%2F2017%2F12%2F21%2F16806676%2 ... [truncated 225 chars](2714 chars) |
| What term can describe the feeling that a job just does itself? Is there a term that can describe that a job, however exhausting it might be, just does itself? Meaning, for example, that all doubt concerning how you're doing ... [truncated 225 chars](943 chars) | Challenges to maintaining flow [ [ edit ](/w/index.php?title=Flow_\(psychology\)&action=edit&section=10 "Edit section: Challenges to maintaining flow") ] Some of the challenges to staying in flow include states of [ apathy ]( ... [truncated 225 chars](1037 chars) |
| What is the term for the "knowing what you think but can't explain it" phenomenon? I think we all experience this phenomenon once in a while, and I am experiencing it right now. It's the feeling that whatever word one tries t ... [truncated 225 chars](504 chars) | sitelinks- wikipedia "Edit interlanguage links") * [ Article ](/wiki/Mental_block "View the content page \[c\]") * [ Talk ](/wiki/Talk:Mental_block "Discuss improvements to the content page \[t\]") English * [ Read ](/wiki/Me ... [truncated 225 chars](3508 chars) |
| Saying things to shock others Is it strange or categorically bad to say things that shock others knowingly, and enjoy their reaction? I have a close friend who partakes in such behavior, and I want to understand his motivatio ... [truncated 225 chars](830 chars) | How excessive attention-seeking evolves in adults Brains wired to equate lack of attention as dangerous, naturally respond to it as a threat in the amygdala, a subcortical structure, where thinking does not occur. [6-11] Now ... [truncated 225 chars](1161 chars) |
| What is the term for the inability to see past one's own current emotional state? I'm looking for a specific latin or greek word that describes something like the inability to empathize with emotions that are not in line with ... [truncated 225 chars](1889 chars) | sitelinks- wikipedia "Edit interlanguage links") * [ Article ](/wiki/Hot-cold_empathy_gap "View the content page \[c\]") * [ Talk ](/wiki/Talk:Hot-cold_empathy_gap "Discuss improvements to the content page \[t\]") English * [ ... [truncated 225 chars](4615 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoBRIGHT |
| Backing dataset | NanoBRIGHT |
| Task / split | NanoBrightPsychology |
| Source task | Psychology StackExchange |
| Hugging Face dataset | [hakari-bench/NanoBRIGHT](https://huggingface.co/datasets/hakari-bench/NanoBRIGHT) |
| Source dataset | [xlangai/BRIGHT](https://huggingface.co/datasets/xlangai/BRIGHT) |
| Language | en |
| Category | natural_language |
| Queries | 101 |
| Documents | 10000 |
| Positive qrels | 692 |
| Positives per query | avg 6.85, min 1, median 3, max 54 |
| Multi-positive queries | 66 (65.35%) |
| BM25 nDCG@10 | 0.2474 |
| BM25 hit@10 | 0.4653 |
| BM25 Recall@100 | 0.3829 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.4591 |
| Dense hit@10 | 0.6634 |
| Dense Recall@100 | 0.6329 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.4124 |
| Reranking hybrid hit@10 | 0.6634 |
| Reranking hybrid Recall@100 | 0.5853 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 11 |
| Query length avg chars | 693.16 |
| Document length avg chars | 504.47 |

### Public Sources

- [BRIGHT: A Realistic and Challenging Benchmark for Reasoning-Intensive Retrieval](https://arxiv.org/abs/2407.12883).
- [BRIGHT project page](https://brightbenchmark.github.io/).
- [xlangai/BRIGHT](https://huggingface.co/datasets/xlangai/BRIGHT).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBRIGHT](https://huggingface.co/datasets/hakari-bench/NanoBRIGHT)
- Source dataset: [xlangai/BRIGHT](https://huggingface.co/datasets/xlangai/BRIGHT)
- MTEB dataset record: [mteb/BRIGHT](https://huggingface.co/datasets/mteb/BRIGHT)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| BRIGHT: A Realistic and Challenging Benchmark for Reasoning-Intensive Retrieval | 2024 | benchmark paper | https://arxiv.org/abs/2407.12883 |
| BRIGHT project page | 2024 | project page | https://brightbenchmark.github.io/ |
| xlangai/BRIGHT | 2024 | dataset card | https://huggingface.co/datasets/xlangai/BRIGHT |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoBRIGHT
  backing_dataset: NanoBRIGHT
  dataset_id: hakari-bench/NanoBRIGHT
  task_name: NanoBrightPsychology
  split_name: NanoBrightPsychology
  source_task: Psychology StackExchange
  source_dataset_id: xlangai/BRIGHT
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoBRIGHT/NanoBrightPsychology.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 101
    documents: 10000
    positive_qrels: 692
  positives_per_query:
    average: 6.851485148514851
    min: 1
    median: 3
    max: 54
    multi_positive_queries: 66
    multi_positive_query_percent: 65.34653465346534
  text_stats_chars:
    query_mean: 693.1584158415842
    document_mean: 504.4673
  bm25:
    ndcg_at_10: 0.24741945854194833
    hit_at_10: 0.46534653465346537
    source: dataset_candidate_subset
  learning:
    original_train_split: unknown
    evaluation_split_origin: BRIGHT Psychology StackExchange evaluation split
    train_eval_overlap_audit: not_audited
    leakage_note: exclude NanoBRIGHT Psychology queries, cited positives, and linked
      answer pages
    useful_training_data:
    - non-overlapping Psychology StackExchange posts with cited sources
    - psychology QA with references
    - paper-to-question retrieval data
    synthetic_data:
      document_generation: psychology source passages naming constructs, experiments,
        or measures
      question_generation: user-style psychology questions with concrete scenarios
      answerability: positives should support the specific psychological explanation
    multi_positive_training: multi_positive_objective
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoBRIGHT
    source_urls:
    - label: BRIGHT arXiv
      url: https://arxiv.org/abs/2407.12883
    - label: BRIGHT project
      url: https://brightbenchmark.github.io/
    - label: xlangai/BRIGHT
      url: https://huggingface.co/datasets/xlangai/BRIGHT
    source_notes: []
  references:
  - title: 'BRIGHT: A Realistic and Challenging Benchmark for Reasoning-Intensive
      Retrieval'
    url: https://arxiv.org/abs/2407.12883
    year: 2024
    doi: 10.48550/arXiv.2407.12883
    is_paper: true
    source_confidence: definitive_paper_link
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.2474194585
      hit_at_10: 0.4653465347
      recall_at_100: 0.3829479769
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 101
      query_coverage: 1.0
      relevant_coverage_at_100: 0.3829479769
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.4591441906
      hit_at_10: 0.6633663366
      recall_at_100: 0.6329479769
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 101
      query_coverage: 1.0
      relevant_coverage_at_100: 0.6329479769
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.4124033275
      hit_at_10: 0.6633663366
      recall_at_100: 0.5852601156
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.108911
      query_count: 101
      query_coverage: 1.0
      relevant_coverage_at_100: 0.5852601156
      safeguard_positive_rows: 11
      rows_with_101_candidates: 11
```
