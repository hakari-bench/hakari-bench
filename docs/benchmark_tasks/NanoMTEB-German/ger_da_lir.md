# NanoMTEB-German / ger_da_lir

## Overview

`ger_da_lir` is the GerDaLIR split in `NanoMTEB-German`. Queries are German
legal reasoning passages from court decisions, and documents are full German
case documents. The retriever must find precedent cases that are relevant to
the passage, usually because the original passage cited those cases.

## Details

### What the Original Data Measures

[GerDaLIR: A German Dataset for Legal Information Retrieval](https://aclanthology.org/2021.nllp-1.13/)
defines a German legal information retrieval benchmark from Open Legal Data
case documents. The paper describes a precedent-retrieval setup: passages that
refer to known cases become queries, and the referenced cases are labeled as
relevant. This differs from ordinary QA retrieval because the query is already a
legal argument fragment, not a short user question.

The GerDaLIR paper reports a large original collection with case documents,
passages, and relevance labels, and emphasizes that German legal IR had little
standardized benchmark coverage. It also notes that citations and statute
references are sanitized so systems should not simply exploit citation strings.
[MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316)
frames retrieval tasks as query-corpus relevance ranking, while
[MMTEB](https://arxiv.org/abs/2502.13595) later expands MTEB with many more
multilingual and language-specific tasks, including German retrieval coverage.

### Observed Data Profile

The Nano split has 200 queries, 10,000 documents, and 235 positive qrels. The
average query is long for a retrieval benchmark at 879.53 characters, and the
average document is very long at 18,071.48 characters. The examples are German
administrative, constitutional, and civil-procedure legal prose with placeholders
such as `[DATE]` and `[REF]`.

This is not a simple title lookup task. Queries often discuss legal standards,
procedural posture, or statutory interpretation, while the positive document is
a full case decision that may contain the relevant line of reasoning many
paragraphs later. About 14.5% of sampled queries have multiple positives, so
models should support more than one relevant precedent per legal passage.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.5444 and hit@10 = 0.6900. BM25 is useful because German legal decisions repeat
specialized terms, statutes, and procedural phrases, and 91 positives are ranked
first in the Nano sample.

The misses are still important. Some positives appear at ranks 8 or 9 even when
the topic is clear, and the median best rank is 2.0. Long case documents dilute
the matching signal, and many non-relevant decisions share generic legal
phrases. Strong models need legal-domain semantic matching and should preserve
statutory and procedural terminology without over-rewarding boilerplate.

### Training Data That May Help

The original GerDaLIR train split is the first source to inspect, subject to the
leaderboard's contamination policy. Other useful data includes non-overlapping
German court-decision citation pairs, legal passage-to-case pairs, German legal
semantic-search supervision, and hard negatives from same-court or same-statute
decisions. Training should exclude the upstream test split, Nano queries, Nano
qrels, and positive case documents likely to overlap with the evaluation set.

### Synthetic Data Guidance

For document-to-question generation, use non-evaluation German legal decisions
and create query passages that state a legal issue, procedural finding, or
argument without exposing raw citation labels. For joint generation, create
German legal case summaries and matching precedent-style query passages with
explicit grounding in the document's reasoning.

Synthetic data should retain legal entities, courts, dates, statute references,
procedural outcomes, and German legal phrasing. It should include multi-positive
training examples when several cases support the same issue, and it should not
use Nano evaluation passages or positive decisions as seeds.

## Example Data

| Query | Positive document |
| --- | --- |
| Die Entscheidung des Landgerichts, die Beklagte zur Erteilung der Auskunft durch Vorlage eines notariellen Nachlassverzeichnisses und nicht nur zu dessen Ergänzung zu verurteilen, begegnet ebenfalls keinen Bedenken. Wegen der ... [truncated 225 chars](1431 chars) | Tenor Die Rechtsbeschwerde gegen den Beschluss des 0. Familiensenats in Freiburg des Oberlandesgerichts Karlsruhe vom [DATE] wird auf Kosten des Antragsgegners zurückgewiesen. Von Rechts wegen Gründe I. Die beteiligten Ehegat ... [truncated 225 chars](11013 chars) |
| Der Vergütungsanspruch des Krankenhauses entsteht unmittelbar mit Inanspruchnahme der Leistung durch den Versicherten kraft Gesetzes, wenn die Versorgung wie hier in einem zugelassenen Krankenhaus erfolgt und iSv [REF] erford ... [truncated 225 chars](1165 chars) | Der Antragsteller wendet sich mit seinem Normenkontrollantrag gegen die am [DATE] bekannt gemachte städtebauliche Entwicklungssatzung der Antragsgegnerin für das Wohnbaugebiet „B.“ am südöstlichen Ortsrand der Stadt Dannenber ... [truncated 225 chars](32444 chars) |
| Die Auslegung der in §§ 0 Abs. 0, 0 NHundG enthaltenen Vorgaben ergibt, dass das erwähnte Erfordernis mit dem Sinn und Zweck der gesetzlichen Regelungen in Einklang steht. Zweck des niedersächsischen Gesetzes über das Halten ... [truncated 225 chars](1335 chars) | Die Beschwerde des Antragsgegners gegen den Beschluss des Verwaltungsgerichts, mit dem dieses die aufschiebende Wirkung der gegen den Bescheid des Antragsgegners vom [DATE] gerichteten Klage des Antragstellers wiederhergestel ... [truncated 225 chars](15391 chars) |
| Zwar ergibt sich aus [REF] das Erfordernis, dass die Begründung einen bestimmten Antrag enthalten muss. Das Fehlen eines ausdrücklich formulierten Antrags ist aber ausnahmsweise unschädlich, wenn sich das Rechtsschutzziel aus ... [truncated 225 chars](818 chars) | Tenor Die Beschwerde wird zurückgewiesen. Der Antragsteller trägt die Kosten des Beschwerdeverfahrens mit Ausnahme etwaiger außergerichtlicher Kosten der Beigeladenen, die diese selbst trägt. Der Streitwert wird auch für das ... [truncated 225 chars](16881 chars) |
| Die gerichtliche Kontrolle einer behördlichen Ermessensentscheidung beschränkt sich gemäß [REF] darauf, anhand der von der Behörde tatsächlich angestellten Erwägungen zu prüfen, ob die Verwaltung den ihr eingeräumten Ermessen ... [truncated 225 chars](667 chars) | Der Beklagte gewährte der Klägerin im [DATE] eine Zuwendung von bis zu 0 0 0 DM aus Mitteln der Finanzhilfen des Bundes für Investitionen zur Verbesserung der Verkehrsverhältnisse der Gemeinden als Anteilfinanzierung unter Zu ... [truncated 225 chars](14680 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-German |
| Backing dataset | NanoMTEB-German |
| Task / split | ger_da_lir |
| Hugging Face dataset | [hakari-bench/NanoMTEB-German](https://huggingface.co/datasets/hakari-bench/NanoMTEB-German) |
| Language | de |
| Category | natural_language |
| Queries | 200 |
| Documents | 10,000 |
| Positive qrels | 235 |
| Avg positives / query | 1.18 |
| Positives per query (min / median / max) | 1 / 1.0 / 4 |
| Queries with multiple positives | 29 (14.5%) |
| BM25 nDCG@10 | 0.5444 |
| BM25 hit@10 | 0.6900 |
| Query length avg chars | 879.53 |
| Document length avg chars | 18,071.48 |

### Public Sources

- [GerDaLIR: A German Dataset for Legal Information Retrieval](https://aclanthology.org/2021.nllp-1.13/); 2021; Marco Wrzalik and Dirk Krechel; DOI: `10.18653/v1/2021.nllp-1.13`.
- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316); 2023; Niklas Muennighoff, Nouamane Tazi, Loïc Magne, and Nils Reimers; DOI: `10.48550/arXiv.2210.07316`.
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595); 2025.
- [GerDaLIR GitHub repository](https://github.com/lavis-nlp/GerDaLIR).
- [mteb/GerDaLIR dataset card](https://huggingface.co/datasets/mteb/GerDaLIR).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMTEB-German](https://huggingface.co/datasets/hakari-bench/NanoMTEB-German)
- Source dataset: [mteb/GerDaLIR](https://huggingface.co/datasets/mteb/GerDaLIR)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| GerDaLIR: A German Dataset for Legal Information Retrieval | 2021 | paper | https://aclanthology.org/2021.nllp-1.13/ |
| MTEB: Massive Text Embedding Benchmark | 2023 | benchmark paper | https://arxiv.org/abs/2210.07316 |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | https://arxiv.org/abs/2502.13595 |
| mteb/GerDaLIR | 2025 | dataset card | https://huggingface.co/datasets/mteb/GerDaLIR |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMTEB-German
  backing_dataset: NanoMTEB-German
  dataset_id: hakari-bench/NanoMTEB-German
  task_name: ger_da_lir
  split_name: ger_da_lir
  language: de
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-German/ger_da_lir.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    paper_url: https://aclanthology.org/2021.nllp-1.13/
    additional_source_urls:
      - https://arxiv.org/abs/2210.07316
      - https://arxiv.org/abs/2502.13595
      - https://github.com/lavis-nlp/GerDaLIR
      - https://huggingface.co/datasets/mteb/GerDaLIR
  counts:
    queries: 200
    documents: 10000
    positive_qrels: 235
  positives_per_query:
    average: 1.175
    min: 1
    median: 1.0
    max: 4
    multi_positive_queries: 29
    multi_positive_query_percent: 14.5
  text_stats_chars:
    query_mean: 879.53
    document_mean: 18071.4799
  bm25:
    ndcg_at_10: 0.5444239126
    hit_at_10: 0.69
    source: dataset_bm25_column
  learning:
    original_train_split: available
    evaluation_split_origin: test
    train_eval_overlap_audit: not_audited
    leakage_note: exclude GerDaLIR test data, Nano queries, qrels, and positive case documents likely to overlap with the evaluation split
    useful_training_data:
      - non-overlapping GerDaLIR train examples
      - German court-decision citation retrieval pairs
      - German legal passage-to-case relevance pairs
      - same-statute and same-court hard negatives
    synthetic_data:
      document_generation: German legal decisions with courts, statutes, procedural posture, findings, and sanitized references
      question_generation: German legal argument passages that imply one or more relevant precedent cases
      answerability: positives should contain the precedent reasoning or case context needed by the query passage
    multi_positive_training: multi_positive_objective
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMTEB-German
    source_urls:
      - label: GerDaLIR paper
        url: https://aclanthology.org/2021.nllp-1.13/
      - label: GerDaLIR GitHub
        url: https://github.com/lavis-nlp/GerDaLIR
      - label: mteb/GerDaLIR
        url: https://huggingface.co/datasets/mteb/GerDaLIR
    source_notes: []
  references:
    - title: "GerDaLIR: A German Dataset for Legal Information Retrieval"
      url: https://aclanthology.org/2021.nllp-1.13/
      year: 2021
      doi: 10.18653/v1/2021.nllp-1.13
      is_paper: true
      source_confidence: definitive_paper_link
    - title: "MTEB: Massive Text Embedding Benchmark"
      url: https://arxiv.org/abs/2210.07316
      year: 2023
      doi: 10.48550/arXiv.2210.07316
      is_paper: true
      source_confidence: definitive_paper_link
```
