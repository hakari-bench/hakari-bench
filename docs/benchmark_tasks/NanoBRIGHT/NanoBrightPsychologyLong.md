# NanoBRIGHT / NanoBrightPsychologyLong

## Overview

`NanoBrightPsychologyLong` is the long-document version of the Psychology
StackExchange BRIGHT task. Queries are detailed psychology posts, and the
documents are full cited pages or long source documents.

## Details

### What the Original Data Measures

[BRIGHT](https://arxiv.org/abs/2407.12883) says its long-context variants use
complete web pages rather than split passages, creating a smaller but much
longer corpus. This setting tests document-level retrieval when the relevant
psychology evidence is embedded in a long article, encyclopedia page, or
publisher page with navigation and unrelated sections.

### Observed Data Profile

The split has 101 queries, 509 documents, and 116 positive qrels. Queries
average 693.16 characters. Documents average 40,097.47 characters and include
long pages about fables, disorders, social psychology articles, theory of mind,
and similarity measures. Most queries have one positive, with 11 multi-positive
queries.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.2270 and hit@10 = 0.3366. It ranks 14 queries with a positive first, and the
median best positive rank is 30. Long pages amplify generic psychological and
navigation terms, so the retriever must locate the right source page despite
substantial irrelevant text.

### Training Data That May Help

Useful data includes document-level psychology reference retrieval, cited-source
retrieval from psychology forums, and long-article QA with evidence grounding.
Training should avoid the same BRIGHT evaluation posts and cited pages.

### Synthetic Data Guidance

Generate long psychology source pages with sections, definitions, examples, and
research context. Questions should describe a concrete behavior or construct and
require one part of the page. Hard negatives should be long pages about adjacent
constructs that are plausible but not the right explanation.

## Example Data

| Query | Positive document |
| --- | --- |
| Asking for illogical things to make extreme views normal? A couple of months back I was reading an article about how politicians were asking to make decisions that are way beyond possible (name it unreasonable, unacceptable, ... [truncated 225 chars](363 chars) | Skip to main content clock menu more-arrow no yes mobile [ Vox homepage ](/) * ## Give [ Give ](http://vox.com/pages/support- now?itm_campaign=contribute&itm_medium=site&itm_source=navigation) * ## Newsletters [ Newsletters ] ... [truncated 225 chars](14364 chars) |
| What term can describe the feeling that a job just does itself? Is there a term that can describe that a job, however exhausting it might be, just does itself? Meaning, for example, that all doubt concerning how you're doing ... [truncated 225 chars](943 chars) | Jump to content Main menu Main menu move to sidebar hide Navigation * [ Main page ](/wiki/Main_Page "Visit the main page \[z\]") * [ Contents ](/wiki/Wikipedia:Contents "Guides to browsing Wikipedia") * [ Current events ](/wi ... [truncated 225 chars](132869 chars) |
| What is the term for the "knowing what you think but can't explain it" phenomenon? I think we all experience this phenomenon once in a while, and I am experiencing it right now. It's the feeling that whatever word one tries t ... [truncated 225 chars](504 chars) | Jump to content Main menu Main menu move to sidebar hide Navigation * [ Main page ](/wiki/Main_Page "Visit the main page \[z\]") * [ Contents ](/wiki/Wikipedia:Contents "Guides to browsing Wikipedia") * [ Current events ](/wi ... [truncated 225 chars](23048 chars) |
| Saying things to shock others Is it strange or categorically bad to say things that shock others knowingly, and enjoy their reaction? I have a close friend who partakes in such behavior, and I want to understand his motivatio ... [truncated 225 chars](830 chars) | Skip to main content Psychology Today Find a Therapist Get Help Magazine Today INTL Search Find a Therapist (City or Postcode) Verified by Psychology Today Billi Gordon Ph.D. Billi Gordon Ph.D. Obesely Speaking ATTENTION Exce ... [truncated 225 chars](19857 chars) |
| What is the term for the inability to see past one's own current emotional state? I'm looking for a specific latin or greek word that describes something like the inability to empathize with emotions that are not in line with ... [truncated 225 chars](1889 chars) | Jump to content Main menu Main menu move to sidebar hide Navigation * [ Main page ](/wiki/Main_Page "Visit the main page \[z\]") * [ Contents ](/wiki/Wikipedia:Contents "Guides to browsing Wikipedia") * [ Current events ](/wi ... [truncated 225 chars](26976 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoBRIGHT |
| Backing dataset | NanoBRIGHT |
| Task / split | NanoBrightPsychologyLong |
| Source task | Psychology StackExchange long-document |
| Hugging Face dataset | [hakari-bench/NanoBRIGHT](https://huggingface.co/datasets/hakari-bench/NanoBRIGHT) |
| Source dataset | [xlangai/BRIGHT](https://huggingface.co/datasets/xlangai/BRIGHT) |
| Language | en |
| Category | natural_language |
| Queries | 101 |
| Documents | 509 |
| Positive qrels | 116 |
| Positives per query | avg 1.15, min 1, median 1, max 5 |
| Multi-positive queries | 11 (10.89%) |
| BM25 nDCG@10 | 0.2270 |
| BM25 hit@10 | 0.3366 |
| Query length avg chars | 693.16 |
| Document length avg chars | 40097.47 |

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
  task_name: NanoBrightPsychologyLong
  split_name: NanoBrightPsychologyLong
  source_task: Psychology StackExchange long-document
  source_dataset_id: xlangai/BRIGHT
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoBRIGHT/NanoBrightPsychologyLong.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 101
    documents: 509
    positive_qrels: 116
  positives_per_query:
    average: 1.1485148514851484
    min: 1
    median: 1
    max: 5
    multi_positive_queries: 11
    multi_positive_query_percent: 10.891089108910892
  text_stats_chars:
    query_mean: 693.1584158415842
    document_mean: 40097.47347740668
  bm25:
    ndcg_at_10: 0.22701053658053216
    hit_at_10: 0.33663366336633666
    source: dataset_bm25_column
  learning:
    original_train_split: unknown
    evaluation_split_origin: BRIGHT Psychology long-document evaluation split
    train_eval_overlap_audit: not_audited
    leakage_note: exclude NanoBRIGHT PsychologyLong queries and full cited source pages
    useful_training_data:
      - document-level psychology reference retrieval
      - cited-source retrieval from psychology forums
      - long-article QA with evidence grounding
    synthetic_data:
      document_generation: long psychology source pages with sections and research context
      question_generation: user-style questions about behavior, cognition, or measurement
      answerability: positive full document should contain the relevant construct or evidence
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
    - title: "BRIGHT: A Realistic and Challenging Benchmark for Reasoning-Intensive Retrieval"
      url: https://arxiv.org/abs/2407.12883
      year: 2024
      doi: 10.48550/arXiv.2407.12883
      is_paper: true
      source_confidence: definitive_paper_link
```
