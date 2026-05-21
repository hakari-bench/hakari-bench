# NanoMMTEB-v2 / ailastatutes

## Overview

`ailastatutes` is an English legal statute-retrieval task from AILA 2019. Each
query is a long Indian legal fact pattern, and the retriever must return the
statutory provisions that apply to the situation. The task tests whether a model
can connect legal facts, procedure, and remedies to governing statute text.

## Details

### What the Original Data Measures

[Overview of the FIRE 2019 AILA Track: Artificial Intelligence for Legal Assistance](https://ceur-ws.org/Vol-2517/T1-1.pdf)
describes a statute retrieval task where systems receive factual legal
scenarios and identify relevant statutes from a pool of frequently cited Indian
legal provisions. The [AILA Zenodo release](https://zenodo.org/records/4063986)
and [mteb/AILA_statutes](https://huggingface.co/datasets/mteb/AILA_statutes)
package the same retrieval problem for embedding evaluation.

### Observed Data Profile

The NanoMMTEB-v2 split has 50 long scenario queries, 82 statute documents, and
217 positive qrels. Queries average 3,038.42 characters, while statute documents
average 1,972.63 characters and usually combine a title with provision text.
Every query has multiple applicable statutes, averaging 4.34 positives per
query.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.1880
and hit@10 = 0.6600. Lexical retrieval is weak because the queries are factual
narratives and the relevant provisions may be implied by procedure or legal
effect rather than repeated by title.

### Training Data That May Help

Useful training data includes fact-to-statute retrieval pairs, statutory legal
entailment data, legal issue spotting, and hard negatives from adjacent Indian
criminal, evidence, constitutional, and procedure sections. Training should keep
the multi-positive structure because several provisions can apply to one
scenario.

### Synthetic Data Guidance

Generate realistic legal fact patterns and match them to several statute-like
provisions. Synthetic negatives should share legal vocabulary but fail on an
element such as jurisdiction, procedure, remedy, detention status, or evidentiary
rule. Do not seed generation from evaluation scenarios or positive statutes.

## Example Data

| Query | Positive document |
| --- | --- |
| Appellant calls in question legality of the judgment rendered by High Court confirming his conviction for offence and sentence of imprisonment for life as awarded by the learned Sessions Judge. Background facts as unfolded du ... [truncated 225 chars](3569 chars) | Title: Attempt to murder Desc: Whoever does any act with such intention or knowledge, and under such circumstances that, if he by that act caused death, he would be guilty or murder, shall be punished with imprisonment of eit ... [truncated 225 chars](1973 chars) |
| This appeal, by special leave, has been preferred against the judgment and order dated 23 February 2005 of the High Court (Aurangabad Bench), by which the appeal preferred by the appellants was dismissed and their conviction ... [truncated 225 chars](3266 chars) | Title: Dowry death Desc: (1) Where the death of a woman is caused by any burns or bodily injury or occurs otherwise than under normal circumstances within seven years of her marriage and it is shown that soon before her death ... [truncated 225 chars](856 chars) |
| The appellant before us was examined as prime witness in the trial of T.R. on the file of the Special Judge against the first respondent. The trial ended in conviction against the first respondent and when the appeal filed by ... [truncated 225 chars](2857 chars) | Title: Certain laws not to be affected by this Act Desc: Nothing in this Act shall affect the provisions of any Act for punishing mutiny and desertion of officers, soldiers, sailors or airmen in the service of the Government ... [truncated 225 chars](337 chars) |
| Whether sanction is required to initiate criminal proceedings in respect of offences is the question arising for consideration in these cases. The District Registrar lodged a complaint with the Inspector of Police, CBCID on 0 ... [truncated 225 chars](1664 chars) | Title: Punishment of criminal conspiracy Desc: (1) Whoever is a party to a criminal conspiracy to commit an offence punishable with death, 1 [imprisonment for life] or rigorous imprisonment for a term of two years or upwards, ... [truncated 225 chars](742 chars) |
| These appeals involve a pure question of law as to whether an award by which residue assets of a partnership firm are distributed amongst the partners on dissolution of the partnership firm requires registration. Briefly the ... [truncated 225 chars](1668 chars) | Title: Documents of which registration is compulsory Desc: (1) The following documents shall be registered, if the property to which they relate is situate in a district in which, and if they of have been executed on or after ... [truncated 225 chars](10961 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMMTEB-v2 |
| Backing dataset | NanoMMTEB-v2 |
| Task / split | ailastatutes |
| Hugging Face dataset | [hakari-bench/NanoMMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoMMTEB-v2) |
| Source dataset | [mteb/AILA_statutes](https://huggingface.co/datasets/mteb/AILA_statutes) |
| Language | en |
| Category | natural_language |
| Queries | 50 |
| Documents | 82 |
| Positive qrels | 217 |
| Avg positives / query | 4.34 |
| Positives per query (min / median / max) | 2 / 4.5 / 5 |
| Queries with multiple positives | 50 (100.00%) |
| BM25 nDCG@10 | 0.1880 |
| BM25 hit@10 | 0.6600 |
| Query length avg chars | 3038.42 |
| Document length avg chars | 1972.63 |

### Public Sources

- [Overview of the FIRE 2019 AILA Track: Artificial Intelligence for Legal Assistance](https://ceur-ws.org/Vol-2517/T1-1.pdf).
- [AILA 2019 Precedent & Statute Retrieval Task](https://zenodo.org/records/4063986).
- [mteb/AILA_statutes](https://huggingface.co/datasets/mteb/AILA_statutes).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoMMTEB-v2)
- Source dataset: [mteb/AILA_statutes](https://huggingface.co/datasets/mteb/AILA_statutes)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Overview of the FIRE 2019 AILA Track: Artificial Intelligence for Legal Assistance | 2019 | task paper | https://ceur-ws.org/Vol-2517/T1-1.pdf |
| AILA 2019 Precedent & Statute Retrieval Task | 2020 | dataset release | https://zenodo.org/records/4063986 |
| mteb/AILA_statutes | 2024 | dataset card | https://huggingface.co/datasets/mteb/AILA_statutes |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMMTEB-v2
  backing_dataset: NanoMMTEB-v2
  dataset_id: hakari-bench/NanoMMTEB-v2
  task_name: ailastatutes
  split_name: ailastatutes
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMMTEB-v2/ailastatutes.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 50
    documents: 82
    positive_qrels: 217
  positives_per_query:
    average: 4.34
    min: 2
    median: 4.5
    max: 5
    multi_positive_queries: 50
    multi_positive_query_percent: 100.0
  text_stats_chars:
    query_mean: 3038.42
    document_mean: 1972.6341463414635
  bm25:
    ndcg_at_10: 0.18801076191814994
    hit_at_10: 0.66
    source: dataset_bm25_column
  learning:
    original_train_split: available
    evaluation_split_origin: test
    train_eval_overlap_audit: not_audited
    leakage_note: do not train on this Nano split's scenarios, qrels, or positive statute text
    useful_training_data:
      - fact-to-statute retrieval pairs
      - statutory legal entailment data
      - legal issue spotting examples
      - adjacent statute hard negatives
    synthetic_data:
      document_generation: statute provisions with titles and clause-level legal conditions
      question_generation: long legal fact patterns requiring several applicable provisions
      answerability: each positive statute should govern at least one material issue in the scenario
    multi_positive_training: multi_positive_objective
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMMTEB-v2
    source_urls:
      - label: AILA 2019 paper
        url: https://ceur-ws.org/Vol-2517/T1-1.pdf
      - label: AILA Zenodo release
        url: https://zenodo.org/records/4063986
      - label: mteb/AILA_statutes
        url: https://huggingface.co/datasets/mteb/AILA_statutes
    source_notes: []
  references:
    - title: "Overview of the FIRE 2019 AILA Track: Artificial Intelligence for Legal Assistance"
      url: https://ceur-ws.org/Vol-2517/T1-1.pdf
      year: 2019
      is_paper: true
      source_confidence: definitive_paper_link
```
