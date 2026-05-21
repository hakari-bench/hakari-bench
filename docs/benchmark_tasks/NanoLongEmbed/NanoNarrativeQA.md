# NanoLongEmbed / NanoNarrativeQA

## Overview

`NanoNarrativeQA` is the NarrativeQA long-document retrieval task inside
LongEmbed. Queries are short questions about stories, and documents are whole
books or movie scripts. The retriever must identify the narrative source that
contains the evidence needed to answer the question, often from hundreds of
thousands of characters rather than a compact passage.

## Details

### What the Original Data Measures

[The NarrativeQA Reading Comprehension Challenge](https://arxiv.org/abs/1712.07040)
introduces a reading-comprehension dataset where systems answer questions about
books and movie scripts. The paper emphasizes that questions and answers were
written from human summaries rather than from the full text, so many questions
target story-level events, motivations, and character relations rather than a
single copied sentence.

[LongEmbed: Extending Embedding Models for Long Context Retrieval](https://arxiv.org/abs/2404.12096)
adapts NarrativeQA into long-context retrieval by using questions as queries and
whole source documents as candidates. LongEmbed reports that the benchmark is
intended to test whether embedding models can process long documents whose
target information may be dispersed or far from the beginning.

### Observed Data Profile

The Nano split contains 200 English queries, 355 candidate documents, and 200
positive qrels. Every query has one positive document. Queries average 49.32
characters and look like direct story questions, while documents average
326,753 characters in repository metadata and include Project Gutenberg books
as well as scraped movie-script HTML.

The sampled positives include questions about `The Time Machine`, Tacitus,
`Fright Night`, Edith Wharton's `The Reef`, and `Hot Tub Time Machine`.
Several documents begin with license headers, web boilerplate, or script-site
markup before the narrative content, so a retriever that overweights early
tokens can miss the actual answer-bearing region.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.6910 and hit@10 = 0.7900. BM25 ranks 117 positives first and 158 positives in
the top 10, but the observed sample includes a positive at rank 16 for the
short query "Who killed Peter's parents?".

The score should be read as moderate lexical help rather than solved
retrieval. Character names and rare titles often identify the right story, but
questions about causes, relationships, and events can be too short or too
ambiguous for term matching alone.

### Training Data That May Help

Useful training data includes the official NarrativeQA train split, long-form
book and script question-answer retrieval pairs, and supervised pairs that map
story questions to full source texts or long chapters. Training should avoid
NarrativeQA test examples, Nano queries, qrels, and positive documents likely to
overlap with this evaluation.

Because the qrels are single-positive, standard question-to-document retrieval
training is appropriate. Long-document hard negatives from the same genre or
with overlapping character names are especially useful.

### Synthetic Data Guidance

For document-to-question generation, use non-evaluation books, plays, or movie
scripts and generate story questions about motives, deaths, family relations,
travel, actions, and event consequences. For joint generation, create long
narrative-style documents with repeated character mentions and questions whose
answer is grounded in a specific event.

Synthetic examples should preserve long-context noise: prefaces, scene
headers, license text, and distant evidence. Do not use Nano evaluation
questions or positive documents as seeds.

## Example Data

| Query | Positive document |
| --- | --- |
| Why hasn't Irena killed herself before? (39 chars) | ï»¿The Project Gutenberg EBook of When We Dead Awaken, by Henrik Ibsen This eBook is for the use of anyone anywhere at no cost and with almost no restrictions whatsoever. You may copy it, give it away or re-use it under the t ... [truncated 225 chars](131749 chars) |
| What does the bomber leave behind that reveals his identity? (60 chars) | <html> <head><title>Source Code Script at IMSDb.</title> <meta name="description" content="Source Code script at the Internet Movie Script Database."> <meta name="keywords" content="Source Code script, Source Code movie scrip ... [truncated 225 chars](219018 chars) |
| Whose hand does Grayes reluctantly take in marriage? (52 chars) | ï»¿The Project Gutenberg EBook of Desperate Remedies, by Thomas Hardy This eBook is for the use of anyone anywhere at no cost and with almost no restrictions whatsoever. You may copy it, give it away or re-use it under the te ... [truncated 225 chars](817284 chars) |
| Who did Plato not deter from writing according to Cicero in speaking to Romans? (79 chars) | ï»¿The Project Gutenberg EBook of Cicero's Brutus or History of Famous Orators; also His Orator, or Accomplished Speaker., by Cicero This eBook is for the use of anyone anywhere at no cost and with almost no restrictions what ... [truncated 225 chars](481075 chars) |
| What did Mrs. Lovett reveal to Todd? (36 chars) | <html> <head><title>Sweeney Todd: The Demon Barber of Fleet Street Script at IMSDb.</title> <meta name="description" content="Sweeney Todd: The Demon Barber of Fleet Street script at the Internet Movie Script Database."> <met ... [truncated 225 chars](252633 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoLongEmbed |
| Backing dataset | NanoLongEmbed |
| Task / split | NanoNarrativeQA |
| Hugging Face dataset | [hakari-bench/NanoLongEmbed](https://huggingface.co/datasets/hakari-bench/NanoLongEmbed) |
| Language | en |
| Category | natural_language |
| Queries | 200 |
| Documents | 355 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.6910 |
| BM25 hit@10 | 0.7900 |
| Query length avg chars | 49.32 |
| Document length avg chars | 326753.00 |

### Public Sources

- [The NarrativeQA Reading Comprehension Challenge](https://arxiv.org/abs/1712.07040); 2018; Tomas Kocisky et al.; DOI: `10.1162/tacl_a_00023`.
- [LongEmbed: Extending Embedding Models for Long Context Retrieval](https://arxiv.org/abs/2404.12096); 2024; Dawei Zhu et al.; DOI: `10.18653/v1/2024.emnlp-main.47`.
- [dwzhu/LongEmbed dataset card](https://huggingface.co/datasets/dwzhu/LongEmbed).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoLongEmbed](https://huggingface.co/datasets/hakari-bench/NanoLongEmbed)
- Source dataset: [dwzhu/LongEmbed](https://huggingface.co/datasets/dwzhu/LongEmbed)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| The NarrativeQA Reading Comprehension Challenge | 2018 | arXiv paper | https://arxiv.org/abs/1712.07040 |
| LongEmbed: Extending Embedding Models for Long Context Retrieval | 2024 | arXiv paper | https://arxiv.org/abs/2404.12096 |
| dwzhu/LongEmbed | 2024 | dataset card | https://huggingface.co/datasets/dwzhu/LongEmbed |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoLongEmbed
  backing_dataset: NanoLongEmbed
  dataset_id: hakari-bench/NanoLongEmbed
  task_name: NanoNarrativeQA
  split_name: NanoNarrativeQA
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoLongEmbed/NanoNarrativeQA.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 200
    documents: 355
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 49.315
    document_mean: 326752.9971830986
  bm25:
    ndcg_at_10: 0.6909643972
    hit_at_10: 0.79
    source: dataset_bm25_column
  learning:
    original_train_split: available
    evaluation_split_origin: test
    train_eval_overlap_audit: not_audited
    leakage_note: exclude NarrativeQA test data, Nano queries, qrels, and positive long documents likely to overlap with this evaluation
    useful_training_data:
      - official non-overlapping NarrativeQA train pairs
      - long-form book and screenplay question-document retrieval pairs
      - story-level QA over chapters or full narratives
      - hard negatives from similar stories or shared character names
    synthetic_data:
      document_generation: long narrative documents, books, plays, or screenplay-style texts with distant events and recurring character names
      question_generation: story questions about motives, deaths, relationships, travel, actions, and event consequences
      answerability: the relevant event should be explicitly grounded somewhere in the long document, not only implied by metadata
    multi_positive_training: single_positive_question_document_focus
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoLongEmbed
    source_urls:
      - label: NarrativeQA arXiv
        url: https://arxiv.org/abs/1712.07040
      - label: LongEmbed arXiv
        url: https://arxiv.org/abs/2404.12096
      - label: dwzhu/LongEmbed
        url: https://huggingface.co/datasets/dwzhu/LongEmbed
    source_notes: []
  references:
    - title: "The NarrativeQA Reading Comprehension Challenge"
      url: https://arxiv.org/abs/1712.07040
      year: 2018
      doi: 10.1162/tacl_a_00023
      is_paper: true
      source_confidence: definitive_paper_link
    - title: "LongEmbed: Extending Embedding Models for Long Context Retrieval"
      url: https://arxiv.org/abs/2404.12096
      year: 2024
      doi: 10.18653/v1/2024.emnlp-main.47
      is_paper: true
      source_confidence: definitive_paper_link
```
